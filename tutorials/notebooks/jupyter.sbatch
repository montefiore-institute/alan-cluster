#!/usr/bin/env bash
#
# Slurm arguments
#
#SBATCH --cpus-per-task=1        # Number of CPU cores to allocate
#SBATCH --export=ALL
#SBATCH --job-name "JUPYTER"
#SBATCH --mem-per-cpu=4000       # Memory to allocate in MB per allocated CPU core
#SBATCH --output "jupyter.log"   # Log-file (important!)
#SBATCH --gres=gpu:0             # Number of GPU's
#SBATCH --time="7-00:00:00"      # Max execution time
#

# Activate the Anaconda environment in which to execute the Jupyter instance.
conda init bash # Initialize shell
conda activate default # CHANGEME

jupyter lab --ip='*' --no-browser
