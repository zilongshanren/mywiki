---
title: Kubernetes集群DNS插件安装
url: https://tonybai.com/2016/10/23/install-dns-addon-for-k8s/
published: '2016-10-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Kubernetes集群DNS插件安装

在[上一篇关于Kubernetes集群安装的文章](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)中，我们建立一个最小可用的k8s集群，不过k8s与[1.12版本后的内置了集群管理的Docker](http://tonybai.com/2016/10/11/some-problems-under-swarm-mode-in-docker-1-12/)不同，k8s是一组松耦合的组件组合而成对外提供服务的。除了核心组件，其他组件是以Add-on形式提供的，比如[集群内kube-DNS](https://github.com/kubernetes/kubernetes/blob/master/build/kube-dns/README.md)、[K8s Dashboard](https://github.com/kubernetes/dashboard/)等。kube-dns是k8s的重要插件，用于完成集群内部service的注册和发现。随着k8s安装和管理体验的进一步完善，DNS插件势必将成为k8s默认安装的一部分。本篇将在[《一篇文章带你了解Kubernetes安装》](http://tonybai.com/2016/10/18/learn-how-to-install-kubernetes-on-ubuntu/)一文的基础上，进一步探讨DNS组件的安装”套路”^_^以及问题的troubleshooting。

#### 一、安装前提和原理

上文说过，K8s的安装根据Provider的不同而不同，我们这里是基于provider=ubuntu为前提的，使用的安装脚本是[浙大团队](http://www.sel.zju.edu.cn/)维护的那套。因此如果你的provider是其他选项，那么这篇文章里所讲述的内容可能不适用。但了解provider=ubuntu下的DNS组件的安装原理，总体上对其他安装方式也是有一定帮助的。

在部署机k8s安装工作目录的cluster/ubuntu下面，除了安装核心组件所用的download-release.sh、util.sh外，我们看到了另外一个脚本deployAddons.sh，这个脚本内容不多，结构也很清晰，大致的执行步骤就是：

```
init
deploy_dns
deploy_dashboard
```


可以看出，这个脚本就是用来部署k8s的两个常用插件：dns和dashboard的。进一步分析，发现deployAddons.sh的执行也是基于./cluster/ubuntu/config-default.sh中的配置，相关的几个配置包括：

```
# Optional: Install cluster DNS.
ENABLE_CLUSTER_DNS="${KUBE_ENABLE_CLUSTER_DNS:-true}"
# DNS_SERVER_IP must be a IP in SERVICE_CLUSTER_IP_RANGE
DNS_SERVER_IP=${DNS_SERVER_IP:-"192.168.3.10"}
DNS_DOMAIN=${DNS_DOMAIN:-"cluster.local"}
DNS_REPLICAS=${DNS_REPLICAS:-1}
```


deployAddons.sh首先会根据上述配置生成skydns-rc.yaml和skydns-svc.yaml两个k8s描述文件，再通过kubectl create创建dns service。

#### 二、安装k8s DNS

##### 1、试装

为了让deployAddons.sh脚本执行时只进行DNS组件安装，需要先设置一下环境变量：

```
export KUBE_ENABLE_CLUSTER_UI=false
```


执行安装脚本：

```
# KUBERNETES_PROVIDER=ubuntu ./deployAddons.sh
Creating kube-system namespace...
The namespace 'kube-system' is successfully created.
Deploying DNS on Kubernetes
replicationcontroller "kube-dns-v17.1" created
service "kube-dns" created
Kube-dns rc and service is successfully deployed.
```


似乎很顺利。我们通过kubectl来查看一下(注意：由于DNS服务被创建在了一个名为kube-system的namespace中，kubectl执行时要指定namespace名字，否则将无法查到dns service)：

```
# kubectl --namespace=kube-system get services
NAME CLUSTER-IP EXTERNAL-IP PORT(S) AGE
kube-dns 192.168.3.10 <none> 53/UDP,53/TCP 1m
root@iZ25cn4xxnvZ:~/k8stest/1.3.7/kubernetes/cluster/ubuntu# kubectl --namespace=kube-system get pods
NAME READY STATUS RESTARTS AGE
kube-dns-v17.1-n4tnj 0/3 ErrImagePull 0 4m
```


在查看DNS组件对应的Pod时，发现Ready为0/3，STATUS为”ErrImagePull”，DNS服务并没有真正起来。

##### 2、修改skydns-rc.yaml

我们来修正上面的问题。在cluster/ubuntu下，我们发现多了两个文件：skydns-rc.yaml和skydns-svc.yaml，这两个文件就是deployAddons.sh执行时根据config-default.sh中的配置生成的两个k8s service描述文件，问题就出在skydns-rc.yaml中。在该文件中，我们看到了dns service启动的pod所含的三个容器对应的镜像名字：

```
gcr.io/google_containers/kubedns-amd64:1.5
gcr.io/google_containers/kube-dnsmasq-amd64:1.3
gcr.io/google_containers/exechealthz-amd64:1.1
```


在这次安装时，我并没有配置加速器（vpn）。因此在pull gcr.io上的镜像文件时出错了。在没有加速器的情况，我们在docker hub上可以很容易寻找到替代品（由于国内网络连接docker hub慢且经常无法连接，建议先手动pull出这三个替代镜像）：

```
gcr.io/google_containers/kubedns-amd64:1.5
=> chasontang/kubedns-amd64:1.5
gcr.io/google_containers/kube-dnsmasq-amd64:1.3
=> chasontang/kube-dnsmasq-amd64:1.3
gcr.io/google_containers/exechealthz-amd64:1.1
=> chasontang/exechealthz-amd64:1.1
```


我们需要手工将skydns-rc.yaml中的三个镜像名进行替换。并且为了防止deployAddons.sh重新生成skydns-rc.yaml，我们需要注释掉deployAddons.sh中的下面两行：

```
#sed -e "s/\\\$DNS_REPLICAS/${DNS_REPLICAS}/g;s/\\\$DNS_DOMAIN/${DNS_DOMAIN}/g;" "${KUBE_ROOT}/cluster/saltbase/salt/kube-dns/skydns-rc.yaml.sed" > skydns-rc.yaml
#sed -e "s/\\\$DNS_SERVER_IP/${DNS_SERVER_IP}/g" "${KUBE_ROOT}/cluster/saltbase/salt/kube-dns/skydns-svc.yaml.sed" > skydns-svc.yaml
```


删除dns服务：

```
# kubectl --namespace=kube-system delete rc/kube-dns-v17.1 svc/kube-dns
replicationcontroller "kube-dns-v17.1" deleted
service "kube-dns" deleted
```


再次执行deployAddons.sh重新部署DNS组件（不赘述）。安装后，我们还是来查看一下是否安装ok，这次我们直接用docker ps查看pod内那三个容器是否都起来了：

```
# docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
e8dc52cba2c7 chasontang/exechealthz-amd64:1.1 "/exechealthz '-cmd=n" 7 minutes ago Up 7 minutes k8s_healthz.1a0d495a_kube-dns-v17.1-0zhfp_kube-system_78728001-974c-11e6-ba01-00163e1625a9_b42e68fc
f1b83b442b15 chasontang/kube-dnsmasq-amd64:1.3 "/usr/sbin/dnsmasq --" 7 minutes ago Up 7 minutes k8s_dnsmasq.f16970b7_kube-dns-v17.1-0zhfp_kube-system_78728001-974c-11e6-ba01-00163e1625a9_da111cd4
d9f09b440c6e gcr.io/google_containers/pause-amd64:3.0 "/pause" 7 minutes ago Up 7 minutes k8s_POD.a6b39ba7_kube-dns-v17.1-0zhfp_kube-system_78728001-974c-11e6-ba01-00163e1625a9_b198b4a8
```


似乎kube-dns这个镜像的容器并没有启动成功。docker ps -a印证了这一点：

```
# docker ps -a
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
24387772a2a9 chasontang/kubedns-amd64:1.5 "/kube-dns --domain=c" 3 minutes ago Exited (255) 2 minutes ago k8s_kubedns.cdbc8a07_kube-dns-v17.1-0zhfp_kube-system_78728001-974c-11e6-ba01-00163e1625a9_473144a6
3b8bb401ac6f chasontang/kubedns-amd64:1.5 "/kube-dns --domain=c" 5 minutes ago Exited (255) 4 minutes ago k8s_kubedns.cdbc8a07_kube-dns-v17.1-0zhfp_kube-system_78728001-974c-11e6-ba01-00163e1625a9_cdd57b87
```


查看一下stop状态下的kube-dns container的容器日志：

```
# docker logs 24387772a2a9
I1021 05:18:00.982731 1 server.go:91] Using https://192.168.3.1:443 for kubernetes master
I1021 05:18:00.982898 1 server.go:92] Using kubernetes API <nil>
I1021 05:18:00.983810 1 server.go:132] Starting SkyDNS server. Listening on port:10053
I1021 05:18:00.984030 1 server.go:139] skydns: metrics enabled on :/metrics
I1021 05:18:00.984152 1 dns.go:166] Waiting for service: default/kubernetes
I1021 05:18:00.984672 1 logs.go:41] skydns: ready for queries on cluster.local. for tcp://0.0.0.0:10053 [rcache 0]
I1021 05:18:00.984697 1 logs.go:41] skydns: ready for queries on cluster.local. for udp://0.0.0.0:10053 [rcache 0]
I1021 05:18:01.292557 1 dns.go:172] Ignoring error while waiting for service default/kubernetes: the server has asked for the client to provide credentials (get services kubernetes). Sleeping 1s before retrying.
E1021 05:18:01.293232 1 reflector.go:216] pkg/dns/dns.go:155: Failed to list *api.Service: the server has asked for the client to provide credentials (get services)
E1021 05:18:01.293361 1 reflector.go:216] pkg/dns/dns.go:154: Failed to list *api.Endpoints: the server has asked for the client to provide credentials (get endpoints)
I1021 05:18:01.483325 1 dns.go:439] Received DNS Request:kubernetes.default.svc.cluster.local., exact:false
I1021 05:18:01.483390 1 dns.go:539] records:[], retval:[], path:[local cluster svc default kubernetes]
I1021 05:18:01.582598 1 dns.go:439] Received DNS Request:kubernetes.default.svc.cluster.local., exact:false
... ...
I1021 05:19:07.458786 1 dns.go:172] Ignoring error while waiting for service default/kubernetes: the server has asked for the client to provide credentials (get services kubernetes). Sleeping 1s before retrying.
E1021 05:19:07.460465 1 reflector.go:216] pkg/dns/dns.go:154: Failed to list *api.Endpoints: the server has asked for the client to provide credentials (get endpoints)
E1021 05:19:07.462793 1 reflector.go:216] pkg/dns/dns.go:155: Failed to list *api.Service: the server has asked for the client to provide credentials (get services)
F1021 05:19:07.867746 1 server.go:127] Received signal: terminated
```


从日志上去看，应该是kube-dns去连接apiserver失败，重试一定次数后，退出了。从日志上看，kube-dns视角中的kubernetes api server的地址是：

```
I1021 05:18:00.982731 1 server.go:91] Using https://192.168.3.1:443 for kubernetes master
```


而实际上我们的k8s apiserver监听的insecure port是8080，secure port是6443(由于没有显式配置，6443是源码中的默认端口)，通过https+443端口访问apiserver毫无疑问将以失败告终。问题找到了，接下来就是如何解决了。

##### 3、指定–kube-master-url

我们看一下kube-dns命令都有哪些可以传入的命令行参数：

```
# docker run -it chasontang/kubedns-amd64:1.5 kube-dns --help
Usage of /kube-dns:
--alsologtostderr[=false]: log to standard error as well as files
--dns-port=53: port on which to serve DNS requests.
--domain="cluster.local.": domain under which to create names
--federations=: a comma separated list of the federation names and their corresponding domain names to which this cluster belongs. Example: "myfederation1=example.com,myfederation2=example2.com,myfederation3=example.com"
--healthz-port=8081: port on which to serve a kube-dns HTTP readiness probe.
--kube-master-url="": URL to reach kubernetes master. Env variables in this flag will be expanded.
--kubecfg-file="": Location of kubecfg file for access to kubernetes master service; --kube-master-url overrides the URL part of this; if neither this nor --kube-master-url are provided, defaults to service account tokens
--log-backtrace-at=:0: when logging hits line file:N, emit a stack trace
--log-dir="": If non-empty, write log files in this directory
--log-flush-frequency=5s: Maximum number of seconds between log flushes
--logtostderr[=true]: log to standard error instead of files
--stderrthreshold=2: logs at or above this threshold go to stderr
--v=0: log level for V logs
--version[=false]: Print version information and quit
--vmodule=: comma-separated list of pattern=N settings for file-filtered logging
```


可以看出：–kube-master-url这个命令行选项可以实现我们的诉求。我们需要再次修改一下skydns-rc.yaml：

```
args:
# command = "/kube-dns"
- --domain=cluster.local.
- --dns-port=10053
- --kube-master-url=http://10.47.136.60:8080 # 新增一行
```


再次重新部署DNS Addon，不赘述。部署后查看kube-dns服务信息：

```
# kubectl --namespace=kube-system describe service/kube-dns
Name: kube-dns
Namespace: kube-system
Labels: k8s-app=kube-dns
kubernetes.io/cluster-service=true
kubernetes.io/name=KubeDNS
Selector: k8s-app=kube-dns
Type: ClusterIP
IP: 192.168.3.10
Port: dns 53/UDP
Endpoints: 172.16.99.3:53
Port: dns-tcp 53/TCP
Endpoints: 172.16.99.3:53
Session Affinity: None
No events
```


在通过docker logs直接查看kube-dns容器的日志：

```
docker logs 2f4905510cd2
I1023 11:44:12.997606 1 server.go:91] Using http://10.47.136.60:8080 for kubernetes master
I1023 11:44:13.090820 1 server.go:92] Using kubernetes API v1
I1023 11:44:13.091707 1 server.go:132] Starting SkyDNS server. Listening on port:10053
I1023 11:44:13.091828 1 server.go:139] skydns: metrics enabled on :/metrics
I1023 11:44:13.091952 1 dns.go:166] Waiting for service: default/kubernetes
I1023 11:44:13.094592 1 logs.go:41] skydns: ready for queries on cluster.local. for tcp://0.0.0.0:10053 [rcache 0]
I1023 11:44:13.094606 1 logs.go:41] skydns: ready for queries on cluster.local. for udp://0.0.0.0:10053 [rcache 0]
I1023 11:44:13.104789 1 server.go:101] Setting up Healthz Handler(/readiness, /cache) on port :8081
I1023 11:44:13.105912 1 dns.go:660] DNS Record:&{192.168.3.182 0 10 10 false 30 0 }, hash:6a8187e0
I1023 11:44:13.106033 1 dns.go:660] DNS Record:&{kubernetes-dashboard.kube-system.svc.cluster.local. 0 10 10 false 30 0 }, hash:529066a8
I1023 11:44:13.106120 1 dns.go:660] DNS Record:&{192.168.3.10 0 10 10 false 30 0 }, hash:bdfe50f8
I1023 11:44:13.106193 1 dns.go:660] DNS Record:&{kube-dns.kube-system.svc.cluster.local. 53 10 10 false 30 0 }, hash:fdbb4e78
I1023 11:44:13.106268 1 dns.go:660] DNS Record:&{kube-dns.kube-system.svc.cluster.local. 53 10 10 false 30 0 }, hash:fdbb4e78
I1023 11:44:13.106306 1 dns.go:660] DNS Record:&{kube-dns.kube-system.svc.cluster.local. 0 10 10 false 30 0 }, hash:d1247c4e
I1023 11:44:13.106329 1 dns.go:660] DNS Record:&{192.168.3.1 0 10 10 false 30 0 }, hash:2b11f462
I1023 11:44:13.106350 1 dns.go:660] DNS Record:&{kubernetes.default.svc.cluster.local. 443 10 10 false 30 0 }, hash:c3f6ae26
I1023 11:44:13.106377 1 dns.go:660] DNS Record:&{kubernetes.default.svc.cluster.local. 0 10 10 false 30 0 }, hash:b9b7d845
I1023 11:44:13.106398 1 dns.go:660] DNS Record:&{192.168.3.179 0 10 10 false 30 0 }, hash:d7e0b1e
I1023 11:44:13.106422 1 dns.go:660] DNS Record:&{my-nginx.default.svc.cluster.local. 0 10 10 false 30 0 }, hash:b0f41a92
I1023 11:44:16.083653 1 dns.go:439] Received DNS Request:kubernetes.default.svc.cluster.local., exact:false
I1023 11:44:16.083950 1 dns.go:539] records:[0xc8202c39d0], retval:[{192.168.3.1 0 10 10 false 30 0 /skydns/local/cluster/svc/default/kubernetes/3262313166343632}], path:[local cluster svc default kubernetes]
I1023 11:44:16.084474 1 dns.go:439] Received DNS Request:kubernetes.default.svc.cluster.local., exact:false
I1023 11:44:16.084517 1 dns.go:539] records:[0xc8202c39d0], retval:[{192.168.3.1 0 10 10 false 30 0 /skydns/local/cluster/svc/default/kubernetes/3262313166343632}], path:[local cluster svc default kubernetes]
I1023 11:44:16.085024 1 dns.go:583] Received ReverseRecord Request:1.3.168.192.in-addr.arpa.
```


通过日志可以看到，apiserver的url是正确的，kube-dns组件没有再输出错误，安装似乎成功了，还需要测试验证一下。

#### 三、测试验证k8s DNS

按照预期，k8s dns组件可以为k8s集群内的service做dns解析。当前k8s集群默认namespace已经部署的服务如下：

```
# kubectl get services
NAME CLUSTER-IP EXTERNAL-IP PORT(S) AGE
kubernetes 192.168.3.1 <none> 443/TCP 10d
my-nginx 192.168.3.179 <nodes> 80/TCP 6d
```


我们在k8s集群中的一个myclient容器中尝试去ping和curl my-nginx服务：

ping my-nginx解析成功(找到my-nginx的clusterip: 192.168.3.179)：

```
root@my-nginx-2395715568-gpljv:/# ping my-nginx
PING my-nginx.default.svc.cluster.local (192.168.3.179): 56 data bytes
```


curl my-nginx服务也得到如下成功结果：

```
# curl -v my-nginx
* Rebuilt URL to: my-nginx/
* Hostname was NOT found in DNS cache
* Trying 192.168.3.179...
* Connected to my-nginx (192.168.3.179) port 80 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.35.0
> Host: my-nginx
> Accept: */*
>
< HTTP/1.1 200 OK
* Server nginx/1.10.1 is not blacklisted
< Server: nginx/1.10.1
< Date: Sun, 23 Oct 2016 12:14:01 GMT
< Content-Type: text/html
< Content-Length: 612
< Last-Modified: Tue, 31 May 2016 14:17:02 GMT
< Connection: keep-alive
< ETag: "574d9cde-264"
< Accept-Ranges: bytes
<
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
body {
width: 35em;
margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif;
}
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>
<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>
<p><em>Thank you for using nginx.</em></p>
</body>
</html>
* Connection #0 to host my-nginx left intact
```


客户端容器的dns配置，这应该是k8s安装时采用的默认配置（与config-default.sh有关）：

```
# cat /etc/resolv.conf
search default.svc.cluster.local svc.cluster.local cluster.local
nameserver 192.168.3.10
options timeout:1 attempts:1 rotate
options ndots:5
```


到此，k8s dns组件就安装ok了。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

验证dns同样可以到 node 机上，dig @192.168.3.10 my-nginx.default.svc.cluster.local

mirrors.aliyun.com 有镜像