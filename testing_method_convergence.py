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

sampling_method = monte_carlo_sampling
experiment_name = "monte_carlo"

# sampling_method = latin_hypercube_sampling
# experiment_name = "latin_hypercube"

# sampling_method = orthogonal_sampling
# experiment_name = "orthogonal"

experiment_itr = 50

xmin = -2
xmax = 0.75
ymin = -1.25
ymax = 1.25

mandelbrot_itr = np.logspace(2, 5, 15)
sample_sizes = [100, 625, 4225, 22500, 160000, 1000000]

seed = ord(str(experiment_name)[0]) * ord(str(experiment_name[1]))

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
    df.to_csv('results/'+experiment_name+'_'+str(samp_size)+'_samples'+'.csv')
        
end = time()
runtime = ((end-start)/60)/60
print("run time = ",runtime," hours")
        
        
