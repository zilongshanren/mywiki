---
title: minikube v1.20.0版本的一个bug
url: https://tonybai.com/2021/05/14/a-bug-of-minikube-1-20/
published: '2021-05-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# minikube v1.20.0版本的一个bug

![img{512x368}](../../assets/850ad21831a9d766.png)


[本文永久链接](https://tonybai.com/2021/05/14/a-bug-of-minikube-1-20) – https://tonybai.com/2021/05/14/a-bug-of-minikube-1-20

近期在研究[dapr(分布式应用运行时)](https://dapr.io)，这是一个很朴素却很棒的想法，目前大厂，如[阿里](https://mp.weixin.qq.com/s/Dsb7rwu5tRAizJ7Wdr23Fw)和[鹅厂](https://mp.weixin.qq.com/s/4HHMVxa3l_gCsltoX4euyg)都有大牛在研究该项目，甚至是利用dapr落地了部分应用。关于dapr，后续我也会用单独的文章详细说说。

dapr不仅支持k8s部署，还支持本地部署，并可以对接多个世界知名的公有云厂商的服务，比如：aws、azure、阿里云等。为了体验dapr对云原生应用的支持，我选择了将其部署于k8s中，同时我选择使用[minikube](https://github.com/kubernetes/minikube)来构建本地k8s开发环境。而本文要说的就是将dapr安装到minikube时遇到的问题。

### 1. 安装minikube

Kubernetes在4月份发布了最新的[1.21版本](https://kubernetes.io/blog/2021/04/08/kubernetes-1-21-release-announcement/)，但目前minikube的最新版依然为[1.20版本](https://github.com/kubernetes/minikube/releases/tag/v1.20.0)。

minikube是k8s项目自己维护的一个k8s本地开发环境项目，它与k8s的api接口兼容，我们可以快速搭建一个minikube来进行k8s学习和实践。[minikube官网](https://minikube.sigs.k8s.io/docs/start/)上有关于它的安装、使用和维护的详尽资料。

我这里在一个ubuntu 18.04的腾讯云主机上(1 vcpu, 2g mem)上安装minikube v1.20，minikube是一个单体二进制文件，我们先将这个文件下载到本地：

```
# curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
% Total % Received % Xferd Average Speed Time Time Time Current
Dload Upload Total Spent Left Speed
0 0 0 0 0 0 0 0 --:--:-- --:--:-- --:--:-- 0
100 60.9M 100 60.9M 0 0 7764k 0 0:00:08 0:00:08 --:--:-- 11.5M
# install minikube-linux-amd64 /usr/local/bin/minikube
```


验证是否下载ok：

```
# minikube version
minikube version: v1.20.0
commit: c61663e942ec43b20e8e70839dcca52e44cd85ae
```


接下来我们就利用minikube启动一个k8s cluster用作本地开发环境。由于minikube默认的最低安装要求为2核cpu，而我的虚机仅为1核，我们需要为minikube传递一些命令行参数以让其在单核CPU上也能顺利地启动一个k8s cluster。另外minikube会从gcr.io这个国内被限制访问的站点下载一些控制平面的容器镜像，为了能让此过程顺利进行下去，我们还需要告诉minikube从哪个gcr.io的mirror站点下载容器镜像：

```
# minikube start --extra-config=kubeadm.ignore-preflight-errors=NumCPU --force --cpus 1 --memory=1024mb --image-mirror-country='cn'
minikube v1.20.0 on Ubuntu 18.04 (amd64)
minikube skips various validations when --force is supplied; this may lead to unexpected behavior
Automatically selected the docker driver. Other choices: ssh, none
Requested cpu count 1 is less than the minimum allowed of 2
has less than 2 CPUs available, but Kubernetes requires at least 2 to be available
Your cgroup does not allow setting memory.
▪ More information: https://docs.docker.com/engine/install/linux-postinstall/#your-kernel-does-not-support-cgroup-swap-limit-capabilities
Requested memory allocation 1024MiB is less than the usable minimum of 1800MB
Requested memory allocation (1024MB) is less than the recommended minimum 1900MB. Deployments may fail.
The requested memory allocation of 1024MiB does not leave room for system overhead (total system memory: 1833MiB). You may face stability issues.
Suggestion: Start minikube with less memory allocated: 'minikube start --memory=1833mb'
The "docker" driver should not be used with root privileges.
If you are running minikube within a VM, consider using --driver=none:
https://minikube.sigs.k8s.io/docs/reference/drivers/none/
Using image repository registry.cn-hangzhou.aliyuncs.com/google_containers
Starting control plane node minikube in cluster minikube
Pulling base image ...
> registry.cn-hangzhou.aliyun...: 20.48 MiB / 358.10 MiB 5.72% 2.89 MiB p/
> registry.cn-hangzhou.aliyun...: 358.10 MiB / 358.10 MiB 100.00% 3.50 MiB
> registry.cn-hangzhou.aliyun...: 358.10 MiB / 358.10 MiB 100.00% 3.50 MiB
> registry.cn-hangzhou.aliyun...: 358.10 MiB / 358.10 MiB 100.00% 3.50 MiB
> registry.cn-hangzhou.aliyun...: 358.10 MiB / 358.10 MiB 100.00% 6.83 MiB
Creating docker container (CPUs=1, Memory=1024MB) ...
Preparing Kubernetes v1.20.2 on Docker 20.10.6 ...
▪ kubeadm.ignore-preflight-errors=NumCPU
▪ Generating certificates and keys ...
▪ Booting up control plane ...
▪ Configuring RBAC rules ...
Verifying Kubernetes components...
▪ Using image registry.cn-hangzhou.aliyuncs.com/google_containers/k8s-minikube/storage-provisioner:v5 (global image repository)
Enabled addons: default-storageclass, storage-provisioner
/usr/local/bin/kubectl is version 1.17.9, which may have incompatibilites with Kubernetes 1.20.2.
▪ Want kubectl v1.20.2? Try 'minikube kubectl -- get pods -A'
Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```


查看启动的k8s集群状态：

```
# minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```


我们看到minikube似乎成功启动了一个k8s cluster。

### 2. pod storage-provisioner处于ErrImagePull状态

在后续使用helm安装[redis](https://mp.weixin.qq.com/s/vhhARqk0QT0sltJQMi_s7w)作为state store组件(components)时，发现安装后的redis处于下面的状态：

```
# kubectl get pod
NAME READY STATUS RESTARTS AGE
redis-master-0 0/1 Pending 0 7m48s
redis-replicas-0 0/1 Pending 0 7m48s
```


通过kubectl describe命令详细查看redis-master-0这个pod：

```
# kubectl describe pod redis-master-0
Name: redis-master-0
Namespace: default
Priority: 0
Node: <none>
Labels: app.kubernetes.io/component=master
app.kubernetes.io/instance=redis
app.kubernetes.io/managed-by=Helm
app.kubernetes.io/name=redis
controller-revision-hash=redis-master-694655df77
helm.sh/chart=redis-14.1.1
statefulset.kubernetes.io/pod-name=redis-master-0
Annotations: checksum/configmap: 0898a3adcb5d0cdd6cc60108d941d105cc240250ba6c7f84ed8b5337f1edd470
checksum/health: 1b44d34c6c39698be89b2127b9fcec4395a221cff84aeab4fbd93ff4a636c210
checksum/scripts: 465f195e1bffa9700282b017abc50056099e107d7ce8927fb2b97eb348907484
checksum/secret: cd7ff82a84f998f50b11463c299c1200585036defc7cbbd9c141cc992ad80963
Status: Pending
IP:
IPs: <none>
Controlled By: StatefulSet/redis-master
Containers:
redis:
Image: docker.io/bitnami/redis:6.2.3-debian-10-r0
Port: 6379/TCP
Host Port: 0/TCP
Command:
/bin/bash
Args:
-c
/opt/bitnami/scripts/start-scripts/start-master.sh
Liveness: exec [sh -c /health/ping_liveness_local.sh 5] delay=5s timeout=6s period=5s #success=1 #failure=5
Readiness: exec [sh -c /health/ping_readiness_local.sh 1] delay=5s timeout=2s period=5s #success=1 #failure=5
Environment:
BITNAMI_DEBUG: false
REDIS_REPLICATION_MODE: master
ALLOW_EMPTY_PASSWORD: no
REDIS_PASSWORD: <set to the key 'redis-password' in secret 'redis'> Optional: false
REDIS_TLS_ENABLED: no
REDIS_PORT: 6379
Mounts:
/data from redis-data (rw)
/health from health (rw)
/opt/bitnami/redis/etc/ from redis-tmp-conf (rw)
/opt/bitnami/redis/mounted-etc from config (rw)
/opt/bitnami/scripts/start-scripts from start-scripts (rw)
/tmp from tmp (rw)
/var/run/secrets/kubernetes.io/serviceaccount from redis-token-rtxk2 (ro)
Conditions:
Type Status
PodScheduled False
Volumes:
redis-data:
Type: PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
ClaimName: redis-data-redis-master-0
ReadOnly: false
start-scripts:
Type: ConfigMap (a volume populated by a ConfigMap)
Name: redis-scripts
Optional: false
health:
Type: ConfigMap (a volume populated by a ConfigMap)
Name: redis-health
Optional: false
config:
Type: ConfigMap (a volume populated by a ConfigMap)
Name: redis-configuration
Optional: false
redis-tmp-conf:
Type: EmptyDir (a temporary directory that shares a pod's lifetime)
Medium:
SizeLimit: <unset>
tmp:
Type: EmptyDir (a temporary directory that shares a pod's lifetime)
Medium:
SizeLimit: <unset>
redis-token-rtxk2:
Type: Secret (a volume populated by a Secret)
SecretName: redis-token-rtxk2
Optional: false
QoS Class: BestEffort
Node-Selectors: <none>
Tolerations: node.kubernetes.io/not-ready:NoExecute for 300s
node.kubernetes.io/unreachable:NoExecute for 300s
Events:
Type Reason Age From Message
---- ------ ---- ---- -------
Warning FailedScheduling 18s (x6 over 5m7s) default-scheduler 0/1 nodes are available: 1 pod has unbound immediate PersistentVolumeClaims.
```


我们发现是该pod的PersistentVolumeClaims没有得到满足，没有绑定到适当PV(persistent volume)上。查看pvc的状态，也都是pending：

```
# kubectl get pvc
NAME STATUS VOLUME CAPACITY ACCESS MODES STORAGECLASS AGE
redis-data-redis-master-0 Pending standard 35m
redis-data-redis-replicas-0 Pending standard 35m
```


详细查看其中一个pvc的状态：

```
# kubectl describe pvc redis-data-redis-master-0
Name: redis-data-redis-master-0
Namespace: default
StorageClass: standard
Status: Pending
Volume:
Labels: app.kubernetes.io/component=master
app.kubernetes.io/instance=redis
app.kubernetes.io/name=redis
Annotations: volume.beta.kubernetes.io/storage-provisioner: k8s.io/minikube-hostpath
Finalizers: [kubernetes.io/pvc-protection]
Capacity:
Access Modes:
VolumeMode: Filesystem
Mounted By: redis-master-0
Events:
Type Reason Age From Message
---- ------ ---- ---- -------
Normal ExternalProvisioning 55s (x143 over 35m) persistentvolume-controller waiting for a volume to be created, either by external provisioner "k8s.io/minikube-hostpath" or manually created by system administrator
```


我们看到该pvc在等待绑定一个volume，而k8s cluster当前在default命名空间中没有任何pv资源。问题究竟出在哪里？

我们回到minikube自身上来，在minikube文档中，负责自动创建HostPath类型pv的是storage-provisioner插件：

![img{512x368}](../../assets/59adf940a0bce7ea.png)



我们看到storage-provisioner插件的状态为enabled，那么为什么该插件没能为redis提供需要的pv资源呢？我顺便查看了一下当前k8s cluster的控制平面组件的运行情况：

```
# kubectl get po -n kube-system
NAMESPACE NAME READY STATUS RESTARTS AGE
kube-system coredns-54d67798b7-n6vw4 1/1 Running 0 20h
kube-system etcd-minikube 1/1 Running 0 20h
kube-system kube-apiserver-minikube 1/1 Running 0 20h
kube-system kube-controller-manager-minikube 1/1 Running 0 20h
kube-system kube-proxy-rtvvj 1/1 Running 0 20h
kube-system kube-scheduler-minikube 1/1 Running 0 20h
kube-system storage-provisioner 0/1 ImagePullBackOff 0 20h
```


我们惊奇的发现：storage-provisioner这个pod居然处于ImagePullBackOff状态，即下载镜像有误！

### 3. 发现真相

还记得在minikube start命令的输出信息的末尾，我们看到这样一行内容：

```
Using image registry.cn-hangzhou.aliyuncs.com/google_containers/k8s-minikube/storage-provisioner:v5 (global image repository)
```


也就是说我们从registry.cn-hangzhou.aliyuncs.com下载storage-provisioner:v5有错误！我手动在本地执行了一下下面命令：

```
# docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/k8s-minikube/storage-provisioner:v5
Error response from daemon: pull access denied for registry.cn-hangzhou.aliyuncs.com/google_containers/k8s-minikube/storage-provisioner, repository does not exist or may require 'docker login': denied: requested access to the resource is denied
```


居然真的无法下载成功！

究竟是什么地方出现问题了呢？从提示来看，要么是该镜像不存在，要么是docker login被拒绝，由于registry.cn-hangzhou.aliyuncs.com是公共仓库，因此不存在docker login的问题，那么就剩下一个原因了：镜像不存在！

于是我在minikube官方的issue试着搜索了一下有关registry.cn-hangzhou.aliyuncs.com作为mirror的问题，还真让我捕捉到了蛛丝马迹。

在https://github.com/kubernetes/minikube/pull/10770这PR中，有人提及当–image-mirror-country使用cn时，minikube使用了错误的storage-provisioner镜像，镜像的地址不应该是registry.cn-hangzhou.aliyuncs.com/google_containers/k8s-minikube/storage-provisioner:v5，而应该是registry.cn-hangzhou.aliyuncs.com/google_containers/storage-provisioner:v5。

我在本地试了一下registry.cn-hangzhou.aliyuncs.com/google_containers/k8s-minikube/storage-provisioner:v5，的确可以下载成功：

```
# docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/storage-provisioner:v5
v5: Pulling from google_containers/storage-provisioner
Digest: sha256:18eb69d1418e854ad5a19e399310e52808a8321e4c441c1dddad8977a0d7a944
Status: Image is up to date for registry.cn-hangzhou.aliyuncs.com/google_containers/storage-provisioner:v5
registry.cn-hangzhou.aliyuncs.com/google_containers/storage-provisioner:v5
```


### 4. 解决问题

发现问题真相：当–image-mirror-country使用cn时，minikube使用了错误的storage-provisioner镜像。那我们如何修正这个问题呢？

我们查看一下storage-provisioner pod的imagePullPolicy：

```
# kubectl get pod storage-provisioner -n kube-system -o yaml
... ...
spec:
containers:
- command:
- /storage-provisioner
image: registry.cn-hangzhou.aliyuncs.com/google_containers/k8s-minikube/storage-provisioner:v5
imagePullPolicy: IfNotPresent
name: storage-provisioner
```


我们发现storage-provisioner的imagePullPolicy为ifNotPresent，这意味着如果本地有storage-provisioner:v5这个镜像的话，minikube不会再去远端下载该image。这样我们可以先将storage-provisioner:v5下载到本地并重新tag为registry.cn-hangzhou.aliyuncs.com/google_containers/k8s-minikube/storage-provisioner:v5。

下面我们就来操作一下：

```
# docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/storage-provisioner:v5 registry.cn-hangzhou.aliyuncs.com/google_containers/k8s-minikube/storage-provisioner:v5
```


一旦有了image，通过minikube addons子命令重新enable对应pod，可以重启storage-provisioner pod，让其进入正常状态：

```
# minikube addons enable storage-provisioner
▪ Using image registry.cn-hangzhou.aliyuncs.com/google_containers/k8s-minikube/storage-provisioner:v5 (global image repository)
The 'storage-provisioner' addon is enabled
# kubectl get po -n kube-system
NAME READY STATUS RESTARTS AGE
coredns-54d67798b7-n6vw4 1/1 Running 0 25h
etcd-minikube 1/1 Running 0 25h
kube-apiserver-minikube 1/1 Running 0 25h
kube-controller-manager-minikube 1/1 Running 0 25h
kube-proxy-rtvvj 1/1 Running 0 25h
kube-scheduler-minikube 1/1 Running 0 25h
storage-provisioner 1/1 Running 0 69m
```


当storgae-provisioner恢复正常后，之前安装的dapr state component组件redis也自动恢复正常了：

```
# kubectl get pod
NAME READY STATUS RESTARTS AGE
redis-master-0 1/1 Running 0 18h
redis-replicas-0 1/1 Running 1 18h
redis-replicas-1 1/1 Running 0 16h
redis-replicas-2 1/1 Running 0 16h
```


[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论