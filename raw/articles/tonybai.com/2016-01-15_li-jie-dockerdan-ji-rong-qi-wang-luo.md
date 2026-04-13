---
title: 理解Docker单机容器网络
url: https://tonybai.com/2016/01/15/understanding-container-networking-on-single-host/
published: '2016-01-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 理解Docker单机容器网络

[Docker](https://www.docker.com/)容器是近两年最 火的IT技术之一，用“火山爆发式“来形容Docker的成 长也不为过。Docker在产品服务的[devops](https://en.wikipedia.org/wiki/DevOps) 运维、云 计算(CaaS)、大数据以及企业内部应用等领域正在被越来越多的接受和广泛应用。Docker技术的本质在于提升计算密度和提升部署效率，高屋 建瓴的讲，它的出现符合人类社会对绿色发展的追求，降低资源消耗，提升资源的单位利用率。不过经历了两年多的发展，Docker依旧年轻，尚未成 熟，在集群调度、存储、网络、安全等方面，Docker依旧有很长的路要走。

在一年多以前，也就是[Docker发布1.0](http://blog.docker.com/2014/06/its-here-docker-1-0/)后没几个月时，我曾经学习过一段时间的[Docker](http://tonybai.com/tag/docker)，主要学习Docker的概念和基本使用方法。由于当时docker 还相对“稚嫩”，在产品和项目中暂无用武之地，也就没有深入，但对Docker技术的跟踪倒是没有停下来。今年[Docker 1.9发布](https://blog.docker.com/2015/11/docker-1-9-production-ready-swarm-multi-host-networking/)，支持跨主机container netwoking；第三方容器集群调度和服务编织工具蓬勃发展，如[Kubernetes](http://kubernetes.io/) 、[mesos](http://mesos.apache.org/)、 [flannel](https://github.com/coreos/flannel)以及[rancher](http://rancher.com/)等；国内基于Docker的云服 务及产品也 如雨后春笋般发展开来。虽然不到2年，但Docker的演进速度是飞快的，要想跟的上Docker的步伐，仅仅跟踪技术信息是不够的，对伴生 Docker发展起来的一些新理念、新技术、新方案需要更深入的理解，这便是这篇文章（以及后续关于这个主题文章）编写的初衷。

我计划从容器网络开始，我们先来看看单机容器网络。

### 一、目标

Docker实质上是汇集了linux容器（各种namespaces）、cgroups以及“叠加”类文件系统等多种核心技术的一种复合技术。 其默认容器网络的建立和控制是一种结合了network namespace、iptables、linux网桥、route table等多种Linux内核技术的综合方案。理解Docker容器网络，首先是以对TCP/IP网络体系的理解为前提的，不过也不需要多深刻，大学本 科学的那套“计算机网络”足矣^_^，另外还要考虑Linux上对虚拟网络设备实现的独特性（区分于硬件网络设备）。

本篇文章主要针对单机Docker容器网络，目的是了解Docker容器网络中容器与容器间通信、容器与宿主机间通信、容器与宿主机所在的物理网 络中主机通信、容器网络控制等机制，为后续理解跨主机容器网络的理解打下基础。同时稍带利用工具对Docker容器网络的网络性能做初步测量，通 过直观数据初步评估容器网络的适用性。

### 二、试验环境以及拓扑

本文试验环境如下：

```
- 宿主机 Ubuntu 12.04 x86_64 3.13.0-61-generic
- 容器OS：基于Ubuntu 14.04 Server x86_64的自制image
- Docker版本 - v1.9.1 for linux/amd64
```


为了试验方便，这里基于官方[ubuntu](http://tonybai.com/tag/ubuntu):14.04 image制作了带有traceroute、brctl以及tcpdump等网络调试工具的image，简单起见（考虑到公司内网代理），这里就没有写 Dockerfile(即便写也很简单)，而是直接z在容器内apt-get install后，再通过docker commit基于已经安装好上述工具的container创建的一个新image：

```
$sudo docker commit 0580adb079a3 dockernetworking/ubuntu:14.04
a692757cbb7bd7d8b70f393930e954cce625934485e93cf1b28c15efedb5f2d3
$ docker images
REPOSITORY TAG IMAGE ID CREATED VIRTUAL SIZE
dockernetworking/ubuntu 14.04 a692757cbb7b 5 seconds ago 302.1 MB
```


后续的container均是基于dockernetworking/ubuntu创建的。

另外试验环境的拓扑图如下：

![img{500x428}](../../assets/77140c1112e01b2d.jpg)


从拓扑图中我们可以看到，物理宿主机为10.10.126.101，置于物理局域网10.10.126.0/24中。在宿主机上我们创建了两 个 Container：Container1和Container2，Container所用网段为172.17.0.0/16。

### 三、Docker Daemon初始网络

当你在一个clean环境下，启动Docker daemon后，比如在Ubuntu下，使用sudo service docker start，Docker Daemon就会初始化后续创建容器时所需的基础网络设备和配置。

以下是从宿主机的角度看到的：

```
// 网桥
$ brctl show
bridge name bridge id STP enabled interfaces
docker0 8000.0242f9f8c9ad no
// 网络设备
$ ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
link/ether 2c:59:e5:01:98:28 brd ff:ff:ff:ff:ff:ff
... ...
5: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
link/ether 02:42:f9:f8:c9:ad brd ff:ff:ff:ff:ff:ff
// 网络设备ip地址
$ ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
link/ether 2c:59:e5:01:98:28 brd ff:ff:ff:ff:ff:ff
inet 10.10.126.101/24 brd 10.10.126.255 scope global eth0
valid_lft forever preferred_lft forever
inet6 fe80::2e59:e5ff:fe01:9828/64 scope link
valid_lft forever preferred_lft forever
... ...
5: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
link/ether 02:42:f9:f8:c9:ad brd ff:ff:ff:ff:ff:ff
inet 172.17.0.1/16 scope global docker0
valid_lft forever preferred_lft forever
inet6 fe80::42:f9ff:fef8:c9ad/64 scope link
valid_lft forever preferred_lft forever
```


可以看出，与Docker Daemon启动前相比，宿主物理机中多出来一个虚拟网络设备：docker0。

docker0是一个标准Linux虚拟网桥设备。在Docker默认的桥接网络工作模式中，docker0网桥起到了至关重要的作用。物理网桥 是标准的二层网络设备，一般说，标准物理网桥只有两个网口，可以将两个物理网络（区分以IP为寻址单位的逻辑网络）连接在一起。但与物理层设备集 线器等相比，网桥具备隔离冲突域的功能。网桥通过MAC地址学习和泛洪的方式实现二层相对高效的通信。在今天，标准网桥设备已经基本被淘汰了，替 代网桥的是是二层交换机。二层交换机也可以看成一个多口网桥。在不划分vlan的前提下，可以将其当做两两端口间都是独立通道的”hub”使用。

前面说过docker0是一个标准Linux虚拟网桥设备，即一个以软件实现的网桥，由于其支持多口，实际上它算是一个虚拟交换机设备。与物理网 桥不同的是，它不但可以二层转发包，还可以将包送到用户层进行处理。在我们尚未创建container的时候，docker0以一个Linux网 络设 备的身份存在，并且Linux虚拟网桥可以配置IP，可以作为在三层网络上的一个Gateway，在主机眼中和物理网口设备eth0区别不大。与 Linux其他网络设备也可以在三层相互通信，前提是Docker Daemon打开了ip包转发功能：

```
$ cat /proc/sys/net/ipv4/ip_forward
1
```


宿主机的路由表也增加了一条路由(见最后一条)：

```
$ ip route
default via 10.10.126.1 dev eth0 proto static
10.10.126.0/24 dev eth0 proto kernel scope link src 10.10.126.101 metric 1
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
```


除此之外，Docker Daemon还设置了若干iptables规则以管理containers间的通信以及辅助container访问外部网络（NAT转换）：

```
sudo iptables-save > ./iptables.init.rules
# Generated by iptables-save v1.4.12 on Wed Jan 13 17:25:55 2016
*raw
: PREROUTING ACCEPT [9469:2320376]
:OUTPUT ACCEPT [2990:1335235]
COMMIT
# Completed on Wed Jan 13 17:25:55 2016
# Generated by iptables-save v1.4.12 on Wed Jan 13 17:25:55 2016
*filter
:INPUT ACCEPT [1244:341290]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [483:153047]
: DOCKER - [0:0]
-A FORWARD -o docker0 -j DOCKER
-A FORWARD -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i docker0 ! -o docker0 -j ACCEPT
-A FORWARD -i docker0 -o docker0 -j ACCEPT
COMMIT
# Completed on Wed Jan 13 17:25:55 2016
# Generated by iptables-save v1.4.12 on Wed Jan 13 17:25:55 2016
*nat
: PREROUTING ACCEPT [189:88629]
:INPUT ACCEPT [111:60817]
:OUTPUT ACCEPT [23:1388]
: POSTROUTING ACCEPT [23:1388]
: DOCKER - [0:0]
-A PREROUTING -m addrtype --dst-type LOCAL -j DOCKER
-A OUTPUT ! -d 127.0.0.0/8 -m addrtype --dst-type LOCAL -j DOCKER
-A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
COMMIT
# Completed on Wed Jan 13 17:25:55 2016
```


[iptables](https://en.wikipedia.org/wiki/iptables)是Linux内核自带的包过滤防火墙，支持[NAT](https://en.wikipedia.org/wiki/Network_address_translation)等诸多功能。iptables由表和规则chain概念组成，Docker中所 用的表包括filter表和nat表（参见上述命令输出结果），这也是iptables中最常用的两个表。iptables是一个复杂的存在，曾 有一本书《[linux firewalls](http://book.douban.com/subject/2148593/)》 专门讲解iptables，这里先借用本书 中的一幅图来描述一下ip packets在各个表和chain之间的流转过程：

![img{500x165}](../../assets/a2ffc26ba659acd3.jpg)


网卡收到的数据包进入到iptables后，做路由选择，本地的包通过INPUT链送往user层应用；转发到其他网口的包通过FORWARD chain；本地产生的数据包在路由选择后，通过OUTPUT chain；最后POSTROUTING chain多用于source nat转换。

iptables在容器网络中最重要的两个功能：

1、限制container间的通信

2、将container到外部网络包的源地址换成宿主主机地址(MASQUERADE)

后续还会在详细描述容器通信流程中还会掺杂说明iptables的规则在容器通信中的作用。

### 四、准备工作：让iptables输出log

iptables在Docker单机容器默认网络工作模式下扮演着重要的角色，并且由于是虚拟设备网络，数据的流转是十分复杂的，为了便于跟踪 iptables在docker容器网络数据通信过程中起到的作用，这里在默认iptables规则的基础上，做一些调整，在关键位置输出一些 log，以便调试和理解，这些修改不会影响iptables对数据包的匹配和操作。注意：在操作iptables前，建议通过iptables- save命令备份一份iptables的配置数据。

iptables自身就支持LOG target，日志会输出到/var/log/syslog或kern.log中。我们的目标就是在关键节点输出iptables的数据日志。考虑到日志 量较大，我们仅拦截icmp包（ping)以及tcp 源端口或目的端口为12580的数据。

考虑到篇幅有限，这里仅给出配置后导出的iptables.final.rules，需要的同学可以通过iptables-restore < iptables.final.rules导入。

```
# Generated by iptables-save v1.4.12 on Thu Jan 14 09:28:43 2016
*raw
: PREROUTING ACCEPT [788:127290]
:OUTPUT ACCEPT [574:100918]
-A PREROUTING -p tcp -m tcp --dport 12580 -j LOG --log-prefix "[TonyBai]-RawPrerouting:" --log-level 7
-A PREROUTING -p tcp -m tcp --sport 12580 -j LOG --log-prefix "[TonyBai]-RawPrerouting:" --log-level 7
-A OUTPUT -p tcp -m tcp --dport 12580 -j LOG --log-prefix "[TonyBai]-RawOutput:" --log-level 7
-A OUTPUT -p tcp -m tcp --sport 12580 -j LOG --log-prefix "[TonyBai]-RawOutput:" --log-level 7
COMMIT
# Completed on Thu Jan 14 09:28:43 2016
# Generated by iptables-save v1.4.12 on Thu Jan 14 09:28:43 2016
*filter
:INPUT ACCEPT [284:49631]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [81:28047]
: DOCKER - [0:0]
:FwdId0Od0 - [0:0]
:FwdId0Ond0 - [0:0]
:FwdOd0 - [0:0]
-A INPUT ! -i lo -p icmp -j LOG --log-prefix "[TonyBai]-EnterFilterInput:" --log-level 7
-A INPUT -p tcp -m tcp --dport 12580 -j LOG --log-prefix "[TonyBai]-FilterInput:" --log-level 7
-A INPUT -p tcp -m tcp --sport 12580 -j LOG --log-prefix "[TonyBai]-FilterInput:" --log-level 7
-A FORWARD -o docker0 -j DOCKER
-A FORWARD -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j FwdOd0
-A FORWARD -i docker0 ! -o docker0 -j FwdId0Ond0
-A FORWARD -i docker0 -o docker0 -j FwdId0Od0
-A OUTPUT ! -s 127.0.0.1/32 -p icmp -j LOG --log-prefix "[TonyBai]-EnterFilterOutput:" --log-level 7
-A OUTPUT -p tcp -m tcp --dport 12580 -j LOG --log-prefix "[TonyBai]-FilterOutput:" --log-level 7
-A OUTPUT -p tcp -m tcp --sport 12580 -j LOG --log-prefix "[TonyBai]-FilterOutput:" --log-level 7
-A FwdId0Od0 -i docker0 -o docker0 -j LOG --log-prefix "[TonyBai]-FwdId0Od0:" --log-level 7
-A FwdId0Od0 -i docker0 -o docker0 -j ACCEPT
-A FwdId0Ond0 -i docker0 ! -o docker0 -j LOG --log-prefix "[TonyBai]-FwdId0Ond0:" --log-level 7
-A FwdId0Ond0 -i docker0 ! -o docker0 -j ACCEPT
-A FwdOd0 -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j LOG --log-prefix "[TonyBai]-FwdOd0:" --log-level 7
-A FwdOd0 -o docker0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
COMMIT
# Completed on Thu Jan 14 09:28:43 2016
# Generated by iptables-save v1.4.12 on Thu Jan 14 09:28:43 2016
*nat
: PREROUTING ACCEPT [37:6070]
:INPUT ACCEPT [20:2585]
:OUTPUT ACCEPT [6:364]
```

OSTROUTING ACCEPT [6:364]
: DOCKER - [0:0]
:LogNatPostRouting - [0:0]
-A PREROUTING -p icmp -j LOG --log-prefix "[TonyBai]-Enter iptables:" --log-level 7
-A PREROUTING -p tcp -m tcp --dport 12580 -j LOG --log-prefix "[TonyBai]-NatPrerouting:" --log-level 7
-A PREROUTING -p tcp -m tcp --sport 12580 -j LOG --log-prefix "[TonyBai]-NatPrerouting:" --log-level 7
-A INPUT ! -i lo -p icmp -j LOG --log-prefix "[TonyBai]-EnterNatInput:" --log-level 7
-A INPUT -p tcp -m tcp --dport 12580 -j LOG --log-prefix "[TonyBai]-NatInput:" --log-level 7
-A INPUT -p tcp -m tcp --sport 12580 -j LOG --log-prefix "[TonyBai]-NatInput:" --log-level 7
-A OUTPUT ! -d 127.0.0.0/8 -m addrtype --dst-type LOCAL -j DOCKER
-A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j LogNatPostRouting
-A LogNatPostRouting -s 172.17.0.0/16 ! -o docker0 -j LOG --log-prefix "[TonyBai]-NatPostRouting:" --log-level 7
-A LogNatPostRouting -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
COMMIT
# Completed on Thu Jan 14 09:28:43 2016


一切就绪，只待对docker网络的分析了。

### 五、容器网络

现在我们来启动容器。根据试验环境拓扑图，我们需要创建和启动两个容器：container1和container2。

```
$ docker run -it --name container1 dockernetworking/ubuntu:14.04 /bin/bash
$ docker run -it --name container2 dockernetworking/ubuntu:14.04 /bin/bash
$ docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
1104fc63c571 dockernetworking/ubuntu:14.04 "/bin/bash" 7 seconds ago Up 6 seconds container2
8b38131deb28 dockernetworking/ubuntu:14.04 "/bin/bash" 16 seconds ago Up 15 seconds container1
```


容器启动后，从宿主机的视角，可以看到网络配置有如下变化：

```
$ brctl show
bridge name bridge id STP enabled interfaces
docker0 8000.0242f9f8c9ad no veth00855d7
vethee8659f
$ifconfig -a
... ...
veth00855d7 Link encap:以太网 硬件地址 ea:70:65:cf:28:6b
inet6 地址: fe80::e870:65ff:fecf:286b/64 Scope:Link
UP BROADCAST RUNNING MULTICAST MTU:1500 跃点数:1
接收数据包:8 错误:0 丢弃:0 过载:0 帧数:0
发送数据包:37 错误:0 丢弃:0 过载:0 载波:0
碰撞:0 发送队列长度:0
接收字节:648 (648.0 B) 发送字节:5636 (5.6 KB)
vethee8659f Link encap:以太网 硬件地址 fa:30:bb:0b:1d:eb
inet6 地址: fe80::f830:bbff:fe0b:1deb/64 Scope:Link
UP BROADCAST RUNNING MULTICAST MTU:1500 跃点数:1
接收数据包:61 错误:0 丢弃:0 过载:0 帧数:0
发送数据包:82 错误:0 丢弃:0 过载:0 载波:0
碰撞:0 发送队列长度:0
接收字节:5686 (5.6 KB) 发送字节:9678 (9.6 KB)
... ...
```


Docker Daemon创建了两个veth网络设备，并将veth挂接到docker0网桥上了。veth是一种虚拟网卡设备，创建时成对(veth pair)出现，从一个veth peer发出的数据包可以到达其pair peer。不过从上面命令输出来看，我们似乎并没有看到veth pair，这是因为每个pair的另一peer被放到container的network namespace中了，变成了container中的eth0。veth pair常用于在不同网络命名空间之间通信。在拓扑图中，container1中的eth0与veth-x是一个pair；container2中的 eth0与veth-y是另一个pair。veth-x和veth-y挂接在docker0网桥上，这对于container1和 container2来说，就好比用网线将本地网卡(eth0)与网桥设备docker0的网口连接起来一样。在docker容器网络默认桥接模式 中，veth只是在二层起作用。

下面是从container1内部看到的网络配置：

```
root@8b38131deb28:/# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
47: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.2/16 scope global eth0
valid_lft forever preferred_lft forever
inet6 fe80::42:acff:fe11:2/64 scope link
valid_lft forever preferred_lft forever
root@8b38131deb28:/# netstat -rn
Kernel IP routing table
Destination Gateway Genmask Flags MSS Window irtt Iface
0.0.0.0 172.17.0.1 0.0.0.0 UG 0 0 0 eth0
172.17.0.0 0.0.0.0 255.255.0.0 U 0 0 0 eth0
```


container网络配置很简单，一个eth0网卡，一个loopback口，route表里将网桥作为默认Gateway。

至此，我们拓扑图中的环境已经全部就绪。接下来我们来探索和理解一下容器网络的几种通信流程。

### 六、Docker0的“双重身份”

在正式进入每个通信流程前，我们先来点预备性内容 – 如何理解Docker0。下图中我们给出了Docker0的双重身份，并对比物理交换机，我们来理解一下Docker0这个软网桥。

![img{500x165}](../../assets/e28a4264cb338480.jpg)


#### 1、从容器视角，网桥（交换机）身份

docker0对于通过veth pair“插在”网桥上的container1和container2来说，首先就是一个二层的交换机的角色：泛洪、维护cam表，在二层转发数据包；同 时由于docker0自身也具有mac地址（这个与纯二层交换机不同），并且绑定了ip(这里是172.17.0.1)，因此在 container中还作为container default路由的默认Gateway而存在。

#### 2、从宿主机视角，网卡身份

物理交换机提供了由硬件实现的高效的背板通道，供连接在交换机上的主机高效实现二层通信；对于开启了三层协议的物理交换机而言，其ip路由的处理 也是由物理交换机管理程序提供的。对于docker0而言，其负责处理二层交换机逻辑以及三层的处理程序其实就是宿主机上的Linux内核 tcp/ip协议栈程序。而从宿主机来看，所有docker0从veth（只是个二层的存在，没有绑定ipv4地址）接收到的数据包都会被宿主机 看成从docker0这块网卡（第二个身份，绑定172.17.0.1)接收进来的数据包，尤其是在进入三层时，宿主机上的iptables就会 对docker0进来的数据包按照rules进行相应处理（通过一些内核网络设置也可以忽略docker0 brigde数据的处理）。

在后续的Docker容器网络通信流程分析中，docker0将在这两种身份间来回切换。

### 七、容器网络通信流程

考虑到大部分tcp/ip实现都是在内核实现的ping服务器，这可能会导致iptables流程走不全，影响我们的理解，因此我这里通过tcp 连接建立的握手过程(sync, ack sync, ack)的通信包来理解container网络通信。我们可以简单在服务端启动一个python httpserver: python -m SimpleHTTPServer 12580或用[Go](http://tonybai.com/tag/go)写个简单的http server来监听12580端口；客户端用telnet ip port的方式与服务端建立连接。

iptables的log我们可以在宿主机(ubuntu 12.04)的/var/log/syslog中查看到。考虑到篇幅，头两个例子会作详细说明，后续将简要阐述。

#### 1、container to container

场景：我们在container2(172.17.0.3)中启动监听12580的服务程序，并在container1(172.17.0.2) 中执行：telnet 172.17.0.3 12580。

分析：

我们首先从container1的视角去看。

在container1中无需考虑iptables过程，可以理解为未开启。container1的用户层的数据进入该网络名字空间 (network namespace)的网络协议栈处理。在route decision过程中，协议栈处理程序发现目的地址匹配172.17.0.0/16这条网络路由，该条路由的Flag为U，即该网络为直连链路上的网 络，即无需使用Gateway，直接可以将数据包发到eth0上并封包发出去即可。

由于可以在直连网路链路上找到目的主机，于是二层欲填写的目的mac地址为172.17.0.3这个ip对应的mac。container1在 arp缓存中查询172.17.0.3对应的mac地址。如没有发现172.17.0.3这个ip地址对应的缓存mac地址，则发起一个arp请 求，arp请求的二层目的mac地址填写为二层广播地址：bit全1的mac地址（48bit），并通过eth0发出去。

docker0在这个过程中二层交换机的作用。接收到来自veth上的广播arp请求后，将请求通过二层网络转发到其他docker0上的 veth口上。这时container2收到了arp请求，container2上的以太网驱动程序收到arp请求后，将其发给 container2上的arp协议处理程序(不走iptables)，arp协议处理程序封装arp reply后转出。container1收到reply后，处理二层封包，将container2的mac地址填入以太网数据帧的目的mac地址字段中， 并发出。

上一节提到过，docker0收到container1发来的ip数据包，交由其处理程序，也就是linux内核协议栈处理程序处理，这时 docker0的身份开始转换了。

我们现在转换到宿主机视角。

从宿主机视角，docker0是一个mac地址为02:42:f9:f8:c9:ad，ip为172.17.0.1的网卡（网卡身份）。 container1发出的进入到docker0的包，对于host来说，就好比从docker0这块网卡设备进入到宿主机的数据包。当数据包进 入到三层时，iptables的处理规则就起了作用。我们看到在raw prerouting中的日志：

```
Jan 14 10:08:12 pc-baim kernel: [830038.910054] [TonyBai]-RawPrerouting:IN=docker0 OUT= PHYSIN=vethd9f6465 MAC=02:42:ac:11:00:03:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=172.17.0.3 LEN=60 TOS=0x10 PREC=0x00 TTL=64 ID=24284 DF PROTO=TCP SPT=43292 DPT=12580 WINDOW=29200 RES=0x00 SYN URGP=0
```


这是第一个ip包，承载着tcp sync数据。按照iptables的数据流转，接下来的route decision发现目的地址是172.17.0.3，不是自身绑定的172.17.0.1，不用送到user层（不走input链），在host的路由 表中继续匹配路由表项，匹配到如下路由表项：172.17.0.0/16 dev docker0，于是走forward链：

```
Jan 14 10:08:12 pc-baim kernel: [830038.910120] [TonyBai]-FwdId0Od0:IN=docker0 OUT=docker0 PHYSIN=vethd9f6465 PHYSOUT=vethfcceafa MAC=02:42:ac:11:00:03:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=172.17.0.3 LEN=60 TOS=0x10 PREC=0x00 TTL=64 ID=24284 DF PROTO=TCP SPT=43292 DPT=12580 WINDOW=29200 RES=0x00 SYN URGP=0
```


这又是一个直连网络，无需Gateway作为下一跳，于是再从docker0将数据送出。

docker0送出时，docker0又回到二层功能范畴。在cam表中查找mac地址02:42:ac:11:00:03对应的网口 vethfcceafa，将数据从vethfcceafa送出去。根据veth pair的描述，container2中的eth0将收到这份数据。container2发现数据包中目的地址是172.17.0.3，就是自身eth0 的地址，于是送到user层处理。

接下来是container 3 回复ack sync的过程。与上面类似，container3通过直连网络将数据包发给docker0。从host视角看，数据包从docker0这个网卡设备进 来：

```
Jan 14 10:08:12 pc-baim kernel: [830038.910200] [TonyBai]-RawPrerouting:IN=docker0 OUT= PHYSIN=vethfcceafa MAC=02:42:ac:11:00:02:02:42:ac:11:00:03:08:00 SRC=172.17.0.3 DST=172.17.0.2 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=0 DF PROTO=TCP SPT=12580 DPT=43292 WINDOW=28960 RES=0x00 ACK SYN URGP=0
```


route decision，由于目的地址不是docker0自身的目的地址，匹配路由条目：172.17.0.0/16 dev docker0，于是走forward链。这次在iptables forward链中匹配到的rules是：FwdOd0

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)

pkts bytes target prot opt in out source destination

6 328 DOCKER all — * docker0 0.0.0.0/0 0.0.0.0/0

5 268 FwdOd0 all — * docker0 0.0.0.0/0 0.0.0.0/0 ctstate RELATED,ESTABLISHED

… …

因为这次是conn established相关的链路上回包，日志如下：

```
Jan 14 10:08:12 pc-baim kernel: [830038.910230] [TonyBai]-FwdOd0:IN=docker0 OUT=docker0 PHYSIN=vethfcceafa PHYSOUT=vethd9f6465 MAC=02:42:ac:11:00:02:02:42:ac:11:00:03:08:00 SRC=172.17.0.3 DST=172.17.0.2 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=0 DF PROTO=TCP SPT=12580 DPT=43292 WINDOW=28960 RES=0x00 ACK SYN URGP=0
```


于是ack sync再从docker0送出。docker0送出时封装包时回到二层功能范畴。在cam表中查找mac地址02:42:ac:11:00:02对应的 网口vethd9f6465，将数据从vethd9f6465送出去。根据veth pair的描述，container1中的eth0将收到这份数据包。container1发现数据包中目的地址是172.17.0.2，就是自身 eth0的地址，于是送到user层处理。

container1接下来的回送ack过程与sync过程类似，这里就不赘述了。

#### 2、container to docker0

场景：我在container1(172.17.0.2)中执行：telnet 172.17.0.1 12580。docker0所在宿主机上并没有程序在监听12580端口，因此这个tcp连接是无法建立起来的。sync过去后，对方返回ack rst，而不是ack sync。

分析：

我们首先从container1的视角去看。

container1向172.17.0.1建立连接，在路由decision后，发现目标主机在直连网络中，于是将对方mac地址封装到二层协 议帧中后通过eth0将包转出。docker0收到包后，送到宿主机网络协议栈，也就是docker0的管理程序去处理。

切换到宿主机视角。宿主机从网卡docker0获取数据包，宿主机网络协议栈处理数据包，进入iptables中：

```
Jan 14 12:53:02 pc-baim kernel: [839935.434253] [TonyBai]-RawPrerouting:IN=docker0 OUT= PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=172.17.0.1 LEN=60 TOS=0x10 PREC=0x00 TTL=64 ID=29166 DF PROTO=TCP SPT=41362 DPT=12580 WINDOW=29200 RES=0x00 SYN URGP=0
```


路由decision后发现目的地址就是docker0自己的地址(172.17.0.1)，要送给user层，于是走filter input链：

```
Jan 14 12:53:02 pc-baim kernel: [839935.434309] [TonyBai]-FilterInput:IN=docker0 OUT= PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=172.17.0.1 LEN=60 TOS=0x10 PREC=0x00 TTL=64 ID=29166 DF PROTO=TCP SPT=41362 DPT=12580 WINDOW=29200 RES=0x00 SYN URGP=0
```


送到user层后，user层发现没有程序监听12580端口，于是向下发出ack rst包。数据包重新路由后，发现是直连网络，从docker0口出。但出去之前需要先进入iptables的filter output链：

```
Jan 14 12:53:02 pc-baim kernel: [839935.434344] [TonyBai]-FilterOutput:IN= OUT=docker0 SRC=172.17.0.1 DST=172.17.0.2 LEN=40 TOS=0x10 PREC=0x00 TTL=64 ID=781 DF PROTO=TCP SPT=12580 DPT=41362 WINDOW=0 RES=0x00 ACK RST URGP=0
```


数据包从docker0进入后，docker0承担网桥角色，在二层转发给container1，结束处理。

#### 3、container to host

场景：我在container1(172.17.0.2)中执行：telnet 10.10.126.101 12580。docker0所在宿主机上启动服务程序在监听12580端口，因此这是个标准tcp连接建立过程（sync, ack sync, ack）。

分析：

我们首先从container1的视角去看。

container1在经过路由判断后，匹配到default路由，需要走gateway(flags = UG)，于是将目的mac填写为Gateway 172.0.0.1的mac地址，将包通过eth0转给Gateway，即docker0。

切换到宿主机视角。

宿主机从网卡docker0收到一个数据包，进入iptables：

```
Jan 14 14:11:28 pc-baim kernel: [844644.563436] [TonyBai]-RawPrerouting:IN=docker0 OUT= PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=10.10.126.101 LEN=60 TOS=0x10 PREC=0x00 TTL=64 ID=55780 DF PROTO=TCP SPT=59373 DPT=12580 WINDOW=29200 RES=0x00 SYN URGP=0
```


路由decision，由于目的地址是10.10.126.101，docker0的管理程序，也就是host的linux网络栈处理程序发现这 不是我自己么（虽然是从 docker0收到的，但网络栈程序知道172.0.0.1和10.10.126.101都是自己），于是user层收下了这个包。因此在路由 后，数据包走到filter input:

```
Jan 14 14:11:28 pc-baim kernel: [844644.563476] [TonyBai]-FilterInput:IN=docker0 OUT= PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=10.10.126.101 LEN=60 TOS=0x10 PREC=0x00 TTL=64 ID=55780 DF PROTO=TCP SPT=59373 DPT=12580 WINDOW=29200 RES=0x00 SYN URGP=0
```


user层监听12580的服务程序收到包后，回复ack syn到172.17.0.2，路由Decision后，发现在直连网络中，通过docker0转出，于是走iptable filter output。

```
Jan 14 14:11:28 pc-baim kernel: [844644.563519] [TonyBai]-FilterOutput:IN= OUT=docker0 SRC=10.10.126.101 DST=172.17.0.2 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=0 DF PROTO=TCP SPT=12580 DPT=59373 WINDOW=28960 RES=0x00 ACK SYN URGP=0
```


container1收到ack syn后再回复ack，路径与sync一致，日志如下：

```
Jan 14 14:11:28 pc-baim kernel: [844644.563566] [TonyBai]-RawPrerouting:IN=docker0 OUT= PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=10.10.126.101 LEN=52 TOS=0x10 PREC=0x00 TTL=64 ID=55781 DF PROTO=TCP SPT=59373 DPT=12580 WINDOW=229 RES=0x00 ACK URGP=0
Jan 14 14:11:28 pc-baim kernel: [844644.563584] [TonyBai]-FilterInput:IN=docker0 OUT= PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=10.10.126.101 LEN=52 TOS=0x10 PREC=0x00 TTL=64 ID=55781 DF PROTO=TCP SPT=59373 DPT=12580 WINDOW=229 RES=0x00 ACK URGP=0
```


#### 4、host to container

场景：我在宿主机(10.10.126.101)中执行：telnet 172.17.0.2 12580。container1上启动服务程序在监听12580端口，因此这是个标准tcp连接建立过程（sync, ack sync, ack）。

分析：

这次我们首先从宿主机角度出发。

host的telnet程序在用户层产生数据包，经路由decision，匹配直连网络路由，出口docker0，然后进入iptables的 filter output链：

```
Jan 14 14:19:25 pc-baim kernel: [845121.897441] [TonyBai]-FilterOutput:IN= OUT=docker0 SRC=172.17.0.1 DST=172.17.0.2 LEN=60 TOS=0x10 PREC=0x00 TTL=64 ID=51756 DF PROTO=TCP SPT=44120 DPT=12580 WINDOW=29200 RES=0x00 SYN URGP=0
```


你会发现在这个log中，数据包的src ip地址为172.17.0.1，这是协议栈处理程序的选择，没有选择10.10.126.101，这些地址都标识host自己。

container1在收到sync后，回复ack sync，这就相当于container to host。host这次从docker0收到目的为172.17.0.1的ack sync包 , 走的是filer input，这里不赘述。

```
Jan 14 14:19:25 pc-baim kernel: [845121.897552] [TonyBai]-FilterInput:IN=docker0 OUT= PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=172.17.0.1 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=0 DF PROTO=TCP SPT=12580 DPT=44120 WINDOW=28960 RES=0x00 ACK SYN URGP=0
```


host再回复ack，与sync相同，走filter output链，不赘述。

```
Jan 14 14:19:25 pc-baim kernel: [845121.897588] [TonyBai]-FilterOutput:IN= OUT=docker0 SRC=172.17.0.1 DST=172.17.0.2 LEN=52 TOS=0x10 PREC=0x00 TTL=64 ID=51757 DF PROTO=TCP SPT=44120 DPT=12580 WINDOW=229 RES=0x00 ACK URGP=0
```


#### 5、container to 10.10.126.187

场景：我们在container1中向与宿主机直接网络的主机10.10.126.187建立连接。我在container1中执 行：telnet 10.10.126.187 12580。187上启动服务程序在监听12580端口，因此这是个标准tcp连接建立过程（sync, ack sync, ack）。

分析：

container1视角：将sync包发个目的地址10.10.126.187，根据路由选择，从默认路由走，下一跳为Gateway，即 172.17.0.1。消息发到docker0。

切换到host视角：host从docker0网卡收到一个sync包，目的地址是10.10.126.187，进入到iptables：

```
Jan 14 14:47:17 pc-baim kernel: [846795.243863] [TonyBai]-RawPrerouting:IN=docker0 OUT= PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=10.10.126.187 LEN=60 TOS=0x10 PREC=0x00 TTL=64 ID=34160 DF PROTO=TCP SPT=55148 DPT=12580 WINDOW=29200 RES=0x00 SYN URGP=0
```


路由选择后，匹配到host的直连网络路由(10.10.126.0/24 via eth0)，包将从eth0出去，于是docker0转发到eth0，走foward chain：

```
Jan 14 14:47:17 pc-baim kernel: [846795.243931] [TonyBai]-FwdId0Ond0:IN=docker0 OUT=eth0 PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=10.10.126.187 LEN=60 TOS=0x10 PREC=0x00 TTL=63 ID=34160 DF PROTO=TCP SPT=55148 DPT=12580 WINDOW=29200 RES=0x00 SYN URGP=0
```


出forward chain后，匹配到nat表的postrouting链，做Masquerade(SNAT)。将源地址从172.0.0.2换为 10.10.126.101再发出去。

```
Jan 14 14:47:17 pc-baim kernel: [846795.243940] [TonyBai]-NatPostRouting:IN= OUT=eth0 PHYSIN=vethd9f6465 SRC=172.17.0.2 DST=10.10.126.187 LEN=60 TOS=0x10 PREC=0x00 TTL=63 ID=34160 DF PROTO=TCP SPT=55148 DPT=12580 WINDOW=29200 RES=0x00 SYN URGP=0
```


10.10.126.187收到后，回复ack sync。由于10.10.126.187上增加了172.17.0.0/16的路由，gateway为10.10.126.101，因此ack sync被回送给宿主机，host会从187收到ack sync包。

```
Jan 14 14:47:17 pc-baim kernel: [846795.244155] [TonyBai]-RawPrerouting:IN=eth0 OUT= MAC=2c:59:e5:01:98:28:00:19:bb:5e:0a:86:08:00 SRC=10.10.126.187 DST=10.10.126.101 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=0 DF PROTO=TCP SPT=12580 DPT=55148 WINDOW=5792 RES=0x00 ACK SYN URGP=0
```


进入iptables时，目的地址还是10.10.126.101，进入路由选择前iptables会将10.10.126.101换成 172.17.0.2（由于之间在natpostrouting做了masquerade）。这样后续路由的目的地址为docker0，需要由 eth0转到docker0，走 forward链。由于是RELATED, ESTABLISHED 连接，因此匹配到FwdOd0:

```
Jan 14 14:47:17 pc-baim kernel: [846795.244182] [TonyBai]-FwdOd0:IN=eth0 OUT=docker0 MAC=2c:59:e5:01:98:28:00:19:bb:5e:0a:86:08:00 SRC=10.10.126.187 DST=172.17.0.2 LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=0 DF PROTO=TCP SPT=12580 DPT=55148 WINDOW=5792 RES=0x00 ACK SYN URGP=0
```


切换到container1视角。收到ack sync后，回复ack，同sync流程，不赘述：

```
Jan 14 14:47:17 pc-baim kernel: [846795.244249] [TonyBai]-RawPrerouting:IN=docker0 OUT= PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=10.10.126.187 LEN=52 TOS=0x10 PREC=0x00 TTL=64 ID=34161 DF PROTO=TCP SPT=55148 DPT=12580 WINDOW=229 RES=0x00 ACK URGP=0
Jan 14 14:47:17 pc-baim kernel: [846795.244266] [TonyBai]-FwdId0Ond0:IN=docker0 OUT=eth0 PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=10.10.126.187 LEN=52 TOS=0x10 PREC=0x00 TTL=63 ID=34161 DF PROTO=TCP SPT=55148 DPT=12580 WINDOW=229 RES=0x00 ACK URGP=0
```


不用再走一遍natpostrouting，属于一个流的包只会 经过这个表一次。如果第一个包被允许做NAT或Masqueraded，那么余下的包都会自 动地被做 相同的操作。也就是说,余下的包不会再通过这个表一个一个的被NAT，而是自动地完成。

#### 6、10.10.126.187 to container

场景：我们在10.10.126.187向container1建立连接。我在187中执行：telnet 172.17.0.2 12580。container1上启动服务程序在监听12580端口，因此这是个标准tcp连接建立过程（sync, ack sync, ack）。

分析：

由于187上增加了container1的路由，187将sync包发到gateway 10.10.126.101。

宿主机视角：从eth0收到目的地址为172.17.0.2的sync包，到达iptables：

```
Jan 14 15:06:08 pc-baim kernel: [847926.218791] [TonyBai]-RawPrerouting:IN=eth0 OUT= MAC=2c:59:e5:01:98:28:00:19:bb:5e:0a:86:08:00 SRC=10.10.126.187 DST=172.17.0.2 LEN=60 TOS=0x10 PREC=0x00 TTL=64 ID=48735 DF PROTO=TCP SPT=53225 DPT=12580 WINDOW=5840 RES=0x00 SYN URGP=0
```


路由后应该通过docker0发到直连网络。应该走Forward链，但由于上面的log没有覆盖到，只是匹配到DOCKER chain，没有匹配到可以log的rules，没有打印出来log。

docker0将sync发给container1，container1回复ack sync。消息报目的地址187，走gateway，即docker0。

再回到主机视角，host从docker0网卡收到ack sync包，目的187，因此路由后，走直连网络转发口eth0。iptables中走forward chain：FwdId0Ond0:

```
Jan 14 15:06:08 pc-baim kernel: [847926.219010] [TonyBai]-RawPrerouting:IN=docker0 OUT= PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=10.10.126.187 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=0 DF PROTO=TCP SPT=12580 DPT=53225 WINDOW=28960 RES=0x00 ACK SYN URGP=0
Jan 14 15:06:08 pc-baim kernel: [847926.219103] [TonyBai]-FwdId0Ond0:IN=docker0 OUT=eth0 PHYSIN=vethd9f6465 MAC=02:42:f9:f8:c9:ad:02:42:ac:11:00:02:08:00 SRC=172.17.0.2 DST=10.10.126.187 LEN=60 TOS=0x00 PREC=0x00 TTL=63 ID=0 DF PROTO=TCP SPT=12580 DPT=53225 WINDOW=28960 RES=0x00 ACK SYN URGP=0
```


注意这块是已经建立的连接，双方都知道对方的地址了（187上配置了172.17.0.2的路由），因此并没有走nat postroutiing chain，没有SNAT转换地址。

187收到后，回复ack。这个过程重复sync过程，但forward链可以匹配到FwdOd0：

```
Jan 14 15:06:08 pc-baim kernel: [847926.219417] [TonyBai]-RawPrerouting:IN=eth0 OUT= MAC=2c:59:e5:01:98:28:00:19:bb:5e:0a:86:08:00 SRC=10.10.126.187 DST=172.17.0.2 LEN=52 TOS=0x10 PREC=0x00 TTL=64 ID=48736 DF PROTO=TCP SPT=53225 DPT=12580 WINDOW=92 RES=0x00 ACK URGP=0
Jan 14 15:06:08 pc-baim kernel: [847926.219477] [TonyBai]-FwdOd0:IN=eth0 OUT=docker0 MAC=2c:59:e5:01:98:28:00:19:bb:5e:0a:86:08:00 SRC=10.10.126.187 DST=172.17.0.2 LEN=52 TOS=0x10 PREC=0x00 TTL=63 ID=48736 DF PROTO=TCP SPT=53225 DPT=12580 WINDOW=92 RES=0x00 ACK URGP=0
```


### 八、容器网络性能测量

这里顺便对容器网络性能做一个初步的测量，测量可以考虑使用传统工具：[netperf](http://www.netperf.org/netperf/)，其服务端为netserver，会同netperf一并安装到主机中。但前些时候发现了一款显示结果更直观的用go实现的工具：[sparkyfish](https://github.com/chrissnell/sparkyfish)。这里我打算用这个新工具来粗粗的测量一下容器网络的性能。

由于sparkyfish会执行upload和download场景，因此server放在哪个位置均可。

我们执行两个场景，对比host和container的网络性能：

#### 1、与同局域网的一个主机通信

我们在一台与host在同一局域网的主机(105.71)上启动sparkyfish-server，然后分别在host和container上执行sparkyfish-cli 10.10.105.71，结果截图如下：

![img{}](../../assets/5bb3c90c20b4b05c.png)


host to 105.71

![img{}](../../assets/96eef2c6387879b0.png)


container to 105.71

对比发现：container、host到外部网络的度量值差不多，avg值几乎相同。

#### 2、container to host and container

我们在host和另一个container2上分别启动一个sparkyfish-server，然后在container1上执行分别执行sparkyfish-cli 10.10.126.101和sparkyfish-cli 172.17.0.3，结果截图如下：

![img{}](../../assets/0f554487f56dd02f.png)


container to host

![img{}](../../assets/92d356313e2e28e8.png)


container to container

对比可以看出：container to container的出入网络性能均仅为container to host的网络性能的三分之一不到。

### 九、小结

以上粗略理解了docker单机容器网络，有些地方理解难免有偏颇，甚至是错误，欢迎指正。

Docker技术虽然成长迅猛，前景广阔，但Docker也非银弹，深入之处必然有坑。填坑之路虽然痛苦，但能有所收获也算是很好了。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

Docker的确是新事物，我也刚学习，刚把自己写的博客程序移植到了Docker中，我是直接写Dockerfile，然后将Golang写的博客代码直接用CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o来编译为无需动态链接库的模式，用的alpine基系统，尽量减少images大小~

没看明白一点：container对container通信，在虚拟交换机上直接通过mac地址表直接交换就可以了，为什么还要通过docker0接口上升到三层？

从发送数据包的container的视角去看，数据包从未进入过三层，而是通过docker0这个二层交换机送到对端的。但docker0对于物理机而言，他是个网卡设备，数据从该网卡设备流入，这个过程必须走到主机自己的三层了，而不是网络传输过程中的三层。而该网卡设备的处理程序就是内核的tcp/ip处理逻辑。

那veth也是宿主机的一个interface啊，从container发来的包，理应从veth接口进入，主机从veth接口收到包后，数据包的目的mac地址与veth的不一致，所以需要进行二层转发，根据brctl showmac docker0显示的mac转发表，直接转发到响应的虚拟交换机port就行了。为什么veth收到的包会转发给docker0这个接口呢？请赐教 :）

我也不是网络专家。但我的理解是：veth仅是一个peer端，veth成对出现(veth0-veth1)。container向veth0发送数据，docker0 bridge中的veth1收到数据。在这种网络连接模式下，内核程序不会针对veth0和veth1做处理，而是响应docker0的recv data事件，并进行处理，而docker0的处理逻辑从iptables的日志输出来看，就是文章中提到的那些。

疑惑未释，不过还是感谢你的解答。有机会可以认识一下，我的微信：2202086749

两个veth(container中的veth0和“插”在docker0上的veth1)将两个network namespace连接起来，一个是container的namespace，一个是host的network namespace。内核对veth0上进入的数据的处理方>式就是简单传给veth1，从而触发docker0上的data recv event，该事件引发内核的处理。内核究竟如何处理的，细节我也不清楚。但从iptable的日志来看，内核是将数据包做了很多诸多判断，并最终将数据包发回docker0的另外一个veth2口上。

谢谢解答，这么认真负责回复的博主不多了。我关注你博客了，再次感谢。

就算这样，感觉也说不通，数据包的destination mac是container2的接口地址，不是docker0的接口地址，docker0接口开启混杂模式，由于mac地址和docker0的mac地址不一样，docker0接口也应该在二层转发的，不应该上升到三层。只有数据包的目的mac地址是docker接口的mac地址，才进一步上升到三层，由iptables规则来确定IP数据报是应该转发还是再继续往上层协议传递。

十分感谢关注。不过目前我从表象的理解只能理解到这了，有空可以深入代码分析。如果您有更好的理解，可以在这里留言，我也学习一下:)

博主你好，文章写的很好，原理写的很细，这里有个问题想请教一下。关于实例：6、10.10.126.187 to container 中另一台宿主机访问容器，有增加路由，可否提供一下详细怎么写吗？我是初学者，添加到容器主机的静态路由也无法ping通。不知道是否有其它地方还需要配置。在10.10.126.187上配置的静态路由为：route add -host 172.17.0.2 gw eth0 ，能得到解答无比感谢。

为什么我看到的 6、10.10.126.187 to container， 这一类请求，其实是发往宿主，然后通过DNAT改变 目的ip为 container的 172.17.0.2 吧？ “由于187上增加了container1的路由” 好像docker本身并不会这样做把。

2016/11/04：

没看明白一点：container对container通信，在虚拟交换机上直接通过mac地址表直接交换就可以了，为什么还要通过docker0接口上升到三层？

这个问题，找到标准答案了不？有的话，回复一下！

博主在之后一篇博文里引用了 IBM 一篇关于 bridge 实现的博文，里面某种程度上解释了在 container to container 的场景下，为什么 docker0 会进行三层的处理而不是二层的转发，应该是由于 docker 0 被分配了 IP 的缘故。

https://www.ibm.com/developerworks/cn/linux/1310_xiawc_networkdevice/

帅气