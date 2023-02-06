# Minikube

# Task 1 - Installation of Minikube

(> v1.25.2)  & Kube-cli (> v1.23.6)

## Install localy 

1. Install KVM - Kernel Virtual Machine [Installation guide](https://linuxhint.com/install-kvm-ubuntu-22-04/)

    Evaluate network drivers if required.

2. Install kube-ctl: [Docs](https://kubernetes.io/de/docs/tasks/tools/install-minikube/)

3. Install minikube: [Docs](https://kubernetes.io/de/docs/tasks/tools/install-minikube/)


## Verify running version

```bash
$ minikube version

minikube version: v1.28.0
commit: 986b1ebd987211ed16f8cc10aed7d2c42fc8392f


$ kubectl version 

Client Version: version.Info{Major:"1", Minor:"25", GitVersion:"v1.25.4", GitCommit:"872a965c6c6526caa949f0c6ac028ef7aff3fb78", GitTreeState:"clean", BuildDate:"2022-11-09T13:36:36Z", GoVersion:"go1.19.3", Compiler:"gc", Platform:"linux/amd64"}
Kustomize Version: v4.5.7
Server Version: version.Info{Major:"1", Minor:"25", GitVersion:"v1.25.3", GitCommit:"434bfd82814af038ad94d62ebe59b133fcb50506", GitTreeState:"clean", BuildDate:"2022-10-12T10:49:09Z", GoVersion:"go1.19.2", Compiler:"gc", Platform:"linux/amd64"}
```

## Start cluster

```bash
$ minikube start

....

$ minikube status 

minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured


$ kubectl get nodes

NAME       STATUS   ROLES           AGE     VERSION
minikube   Ready    control-plane   4m57s   v1.25.3


$ minikube stop

...
```

## Start webbased kubernetes dashboard [Docs](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/)

1. Start dashboard:

```bash
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.6.1/aio/deploy/recommended.yaml


$ kubectl proxy
```

Access via: `http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/`

1. Authentication [Docs](https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md)

`dashboard-adminuser.yaml`:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
```

```bash
kubectl apply -f dashboard-adminuser.yaml       # Apply mainfest

kubectl -n kubernetes-dashboard create token admin-user     # Create token, use to access dashboard
```

## Describe System architecture of minikube

Minikube is a locally running version of kubernetes nested inside a docker-container.
The actual pods are executed inside this docker container.
The architecture of minikube is basically docker inside docker.


# Task 2 - Minikube Setup & Testing

## Enable kubectl = k alias and autocompletion

Add the following to `~/.bashrc` and reload `source ~/bashrc`

```
alias k=kubectl
complete -o default -F __start_kubectl k
```

## Test cluster

```bash
$ k get nodes

NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   36m   v1.25.3

$ k cluster-info 

Kubernetes control plane is running at https://192.168.39.153:8443
CoreDNS is running at https://192.168.39.153:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

```

## Further information


```
$ k describe nodes minikube
```

<details>
    </br>
    
        Name:               minikube
        Roles:              control-plane
        Labels:             beta.kubernetes.io/arch=amd64
                            beta.kubernetes.io/os=linux
                            kubernetes.io/arch=amd64
                            kubernetes.io/hostname=minikube
                            kubernetes.io/os=linux
                            minikube.k8s.io/commit=986b1ebd987211ed16f8cc10aed7d2c42fc8392f
                            minikube.k8s.io/name=minikube
                            minikube.k8s.io/primary=true
                            minikube.k8s.io/updated_at=2022_11_28T13_17_05_0700
                            minikube.k8s.io/version=v1.28.0
                            node-role.kubernetes.io/control-plane=
                            node.kubernetes.io/exclude-from-external-load-balancers=
        Annotations:        kubeadm.alpha.kubernetes.io/cri-socket: unix:///var/run/cri-dockerd.sock
                            node.alpha.kubernetes.io/ttl: 0
                            volumes.kubernetes.io/controller-managed-attach-detach: true
        CreationTimestamp:  Mon, 28 Nov 2022 13:17:02 +0100
        Taints:             <none>
        Unschedulable:      false
        Lease:
        HolderIdentity:  minikube
        AcquireTime:     <unset>
        RenewTime:       Mon, 28 Nov 2022 13:54:45 +0100
        Conditions:
        Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
        ----             ------  -----------------                 ------------------                ------                       -------
        MemoryPressure   False   Mon, 28 Nov 2022 13:52:06 +0100   Mon, 28 Nov 2022 13:17:01 +0100   KubeletHasSufficientMemory   kubelet has sufficient memory available
        DiskPressure     False   Mon, 28 Nov 2022 13:52:06 +0100   Mon, 28 Nov 2022 13:17:01 +0100   KubeletHasNoDiskPressure     kubelet has no disk pressure
        PIDPressure      False   Mon, 28 Nov 2022 13:52:06 +0100   Mon, 28 Nov 2022 13:17:01 +0100   KubeletHasSufficientPID      kubelet has sufficient PID available
        Ready            True    Mon, 28 Nov 2022 13:52:06 +0100   Mon, 28 Nov 2022 13:17:05 +0100   KubeletReady                 kubelet is posting ready status
        Addresses:
        InternalIP:  192.168.39.153
        Hostname:    minikube
        Capacity:
        cpu:                2
        ephemeral-storage:  17784752Ki
        hugepages-2Mi:      0
        memory:             5823240Ki
        pods:               110
        Allocatable:
        cpu:                2
        ephemeral-storage:  17784752Ki
        hugepages-2Mi:      0
        memory:             5823240Ki
        pods:               110
        System Info:
        Machine ID:                 c17d4c463e814d02abc95ae38cff2918
        System UUID:                c17d4c46-3e81-4d02-abc9-5ae38cff2918
        Boot ID:                    a183d048-9bdd-49f2-a386-d95fc7c95165
        Kernel Version:             5.10.57
        OS Image:                   Buildroot 2021.02.12
        Operating System:           linux
        Architecture:               amd64
        Container Runtime Version:  docker://20.10.20
        Kubelet Version:            v1.25.3
        Kube-Proxy Version:         v1.25.3
        PodCIDR:                      10.244.0.0/24
        PodCIDRs:                     10.244.0.0/24
        Non-terminated Pods:          (9 in total)
        Namespace                   Name                                          CPU Requests  CPU Limits  Memory Requests  Memory Limits  Age
        ---------                   ----                                          ------------  ----------  ---------------  -------------  ---
        kube-system                 coredns-565d847f94-zgmvz                      100m (5%)     0 (0%)      70Mi (1%)        170Mi (2%)     37m
        kube-system                 etcd-minikube                                 100m (5%)     0 (0%)      100Mi (1%)       0 (0%)         37m
        kube-system                 kube-apiserver-minikube                       250m (12%)    0 (0%)      0 (0%)           0 (0%)         37m
        kube-system                 kube-controller-manager-minikube              200m (10%)    0 (0%)      0 (0%)           0 (0%)         37m
        kube-system                 kube-proxy-lbgtk                              0 (0%)        0 (0%)      0 (0%)           0 (0%)         37m
        kube-system                 kube-scheduler-minikube                       100m (5%)     0 (0%)      0 (0%)           0 (0%)         37m
        kube-system                 storage-provisioner                           0 (0%)        0 (0%)      0 (0%)           0 (0%)         37m
        kubernetes-dashboard        dashboard-metrics-scraper-64bcc67c9c-8sqr7    0 (0%)        0 (0%)      0 (0%)           0 (0%)         29m
        kubernetes-dashboard        kubernetes-dashboard-66c887f759-c2vbh         0 (0%)        0 (0%)      0 (0%)           0 (0%)         29m
        Allocated resources:
        (Total limits may be over 100 percent, i.e., overcommitted.)
        Resource           Requests    Limits
        --------           --------    ------
        cpu                750m (37%)  0 (0%)
        memory             170Mi (2%)  170Mi (2%)
        ephemeral-storage  0 (0%)      0 (0%)
        hugepages-2Mi      0 (0%)      0 (0%)
        Events:
        Type    Reason                   Age                From             Message
        ----    ------                   ----               ----             -------
        Normal  Starting                 37m                kube-proxy       
        Normal  Starting                 29m                kube-proxy       
        Normal  Starting                 37m                kubelet          Starting kubelet.
        Normal  NodeHasSufficientMemory  37m (x3 over 37m)  kubelet          Node minikube status is now: NodeHasSufficientMemory
        Normal  NodeHasNoDiskPressure    37m (x3 over 37m)  kubelet          Node minikube status is now: NodeHasNoDiskPressure
        Normal  NodeHasSufficientPID     37m (x3 over 37m)  kubelet          Node minikube status is now: NodeHasSufficientPID
        Normal  NodeAllocatableEnforced  37m                kubelet          Updated Node Allocatable limit across pods
        Normal  NodeHasNoDiskPressure    37m                kubelet          Node minikube status is now: NodeHasNoDiskPressure
        Normal  NodeAllocatableEnforced  37m                kubelet          Updated Node Allocatable limit across pods
        Normal  NodeHasSufficientMemory  37m                kubelet          Node minikube status is now: NodeHasSufficientMemory
        Normal  NodeHasSufficientPID     37m                kubelet          Node minikube status is now: NodeHasSufficientPID
        Normal  NodeReady                37m                kubelet          Node minikube status is now: NodeReady
        Normal  Starting                 37m                kubelet          Starting kubelet.
        Normal  RegisteredNode           37m                node-controller  Node minikube event: Registered Node minikube in Controller
        Normal  Starting                 29m                kubelet          Starting kubelet.
        Normal  NodeHasSufficientMemory  29m (x8 over 29m)  kubelet          Node minikube status is now: NodeHasSufficientMemory
        Normal  NodeHasNoDiskPressure    29m (x8 over 29m)  kubelet          Node minikube status is now: NodeHasNoDiskPressure
        Normal  NodeHasSufficientPID     29m (x7 over 29m)  kubelet          Node minikube status is now: NodeHasSufficientPID
        Normal  NodeAllocatableEnforced  29m                kubelet          Updated Node Allocatable limit across pods
        Normal  RegisteredNode           29m                node-controller  Node minikube event: Registered Node minikube in Controller
    

</details>
Contains information about:
- General information (lables, creationtime, identities)
- System Resources
- Running pods
- Events


## Run Image/Container as Pod 

[Blog](https://medium.com/swlh/how-to-run-locally-built-docker-images-in-kubernetes-b28fbc32cc1d)

```bash
$ k run miniserver --image miniserver           # Run & Create pod

$ k get pods

NAME          READY   STATUS              RESTARTS   AGE
miniserver2   0/1     ErrImagePull        0          11s
```
> Problem: Image Pull source is not specified (Default remote)

```bash
$ k run miniserver --image miniserver --image-pull-policy Never

$ k get pods

NAME          READY   STATUS              RESTARTS   AGE
miniserver    0/1     ErrImageNeverPull   0          5m44s
```
> Problem: Minikube node uses own docker-repository which is not connected to current docker registry.

```bash
$ minikube docker-env                           # Print minikube docker-repo

$ eval $(minikube -p minikube docker-env)       # Point Docker deamon to current minikube internal Docker registry (only temporary exported variables!)

$ docker build . -t miniwhoami                  # Build images in new registry

$ k run miniwhoami --image miniwhoami --image-pull-policy Never

$ k get pods 

NAME          READY   STATUS         RESTARTS   AGE
miniwhoami2   1/1     Running        0          3s

! POD IS RUNNING !
```

## Show information about running pod

```bash
$ k describe pods miniwhoami


Name:             miniwhoami
Namespace:        default
Priority:         0
Service Account:  default
Node:             minikube/192.168.39.153
Start Time:       Mon, 28 Nov 2022 14:22:29 +0100
Labels:           run=miniwhoami
Annotations:      <none>
Status:           Pending
IP:               172.17.0.5
IPs:
  IP:  172.17.0.5
Containers:
  miniwhoami:
    Container ID:   
    Image:          miniserver
    Image ID:       
    Port:           <none>
    Host Port:      <none>
    State:          Waiting
      Reason:       ImagePullBackOff
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-tdk5z (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
Volumes:
  kube-api-access-tdk5z:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age                  From               Message
  ----     ------     ----                 ----               -------
  Normal   Scheduled  2m48s                default-scheduler  Successfully assigned default/miniwhoami to minikube
  Normal   Pulling    78s (x4 over 2m48s)  kubelet            Pulling image "miniserver"
  Warning  Failed     76s (x4 over 2m46s)  kubelet            Failed to pull image "miniserver": rpc error: code = Unknown desc = Error response from daemon: pull access denied for miniserver, repository does not exist or may require 'docker login': denied: requested access to the resource is denied
  Warning  Failed     76s (x4 over 2m46s)  kubelet            Error: ErrImagePull
  Warning  Failed     53s (x6 over 2m46s)  kubelet            Error: ImagePullBackOff
  Normal   BackOff    40s (x7 over 2m46s)  kubelet            Back-off pulling image "miniserver"

```

##  Delete pod

```
$ k delete pod miniwhoami
```