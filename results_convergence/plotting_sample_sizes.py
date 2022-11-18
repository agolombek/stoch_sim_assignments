# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:53:03 2022

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


    
for i in range(len(mandelbrot_itr)):
    
    c = 0
    for method in methods:
    
        avg_area = []
        std_area = []
    
        
        for samp_size in sample_sizes:
            
            df = pd.read_csv(method+'_'+str(samp_size)+'_samples'+'.csv')
            df = df.iloc[: , 1:]
            
            areas = df.iloc[:,i]
            tested_areas = []
            
            for j in range(int((len(areas)+1)/20)):
                tested_areas.append(areas[j*20])
            
            avg_area.append(np.mean(tested_areas))
            std_area.append(np.std(tested_areas))
        
        avg_error = [np.abs(x-1.506484) for x in avg_area]
        std_error = np.std(np.array(avg_error))
        
        # plt.errorbar(sample_sizes, avg_area, yerr=std_area, color=colours[c], label=method, capsize=5)
        
        # plt.ylim((1, 2))
    
        plt.errorbar(sample_sizes, avg_error, yerr=std_error, color=colours[c], label=method, capsize=5)
        # plt.ylim((-0.02, 0.09))
        
        c+=1
        
    # plt.plot(mandelbrot_itr, real_area, color='black', label="Best Estimate")    
    plt.xscale('log')
    plt.title(str(int(mandelbrot_itr[i]))+" Mandelbrot Iterations")
    plt.xlabel('Sample Size', fontsize=13)
    plt.ylabel('Area', fontsize=13)
    plt.grid(axis='both')
    plt.legend()
    plt.show()