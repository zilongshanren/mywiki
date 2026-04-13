---
title: 一步步打造基于Kubeadm的高可用Kubernetes集群-第一部分
url: https://tonybai.com/2017/05/15/setup-a-ha-kubernetes-cluster-based-on-kubeadm-part1/
published: '2017-05-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一步步打造基于Kubeadm的高可用Kubernetes集群-第一部分

[Kubernetes集群](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)的核心是其[master node](http://tonybai.com/2017/01/24/explore-kubernetes-cluster-installed-by-kubeadm/)，但目前默认情况下master node只有一个，一旦master node出现问题，[Kubernetes集群](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)将陷入“瘫痪”，对[集群的管理](http://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster/)、Pod的调度等均将无法实施，即便此时某些用户的Pod依旧可以正常运行。这显然不能符合我们对于运行于生产环境下的Kubernetes集群的要求，我们需要一个高可用的Kubernetes集群。

不过，目前[Kubernetes官方](https://kubernetes.io)针对构建高可用(high-availability)的集群的支持还是非常有限的，只是针对少数cloud-provider提供了粗糙的部署方法，比如：[使用kube-up.sh脚本在GCE上](https://kubernetes.io/docs/tasks/administer-cluster/highly-available-master/)、[使用kops在AWS上](https://kubernetes.io/docs/getting-started-guides/kops/)等等。

高可用Kubernetes集群是Kubernetes演进的必然方向，官方在“[Building High-Availability Clusters](https://kubernetes.io/docs/admin/high-availability/)”一文中给出了当前搭建HA cluster的粗略思路。[Kubeadm](https://github.com/kubernetes/kubeadm)也将HA列入了后续版本的[里程碑计划](https://github.com/kubernetes/kubeadm/issues/261)，并且已经出了一版[使用kubeadm部署高可用cluster的方法提议草案](https://docs.google.com/document/d/1lH9OKkFZMSqXCApmSXemEDuy9qlINdm5MfWWGrK3JYc/edit#heading=h.8hdxw3quu67g)。

在kubeadm没有真正支持自动bootstrap的HA Kubernetes cluster之前，如果要搭建一个HA k8s cluster，我们应该如何做呢？本文将探索性地一步一步的给出打造一个HA K8s cluster的思路和具体步骤。**不过需要注意的是：这里搭建的HA k8s cluser仅在实验室中测试ok，还并未在生产环境中run过，因此在某些未知的细节方面可能存在思路上的纰漏**。

## 一、测试环境

高可用Kubernetes集群主要就是master node的高可用，因此，我们申请了三台美国西部区域的阿里云ECS作为三个master节点。通过[hostnamectl](http://tonybai.com/2017/05/09/exception-caused-by-kubernetes-node-hostname-change/)将这三个节点的static hostname分别改为shaolin、wudang和emei：

```
shaolin: 10.27.53.32
wudang: 10.24.138.208
emei: 10.27.52.72
```


三台主机运行的都是[Ubuntu](http://tonybai.com/tag/ubuntu) 16.04.2 LTS (GNU/Linux 4.4.0-63-generic x86_64)，使用root用户。

Docker版本如下：

```
root@shaolin:~# docker version
Client:
Version: 17.03.1-ce
API version: 1.27
Go version: go1.7.5
Git commit: c6d412e
Built: Mon Mar 27 17:14:09 2017
OS/Arch: linux/amd64
Server:
Version: 17.03.1-ce
API version: 1.27 (minimum version 1.12)
Go version: go1.7.5
Git commit: c6d412e
Built: Mon Mar 27 17:14:09 2017
OS/Arch: linux/amd64
Experimental: false
```


Ubuntu上[Docker CE版本](https://www.docker.com/community-edition)的安装步骤可以参看[这里](https://store.docker.com/editions/community/docker-ce-server-ubuntu?tab=description)，由于我的服务器在美西，因此不存在”墙”的问题。对于主机在国内的朋友，你需要根据安装过程中是否输出错误日志自行决定是否需要配置一个加速器。另外，这里用的docker版本有些新，Kubernetes官网上提及最多的、兼容最好的还是[docker 1.12.x版本](https://github.com/moby/moby/releases/tag/v1.12.5)，你也可以直接安装这个版本。

## 二、Master节点高可用的思路

通过[对single-master node的探索](http://tonybai.com/2017/01/24/explore-kubernetes-cluster-installed-by-kubeadm/)，我们知道master节点上运行着如下几个Kubernetes组件：

- kube-apiserver：集群核心，集群API接口、集群各个组件通信的中枢；集群安全控制；
- etcd：集群的数据中心；
- kube-scheduler：集群Pod的调度中心；
- kube-controller-manager：集群状态管理器，当集群状态与期望不同时，kcm会努力让集群恢复期望状态，比如：当一个pod死掉，kcm会努力新建一个pod来恢复对应replicas set期望的状态；
- kubelet: kubernetes node agent，负责与node上的
[docker engine](http://tonybai.com/tag/docke)打交道； - kubeproxy: 每个node上一个，负责service vip到endpoint pod的流量转发，当前主要通过设置iptables规则实现。

Kubernetes集群的高可用就是master节点的高可用，master节点的高可用归根结底就是上述这些运行于master node上的组件的高可用。因此，我们的思路就是考量如何让这些组件高可用起来！综合Kubernetes官方提供的资料以及一些proposal draft，我们知道完全从头搭建的[hard way形式](https://github.com/kelseyhightower/kubernetes-the-hard-way)似乎不甚理智^0^，将一个由kubeadm创建的k8s cluster改造为一个ha的k8s cluster似乎更可行。下面是我的思路方案：

![img{512x368}](../../assets/f1bea3d47029365e.png)


前面提到过，我们的思路是基于kubeadm启动的kubernetes集群，通过逐步修改配置或替换，形成最终HA的k8s cluster。上图是k8s ha cluster的最终图景，我们可以看到：

- kube-apiserver：得益于apiserver的无状态，每个master节点的apiserver都是active的，并处理来自Load Balance分配过来的流量；
- etcd：状态的集中存储区。通过将多个master节点上的etcd组成一个etcd集群，使得apiserver共享集群状态和数据；
- kube-controller-manager：kcm自带leader-elected功能，多个master上的kcm构成一个集群，但只有被elected为leader的kcm在工作。每个master节点上的kcm都连接本node上的apiserver；
- kube-scheduler：scheduler自带leader-elected功能，多个master上的scheduler构成一个集群，但只有被elected为leader的scheduler在工作。每个master节点上的scheduler都连接本node上的apiserver；
- kubelet: 由于master上的各个组件均以container的形式呈现，因此不承担workload的master节点上的kubelet更多是用来管理这些master组件容器。每个master节点上的kubelet都连接本node上的apiserver；
- kube-proxy: 由于master节点不承载workload，因此master节点上的kube-proxy同样仅服务于一些特殊的服务，比如: kube-dns等。由于kubeadm下kube-proxy没有暴露出可供外部调整的配置，因此kube-proxy需要连接Load Balance暴露的apiserver的端口。

接下来，我们就来一步步按照我们的思路，对kubeadm启动的single-master node k8s cluster进行改造，逐步演进到我们期望的ha cluster状态。

## 三、第一步：使用kubeadm安装single-master k8s cluster

距离第一次[使用kubeadm安装kubernetes 1.5.1集群](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)已经有一些日子了，kubernetes和kubeadm都有了一些变化。当前kubernetes和kubeadm的最新release版都是1.6.2版本：

```
root@wudang:~# kubeadm version
kubeadm version: version.Info{Major:"1", Minor:"6", GitVersion:"v1.6.2", GitCommit:"477efc3cbe6a7effca06bd1452fa356e2201e1ee", GitTreeState:"clean", BuildDate:"2017-04-19T20:22:08Z", GoVersion:"go1.7.5", Compiler:"gc", Platform:"linux/amd64"}
root@wudang:~# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
gcr.io/google_containers/kube-proxy-amd64 v1.6.2 7a1b61b8f5d4 3 weeks ago 109 MB
gcr.io/google_containers/kube-controller-manager-amd64 v1.6.2 c7ad09fe3b82 3 weeks ago 133 MB
gcr.io/google_containers/kube-apiserver-amd64 v1.6.2 e14b1d5ee474 3 weeks ago 151 MB
gcr.io/google_containers/kube-scheduler-amd64 v1.6.2 b55f2a2481b9 3 weeks ago 76.8 MB
... ...
```


虽然kubeadm版本有更新，但安装过程没有太多变化，这里仅列出一些关键步骤，一些详细信息输出就在这里省略了。

我们先在shaolin node上安装相关程序文件：

```
root@shaolin:~# apt-get update && apt-get install -y apt-transport-https
root@shaolin:~# curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
OK
root@shaolin:~# cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
> deb http://apt.kubernetes.io/ kubernetes-xenial main
> EOF
root@shaolin:~# apt-get update
root@shaolin:~# apt-get install -y kubelet kubeadm kubectl kubernetes-cni
```


接下来，使用kubeadm启动集群。注意：由于在aliyun上[flannel](https://github.com/coreos/flannel) 网络插件一直不好用，这里还是使用[weave network](https://www.weave.works)。

```
root@shaolin:~/k8s-install# kubeadm init --apiserver-advertise-address 10.27.53.32
[kubeadm] WARNING: kubeadm is in beta, please do not use it for production clusters.
[init] Using Kubernetes version: v1.6.2
[init] Using Authorization mode: RBAC
[preflight] Running pre-flight checks
[preflight] WARNING: docker version is greater than the most recently validated version. Docker version: 17.03.1-ce. Max validated version: 1.12
[preflight] Starting the kubelet service
[certificates] Generated CA certificate and key.
[certificates] Generated API server certificate and key.
[certificates] API Server serving cert is signed for DNS names [shaolin kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 10.27.53.32]
[certificates] Generated API server kubelet client certificate and key.
[certificates] Generated service account token signing key and public key.
[certificates] Generated front-proxy CA certificate and key.
[certificates] Generated front-proxy client certificate and key.
[certificates] Valid certificates and keys now exist in "/etc/kubernetes/pki"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/admin.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/controller-manager.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/scheduler.conf"
[apiclient] Created API client, waiting for the control plane to become ready
[apiclient] All control plane components are healthy after 17.045449 seconds
[apiclient] Waiting for at least one node to register
[apiclient] First node has registered after 5.008588 seconds
[token] Using token: a8dd42.afdb86eda4a8c987
[apiconfig] Created RBAC rules
[addons] Created essential addon: kube-proxy
[addons] Created essential addon: kube-dns
Your Kubernetes master has initialized successfully!
To start using your cluster, you need to run (as a regular user):
sudo cp /etc/kubernetes/admin.conf $HOME/
sudo chown $(id -u):$(id -g) $HOME/admin.conf
export KUBECONFIG=$HOME/admin.conf
You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
http://kubernetes.io/docs/admin/addons/
You can now join any number of machines by running the following on each node
as root:
kubeadm join --token abcdefghijklmn 10.27.53.32:6443
root@shaolin:~/k8s-install# pods
NAMESPACE NAME READY STATUS RESTARTS AGE IP NODE
kube-system etcd-shaolin 1/1 Running 0 34s 10.27.53.32 shaolin
kube-system kube-apiserver-shaolin 1/1 Running 0 35s 10.27.53.32 shaolin
kube-system kube-controller-manager-shaolin 1/1 Running 0 23s 10.27.53.32 shaolin
kube-system kube-dns-3913472980-tkr91 0/3 Pending 0 1m <none>
kube-system kube-proxy-bzvvk 1/1 Running 0 1m 10.27.53.32 shaolin
kube-system kube-scheduler-shaolin 1/1 Running 0 46s 10.27.53.32 shaolin
```


k8s 1.6.2版本的weave network的安装与之前稍有不同，因为k8s 1.6启用了更为安全的机制，默认采用[RBAC](http://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster/)对运行于cluster上的workload进行有限授权。我们要使用的weave network plugin的yaml为[weave-daemonset-k8s-1.6.yaml](https://github.com/weaveworks/weave/releases/download/latest_release/weave-daemonset-k8s-1.6.yaml)：

```
root@shaolin:~/k8s-install# kubectl apply -f https://git.io/weave-kube-1.6
clusterrole "weave-net" created
serviceaccount "weave-net" created
clusterrolebinding "weave-net" created
daemonset "weave-net" created
```


如果你的weave pod启动失败且原因类似如下日志：

```
Network 172.30.0.0/16 overlaps with existing route 172.16.0.0/12 on host.
```


你需要修改你的weave network的 IPALLOC_RANGE(这里我使用了172.32.0.0/16)：

```
//weave-daemonset-k8s-1.6.yaml
... ...
spec:
template:
metadata:
labels:
name: weave-net
spec:
hostNetwork: true
hostPID: true
containers:
- name: weave
env:
- name: IPALLOC_RANGE
value: 172.32.0.0/16
... ...
```


master安装ok后，我们将wudang、emei两个node作为k8s minion node，来测试一下cluster的搭建是否是正确的，同时这一过程也在wudang、emei上安装上了kubelet和kube-proxy，这两个组件在后续的“改造”过程中是可以直接使用的：

```
以emei node为例：
root@emei:~# kubeadm join --token abcdefghijklmn 10.27.53.32:6443
[kubeadm] WARNING: kubeadm is in beta, please do not use it for production clusters.
[preflight] Running pre-flight checks
[preflight] WARNING: docker version is greater than the most recently validated version. Docker version: 17.03.1-ce. Max validated version: 1.12
[preflight] Starting the kubelet service
[discovery] Trying to connect to API Server "10.27.53.32:6443"
[discovery] Created cluster-info discovery client, requesting info from "https://10.27.53.32:6443"
[discovery] Cluster info signature and contents are valid, will use API Server "https://10.27.53.32:6443"
[discovery] Successfully established connection with API Server "10.27.53.32:6443"
[bootstrap] Detected server version: v1.6.2
[bootstrap] The server supports the Certificates API (certificates.k8s.io/v1beta1)
[csr] Created API client to obtain unique certificate for this node, generating keys and certificate signing request
[csr] Received signed certificate from the API server, generating KubeConfig...
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/kubelet.conf"
Node join complete:
* Certificate signing request sent to master and response
received.
* Kubelet informed of new secure connection details.
Run 'kubectl get nodes' on the master to see this machine join.
```


建立一个多pod的nginx服务，测试一下集群网络是否通！这里就不赘述了。

安装后的single-master kubernetes cluster的状态就如下图所示：

![img{512x368}](../../assets/99effc261eef3dfd.png)


## 四、第二步：搭建etcd cluster for ha k8s cluster

k8s集群状态和数据都存储在etcd中，高可用的k8s集群离不开高可用的etcd cluster。我们需要为最终的ha k8s cluster提供一个ha的etcd cluster，如何做呢？

当前k8s cluster中，shaolin master node上的etcd存储着k8s集群的所有数据和状态。我们需要在wudang和emei两个节点上也建立起etcd实例，与现存在 etcd共同构建成为高可用的且存储有cluster数据和状态的集群。我们将这一过程再细化为几个小步骤：

### 0、在emei、wudang两个节点上启动kubelet服务

etcd cluster可以采用完全独立的、与k8s组件无关的建立方法。不过这里我采用的是和master一样的方式，即采用由wudang和emei两个node上kubelet启动的etcd作为etcd cluster的两个member。此时，wudang和emei两个node的角色是k8s minion node，我们需要首先清理一下这两个node的数据：

```
root@shaolin:~/k8s-install # kubectl drain wudang --delete-local-data --force --ignore-daemonsets
node "wudang" cordoned
WARNING: Ignoring DaemonSet-managed pods: kube-proxy-mxwp3, weave-net-03jbh; Deleting pods with local storage: weave-net-03jbh
pod "my-nginx-2267614806-fqzph" evicted
node "wudang" drained
root@wudang:~# kubeadm reset
[preflight] Running pre-flight checks
[reset] Stopping the kubelet service
[reset] Unmounting mounted directories in "/var/lib/kubelet"
[reset] Removing kubernetes-managed containers
[reset] No etcd manifest found in "/etc/kubernetes/manifests/etcd.yaml", assuming external etcd.
[reset] Deleting contents of stateful directories: [/var/lib/kubelet /etc/cni/net.d /var/lib/dockershim]
[reset] Deleting contents of config directories: [/etc/kubernetes/manifests /etc/kubernetes/pki]
[reset] Deleting files: [/etc/kubernetes/admin.conf /etc/kubernetes/kubelet.conf /etc/kubernetes/controller-manager.conf /etc/kubernetes/scheduler.conf]
root@shaolin:~/k8s-install # kubectl drain emei --delete-local-data --force --ignore-daemonsets
root@emei:~# kubeadm reset
root@shaolin:~/k8s-install# kubectl delete node/wudang
root@shaolin:~/k8s-install# kubectl delete node/emei
```


我们的小目标中：etcd cluster将由各个node上的kubelet自动启动；而kubelet则是由systemd在sys init时启动，且其启动配置如下：

```
root@wudang:~# cat /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
[Service]
Environment="KUBELET_KUBECONFIG_ARGS=--kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true"
Environment="KUBELET_SYSTEM_PODS_ARGS=--pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true"
Environment="KUBELET_NETWORK_ARGS=--network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin"
Environment="KUBELET_DNS_ARGS=--cluster-dns=10.96.0.10 --cluster-domain=cluster.local"
Environment="KUBELET_AUTHZ_ARGS=--authorization-mode=Webhook --client-ca-file=/etc/kubernetes/pki/ca.crt"
ExecStart=
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_SYSTEM_PODS_ARGS $KUBELET_NETWORK_ARGS $KUBELET_DNS_ARGS $KUBELET_AUTHZ_ARGS $KUBELET_EXTRA_ARGS
```


我们需要首先在wudang和emei node上将kubelet启动起来，我们以wudang node为例：

```
root@wudang:~# systemctl enable kubelet
root@wudang:~# systemctl start kubelet
```


查看kubelet service日志：

```
root@wudang:~# journalctl -u kubelet -f
May 10 10:58:41 wudang systemd[1]: Started kubelet: The Kubernetes Node Agent.
May 10 10:58:41 wudang kubelet[27179]: I0510 10:58:41.798507 27179 feature_gate.go:144] feature gates: map[]
May 10 10:58:41 wudang kubelet[27179]: error: failed to run Kubelet: invalid kubeconfig: stat /etc/kubernetes/kubelet.conf: no such file or directory
May 10 10:58:41 wudang systemd[1]: kubelet.service: Main process exited, code=exited, status=1/FAILURE
May 10 10:58:41 wudang systemd[1]: kubelet.service: Unit entered failed state.
May 10 10:58:41 wudang systemd[1]: kubelet.service: Failed with result 'exit-code'.
```


kubelet启动失败，因为缺少/etc/kubernetes/kubelet.conf这个配置文件。我们需要向shaolin node求援，我们需要将shaolin node上的同名配置文件copy到wudang和emei两个node下面，当然同时需要copy的还包括shaolin node上的/etc/kubernetes/pki目录：

```
root@wudang:~# kubectl --kubeconfig=/etc/kubernetes/kubelet.conf config view
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: REDACTED
server: https://10.27.53.32:6443
name: kubernetes
contexts:
- context:
cluster: kubernetes
user: system:node:shaolin
name: system:node:shaolin@kubernetes
current-context: system:node:shaolin@kubernetes
kind: Config
preferences: {}
users:
- name: system:node:shaolin
user:
client-certificate-data: REDACTED
client-key-data: REDACTED
root@wudang:~# ls /etc/kubernetes/pki
apiserver.crt apiserver-kubelet-client.crt ca.crt ca.srl front-proxy-ca.key front-proxy-client.key sa.pub
apiserver.key apiserver-kubelet-client.key ca.key front-proxy-ca.crt front-proxy-client.crt sa.key
```


systemctl daemon-reload; systemctl restart kubelet后，再查看kubelet service日志，你会发现kubelet起来了！

```
以wudang node为例：
root@wudang:~# journalctl -u kubelet -f
-- Logs begin at Mon 2017-05-08 15:12:01 CST. --
May 11 10:37:07 wudang kubelet[26907]: I0511 10:37:07.213529 26907 factory.go:54] Registering systemd factory
May 11 10:37:07 wudang kubelet[26907]: I0511 10:37:07.213674 26907 factory.go:86] Registering Raw factory
May 11 10:37:07 wudang kubelet[26907]: I0511 10:37:07.213813 26907 manager.go:1106] Started watching for new ooms in manager
May 11 10:37:07 wudang kubelet[26907]: I0511 10:37:07.216383 26907 oomparser.go:185] oomparser using systemd
May 11 10:37:07 wudang kubelet[26907]: I0511 10:37:07.217415 26907 manager.go:288] Starting recovery of all containers
May 11 10:37:07 wudang kubelet[26907]: I0511 10:37:07.285428 26907 manager.go:293] Recovery completed
May 11 10:37:07 wudang kubelet[26907]: I0511 10:37:07.344425 26907 kubelet_node_status.go:230] Setting node annotation to enable volume controller attach/detach
May 11 10:37:07 wudang kubelet[26907]: E0511 10:37:07.356188 26907 eviction_manager.go:214] eviction manager: unexpected err: failed GetNode: node 'wudang' not found
May 11 10:37:07 wudang kubelet[26907]: I0511 10:37:07.358402 26907 kubelet_node_status.go:77] Attempting to register node wudang
May 11 10:37:07 wudang kubelet[26907]: I0511 10:37:07.363083 26907 kubelet_node_status.go:80] Successfully registered node wudang
```


此时此刻，我们先让wudang、emei node上的kubelet先连着shaolin node上的apiserver。

### 1、在emei、wudang两个节点上建立一个etcd cluster

我们以shaolin node上的/etc/kubernetes/manifests/etcd.yaml为蓝本，修改出wudang和emei上的etcd.yaml，主要的变化在于containers:command部分：

```
wudang上的/etc/kubernetes/manifests/etcd.yaml：
spec:
containers:
- command:
- etcd
- --name=etcd-wudang
- --initial-advertise-peer-urls=http://10.24.138.208:2380
- --listen-peer-urls=http://10.24.138.208:2380
- --listen-client-urls=http://10.24.138.208:2379,http://127.0.0.1:2379
- --advertise-client-urls=http://10.24.138.208:2379
- --initial-cluster-token=etcd-cluster
- --initial-cluster=etcd-wudang=http://10.24.138.208:2380,etcd-emei=http://10.27.52.72:2380
- --initial-cluster-state=new
- --data-dir=/var/lib/etcd
image: gcr.io/google_containers/etcd-amd64:3.0.17
emei上的/etc/kubernetes/manifests/etcd.yaml：
spec:
containers:
- command:
- etcd
- --name=etcd-emei
- --initial-advertise-peer-urls=http://10.27.52.72:2380
- --listen-peer-urls=http://10.27.52.72:2380
- --listen-client-urls=http://10.27.52.72:2379,http://127.0.0.1:2379
- --advertise-client-urls=http://10.27.52.72:2379
- --initial-cluster-token=etcd-cluster
- --initial-cluster=etcd-emei=http://10.27.52.72:2380,etcd-wudang=http://10.24.138.208:2380
- --initial-cluster-state=new
- --data-dir=/var/lib/etcd
image: gcr.io/google_containers/etcd-amd64:3.0.17
```


将这两个文件分别放入各自node的/etc/kubernetes/manifests目录后，各自node上的kubelet将会自动将对应的etcd pod启动起来！

```
root@shaolin:~# pods
NAMESPACE NAME READY STATUS RESTARTS AGE IP NODE
kube-system etcd-emei 1/1 Running 0 11s 10.27.52.72 emei
kube-system etcd-shaolin 1/1 Running 0 25m 10.27.53.32 shaolin
kube-system etcd-wudang 1/1 Running 0 24s 10.24.138.208 wudang
```


我们查看一下当前etcd cluster的状态：

```
# etcdctl endpoint status --endpoints=10.27.52.72:2379,10.24.138.208:2379
10.27.52.72:2379, 6e80adf8cd57f826, 3.0.17, 25 kB, false, 17, 660
10.24.138.208:2379, f3805d1ab19c110b, 3.0.17, 25 kB, true, 17, 660
注：输出的列从左到右分别表示：endpoint URL, ID, version, database size, leadership status, raft term, and raft status.
因此，我们可以看出wudang(10.24.138.208)上的etcd被选为cluster leader了
```


我们测试一下etcd cluster，put一些key：

```
在wudang节点：(注意：export ETCDCTL_API=3)
root@wudang:~# etcdctl put foo bar
OK
root@wudang:~# etcdctl put foo1 bar1
OK
root@wudang:~# etcdctl get foo
foo
bar
在emei节点：
root@emei:~# etcdctl get foo
foo
bar
```


至此，当前kubernetes cluster的状态示意图如下：

![img{512x368}](../../assets/d0ef384d0f79181c.png)


### 2、同步shaolin上etcd的数据到etcd cluster中

kubernetes 1.6.2版本默认使用3.x版本etcd。etcdctl 3.x版本提供了一个make-mirror功能用于在etcd cluster间同步数据，这样我们就可以通过etcdctl make-mirror将shaolin上etcd的k8s cluster数据同步到上述刚刚创建的etcd cluster中。在emei node上执行下面命令：

```
root@emei:~# etcdctl make-mirror --no-dest-prefix=true 127.0.0.1:2379 --endpoints=10.27.53.32:2379 --insecure-skip-tls-verify=true
... ...
261
302
341
380
420
459
498
537
577
616
655
... ...
```


etcdctl make-mirror每隔30s输出一次日志，不过通过这些日志无法看出来同步过程。并且etcdctl make-mirror似乎是流式同步：没有结束的边界。因此你需要手工判断一下数据是否都同步过去了！比如通过查看某个key，对比两边的差异的方式：

```
# etcdctl get --from-key /api/v2/registry/clusterrolebindings/cluster-admin
.. ..
compact_rev_key
122912
```


或者通过endpoint status命令查看数据库size大小，对比双方的size是否一致。一旦差不多了，就可以停掉make-mirror的执行了！

### 3、将shaolin上的apiserver连接的etcd改为连接etcd cluster，停止并删除shaolin上的etcd

修改shaolin node上的/etc/kubernetes/manifests/kube-apiserver.yaml，让shaolin上的kube0-apiserver连接到emei node上的etcd：

```
修改下面一行：
- --etcd-servers=http://10.27.52.72:2379
```


修改保存后，kubelet会自动重启kube-apiserver，重启后的kube-apiserver工作正常！

接下来，我们停掉并删除掉shaolin上的etcd(并删除相关数据存放目录)：

```
root@shaolin:~# rm /etc/kubernetes/manifests/etcd.yaml
root@shaolin:~# rm -fr /var/lib/etcd
```


再查看k8s cluster当前pod，你会发现etcd-shaolin不见了。

至此，k8s集群的当前状态示意图如下：

![img{512x368}](../../assets/5347cf154d45c41f.png)


### 4、重新创建shaolin上的etcd ，并以member形式加入etcd cluster

我们首先需要在已存在的etcd cluster中添加etcd-shaolin这个member:

```
root@wudang:~/kubernetes-conf-shaolin/manifests# etcdctl member add etcd-shaolin --peer-urls=http://10.27.53.32:2380
Member 3184cfa57d8ef00c added to cluster 140cec6dd173ab61
```


然后，在shaolin node上基于原shaolin上的etcd.yaml文件进行如下修改：

```
// /etc/kubernetes/manifests/etcd.yaml
... ...
spec:
containers:
- command:
- etcd
- --name=etcd-shaolin
- --initial-advertise-peer-urls=http://10.27.53.32:2380
- --listen-peer-urls=http://10.27.53.32:2380
- --listen-client-urls=http://10.27.53.32:2379,http://127.0.0.1:2379
- --advertise-client-urls=http://10.27.53.32:2379
- --initial-cluster-token=etcd-cluster
- --initial-cluster=etcd-shaolin=http://10.27.53.32:2380,etcd-wudang=http://10.24.138.208:2380,etcd-emei=http://10.27.52.72:2380
- --initial-cluster-state=existing
- --data-dir=/var/lib/etcd
image: gcr.io/google_containers/etcd-amd64:3.0.17
```


修改保存后，kubelet将自动拉起etcd-shaolin：

```
root@shaolin:~/k8s-install# pods
NAMESPACE NAME READY STATUS RESTARTS AGE IP NODE
kube-system etcd-emei 1/1 Running 0 3h 10.27.52.72 emei
kube-system etcd-shaolin 1/1 Running 0 8s 10.27.53.32 shaolin
kube-system etcd-wudang 1/1 Running 0 3h 10.24.138.208 wudang
```


查看etcd cluster状态：

```
root@shaolin:~# etcdctl endpoint status --endpoints=10.27.52.72:2379,10.24.138.208:2379,10.27.53.32:2379
10.27.52.72:2379, 6e80adf8cd57f826, 3.0.17, 11 MB, false, 17, 34941
10.24.138.208:2379, f3805d1ab19c110b, 3.0.17, 11 MB, true, 17, 34941
10.27.53.32:2379, 3184cfa57d8ef00c, 3.0.17, 11 MB, false, 17, 34941
```


可以看出三个etcd实例的数据size、raft status是一致的，wudang node上的etcd是leader！

### 5、将shaolin上的apiserver的etcdserver指向改回etcd-shaolin

```
// /etc/kubernetes/manifests/kube-apiserver.yaml
... ...
- --etcd-servers=http://127.0.0.1:2379
... ...
```


生效重启后，当前kubernetes cluster的状态如下面示意图：

![img{512x368}](../../assets/97b89797dd43ead9.png)


第二部分在[这里](http://tonybai.com/2017/05/15/setup-a-ha-kubernetes-cluster-based-on-kubeadm-part2/)。

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

我参考你的文章做测试，etcdctl make-mirror 时无法成功。怀疑是因为我使用的docker run的etcd集群 而不是是用kubelet，导致网络无法连接。

docker logs etcd

===========

2017-07-05 03:26:21.485993 I | v3rpc/grpc: transport: http2Server.HandleStreams failed to read frame: read tcp 172.17.0.2:2369->10.9.5.105:53550: read: connection reset bypeer

嗯，看起来像是网络问题。

网络问题解决了。但是还是有错

etcdctl make-mirror –no-dest-prefix=true –endpoints=127.0.0.1:2379 –insecure-skip-tls-verify=true 127.0.0.1:2369

Error: etcdserver: duplicate key given in txn request

这个没遇到过。理论上你新建的etcd cluster，怎么会与k8s的etcd有重复的key呢？

就是啊。我把目录都清空了，重启，然后在导入，就是这个错。

大概知道原因了，因为k8s api server 还在读写当中，在make-mirror中，同一个事务中包含了相同的key，所以报错。

请问，我们在对节点做了kubeadm reset后，把kubelet.conf复制到节点上后，节点的kubelet服务启了，但集群网络断开了，这个网络怎么处理呢，我一直报kubelet服务一直报下在的网络问题。

forbidden: node master.medlab.com.cn cannot modify node node1.medlab.com.cn

Oct 10 11:16:38 node1.medlab.com.cn kubelet[2165]: W1010 11:16:38.853171 2165 cni.go:189] Unable to update cni config: No networks found in /etc/cni/net.d

Oct 10 11:16:38 node1.medlab.com.cn kubelet[2165]: E1010 11:16:38.853520 2165 kubelet.go:2136] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized

Oct 10 11:16:39 node1.medlab.com.cn kubelet[2165]: E1010 11:16:39.029403 2165 eviction_manager.go:238] eviction manager: unexpected err: failed GetNode: node ‘node1.medlab.com.cn’ not found

，你的文档中没有说明这个网络配置，谢谢。可否指导下，谢谢QQ:279180162，邮箱：chenfengli1985@126.com

请问，我们在对节点做了kubeadm reset后，集群网络就断开了，这个网络怎么处理呢，我一直报 forbidden: node master.medlab.com.cn cannot modify node node1.medlab.com.cn

Oct 10 11:16:38 node1.medlab.com.cn kubelet[2165]: W1010 11:16:38.853171 2165 cni.go:189] Unable to update cni config: No networks found in /etc/cni/net.d

Oct 10 11:16:38 node1.medlab.com.cn kubelet[2165]: E1010 11:16:38.853520 2165 kubelet.go:2136] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized

Oct 10 11:16:39 node1.medlab.com.cn kubelet[2165]: E1010 11:16:39.029403 2165 eviction_manager.go:238] eviction manager: unexpected err: failed GetNode: node ‘node1.medlab.com.cn’ not found

，你的文档中没有说明这个网络配置，谢谢。

停掉api server 后可以了

在node节点上部署etcd的时候，一直没成功，提示我etcdmain: couldn’t find local name “etcd-ip-172-31-0-153″ in the initial cluster configuration，dns貌似出错了,并没有出现node节点上面的etcd全部是running状态

请问，我们在对节点做了kubeadm reset后，把kubelet.conf复制到节点上后，节点的kubelet服务启了，但集群网络断开了，这个网络怎么处理呢，我一直报kubelet服务一直报下在的网络问题。

forbidden: node master.medlab.com.cn cannot modify node node1.medlab.com.cn

Oct 10 11:16:38 node1.medlab.com.cn kubelet[2165]: W1010 11:16:38.853171 2165 cni.go:189] Unable to update cni config: No networks found in /etc/cni/net.d

Oct 10 11:16:38 node1.medlab.com.cn kubelet[2165]: E1010 11:16:38.853520 2165 kubelet.go:2136] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:docker: network plugin is not ready: cni config uninitialized

Oct 10 11:16:39 node1.medlab.com.cn kubelet[2165]: E1010 11:16:39.029403 2165 eviction_manager.go:238] eviction manager: unexpected err: failed GetNode: node ‘node1.medlab.com.cn’ not found

，你的文档中没有说明这个网络配置，谢谢。可否指导下，谢谢QQ:279180162，邮箱：chenfengli1985@126.com

试试查看一下reset的那个node上的/etc/cni/net.d目录下是否有cni配置文件，如果使用的是weave network，那么应该有一个10-weave.conf之类的配置文件，如果没有，可以从其他节点copy一个过来。

Oct 12 11:20:14 box249 kubelet[30067]: E1012 11:20:14.076836 30067 eviction_manager.go:238] eviction manager: unexpected err: failed GetNode: node ‘box249′ not found

Oct 12 11:20:15 box249 kubelet[30067]: I1012 11:20:15.557100 30067 kubelet_node_status.go:247] Setting node annotation to enable volume controller attach/detach

Oct 12 11:20:15 box249 kubelet[30067]: I1012 11:20:15.565161 30067 kubelet_node_status.go:82] Attempting to register node box249

Oct 12 11:20:15 box249 kubelet[30067]: E1012 11:20:15.568022 30067 kubelet_node_status.go:106] Unable to register node “box249″ with API server: nodes “box249″ is forbidden: node box234 cannot modify node box249

centos7.2 下kubeadm部署的k8s1.7.5在node节点上启动kubelet时报的错误，已经拷贝了/etc/cni/10-weave.conf文件，请问这可能是什么原因导致的？

在1.6及之前的版本中没遇到过，不过你可以翻翻k8s 的issue，比如这个：https://github.com/kubernetes/kubernetes/issues/47695 ，似乎与k8s 1.7.x开启RBAC mode有关。

这个问题，我已经试过

v1.7.x使用了NodeRestriction等安全检查控制，要设置成v1.6.x推荐的admission-control配置即可

vi /etc/kubernetes/manifests/kube-apiserver.yaml

# – –admission-control=Initializers,NamespaceLifecycle,LimitRanger,ServiceAccount,PersistentVolumeLabel,DefaultStorageClass,DefaultTolerationSeconds,NodeRestriction,ResourceQuota

– –admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,PersistentVolumeLabel,DefaultStorageClass,ResourceQuota,DefaultTolerationSeconds

我想请问的是这个架构部署好后，执行kubeadm token list | grep authentication,signing | awk ‘{print $1}’ 得到几个token,是一个还是三个，三个的话对于master集群外的node节点怎么添加进来，kubeadm join –token ‘token’ 负载IP:6443？？

复制/etc/kubernetes/kubelet.conf和pki目录到其他节点并重启kubelete之后，日志卡在了

18971 certificate_manager.go:361] Requesting new certificate.

1、你用的kubernetes是什么版本？ 2、你在出问题的节点上换回原先的kubelet.conf和pki目录，看能否启动起来？

请问使用kubeadm 你的 cloud provider 怎么解决的。 是编辑 10-kubeadm.conf 吗 。如果编辑的话具体格式是怎么样的。

我没有使用过cloud provider。

etcdctl make-mirror –no-dest-prefix=false 127.0.0.1:2379 –endpoints=192.168.186.111:2379 –insecure-skip-tls-verify=true

Error: grpc: timed out when dialing

我的是master是192.168.186.111，节点分别是192.168.186.112，192.168.186.113，

我在186.112，186.113上面执行下面语句有报错：

etcdctl make-mirror –no-dest-prefix=false 127.0.0.1:2379 –endpoints=192.168.186.111:2379 –insecure-skip-tls-verify=true

Error: grpc: timed out when dialing

也就是想把186.111上面的etcd数据同步到cluster上面同步报错，但是我在186.111上面执行就可以，也就是可以把cluster上面的数据同步到186.111上面。

timeout: 显然是etcdctl连不上master上的etcd。你在master上打开/etc/kubernetes/manifests/etcd.yaml，查看一下listen-client-urls和advertise-client-urls，是不是都是127.0.0.1:2379啊，把这两个ip修改一下，改为master的local ip。修改保存后，kubelet会重启master 上的etcd。然后再在某个slave node上sync master的etcd的配置。

我修改为本地IP后集群都起不来了

spec:

containers:

– command:

– etcd

– –listen-client-urls=http://192.168.186.111:2379

– –advertise-client-urls=http://192.168.186.111:2379

– –data-dir=/var/lib/etcd

image: gcr.io/google_containers/etcd-amd64:3.0.17

livenessProbe:

failureThreshold: 8

httpGet:

[root@node1 kubernetes]# systemctl status kubelet

● kubelet.service – kubelet: The Kubernetes Node Agent

Loaded: loaded (/etc/systemd/system/kubelet.service; enabled; vendor preset: disabled)

Drop-In: /etc/systemd/system/kubelet.service.d

└─10-kubeadm.conf

Active: active (running) since Thu 2017-12-14 11:22:16 CST; 47s ago

Docs: http://kubernetes.io/docs/

Main PID: 117270 (kubelet)

Memory: 27.2M

CGroup: /system.slice/kubelet.service

├─117270 /usr/bin/kubelet –kubeconfig=/etc/kubernetes/kubelet.conf –require-kubeconfig=true –pod-manifest-path=/etc/kubernetes/manifests –allow-privileged=true –network-p…

└─117293 journalctl -k -f

Dec 14 11:22:47 node1 kubelet[117270]: W1214 11:22:47.277864 117270 cni.go:157] Unable to update cni config: No networks found in /etc/cni/net.d

Dec 14 11:22:47 node1 kubelet[117270]: E1214 11:22:47.277953 117270 kubelet.go:2067] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady mes…ninitialized

Dec 14 11:22:47 node1 kubelet[117270]: I1214 11:22:47.281257 117270 kubelet_node_status.go:230] Setting node annotation to enable volume controller attach/detach

Dec 14 11:22:47 node1 kubelet[117270]: I1214 11:22:47.282871 117270 kubelet_node_status.go:77] Attempting to register node node1

Dec 14 11:22:52 node1 kubelet[117270]: W1214 11:22:52.279739 117270 cni.go:157] Unable to update cni config: No networks found in /etc/cni/net.d

Dec 14 11:22:52 node1 kubelet[117270]: E1214 11:22:52.280011 117270 kubelet.go:2067] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady mes…ninitialized

Dec 14 11:22:57 node1 kubelet[117270]: W1214 11:22:57.282005 117270 cni.go:157] Unable to update cni config: No networks found in /etc/cni/net.d

Dec 14 11:22:57 node1 kubelet[117270]: E1214 11:22:57.282151 117270 kubelet.go:2067] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady mes…ninitialized

Dec 14 11:23:02 node1 kubelet[117270]: W1214 11:23:02.283695 117270 cni.go:157] Unable to update cni config: No networks found in /etc/cni/net.d

Dec 14 11:23:02 node1 kubelet[117270]: E1214 11:23:02.283785 117270 kubelet.go:2067] Container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady mes…ninitialized

Hint: Some lines were ellipsized, use -l to show in full.

[root@node1 kubernetes]# kubectl get pods -n kube-system -o wide

Error from server (ServerTimeout): the server cannot complete the requested operation at this time, try again later (get pods)

我查看etcd错误日志：

[root@node1 kubernetes]# docker logs 70fe

2017-12-14 03:27:54.511300 I | etcdmain: etcd Version: 3.0.17

2017-12-14 03:27:54.511376 I | etcdmain: Git SHA: cc198e2

2017-12-14 03:27:54.511380 I | etcdmain: Go Version: go1.6.4

2017-12-14 03:27:54.511382 I | etcdmain: Go OS/Arch: linux/amd64

2017-12-14 03:27:54.511386 I | etcdmain: setting maximum number of CPUs to 1, total number of available CPUs is 1

2017-12-14 03:27:54.511676 I | etcdmain: listening for peers on http://localhost:2380

2017-12-14 03:27:54.511714 I | etcdmain: listening for client requests on 192.168.186.111:2379

2017-12-14 03:27:54.528431 I | etcdserver: name = default

2017-12-14 03:27:54.528514 I | etcdserver: data dir = /var/lib/etcd

2017-12-14 03:27:54.528527 I | etcdserver: member dir = /var/lib/etcd/member

2017-12-14 03:27:54.528534 I | etcdserver: heartbeat = 100ms

2017-12-14 03:27:54.528540 I | etcdserver: election = 1000ms

2017-12-14 03:27:54.528546 I | etcdserver: snapshot count = 10000

2017-12-14 03:27:54.528564 I | etcdserver: advertise client URLs = http://192.168.186.111:2379

2017-12-14 03:27:54.528600 I | etcdserver: initial advertise peer URLs = http://localhost:2380

2017-12-14 03:27:54.528610 I | etcdserver: initial cluster = default=http://localhost:2380

2017-12-14 03:27:54.539365 I | etcdserver: starting member 8e9e05c52164694d in cluster cdf818194e3a8c32

2017-12-14 03:27:54.539408 I | raft: 8e9e05c52164694d became follower at term 0

2017-12-14 03:27:54.539422 I | raft: newRaft 8e9e05c52164694d [peers: [], term: 0, commit: 0, applied: 0, lastindex: 0, lastterm: 0]

2017-12-14 03:27:54.539425 I | raft: 8e9e05c52164694d became follower at term 1

2017-12-14 03:27:54.602614 I | etcdserver: starting server… [version: 3.0.17, cluster version: to_be_decided]

2017-12-14 03:27:54.603825 I | membership: added member 8e9e05c52164694d [http://localhost:2380] to cluster cdf818194e3a8c32

2017-12-14 03:27:54.741124 I | raft: 8e9e05c52164694d is starting a new election at term 1

2017-12-14 03:27:54.741270 I | raft: 8e9e05c52164694d became candidate at term 2

2017-12-14 03:27:54.741314 I | raft: 8e9e05c52164694d received vote from 8e9e05c52164694d at term 2

2017-12-14 03:27:54.741407 I | raft: 8e9e05c52164694d became leader at term 2

2017-12-14 03:27:54.741443 I | raft: raft.node: 8e9e05c52164694d elected leader 8e9e05c52164694d at term 2

2017-12-14 03:27:54.743118 I | etcdserver: setting up the initial cluster version to 3.0

2017-12-14 03:27:54.745342 N | membership: set the initial cluster version to 3.0

2017-12-14 03:27:54.745447 I | api: enabled capabilities for version 3.0

2017-12-14 03:27:54.745778 I | etcdserver: published {Name:default ClientURLs:[http://192.168.186.111:2379]} to cluster cdf818194e3a8c32

2017-12-14 03:27:54.745808 I | etcdmain: ready to serve client requests

2017-12-14 03:27:54.747113 N | etcdmain: serving insecure client requests on 192.168.186.111:2379, this is strongly discouraged!

2017-12-14 03:29:25.151993 N | osutil: received terminated signal, shutting down…

[root@node1 kubernetes]#

估计：这是因为kube-apiserver使用的是127.0.0.1:2379去访问etcd，修改后，访问失败了。试试修改apiserver的–etcd-servers配置，改为192.168.186.111:2379

这样改是启动起来了，但是一起在restart

[root@node1 manifests]# kubectl get pods -n kube-system

NAME READY STATUS RESTARTS AGE

etcd-node1 1/1 Running 5 5m

etcd-node2 1/1 Running 6 15m

etcd-node3 1/1 Running 0 12m

kube-apiserver-node1 1/1 Running 0 5m

kube-controller-manager-node1 1/1 Running 1 1h

kube-dns-3913472980-fb545 3/3 Running 0 1h

kube-proxy-1799f 1/1 Running 0 1h

kube-proxy-8413q 1/1 Running 0 16m

kube-proxy-nmjds 1/1 Running 0 12m

kube-scheduler-node1 1/1 Running 1 1h

weave-net-5nh94 2/2 Running 0 1h

weave-net-bd2lj 2/2 Running 0 16m

weave-net-q6ktt 2/2 Running 0 12m

而且我执行这条命令的时候要好久才会出现，大概一分钟，很慢。

只是改了个连接的ip地址，理论上不应该啊。不过这一步是为了让你做etcd数据同步的。后续kube-apiserver也是要去连新建的etcd cluster的。

[root@node131 net.d]# docker exec -it 98bc06acd262 ash

/ # etcdctl make-mirror –no-dest-prefix=true 127.0.0.1:2379 –endpoints=192.168.1.56:2379 –insecure-skip-tls-verify=true

No help topic for ‘make-mirror’

/ # etcdctl –version

etcdctl version: 3.0.17

API version: 2

/ # etcdctl help

NAME:

etcdctl – A simple command line client for etcd.

USAGE:

etcdctl [global options] command [command options] [arguments...]

VERSION:

3.0.17

COMMANDS:

backup backup an etcd directory

cluster-health check the health of the etcd cluster

mk make a new key with a given value

mkdir make a new directory

rm remove a key or a directory

rmdir removes the key if it is an empty directory or a key-value pair

get retrieve the value of a key

ls retrieve a directory

set set the value of a key

setdir create a new directory or update an existing directory TTL

update update an existing key with a given value

updatedir update an existing directory

watch watch a key for changes

exec-watch watch a key for changes and exec an executable

member member add, remove and list subcommands

import import a snapshot to a cluster

user user add, grant and revoke subcommands

role role add, grant and revoke subcommands

auth overall auth controls

我的etcd是v2 怎么样在容器内设置成v3，求教··