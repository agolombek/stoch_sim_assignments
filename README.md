# Investigating stochastic sampling techniques by estimating the area of the Mandelbrot set

This repository invesigates how different sampling techniques compare to one another in terms of estimating the area of the Mandelbrot set. Part of this will be to compare methods for given experiment parameters but also to investigate how the methods behave individually over varying experiment paramaters. The parameters which will be investigated are the sample size as well as the number of mandelbrot function iterations which are performed. For each set of parameters the experiment is repeated 50 times and the mean and varaince of the experiments will be used as a measure for the comparison. The test used to ensure statistical significance are Welch's t-test for equality of mean and Levene's test for equality of variance. The sampling methods tested are pure monte carlo sampling, latin hypercube sampling and orthogonal sampling. Additionally control variates are tested on all sampling methods to study their effectiveness in reducing variance.

## Motivation 


## Results

The results produced by all methods decrease significantly in variance as the sample size is increased. It can not be said conclusively that this convergence happens at different rates for different methods. Additionally it is shown that the area estimate approaches the "true value" for all methods when the number of Mandelbrot iterations are increased. Regrading this it was also shown that statistically significant changes occur over a larger range of increasing Mandelbrot function iterations for latin hypercube sampling compared to pure monte carlo sampling and an even larger range for orthogonal sampling. Comparing the individual methods it can also be concluded that orthogonal sampling produces results with statsically significant difference in variance compared to both other methods over a large range of experiment parameters while the variances of latin hypercube and pure monter carlo sampling become less distinguishable as the parameters of Mandelbrot iterations and sample size are increased. Finally no statistically signifcant imporvemnets could be measured when introducing control variates for any metho. However, the results indicate that a different variable with a higher covariance to the area approximation of the mandelbrot set could have this effect.

## Instructions
