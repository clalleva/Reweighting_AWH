#########Initializing libraries###############

import time

## To work on data ##
import numpy as np
import pandas as pd
from MDAnalysis.analysis import distances
import scipy as sc

## To plot ##
from matplotlib import cm 
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


## Argument parsing ##
import argparse

#########Parsing the arguments###############
parser = argparse.ArgumentParser()

parser.add_argument("-v","--verbosity", help="increase output verbosity",
                    action="store_true")

parser.add_argument("--input", help = "Time series of variable of interest", default= "time_EC_IC.npy")
parser.add_argument("-b", "--bias", help = "Bias", default= "calculated_bias.npy")
parser.add_argument("-w", "--weights", help = "weights", default="calculated_weigths.npy")
parser.add_argument("-c", "--column", help = "weights", default=1, type=int)
parser.add_argument("--bins", help = "Number of bins to use", default=25, type=int)


args = parser.parse_args()

if args.verbosity:
    print("Verbosity turned on")

#############################################
#########Opening files###############
a = np.load(args.input)[::25]
if args.verbosity:
    print (f'Shape of variable input is {a.shape}\nusing {args.column} column as variable')

bias=np.load(args.bias)
if args.verbosity:
    print (f'Shape of bias input is {bias.shape}')
weights=np.load(args.weights)
if args.verbosity:
    print (f'Shape of weights input is {weights.shape}')

#############################################
#########Check if the ###############
check_passed=False
if a.shape[0]==bias.shape and a.shape[0]==weights.shape:
      check_passed=True
else:
    if  a.shape[0]!=weights.shape[0]:
        print (f'Bias and variable have different shapes: {a.shape[0]} and {bias.shape}')
    if  a.shape[0]!=bias.shape[0]:
        print (f'Weights and variable have different shapes: {a.shape[0]} and {weights.shape}')
        
#############################################
#########Calculating probability and corrected probability###############

results_uncorrected=np.zeros(shape=(args.bins))
results_corrected=np.zeros(shape=(args.bins))

varint=a[:,1]
var_range=np.linspace(np.min(varint),np.max(varint),args.bins)

for j, l in enumerate(var_range[:-1]):
    here = np.where((varint>=l)&(varint<var_range[j+1]))
    results_uncorrected[j]+=len(here[0])
    results_corrected[j]+=weights[here[0]].sum()

results_uncorrected=np.asarray(results_uncorrected)
results_corrected=np.asarray(results_corrected)

plt.figure()
plt.plot(var_range,results_uncorrected/results_uncorrected.sum(), label='uncorrected')

plt.plot(var_range,results_corrected/results_corrected.sum(), label='corrected')
plt.legend()
plt.savefig('Probability')
