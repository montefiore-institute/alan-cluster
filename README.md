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

This section shows you how to transfer your datasets to the GPU cluster. It is a good practice to centralize your datasets in a common folder:

```console
you@alan-master:~ $ mkdir datasets
you@alan-master:~ $ cd datasets
```

Next, the transfer is initiated using `scp`:

```console
you@local:~ $ scp -r my_amazing_dataset alan.calc.priv:~/datasets/
```

Alternativly, one can rely on `rsync`:

```console
you@local:~ $ rsync -r -v --progress my_amazing_dataset -e ssh jhermans@alan.calc.priv:~/datasets/
```

### Preparing an Anaconda environment

> **Recommended**. **This installs a Python 3 environment by default.**

```console
you@alan-master:~ $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
you@alan-master:~ $ sh Miniconda3-latest-Linux-x86_64.sh
```

## Tutorials

1. [Hello world](https://github.com/montefiore-ai/alan-cluster/tree/master/tutorials/01-hello-world)
