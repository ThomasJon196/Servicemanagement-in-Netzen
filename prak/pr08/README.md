# Pods

# Task 1 - Podmanifest

## a. Create a podmanifest for the miniwhoami-service

`miniwhoami-manual.yaml`:

```yml
apiVersion: v1
kind: Pod
metadata:
  name: miniwhoami-manual
spec:
  containers:
  - image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami:latest
    name: miniwhoami
    ports:
    - containerPort: 80
      protocol: TCP
    imagePullPolicy: IfNotPresent
```

## b. Start the pod miniwhoami-manual. How can you retrieve the log-protokols of the running pod?


```bash
# Load image into minikube docker registry
$ minikube image load <image>:<tag>

# Start pod
$ kubectl create -f miniwhoami-manual.yaml

# Show logs
$ kubectl logs miniwhoami-manual
 * Serving Flask app 'index'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (::)
 * Running on http://[::1]:80
 * Running on http://[::1]:80
Press CTRL+C to quit
```

## c. Show Pods yaml-descriptor

```bash
$ kubectl get po miniwhoami-manual -o yaml
```

- qosClass: 'BestEffort'
- Yaml-Deskriptor: Full definition of POD
- `kubectl describe` provides only important information

## d. Is the pod accessible via curl on port 8080?

No. The pod is not mapped to any host-machine-port.

## e. How to access pod via host machine?

```
# port forwarding
kubectl port-forward miniwhoami-manual 8080:80

# get website
curl localhost:8080
```

Portforwarding via kubectl should only be used for development and debugging.

# Task 2 - Labels

## a. Create a pod with labels hochschule: hbrs & sem: ws22

`miniwhoami-manual.yaml`:

```yml
apiVersion: v1
kind: Pod
metadata:
  name: miniwhoami-manual-pod2
  labels:
    hochschule: hbrs
    sem: ws22
spec:
  containers:
  - image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami:latest
    name: miniwhoami
    ports:
    - containerPort: 80
      protocol: TCP
    imagePullPolicy: IfNotPresent
```

```
# Create and Start pod
$ kubectl create -f miniwhoami-manual-pod2.yaml 
```

## b. Display all running pods with labels

```bash
$ kubectl get po --show-labels

NAME                     READY   STATUS    RESTARTS   AGE     LABELS
miniwhoami-manual        1/1     Running   0          15m     <none>
miniwhoami-manual-pod2   1/1     Running   0          3m46s   hochschule=hbrs,sem=ws22
```

## c. Create a POD miniwhoami-manual-pod3 with labels hochschule: th-koeln & sem: ss19

```yml
apiVersion: v1
kind: Pod
metadata:
  name: miniwhoami-manual-pod3
  labels:
    hochschule: th-koeln
    sem: ss19
spec:
  containers:
  - image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami:latest
    name: miniwhoami
    ports:
    - containerPort: 80
      protocol: TCP
    imagePullPolicy: IfNotPresent
```

## d. Display running pods with labels

```
$ kubectl get po --show-labels

NAME                     READY   STATUS    RESTARTS   AGE     LABELS
miniwhoami-manual        1/1     Running   0          20m     <none>
miniwhoami-manual-pod2   1/1     Running   0          8m55s   hochschule=hbrs,sem=ws22
miniwhoami-manual-pod3   1/1     Running   0          6s      hochschule=th-koeln,sem=ss19
```


## e. Change the label of the running pod miniwhoami-manual-pod3 `sem` to `ws22`

```
$ kubectl label po miniwhoami-manual-pod3 sem=ws22 --overwrite

```

## f. Display pods with labels again

```
$ kubectl get po --show-labels

NAME                     READY   STATUS    RESTARTS   AGE   LABELS
miniwhoami-manual        1/1     Running   0          21m   <none>
miniwhoami-manual-pod2   1/1     Running   0          10m   hochschule=hbrs,sem=ws22
miniwhoami-manual-pod3   1/1     Running   0          78s   hochschule=th-koeln,sem=ws22
```

# Task 3 - Namespaces

## a. Create namespace

```
$ kubectl create namespace tjonas2s
```

## b. Which namespaces currently exists?

```
$ kubectl get ns

NAME                   STATUS   AGE
default                Active   3d1h
kube-node-lease        Active   3d1h
kube-public            Active   3d1h
kube-system            Active   3d1h
kubernetes-dashboard   Active   3d1h
tjonas2s               Active   11s
```


## c. Which is the current selected namespace?

Without specifying namespaces `default` namespace is selected.

## d. Move Pod miniwhoami-manual to newly generated namespace

```
kubectl create -f miniwhoami-manual.yaml -n tjonas2s
```

## e. Check if pod is in new namespace

```
$ kubectl get po --namespace tjonas2s

NAME                READY   STATUS    RESTARTS   AGE
miniwhoami-manual   1/1     Running   0          59s
```


## f. Clear whole system.

```
$ kubectl delete all --all
```


# Task 4 - HTTP-Activityprobe

## a. Make the `miniwhoami` service repond with error message after 5 calls

Extended `miniwhoami.py`

```py
if access_counter >= 5:
        return 'Server shutdown', 500
```

## b. Test program localy and push to docker-registry

`docker push docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami-crash:v1`



## c. Create Pod-manifest `miniwhiami-liveness-probe.yaml` which observes the defective container `miniwhoami-crash`.

`miniwhoami-liveness-probe.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: miniwhoami-liveness-probe
spec:
  containers:
  - image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami-crash:v1
    name: miniwhoami-crash
    livenessProbe:
        httpGet:
            path: / 
            port: 80

```

## d. Start liveness-probe Pod. Check how long the pod is running. After how many seconds does the first problem arrise? How can you determine if the pod is terminated?

```
# Start pod
$ kubectl create -f miniwhoami-liveness-probe.yaml


# Check status
$ k get pod

NAME                        READY   STATUS    RESTARTS      AGE
miniwhoami-liveness-probe   1/1     Running   1 (67s ago)   6m17s
```

The liveness-probe automatically restarts the server after a crash is detected. Checks the server state once a minute.

## e. Remove the http-livenessprobe for this subtask from the manifest and restart the pod. Which behavior do you observe?

Without the liveness-probe, the server-crash will not be detected and the server wont be restarted.

## f. How can you display the observed-tasks?

```
$ kubectl describe po miniwhoami-liveness-probe


....


Events:
  Type     Reason     Age                   From               Message
  ----     ------     ----                  ----               -------
  Normal   Scheduled  12m                   default-scheduler  Successfully assigned default/miniwhoami-liveness-probe to minikube
  Warning  Failed     10m (x6 over 12m)     kubelet            Error: ImagePullBackOff
  Normal   Pulling    10m (x4 over 12m)     kubelet            Pulling image "docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami-crash:v1"
  Warning  Failed     10m (x4 over 12m)     kubelet            Failed to pull image "docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami-crash:v1": rpc error: code = Unknown desc = Error response from daemon: Head "https://docker.fslab.de/v2/tjonas2s/servmgmt-ws22/miniwhoami-crash/manifests/v1": denied: access forbidden
  Warning  Failed     10m (x4 over 12m)     kubelet            Error: ErrImagePull
  Normal   BackOff    10m (x7 over 12m)     kubelet            Back-off pulling image "docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami-crash:v1"
  Normal   Pulled     116s (x5 over 8m33s)  kubelet            Container image "docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami-crash:v1" already present on machine
```


# Task 5 - Replication Controller

## a. Create pod manifest `miniwhoami-rc.yaml` with e replication controller which creates 3 miniwhoami pods.

`miniwhoami-rc.yaml`:

```yaml
apiVersion: v1
kind: ReplicationController
metadata: 
    name: miniwhoami-rc
spec:
    replicas: 3
    selector:
        app: miniwhoami
    template:
        metadata:
            labels:
                app: miniwhoami
        spec:
            containers:
            - image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami:latest
              name: miniwhoami
              ports:
              - containerPort: 80
                protocol: TCP
              imagePullPolicy: IfNotPresent
```

```bash
# create
kubectl create -f miniwhoami-rc.yaml 

# show pods
kubectl get po

NAME                  READY   STATUS    RESTARTS   AGE
miniwhoami-rc-brvc4   1/1     Running   0          5s
miniwhoami-rc-dts6d   1/1     Running   0          5s
miniwhoami-rc-gfrr7   1/1     Running   0          5s
```

## b. What happens after a pod is deleted?


```bash
# Delete pod
$ kubectl delete po miniwhoami-rc-brvc4

# Display pods
$ kubectl get pod

NAME                  READY   STATUS        RESTARTS   AGE
miniwhoami-rc-brvc4   1/1     Terminating   0          3m36s
miniwhoami-rc-dts6d   1/1     Running       0          3m36s
miniwhoami-rc-gfrr7   1/1     Running       0          3m36s
miniwhoami-rc-p7v5t   1/1     Running       0          12s
```

After deleting a pod the replication-service automatically start up a new one.

## c. Print describtion of replication-controller

```bash
$ kubectl describe rc miniwhoami-rc

Name:         miniwhoami-rc
Namespace:    default
Selector:     app=miniwhoami
Labels:       app=miniwhoami
Annotations:  <none>
Replicas:     3 current / 3 desired
Pods Status:  3 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  app=miniwhoami
  Containers:
   miniwhoami:
    Image:        docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami:latest
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age    From                    Message
  ----    ------            ----   ----                    -------
  Normal  SuccessfulCreate  4m51s  replication-controller  Created pod: miniwhoami-rc-brvc4
  Normal  SuccessfulCreate  4m51s  replication-controller  Created pod: miniwhoami-rc-dts6d
  Normal  SuccessfulCreate  4m51s  replication-controller  Created pod: miniwhoami-rc-gfrr7
  Normal  SuccessfulCreate  86s    replication-controller  Created pod: miniwhoami-rc-p7v5t
```

The describtion whos information about the replicated pod, how many replications were created and which states the pods are in.

## d. Edit the pod-manifest with an additional label app2: neu. How can this change be applied to a running system?

Added label `app2: neu` to `miniwhoami-rc.yaml`

```
# Apply changes to running configuration
$ kubectl apply -f miniwhoami-rc.yaml
```

## e. Delete one pod and show change in active labels.

```bash
# Show current pod with labels
$ kubectl get po --show-labels

NAME                  READY   STATUS    RESTARTS   AGE   LABELS
miniwhoami-rc-dts6d   1/1     Running   0          11m   app=miniwhoami
miniwhoami-rc-gfrr7   1/1     Running   0          11m   app=miniwhoami
miniwhoami-rc-p7v5t   1/1     Running   0          8m    app=miniwhoami

# Delete pod
$ kubectl delete pod miniwhoami-rc-dts6d


# Show current pod with labels
$ kubectl get po --show-labels

NAME                  READY   STATUS    RESTARTS   AGE     LABELS
miniwhoami-rc-f74vs   1/1     Running   0          34s     app2=neu,app=miniwhoami
miniwhoami-rc-gfrr7   1/1     Running   0          13m     app=miniwhoami
miniwhoami-rc-p7v5t   1/1     Running   0          9m43s   app=miniwhoami

```

The newly created pod gets the updated lables. Already running pods dont have the new labels yet.

## f. Edit the pod manifest. Replace the replication-controller SELECTOR `app: miniwhoami `with `app2: neu`. Apply changes to `miniwhoami-rc`

Replaced `app: miniwhoami` with `app2: neu`.

```
# Display pods
$ kubectl get po --show-labels

NAME                  READY   STATUS    RESTARTS   AGE    LABELS
miniwhoami-rc-f74vs   1/1     Running   0          6m1s   app2=neu,app=miniwhoami
miniwhoami-rc-gfrr7   1/1     Running   0          18m    app=miniwhoami
miniwhoami-rc-p7v5t   1/1     Running   0          15m    app=miniwhoami


# Apply changes
$ kubectl apply -f miniwhoami-rc.yaml

# Display pods
$ kubectl get po --show-labels

NAME                  READY   STATUS    RESTARTS   AGE     LABELS
miniwhoami-rc-f74vs   1/1     Running   0          6m33s   app2=neu,app=miniwhoami
miniwhoami-rc-gfrr7   1/1     Running   0          19m     app=miniwhoami
miniwhoami-rc-jns6m   1/1     Running   0          3s      app2=neu,app=miniwhoami
miniwhoami-rc-p7v5t   1/1     Running   0          15m     app=miniwhoami
miniwhoami-rc-q67pf   1/1     Running   0          3s      app2=neu,app=miniwhoami
```

The `ReplicationController` started 2 new pods with the label `app2: neu`.
Changing the `selector` of the `ReplicationController` to `app2: neu` decouples the previously assigned pods from the controller. 


# Task 6 - ReplicaSet

## a. Clear the system once more and restart miniwhoami-rc.yaml

```bash
# Clear system
kubectl delete all --all

# Start replicationController 
kubectl create -f miniwhoami-rc.yaml 

```

## b. Delete the `ReplicationController` without deleting the created pods.

```bash
# Delete replication controller without deleting created pods
$ kubectl delete rc miniwhoami-rc --cascade=orphan


# Show replication controllers
$ kubectl get rc
No resources found in default namespace.

# Show pods
$ kubectl get po
NAME                  READY   STATUS    RESTARTS   AGE
miniwhoami-rc-g7t2l   1/1     Running   0          113s
miniwhoami-rc-p5sn4   1/1     Running   0          113s
miniwhoami-rc-ww46s   1/1     Running   0          113s
```

## c. Create pod-manifest `miniwhoami-rs.yaml` for a `ReplicaSet` which creates `5` miniwhoami Pods tagged with app: miniwhoami.

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata: 
    name: miniwhoami-rs
spec:
    replicas: 5
    selector:
        matchLabels:
            app: miniwhoami
    template:
        metadata:
            labels:
                app: miniwhoami
        spec:
            containers:
            - image: docker.fslab.de/tjonas2s/servmgmt-ws22/miniwhoami:latest
              name: miniwhoami
              ports:
              - containerPort: 80
                protocol: TCP
              imagePullPolicy: IfNotPresent
```

## d. Check currently running pods. Create the `ReplicaSet` with `miniwhoami-rs.yaml` and check again.

```bash
# show pods
$ kubectl get pods
NAME                  READY   STATUS    RESTARTS   AGE
miniwhoami-rc-g7t2l   1/1     Running   0          6m26s
miniwhoami-rc-p5sn4   1/1     Running   0          6m26s
miniwhoami-rc-ww46s   1/1     Running   0          6m26s


# Create rc
kubectl create -f miniwhoami-rs.yaml 

# show pods
$ kubectl get pods --show-labels
NAME                  READY   STATUS    RESTARTS   AGE     LABELS
miniwhoami-rc-g7t2l   1/1     Running   0          7m54s   app2=neu,app=miniwhoami
miniwhoami-rc-p5sn4   1/1     Running   0          7m54s   app2=neu,app=miniwhoami
miniwhoami-rc-ww46s   1/1     Running   0          7m54s   app2=neu,app=miniwhoami
miniwhoami-rs-8f4xv   1/1     Running   0          75s     app=miniwhoami
miniwhoami-rs-xcgbg   1/1     Running   0          75s     app=miniwhoami
```

## e. Interpret the observations

The `ReplicaSet` identifies 3 already running Pods and creates only 2 additional ones.

## f. Start the `ReplicationController` from the previous task again and intepret observations.

```
# Start replicationController
$ kubectl create -f miniwhoami-rc.yaml 


# Display pods
$ kubectl get pod --show-labels
NAME                  READY   STATUS    RESTARTS   AGE     LABELS
miniwhoami-rc-g7t2l   1/1     Running   0          11m     app2=neu,app=miniwhoami
miniwhoami-rc-p5sn4   1/1     Running   0          11m     app2=neu,app=miniwhoami
miniwhoami-rc-ww46s   1/1     Running   0          11m     app2=neu,app=miniwhoami
miniwhoami-rc-xx2ps   1/1     Running   0          3s      app2=neu,app=miniwhoami
miniwhoami-rc-z2vhx   1/1     Running   0          3s      app2=neu,app=miniwhoami
miniwhoami-rc-z592m   1/1     Running   0          3s      app2=neu,app=miniwhoami
miniwhoami-rs-8f4xv   1/1     Running   0          4m51s   app=miniwhoami
miniwhoami-rs-xcgbg   1/1     Running   0          4m51s   app=miniwhoami

```

The replication controller creates 3 new pods even when 3 pods with the same labels are already running. The `ReplicationController` is thus not checking if pods with the same labels are already deployed.