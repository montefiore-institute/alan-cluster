# Running a Jupyter instance on Alan

This tutorial will guide you on how to setup your personalized Jupyter instance on the GPU cluster. This document assumes you have an Anaconda environment configured with Jupyter Lab.
```console
you@alan-master:~ $ conda activate myenvironment
you@alan-master:~ $ conda install jupyterlab
```

**Attention:** This document only provides a setup to use Jupyter *interactively*. If you simply would like to execute notebooks to summarize results, please have a look at [Papermill](https://github.com/nteract/papermill).

**Use the allocated resources responsibly, kill your Jupyter instance if you are ready of if it is unused!**

## Securing the notebook server

A first prerequisite is the notebook configuration file and can be generated as follows:
```console
you@alan-master:~ $ jupyter notebook --generate-config
```
This operation will write a new default config to your home directory.

Since the notebook server will be allocated on a compute node by Slurm, and is publicly available to everyone on the internal ULG network, it is good practice to secure your instance with a password.
```console
you@alan-master:~ $ jupyter notebook password
Enter password:  ****
Verify password: ****
```
You will only have to execute this once, as the password will be shared across all the Juypter servers you will allocate.

## Resource allocation
The default Slurm submission script can be obtained by:
```console
you@alan-master:~ $ wget https://raw.githubusercontent.com/montefiore-ai/alan-cluster/master/tutorials/notebooks/jupyter.sbatch
```
The resource allocation of your server can be controlled by changing the parameters in `jupyter.sbatch` and can be found at the top of the submission file.
```bash
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
conda activate myenvironment     # CHANGEME

# Start Jupyter Lab
jupyter lab --ip='*' --no-browser
```
Please make sure you change the Anaconda environment in the submission file. By default is set to `myenvironment`. After your resources have been properly configured, the Jupyter instance is ready to be scheduled by Slurm:
```console
you@alan-master:~ $ sbatch jupyter.sbatch
Submitted batch job 1333969
```

## Accessing the Juypter server

After the Jupyter instance has been scheduled by Slurm, i.e., it is in a running state:
```console
you@alan-master:~ $ squeue | grep you | grep JUPYTER
```
The IP address and port allocated to your Jupyter instance can be extracted from the log file, as specified above.
```console
you@alan-master:~ $ cat jupyter.log | grep compute
[I 17:00:28.508 LabApp] http://compute-05:8888/
```
The address in conjunction with the ealier defined password can be used to access the Jupyter instance through your browser.
Remember the addess `compute-05` is only defined within the domain of the cluster (`alan.priv`). You therefore have to access
the instance using the addess `http://compute-05.alan.priv:8888/`, 
assuming you are connected to the ULiège internal network (e.g., through the VPN or some other service). The server can be terminated through the browser or via the `scancel` command.

## Advanced options

Additional information on the configuration of your notebook server can be found [here](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html).
