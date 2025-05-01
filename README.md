# Reweighting_AWH
These scripts help in reweighting a variable of interest on an AWH run in which the collective variable (CV) selected to sample is different.


## arg_Bias.py 

This script extract the bias applied in each timestep.
This script assumes you have a few files:

- a `pullx.xvg` file, which contains the timestep and value of the CV at that timestep, these are find in position `0` and `1` as printed out by `AWH` itself;
- a number of `awh_t*.xvg` files, corresponding to the output from the command `gmx awh -more`, with one file for each writing step of `AWH` as selected in the `.mdp`;
- a timeseries of the variable of interest, which will have a timestep corresponding to the save frequency for the `.xtc` file.

### Usage

python arg_Bias.py -v --input variable_timeseries.npy --pullx pullx_file.xvg --awh folder_containing_awh_files  --bpos int  --folder folder_to_save_in -eb Boolean -cw Boolean

`-v` for verbosity

`--bops` Position of bias in the files contained in `older_containing_awh_files`

`-eb` If you want to extract the bias values set to True

`-cw`  If you want to calculate the weights values set to True



#### Note 
This script assumes that the frequency of `AWH` writing is 25 times the frequency of the trajectory writing. You can modify this modifying the number in the lines `a = np.load(args.input)[::25]` and `a = np.load(ts_input)[::25]`.

## arg_prob.py 

This script calculates the corrected probability for the variable of interest, given the files for bias and weight values as obtained by  `arg_Bias.py` and the timeseries for the variable of interest.

### Usage

python arg_prob.py -v --input variable_timeseries.npy -b extracted_bias.npy -w  calculated_weigths.npy --bins int

`-v` for verbosity
`--bins` Number of bins to use

