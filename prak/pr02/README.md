## Task 1 - Install Docker & Docker-Compose

a)
Docker Versionsinformationen: 
- Client: 20.10.18
- Server:
    - Engine: 20.10.18
    - API-version: 1.41

b)
Docker-compose installation:
1. Download des offiziellen docker compose github repositories und einfuegen in den .docker/cli-plugins/ Ordner.
    ```
    mkdir -p ~/.docker/cli-plugins/
    curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
    ```
2. docker-compose ausfuehrbar machen:
    `chmod +x ~/.docker/cli-plugins/docker-compose`

Docker-Compose Version: 1.29.2


## Task 2 Primitive webserver

a)
1. Install Flask (Python web-framework)
    `pip install Flask`

2. Create new python-file `index.py`:
    ```py
    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "<p>Hallo Service Management winter term 2022. My name is Thomas</p>"
    ```

b)
1. Start Flask-Servers
    ```bash
        flask --app index run # Startet automatisch den Flask Server auf localhost port 5000.
    ```
2. Access Flask Server via http://127.0.0.1:5000.

![](./pictures/Screenshot%20from%202022-10-15%2017-18-24.png)


c)

Create Dockerfile:
    
```yml
FROM python:slim-buster                 # Base-Image. slim-buster -> lightweight python
RUN pip install Flask                   # Install Flask library
COPY index.py .                         # Copy index.py to image
CMD flask --app index run -h 0.0.0.0    # Start flask-server via index(.py) file using the host 0.0.0.0
```

d)

Create Docker-Image with tag 'miniserver': 

    `$ docker build . -t miniserver:v1`

e) 

Start miniserver-Container:

    $ docker run -d -p 20221:5000 miniserver:v1

`-p 20221:5000` - bind local port 20221 to container port 5000
`-d` - detached mode


# Task 3 - Service miniwhoami

Created a service which displays:
- hostname
- ipv4
- ipv6
- access count
- Changes color based on hostname

c)

Dockerfile used to create image:

```yml
FROM python:slim-buster
RUN pip install Flask colorhash
COPY index.py .
CMD flask --app index run -h 0.0.0.0
```

    $ docker build . -t miniwhoami

d) Deploy multiple containers

    $ docker run -d -p 20231:5000 --name miniwhoami_1 miniwhoami

    $ docker run -d -p 20232:5000 --name miniwhoami_2 miniwhoami

c) Results

![](./pictures/Screenshot%20from%202022-10-15%2020-47-50.png)

![](./pictures/Screenshot%20from%202022-10-15%2020-48-00.png)


# Task 4 - Network Troubleshooting

a) Access running container

    $ docker exec -it miniwhoami_1 bash


### Can you execute any of the following commands inside the container? - ping, ip a, curl, dig, nslookup

- No, because I chose a slim-python image for my application, which only contains the necessary libraries for the execution of python.

b) Use nicolaka/netshoot for troubleshooting:

`$ docker run -it --net container:miniwhoami_1 nicolaka/netshoot`

All previously mentioned commands function inside the netshoot tool.

c) Can you access miniwhoami_2 from miniwhoami_1 ?

Yes, a ping too miniwhoami_2 works.

d) How are the two containers connected ?

via the docker0-bridge

e) Can you connect to the website heise.de ?

Yes. A ping works.

f) Display and interpret the containers routing table:

```
    ~$ netstat -rn    
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
    0.0.0.0         172.17.0.1      0.0.0.0         UG        0 0          0 eth0
    172.17.0.0      0.0.0.0         255.255.0.0     U         0 0          0 eth0
```

1. The first entry corresponds to the gateway `172.17.0.1` indicated by the Flag `G`. The container is connected to it via the `eth0` interface.
2. The second entry corresponds to the localhost `172.17.0.0` of the container.




***
### Questions:

- Why does the interface 0.0.0.0 have to be explicitly defined in flask/docker?
    
    localhost inside the container is not the same as localhost outside. 
    In the context of servers, 0.0.0.0 means all IPv4 addresses on the local machine

- How to find out from container to which bridge it is connected?