#!/bin/bash

# set the number of nodes
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8

# set max wallclock time
#SBATCH --time=10:00:00

# set name of job
#SBATCH --job-name=team2Module05
#SBATCH --output=slurm.out
#SBATCH --error=slurm.err
#SBATCH --qos=long

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=steven.hussung@gmail.com

# run the application
python scatter.py 100
