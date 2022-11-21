# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 16:21:05 2022

@author: arong
"""
import numpy as np
import matplotlib.pyplot as plt
import random
from numba import njit
from time import time
import seaborn as sns
import pandas as pd
from scipy.stats import ttest_ind, ttest_ind_from_stats

mandelbrot_itr = np.logspace(1, 4, 20)

# the refrence point is the point to which all others are compared in terms
# of the Welch Test. It must be between in the interval 0 to 19
refrence_point = 19

sample_sizes = [100, 625, 4225, 22500, 160000]

methods = ["monte_carlo", "latin_hypercube", "orthogonal"]
colours = ['red', 'blue', 'green']

for samp_size in sample_sizes:
    c = 0
    for method in methods:
        df = pd.read_csv(method+'_'+str(samp_size)+'_samples'+'.csv')
        df = df.iloc[: , 1:]
        
        p_values = []
        
        ref = df.iloc[:,refrence_point] 
        
        for i in range(len(df.columns)):
            areas = df.iloc[:,i]
            
            p = ttest_ind(ref, areas, equal_var=False)[1]

            p_values.append(p)
            
        
        plt.plot(mandelbrot_itr, p_values, color=colours[c], label=method,linestyle='--')
        
        c+=1
   
    filename = "welch_test_"+str(int(samp_size))+"Samples"
    
    tick_size = 16
    font = 16
    title_size = 16
    
    plt.xscale('log')
    plt.title(str(samp_size)+" Samples", fontsize=title_size)
    plt.xticks(fontsize=tick_size)
    plt.yticks(fontsize=tick_size)
    plt.xlabel('Mandelbrot Iterations', fontsize=font)
    plt.ylabel('p value', fontsize=font)
    plt.grid(axis='both')
    plt.legend(fontsize=font)
    plt.tight_layout()
    plt.savefig('graphs/welch_test/'+filename+'.pdf')
    plt.show()