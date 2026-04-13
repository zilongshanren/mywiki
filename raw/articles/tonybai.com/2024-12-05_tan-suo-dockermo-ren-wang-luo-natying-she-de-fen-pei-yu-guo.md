---
title: 探索Docker默认网络NAT映射的分配与过滤行为
url: https://tonybai.com/2024/12/05/exploring-nat-mapping-assignment-and-filtering-behavior-of-docker-default-network/
published: '2024-12-05'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 探索Docker默认网络NAT映射的分配与过滤行为

![](../../assets/6ed38b963b468815.png)


[本文永久链接](https://tonybai.com/2024/12/05/exploring-nat-mapping-assignment-and-filtering-behavior-of-docker-default-network) – https://tonybai.com/2024/12/05/exploring-nat-mapping-assignment-and-filtering-behavior-of-docker-default-network

在《[WebRTC第一课：网络架构与NAT工作原理](https://tonybai.com/2024/11/27/webrtc-first-lesson-network-architecture-and-how-nat-work/)》一文中，我们对WebRTC的网路架构进行说明，了解到了NAT的工作原理、[RFC 3489](https://datatracker.ietf.org/doc/html/rfc3489)对NAT的四种传统分类以及较新的[RFC 4787](https://datatracker.ietf.org/doc/html/rfc4787)中按分配行为和过滤行为对NAT行为的分类。

不过，“纸上得来终觉浅，绝知此事要躬行”，在这篇文章中，我打算选取一个具体的NAT实现进行案例研究(Case Study)。在市面上的NAT实现中，Docker容器的网络NAT绝对是最容易获得的一种实现。因此，我们将把[Docker默认网络](https://tonybai.com/2016/01/15/understanding-container-networking-on-single-host/)的NAT实现机制作为本篇的研究对象，探索该NAT的分配行为和过滤行为，以确定Docker默认网络的NAT类型。

为了这次探索，我们首选需要构建实验网络环境。

## 1. 构建实验环境

Docker默认网络使用NAT（网络地址转换）来允许容器访问外部网络。创建容器时，如果未指定网络设置，容器会连接到默认的”bridge”网络，并分配一个内部IP地址（通常在172.17.0.0/16范围内）。Docker在宿主机上创建一个虚拟网桥（docker0），作为容器与外部网络的接口。当容器尝试访问外部网络时，使用源网络地址转换（SNAT），将内部IP和端口转换为宿主机的IP和一个随机高位端口，以便与外部网络通信。Docker通过配置iptables规则来实现这些NAT功能，处理数据包的转发、地址转换和过滤。

基于上述描述，我们用两台主机来构建一个实验环境，拓扑图如下：

![](../../assets/32560a7d1bd53bd5.png)


从上图可以看到：我们的实验环境有两台主机：192.168.0.124和192.168.0.125。在124上，我们基于docker默认网络启动一个容器，在该容器中放置一个用于NAT打洞验证的nat-hole-puncher程序，该程序通过访问192.168.0.125上的udp-client-addr-display程序在Docker的NAT上留下一个“洞”，然后我们在125上使用[nc(natcat)工具](https://man.openbsd.org/nc.1)验证是否可以通过这个洞向容器发送数据。

我们要确定Docker默认网络NAT的具体类型，需要进行一些测试来观察其行为。具体来说，主要需要关注两个方面：

- 端口分配行为：观察NAT是如何为内部主机（容器）分配外部端口的。
- 过滤行为：检查NAT如何处理和过滤入站数据的，是否与源IP、源Port有关等。

接下来，我们来准备一下验证NAT类型需要的两个程序：nat-hole-puncher和udp-client-addr-display。

## 2. 准备nat-hole-puncher程序和udp-client-addr-display程序

下图描述了nat-hole-puncher、udp-client-addr-display以及nc命令的交互流程：

![](../../assets/53cb4e5dc6a4aa83.png)


三者的交互流程在图中已经用文字标记的十分清楚了。

根据该图中的逻辑，我们分别实现一下nat-hole-puncher和udp-client-addr-display。

下面是nat-hole-puncher的源码：

```
// docker-default-nat/nat-hole-puncher/main.go
package main
import (
"fmt"
"net"
"os"
"strconv"
)
func main() {
if len(os.Args) != 5 {
fmt.Println("Usage: nat-hole-puncher <local_ip> <local_port> <target_ip> <target_port>")
return
}
localIP := os.Args[1]
localPort := os.Args[2]
targetIP := os.Args[3]
targetPort := os.Args[4]
// 向target_ip:target_port发送数据
err := sendUDPMessage("Hello, World!", localIP, localPort, targetIP+":"+targetPort)
if err != nil {
fmt.Println("Error sending message:", err)
return
}
fmt.Println("sending message to", targetIP+":"+targetPort, "ok")
// 向target_ip:target_port+1发送数据
p, _ := strconv.Atoi(targetPort)
nextTargetPort := fmt.Sprintf("%d", p+1)
err = sendUDPMessage("Hello, World!", localIP, localPort, targetIP+":"+nextTargetPort)
if err != nil {
fmt.Println("Error sending message:", err)
return
}
fmt.Println("sending message to", targetIP+":"+nextTargetPort, "ok")
// 重新监听local addr
startUDPReceiver(localIP, localPort)
}
func sendUDPMessage(message, localIP, localPort, target string) error {
addr, err := net.ResolveUDPAddr("udp", target)
if err != nil {
return err
}
lport, _ := strconv.Atoi(localPort)
conn, err := net.DialUDP("udp", &net.UDPAddr{
IP: net.ParseIP(localIP),
Port: lport,
}, addr)
if err != nil {
return err
}
defer conn.Close()
// 发送数据
_, err = conn.Write([]byte(message))
if err != nil {
return err
}
return nil
}
func startUDPReceiver(ip, port string) {
addr, err := net.ResolveUDPAddr("udp", ip+":"+port)
if err != nil {
fmt.Println("Error resolving address:", err)
return
}
conn, err := net.ListenUDP("udp", addr)
if err != nil {
fmt.Println("Error listening:", err)
return
}
defer conn.Close()
fmt.Println("listen address:", ip+":"+port, "ok")
buf := make([]byte, 1024)
for {
n, senderAddr, err := conn.ReadFromUDP(buf)
if err != nil {
fmt.Println("Error reading:", err)
return
}
fmt.Printf("Received message: %s from %s\n", string(buf[:n]), senderAddr.String())
}
}
```


我们将其编译完打到镜像中去，Makefile和Dockerfile如下：

```
// docker-default-nat/nat-hole-puncher/Makefile
all:
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o nat-hole-puncher main.go
image:
docker build -t nat-hole-puncher .
// docker-default-nat/nat-hole-puncher/Dockerfile
# 使用 Alpine 作为基础镜像
FROM alpine:latest
# 创建工作目录
WORKDIR /app
# 复制已编译的可执行文件到镜像中
COPY nat-hole-puncher .
# 设置文件权限
RUN chmod +x nat-hole-puncher
```


执行构建和打镜像命令：

```
$ make
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o nat-hole-puncher main.go
$ make image
docker build -t nat-hole-puncher .
[+] Building 0.7s (9/9) FINISHED docker:default
=> [internal] load .dockerignore 0.0s
=> => transferring context: 2B 0.0s
=> [internal] load build definition from Dockerfile 0.0s
=> => transferring dockerfile: 265B 0.0s
=> [internal] load metadata for docker.io/library/alpine:latest 0.0s
=> [1/4] FROM docker.io/library/alpine:latest 0.0s
=> [internal] load build context 0.0s
=> => transferring context: 2.70MB 0.0s
=> CACHED [2/4] WORKDIR /app 0.0s
=> [3/4] COPY nat-hole-puncher . 0.2s
=> [4/4] RUN chmod +x nat-hole-puncher 0.3s
=> exporting to image 0.1s
=> => exporting layers 0.1s
=> => writing image sha256:fec6c105f36b1acce5e3b0a5fb173f3cac5c700c2b07d1dc0422a5917f934530 0.0s
=> => naming to docker.io/library/nat-hole-puncher 0.0s
```


接下来，我们再来看看udp-client-addr-display源码：

```
// docker-default-nat/udp-client-addr-display/main.go
package main
import (
"fmt"
"net"
"os"
"strconv"
"sync"
)
func main() {
if len(os.Args) != 3 {
fmt.Println("Usage: udp-client-addr-display <local_ip> <local_port>")
return
}
localIP := os.Args[1]
localPort := os.Args[2]
var wg sync.WaitGroup
wg.Add(2)
go func() {
defer wg.Done()
startUDPReceiver(localIP, localPort)
}()
go func() {
defer wg.Done()
p, _ := strconv.Atoi(localPort)
nextLocalPort := fmt.Sprintf("%d", p+1)
startUDPReceiver(localIP, nextLocalPort)
}()
wg.Wait()
}
func startUDPReceiver(localIP, localPort string) {
addr, err := net.ResolveUDPAddr("udp", localIP+":"+localPort)
if err != nil {
fmt.Println("Error:", err)
return
}
conn, err := net.ListenUDP("udp", addr)
if err != nil {
fmt.Println("Error:", err)
return
}
defer conn.Close()
buf := make([]byte, 1024)
n, clientAddr, err := conn.ReadFromUDP(buf)
if err != nil {
fmt.Println("Error:", err)
return
}
fmt.Printf("Received message: %s from %s\n", string(buf[:n]), clientAddr.String())
}
```


现在两个程序都就绪了，接下来我们就开始我们的探索。

## 3. 探索步骤

我们先在192.168.0.125上启动udp-client-addr-display，监听6000和6001 UDP端口：

```
// 在192.168.0.125上执行
$./udp-client-addr-display 192.168.0.125 6000
```


然后在192.168.0.124上创建client1容器：

```
// 在192.168.0.124上执行
$docker run -d --name client1 nat-hole-puncher:latest sleep infinity
eeebc0fbe3c7d56e7f43cd5af19a18e65a703b3f987115c521e81bb8cdc6c0be
```


获取client1容器的IP地址：

```
// 在192.168.0.124上执行
$docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' client1
172.17.0.5
```


启动client1容器中的nat-hole-puncher程序，绑定本地5000端口，然后向192.168.0.125的6000和6001端口发送数据包：

```
$ docker exec client1 /app/nat-hole-puncher 172.17.0.5 5000 192.168.0.125 6000
sending message to 192.168.0.125:6000 ok
sending message to 192.168.0.125:6001 ok
listen address: 172.17.0.5:5000 ok
```


之后，我们会在125的udp-client-addr-display输出中看到如下结果：

```
./udp-client-addr-display 192.168.0.125 6000
Received message: Hello, World! from 192.168.0.124:5000
Received message: Hello, World! from 192.168.0.124:5000
```


通过这个结果我们得到了NAT映射后的源地址和端口：192.168.0.124:5000。

现在我们在125上用nc程序向该映射后的地址发送三个UDP包：

```
$ echo "hello from 192.168.0.125:6000" | nc -u -p 6000 -v 192.168.0.124 5000
Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Connected to 192.168.0.124:5000.
Ncat: 30 bytes sent, 0 bytes received in 0.01 seconds.
$ echo "hello from 192.168.0.125:6001" | nc -u -p 6001 -v 192.168.0.124 5000
Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Connected to 192.168.0.124:5000.
Ncat: 30 bytes sent, 0 bytes received in 0.01 seconds.
$ echo "hello from 192.168.0.125:6002" | nc -u -p 6002 -v 192.168.0.124 5000
Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Connected to 192.168.0.124:5000.
Ncat: 30 bytes sent, 0 bytes received in 0.01 seconds.
```


在124上，我们看到nat-hole-puncher程序输出如下结果：

```
Received message: hello from 192.168.0.125:6000
from 192.168.0.125:6000
Received message: hello from 192.168.0.125:6001
from 192.168.0.125:6001
```


## 4. 探索后的结论

通过上面的执行步骤以及输出的结果，我们从端口分配行为和过滤行为这两方面分析一下Docker默认网络NAT的行为特征。

首先，我们先来看端口分配行为。

在上面的探索步骤中，我们先后执行了：

- 172.17.0.5:5000 -> 192.168.0.125:6000
- 172.17.0.5:5000 -> 192.168.0.125:6001

但从udp-client-addr-display的输出来看：

```
Received message: Hello, World! from 192.168.0.124:5000
Received message: Hello, World! from 192.168.0.124:5000
```


Docker默认网络的NAT的端口分配行为肯定不是Address and Port-Dependent Mapping，那么到底是不是Address-Dependent Mapping的呢？你可以将nat-hole-puncher/main.go中的startUDPReceiver调用注释掉，然后再在另外一台机器192.168.0.126上启动一个udp-client-addr-display（监听7000和7001），然后在124上分别执行：

```
$ docker exec client1 /app/nat-hole-puncher 172.17.0.5 5000 192.168.0.125 6000
sending message to 192.168.0.125:6000 ok
sending message to 192.168.0.125:6001 ok
$ docker exec client1 /app/nat-hole-puncher 172.17.0.4 5000 192.168.0.126 7000
sending message to 192.168.0.126:7000 ok
sending message to 192.168.0.126:7001 ok
```


而从125和126上的udp-client-addr-display的输出来看：

```
//125:
./udp-client-addr-display 192.168.0.125 6000
Received message: Hello, World! from 192.168.0.124:5000
Received message: Hello, World! from 192.168.0.124:5000
//126:
./udp-client-addr-display 192.168.0.126 7000
Received message: Hello, World! from 192.168.0.124:5000
Received message: Hello, World! from 192.168.0.124:5000
```


可以看出：即便是target ip不同，只要源ip+port一致，NAT也只会分配同一个端口(这里是5000)，显然**在端口分配行为上，Docker默认网络的NAT是Endpoint-Independent Mapping类型的**！

我们再来看过滤行为。nat-hole-puncher在NAT打洞后，我们在125上使用nc工具向该“洞”发UDP包，结果是只有nat-hole-puncher发过的目的ip和端口(比如6000和6001)才可以成功将数据通过“洞”发给nat-hole-puncher。换个端口（比如6002），数据都会被丢弃掉。即便我们没有测试从不同IP向“洞”发送udp数据，但上述过滤行为已经足够让我们判定**Docker默认网络的NAT过滤行为属于Address and Port-Dependent Filtering**。

综合上述两个行为特征，如果按照传统NAT类型划分，**Docker默认网络的NAT应该属于端口受限锥形**。

## 5. 小结

本文探讨了Docker默认网络的NAT(网络地址转换)行为。我们通过构建实验环境，使用两个自制程序(nat-hole-puncher和udp-client-addr-display)以及nc工具，来测试和分析Docker NAT的端口分配行为和过滤行为。

主要的探索结论如下：

-
端口分配行为：Docker默认网络的NAT表现为Endpoint-Independent Mapping类型。即无论目标IP和端口如何变化，只要源IP和端口相同，NAT就会分配相同的外部端口。

-
过滤行为：Docker默认网络的NAT表现为Address and Port-Dependent Filtering类型。只有之前通信过的特定IP和端口组合才能成功穿透NAT发送数据包到内部网络。


基于这两种行为特征，我们可以得出结论：按照传统NAT类型划分，Docker默认网络的NAT属于端口受限锥形(Port Restricted Cone)NAT。

不过，在真正实践中判断一个NAT的类型无需如此费劲，[RFC3489给出检测NAT类型（传统四种类别）的流程图](https://www.rfc-editor.org/rfc/rfc3489#section-10.2)：

![](../../assets/4637c742c1420e3b.png)


github上也有上述算法的开源的实现，比如：[pystun3](https://github.com/talkiq/pystun3)。下面是利用pystun3检测网络NAT类型的方法：

```
$docker run -it python:3-alpine /bin/sh
/ # pip install pystun3
/ # pystun3
NAT Type: Symmetric NAT
External IP: xxx.xxx.xxx.xxx
External Port: yyyy
```


注：这里pystun3的检测结果是多层NAT的结果，并非单纯的Docker默认网络的NAT类型。


本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/blob/master/docker-default-nat)下载 – https://github.com/bigwhite/experiments/blob/master/docker-default-nat

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论