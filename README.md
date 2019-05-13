![](https://github.com/montefiore-ai/alan-cluster/blob/master/.github/alan-header.png?raw=true)

Documentation and guidelines for the Alan GPU cluster at the University of Liège.

**The documentation assumes you have access to the private network of the university.**

## Table of content

- [General actions](#general-actions)
- [Cluster-wide datasets](#cluster-wide-datasets)
- [Account setup](#user-account-setup)
- [Cluster usage](#cluster-usage)

## General actions

- [Account registration](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=new+user&template=new-user.md&title=%5BNew+User%5D+TODO)
- [Request a new feature](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=enhancement&template=feature-request.md&title=%5BFeature+Request%5D+TODO)
- [Submit an issue](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=bug&template=issue-report.md&title=%5BIssue%5D+TODO)

## Cluster-wide datasets

At the moment we provide the following cluster-wide, read-only datasets which are accessible at `/data/datasets`:

```console
admin@alan-master:~ $ ll /data/datasets
```

If you would like to propose a new cluster-wide dataset, feel free to [submit a proposal](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=enhancement&template=feature-request.md&title=%5BFeature+Request%5D+TODO).

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
you@local:~ $ ssh-copy-id -i .ssh/id_rsa.alan you@alan.calc.priv
```

Now you should be able to login to the cluster using your Alan identity file.

```console
you@local:~ $ ssh -i .ssh/id_rsa.alan you@alan.calc.priv
```

To prevent you from having to type the `-i` flag every time you log in, you can simply add the following to `.ssh/config`.

```ssh
Host alan
  HostName alan.calc.priv
  IdentityFile ~/.ssh/id_rsa.alan
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

### Preparing an Anaconda environment

> **Recommended**. **This installs a Python 3 environment by default.**

```console
you@alan-master:~ $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
you@alan-master:~ $ sh Miniconda3-latest-Linux-x86_64.sh
```

### Preparing your Deep Learning environment

#### PyTorch

TODO

#### TensorFlow

TODO

## Cluster usage

The CECI cluster documentation features a [thorough Slurm guide](https://support.ceci-hpc.be/doc/_contents/QuickStart/SubmittingJobs/SlurmTutorial.html). Read it carefully before using Alan. 

### Main `slurm` commands

- [`sbatch`](https://slurm.schedmd.com/sbatch.html): submit a job to the cluster
 - for reserving gpu(s) use: `--gres=gpu:N_GPUS`
- [`scancel`](https://slurm.schedmd.com/scancel.html): cancel queued or running jobs
- [`srun`](https://slurm.schedmd.com/srun.html): launch a job step
- [`squeue`](https://slurm.schedmd.com/squeue.html): display jobs currently in the queue and their associated metadata
- [`sacct`](https://slurm.schedmd.com/sacct.html): display accounting data for jobs (including finished/cancelled jobs)
- [`sinfo`](https://slurm.schedmd.com/sinfo.html): get information about the cluster and its nodes

## Tutorials

1. [Hello world](https://github.com/montefiore-ai/alan-cluster/tree/master/tutorials/01-hello-world)
