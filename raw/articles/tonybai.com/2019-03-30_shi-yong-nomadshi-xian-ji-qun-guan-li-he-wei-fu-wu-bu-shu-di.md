---
title: 使用nomad实现集群管理和微服务部署调度
url: https://tonybai.com/2019/03/30/cluster-management-and-microservice-deployment-and-scheduled-by-nomad/
published: '2019-03-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用nomad实现集群管理和微服务部署调度

在[“云原生”](https://www.cncf.io/)、[“容器化”](https://tonybai.com/tag/docker)、[“微服务”](https://en.wikipedia.org/wiki/Microservices)、[“服务网格”](https://tonybai.com/2018/01/03/an-intro-of-microservices-governance-by-istio/)等概念大行其道的今天，一提到集群管理、容器工作负载调度，人们首先想到的是[Kubernetes](https://tonybai.com/tag/kubernetes)。

[Kubernetes](https://kubernetes.io/)经过多年的发展，目前已经成为了云原生计算平台的事实标准，得到了诸如谷歌、微软、红帽、亚马逊、IBM、阿里等大厂的大力支持，各大云计算提供商也都提供了专属Kubernetes集群服务。开发人员可以**一键**在这些大厂的云上[创建k8s集群](https://tonybai.com/2017/05/15/setup-a-ha-kubernetes-cluster-based-on-kubeadm-part1/)。对于那些不愿被cloud provider绑定的组织或开发人员，Kubernetes也提供了诸如[Kubeadm](https://tonybai.com/2017/05/15/setup-a-ha-kubernetes-cluster-based-on-kubeadm-part1/)这样的k8s集群引导工具，帮助大家在裸金属机器上[搭建自己的k8s集群](https://tonybai.com/2018/10/17/imooc-course-kubernetes-practice-go-online/)，当然这样做的门槛较高（如果您想学习自己搭建和管理k8s集群，可以参考我在[慕课网](https://www.imooc.com/)上发布的实战课[《高可用集群搭建、配置、运维与应用》](https://coding.imooc.com/class/284.html)）。

Kubernetes的学习曲线是公认的较高，尤其是对于应用开发人员。再加上Kubernetes发展很快，越来越多的概念和功能加入到k8s技术栈，这让人们不得不考虑建立和维护这样一套集群所要付出的成本。人们也在考虑是否所有场景都需要部署一个k8s集群，是否有轻量级的且能满足自身需求的集群管理和微服务部署调度方案呢？外国朋友Matthias Endler就在其文章[《也许你不需要Kubernetes》](https://matthias-endler.de/2019/maybe-you-dont-need-kubernetes/)中给出一个轻量级的集群管理方案 – 使用[hashicorp](https://www.hashicorp.com/)开源的[nomad工具](https://github.com/hashicorp/nomad)。

这让我想起了去年写的[《基于consul实现微服务的服务发现和负载均衡》](https://tonybai.com/2018/09/10/setup-service-discovery-and-load-balance-based-on-consul/)一文。文中虽然实现了基于[consul](https://tonybai.com/2015/07/06/implement-distributed-services-registery-and-discovery-by-consul/)的服务注册、发现以及负载均衡，但是缺少一个环节：那就是整个集群管理以及工作负载部署调度自动化的缺乏。nomad应该恰好可以补足这一短板，并且它足够轻量。本文我们就来探索和实践一下使用[nomad](https://github.com/hashicorp/nomad)实现集群管理和微服务部署调度。

## 一. 安装nomad集群

nomad是Hashicorp公司出品的集群管理和工作负荷调度器，支持多种驱动形式的工作负载调度，包括[Docker容器](https://tonybai.com/tag/docker)、虚拟机、原生可执行程序等，并支持跨数据中心调度。Nomad不负责服务发现或密钥管理等 ，它将这些功能分别留给了HashiCorp的[Consul](https://tonybai.com/tag/consul)和[Vault](https://github.com/hashicorp/vault)。HashiCorp的创始人认为，这会使得Nomad更为轻量级，调度性能更高。

nomad使用[Go语言](https://tonybai.com/tag/golang)实现，因此其本身仅仅是一个可执行的二进制文件。和Hashicorp其他工具产品(诸如：consul等)类似，nomad一个可执行文件既可以以server模式运行，亦可以client模式运行，甚至可以启动一个实例，既是server，也是client。

下面是nomad集群的架构图(来自hashicorp官方）:

![img{512x368}](../../assets/b15e1232a038ffc7.png)


一个nomad集群至少要包含一个server，作为集群的控制平面；一个或多个client则用于承载工作负荷。通常生产环境nomad集群的控制平面至少要有5个及以上的server才能在高可用上有一定保证。

建立一个nomad集群有多种方法，包括手工建立、基于consul自动建立和基于云自动建立。考虑到后续涉及微服务的注册发现，这里我们采用基于consul自动建立nomad集群的方法，下面是部署示意图：

![img{512x368}](../../assets/755de30347996eac.png)


我这里的试验环境仅有三台hosts，因此这三台host既承载consul集群，也承载nomad集群（包括server和client），即nomad的控制平面和工作负荷由这三台host一并承担了。

### 1. consul集群启动

在之前的[《基于consul实现微服务的服务发现和负载均衡》](https://tonybai.com/2018/09/10/setup-service-discovery-and-load-balance-based-on-consul/)一文中，我对consul集群的建立做过详细地说明，因此这里只列出步骤，不详细解释了。注意：这次consul的版本升级到了consul v1.4.4了。

在每个node上分别下载consul 1.4.4：

```
# wget -c https://releases.hashicorp.com/consul/1.4.4/consul_1.4.4_linux_amd64.zip
# unzip consul_1.4.4_linux_amd64.zip
# cp consul /usr/local/bin
# consul -v
Consul v1.4.4
Protocol 2 spoken by default, understands 2 to 3 (agent will automatically use protocol >2 when speaking to compatible agents)
```


启动consul集群：(每个node上创建~/.bin/consul-install目录，并进入该目录下执行)

```
dxnode1:
# nohup consul agent -server -ui -dns-port=53 -bootstrap-expect=3 -data-dir=~/.bin/consul-install/consul-data -node=consul-1 -client=0.0.0.0 -bind=172.16.66.102 -datacenter=dc1 > consul-1.log & 2>&1
dxnode2:
# nohup consul agent -server -ui -dns-port=53 -bootstrap-expect=3 -data-dir=/root/consul-install/consul-data -node=consul-2 -client=0.0.0.0 -bind=172.16.66.103 -datacenter=dc1 -join 172.16.66.102 > consul-2.log & 2>&1
dxnode3:
nohup consul agent -server -ui -dns-port=53 -bootstrap-expect=3 -data-dir=/root/consul-install/consul-data -node=consul-3 -client=0.0.0.0 -bind=172.16.66.104 -datacenter=dc1 -join 172.16.66.102 > consul-3.log & 2>&1
```


consul集群启动结果查看如下：

```
# consul members
Node Address Status Type Build Protocol DC Segment
consul-1 172.16.66.102:8301 alive server 1.4.4 2 dc1 <all>
consul-2 172.16.66.103:8301 alive server 1.4.4 2 dc1 <all>
consul-3 172.16.66.104:8301 alive server 1.4.4 2 dc1 <all>
# consul operator raft list-peers
Node ID Address State Voter RaftProtocol
consul-3 d048e55b-5f6a-34a4-784c-e6607db0e89e 172.16.66.104:8300 leader true 3
consul-1 160a7a20-f177-d2f5-0765-e6d1a9a1a9a4 172.16.66.102:8300 follower true 3
consul-2 6795cd2c-fad5-9d4f-2531-13b0a65e0893 172.16.66.103:8300 follower true 3
```


### 2. DNS设置（可选）

如果采用基于consul DNS的方式进行服务发现，那么在每个**nomad client node**上设置DNS则很必要。否则如果要是基于consul service catalog的API去查找service，则可忽略这个步骤。设置步骤如下：

在每个node上，创建和编辑/etc/resolvconf/resolv.conf.d/base，填入如下内容：

```
nameserver {consul-1-ip}
nameserver {consul-2-ip}
```


然后重启resolvconf服务:

```
# /etc/init.d/resolvconf restart
[ ok ] Restarting resolvconf (via systemctl): resolvconf.service.
```


新的resolv.conf将变成：

```
# cat /etc/resolv.conf
# Dynamic resolv.conf(5) file for glibc resolver(3) generated by resolvconf(8)
# DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
nameserver {consul-1-ip}
nameserver {consul-2-ip}
nameserver 100.100.2.136
nameserver 100.100.2.138
options timeout:2 attempts:3 rotate single-request-reopen
```


这样无论是在host上，还是在新启动的container里就都可以访问到xx.xx.consul域名的服务了：

```
# ping -c 3 consul.service.dc1.consul
PING consul.service.dc1.consul (172.16.66.103) 56(84) bytes of data.
64 bytes from 172.16.66.103: icmp_seq=1 ttl=64 time=0.227 ms
64 bytes from 172.16.66.103: icmp_seq=2 ttl=64 time=0.158 ms
^C
--- consul.service.dc1.consul ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 999ms
rtt min/avg/max/mdev = 0.158/0.192/0.227/0.037 ms
# docker run busybox ping -c 3 consul.service.dc1.consul
PING consul.service.dc1.consul (172.16.66.104): 56 data bytes
64 bytes from 172.16.66.104: seq=0 ttl=64 time=0.067 ms
64 bytes from 172.16.66.104: seq=1 ttl=64 time=0.061 ms
64 bytes from 172.16.66.104: seq=2 ttl=64 time=0.076 ms
--- consul.service.dc1.consul ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 0.061/0.068/0.076 ms
```


### 3. 基于consul集群引导启动nomad集群

按照之前的拓扑图，我们需先在每个node上分别下载nomad：

```
# wget -c https://releases.hashicorp.com/nomad/0.8.7/nomad_0.8.7_linux_amd64.zip
# unzip nomad_0.8.7_linux_amd64.zip.zip
# cp ./nomad /usr/local/bin
# nomad -v
Nomad v0.8.7 (21a2d93eecf018ad2209a5eab6aae6c359267933+CHANGES)
```


我们已经建立了consul集群，因为我们将采用[基于consul集群引导启动nomad集群](https://www.nomadproject.io/guides/operations/cluster/automatic.html)这一创建nomad集群的最Easy方式。同时，我们每个node上既要运行nomad server，也要nomad client，于是我们在nomad的配置文件中，对server和client都设置为”enabled = true”。下面是nomad启动的配置文件，每个node上的nomad均将该配置文件作为为输入：

```
// agent.hcl
data_dir = "/root/.bin/nomad-install/nomad.d"
server {
enabled = true
bootstrap_expect = 3
}
client {
enabled = true
}
```


下面是在各个节点上启动nomad的操作步骤：

```
dxnode1:
# nohup nomad agent -config=/root/.bin/nomad-install/agent.hcl > nomad-1.log & 2>&1
dxnode2:
# nohup nomad agent -config=/root/.bin/nomad-install/agent.hcl > nomad-2.log & 2>&1
dxnode3:
# nohup nomad agent -config=/root/.bin/nomad-install/agent.hcl > nomad-3.log & 2>&1
```


查看nomad集群的启动结果：

```
# nomad server members
Name Address Port Status Leader Protocol Build Datacenter Region
dxnode1.global 172.16.66.102 4648 alive true 2 0.8.7 dc1 global
dxnode2.global 172.16.66.103 4648 alive false 2 0.8.7 dc1 global
dxnode3.global 172.16.66.104 4648 alive false 2 0.8.7 dc1 global
# nomad operator raft list-peers
Node ID Address State Voter RaftProtocol
dxnode1.global 172.16.66.102:4647 172.16.66.102:4647 leader true 2
dxnode2.global 172.16.66.103:4647 172.16.66.103:4647 follower true 2
dxnode3.global 172.16.66.104:4647 172.16.66.104:4647 follower true 2
# nomad node-status
ID DC Name Class Drain Eligibility Status
7acdd7bc dc1 dxnode1 <none> false eligible ready
c281658a dc1 dxnode3 <none> false eligible ready
9e3ef19f dc1 dxnode2 <none> false eligible ready
```


以上这些命令的结果都显示nomad集群工作正常！

nomad还提供一个ui界面（http://nomad-node-ip:4646/ui），可以让运维人员以可视化的方式直观看到当前nomad集群的状态，包括server、clients、工作负载(job)的情况：

![img{512x368}](../../assets/040dabb42cf38471.png)


nomad ui首页

![img{512x368}](../../assets/0fadef77c974940c.png)


nomad server列表和状态

![img{512x368}](../../assets/c757c3fe50ff279f.png)


nomad client列表和状态

## 二. 部署工作负载

引导启动成功nomad集群后，我们接下来就要向集群中添加“工作负载”了。

在[Kubernetes](https://coding.imooc.com/class/284.html)中，我们可以通过创建deployment、pod等向集群添加工作负载；在nomad中我们也可以通过类似的声明式的方法向nomad集群添加工作负载。不过nomad相对简单许多，它**仅提供了一种**名为job的抽象，并给出了[job的specification](https://www.nomadproject.io/docs/job-specification/index.html)。nomad集群所有关于工作负载的操作均通过job描述文件和nomad job相关子命令完成。下面是通过job部署工作负载的流程示意图：

![img{512x368}](../../assets/989984b64b7f3948.png)


从图中可以看到，我们需要做的仅仅是将编写好的job文件提交给nomad即可。

Job spec定义了：job -> group -> task的层次关系。每个job文件只有一个job，但是一个job可能有多个group，每个group可能有多个task。group包含一组要放在同一个集群中调度的task。一个Nomad task是由其驱动程序（driver）在Nomad client节点上执行的命令、服务、应用程序或其他工作负载。task可以是短时间的批处理作业（batch）或长时间运行的服务(service)，例如web应用程序、数据库服务器或API。

Tasks是在用[HCL语法](https://github.com/hashicorp/hcl)的声明性job规范中定义的。Job文件提交给Nomad服务端，服务端决定在何处以及如何将job文件中定义的task分配给客户端节点。另一种概念化的理解是:job规范表示工作负载的期望状态，Nomad服务端创建并维护其实际状态。

通过job，开发人员还可以为工作负载定义约束和资源。约束（constraint）通过内核类型和版本等属性限制了工作负载在节点上的位置。资源（resources）需求包括运行task所需的内存、网络、CPU等。

有三种类型的job：system、service和batch，它们决定Nomad将用于此job中task的调度器。service 调度器被设计用来调度永远不会宕机的长寿命服务。batch作业对短期性能波动的敏感性要小得多，寿命也很短，几分钟到几天就可以完成。system调度器用于注册应该在满足作业约束的所有nomad client上运行的作业。当某个client加入到nomad集群或转换到就绪状态时也会调用它。

Nomad允许job作者为自动重新启动失败和无响应的任务指定策略，并自动将失败的任务重新调度到其他节点，从而使任务工作负载具有弹性。

如果对应到k8s中的概念，group更像是某种controller，而task更类似于pod，是被真实调度的实体。Job spec对应某个k8s api object的spec，具体体现在某个yaml文件中。

下面我们就来真实地在nomad集群中创建一个工作负载。我们使用之前在[《基于consul实现微服务的服务发现和负载均衡》](https://tonybai.com/2018/09/10/setup-service-discovery-and-load-balance-based-on-consul/)一文中使用过的那几个demo image，这里我们先使用[httpbackendservice镜像](https://hub.docker.com/r/bigwhite/httpbackendservice)来创建一个job。

下面是httpbackend的job文件：

```
// httpbackend-1.nomad
job "httpbackend" {
datacenters = ["dc1"]
type = "service"
group "httpbackend" {
count = 2
task "httpbackend" {
driver = "docker"
config {
image = "bigwhite/httpbackendservice:v1.0.0"
port_map {
http = 8081
}
logging {
type = "json-file"
}
}
resources {
network {
mbits = 10
port "http" {}
}
}
service {
name = "httpbackend"
port = "http"
}
}
}
}
```


这个文件基本都是自解释的，重点提几个地方：

-
job type: service ： 说明该job创建和调度的是一个service类型的工作负载；

-
count = 2 ： 类似于k8s的replicas字段，期望在nomad集群中运行2个httpbackend服务实例，nomad来保证始终处于期望状态。

-
关于port：port_map指定了task中容器的监听端口。network中的port “http” {}没有指定静态IP，因此将采用动态主机端口。service中的port则指明使用”http”这个tag的动态主机端口。这和k8s中service中port使用名称匹配的方式映射到具体pod中的port的方法类似。


我们使用nomad job子命令来创建该工作负载。正式创建之前，我们可以先通过nomad job plan来dry-run一下，一是看job文件格式是否ok；二来检查一下nomad集群是否有空余资源创建和调度新的工作负载：

```
# nomad job plan httpbackend-1.nomad
+/- Job: "httpbackend"
+/- Stop: "true" => "false"
Task Group: "httpbackend" (2 create)
Task: "httpbackend"
Scheduler dry-run:
- All tasks successfully allocated.
Job Modify Index: 4248
To submit the job with version verification run:
nomad job run -check-index 4248 httpbackend-1.nomad
When running the job with the check-index flag, the job will only be run if the
server side version matches the job modify index returned. If the index has
changed, another user has modified the job and the plan's results are
potentially invalid.
```


如果plan的输出结果没有问题，则可以用nomad job run正式创建和调度job：

```
# nomad job run httpbackend-1.nomad
==> Monitoring evaluation "40c63529"
Evaluation triggered by job "httpbackend"
Allocation "6b0b83de" created: node "9e3ef19f", group "httpbackend"
Allocation "d0710b85" created: node "7acdd7bc", group "httpbackend"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "40c63529" finished with status "complete"
```


接下来，我们可以使用nomad job status命令查看job的创建情况以及某个job的详细状态信息：

```
# nomad job status
ID Type Priority Status Submit Date
httpbackend service 50 running 2019-03-30T04:58:09+08:00
# nomad job status httpbackend
ID = httpbackend
Name = httpbackend
Submit Date = 2019-03-30T04:58:09+08:00
Type = service
Priority = 50
Datacenters = dc1
Status = running
Periodic = false
Parameterized = false
Summary
Task Group Queued Starting Running Failed Complete Lost
httpbackend 0 0 2 0 0 0
Allocations
ID Node ID Task Group Version Desired Status Created Modified
6b0b83de 9e3ef19f httpbackend 11 run running 8m ago 7m50s ago
d0710b85 7acdd7bc httpbackend 11 run running 8m ago 7m39s ago
```


前面说过，nomad只是集群管理和负载调度，服务发现它是不管的，并且服务发现的问题早已经被consul解决掉了。所以httpbackend创建后，要想使用该服务，我们还得走consul提供的路线：

DNS方式(前面已经做过铺垫了)：

```
# dig SRV httpbackend.service.dc1.consul
; <<>> DiG 9.10.3-P4-Ubuntu <<>> SRV httpbackend.service.dc1.consul
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7742
;; flags: qr aa rd; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 5
;; WARNING: recursion requested but not available
;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;httpbackend.service.dc1.consul. IN SRV
;; ANSWER SECTION:
httpbackend.service.dc1.consul. 0 IN SRV 1 1 23578 consul-1.node.dc1.consul.
httpbackend.service.dc1.consul. 0 IN SRV 1 1 22819 consul-2.node.dc1.consul.
;; ADDITIONAL SECTION:
consul-1.node.dc1.consul. 0 IN A 172.16.66.102
consul-1.node.dc1.consul. 0 IN TXT "consul-network-segment="
consul-2.node.dc1.consul. 0 IN A 172.16.66.103
consul-2.node.dc1.consul. 0 IN TXT "consul-network-segment="
;; Query time: 471 msec
;; SERVER: 172.16.66.102#53(172.16.66.102)
;; WHEN: Sat Mar 30 05:07:54 CST 2019
;; MSG SIZE rcvd: 251
# curl http://172.16.66.102:23578
this is httpbackendservice, version: v1.0.0
# curl http://172.16.66.103:22819
this is httpbackendservice, version: v1.0.0
```


或http api方式(可通过[官方API](https://godoc.org/github.com/hashicorp/consul/api)查询服务)：

```
# curl http://127.0.0.1:8500/v1/health/service/httpbackend
[
{
"Node": {"ID":"160a7a20-f177-d2f5-0765-e6d1a9a1a9a4","Node":"consul-1","Address":"172.16.66.102","Datacenter":"dc1","TaggedAddresses":{"lan":"172.16.66.102","wan":"172.16.66.102"},"Meta":{"consul-network-segment":""},"CreateIndex":7,"ModifyIndex":10},
"Service": {"ID":"_nomad-task-5uxc3b7hjzivbklslt4yj5bpsfagibrb","Service":"httpbackend","Tags":[],"Address":"172.16.66.102","Meta":null,"Port":23578,"Weights":{"Passing":1,"Warning":1},"EnableTagOverride":false,"ProxyDestination":"","Proxy":{},"Connect":{},"CreateIndex":30727,"ModifyIndex":30727},
"Checks": [{"Node":"consul-1","CheckID":"serfHealth","Name":"Serf Health Status","Status":"passing","Notes":"","Output":"Agent alive and reachable","ServiceID":"","ServiceName":"","ServiceTags":[],"Definition":{},"CreateIndex":7,"ModifyIndex":7}]
},
{
"Node": {"ID":"6795cd2c-fad5-9d4f-2531-13b0a65e0893","Node":"consul-2","Address":"172.16.66.103","Datacenter":"dc1","TaggedAddresses":{"lan":"172.16.66.103","wan":"172.16.66.103"},"Meta":{"consul-network-segment":""},"CreateIndex":5,"ModifyIndex":5},
"Service": {"ID":"_nomad-task-hvqnbklzqr6q5mpspqcqbnhxdil4su4d","Service":"httpbackend","Tags":[],"Address":"172.16.66.103","Meta":null,"Port":22819,"Weights":{"Passing":1,"Warning":1},"EnableTagOverride":false,"ProxyDestination":"","Proxy":{},"Connect":{},"CreateIndex":30725,"ModifyIndex":30725},
"Checks": [{"Node":"consul-2","CheckID":"serfHealth","Name":"Serf Health Status","Status":"passing","Notes":"","Output":"Agent alive and reachable","ServiceID":"","ServiceName":"","ServiceTags":[],"Definition":{},"CreateIndex":8,"ModifyIndex":8}]
}
]
```


## 三. 将服务暴露到外部以及负载均衡

集群内部的东西向流量可以通过consul的服务发现来实现，南北向流量则需要我们将部分服务暴露到外部才能实现流量导入。在[《基于consul实现微服务的服务发现和负载均衡》](https://tonybai.com/2018/09/10/setup-service-discovery-and-load-balance-based-on-consul/)一文中，我们是通过[nginx](https://tonybai.com/tag/nginx)实现服务暴露和负载均衡的，但是需要[consul-template](https://github.com/hashicorp/consul-template)的协助，并且自己需要实现一个nginx的配置模板，门槛较高也比较复杂。

nomad的官方文档推荐了[fabio](https://github.com/fabiolb/fabio)这个反向代理和负载均衡工具。fabio最初由位于荷兰的“[eBay Classifieds Group](https://www.ebayclassifiedsgroup.com/)”开发，它为荷兰（marktplaats.nl），澳大利亚（gumtree.com.au）和意大利（www.kijiji.it）的一些最大网站提供支持。自2015年9月以来，它为这些站点提供23000个请求/秒的处理能力(性能应对一般中等流量是没有太大问题的)，没有发现重大问题。

与consul-template+nginx的组合不同，fabio无需开发人员做任何二次开发，也不需要自定义模板，它直接从consul读取service list并生成相关路由。至于哪些服务要暴露在外部，路由形式是怎样的，是需要在服务启动时为服务设置特定的tag，fabio定义了一套灵活的路由匹配描述方法。

下面我们就来部署fabio，并将上面的httpbackend暴露到外部。

### 1. 部署fabio

fabio也是nomad集群的一个工作负载，因此我们可以像普通job那样部署fabio。我们先来使用nomad官方文档中给出fabio.nomad：

```
//fabio.nomad
job "fabio" {
datacenters = ["dc1"]
type = "system"
group "fabio" {
task "fabio" {
driver = "docker"
config {
image = "fabiolb/fabio"
network_mode = "host"
logging {
type = "json-file"
}
}
resources {
cpu = 200
memory = 128
network {
mbits = 20
port "lb" {
static = 9999
}
port "ui" {
static = 9998
}
}
}
}
}
}
```


这里有几点值得注意：

-
fabio job的类型是”system”，也就是说该job会被部署到job可以匹配到（通过设定的约束条件）的所有nomad client上，且每个client上仅部署一个实例，有些类似于k8s的daemonset控制下的pod；

-
network_mode = “host” 告诉fabio的驱动docker：fabio容器使用host网络，即与主机同网络namespace；

-
static = 9999和static = 9998，说明fabio在每个nomad client上监听固定的静态端口而不是使用动态端口。这也要求了每个nomad client上不允许存在与fabio端口冲突的应用启动。


我们来plan和run一下这个fabio job：

```
# nomad job plan fabio.nomad
+ Job: "fabio"
+ Task Group: "fabio" (3 create)
+ Task: "fabio" (forces create)
Scheduler dry-run:
- All tasks successfully allocated.
Job Modify Index: 0
To submit the job with version verification run:
nomad job run -check-index 0 fabio.nomad
When running the job with the check-index flag, the job will only be run if the
server side version matches the job modify index returned. If the index has
changed, another user has modified the job and the plan's results are
potentially invalid.
# nomad job run fabio.nomad
==> Monitoring evaluation "97bfc16d"
Evaluation triggered by job "fabio"
Allocation "1b77dcfa" created: node "c281658a", group "fabio"
Allocation "da35a778" created: node "7acdd7bc", group "fabio"
Allocation "fc915ab7" created: node "9e3ef19f", group "fabio"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "97bfc16d" finished with status "complete"
```


查看一下fabio job的运行状态：

```
# nomad job status fabio
ID = fabio
Name = fabio
Submit Date = 2019-03-27T14:30:29+08:00
Type = system
Priority = 50
Datacenters = dc1
Status = running
Periodic = false
Parameterized = false
Summary
Task Group Queued Starting Running Failed Complete Lost
fabio 0 0 3 0 0 0
Allocations
ID Node ID Task Group Version Desired Status Created Modified
1b77dcfa c281658a fabio 0 run running 1m11s ago 58s ago
da35a778 7acdd7bc fabio 0 run running 1m11s ago 54s ago
fc915ab7 9e3ef19f fabio 0 run running 1m11s ago 58s ago
```


通过9998端口，可以查看fabio的ui页面，这个页面主要展示的是fabio生成的路由信息：

![img{512x368}](../../assets/4482b593aba1f5f0.png)


由于尚未暴露任何服务，因此fabio的路由表为空。

fabio的流量入口为9999端口，不过由于没有配置路由和upstream service，因此如果此时向9999端口发送http请求，将会得到404的应答。

### 2. 暴露HTTP服务到外部

接下来，我们就将上面创建的httpbackend服务通过fabiolb暴露到外部，使得特定条件下通过fabiolb进入集群内部的流量可以被准确路由到集群中的httpbackend实例上面。

下面是fabio将nomad集群内部服务暴露在外部的原理图：

![img{512x368}](../../assets/0933b00d70445ebb.png)


我们看到原理图中最为关键的一点就是service tag，该信息由nomad在创建job时写入到consul集群；fabio监听consul集群service信息变更，读取有新变动的job，解析job的service tag，生成路由规则。fabio关注所有带有”urlprefix-”前缀的service tag。

fabio启动时监听的9999端口，默认是http接入。我们修改一下之前的httpbackend.nomad，为该job中的service增加tag字段：

```
// httpbackend.nomad
... ...
service {
name = "httpbackend"
tags = ["urlprefix-mysite.com:9999/"]
port = "http"
check {
name = "alive"
type = "http"
path = "/"
interval = "10s"
timeout = "2s"
}
}
```


对于上面httpbackend.nomad中service块的变更，主要有两点：

1) 增加tag：匹配的路由信息为：“mysite.com:9999/”

2) 增加check块：如果没有check设置，该路由信息将不会在fabio中生效

更新一下httpbackend:

```
# nomad job run httpbackend-2.nomad
==> Monitoring evaluation "c83af3d3"
Evaluation triggered by job "httpbackend"
Allocation "6b0b83de" modified: node "9e3ef19f", group "httpbackend"
Allocation "d0710b85" modified: node "7acdd7bc", group "httpbackend"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "c83af3d3" finished with status "complete"
```


查看fabio的route表，可以看到增加了两条新路由信息：

![img{512x368}](../../assets/375ad96ad48c1c52.png)


我们通过fabio来访问一下httpbackend服务：

```
# curl http://mysite.com:9999/ --- 注意：事先已经在/etc/hosts中添加了 mysite.com的地址为127.0.0.1
this is httpbackendservice, version: v1.0.0
```


我们看到httpbackend service已经被成功暴露到lb的外部了。

## 四. 暴露HTTPS、TCP服务到外部

### 1. 定制fabio

我们的目标是将https、tcp服务暴露到lb的外部，nomad官方文档中给出的fabio.nomad将不再适用，我们需要让fabio监听多个端口，每个端口有着不同的用途。同时，我们通过给fabio传入适当的命令行参数来帮助我们查看fabio的详细access日志信息，并让fabio支持[TRACE机制](https://github.com/fabiolb/fabio/wiki/Features#request-tracing)。

fabio.nomad调整如下：

```
job "fabio" {
datacenters = ["dc1"]
type = "system"
group "fabio" {
task "fabio" {
driver = "docker"
config {
image = "fabiolb/fabio"
network_mode = "host"
logging {
type = "json-file"
}
args = [
"-proxy.addr=:9999;proto=http,:9997;proto=tcp,:9996;proto=tcp+sni",
"-log.level=TRACE",
"-log.access.target=stdout"
]
}
resources {
cpu = 200
memory = 128
network {
mbits = 20
}
}
}
}
}
```


我们让fabio监听三个端口：

-
9999: http端口

-
9997: tcp端口

-
9996: tcp+sni端口


后续会针对这三个端口暴露的不同服务做细致说明。

我们将fabio的日志级别调低为TRACE级别，以便能查看到fabio日志中输出的trace信息，帮助我们进行路由匹配的诊断。

重新nomad job run fabio.nomad后，我们来看看TRACE的效果：

```
//访问后端服务，在http header中添加"Trace: abc"：
# curl -H 'Trace: abc' 'http://mysite.com:9999/'
this is httpbackendservice, version: v1.0.0
//查看fabio的访问日志：
2019/03/30 08:13:15 [TRACE] abc Tracing mysite.com:9999/
2019/03/30 08:13:15 [TRACE] abc Matching hosts: [mysite.com:9999]
2019/03/30 08:13:15 [TRACE] abc Match mysite.com:9999/
2019/03/30 08:13:15 [TRACE] abc Routing to service httpbackend on http://172.16.66.102:23578/
127.0.0.1 - - [30/Mar/2019:08:13:15 +0000] "GET / HTTP/1.1" 200 44
```


我们可以清晰的看到fabio收到请求后，匹配到一条路由：”mysite.com:9999/”，然后将http请求转发到 172.16.66.102:23578这个httpbackend服务实例上去了。

### 2. https服务

接下来，我们考虑将一个https服务暴露在lb外部。

一种方案是fabiolb做ssl termination，然后再在与upstream https服务建立的ssl连接上传递数据。这种两段式https通信是比较消耗资源的，fabio要对数据进行两次加解密。

另外一种方案是fabiolb将收到的请求透传给后面的upsteam https服务，由client与upsteam https服务直接建立“安全数据通道”，这个方案我们在后续会提到。

第三种方案，那就是对外依旧暴露http，但是fabiolb与upsteam之间通过https通信。我们先来看一下这种“间接暴露https”的方案。

```
// httpsbackend-upstreamhttps.nomad
job "httpsbackend" {
datacenters = ["dc1"]
type = "service"
group "httpsbackend" {
count = 2
restart {
attempts = 2
interval = "30m"
delay = "15s"
mode = "fail"
}
task "httpsbackend" {
driver = "docker"
config {
image = "bigwhite/httpsbackendservice:v1.0.0"
port_map {
https = 7777
}
logging {
type = "json-file"
}
}
resources {
network {
mbits = 10
port "https" {}
}
}
service {
name = "httpsbackend"
tags = ["urlprefix-mysite-https.com:9999/ proto=https tlsskipverify=true"]
port = "https"
check {
name = "alive"
type = "tcp"
path = "/"
interval = "10s"
timeout = "2s"
}
}
}
}
}
```


我们将创建名为httpsbackend的job，job中Task对应的tag为：”urlprefix-mysite-https.com:9999/ proto=https tlsskipverify=true”。解释为：路由mysite-https.com:9999/，上游upstream服务为https服务，fabio不验证upstream服务的公钥数字证书。

我们创建该job：

```
# nomad job run httpsbackend-upstreamhttps.nomad
==> Monitoring evaluation "ba7af6d4"
Evaluation triggered by job "httpsbackend"
Allocation "3127aac8" created: node "7acdd7bc", group "httpsbackend"
Allocation "b5f1b7a7" created: node "9e3ef19f", group "httpsbackend"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "ba7af6d4" finished with status "complete"
```


我们来通过fabiolb访问一下httpsbackend这个服务：

```
# curl -H "Trace: abc" http://mysite-https.com:9999/
this is httpsbackendservice, version: v1.0.0
// fabiolb 日志
2019/03/30 09:35:48 [TRACE] abc Tracing mysite-https.com:9999/
2019/03/30 09:35:48 [TRACE] abc Matching hosts: [mysite-https.com:9999]
2019/03/30 09:35:48 [TRACE] abc Match mysite-https.com:9999/
2019/03/30 09:35:48 [TRACE] abc Routing to service httpsbackend on https://172.16.66.103:29248
127.0.0.1 - - [30/Mar/2019:09:35:48 +0000] "GET / HTTP/1.1" 200 45
```


### 3. 基于tcp代理暴露https服务

上面的方案虽然将https暴露在外面，但是client到fabio这个环节的数据传输不是在安全通道中。上面提到的方案2：fabiolb将收到的请求透传给后面的upsteam https服务，由client与upsteam https服务直接建立“安全数据通道”似乎更佳。fabiolb支持tcp端口的反向代理，我们基于tcp代理来暴露https服务到外部。

我们建立httpsbackend-tcp.nomad文件，考虑篇幅有限，我们仅列出差异化的部分：

```
job "httpsbackend-tcp" {
... ...
service {
name = "httpsbackend-tcp"
tags = ["urlprefix-:9997 proto=tcp"]
port = "https"
check {
name = "alive"
type = "tcp"
path = "/"
interval = "10s"
timeout = "2s"
}
}
... ...
}
```


从httpsbackend-tcp.nomad文件，我们看到我们在9997这个tcp端口上暴露服务，tag为：“urlprefix-:9997 proto=tcp”，即凡是到达9997端口的流量，无论应用协议类型是什么，都转发到httpsbackend-tcp上，且通过tcp协议转发。

我们创建并测试一下该方案：

```
# nomad job run httpsbackend-tcp.nomad
# curl -k https://localhost:9997 //由于使用的是自签名证书，所有告诉curl不校验server端公钥数字证书
this is httpsbackendservice, version: v1.0.0
```


### 4. 多个https服务共享一个fabio端口

上面的基于tcp代理暴露https服务的方案还有一个问题，那就是每个https服务都要独占一个fabio listen的端口。那是否可以实现多个https服务使用一个fabio端口，并通过host name route呢？fabio支持tcp+sni的route策略。

SNI, 全称Server Name Indication，即服务器名称指示。它是一个扩展的TLS计算机联网协议。该协议允许在握手过程开始时通过客户端告诉它正在连接的服务器的主机名称。这允许服务器在相同的IP地址和TCP端口号上呈现多个证书，也就是允许在相同的IP地址上提供多个安全HTTPS网站（或其他任何基于TLS的服务），而不需要所有这些站点使用相同的证书。

接下来，我们就来看一下如何在fabio中让多个后端https服务共享一个Fabio服务端口(9996)。我们建立两个job：httpsbackend-sni-1和httpsbackend-sni-2。

```
//httpsbackend-tcp-sni-1.nomad
job "httpsbackend-sni-1" {
... ...
service {
name = "httpsbackend-sni-1"
tags = ["urlprefix-mysite-sni-1.com/ proto=tcp+sni"]
port = "https"
check {
name = "alive"
type = "tcp"
path = "/"
interval = "10s"
timeout = "2s"
}
}
.... ...
}
//httpsbackend-tcp-sni-2.nomad
job "httpsbackend-sni-2" {
... ...
task "httpsbackend-sni-2" {
driver = "docker"
config {
image = "bigwhite/httpsbackendservice:v1.0.1"
port_map {
https = 7777
}
logging {
type = "json-file"
}
}
service {
name = "httpsbackend-sni-2"
tags = ["urlprefix-mysite-sni-2.com/ proto=tcp+sni"]
port = "https"
check {
name = "alive"
type = "tcp"
path = "/"
interval = "10s"
timeout = "2s"
}
}
.... ...
}
```


我们看到与之前的server tag不同的是：这里proto=tcp+sni，即告诉fabio建立sni路由。httpsbackend-sni-2 task与httpsbackend-sni-1不同之处在于其使用image为bigwhite/httpsbackendservice:v1.0.1，为的是能通过https的应答结果，将这两个服务区分开来。

除此之外，我们还看到tag中并不包含端口号了，而是直接采用host name作为路由匹配标识。

创建这两个job：

```
# nomad job run httpsbackend-tcp-sni-1.nomad
==> Monitoring evaluation "af170d98"
Evaluation triggered by job "httpsbackend-sni-1"
Allocation "8ea1cc8d" modified: node "7acdd7bc", group "httpsbackend-sni-1"
Allocation "e16cdc73" modified: node "9e3ef19f", group "httpsbackend-sni-1"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "af170d98" finished with status "complete"
# nomad job run httpsbackend-tcp-sni-2.nomad
==> Monitoring evaluation "a77d3799"
Evaluation triggered by job "httpsbackend-sni-2"
Allocation "32df450c" modified: node "c281658a", group "httpsbackend-sni-2"
Allocation "e1bf4871" modified: node "7acdd7bc", group "httpsbackend-sni-2"
Evaluation status changed: "pending" -> "complete"
==> Evaluation "a77d3799" finished with status "complete"
```


我们来分别访问这两个服务：

```
# curl -k https://mysite-sni-1.com:9996/
this is httpsbackendservice, version: v1.0.0
# curl -k https://mysite-sni-2.com:9996/
this is httpsbackendservice, version: v1.0.1
```


从返回的结果我们看到，通过9996，我们成功暴露出两个不同的https服务。

## 五. 小结

到这里，我们实现了我们的既定目标：

-
使用nomad实现了工作负载的创建和调度；

-
东西向流量通过consul机制实现；

-
通过fabio实现了http、https(through tcp)、多https(though tcp+sni)的服务暴露和负载均衡。


后续我们将进一步探索基于nomad实现负载的多种场景的升降级操作(滚动、金丝雀、蓝绿部署)、对非host网络的支持（比如weave network)等。

本文涉及到的源码文件在[这里](https://github.com/bigwhite/experiments/tree/master/nomad-demo/part1/jobs)可以下载。

## 六. 参考资料

[使用Nomad构建弹性基础设施：nomad调度](https://www.hashicorp.com/blog/resilient-infrastructure-with-nomad-scheduling)[使用Nomad构建弹性基础设施：重启任务](https://www.hashicorp.com/blog/resilient-infrastructure-with-nomad-restarting-tasks)[使用Nomad构建弹性基础设施: job生命周期](https://www.hashicorp.com/blog/building-resilient-infrastructure-with-nomad-job-lifecycle)[使用Nomad构建弹性基础设施：容错和自我修复](https://www.hashicorp.com/blog/resilient-infrastructure-with-nomad-fault-tolerance-outage-recovery)[fabio参考指南](https://fabiolb.net/ref/)

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

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

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

HashiCorp 是个很牛的公司，很喜欢他家的 Vagrant 和 Terraform，不过 Nomad 这一套搭下来，不比 k8s 轻松啊

正如您说的，如果要通过nomad把k8s实现的大部分主流功能都搭完，肯定不比搭建一个k8s轻松。但nomad好在满足开发者/运维者的“递进式”需求。如果我仅需要一个简单的集群管理，nomad可以快速满足。而不用非得安装一个“五脏俱全”的k8s。尤其是面对规模较小的、运维需求没那么复杂的环境，nomad多数情况下够用了。

HashiCorp出口管制了吧~

开源版不再管制范围之列。只有企业版才被管制。而且据说是因为不满足中国地区关于加密算法的要求而不允许售卖。不是美帝政府对其管制。