# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 14:15:27 2022

@author: arong
"""
import numpy as np
import matplotlib.pyplot as plt
import random
from numba import njit
from time import time
import seaborn as sns
from mandelbrot_functions import *
import pandas as pd

"""
This file contains the experiment to test the effect of using control 
variates on the accuracy of the estimation of the Mandelbrot set Area. The
experiment is performed for a few values of Mandelbrot function iterations 
but is kept constant for one experiment while the sample size is varied.

Uncomment one of the sampling methods below along with its corresponding 
experiment name so that the file is saved accordingly
"""

######################### Experiment Set-up #################################

sampling_method = monte_carlo_sampling
experiment_name = "monte_carlo"

# sampling_method = latin_hypercube_sampling
# experiment_name = "latin_hypercube"

# sampling_method = orthogonal_sampling
# experiment_name = "orthogonal"

######################### Experiment Parameters ##############################

# number of times a simulation is repeated for a given combination of 
# parameters with a different seed
experiment_itr = 50

# range of values in which sample points are taken
xmin = -2
xmax = 0.75
ymin = -1.25
ymax = 1.25

# for each value of mandelbrot iterations a new file will be created storing 
# the resulting area estimations for each point in sample_sizes in a seperate
# column
mandelbrot_itr = np.logspace(1, 4, 4)

# different sample sizes to test for each number of mandelbrot iterations
sample_sizes = np.linspace(50, 10000, 50)
sample_sizes = [int(np.sqrt(x))**2 for x in list(sample_sizes)]
sample_sizes = np.array(sample_sizes)

# set the seed accoring to the experiment name above
seed = ord(str(experiment_name)[0]) + ord(str(experiment_name[1]))

######################### Performing Experiment #############################

start = time()

for mandel_itr in mandelbrot_itr:
    
    area_data = []
    
    for samp_size in sample_sizes:
    
        data = covariate_mandelbrot_area_estimation(samp_size, sampling_method, experiment_itr, int(mandel_itr), xmin, xmax, ymin, ymax, seed, 0.5)
        area_data.append(data)
        
        seed += 1
        
    save_data = np.array(area_data).transpose()
    columns = [str(int(x)) for x in sample_sizes]
    df = pd.DataFrame(save_data, columns = columns)
    df.to_csv('sample_size_test/control_variates/'+experiment_name+'_control_variates_'+str(mandel_itr)+'_iterations'+'.csv')
        
end = time()
runtime = ((end-start)/60)/60
print("run time = ",runtime," hours")
    
