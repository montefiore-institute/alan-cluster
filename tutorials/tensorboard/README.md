### How to use Tensorboard via VPN to track real-time training from your local browser

`alan_username = Your provided username to connect Alan.`

`remote_port = Preffered port to run tensorboard in Alan.`

`local_port = Preffered port to run forward from your local PC.`

`remote_path = Path in Alan contains your Tensorboard checkpoints (either in scratch or your personal workspace).`

*(Order of steps doesn't actually matter.)*

First step is to connect Alan via SSH and start Tensorboard with command below.
`\$tensorboard --logdir ${remote_path} --port ${remote_port}`

This will start live-tracking of training of your job in Alan.

In order to port-forward in your local PC execute command below.

`\$ssh -N -f -L localhost:\${local_port}:localhost:${remote_port}  \${alan_username}@master.alan.priv`

This will enable to track training from any web browser on your local PC , go the "localhost:portNumber/" to track your training.




### Things to notice

* You have to be connected ULiege VPN / Alan Clusters.

* Sometimes if you didn't properly kill / disconnected tensorboard will live as background process , just kill via SSH. ( Or change port number for remote)

![test](https://i.ibb.co/PGbxgWy/test.png)

