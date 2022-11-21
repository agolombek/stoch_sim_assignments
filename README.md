# Investigating stochastic sampling techniques by estimating the area of the Mandelbrot set

This repository invesigates how different sampling techniques compare to one another in terms of estimating the area of the Mandelbrot set. Part of this will be to compare methods for given experiment parameters but also to investigate how the methods behave individually over varying experiment paramaters. The parameters which will be investigated are the sample size as well as the number of mandelbrot function iterations which are performed. For each set of parameters the experiment is repeated 50 times and the mean and varaince of the experiments will be used as a measure for the comparison. The test used to ensure statistical significance are Welch's t-test for equality of mean and Levene's test for equality of variance. The sampling methods tested are pure monte carlo sampling, latin hypercube sampling and orthogonal sampling. Additionally control variates are tested on all sampling methods to study their effectiveness in reducing variance.

## Motivation

The aim of this project is essentially to find ways to improve how samples are drawn stochastically from a sample space in a way that yield more accurate results with equal or lower computational expense. An increase can be a convergence towards the "real value" of some variable as well as a decrease in variance.

## Results

The results produced by all methods decrease significantly in variance as the sample size is increased. It can not be said conclusively that this convergence happens at different rates for different methods. Additionally it is shown that the area estimate approaches the "true value" for all methods when the number of Mandelbrot iterations are increased. Regrading this it was also shown that statistically significant changes occur over a larger range of increasing Mandelbrot function iterations for latin hypercube sampling compared to pure monte carlo sampling and an even larger range for orthogonal sampling. Comparing the individual methods it can also be concluded that orthogonal sampling produces results with statsically significant difference in variance compared to both other methods over a large range of experiment parameters while the variances of latin hypercube and pure monter carlo sampling become less distinguishable as the parameters of Mandelbrot iterations and sample size are increased. Finally no statistically signifcant imporvemnets could be measured when introducing control variates for any metho. However, the results indicate that a different variable with a higher covariance to the area approximation of the mandelbrot set could have this effect.

## Repository Overview
Below there will be a short overview of the repository, the files it contains and how the results can be recreated. Note that the experiments can be recreated precisley by running the code for the same parameter combinations and using the same experiment name as the random seed is generated using the first strings of the experiment name. 

### mandelbrot_functions.py
This file contains all the necessary function to reproduce the results of all the experiments which have been performed. 

### testing_sample_size.py
This file contains the experiment for testing the three sampling methods for a large range of sample sizes. This experiment is performed for 4 different orders of magnitude of mandelbrot function iterations.

The results of these experiments are saved as csv files into the folder sample_size_test. One file contains to the results of one method being tested for a large range of sample sizes given the number of mandelbrot iterations, the files are labeled as such. One column contains the 50 area value estimation for the given parameter combination.

### testing_mandelbrot_iterations.py
This file contains the experiment for testing the three sampling methods for a large range of mandlebrot function iterations. This experiment is performed for 5 different sample sizes which are spread out logarithmically.

The results of these experiments are saved as csv files into the folder iterations_test. One file contains to the results of one method being tested for a large range of mandelbrot iterations given the sample size, the files are labeled as such. One column contains the 50 area value estimation for the given parameter combination.

### testing_control_variates.py
This file contains the experiment for testing the three sampling methods with control variates for a large range of sample sizes. This experiment is performed for 4 different orders of magnitude of mandelbrot function iterations.

The results of these experiments are saved as csv files into the folder colntrol_variates within the folder sample_size_test. One file contains to the results of one method being tested for a large range of sample sizes given the number of mandelbrot iterations, the files are labeled as such. One column contains the 50 area value estimation for the given parameter combination.

### mandelbrot_picture.py
This file contains the code to produce a picture of the mandelbrot fractal over a grid with specified size. It is also possible to produce a fractal of a zoomed in part of the fractal.

### report.pdf
This file contains a report written on this topic with all the relevant results presented and explained.

### sample_size_test
This folder contains the results of the experiments performed in testing_sample_size.py and testing_control_variates.py. Furthermore it contains files to plot these results in an appropriate manner (figures stored in plots folder) and to both perform and visualize the signifcance testing (figures stored in correspong subfolder of plots). Below will be a breif outline of the python scripts within the folder.

**plotting_sample_size_results.py -** plots results of experiments with varying smaple size

**plotting_with_control_variates.py -** plots results experiments with varying smaple size and corresponding experiments using control variates

**welch_test.py -** performs and plots welch's test between a specified value in dataset to all other values of the same experiment (i.e. same method but different experiment parameters)

**levene_test.py -** performs and plots leven's test between a specified value in dataset to all other values of the same experiment (i.e. same method but different experiment parameters)

**welch_test_method_comparison.py -** performs and plots welch's test comparing all tested methods (i.e. same experiment parameters but across different methods)

**levene_test_method_comparison.py -** performs and plots levene's test comparing all tested methods (i.e. same experiment parameters but across different methods)

**welch_test_control_variates.py -**  performs and plots welch's test comparing results for equal experiment parameters of all methods with and without control variates 

**levene_test_control_variates.py -**  performs and plots levene's test comparing results for equal experiment parameters of all methods with and without control variates 

### iterations_test

This folder contains the results of the experimnets relating to varying mandelbrot function iterations performed using the file testing_mandelbrot_iterations.py. The structure and files contained is the same as for the folder detailed above with the exception that it does not include any results or graphs relating to control variates as these were not tested to increasing mandelbrot iterations as the reduction in variance rather than the convergence to the "real area" was to be tested.
