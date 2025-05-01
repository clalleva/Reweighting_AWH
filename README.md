# Reweighting_AWH
This script helps in reweighting a variable of interest on an AWH run in which the collective variable (CV) selected to sample is different.
This script assumes you have a few files:

- a `pullx.xvg` file, which contains the timestep and value of the CV at that timestep, these are find in position `0` and `1` as printed out by `AWH` itself;
- a number of `awh_t*.xvg` files, corresponding to the output from the command `gmx awh -more`, with one file for each writing step of `AWH` as selected in the `.mdp`;
- a timeseries of the variable of interest, which will have a timestep corresponding to the save frequency for the `.xtc` file.
