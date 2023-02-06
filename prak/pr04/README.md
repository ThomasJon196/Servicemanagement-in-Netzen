# IPv6 and Docker

## Task 1 - Remote Deployment of application

### a) Familiarize with Docker-Registry Access on gitlab

Space inside gitlab to store docker images. Similar to dockerhub.io.

### b) Create docker image for registry

```bash
$ docker build -t docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami . # Create imagae
```


### c) Push imgage to registry
1. Login to registry    : `$ docker login docker.fslab.de`
2. Push image           :`$ docker push docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami`


### d) Deploy image on VM

1. SSH into VM & login into docker registry
2. Pull latest image: `docker pull docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami`
3. Run container: `docker run --rm -d -p 20411:80  --name miniwhoami docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami`

### e) Deploy image with docker-compose inside the same network

1. Create docker network: `$ docker create network -d bridge mynetwork`

2. Create `docker-compose.yml` file:

```yml
version: '3.9'
services:
  miniwhoami_20412:
    image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami
    ports:
      - "20412:80"

  miniwhoami_20413:
    image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami
    ports:
      - "20413:80"

networks:
  default:
    name: mynetwork
    external: true

```

3. Start services:

`$ docker-compose up`

> All services are now accessible over the internet via: [< IPv6-address-VM >]:< exposed_port >

### f) Question: How big was the effort? Can the process be automatized further?

- There are alot of steps involved to deploy the container on the VM:
    1. SSH into vm
    2. Login into docker registry
    3. Pull latest image
    4. Run container
    5. (Logout from registry)
    6. Exit ssh connection

- The process can be automated via ansible. And additionally applied to many VM's simulatiously.


## Task 2 - Explore network structure

### a) List Container interfaces

| Con-Name | IP-Addr | Netmask | Default gateway |
|--|--|--|--|
| /miniwhoami | 172.17.0.2 | 172.17.0.0/16 | 172.17.0.1 |
| /miniserver_miniwhoami_20412_1 | 172.18.0.2 |172.18.0.0/16 | 172.18.0.1 |
| /miniserver_miniwhoami_20413_1 | 172.18.0.3 |172.18.0.0/16 | 172.18.0.1 |

### b) List docker networks
```bash
NETWORK ID     NAME        DRIVER    SCOPE
8d0feb521ecc   bridge      bridge    local
8f481771b2d0   host        host      local
559a8c94063d   mynetwork   bridge    local
d87606cc61eb   none        null      local
```
 How to find containers network?
 1. Run `docker container inspect <container_name>`
 2. Search for: `NetworkSettings/Networks`

### c) Enter container and experiment with network access

Used tool to analize container: NETSHOOT

`docker run -it --net container:<container_name> nicolaka/netshoot`

- Each container can a website outisde of the virtual machine.
- Containers inside the docker-network `mynetwork` can ping each other.
- Containers in seperate docker-networks can not ping each other.

### d) How is container access with IPv6 address possible?

Docker automatically maps IPv4 & IPv6 ports.

### e) Troubleshoot default docker network

1. Enter container in network via netshoot
2. Exec. `$ nsenter` to enter network

Is it possible to ping a container inside the same docker network by IP/service_name?

No. `$ ping miniwhoami` does not work.
Inside the default network containers are not callable by name.


### f) Troubleshoot user-defined docker network

1. Enter container in network via netshoot
2. Exec. `$ nsenter` to enter network

Is it possible to ping a container inside the same docker network by service_name?

Yes. `$ ping miniserver_miniwhoami_20412_1` works.
Inside the same user-defined network containers can call each other by name & IP.

### g) Test docker intern DNS-resolution with dig

1. Enter container in network via netshoot

2. Exec: `$ dig <another_container_in_same_network>`

Result:
  ```bash
  9afab085f3e6:~# dig miniserver_miniwhoami_20413_1

  ; <<>> DiG 9.18.3 <<>> miniserver_miniwhoami_20413_1
  ;; global options: +cmd
  ;; Got answer:
  ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41863
  ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

  ;; QUESTION SECTION:
  ;miniserver_miniwhoami_20413_1.	IN	A

  ;; ANSWER SECTION:
  miniserver_miniwhoami_20413_1. 600 IN	A	172.18.0.3

  ;; Query time: 0 msec
  ;; SERVER: 127.0.0.11#53(127.0.0.11) (UDP)
  ;; WHEN: Wed Oct 26 21:04:11 UTC 2022
  ;; MSG SIZE  rcvd: 92
  ```

There is a DNS server running inside the user-defined docker network `127.0.0.11`.

## Task 3 - Activate IPv6 for Docker containers on Virtual Machine

### a) Split avaliable subnet into 4 subnets and assign one to the docker daemon:

The previously assigned subnet
`2001:638:408:200:ff38::/78` is divided into 4 smaller subnets:
1. `2001:638:408:200:ff38::/80`
2. `2001:638:408:200:ff39::/80`
3. `2001:638:408:200:ff40::/80`
4. `2001:638:408:200:ff41::/80`

The first one allready contains the VM's IPv6 address. The second one is used for the docker subnet.

Create /etc/docker/daemon.json and add:
```
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:638:408:200:ff39::/80"
}
```

Default docker bridge IP (before restarting docker):
```bash
$ docker network inspect bridge

...
"Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.17.0.0/16"
                }
            ]
        }
```

After restarting docker daemon with:
`$ systemctl restart docker`

```bash
$ docker network inspect bridge

"Driver": "bridge",
        "EnableIPv6": true,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.17.0.0/16",
                    "Gateway": "172.17.0.1"
                },
                {
                    "Subnet": "2001:638:408:200:ff39::/80",
                    "Gateway": "2001:638:408:200:ff39::1"
                }
            ]
        },
```

The IPv6 option and subnet is now enabled. Started docker containers additionally get a IPv6 address assigned.

### b) Try to access miniwhoami_20411 container via its IPv6 address

Start container:

`$ docker run --rm -d -p 20411:80  --name miniwhoami docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami`

1. Access miniwhoami from the internet. Which IPv6 address is displayed?

The address assigned inside the subnet: `2001:638:408:200:ff39:242:ac11:2`

2. From where can you access miniwhoami?

Only over the host IP and mapped port.

3. Check the routing tables of miniwhoami. Is the Subnet routed correctly? Which problems may arise?

```bash
 db6924d27e07  ~  ip -6 r
2001:638:408:200:ff39::/80 dev eth0 proto kernel metric 256 pref medium
fe80::/64 dev eth0 proto kernel metric 256 pref medium
default via 2001:638:408:200:ff39::1 dev eth0 metric 1024 pref medium
```

- The Subet is routed correctly via the gateway: `2001:638:408:200:ff39::1/80`
- The actual IPv6 address of the VM is `2001:638:408:200:ff38::1/78`, which is currently the only endpoint accessible from the internet.
To route the package to `2001:638:408:200:ff39::1/80`, an additional NDP-Server is required, which has to be installed on the VM itself.

4. Why is the service accessible over the internet anyway?

- The docker port mapping automatically binds a host machine port to the container.


5. Which conditions have to be meet, to access the container via its IPv6 address?

- NDP-Server on VM which routes the packages to subnet-gateways

## Task 4 - Docker IPv6-NDP

To acccess the container which lies inside a subnet of the Server, an NDP(Neighbour discovery protocol) Proxy has to configured.

a) Turn on NDP-Proxy function of the ens18 interface which works over IPv6 & add container IPv6 to it.

Enable NDP interface option: `sysctl net.ipv6.conf.ens18.proxy_ndp=1`

Add neigh proxy: `ip -6 neigh add proxy < Container-IPv6 > dev ens18`

Try pinging `miniwhoami_20421`:

`$ nc -vz 2001:638:408:200:ff38::1 20411` : Pinging a specific port requires the `nc` command. Pinging succeds.
 

Additionally flask requires the listen address to be IPv6 instead of IPv4. The Dockerfile was changed accordingly:

```dockerfile
FROM python:slim-buster
RUN pip install Flask colorhash
COPY index.py .
COPY miniwhoami.py .
CMD flask --app index run -h ::
```

Pinging the port via `nc -vz 2001:638:408:200:ff39:242:ac11:2 80`
now works as well.

The container running on `2001:638:408:200:ff39:242:ac11:2` was started with `$ docker run --rm -d -p 80:80  --name miniwhoami docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami`, and is currently only reachable over the mapped port 80 on the host-machine.

b + c) Install NDP-Proxy:

Install ndppd: `$ apt install ndppd`

Copy template from `/usr/share/doc/ndppd/ndppd.conf-dist` and create file `/etc/ndppd.conf`:

Adjust:
- proxy :`ens18` interface 
- rule: `<IP_subnet_mask>`

```bash
proxy ens18 {

   # router <yes|no|true|false>
   # This option turns on or off the router flag for Neighbor Advertisement
   # messages. Default value is 'true'.

   router yes

   # timeout <integer>
   # Controls how long to wait for a Neighbor Advertisment message before 
   # invalidating the entry, in milliseconds. Default value is '500'.

   timeout 500

   # ttl <integer>
   # Controls how long a valid or invalid entry remains in the cache, in 
   # milliseconds. Default value is '30000' (30 seconds).

   ttl 30000

   # rule <ip>[/<mask>]
   # This is a rule that the target address is to match against. If no netmask
   # is provided, /128 is assumed. You may have several rule sections, and the
   # addresses may or may not overlap.

   rule 2001:638:408:200:ff39::/80 {
      # Only one of 'static', 'auto' and 'interface' may be specified. Please
      # read 'ndppd.conf' manpage for details about the methods below.

      # 'auto' should work in most cases.

      # static (NEW)
      # 'ndppd' will immediately answer any Neighbor Solicitation Messages
      # (if they match the IP rule).

      # iface <interface>
      # 'ndppd' will forward the Neighbor Solicitation Message through the
      # specified interface - and only respond if a matching Neighbor
      # Advertisement Message is received.

      # auto (NEW)
      # Same as above, but instead of manually specifying the outgoing
      # interface, 'ndppd' will check for a matching route in /proc/net/ipv6_route.

      static

      # Note that before version 0.2.2 of 'ndppd', if you didn't choose a
      # method, it defaulted to 'static'. For compatibility reasons we choose
      # to keep this behavior - for now (it may be removed in a future version).
   }
}
```

> ## ndppd. service has to be restarted after changing configuration file: `$ systemctl restart ndppd.service`


## Task 5: Public IPv6 Subnet with Docker

Inside the provided address-space `2001:638:408:200:ff??::/78` an IPv6-docker-subnet should be created with the following mask: `2001:638:408:200:ff??:cafe::/96`

a) Is the size of the subnet suffizient?

Yes, there is still 32 bit of usable address space left.

b) Setup a docker IPv6 network `my_ipv6` on your server:

```bash
docker network create --ipv6 --subnet 2001:638:408:200:ff38:cafe::/96 --driver bridge my_ipv6
```

c) Adjust ndppd for the new subnet

Added new rule to `/etc/ndppd.conf`
```bash
rule 2001:638:408:200:ff38:cafe::/96 {
      static
  }
```

## Task 6 - Public IPv6 Docker services

- ipv6_1:  2001:638:408:200:ff??:cafe::1111/96
- ipv6_2: 2001:638:408:200:ff??:cafe::2222/96
- ipv6_3: 2001:638:408:200:ff??:cafe::3333/96

Each address requires a new `ip neighbour` entry:
`ip -6 neigh add proxy < Container-IPv6 > dev ens18`


a) Deploy miniwhoami with ipv6_1 as the global address:

```bash
$ docker run --rm -d --expose 80 --ip6 2001:638:408:200:ff38:cafe::1111 
--name miniwhoami1 --network my_ipv6 docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami
```

b) Deploy miniwhoami with ipv6_2/3 via docker-compose:

```yml
version: '3.9'
services:
  miniwhoami2:
    image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami
    expose: [80]
    networks:
      my_ipv6:
        ipv6_address: 2001:638:408:200:ff38:cafe::2222

  miniwhoami3:
      image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami
      expose: [80]
      networks:
        my_ipv6:
          ipv6_address: 2001:638:408:200:ff38:cafe::3333    

networks:
   my_ipv6:
    external: true
```

c) Create AAAA records for your domain

Configure inside your domain-providers website AAAA records for each docker-service.

- `miniwhoami1`s IPv6 was bound to `miniwhoami1.mydomain.de`

d) Ping Profs container-URL & Interpret result:


... Added new address to ip neigh proxy...



## Task 7 - Local IPv6 subnet

a) Create a local docker IPv6 network

`$ docker network create --driver bridge --ipv6 --subnet fd00:dead:beef::/48 loc_ipv6`

b) Explain the address fd00:dead:beef::/48

...


c) Analyze loc_ipv6 with netshoot. Display ip-addresses and default routes:









| Q | A |
|--|--|
| Is docker port mapping obscuring the mapped docker port? | |
| why does the connection via the proxy server take forever? | |