---
title: Docker 1.12 swarm模式下遇到的各种问题
url: https://tonybai.com/2016/10/11/some-problems-under-swarm-mode-in-docker-1-12/
published: '2016-10-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Docker 1.12 swarm模式下遇到的各种问题

前段时间，由于工作上的原因，与[Docker](http://tonybai.com/tag/docker)的联系发生了几个月的中断^_^，从10月份开始，工作中又与Docker建立了广泛密切的联系。不过这次，Docker却给我泼了一盆冷水:(。事情的经过请允许多慢慢道来。

经过几年的开发，[Docker](https://www.docker.com/)已经成为轻量级容器领域不二的事实标准，应用范围以及社区都在快速发展和壮大。今年的年中，Docker发布了其里程碑的版本[Docker 1.12](https://github.com/docker/docker/releases/tag/v1.12.0)，该版本最大的变动就在于其引擎自带了swarmkit ，一款Docker开发的容器集群管理工具，可以让用户无需安装第三方公司提供的工具或Docker公司提供的引擎之外的工具，就能搭建并管理好一个容器集群，并兼有负载均衡、服务发现和服务编排管理等功能。这对于容器生态圈内的企业，尤其是那些做容器集群管理和服务编排平台的公司来说，不亚于当年微软在Windows操作系统中集成Internet Explorer。对此，网上和社区对Docker口诛笔伐之声不绝于耳，认为Docker在亲手打击社区，葬送大好前程。关于商业上的是是非非，我们这里暂且不提。不可否认的是，对于容器的普通用户而言，Docker引擎内置集群管理功能带来的更多是便利。

9月末启动的一款新产品的开发中，决定使用容器技术，需要用到容器的集群管理以及服务伸缩、服务发现、负载均衡等特性。鉴于团队的能力和开发时间约束，初期我们确定直接利用Docker 1.12版本提供的这些内置特性，而不是利用第三方，诸如[k8s](http://kubernetes.io/)或[Rancher](http://tonybai.com/2016/04/14/an-introduction-about-rancher/)这样的第三方容器集群管理工具或是手工利用各种开源组件“拼凑”出一套满足需求的集群管理系统，如利用[consul](http://tonybai.com/2015/07/06/implement-distributed-services-registery-and-discovery-by-consul/)做服务注册和发现等。于是Docker 1.12的集群模式之旅就开始了。

#### 一、环境准备

这次我们直接使用的是阿里的公有云虚拟主机服务，这里使用两台aliyun ECS：

manager: 10.46.181.146/21(内网)

worker: 10.47.136.60/22 (内网）

系统版本为：

```
Ubuntu 14.04.4:
Linux iZ25cn4xxnvZ 3.13.0-86-generic #130-Ubuntu SMP Mon Apr 18 18:27:15 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
```


Docker版本：

```
# docker version
Client:
Version: 1.12.1
API version: 1.24
Go version: go1.6.3
Git commit: 23cf638
Built: Thu Aug 18 05:22:43 2016
OS/Arch: linux/amd64
Server:
Version: 1.12.1
API version: 1.24
Go version: go1.6.3
Git commit: 23cf638
Built: Thu Aug 18 05:22:43 2016
OS/Arch: linux/amd64
```


在[Ubuntu](http://tonybai.com/tag/ubuntu)上Docker的安装日益方便了，我个人习惯于采用daocloud推荐的方式，在[这里](http://get.daocloud.io/#install-docker)可以看到。当然你也可以参考Docker[官方的doc](https://docs.docker.com/engine/installation/linux/ubuntulinux/)。

如果你的Ubuntu上已经安装了old版的Docker，也可以在docker的github上下载相应平台的二进制包，覆盖本地版本即可（注意1.10.0版本前后的Docker组件有所不同）。

#### 二、Swarm集群搭建

Docker 1.12内置swarm mode，即docker原生支持的docker容器集群管理模式，只要是执行了docker swarm init或docker swarm join到一个swarm cluster中，执行了这些命令的host上的docker engine daemon就进入了swarm mode。

swarm mode中，Docker进行了诸多抽象概念（这些概念与k8s、rancher中的概念大同小异，也不知是谁参考了谁^_^）：

```
- node: 部署了docker engine的host实例，既可以是物理主机，也可以是虚拟主机。
- service: 由一系列运行于集群容器上的tasks组成的。
- task: 在具体某个docker container中执行的具体命令。
- manager: 负责维护docker cluster的docker engine，通常有多个manager在集群中，manager之间通过raft协议进行状态同步，当然manager角色engine所在host也参与负载调度。
- worker: 参与容器集群负载调度，仅用于承载tasks。
```


swarm mode下，一个Docker原生集群至少要有一个manager，因此第一步我们就要初始化一个swarm cluster：

```
# docker swarm init --advertise-addr 10.46.181.146
Swarm initialized: current node (c7vo4qtb2m41796b4ji46n9uw) is now a manager.
To add a worker to this swarm, run the following command:
docker swarm join \
--token SWMTKN-1-1iwaui223jy6ggcsulpfh1bufn0l4oq97zifbg8l5na914vyz5-2mg011xh7vso9hu7x542uizpt \
10.46.181.146:2377
To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```


通过一行swarm init命令，我们就创建了一个swarm集群。同时，Docker daemon给出了清晰提示，如果要向swarm集群添加worker node，执行上述提示中的语句。如果其他node要以manager身份加入集群，则需要执行：docker swarm join-token manager以获得下一个“通关密语”^_^。

```
# docker swarm join-token manager
To add a manager to this swarm, run the following command:
docker swarm join \
--token SWMTKN-1-1iwaui223jy6ggcsulpfh1bufn0l4oq97zifbg8l5na914vyz5-8wh5gp043i1cqz4at76wvx29m \
10.46.181.146:2377
```


对比两个“通关密语”，我们发现仅是token串的后半部分有所不同(2mg011xh7vso9hu7x542uizpt vs. 8wh5gp043i1cqz4at76wvx29m)。

在未添加新node之前，我们可以通过docker node ls查看当前集群内的node状态：

```
# docker node ls
ID HOSTNAME STATUS AVAILABILITY MANAGER STATUS
c7vo4qtb2m41796b4ji46n9uw * iZ25mjza4msZ Ready Active Leader
```


可以看出当前swarm仅有一个node，且该node是manager，状态是manager中的leader。

我们现在将另外一个node以worker身份加入到该swarm：

```
# docker swarm join \
--token SWMTKN-1-1iwaui223jy6ggcsulpfh1bufn0l4oq97zifbg8l5na914vyz5-2mg011xh7vso9hu7x542uizpt \
10.46.181.146:2377
This node joined a swarm as a worker.
```


在manager上查看node情况：

```
# docker node ls
ID HOSTNAME STATUS AVAILABILITY MANAGER STATUS
8asff8ta70j91myh734os6ihg iZ25cn4xxnvZ Ready Active
c7vo4qtb2m41796b4ji46n9uw * iZ25mjza4msZ Ready Active Leader
```


Swarm集群中已经有了两个active node：一个manager和一个worker。这样我们的集群环境初建ok。

#### 三、Service启动

Docker 1.12版本宣称提供服务的Scaling、health check、滚动升级等功能，并提供了内置的dns、vip机制，实现service的服务发现和负载均衡能力。接下来，我们来测试一下docker的“服务能力”：

我们先来创建一个用户承载服务的自定义内部overlay网络：

```
root@iZ25mjza4msZ:~# docker network create -d overlay mynet1
avjvpxkfg6u8xt0qd5xynoc28
root@iZ25mjza4msZ:~# docker network ls
NETWORK ID NAME DRIVER SCOPE
dba1faa24c0d bridge bridge local
a2807d0ec7ed docker_gwbridge bridge local
2b6eb8b95c00 host host local
55v43pasf7p9 ingress overlay swarm
avjvpxkfg6u8 mynet1 overlay swarm
6f2d47678226 none null local
```


我们看到在network list中，我们的overlay网络mynet1出现在列表中。这时，在worker node上你还看不到mynet1的存在，因为按照目前docker的机制，只有将归属于mynet1的task调度到worker node上时，mynet1的信息才会同步到worker node上。

接下来就是在mynet1上启动service的时候了，我们先来测试一下：

```
在manager节点上，用docker service命令启动服务mytest：
# docker service create --replicas 2 --name mytest --network mynet1 alpine:3.3 ping baidu.com
0401ri7rm1bdwfbvhgyuwroqn
```


似乎启动成功了，我们来查看一下服务状态：

```
root@iZ25mjza4msZ:~# docker service ps mytest
ID NAME IMAGE NODE DESIRED STATE CURRENT STATE ERROR
73hyxfhafguivtrbi8dyosufh mytest.1 alpine:3.3 iZ25mjza4msZ Ready Preparing 1 seconds ago
c5konzyaeq4myzswthm8ax77w \_ mytest.1 alpine:3.3 iZ25mjza4msZ Shutdown Failed 1 seconds ago "starting container failed: co…"
6umn2qlj34okagb4mldpl6yga \_ mytest.1 alpine:3.3 iZ25mjza4msZ Shutdown Failed 6 seconds ago "starting container failed: co…"
5y7c1uoi73272uxjp2uscynwi \_ mytest.1 alpine:3.3 iZ25mjza4msZ Shutdown Failed 11 seconds ago "starting container failed: co…"
4belae8b8mhd054ibhpzbx63q \_ mytest.1 alpine:3.3 iZ25mjza4msZ Shutdown Failed 16 seconds ago "starting container failed: co…"
```


似乎服务并没有起来，service ps的结果告诉我：出错了！

但从ps的输出来看，ERROR那行的日志太过简略：“starting container failed: co…” ，无法从这里面分析出失败原因，通过docker logs查看失败容器的日志（实际上日志是空的）以及通过syslog查看docker engine的日志都没有特殊的发现。调查了许久，无意中尝试手动重启一下失败的Service task：

```
# docker start 4709dbb40a7b
Error response from daemon: could not add veth pair inside the network sandbox: could not find an appropriate master "ov-000101-46gc3" for "vethf72fc59"
Error: failed to start containers: 4709dbb40a7b
```


从这个Daemon返回的Response Error来看似乎与overlay vxlan的网络驱动有关。又经过搜索引擎的确认，大致确定可能是因为host的kernel version太low导致的，当前kernel是3.13.0-86-generic，记得之前在docker 1.9.1时玩vxlan overlay我是将kernel version升级到3.19以上了。于是决定[升级kernel version](https://github.com/docker/docker/issues/25039)。

```
升级到15.04 ubuntu版本的内核：
命令：
apt-get install linux-generic-lts-vivid
```


升级后：

```
# uname -a
Linux iZ25cn4xxnvZ 3.19.0-70-generic #78~14.04.1-Ubuntu SMP Fri Sep 23 17:39:18 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
```


reboot虚拟机后，重新启动mytest service，这回服务正常启动了。看来升级内核版本这味药是对了症了。

```
这里issue第一个吐槽：Docker强依赖linux kernel提供的诸多feature，但docker似乎在kernel版本依赖这块并未给出十分明确的对应关系，导致使用者莫名其妙的不断遇坑填坑，浪费了好多时间。
```


顺便这里把service的基本管理方式也一并提一下：

scale mytest服务的task数量从2到4：

```
docker service scale mytest=4
```


删除mytest服务：

```
docker service rm mytest
```


服务删除执行后，需要一些时间让docker engine stop and remove container instance。

#### 四、vip机制测试

Docker 1.12通过集群内置的DNS服务实现服务发现，通过vip实现自动负载均衡。单独使用DNS RR机制也可以实现负载均衡，但这种由client端配合实现的机制，无法避免因dns update latency导致的服务短暂不可用的情况。vip机制才是相对理想的方式。

所谓Vip机制，就是docker swarm为每一个启动的service分配一个vip，并在DNS中将service name解析为该vip，发往该vip的请求将被自动分发到service下面的诸多active task上（down掉的task将被自动从vip均衡列表中删除）。

我们用nginx作为backend service来测试这个vip机制，首先在集群内启动mynginx service，内置2个task，一般来说，docker swarm会在manager和worker node上各启动一个container来承载一个task：

```
# docker service create --replicas 2 --name mynginx --network mynet1 --mount type=bind,source=/root/dockertest/staticcontents,dst=/usr/share/nginx/html,ro=true nginx:1.10.1
3n7dlr8km9v2xd66bf0mumh1h
```


一切如预期，swarm在manager和worker上各自启动了一个nginx container:

```
# docker service ps mynginx
ID NAME IMAGE NODE DESIRED STATE CURRENT STATE ERROR
bcyffgo1q3i5x0qia26fs703o mynginx.1 nginx:1.10.1 iZ25mjza4msZ Running Running about a minute ago
arkol2l7gpvq42f0qytqf0u85 mynginx.2 nginx:1.10.1 iZ25cn4xxnvZ Running Running about a minute ago
```


接下来，我们尝试在mynet1中启动一个client container，并在client container中使用ping、curl对mynginx service进行vip机制的验证测试。client container的image是基于ubuntu:14.04 commit的本地image，只是在官方image中添加了curl, dig, traceroute等网络探索工具，读者朋友可自行完成。

我们在manager node上尝试启动client container:

```
# docker run -it --network mynet1 ubuntu:14.04 /bin/bash
docker: Error response from daemon: swarm-scoped network (mynet1) is not compatible with `docker create` or `docker run`. This network can only be used by a docker service.
See 'docker run --help'.
```


可以看到：直接通过docker run的方式在mynet1网络里启动container的方法失败了，docker提示：docker run与swarm范围的网络不兼容。看来我们还得用docker service create的方式来做。

```
# docker service create --replicas 1 --name myclient --network mynet1 test/client tail -f /var/log/bootstrap.log
0eippvade7j5e0zdyr5nkkzyo
# docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
4da6700cdf4d test/client:latest "tail -f /var/log/boo" 33 seconds ago Up 32 seconds myclient.1.3cew8x46i5b28e2q3kd1zz3mq
```


我们使用exec命令attach到client container中：

```
root@iZ25mjza4msZ:~# docker exec -it 4da6700cdf4d /bin/bash
root@4da6700cdf4d:/#
```


在client container中，我们可以通过dig命令查看mynginx service的vip：

```
root@4da6700cdf4d:/# dig mynginx
; <<>> DiG 9.9.5-3ubuntu0.9-Ubuntu <<>> mynginx
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 34806
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
;; QUESTION SECTION:
;mynginx. IN A
;; ANSWER SECTION:
mynginx. 600 IN A 10.0.0.2
;; Query time: 0 msec
;; SERVER: 127.0.0.11#53(127.0.0.11)
;; WHEN: Tue Oct 11 08:58:58 UTC 2016
;; MSG SIZE rcvd: 48
```


可以看到为mynginx service分配的vip是10.0.0.2。

接下来就是见证奇迹的时候了，我们尝试通过curl访问mynginx这个service，预期结果是：请求被轮询转发到不同的nginx container中，返回结果输出不同内容。实际情况如何呢？

```
root@4da6700cdf4d:/# curl mynginx
^C
root@4da6700cdf4d:/# curl mynginx
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title> 主标题 | 副标题< /title>
</head>
<body>
<p>hello world, i am manager</p>
</body>
</html>
root@4da6700cdf4d:/# curl mynginx
curl: (7) Failed to connect to mynginx port 80: Connection timed out
```


第一次执行curl mynginx，curl就hang住了。ctrl+c后，再次执行curl mynginx，顺利返回manager节点上的nginx container的response结果：”hello world, i am manager“。

第三次执行curl mynginx，又hang住了，一段时间后显示timed out，这也从侧面说明了，swarm下的docker engine的确按照rr规则将request均衡转发到不同nginx container，但实际看来，从manager node上的client container到worker node上的nginx container的网络似乎不通。我们来验证一下这两个container间的网络是否ok。

我们在两个node上分别用docker inspect获得client container和nginx container的ip地址：

```
manager node:
client container: 10.0.0.6
nginx container: 10.0.0.4
worker node:
nginx container: 10.0.0.3
```


理论上，位于同一overlay网络中的三个container之间应该是互通的。但实际上通过docker exec -it container_id /bin/bash进入每个docker container内部进行互ping来看，manager node上的两个container可以互相ping通，但无法ping通 worker node上的nginx container，同样，位于worker node上的nginx container也无法ping通位于manager node上的任何container。

通过docker swarm leave将worker节点从swarm cluster中摘出，docker swarm会在manager上再启动一个nginx container，这时如果再再client container测试vip机制，那么测试是ok的。

也就是说我遇到的问题是跨node的swarm network不好用，导致vip机制无法按预期执行。

后续我又试过双swarm manager等方式，vip机制在跨node时均不可用。在docker github的issue中，很多人遇到了同样的问题，涉及的环境也是多种多样（不同内核版本、不同linux发行版，不同公有云提供商或本地虚拟机管理软件），似乎这个问题是随机出现的。 按照docker developer的提示检查了swarm必要端口的开放情况、防火墙、swarm init的传递参数，都是无误的。也尝试过重建swarm，在init和join时全部显式带上–listen-addr和–advertise-addr选项，问题依旧没能解决。

最后，又将docker版本从1.12.1升级到最新发布的docker 1.12.2rc3版本，重建集群，问题依旧没有解决。

自此确定，docker 1.12的vip机制尚不稳定，并且没有临时解决方案能绕过这一问题。

#### 五、Routing mesh机制测试

内部网络的vip机制的测试失败，让我在测试Docker 1.12的另外一个机制：Routing mesh之前心里蒙上了一丝阴影，一个念头油然而生：Routing mesh可能也不好用。

对于外部网络和内部网络的边界，docker 1.12提供了ingress（入口） overlay网络应对，通过routing mesh机制，保证外部的请求可以被任意集群node转发到启动了相应服务container的node中，并保证高

可用。如果有多个container，还可以实现负载均衡的转发。

与vip不同，Routing mesh在启动服务前强调暴露一个node port的概念。既然叫node port，说明这个暴露的port是docker engine listen的，并由docker engine将发到port上的流量转到相应启动了service container的节点上去（如果本node也启动了service task，那么也会负载分担留给自己node上的service task container去处理）。

我们先清除上面的service，还是利用nginx来作为网络入口服务：

```
# docker service create --replicas 2 --name mynginx --network mynet1 --mount type=bind,source=/root/dockertest/staticcontents,dst=/usr/share/nginx/html,ro=true --publish 8091:80/tcp nginx:1.10.1
cns4gcsrs50n2hbi2o4gpa1tp
```


看看node上的8091端口状态：

```
root@iZ25mjza4msZ:~# lsof -i tcp:8091
COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
dockerd 13909 root 37u IPv6 121343 0t0 TCP *:8091 (LISTEN)
```


dockerd负责监听该端口。

接下来，我们在manager node上通过curl来访问10.46.181.146:8091。

```
# curl 10.46.181.146:8091
^C
root@iZ25mjza4msZ:~# curl 10.46.181.146:8091
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title> 主标题 | 副标题< /title>
</head>
<body>
<p>hello world, i am master</p>
</body>
</html>
root@iZ25mjza4msZ:~# curl 10.46.181.146:8091
```


在vip测试中的一幕又出现了，docker swarm似乎再将请求负载分担到两个node上，当分担到worker node上时，curl又hang住了。routing mesh机制失效。

理论上再向swarm cluster添加一个worker node，该node上并未启动nginx service，当访问这个新node的8091端口时，流量也会被转到manager node或之前的那个worker node，但实际情况是，跨node流量互转失效，和vip机制测试似乎是一个问题。

#### 六、小结

Docker 1.12的routing mesh和vip均因swarm network的问题而不可用，这一点出乎我的预料。

翻看Docker在github上的issues，发现类似问题从Docker 1.12发布起就出现很多，近期也有不少：

```
https://github.com/docker/docker/issues/27237
https://github.com/docker/docker/issues/27218
https://github.com/docker/docker/issues/25266
https://github.com/docker/docker/issues/26946
*https://github.com/docker/docker/issues/27016
```


这里除了27016的issue发起者在issue最后似乎顿悟到了什么（也没了下文）：Good news. I believe I discovered the root cause of our issue. Remember above I noted our Swarm spanned across L3 networks? I appears there is some network policy that is blocking VxLAN traffic (4789/udp) across the two L3 networks. I redeployed our same configuration to a single L3 network and can reliably access the published port on all worker nodes (based on a few minutes of testing)。其余的几个issue均未有solution。

不知道我在阿里云的两个node之间是否有阻隔vxlan traffic的什么policy，不过使用nc探测4789 udp端口均是可用的：

```
nc -vuz 10.47.136.60 4789
```


无论是配置原因还是代码bug导致的随机问题，Docker日益庞大的身躯和背后日益复杂的网络机制，让开发者（包括docker自己的开发人员）查找问题的难度都变得越来越高。Docker代码的整体质量似乎也呈现出一定下滑的不良趋势。

针对上述问题，尚未找到很好的解决方案。如果哪位读者能发现其中玄机，请不吝赐教。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

同样也入坑中，问题随机出现。

也就是说swarm mode现在还无法做到自动扩容缩容？？？

截止目前，发现有些问题是我所使用的aliyun的ECS在某些UDP端口的通信上的问题。docker 1.12集群模式在多数Docker 1.12的试验者的反馈结果中是好用的。

阿里云的ECS上是有问题的 内网和青云都OK 唯独阿里云

从你的现象上看，是 overlay 网络的通讯有问题，也就是 VxLAN 的4789/udp 的问题。除了阿里云的问题外，我还注意到你的内核版本不对。你所使用的内核版本是 Ubuntu 15.04 的 3.19，对于 Ubuntu 14.04 来说，现在官方默认的版本应该是 4.4，也就是 16.04 的 xenial 的。你可以用命令：sudo apt-get install -y –install-recommends linux-generic-lts-xenial来安装。在Docker环境中，如果打算使用 overlay network，一般建议使用 4.+ 的内核，现在比较稳定的是 4.2。4.4 的内核现在也可以用。而你选择的 3.19 对于 overlay network 来说太老了。建议你升级内核后在测试一下。我这里碰到别人问到 overlay 的问题的情况，大多是 CentOS 7的老内核的问题，而 Ubuntu 和 CentOS 是不同的，CentOS 一个版本走到底，而 Ubuntu 是官方维护新版本内核的，因此是鼓励升级到lts新版本内核的，所以很少见到 Ubuntu 用户提到 overlay network 的问题，除了设置了防火墙外。

十分感谢你的建议。之所以用3.19内核，是因为在玩docker 1.9.1的overlay network时是好用的，所以就没有继续升级内核。阿里云的udp 4789端口初步测试的确有些问题，但问题原因不明，aliyun的售后也没给出啥说法，就是让我配合他们抓包。后续我再升级内核到4.x版本试试吧。

问题有什么进展么

后来改用kubernetes了。前不久新申请了两个aliyun华东节点，使用docker 1.12搭建swarm cluster依旧有问题。没有继续跟。

由阿里云的售后工程师确认，经典网络4789/udp被底层网络拦截，专有网络VPC下的机器可以4789/udp可以通讯

嗯，从现象看也是阿里云底层的问题。十分感谢。

我也遇到docker swarm 下使用keepalived设置vip，跨node无法ping通的情况，想请问你现在解决了吗？