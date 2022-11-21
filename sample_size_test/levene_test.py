# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 09:47:01 2022

@author: arong
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from numba import njit
from time import time
import seaborn as sns
import pandas as pd
from scipy.stats import levene

mandelbrot_itr = np.logspace(1, 4, 4)

sample_sizes = np.linspace(50, 10000, 50)

# the refrence point is the point to which all others are compared in terms
# of the Welch Test. It must be between in the interval 0 to 49
refrence_point = 49

methods = ["monte_carlo", "latin_hypercube", "orthogonal"]
colours = ['red', 'blue', 'green']
avg_area = []

for mandel_itr in mandelbrot_itr:
    c = 0
    for method in methods:
        df = pd.read_csv(method+'_'+str(mandel_itr)+'_iterations'+'.csv')
        df = df.iloc[: , 1:]
        
        p_value = []
        
        ref = df.iloc[:,refrence_point]
        
        for i in range(len(df.columns)):
            areas = df.iloc[:,i]
            
            p = levene(ref, areas, center='mean')[1]

            p_value.append(p)
        
        plt.plot(sample_sizes, p_value, color=colours[c], label=method,linestyle='--')
        
        c+=1
        
    filename = "levene_test_"+str(int(mandel_itr))+"Iterations"
    
    tick_size = 16
    font = 16
    title_size =16
    
    plt.xscale('log')
    plt.title(str(int(mandel_itr))+" Iterations", fontsize=title_size)
    plt.xlabel('Sample Size', fontsize=font)
    plt.ylabel('p values', fontsize=font)
    plt.grid(axis='both')
    plt.legend(fontsize=12)
    plt.xticks(fontsize=tick_size)
    plt.yticks(fontsize=tick_size)
    plt.tight_layout()
    plt.savefig('graphs/levene_test/'+filename+'.pdf')
    plt.show()