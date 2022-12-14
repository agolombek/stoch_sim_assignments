# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 22:54:59 2022

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
This file contains the experiment to test the effect of increasing 
Mandelbrot function iterations on the accuracy of the estimation of the 
Mandelbrot set Area. The experiment is performed for a few values of sample
size but is kept constant for one experiment.

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

# for each value of sample size a new file will be created storing the 
# resulting area estimations for each point in mandelbrot_itr in a seperate
# column
sample_sizes = [100, 625, 4225, 22500, 160000]

# different number of mandelbrot iterations to test for sample size
mandelbrot_itr = np.logspace(1, 4, 20)

# set the seed accoring to the experiment name above
seed = ord(str(experiment_name)[0]) * ord(str(experiment_name[1]))

######################### Performing Experiment #############################

start = time()

for samp_size in sample_sizes:
    print(samp_size)
    area_data = []
    
    for mandel_itr in mandelbrot_itr:
    
        data = mandelbrot_set_area_estimate(samp_size, sampling_method, experiment_itr, int(mandel_itr), xmin, xmax, ymin, ymax, seed)
        area_data.append(data)
        
        seed += 1
        
    save_data = np.array(area_data).transpose()
    columns = [str(int(x)) for x in mandelbrot_itr]
    df = pd.DataFrame(save_data, columns = columns)
    df.to_csv('iterations_test/'+experiment_name+'_'+str(samp_size)+'_samples'+'.csv')
        
end = time()
runtime = ((end-start)/60)/60
print("run time = ",runtime," hours")
        
        
