#!/usr/bin/env bash
#
# Slurm arguments
#
#SBATCH --job-name=mnist            # Name of the job 
#SBATCH --export=ALL                # Export all environment variables
#SBATCH --output=mnist-output.log   # Log-file (important!)
#SBATCH --cpus-per-task=2           # Number of CPU cores to allocate
#SBATCH --mem-per-cpu=4G            # Memory to allocate per allocated CPU core
#SBATCH --gres=gpu:1                # Number of GPU's
#SBATCH --time=1:00:00              # Max execution time
#

# Activate your Anaconda environment
source activate sandbox         # CHANGEME

# Run your Python script
cd /home/glouppe/sandbox/mnist  # CHANGEME
python mnist.py
