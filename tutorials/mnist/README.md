# Running a Deep Learning job 

This short tutorial will guide you on how to run your first Deep Learning job on Alan.

**Attention:** This document assumes you have an Anaconda environment configured with PyTorch.

```console
you@alan-master:~ $ conda activate myenvironment
you@alan-master:~ $ conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
```

## Training a Convolutional network on MNIST

You have just followed the last lecture of INFO8010 and you are now ready to train your first neural network on MNIST! After some long nights of debugging, you arrive to a PyTorch script similar to `mnist.py`. 

## Scheduling your job

Jobs are scheduled on Alan through Slurm scripts. They specify the resources you are requesting to execute your job, as well as the sequence of instructions you want to execute. In the Slurm script `mnist.sbatch` below, we allocate 2 CPUs et 1 GPU and specify the Python script we want to run on the cluster. 

```console
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
source activate myenvironment         # CHANGEME

# Run your Python script
cd /home/you/mnist  # CHANGEME
python mnist.py
```

After your resources have been properly configured, your PyTorch script is ready to be scheduled by Slurm:
```console
you@alan-master:~ $ sbatch mnist.sbatch
Submitted batch job 1346061
```

You can check the scheduling queue using the `squeue` command. It tells you about the jobs that are pending for resources and indicates those currently running:

```console
you@alan-master:~ $ squeue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
               ...
           1346061       all    mnist  glouppe  R       0:07      1 alan-compute-02
```

The ouput file of the execution will be written to `mnist/mnist-output.log`:

```console
you@alan-master:~ $ more mnist/mnist-output.log 
Downloading http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz to ../data/MNIST/raw/train-images-idx3-ubyte.gz
Extracting ../data/MNIST/raw/train-images-idx3-ubyte.gz to ../data/MNIST/raw
Downloading http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz to ../data/MNIST/raw/train-labels-idx1-ubyte.gz
Extracting ../data/MNIST/raw/train-labels-idx1-ubyte.gz to ../data/MNIST/raw
Downloading http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz to ../data/MNIST/raw/t10k-images-idx3-ubyte.gz
Extracting ../data/MNIST/raw/t10k-images-idx3-ubyte.gz to ../data/MNIST/raw
Downloading http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz to ../data/MNIST/raw/t10k-labels-idx1-ubyte.gz
Extracting ../data/MNIST/raw/t10k-labels-idx1-ubyte.gz to ../data/MNIST/raw
Processing...
Done!

Train Epoch: 1 [0/60000 (0%)]	Loss: 2.300039
Train Epoch: 1 [640/60000 (1%)]	Loss: 2.213470
Train Epoch: 1 [1280/60000 (2%)]	Loss: 2.170460
Train Epoch: 1 [1920/60000 (3%)]	Loss: 2.076699
Train Epoch: 1 [2560/60000 (4%)]	Loss: 1.868078
...
```