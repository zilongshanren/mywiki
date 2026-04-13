---
title: Go 1.18新特性前瞻：Go工作区模式
url: https://tonybai.com/2021/11/12/go-workspace-mode-in-go-1-18/
published: '2021-11-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.18新特性前瞻：Go工作区模式

![](../../assets/4ac1d6497f80662a.png)


[本文永久链接](https://tonybai.com/2021/11/12/go-workspace-mode-in-go-1-18) – https://tonybai.com/2021/11/12/go-workspace-mode-in-go-1-18

**Go 1.18版本如无意外，将于2022年2月发布**。

在这个版本中，除了包含万众期待的[Go泛型](https://mp.weixin.qq.com/s/ur1eiZl4PKbF1PqELAdfKg)之外，还包含很多实用的功能特性，Go工作区模式(Go workspace mode)就是其中之一，它弥补了当前go module构建模式的一些不足，堪称是**go module构建模式的最后一块拼图**。这篇文章我们就来看看什么是Go工作区模式，它究竟能解决什么问题。

### 一. 引子

#### 1. replace带来的烦恼

近期在研究[raft算法](https://raft.github.io/)，参考的是[etcd的raft实现](https://github.com/etcd-io/etcd)。etcd还提供了一个[raftexample](https://github.com/etcd-io/etcd/tree/main/contrib/raftexample)的样例来说明如何实现基于raft的分布式应用。

要学习raftexample，我们首先要对其进行构建。[raftexample的README.md](https://github.com/etcd-io/etcd/blob/main/contrib/raftexample/README.md)文件中有raftexample编译方法的步骤，但这份安装步骤还停留在[Go 1.11版本](https://tonybai.com/2018/11/19/some-changes-in-go-1-11)之前的gopath构建模式时期。如今我们要构建它，最好将其先转换为一个go module后再在go module模式下进行构建。不知道如何将一个legecy go project转换为go module的朋友可以去看一下我的极客时间专栏[《Go语言第一课》](http://gk.link/a/10AVZ)^_^。

我们先把raftexample单独copy出来，放到一个单独的目录下，然后进入raftexample目录并在该其下执行下面命令添加go.mod文件，这里我们构建使用的go版本是[go 1.17](https://mp.weixin.qq.com/s/y_pC6GYeZnKuHG8ycNy6rg)：

```
$cd raftexample
$go mod init github.com/bigwhite/raftexample
```


生成的go.mod内容如下：

```
$cat go.mod
module github.com/bigwhite/raftexample
go 1.17
```


接下来，我们执行go mod tidy命令让go命令自行分析raftexample的依赖并下载这些依赖：

```
$go mod tidy
go: finding module for package go.etcd.io/etcd/client/pkg/v3/types
go: finding module for package go.etcd.io/etcd/raft/v3/raftpb
go: finding module for package go.etcd.io/etcd/client/pkg/v3/fileutil
go: finding module for package go.etcd.io/etcd/server/v3/storage/wal
go: finding module for package go.etcd.io/etcd/server/v3/etcdserver/api/v2stats
go: finding module for package go.etcd.io/etcd/server/v3/etcdserver/api/snap
go: finding module for package go.etcd.io/etcd/server/v3/etcdserver/api/rafthttp
go: finding module for package go.etcd.io/etcd/raft/v3
... ...
go: downloading go.etcd.io/etcd/pkg/v3 v3.5.1
go: downloading go.etcd.io/etcd/api/v3 v3.5.1
go: finding module for package go.etcd.io/etcd/server/v3/storage/wal/walpb
go: finding module for package go.etcd.io/etcd/server/v3/storage/wal
github.com/bigwhite/raftexample imports
go.etcd.io/etcd/server/v3/storage/wal: module go.etcd.io/etcd/server/v3@latest found (v3.5.1), but does not contain package go.etcd.io/etcd/server/v3/storage/wal
github.com/bigwhite/raftexample imports
go.etcd.io/etcd/server/v3/storage/wal/walpb: module go.etcd.io/etcd/server/v3@latest found (v3.5.1), but does not contain package go.etcd.io/etcd/server/v3/storage/wal/walpb
```


go mod tidy命令报错，提示没找到server/v3.5.1下面的go.etcd.io/etcd/server/v3/storage/wal和go.etcd.io/etcd/server/v3/storage/wal/walpb包。翻看etcd工程server/v3.5.1标签下的源码，server下的确不包含storage这个目录。但在**main分支**下，storage目录是存在的。这很可能是etcd项目自v3.5.0版本开始进行多module改造(原先etcd项目是一个module，后该项目下拆分为多个module，并使用多module标签来管理)后的bug。

怎么处理这一情况呢？我们只能祭出replace大法了！刚说过etcd的main分支下storage目录是存在的，于是我们就手工修改一下raftexample的go.mod文件，添加下面这一行配置：

```
replace go.etcd.io/etcd/server/v3 v3.5.1 => /Users/tonybai/go/src/github.com/etcd-io/etcd/server
```


然后我们再执行go mod tidy，这回依赖分析与下载顺利完成了并且通过go build命令我们可以成功构建raftexample了。此时，raftexample的go.mod变成了这个样子：

```
module github.com/bigwhite/raftexample
go 1.17
replace go.etcd.io/etcd/server/v3 v3.5.1 => /Users/tonybai/go/src/github.com/etcd-io/etcd/server
require (
go.etcd.io/etcd/client/pkg/v3 v3.5.1
go.etcd.io/etcd/raft/v3 v3.5.1
go.etcd.io/etcd/server/v3 v3.5.1
go.uber.org/zap v1.19.1
)
require (
github.com/beorn7/perks v1.0.1 // indirect
github.com/cespare/xxhash/v2 v2.1.1 // indirect
github.com/coreos/go-semver v0.3.0 // indirect
github.com/dustin/go-humanize v1.0.0 // indirect
github.com/gogo/protobuf v1.3.2 // indirect
github.com/golang/protobuf v1.5.2 // indirect
github.com/matttproud/golang_protobuf_extensions v1.0.1 // indirect
github.com/prometheus/client_golang v1.11.0 // indirect
github.com/prometheus/client_model v0.2.0 // indirect
github.com/prometheus/common v0.26.0 // indirect
github.com/prometheus/procfs v0.6.0 // indirect
github.com/xiang90/probing v0.0.0-20190116061207-43a291ad63a2 // indirect
go.etcd.io/etcd/api/v3 v3.5.0 // indirect
go.etcd.io/etcd/pkg/v3 v3.5.0 // indirect
go.uber.org/atomic v1.7.0 // indirect
go.uber.org/multierr v1.7.0 // indirect
golang.org/x/sys v0.0.0-20210603081109-ebe580a85c40 // indirect
golang.org/x/time v0.0.0-20210220033141-f8bda1e9f3ba // indirect
google.golang.org/protobuf v1.26.0 // indirect
)
```


**但问题来了**！require指示符将go.etcd.io/etcd/server/v3 v3.5.1替换为一个本地路径etcd源码拷贝下的server module，这个**本地路径**是因开发者环境而异的，但go.mod文件通常是上传到代码服务器上，这就意味着另外一个开发人员下载了这份代码后极大可能是无法成功编译的，他要想完成raftexample的编译，就得将replace后面的本地路径改为适配自己环境下的路径。于是乎每当开发人员pull代码后，第一件事就是要修改go.mod中的replace，每次上传代码前，可能也要将replace路径复原，这是一个很糟心的事情，但在Go 1.18版本之前似乎只能这样做。

#### 2. 依赖本地尚未发布的module更糟糕

别急着学习Go工作区模式！我们再来看另外一个当前go module机制的问题。这个问题同样也是一位学员在我的[《Go语言第一课》](http://gk.link/a/10AVZ)中咨询过的一个问题，我在[《Go语言第一课FAQ》](https://tonybai.com/go-course-faq)中曾对这个问题做个解答。在这里我再详细举例说明一下。

假设我有一个名为hello-module的项目，它的结构和代码都很简单：

```
// https://github.com/bigwhite/experiments/tree/master/go1.18-examples/foresight/workspace/local-module/hello-module
$cat go.mod
module github.com/bigwhite/hello-module
go 1.17
$cat main.go
package main
import "github.com/bigwhite/a"
func main() {
a.A()
}
```


我们看到：hello-module对外唯一的依赖是module path为github.com/bigwhite/a的module，但后者是一个尚在本地进行开发，还未发布到github.com上的module。如果此时执行go mod tidy，我们将得到下面错误提示：

```
$go mod tidy
go: finding module for package github.com/bigwhite/a
github.com/bigwhite/hello-module imports
github.com/bigwhite/a: cannot find module providing package github.com/bigwhite/a: module github.com/bigwhite/a: reading https://goproxy.io/github.com/bigwhite/a/@v/list: 404 Not Found
server response:
not found: github.com/bigwhite/a@latest: terminal prompts disabled
Confirm the import path was entered correctly.
If this is a private repository, see https://golang.org/doc/faq#git_https for additional information.
```


go命令无法找到github.com/bigwhite/a这个module。怎么办呢？我们目前的一个“土办法”就是**自己“伪造”一个require，然后用replace将伪造的require指向本地的module a的目录**。

下面是伪造的go.mod文件的内容：

```
// https://github.com/bigwhite/experiments/tree/master/go1.18-examples/foresight/workspace/local-module/hello-module
module github.com/bigwhite/hello-module
go 1.17
require github.com/bigwhite/a v1.0.0
replace github.com/bigwhite/a v1.0.0 => /Users/tonybai/go/src/github.com/bigwhite/experiments/go1.18-examples/foresight/workspace/local-module/module-a
```


通过go.mod内容可以看到，我们伪造了hello-module对github.com/bigwhite/a的v1.0.0版本的依赖，并用replace指示符将该版本指向本地的module-a的开发目录。

虽然“伪造”go.mod文件内容可以解决这个场景中的问题，但显然这种方法给开发者的体验也很差，这样的hello-module的go.mod文件一旦提交到代码仓库，同样会给其他开发者带去心智负担。

目前的Go module机制在解决上述两个场景时力不从心，显然缺少最后的那块拼图。而Go 1.18中将引入的Go工作区模式就是go module的最后那块拼图。下面我们就来简要看看Go工作区模式。

### 二. Go工作区模式

Go工作区模式是Go开发者Michael Matloob在2021年4月提出的一个[名为“Multi-Module Workspaces in cmd/go”的proposal](https://github.com/golang/proposal/blob/master/design/45713-workspace.md)。这个proposal引入一个go.work文件用于开启Go工作区模式。go.work通过directory指示符设置一些本地路径，这些路径下的go module构成一个工作区(workspace)，**Go命令可以操作这些路径下的go module，也会优先使用工作区中的go module**。

我们先用go工作区模式解决一下前面提到的第一个问题。

在go 1.18版本发布之前，你需要使用gotip才能体验go工作区模式，安装gotip的方法如下：

```
$go install golang.org/dl/gotip@latest // go 1.17版本及以后使用go install。go 1.16及之前的版本用go get
$gotip download
$gotip version
go version devel go1.18-b7529c3 Tue Nov 9 06:27:04 2021 +0000 darwin/amd64
```


现在我们进入raftexample下面，然后通过下面命令初始化一个go.work:

```
$gotip work init .
$cat go.work
go 1.18
directory ./.
```


我们看到gotip work init命令创建了一个go.work文件，init后的路径被放在了go.work的directory指示符代码块中，directory指示符中的这些路径共同构成了一个Go工作区。我们将当前目录放入directory中，当前目录下的module就被置于我们的工作区当中了。

go.work还支持replace指示符，我们将前面放置在go.mod中的replace挪到go.work中：

```
// https://github.com/bigwhite/experiments/tree/master/go1.18-examples/foresight/workspace/raftexample-with-go-workspace/go.work
go 1.18
directory ./.
replace go.etcd.io/etcd/server/v3 v3.5.1 => /Users/tonybai/go/src/github.com/etcd-io/etcd/server
```


然后我们再执行构建：

```
$gotip build
```


这回顺利通过了构建。将replace挪到go.work后，go.mod文件就可以放心地提交到远程代码仓库了，其他开发人员下载后也无需修改go.mod，因为他们也有自己的Go工作区模式go.work文件。

go.work配置的是开发者的本地工作区，因此是不建议提交到远程代码仓库中的，我们可以通过.gitignore将其忽略掉。我们甚至可以在任何go module的项目目录之外下放置go.work文件。

除了用replace，我们还可以将本地的etcd项目拷贝也纳入到我们的工作区当中，这样就无需replace了，比如我们可以将上面的go.work改为如下这样：

```
// https://github.com/bigwhite/experiments/tree/master/go1.18-examples/foresight/workspace/raftexample-with-go-workspace/go.work
$cat go.work
go 1.18
directory (
./.
/Users/tonybai/go/src/github.com/etcd-io/etcd
)
```


这样raftexample同样可以成功编译。

同样我们也可以通过这种方法解决我们在引子中提到的第二个问题。

和上面例子一样，我们为hello-module这个项目添加一个go.work：

```
// https://github.com/bigwhite/experiments/tree/master/go1.18-examples/foresight/workspace/local-module/hello-module
$gotip work init ./ ../module-a
$cat go.work
go 1.18
directory (
./
../module-a
)
```


在这次init中，我们为init传入了两个路径，除了当前路径外，还将hello-module依赖的module-a在本地的路径传给了init，这样当前目录下的module与上层的module-a下的module就在同一个工作区当中了。接下来我们直接执行构建，go命令就可以在工作区顺利找到hello-module的依赖module-a了。

```
$gotip build
$./hello-module
this is a.A
```


### 三. 管理多module的工作区

最初这个proposal的名字就是multi modules workspace，即多module的工作区管理。当你的本地有很多module，且这些module存在相互依赖，那么我们可以在这些module的外面建立一个Go工作区，基于这个Go工作区开发与调试这些module就变得十分方便。

比如我们有三个module：a、b和c，其中a与b都依赖c。我们可以在a、b、c三个module路径的上一层创建一个Go工作区：

```
// https://github.com/bigwhite/experiments/tree/master/go1.18-examples/foresight/workspace/multi-modules
$go work init a b c
$cat go.work
go 1.18
directory (
./a
./b
./c
)
```


这之后，三个module:a、b和c就都在刚刚创建的这个go工作空间了，我们基于该工作空间便可以构建a与b，以构建a为例：

```
// https://github.com/bigwhite/experiments/tree/master/go1.18-examples/foresight/workspace/multi-modules
$gotip build -o a_bin github.com/bigwhite/a
$./a_bin
C in c
```


### 四. 小结

Go 1.18尚未发布，Go工作区还在active开发中，很多机制可能在后续的几个月还会发生变化。上面的内容仅仅是对Go工作空间做一个前瞻性的介绍，Go 1.18正式发布后，Go工作空间的机制和使用可能与目前有一定差别。

另外，go mod tidy目前并不care Go工作区，这块在原proposal有提到，大家注意！

go workspace特性的作者在油管曾发过一个[go工作空间的demo视频](https://www.youtube.com/watch?v=wQglU5aB5NQ&feature=youtu.be)：https://www.youtube.com/watch?v=wQglU5aB5NQ&feature=youtu.be，demo是基于最初的go工作区实现做的，大家也可以去看看。

本文所涉及的源码在[这里](https://github.com/bigwhite/experiments/tree/master/go1.18-examples)下载：https://github.com/bigwhite/experiments/tree/master/go1.18-examples。

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

简单地问题复杂化了，愣是没有看懂

那就再看一遍:)

弄得go mod tidy 好麻烦

只是排版有点杂乱。

TonyBai 的github 例子倒是非常清晰的。你下载代码实践一下就明白了。

就是把go replace 映射从go.mod 拆分到go.work，独立出来了而已。

gogo.work 属于本地配置，不应该混入到go.mod这种源码里面。

我的意思用了work时 如果用go mod tidy会报错

> 我的意思用了work时 如果用go mod tidy会报错

+1

2 年多了 issue 都叠了这么多楼了 还一直没修