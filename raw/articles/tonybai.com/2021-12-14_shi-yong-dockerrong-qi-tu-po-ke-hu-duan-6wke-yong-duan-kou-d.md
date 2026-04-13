---
title: 使用Docker容器突破客户端6w可用端口的误区
url: https://tonybai.com/2021/12/14/the-misconception-of-using-docker-to-break-out-of-6w-ports-of-the-client/
published: '2021-12-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Docker容器突破客户端6w可用端口的误区

![](../../assets/582a750917556de6.jpeg)


[本文永久链接](https://tonybai.com/2021/12/14/the-misconception-of-using-docker-to-break-out-of-6w-ports-of-the-client) – https://tonybai.com/2021/12/14/the-misconception-of-using-docker-to-break-out-of-6w-ports-of-the-client

近期的一个项目刚刚完成了第一个版本的开发，经过一段时间的自测与集成测试，功能问题已经不是重点了。项目在初期设定了性能目标，压测与性能优化势在必行，因此这一阶段我们都在做压测前的准备，包括压测方案、环境部署、各种工具的开发等。在互联网大厂的一波接着一波的熏陶与教育下，**但凡一个有点用户量的系统，交付前不压测与优化一下，似乎都不好意思上线^_^**。

压测准备阶段逃不过“模拟并发连接数量”这一环节，我们第一次压测设定的系统运行背景是100w的并发长连接。**那么怎么构造出这么多的并发连接呢**？有经验的朋友可能知道这句话中隐含的“难点”，那就是一个客户机最多向外面建立65535-1024+1=**64512**个连接。为什么会这样呢？这是因为一个TCP连接由一个四元组唯一确定，这个四元组是**（源端口，源地址，目的地址，目的端口）**。这个四元组中的源端口是一个16bit的短整型，它的表示范围是0~65535。但1024及以下的端口号通常为系统保留，因此用户可用的端口号仅剩下64512个。

当一个客户机向服务端建立TCP连接时，四元组中的目的地址、目的端口是固定的，客户机通常只有一个IP地址，这样源地址也是固定的，于是唯一的变数就是源端口了。而源端口在这种情况下仅有64512种变化，因此客户机向外建立的连接数量也就受到了限制。

于是有人想到了[Docker容器](https://tonybai.com/tag/docker)。由于[容器具有独立的网络命名空间以及独立的IP地址](https://tonybai.com/2016/01/15/understanding-container-networking-on-single-host/)，这样容器可以向外建立的连接就不受到宿主机的限制，真的是这样么？

下面我们在一台宿主机上用多个容器模拟的“客户机”向该宿主机上的一个Server程序建立连接，我们看是否能突破6w壁垒。下面是server端程序的代码(仅作示例，勿要深究)：

```
// https://github.com/bigwhite/experiments/tree/master/break-out-of-6w-ports/server/server.go
func main() {
l, err := net.Listen("tcp", "0.0.0.0:9000")
if err != nil {
fmt.Println("error listening:", err.Error())
return
}
defer l.Close()
fmt.Println("listen ok")
var mu sync.Mutex
var count int
for {
conn, err := l.Accept()
if err != nil {
fmt.Println("error accept:", err)
return
}
fmt.Printf("recv conn from [%s]\n", conn.RemoteAddr())
go func(conn net.Conn) {
var b = make([]byte, 10)
for {
_, err := conn.Read(b)
if err != nil {
e, ok := err.(net.Error)
if ok {
if e.Timeout() {
continue
}
}
mu.Lock()
count--
mu.Unlock()
return
}
}
}(conn)
mu.Lock()
count++
mu.Unlock()
fmt.Println("total count =", count)
}
select {}
}
```


这个server程序运行于宿主机上(宿主机的各个资源参数需要你自行调整，比如：/proc/sys/fs/file-max、/proc/sys/fs/nr_open等，可参考[这里](https://colobu.com/2019/02/23/1m-go-tcp-connection/))，并监听9000端口，每accept一个来自客户机的TCP连接，就会创建一个goroutine来处理这个TCP连接。

客户机模拟客户端连接的程序如下：

```
// https://github.com/bigwhite/experiments/tree/master/break-out-of-6w-ports/client/client.go
func main() {
var count = 25000
for i := 0; i < count; i++ {
go func() {
conn, err := net.Dial("tcp", "192.168.49.6:9000") // 192.168.49.6是宿主机地址
if err != nil {
fmt.Println("net.Dial error:", err)
return
}
for {
_, err := conn.Write([]byte("ping"))
if err != nil {
fmt.Println("conn.Write error:", err)
return
}
time.Sleep(100 * time.Second)
}
}()
}
select {}
}
```


从代码中可以看到，每个客户机客户端程序会向服务端建立25000个TCP长连接。这里将client端放入基于alpine:3.14.2 image的容器中运行，容器中每个程序可以对外建立的连接数量我们可以通过下面命令的输出计算出来：

```
$ docker run alpine:3.14.2 cat /proc/sys/net/ipv4/ip_local_port_range
32768 60999
> 60999-32768+1
28232
```


代码中每个client建立25000个连接，在28232范围之内，正常建立全部连接不是问题。实际的试验结果也证明了这一点：我们启动server后，逐一用下面命令启动多个client：

```
$go build client.go
$docker run -v /Users/tonybai/Go/src/github.com/bigwhite/experiments/break-out-of-6w-ports/client/client:/root/client alpine:3.14.2 /root/client
```


创建三个client后，我们很快就能看到Server端完成了75000个连接的创建：

```
listen ok
recv conn from [172.17.0.2:50238]
... ...
recv conn from [172.17.0.4:35202]
total count = 74997
recv conn from [172.17.0.4:35282]
total count = 74998
recv conn from [172.17.0.4:33168]
total count = 74999
recv conn from [172.17.0.4:44703]
total count = 75000
```


我们看到，**在同一个宿主机上利用容器充当客户端我们轻松突破客户端可用端口的限制**。

那么如果server程序在另外的一个主机上呢? 我们是否还可以这么顺利的建立如此多的连接呢？我们来试一下，执行的命令与过程与上面大致相同，但server端在建立64000左右连接后，无论再加入几个client向服务端建立连接，server端的总连接数也不会向上了。你或许怀疑server端程序有问题？其实不是，此时如果你在另外一台机器上向server建立连接，连接可以很快的建立成功。

问题还是出在了Docker所在的那台宿主机上了。为什么各个客户端建立不上连接了呢？从server端的一些输出日志可见端倪：

```
// 192.168.49.6是客户端所在宿主机的ip地址
recv conn from [192.168.49.6:11431]
total count = 64001
recv conn from [192.168.49.6:28365]
total count = 64002
```


我们看到无论docker容器内ip地址是多少，从宿主机连出来后的ip都是192.168.49.6（宿主机的ip地址），默认情况下，Docker容器访问宿主机外部的主机时，其源地址和端口都会被SNAT成宿主机的IP及某一个随机端口，下面是一个简略的SNAT转换表：

![](../../assets/811f05037c6a4c7e.png)


我们看到docker中的请求经过NAT后其源ip转换为宿主机的源ip地址192.168.49.6，源端口为宿主机的一个随机端口(1024~65535范围内)。客户端发出请求后，server端处理并返回响应，响应回到宿主机后，NAT会根据上面的转换表，根据nat后的源ip、nat后的源port、目的ip和目的port找到唯一的源ip和源port，并将替换数据包中相应的字段，这样数据包才能返回给对应的容器中的客户端程序。这样当目的ip、目的port以及nat后的源ip都是“固定值”的情况下，就只能要求nat后的源port不能重复，而nat后的源port的可选范围却只能为1024~65535，当nat后的源port耗尽，容器中的客户端程序就再也无法与server建立新连接了。

我们再重新审视一下nat转换表，nat后的源port是自动分配的，目的port是知名port，不能变化，剩下的只有nat后的源ip地址与目的ip地址是可变动的要素。每新增一种nat后的源ip或目的ip，都可以新增加64521(65535-1024+1)个到server端的TCP连接容量。

下面我们就以添加多个目的ip的方式为例，看看docker如何突破6w可用端口的约束。我们的server服务器是一台ubuntu 20.04的虚拟机，我们可以通过修改netplan配置的方式为enp0s8网卡（连接内部网络, ip为192.168.49.5）添加额外两个ip：192.168.49.15和192.168.49.25。

```
$ cat /etc/netplan/00-installer-config.yaml
# This is the network config written by 'subiquity'
network:
ethernets:
enp0s3:
addresses: [10.0.2.15/24]
gateway4: 10.0.2.2
nameservers:
addresses: [8.8.8.8,127.0.0.53]
dhcp4: no
enp0s8:
addresses: [192.168.49.5/24,192.168.49.15/24,192.168.49.25/24]
gateway4: 192.168.49.1
nameservers:
addresses: [8.8.8.8,127.0.0.53]
dhcp4: no
version: 2
```


执行sudo netplan apply后，我们可以看到enp0s8网口上配置的三个ip信息如下，

```
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
link/ether 08:00:27:f1:bb:67 brd ff:ff:ff:ff:ff:ff
inet 192.168.49.5/24 brd 192.168.49.255 scope global enp0s8
valid_lft forever preferred_lft forever
inet 192.168.49.15/24 brd 192.168.49.255 scope global secondary enp0s8
valid_lft forever preferred_lft forever
inet 192.168.49.25/24 brd 192.168.49.255 scope global secondary enp0s8
valid_lft forever preferred_lft forever
inet6 fe80::a00:27ff:fef1:bb67/64 scope link
valid_lft forever preferred_lft forever
```


现在我们将按下图所示通过docker向server建立75000个连接(每个容器建立25000个)：

![](../../assets/2f1a2e5119b71760.png)


我们改造一下server程序，让其不仅输出RemoteAddr，还要输出LocalAddr：

```
// https://github.com/bigwhite/experiments/tree/master/break-out-of-6w-ports/server/server1.go
fmt.Printf("recv conn from [%s], localaddr: [%s]\n", conn.RemoteAddr(), conn.LocalAddr())
```


为了方便向client传入要连接的server的地址，我们也改造一下client：

```
// https://github.com/bigwhite/experiments/tree/master/break-out-of-6w-ports/client/client_with_remoteaddr.go
var remoteIP string
func init() {
flag.StringVar(&remoteIP, "rip", "", "remoteIP")
}
func main() {
flag.Parse()
var count = 25000
for i := 0; i < count; i++ {
go func() {
conn, err := net.Dial("tcp", remoteIP+":9000")
if err != nil {
fmt.Println("net.Dial error:", err)
return
}
for {
_, err := conn.Write([]byte("ping"))
if err != nil {
fmt.Println("conn.Write error:", err)
return
}
time.Sleep(100 * time.Second)
}
}()
}
select {}
}
```


接下来我们就将新client放入容器中执行，并分别用三个remote ip向server建立连接：

```
$go build -o client client_with_remoteaddr.go
$docker run -v /Users/tonybai/Go/src/github.com/bigwhite/experiments/break-out-of-6w-ports/client/client:/root/client alpine:3.14.2 /root/client -rip 192.168.49.5
$docker run -v /Users/tonybai/Go/src/github.com/bigwhite/experiments/break-out-of-6w-ports/client/client:/root/client alpine:3.14.2 /root/client -rip 192.168.49.15
$docker run -v /Users/tonybai/Go/src/github.com/bigwhite/experiments/break-out-of-6w-ports/client/client:/root/client alpine:3.14.2 /root/client -rip 192.168.49.25
```


我们很快就在server的log中看到所有连接都建立成功了：

```
... ...
recv conn from [192.168.49.6:43505], localaddr: [192.168.49.25:9000]
total count = 74998
recv conn from [192.168.49.6:43483], localaddr: [192.168.49.25:9000]
total count = 74999
recv conn from [192.168.49.6:47790], localaddr: [192.168.49.25:9000]
total count = 75000
```


并且当我们以37816这个端口为例，我们查询一下日志：

```
$ grep 37816 server.log
recv conn from [192.168.49.6:37816], localaddr: [192.168.49.5:9000]
recv conn from [192.168.49.6:37816], localaddr: [192.168.49.15:9000]
recv conn from [192.168.49.6:37816], localaddr: [192.168.49.25:9000]
```


我们看到有三个来自192.168.49.6:37816的连接，但目的地址均不相同，这也印证了我们的分析是正确的。

以上就是对使用docker突破客户端可用端口的限制的误区的分析，所谓的误区**即当客户端与server在同一台宿主机上可突破6w端口，就认为客户端与server在不同主机上时不需做任何改变也同样可以突破6w**。上面的分析证实了我们要么增加服务端的ip，要么增加客户端的ip，或对两者的ip进行同时增加，后两个情况大家可以自行进行试验，这里就不赘述了。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强，欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

![](../../assets/769fc94e8bba6b65.png)


微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论