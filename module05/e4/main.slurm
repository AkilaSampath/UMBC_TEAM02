#!/bin/bash

# set name of job and outputs
#SBATCH --job-name=team2Module05
#SBATCH --output=slurm.out
#SBATCH --error=slurm.err

# set max wallclock time
#SBATCH --qos=long
#SBATCH --time=00:05:00

# set the number of nodes
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=steven.hussung@gmail.com

# run the application
python scatter.py 10000
