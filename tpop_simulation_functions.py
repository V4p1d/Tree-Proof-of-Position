import os
import car_class as c
import environment_class as e
import tpop as t
import pandas as pd
import initialiser_functions as i
import numpy as np

def parser(simulation_number, probability_of_honest, probability_of_coerced, density, threshold, True_Positive, True_Negative, False_Positive, False_Negative, total_honest, total_dishonest):
    
    if total_honest:
        percent_true_positives = (True_Positive / total_honest) * 100
        percent_false_negatives = False_Negative / total_honest * 100

    else:
        percent_true_positives = 0
        percent_false_negatives = 100
    if total_dishonest:
        percent_true_negatives = (True_Negative / total_dishonest) * 100
        percent_false_positives = False_Positive / total_dishonest * 100
    else:
        percent_true_negatives = 100
        percent_false_positives = 0

    row_list = [simulation_number, probability_of_honest, probability_of_coerced, density, threshold,
    True_Positive, True_Negative, False_Positive, False_Negative, percent_true_positives, percent_true_negatives, 
    percent_false_positives, percent_false_negatives]

    return row_list

def tpop_simulator(number_of_simulations:int, number_of_cars:int, probability_of_honest:float, probability_of_coerced:float, depth:int, witness_number_per_depth:list, threshold:float):
    data = []

    import time 
    for simulation in range(number_of_simulations):
        environment = e.Environment([0,5], [0,5], 0.25)
        car_list = []
        for n in range(number_of_cars):
            car = i.car_gen(probability_of_honest, probability_of_coerced, environment)
            car_list.append(car)

        s=time.time()
        environment.environment_update(car_list, 0.01)
        env_update = time.time() - s
        density =  number_of_cars / (environment.width * environment.height)

        #Load the PoL algoritm and feed it the initialised objects
        s=time.time()

        for car in car_list:
            
            tree = t.Tree2(car, depth, witness_number_per_depth)
            car.algorithm_honesty_output = t.TPoP(tree, threshold, witness_number_per_depth)
        
        True_Positive, True_Negative, False_Positive, False_Negative, total_honest, total_dishonest = t.results(car_list)
        row = parser(simulation, probability_of_honest, probability_of_coerced, density, threshold, True_Positive, True_Negative, False_Positive, False_Negative, total_honest, total_dishonest)
        
        data.append(row)
        
        tpop_update=time.time() - s

        #print(f'Ran simulation {simulation+1}/{number_of_simulations}. Env update time: {env_update:.3g}. Tpop update time: {tpop_update:.3g}')
    simulation_df = pd.DataFrame(data, columns=['Simulation number', 'Probability of honest cars', 'Probability of coerced cars', 'Density', 'Threshold','Accuracy', 
    'True Positives', 'True Negatives', 'False Positives', 'False Negatives', 
    'Percent True Positives', 'Percent True Negatives', 'Percent False Positives','Percent False Negatives'])

    return simulation_df

def save_simulation(simulation_df, path, simulation_id):
    simulation_path = path + str(simulation_id) + '.txt'
    simulation_df.to_csv(simulation_path)

    return simulation_path

def make_directory(target_path):
    cwd = os.getcwd()
    path = cwd + target_path
    os.makedirs(path, exist_ok =True)
    return path

def full_csv(directory_path_string):
    """Given a directory pathfile with .txt files of simulation data, 
    loops through each one, reads them and creates one .csv file with 
    all the simulation data"""
    
    directory = os.fsencode(directory_path_string)
    print(directory)
    dfs = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        
        if filename.endswith('.txt'):
            simulation_path = directory_path_string + filename
            data = pd.read_csv(simulation_path)
            dfs.append(data)

    return pd.concat(dfs)

def full_csv_windows(directory_path_string):
    """Given a directory pathfile with .txt files of simulation data, 
    loops through each one, reads them and creates one .csv file with 
    all the simulation data"""
    
    directory = os.fsencode(directory_path_string)
    print(directory)
    dfs = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        
        if filename.endswith('.txt'):
            simulation_path = directory_path_string + '\\' + filename
            data = pd.read_csv(simulation_path)
            dfs.append(data)

    return pd.concat(dfs)
#test