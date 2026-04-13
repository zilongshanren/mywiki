---
title: Kubernetes集群的安全配置
url: https://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster/
published: '2016-11-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes集群的安全配置

使用kubernetes/cluster/kube-up.sh脚本在装有[Ubuntu](http://tonybai.com/tag/ubuntu)操作系统的bare metal上[搭建的Kubernetes集群](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)并不安全，甚至可以说是“完全不设防的”，这是因为Kubernetes集群的核心组件：[kube-apiserver](http://kubernetes.io/docs/admin/kube-apiserver/)启用了insecure-port。insecure-port背后的api server默认完全信任访问该端口的流量，内部无任何安全机制。并且监听insecure-port的api server bind的insecure-address为0.0.0.0。也就是说任何内外部请求，都可以通过insecure-port端口任意操作Kubernetes集群。我们的平台虽小，但“裸奔”的k8s集群也并不是我们想看到的，适当的安全配置是需要的。

在本文中，我将和大家一起学习一下Kubernetes提供的安全机制，并通过安全配置调整，实现K8s集群的“有限”安全。

#### 一、集群现状

我们先来“回顾”一下集群现状，为后续配置调整提供一个可回溯和可比对的“基线”。

##### 1、Nodes

集群基本信息：

```
# kubectl cluster-info
Kubernetes master is running at http://10.47.136.60:8080
KubeDNS is running at http://10.47.136.60:8080/api/v1/proxy/namespaces/kube-system/services/kube-dns
To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```


当前集群逻辑上由一个master node和两个worker nodes组成：

```
单master： 10.47.136.60
worker nodes： 10.47.136.60和10.46.181.146
# kubectl get node --show-labels=true
NAME STATUS AGE LABELS
10.46.181.146 Ready 41d beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=10.46.181.146
10.47.136.60 Ready 41d beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=10.47.136.60
```


##### 2、kubernetes核心组件的启动参数

我们再来明确一下当前集群中各k8s核心组件的启动参数，这些参数决定着组件背后的行为：

master node & worker node1 – 10.47.136.60上：

```
root 22000 1 0 Oct17 ? 03:52:55 /opt/bin/kube-controller-manager --master=127.0.0.1:8080 --root-ca-file=/srv/kubernetes/ca.crt --service-account-private-key-file=/srv/kubernetes/server.key --logtostderr=true
root 22021 1 1 Oct17 ? 17:11:15 /opt/bin/kube-apiserver --insecure-bind-address=0.0.0.0 --insecure-port=8080 --etcd-servers=http://127.0.0.1:4001 --logtostderr=true --service-cluster-ip-range=192.168.3.0/24 --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,SecurityContextDeny,ResourceQuota --service-node-port-range=30000-32767 --advertise-address=10.47.136.60 --client-ca-file=/srv/kubernetes/ca.crt --tls-cert-file=/srv/kubernetes/server.cert --tls-private-key-file=/srv/kubernetes/server.key
root 22121 1 0 Oct17 ? 00:22:30 /opt/bin/kube-scheduler --logtostderr=true --master=127.0.0.1:8080
root 2140405 1 0 Nov15 ? 00:05:26 /opt/bin/kube-proxy --hostname-override=10.47.136.60 --master=http://10.47.136.60:8080 --logtostderr=true
root 1912455 1 1 Nov15 ? 03:43:09 /opt/bin/kubelet --hostname-override=10.47.136.60 --api-servers=http://10.47.136.60:8080 --logtostderr=true --cluster-dns=192.168.3.10 --cluster-domain=cluster.local --config=
```


worker node2 – 10.46.181.146上:

```
root 7934 1 1 Nov15 ? 03:06:00 /opt/bin/kubelet --hostname-override=10.46.181.146 --api-servers=http://10.47.136.60:8080 --logtostderr=true --cluster-dns=192.168.3.10 --cluster-domain=cluster.local --config=
root 23026 1 0 Nov15 ? 00:04:49 /opt/bin/kube-proxy --hostname-override=10.46.181.146 --master=http://10.47.136.60:8080 --logtostderr=true
```


从master node的核心组件kube-apiserver 的启动命令行参数也可以看出我们在开篇处所提到的那样：apiserver insecure-port开启，且bind 0.0.0.0:8080，可以任意访问，连basic_auth都没有。当然api server不只是监听这一个端口，在[api server源码](http://kubernetes.io/docs/admin/accessing-the-api/)中，我们可以看到默认情况下，apiserver还监听了另外一个secure port，该端口的默认值是6443，通过lsof命令查看6443端口的监听进程也可以印证这一点：

```
//master node上
# lsof -i tcp:6443
COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
kube-apis 22021 root 46u IPv6 921529 0t0 TCP *:6443 (LISTEN)
```


##### 3、私钥文件和公钥证书

通过[安装脚本在bare-metal上安装的k8s集群](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)，在master node上你会发现如下文件：

```
root@node1:/srv/kubernetes# ls
ca.crt kubecfg.crt kubecfg.key server.cert server.key
```


这些私钥文件和公钥证书是在k8s(1.3.7)集群安装过程由安装脚本创建的，在kubernetes/cluster/common.sh中你可以发现function create-certs这样一个函数，这些文件就是它创建的。

```
# Create certificate pairs for the cluster.
# $1: The public IP for the master.
#
# These are used for static cert distribution (e.g. static clustering) at
# cluster creation time. This will be obsoleted once we implement dynamic
# clustering.
#
# The following certificate pairs are created:
#
# - ca (the cluster's certificate authority)
# - server
# - kubelet
# - kubecfg (for kubectl)
#
# TODO(roberthbailey): Replace easyrsa with a simple Go program to generate
# the certs that we need.
#
# Assumed vars
# KUBE_TEMP
#
# Vars set:
# CERT_DIR
# CA_CERT_BASE64
# MASTER_CERT_BASE64
# MASTER_KEY_BASE64
# KUBELET_CERT_BASE64
# KUBELET_KEY_BASE64
# KUBECFG_CERT_BASE64
# KUBECFG_KEY_BASE64
function create-certs {
local -r primary_cn="${1}"
... ...
}
```


简单描述一下这些文件的用途：

```
- ca.crt：the cluster's certificate authority，CA证书，即根证书，内置CA公钥，用于验证某.crt文件，是否是CA签发的证书；
- server.cert：kube-apiserver服务端公钥数字证书；
- server.key：kube-apiserver服务端私钥文件；
- kubecfg.crt 和kubecfg.key：按照 create-certs函数注释中的说法：这两个文件是为kubectl访问apiserver[双向证书验证](http://tonybai.com/2015/04/30/go-and-https/)时使用的。
```


不过，这里我们没有CA的key，无法签发新证书，如果要用这几个文件，那么就仅能限于这几个文件。我们可以利用kubecfg.crt 和kubecfg.key 作为访问api server的client端的key和crt使用。我们来查看一下这几个文件：

查看ca.crt：

```
#openssl x509 -noout -text -in ca.crt
... ...
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 16946557986148168970 (0xeb2e44b3a1ebb50a)
Signature Algorithm: sha256WithRSAEncryption
Issuer: CN=10.47.136.60@1476362758
Validity
Not Before: Oct 13 12:45:58 2016 GMT
Not After : Oct 11 12:45:58 2026 GMT
Subject: CN=10.47.136.60@1476362758
... ..
```


查看server.cert：

```
...
Data:
Version: 3 (0x2)
Serial Number: 1 (0x1)
Signature Algorithm: sha256WithRSAEncryption
Issuer: CN=10.47.136.60@1476362758
Validity
Not Before: Oct 13 12:45:59 2016 GMT
Not After : Oct 11 12:45:59 2026 GMT
Subject: CN=kubernetes-master
...
```


查看kubecfg.crt：

```
...
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 2 (0x2)
Signature Algorithm: sha256WithRSAEncryption
Issuer: CN=10.47.136.60@1476362758
Validity
Not Before: Oct 13 12:45:59 2016 GMT
Not After : Oct 11 12:45:59 2026 GMT
Subject: CN=kubecfg
...
```


再来验证一下server.cert和kubecfg.crt是否是ca.crt签发的：

```
# openssl verify -CAfile ca.crt kubecfg.crt
kubecfg.crt: OK
# openssl verify -CAfile ca.crt server.cert
server.cert: OK
```


在前面的apiserver的启动参数展示中，我们已经看到kube-apiserver使用了ca.crt, server.cert和server.key：

```
/opt/bin/kube-apiserver --insecure-bind-address=0.0.0.0 --insecure-port=8080 --etcd-servers=http://127.0.0.1:4001 --logtostderr=true --service-cluster-ip-range=192.168.3.0/24 --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,SecurityContextDeny,ResourceQuota --service-node-port-range=30000-32767 --advertise-address=10.47.136.60 --client-ca-file=/srv/kubernetes/ca.crt --tls-cert-file=/srv/kubernetes/server.cert --tls-private-key-file=/srv/kubernetes/server.key
```


在后续章节中，我们还会详细说明这些密钥和公钥证书在K8s集群安全中所起到的作用。

#### 二、集群环境

还是那句话，Kubernetes在active development中，老版本和新版本的安全机制可能有较大变动，本篇中的配置方案和步骤都是针对一定环境有效的，我们的环境如下：

```
OS：
Ubuntu 14.04.4 LTS Kernel：3.19.0-70-generic #78~14.04.1-Ubuntu SMP Fri Sep 23 17:39:18 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
Docker：
# docker version
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
Kubernetes集群：1.3.7
私有镜像仓库：阿里云镜像仓库
```


#### 三、目标

目前，我们尚不具备一步迈向“绝对安全”的能力，在目标设定时，我们的一致想法是在当前阶段“有限安全”的K8s集群更适合我们。在这一原则下，我们针对不同情况提出不同的目标设定。

前面说过，k8s针对insecure port(–insecure-bind-address=0.0.0.0 –insecure-port=8080)的流量没有任何安全机制限制，相当于k8s“裸奔”。但是走k8s apiserver secure port(–bind-address=0.0.0.0 –secure-port=6443)的流量，将会遇到[验证、授权等安全机制](http://kubernetes.io/docs/admin/accessing-the-api/)的限制。具体使用哪个端口与API server的交互方式，要视情况而定。

在分情况说明之前，将api server的insecure port的bind address由0.0.0.0改为local address是必须要做的。

##### 1、Cluster -> Master(apiserver)

从集群到Apiserver的流量也可以细分为几种情况：

###### a) kubernetes component on master node -> apiserver

由于master node上的components与apiserver运行在一台机器上，因此可以通过local address的insecure-port访问apiserver，无需走insecure port。从现状中当前master上的component组件的启动参数来看，目前已经符合要求，于是针对这些components，我们无需再做配置上的调整。

###### b) kubernetes component on worker node -> apiserver

目标是实现kubernetes components on worker node和运行于master上的apiserver之间的基于https的双向认证。kubernetes的各个组件均支持在命令行参数中传入tls相关参数，比如ca文件路径，比如client端的cert文件和key等。

###### c) componet in pod for kubernetes -> apiserver

像kube dns和kube dashboard这些运行于pod中的k8s 组件也是在k8s cluster范围内调度的，它们可能运行在任何一个worker node上。理想情况下，它们与master上api server的通信也应该是基于一定安全机制的。不过在本篇中，我们暂时不动它们的设置，以免对其他目标的实现造成一定障碍和更多的工作量，在后续文章中，可能会专门将dns和dashboard拿出来做安全加固说明。因此，dns和dashboard在这里仍然使用的是insecure-port：

```
root 10531 10515 0 Nov15 ? 00:03:02 /dashboard --port=9090 --apiserver-host=http://10.47.136.60:8080
root 2018255 2018240 0 Nov15 ? 00:03:50 /kube-dns --domain=cluster.local. --dns-port=10053 --kube-master-url=http://10.47.136.60:8080
```


###### d) user service in pod -> apiserver

我们的集群管理程序也是以service的形式运行在k8s cluster中的，这些程序如何访问apiserver才是我们关心的重点，我们希望管理程序通过secure-port，在一定的安全机制下与apiserver交互。

##### 2、Master(apiserver) -> Cluster

apiserver作为client端访问Cluster，在k8s文档中，这个访问路径主要包含两种情况：

a) apiserver与各个node上kubelet交互，采集Pod的log；

b) apiserver通过自身的proxy功能访问node、pod以及集群中的各种service。

在“有限安全”的原则下，我们暂不考虑这种情况下的安全机制。

#### 四、Kubernetes的安全机制

kube-apiserver是整个kubernetes集群的核心，无论是kubectl还是通过api管理集群，最终都会落到与kube-apiserver的交互，apiserver是集群管理命令的入口。kube-apiserver同时监听两个端口：insecure-port和secure-port。之前提到过：通过insecure-port进入apiserver的流量可以有控制整个集群的全部权限；而通过secure-port的流量将经过k8s的安全机制的重重考验，这也是这一节我们重要要说明的。insecure-port的存在一般是为了集群bootstrap或集群开发调试使用的。官方文档建议：集群外部流量都应该走secure port。insecure-port可通过firewall rule使外部流量unreachable。

下面这幅官方图示准确解释了通过secure port的流量将要通过的“安全关卡”：

我们可以看到外界到APIServer的请求先后经过了：

```
安全通道(tls) -> Authentication(身份验证) -> Authorization（授权）-> Admission Control(入口条件控制)
```


-
安全通道：即基于tls的https的安全通道建立，对流量进行加密，防止嗅探、身份冒充和篡改；

-
Authentication：即身份验证，这个环节它面对的输入是整个http request。它负责对来自client的请求进行身份校验，支持的方法包括：client证书验证（https双向验证）、basic auth、普通token以及jwt token(用于serviceaccount)。APIServer启动时，可以指定一种Authentication方法，也可以指定多种方法。如果指定了多种方法，那么APIServer将会逐个使用这些方法对客户端请求进行验证，只要请求数据通过其中一种方法的验证，APIServer就会认为Authentication成功；

-
Authorization：授权。这个阶段面对的输入是http request context中的各种属性，包括：user、group、request path（比如：/api/v1、/healthz、/version等）、request verb(比如：get、list、create等)。APIServer会将这些属性值与事先配置好的访问策略(access policy）相比较。APIServer支持多种authorization mode，包括AlwaysAllow、AlwaysDeny、ABAC、RBAC和Webhook。APIServer启动时，可以指定一种authorization mode，也可以指定多种authorization mode，如果是后者，只要Request通过了其中一种mode的授权，那么该环节的最终结果就是授权成功。

-
Admission Control：从技术的角度看，Admission control就像a chain of interceptors（拦截器链模式），它拦截那些已经顺利通过authentication和authorization的http请求。http请求沿着APIServer启动时配置的admission control chain顺序逐一被拦截和处理，如果某个interceptor拒绝了该http请求，那么request将会被直接reject掉，而不是像authentication或authorization那样有继续尝试其他interceptor的机会。


#### 五、实现安全传输通道（https)与身份校验(authentication)

在建立安全传输通道、身份校验环节，我们根据”目标“设定一节中的分类，也分为三种情况：

a) 运行于master上的核心k8s components走insecure port，这个暂不用修改配置；

b) worker node上的k8s组件配置通过insecure-port访问，并采用https双向认证的身份验证机制；

c) pod in k8s访问apiserver，通过https+ basic auth的方式进行身份验证。

APIServer直接使用了集群创建时创建的ca.crt、server.cert和server.key，由于没有ca.key，所以我们只能直接利用其它两个文件: kubecfg.key和kubecfg.crt作为客户端的私钥文件和公钥证书。当然你也可以[手动重新创建ca](http://tonybai.com/2015/04/30/go-and-https/)，并将apiserver使用的.key、.crt以及各个components的client.key和client.crt都生成一份，并用你生成的Ca签发。这里我们就偷个懒儿了。

在开始之前，我们再来看看apiserver的启动参数：

```
root 22021 1 1 Oct17 ? 17:11:15 /opt/bin/kube-apiserver --insecure-bind-address=0.0.0.0 --insecure-port=8080 --etcd-servers=http://127.0.0.1:4001 --logtostderr=true --service-cluster-ip-range=192.168.3.0/24 --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,SecurityContextDeny,ResourceQuota --service-node-port-range=30000-32767 --advertise-address=10.47.136.60 --client-ca-file=/srv/kubernetes/ca.crt --tls-cert-file=/srv/kubernetes/server.cert --tls-private-key-file=/srv/kubernetes/server.key
```


由于之前简述了Kubernetes的安全机制，于是我们对这些参数又有了进一步认识

```
https安全通道建立阶段：端口6443(通过 /opt/bin/kube-apiserver --help查看options说明可以得到)，公钥证书server.cert ，私钥文件：server.key。
Authentication阶段：从当前启动参数中，我们仅能看到一种机制：--client-ca-file=/srv/kubernetes/ca.crt，也就是client证书校验机制。apiserver会用/srv/kubernetes/ca.crt对client端发过来的client.crt进行验证。
Authorization阶段：通过 /opt/bin/kube-apiserver --help查看options说明可以得到：--authorization-mode="AlwaysAllow"，也就是说在这一环节，所有Request都可以顺利通过。
Admission Control阶段：apiserver指定了“NamespaceLifecycle,LimitRanger,ServiceAccount,SecurityContextDeny,ResourceQuota”这样一个interceptor链。
```


我们首先来测试一下通过kubecfg.key和kubecfg.crt访问APIServer的insecure-port，验证一下kubecfg.key和kubecfg.crt作为client端私钥文件和公钥证书的可行性：

```
# curl https://10.47.136.60:6443/version --cert /srv/kubernetes/kubecfg.crt --key /srv/kubernetes/kubecfg.key --cacert /srv/kubernetes/ca.crt
{
"major": "1",
"minor": "3",
"gitVersion": "v1.3.7",
"gitCommit": "a2cba278cba1f6881bb0a7704d9cac6fca6ed435",
"gitTreeState": "clean",
"buildDate": "2016-09-12T23:08:43Z",
"goVersion": "go1.6.2",
"compiler": "gc",
"platform": "linux/amd64"
}
```


接下来，我们就来开始调整k8s配置。

##### 第一个场景：components on worker node -> master

worker node上有两个k8s components：kubelet和kube-proxy，当前它们的启动参数为：

```
root 7934 1 1 Nov15 ? 03:33:35 /opt/bin/kubelet --hostname-override=10.46.181.146 --api-servers=http://10.47.136.60:8080 --logtostderr=true --cluster-dns=192.168.3.10 --cluster-domain=cluster.local --config=
root 8140 1 0 14:59 ? 00:00:00 /opt/bin/kube-proxy --hostname-override=10.46.181.146 --master=http://10.47.136.60:8080 --logtostderr=true
```


我们将ca.crt、kubecfg.key和kubecfg.crt scp到其他各个Worker node的/srv/kubernetes目录下：

```
root@node1:/srv/kubernetes# scp ca.crt root@10.46.181.146:/srv/kubernetes
ca.crt 100% 1220 1.2KB/s 00:00
root@node1:/srv/kubernetes# scp kubecfg.crt root@10.46.181.146:/srv/kubernetes
kubecfg.crt 100% 4417 4.3KB/s 00:00
root@node1:/srv/kubernetes# scp kubecfg.key root@10.46.181.146:/srv/kubernetes
kubecfg.key
在worker node: 10.46.181.146上：
# ls -l
total 16
-rw-r----- 1 root root 1220 Nov 25 15:51 ca.crt
-rw------- 1 root root 4417 Nov 25 15:51 kubecfg.crt
-rw------- 1 root root 1708 Nov 25 15:51 kubecfg.key
```


创建worker node上kubelet和kube-proxy所要使用的[config文件](http://kubernetes.io/docs/user-guide/kubeconfig-file/)：/root/.kube/config

```
/root/.kube/config
apiVersion: v1
kind: Config
preferences: {}
users:
- name: kubecfg
user:
client-certificate: /srv/kubernetes/kubecfg.crt
client-key: /srv/kubernetes/kubecfg.key
clusters:
- cluster:
certificate-authority: /srv/kubernetes/ca.crt
name: ubuntu
contexts:
- context:
cluster: ubuntu
user: kubecfg
name: ubuntu
current-context: ubuntu
```


这个文件参考了master node上的/root/.kube/config文件的格式，你也可以在master node上使用kubectl config view查看config文件内容：

```
# kubectl config view
apiVersion: v1
clusters:
- cluster:
insecure-skip-tls-verify: true
server: http://10.47.136.60:8080
name: ubuntu
contexts:
- context:
cluster: ubuntu
user: ubuntu
name: ubuntu
current-context: ubuntu
kind: Config
preferences: {}
users:
- name: ubuntu
user:
password: xxxxxA
username: admin
```


Worker node上/root/.kube/config中的user.name使用的是kubecfg，这也是在前面查看kubecfg.crt时，kubecfg.crt在/CN域中使用的值。

接下来我们来修改worker node上的/etc/default/kubelet文件：

```
KUBELET_OPTS=" --hostname-override=10.46.181.146 --api-servers=https://10.47.136.60:6443 --logtostderr=true --cluster-dns=192.168.3.10 --cluster-domain=cluster.local --kubeconfig=/root/.kube/config"
#KUBELET_OPTS=" --hostname-override=10.46.181.146 --api-servers=http://10.47.136.60:8080 --logtostderr=true --cluster-dns=192.168.3.10 --cluster-domain=cluster.local --config= "
```


在worker node上重启kubelet并查看/var/log/upstart/kubelet.log：

```
# service kubelet restart
kubelet stop/waiting
kubelet start/running, process 9716
///var/log/upstart/kubelet.log
... ...
I1125 16:12:26.332652 9716 server.go:784] Watching apiserver
W1125 16:12:26.338581 9716 kubelet.go:572] Hairpin mode set to "promiscuous-bridge" but configureCBR0 is false, falling back to "hairpin-veth"
I1125 16:12:26.338641 9716 kubelet.go:393] Hairpin mode set to "hairpin-veth"
I1125 16:12:26.366600 9716 docker_manager.go:235] Setting dockerRoot to /var/lib/docker
I1125 16:12:26.367067 9716 server.go:746] Started kubelet v1.3.7
E1125 16:12:26.369508 9716 kubelet.go:954] Image garbage collection failed: unable to find data for container /
I1125 16:12:26.370534 9716 fs_resource_analyzer.go:66] Starting FS ResourceAnalyzer
I1125 16:12:26.370567 9716 status_manager.go:123] Starting to sync pod status with apiserver
I1125 16:12:26.370601 9716 kubelet.go:2501] Starting kubelet main sync loop.
I1125 16:12:26.370632 9716 kubelet.go:2510] skipping pod synchronization - [network state unknown container runtime is down]
I1125 16:12:26.370981 9716 server.go:117] Starting to listen on 0.0.0.0:10250
I1125 16:12:26.384336 9716 volume_manager.go:227] Starting Kubelet Volume Manager
I1125 16:12:26.480387 9716 factory.go:295] Registering Docker factory
I1125 16:12:26.480483 9716 factory.go:54] Registering systemd factory
I1125 16:12:26.481446 9716 factory.go:86] Registering Raw factory
I1125 16:12:26.482888 9716 manager.go:1072] Started watching for new ooms in manager
I1125 16:12:26.484242 9716 oomparser.go:200] OOM parser using kernel log file: "/var/log/kern.log"
I1125 16:12:26.485330 9716 manager.go:281] Starting recovery of all containers
I1125 16:12:26.562959 9716 kubelet.go:1213] Node 10.46.181.146 was previously registered
I1125 16:12:26.712150 9716 manager.go:286] Recovery completed
```


一次点亮！

再来修改worker node上kube-proxy的配置：/etc/default/kube-proxy:

```
// /etc/default/kube-proxy
KUBE_PROXY_OPTS=" --hostname-override=10.46.181.146 --master=https://10.47.136.60:6443 --logtostderr=true --kubeconfig=/root/.kube/config"
#KUBE_PROXY_OPTS=" --hostname-override=10.46.181.146 --master=http://10.47.136.60:8080 --logtostderr=true "
```


在worker node上重启kube-proxy并查看/var/log/upstart/kube-proxy.log：

```
# service kube-proxy restart
kube-proxy stop/waiting
kube-proxy start/running, process 26185
// /var/log/upstart/kube-proxy.log
I1125 16:30:28.224491 26185 server.go:202] Using iptables Proxier.
I1125 16:30:28.228067 26185 server.go:214] Tearing down userspace rules.
I1125 16:30:28.245634 26185 conntrack.go:40] Setting nf_conntrack_max to 65536
I1125 16:30:28.247422 26185 conntrack.go:57] Setting conntrack hashsize to 16384
I1125 16:30:28.249456 26185 conntrack.go:62] Setting nf_conntrack_tcp_timeout_established to 86400
```


从日志上看不出有啥异常，算是成功！:)

##### 第二个场景：pod in cluster -> master

通过阅读K8s的官方文档“[Accessing the api from a pod](http://kubernetes.io/docs/user-guide/accessing-the-cluster/#accessing-the-api-from-a-pod)”，我们知道K8s cluster为Pod访问API Server做了很多“预备”工作，最重要的一点就是在Pod被创建的时候，一个[serviceaccount](https://github.com/kubernetes/kubernetes/blob/master/docs/design/service_accounts.md) 被自动mount到/var/run/secrets/kubernetes.io/serviceaccount路径下：

```
#kubectl describe pod/my-golang-1147314274-0qms5
Name: my-golang-1147314274-0qms5
Namespace: default
Node: 10.47.136.60/10.47.136.60
Start Time: Thu, 24 Nov 2016 14:59:52 +0800
Labels: pod-template-hash=1147314274
run=my-golang
Status: Running
IP: 172.16.99.9
... ...
Containers:
my-golang:
... ...
Volume Mounts:
/var/run/secrets/kubernetes.io/serviceaccount from default-token-40z0x (ro)
Environment Variables: <none>
... ...
Volumes:
default-token-40z0x:
Type: Secret (a volume populated by a Secret)
SecretName: default-token-40z0x
QoS Class: BestEffort
Tolerations: <none>
```


serviceaccount顾名思义，是Pod中程序访问APIServer所要使用的账户信息，我们来看看都有啥：

```
# kubectl get serviceaccount
NAME SECRETS AGE
default 1 43d
# kubectl describe serviceaccount/default
Name: default
Namespace: default
Labels: <none>
Image pull secrets: <none>
Mountable secrets: default-token-40z0x
Tokens: default-token-40z0x
# kubectl describe secret/default-token-40z0x
Name: default-token-40z0x
Namespace: default
Labels: <none>
Annotations: kubernetes.io/service-account.name=default
kubernetes.io/service-account.uid=90de59ad-9120-11e6-a0a6-00163e1625a9
Type: kubernetes.io/service-account-token
Data
====
ca.crt: 1220 bytes
namespace: 7 bytes
token: {Token data}
```


mount到Pod中/var/run/secrets/kubernetes.io/serviceaccount路径下的default-token-40z0x volume包含三个文件：

- ca.crt：CA的公钥证书
- namspace文件：里面的内容为：”default”
- token：用在Pod访问APIServer时候的身份验证。

理论上，使用这些信息Pod可以成功访问APIServer，我们来测试一下。注意在Pod的世界中，APIServer也是一个Service，通过kubectl get service可以看到：

```
# kubectl get services
NAME CLUSTER-IP EXTERNAL-IP PORT(S) AGE
kubernetes 192.168.3.1 <none> 443/TCP 43d
```


kubernetes这个Service监听的端口是443，也就是说在Pod的视角中，APIServer暴露的仅仅是insecure-port。并且使用”kubernetes”这个名字，我们可以通过[kube-dns](http://tonybai.com/2016/10/23/install-dns-addon-for-k8s/)获得APIServer的ClusterIP。

启动一个基于golang:latest的pod，pod.yaml如下：

```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: my-golang
spec:
replicas: 1
template:
metadata:
labels:
run: my-golang
spec:
containers:
- name: my-golang
image: golang:latest
command: ["tail", "-f", "/var/log/bootstrap.log"]
```


Pod启动后，docker exec -it container-id /bin/bash切入container，并执行如下命令：

```
# TOKEN="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
# curl --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt https://kubernetes:443/version -H "Authorization: Bearer $TOKEN"
Unauthorized
```


查看API Server的log：

```
E1125 17:30:22.504059 2743425 handlers.go:54] Unable to authenticate the request due to an error: crypto/rsa: verification error
```


似乎是验证token失败。这个问题在kubernetes的[github issue中也有被提及](https://github.com/kubernetes/kubernetes/issues/22351)，目前尚未解决。

不过仔细想了想，如果每个Pod都默认可以访问APIServer，显然也是不安全的，虽然我们可以通过authority和admission control对默认的token访问做出限制，但总感觉不那么“安全”。

我们来试试basic auth方式（这种方式的弊端是API Server运行中，无法在运行时动态更新auth文件，对于auth文件的修改，必须重启APIServer后生效）。

我们首先在APIServer侧为APIServer创建一个basic auth file：

```
// /srv/kubernetes/basic_auth_file
admin123,admin,admin
```


basic_auth_file中每一行的格式：password,username,useruid

修改APIServer的启动参数，将basic_auth_file传入并重启apiserver：

```
KUBE_APISERVER_OPTS=" --insecure-bind-address=10.47.136.60 --insecure-port=8080 --etcd-servers=http://127.0.0.1:4001 --logtostderr=true --service-cluster-ip-range=192.168.3.0/24 --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,SecurityContextDeny,ResourceQuota --service-node-port-range=30000-32767 --advertise-address=10.47.136.60 --basic-auth-file=/srv/kubernetes/basic_auth_file --client-ca-file=/srv/kubernetes/ca.crt --tls-cert-file=/srv/kubernetes/server.cert --tls-private-key-file=/srv/kubernetes/server.key"
```


我们在Pod中使用basic auth访问API Server：

```
# curl --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt https://kubernetes:443/version -basic -u admin:admin123
{
"major": "1",
"minor": "3",
"gitVersion": "v1.3.7",
"gitCommit": "a2cba278cba1f6881bb0a7704d9cac6fca6ed435",
"gitTreeState": "clean",
"buildDate": "2016-09-12T23:08:43Z",
"goVersion": "go1.6.2",
"compiler": "gc",
"platform": "linux/amd64"
}
```


Pod to APIServer authentication成功了。

#### 六、小结

再重申一次：上述配置不是绝对安全的理想配置方案，只是阶段性满足我目前项目需求的一个“有限安全”方案，大家谨慎参考。

到目前为止，我们的“有限安全”也仅仅做到Authentication这一步，至于Authority和Admission Control，目前尚未有相关实践，可能会在后续的文章中做单独说明。

#### 七、参考资料

- Master <-> Node Communication – http://kubernetes.io/docs/admin/master-node-communication/
- Authentication – http://kubernetes.io/docs/admin/authentication/
- Using Authorization Plugins – http://kubernetes.io/docs/admin/authorization/
- Accessing the API – http://kubernetes.io/docs/admin/accessing-the-api/
- Managing Service Accounts – http://kubernetes.io/docs/admin/service-accounts-admin/
- Authenticating Across Clusters with kubeconfig — http://kubernetes.io/docs/user-guide/kubeconfig-file/
- Service Accounts — https://docs.openshift.com/enterprise/3.1/dev_guide/service_accounts.html
- 4S: SERVICES ACCOUNT, SECRET, SECURITY CONTEXT AND SECURITY IN KUBERNETES — http://www.sel.zju.edu.cn/?p=588
- KUBERNETES APISERVER源码分析——API请求的认证过程 – http://www.sel.zju.edu.cn/?p=609
- Kubernetes安全配置案例 – http://www.cnblogs.com/breg/p/5923604.html

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

好文！

另外

“kubernetes这个Service监听的端口是443，也就是说在Pod的视角中，APIServer暴露的仅仅是insecure-port”

这里是否有个 typo ? insecure-port ==> secure-port

应该是一个typo，3ks