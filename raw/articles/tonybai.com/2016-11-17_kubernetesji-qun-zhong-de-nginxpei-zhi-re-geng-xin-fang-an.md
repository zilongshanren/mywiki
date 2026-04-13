---
title: Kubernetes集群中的Nginx配置热更新方案
url: https://tonybai.com/2016/11/17/nginx-config-hot-reloading-approach-for-kubernetes-cluster/
published: '2016-11-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes集群中的Nginx配置热更新方案

[Nginx](https://nginx.org/)已经是互联网IT业界一个无敌的存在，作为反向代理、负载均衡、Web服务器等多种角色的扮演者，Nginx在全球各个互联网公司落地、开花和结果，Ngnix已经成为了支撑全球互联网应用的一个不可获取的组成部分。

在我们的平台中，Nginx同样被拿来作为服务接入的最前端的反向代理，并且我们的Nginx也是作为一个Service跑在我们的[Kubernetes集群](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)中的。Ngnix背后的服务众多，服务的生生死死都要在Nginx上这些服务路由的配置中有所体现，这就要求部署在Kubernetes集群中的Nginx需要有一个合理的配置热更新方案。

Nginx自身是支持配置热更新的，通过nginx -s reload命令可以实现这一点：

```
# sudo nginx -s reload
# sudo tail -100f /var/log/nginx/error.log
2016/11/18 08:21:03 [notice] 31516#31516: signal process started
```


这也是诸多nginx热更新方案的基础。

随着Docker容器以及容器集群/云的出现，Nginx也被Dockerize了，Docker中Nginx的配置热更新方案在[Jason Wilder](http://jasonwilder.com/)的[这篇文章](http://jasonwilder.com/blog/2014/03/25/automated-nginx-reverse-proxy-for-docker/)中有体现，在该方案中，你可以直接使用Jason Wilder开源的[Nginx-proxy](https://github.com/jwilder/nginx-proxy)实现容器中Nginx的配置的热更新。但这个方案并不能直接适用于Kubernetes，而且[作者也并没有Plan support k8s](https://github.com/jwilder/nginx-proxy/issues/336)。

在Kubernetes集群中部署的Nginx，我其实也找到了一个配置热更新的方案，这是普元的一份技术资料《[微服务动态路由实现：OpenResty与kubernetes](http://www.dockerinfo.net/1700.html)》中提供的，这个方案通过[OpenResty](https://openresty.org)与K8s的结合实现了配置热更新。由于我对OpenResty并不熟悉，并且我个人更希望通过Kubernetes自身的一些Feature来实现这个方案，于是我开始了我自己的探索。

#### 一、需求场景和方案原理

我们要实现的就是：当Kubernetes集群中的Service发生变化时，比如新创建一个Service或删除了一个Service，这些Service在Nginx反向代理中的路由配置需要同步更新并生效。因此，这个过程的场景大致如下：

- 管理员通过命令或程序通过API操作K8s集群创建或删除Service；
- 监听API Server Event的某个程序获取该Event，并从API Server读取最新Service数据，重新生成/etc/nginx/conf.d/default.conf；
- /etc/nginx/conf.d/default.conf文件的变动触发文件变更事件，监听该事件的脚本调用“nginx -s reload”命令实现Nginx的配置热更新。

针对这一需求场景，我这里给出一个实现方案，先上图：

![img{512x368}](../../assets/a55ffff195c0cc22.png)


简答说明一下：

- Nginx作为一个Service部署在Kubernetes集群中，可以有多个Pod副本；
- 以一个nginx pod为例，该Pod中包含三个Container，分别是
[init container](http://kubernetes.io/docs/user-guide/production-pods/)、nginx container和config-nginx-generator container； - 三个Container共同挂载且共享一个Pod volume，emptyDir类型即可，无需
[持久化的存储卷](http://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd/)，三个Container的挂载路径均为/etc/nginx/conf.d； - Pod启动时，init container首先启动并访问API Server，获取Service列表，按照一定条件过滤后(比如通过label的key和Value值)，初始创建/etc/nginx/conf.d/default.conf。创建成功后，Container退出；
- nginx container启动，加载配置，开始提供反向代理服务，并通过inotify工具监视/etc/nginx/conf.d/default.conf文件状态变化，一般变化，就执行nginx -s reload热加载最新配置。
- config-nginx-generator container同时也启动起来，监听API Server的service变更Event，一旦有Event出现，就重新读取API Server中的Service list，并重新生成一份新的default.conf，覆盖old版本 default.conf。

#### 二、环境

由于[Kubernetes](http://tonybai.com/tag/kubernetes)和[Docker](http://tonybai.com/tag/docker)都在Active Develop的过程中，两个项目的变动都很快，因此，特定的Feature（比如k8s的init container）、操作和说明在某些版本是好用的，但对另外一些版本却是不灵光的。这里先把环境确定清楚，避免误导。

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


#### 三、实现

##### 1、nginx image的创建

nginx image实现了两个功能，一个自然是nginx自身了，另外一个就是监听/etc/nginx/conf.d/default.conf文件的变化，并适时调用nginx -s reload更新nginx配置。在kubernetes的源码目录kubernetes/examples下有一个例子：[https-nginx](https://github.com/kubernetes/kubernetes/tree/master/examples/https-nginx)，这里面已经为我们实现了一个基于[auto-reload-nginx.sh](https://github.com/kubernetes/kubernetes/blob/master/examples/https-nginx/auto-reload-nginx.sh)的Nginx image Dockerfile，我们稍作改造就可以直接使用了：

```
//Dockerfile
FROM nginx
MAINTAINER Tony Bai <bigwhite.cn@aliyun.com>
COPY auto-reload-nginx.sh /home/auto-reload-nginx.sh
RUN chmod +x /home/auto-reload-nginx.sh
# install inotify
RUN apt-get update && apt-get install -y inotify-tools
```


基于该Dockefile构建image：

```
# docker build -t xxxx/nginx
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
xxxx/nginx latest a1503b1c2b70 42 seconds ago 191.9 MB
```


官方nginx image基于debian jessie版本构建，apt-get update & install时需要耐心等待一下。

打标签并推送到我们的阿里云[私有镜像库](http://tonybai.com/2016/11/16/how-to-pull-images-from-private-registry-on-kubernetes-cluster/)：

```
# docker tag a1503b1c2b70 registry.cn-hangzhou.aliyuncs.com/xxxx/nginx
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
xxxx/nginx latest a1503b1c2b70 12 minutes ago 191.9 MB
registry.cn-hangzhou.aliyuncs.com/xxxx/nginx latest a1503b1c2b70 12 minutes ago 191.9 MB
# docker push registry.cn-hangzhou.aliyuncs.com/xxxx/nginx
```


##### 2、编写Pod yaml

由于init container和config-nginx-generator container在真实场景中都是要与Kubernetes的API Server交互，并生成/etc/nginx/conf.d/default.conf，这需要一个实现过程，在这里我们暂不给出两个Container的具体Dockerfile以及实现功能的实际程序，而是用两个通用docker image，并通过“手动”方式实现它们各自的功能。因此，我们在这一节中就可以给出Nginx Pod的yaml描述文件了：

```
//nginx-reload-on-k8s.yaml
apiVersion: v1
kind: Pod
metadata:
name: nginx-reload-on-k8s
annotations:
pod.beta.kubernetes.io/init-containers: '[
{
"name": "nginx-reload-on-k8s-init-1",
"image": "busybox",
"command": ["wget", "-O", "/etc/nginx/conf.d/index1.html", "http://www.baidu.com"],
"volumeMounts": [
{
"name": "conf-volume",
"mountPath": "/etc/nginx/conf.d"
}
]
},
{
"name": "nginx-reload-on-k8s-init-2",
"image": "busybox",
"command": ["wget", "-O", "/etc/nginx/conf.d/index2.html", "http://dict.cn"],
"volumeMounts": [
{
"name": "conf-volume",
"mountPath": "/etc/nginx/conf.d"
}
]
}
]'
spec:
containers:
- name: nginx-config-generator
volumeMounts:
- mountPath: /etc/nginx/conf.d
name: conf-volume
image: registry.cn-hangzhou.aliyuncs.com/xxxx/test:latest
imagePullPolicy: IfNotPresent
command:
- "tail"
- "-f"
- "/var/log/bootstrap.log"
- name: nginx-origin
volumeMounts:
- mountPath: /etc/nginx/conf.d
name: conf-volume
image: registry.cn-hangzhou.aliyuncs.com/xxxx/nginx:latest
imagePullPolicy: IfNotPresent
command: ["/home/auto-reload-nginx.sh"]
ports:
- containerPort: 80
volumes:
- name: conf-volume
emptyDir: {}
```


Yaml中，我们创建了两个init container，分别用于从baidu.com和dict.cn抓取主页，并存储于/etc/nginx/conf.d的下面备用。nginx-config-generator我们使用image xxxx/test，这就是一个基于ubuntu且安装了诸多网络工具的镜像，用于做目标镜像调试的；nginx container用的就是上面push到私有镜像仓库的那个镜像，command则是执行/home/auto-reload-nginx.sh这个脚本，从而启动nginx和通过inotify监控/etc/nginx/conf.d/default.conf文件。

我们来创建这个Pod(注意：只有用kubectl apply命令时，init container才会被创建和执行，如果用kubectl create -f ，那么将忽略init container)：

```
# kubectl apply -f nginx-reload-on-k8s.yaml
pod "nginx-reload-on-k8s" created
# kubectl get pod
NAME READY STATUS RESTARTS AGE
nginx-reload-on-k8s 2/2 Running 0 41s
```


通过describe pod/nginx-reload-on-k8s，我们能看到一些Container创建的详细信息：

```
# kubectl describe pod/nginx-reload-on-k8s
Name: nginx-reload-on-k8s
Namespace: default
Node: 10.46.181.146/10.46.181.146
Start Time: Thu, 17 Nov 2016 21:39:55 +0800
Labels: <none>
Status: Running
IP: 172.16.57.9
... ...
Events:
FirstSeen LastSeen Count From SubobjectPath Type Reason Message
--------- -------- ----- ---- ------------- -------- ------ -------
57s 57s 1 {default-scheduler } Normal Scheduled Successfully assigned nginx-reload-on-k8s to 10.46.181.146
39s 39s 1 {kubelet 10.46.181.146} spec.initContainers{nginx-reload-on-k8s-init-1} Normal Created Created container with docker id 0e21afb58eee
39s 39s 1 {kubelet 10.46.181.146} spec.initContainers{nginx-reload-on-k8s-init-1} Normal Started Started container with docker id 0e21afb58eee
56s 38s 2 {kubelet 10.46.181.146} spec.initContainers{nginx-reload-on-k8s-init-1} Normal Pulling pulling image "busybox"
39s 26s 2 {kubelet 10.46.181.146} spec.initContainers{nginx-reload-on-k8s-init-1} Normal Pulled Successfully pulled image "busybox"
26s 26s 1 {kubelet 10.46.181.146} spec.initContainers{nginx-reload-on-k8s-init-2} Normal Created Created container with docker id 85632ff73ea8
26s 26s 1 {kubelet 10.46.181.146} spec.initContainers{nginx-reload-on-k8s-init-2} Normal Started Started container with docker id 85632ff73ea8
25s 25s 1 {kubelet 10.46.181.146} spec.containers{nginx-config-generator} Normal Pulled Container image "registry.cn-hangzhou.aliyuncs.com/xxxx/test:latest" already present on machine
25s 25s 1 {kubelet 10.46.181.146} spec.containers{nginx-config-generator} Normal Created Created container with docker id 1ce8c6d8a8af
25s 25s 1 {kubelet 10.46.181.146} spec.containers{nginx-config-generator} Normal Started Started container with docker id 1ce8c6d8a8af
25s 25s 1 {kubelet 10.46.181.146} spec.containers{nginx-origin} Normal Pulled Container image "registry.cn-hangzhou.aliyuncs.com/xxxx/nginx:latest" already present on machine
25s 25s 1 {kubelet 10.46.181.146} spec.containers{nginx-origin} Normal Created Created container with docker id 0c692ec28acd
25s 25s 1 {kubelet 10.46.181.146} spec.containers{nginx-origin} Normal Started Started container with docker id 0c692ec28acd
... ...
```


可以看到四个container依次被pull and create。

#### 四、测试

现在我们就来测试一下nginx的reload。

之前的两个init container分别在/etc/nginx/conf.d下创建了index1.html和index2.html，我们就用这两个文件分别作为配置变更前和变更后的首页。

注意：这时我们还没有/etc/nginx/conf.d/default.conf文件，我们在Pod内访问localhost:80将会得到失败结果：

```
# curl localhost:80
curl: (7) Failed to connect to localhost port 80: Connection refused
```


我们进入nginx-config-generator，创建/etc/nginx/conf.d/default.conf文件，与此同时，通过docker logs -f 监控nginx-origin容器的日志：

```
//default.conf
server {
listen 80;
server_name localhost;
#charset koi8-r;
#access_log /var/log/nginx/log/host.access.log main;
location / {
root /etc/nginx/conf.d;
index index1.html index1.htm;
}
#error_page 404 /404.html;
# redirect server error pages to the static page /50x.html
#
error_page 500 502 503 504 /50x.html;
location = /50x.html {
root /usr/share/nginx/html;
}
}
```


我们把/etc/nginx/conf.d/index1.html作为服务站点的首页了。文件创建完毕后，我们同时就可以从nginx-origin容器的日志能看到如下内容：

```
At 14:07 on 17/11/16, config file update detected.
2016/11/17 14:07:25 [notice] 20#20: signal process started
```


我们再从Pod中访问localhost:80（注意：Pod中的多个container共享network namespace，通过localhost就可以进行互访）：

```
root@nginx-reload-on-k8s:/etc/nginx# curl localhost:80
<!DOCTYPE html>
<!--STATUS OK--><html> <head><meta http-equiv=content-type content=text/html;charset=utf-8><meta http-equiv=X-UA-Compatible content=IE=Edge><meta content=always name=referrer><link rel=stylesheet type=text/css href=http://s1.bdstatic.com/r/www/cache/bdorz/baidu.min.css><title>百度一下，你就知道</title></head> .... </html>
```


我们顺利得到index1.html的内容，这说明配置实时生效了。

我们再来“触发”一次配置变更。我们将default.conf中的：

```
location / {
root /etc/nginx/conf.d;
index index1.html index1.htm;
}
```


改为：

```
location / {
root /etc/nginx/conf.d;
index index2.html index2.htm;
}
```


保存！

从nginx-origin容器日志可以看到如下输出：

```
At 14:17 on 17/11/16, config file update detected.
2016/11/17 14:17:46 [notice] 32#32: signal process started
```


在Pod中再次访问站点首页：

```
# curl localhost:80
<!DOCTYPE HTML>
<html>
<head>
<meta name="renderer" content="webkit"/>
<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>海词词典_在线词典_在线翻译_海量正版权威词典官方网站</title>
... ...
```


可以看到配置更新成功，首页换成了dict.cn的首页。

#### 五、测试

通过上述这些“手动”的触发和测试，可以看出这个方案是可行的。并且我们可以看出，这个方案是有一些好处的：

- 不需要依赖外部持久化存储卷；
- 通过k8s api server获取当前所有 service列表，通过service label来过滤，无需依赖额外的redis server或etcd服务；

剩下的就是具体init container以及config-generator的实现了。这个留给我以及大家后续去完成^_^。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

好文

很精致有用的小case，后续会有博客更新？

博客一直在更啊。但针对这个nginx配置热更新方案可能不会有后续的进一步更新了。

好文！没想到我软还有这样高手，希望有机会结识。

过奖，欢迎沟通交流。

好文，想求与Kubernetes API Server通信a获取service列表的dockerfile

这个是内部系统使用的，并不开源。但是实现逻辑也并不难，可以试试。另外也可以直接使用kubernetes提供的现成的ingress-nginx :https://github.com/kubernetes/ingress-nginx/。当初我并不知道ingress-nginx的存在，于是自己才搭了这个类似的、但没有那么通用的ingress-nginx。

你好，我想做一款定制的ingress ,因为有一些生产环境的应用每个nginx的conf文件配置都不同,我查看nginx做的容器，里面包装了nginx-ingress-controller,reload 一整个大的nginx.conf，不知道您觉得这个方法可行吗

我了理解你就是要部署一个ingress-nginx controller来控制所有nginx规则吧？nginx reload还是很快的。但如果应用特别多，nginx.conf中的规则过多（究竟多少算多？），究竟结果如何，我也没测试过。不过你的想法是可行的。实在不行也可以建立多个ingress-nginx controller，每个控制一部分应用。