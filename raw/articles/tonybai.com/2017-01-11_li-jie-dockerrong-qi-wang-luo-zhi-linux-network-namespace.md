---
title: 理解Docker容器网络之Linux Network Namespace
url: https://tonybai.com/2017/01/11/understanding-linux-network-namespace-for-docker-network/
published: '2017-01-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 理解Docker容器网络之Linux Network Namespace

由于2016年年中[调换工作](http://tonybai.com/2017/01/03/2016-summary/)的原因，对容器网络的研究中断过一段时间。随着当前项目对[Kubernetes](http://tonybai.com/tag/kubernetes)应用的深入，我感觉之前对于[容器网络的粗浅理解](http://tonybai.com/2016/01/15/understanding-container-networking-on-single-host/)已经不够了，容器网络成了摆在前面的“一道坎”。继续深入理解K8s网络、容器网络已经势在必行。而这篇文章就算是一个重新开始，也是对之前浅表理解的一个补充。

我还是先从[Docker](https://www.docker.com/)容器网络入手，虽然Docker与Kubernetes采用了不同的网络模型：K8s是[Container Network Interface, CNI](https://github.com/containernetworking/cni)模型，而Docker则采用的是[Container Network Model, CNM](https://github.com/docker/libnetwork/blob/master/docs/design.md)模型。而要了解Docker容器网络，理解Linux Network Namespace是不可或缺的。在本文中我们将尝试理解Linux Network Namespace及相关Linux内核网络设备的概念，并手工模拟Docker容器网络模型的部分实现，包括[单机容器网络](http://tonybai.com/2016/01/15/understanding-container-networking-on-single-host/)中的容器与主机连通、容器间连通以及[端口映射](http://tonybai.com/2016/01/18/understanding-binding-docker-container-ports-to-host/)等。

### 一、Docker的CNM网络模型

Docker通过[libnetwork](https://github.com/docker/libnetwork)实现了CNM网络模型。libnetwork设计doc中对CNM模型的简单诠释如下：

![img{512x368}](../../assets/3614bce27f783666.jpg)


CNM模型有三个组件：

- Sandbox(沙盒)：每个沙盒包含一个容器网络栈(network stack)的配置，配置包括：容器的网口、路由表和DNS设置等。
- Endpoint(端点)：通过Endpoint，沙盒可以被加入到一个Network里。
- Network(网络)：一组能相互直接通信的Endpoints。

光看这些，我们还很难将之与现实中的Docker容器联系起来，毕竟是抽象的模型不对应到实体，总有种漂浮的赶脚。文档中又给出了CNM模型在Linux上的参考实现技术，比如：沙盒的实现可以是一个[Linux Network Namespace](https://en.wikipedia.org/wiki/Linux_namespaces#Network_.28net.29)；Endpoint可以是一对[VETH](https://openvz.org/Virtual_Ethernet_device)；Network则可以用[Linux Bridge](https://wiki.linuxfoundation.org/networking/bridge)或[Vxlan](https://en.wikipedia.org/wiki/Virtual_Extensible_LAN)实现。

这些实现技术反倒是比较接地气。之前我们在使用Docker容器时，了解过Docker是用linux network namespace实现的容器网络隔离的。使用docker时，在物理主机或虚拟机上会有一个docker0的linux bridge，brctl show时能看到 docker0上“插上了”好多veth网络设备：

```
# ip link show
... ...
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
link/ether 02:42:30:11:98:ef brd ff:ff:ff:ff:ff:ff
19: veth4559467@if18: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
link/ether a6:14:99:52:78:35 brd ff:ff:ff:ff:ff:ff link-netnsid 3
... ...
$ brctl show
bridge name bridge id STP enabled interfaces
... ...
docker0 8000.0242301198ef no veth4559467
```


模型与现实终于有点接驳了！下面我们将进一步深入对这些术语概念的理解。

### 二、Linux Bridge、VETH和Network Namespace

[Linux Bridge](https://wiki.linuxfoundation.org/networking/bridge)，即Linux网桥设备，是Linux提供的一种虚拟网络设备之一。其工作方式非常类似于物理的网络交换机设备。Linux Bridge可以工作在二层，也可以工作在三层，默认工作在二层。工作在二层时，可以在同一网络的不同主机间转发以太网报文；一旦你给一个Linux Bridge分配了IP地址，也就开启了该Bridge的三层工作模式。在Linux下，你可以用[iproute2](https://wiki.linuxfoundation.org/networking/iproute2)工具包或brctl命令对Linux bridge进行管理。

VETH(Virtual Ethernet )是Linux提供的另外一种特殊的网络设备，中文称为虚拟网卡接口。它总是成对出现，要创建就创建一个pair。一个Pair中的veth就像一个网络线缆的两个端点，数据从一个端点进入，必然从另外一个端点流出。每个veth都可以被赋予IP地址，并参与三层网络路由过程。

关于Linux Bridge和VETH的具体工作原理，可以参考IBM developerWorks上的这篇文章《[Linux 上的基础网络设备详解](http://www.ibm.com/developerworks/cn/linux/1310_xiawc_networkdevice/)》。

Network namespace，网络名字空间，允许你在Linux创建相互隔离的网络视图，每个网络名字空间都有独立的网络配置，比如：网络设备、路由表等。新建的网络名字空间与主机默认网络名字空间之间是隔离的。我们平时默认操作的是主机的默认网络名字空间。

概念总是抽象的，接下来我们将在一个模拟Docker容器网络的例子中看到这些Linux网络概念和网络设备到底是起到什么作用的以及是如何操作的。

### 三、用Network namespace模拟Docker容器网络

为了进一步了解network namespace、bridge和veth在docker容器网络中的角色和作用，我们来做一个demo：用network namespace模拟Docker容器网络，实际上Docker容器网络在linux上也是基于network namespace实现的，我们只是将其“自动化”的创建过程做成了“分解动作”，便于大家理解。

#### 1、环境

我们在一台物理机上进行这个Demo实验。物理机安装了Ubuntu 16.04.1，内核版本：4.4.0-57-generic。Docker容器版本：

```
Client:
Version: 1.12.1
API version: 1.24
Go version: go1.6.3
Git commit: 23cf638
Built: Thu Aug 18 05:33:38 2016
OS/Arch: linux/amd64
Server:
Version: 1.12.1
API version: 1.24
Go version: go1.6.3
Git commit: 23cf638
Built: Thu Aug 18 05:33:38 2016
OS/Arch: linux/amd64
```


另外，环境中需安装了[iproute2](https://wiki.linuxfoundation.org/networking/iproute2)和brctl工具。

#### 2、拓扑

我们来模拟一个拥有两个容器的容器桥接网络：

![img{512x368}](../../assets/9579b7e764f17456.png)


对应的用手工搭建的模拟版本拓扑如下(由于在同一台主机，模拟版本采用172.16.0.0/16网段)：

![img{512x368}](../../assets/b0b0d31b8ea425e4.png)


#### 3、创建步骤

##### a) 创建Container_ns1和Container_ns2 network namespace

默认情况下，我们在Host上看到的都是default network namespace的视图。为了模拟容器网络，我们新建两个network namespace：

```
sudo ip netns add Container_ns1
sudo ip netns add Container_ns2
$ sudo ip netns list
Container_ns2
Container_ns1
```


创建的ns也可以在/var/run/netns路径下看到：

```
$ sudo ls /var/run/netns
Container_ns1 Container_ns2
```


我们探索一下新创建的ns的网络空间(通过ip netns exec命令可以在特定ns的内部执行相关程序，这个exec命令是至关重要的，后续还会发挥更大作用)：

```
$ sudo ip netns exec Container_ns1 ip a
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
$ sudo ip netns exec Container_ns2 ip a
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
$ sudo ip netns exec Container_ns2 ip route
```


可以看到，新建的ns的网络设备只有一个loopback口，并且路由表为空。

##### b) 创建MyDocker0 bridge

我们在default network namespace下创建MyDocker0 linux bridge：

```
$ sudo brctl addbr MyDocker0
$ brctl show
bridge name bridge id STP enabled interfaces
MyDocker0 8000.000000000000 no
```


给MyDocker0分配ip地址并生效该设备，开启三层，为后续充当Gateway做准备：

```
$ sudo ip addr add 172.16.1.254/16 dev MyDocker0
$ sudo ip link set dev MyDocker0 up
```


启用后，我们发现default network namespace的路由配置中增加了一条路由：

```
$ route -n
内核 IP 路由表
目标 网关 子网掩码 标志 跃点 引用 使用 接口
0.0.0.0 10.11.36.1 0.0.0.0 UG 100 0 0 eno1
... ...
172.16.0.0 0.0.0.0 255.255.0.0 U 0 0 0 MyDocker0
... ...
```


##### c) 创建VETH，连接两对network namespaces

到目前为止，default ns与Container_ns1、Container_ns2之间还没有任何瓜葛。接下来就是见证奇迹的时刻了。我们通过veth pair建立起多个ns之间的联系：

创建连接default ns与Container_ns1之间的veth pair – veth1和veth1p：

```
$sudo ip link add veth1 type veth peer name veth1p
$sudo ip -d link show
... ...
21: veth1p@veth1: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
link/ether 66:6d:e7:75:3f:43 brd ff:ff:ff:ff:ff:ff promiscuity 0
veth addrgenmode eui64
22: veth1@veth1p: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
link/ether 56:cd:bb:f2:10:3f brd ff:ff:ff:ff:ff:ff promiscuity 0
veth addrgenmode eui64
... ...
```


将veth1“插到”MyDocker0这个bridge上：

```
$ sudo brctl addif MyDocker0 veth1
$ sudo ip link set veth1 up
$ brctl show
bridge name bridge id STP enabled interfaces
MyDocker0 8000.56cdbbf2103f no veth1
```


将veth1p“放入”Container_ns1中：

```
$ sudo ip link set veth1p netns Container_ns1
$ sudo ip netns exec Container_ns1 ip a
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
21: veth1p@if22: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
link/ether 66:6d:e7:75:3f:43 brd ff:ff:ff:ff:ff:ff link-netnsid 0
```


这时，你在default ns中将看不到veth1p这个虚拟网络设备了。按照上面拓扑，位于Container_ns1中的veth应该更名为eth0：

```
$ sudo ip netns exec Container_ns1 ip link set veth1p name eth0
$ sudo ip netns exec Container_ns1 ip a
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
21: eth0@if22: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
link/ether 66:6d:e7:75:3f:43 brd ff:ff:ff:ff:ff:ff link-netnsid 0
```


将Container_ns1中的eth0生效并配置IP地址：

```
$ sudo ip netns exec Container_ns1 ip link set eth0 up
$ sudo ip netns exec Container_ns1 ip addr add 172.16.1.1/16 dev eth0
```


赋予IP地址后，自动生成一条直连路由：

```
sudo ip netns exec Container_ns1 ip route
172.16.0.0/16 dev eth0 proto kernel scope link src 172.16.1.1
```


现在在Container_ns1下可以ping通MyDocker0了，但由于没有其他路由，包括默认路由，ping其他地址还是不通的（比如：docker0的地址：172.17.0.1）：

```
$ sudo ip netns exec Container_ns1 ping -c 3 172.16.1.254
PING 172.16.1.254 (172.16.1.254) 56(84) bytes of data.
64 bytes from 172.16.1.254: icmp_seq=1 ttl=64 time=0.074 ms
64 bytes from 172.16.1.254: icmp_seq=2 ttl=64 time=0.064 ms
64 bytes from 172.16.1.254: icmp_seq=3 ttl=64 time=0.068 ms
--- 172.16.1.254 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1998ms
rtt min/avg/max/mdev = 0.064/0.068/0.074/0.010 ms
$ sudo ip netns exec Container_ns1 ping -c 3 172.17.0.1
connect: Network is unreachable
```


我们再给Container_ns1添加一条默认路由，让其能ping通物理主机上的其他网络设备或其他ns空间中的网络设备地址：

```
$ sudo ip netns exec Container_ns1 ip route add default via 172.16.1.254
$ sudo ip netns exec Container_ns1 ip route
default via 172.16.1.254 dev eth0
172.16.0.0/16 dev eth0 proto kernel scope link src 172.16.1.1
$ sudo ip netns exec Container_ns1 ping -c 3 172.17.0.1
PING 172.17.0.1 (172.17.0.1) 56(84) bytes of data.
64 bytes from 172.17.0.1: icmp_seq=1 ttl=64 time=0.068 ms
64 bytes from 172.17.0.1: icmp_seq=2 ttl=64 time=0.076 ms
64 bytes from 172.17.0.1: icmp_seq=3 ttl=64 time=0.069 ms
--- 172.17.0.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1999ms
rtt min/avg/max/mdev = 0.068/0.071/0.076/0.003 ms
```


不过这时候，如果想在Container_ns1中ping通物理主机之外的地址，比如:google.com，那还是不通的。为什么呢？因为ping的icmp的包的源地址没有做snat（docker是通过设置[iptables](https://www.netfilter.org/)规则实现的），导致出去的以172.16.1.1为源地址的包“有去无回”了^0^。

接下来，我们按照上述步骤，再创建连接default ns与Container_ns2之间的veth pair – veth2和veth2p，由于步骤相同，这里就不列出那么多信息了，只列出关键操作：

```
$ sudo ip link add veth2 type veth peer name veth2p
$ sudo brctl addif MyDocker0 veth2
$ sudo ip link set veth2 up
$ sudo ip link set veth2p netns Container_ns2
$ sudo ip netns exec Container_ns2 ip link set veth2p name eth0
$ sudo ip netns exec Container_ns2 ip link set eth0 up
$ sudo ip netns exec Container_ns2 ip addr add 172.16.1.2/16 dev eth0
$ sudo ip netns exec Container_ns2 ip route add default via 172.16.1.254
```


至此，模拟创建告一段落！两个ns之间以及它们与default ns之间连通了！

```
$ sudo ip netns exec Container_ns2 ping -c 3 172.16.1.1
PING 172.16.1.1 (172.16.1.1) 56(84) bytes of data.
64 bytes from 172.16.1.1: icmp_seq=1 ttl=64 time=0.101 ms
64 bytes from 172.16.1.1: icmp_seq=2 ttl=64 time=0.083 ms
64 bytes from 172.16.1.1: icmp_seq=3 ttl=64 time=0.087 ms
--- 172.16.1.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1998ms
rtt min/avg/max/mdev = 0.083/0.090/0.101/0.010 ms
$ sudo ip netns exec Container_ns1 ping -c 3 172.16.1.2
PING 172.16.1.2 (172.16.1.2) 56(84) bytes of data.
64 bytes from 172.16.1.2: icmp_seq=1 ttl=64 time=0.053 ms
64 bytes from 172.16.1.2: icmp_seq=2 ttl=64 time=0.092 ms
64 bytes from 172.16.1.2: icmp_seq=3 ttl=64 time=0.089 ms
--- 172.16.1.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1999ms
rtt min/avg/max/mdev = 0.053/0.078/0.092/0.017 ms
```


当然此时两个ns之间连通，主要还是通过直连网络，实质上是MyDocker0在二层起到的作用。以在Container_ns1中ping Container_ns2的eth0地址为例：

Container_ns1此时的路由表：

```
$ sudo ip netns exec Container_ns1 ip route
default via 172.16.1.254 dev eth0
172.16.0.0/16 dev eth0 proto kernel scope link src 172.16.1.1
```


ping 172.16.1.2执行后，根据路由表，将首先匹配到直连网络（第二条），即无需gateway转发便可以直接将数据包送达。arp查询后（要么从arp cache中找到，要么在MyDocker0这个二层交换机中泛洪查询）获得172.16.1.2的mac地址。ip包的目的ip填写172.16.1.2，二层数据帧封包将目的mac填写为刚刚查到的mac地址，通过eth0(172.16.1.1)发送出去。eth0实际上是一个veth pair，另外一端“插”在MyDocker0这个交换机上，因此这一过程就是一个标准的二层交换机的数据报文交换过程, MyDocker0相当于从交换机上的一个端口收到以太帧数据，并将数据从另外一个端口发出去。ping应答包亦如此。

而如果是在Container_ns1中ping某个docker container的地址，比如172.17.0.2。当ping执行后，根据Container_ns1下的路由表，没有匹配到直连网络，只能通过default路由将数据包发给Gateway: 172.16.1.254。虽然都是MyDocker0接收数据，但这次更类似于“数据被直接发到 Bridge 上，而不是Bridge从一个端口接收(这块儿与我之前的文章中的理解稍有差异)”。二层的目的mac地址填写的是gateway 172.16.1.254自己的mac地址（Bridge的mac地址），此时的MyDocker0更像是一块普通网卡的角色，工作在三层。MyDocker0收到数据包后，发现并非是发给自己的ip包，通过主机路由表找到直连链路路由，MyDocker0将数据包Forward到docker0上（封装的二层数据包的目的MAC地址为docker0的mac地址）。此时的docker0也是一种“网卡”的角色，由于目的ip依然不是docker0自身，因此docker0也会继续这一转发流程。通过traceroute可以印证这一过程：

```
$ sudo ip netns exec Container_ns1 traceroute 172.17.0.2
traceroute to 172.17.0.2 (172.17.0.2), 30 hops max, 60 byte packets
1 172.16.1.254 (172.16.1.254) 0.082 ms 0.023 ms 0.019 ms
2 172.17.0.2 (172.17.0.2) 0.054 ms 0.034 ms 0.029 ms
$ sudo ip netns exec Container_ns1 ping -c 3 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=63 time=0.084 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=63 time=0.101 ms
64 bytes from 172.17.0.2: icmp_seq=3 ttl=63 time=0.098 ms
--- 172.17.0.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1998ms
rtt min/avg/max/mdev = 0.084/0.094/0.101/0.010 ms
```


现在，你应该大致了解docker engine在创建单机容器网络时都在背后做了哪些手脚了吧（当然，这里只是简单模拟，docker实际做的要比这复杂许多）。

### 四、基于userland proxy的容器端口映射的模拟

[端口映射](http://tonybai.com/2016/01/18/understanding-binding-docker-container-ports-to-host/)让位于容器中的service可以将服务范围扩展到主机之外，比如：一个运行于container中的[nginx](http://tonybai.com/2016/11/22/deploy-nginx-service-for-the-services-in-kubernetes-cluster/)可以通过宿主机的9091端口对外提供http server服务：

```
$ sudo docker run -d -p 9091:80 nginx:latest
8eef60e3d7b48140c20b11424ee8931be25bc47b5233aa42550efabd5730ac2f
$ curl 10.11.36.15:9091
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
```


容器的端口映射实际是通过docker engine的docker proxy功能实现的。默认情况下，docker engine(截至docker 1.12.1版本)采用userland proxy(–userland-proxy=true)为每个expose端口的容器启动一个proxy实例来做端口流量转发：

```
$ ps -ef|grep docker-proxy
root 26246 6228 0 16:18 ? 00:00:00 /usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 9091 -container-ip 172.17.0.2 -container-port 80
```


docker-proxy实际上就是在default ns和container ns之间转发流量而已。我们完全可以模拟这一过程。

我们创建一个fileserver demo：

```
//testfileserver.go
package main
import "net/http"
func main() {
http.ListenAndServe(":8080", http.FileServer(http.Dir(".")))
}
```


我们在Container_ns1下启动这个Fileserver service:

```
$ sudo ip netns exec Container_ns1 ./testfileserver
$ sudo ip netns exec Container_ns1 lsof -i tcp:8080
COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
testfiles 3605 root 3u IPv4 297022 0t0 TCP *:http-alt (LISTEN)
```


可以看到在Container_ns1下面，8080已经被testfileserver监听，不过在default ns下，8080端口依旧是avaiable的。

接下来，我们在default ns下创建一个简易的proxy：

```
//proxy.go
... ...
var (
host string
port string
container string
containerport string
)
func main() {
flag.StringVar(&host, "host", "0.0.0.0", "host addr")
flag.StringVar(&port, "port", "", "host port")
flag.StringVar(&container, "container", "", "container addr")
flag.StringVar(&containerport, "containerport", "8080", "container port")
flag.Parse()
fmt.Printf("%s\n%s\n%s\n%s", host, port, container, containerport)
ln, err := net.Listen("tcp", host+":"+port)
if err != nil {
// handle error
log.Println("listen error:", err)
return
}
log.Println("listen ok")
for {
conn, err := ln.Accept()
if err != nil {
// handle error
log.Println("accept error:", err)
continue
}
log.Println("accept conn", conn)
go handleConnection(conn)
}
}
func handleConnection(conn net.Conn) {
cli, err := net.Dial("tcp", container+":"+containerport)
if err != nil {
log.Println("dial error:", err)
return
}
log.Println("dial ", container+":"+containerport, " ok")
go io.Copy(conn, cli)
_, err = io.Copy(cli, conn)
fmt.Println("communication over: error:", err)
}
```


在default ns下执行：

```
./proxy -host 0.0.0.0 -port 9090 -container 172.16.1.1 -containerport 8080
0.0.0.0
9090
172.16.1.1
80802017/01/11 17:26:10 listen ok
```


我们http get一下宿主机的9090端口：

```
$curl 10.11.36.15:9090
<pre>
<a href="proxy">proxy</a>
<a href="proxy.go">proxy.go</a>
<a href="testfileserver">testfileserver</a>
<a href="testfileserver.go">testfileserver.go</a>
</pre>
```


成功获得file list！

proxy的输出日志：

```
2017/01/11 17:26:16 accept conn &{{0xc4200560e0}}
2017/01/11 17:26:16 dial 172.16.1.1:8080 ok
communication over: error:<nil>
```


由于每个做端口映射的Container都要启动至少一个docker proxy与之配合，一旦运行的container增多，那么docker proxy对资源的消耗将是大大的。因此docker engine在docker 1.6之后（好像是这个版本）提供了基于iptables的端口映射机制，无需再启动docker proxy process了。我们只需修改一下docker engine的启动配置即可：

在使用systemd init system的系统中如果为docker engine配置–userland-proxy=false，可以参考《[当Docker遇到systemd](http://tonybai.com/2016/12/27/when-docker-meets-systemd)》这篇文章。

由于这个与network namespace关系不大，后续单独理解^0^。

### 六、参考资料

1、《[Docker networking cookbook](https://book.douban.com/subject/26929989/)》

2、《[Docker cookbook](https://book.douban.com/subject/26631435/)》

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

您现在描述的是单主机不同容器之间网络通信原理，那么如果要是跨主机呢？比如overlay网络，这方面的通信原理能分享下吗

之前写过一篇: 理解Docker跨多主机容器网络http://tonybai.com/2016/02/15/understanding-docker-multi-host-networking/

写的真好！受益匪浅！

你好，我在云主机上创建一个network namespce（ns1），之后创建一个linux网桥br0，以及一对veth pair（veth0和veth1）。之后，将veth0连在ns1中，将veth0挂在br0上，最后再将对外的eth1口也挂在br0上，并将eth1上的IP配在br0上。但是这样配置了之后，ping与br0 ip所在同一网段的IP均不通，这是什么原因呢？

“将veth0连在ns1中，将veth0挂在br0上” 笔误？ veth1挂载br0上吧？

你好， linux默认是把bridge的FORWORD给禁掉的，所以在Container_ns1里面是ping不通Container_ns2。需要给iptables加一个rule才行：sudo iptables -A FORWARD -i MyDocker0 -j ACCEPT

记得当时在我的host上 已经设置了 /proc/sys/net/ipv4/ip_forward = 1