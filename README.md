![](https://github.com/montefiore-ai/alan-cluster/blob/master/.github/alan-header.png?raw=true)

Documentation and guidelines for the Alan GPU cluster at the University of Liège.

**The documentation assumes you have access to the private network of the university.**

---

Table of contents:
- [General actions](#general-actions)
- [User account setup](#user-account-setup)
  - [Connecting to Alan](#connecting-to-alan)
  - [SSH keys](#ssh-keys)
  - [Preparing an Anaconda environment](#preparing-an-anaconda-environment)
  - [Preparing your (Deep Learning) project](#preparing-your-deep-learning-project)
    - [PyTorch](#pytorch)
    - [TensorFlow](#tensorflow)
- [Cluster usage](#cluster-usage)
  - [Slurm commands](#slurm-commands)
  - [Partitions](#partitions)
  - [Filesytems](#filesystems)
  - [Transferring data to the cluster](#transferring-data-to-the-cluster)
- [Cluster-wide datasets](#cluster-wide-datasets)

---

## General actions

- [Request an account](https://alan.montefiore.uliege.be/register)
- [Request a new feature](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=enhancement&template=feature-request.md&title=%5BFeature+Request%5D+TODO)
- [Submit an issue](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=bug&template=issue-report.md&title=%5BIssue%5D+TODO)

## User account setup

If you do not have an account, please submit [this](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=new+user&template=new-user.md&title=%5BNew+User%5D+TODO) form to request access to the GPU cluster.

### Connecting to Alan

Once you have been provided with your account details by e-mail, you can connect to Alan through SSH:

```console
you@local:~ $ ssh you@master.alan.priv
```
After logging in with the password provided by the acceptance e-mail, you will be forced to change the password.

The e-mail will additionally contain a private authentication key which can be used to connect to the GPU cluster.
The key can be used by manually executing:
```console
you@local:~ $ ssh -i /path/to/privatekey/alan you@master.alan.priv
```
Likewise, the authentication procedure can be automated by moving the private key
```console
you@local:~ $ cp ~/Downloads/alan ~/.ssh/alan
you@local:~ $ chmod 400 ~/.ssh/alan
```
and adding
```bash
Host alan
  HostName master.alan.priv
  IdentityFile ~/.ssh/alan
```
to `.ssh/config`.


### Preparing an Anaconda environment

On your initial login, we will guide you to automatically install an Anaconda environment. **Carefully** read the instructions.
If you cancelled the installation procedure, you can still setup your Anaconda by executing:

> **Recommended**. **This installs a Python 3 environment by default.**

```console
you@alan-master:~ $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
you@alan-master:~ $ sh Miniconda3-latest-Linux-x86_64.sh
```

### Preparing your (Deep Learning) project

The installation of your Deep Learning environment is quite straightforward after Anaconda has been configured. In general we recommend to work with [environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) on a per-project basis. This is generally good practice as it allows for more convenient reproducability of your experiments.

#### PyTorch

```console
you@alan-master:~ $ conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
```

#### TensorFlow

> **Attention**. Install `tensorflow-gpu` to use `tensorflow` on the GPU's! The same holds for `keras-gpu`.

```console
you@alan-master:~ $ conda install tensorflow-gpu
```

### Transferring your datasets to Alan

This section shows you how to transfer your datasets to the GPU cluster. It is a good practice to centralize your datasets in a common folder:

```console
you@alan-master:~ $ mkdir datasets
you@alan-master:~ $ cd datasets
```

The transfer is initiated using `scp` from the machine storing the data (e.g., your desktop computer) to the cluster:

```console
you@local:~ $ scp -r my_amazing_dataset you@master.alan.priv:/location/of/datasets/
```

Alternatively, one can rely on `rsync`:

```console
you@local:~ $ rsync -r -v --progress my_amazing_dataset -e ssh you@master.alan.priv:/location/of/datasets/
```

## Cluster usage

The CECI cluster documentation features a [thorough Slurm guide](https://support.ceci-hpc.be/doc/_contents/QuickStart/SubmittingJobs/SlurmTutorial.html). Read it carefully before using Alan.

Elementary tutorials can also be found in [`/tutorials/`](https://github.com/montefiore-ai/alan-cluster/tree/master/tutorials).

### Slurm commands

- [`sbatch`](https://slurm.schedmd.com/sbatch.html): submit a job to the cluster.
  - To reserve GPU(s) add `--gres=gpu:N_GPUS` to `sbatch`.
- [`scancel`](https://slurm.schedmd.com/scancel.html): cancel queued or running jobs.
- [`srun`](https://slurm.schedmd.com/srun.html): launch a job step.
- [`squeue`](https://slurm.schedmd.com/squeue.html): display jobs currently in the queue and their associated metadata.
- [`sacct`](https://slurm.schedmd.com/sacct.html): display accounting data for jobs (including finished/cancelled jobs).
- [`sinfo`](https://slurm.schedmd.com/sinfo.html): get information about the cluster and its nodes.

### Partitions
The cluster provides several queues or job partitions. We made the design decision to partition the job queues based on the GPU type. This enables the user to specifically request certain GPU types. For instance, the high-memory Quadro and Tesla hardware. A specific job partition can be acessed by specifying `--partition=<partition>` to the `sbatch` command or in your submission script. For instance, if you would like to test your script, you can make use of the `debug` partition by specifying `--partition=debug`, which has a maximum execution time of 15 minutes. A full overview of the available partitions is shown below.
```console
root@master:~ sinfo -s
PARTITION       AVAIL  TIMELIMIT   NODELIST
all*               up 14-00:00:0   compute-[01-04,06-13]
debug              up      15:00   compute-05
1080ti             up 14-00:00:0   compute-[01-04]
2080ti             up 14-00:00:0   compute-[06-10]
quadro             up 14-00:00:0   compute-[11-12]
tesla              up 14-00:00:0   compute-13
priority-quadro    up 14-00:00:0   compute-[11-12]
priority-tesla     up 14-00:00:0   compute-13
```
Your priority status can be obtained by executing
```console
you@master:~ sacctmgr show assoc | grep $USER | grep priority > /dev/null && echo "Allowed" || echo "Not allowed"
```
After verifying you have permissions, you can submit your job using by specifying `--partition=priority-quadro` or `--partition=priority-tesla`. Specifying this option while insufficient permissions will result in a submission failure anyway.

### Recommended ways to load data into the GPU

It is generally not recommended to load small batches from the main storage disk because most of Deep Learning requires (small) random batches. This translates into a lot of random IO operations on the main storage *hard disks* of the cluster. Which in turn degrades the performance. We recommend the following ways to load data into the GPU:

#### My dataset does not fit in memory

We configured the Cluster to allocate user-directories on the local SSD's of the compute nodes. These are perfectly capable to handle many concurrent random IO operations.

##### Use the preallocated space on a per-job basis
You can use the folder defined in `/scratch/$SLURM_JOB_USER/$SLURM_JOB_ID` for the entirety of your job. It will be cleaned up automatically after your job has been completed. If your dataset is sufficiently small (say < 50GB), we recommend to use this option. For a 50GB dataset we expect a transfer time of about 1 minute. This option can be used by adding the following line to your Slurm submission script:

```bash
cp -r /home/you/datasets/my_dataset /scratch/$SLURM_JOB_USER/$SLURM_JOB_ID
```

**Attention**: Do not forget to actually load the data from `/scratch/$SLURM_JOB_USER/$SLURM_JOB_ID`.

##### Transfer your dataset to the SSD's on the compute nodes

A bottleneck in the approach above is obviously the transfer time to the compute node. This can be resolved by manually transferring the dataset to your scratch-directory on one or several compute nodes. Afterwards, you can add `--nodelist=alan-compute-xx` to your `sbatch` arguments. This will instruct Slurm to allocate the job on `alan-compute-xx`.

**Attention**: Do not forget to delete your dataset from the SSD's when you completed a project.

#### My dataset fits in memory

In this case, we recommend to simply read the dataset into memory and load your batches directly from RAM. This will not cause any issues as the data is sequentially read from the main RAID array on the master. This has the desirable effect that the heads of the hard disks do not have to move around constantly for every (random) small batch your are trying to load, thereby not degrading the performance of the main cluster storage.

## Cluster-wide datasets

At the moment we provide the following cluster-wide, **read-only** datasets which are accessible at `/data/datasets`:

```console
you@alan-master:~ $ ls -al /scratch/datasets
```

If you would like to propose a new cluster-wide dataset, feel free to [submit a proposal](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=enhancement&template=feature-request.md&title=%5BFeature+Request%5D+TODO).
