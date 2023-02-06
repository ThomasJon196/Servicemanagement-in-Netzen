# Serverless Computing

# Task 1 - Definition

1. Define serverless computing.

Definition:
automatic horizontal scaling.
Load balancing
Transparent execution of functions

2. Differentiate between kubernetes based PaaS.

Both run containers.

Platform as a Service

- Runs containers (or on other runtimes)
- Long running (usually)
- Stateless or stateful
- Scales by configuration
- Event-driven or permanently running

Function as a Service

- Runs containers (usually)
- Short lived = ephemeral = transient
- Stateless
- Scales automatically
- Event-driven → executed when triggered

FaaS benefits:

- More tasks automatized in the cloud. e.g. autoscaling
Transparent automatic horizontal scaling makes the technology appear “serverless”
- In public clouds finely granular on-demand billing based on milliseconds execution time
- In public clouds no cost because of scale-to-zero






Serverless Computing is ledigleich eine Hosting-Technologie.
Unterscheiden von Software-Architektur. Die endpoints koennen beliebige Funktionen sein. zb auch Monolithen.



# Task 2 - Instal knative on kubernets cluster (minikube)

## a. Installation

Started a virutal box with ubuntu:22.04
Using: 
```bash
# Install kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.17.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind


# install kubectl (see: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Knative cli
wget https://github.com/knative/client/releases/download/knative-v1.8.1/kn-linux-amd64
mv kn-linux-amd64 kn
chmod +x kn
sudo mv kn /usr/local/bin

# install kn-quickstart (download: https://github.com/knative-sandbox/kn-plugin-quickstart/releases) 
wget https://github.com/knative-sandbox/kn-plugin-quickstart/releases/download/knative-v1.8.1/kn-quickstart-linux-amd64
mv kn-quickstart-linux-amd64 kn-quickstart
chmod +x kn-quickstart
sudo mv kn-quickstart /usr/local/bin

# install knative functions (download: https://github.com/knative/func/releases/tag/knative-v1.8.1)
wget https://github.com/knative/func/releases/download/knative-v1.8.1/func_linux_amd64
chmod +x func_linux_amd64
sudo mv func_linux_amd64 /usr/local/bin/kn-func


# Install docker: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository


# Run quickstart plugin
kn quickstart kind
kind get clusters
kubectl get namespaces


```

## b. Create knative service with webapp and send request with http-client

```bash

# Create webapp hello
vagrant@vagrant:~$ sudo kn service create hello \
 --image gcr.io/knative-samples/helloworld-go \
 --port 8080 \
 --env TARGET=World
Creating service 'hello' in namespace 'default':

  0.268s The Route is still working to reflect the latest desired specification.
  0.483s ...
  0.546s Configuration "hello" is waiting for a Revision to become ready.
 45.134s ...
 45.710s Ingress has not yet been reconciled.
 46.244s Waiting for load balancer to be ready
 46.671s Ready to serve.

Service 'hello' created to latest revision 'hello-00001' is available at URL:
http://hello.default.127.0.0.1.sslip.io


# Send request
vagrant@vagrant:~$ curl http://hello.default.127.0.0.1.sslip.io
Hello World!

```


# Task 3 - Cold-start-delay

## a. Describe cold-start delay cases

Cases, in which a new instance has to be created via `cold-start`:
- Scale-to-Zero
- Crash
- New deployment
- Load-Balancing Up

`Cold-start-delay` = Initialization & Execution time of a function.


## b. Create a service in knative that uses the standard knative pod autoscaler and for which the occurrence of cold-start-delays is impossible.

Source: https://knative.dev/docs/serving/autoscaling/scale-to-zero/, https://knative.dev/docs/serving/autoscaling/scale-bounds/#lower-bound

`knative-lower-bound.yaml`:
```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: helloworld-go
  namespace: default
spec:
  template:
    metadata:
      annotations:
        # Specify that at least one instance has to be running
        autoscaling.knative.dev/min-scale: "1"
    spec:
      containers:
        - image: gcr.io/knative-samples/helloworld-go

```

```bash
kubectl apply -f filename
```


## c) Wait one minute to simulate that the service didn't receive any traffic for one minute. Verify that no cold start occurs when sending a request to the service.


```bash
sudo kubectl get pod
NAME                                              READY   STATUS    RESTARTS   AGE
helloworld-go-00001-deployment-7cdbf6f968-8w27p   2/2     Running   0          45s



time curl http://helloworld-go.default.127.0.0.1.sslip.io -v
*   Trying 127.0.0.1:80...
* Connected to helloworld-go.default.127.0.0.1.sslip.io (127.0.0.1) port 80 (#0)
> GET / HTTP/1.1
> Host: helloworld-go.default.127.0.0.1.sslip.io
> User-Agent: curl/7.81.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< content-length: 13
< content-type: text/plain; charset=utf-8
< date: Mon, 19 Dec 2022 19:03:03 GMT
< x-envoy-upstream-service-time: 61
< server: envoy
< 
Hello World!
* Connection #0 to host helloworld-go.default.127.0.0.1.sslip.io left intact

real	0m0.194s
user	0m0.000s
sys	0m0.019s


```


# Task 4 - Revisions and Traffi Splitting

## a. Create a knative service responding with http status code 200 to all http GET requests

Using base image: ealen/echo-server

```yml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: helloworld-traffic-splitting
  namespace: default
spec:
  template:
    metadata:
      name: helloworld-traffic-splitting-v1
      annotations:
        autoscaling.knative.dev/min-scale: "3"
    spec:
      containers:
        - image: ealen/echo-server
          env:
            - name: "COMMANDS__HTTPCODE__HEADER"
              value: "200"


```

```bash
kubectl apply -f filename
```


## b. Create a new revision of this knative service, which responds with http status code 201 to all http GET requests

```yml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: helloworld-traffic-splitting
  namespace: default
spec:
  template:
    metadata:
      name: helloworld-traffic-splitting-v2
      annotations:
        autoscaling.knative.dev/min-scale: "3"
    spec:
      containers:
        - image: ealen/echo-server
          env:
            - name: "COMMANDS__HTTPCODE__HEADER"
              value: "201"

```


```bash
kubectl apply -f filename
```

```bash
sudo kubectl get pods
NAME                                                          READY   STATUS    RESTARTS   AGE
helloworld-go-00001-deployment-7cdbf6f968-8w27p               2/2     Running   0          15m
helloworld-traffic-splitting-v1-deployment-65f9556cf6-5h24h   2/2     Running   0          2m19s
helloworld-traffic-splitting-v1-deployment-65f9556cf6-9mr28   2/2     Running   0          2m18s
helloworld-traffic-splitting-v1-deployment-65f9556cf6-cb4q4   2/2     Running   0          2m23s
helloworld-traffic-splitting-v2-deployment-5f476dfc96-gm4rv   0/2     Pending   0          6s
helloworld-traffic-splitting-v2-deployment-5f476dfc96-jwms5   0/2     Pending   0          3s
helloworld-traffic-splitting-v2-deployment-5f476dfc96-xd2gw   0/2     Pending   0          3s
```



## c. Let knative split the incoming traffic 40% to the first revision and 60% to the second revision

`traffic-splitting.yml`:
```yml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: helloworld-traffic-splitting
  namespace: default
spec:
  template:
    metadata:
      name: helloworld-traffic-splitting-v2
      annotations:
        autoscaling.knative.dev/min-scale: "3"
    spec:
      containers:
        - image: ealen/echo-server
          env:
            - name: "COMMANDS__HTTPCODE__HEADER"
              value: "201"
  traffic:
    - tag: v1
      revisionName: helloworld-traffic-splitting-v1
      percent: 40
    - tag: v2
      revisionName: helloworld-traffic-splitting-v2
      percent: 60

```

## d. Test the traffic splitting functionality by using a load generator. (For example, use the tool "hey")

```bash
sudo apt install hey
```

```
