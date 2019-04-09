# Alan

Documentation and guidelines for the Alan GPU cluster at the University of Liège.

**The documentation assumes you have access to the private network of the university.**

## General actions

- [Account registration](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=new+user&template=new-user.md&title=%5BNew+User%5D+TODO)
- [Request a new feature](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=enhancement&template=feature-request.md&title=%5BFeature+Request%5D+TODO)
- [Submit an issue](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=bug&template=issue-report.md&title=%5BIssue%5D+TODO)

## Cluster-wide datasets

## User account setup

If you do not have an account, please submit [this](https://github.com/montefiore-ai/alan-cluster/issues/new?assignees=JoeriHermans&labels=new+user&template=new-user.md&title=%5BNew+User%5D+TODO) form to request access to the GPU cluster.

### Generation of SSH keys

### Transferring datasets

In general there are two options to transfer your dataset from a remote location to the cluster. One option is to rely on [NFS](#NFS) directly, while the other transfers your dataset over an [SSH](#SSH) connection. There is no preferred option, both are equally suitable. However, if you are dealing with sensitive data we recommend to rely on SSH as NFS transfers are not encrypted.

```console
you@alan-master:~ $ mkdir Datasets
you@alan-master:~ $ cd Datasets
```

#### SSH

```console
you@local:~ $ ...
```

### Preparing an Anaconda environment

> **This installs a Python 3 environment by default**

```console
you@alan-master:~ $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
you@alan-master:~ $ sh Miniconda3-latest-Linux-x86_64.sh
```

## Tutorials

1. [Hello World](https://github.com/montefiore-ai/alan-cluster/tree/master/tutorials/01-hello-world)
