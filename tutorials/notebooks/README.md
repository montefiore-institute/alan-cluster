# Running a Jupyter instance on Alan

This tutorial will guide you on how to setup your personalized Jupyter instance on the GPU cluster.

## Securing the notebook server

A first prerequisite is the notebook configuration file and can be generated as follows:
```bash
jupyter notebook --generate-config
```
This operation will write a new default config to your home directory.

Since the notebook server will be allocated

Additional information on the configuration of your notebook server can be found [here](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html).
