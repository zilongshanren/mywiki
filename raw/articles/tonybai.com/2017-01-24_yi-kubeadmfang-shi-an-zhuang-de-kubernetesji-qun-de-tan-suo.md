---
title: 以Kubeadm方式安装的Kubernetes集群的探索
url: https://tonybai.com/2017/01/24/explore-kubernetes-cluster-installed-by-kubeadm/
published: '2017-01-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 以Kubeadm方式安装的Kubernetes集群的探索

当前手上有两个[Kubernetes](http://tonybai.com/tag/kubernetes) cluster，一个是[采用kube-up.sh安装的k8s 1.3.7版本](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)，另外一个则是[采用kubeadm安装的k8s 1.5.1版本](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)。由于1.3.7版本安装在前，并且目前它也是承载了我们[PaaS平台](http://tonybai.com/2017/01/03/2016-summary/)的环境，因此对于这个版本的Kubernetes安装环境、配置操作、日志查看、集群操作等相对较为熟悉。而Kubeadm安装的1.5.1版本K8s集群在组件部署、配置、日志等诸多方面与1.3.7版本有了较大差异。刚上手的时候，你会发现你原来所熟知的1.3.7的东西都不在原先的位置上了。估计很多和我一样，采用[kubeadm](https://github.com/kubernetes/kubeadm)将集群升级到1.5.1版本的朋友们都会遇到这类问题，于是这里打算对[Kubeadm方式](https://kubernetes.io/docs/getting-started-guides/kubeadm/)安装的Kubernetes集群进行一些小小的探索，把一些变动较大的点列出来，供大家参考。

### 一、环境

这里使用的依然是文章《[使用Kubeadm安装Kubernetes](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)》中安装完毕的Kubernetes 1.5.1集群环境，底层是阿里云ECS，操作系统是[Ubuntu](http://tonybai.com/tag/ubuntu) 16.04.1。网络用的是[weave network](https://www.weave.works/)。

试验集群只有两个Node：一个master node和一个minion node。但[Master node由于被taint](https://kubernetes.io/docs/getting-started-guides/kubeadm/)了，因此它与minion node一样参与集群调度和承担负载。

### 二、核心组件的Pod化

Kubeadm安装的k8s集群与kube-up.sh安装集群相比，最大的不同应该算是kubernetes核心组件的Pod化，即：kube-apiserver、kube-controller-manager、kube-scheduler、kube-proxy、kube-discovery以及[etcd](https://github.com/coreos/etcd/)等核心组件都运行在集群中的Pod里的，这颇有些[CoreOS](https://github.com/coreos/)的风格。只有一个组件是例外的，那就是负责在node上与本地容器引擎交互的Kubelet。

K8s的核心组件Pod均放在kube-system namespace中，通过kubectl(on master node)可以查看到：

```
# kubectl get pods -n kube-system
NAME READY STATUS RESTARTS AGE
etcd-iz25beglnhtz 1/1 Running 2 26d
kube-apiserver-iz25beglnhtz 1/1 Running 3 26d
kube-controller-manager-iz25beglnhtz 1/1 Running 2 26d
kube-scheduler-iz25beglnhtz 1/1 Running 4 26d
... ...
```


另外细心的朋友可能会发现，这些核心组建的Pod名字均以所在Node的主机名为结尾，比如：kube-apiserver-iz25beglnhtz中的”iz25beglnhtz”就是其所在Node的主机名。

不过，即便这些核心组件是一个容器的形式运行在集群中，组件所使用网络依然是所在Node的主机网络，而不是[Pod Network](http://tonybai.com/2017/01/17/understanding-flannel-network-for-kubernetes/)：

```
# docker ps|grep apiserver
98ea64bbf6c8 gcr.io/google_containers/kube-apiserver-amd64:v1.5.1 "kube-apiserver --ins" 10 days ago Up 10 days k8s_kube-apiserver.6c2e367b_kube-apiserver-iz25beglnhtz_kube-system_033de1afc0844729cff5e100eb700a81_557d1fb2
4f87d22b8334 gcr.io/google_containers/pause-amd64:3.0 "/pause" 10 days ago Up 10 days k8s_POD.d8dbe16c_kube-apiserver-iz25beglnhtz_kube-system_033de1afc0844729cff5e100eb700a81_5931e490
# docker inspect 98ea64bbf6c8
... ...
"HostConfig": {
"NetworkMode": "container:4f87d22b833425082be55851d72268023d41b50649e46c738430d9dfd3abea11",
}
... ...
# docker inspect 4f87d22b833425082be55851d72268023d41b50649e46c738430d9dfd3abea11
... ...
"HostConfig": {
"NetworkMode": "host",
}
... ...
```


从上面docker inspect的输出可以看出kube-apiserver pod里面的pause容器采用的网络模式是host网络，而以pause容器网络为基础的kube-apiserver 容器显然就继承了这一[network namespace](http://tonybai.com/2017/01/11/understanding-linux-network-namespace-for-docker-network/)。因此从外面看，访问Kube-apiserver这样的组件和以前没什么两样：在Master node上可以通过localhost:8080访问；在Node外，可以通过master_node_ip:6443端口访问。

### 三、核心组件启动配置调整

在kube-apiserver等核心组件还是以本地程序运行在物理机上的时代，修改kube-apiserver的启动参数，比如修改一下–service-node-port-range的范围、添加一个–basic-auth-file等，我们都可以通过直接修改/etc/default/kube-apiserver(以Ubuntu 14.04为例)文件的内容并重启kube-apiserver service(service restart kube-apiserver)的方式实现。其他核心组件：诸如：kube-controller-manager、kube-proxy和kube-scheduler均是如此。

但在kubeadm时代，这些配置文件不再存在，取而代之的是和用户Pod描述文件类似的manifest文件(都放置在/etc/kubernetes/manifests下面)：

```
/etc/kubernetes/manifests# ls
etcd.json kube-apiserver.json kube-controller-manager.json kube-scheduler.json
```


我们以为kube-apiserver增加一个启动参数：”–service-node-port-range=80-32767″ 为例：

打开并编辑/etc/kubernetes/manifests/kube-apiserver.json，在“command字段对应的值中添加”–service-node-port-range=80-32767″：

```
"containers": [
{
"name": "kube-apiserver",
"image": "gcr.io/google_containers/kube-apiserver-amd64:v1.5.1",
"command": [
"kube-apiserver",
"--insecure-bind-address=127.0.0.1",
"--admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,PersistentVolumeLabel,DefaultStorageClass,ResourceQuota",
"--service-cluster-ip-range=10.96.0.0/12",
"--service-account-key-file=/etc/kubernetes/pki/apiserver-key.pem",
"--client-ca-file=/etc/kubernetes/pki/ca.pem",
"--tls-cert-file=/etc/kubernetes/pki/apiserver.pem",
"--tls-private-key-file=/etc/kubernetes/pki/apiserver-key.pem",
"--token-auth-file=/etc/kubernetes/pki/tokens.csv",
"--secure-port=6443",
"--allow-privileged",
"--advertise-address=10.47.217.91",
"--kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname",
"--anonymous-auth=false",
"--etcd-servers=http://127.0.0.1:2379",
"--service-node-port-range=80-32767"
],
```


注意：不要忘记在–etcd-servers这一行后面添加一个逗号，否则kube-apiserver会退出。

修改后，你会发现kube-apiserver会被自动重启。这是kubelet的功劳。kubelet在启动时监听/etc/kubernetes/manifests目录下的文件变化并做适当处理：

```
# ps -ef|grep kubelet
root 1633 1 5 2016 ? 1-09:24:47 /usr/bin/kubelet --kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true --pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true --network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin --cluster-dns=10.96.0.10 --cluster-domain=cluster.local
```


kubelet自身是一个[systemd](http://tonybai.com/2016/12/27/when-docker-meets-systemd/)的service，它的启动配置可以通过下面文件修改：

```
# cat /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
[Service]
Environment="KUBELET_KUBECONFIG_ARGS=--kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true"
Environment="KUBELET_SYSTEM_PODS_ARGS=--pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true"
Environment="KUBELET_NETWORK_ARGS=--network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin"
Environment="KUBELET_DNS_ARGS=--cluster-dns=10.96.0.10 --cluster-domain=cluster.local"
ExecStart=
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_SYSTEM_PODS_ARGS $KUBELET_NETWORK_ARGS $KUBELET_DNS_ARGS $KUBELET_EXTRA_ARGS
```


### 四、kubectl的配置

kube-up.sh安装的k8s集群会在每个Node上的~/.kube/下创建config文件，用于kubectl访问apiserver和操作集群使用。但在kubeadm模式下，~/.kube/下面的内容变成了：

```
~/.kube# ls
cache/ schema/
```


于是有了问题1：config哪里去了？

之所以在master node上我们的kubectl依旧可以工作，那是因为默认kubectl会访问localhost:8080来与kube-apiserver交互。如果kube-apiserver没有关闭–insecure-port，那么kubectl便可以正常与kube-apiserver交互，因为–insecure-port是没有任何校验机制的。

于是又了问题2：如果是其他node上的kubectl与kube-apiserver通信或者master node上的kubectl通过secure port与kube-apiserver通信，应该如何配置？

接下来，我们一并来回答上面两个问题。kubeadm在创建集群时，在master node的/etc/kubernetes下面创建了两个文件：

```
/etc/kubernetes# ls -l
total 32
-rw------- 1 root root 9188 Dec 28 17:32 admin.conf
-rw------- 1 root root 9188 Dec 28 17:32 kubelet.conf
... ...
```


这两个文件的内容是完全一样的，仅从文件名可以看出是谁在使用。比如kubelet.conf这个文件，我们就在kubelet程序的启动参数中看到过：–kubeconfig=/etc/kubernetes/kubelet.conf

```
# ps -ef|grep kubelet
root 1633 1 5 2016 ? 1-09:26:41 /usr/bin/kubelet --kubeconfig=/etc/kubernetes/kubelet.conf --require-kubeconfig=true --pod-manifest-path=/etc/kubernetes/manifests --allow-privileged=true --network-plugin=cni --cni-conf-dir=/etc/cni/net.d --cni-bin-dir=/opt/cni/bin --cluster-dns=10.96.0.10 --cluster-domain=cluster.local
```


打开这个文件，你会发现这就是一个kubeconfig文件，文件内容较长，我们通过kubectl config view来查看一下这个文件的结构：

```
# kubectl --kubeconfig /etc/kubernetes/kubelet.conf config view
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: REDACTED
server: https://{master node local ip}:6443
name: kubernetes
contexts:
- context:
cluster: kubernetes
user: admin
name: admin@kubernetes
- context:
cluster: kubernetes
user: kubelet
name: kubelet@kubernetes
current-context: admin@kubernetes
kind: Config
preferences: {}
users:
- name: admin
user:
client-certificate-data: REDACTED
client-key-data: REDACTED
- name: kubelet
user:
client-certificate-data: REDACTED
client-key-data: REDACTED
```


这和我们在《[Kubernetes集群Dashboard插件安装](http://tonybai.com/2017/01/19/install-dashboard-addon-for-k8s/)》一文中介绍的kubeconfig文件内容并不二致。不同之处就是“REDACTED”这个字样的值，我们对应到kubelet.conf中，发现每个REDACTED字样对应的都是一段数据，这段数据是由对应的数字证书内容或密钥内容转换(base64)而来的，在访问apiserver时会用到。

我们在minion node上测试一下：

```
minion node：
# kubectl get pods
The connection to the server localhost:8080 was refused - did you specify the right host or port?
# kubectl --kubeconfig /etc/kubernetes/kubelet.conf get pods
NAME READY STATUS RESTARTS AGE
my-nginx-1948696469-359d6 1/1 Running 2 26d
my-nginx-1948696469-3g0n7 1/1 Running 3 26d
my-nginx-1948696469-xkzsh 1/1 Running 2 26d
my-ubuntu-2560993602-5q7q5 1/1 Running 2 26d
my-ubuntu-2560993602-lrrh0 1/1 Running 2 26d
```


kubeadm创建k8s集群时，会在master node上创建一些用于组件间访问的证书、密钥和token文件，上面的kubeconfig中的“REDACTED”所代表的内容就是从这些文件转化而来的：

```
/etc/kubernetes/pki# ls
apiserver-key.pem apiserver.pem apiserver-pub.pem ca-key.pem ca.pem ca-pub.pem sa-key.pem sa-pub.pem tokens.csv
```


- apiserver-key.pem：kube-apiserver的私钥文件
- apiserver.pem：kube-apiserver的公钥证书
- apiserver-pub.pem kube-apiserver的公钥文件
- ca-key.pem：CA的私钥文件
- ca.pem：CA的公钥证书
- ca-pub.pem ：CA的公钥文件
- sa-key.pem ：serviceaccount私钥文件
- sa-pub.pem ：serviceaccount的公钥文件
- tokens.csv：kube-apiserver用于校验的token文件

在k8s各核心组件的启动参数中会看到上面文件的身影，比如：

```
kube-apiserver --insecure-bind-address=127.0.0.1 --admission-control=NamespaceLifecycle,LimitRanger,ServiceAccount,PersistentVolumeLabel,DefaultStorageClass,ResourceQuota --service-cluster-ip-range=10.96.0.0/12 --service-account-key-file=/etc/kubernetes/pki/apiserver-key.pem --client-ca-file=/etc/kubernetes/pki/ca.pem --tls-cert-file=/etc/kubernetes/pki/apiserver.pem --tls-private-key-file=/etc/kubernetes/pki/apiserver-key.pem --token-auth-file=/etc/kubernetes/pki/tokens.csv --secure-port=6443 --allow-privileged --advertise-address={master node local ip} --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname --anonymous-auth=false --etcd-servers=http://127.0.0.1:2379 --service-node-port-range=80-32767
```


我们还可以在minion node上通过curl还手工测试一下通过安全通道访问master node上的kube-apiserver。在《[Kubernetes集群的安全配置](http://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster/)》一文中，我们提到过k8s的authentication（包括：客户端证书认证、basic auth、static token等）只要通过其中一个即可。当前kube-apiserver开启了客户端证书认证（–client-ca-file）和static token验证(–token-auth-file)，我们只要通过其中一个，就可以通过authentication，于是我们使用static token方式。static token file的内容格式：

```
token,user,uid,"group1,group2,group3"
```


对应到master node上的tokens.csv

```
# cat /etc/kubernetes/pki/tokens.csv
{token},{user},812ffe41-cce0-11e6-9bd3-00163e1001d7,system:kubelet-bootstrap
```


我们用这个token通过curl与apiserver交互：

```
# curl --cacert /etc/kubernetes/pki/ca.pem -H "Authorization: Bearer {token}" https://{master node local ip}:6443
{
"paths": [
"/api",
"/api/v1",
"/apis",
"/apis/apps",
"/apis/apps/v1beta1",
"/apis/authentication.k8s.io",
"/apis/authentication.k8s.io/v1beta1",
"/apis/authorization.k8s.io",
"/apis/authorization.k8s.io/v1beta1",
"/apis/autoscaling",
"/apis/autoscaling/v1",
"/apis/batch",
"/apis/batch/v1",
"/apis/batch/v2alpha1",
"/apis/certificates.k8s.io",
"/apis/certificates.k8s.io/v1alpha1",
"/apis/extensions",
"/apis/extensions/v1beta1",
"/apis/policy",
"/apis/policy/v1beta1",
"/apis/rbac.authorization.k8s.io",
"/apis/rbac.authorization.k8s.io/v1alpha1",
"/apis/storage.k8s.io",
"/apis/storage.k8s.io/v1beta1",
"/healthz",
"/healthz/poststarthook/bootstrap-controller",
"/healthz/poststarthook/extensions/third-party-resources",
"/healthz/poststarthook/rbac/bootstrap-roles",
"/logs",
"/metrics",
"/swaggerapi/",
"/ui/",
"/version"
]
}
```


交互成功！

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论