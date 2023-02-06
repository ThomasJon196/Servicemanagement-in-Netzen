## Docker Datamanagement und Networking presentation

Miniwhoami is used to demonstrate the different kinds of storage options
and is directly connected to the host network namespace/ the default bridge and a user-defined bridge.

## Storage options

miniwhoami service creates a count.txt file.

### Default

No specification of volume/mount

`$ docker run --rm -d -p 20231:5000 --name miniwhoami_default miniwhoami`

### Volume

`$ docker volume create myvol`

`$ docker run --rm -d -p 20237:5000 --name miniwhoami_volume -v myvol:/resources miniwhoami`

Data is created inside specified dir.
Usable by multiple containers.
Directory is managed by docker additionally!


### Bind mount

`$ docker run --rm -d -p 20232:5000 --name miniwhoami_bind_mount -v "$(pwd)"/local_resources:/resources miniwhoami`

Data is created inside specified dir.
Usable by multiple containers.

### tmpfs mount

`$ docker run --rm -d -p 20233:5000 --name miniwhoami_tmpfs_mount --tmpfs /resources miniwhoami`

After restarting the container all data is lost.



## Networking


### Host network

`$ docker run --rm -d --name miniwhoami_host_network --net host miniwhoami`

### Bridge network

`$ docker network create -d bridge --subnet 10.0.0.0/24 my_bridge`

`$ docker run --rm -d -p 20234:5000 --net my_bridge --name miniwhoami_1 miniwhoami`

`$ docker run --rm -d -p 20235:5000 --net my_bridge --ip 10.0.0.254 --name miniwhoami_2 miniwhoami`



### Networking-Tool: netshoot

`$ docker run -it --net container:miniwhoami_1 nicolaka/netshoot`

Pinging a container in a different namespace does not work.


## Insights

Binding a volume without a path mapping creates a new directory with the volume name `myvol` inside the container root path.

`$ docker run --rm -d -p 20237:5000 --name miniwhoami_volume -v myvol miniwhoami`

The port mapping specifies the communication from the host address to the container.
Communication from container to the outside world happens automaticaly over NAT/masquerade.