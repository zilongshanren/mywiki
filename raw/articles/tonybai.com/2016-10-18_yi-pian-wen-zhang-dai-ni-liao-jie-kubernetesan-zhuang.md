---
title: 一篇文章带你了解Kubernetes安装
url: https://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/
published: '2016-10-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一篇文章带你了解Kubernetes安装

由于之前在阿里云上部署的[Docker 1.12.2的Swarm集群](http://tonybai.com/2016/10/11/some-problems-under-swarm-mode-in-docker-1-12/)没能正常展示出其所宣称的Routing mesh和VIP等功能，为了满足项目需要，我们只能转向另外一种容器集群管理和服务编排工具[Kubernetes](http://kubernetes.io/)。


注：之前Docker1.12集群的Routing mesh和VIP功能失效的问题，经过在github上[与Docker开发人员的沟通]，目前已经将问题原因缩小在阿里云的网络上面，目前看是用于承载vxlan数据通信的节点4789 UDP端口不通的问题，针对这个问题，我正在通过阿里云售后工程师做进一步沟通，希望能找出真因。

Kubernetes(以下称k8s)是Google开源的一款容器集群管理工具，是Google内部工具Borg的“开源版”。背靠Google这个高大上的亲爹，k8s一出生就吸引了足够的眼球，并得到了诸多知名IT公司的支持。至于Google开源k8s的初衷，美好的说法是Google希望通过输出自己在容器领域长达10多年的丰富经验，帮助容器领域的开发人员和客户提升开发效率和容器管理的档次。但任何一种公司行为都会有其背后的短期或长期的商业目的，Google作为一个商业公司也不会例外。Google推出k8s到底为啥呢？众说纷纭。一种说法是Google通过k8s输出其容器工具的操作和使用方法、API标准等，为全世界的开发人员使用其公有容器预热并提供“零门槛”体验。

k8s目前是公认的最先进的容器集群管理工具，在1.0版本发布后，k8s的发展速度更加迅猛，并且得到了容器生态圈厂商的全力支持，这包括[coreos](https://coreos.com/)、[rancher](http://tonybai.com/2016/04/14/an-introduction-about-rancher/)等，诸多提供公有云服务的厂商在提供容器服务时也都基于k8s做二次开发来提供基础设施层的支撑，比如华为。可以说k8s也是Docker进军容器集群管理和服务编排领域最为强劲的竞争对手。

不过和已经原生集成了集群管理工具swarmkit的Docker相比，k8s在文档、安装和集群管理方面的体验还有很大的提升空间。k8s最新发布的[1.4版本](http://blog.kubernetes.io/2016/09/kubernetes-1.4-making-it-easy-to-run-on-kuberentes-anywhere.html)就是一个着重在这些方面进行改善的版本。比如1.4版本对于Linux主要发行版本Ubuntu Xenial和Red Hat centos7的用户，可以使用熟悉的apt-get和yum来直接安装Kubernetes。再比如，1.4版本引入了kubeadm命令，将集群启动简化为两条命令，不需要再使用复杂的kube-up脚本。

但对于1.4版本以前的1.3.x版本来说，安装起来的赶脚用最近流行的网络词汇来形容就是“蓝瘦，香菇”，但有些时候我们还不得不去挑战这个过程，本文要带大家了解的就是利用[阿里云](https://www.aliyun.com/)国内区的ECS主机，在[Ubuntu 14.04.4](http://tonybai.com/tag/ubuntu)操作系统上安装[k8s 1.3.7版本](https://github.com/kubernetes/kubernetes/releases/tag/v1.3.7)的方法和安装过程。

#### 零、心理建设

由于k8s是Google出品，很多组件与google是“打断了骨头还连着筋”，因此在国内网络中安装k8s是需要先进行心理建设的^_^，因为和文档中宣称的k8s 1.4版的安装或docker 1.12.x的安装相比，k8s 1.3.7版本的安装简直就是“灾难级”的。

要想让这一过程适当顺利一些，我们必须准备一个“加速器（你懂的）”。利用加速器应对三件事：慢、断和无法连接。

- 慢：国内从github或其他国外公有云上下东西简直太慢了，稍大一些的文件，通常都是几个小时或是10几个小时。
- 断：你说慢就算了，还总断。断了之后，遇到不支持断点续传的，一切还得重来。动不动就上G的文件，重来的时间成本是我们无法承受的。
- 无法连接：这个你知道的，很多托管在google名下的东西，你总是无法下载的。

总而言之，k8s的安装和容器集群的搭建过程是一个“漫长”且可能反复的过程，需要做好心理准备。

BTW，我在安装过程使用的 网友[noah_昨夜星辰](http://weibo.com/p/1005051016825817)推荐的[多态](https://duotai.org)加速器，只需配置一个http_proxy即可，尤其适合服务器后台加速，非常方便，速度也很好。

#### 一、安装模型

k8s的文档不可谓不丰富，尤其在k8s安装这个环节，k8s提供了针对各种云平台、裸机、各类OS甚至各类cluster network model实现的[安装文档](http://kubernetes.io/docs/getting-started-guides/)，你着实得费力挑选一个最适合自己情况的。

由于目前国内阿里云尚未提供[Ubuntu 16.04LTS](https://wiki.ubuntu.com/XenialXerus/ReleaseNotes)版本虚拟机镜像（通过apt-get install可直接安装最新1.4.x版本k8s），我们只能用ubuntu 14.04.x来安装k8s 1.3.x版本，k8s 1.4版本使用了systemd的相关组件，在ubuntu 14.04.x上手工安装k8s 1.4难度估计将是“地狱级”的。网络模型实现我选择coreos提供的[flannel](https://github.com/coreos/flannel)，因此我们需要参考的是由国内浙大团队维护的[这份k8s安装文档](http://kubernetes.io/docs/getting-started-guides/ubuntu)。浙大的这份安装文档针对的是k8s 1.2+的，从文档评分来看，只是二星半，由此推断，完全按照文档中的步骤安装，成功与否要看运气^_^。注意该文档中提到：文档针对ubuntu 14.04是测试ok的，但由于ubuntu15.xx使用systemd替代upstart了，因此无法保证在ubuntu 15.xx上可以安装成功。

关于k8s的安装过程，网上也有很多资料，多数资料一上来就是下载xxx，配置yyy，install zzz，缺少一个k8s安装的总体视图。与内置编排引擎swarmkit的单一docker engine的安装不同，k8s是由一系列核心组件配合协作共同完成容器集群调度和服务编排功能的，安装k8s实际上就是将不同组件安装到承担不同角色的节点上去。

k8s的节点只有两种角色：master和minion，对比Docker swarm集群，master相当于docker swarm集群中的manager，而minion则相当于docker swarm集群中的worker。

在master节点上运行的k8s核心组件包括：

```
# ls /opt/bin|grep kube
kube-apiserver
kube-controller-manager
kubelet
kube-proxy
kube-scheduler
```


在minion节点上，k8s核心组件较少，包括：

```
# ls /opt/bin|grep kube
kubelet
kube-proxy
```


k8s的安装模型可以概述为：在安装机上将k8s的各个组件分别部署到不同角色的节点上去(通过ssh远程登录到各节点)，并启动起来。用下面这个简易图表达起来可能更加形象：

```
安装机(放置k8s的安装程序和安装脚本） ----- install k8s core components to(via ssh) ----> master and minion nodes
```


在安装之前，这里再明确一下我所用的环境信息：

阿里云ECS: Ubuntu 14.04.4 LTS (GNU/Linux 3.19.0-70-generic x86_64)

root@iZ25cn4xxnvZ:~# docker version

Client:

Version: 1.12.2

API version: 1.24

Go version: go1.6.3

Git commit: bb80604

Built: Tue Oct 11 17:00:50 2016

OS/Arch: linux/amd64

Server:

Version: 1.12.2

API version: 1.24

Go version: go1.6.3

Git commit: bb80604

Built: Tue Oct 11 17:00:50 2016

OS/Arch: linux/amd64

#### 二、先决条件

根据浙大团队的那篇在Ubuntu上安装k8s的[文章](http://kubernetes.io/docs/getting-started-guides/ubuntu)，在真正安装k8s组件之前，需要先满足一些先决条件：

##### 1、安装Docker

关于[Docker](http://tonybai.com/tag/docker)的文档，不得不说，写的还是不错的。Docker到目前为止已经发展了许多年了，其在Ubuntu上的安装已经逐渐成熟了。在其[官方文档](https://docs.docker.com/engine/installation/linux/ubuntulinux/)中有针对ubuntu 12.04、14.04和16.04的详细安装说明。如果你的Ubuntu服务器上docker版本较低，还可以用国内Daocloud提供的[一键安装服务](http://get.daocloud.io/#install-docker)来安装最新版的Docker。

##### 2、安装bridge-utils

安装网桥管理工具：

```
[sudo] apt-get install bridge-utils
```


安装后，可以测试一下安装是否ok：

```
root@iZ25cn4xxnvZ:~# brctl show
bridge name bridge id STP enabled interfaces
docker0 8000.0242988b938c no veth901efcb
docker_gwbridge 8000.0242bffb02d5 no veth21546ed
veth984b294
```


##### 3、确保master node可以连接互联网并下载必要的文件

这里要提到的是为master node配置上”加速器”。同时如果master node还承担逻辑上的minion node角色，还需要为节点上Docker配置上加速器（如果加速器是通过代理配置的），minion node上亦是如此，比如：

```
/etc/default/docker
export http_proxy=http://duotai:xxxxx@sheraton.h.xduotai.com:24448
export https_proxy=$http_proxy
```


##### 4、在安装机上配置自动[免密ssh登录](http://tonybai.com/2009/07/17/physical-examination-and-ssh-and-safari4/)各个master node 和minion node

我在阿里云上开了两个ECS（暂成为node1 – 10.47.136.60和node2 – 10.46.181.146），我的k8s集群就由这两个物理node承载，但在逻辑上node1和node2承担着多种角色，逻辑上这是一个由一个master node和两个minion node组成的k8s集群：

```
安装机：node1
master node：node1
minion node: node1和node2
```


因此为了满足安装机到各个k8s node免密ssh登录的先决条件，我需要实现从安装机(node1)到master node(node1)和minion node(node1和node2)的免费ssh登录设置。

在安装机node上执行：

```
# ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
... ...
```


安装机免密登录逻辑意义上的master node(实际上就是登录自己，即node1）：

```
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```


安装机免费登录minion node(node2)：

```
将公钥复制到server：
#scp ~/.ssh/id_rsa.pub root@10.46.181.146:/root/id_rsa.pub
The authenticity of host '10.46.181.146 (10.46.181.146)' can't be established.
ECDSA key fingerprint is b7:31:8d:33:f5:6e:ef:a4:a1:cc:72:5f:cf:68:c6:3d.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.46.181.146' (ECDSA) to the list of known hosts.
root@10.46.181.146's password:
id_rsa.pub
```


在minion node，即node2上，导入安装机的公钥并修改访问权限：

```
cat ~/id_rsa.pub >> ~/.ssh/authorized_keys
root@iZ25mjza4msZ:~# chmod 700 ~/.ssh
root@iZ25mjza4msZ:~# chmod 600 ~/.ssh/authorized_keys
```


配置完成，你可以在安装机上测试一下到自身(node1)和到node2的免密登录，以免密登录node2为例：

```
root@iZ25cn4xxnvZ:~/.ssh# ssh 10.46.181.146
Welcome to Ubuntu 14.04.4 LTS (GNU/Linux 3.19.0-70-generic x86_64)
* Documentation: https://help.ubuntu.com/
New release '16.04.1 LTS' available.
Run 'do-release-upgrade' to upgrade to it.
Welcome to aliyun Elastic Compute Service!
Last login: Thu Oct 13 12:55:21 2016 from 218.25.32.210
```


##### 5、下载pause-amd64镜像

k8s集群启动后，启动容器时会去下载google的gcr.io/google_containers下的一个pause-amd64镜像，为了避免那时出错时不便于查找，这些先下手为强，先通过“加速器”将该镜像下载到各个k8s node上：

修改/etc/default/docker，添加带有加速器的http_proxy/https_proxy，并增加–insecure-registry gcr.io

```
# If you need Docker to use an HTTP proxy, it can also be specified here.
export http_proxy=http://duotai:xxxx@sheraton.h.xduotai.com:24448
export https_proxy=http://duotai:xxxx@sheraton.h.xduotai.com:24448
# This is also a handy place to tweak where Docker's temporary files go.
#export TMPDIR="/mnt/bigdrive/docker-tmp"
DOCKER_OPTS="$DOCKER_OPTS -H unix:///var/run/docker.sock -H tcp://0.0.0.0:2375 --insecure-registry gcr.io"
```


重启docker daemon服务。下载pause-amd64 image：

```
root@iZ25cn4xxnvZ:~# docker search gcr.io/google_containers/pause-amd64
NAME DESCRIPTION STARS OFFICIAL AUTOMATED
google_containers/pause-amd64 0
root@iZ25cn4xxnvZ:~# docker pull gcr.io/google_containers/pause-amd64
Using default tag: latest
Pulling repository gcr.io/google_containers/pause-amd64
Tag latest not found in repository gcr.io/google_containers/pause-amd64
```


latest标签居然都没有，尝试下载3.0标签的pause-amd64：

```
root@iZ25cn4xxnvZ:~# docker pull gcr.io/google_containers/pause-amd64:3.0
3.0: Pulling from google_containers/pause-amd64
a3ed95caeb02: Pull complete
f11233434377: Pull complete
Digest: sha256:163ac025575b775d1c0f9bf0bdd0f086883171eb475b5068e7defa4ca9e76516
Status: Downloaded newer image for gcr.io/google_containers/pause-amd64:3.0
```


#### 三、设置工作目录，进行安装前的各种配置

到目前为止，所有node上，包括安装机node上还是“一无所有”的。接下来，我们开始在安装机node上做文章。

俗话说：“巧妇不为无米炊”。安装机想在各个node上安装k8s组件，安装机本身就要有”米”才行，这个米就是k8s源码包或release包中的安装脚本。

在官方文档中，这个获取“米”的步骤为clone k8s的源码库。由于之前就下载了[k8s 1.3.7的release包](https://github.com/kubernetes/kubernetes/releases/download/v1.3.7/kubernetes.tar.gz)，这里我就直接使用release包中的”米”。

解压kubernetes.tar.gz后，在当前目录下将看到kubernetes目录：

```
root@iZ25cn4xxnvZ:~/k8stest/1.3.7/kubernetes# ls -F
cluster/ docs/ examples/ federation/ LICENSES platforms/ README.md server/ third_party/ Vagrantfile version
```


这个kubernetes目录就是我们安装k8s的**工作目录**。由于我们在ubuntu上安装k8s，因此我们实际上要使用的脚本都在工作目录下的cluster/ubuntu下面，后续有详细说明。

在安装机上，我们最终是要执行这样一句脚本的：

```
KUBERNETES_PROVIDER=ubuntu ./cluster/kube-up.sh
```


在provider=ubuntu的情况下，./cluster/kube-up.sh最终会调用到./cluster/ubuntu/util.sh中的kube-up shell函数，kube-up函数则会调用./cluster/ubuntu/download-release.sh下载k8s安装所使用到的所有包，包括k8s的安装包(kubernetes.tar.gz)、etcd和flannel等。由于之前我们已经下载完k8s的1.3.7版本release包了，这里我们就需要对down-release.sh做一些修改，防止重新下载，导致安装时间过长。

```
./cluster/ubuntu/download-release.sh
# KUBE_VERSION=$(get_latest_version_number | sed 's/^v//')
#curl -L https://github.com/kubernetes/kubernetes/releases/download/v${KUBE_VERSION}/kubernetes.tar.gz -o kubernetes.tar.gz
```


这种情况下，你还需要把已经下载的kubernetes.tar.gz文件copy一份，放到./cluster/ubuntu下面。

如果你的网络访问国外主机足够快，你还有足够耐心，那么你大可忽略上面脚本修改的步骤。

在真正执行./cluster/kube-up.sh之前，安装机还需要知道：

1、k8s物理集群都有哪些node组成，node的角色都是什么？

2、k8s的各个依赖程序，比如etcd的版本是什么？

我们需要通过配置./cluster/ubuntu/config-default.sh让./cluster/kube-up.sh获取这些信息。

```
./cluster/ubuntu/config-default.sh
# node信息，本集群由两个物理node组成，其中第一个node既是master，也是minion
export nodes=${nodes:-"root@10.47.136.60 root@10.46.181.146"}
roles=${roles:-"ai i"}
# minion node个数
export NUM_NODES=${NUM_NODES:-2}
# 为安装脚本配置网络代理，这里主要是为了使用加速器，方便或加速下载一些包
PROXY_SETTING=${PROXY_SETTING:-"http_proxy=http://duotai:xxxx@sheraton.h.xduotai.com:24448 https_proxy=http://duotai:xxxx@sheraton.h.xduotai.com:24448"}
```


通过环境变量设置k8s要下载的依赖程序的版本：

```
export KUBE_VERSION=1.3.7
export FLANNEL_VERSION=0.5.5
export ETCD_VERSION=3.0.12
```


如果不设置环境变量，./cluster/ubuntu/download-release.sh中默认的版本号将是：

```
k8s： 最新版本
etcd：2.3.1
flannel : 0.5.5
```


#### 四、执行安装

在安装机上，进入./cluster目录，执行如下安装命令：

```
KUBERNETES_PROVIDER=ubuntu ./kube-up.sh
```


执行输出如下：

```
root@iZ25cn4xxnvZ:~/k8stest/1.3.7/kubernetes/cluster# KUBERNETES_PROVIDER=ubuntu ./kube-up.sh
... Starting cluster using provider: ubuntu
... calling verify-prereqs
Identity added: /root/.ssh/id_rsa (/root/.ssh/id_rsa)
... calling kube-up
~/k8stest/1.3.7/kubernetes/cluster/ubuntu ~/k8stest/1.3.7/kubernetes/cluster
Prepare flannel 0.5.5 release ...
% Total % Received % Xferd Average Speed Time Time Time Current
Dload Upload Total Spent Left Speed
100 608 0 608 0 0 410 0 --:--:-- 0:00:01 --:--:-- 409
100 3408k 100 3408k 0 0 284k 0 0:00:11 0:00:11 --:--:-- 389k
Prepare etcd 3.0.12 release ...
% Total % Received % Xferd Average Speed Time Time Time Current
Dload Upload Total Spent Left Speed
100 607 0 607 0 0 388 0 --:--:-- 0:00:01 --:--:-- 388
3 9.8M 3 322k 0 0 84238 0 0:02:02 0:00:03 0:01:59 173k
100 9.8M 100 9.8M 0 0 327k 0 0:00:30 0:00:30 --:--:-- 344k
Prepare kubernetes 1.3.7 release ...
~/k8stest/1.3.7/kubernetes/cluster/ubuntu/kubernetes/server ~/k8stest/1.3.7/kubernetes/cluster/ubuntu ~/k8stest/1.3.7/kubernetes/cluster
~/k8stest/1.3.7/kubernetes/cluster/ubuntu ~/k8stest/1.3.7/kubernetes/cluster
Done! All your binaries locate in kubernetes/cluster/ubuntu/binaries directory
~/k8stest/1.3.7/kubernetes/cluster
Deploying master and node on machine 10.47.136.60
saltbase/salt/generate-cert/make-ca-cert.sh: No such file or directory
easy-rsa.tar.gz 100% 42KB 42.4KB/s 00:00
config-default.sh 100% 5610 5.5KB/s 00:00
util.sh 100% 29KB 28.6KB/s 00:00
kubelet.conf 100% 644 0.6KB/s 00:00
kube-proxy.conf 100% 684 0.7KB/s 00:00
kubelet 100% 2158 2.1KB/s 00:00
kube-proxy 100% 2233 2.2KB/s 00:00
etcd.conf 100% 709 0.7KB/s 00:00
kube-scheduler.conf 100% 674 0.7KB/s 00:00
kube-apiserver.conf 100% 674 0.7KB/s 00:00
kube-controller-manager.conf 100% 744 0.7KB/s 00:00
kube-scheduler 100% 2360 2.3KB/s 00:00
kube-controller-manager 100% 2672 2.6KB/s 00:00
kube-apiserver 100% 2358 2.3KB/s 00:00
etcd 100% 2073 2.0KB/s 00:00
reconfDocker.sh 100% 2074 2.0KB/s 00:00
kube-scheduler 100% 56MB 56.2MB/s 00:01
kube-controller-manager 100% 95MB 95.4MB/s 00:01
kube-apiserver 100% 105MB 104.9MB/s 00:00
etcdctl 100% 18MB 17.6MB/s 00:00
flanneld 100% 16MB 15.8MB/s 00:01
etcd 100% 2074 2.0KB/s 00:00
kube-scheduler 100% 56MB 56.2MB/s 0 100% 56MB 56.2MB/s 00:01
kube-controller-manager 100% 95MB 95.4MB/s 100% 95MB 95.4MB/s 00:01
kube-apiserver 100% 105MB 104.9MB/s 100% 105MB 104.9MB/s 00:00
etcdctl 100% 18MB 17.6MB/s us 100% 18MB 17.6MB/s 00:00
flanneld 10 100% 16MB 15.8MB/sge 100% 16MB 15.8MB/s 00:01
... ...
```


结果中并没有出现代表着安装成功的如下log字样：

```
Cluster validation succeeded
```


查看上面安装日志输出，发现在向10.47.136.60 master节点部署组件时，出现如下错误日志：

```
saltbase/salt/generate-cert/make-ca-cert.sh: No such file or directory
```


查看一下./cluster下的确没有saltbase目录，这个问题在网上找到了答案，解决方法如下：

```
k8s安装包目录下，在./server/kubernetes下已经有salt包：kubernetes-salt.tar.gz，解压后，将saltbase整个目录cp到.cluster/下即可。
```


再次执行：KUBERNETES_PROVIDER=ubuntu ./kube-up.sh，可以看到如下执行输出：

```
... ...
Deploying master and node on machine 10.47.136.60
make-ca-cert.sh 100% 4028 3.9KB/s 00:00
easy-rsa.tar.gz 100% 42KB 42.4KB/s 00:00
config-default.sh 100% 5632 5.5KB/s 00:00
util.sh 100% 29KB 28.6KB/s 00:00
kubelet.conf 100% 644 0.6KB/s 00:00
kube-proxy.conf 100% 684 0.7KB/s 00:00
kubelet 100% 2158 2.1KB/s 00:00
kube-proxy 100% 2233 2.2KB/s 00:00
etcd.conf 100% 709 0.7KB/s 00:00
kube-scheduler.conf 100% 674 0.7KB/s 00:00
kube-apiserver.conf 100% 674 0.7KB/s 00:00
kube-controller-manager.conf 100% 744 0.7KB/s 00:00
kube-scheduler 100% 2360 2.3KB/s 00:00
kube-controller-manager 100% 2672 2.6KB/s 00:00
kube-apiserver 100% 2358 2.3KB/s 00:00
etcd 100% 2073 2.0KB/s 00:00
reconfDocker.sh 100% 2074 2.0KB/s 00:00
kube-scheduler 100% 56MB 56.2MB/s 00:01
kube-controller-manager 100% 95MB 95.4MB/s 00:00
kube-apiserver 100% 105MB 104.9MB/s 00:01
etcdctl 100% 18MB 17.6MB/s 00:00
flanneld 100% 16MB 15.8MB/s 00:00
etcd 100% 19MB 19.3MB/s 00:00
flanneld 100% 16MB 15.8MB/s 00:00
kubelet 100% 103MB 103.1MB/s 00:01
kube-proxy 100% 48MB 48.4MB/s 00:00
flanneld.conf 100% 577 0.6KB/s 00:00
flanneld 100% 2121 2.1KB/s 00:00
flanneld.conf 100% 568 0.6KB/s 00:00
flanneld 100% 2131 2.1KB/s 00:00
etcd start/running, process 7997
Error: dial tcp 127.0.0.1:2379: getsockopt: connection refused
{"Network":"172.16.0.0/16", "Backend": {"Type": "vxlan"}}
{"Network":"172.16.0.0/16", "Backend": {"Type": "vxlan"}}
docker stop/waiting
docker start/running, process 8220
Connection to 10.47.136.60 closed.
Deploying node on machine 10.46.181.146
config-default.sh 100% 5632 5.5KB/s 00:00
util.sh 100% 29KB 28.6KB/s 00:00
reconfDocker.sh 100% 2074 2.0KB/s 00:00
kubelet.conf 100% 644 0.6KB/s 00:00
kube-proxy.conf 100% 684 0.7KB/s 00:00
kubelet 100% 2158 2.1KB/s 00:00
kube-proxy 100% 2233 2.2KB/s 00:00
flanneld 100% 16MB 15.8MB/s 00:00
kubelet 100% 103MB 103.1MB/s 00:01
kube-proxy 100% 48MB 48.4MB/s 00:00
flanneld.conf 100% 577 0.6KB/s 00:00
flanneld 100% 2121 2.1KB/s 00:00
flanneld start/running, process 2365
docker stop/waiting
docker start/running, process 2574
Connection to 10.46.181.146 closed.
Validating master
Validating root@10.47.136.60
Validating root@10.46.181.146
Using master 10.47.136.60
cluster "ubuntu" set.
user "ubuntu" set.
context "ubuntu" set.
switched to context "ubuntu".
Wrote config for ubuntu to /root/.kube/config
... calling validate-cluster
Error from server: an error on the server has prevented the request from succeeding
(kubectl failed, will retry 2 times)
Error from server: an error on the server has prevented the request from succeeding
(kubectl failed, will retry 1 times)
Error from server: an error on the server has prevented the request from succeeding
('kubectl get nodes' failed, giving up)
```


安装并未成功，至少calling validate-cluster后的validation过程并未成功。

但是和第一次的失败有所不同的是，在master node和minion node上，我们都可以看到已经安装并启动了的k8s核心组件：

master node：

```
root@iZ25cn4xxnvZ:~/k8stest/1.3.7/kubernetes/cluster# ps -ef|grep kube
root 8006 1 0 16:39 ? 00:00:00 /opt/bin/kube-scheduler --logtostderr=true --master=127.0.0.1:8080
root 8008 1 0 16:39 ? 00:00:01 /opt/bin/kube-apiserver --insecure-bind-address=0.0.0.0 --insecure-port=8080 --etcd-servers=http://127.0.0.1:4001 --logtostderr=true --service-cluster-ip-range=192.168.3.0/24 --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,SecurityContextDeny,ResourceQuota --service-node-port-range=30000-32767 --advertise-address=10.47.136.60 --client-ca-file=/srv/kubernetes/ca.crt --tls-cert-file=/srv/kubernetes/server.cert --tls-private-key-file=/srv/kubernetes/server.key
root 8009 1 0 16:39 ? 00:00:02 /opt/bin/kube-controller-manager --master=127.0.0.1:8080 --root-ca-file=/srv/kubernetes/ca.crt --service-account-private-key-file=/srv/kubernetes/server.key --logtostderr=true
root 8021 1 0 16:39 ? 00:00:04 /opt/bin/kubelet --hostname-override=10.47.136.60 --api-servers=http://10.47.136.60:8080 --logtostderr=true --cluster-dns=192.168.3.10 --cluster-domain=cluster.local --config=
root 8023 1 0 16:39 ? 00:00:00 /opt/bin/kube-proxy --hostname-override=10.47.136.60 --master=http://10.47.136.60:8080 --logtostderr=true
```


minion node：

```
root@iZ25mjza4msZ:~# ps -ef|grep kube
root 2370 1 0 16:39 ? 00:00:04 /opt/bin/kubelet --hostname-override=10.46.181.146 --api-servers=http://10.47.136.60:8080 --logtostderr=true --cluster-dns=192.168.3.10 --cluster-domain=cluster.local --config=
root 2371 1 0 16:39 ? 00:00:00 /opt/bin/kube-proxy --hostname-override=10.46.181.146 --master=http://10.47.136.60:8080 --logtostderr=true
```


那为什么安装节点上的安装脚本在验证安装是否成功时一直阻塞、最终超时失败呢？我在安装节点，同时也是master node上执行了一下kubectl get node命令：

```
root@iZ25cn4xxnvZ:~/k8stest/1.3.7/kubernetes/cluster# kubectl get nodes
Error from server: an error on the server ("<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">\n<html><head>\n<meta type=\"copyright\" content=\"Copyright (C) 1996-2015 The Squid Software Foundation and contributors\">\n<meta http-equiv=\"Content-Type\" CONTENT=\"text/html; charset=utf-8\">\n<title>ERROR: The requested URL could not be retrieved</title>\n<style type=\"text/css\"><!-- \n /*\n * Copyright (C) 1996-2015 The Squid Software Foundation and contributors\n *\n * Squid software is distributed under GPLv2+ license and includes\n * contributions from numerous individuals and organizations.\n * Please see the COPYING and CONTRIBUTORS files for details.\n */\n\n/*\n Stylesheet for Squid Error pages\n Adapted from design by Free CSS Templates\n http://www.freecsstemplates.org\n Released for free under a Creative Commons Attribution 2.5 License\n*/\n\n/* Page basics */\n* {\n\tfont-family: verdana, sans-serif;\n}\n\nhtml body {\n\tmargin: 0;\n\tpadding: 0;\n\tbackground: #efefef;\n\tfont-size: 12px;\n\tcolor: #1e1e1e;\n}\n\n/* Page displayed title area */\n#titles {\n\tmargin-left: 15px;\n\tpadding: 10px;\n\tpadding-left: 100px;\n\tbackground: url('/squid-internal-static/icons/SN.png') no-repeat left;\n}\n\n/* initial title */\n#titles h1 {\n\tcolor: #000000;\n}\n#titles h2 {\n\tcolor: #000000;\n}\n\n/* special event: FTP success page titles */\n#titles ftpsuccess {\n\tbackground-color:#00ff00;\n\twidth:100%;\n}\n\n/* Page displayed body content area */\n#content {\n\tpadding: 10px;\n\tbackground: #ffffff;\n}\n\n/* General text */\np {\n}\n\n/* error brief description */\n#error p {\n}\n\n/* some data which may have caused the problem */\n#data {\n}\n\n/* the error message received from the system or other software */\n#sysmsg {\n}\n\npre {\n font-family:sans-serif;\n}\n\n/* special event: FTP / Gopher directory listing */\n#dirmsg {\n font-family: courier;\n color: black;\n font-size: 10pt;\n}\n#dirlisting {\n margin-left: 2%;\n margin-right: 2%;\n}\n#dirlisting tr.entry td.icon,td.filename,td.size,td.date {\n border-bottom: groove;\n}\n#dirlisting td.size {\n width: 50px;\n text-align: right;\n padding-right: 5px;\n}\n\n/* horizontal lines */\nhr {\n\tmargin: 0;\n}\n\n/* page displayed footer area */\n#footer {\n\tfont-size: 9px;\n\tpadding-left: 10px;\n}\n\n\nbody\n:lang(fa) { direction: rtl; font-size: 100%; font-family: Tahoma, Roya, sans-serif; float: right; }\n:lang(he) { direction: rtl; }\n --></style>\n</head><body id=ERR_CONNECT_FAIL>\n<div id=\"titles\">\n<h1>ERROR</h1>\n<h2>The requested URL could not be retrieved</h2>\n</div>\n<hr>\n\n<div id=\"content\">\n<p>The following error was encountered while trying to retrieve the URL: <a href=\"http://10.47.136.60:8080/api\">http://10.47.136.60:8080/api</a></p>\n\n<blockquote id=\"error\">\n<p><b>Connection to 10.47.136.60 failed.</b></p>\n</blockquote>\n\n<p id=\"sysmsg\">The system returned: <i>(110) Connection timed out</i></p>\n\n<p>The remote host or network may be down. Please try the request again.</p>\n\n<p>Your cache administrator is <a href=\"mailto:webmaster?subject=CacheErrorInfo%20-%20ERR_CONNECT_FAIL&body=CacheHost%3A%20192-241-236-182%0D%0AErrPage%3A%20ERR_CONNECT_FAIL%0D%0AErr%3A%20(110)%20Connection%20timed%20out%0D%0ATimeStamp%3A%20Thu,%2013%20Oct%202016%2008%3A49%3A35%20GMT%0D%0A%0D%0AClientIP%3A%20127.0.0.1%0D%0AServerIP%3A%2010.47.136.60%0D%0A%0D%0AHTTP%20Request%3A%0D%0AGET%20%2Fapi%20HTTP%2F1.1%0AUser-Agent%3A%20kubectl%2Fv1.4.0%20(linux%2Famd64)%20kubernetes%2F4b28af1%0D%0AAccept%3A%20application%2Fjson,%20*%2F*%0D%0AAccept-Encoding%3A%20gzip%0D%0AHost%3A%2010.47.136.60%3A8080%0D%0A%0D%0A%0D%0A\">webmaster</a>.</p>\n\n<br>\n</div>\n\n<hr>\n<div id=\"footer\">\n<p>Generated Thu, 13 Oct 2016 08:49:35 GMT by 192-241-236-182 (squid/3.5.12)</p>\n<!-- ERR_CONNECT_FAIL -->\n</div>\n</body></html>") has prevented the request from succeeding
```


可以看到kubectl得到一坨信息，这是一个html页面内容的数据，仔细分析body内容，我们可以看到：

```
<body id=ERR_CONNECT_FAIL>\n<div id=\"titles\">\n<h1>ERROR</h1>\n<h2>The requested URL could not be retrieved</h2>\n</div>\n<hr>\n\n<div id=\"content\">\n<p>The following error was encountered while trying to retrieve the URL: <a href=\"http://10.47.136.60:8080/api\">http://10.47.136.60:8080/api</a></p>\n\n<blockquote id=\"error\">\n<p><b>Connection to 10.47.136.60 failed.</b></p>\n</blockquote>\n\n<p id=\"sysmsg\">The system returned: <i>(110) Connection timed out</i></p>\n\n<p>The remote host or network may be down. Please try the request again.</p>
```


kubectl在访问http://10.47.136.60:8080/api这个url时出现了timed out错误。在master node上直接执行curl http://10.47.136.60:8080/api也是这个错误。猜想是否是我.bashrc中的http_proxy在作祟。于是在.bashrc中增加no_proxy:

```
export no_proxy='10.47.136.60,10.46.181.146,localhost,127.0.0.1'
```


生效后，再在master node上执行curl：

```
# curl http://10.47.136.60:8080/api
{
"kind": "APIVersions",
"versions": [
"v1"
],
"serverAddressByClientCIDRs": [
{
"clientCIDR": "0.0.0.0/0",
"serverAddress": "10.47.136.60:6443"
}
]
}
```


看来问题原因就是安装程序的PROXY_SETTING中没有加入no_proxy的设置的缘故，于是修改config-default.sh中的代理设置：

```
PROXY_SETTING=${PROXY_SETTING:-"http_proxy=http://duotai:xxxx@sheraton.h.xduotai.com:24448 https_proxy=http://duotai:xxxx@sheraton.h.xduotai.com:24448 no_proxy=10.47.136.60,10.46.181.146,localhost,127.0.0.1"}
```


然后重新deploy：

```
root@iZ25cn4xxnvZ:~/k8stest/1.3.7/kubernetes/cluster# KUBERNETES_PROVIDER=ubuntu ./kube-up.sh
... Starting cluster using provider: ubuntu
... calling verify-prereqs
Identity added: /root/.ssh/id_rsa (/root/.ssh/id_rsa)
... calling kube-up
~/k8stest/1.3.7/kubernetes/cluster/ubuntu ~/k8stest/1.3.7/kubernetes/cluster
Prepare flannel 0.5.5 release ...
Prepare etcd 3.0.12 release ...
Prepare kubernetes 1.3.7 release ...
Done! All your binaries locate in kubernetes/cluster/ubuntu/binaries directory
~/k8stest/1.3.7/kubernetes/cluster
Deploying master and node on machine 10.47.136.60
make-ca-cert.sh 100% 4028 3.9KB/s 00:00
easy-rsa.tar.gz 100% 42KB 42.4KB/s 00:00
config-default.sh 100% 5678 5.5KB/s 00:00
... ...
cp: cannot create regular file ‘/opt/bin/etcd’: Text file busy
cp: cannot create regular file ‘/opt/bin/flanneld’: Text file busy
cp: cannot create regular file ‘/opt/bin/kube-apiserver’: Text file busy
cp: cannot create regular file ‘/opt/bin/kube-controller-manager’: Text file busy
cp: cannot create regular file ‘/opt/bin/kube-scheduler’: Text file busy
Connection to 10.47.136.60 closed.
Deploying master and node on machine 10.47.136.60 failed
```


重新部署时，由于之前k8s cluster在各个node的组件已经启动，因此failed。我们需要通过

```
KUBERNETES_PROVIDER=ubuntu kube-down.sh
```


将k8s集群停止后再尝试up，或者如果不用这个kube-down.sh脚本，也可以在各个节点上手动shutdown各个k8s组件(master上有五个核心组件，minion node上有两个核心组件，另外别忘了停止etcd和flanneld服务)，以kube-controller-manager为例：

```
service kube-controller-manager stop
```


即可。

再次执行kube-up.sh：

```
... ...
.. calling validate-cluster
Waiting for 2 ready nodes. 1 ready nodes, 2 registered. Retrying.
Found 2 node(s).
NAME STATUS AGE
10.46.181.146 Ready 4h
10.47.136.60 Ready 4h
Validate output:
NAME STATUS MESSAGE ERROR
scheduler Healthy ok
controller-manager Healthy ok
etcd-0 Healthy {"health": "true"}
Cluster validation succeeded
Done, listing cluster services:
Kubernetes master is running at http://10.47.136.60:8080
To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```


通过字样：”Cluster validation succeeded”可以证明我们成功安装了k8s集群。

执行kubectl get node可以看到当前集群的节点组成情况：

```
# kubectl get node
NAME STATUS AGE
10.46.181.146 Ready 4h
10.47.136.60 Ready 4h
```


通过执行kubectl cluster-info dump 可以看到k8s集群更为详尽的信息。

#### 五、测试k8s的service特性

之所以采用k8s，初衷就是因为Docker 1.12在阿里云搭建的swarm集群的VIP和Routing mesh机制不好用。因此，在k8s集群部署成功后，我们需要测试一下这两种机制在k8s上是否能够获得支持。

k8s中一些关于集群的抽象概念，比如node、deployment、pod、service等，这里就不赘述了，需要的话可以参考[这里](http://kubernetes.io/docs/user-guide/)的Concept guide。

##### 1、集群内负载均衡

在k8s集群中，有一个等同于docker swarm vip的概念，成为cluster ip，k8s回为每个service分配一个cluster ip，这个cluster ip在service生命周期中不会改变，并且访问cluster ip的请求会被自动负载均衡到service里的后端container中。

我们来启动一个replicas= 2的nginx service，我们需要先从一个描述文件来部署一个deployment：

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


启动deployment:

```
root@iZ25cn4xxnvZ:~/k8stest/demo# kubectl create -f ./run-my-nginx.yaml
deployment "my-nginx" created
root@iZ25cn4xxnvZ:~/k8stest/demo# kubectl get deployment
NAME DESIRED CURRENT UP-TO-DATE AVAILABLE AGE
my-nginx 2 2 2 2 9s
root@iZ25cn4xxnvZ:~/k8stest/demo# kubectl get pods -l run=my-nginx -o wide
NAME READY STATUS RESTARTS AGE IP NODE
my-nginx-2395715568-2t6xe 1/1 Running 0 50s 172.16.57.3 10.46.181.146
my-nginx-2395715568-gpljv 1/1 Running 0 50s 172.16.99.2 10.47.136.60
```


可以看到my-nginx deployment已经成功启动，并且被调度在两个minion node上。

接下来，我们将deployment转化为service:

```
# kubectl expose deployment/my-nginx
service "my-nginx" exposed
root@iZ25cn4xxnvZ:~/k8stest/demo# kubectl get svc my-nginx
NAME CLUSTER-IP EXTERNAL-IP PORT(S) AGE
my-nginx 192.168.3.239 <none> 80/TCP 15s
# kubectl describe svc my-nginx
Name: my-nginx
Namespace: default
Labels: run=my-nginx
Selector: run=my-nginx
Type: ClusterIP
IP: 192.168.3.239
Port: <unset> 80/TCP
Endpoints: 172.16.57.3:80,172.16.99.2:80
Session Affinity: None
```


我们看到通过expose命令，可以将deployment转化为service，转化后，my-nginx service被分配了一个cluster-ip：192.168.3.239。

我们启动一个client container用于测试内部负载均衡：

```
root@iZ25cn4xxnvZ:~/k8stest/demo# kubectl run myclient --image=registry.cn-hangzhou.aliyuncs.com/mioss/test --replicas=1 --command -- tail -f /var/log/bootstrap.log
deployment "myclient" created
root@iZ25cn4xxnvZ:~/k8stest/demo# kubectl get pods
NAME READY STATUS RESTARTS AGE
my-nginx-2395715568-2t6xe 1/1 Running 0 24m
my-nginx-2395715568-gpljv 1/1 Running 0 24m
myclient-1460251692-g7rnl 1/1 Running 0 21s
```


通过docker exec -it containerid /bin/bash进入myclient容器内，通过curl向上面的cluster-ip发起http请求：

```
root@myclient-1460251692-g7rnl:/# curl -v 192.168.3.239:80
```


同时在两个minion节点上，通过docker logs -f查看my-nginx service下面的两个nginx container实例日志，可以看到两个container轮询收到http request:

```
root@iZ25cn4xxnvZ:~/k8stest/demo# docker logs -f ccc2f9bb814a
172.16.57.0 - - [17/Oct/2016:06:35:57 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
172.16.57.0 - - [17/Oct/2016:06:36:13 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
172.16.57.0 - - [17/Oct/2016:06:37:06 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
172.16.57.0 - - [17/Oct/2016:06:37:45 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
172.16.57.0 - - [17/Oct/2016:06:37:46 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
172.16.57.0 - - [17/Oct/2016:06:37:50 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
root@iZ25mjza4msZ:~# docker logs -f 0e533ec2dc71
172.16.57.4 - - [17/Oct/2016:06:33:14 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
172.16.57.4 - - [17/Oct/2016:06:33:18 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
172.16.57.4 - - [17/Oct/2016:06:34:06 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
172.16.57.4 - - [17/Oct/2016:06:34:09 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
172.16.57.4 - - [17/Oct/2016:06:35:45 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
172.16.57.4 - - [17/Oct/2016:06:36:59 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
```


cluster-ip机制有效。

##### 2、nodeport机制

k8s通过nodeport机制实现类似docker的routing mesh，但底层机制和原理是不同的。

k8s的nodePort的原理是在集群中的每个node上开了一个端口，将访问该端口的流量导入到该node上的kube-proxy，然后再由kube-proxy进一步讲流量转发给该对应该nodeport的service的alive的pod上。

我们先来删除掉前面启动的my-nginx service，再重新创建支持nodeport的新my-nginx service。在k8s delete service有点讲究，我们删除service的目的不仅要删除service“索引”，还要stop并删除该service对应的Pod中的所有docker container。但在k8s中，直接删除service或delete pods都无法让对应的container stop并deleted，而是要通过delete service and delete deployment两步才能彻底删除service。

```
root@iZ25cn4xxnvZ:~# kubectl delete svc my-nginx
service "my-nginx" deleted
root@iZ25cn4xxnvZ:~# kubectl get service my-nginx
Error from server: services "my-nginx" not found
//容器依然在运行
root@iZ25cn4xxnvZ:~# kubectl get deployment my-nginx
NAME DESIRED CURRENT UP-TO-DATE AVAILABLE AGE
my-nginx 2 2 2 2 20h
root@iZ25cn4xxnvZ:~# kubectl delete deployment my-nginx
deployment "my-nginx" deleted
再执行docker ps，看看对应docker container应该已经被删除。
```


重新创建暴露nodeport的my-nginx服务，我们先来创建一个新的service文件：

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


创建服务：

```
root@iZ25cn4xxnvZ:~/k8stest/demo# kubectl create -f ./my-nginx-svc.yaml
deployment "my-nginx" created
```


查看服务信息：

```
root@iZ25cn4xxnvZ:~/k8stest/demo# kubectl describe service my-nginx
Name: my-nginx
Namespace: default
Labels: run=my-nginx
Selector: run=my-nginx
Type: NodePort
IP: 192.168.3.179
Port: <unset> 80/TCP
NodePort: <unset> 30062/TCP
Endpoints: 172.16.57.3:80,172.16.99.2:80
Session Affinity: None
```


可以看到与上一次的service信息相比，这里多出一个属性:NodePort 30062/TCP，这个就是整个服务暴露到集群外面的端口。

接下来我们通过这两个node的公网地址访问一下这个暴露的nodeport，看看service中的两个ngnix container是否能收到request：

通过公网ip curl 30062端口:

```
curl -v x.x.x.x:30062
curl -v y.y.y.y:30062
```


同样，我们用docker logs -f来监控两个nginx container的日志输出，可以看到：

```
nginx1:
172.16.57.4 - - [17/Oct/2016:08:19:56 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
172.16.57.1 - - [17/Oct/2016:08:21:55 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.30.0" "-"
172.16.57.1 - - [17/Oct/2016:08:21:56 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.30.0" "-"
172.16.57.1 - - [17/Oct/2016:08:21:59 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.30.0" "-"
172.16.57.1 - - [17/Oct/2016:08:22:07 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.30.0" "-"
172.16.57.1 - - [17/Oct/2016:08:22:09 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.30.0" "-"
nginx2：
172.16.57.0 - - [17/Oct/2016:08:22:05 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.30.0" "-"
172.16.57.0 - - [17/Oct/2016:08:22:06 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.30.0" "-"
172.16.57.0 - - [17/Oct/2016:08:22:08 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.30.0" "-"
172.16.57.0 - - [17/Oct/2016:08:22:09 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.30.0" "-"
```


两个container轮询地收到外部转来的http request。

现在我们将my-nginx服务的scale由2缩减为1：

```
root@iZ25cn4xxnvZ:~# kubectl scale --replicas=1 deployment/my-nginx
deployment "my-nginx" scaled
```


再次测试nodeport机制：

```
curl -v x.x.x.x:30062
curl -v y.y.y.y:30062
```


scale后，只有master上的my-nginx存活。由于nodeport机制，没有my-nginx上的node收到请求后，将请求转给kube-proxy，通过内部clusterip机制，发给有my-nginx的container。

```
master上的nginx container：
172.16.99.1 - - [18/Oct/2016:00:55:04 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.30.0" "-"
172.16.57.0 - - [18/Oct/2016:00:55:10 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.30.0" "-"
```


nodeport机制测试ok。通过netstat我们可以看到30062端口是node上的kube-proxy监听的端口，因此即便该node上没有nginx服务container运行，kube-proxy也会转发request。

```
root@iZ25cn4xxnvZ:~# netstat -tnlp|grep 30062
tcp6 0 0 :::30062 :::* LISTEN 22076/kube-proxy
```


#### 六、尾声

到这里，k8s集群已经是可用的了。但要用好背后拥有15年容器经验沉淀的k8s，还有很长的路要走，比如安装Addon（DNS plugin等）、比如安装Dashboard等。这些在这里暂不提了，文章已经很长了。后续可能会有单独文章说明。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

写得很好，关于停止各个组件的服务。提供以下两种更简单的方案：1）不改动代码：sudo service etcd stop由于etcd负责分布式配置，所以只要停止etcd，其他kube服务也就停止了。2）改代码，一劳永逸：修改ubuntu/util.sh中的etcd/flanneled/kube-proxy/kubelet启动服务service etcd start -> service etcd restart其他的组件修改方式也一样。谢谢Tony的文章

谢谢的你的方案，受教了。

我按照你的这个教程配置了一下，在validate cluster的时候出错了。不知道你有没有遇到过，请教一下：master and minion node ip：9.91.9.130minion node: 9.91.9.127bash kube-up.sh后，有2个异常信息：1）etcd start/running, process 17065{“Network”:”172.16.0.0/16″, “Backend”: {“Type”: “vxlan”}}Connection to 9.91.9.130 closed.2）… calling validate-clusterThe connection to the server 9.91.9.130:8080 was refused – did you specify the right host or port?(kubectl failed, will retry 2 times)The connection to the server 9.91.9.130:8080 was refused – did you specify the right host or port?(kubectl failed, will retry 1 times)The connection to the server 9.91.9.130:8080 was refused – did you specify the right host or port?(‘kubectl get nodes’ failed, giving up)

第一个问题没遇到过。第二个问题遇到过，当时的原因是因为config-default.sh中的proxy_setting设置的问题导致kube-up.sh无法连接到master node上的apiserver。后来在proxy_setting中增加了no_proxy的设置后，问题就解决了。不知道我们遇到的问题是否是一个问题。

第二个问题我解决了，不过我不知no_proxy的问题，而是config-default.sh中用到了DefaultStorageClass，我的apiserver log中说这是一个unknown admission plugin，把它注释掉就可以了。第一个问题我现在还没有解决，不过集群可以启动了。跑你的mg-nginx的yaml，结果node不能运行，一直处于ImagePullBackOff或者ContainerCreated状态。

ImagePullBackOff这个错误是不是因为image pull错误啊，确认image是可以pull下了，或先手动pull image后再尝试创建pod。ContainerCreated状态，没遇到过，但这个状态下，如果用docker ps -a能看到启动失败的container，可以试试docker logs 看看这个container的输出日志。再兼顾一下k8s daemon的各种日志，综合分析吧。

1.4的安装教程来一发吧

kubernetes 1.4以后版本在ubuntu 16.04上可以直接apt-get install，应该方便多了。另外集群也开始使用kubeadm进行管理。官方文档http://kubernetes.io/docs/getting-started-guides/kubeadm/ 的描述已经较为清晰。等有时间，有环境，肯定是要升级到1.4或以后版本的。到时候会写一篇k8s 1.4 install “填坑”教程的^_^

不错，最近也在学习，不过没用kube提供的脚本，手动一步一步来的，用脚本应该可以方便不少。这里测试 clusterIP 其实可以不用创建 一个 client 的 deploy, 直接到任意一台 node 机，运行 curl clusterIP:port 就可以了访问到服务 ( k8s v1.4)。

楼主是否在阿里云上试过 calico 我用k81.4 使用calico作为pod 网络，容器间网络死活不通。

没有试过。一直再用Flannel网络，目前Flannel没啥问题。

有个问题一直没明白，有十几年容器经验的google，在docker没有出来的时候他们的容器是怎么做的？

你看过docker原理的介绍就知道了.docker实际上是基于内核namespace和cgroup技术的基础,做了应用层的封装.namespace技术很早就出现了,最早的好象是mount ns,是在内核2.4的时候就有了,cgroup忘记是2.4还是2.6. linux内核2.4实在2000年左右的上古时期发布的.上古时期还有solaries的zone. 这些概念老早就提出来. 有段时期ubuntu和redhat分别在应用层整了两个管理库,一个叫LXC,一个叫libcontaner