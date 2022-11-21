# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 21:30:33 2022

@author: arong
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from numba import njit
from time import time
import seaborn as sns
import pandas as pd

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
        
        avg_area = []
        std_area = []
        avg_area_cv = []
        std_area_cv = []
        
        for i in range(len(df.columns)):
            areas = df.iloc[:,i]
            avg_area.append(np.mean(areas))
            std_area.append(np.std(areas))
            
            areas_cv = df_cv.iloc[:,i]
            avg_area_cv.append(np.mean(areas_cv))
            std_area_cv.append(np.std(areas_cv))
        
        avg_area = np.array(avg_area)
        std_area = np.array(std_area)
        
        avg_area_cv = np.array(avg_area_cv)
        std_area_cv = np.array(std_area_cv)
        
        plt.plot(sample_sizes, avg_area, color=colours[c], label=method)
        plt.fill_between(sample_sizes,  avg_area-std_area, avg_area+std_area, alpha=0.2, edgecolor=colours[c], facecolor=colours[c])
        
        plt.plot(sample_sizes, avg_area_cv, color='black', label='control variates')
        plt.fill_between(sample_sizes,  avg_area_cv-std_area_cv, avg_area_cv+std_area_cv, alpha=0.2, edgecolor='black', facecolor='black')
        
        c+=1
        filename = method+"_control_variates_"+str(int(mandel_itr))+" Iterations"
        
        tick_size = 22
        font = 25
        title_size =25
        
        plt.xscale('log')
        plt.title(str(int(mandel_itr))+" Iterations", fontsize=title_size)
        plt.xlabel('Sample Size', fontsize=font)
        plt.ylabel('Area', fontsize=font)
        plt.grid(axis='both')
        plt.xticks(fontsize=tick_size)
        plt.yticks(fontsize=tick_size)
        plt.tight_layout()
        plt.savefig('graphs/control_variates/'+filename+'.pdf')
        plt.show()