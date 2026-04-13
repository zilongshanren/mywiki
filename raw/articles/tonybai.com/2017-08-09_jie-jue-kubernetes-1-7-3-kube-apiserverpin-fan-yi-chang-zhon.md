---
title: 解决Kubernetes 1.7.3 kube-apiserver频繁异常重启的问题
url: https://tonybai.com/2017/08/09/fix-kube-apiserver-restart-exceptionally-in-k8s-1-7-3/
published: '2017-08-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 解决Kubernetes 1.7.3 kube-apiserver频繁异常重启的问题

近期将之前的一个[用kube-up.sh安装的Kubernetes 1.3.7](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)的环境更换为最新发布的[用kubeadm安装](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)的[Kubernetes 1.7.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.7.3)版本。新版本的安装过程和之前的[采用kubeadm安装](http://tonybai.com/2017/01/24/explore-kubernetes-cluster-installed-by-kubeadm/)的k8s 1.5.x、[1.6.x版本](http://tonybai.com/2017/07/20/fix-cannot-access-dashboard-in-k8s-1-6-4/)类似，这里不赘述了。但在安装[Dashboard](http://tonybai.com/2017/01/19/install-dashboard-addon-for-k8s/)后，发现了一些问题，这里记录一下解决的过程。

## 一、第一个问题

我们先来做一下回顾。在《[解决Kubernetes 1.6.4 Dashboard无法访问的问题](http://tonybai.com/2017/07/20/fix-cannot-access-dashboard-in-k8s-1-6-4/)》一文中，我们通过把用户admin bind到cluster-admin这个clusterrole角色上使得dashboard得以正常访问。但访问几次后，我发现了一个问题：那就是用safari访问dashboard时，浏览器可以正常弹出鉴权对话框，让我输入用户名和密码；但用chrome访问时，总是无法弹出鉴权对话框，而直接显示如下错误：

```
User "system:anonymous" cannot get at the cluster scope.
```


[kube-apiserver身份验证](https://kubernetes.io/docs/admin/authentication/#anonymous-requests)文档中对anonymous requests做了说明：对于没有被其他身份验证方法拒绝的requests，kube-apiserver会为这样的request赋予用户名: **system:anonymous**和用户group: **system:unauthenticated**，这个request将继续流向后面的环节：[authorization](http://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster/)和admission-control，直到被后面的环节拒绝，返回失败应答。这一些都源于k8s 1.6以后的版本中，kube-apiserver的命令行选项：–anonymous-auth的默认值改为了true，即允许anonymous request的存在，因此上面chrome在访问kube-apiserver时，不输入user、password也能继续下面的环节，这就是第一个问题及其原因。

## 二、关闭匿名请求的身份验证权

解决上面这个问题，最直接的方法就是关闭匿名请求的身份验证权，即不接受匿名请求。我们通过在/etc/kubernetes/manifests/kube-apiserver.yaml中添加下面一行来实现：

```
spec:
containers:
- command:
- kube-apiserver
- --anonymous-auth=false
```


/etc/kubernetes/manifests/kube-apiserver.yaml被修改后，kubelet会重启kube-apiserver。重启后，我再用chrome访问dashboard，身份验证对话框就出现在眼前了。

## 三、kube-apiserver周期性异常重启

一直以为问题到这里就解决了。但随后又发生了一个更为严重的问题，那就是：[kube-apiserver](https://kubernetes.io/docs/admin/kube-apiserver/)定期重启，并牵连kube-controller-manager和kube-scheduler的status也不正常了。

通过kubectl describe查看状态异常的kube-apiserver pod，发现如下输出：

```
root@yypdcom2:# kubectl describe pods/kube-apiserver-yypdcom2 -n kube-system|grep health
Liveness: http-get https://127.0.0.1:6443/healthz delay=15s timeout=15s period=10s #success=1 #failure=8
```


可以看到liveness check有8次failure！8次是kube-apiserver的failure门槛值，这个值在/etc/kubernetes/manifests/kube-apiserver.yaml中我们可以看到：

```
livenessProbe:
failureThreshold: 8
httpGet:
host: 127.0.0.1
path: /healthz
port: 6443
scheme: HTTPS
initialDelaySeconds: 15
timeoutSeconds: 15
```


这样，一旦failure次数超限，kubelet会尝试Restart kube-apiserver，这就是问题的原因。那么为什么kube-apiserver的[liveness check](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/)会fail呢？这缘于我们关闭了匿名请求的身份验证权。还是来看/etc/kubernetes/manifests/kube-apiserver.yaml中的livenessProbe段，对于kube-apiserver来说，kubelet会通过访问: https://127.0.0.1:6443/healthz的方式去check是否ok？并且kubelet使用的是anonymous requests。由于上面我们已经关闭了对anonymous-requests的身份验证权，kubelet就会一直无法访问kube-apiserver的/healthz端点，导致kubelet认为kube-apiserver已经死亡，并尝试重启它。

## 四、调整/healthz检测的端点

我们既要保留 –anonymous-auth=false，还要保证kube-apiserver稳定运行不重启，我们就需要调整kube-apiserver的livenessProbe配置，将liveness probe的endpoint从

```
https://127.0.0.1:6443/healthz
```


改为：

```
http://127.0.0.1:8080/healthz
```


具体对/etc/kubernetes/manifests/kube-apiserver.yaml的修改是：

```
spec:
containers:
- command:
- kube-apiserver
- --anonymous-auth=false
... ...
- --insecure-bind-address=127.0.0.1
- --insecure-port=8080
livenessProbe:
failureThreshold: 8
httpGet:
host: 127.0.0.1
path: /healthz
port: 8080
scheme: HTTP
initialDelaySeconds: 15
timeoutSeconds: 15
... ...
```


我们不再用anonymous-requests，但我们可以利用–insecure-bind-address和–insecure-port。让kubelet的请求到insecure port，而不是secure port。由于insecure port的流量不会受到身份验证、授权等功能的限制，因此可以成功probe到kube-apiserver的liveness，kubelet不会再重启kube-apiserver了。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

希望 Tony 大佬有空写一篇调试 k8s 源码以及解读的文章, 学习 k8s 看源码感觉无从下手