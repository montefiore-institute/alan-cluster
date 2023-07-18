![](https://github.com/montefiore-ai/alan-cluster/blob/master/.github/alan-header.png?raw=true)

Documentation and guidelines for the Alan GPU cluster at the University of Liège.

**The documentation assumes you have access to the private network of the university.**

## General actions

- [Request an account](https://alan.montefiore.uliege.be/register)
- [Request a new feature](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=enhancement&template=feature-request.md&title=%5BFeature+Request%5D+TODO)
- [Submit an issue](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=bug&template=issue-report.md&title=%5BIssue%5D+TODO)
- [Access JupyterHub](https://alan.montefiore.uliege.be/jupyter/)

---

Table of contents:
- [General actions](#general-actions)
- [User account setup](#user-account-setup)
  - [Connecting to Alan](#connecting-to-alan)
  - [Preparing a conda environment](#preparing-a-conda-environment)
  - [Preparing your (Deep Learning) project](#preparing-your-deep-learning-project)
    - [PyTorch](#pytorch)
    - [Jax](#jax)
    - [TensorFlow](#tensorflow)
  - [Transferring your datasets to Alan](#transferring-your-datasets-to-alan)
- [Cluster usage](#cluster-usage)
  - [Slurm commands](#slurm-commands)
  - [Partitions](#partitions)
  - [Filesystems](#filesystems)
  - [Recommended ways to load data into the GPU](#recommended-ways-to-load-data-into-the-gpu)
    - [My dataset does not fit in memory](#my-dataset-does-not-fit-in-memory)
    - [My dataset fits in memory](#my-dataset-fits-in-memory)
- [Cluster-wide datasets](#cluster-wide-datasets)
- [Centralised Jupyter Access](#centralised-jupyter-access)
    - [Accessing Jupyter Lab](#is-it-possible-to-access-jupyter-lab)
    - [Launching multiple servers](#launching-multiple-servers)

---

## User account setup

If you do not have an account, then first [request an account](https://alan.montefiore.uliege.be/register) to the GPU cluster.

### Connecting to Alan

Once you have been provided with your account details by e-mail, you can connect to Alan through SSH:
```console
you@local:~ $ ssh you@master.alan.priv
```
After logging in with the password provided by the account confirmation e-mail, you will be forced to change the password.

The e-mail will additionally contain a private authentication key which can be used to connect to the GPU cluster. The key can be used by manually executing:
```console
you@local:~ $ ssh -i path/to/privatekey you@master.alan.priv
```
The authentication procedure can be automated by moving the private key
```console
you@local:~ $ cp path/to/privatekey ~/.ssh/id_alan
you@local:~ $ chmod 400 ~/.ssh/id_alan
```
and adding
```
Host alan
  HostName master.alan.priv
  User you
  IdentityFile ~/.ssh/id_alan
```
to `~/.ssh/config`.

### Preparing a conda environment

On your initial login, we will guide you to automatically install a conda environment. **Carefully** read the instructions. If you cancelled the installation procedure, you can still setup conda by executing:

```console
you@master:~ $ wget https://repo.anaconda.com/archive/Anaconda3-2023.07-1-Linux-x86_64.sh
you@master:~ $ sh Anaconda3-2023.07-1-Linux-x86_64.sh
```

Alternatively, for a lightweight drop-in replacement of conda, you can install [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) by executing

```console
you@master:~ $ bash <(curl -L micro.mamba.pm/install.sh)
```

### Preparing your (Deep Learning) project

The installation of your Deep Learning environment is quite straightforward after `conda` has been configured. In general we recommend to work with [environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) on a per-project basis as it allows for better encapsulation and reproducibility of your experiments.

```console
you@master:~ $ conda create -n myenv python=3.9 -c conda-forge
you@master:~ $ conda activate myenv
(myenv) you@master:~ $ python --version
Python 3.9.13
```

#### PyTorch

```console
(myenv) you@master:~ $ conda install pytorch torchvision -c pytorch -c nvidia
```

#### Jax

```console
(myenv) you@master:~ $ pip install --upgrade "jax[cuda11_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
```

#### TensorFlow

```console
(myenv) you@master:~ $ conda install tensorflow-gpu -c conda-forge
```

### Transferring your datasets to Alan

This section shows you how to transfer your datasets to the GPU cluster. It is a good practice to centralize your datasets in a common folder:
```console
you@master:~ $ mkdir -p path/to/datasets
you@master:~ $ cd path/to/datasets
```

The transfer is initiated using `scp` from the machine storing the data (e.g. your desktop computer) to the cluster:
```console
you@local:~ $ scp -r my_dataset alan:path/to/datasets
```

Alternatively, one can rely on `rsync`:
```console
you@local:~ $ rsync -r -v --progress my_dataset -e ssh alan:path/to/datasets
```

## Cluster usage

The CECI cluster documentation features a [thorough Slurm guide](https://support.ceci-hpc.be/doc/_contents/QuickStart/SubmittingJobs/SlurmTutorial.html). Read it carefully before using Alan.

Elementary tutorials can also be found in [`/tutorials`](tutorials). Read them to get started quickly.

### Slurm commands

- [`sbatch`](https://slurm.schedmd.com/sbatch.html): submit a job to the cluster.
  - To reserve `N` GPU(s) add `--gres=gpu:N` to `sbatch`.
- [`scancel`](https://slurm.schedmd.com/scancel.html): cancel queued or running jobs.
- [`srun`](https://slurm.schedmd.com/srun.html): launch a job step.
- [`squeue`](https://slurm.schedmd.com/squeue.html): display jobs currently in the queue and their associated metadata.
- [`sacct`](https://slurm.schedmd.com/sacct.html): display accounting data for jobs (including finished/cancelled jobs).
- [`sinfo`](https://slurm.schedmd.com/sinfo.html): get information about the cluster and its nodes.
- [`seff`](https://bugs.schedmd.com/show_bug.cgi?id=1611): resource utilization efficiency of the specified job.

### Partitions

The cluster provides several queues or job partitions. We made the design decision to partition the job queues based on the GPU type: `1080ti` (GTX 1080 Ti), `2080ti` (RTX 2080 Ti), `quadro` (Quadro RTX 6000) and `tesla` (Tesla V100). This enables the user to specifically request specific GPUs depending on her needs. A specific job partition can be requested by specifying `--partition=<partition>` to the `sbatch` command or in your submission script. If no partition is specified, then a job will be scheduled where resources are available.

For debugging purposes, e.g. if you would like to quickly test your script, you can also make use of the `debug` partition by specifying `--partition=debug`. This partition has a maximum execution time of 15 minutes.

A full overview of the available partitions is shown below.
```console
you@master:~ $ sinfo -s
PARTITION       AVAIL  TIMELIMIT   NODELIST
all*               up 14-00:00:0   compute-[01-04,06-13]
debug              up      15:00   compute-05
1080ti             up 14-00:00:0   compute-[01-04]
2080ti             up 14-00:00:0   compute-[06-10]
quadro             up 14-00:00:0   compute-[11-12]
tesla              up 14-00:00:0   compute-13
priority-quadro    up 14-00:00:0   compute-[11-12]
priority-tesla     up 14-00:00:0   compute-13
priority           up 14-00:00:0   compute-[01-04,06-13]
```
The high-priority partitions `priority-quadro` and `priority-tesla` can be used to request either Quadro RTX 6000 or Tesla V100 GPUs while flagging your job as high priority in the job queue. This privilege is only available to some users. The `quadro` and `tesla` partitions can be requested by all users, but the priority of the corresponding jobs will be kept as normal.

Your priority status can be obtained by executing:
```console
you@master:~ $ sacctmgr show assoc | grep $USER | grep priority > /dev/null && echo "allowed" || echo "not allowed"
```

### Filesystems

We provide the following filesystems to the user.

| Mountpoint             | Name                     | Capacity | Purpose                                                                                                                            | Load data to GPU from filesystem?                                                                      | Data persistance   |
|------------------------|--------------------------|----------|------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|--------------------|
| `/home/$USER`          | Home directory           | 11TB     | Hosts your main files and binaries.                                                                                                | Only if the dataset fits in memory. Do not use this endpoint if your jobs perform a lot of random I/O. | :heavy_check_mark: |
| `/scratch/users/$USER` | Global scratch directory | 65TB     | Global decentralized filesystem. Store your datasets here if they do not fit in memory, or if it consists of a lot of small files. | Yes                                                                                                    | :x:                |

Data persistance is only guaranteed on `/home/$USER`. Backing-up data hosted on `/scratch` is your responsibility. The results of a computation should preferably stored in `/home/$USER`.

### Recommended ways to load data into the GPU

It is generally not recommended to load small batches from the main storage disk. This translates into a lot of random IO operations on the main storage *hard disks* of the cluster, which in turn degrades the performance of all jobs. We recommend the following ways to load data into the GPU:

#### My dataset does not fit in memory

Use the global `/scratch` filesystem.

#### My dataset fits in memory

In this case, we recommend to simply read the dataset into memory and load your batches directly from RAM. This will not cause any issues as the data is sequentially read from the main RAID array on the master. This has the desirable effect that the heads of the hard disks do not have to move around constantly for every (random) small batch your are trying to load, thereby not degrading the performance of the main cluster storage.

## Cluster-wide datasets

At the moment we provide the following cluster-wide, **read-only** datasets which are accessible at `/scratch/datasets`:
```console
you@master:~ $ ls -l /scratch/datasets
```

If you would like to propose a new cluster-wide dataset, feel free to [submit a proposal](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=enhancement&template=feature-request.md&title=%5BFeature+Request%5D+TODO).

## Centralised Jupyter Access

We provide a centralised Jupyter instance which can be accessed using your Alan account at [https://alan.montefiore.uliege.be/jupyter](https://alan.montefiore.uliege.be/jupyter).
Launching kernels within existing environments is possible. No additional configuration is required.

> Please note that, in order to use existing environments, Anaconda should be installed (compact installations such as miniconda will not work).

> **Important**: Make sure `nb_conda_kernels` installed in your `base` environment if you want your Anaconda environments to show up in JupyterHub. In addition, ensure `ipykernel` is installed in your environments of interest.

### Is it possible to access Jupyter Lab?

Yes, simply change the `tree` keyword in the URL to `lab`. For instance
```
https://alan.montefiore.uliege.be/jupyter/user/you/tree
```
becomes
```
https://alan.montefiore.uliege.be/jupyter/user/you/lab
```

### Launching multiple servers

We allow you to have more than one running server at the same time. To add a new server, navigate to the control panel.

#### Via Jupyter Lab

In the top left corner: `File -> Hub Control Panel`

#### Via Jupyter Notebook

In the top right corner: `Control Panel`
