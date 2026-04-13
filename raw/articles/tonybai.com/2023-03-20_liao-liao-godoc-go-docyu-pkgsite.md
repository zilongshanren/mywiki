---
title: 聊聊godoc、go doc与pkgsite
url: https://tonybai.com/2023/03/20/godoc-vs-go-doc-vs-pkgsite/
published: '2023-03-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 聊聊godoc、go doc与pkgsite

![](../../assets/929b6cded30495b6.png)


[本文永久链接](https://tonybai.com/2023/03/20/godoc-vs-go-doc-vs-pkgsite) – https://tonybai.com/2023/03/20/godoc-vs-go-doc-vs-pkgsite

就像[上一篇文章聊到的Go内置单元测试框架](https://tonybai.com/2023/03/15/an-intro-of-go-subtest/)一样，[既重视语言特性，又不忘对Go软件项目提供整体环境特性的Go](https://tonybai.com/2022/05/04/the-paper-of-go-programming-language-and-environment)在诞生伊始就定义了[如何在源码中通过注释编写代码文档的格式](https://go.dev/doc/comment)，并提供了基于代码注释实时生成Go文档并支持文档查看的工具。

而一些早期的语言，比如C、C++等则需要使用第三方工具(如[doxygen](https://www.doxygen.nl))以及这些工具规定的特定格式编写文档，缺少语言原生的文档标准与工具，给后期开发人员之间的协作带去了麻烦。

查看文档是开发人员日常必不可少的开发活动之一。Go语言从诞生那天起就十分重视项目文档的建设，为此Go为gopher们提供了多种丰富的文档查看工具，除了在[Go官方网站](https://go.dev/doc)可以在线查看到最新稳定发布版的文档之外，Go还为开发人员提供了**本地离线查看文档的工具**，比如：[godoc](https://github.com/golang/tools/tree/master/cmd/godoc)、go doc以及[pkgsite](https://github.com/golang/pkgsite)。在这篇短文中，我们就来分别看看这三个Go文档查看工具。

## 一. godoc

很多接触Go语言较早的gopher都知道，Go安装包中曾原生自带了一个和go、gofmt一起发布的文档查看工具：**godoc**。它也是**Go的第一个文档查看工具**！

godoc实质上是一个web服务，它会在本地离线建立起一个web形式的Go文档中心，对本地安装的go包提供文档查看服务。

当我们执行下面命令时这个文档中心服务就启动了：

```
$godoc -http=localhost:8080
```


在浏览器地址栏输入http://localhost:8080打开Go文档中心首页，godoc默认会展示\$GOROOT下的目录结构：

![](../../assets/912296aa20eca508.png)


我们看到首页顶部的菜单与**Go旧版官方主页**的菜单基本如出一辙。

再点击Packages我们会看到godoc会展示本地包的参考文档页面：

![](../../assets/97cf85f1222ed17f.png)


Go包参考文档页面将包分为几类：标准库包（Standard library）、第三方包（Third party）和其它包（Other packages），其中的第三方包就是本地\$GOPATH下面的各个包。

在“Packages”页面中的Standard Library下面找到标准库io包，点击打开Go io包的参考文档页面如下图所示：

![](../../assets/589a255472575ed6.png)


这样我们就可以离线以web页面的形式查看go module相关文档了! [Go 1.13版本](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)之前，这就像是在本地建立一个Go官方站点的mirror site。

并且，godoc支持-play命令行选项，可以启动playground功能，go文档中的example也可以像online playground那样运行：

![](../../assets/da79cc6d78b3b101.png)


不过这个功能**不是离线的**，不能使用本机的Go编译器和环境运行，需要连接网络进行。

[Godoc还支持查看历史版本的Go文档](https://tonybai.com/2020/12/15/how-to-see-the-manual-of-go-history-version)，这个之前写过，大家可以移步阅读。

接下来聊聊godoc这个工具的现状！很遗憾，从[Go 1.13版本](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)开始，godoc就失去了官方工具的地位，不再和go、gofmt一起内置在Go安装包中发布了！如果你想使用godoc，需要使用下面命令自行安装：

```
$go install golang.org/x/tools/cmd/godoc@latest
```


随着2019年[Go新官方站点的发布](https://tonybai.com/2019/11/14/what-the-godev-website-bring-to-gophers)，godoc风格的web文档查看方式渐渐被人遗忘了！godoc.org也关闭了。

2021年末，godoc工具也被标记为deprecated了(虽然这两年还有几个commit)，标志着godoc正式退出历史舞台！

![](../../assets/c4cb08c5e636f30b.png)


注：怀旧的gopher建立了godoc.org的替代站点：https://godocs.io，由Go社区维护。


那么，没有了godoc，我们如何离线查询go文档呢？我们接下来来聊聊本地查看go文档的命令行工具go doc。

## 二. go doc

go doc是Go语言自带的命令行工具，可以用来查看本地安装的Go包的文档。与godoc不同的是，go doc不需要启动HTTP服务器，直接在终端中使用即可：

![](../../assets/0b53f98f52b4595c.png)


自go doc在[Go 1.5版本](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)加入Go工具链之后，它就和go get、go build一样成为了Gopher们每日必用的go子命令。

在查看包文档时，go doc在命令行上接受的参数使用了Go语法的格式，这使得go doc的上手使用几乎是“零门槛”：

```
go doc <pkg>
go doc <sym>[.<methodOrField>]
go doc [<pkg>.]<sym>[.<methodOrField>]
go doc [<pkg>.][<sym>.]<methodOrField>
```


下面我们就来简要介绍一下如何使用go doc查看各类包文档。

- 查看标准库文档

我们可以在任意路径下执行go doc命令查看标准库文档，下面是一些查看标准库不同元素文档的命令示例。

查看标准库net/http包文档：

```
$go doc net/http
或
$go doc http
```


查看http包的Get函数的文档：

```
$ go doc net/http.Get
或
$ go doc http.Get
```


查看http包中结构体类型Requset中字段Form的文档：

```
$go doc net/http.Request.Form
或
$go doc http.Request.Form
```


- 查看当前项目文档

除了查看标准库文档，我们在从事项目开发时很可能会查看当前项目中其他包的文档以决定如何使用这些包。go doc也可以很方便地查看当前路径下项目的文档，我们还以已经下载到本地（比如：~/temp/gocmpp）的github.com/bigwhite/gocmpp项目为例。

查看当前路径下的包的文档：

```
$go doc
package cmpp // import "github.com/bigwhite/gocmpp"
const CmppActiveTestReqPktLen uint32 = 12 ...
const CmppConnReqPktLen uint32 = 4 + 4 + 4 + 6 + 16 + 1 + 4 ...
const Cmpp2DeliverReqPktMaxLen uint32 = 12 + 233 ...
... ...
```


查看当前路径下包的导出元素的文档：

```
$go doc CmppActiveTestReqPktLen
package cmpp // import "."
const (
CmppActiveTestReqPktLen uint32 = 12 //12d, 0xc
CmppActiveTestRspPktLen uint32 = 12 + 1 //13d, 0xd
)
Packet length const for cmpp active test request and response packets.
```


我们看到包导出元素(比如CmppActiveTestReqPktLen)的头字母是大写的，go doc不会将其解析为包名，而会认为它是当前包中的某个元素。

通过-u选项，我们也可以查看当前路径下包的非导出元素的文档：

```
$go doc -u newPacketWriter
package cmpp // import "github.com/bigwhite/gocmpp"
func newPacketWriter(initSize uint32) *packetWriter
```


查看当前路径的子路径下的包的文档：

```
$go doc ./utils
或
$go doc utils
package cmpputils // import "github.com/bigwhite/gocmpp/utils"
var ErrInvalidUtf8Rune = errors.New("Not Invalid Utf8 runes")
func GB18030ToUtf8(in string) (string, error)
... ...
```


- 查看项目依赖的第三方module的文档

如今，go module已经是Go依赖管理的标准模式了。一个项目依赖的go module会被cache到go mod专有路径中，包含不同版本和其代码。因此，目前go doc在查看项目依赖的第三方module的文档时，会自动到go mod cache中找到该module，并显示其文档，例如：

```
$go doc github.com/lni/dragonboat/v3
package dragonboat // import "github.com/lni/dragonboat/v3"
Package dragonboat is a multi-group Raft implementation.
The NodeHost struct is the facade interface for all features provided by the
dragonboat package. Each NodeHost instance usually runs on a separate host
managing its CPU, storage and network resources. Each NodeHost can manage Raft
nodes from many different Raft groups known as Raft clusters. Each Raft cluster
is identified by its ClusterID and it usually consists of multiple nodes,
each identified its NodeID value. Nodes from the same Raft cluster can be
considered as replicas of the same data, they are suppose to be distributed on
different NodeHost instances across the network, this brings fault tolerance to
machine and network failures as application data stored in the Raft cluster will
be available as long as the majority of its managing NodeHost instances (i.e.
its underlying hosts) are available.
... ...
const DragonboatMajor = 3 ...
var ErrClosed = errors.New("dragonboat: closed") ...
var ErrInvalidOperation = errors.New("invalid operation") ...
var ErrBadKey = errors.New("bad key try again later") ...
var ErrNoSnapshot = errors.New("no snapshot available") ...
func IsTempError(err error) bool
func WriteHealthMetrics(w io.Writer)
type ClusterInfo struct{ ... }
type GossipInfo struct{ ... }
type INodeUser interface{ ... }
type Membership struct{ ... }
type NodeHost struct{ ... }
func NewNodeHost(nhConfig config.NodeHostConfig) (*NodeHost, error)
type NodeHostInfo struct{ ... }
type NodeHostInfoOption struct{ ... }
var DefaultNodeHostInfoOption NodeHostInfoOption
type RequestResult struct{ ... }
type RequestResultCode int
type RequestState struct{ ... }
type SnapshotOption struct{ ... }
var DefaultSnapshotOption SnapshotOption
type SysOpState struct{ ... }
type Target = string
```


如果要查看的依赖的module尚未get到本地，那么go doc会提示你先go get。

在传统gopath模式下，go doc则会自动到\$GOPATH下面查找对应的包路径，如果该包存在，就可以输出该包的相关文档。因此我们可以在任意路径下通过go doc查看第三方项目包的文档：

```
$export GO111MODULE=off
$go doc github.com/bigwhite/gocmpp.CmppActiveTestReqPktLen
package cmpp // import "github.com/bigwhite/gocmpp"
const (
CmppActiveTestReqPktLen uint32 = 12 //12d, 0xc
CmppActiveTestRspPktLen uint32 = 12 + 1 //13d, 0xd
)
Packet length const for cmpp active test request and response packets.
```


- 查看源码

如果要查看包的源码，我们没有必要将目录切换到该包所在路径并通过编辑器打开源文件查看，通过go doc我们一样可以查看包的完整源码或包的某元素的源码。

查看标准库包源码：

```
$go doc -src fmt.Printf
package fmt // import "fmt"
// Printf formats according to a format specifier and writes to standard output.
// It returns the number of bytes written and any write error encountered.
func Printf(format string, a ...interface{}) (n int, err error) {
return Fprintf(os.Stdout, format, a...)
}
```


查看当前路径包中导出元素的源码：

```
$go doc -src NewClient
package cmpp // import "."
// New establishes a new cmpp client.
func NewClient(typ Type) *Client {
return &Client{
typ: typ,
}
}
```


查看当前路径包中未导出元素的源码：

```
$go doc -u -src newPacketWriter
package cmpp // import "github.com/bigwhite/gocmpp"
func newPacketWriter(initSize uint32) *packetWriter {
buf := make([]byte, 0, initSize)
return &packetWriter{
wb: bytes.NewBuffer(buf),
}
}
```


查看当前项目依赖的第三方包的某个函数的源码：

```
$go doc -src github.com/lni/dragonboat/v3 IsTempError
package dragonboat // import "github.com/lni/dragonboat/v3"
// IsTempError returns a boolean value indicating whether the specified error
// is a temporary error that worth to be retried later with the exact same
// input, potentially on a more suitable NodeHost instance.
func IsTempError(err error) bool {
return err == ErrSystemBusy ||
err == ErrClusterClosed ||
err == ErrClusterNotInitialized ||
err == ErrClusterNotReady ||
err == ErrTimeout ||
err == ErrClosed
}
```


go doc是原生工具，也非常强大，但是go doc是cli工具，不是能满足所有人的“口味”，那么小伙伴们可能会问：是否有godoc那样的离线web文档中心的替代工具呢？我们接下来就来聊聊[pkgsite](https://github.com/golang/pkgsite)。

## 三. pkgsite

Go官方推出新包文档站点后，在使用体验上的确有不少改善，新增了很多功能，下面是io包的在新包文档站点下的呈现形式：

![](../../assets/d1cddf48ae8fe7aa.png)


Go老版官方站点与godoc是匹配的，同样，Go在推出新版[Go包文档站点](https://pkg.go.dev)后，也开源了其站点源码，这个项目就是[pkgsite](https://github.com/golang/pkgsite)。我们可以通过下面命令安装pkgsite：

```
$go install golang.org/x/pkgsite/cmd/pkgsite@latest
```


和godoc一样，pkgsite支持local mode，即离线模式。我们在某个go module下面(这里在gocmpp module的本地路径下)执行下面命令即可：

```
$pkgsite
2023/03/16 23:26:37 Info: go/packages.Load(["all"]) loaded 247 packages from . in 3.762976863s
2023/03/16 23:26:37 Info: Listening on addr http://localhost:8080
```


我们看到pkgsite加载了“all”范围的所有包以及当前module的包。打开浏览器，输入localhost:8080，便可以打开pkgsite服务的首页：

![](../../assets/fa3eaa7f2cac3b82.png)


注：通过go help packages查看all的含义


搜索你要的包，得到列表后，打开包的详情页面，其展示形式与官方pkg.go.dev是一模一样的。

不过目前[pkgsite在local模式下查看标准库包是有问题的](https://github.com/golang/go/issues/57742)，页面无法打开。

总体感觉pkgsite目前主要还是以满足官方站点在线文档查看需求为主，[对local模式的支持不是很好](https://github.com/golang/go/issues/39827)，用起来也较为晦涩，这里也有gopher抱怨，[希望能重新恢复godoc工具](https://github.com/golang/go/issues/50229)，但估计Go官方肯定不会答应，毕竟不想维护两套展示风格不同的工具。pkgsite后续可能会有改善，但目前看来优先级似乎不高。

## 四. 小结

日常开发工作中，我们总是online的，通过pkg.go.dev的在线文档可以满足绝大部分需求。

如果真是处于离线状态，我个人建议你的开发机上至少要将godoc、pkgsite都装上。对于习惯了godoc的gopher而言，虽然godoc已“作废”，但Go基于注释的文档兼容性不错，godoc依然可以满足初步的离线文档查看需求。如果你已经喜欢上Go新站点的风格，对新站点功能有依赖，那么pkgsite也是可以使用的。再辅以go doc命令行工具，离线查看文档需求也能满足个七七八八。

注：如果你使用的是像goland这样的IDE工具，其内置离线文档功能可能就会满足你的需求。


Go社区也有一些的第三方的离线go文档工具，比如[貘兄(go101)](https://go101.org)的[golds](https://github.com/go101/golds)也是不错的。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论