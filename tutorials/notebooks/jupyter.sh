#!/usr/bin/env bash
#
# Slurm arguments
#
#SBATCH --cpus-per-task=1
#SBATCH --export=ALL
#SBATCH --job-name "JUPYTER"
#SBATCH --mem-per-cpu=4000
#SBATCH --output "jupyter.log"
#SBATCH --gres=gpu:0
#SBATCH --time="7-00:00:00"
#

# Activate the Anaconda environment in which to execute the Jupyter instance.
conda activate TODO

jupyter lab --ip='*'
