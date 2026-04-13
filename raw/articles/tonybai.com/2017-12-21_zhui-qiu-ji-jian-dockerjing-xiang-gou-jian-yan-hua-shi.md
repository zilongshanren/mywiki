---
title: 追求极简：Docker镜像构建演化史
url: https://tonybai.com/2017/12/21/the-concise-history-of-docker-image-building/
published: '2017-12-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 追求极简：Docker镜像构建演化史

本文首发于[CSDN](https://www.csdn.net/)[《程序员》](http://programmer.csdn.net/)杂志[2017.12期](http://blog.csdn.net/qq_40027052/article/details/78720370)，这里是[原文地址](https://mp.weixin.qq.com/s/6--iyRTiAtpSpsLd0Tgf8w)。

本文为《程序员》杂志授权转载，谢绝其他转载。全文如下：

自从2013年[dotCloud公司](https://en.wikipedia.org/wiki/DotCloud)(现已改名为[Docker Inc](https://en.wikipedia.org/wiki/Docker,_Inc.))发布[Docker容器技术](http://tonybai.com/tag/docker)以来，到目前为止已经有四年多的时间了。这期间[Docker技术](https://en.wikipedia.org/wiki/Docker_(software))飞速发展，并催生出一个生机勃勃的、以轻量级容器技术为基础的庞大的容器平台生态圈。作为Docker三大核心技术之一的镜像技术在Docker的快速发展之路上可谓功不可没：镜像让容器真正插上了翅膀，实现了容器自身的重用和标准化传播，使得开发、交付、运维流水线上的各个角色真正围绕同一交付物，“test what you write, ship what you test”成为现实。

对于已经接纳和使用Docker技术在日常开发工作中的开发者而言，构建Docker镜像已经是家常便饭。但如何更高效地构建以及构建出Size更小的镜像却是很多Docker技术初学者心中常见的疑问，甚至是一些老手都未曾细致考量过的问题。本文将从一个Docker用户角度来阐述Docker镜像构建的演化史，希望能起到一定的解惑作用。

### 一、镜像：继承中的创新

谈镜像构建之前，我们先来简要说下**镜像**。

Docker技术本质上并不是新技术，而是将已有技术进行了更好地整合和包装。内核容器技术以一种完整形态最早出现在[Sun公司](https://en.wikipedia.org/wiki/Sun_Microsystems)的[Solaris操作系统](https://en.wikipedia.org/wiki/Solaris_(operating_system))上，[Solaris](http://tonybai.com/tag/solaris)是当时最先进的服务器操作系统。2005年Sun发布了[Solaris Container](https://en.wikipedia.org/wiki/Solaris_Containers)技术，从此开启了内核容器之门。

2008年，以Google公司开发人员为主导实现的Linux Container(即[LXC](https://en.wikipedia.org/wiki/LXC))功能在被merge到[Linux内核](https://www.kernel.org/)中。LXC是一种内核级虚拟化技术，主要基于[Namespaces](https://en.wikipedia.org/wiki/Cgroups#NAMESPACE-ISOLATION)和[Cgroups](https://en.wikipedia.org/wiki/Cgroups)技术，实现共享一个操作系统内核前提下的进程资源隔离，为进程提供独立的虚拟执行环境，这样的一个虚拟的执行环境就是一个容器。本质上说，LXC容器与现在的Docker所提供容器是一样的。Docker也是基于Namespaces和Cgroups技术之上实现的，Docker的**创新之处**在于其基于[Union File System](https://en.wikipedia.org/wiki/UnionFS)技术定义了一套容器打包规范，真正将容器中的应用及其运行的所有依赖都封装到一种特定格式的文件中去，而这种文件就被称为**镜像**（即image），原理见下图（引自Docker官网）：

![img{512x368}](../../assets/371e684b3e86d8b6.png)


图1：Docker镜像原理

镜像是容器的“序列化”标准，这一创新为容器的存储、重用和传输奠定了基础。并且“坐上了巨轮”的容器镜像可以传播到世界每一个角落，这无疑助力了容器技术的飞速发展。

与[Solaris Container](https://en.wikipedia.org/wiki/Solaris_Containers)、LXC等早期内核容器技术不同，Docker为开发者提供了开发者体验良好的工具集，这其中就包括了用于镜像构建的Dockerfile以及一种用于编写Dockerfile领域特定语言。采用Dockerfile方式构建成为镜像构建的标准方法，其可重复、可自动化、可维护以及分层精确控制等特点是采用传统采用docker commit命令提交的镜像所不能比拟的。

### 二、“镜像是个筐”：初学者的认知

**“镜像是个筐，什么都往里面装”** – 这句俏皮话可能是大部分Docker初学者对镜像最初认知的真实写照。这里我们用一个例子来生动地展示一下。我们将httpserver.go这个源文件编译为httpd程序并通过镜像发布，考虑到被编译的源码并非本文重点，这里使用了一个极简的demo代码：

```
//httpserver.go
package main
import (
"fmt"
"net/http"
)
func main() {
fmt.Println("http daemon start")
fmt.Println(" -> listen on port:8080")
http.ListenAndServe(":8080", nil)
}
```


接下来，我们来编写一个用于构建目标image的Dockerfile：

```
From ubuntu:14.04
RUN apt-get update \
&& apt-get install -y software-properties-common \
&& add-apt-repository ppa:gophers/archive \
&& apt-get update \
&& apt-get install -y golang-1.9-go \
git \
&& rm -rf /var/lib/apt/lists/*
ENV GOPATH /root/go
ENV GOROOT /usr/lib/go-1.9
ENV PATH="/usr/lib/go-1.9/bin:${PATH}"
COPY ./httpserver.go /root/httpserver.go
RUN go build -o /root/httpd /root/httpserver.go \
&& chmod +x /root/httpd
WORKDIR /root
ENTRYPOINT ["/root/httpd"]
```


构建这个Image：

```
# docker build -t repodemo/httpd:latest .
//...构建输出这里省略...
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
repodemo/httpd latest 183dbef8eba6 2 minutes ago 550MB
ubuntu 14.04 dea1945146b9 2 months ago 188MB
```


整个镜像的构建过程因环境而定。如果您的网络速度一般，这个构建过程可能会花费你10多分钟甚至更多。最终如我们所愿，基于repodemo/httpd:latest这个镜像的容器可以正常运行：

```
# docker run repodemo/httpd
http daemon start
-> listen on port:8080
```


一个Dockerfile最终生产出一个镜像。Dockerfile由若干Command组成，每个Command执行结果都会单独形成一个layer。我们来探索一下构建出来的镜像：

```
# docker history 183dbef8eba6
IMAGE CREATED CREATED BY SIZE COMMENT
183dbef8eba6 21 minutes ago /bin/sh -c #(nop) ENTRYPOINT ["/root/httpd"] 0B
27aa721c6f6b 21 minutes ago /bin/sh -c #(nop) WORKDIR /root 0B
a9d968c704f7 21 minutes ago /bin/sh -c go build -o /root/httpd /root/h... 6.14MB
... ...
aef7700a9036 30 minutes ago /bin/sh -c apt-get update && apt-get... 356MB
.... ...
<missing> 2 months ago /bin/sh -c #(nop) ADD file:8f997234193c2f5... 188MB
```


我们去除掉那些Size为0或很小的layer，我们看到三个size占比较大的layer，见下图：

![img{512x368}](../../assets/dfc1b7f6a0a48400.png)


图2：Docker镜像分层探索

虽然Docker引擎利用r缓存机制可以让同主机下非首次的镜像构建执行得很快，但是在Docker技术热情催化下的这种构建思路让docker镜像在存储和传输方面的优势荡然无存，要知道一个ubuntu-server 16.04的虚拟机ISO文件的大小也就不过600多MB而已。

### 三、”理性的回归”：builder模式的崛起

Docker使用者在新技术接触初期的热情“冷却”之后迎来了“理性的回归”。根据上面分层镜像的图示，我们发现最终镜像中包含构建环境是多余的，我们只需要在最终镜像中包含足够支撑httpd运行的运行环境即可，而base image自身就可以满足。于是我们应该去除不必要的中间层：

![img{512x368}](../../assets/7dfd85f34d95466b.png)


图3：去除不必要的分层

现在问题来了！如果不在同一镜像中完成应用构建，那么在哪里、由谁来构建应用呢？至少有两种方法：

- 在本地构建并COPY到镜像中；
- 借助构建者镜像(builder image)构建。

不过方法1本地构建有很多局限性，比如：本地环境无法复用、无法很好融入持续集成/持续交付流水线等。借助builder image进行构建已经成为Docker社区的一个最佳实践，Docker官方为此也推出了各种主流编程语言的官方base image，比如：[go](http://tonybai.com/tag/go)、[java](http://tonybai.com/tag/java)、node、[python](http://tonybai.com/tag/python)以及[ruby](http://tonybai.com/tag/ruby)等。借助builder image进行镜像构建的流程原理如下图：

![img{512x368}](../../assets/551c5e4c7863c892.png)


图4：借助builder image进行镜像构建的流程图

通过原理图，我们可以看到整个目标镜像的构建被分为了两个阶段：

- 第一阶段：构建负责编译源码的构建者镜像；
- 第二阶段：将第一阶段的输出作为输入，构建出最终的目标镜像。

我们选择golang:1.9.2作为builder base image，构建者镜像的Dockerfile.build如下：

```
// Dockerfile.build
FROM golang:1.9.2
WORKDIR /go/src
COPY ./httpserver.go .
RUN go build -o httpd ./httpserver.go
```


执行构建：

```
# docker build -t repodemo/httpd-builder:latest -f Dockerfile.build .
```


构建好的应用程序httpd放在了镜像repodemo/httpd-builder中的/go/src目录下，我们需要一些“胶水”命令来连接两个构建阶段，这些命令将httpd从**构建者镜像**中取出并作为下一阶段构建的输入：

```
# docker create --name extract-httpserver repodemo/httpd-builder
# docker cp extract-httpserver:/go/src/httpd ./httpd
# docker rm -f extract-httpserver
# docker rmi repodemo/httpd-builder
```


通过上面的命令，我们将编译好的httpd程序拷贝到了本地。下面是目标镜像的Dockerfile：

```
//Dockerfile.target
From ubuntu:14.04
COPY ./httpd /root/httpd
RUN chmod +x /root/httpd
WORKDIR /root
ENTRYPOINT ["/root/httpd"]
```


接下来我们来构建目标镜像：

```
# docker build -t repodemo/httpd:latest -f Dockerfile.target .
```


我们来看看这个镜像的“体格”：

```
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
repodemo/httpd latest e3d009d6e919 12 seconds ago 200MB
```


200MB！目标镜像的Size降为原来的 1/2 还多。

### 四、“像赛车那样减去所有不必要的东西”：追求最小镜像

前面我们构建出的镜像的Size已经缩小到200MB，但这还不够。200MB的“体格”在我们的网络环境下缓存和传输仍然很难令人满意。我们要为镜像进一步减重，减到尽可能的小，就像赛车那样，为了能减轻重量将所有不必要的东西都拆除掉：我们仅保留能支撑我们的应用运行的必要库、命令，其余的一律不纳入目标镜像。当然不仅仅是Size上的原因，小镜像还有额外的好处，比如：内存占用小，启动速度快，更加高效；不会因其他不必要的工具、库的漏洞而被攻击，减少了“攻击面”，更加安全。

![img{512x368}](../../assets/65d4f744931833e1.png)


图5：目标镜像还能更小些吗？

一般应用开发者不会从scratch镜像从头构建自己的base image以及目标镜像的，开发者会挑选适合的base image。一些“蝇量级”甚至是“草量级”的官方base image的出现为这种情况提供了条件。

![img{512x368}](../../assets/a95c142470e74f08.png)


图6：一些base image的Size比较(来自imagelayers.io截图)

单从image的size上来说，busybox更小。不过busybox默认的libc实现是uClibc，而我们通常运行环境使用的libc实现都是glibc，因此我们要么选择静态编译程序，要么使用busybox:glibc镜像作为base image。

而 alpine image 是另外一种蝇量级 base image，它使用了比 glibc 更小更安全的 [musl libc](http://www.musl-libc.org/) 库。 不过和 busybox image 相比，alpine image 体积还是略大。除了因为 musl比uClibc 大一些之外，alpine还在镜像中添加了自己的包管理系统apk，开发者可以使用apk在基于alpine的镜像中添 加需要的包或工具。因此，对于普通开发者而言，alpine image显然是更佳的选择。不过alpine使用的libc实现为[musl](http://www.musl-libc.org/)，与基于glibc上编译出来的应用程序不兼容。如果直接将前面构建出的httpd应用塞入alpine，在容器启动时会遇到下面错误，因为加载器找不到glibc这个动态共享库文件：

```
standard_init_linux.go:185: exec user process caused "no such file or directory"
```


对于Go应用来说，我们可以采用静态编译的程序，但一旦采用静态编译，也就意味着我们将失去一些libc提供的原生能力，比如：在linux上，你无法使用系统提供的DNS解析能力，只能使用Go自实现的DNS解析器。

我们还可以采用基于alpine的builder image，golang base image就提供了alpine 版本。 我们就用这种方式构建出一个基于alpine base image的极小目标镜像。

![img{512x368}](../../assets/a82b00ac7404d8c4.png)


图7：借助 alpine builder image 进行镜像构建的流程图

我们新建两个用于 alpine 版本目标镜像构建的 Dockerfile：Dockerfile.build.alpine 和Dockerfile.target.alpine：

```
//Dockerfile.build.alpine
FROM golang:alpine
WORKDIR /go/src
COPY ./httpserver.go .
RUN go build -o httpd ./httpserver.go
// Dockerfile.target.alpine
From alpine
COPY ./httpd /root/httpd
RUN chmod +x /root/httpd
WORKDIR /root
ENTRYPOINT ["/root/httpd"]
```


构建builder镜像：

```
# docker build -t repodemo/httpd-alpine-builder:latest -f Dockerfile.build.alpine .
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
repodemo/httpd-alpine-builder latest d5b5f8813d77 About a minute ago 275MB
```


执行“胶水”命令：

```
# docker create --name extract-httpserver repodemo/httpd-alpine-builder
# docker cp extract-httpserver:/go/src/httpd ./httpd
# docker rm -f extract-httpserver
# docker rmi repodemo/httpd-alpine-builder
```


构建目标镜像：

```
# docker build -t repodemo/httpd-alpine -f Dockerfile.target.alpine .
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
repodemo/httpd-alpine latest 895de7f785dd 13 seconds ago 16.2MB
```


16.2MB！目标镜像的Size降为不到原来的十分之一。我们得到了预期的结果。

### 五、“要有光，于是便有了光”：对多阶段构建的支持

至此，虽然我们实现了目标Image的最小化，但是整个构建过程却是十分繁琐，我们需要准备两个Dockerfile、需要准备“胶水”命令、需要清理中间产物等。作为Docker用户，我们希望用一个Dockerfile就能解决所有问题，于是就有了Docker引擎对多阶段构建(multi-stage build)的支持。注意：这个特性非常新，只有Docker 17.05.0-ce及以后的版本才能支持。

现在我们就按照“多阶段构建”的语法将上面的Dockerfile.build.alpine和Dockerfile.target.alpine合并到一个Dockerfile中：

```
//Dockerfile
FROM golang:alpine as builder
WORKDIR /go/src
COPY httpserver.go .
RUN go build -o httpd ./httpserver.go
From alpine:latest
WORKDIR /root/
COPY --from=builder /go/src/httpd .
RUN chmod +x /root/httpd
ENTRYPOINT ["/root/httpd"]
```


Dockerfile的语法还是很简明和易理解的。即使是你第一次看到这个语法也能大致猜出六成含义。与之前Dockefile最大的不同在于在支持多阶段构建的Dockerfile中我们可以写多个“From baseimage”的语句了，每个From语句开启一个构建阶段，并且可以通过“as”语法为此阶段构建命名(比如这里的builder)。我们还可以通过COPY命令在两个阶段构建产物之间传递数据，比如这里传递的httpd应用，这个工作之前我们是使用“胶水”代码完成的。

构建目标镜像：

```
# docker build -t repodemo/httpd-multi-stage .
# docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
repodemo/httpd-multi-stage latest 35e494aa5c6f 2 minutes ago 16.2MB
```


我们看到通过多阶段构建特性构建的Docker Image与我们之前通过builder模式构建的镜像在效果上是等价的。

### 六、来到现实

沿着时间的轨迹，Docker 镜像构建走到了今天。追求又快又小的镜像已成为了 Docker 社区 的共识。社区在自创 builder 镜像构建的最佳实践后终于迎来了多阶段构建这柄利器，从此构建 出极简的镜像将不再困难。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/71dbd0d64d261ba9.jpg)


© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

赞！文章质量很高，持续关注大师的博客。

谢谢，欢迎关注。

go应用可以直接from scratch吧，那镜像的大小就是应用的大小了