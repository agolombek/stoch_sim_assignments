# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 12:36:24 2022

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

mandelbrot_itr = np.logspace(1, 4, 4)

sample_sizes = np.linspace(50, 10000, 50)

methods = ["monte_carlo", "latin_hypercube", "orthogonal"]
colours = ['red', 'blue', 'green']
avg_area = []

for mandel_itr in mandelbrot_itr:
    c = 0

    df_mc = pd.read_csv(methods[0]+'_'+str(mandel_itr)+'_iterations'+'.csv')
    df_mc = df_mc.iloc[: , 1:]
    
    df_lh = pd.read_csv(methods[1]+'_'+str(mandel_itr)+'_iterations'+'.csv')
    df_lh = df_lh.iloc[: , 1:]
    
    df_o = pd.read_csv(methods[2]+'_'+str(mandel_itr)+'_iterations'+'.csv')
    df_o = df_o.iloc[: , 1:] 
    
    mc_vs_lh = []
    mc_vs_o = []
    lh_vs_o = []
    
    for i in range(len(df_mc.columns)):
        areas_mc = df_mc.iloc[:,i]
        areas_lh = df_lh.iloc[:,i]
        areas_o = df_o.iloc[:,i]
        
        mc_vs_lh.append(ttest_ind(areas_mc, areas_lh, equal_var=False)[1])
        mc_vs_o.append(ttest_ind(areas_mc, areas_o, equal_var=False)[1])
        lh_vs_o.append(ttest_ind(areas_lh, areas_o, equal_var=False)[1])

    
    plt.plot(sample_sizes, mc_vs_lh, color='fuchsia', label='monte carlo vs LH',linestyle='--')
    plt.plot(sample_sizes, mc_vs_o, color='lime', label='monte carlo vs orthogonal',linestyle='--')
    plt.plot(sample_sizes, lh_vs_o, color='orange', label='LH vs orthogonal',linestyle='--')
    
    filename = "welch_test_method_comparison"+str(int(mandel_itr))+"iterations"
    
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
    plt.savefig('graphs/welch_test_method_comparison/'+filename+'.pdf')
    plt.show()