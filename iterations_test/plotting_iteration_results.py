# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 10:28:25 2022

@author: arong
"""
import numpy as np
import matplotlib.pyplot as plt
import random
from numba import njit
from time import time
import seaborn as sns
import pandas as pd

mandelbrot_itr = np.logspace(1, 4, 20)
real_area = np.ones(20)*1.506484

sample_sizes = [100, 625, 4225, 22500, 160000]

methods = ["monte_carlo", "latin_hypercube", "orthogonal"]
colours = ['red', 'blue', 'green']

for samp_size in sample_sizes:
    c = 0
    for method in methods:
        df = pd.read_csv(method+'_'+str(samp_size)+'_samples'+'.csv')
        df = df.iloc[: , 1:]
        
        avg_area = []
        std_area = []
        
        for i in range(len(df.columns)):
            areas = df.iloc[:,i]
            avg_area.append(np.mean(areas))
            std_area.append(np.std(areas))
        
        avg_error = [np.abs(x-1.506484) for x in avg_area]
        std_error = np.std(np.array(avg_error))
        
        plt.errorbar(mandelbrot_itr, avg_area, yerr=std_area, color=colours[c], label=method, capsize=5)
        # plt.ylim((1, 2))

        # plt.errorbar(mandelbrot_itr, avg_error, yerr=std_error, color=colours[c], label=method, capsize=5)
        # plt.ylim((-0.02, 0.09))
        
        c+=1
   
    plt.plot(mandelbrot_itr, real_area, color='black', label="Best Estimate")
    filename = str(int(samp_size))+"Samples"
    
    tick_size = 16
    font = 16
    title_size = 16
    
    plt.xscale('log')
    plt.title(str(samp_size)+" Samples", fontsize=title_size)
    plt.xticks(fontsize=tick_size)
    plt.yticks(fontsize=tick_size)
    plt.xlabel('Mandelbrot Iterations', fontsize=font)
    plt.ylabel('Area', fontsize=font)
    plt.grid(axis='both')
    plt.legend(fontsize=font)
    plt.tight_layout()
    plt.savefig('graphs/'+filename+'.pdf')
    plt.show()
        
        