---
title: 为Kubernetes集群中服务部署Nginx入口服务
url: https://tonybai.com/2016/11/22/deploy-nginx-service-for-the-services-in-kubernetes-cluster/
published: '2016-11-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 为Kubernetes集群中服务部署Nginx入口服务

这段日子，一直在搞与[Kubernetes](http://tonybai.com/tag/kubernetes)有关的东东：像什么[Kubernetes集群搭建](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)、[DNS插件安装和配置](http://tonybai.com/2016/10/23/install-dns-addon-for-k8s/)、[集成Ceph RBD持久卷](http://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd/)、[Private Registry镜像库访问](http://tonybai.com/2016/11/16/how-to-pull-images-from-private-registry-on-kubernetes-cluster/)等，这些都缘于正在开发的一个类[PaaS](https://en.wikipedia.org/wiki/Platform_as_a_service)小平台的需要：“平台虽小，五脏俱全”。整个平台由Kubernetes集群承载，对于K8s集群内部的Service来说，目前还欠缺一个服务入口。之前的《[Kubernetes集群中的Nginx配置热更新方案](http://tonybai.com/2016/11/17/nginx-config-hot-reloading-approach-for-kubernetes-cluster/)》一文实际上就是入口方案设计的一个前奏，而本文则是说明一下Nginx入口服务部署设计和实施过程中遇到的一些坑。

#### 一、Nginx入口方案简述

[Nginx](http://tonybai.com/tag/nginx)作为集群入口服务，从功能上说，一般都是充当反向代理和负载均衡的角色。在我们这里它更多是用于反向代理，因为负载均衡的事情“移交”给了K8s去实现了。k8s通过ClusterIP- 一种VIP机制，默认[基于iptables的负载分担](http://kubernetes.io/docs/user-guide/debugging-services/#is-the-kube-proxy-working)实现服务请求的负载均衡（如iptable nat table的规则：-m statistic –mode random –probability 0.33332999982），查看iptables nat链的rules，可以看到如下样例：

```
# iptables -t nat -nL
... ...
Chain KUBE-SVC-UQG6736T32JE3S7H (2 references)
target prot opt source destination
KUBE-SEP-Z7UQLD332S673VAF all -- 0.0.0.0/0 0.0.0.0/0 /* default/nginx-kit: */ statistic mode random probability 0.50000000000
KUBE-SEP-TWOIACCAJCPK3HWO all -- 0.0.0.0/0 0.0.0.0/0 /* default/nginx-kit: */
... ..
```


接下来，我们简单说说我们的Nginx入口方案。事先声明：这绝对不是一个理想的方案，因为它还有诸多缺陷，只是在目前平台需求上下文和资源的约束前提下，它可以作为我们的一个可用的过渡方案，方案示意图如下：

![img{512x368}](../../assets/89d7e083b455a737.png)


- Nginx以Kubernetes service的形式运行于K8s cluster内部，并限制只能被K8s调度到带有label: role=entry的Node上；
- 最外层，通过DNS域名的轮询机制，实现用户请求在Node这一层上的“负载均衡”；
- 访问某个NodeIP:NodePort的请求，被转发到Nginx ClusterIP: Port，并通过iptables nat的负载机制，分发到Nginx service的多个real endpoints上；
- 位于real endpoint上的Nginx程序处理用户请求，并根据配置，将请求proxy_pass到后端服务的ClusterIP:Port上，并最终由k8s实现将请求均衡分发到后端服务的endpoint。

#### 二、Nginx入口服务部署

部署前，我们先来给运行Nginx Pod的Node打label：

```
# kubectl label node/10.47.136.60 role=entry
node "10.47.136.60" labeled
# kubectl label node/10.47.136.60 role=entry
node "10.47.136.60" labeled
# kubectl get nodes --show-labels
NAME STATUS AGE LABELS
10.46.181.146 Ready 39d beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=10.46.181.146,role=entry,zone=ceph
10.47.136.60 Ready 39d beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=10.47.136.60,role=entry,zone=ceph
```


在[Nginx配置热加载方案](http://tonybai.com/2016/11/17/nginx-config-hot-reloading-approach-for-kubernetes-cluster/)一文中，我们提到一个nginx pod中包含三个Container：nginx、nginx-conf-generator和init container，Nginx service的yaml示例如下：

```
//nginx-kit.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: nginx-kit
spec:
replicas: 2
template:
metadata:
labels:
run: nginx-kit
annotations:
pod.beta.kubernetes.io/init-containers: '[
{
"name": "nginx-kit-init-container",
"image": "registry.cn-beijing.aliyuncs.com/xxxx/nginx-conf-generator",
"imagePullPolicy": "IfNotPresent",
"command": ["/root/conf-generator/nginx-conf-gen", "-mode", "gen-once"],
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
- name: nginx-conf-generator
volumeMounts:
- mountPath: /etc/nginx/conf.d
name: conf-volume
image: registry.cn-beijing.aliyuncs.com/xxxx/nginx-conf-generator:latest
imagePullPolicy: IfNotPresent
- name: xxxx-nginx
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
nodeSelector:
role: entry
---
apiVersion: v1
kind: Service
metadata:
name: nginx-kit
labels:
run: nginx-kit
spec:
type: NodePort
ports:
- port: 80
nodePort: 28888
protocol: TCP
selector:
run: nginx-kit
```


关于这个yaml，有几点我们是必须要说说的：

##### 1、关于init container

通过上述yaml文件内容，我们可以看到init container和nginx-conf-generator container都是基于同一镜像创建的，只是工作mode不同罢了。在deployment描述文件中，init container的描述需要放在deployment.spec.template.metadata下面，而不是deployment的metadata下面。如果按照后者编写，那么init container将不会被创建和启动，nginx container启动后也就会提示：找不到”default.conf”。

另外，虽然源自同一个image，但init container启动时却提示在$PATH里找不到名为”-mode”的可执行程序，显然init container中的ENTRYPOINT并不起作用，nginx-conf-generator的Dockerfile节选如下：

```
//Dockerfile
From ubuntu:14.04
... ...
ENTRYPOINT ["/root/conf-generator/nginx-conf-gen"]
```


为此我们在init container的”command”命令参数中增加了可执行程序全路径以供container执行：

```
"command" : ["/root/conf-generator/nginx-conf-gen", "-mode", "gen-once"],
```


最后，通过上面yaml文件创建nginx-kit服务依旧要用kubectl apply，而不是kubectl create，否则init container不会被理会。

##### 2、关于nginx conf模板

由于种种原因，当前我们是通过server host的location path来映射后端cluster中的不同Service的，nginx default.conf模板如下：

```
server {
listen 80;
#server_name opp.neusoft.com;
{{range .}}
location {{.Path}} {
proxy_pass http://{{.ClusterIP}}:{{.Port}}/;
proxy_redirect off;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
{{end}}
#error_page 404 /404.html;
# redirect server error pages to the static page /50x.html
#
error_page 500 502 503 504 /50x.html;
location = /50x.html {
root /usr/share/nginx/html;
}
}
```


这里要注意的是proxy_pass directive后面值的写法，如果你选择这样写：

```
proxy_pass http://{{.ClusterIP}}:{{.Port}};
```


那么当访问某个路径时，比如：localhost/volume/api/v1/pools时，nginx后端的Service收到的url访问路径将是：/volume/api/v1/pools，volume这个location path并不能被去除，后端的Service在做路由匹配时基本都是会出错的。fix的方法是赋予proxy_pass directive下面这样的值：

```
proxy_pass http://{{.ClusterIP}}:{{.Port}}/;
```


没错，在最后加上一个”/”，这样nginx所反向代理的Service将会收到/api/v1/pools这样的访问URl路径。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论