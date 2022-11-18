# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:10:04 2022

@author: arong
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from numba import njit
from time import time
import seaborn as sns
import pandas as pd

mandelbrot_itr = np.logspace(2, 5, 15)
real_area = np.ones(15)*1.506484

sample_sizes = [100, 625, 4225, 22500, 160000, 1000000]

methods = ["monte_carlo", "latin_hypercube", "orthogonal"]
colours = ['red', 'blue', 'green']
avg_area = []

bootstrapping_iterations = 100

for samp_size in sample_sizes:
    c = 0
    for method in methods:
        df = pd.read_csv(method+'_'+str(samp_size)+'_samples'+'.csv')
        df = df.iloc[: , 1:]
        
        avg_area = []
        std_area = []
        
        for i in range(len(df.columns)):
            areas = df.iloc[:,i]
            tested_areas = []
            
            for j in range(int((len(areas)+1)/20)):
                tested_areas.append(areas[j*20])
            
            bootstrapped_areas = tested_areas
            for boot in range(bootstrapping_iterations):
                bootstrapped_areas.append(np.random.choice(tested_areas))
            
            avg_area.append(np.mean(bootstrapped_areas))
            std_area.append(np.std(bootstrapped_areas))
        
        avg_error = [np.abs(x-1.506484) for x in avg_area]
        std_error = np.std(np.array(avg_error))
        
        plt.errorbar(mandelbrot_itr, avg_area, yerr=std_area, color=colours[c], label=method, capsize=5)
        
        # plt.ylim((1, 2))

        # plt.errorbar(mandelbrot_itr, avg_error, yerr=std_error, color=colours[c], label=method, capsize=5)
        # plt.ylim((-0.02, 0.09))
        
        c+=1
        
    plt.plot(mandelbrot_itr, real_area, color='black', label="Best Estimate")    
    plt.xscale('log')
    plt.title(str(samp_size)+" Samples")
    plt.xlabel('Mandelbrot Iterations', fontsize=13)
    plt.ylabel('Area', fontsize=13)
    plt.grid(axis='both')
    plt.legend()
    plt.show()