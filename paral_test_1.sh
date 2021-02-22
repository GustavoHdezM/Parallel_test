#!/bin/bash
 
#SBATCH --nodes=1                   # the number of nodes you want to reserve
#SBATCH --ntasks-per-node=36        # the number of CPU cores per node
#SBATCH --partition=normal          # on which partition to submit the job
#SBATCH --time=1:00:00              # the max wallclock time (time limit your job will run)
 
#SBATCH --job-name=GHM_test         # the name of your job
#SBATCH --mail-type=FAIL             # receive an email when your job starts, finishes normally or is aborted
#SBATCH --mail-user=mejia@uni-muenster.de # your mail address

python shifts_sympt_wall.py

# python test_1_main.py

# LOAD MODULES HERE IF REQUIRED

# START THE APPLICATION
