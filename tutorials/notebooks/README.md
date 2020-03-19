# Running a Jupyter instance on Alan

This tutorial will guide you on how to setup your personalized Jupyter instance on the GPU cluster.

## Securing the notebook server

A first prerequisite is the notebook configuration file and can be generated as follows:
```bash
jupyter notebook --generate-config
```
This operation will write a new default config to your home directory.

Since the notebook server will be allocated on a compute node by Slurm, and is publicly available to everyone on the internal ULG network, it is good practice to secure your instance with a password.
```bash
jupyter notebook password
Enter password:  ****
Verify password: ****
```
You will only have to execute this once, as the password will be shared across all the Juypter servers you will allocate.

## Resource allocation
The resource allocation of your server can be controlled by changing the parameters in `jupyter.sbatch` and can be found at the top of the submission file.
```bash
#!/usr/bin/env bash
#
# Slurm arguments
#
#SBATCH --cpus-per-task=1        # Number of CPU cores to allocate
#SBATCH --export=ALL
#SBATCH --job-name "JUPYTER"
#SBATCH --mem-per-cpu=4000       # Allocated memory in MB per allocated CPU cores
#SBATCH --output "jupyter.log"   # Log-file (important!)
#SBATCH --gres=gpu:0             # Number of GPU's
#SBATCH --time="7-00:00:00"      # Max execution time
#

# Activate the Anaconda environment in which to execute the Jupyter instance.
conda activate default
```
Please make sure you change the Anaconda environment in the submission file. Currently it is set to `default` as shown above.

## Accessing the Juypter server
After the Jupyter instance has been scheduled by Slurm, i.e., it is in a running state:
```bash
TODO
```
The IP address and port allocated to your Jupyter instance can be extracted from the log file, as specified above.
```bash
TODO
```
The address in conjunction with the ealier defined password can be used to access the Jupyter instance. Assuming you are connected to the ULG internal network (e.g., through the VPN or some other service).

## Advanced options
Additional information on the configuration of your notebook server can be found [here](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html).
