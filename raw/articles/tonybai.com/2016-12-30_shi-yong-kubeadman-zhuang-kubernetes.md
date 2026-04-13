---
title: 使用Kubeadm安装Kubernetes
url: https://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/
published: '2016-12-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Kubeadm安装Kubernetes

在《[当Docker遇到systemd](http://tonybai.com/2016/12/27/when-docker-meets-systemd/)》一文中，我提到过这两天儿一直在做的一个task：使用[kubeadm](http://kubernetes.io/docs/admin/kubeadm/)在[Ubuntu 16.04](http://tonybai.com/tag/ubuntu)上安装部署[Kubernetes](http://kubernetes.io/)的最新发布版本-[k8s 1.5.1](http://blog.kubernetes.io/2016/12/kubernetes-1.5-supporting-production-workloads.html)。

年中，Docker宣布在Docker engine中集成swarmkit工具包，这一announcement在轻量级容器界引发轩然大波。毕竟开发者是懒惰的^0^，有了docker swarmkit，驱动developer去安装其他容器编排工具的动力在哪里呢？即便docker engine还不是当年那个被人们高频使用的IE浏览器。作为针对Docker公司这一市场行为的回应，容器集群管理和服务编排领先者Kubernetes在三个月后发布了[Kubernetes1.4.0版本](http://blog.kubernetes.io/2016/09/kubernetes-1.4-making-it-easy-to-run-on-kuberentes-anywhere.html)。在这个版本中K8s新增了kubeadm工具。kubeadm的使用方式有点像集成在[docker engine](http://tonybai.com/tag/docker)中的[swarm kit工具](http://tonybai.com/2016/10/11/some-problems-under-swarm-mode-in-docker-1-12)，旨在改善开发者在安装、调试和使用k8s时的体验，降低安装和使用门槛。理论上通过两个命令：init和join即可搭建出一套完整的Kubernetes cluster。

不过，和初入docker引擎的swarmkit一样，kubeadm目前也在active development中，也不是那么stable，因此即便在当前最新的k8s 1.5.1版本中，它仍然处于Alpha状态，官方不建议在Production环境下使用。每次执行kubeadm init时，它都会打印如下提醒日志：

```
[kubeadm] WARNING: kubeadm is in alpha, please do not use it for production clusters.
```


不过由于[之前部署的k8s 1.3.7集群](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu)运行良好，这给了我们在k8s这条路上继续走下去并走好的信心。但k8s在部署和管理方面的体验的确是太繁琐了，于是我们准备试验一下kubeadm是否能带给我们超出预期的体验。之前在aliyun ubuntu 14.04上安装kubernetes 1.3.7的经验和教训，让我略微有那么一丢丢底气，但实际安装过程依旧是一波三折。这既与kubeadm的unstable有关，同样也与[cni](https://github.com/containernetworking/cni)、第三方网络add-ons的质量有关。无论哪一方出现问题都会让你的install过程异常坎坷曲折。

### 一、环境与约束

在kubeadm支持的Ubuntu 16.04+, CentOS 7 or HypriotOS v1.0.1+三种操作系统中，我们选择了Ubuntu 16.04。由于阿里云尚无官方16.04 Image可用，我们新开了两个Ubuntu 14.04ECS实例，并通过apt-get命令手工将其升级到Ubuntu 16.04.1，详细版本是：Ubuntu 16.04.1 LTS (GNU/Linux 4.4.0-58-generic x86_64)。

Ubuntu 16.04使用了[systemd](https://github.com/systemd/systemd)作为init system，在安装和配置Docker时，可以参考我的这篇《[当Docker遇到system](http://tonybai.com/2016/12/27/when-docker-meets-systemd/)》。Docker版本我选择了目前可以得到的lastest stable release: 1.12.5。

```
# docker version
Client:
Version: 1.12.5
API version: 1.24
Go version: go1.6.4
Git commit: 7392c3b
Built: Fri Dec 16 02:42:17 2016
OS/Arch: linux/amd64
Server:
Version: 1.12.5
API version: 1.24
Go version: go1.6.4
Git commit: 7392c3b
Built: Fri Dec 16 02:42:17 2016
OS/Arch: linux/amd64
```


至于Kubernetes版本，前面已经提到过了，我们就使用最新发布的Kubernetes 1.5.1版本。1.5.1是[1.5.0](http://blog.kubernetes.io/2016/12/kubernetes-1.5-supporting-production-workloads.html)的一个[紧急fix版本](https://groups.google.com/forum/#!topic/kubernetes-announce/iclRj-6Nfsg)，主要”to address default flag values which in isolation were not problematic, but in concert could result in an insecure cluster”。官方建议skip 1.5.0，直接用1.5.1。

这里再重申一下：Kubernetes的安装、配置和调通是很难的，在阿里云上调通就更难了，有时还需要些运气。Kubernetes、Docker、cni以及各种网络Add-ons都在active development中，也许今天还好用的step、tip和trick，明天就out-dated，因此在借鉴本文的操作步骤时，请谨记这些^0^。

### 二、安装包准备

我们这次新开了两个ECS实例，一个作为master node，一个作为minion node。Kubeadm默认安装时，master node将不会参与Pod调度，不会承载work load，即不会有非核心组件的Pod在Master node上被创建出来。当然通过kubectl taint命令可以解除这一限制，不过这是后话了。

集群拓扑：

```
master node：10.47.217.91，主机名：iZ25beglnhtZ
minion node：10.28.61.30，主机名：iZ2ze39jeyizepdxhwqci6Z
```


本次安装的主参考文档就是Kubernetes官方的那篇《[Installing Kubernetes on Linux with kubeadm](http://kubernetes.io/docs/getting-started-guides/kubeadm)》。

本小节，我们将进行安装包准备，即将kubeadm以及此次安装所需要的k8s核心组件统统下载到上述两个Node上。注意：如果你有加速器，那么本节下面的安装过程将尤为顺利，反之，… ![:(](../../assets/5609ccdbbda60d85.gif)


#### 1、添加apt-key

```
# curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
OK
```


#### 2、添加Kubernetes源并更新包信息

添加Kubernetes源到sources.list.d目录下：

```
# cat <<EOF > /etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
# cat /etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
```


更新包信息：

```
# apt-get update
... ...
Hit:2 http://mirrors.aliyun.com/ubuntu xenial InRelease
Hit:3 https://apt.dockerproject.org/repo ubuntu-xenial InRelease
Get:4 http://mirrors.aliyun.com/ubuntu xenial-security InRelease [102 kB]
Get:1 https://packages.cloud.google.com/apt kubernetes-xenial InRelease [6,299 B]
Get:5 https://packages.cloud.google.com/apt kubernetes-xenial/main amd64 Packages [1,739 B]
Get:6 http://mirrors.aliyun.com/ubuntu xenial-updates InRelease [102 kB]
Get:7 http://mirrors.aliyun.com/ubuntu xenial-proposed InRelease [253 kB]
Get:8 http://mirrors.aliyun.com/ubuntu xenial-backports InRelease [102 kB]
Fetched 568 kB in 19s (28.4 kB/s)
Reading package lists... Done
```


#### 3、下载Kubernetes核心组件

在此次安装中，我们通过apt-get就可以下载Kubernetes的核心组件，包括kubelet、kubeadm、kubectl和kubernetes-cni等。

```
# apt-get install -y kubelet kubeadm kubectl kubernetes-cni
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following package was automatically installed and is no longer required:
libtimedate-perl
Use 'apt autoremove' to remove it.
The following additional packages will be installed:
ebtables ethtool socat
The following NEW packages will be installed:
ebtables ethtool kubeadm kubectl kubelet kubernetes-cni socat
0 upgraded, 7 newly installed, 0 to remove and 0 not upgraded.
Need to get 37.6 MB of archives.
After this operation, 261 MB of additional disk space will be used.
Get:2 http://mirrors.aliyun.com/ubuntu xenial/main amd64 ebtables amd64 2.0.10.4-3.4ubuntu1 [79.6 kB]
Get:6 http://mirrors.aliyun.com/ubuntu xenial/main amd64 ethtool amd64 1:4.5-1 [97.5 kB]
Get:7 http://mirrors.aliyun.com/ubuntu xenial/universe amd64 socat amd64 1.7.3.1-1 [321 kB]
Get:1 https://packages.cloud.google.com/apt kubernetes-xenial/main amd64 kubernetes-cni amd64 0.3.0.1-07a8a2-00 [6,877 kB]
Get:3 https://packages.cloud.google.com/apt kubernetes-xenial/main amd64 kubelet amd64 1.5.1-00 [15.1 MB]
Get:4 https://packages.cloud.google.com/apt kubernetes-xenial/main amd64 kubectl amd64 1.5.1-00 [7,954 kB]
Get:5 https://packages.cloud.google.com/apt kubernetes-xenial/main amd64 kubeadm amd64 1.6.0-alpha.0-2074-a092d8e0f95f52-00 [7,120 kB]
Fetched 37.6 MB in 36s (1,026 kB/s)
... ...
Unpacking kubeadm (1.6.0-alpha.0-2074-a092d8e0f95f52-00) ...
Processing triggers for systemd (229-4ubuntu13) ...
Processing triggers for ureadahead (0.100.0-19) ...
Processing triggers for man-db (2.7.5-1) ...
Setting up ebtables (2.0.10.4-3.4ubuntu1) ...
update-rc.d: warning: start and stop actions are no longer supported; falling back to defaults
Setting up ethtool (1:4.5-1) ...
Setting up kubernetes-cni (0.3.0.1-07a8a2-00) ...
Setting up socat (1.7.3.1-1) ...
Setting up kubelet (1.5.1-00) ...
Setting up kubectl (1.5.1-00) ...
Setting up kubeadm (1.6.0-alpha.0-2074-a092d8e0f95f52-00) ...
Processing triggers for systemd (229-4ubuntu13) ...
Processing triggers for ureadahead (0.100.0-19) ...
... ...
```


下载后的kube组件并未自动运行起来。在 /lib/systemd/system下面我们能看到kubelet.service：

```
# ls /lib/systemd/system|grep kube
kubelet.service
//kubelet.service
[Unit]
Description=kubelet: The Kubernetes Node Agent
Documentation=http://kubernetes.io/docs/
[Service]
ExecStart=/usr/bin/kubelet
Restart=always
StartLimitInterval=0
RestartSec=10
[Install]
WantedBy=multi-user.target
```


kubelet的版本：

```
# kubelet --version
Kubernetes v1.5.1
```


k8s的核心组件都有了，接下来我们就要boostrap kubernetes cluster了。同时，问题也就随之而来了，而这些问题以及问题的解决才是本篇要说明的重点。

### 三、初始化集群

前面说过，理论上通过kubeadm使用init和join命令即可建立一个集群，这init就是在master节点对集群进行初始化。和k8s 1.4之前的部署方式不同的是，kubeadm安装的k8s核心组件都是以容器的形式运行于master node上的。因此在kubeadm init之前，最好给master node上的docker engine挂上加速器代理，因为kubeadm要从gcr.io/google_containers repository中pull许多核心组件的images，大约有如下一些：

```
gcr.io/google_containers/kube-controller-manager-amd64 v1.5.1 cd5684031720 2 weeks ago 102.4 MB
gcr.io/google_containers/kube-apiserver-amd64 v1.5.1 8c12509df629 2 weeks ago 124.1 MB
gcr.io/google_containers/kube-proxy-amd64 v1.5.1 71d2b27b03f6 2 weeks ago 175.6 MB
gcr.io/google_containers/kube-scheduler-amd64 v1.5.1 6506e7b74dac 2 weeks ago 53.97 MB
gcr.io/google_containers/etcd-amd64 3.0.14-kubeadm 856e39ac7be3 5 weeks ago 174.9 MB
gcr.io/google_containers/kubedns-amd64 1.9 26cf1ed9b144 5 weeks ago 47 MB
gcr.io/google_containers/dnsmasq-metrics-amd64 1.0 5271aabced07 7 weeks ago 14 MB
gcr.io/google_containers/kube-dnsmasq-amd64 1.4 3ec65756a89b 3 months ago 5.13 MB
gcr.io/google_containers/kube-discovery-amd64 1.0 c5e0c9a457fc 3 months ago 134.2 MB
gcr.io/google_containers/exechealthz-amd64 1.2 93a43bfb39bf 3 months ago 8.375 MB
gcr.io/google_containers/pause-amd64 3.0 99e59f495ffa 7 months ago 746.9 kB
```


在Kubeadm的文档中，Pod Network的安装是作为一个单独的步骤的。kubeadm init并没有为你选择一个默认的Pod network进行安装。我们将首选[Flannel](https://tonybai.com/github.com/coreos/flannel) 作为我们的Pod network，这不仅是因为我们的上一个集群用的就是flannel，而且表现稳定。更是由于Flannel就是coreos为k8s打造的专属overlay network add-ons。甚至于flannel repository的readme.md都这样写着：“flannel is a network fabric for containers, designed for Kubernetes”。如果我们要使用Flannel，那么在执行init时，按照kubeadm文档要求，我们必须给init命令带上option：–pod-network-cidr=10.244.0.0/16。

#### 1、执行kubeadm init

执行kubeadm init命令：

```
# kubeadm init --pod-network-cidr=10.244.0.0/16
[kubeadm] WARNING: kubeadm is in alpha, please do not use it for production clusters.
[preflight] Running pre-flight checks
[preflight] Starting the kubelet service
[init] Using Kubernetes version: v1.5.1
[tokens] Generated token: "2e7da9.7fc5668ff26430c7"
[certificates] Generated Certificate Authority key and certificate.
[certificates] Generated API Server key and certificate
[certificates] Generated Service Account signing keys
[certificates] Created keys and certificates in "/etc/kubernetes/pki"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/admin.conf"
[apiclient] Created API client, waiting for the control plane to become ready //如果没有挂加速器，可能会在这里hang住。
[apiclient] All control plane components are healthy after 54.789750 seconds
[apiclient] Waiting for at least one node to register and become ready
[apiclient] First node is ready after 1.003053 seconds
[apiclient] Creating a test deployment
[apiclient] Test deployment succeeded
[token-discovery] Created the kube-discovery deployment, waiting for it to become ready
[token-discovery] kube-discovery is ready after 62.503441 seconds
[addons] Created essential addon: kube-proxy
[addons] Created essential addon: kube-dns
Your Kubernetes master has initialized successfully!
You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
http://kubernetes.io/docs/admin/addons/
You can now join any number of machines by running the following on each node:
kubeadm join --token=2e7da9.7fc5668ff26430c7 123.56.200.187
```


init成功后的master node有啥变化？k8s的核心组件均正常启动：

```
# ps -ef|grep kube
root 2477 2461 1 16:36 ? 00:00:04 kube-proxy --kubeconfig=/run/kubeconfig
root 30860 1 12 16:33 ? 00:01:09 /usr/bin/kubelet --kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true --pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true --network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin --cluster-dns=10.96.0.10 --cluster-domain=cluster.local
root 30952 30933 0 16:33 ? 00:00:01 kube-scheduler --address=127.0.0.1 --leader-elect --master=127.0.0.1:8080
root 31128 31103 2 16:33 ? 00:00:11 kube-controller-manager --address=127.0.0.1 --leader-elect --master=127.0.0.1:8080 --cluster-name=kubernetes --root-ca-file=/etc/kubernetes/pki/ca.pem --service-account-private-key-file=/etc/kubernetes/pki/apiserver-key.pem --cluster-signing-cert-file=/etc/kubernetes/pki/ca.pem --cluster-signing-key-file=/etc/kubernetes/pki/ca-key.pem --insecure-experimental-approve-all-kubelet-csrs-for-group=system:kubelet-bootstrap --allocate-node-cidrs=true --cluster-cidr=10.244.0.0/16
root 31223 31207 2 16:34 ? 00:00:10 kube-apiserver --insecure-bind-address=127.0.0.1 --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,PersistentVolumeLabel,DefaultStorageClass,ResourceQuota --service-cluster-ip-range=10.96.0.0/12 --service-account-key-file=/etc/kubernetes/pki/apiserver-key.pem --client-ca-file=/etc/kubernetes/pki/ca.pem --tls-cert-file=/etc/kubernetes/pki/apiserver.pem --tls-private-key-file=/etc/kubernetes/pki/apiserver-key.pem --token-auth-file=/etc/kubernetes/pki/tokens.csv --secure-port=6443 --allow-privileged --advertise-address=123.56.200.187 --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname --anonymous-auth=false --etcd-servers=http://127.0.0.1:2379
root 31491 31475 0 16:35 ? 00:00:00 /usr/local/bin/kube-discovery
```


而且是多以container的形式启动：

```
# docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
c16c442b7eca gcr.io/google_containers/kube-proxy-amd64:v1.5.1 "kube-proxy --kubecon" 6 minutes ago Up 6 minutes k8s_kube-proxy.36dab4e8_kube-proxy-sb4sm_kube-system_43fb1a2c-cb46-11e6-ad8f-00163e1001d7_2ba1648e
9f73998e01d7 gcr.io/google_containers/kube-discovery-amd64:1.0 "/usr/local/bin/kube-" 8 minutes ago Up 8 minutes k8s_kube-discovery.7130cb0a_kube-discovery-1769846148-6z5pw_kube-system_1eb97044-cb46-11e6-ad8f-00163e1001d7_fd49c2e3
dd5412e5e15c gcr.io/google_containers/kube-apiserver-amd64:v1.5.1 "kube-apiserver --ins" 9 minutes ago Up 9 minutes k8s_kube-apiserver.1c5a91d9_kube-apiserver-iz25beglnhtz_kube-system_eea8df1717e9fea18d266103f9edfac3_8cae8485
60017f8819b2 gcr.io/google_containers/etcd-amd64:3.0.14-kubeadm "etcd --listen-client" 9 minutes ago Up 9 minutes k8s_etcd.c323986f_etcd-iz25beglnhtz_kube-system_3a26566bb004c61cd05382212e3f978f_06d517eb
03c2463aba9c gcr.io/google_containers/kube-controller-manager-amd64:v1.5.1 "kube-controller-mana" 9 minutes ago Up 9 minutes k8s_kube-controller-manager.d30350e1_kube-controller-manager-iz25beglnhtz_kube-system_9a40791dd1642ea35c8d95c9e610e6c1_3b05cb8a
fb9a724540a7 gcr.io/google_containers/kube-scheduler-amd64:v1.5.1 "kube-scheduler --add" 9 minutes ago Up 9 minutes k8s_kube-scheduler.ef325714_kube-scheduler-iz25beglnhtz_kube-system_dc58861a0991f940b0834f8a110815cb_9b3ccda2
.... ...
```


不过这些核心组件并不是跑在pod network中的（没错，此时的pod network还没有创建），而是采用了host network。以kube-apiserver的pod信息为例：

```
kube-system kube-apiserver-iz25beglnhtz 1/1 Running 0 1h 10.47.217.91 iz25beglnhtz
```


kube-apiserver的IP是host ip，从而推断容器使用的是host网络，这从其对应的pause容器的network属性就可以看出：

```
# docker ps |grep apiserver
a5a76bc59e38 gcr.io/google_containers/kube-apiserver-amd64:v1.5.1 "kube-apiserver --ins" About an hour ago Up About an hour k8s_kube-apiserver.2529402_kube-apiserver-iz25beglnhtz_kube-system_25d646be9a0092138dc6088fae6f1656_ec0079fc
ef4d3bf057a6 gcr.io/google_containers/pause-amd64:3.0 "/pause" About an hour ago Up About an hour k8s_POD.d8dbe16c_kube-apiserver-iz25beglnhtz_kube-system_25d646be9a0092138dc6088fae6f1656_bbfd8a31
```


inspect pause容器，可以看到pause container的NetworkMode的值：

```
"NetworkMode": "host",
```


如果kubeadm init执行过程中途出现了什么问题，比如前期忘记挂加速器导致init hang住，你可能会ctrl+c退出init执行。重新配置后，再执行kubeadm init，这时你可能会遇到下面kubeadm的输出：

```
# kubeadm init --pod-network-cidr=10.244.0.0/16
[kubeadm] WARNING: kubeadm is in alpha, please do not use it for production clusters.
[preflight] Running pre-flight checks
[preflight] Some fatal errors occurred:
Port 10250 is in use
/etc/kubernetes/manifests is not empty
/etc/kubernetes/pki is not empty
/var/lib/kubelet is not empty
/etc/kubernetes/admin.conf already exists
/etc/kubernetes/kubelet.conf already exists
[preflight] If you know what you are doing, you can skip pre-flight checks with `--skip-preflight-checks`
```


kubeadm会自动检查当前环境是否有上次命令执行的“残留”。如果有，必须清理后再行执行init。我们可以通过”kubeadm reset”来清理环境，以备重来。

```
# kubeadm reset
[preflight] Running pre-flight checks
[reset] Draining node: "iz25beglnhtz"
[reset] Removing node: "iz25beglnhtz"
[reset] Stopping the kubelet service
[reset] Unmounting mounted directories in "/var/lib/kubelet"
[reset] Removing kubernetes-managed containers
[reset] Deleting contents of stateful directories: [/var/lib/kubelet /etc/cni/net.d /var/lib/etcd]
[reset] Deleting contents of config directories: [/etc/kubernetes/manifests /etc/kubernetes/pki]
[reset] Deleting files: [/etc/kubernetes/admin.conf /etc/kubernetes/kubelet.conf]
```


#### 2、安装flannel pod网络

kubeadm init之后，如果你探索一下当前cluster的状态或者核心组件的日志，你会发现某些“异常”，比如：从kubelet的日志中我们可以看到一直刷屏的错误信息：

```
Dec 26 16:36:48 iZ25beglnhtZ kubelet[30860]: E1226 16:36:48.365885 30860 docker_manager.go:2201] Failed to setup network for pod "kube-dns-2924299975-pddz5_kube-system(43fd7264-cb46-11e6-ad8f-00163e1001d7)" using network plugins "cni": cni config unintialized; Skipping pod
```


通过命令kubectl get pod –all-namespaces -o wide，你也会发现kube-dns pod处于ContainerCreating状态。

这些都不打紧，因为我们还没有为cluster安装Pod network呢。前面说过，我们要使用Flannel网络，因此我们需要执行如下安装命令：

```
#kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
configmap "kube-flannel-cfg" created
daemonset "kube-flannel-ds" created
```


稍等片刻，我们再来看master node上的cluster信息：

```
# ps -ef|grep kube|grep flannel
root 6517 6501 0 17:20 ? 00:00:00 /opt/bin/flanneld --ip-masq --kube-subnet-mgr
root 6573 6546 0 17:20 ? 00:00:00 /bin/sh -c set -e -x; cp -f /etc/kube-flannel/cni-conf.json /etc/cni/net.d/10-flannel.conf; while true; do sleep 3600; done
# kubectl get pods --all-namespaces
NAMESPACE NAME READY STATUS RESTARTS AGE
kube-system dummy-2088944543-s0c5g 1/1 Running 0 50m
kube-system etcd-iz25beglnhtz 1/1 Running 0 50m
kube-system kube-apiserver-iz25beglnhtz 1/1 Running 0 50m
kube-system kube-controller-manager-iz25beglnhtz 1/1 Running 0 50m
kube-system kube-discovery-1769846148-6z5pw 1/1 Running 0 50m
kube-system kube-dns-2924299975-pddz5 4/4 Running 0 49m
kube-system kube-flannel-ds-5ww9k 2/2 Running 0 4m
kube-system kube-proxy-sb4sm 1/1 Running 0 49m
kube-system kube-scheduler-iz25beglnhtz 1/1 Running 0 49m
```


至少集群的核心组件已经全部run起来了。看起来似乎是成功了。

#### 3、minion node：join the cluster

接下来，就该minion node加入cluster了。这里我们用到了kubeadm的第二个命令：kubeadm join。

在minion node上执行（注意：这里要保证master node的9898端口在防火墙是打开的）：

```
# kubeadm join --token=2e7da9.7fc5668ff26430c7 123.56.200.187
[kubeadm] WARNING: kubeadm is in alpha, please do not use it for production clusters.
[preflight] Running pre-flight checks
[tokens] Validating provided token
[discovery] Created cluster info discovery client, requesting info from "http://123.56.200.187:9898/cluster-info/v1/?token-id=2e7da9"
[discovery] Cluster info object received, verifying signature using given token
[discovery] Cluster info signature and contents are valid, will use API endpoints [https://123.56.200.187:6443]
[bootstrap] Trying to connect to endpoint https://123.56.200.187:6443
[bootstrap] Detected server version: v1.5.1
[bootstrap] Successfully established connection with endpoint "https://123.56.200.187:6443"
[csr] Created API client to obtain unique certificate for this node, generating keys and certificate signing request
[csr] Received signed certificate from the API server:
Issuer: CN=kubernetes | Subject: CN=system:node:iZ2ze39jeyizepdxhwqci6Z | CA: false
Not before: 2016-12-26 09:31:00 +0000 UTC Not After: 2017-12-26 09:31:00 +0000 UTC
[csr] Generating kubelet configuration
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/kubelet.conf"
Node join complete:
* Certificate signing request sent to master and response
received.
* Kubelet informed of new secure connection details.
Run 'kubectl get nodes' on the master to see this machine join.
```


也很顺利。我们在minion node上看到的k8s组件情况如下：

```
d85cf36c18ed gcr.io/google_containers/kube-proxy-amd64:v1.5.1 "kube-proxy --kubecon" About an hour ago Up About an hour k8s_kube-proxy.36dab4e8_kube-proxy-lsn0t_kube-system_b8eddf1c-cb4e-11e6-ad8f-00163e1001d7_5826f32b
a60e373b48b8 gcr.io/google_containers/pause-amd64:3.0 "/pause" About an hour ago Up About an hour k8s_POD.d8dbe16c_kube-proxy-lsn0t_kube-system_b8eddf1c-cb4e-11e6-ad8f-00163e1001d7_46bfcf67
a665145eb2b5 quay.io/coreos/flannel-git:v0.6.1-28-g5dde68d-amd64 "/bin/sh -c 'set -e -" About an hour ago Up About an hour k8s_install-cni.17d8cf2_kube-flannel-ds-tr8zr_kube-system_06eca729-cb72-11e6-ad8f-00163e1001d7_01e12f61
5b46f2cb0ccf gcr.io/google_containers/pause-amd64:3.0 "/pause" About an hour ago Up About an hour k8s_POD.d8dbe16c_kube-flannel-ds-tr8zr_kube-system_06eca729-cb72-11e6-ad8f-00163e1001d7_ac880d20
```


我们在master node上查看当前cluster状态：

```
# kubectl get nodes
NAME STATUS AGE
iz25beglnhtz Ready,master 1h
iz2ze39jeyizepdxhwqci6z Ready 21s
```


k8s cluster创建”成功”！真的成功了吗？“折腾”才刚刚开始:(！

### 三、Flannel Pod Network问题

Join成功所带来的“余温”还未散去，我就发现了Flannel pod network的问题，troubleshooting正式开始:(。

#### 1、minion node上的flannel时不时地报错

刚join时还好好的，可过了没一会儿，我们就发现在kubectl get pod –all-namespaces中有错误出现：

```
kube-system kube-flannel-ds-tr8zr 1/2 CrashLoopBackOff 189 16h
```


我们发现这是minion node上的flannel pod中的一个container出错导致的，跟踪到的具体错误如下：

```
# docker logs bc0058a15969
E1227 06:17:50.605110 1 main.go:127] Failed to create SubnetManager: error retrieving pod spec for 'kube-system/kube-flannel-ds-tr8zr': Get https://10.96.0.1:443/api/v1/namespaces/kube-system/pods/kube-flannel-ds-tr8zr: dial tcp 10.96.0.1:443: i/o timeout
```


10.96.0.1是pod network中apiserver service的cluster ip，而minion node上的flannel组件居然无法访问到这个cluster ip！这个问题的奇怪之处还在于，有些时候这个Pod在被调度restart N多次后或者被删除重启后，又突然变为running状态了，行为十分怪异。

在flannel github.com issues中，至少有两个open issue与此问题有密切关系：

https://github.com/coreos/flannel/issues/545

https://github.com/coreos/flannel/issues/535

这个问题暂无明确解。当minion node上的flannel pod自恢复为running状态时，我们又可以继续了。

#### 2、minion node上flannel pod启动失败的一个应对方法

在下面issue中，很多developer讨论了minion node上flannel pod启动失败的一种可能原因以及临时应对方法：

https://github.com/kubernetes/kubernetes/issues/34101

这种说法大致就是minion node上的kube-proxy使用了错误的interface，通过下面方法可以fix这个问题。在minion node上执行：

```
# kubectl -n kube-system get ds -l 'component=kube-proxy' -o json | jq '.items[0].spec.template.spec.containers[0].command |= .+ ["--cluster-cidr=10.244.0.0/16"]' | kubectl apply -f - && kubectl -n kube-system delete pods -l 'component=kube-proxy'
daemonset "kube-proxy" configured
pod "kube-proxy-lsn0t" deleted
pod "kube-proxy-sb4sm" deleted
```


执行后，flannel pod的状态：

```
kube-system kube-flannel-ds-qw291 2/2 Running 8 17h
kube-system kube-flannel-ds-x818z 2/2 Running 17 1h
```


经过17次restart，minion node上的flannel pod 启动ok了。其对应的flannel container启动日志如下：

```
# docker logs 1f64bd9c0386
I1227 07:43:26.670620 1 main.go:132] Installing signal handlers
I1227 07:43:26.671006 1 manager.go:133] Determining IP address of default interface
I1227 07:43:26.670825 1 kube.go:233] starting kube subnet manager
I1227 07:43:26.671514 1 manager.go:163] Using 59.110.67.15 as external interface
I1227 07:43:26.671575 1 manager.go:164] Using 59.110.67.15 as external endpoint
I1227 07:43:26.746811 1 ipmasq.go:47] Adding iptables rule: -s 10.244.0.0/16 -d 10.244.0.0/16 -j RETURN
I1227 07:43:26.749785 1 ipmasq.go:47] Adding iptables rule: -s 10.244.0.0/16 ! -d 224.0.0.0/4 -j MASQUERADE
I1227 07:43:26.752343 1 ipmasq.go:47] Adding iptables rule: ! -s 10.244.0.0/16 -d 10.244.0.0/16 -j MASQUERADE
I1227 07:43:26.755126 1 manager.go:246] Lease acquired: 10.244.1.0/24
I1227 07:43:26.755444 1 network.go:58] Watching for L3 misses
I1227 07:43:26.755475 1 network.go:66] Watching for new subnet leases
I1227 07:43:27.755830 1 network.go:153] Handling initial subnet events
I1227 07:43:27.755905 1 device.go:163] calling GetL2List() dev.link.Index: 10
I1227 07:43:27.756099 1 device.go:168] calling NeighAdd: 123.56.200.187, ca:68:7c:9b:cc:67
```


issue中说到，在kubeadm init时，显式地指定–advertise-address将会避免这个问题。不过目前不要在–advertise-address后面写上多个IP，虽然文档上说是支持的，但实际情况是，当你显式指定–advertise-address的值为两个或两个以上IP时，比如下面这样：

```
#kubeadm init --api-advertise-addresses=10.47.217.91,123.56.200.187 --pod-network-cidr=10.244.0.0/16
```


master初始化成功后，当minion node执行join cluster命令时，会panic掉：

```
# kubeadm join --token=92e977.f1d4d090906fc06a 10.47.217.91
[kubeadm] WARNING: kubeadm is in alpha, please do not use it for production clusters.
... ...
[bootstrap] Successfully established connection with endpoint "https://10.47.217.91:6443"
[bootstrap] Successfully established connection with endpoint "https://123.56.200.187:6443"
E1228 10:14:05.405294 28378 runtime.go:64] Observed a panic: "close of closed channel" (close of closed channel)
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/pkg/util/runtime/runtime.go:70
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/pkg/util/runtime/runtime.go:63
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/pkg/util/runtime/runtime.go:49
/usr/local/go/src/runtime/asm_amd64.s:479
/usr/local/go/src/runtime/panic.go:458
/usr/local/go/src/runtime/chan.go:311
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/cmd/kubeadm/app/node/bootstrap.go:85
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/pkg/util/wait/wait.go:96
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/pkg/util/wait/wait.go:97
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/pkg/util/wait/wait.go:52
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/cmd/kubeadm/app/node/bootstrap.go:93
/usr/local/go/src/runtime/asm_amd64.s:2086
[csr] Created API client to obtain unique certificate for this node, generating keys and certificate signing request
panic: close of closed channel [recovered]
panic: close of closed channel
goroutine 29 [running]:
panic(0x1342de0, 0xc4203eebf0)
/usr/local/go/src/runtime/panic.go:500 +0x1a1
k8s.io/kubernetes/pkg/util/runtime.HandleCrash(0x0, 0x0, 0x0)
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/pkg/util/runtime/runtime.go:56 +0x126
panic(0x1342de0, 0xc4203eebf0)
/usr/local/go/src/runtime/panic.go:458 +0x243
k8s.io/kubernetes/cmd/kubeadm/app/node.EstablishMasterConnection.func1.1()
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/cmd/kubeadm/app/node/bootstrap.go:85 +0x29d
k8s.io/kubernetes/pkg/util/wait.JitterUntil.func1(0xc420563ee0)
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/pkg/util/wait/wait.go:96 +0x5e
k8s.io/kubernetes/pkg/util/wait.JitterUntil(0xc420563ee0, 0x12a05f200, 0x0, 0xc420022e01, 0xc4202c2060)
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/pkg/util/wait/wait.go:97 +0xad
k8s.io/kubernetes/pkg/util/wait.Until(0xc420563ee0, 0x12a05f200, 0xc4202c2060)
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/pkg/util/wait/wait.go:52 +0x4d
k8s.io/kubernetes/cmd/kubeadm/app/node.EstablishMasterConnection.func1(0xc4203a82f0, 0xc420269b90, 0xc4202c2060, 0xc4202c20c0, 0xc4203d8d80, 0x401, 0x480, 0xc4201e75e0, 0x17, 0xc4201e7560, ...)
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/cmd/kubeadm/app/node/bootstrap.go:93 +0x100
created by k8s.io/kubernetes/cmd/kubeadm/app/node.EstablishMasterConnection
/go/src/k8s.io/kubernetes/_output/dockerized/go/src/k8s.io/kubernetes/cmd/kubeadm/app/node/bootstrap.go:94 +0x3ed
```


关于join panic这个问题，在这个issue中有详细讨论：https://github.com/kubernetes/kubernetes/issues/36988

#### 3、open /run/flannel/subnet.env: no such file or directory

前面说过，默认情况下，考虑安全原因，master node是不承担work load的，不参与pod调度。我们这里机器少，只能让master node也辛苦一下。通过下面这个命令可以让master node也参与pod调度：

```
# kubectl taint nodes --all dedicated-
node "iz25beglnhtz" tainted
```


接下来，我们create一个deployment，manifest描述文件如下：

```
//run-my-nginx.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: my-nginx
spec:
replicas: 2
template:
metadata:
labels:
run: my-nginx
spec:
containers:
- name: my-nginx
image: nginx:1.10.1
ports:
- containerPort: 80
```


create后，我们发现调度到master上的my-nginx pod启动是ok的，但minion node上的pod则一直失败，查看到的失败原因如下：

```
Events:
FirstSeen LastSeen Count From SubObjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
28s 28s 1 {default-scheduler } Normal Scheduled Successfully assigned my-nginx-2560993602-0440x to iz2ze39jeyizepdxhwqci6z
27s 1s 26 {kubelet iz2ze39jeyizepdxhwqci6z} Warning FailedSync Error syncing pod, skipping: failed to "SetupNetwork" for "my-nginx-2560993602-0440x_default" with SetupNetworkError: "Failed to setup network for pod \"my-nginx-2560993602-0440x_default(ba5ce554-cbf1-11e6-8c42-00163e1001d7)\" using network plugins \"cni\": open /run/flannel/subnet.env: no such file or directory; Skipping pod"
```


在minion node上的确没有找到/run/flannel/subnet.env该文件。但master node上有这个文件：

```
// /run/flannel/subnet.env
FLANNEL_NETWORK=10.244.0.0/16
FLANNEL_SUBNET=10.244.0.1/24
FLANNEL_MTU=1450
FLANNEL_IPMASQ=true
```


于是手动在minion node上创建一份/run/flannel/subnet.env，并复制master node同名文件的内容，保存。稍许片刻，minion node上的my-nginx pod从error变成running了。

#### 4、no IP addresses available in network: cbr0

将之前的一个my-nginx deployment的replicas改为3，并创建基于该deployment中pods的my-nginx service：

```
//my-nginx-svc.yaml
apiVersion: v1
kind: Service
metadata:
name: my-nginx
labels:
run: my-nginx
spec:
type: NodePort
ports:
- port: 80
nodePort: 30062
protocol: TCP
selector:
run: my-nginx
```


修改后，通过curl localhost:30062测试服务连通性。发现通过VIP负载均衡到master node上的my-nginx pod的request都成功得到了Response，但是负载均衡到minion node上pod的request，则阻塞在那里，直到timeout。查看pod信息才发现，原来新调度到minion node上的my-nginx pod并没有启动ok，错误原因如下：

```
Events:
FirstSeen LastSeen Count From SubObjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
2m 2m 1 {default-scheduler } Normal Scheduled Successfully assigned my-nginx-1948696469-ph11m to iz2ze39jeyizepdxhwqci6z
2m 0s 177 {kubelet iz2ze39jeyizepdxhwqci6z} Warning FailedSync Error syncing pod, skipping: failed to "SetupNetwork" for "my-nginx-1948696469-ph11m_default" with SetupNetworkError: "Failed to setup network for pod \"my-nginx-1948696469-ph11m_default(3700d74a-cc12-11e6-8c42-00163e1001d7)\" using network plugins \"cni\": no IP addresses available in network: cbr0; Skipping pod"
```


查看minion node上/var/lib/cni/networks/cbr0目录，发现该目录下有如下文件：

```
10.244.1.10 10.244.1.12 10.244.1.14 10.244.1.16 10.244.1.18 10.244.1.2 10.244.1.219 10.244.1.239 10.244.1.3 10.244.1.5 10.244.1.7 10.244.1.9
10.244.1.100 10.244.1.120 10.244.1.140 10.244.1.160 10.244.1.180 10.244.1.20 10.244.1.22 10.244.1.24 10.244.1.30 10.244.1.50 10.244.1.70 10.244.1.90
10.244.1.101 10.244.1.121 10.244.1.141 10.244.1.161 10.244.1.187 10.244.1.200 10.244.1.220 10.244.1.240 10.244.1.31 10.244.1.51 10.244.1.71 10.244.1.91
10.244.1.102 10.244.1.122 10.244.1.142 10.244.1.162 10.244.1.182 10.244.1.201 10.244.1.221 10.244.1.241 10.244.1.32 10.244.1.52 10.244.1.72 10.244.1.92
10.244.1.103 10.244.1.123 10.244.1.143 10.244.1.163 10.244.1.183 10.244.1.202 10.244.1.222 10.244.1.242 10.244.1.33 10.244.1.53 10.244.1.73 10.244.1.93
10.244.1.104 10.244.1.124 10.244.1.144 10.244.1.164 10.244.1.184 10.244.1.203 10.244.1.223 10.244.1.243 10.244.1.34 10.244.1.54 10.244.1.74 10.244.1.94
10.244.1.105 10.244.1.125 10.244.1.145 10.244.1.165 10.244.1.185 10.244.1.204 10.244.1.224 10.244.1.244 10.244.1.35 10.244.1.55 10.244.1.75 10.244.1.95
10.244.1.106 10.244.1.126 10.244.1.146 10.244.1.166 10.244.1.186 10.244.1.205 10.244.1.225 10.244.1.245 10.244.1.36 10.244.1.56 10.244.1.76 10.244.1.96
10.244.1.107 10.244.1.127 10.244.1.147 10.244.1.167 10.244.1.187 10.244.1.206 10.244.1.226 10.244.1.246 10.244.1.37 10.244.1.57 10.244.1.77 10.244.1.97
10.244.1.108 10.244.1.128 10.244.1.148 10.244.1.168 10.244.1.188 10.244.1.207 10.244.1.227 10.244.1.247 10.244.1.38 10.244.1.58 10.244.1.78 10.244.1.98
10.244.1.109 10.244.1.129 10.244.1.149 10.244.1.169 10.244.1.189 10.244.1.208 10.244.1.228 10.244.1.248 10.244.1.39 10.244.1.59 10.244.1.79 10.244.1.99
10.244.1.11 10.244.1.13 10.244.1.15 10.244.1.17 10.244.1.19 10.244.1.209 10.244.1.229 10.244.1.249 10.244.1.4 10.244.1.6 10.244.1.8 last_reserved_ip
10.244.1.110 10.244.1.130 10.244.1.150 10.244.1.170 10.244.1.190 10.244.1.21 10.244.1.23 10.244.1.25 10.244.1.40 10.244.1.60 10.244.1.80
10.244.1.111 10.244.1.131 10.244.1.151 10.244.1.171 10.244.1.191 10.244.1.210 10.244.1.230 10.244.1.250 10.244.1.41 10.244.1.61 10.244.1.81
10.244.1.112 10.244.1.132 10.244.1.152 10.244.1.172 10.244.1.192 10.244.1.211 10.244.1.231 10.244.1.251 10.244.1.42 10.244.1.62 10.244.1.82
10.244.1.113 10.244.1.133 10.244.1.153 10.244.1.173 10.244.1.193 10.244.1.212 10.244.1.232 10.244.1.252 10.244.1.43 10.244.1.63 10.244.1.83
10.244.1.114 10.244.1.134 10.244.1.154 10.244.1.174 10.244.1.194 10.244.1.213 10.244.1.233 10.244.1.253 10.244.1.44 10.244.1.64 10.244.1.84
10.244.1.115 10.244.1.135 10.244.1.155 10.244.1.175 10.244.1.195 10.244.1.214 10.244.1.234 10.244.1.254 10.244.1.45 10.244.1.65 10.244.1.85
10.244.1.116 10.244.1.136 10.244.1.156 10.244.1.176 10.244.1.196 10.244.1.215 10.244.1.235 10.244.1.26 10.244.1.46 10.244.1.66 10.244.1.86
10.244.1.117 10.244.1.137 10.244.1.157 10.244.1.177 10.244.1.197 10.244.1.216 10.244.1.236 10.244.1.27 10.244.1.47 10.244.1.67 10.244.1.87
10.244.1.118 10.244.1.138 10.244.1.158 10.244.1.178 10.244.1.198 10.244.1.217 10.244.1.237 10.244.1.28 10.244.1.48 10.244.1.68 10.244.1.88
10.244.1.119 10.244.1.139 10.244.1.159 10.244.1.179 10.244.1.199 10.244.1.218 10.244.1.238 10.244.1.29 10.244.1.49 10.244.1.69 10.244.1.89
```


这已经将10.244.1.x段的所有ip占满，自然没有available的IP可供新pod使用了。至于为何占满，这个原因尚不明朗。下面两个open issue与这个问题相关：

https://github.com/containernetworking/cni/issues/306

https://github.com/kubernetes/kubernetes/issues/21656

进入到/var/lib/cni/networks/cbr0目录下，执行下面命令可以释放那些可能是kubelet leak的IP资源：

```
for hash in $(tail -n +1 * | grep '^[A-Za-z0-9]*$' | cut -c 1-8); do if [ -z $(docker ps -a | grep $hash | awk '{print $1}') ]; then grep -irl $hash ./; fi; done | xargs rm
```


执行后，目录下的文件列表变成了：

```
ls -l
total 32
drw-r--r-- 2 root root 12288 Dec 27 17:11 ./
drw-r--r-- 3 root root 4096 Dec 27 13:52 ../
-rw-r--r-- 1 root root 64 Dec 27 17:11 10.244.1.2
-rw-r--r-- 1 root root 64 Dec 27 17:11 10.244.1.3
-rw-r--r-- 1 root root 64 Dec 27 17:11 10.244.1.4
-rw-r--r-- 1 root root 10 Dec 27 17:11 last_reserved_ip
```


不过pod仍然处于失败状态，但这次失败的原因又发生了变化：

```
Events:
FirstSeen LastSeen Count From SubObjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
23s 23s 1 {default-scheduler } Normal Scheduled Successfully assigned my-nginx-1948696469-7p4nn to iz2ze39jeyizepdxhwqci6z
22s 1s 22 {kubelet iz2ze39jeyizepdxhwqci6z} Warning FailedSync Error syncing pod, skipping: failed to "SetupNetwork" for "my-nginx-1948696469-7p4nn_default" with SetupNetworkError: "Failed to setup network for pod \"my-nginx-1948696469-7p4nn_default(a40fe652-cc14-11e6-8c42-00163e1001d7)\" using network plugins \"cni\": \"cni0\" already has an IP address different from 10.244.1.1/24; Skipping pod"
```


而/var/lib/cni/networks/cbr0目录下的文件又开始迅速增加！问题陷入僵局。

#### 5、flannel vxlan不通，后端换udp，仍然不通

折腾到这里，基本筋疲力尽了。于是在两个node上执行kubeadm reset，准备重新来过。

kubeadm reset后，之前flannel创建的bridge device cni0和网口设备flannel.1依然健在。为了保证环境彻底恢复到初始状态，我们可以通过下面命令删除这两个设备：

```
# ifconfig cni0 down
# brctl delbr cni0
# ip link delete flannel.1
```


有了前面几个问题的“磨炼”后，重新init和join的k8s cluster显得格外顺利。这次minion node没有再出现什么异常。

```
# kubectl get nodes -o wide
NAME STATUS AGE EXTERNAL-IP
iz25beglnhtz Ready,master 5m <none>
iz2ze39jeyizepdxhwqci6z Ready 51s <none>
# kubectl get pod --all-namespaces
NAMESPACE NAME READY STATUS RESTARTS AGE
default my-nginx-1948696469-71h1l 1/1 Running 0 3m
default my-nginx-1948696469-zwt5g 1/1 Running 0 3m
default my-ubuntu-2560993602-ftdm6 1/1 Running 0 3m
kube-system dummy-2088944543-lmlbh 1/1 Running 0 5m
kube-system etcd-iz25beglnhtz 1/1 Running 0 6m
kube-system kube-apiserver-iz25beglnhtz 1/1 Running 0 6m
kube-system kube-controller-manager-iz25beglnhtz 1/1 Running 0 6m
kube-system kube-discovery-1769846148-l5lfw 1/1 Running 0 5m
kube-system kube-dns-2924299975-mdq5r 4/4 Running 0 5m
kube-system kube-flannel-ds-9zwr1 2/2 Running 0 5m
kube-system kube-flannel-ds-p7xh2 2/2 Running 0 1m
kube-system kube-proxy-dwt5f 1/1 Running 0 5m
kube-system kube-proxy-vm6v2 1/1 Running 0 1m
kube-system kube-scheduler-iz25beglnhtz 1/1 Running 0 6m
```


接下来我们创建my-nginx deployment和service来测试flannel网络的连通性。通过curl my-nginx service的nodeport，发现可以reach master上的两个nginx pod，但是minion node上的pod依旧不通。

在master上看flannel docker的日志：

```
I1228 02:52:22.097083 1 network.go:225] L3 miss: 10.244.1.2
I1228 02:52:22.097169 1 device.go:191] calling NeighSet: 10.244.1.2, 46:6c:7a:a6:06:60
I1228 02:52:22.097335 1 network.go:236] AddL3 succeeded
I1228 02:52:55.169952 1 network.go:220] Ignoring not a miss: 46:6c:7a:a6:06:60, 10.244.1.2
I1228 02:53:00.801901 1 network.go:220] Ignoring not a miss: 46:6c:7a:a6:06:60, 10.244.1.2
I1228 02:53:03.801923 1 network.go:220] Ignoring not a miss: 46:6c:7a:a6:06:60, 10.244.1.2
I1228 02:53:04.801764 1 network.go:220] Ignoring not a miss: 46:6c:7a:a6:06:60, 10.244.1.2
I1228 02:53:05.801848 1 network.go:220] Ignoring not a miss: 46:6c:7a:a6:06:60, 10.244.1.2
I1228 02:53:06.888269 1 network.go:225] L3 miss: 10.244.1.2
I1228 02:53:06.888340 1 device.go:191] calling NeighSet: 10.244.1.2, 46:6c:7a:a6:06:60
I1228 02:53:06.888507 1 network.go:236] AddL3 succeeded
I1228 02:53:39.969791 1 network.go:220] Ignoring not a miss: 46:6c:7a:a6:06:60, 10.244.1.2
I1228 02:53:45.153770 1 network.go:220] Ignoring not a miss: 46:6c:7a:a6:06:60, 10.244.1.2
I1228 02:53:48.154822 1 network.go:220] Ignoring not a miss: 46:6c:7a:a6:06:60, 10.244.1.2
I1228 02:53:49.153774 1 network.go:220] Ignoring not a miss: 46:6c:7a:a6:06:60, 10.244.1.2
I1228 02:53:50.153734 1 network.go:220] Ignoring not a miss: 46:6c:7a:a6:06:60, 10.244.1.2
I1228 02:53:52.154056 1 network.go:225] L3 miss: 10.244.1.2
I1228 02:53:52.154110 1 device.go:191] calling NeighSet: 10.244.1.2, 46:6c:7a:a6:06:60
I1228 02:53:52.154256 1 network.go:236] AddL3 succeeded
```


日志中有大量：“Ignoring not a miss”字样的日志，似乎vxlan网络有问题。这个问题与下面issue中描述颇为接近：

https://github.com/coreos/flannel/issues/427

Flannel默认采用vxlan作为backend，使用kernel vxlan默认的udp 8742端口。Flannel还支持udp的backend，使用udp 8285端口。于是试着更换一下flannel后端。更换flannel后端的步骤如下：

- 将https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml文件下载到本地;
- 修改kube-flannel.yml文件内容：主要是针对net-conf.json属性，增加”Backend”字段属性：

```
---
kind: ConfigMap
apiVersion: v1
metadata:
name: kube-flannel-cfg
namespace: kube-system
labels:
tier: node
app: flannel
data:
cni-conf.json: |
{
"name": "cbr0",
"type": "flannel",
"delegate": {
"isDefaultGateway": true
}
}
net-conf.json: |
{
"Network": "10.244.0.0/16",
"Backend": {
"Type": "udp",
"Port": 8285
}
}
---
... ...
```


- 卸载并重新安装pod网络

```
# kubectl delete -f kube-flannel.yml
configmap "kube-flannel-cfg" deleted
daemonset "kube-flannel-ds" deleted
# kubectl apply -f kube-flannel.yml
configmap "kube-flannel-cfg" created
daemonset "kube-flannel-ds" created
# netstat -an|grep 8285
udp 0 0 123.56.200.187:8285 0.0.0.0:*
```


经过测试发现：udp端口是通的。在两个node上tcpdump -i flannel0 可以看到udp数据包的发送和接收。但是两个node间的pod network依旧不通。

#### 6、failed to register network: failed to acquire lease: node “iz25beglnhtz” not found

正常情况下master node和minion node上的flannel pod的启动日志如下：

master node flannel的运行:

```
I1227 04:56:16.577828 1 main.go:132] Installing signal handlers
I1227 04:56:16.578060 1 kube.go:233] starting kube subnet manager
I1227 04:56:16.578064 1 manager.go:133] Determining IP address of default interface
I1227 04:56:16.578576 1 manager.go:163] Using 123.56.200.187 as external interface
I1227 04:56:16.578616 1 manager.go:164] Using 123.56.200.187 as external endpoint
E1227 04:56:16.579079 1 network.go:106] failed to register network: failed to acquire lease: node "iz25beglnhtz" not found
I1227 04:56:17.583744 1 ipmasq.go:47] Adding iptables rule: -s 10.244.0.0/16 -d 10.244.0.0/16 -j RETURN
I1227 04:56:17.585367 1 ipmasq.go:47] Adding iptables rule: -s 10.244.0.0/16 ! -d 224.0.0.0/4 -j MASQUERADE
I1227 04:56:17.587765 1 ipmasq.go:47] Adding iptables rule: ! -s 10.244.0.0/16 -d 10.244.0.0/16 -j MASQUERADE
I1227 04:56:17.589943 1 manager.go:246] Lease acquired: 10.244.0.0/24
I1227 04:56:17.590203 1 network.go:58] Watching for L3 misses
I1227 04:56:17.590255 1 network.go:66] Watching for new subnet leases
I1227 07:43:27.164103 1 network.go:153] Handling initial subnet events
I1227 07:43:27.164211 1 device.go:163] calling GetL2List() dev.link.Index: 5
I1227 07:43:27.164350 1 device.go:168] calling NeighAdd: 59.110.67.15, ca:50:97:1f:c2:ea
```


minion node上flannel的运行：

```
# docker logs 1f64bd9c0386
I1227 07:43:26.670620 1 main.go:132] Installing signal handlers
I1227 07:43:26.671006 1 manager.go:133] Determining IP address of default interface
I1227 07:43:26.670825 1 kube.go:233] starting kube subnet manager
I1227 07:43:26.671514 1 manager.go:163] Using 59.110.67.15 as external interface
I1227 07:43:26.671575 1 manager.go:164] Using 59.110.67.15 as external endpoint
I1227 07:43:26.746811 1 ipmasq.go:47] Adding iptables rule: -s 10.244.0.0/16 -d 10.244.0.0/16 -j RETURN
I1227 07:43:26.749785 1 ipmasq.go:47] Adding iptables rule: -s 10.244.0.0/16 ! -d 224.0.0.0/4 -j MASQUERADE
I1227 07:43:26.752343 1 ipmasq.go:47] Adding iptables rule: ! -s 10.244.0.0/16 -d 10.244.0.0/16 -j MASQUERADE
I1227 07:43:26.755126 1 manager.go:246] Lease acquired: 10.244.1.0/24
I1227 07:43:26.755444 1 network.go:58] Watching for L3 misses
I1227 07:43:26.755475 1 network.go:66] Watching for new subnet leases
I1227 07:43:27.755830 1 network.go:153] Handling initial subnet events
I1227 07:43:27.755905 1 device.go:163] calling GetL2List() dev.link.Index: 10
I1227 07:43:27.756099 1 device.go:168] calling NeighAdd: 123.56.200.187, ca:68:7c:9b:cc:67
```


但在进行上面问题5的测试过程中，我们发现flannel container的启动日志中有如下错误：

master node:

```
# docker logs c2d1cee3df3d
I1228 06:53:52.502571 1 main.go:132] Installing signal handlers
I1228 06:53:52.502735 1 manager.go:133] Determining IP address of default interface
I1228 06:53:52.503031 1 manager.go:163] Using 123.56.200.187 as external interface
I1228 06:53:52.503054 1 manager.go:164] Using 123.56.200.187 as external endpoint
E1228 06:53:52.503869 1 network.go:106] failed to register network: failed to acquire lease: node "iz25beglnhtz" not found
I1228 06:53:52.503899 1 kube.go:233] starting kube subnet manager
I1228 06:53:53.522892 1 ipmasq.go:47] Adding iptables rule: -s 10.244.0.0/16 -d 10.244.0.0/16 -j RETURN
I1228 06:53:53.524325 1 ipmasq.go:47] Adding iptables rule: -s 10.244.0.0/16 ! -d 224.0.0.0/4 -j MASQUERADE
I1228 06:53:53.526622 1 ipmasq.go:47] Adding iptables rule: ! -s 10.244.0.0/16 -d 10.244.0.0/16 -j MASQUERADE
I1228 06:53:53.528438 1 manager.go:246] Lease acquired: 10.244.0.0/24
I1228 06:53:53.528744 1 network.go:58] Watching for L3 misses
I1228 06:53:53.528777 1 network.go:66] Watching for new subnet leases
```


minion node:

```
# docker logs dcbfef45308b
I1228 05:28:05.012530 1 main.go:132] Installing signal handlers
I1228 05:28:05.012747 1 manager.go:133] Determining IP address of default interface
I1228 05:28:05.013011 1 manager.go:163] Using 59.110.67.15 as external interface
I1228 05:28:05.013031 1 manager.go:164] Using 59.110.67.15 as external endpoint
E1228 05:28:05.013204 1 network.go:106] failed to register network: failed to acquire lease: node "iz2ze39jeyizepdxhwqci6z" not found
I1228 05:28:05.013237 1 kube.go:233] starting kube subnet manager
I1228 05:28:06.041602 1 ipmasq.go:47] Adding iptables rule: -s 10.244.0.0/16 -d 10.244.0.0/16 -j RETURN
I1228 05:28:06.042863 1 ipmasq.go:47] Adding iptables rule: -s 10.244.0.0/16 ! -d 224.0.0.0/4 -j MASQUERADE
I1228 05:28:06.044896 1 ipmasq.go:47] Adding iptables rule: ! -s 10.244.0.0/16 -d 10.244.0.0/16 -j MASQUERADE
I1228 05:28:06.046497 1 manager.go:246] Lease acquired: 10.244.1.0/24
I1228 05:28:06.046780 1 network.go:98] Watching for new subnet leases
I1228 05:28:07.047052 1 network.go:191] Subnet added: 10.244.0.0/24
```


两个Node都有“注册网络”失败的错误：failed to register network: failed to acquire lease: node “xxxx” not found。很难断定是否是因为这两个错误导致的两个node间的网络不通。从整个测试过程来看，这个问题时有时无。在下面flannel issue中也有类似的问题讨论：

https://github.com/coreos/flannel/issues/435

Flannel pod network的诸多问题让我决定暂时放弃在kubeadm创建的kubernetes cluster中继续使用Flannel。

### 四、Calico pod network

Kubernetes支持的pod network add-ons中，除了Flannel，还有[calico](https://projectcalico.org/)、[Weave net](https://www.weave.works/)等。这里我们试试基于边界网关BGP协议实现的Calico pod network。Calico Project针对在kubeadm建立的K8s集群的Pod网络安装也有专门的[文档](http://docs.projectcalico.org/v2.0/getting-started/kubernetes/installation/hosted/kubeadm/)。文档中描述的需求和约束我们均满足，比如：

master node带有kubeadm.alpha.kubernetes.io/role: master标签：

```
# kubectl get nodes -o wide --show-labels
NAME STATUS AGE EXTERNAL-IP LABELS
iz25beglnhtz Ready,master 3m <none> beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubeadm.alpha.kubernetes.io/role=master,kubernetes.io/hostname=iz25beglnhtz
```


在安装calico之前，我们还是要执行kubeadm reset重置环境，并将flannel创建的各种网络设备删除，可参考上面几个小节中的命令。

#### 1、初始化集群

使用calico的kubeadm init无需再指定–pod-network-cidr=10.244.0.0/16 option：

```
# kubeadm init --api-advertise-addresses=10.47.217.91
[kubeadm] WARNING: kubeadm is in alpha, please do not use it for production clusters.
[preflight] Running pre-flight checks
[preflight] Starting the kubelet service
[init] Using Kubernetes version: v1.5.1
[tokens] Generated token: "531b3f.3bd900d61b78d6c9"
[certificates] Generated Certificate Authority key and certificate.
[certificates] Generated API Server key and certificate
[certificates] Generated Service Account signing keys
[certificates] Created keys and certificates in "/etc/kubernetes/pki"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/admin.conf"
[apiclient] Created API client, waiting for the control plane to become ready
[apiclient] All control plane components are healthy after 13.527323 seconds
[apiclient] Waiting for at least one node to register and become ready
[apiclient] First node is ready after 0.503814 seconds
[apiclient] Creating a test deployment
[apiclient] Test deployment succeeded
[token-discovery] Created the kube-discovery deployment, waiting for it to become ready
[token-discovery] kube-discovery is ready after 1.503644 seconds
[addons] Created essential addon: kube-proxy
[addons] Created essential addon: kube-dns
Your Kubernetes master has initialized successfully!
You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
http://kubernetes.io/docs/admin/addons/
You can now join any number of machines by running the following on each node:
kubeadm join --token=531b3f.3bd900d61b78d6c9 10.47.217.91
```


#### 2、创建calico network

```
# kubectl apply -f http://docs.projectcalico.org/v2.0/getting-started/kubernetes/installation/hosted/kubeadm/calico.yaml
configmap "calico-config" created
daemonset "calico-etcd" created
service "calico-etcd" created
daemonset "calico-node" created
deployment "calico-policy-controller" created
job "configure-calico" created
```


实际创建过程需要一段时间，因为calico需要pull 一些images：

```
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
quay.io/calico/node v1.0.0 74bff066bc6a 7 days ago 256.4 MB
calico/ctl v1.0.0 069830246cf3 8 days ago 43.35 MB
calico/cni v1.5.5 ada87b3276f3 12 days ago 67.13 MB
gcr.io/google_containers/etcd 2.2.1 a6cd91debed1 14 months ago 28.19 MB
```


calico在master node本地创建了两个network device：

```
# ip a
... ...
47: tunl0@NONE: <NOARP,UP,LOWER_UP> mtu 1440 qdisc noqueue state UNKNOWN group default qlen 1
link/ipip 0.0.0.0 brd 0.0.0.0
inet 192.168.91.0/32 scope global tunl0
valid_lft forever preferred_lft forever
48: califa32a09679f@if4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
link/ether 62:39:10:55:44:c8 brd ff:ff:ff:ff:ff:ff link-netnsid 0
```


#### 3、minion node join

执行下面命令，将minion node加入cluster：

```
# kubeadm join --token=531b3f.3bd900d61b78d6c9 10.47.217.91
```


calico在minion node上也创建了一个network device:

```
57988: tunl0@NONE: <NOARP,UP,LOWER_UP> mtu 1440 qdisc noqueue state UNKNOWN group default qlen 1
link/ipip 0.0.0.0 brd 0.0.0.0
inet 192.168.136.192/32 scope global tunl0
valid_lft forever preferred_lft forever
```


join成功后，我们查看一下cluster status：

```
# kubectl get pods --all-namespaces -o wide
NAMESPACE NAME READY STATUS RESTARTS AGE IP NODE
kube-system calico-etcd-488qd 1/1 Running 0 18m 10.47.217.91 iz25beglnhtz
kube-system calico-node-jcb3c 2/2 Running 0 18m 10.47.217.91 iz25beglnhtz
kube-system calico-node-zthzp 2/2 Running 0 4m 10.28.61.30 iz2ze39jeyizepdxhwqci6z
kube-system calico-policy-controller-807063459-f21q4 1/1 Running 0 18m 10.47.217.91 iz25beglnhtz
kube-system dummy-2088944543-rtsfk 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
kube-system etcd-iz25beglnhtz 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
kube-system kube-apiserver-iz25beglnhtz 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
kube-system kube-controller-manager-iz25beglnhtz 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
kube-system kube-discovery-1769846148-51wdk 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
kube-system kube-dns-2924299975-fhf5f 4/4 Running 0 23m 192.168.91.1 iz25beglnhtz
kube-system kube-proxy-2s7qc 1/1 Running 0 4m 10.28.61.30 iz2ze39jeyizepdxhwqci6z
kube-system kube-proxy-h2qds 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
kube-system kube-scheduler-iz25beglnhtz 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
```


所有组件都是ok的。似乎是好兆头！但跨node的pod network是否联通，还需进一步探究。

#### 4、探究跨node的pod network联通性

我们依旧利用上面测试flannel网络的my-nginx-svc.yaml和run-my-nginx.yaml，创建my-nginx service和my-nginx deployment。注意：这之前要先在master node上执行一下”kubectl taint nodes –all dedicated-”，以让master node承载work load。

遗憾的是，结果和flannel很相似，分配到master node上http request得到了nginx的响应；minion node上的pod依旧无法联通。

这次我不想在calico这块过多耽搁，我要快速看看下一个候选者：weave net是否满足要求。

### 由于wordpress莫名其妙的问题，导致这篇文章无法发布完整，因此将其拆分为两个部分，本文为第一部分，第二部分请移步[这里](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm-2/)阅读。

© 2016 – 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

我已经顺利安装上了, 目前表示正常

我加了k8s的apt-key，但是apt-get update的时候还是报CAfile丢失的错误，你有遇到这个问题吗？W: Failed to fetch http://apt.kubernetes.io/dists/kubernetes-xenial/main/binary-amd64/Packages server certificate verification failed. CAfile: /etc/ssl/certs/ca-certificates.crt CRLfile: none

没遇到，这个环节比较顺利。

文章没有写完吗？weave-net pod提示:CrashLoopBackOff，也遇到这个问题了，想问下后来是怎么解决的？

wordpress发布有些问题，文章后续部分请在这里阅读：http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm-2/

flannel网络，这个文件的内容/run/flannel/subnet.env ，master节点和minion节点的子网应该不能一样，应该作修改的，master 是FLANNEL_SUBNET=10.244.0.1/24minon应该改为FLANNEL_SUBNET=10.244.1.1/24这样就不会出问题。

我测试的k8s 1.5.1+flannel很稳定，不过在rhel 7上

我在ubuntu 16.04 k8s 1.5.4+docker 1.13.1上测试 ,flannel 失败了，weave是成功的，flannel 失败了还是因为minion节点不通