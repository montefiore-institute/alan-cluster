![](https://github.com/montefiore-ai/alan-cluster/blob/master/.github/alan-header.png?raw=true)

Documentation and guidelines for the Alan GPU cluster at the University of Liège.

**The documentation assumes you have access to the private network of the university.**

Table of contents:
- [General actions](#general-actions)
- [Account setup](#user-account-setup)
- [Cluster usage](#cluster-usage)
- [Cluster-wide datasets](#cluster-wide-datasets)

## General actions

- [Account registration](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=new+user&template=new-user.md&title=%5BNew+User%5D+TODO)
- [Request a new feature](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=enhancement&template=feature-request.md&title=%5BFeature+Request%5D+TODO)
- [Submit an issue](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=bug&template=issue-report.md&title=%5BIssue%5D+TODO)

## User account setup

If you do not have an account, please submit [this](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=new+user&template=new-user.md&title=%5BNew+User%5D+TODO) form to request access to the GPU cluster.

### SSH keys

Once you have been provided with your account details by e-mail, we *strongly recommend* to authenticate your access to Alan using SSH keys. Such a key can be generated on your local machine:

```console
you@local:~ $ ssh-keygen -t rsa -b 4096
Generating public/private rsa key pair.
Enter file in which to save the key (/home/you/.ssh/id_rsa): /home/you/.ssh/id_rsa.alan
Enter passphrase (empty for no passphrase): ************
SHA256:b0uJjgkigIbzdli+EiuZ88hvq6REvGThht8EF9SVC+o you@local
The key's randomart image is:
+---[RSA 4096]----+
|   .o. ...       |
|     .o .        |
| .. .. . .       |
|* .o.   .        |
|*O .o   S        |
|B+o*E    o .     |
|.**o=   . =      |
|X+o+ o + o .     |
|o*=+o o . .      |
+----[SHA256]-----+
```

At this point your public and private keypair should be present in `/home/you/.ssh`:

```console
you@local:~ $ ll .ssh
-rw-r--r-- 1 you you  60 Jan  7 21:53 config
-rw------- 1 you you  1.7K Apr 29  2018 id_rsa
-rw------- 1 you you  3.4K Apr  9 12:39 id_rsa.alan
-rw-r--r-- 1 you you  737 Apr  9 12:39 id_rsa.alan.pub
-rw-r--r-- 1 you you  393 Apr 29  2018 id_rsa.pub
```

Finally, copy the identity file to Alan.

```console
you@local:~ $ ssh-copy-id -i ~/.ssh/id_rsa.alan you@alan.calc.priv
```

Now you should be able to login to the cluster using your Alan identity file.

```console
you@local:~ $ ssh -i ~/.ssh/id_rsa.alan you@alan.calc.priv
```

To prevent you from having to type the `-i` flag every time you log in, you can simply add the following to `~/.ssh/config`.

```ssh
Host alan
  HostName alan.calc.priv
  IdentityFile ~/.ssh/id_rsa.alan
```

### Preparing an Anaconda environment

> **Recommended**. **This installs a Python 3 environment by default.**

```console
you@alan-master:~ $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
you@alan-master:~ $ sh Miniconda3-latest-Linux-x86_64.sh
```

### Preparing your (Deep Learning) project

The installation of your Deep Learning environment is quite straightforward after Anaconda has been installed. In general we recommend to work with [environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) on a per-project basis. This is generally good practice as it allows for more convenient reproducability of your experiments.

#### PyTorch

```console
you@alan-master:~ $ conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
```

#### TensorFlow

**Attention**: Install `tensorflow-gpu`! The same hold for `keras-gpu`.

```console
you@alan-master:~ $ conda install tensorflow-gpu
```

### Transferring datasets

This section shows you how to transfer your datasets to the GPU cluster. It is a good practice to centralize your datasets in a common folder:

```console
you@alan-master:~ $ mkdir datasets
you@alan-master:~ $ cd datasets
```

Next, the transfer is initiated using `scp` from the machine storing the data (e.g., your desktop computer) to the cluster:

```console
you@local:~ $ scp -r my_amazing_dataset alan.calc.priv:~/datasets/
```

Alternatively, one can rely on `rsync`:

```console
you@local:~ $ rsync -r -v --progress my_amazing_dataset -e ssh you@alan.calc.priv:~/datasets/
```

## Cluster usage

The CECI cluster documentation features a [thorough Slurm guide](https://support.ceci-hpc.be/doc/_contents/QuickStart/SubmittingJobs/SlurmTutorial.html). Read it carefully before using Alan. 

### Slurm commands

- [`sbatch`](https://slurm.schedmd.com/sbatch.html): submit a job to the cluster.
  - To reserve GPU(s) add `--gres=gpu:N_GPUS` to `sbatch`.
- [`scancel`](https://slurm.schedmd.com/scancel.html): cancel queued or running jobs.
- [`srun`](https://slurm.schedmd.com/srun.html): launch a job step.
- [`squeue`](https://slurm.schedmd.com/squeue.html): display jobs currently in the queue and their associated metadata.
- [`sacct`](https://slurm.schedmd.com/sacct.html): display accounting data for jobs (including finished/cancelled jobs).
- [`sinfo`](https://slurm.schedmd.com/sinfo.html): get information about the cluster and its nodes.

### Recommended ways to load data into the GPU

It is generally not recommended to load small batches from the main storage disk because most of Deep Learning requires (small) random batches. This translates into a lot of random IO operations on the main storage *hard disks* of the cluster. Which in turn degrades the performance. We recommend the following ways to load data into the GPU:

#### My dataset does not fit in memory

We configured the Cluster to allocate user-directories on the local SSD's of the compute nodes. These are perfectly capable to handle many concurrent random IO operations.

The following environment variables are available to your Slurm submission script:
- `$LOCALSCRATCH` points to `/scratch/$USERNAME`
- `$JOBSCRATCH` points to `/scratch/$USERNAME/$SLURM_JOB_ID`

##### Use the preallocated space on a per-job basis
You can use the folder defined in `$JOBSCRATCH` for the entirety of your job. It will be cleaned up automatically after your job has been completed. If your dataset is sufficiently small (say < 50GB) we recommend to use this option. For a 50GB dataset we expect a transfer time of about 1 minute. This option can be used by adding the following line to your Slurm submission script:

```bash
cp -r /home/you/datasets/my_dataset $JOBSCRATCH
```

##### Transfer your dataset to the SSD's on the compute nodes

A bottleneck in the approach above is obviously the transfer time to the compute node. This can be resolved by manually transferring the dataset to your scratch-directory on one or several compute nodes. Afterwards, you can add `--nodelist=alan-compute-xx` to your `sbatch` arguments. This will instruct Slurm to allocate the job on `alan-compute-xx`.

**Attention**: Do not forget to delete your dataset from the SSD's when you completed a project.

#### My dataset fits in memory

In this case, we recommend to simply read the dataset into memory and load your batches directly from RAM. This will not cause any issues as the data is sequentially read from the main RAID array on the master. This has the desirable effect that the heads of the hard disks do not have to move around constantly for every (random) small batch your are trying to load, thereby not degrading the performance of the main cluster storage.

## Cluster-wide datasets

At the moment we provide the following cluster-wide, read-only datasets which are accessible at `/data/datasets`:

```console
admin@alan-master:~ $ ll /data/datasets
```

If you would like to propose a new cluster-wide dataset, feel free to [submit a proposal](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=enhancement&template=feature-request.md&title=%5BFeature+Request%5D+TODO).
