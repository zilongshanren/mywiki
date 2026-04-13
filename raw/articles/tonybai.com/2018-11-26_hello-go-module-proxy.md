---
title: Hello，Go module proxy
url: https://tonybai.com/2018/11/26/hello-go-module-proxy/
published: '2018-11-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Hello，Go module proxy

## 一. Go module引入的幸福与“无奈”

在[《Go 1.11中值得关注的几个变化》](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)一文中，我们知道了[Go语言](https://tonybai.com/tag/go)通过引入[module的概念](https://github.com/golang/go/wiki/Modules)进而引入了Go tool的另外一种工作模式[module-aware mode](https://tip.golang.org/cmd/go/#hdr-Module_aware_go_get)。在新的工作模式下，[Go module](https://tonybai.com/2018/07/15/hello-go-module/)支持了[Versioned Go](https://research.swtch.com/vgo-tour)，并初步解决了包依赖管理的问题。

对于全世界绝大多数Gophers来说，[Go module](https://tonybai.com/2018/07/15/hello-go-module/)的引入带来的都是**满满的幸福感**，但是对于位于中国大陆地区的Gopher来说，在这种幸福感袭来的同时，也夹带了一丝**“无奈”**。其原因在于module-aware mode下，go tool默认不再使用传统GOPATH下或top vendor下面的包了，而是在GOPATH/pkg/mod(go 1.11中是这个位置，也许以后版本这个位置会变动)下面寻找Go module的local cache。

由于众所周知的原因，在大陆地区我们无法直接通过go get命令或git clone获取到一些第三方包，这其中最常见的就是golang.org/x下面的各种优秀的包。但是在传统的GOPATH mode下，我们可以先从golang.org/x/xxx的mirror站点github.com/golang/xxx上git clone这些包，然后将其重命名为golang.org/x/xxx。这样也能勉强通过开发者本地的编译。又或将这些包放入[vendor](https://tonybai.com/2015/07/31/understand-go15-vendor)目录并提交到repo中，也能实现正确的构建。

但是go module引入后，一旦工作在module-aware mode下，go build将不care GOPATH下或是vendor下的包，而是到GOPATH/pkg/mod查询是否有module的cache，如果没有，则会去下载某个版本的module，而对于golang.org/x/xxx下面的module，在大陆地区往往会get失败。

有朋友可能会说，可以继续通过其他mirror站点下载再改名啊？理论上是可行的。但是现实中，这样做很繁琐。我们先来看看go module的专用本地缓存目录结构：

```
➜ /Users/tony/go/pkg/mod $tree -L 7
.
├── cache
│ └── download
│ └── golang.org
│ └── x
│ └── text
│ └── @v
│ ├── list
│ ├── v0.1.0.info
│ ├── v0.1.0.mod
│ ├── v0.1.0.zip
│ ├── v0.1.0.ziphash
│ ├── v0.3.0.info
│ ├── v0.3.0.mod
│ ├── v0.3.0.zip
│ └── v0.3.0.ziphash
└── golang.org
└── x
├── text@v0.1.0
└── text@v0.3.0
```


我们看到mod下的结构是经过精心设计的。cache/download下面存储了每个module的“元信息”以及每个module不同version的zip包。比如在这里，我们看到了[golang.org/x/text](https://github.com/golang/text)这个module的v0.1.0和v0.3.0两个版本的元信息和对应的源码zip；同时mod下还直接存有text module的两个版本v0.1.0和v0.3.0的源码。

如果我们还像GOPATH mode下那种通过“mirror站下载再改名”的方式来满足go build的需求，那么我们需要手工分别制作某个module的不同版本的元信息以及源码目录，制作元信息时还要了解每个文件（比如：xx.info、xxx.mod等）的内容的生成机制，这样的方法的**“体验”**并不好。

## 二. “解铃还须系铃人” – 使用Go module proxy

那么问题来了：大陆Gopher如何能在go module开启的状态下享受go module带来的福利呢？ “解铃还须系铃人”！答案就在go 1.11中。Go 1.11在引入go module的同时，还引入了Go module proxy(go help goproxy）的概念。

go get命令默认情况下，无论是在gopath mode还是module-aware mode，都是直接从vcs服务(比如github、gitlab等)下载module的。但是Go 1.11中，我们可以通过设置GOPROXY环境变量来做一些改变：让Go命令从其他地方下载module。比如：

```
export GOPROXY=https://goproxy.io
```


一旦如上面设置生效后，后续go命令会通过[go module download protocol](https://golang.org/cmd/go/#hdr-Module_proxy_protocol)与proxy交互下载特定版本的module。聪明的小伙伴们一定想到了。如果我们在某个[国外VPS](https://m.do.co/c/bff6eed92687)上搭建一个go module proxy server的实现，我们将可以通过该proxy下载到类似golang.org/x下面的module。与此同时，一些诸如从github.com上get package慢等次要的问题可能也被一并fix掉了。

显然Go官方加入go proxy的初衷并非为了解决中国大陆地区的下载qiang外包的烦恼的。但不可否认的是，GOPROXY让gopher在versioned go的基础上，对module和package的获取行为上增加了一层控制和干预能力。

## 三. Go module proxy的实现之一：athens

至于proxy具体带来怎样的控制和干预能力、给gopher带来哪些好处，就要看我们选择了哪种go module proxy的具体实现了。

当前go module proxy的一个受关注度较高的实现是微软[Azure](https://azure.microsoft.com/)开发人员[Aaron Schlesinger](https://github.com/arschles)主导[开源](https://open.microsoft.com/2018/08/28/announcing-project-athens-gophersource-go-community/)的[athens](https://github.com/gomods/athens)。athens项目的目标是致力于建设一个联合的、组织良好的go proxy网络（而不是单一的global go module proxy），以提升gopher使用module的体验。athens项目重点关注于：

- Go module代理服务器的实现，用于边缘部署
- 一个带身份验证的module proxy的协议
- 一个module公证服务器，用来验证module源代码
- 满足企业级需求，提供一种方案让企业可以指定包含/排除的Go外部module列表

athens项目从今年[8月份宣布开源](https://open.microsoft.com/2018/08/28/announcing-project-athens-gophersource-go-community/)到现在依旧很年轻，截止至本文发布时，athens刚刚发布了第一个[Beta版本v0.2.0](https://github.com/gomods/athens/releases/tag/v0.2.0)，还尚未发布正式的1.0.0版本。

接下来，我们来试用一下athens，并对其主要功能进行一些验证。

### 1. 安装athens

athens的工作原理并不复杂，athens在收到用户请求的时候，会检查本地缓存是否有对应版本的module，如果有，则直接返回应答；如果没有。则会向upstream vcs请求下载对应的module。获取成功后cache到本地，并給请求端返回应答。athens强调”immutable(不变性)”的理念。这样即便upstream vcs的原始module对应的repo被删除了或被force push破坏了，只要module缓存在athens自己的存储上了，客户端的module请求就会得到满足，gopher的build不会因为repo被删除而受到破坏。

athens目前提供了基于docker和基于k8s的安装方式（物理binary安装目前尚未提供）。我们选择在一个[国外的VPS](https://m.do.co/c/bff6eed92687)上使用docker方式安装athens:

```
# docker run -d -v /root/athens-storage:/var/lib/athens -e ATHENS_DISK_STORAGE_ROOT=/var/lib/athens -e ATHENS_STORAGE_TYPE=disk --name athens-proxy --restart always -p 3000:3000 gomods/athens:v0.2.0
30cdcc55028de0028eae910758a6ee08ecaf960ab0e79a25e8a1353b8e8ff57c
# docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
30cdcc55028d gomods/athens:v0.2.0 "athens-proxy -con..." 12 seconds ago Up 12 seconds 0.0.0.0:3000->3000/tcp athens-proxy
# docker logs -f athens-proxy
buffalo: Unless you set SESSION_SECRET env variable, your session storage is not protected!
time="2018-11-26T09:59:09Z" level=info msg="Exporter not specified. Traces won't be exported"
buffalo: Starting application at :3000
```


我们使用local disk作为athens的存储方案。我们在本地建立/root/athens-storage目录，并将其挂载到容器的/var/lib/athens路径下，并设定ATHENS_DISK_STORAGE_ROOT=/var/lib/athens。从athens container的启动日志来看，容器已经启动成功了！

### 2. 通过athens下载public repo中的module

接下来我们来验证一下通过athens获取public module。我们还使用[gocmpp](https://github.com/bigwhite/gocmpp)这个代码，它依赖golang.org/x/text module下面的package。

![img{512x368}](../../assets/238c51291dfb675f.png)


我们首先clean一下$GOPATH/pkg/mod，然后设置一下GOPROXY环境变量：

```
export GOPROXY=YOUR_VPS_IP:3000
```


接下来，我们进入到gocmpp目录下，执行go build：

```
$go build
go: finding golang.org/x/text v0.3.0
go: downloading golang.org/x/text v0.3.0
```


我们看到go compiler顺利下载了golang.org/x/text module相关文件。再来看一下athens的日志：

```
# docker logs -f athens-proxy
handler: GET /golang.org/x/text/@v/v0.3.0.info [200]
handler: GET /golang.org/x/text/@v/v0.3.0.mod [200]
handler: GET /golang.org/x/text/@v/v0.3.0.zip [200]
```


如果此时我们再次尝试通过athens获取text module，由于text module已经cache到了athens上，所以后续的get速度会很快。并且由于download protocol中获取module是通过get zip包的方式，理论上也要比clone repo快许多。

### 3. 通过athens下载private repo中的module

athens这个go module proxy的实现为module get行为提供的额外控制力之一就包括可以用来获取private repo中的module，这也是一个企业级的需求。通常企业private repo都是有身份验证的，因此我们需要在athens中配置访问private repo的账号和凭证信息。目前athens官方文档中提供了通过.netrc方式访问带有身份验证的private repo的功能，这种方式的不足之处就是要将password明文形式存储在athens部署的host上。

我用bitbucket上的一个private repo来模拟私有git仓库：bitbucket.org/bigwhite/mydog。

![img{512x368}](../../assets/79d299692fe85609.png)


为了让athens可以正常访问该private repo，我们需要为athens做一些额外配置：添加.netrc。

我们创建.netrc文件：

```
//.netrc
machine bitbucket.org
login MY_USERNAME1
password MY_PASSWORD1
machine gitlab.com
login MY_USERNAME2
password MY_PASSWORD2
```


我们在.netrc中配置了我们访问各大repo service的user和password。

接下来，我们需要重新创建一下athens container：

先停掉并删除当前athens-proxy container：

```
# docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
30cdcc55028d gomods/athens:v0.2.0 "athens-proxy -con..." 3 hours ago Up 3 hours 0.0.0.0:3000->3000/tcp athens-proxy
# docker stop athens-proxy
athens-proxy
# docker rm athens-proxy
athens-proxy
```


重新创建athens container时，我们将前面创建的.netrc挂载到container中，并通过ATHENS_NETRC_PATH指定container内.netrc的位置：

```
# docker run -d -v $ATHENS_STORAGE:/var/lib/athens -v /root/athens-install:/root -e ATHENS_NETRC_PATH=/root/.netrc -e ATHENS_DISK_STORAGE_ROOT=/var/lib/athens -e ATHENS_STORAGE_TYPE=disk --name athens-proxy --restart always -p 3000:3000 gomods/athens:v0.2.0
751c88648fd4075aa22ff3a4cc62f6467b50d415b6fbf465af247fc6a3978c2e
```


接下来，我们就来编写一个“驱动”程序：testmydog

```
$tree ./testmydog
./testmydog
├── go.mod
└── main.go
0 directories, 2 files
```


main.go的内容如下：

```
package main
import (
"fmt"
"bitbucket.org/bigwhite/mydog"
)
func main() {
fmt.Println(mydog.Add(1, 2))
}
```


我们来构建一下该程序：

```
$go build
go: finding bitbucket.org/bigwhite/mydog latest
go: downloading bitbucket.org/bigwhite/mydog v0.0.0-20181126081441-684c772f5624
```


go命令从athens成功下载了我的私有repo中的mydog module。我们再来看看athens的日志：

```
handler: GET /bitbucket.org/bigwhite/mydog/@v/list/ [200]
handler: GET /bitbucket.org/bigwhite/mydog/@latest/ [200]
handler: GET /bitbucket.org/bigwhite/mydog/@v/v0.0.0-20181126081441-684c772f5624.zip [200]
handler: GET /bitbucket.org/bigwhite/mydog/@v/v0.0.0-20181126081441-684c772f5624.mod [200]
```


### 4 athens的global proxy

athens还提供了一个试验性的global public proxy：athens.azurefd.net供全球gopher使用。不过在我这里通过联通网络是无法ping通该proxy的：

```
$ping athens.azurefd.net
PING standard.t-0001.t-msedge.net (13.107.246.10): 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1
Request timeout for icmp_seq 2
^C
--- standard.t-0001.t-msedge.net ping statistics ---
4 packets transmitted, 0 packets received, 100.0% packet loss
```


但是在我国外的VPS上，与该global proxy的通信是正常的：

```
# ping athens.azurefd.net
PING standard.t-0001.t-msedge.net (13.107.246.10) 56(84) bytes of data.
64 bytes from 13.107.246.10: icmp_seq=1 ttl=122 time=1.94 ms
64 bytes from 13.107.246.10: icmp_seq=2 ttl=122 time=1.21 ms
64 bytes from 13.107.246.10: icmp_seq=3 ttl=122 time=1.30 ms
--- standard.t-0001.t-msedge.net ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 1.217/1.491/1.949/0.328 ms
```


如果你是国内gopher，那么建议该global proxy还是先不要用了。

## 四. 另外一个go module proxy的实现：goproxy

github上还有另外一个go module proxy的实现：[goproxy](https://github.com/goproxyio/goproxy)。该项目目前看仅是一个public module proxy，并未提供对private repo中module获取的支持。

不过该项目提供的global proxy: https://goproxy.io/ 却是可以在国内使用的，并且速度还很快！Gopher们只需将该proxy配置到GOPROXY中即可：

```
export GOPROXY=https://goproxy.io
```


## 五. 小结

和goproxy项目相比，athens项目显然有更大的“野心”，也有Microsoft这个平台作为背后支撑。但athens毕竟开发时间较短，还有很长之路要走。待Go module在Go 1.12中成型并成熟时，希望那个时候的athens项目能给我们带来更多惊喜。

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

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

老白， goproxy.io 我用了下发现不太稳定。

现在阿里也推出go代理了：

GOPROXY=https://mirrors.aliyun.com/goproxy/

非常好用。推荐。

感谢提醒。