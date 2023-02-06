# Load Balancing

## Task 1 - nginx-Load-Balancer

Create a nginx-Load-Balancer with 3 miniwhoami services running in a local IPv6 subnet.

### a) Compose file with 3 miniwhoami services

```yaml
version: '3.9'
services:
    miniwhoami-s1:
      container_name:  miniwhoami-s1
      image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami
      networks:
        - loc_ipv6
      restart: unless-stopped

    miniwhoami-s2:
      container_name:  miniwhoami-s2
      image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami
      networks:
        - loc_ipv6
      restart: unless-stopped

    miniwhoami-s3:
      container_name:  miniwhoami-s3
      image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami
      networks:
        - loc_ipv6
      restart: unless-stopped

networks:
  loc_ipv6:
    external: true      # Key-word for pre-existing network
  my_ipv6:
    external: true
```

### b) Look up how nginx load balancing works

- Which HTTP-Loadbalancing methods exists?

Decide which server receives the client-request.

1. Round Robin - Even distribution of requests
2. Least Connections - Requests send to server with least number of connections
3. IP Hash - Desination server determined by hash over Client IP-address. Guarantees that client is served by same server.
4. Hash - Determined by a user-defined key e.g. URI
5. Least Time - Selection of server with lowest average latency and active connections.
6. Random

- What is session persistence?

nginx identifies user sessions and routes requests to the same upstream server.

1. Sticky cookie - Session cookie is added to the first response. Clients next response contains the cookie.
2. Sicky route - similar
3. Sticky learn - Automatic identification by either cookie or existing session identifier.


### c) Add a load balancer to the compose file

```yaml
loadbalancer:
      container_name: loadbalancer
      image: nginx:latest
      networks:
        my_ipv6:
          ipv6_address: 2001:638:408:200:ff38:cafe::9999
        loc_ipv6:
      volumes:
        - ./nginx.conf:/etc/nginx/nginx.conf:ro
      environment:
        - ENABLE_IPV6=true 
      restart: unless-stopped
```

## Task 2 - Read Kubernetes chapters

[Book](https://www.manning.com/books/kubernetes-in-action)

Chapter 3 - Pods: running containers in Kubernetes.

Chapter 4 - Replication and other controllers: deploying managed pods.

Chapter 5 - Services: enabling clients to discover and talk to pods.