---
title: Kubernetes集群Pod使用Host的本地时区设置
url: https://tonybai.com/2017/02/20/use-host-timezone-in-kubernetes-pods/
published: '2017-02-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes集群Pod使用Host的本地时区设置

[Kubernetes集群搭建](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)起来后，一直跑得很稳定。之前的关注点更多集中在[安装](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)、[配置](http://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster/)、[组件调试](http://tonybai.com/2017/01/19/install-dashboard-addon-for-k8s/)方面，一些细枝末节被忽略了。Pod中时区的设置就是其中之一。今天腾出功夫打算解决一下这个问题。

### 一、问题现象

在我的[Kubernetes 1.3.7集群](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)的Master Node上，我们执行：

```
# date
Mon Feb 20 11:49:20 CST 2017
```


之后，在该Node上随意找到一个Pod中的Container，通过docker exec切入到容器内执行：

```
# docker exec -it 1975d68de07a /bin/bash
root@1975d68de07a:/# date
Mon Feb 20 03:49:53 UTC 2017
```


我们发现Docker内输出的当前date与Host上输出的date是不一致的。这对于K8s集群自身的运转似乎并没有多大影响，至少运行这么长时间以来，未出现因为时间设置与Host不同而导致的问题。但是对跑在Pod中应用来说，这个时间设置的问题可能会给业务的运行带来很多烦恼。

总之，一般来说，让Pod里的时间设置与Host上的Local time设置保持一致总是没错的。这里我们就来尝试解决这个问题。

### 二、Pod使用Host时区设置的方案

我有两个K8s集群环境，一个是基于[ubuntu](http://tonybai.com/tag/ubuntu) 14.04 node的[k8s 1.3.7 环境](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)，一个是基于ubuntu 16.04 node[以kubeadm安装的k8s 1.5.1环境](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)。由于ubuntu 14.04和ubuntu 16.04 Host在timezone的设置上略有差异，因此我们也要分为几种情况对应(redhat系的os这里暂不涉及，但原理是相同的)：

#### 0、ubuntu上时区设置

在Ubuntu上，[/etc/localtime]是系统的本地时区设置文件，直接影响到系统的当前date输出。不过在Ubuntu 14.04和Ubuntu 16.04上，这个文件的内容稍有不同：

在Ubuntu 14.04上，/etc/localtime就是一个regular file，其存储着本地时区的配置数据：

```
# file /etc/localtime
/etc/localtime: timezone data, version 2, 2 gmt time flags, 2 std time flags, no leap seconds, 16 transition times, 2 abbreviation chars
```


在我的Node上，其内容与/usr/share/zoneinfo/Asia/Shanghai指向的内容一致，好像/etc/localtime是这么得来的：

```
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```


而在Ubuntu 16.04上，/etc/localtime是一个symbolic link，链接到文件：/usr/share/zoneinfo/Asia/Shanghai

```
# file /etc/localtime
/etc/localtime: symbolic link to /usr/share/zoneinfo/Asia/Shanghai
```


/usr/share/zoneinfo下存储着真正的时区设置文件，/usr/share/zoneinfo/Asia/Shanghai也是一个符号链接，指向的是/usr/share/zoneinfo/PRC：

```
# file /usr/share/zoneinfo/PRC
/usr/share/zoneinfo/PRC: timezone data, version 2, 2 gmt time flags, 2 std time flags, no leap seconds, 16 transition times, 2 abbreviation chars
```


在14.04 Node上，/etc/localtime与/usr/share/zoneinfo/PRC文件的内容是一模一样的。但在14.04的Pod中，这两个文件内容却是不同的：

```
# docker exec -it fe936562b6ee /bin/bash
# diff /etc/localtime /usr/share/zoneinfo/PRC
Binary files /etc/localtime and /usr/share/zoneinfo/PRC differ
```


因此，如果要让Pod使用的本地时区设置与Host的一致，就必须在Pod的manifest中做些“手脚”，接下来我们来分门别类地仔细看看。

#### 1、Host 14.04，Pod 16.04

我们在14.04的node上随意run一个16.04的容器，可以看到：

```
# docker run -it ubuntu:16.04 /bin/bash
root@bf7cec08df23:/# ls -l /etc/localtime
lrwxrwxrwx 1 root root 27 Jan 19 16:33 /etc/localtime -> /usr/share/zoneinfo/Etc/UTC
```


容器内的系统时间与host时间是不一致的。

我们来创建一个使用ubuntu 16.04的docker image:

```
//1604pod-image-dockerfile
FROM ubuntu:16.04
CMD ["tail", "-f", "/var/log/bootstrap.log"]
```


在本地构建这个image：

```
# docker build -f ./1604pod-image-dockerfile -t 1604podimage:latest .
Sending build context to Docker daemon 5.632 kB
Step 1 : FROM ubuntu:16.04
---> f49eec89601e
Step 2 : CMD tail -f /var/log/bootstrap.log
---> Using cache
---> 06ffb5c85d7c
Successfully built 06ffb5c85d7c
# docker images|grep 1604pod
1604podimage latest 06ffb5c85d7c 28 minutes ago 129.5 MB
```


我们来编写这个运行于16.04之上的pod的manifest文件：

```
//1604-pod-on-1404-host.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: my-testpod
spec:
replicas: 1
template:
metadata:
labels:
run: my-testpod
spec:
containers:
- name: my-testpod
image: 1604podimage:latest
imagePullPolicy: IfNotPresent
volumeMounts:
- name: tz-config
mountPath: /etc/localtime
volumes:
- name: tz-config
hostPath:
path: /usr/share/zoneinfo/Asia/Shanghai
```


我们将/usr/share/zoneinfo/Asia/Shanghai直接挂载为路径/etc/locatime了。创建该Pod并检查Pod内的系统时间：

```
# kubectl create -f 1604-pod-on-1404-host.yaml
deployment "my-testpod" created
# kubectl exec my-testpod-802169720-ehqlt date
Mon Feb 20 14:19:13 CST 2017
# date
Mon Feb 20 14:19:15 CST 2017
```


可以看出Pod内的系统时间与Host上的时间在时区上保持一致了。

#### 2、Host 14.04， Pod 14.04

在ubuntu 14.04中，由于/etc/localtime自身就存储着时区设置，因此我们需要将其mount到Pod的对应位置中。我们的image demo如下：

```
//1404pod-image-dockerfile
FROM ubuntu:14.04
CMD ["tail", "-f", "/var/log/bootstrap.log"]
```


构建该image：

```
# docker build -f ./1404pod-image-dockerfile -t 1404podimage:latest .
Sending build context to Docker daemon 5.632 kB
Step 1 : FROM ubuntu:14.04
---> f2d8ce9fa988
Step 2 : CMD tail -f /var/log/bootstrap.log
---> Running in 6815ca6fe9d9
---> bc7f7de7690d
Removing intermediate container 6815ca6fe9d9
Successfully built bc7f7de7690d
# docker images|grep 1404pod
1404podimage latest bc7f7de7690d 8 seconds ago 187.9 MB
```


Pod manifest如下：

```
//1404-pod-on-1404-host.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: my-testpod
spec:
replicas: 1
template:
metadata:
labels:
run: my-testpod
spec:
containers:
- name: my-testpod
image: 1404podimage:latest
imagePullPolicy: IfNotPresent
volumeMounts:
- name: tz-config
mountPath: /etc/localtime
volumes:
- name: tz-config
hostPath:
path: /etc/localtime
```


可以看到，我们将host的/etc/locatime挂载到Pod内的/etc/localtime。创建该Pod后，我们查看一下Pod内的系统时间：

```
# kubectl exec my-testpod-2443385716-g9d4n date
Mon Feb 20 14:44:57 CST 2017
# date
Mon Feb 20 14:44:59 CST 2017
```


可以看出：两者在时区设置上已经一致了。

#### 3、Host 16.04，Pod 16.04

由于有了上面的铺垫，后续的这两种情况，鉴于篇幅，我将简单描述。这里我们还将利用上面创建的两个image：1404podimage:latest和1604podimage:latest。

pod的manifest文件如下：

```
//1604-pod-on-1604-host.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: my-testpod
spec:
replicas: 1
template:
metadata:
labels:
run: my-testpod
spec:
containers:
- name: my-testpod
image: 1604podimage:latest
imagePullPolicy: IfNotPresent
volumeMounts:
- name: tz-config
mountPath: /etc/localtime
volumes:
- name: tz-config
hostPath:
path: /usr/share/zoneinfo/Asia/Shanghai
```


创建该Pod后，查看系统时间：

```
# kubectl exec my-testpod-3193072711-7kwdl date
Mon Feb 20 14:55:00 CST 2017
# date
Mon Feb 20 14:55:31 CST 2017
```


主机和Pod内的系统时间在时区上一致了。

#### 4、Host 16.04，Pod 14.04

pod的manifest文件如下：

```
//1404-pod-on-1604-host.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: my-testpod
spec:
replicas: 1
template:
metadata:
labels:
run: my-testpod
spec:
containers:
- name: my-testpod
image: 1404podimage:latest
imagePullPolicy: IfNotPresent
volumeMounts:
- name: tz-config
mountPath: /etc/localtime
volumes:
- name: tz-config
hostPath:
path: /usr/share/zoneinfo/Asia/Shanghai
```


创建该Pod，对比Pod内时间和host时间：

```
# kubectl exec my-testpod-3024383045-xqbcv date
Mon Feb 20 14:58:54 CST 2017
# date
Mon Feb 20 14:58:49 CST 2017
```


主机和Pod内的系统时间在时区上一致了。

### 三、小结

上面所涉及到的manifest文件和Dockerfile文件源码在[这里](https://github.com/bigwhite/experiments/tree/master/k8s-tzconfig)可以下载到，你可能需要根据你自己的k8s环境做些许改动。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com账号: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

为啥我的16.04上不是链接，而是和14.04上一模一样的

centos 7是一个链接，centos6和ubuntu一样，特别是和ubuntu14.04上的文件md5都一样

如果修改了镜像内 CST时区，K8S托管启动容器 内为什么还是UTC呢？

没太理解您的问题。让pod挂载本地时区的路径后，pod内的时区都变成了CST了啊。何来UTC？