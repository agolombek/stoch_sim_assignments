# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 11:42:07 2022

@author: arong
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from numba import njit
from time import time
import seaborn as sns
import pandas as pd
from scipy.stats import ttest_ind

mandelbrot_itr = np.logspace(1, 4, 4)

sample_sizes = np.linspace(50, 10000, 50)

methods = ["monte_carlo", "latin_hypercube", "orthogonal"]
colours = ['red', 'blue', 'green']
avg_area = []

for mandel_itr in mandelbrot_itr:
    c = 0
    for method in methods:
        df = pd.read_csv(method+'_'+str(mandel_itr)+'_iterations'+'.csv')
        df = df.iloc[: , 1:]
        
        df_cv = pd.read_csv('control_variates/'+method+'_control_variates_'+str(mandel_itr)+'_iterations'+'.csv')
        df_cv = df_cv.iloc[: , 1:]
        
        p_value = []
        
        for i in range(len(df.columns)):
            areas = df.iloc[:,i]
            areas_cv = df_cv.iloc[:,i]
            
            p = ttest_ind(areas, areas_cv, equal_var=False)[1]

            p_value.append(p)
        
        plt.plot(sample_sizes, p_value, color=colours[c],linestyle='--', label=method)
        
        c+=1
        
    filename = "welch_test_control_variates"+str(int(mandel_itr))+"Iterations"
    
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
    plt.savefig('graphs/welch_test_control_variates/'+filename+'.pdf')
    plt.show()