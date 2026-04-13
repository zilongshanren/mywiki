---
title: 使用Kubeadm安装Kubernetes-Part2
url: https://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm-2/
published: '2016-12-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Kubeadm安装Kubernetes-Part2

此文为《使用Kubeadm安装Kubernetes》的第二部分。文章第一部分在[这里](http://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)可以看到。

### 五、weave network for pod

经过上面那么多次尝试，结果是令人扫兴的。Weave network似乎是最后一颗救命稻草了。有了前面的铺垫，这里就不详细列出各种命令的输出细节了。Weave network也有[专门的官方文档](https://www.weave.works/docs/net/latest/kube-addon/)用于指导如何与kubernetes集群集成，我们主要也是参考它。

#### 1、安装weave network add-on

在kubeadm reset后，我们重新初始化了集群。接下来我们安装weave network add-on：

```
# kubectl apply -f https://git.io/weave-kube
daemonset "weave-net" created
```


前面无论是Flannel还是calico，在安装pod network add-on时至少都还是顺利的。不过在Weave network这次，我们遭遇“当头棒喝”:(:

```
# kubectl get pod --all-namespaces -o wide
NAMESPACE NAME READY STATUS RESTARTS AGE IP NODE
kube-system dummy-2088944543-4kxtk 1/1 Running 0 42m 10.47.217.91 iz25beglnhtz
kube-system etcd-iz25beglnhtz 1/1 Running 0 42m 10.47.217.91 iz25beglnhtz
kube-system kube-apiserver-iz25beglnhtz 1/1 Running 0 42m 10.47.217.91 iz25beglnhtz
kube-system kube-controller-manager-iz25beglnhtz 1/1 Running 0 42m 10.47.217.91 iz25beglnhtz
kube-system kube-discovery-1769846148-pzv8p 1/1 Running 0 42m 10.47.217.91 iz25beglnhtz
kube-system kube-dns-2924299975-09dcb 0/4 ContainerCreating 0 42m <none> iz25beglnhtz
kube-system kube-proxy-z465f 1/1 Running 0 42m 10.47.217.91 iz25beglnhtz
kube-system kube-scheduler-iz25beglnhtz 1/1 Running 0 42m 10.47.217.91 iz25beglnhtz
kube-system weave-net-3wk9h 0/2 CrashLoopBackOff 16 17m 10.47.217.91 iz25beglnhtz
```


安装后，weave-net pod提示:CrashLoopBackOff。追踪其Container log，得到如下错误信息：

```
# docker logs cde899efa0af
time="2016-12-28T08:25:29Z" level=info msg="Starting Weaveworks NPC 1.8.2"
time="2016-12-28T08:25:29Z" level=info msg="Serving /metrics on :6781"
Wed Dec 28 08:25:29 2016 <5> ulogd.c:843 building new pluginstance stack: 'log1:NFLOG,base1:BASE,pcap1:PCAP'
time="2016-12-28T08:25:29Z" level=fatal msg="ipset [destroy] failed: ipset v6.29: Set cannot be destroyed: it is in use by a kernel component\n: exit status 1"
```


#### 2、解决ipset destroy错误

从上述的错误日志来看，似乎某些内核组件占用了一些IP资源，没有释放。ipset(administration tool for IP sets)这个工具以前从来没有接触过。在node上利用apt-get install 一个ipset工具，手工执行以下命令：

```
# ipset destroy
ipset v6.29: Set cannot be destroyed: it is in use by a kernel component
```


这个错误输出与container中的error log一模一样。试着用ipset看看哪些ip资源没有释放，这一招让我们看到了蛛丝马迹：

在minion node上执行：

```
# ipset list
Name: felix-calico-hosts-4
Type: hash:ip
Revision: 4
Header: family inet hashsize 1024 maxelem 1048576
Size in memory: 224
References: 1
Members:
123.56.200.187
59.110.67.15
Name: felix-all-ipam-pools
Type: hash:net
Revision: 6
Header: family inet hashsize 1024 maxelem 1048576
Size in memory: 448
References: 1
Members:
192.168.0.0/16
Name: felix-masq-ipam-pools
Type: hash:net
Revision: 6
Header: family inet hashsize 1024 maxelem 1048576
Size in memory: 448
References: 1
Members:
192.168.0.0/16
```


我们看到了calico字样。原来是calico的“残留势力”在作祟啊。进一步我们发现calico创建的一个network device依旧存在于两个Node上：

```
47: tunl0@NONE: <NOARP,UP,LOWER_UP> mtu 1440 qdisc noqueue state UNKNOWN group default qlen 1
link/ipip 0.0.0.0 brd 0.0.0.0
inet 192.168.91.0/32 scope global tunl0
valid_lft forever preferred_lft forever
```


我们试图删除它，但最终都以失败告终：

```
# ip tunnel show
tunl0: ip/ip remote any local any ttl inherit nopmtudisc
#ip tunnel del tunl0
delete tunnel "tunl0" failed: Operation not permitted
```


无奈只能把它down掉：

```
#ip -f inet addr delete 192.168.91.0/32 dev tunl0
47: tunl0@NONE: <NOARP,UP,LOWER_UP> mtu 1440 qdisc noqueue state UNKNOWN group default qlen 1
link/ipip 0.0.0.0 brd 0.0.0.0
# ifconfig tunl0 down
47: tunl0@NONE: <NOARP> mtu 1440 qdisc noqueue state DOWN group default qlen 1
link/ipip 0.0.0.0 brd 0.0.0.0
```


但依旧无法删除它。我们通过ipset del命令将上面ipset占用的ip entry逐个删除掉（比如ipset del felix-calico-hosts-4 123.56.200.187）。但即便全部清空，ipset destroy依然失败。

无奈之下，决定重启一下两个Node试试。重启后，calico创建的这个tunnel居然消失了。

#### 3、再遇路由冲突错误

重启ECS实例后，我们重新从头来创建cluster。不过在执行“kubectl apply -f https://git.io/weave-kube” 后我们发现weave-net pod依旧没有起来，这次的错误是“路有冲突”：

```
#docker logs 80383071f721
Network 10.32.0.0/12 overlaps with existing route 10.0.0.0/8 on host.
```


查看当前路由表：

```
netstat -rn
Kernel IP routing table
Destination Gateway Genmask Flags MSS Window irtt Iface
0.0.0.0 123.56.203.247 0.0.0.0 UG 0 0 0 eth1
10.0.0.0 10.47.223.247 255.0.0.0 UG 0 0 0 eth0
10.47.216.0 0.0.0.0 255.255.248.0 U 0 0 0 eth0
100.64.0.0 10.47.223.247 255.192.0.0 UG 0 0 0 eth0
123.56.200.0 0.0.0.0 255.255.252.0 U 0 0 0 eth1
172.16.0.0 10.47.223.247 255.240.0.0 UG 0 0 0 eth0
192.168.0.0 0.0.0.0 255.255.240.0 U 0 0 0 docker0
```


的确weave-net默认要使用的 10.32.0.0/12与 10.0.0.0/8 存在交集。对此，weave net官方是给出[解决方案](https://tonybai.com/:https:/www.weave.works/documentation/net-latest-using-weave/net-latest-configuring-weave/)了的。

我们先将https://git.io/weave-kube对应的yaml文件下载到本地：weave-daemonset.yaml。修改该文件，为container增加IPALLOC_RANGE环境变量：

```
containers:
- name: weave
env:
- name: IPALLOC_RANGE
value: 172.30.0.0/16
```


更新weave net pod：

```
# kubectl delete -f weave-daemonset.yaml
daemonset "weave-net" deleted
# kubectl apply -f weave-daemonset.yaml
daemonset "weave-net" created
```


不过依然存在路有冲突。原来路由表里已经存在了一条这样的路由：

```
172.16.0.0 10.28.63.247 255.240.0.0 UG 0 0 0 eth0
```


这条路由应该没有什么用，也许是之前折腾时被某个network addon加进去的。于是用route命令将其删除：

```
# route del -net 172.16.0.0 netmask 255.240.0.0 gw 10.28.63.247
```


再次更新weave net pod并查看cluster status：

```
# kubectl delete -f weave-daemonset.yaml
daemonset "weave-net" deleted
# kubectl apply -f weave-daemonset.yaml
daemonset "weave-net" created
# kubectl get pods --all-namespaces -o wide
NAMESPACE NAME READY STATUS RESTARTS AGE IP NODE
kube-system dummy-2088944543-93f4c 1/1 Running 0 21m 10.47.217.91 iz25beglnhtz
kube-system etcd-iz25beglnhtz 1/1 Running 0 21m 10.47.217.91 iz25beglnhtz
kube-system kube-apiserver-iz25beglnhtz 1/1 Running 0 20m 10.47.217.91 iz25beglnhtz
kube-system kube-controller-manager-iz25beglnhtz 1/1 Running 0 21m 10.47.217.91 iz25beglnhtz
kube-system kube-discovery-1769846148-wbc7h 1/1 Running 0 21m 10.47.217.91 iz25beglnhtz
kube-system kube-dns-2924299975-206tg 4/4 Running 0 21m 172.30.0.2 iz25beglnhtz
kube-system kube-proxy-n2xmf 1/1 Running 0 21m 10.47.217.91 iz25beglnhtz
kube-system kube-scheduler-iz25beglnhtz 1/1 Running 0 20m 10.47.217.91 iz25beglnhtz
kube-system weave-net-h38k5 2/2 Running 0 18s 10.47.217.91 iz25beglnhtz
```


这回weave-net pod running了。taint master node并且minion node join后cluster依旧是ok的：

```
# kubectl get pods --all-namespaces -o wide
NAMESPACE NAME READY STATUS RESTARTS AGE IP NODE
kube-system dummy-2088944543-93f4c 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
kube-system etcd-iz25beglnhtz 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
kube-system kube-apiserver-iz25beglnhtz 1/1 Running 0 22m 10.47.217.91 iz25beglnhtz
kube-system kube-controller-manager-iz25beglnhtz 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
kube-system kube-discovery-1769846148-wbc7h 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
kube-system kube-dns-2924299975-206tg 4/4 Running 0 23m 172.30.0.2 iz25beglnhtz
kube-system kube-proxy-377zh 1/1 Running 0 8s 10.28.61.30 iz2ze39jeyizepdxhwqci6z
kube-system kube-proxy-n2xmf 1/1 Running 0 23m 10.47.217.91 iz25beglnhtz
kube-system kube-scheduler-iz25beglnhtz 1/1 Running 0 22m 10.47.217.91 iz25beglnhtz
kube-system weave-net-9tf1d 2/2 Running 0 8s 10.28.61.30 iz2ze39jeyizepdxhwqci6z
kube-system weave-net-h38k5 2/2 Running 0 2m 10.47.217.91 iz25beglnhtz
```


#### 4、测试weave net跨节点pod连通性

这回我们依旧启动my-nginx service，在任意一个节点curl localhost:30062，我们发现被调度到minion node上的my-nginx container也收到了request并成功回复response：

```
172.30.0.1 - - [30/Dec/2016:03:14:47 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.47.0" "-"
```


Weave net初步测试ok！

### 六、小结

虽然过程坎坷，但最终在Weave net的帮助下，我们还是初步调通了一个使用kubeadm安装的kubernetes cluster。后来我发现，在K8s官方博客中有一篇名为《[Kubernetes: How we made Kubernetes insanely easy to install](http://blog.kubernetes.io/2016/09/how-we-made-kubernetes-easy-to-install.html)》的文章，其使用的pod network add-on也是weave network。

这是一个试验环境。后续我们还是要进一步探究如何用上Flannel的。同时，Kubernetes 1.5带来的[诸多新特性](http://blog.kubernetes.io/2016/12/five-days-of-kubernetes-1.5.html)，比如：Master HA等还需要进一步试验证明。

为了满足我们的production环境要求，之前实践的[Ceph RBD为K8s提供存储卷](http://tonybai.com/2016/11/07/integrate-kubernetes-with-ceph-rbd)、[k8s从private registry拉取image](http://tonybai.com/2016/11/16/how-to-pull-images-from-private-registry-on-kubernetes-cluster)、[k8s集群的安全配置](http://tonybai.com/2016/11/25/the-security-settings-for-kubernetes-cluster)等还要在新集群上进一步试验，直到满足我们的要求。

© 2016 – 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

不好意思问两个问题。

1. 国内网络无法拉到gcr.io上的镜像，博主怎么解决这个问题的。

2. 我安装Weave net好之后所有kubernetes的node从外网都ping不通也无法ssh，但是从k8s节点所在的局域网机器上可以访问，请问博主有遇到过这样的情况吗？官方文档貌似没有提到这一点。

1、无法拉取gcr.io镜像的问题，这个似乎只能通过开启加速器的情况解决了。在docker引擎的配置中加上加速器的代理，我使用的是“多态”这个厂商的加速器。 2、这个问题我不是很明白。从k8s节点所在局域网可以访问k8s节点，这个肯定是ok的。从外网访问k8s node主机 这个和安装不安装weave net没有关系吧。你没有安装weave net时，能访问么？外网到内网一般都是有防火墙的。是否能访问看防火墙是否做了映射配置。

请问如何开启docker加速器解决gcr.io的镜像问题？

如果通过加速器解决，首先需要购买加速器服务，比如国内的多态，当然加速器国内外有很多，你懂的。有了加速器服务后，如果你直接利用加速器服务的客户端fanqiang，那么docker可以直接pull gcri.io的镜像；如果是使用加速器的代理服务，可以通过在docker config file中配置相应代理解决。比如:ubuntu 14.04版本，可以在/etc/default/docker中配置export http_proxy=”xxxx” export https_proxy=”xxxx”解决；ubuntu 16.04版本docker配置可参考这篇文章：http://tonybai.com/2016/12/27/when-docker-meets-systemd/