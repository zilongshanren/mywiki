---
title: 实践kubernetes ingress controller的四个例子
url: https://tonybai.com/2018/06/21/kubernetes-ingress-controller-practice-using-four-examples/
published: '2018-06-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 实践kubernetes ingress controller的四个例子

我之前并未使用过标准的[Kubernetes ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)，而是自己实现了一个基于[nginx](https://tonybai.com/tag/nginx)的、类似[ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers)的服务入口管理程序nginx-kit。这个程序会部署到[Kubernetes集群](https://tonybai.com/tag/kubernetes)中，以Pod形式运行。该Pod由两个Container组成，一个Container放置了一个由脚本启动的nginx；另外一个Container中放置的是一个conf generator程序，它监听Kubernetes集群service对象的变更，并根据变更情况动态生成nginx的配置文件。第一个Container中的脚本会监听配置文件目录的变化，并reload配置文件信息实现Kubernetes内部服务对外暴露入口的动态管理。关于这个程序的详情可以参考我之前写的两篇文章：《[Kubernetes集群中的Nginx配置热更新方案](http://tonybai.com/2016/11/17/nginx-config-hot-reloading-approach-for-kubernetes-cluster/)》和《[为Kubernetes集群中服务部署Nginx入口服务](http://tonybai.com/2016/11/22/deploy-nginx-service-for-the-services-in-kubernetes-cluster/)》。

近期在使用ingress controller对内部服务入口的暴露进行动态管理，使用后发现我之前实现的nginx kit与ingress controller的实现之一: [ingress-nginx](https://github.com/kubernetes/ingress-nginx/)简直是异曲同工。只是当时对Kubernetes理解还不够深入，在设计nginx-kit时格局“太小了”，只实现了一个满足内部需求的”ingress controller”，而不是一个通用的、可扩展的ingress controller:(。

好了！言归正传，这篇文章是ingress的入门文章，将通过四个例子来说明一下ingress controller的实现之一： [ingress-nginx](https://github.com/kubernetes/ingress-nginx/)在不同服务暴露场景下的使用和配置方法。

## 一. 例子概述与环境准备

我们有四个例子，见下图中的a) ~ d)：

![img{512x368}](../../assets/aac1fd6dee510d2a.png)


- 例子a): 单ingress-nginx controller。通过ingress-svc1将内部服务svc1的http服务端口暴露到集群外，通过访问http://svc1.tonybai.com:30090即可访问svc1服务。
- 例子b)：单ingress-nginx controller。通过ingress-svc1将内部服务svc1的http服务端口暴露到集群外，通过访问http://svc1.tonybai.com:30090即可访问svc1服务；通过ingress-svc2将内部服务svc2的https服务端口暴露到集群外，通过访问http://svc2.tonybai.com:30090即可访问svc2服务。
- 例子c)：单ingress-nginx controller。除了暴露svc1和svc2之外，还暴露了集群内部的一个tcp(四层)服务：svc3，通过tcp连接svc3.tonybai.com:30070即可访问svc3服务。
- 例子d): 多ingress-nginx controllers。其中nginx-ingress-controller-ic1负责暴露svc1、svc2和svc3服务（访问方式如上面所描述的）；nginx-ingress-controller-ic2负责暴露svc4、svc5和svc6，其中svc4是一个http服务；svc5是https服务，svc6是一个tcp（四层)服务。

这里我们使用一个[Kubernetes 1.10.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.10.3)的集群来循序渐进地实践一下这四个例子。关于这四个例子的源码、chart包以及ingress controllers的yaml源文件在[这里](https://github.com/bigwhite/experiments/tree/master/ingress-controller-demo)可以下载到：

```
$tree -L 2 ingress-controller-demo
ingress-controller-demo
├── charts
│ ├── svc1
│ ├── svc2
│ ├── svc3
│ ├── svc4
│ ├── svc5
│ └── svc6
├── manifests
│ ├── ic-common.yaml
│ ├── ic1-mandatory.yaml
│ ├── ic1-service-nodeport.yaml
│ ├── ic2-mandatory.yaml
│ └── ic2-service-nodeport.yaml
└── src
├── svc1
├── svc2
├── svc3
├── svc4
├── svc5
└── svc6
```


其中:

- src下面存放着svc1~svc6的源码（包括Dockerfile）；
- manifests下面存放的是ingress controllers的yaml源文件；
- charts下面存放的是svc1~svc6的
[helm chart](https://helm.sh/)安装包源文件。

## 二. 创建第一个ingress-nginx controller

ingress controller有多种实现，其中应用较广的是kubernetes官方仓库中的[ingress-nginx](https://github.com/kubernetes/ingress-nginx/)。在bare metal上安装ingress-nginx controller十分方便，只需执行下面命令即可：

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/mandatory.yaml
```


不过，考虑到我后续在环境中会安装多个ingress-nginx controller，我们需要对mandatory.yaml中的内容做些调整：

-
首先明确多个ingress-nginx controller及其相关kubernetes object所在的namespace，默认为ingress-nginx，这里统一改为

**ingress-nginx-demo**，yaml描述文件中所有的object的namespace也都改为**ingress-nginx-demo**，clusterrole、clusterrolebinding对象不归属于任何namespace，因此无需修改； -
接下来，将多个ingress-nginx controller能共用的kubernetes object的描述数据从mandatory.yaml中提取出来，放入ic-common.yaml中，包括：namespace: ingress-nginx-demo、deployment: default-http-backend、service: default-http-backend、serviceaccount: nginx-ingress-serviceaccount、clusterrole: nginx-ingress-demo-clusterrole、role: nginx-ingress-role、rolebinding: nginx-ingress-role-nisa-binding以及clusterrolebinding: nginx-ingress-demo-clusterrole-nisa-binding;

-
将“缩水”后的mandatory.yaml改名为ic1-mandatory.yaml，并将其内容中的kubernetes object的name添加上

**“-ic1″**后缀。 - 在ic1-mandatory.yaml中nginx-ingress-controller的启动参数列表尾部添加“–ingress-class=ic1”:

```
// ic1-mandatory.yaml
... ...
spec:
serviceAccountName: nginx-ingress-serviceaccount
containers:
- name: nginx-ingress-controller-ic1
image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.15.0
args:
- /nginx-ingress-controller
- --default-backend-service=$(POD_NAMESPACE)/default-http-backend
- --configmap=$(POD_NAMESPACE)/nginx-configuration-ic1
- --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services-ic1
- --udp-services-configmap=$(POD_NAMESPACE)/udp-services-ic1
- --publish-service=$(POD_NAMESPACE)/ingress-nginx-ic1
- --annotations-prefix=nginx.ingress.kubernetes.io
- --ingress-class=ic1
... ...
```


- ic-common.yaml中的nginx-ingress-role中的resourceNames列表中需添加两项：”ingress-controller-leader-ic1″和”ingress-controller-leader-ic2″：

```
// ic-common.yaml
... ...
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: Role
metadata:
name: nginx-ingress-role
namespace: ingress-nginx-demo
rules:
- apiGroups:
- ""
resources:
- configmaps
- pods
- secrets
- namespaces
verbs:
- get
- apiGroups:
- ""
resources:
- configmaps
resourceNames:
# Defaults to "<election-id>-<ingress-class>"
# Here: "<ingress-controller-leader>-<nginx>"
# This has to be adapted if you change either parameter
# when launching the nginx-ingress-controller.
- "ingress-controller-leader-ic1"
- "ingress-controller-leader-ic2"
... ...
```


这两个resouceName分别给两个ingress-controller使用，当每个ingress-controller存在多副本(replicas > 1)时，多副本会通过ingress-controller-leader-icX这个configmap资源来进行leader election（选主)。以ingress-controller-ic1为例，当存在多副本时，ingress-controller-ic1的启动日志：

```
I0621 09:13:20.646426 7 stat_collector.go:34] changing prometheus collector from to default
I0621 09:13:20.648198 7 status.go:196] new leader elected: nginx-ingress-controller-ic1-7c9bc49cbb-kgjvz
I0621 09:13:20.752485 7 controller.go:177] ingress backend successfully reloaded...
```


不过，虽然存在leader，但业务流量却是负载分担的。

- 为ingress-nginx controller pod创建nodeport类型service

如果只是部署了ingress controller，那么外部依然无法连上ingress controller，因为ingress controller自身还没有对应的service将自己暴露到集群外部。官方文档推荐使用NodePort方式，于是我们创建了ic1-service-nodeport.yaml，让流入host:30090的流量进入ingress controller service。

总结一下ingress-controller-ic1这个ingress controller的完整创建步骤：

```
kubectl apply -f ic-common.yaml
kubectl apply -f ic1-service-nodeport.yaml
kubectl apply -f ic1-mandatory.yaml
```


## 三. 创建例子a)

svc1是一个在容器8080端口提供http服务的服务程序。在例子a)中，我们在k8s集群中创建svc1，并创建ic1-svc1 ingress将svc1暴露在集群外面，外部请求通过svc1.tonybai.com:30090可以访问到svc1。而做到这一点，我们仅需要使用helm install一下svc1这个chart：

```
# helm install --name ic1-svc1 ./svc1
NAME: ic1-svc1
LAST DEPLOYED: Thu Jun 21 20:39:25 2018
NAMESPACE: default
STATUS: DEPLOYED
RESOURCES:
==> v1/Service
NAME TYPE CLUSTER-IP EXTERNAL-IP PORT(S) AGE
ic1-svc1 ClusterIP 10.103.210.182 <none> 80/TCP 0s
==> v1beta2/Deployment
NAME DESIRED CURRENT UP-TO-DATE AVAILABLE AGE
ic1-svc1 1 0 0 0 0s
==> v1beta1/Ingress
NAME HOSTS ADDRESS PORTS AGE
ic1-svc1 svc1.tonybai.com 80 0s
==> v1/Pod(related)
NAME READY STATUS RESTARTS AGE
ic1-svc1-5ff84d7bff-5j7tb 0/1 ContainerCreating 0 0s
NOTES:
1. Get the application URL by running these commands:
http://svc1.tonybai.com/
```


svc1服务以及对应的ic1-svc1 ingress创建后，我们来测试一下：

```
# curl svc1.tonybai.com:30090
Hello, I am svc1 for ingress-controller demo!
```


结果符合预期。而这一切实现的关键在于ingress-controller-demo/charts/svc1/values.yaml:

```
... ...
ingress:
enabled: true
annotations:
# kubernetes.io/ingress.class: nginx
# kubernetes.io/tls-acme: "true"
kubernetes.io/ingress.class: ic1
path: /
hosts:
- svc1.tonybai.com
... ...
```


ingress的enabled改为true，helm才会创建svc1对应的ingress。annotations中的**kubernetes.io/ingress.class: ic1**很关键，设定ingress的这个annotation，可以使得该ingress归属于我们上面创建的nginx-ingress-controller-ic1 ingress controller，而其他ingress controller会忽略这个ingress。

我们再来看看 ingress-controller-ic1的后台日志，当添加svc1时，日志输出：

```
I0621 12:39:25.406331 7 event.go:218] Event(v1.ObjectReference{Kind:"Ingress", Namespace:"default", Name:"ic1-svc1", UID:"2176416f-7550-11e8-a0e8-00163e0cd764", APIVersion:"extensions", ResourceVersion:"1877656", FieldPath:""}): type: 'Normal' reason: 'CREATE' Ingress default/ic1-svc1
I0621 12:39:25.517915 7 controller.go:177] ingress backend successfully reloaded...
W0621 12:39:28.739708 7 controller.go:773] service default/ic1-svc1 does not have any active endpoints
I0621 12:39:34.262824 7 controller.go:168] backend reload required
I0621 12:39:34.371479 7 controller.go:177] ingress backend successfully reloaded...
```


nginx-ingress-controller-ic1会监听到service变化，并reload nginx。

我们可以通过下面命令查看nginx-ingress-controller-ic1内部的nginx的配置文件内容：

```
# kubectl exec nginx-ingress-controller-ic1-7c9bc49cbb-kgjvz -n ingress-nginx-demo -- cat /etc/nginx/nginx.conf
```


我们可以看到有关svc1的相关内容如下：

```
upstream default-ic1-svc1-http {
least_conn;
keepalive 32;
server 192.168.31.9:8080 max_fails=0 fail_timeout=0;
}
## start server svc1.tonybai.com
server {
server_name svc1.tonybai.com ;
listen 80;
listen [::]:80;
set $proxy_upstream_name "-";
location / {
... ...
set $proxy_upstream_name "default-ic1-svc1-http";
set $namespace "default";
set $ingress_name "ic1-svc1";
set $service_name "ic1-svc1";
... ...
proxy_pass http://default-ic1-svc1-http;
proxy_redirect off;
}
}
## end server svc1.tonybai.com
```


可一看出外部到svc1.tonybai.com:30090的流量被转到service ingress-nginx-ic1:80上，进而到达nginx pod的targetPort(80)上。

## 四. 创建例子b)

有了例子a)作为基础，理解接下来的例子就相对简单了。例子b)与a)最大的不同是svc2是一个https服务。外部通过http协议访问：svc2.tonybai.com:30090后，nginx-ingress-controller-ic1内部的nginx需要以[https](https://tonybai.com/tag/https)的方式去访问svc2。ingress-nginx ingress controller支持这种情况，仅需要在svcb的ingress annotations加上下面这个annotation：**nginx.ingress.kubernetes.io/secure-backends: “true”**：

```
// ingress-controller-demo/charts/svc2/values.yaml
... ...
ingress:
enabled: true
annotations:
# kubernetes.io/ingress.class: nginx
# kubernetes.io/tls-acme: "true"
nginx.ingress.kubernetes.io/secure-backends: "true"
kubernetes.io/ingress.class: ic1
path: /
hosts:
- svc2.tonybai.com
... ...
```


和例子a)一样，使用helm安装svc2这个chart后，svc2这个服务就暴露出来了：

```
# helm install --name ic1-svc2 ./svc2
# curl http://svc2.tonybai.com:30090
Hello, I am svc2 for ingress-controller demo!
```


## 五. 创建例子c)

svc3与前面两个服务均不同，因为它直接暴露的是四层的tcp服务。kubernetes ingress无法直接支持四层的服务端口暴露，我们需要[在ingress controller上“动手脚”](https://kubernetes.github.io/ingress-nginx/user-guide/exposing-tcp-udp-services/)。

首先，四层的暴露的端口不能与之前的七层端口30090重叠(因为不是通过ingress来暴露svc3服务的)，我们需要一个新端口：30070，我们需要在ic1-service-nodeport.yaml中增加一组nodeport：

```
//ingress-controller-demo/manifests/ic1-service-nodeport.yaml
apiVersion: v1
kind: Service
metadata:
name: ingress-nginx-ic1
namespace: ingress-nginx-demo
spec:
type: NodePort
ports:
- name: http
port: 80
targetPort: 80
nodePort: 30090
protocol: TCP
- name: tcp
port: 30070
targetPort: 30070
nodePort: 30070
protocol: TCP
selector:
app: ingress-nginx-ic1
```


注意这里两组nodeport中的port不能一样，否则kubernetes会用下面的一组覆盖上面的那组。这里我们暴露30070这个nodeport，service的集群内port也是30070，后面的endpoint中的容器（即nginx-ingress-controller-ic1 pod）监听的也是30070。

接下来，要让nginx-ingress-controller-ic1 pod也监听30070，我们没法用ingress实现，但是ingress-nginx ingress controller支持通过一个名为：**tcp-services-ic1**的configmap来配置：

```
//ingress-controller-demo/manifests/ic1-mandatory.yaml
.... ...
spec:
serviceAccountName: nginx-ingress-serviceaccount
containers:
- name: nginx-ingress-controller-ic1
image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.15.0
args:
- /nginx-ingress-controller
- --default-backend-service=$(POD_NAMESPACE)/default-http-backend
- --configmap=$(POD_NAMESPACE)/nginx-configuration-ic1
- --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services-ic1
- --udp-services-configmap=$(POD_NAMESPACE)/udp-services-ic1
- --publish-service=$(POD_NAMESPACE)/ingress-nginx-ic1
- --annotations-prefix=nginx.ingress.kubernetes.io
... ...
```


在ic1-mandatory.yaml中，我们这样更新tcp-services-ic1 configmap的配置：

```
kind: ConfigMap
apiVersion: v1
metadata:
name: tcp-services-ic1
namespace: ingress-nginx-demo
data:
30070: "default/ic1-svc3:8080"
```


大家可以看到，在configmap的data中，我们用了一个key:value的格式行，其中key就是nginx要暴露的端口：30070，value则为

```
<namespace/service name>:<service port>
```


格式的值，这里我们使用default名字空间下的ic1-svc3服务，服务端口8080。

重新apply ic1-mandatory.yaml和ic1-service-nodeport.yaml后，我们测试一下svc3服务：

```
# telnet svc3.tonybai.com 30070
Trying 127.0.0.1...
Connected to svc3.tonybai.com.
Escape character is '^]'.
hello
hello
world
world
```


svc3是一个echo服务，我们看到svc3 echo了我们输入的内容。

在nginx内部，30070是这样被暴露的：

```
stream {
log_format log_stream [$time_local] $protocol $status $bytes_sent $bytes_received $session_time;
access_log /var/log/nginx/access.log log_stream;
error_log /var/log/nginx/error.log;
# TCP services
upstream tcp-30070-default-ic1-svc3-8080 {
server 192.168.28.13:8080;
}
server {
listen 30070;
listen [::]:30070;
proxy_timeout 600s;
proxy_pass tcp-30070-default-ic1-svc3-8080;
}
# UDP services
}
```


## 六. 创建例子d)

在例子d)对应的图示中，我们建立了另外一个ingress-nginx ingress controller: nginx-ingress-controller-ic2，与nginx-ingress-controller-ic1 不同的是， nginx-ingress-controller-ic2的启动参数中含：

```
- --ingress-class=ic2
```


用以区分ic1。ic2-mandatory.yaml和ic1-mandatory.yaml相比，就是将“rc1”字样整体替换为”ic2″即可。除此之外，有了ic1-service-nodeport.yaml的基础，ic2-service-nodeport.yaml内容也是“雷同”的。建立 nginx-ingress-controller-ic2步骤如下：

```
# kubectl apply -f ic2-service-nodeport.yaml
# kubectl apply -f ic2-mandatory.yaml
```


归属于nginx-ingress-controller-ic2的三个服务svc4、svc5和svc6等价于nginx-ingress-controller-ic1的svc1、svc2和svc3，这里就不赘述了。

```
# curl svc4.tonybai.com:30091
Hello, I am svc4 for ingress-controller demo!
# curl svc5.tonybai.com:30091
Hello, I am svc5 for ingress-controller demo!
# telnet svc6.tonybai.com 30071
Trying 127.0.0.1...
Connected to svc6.tonybai.com.
Escape character is '^]'.
hello
hello
tony
tony
```


如果想使得ingress-nginx controller高可用，只需将其pod副本数量调大即可。

[51短信平台](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论