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


sampling_method = monte_carlo_sampling
experiment_name = "monte_carlo"

# sampling_method = latin_hypercube_sampling
# experiment_name = "latin_hypercube"

# sampling_method = orthogonal_sampling
# experiment_name = "orthogonal"

experiment_itr = 50

radii = np.linspace(0.1, 0.5, 4)

xmin = -2
xmax = 0.75
ymin = -1.25
ymax = 1.25

mandelbrot_itr = np.logspace(2, 5, 15)
sample_size = 22500

seed = ord(str(experiment_name)[0]) * ord(str(experiment_name[1]))

start = time()

area_data = []

for circle_radius in radii:

    data = covariate_mandelbrot_area_estimation(sample_size, sampling_method, experiment_itr, mandelbrot_itr, xmin, xmax, ymin, ymax, seed, circle_radius)
    area_data.append(data)
    
    seed += 1
    
save_data = np.array(area_data).transpose()
columns = [str(x) for x in radii]
df = pd.DataFrame(save_data, columns = columns)
df.to_csv('results/'+'radius_testing'+experiment_name+'.csv')
        
end = time()
runtime = ((end-start)/60)/60
print("run time = ",runtime," hours")