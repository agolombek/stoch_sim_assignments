# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 17:25:00 2021

@author: arong
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from numba import njit
from time import time
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.ticker import MaxNLocator
from matplotlib import cm


######################### MANDELBROT ITERATIONS ##############################

@njit
def mandelbrot_test(points, iterations):
    """
    This function analyzes a range of values for whether they are part of the 
    mandelbrot set or not.
    --------------------------------------------------------------------------
    The first argument is the x and y values of the points to be tested in the 
    form of a n by 2 matrix with n being the number of points to be tested.
    
    The iterations argument is an integer value representing the number of 
    times a point is iterated over before it is concluded whether it is in the
    mandelbrot set or not.
    --------------------------------------------------------------------------
    The fuction returns an array of 0 and 1 with a 1 indicating that the point 
    at that index is part of the mandelbrot set, while a 0 indicates that it 
    diverged and is thus not part of the set.
    """
    # check how many points are being parsed and create an array containing 
    # zeros in the corresponding size
    number_of_points = np.shape(points)[0]
    solution = np.zeros(number_of_points)
    
    for i in range(number_of_points):
        z = 0
        n = 0
        
        while abs(z) <= 2 and n < iterations:
            z = z*z + complex(points[i][0], points[i][1])
            n += 1

        if n == iterations:
            solution[i] = 1
  
    return solution

@njit
def circle_test(points, circle_radius):
    """
    This function checks whether a set of points is inside or outside a circle
    centered at (-0.25, 0) with a given radius.
    --------------------------------------------------------------------------
    The first argument is the x and y values of the points to be tested in the 
    form of a n by 2 matrix with n being the number of points to be tested.
    
    The second argument is the radius of the circle.
    --------------------------------------------------------------------------
    The fuction returns an array of 0 and 1 with a 1 indicating that the point 
    at that index is inside the circle, while a 0 indicates that it is outside.
    """
    # check how many points are being parsed and create an array containing 
    # zeros in the corresponding size
    number_of_points = np.shape(points)[0]
    solution = np.zeros(number_of_points)
    
    for i in range(number_of_points):
        x = points[i][0] 
        y = points[i][1]
        radius = np.sqrt(x**2 + y**2)
        if radius <= circle_radius:
            solution[i] = 1
            
    return solution
    
######################### SAMPLING METHODS ###################################

@njit
def monte_carlo_sampling(samp_size_sqrt, seed):
    """
    This function provides sample points for half open interval 
    x = [0, 1), y = [0, 1) using the random sampling method.
    --------------------------------------------------------------------------
    The function arguments are the root of number of points to be sampled 
    labeled as samp_size_sqrt and the random seed used.
    --------------------------------------------------------------------------
    The function returns a n by 2 matrix with n being the number of points 
    to be tested, containing the x and y values in colum 1 and 2 respectively.  
    """
    np.random.seed(seed)
    
    samp_size = int(samp_size_sqrt**2)
    sample_space = np.zeros((samp_size, 2))
    for i in range(samp_size):
        sample_space[i, 0] = np.random.uniform(0,1)
        sample_space[i, 1] = np.random.uniform(0,1)
    return sample_space

@njit
def latin_hypercube_sampling(samp_size_sqrt, seed):
    """
    This function provides sample points for half open interval 
    x = [0, 1), y = [0, 1) using the latin hypercube sampling 
    method.
    --------------------------------------------------------------------------
    The function arguments are the root of number of points to be sampled 
    labeled as samp_size_sqrt and the random seed used.
    --------------------------------------------------------------------------
    The function returns a n by 2 matrix with n being the number of points 
    to be tested, containing the x and y values in colum 1 and 2 respectively.  
    """
    np.random.seed(seed)
    
    samp_size = int(samp_size_sqrt**2)
    sample_space = np.zeros((samp_size, 2))
    perm1 = np.random.permutation(samp_size)
    perm2 = np.random.permutation(samp_size)
    for i in range(samp_size):
        sample_space[i, 0] = ((np.random.random()+perm1[i])/samp_size)
        sample_space[i, 1] = ((np.random.random()+perm2[i])/samp_size)
    return sample_space

@njit
def orthogonal_sampling(major, seed):
    """
    This function provides sample points for half open interval 
    x = [0, 1), y = [0, 1) using orthogonal sampling.
    --------------------------------------------------------------------------
    The function arguments are the root of number of points to be sampled 
    labeled as major and the random seed used.
    --------------------------------------------------------------------------
    The function returns a n by 2 matrix with n being the number of points 
    to be tested, containing the x and y values in colum 1 and 2 respectively.  
    """
    np.random.seed(seed)
    
    #initialising the final array
    major = int(major)
    sample_space = np.zeros((int(major*major),2))
    #x values of the points
    col1 = np.zeros((int(major*major)))
    col = np.zeros(major)
    for i in range(1,major+1):
        start_idx = (i-1)*major
        stop_idx = (i-1)*major+major
        col[0:major] = 0
        for j in range(1,major+1):
            col[j-1] = (i-1)*major+j
        col1[start_idx:stop_idx] = np.random.permutation(col)


    #y values of the points
    col2 = np.zeros((int(major*major)))
    # changing the elements of the second column
    for j in range(major):
        for i in range(major):
            col2[i+major*j]=i+1
    for i in range(1,major+1):
        col[0:major] = 0
        for j in range(1,major+1):
            col[j-1] = (i-1)*major+j
        change = np.random.permutation(col)
        for j in range(major):
            col2[i-1+j*major] = change[j]
    for i in range(major*major):
        sample_space[i,0] = ((np.random.random()+col1[i]-1)/major**2)
        sample_space[i,1] = ((np.random.random()+col2[i]-1)/major**2)

    return sample_space

@njit
def convert_sample_space(sample, xmin, xmax, ymin, ymax):
    """
    This function converts a set of points generated on the half open interval 
    x = [0, 1), y = [0, 1) to the desired sample space interval 
    x = [xmin, xmax), y = [ymin, ymax).
    --------------------------------------------------------------------------
    The first argument is the x and y values of the sample points to be tested 
    in the form of a n by 2 matrix with n being the number of points to be 
    tested. The remaining arguments are the limits of the sample space in both
    x and y direction
    --------------------------------------------------------------------------
    The function returns a n by 2 matrix with the sample points in the new 
    transformed interval.
    """
    
    x_magnitude = xmax - xmin
    y_magnitude = ymax - ymin
    
    sample[:,0] = sample[:,0] * x_magnitude + xmin
    sample[:,1] = sample[:,1] * y_magnitude + ymin
    
    return sample

######################### Preforming Experiments #############################

@njit
def mandelbrot_set_area_estimate(sample_size, sampling_method, experiment_itr, mandelbrot_itr, xmin, xmax, ymin, ymax, seed):
    """
    This function estimates the area of the madelbrot set given specific 
    parameters and repeats the experiment a given number of times.
    --------------------------------------------------------------------------
    The argumnets of this function are firstly the sample size and secondly a 
    function determining by which method the sample si to be generated.
    
    The third input is the number of times the experiment is to be repeated 
    with a different seed. The fourth input is the number of times each point
    in the sample is tested for divergence according to the criteria of the
    mandelbrot set.
    
    xmin, xmax, ymin and ymax determine the size of the sample space where 
    points are to be sampled and the final input seed is the seed for the
    first experiment.
    --------------------------------------------------------------------------
    The function returns an array with Area estimates in the size of the third
    input i.e. experiment iterations.
    """
    
    data_points = np.zeros(experiment_itr)
    
    for i in range(experiment_itr):
        # Create sample points and adapt to size of area to be sampled
        samp_size_sqrt = np.sqrt(sample_size)
        sample = sampling_method(samp_size_sqrt, seed)
        sample_adapted = convert_sample_space(sample, xmin, xmax, ymin, ymax)
        
        # Test all sample points for convergence
        solution = mandelbrot_test(sample_adapted, mandelbrot_itr)
        
        # Calculate Area 
        x_magnitude = xmax - xmin
        y_magnitude = ymax - ymin
        
        A = np.mean(solution)*(x_magnitude*y_magnitude)
        
        # Place in global solution array
        data_points[i] = A
        seed += 1
    
    return data_points
        
    

@njit
def covariate_mandelbrot_area_estimation(sample_size, sampling_method, experiment_itr, mandelbrot_itr, xmin, xmax, ymin, ymax, seed, circle_radius):
    """
    This function estimates the area of the madelbrot set given specific 
    parameters and repeats the experiment a given number of times. It makes
    use of control variates, specifically a circle centered at (-0.25,0) with 
    a given radius.
    --------------------------------------------------------------------------
    The argumnets of this function are firstly the sample size and secondly a 
    function determining by which method the sample si to be generated.
    
    The third input is the number of times the experiment is to be repeated 
    with a different seed. The fourth input is the number of times each point
    in the sample is tested for divergence according to the criteria of the
    mandelbrot set.
    
    xmin, xmax, ymin and ymax determine the size of the sample space where 
    points are to be sampled and the final input seed is the seed for the
    first experiment.
    
    The final input circle_radius is the radius of the circle used as a control
    variate.
    --------------------------------------------------------------------------
    The function returns an array with Area estimates in the size of the third
    input i.e. experiment iterations.
    """
    mandelbrot_areas = np.zeros(experiment_itr)
    circle_areas = np.zeros(experiment_itr)
    
    for i in range(experiment_itr):
        # Create sample points and adapt to size of area to be sampled
        samp_size_sqrt = np.sqrt(sample_size)
        sample = sampling_method(samp_size_sqrt, seed)
        sample_adapted = convert_sample_space(sample, xmin, xmax, ymin, ymax)
        
        # Test all sample points for convergence
        solution_mandelbrot = mandelbrot_test(sample_adapted, mandelbrot_itr)
        solution_circle = circle_test(sample_adapted, circle_radius)
        
        # Calculate Area 
        x_magnitude = xmax - xmin
        y_magnitude = ymax - ymin
        
        area_mandelbrot = np.mean(solution_mandelbrot)*(x_magnitude*y_magnitude)
        area_circle = np.mean(solution_circle)*(x_magnitude*y_magnitude)
        
        # Place in global solution array
        mandelbrot_areas[i] = area_mandelbrot
        circle_areas[i] = area_circle
        seed += 1
    
    # compute variable Z
    expected_circle_area = (circle_radius**2)*np.pi
    var_x = np.var(mandelbrot_areas)
    var_y = np.var(circle_areas)
    covvar_xy = np.cov(mandelbrot_areas, circle_areas)[0][1]
    
    c = var_x - covvar_xy/var_y
    
    Z = mandelbrot_areas + c*(circle_areas-expected_circle_area)
    
    return Z







