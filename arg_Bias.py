#########Initializing libraries###############

import time

## To work on data ##
import numpy as np
import pandas as pd
from MDAnalysis.analysis import distances
import scipy as sc


## To work on the trajectory ##
import MDAnalysis as mda
   
## For multiprocessing ##
import multiprocessing
from multiprocessing import Pool
from functools import partial

## Argument parsing ##
import argparse

#########Parsing the arguments###############
parser = argparse.ArgumentParser()

parser.add_argument("-v","--verbosity", help="increase output verbosity",
                    action="store_true")

parser.add_argument("--input", help = "Time series of variable of interest", default= "time_EC_IC.npy")
parser.add_argument("--pullx", help = "Time series of AWH CV", default=  "pullx.xvg")
parser.add_argument("--awh", help = "Folder in which to find the awh.xvg files", default=  "./")
parser.add_argument("--bpos", help = "Position of bias in awh.xvg", default=  2)
parser.add_argument("--folder", help = "Folder in which to save results", default=  "./")
parser.add_argument("-eb","--extract", help="extract bias",
                    action="store_true", default=False)
parser.add_argument("-cw","--calculate", help="calculate weigths from bias",
                    action="store_true", default=False)

args = parser.parse_args()

if args.verbosity:
    print("verbosity turned on")

#############################################
#########Opening files###############
if args.extract:
    a = np.load(args.input)[::25]
    if args.verbosity:
          print (f'Shape of variable input is {a.shape}\nusing first column as time')
    pullx=np.genfromtxt(args.pullx, skip_header=44, skip_footer=2)[::1000,:]
    if args.verbosity:
          print (f'Shape of pullx input is {pullx.shape}\nusing last column as CV value')

#############################################
#########Extracting bias###############

def extract_bias(ts_input,awh_input,pullx_input):
    a = np.load(ts_input)[::25]
    print (a.shape)
    pullx=np.genfromtxt(pullx_input, skip_header=44, skip_footer=2)[::1000,:]
    print (pullx.shape)
    bias=[]
    for idx, el in enumerate(a[:,0]):
        try:
	    #Open PMF#
            PMF=np.loadtxt(awh_input+'awh_t%s.xvg' %(int(el)) ,comments=['#','@','&'])
            all_mins = PMF[:,0]-pullx[idx,-1]
	    #Find closest value#
            here=np.where(all_mins**2==np.min(all_mins**2))
            if args.verbosity==True:
                print (f'Pullx {pullx[idx,-1]} closest PMF is {PMF[here[0],0]} with energy {PMF[here[0],1]} KJ/mol')
                print (f'For idx={idx} Pullx value is {pullx[idx,-1]}')
                print (f'PMF value at {PMF[here[0],0]} is {PMF[here[0],2]}')
	    #Append closest value#
            bias.append(PMF[here[0][0],int(args.bpos)]) #Using position bpos as bias of awh.xvg
            
        except:
            if args.verbosity==True:
                print (f'No {el} ps time in awh_results!!!')
            continue
    return np.asarray(bias)
if args.verbosity:
	print (f'Using position {args.bpos} as bias of awh.xvg')


#c_bias=extract_bias(args.input,args.awh,args.pullx)
if args.extract:
	c_bias=extract_bias(args.input,args.awh,args.pullx)#
else:
	print ('NOT extracting bias')
#############################################
#########Calculating weigths###############

def calculate_weigths(bias, T=303.15):
	weigths=[]

	R = sc.constants.R
	if args.verbosity:
		print (f'Calculating weigths with RT {R*T}, so T {T} K.')
	for i in bias:
		w=np.exp((-i/1000)/R*T) # diving i by 1000 to have bigger numbers
		weigths.append(w)
		if args.verbosity:
    			print (f'For bias {i} KJ/mol, weigth is {w}')
	weigths=np.asarray(weigths)
	return weigths/weigths.sum()

if args.calculate:
    if args.extract:
	    c_weigths=calculate_weigths(c_bias)
    else:
	    c_bias=np.load(args.folder+'calculated_bias.npy')	
	    c_weigths=calculate_weigths(c_bias)
else:
      print ('NOT calculating weigths')
#############################################
#########Saving bias###############
if args.extract:
      np.save(args.folder+'calculated_bias.npy', np.asarray(c_bias))
      if args.verbosity:
            print ('Saving file calculated_bias.npy')

#########Saving weigths###############
if args.calculate:
    np.save(args.folder+'calculated_weigths.npy', np.asarray(c_weigths))
    if args.verbosity:
      print ('Saving file calculated_weigths.npy')
