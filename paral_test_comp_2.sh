#!/bin/bash

#SBATCH --nodes=2                   # the number of nodes you want to reserve
#SBATCH --ntasks-per-node=36        # the number of CPU cores per node
#SBATCH --partition=normal          # on which partition to submit the job
#SBATCH --time=2:00:00              # the max wallclock time (time limit your job will run)

#SBATCH --job-name=GHM_com2            # the name of your job
#SBATCH --mail-type=FAIL             # receive an email when your job starts, finishes normally or is aborted
#SBATCH --mail-user=mejia@uni-muenster.de # your mail address

python parall_main_ED_2.py

# LOAD MODULES HERE IF REQUIRED

