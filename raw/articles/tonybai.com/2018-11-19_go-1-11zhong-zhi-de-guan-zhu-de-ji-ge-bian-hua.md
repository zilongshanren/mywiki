---
title: Go 1.11中值得关注的几个变化
url: https://tonybai.com/2018/11/19/some-changes-in-go-1-11/
published: '2018-11-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.11中值得关注的几个变化

转眼间又近年底，距8月25日[Go 1.11版本](https://github.com/golang/go/releases/tag/go1.11)正式发布已过去快三个月了。由于种种原因，[Go语言发布变化系列](https://tonybai.com/tag/golang)的Go 1.11版本没能及时放出。近期[网课发布上线](https://tonybai.com/2018/10/17/imooc-course-kubernetes-practice-go-online/)后，个人时间压力稍缓和。又恰看到近期[Go 1.12 release note的initial version已经加入到master](https://github.com/golang/go/commit/02aa1aeeb1baf9bcfb8b9eeff9c92e93426ae512)，于是这篇文章便上升到个人Todo list的Top3的位置，我也尽一切可能的碎片时间收集素材，撰写文章内容。这个时候谈Go 1.11，总有炒“冷饭”的嫌疑，虽然这碗饭还有一定温度^_^。

## 一. Go 1.11版本的重要意义

在Go 1.11版本之前的[Go user官方调查](https://blog.golang.org/survey2017-results)中，Gopher抱怨最多的三大问题如下：

- 包依赖管理
- 缺少泛型
- 错误处理

而Go 1.11开启了问题1：**包依赖管理**解决的实验。这表明了社区的声音在影响Go语言演化的过程中扮演着日益重要的角色了。

同时，[Go 1.11](https://github.com/golang/go/releases/tag/go1.11)是[Russ Cox](https://research.swtch.com/)在[GopherCon](https://www.gophercon.com/) 2017大会上发表 [“Toward Go2″](https://blog.golang.org/toward-go2)之后的第一个Go版本，是为后续[“Go2”](https://github.com/golang/go/wiki/Go2)的渐进落地奠定基础的一个版本。

## 二. Go 1.11版本变化概述

在”Go2″声音日渐响亮的今天，兼容性(compatibility)也依旧是Go team考虑的Go语言演化的第一原则，这一点通过Rob Pike在9月份的[Go Sydney Meetup](https://www.meetup.com/golang-syd/)上的有关[Go 2 Draft Specifications](https://blog.golang.org/go2draft)的[Talk](https://www.youtube.com/watch?v=RIvL2ONhFBI)可以证明(油管视频)。

![img{512x368}](../../assets/9d5d20b36784bc86.png)


兼容性依然是”Go2″的第一考虑

Go 1.11也一如既往版本那样，继续遵守着[Go1兼容协议](https://golang.org/doc/go1compat.html)，这意味使用从Go1.0到[Go1.10](https://tonybai.com/2018/02/17/some-changes-in-go-1-10/)编写的代码理论上依旧可以通过Go 1.11版本编译并正常运行。

随着Go 1.11版本的发布，一些老版本的操作系统将不再被支持，比如Windows XP、macOS 10.9.x等。不被支持不意味着完全不能用，只是Go 1.11在这些老旧os上运行时出现问题将不被官方support了。同时根据Go的[release support规定](https://golang.org/doc/devel/release.html)，Go 1.11发布也同时意味着Go 1.9版本将和之前的older go release版本一样，官方将不再提供支持了(关键bug fix、security problem fix等)。

Go 1.11中为近两年逐渐兴起的[RISC-V](https://en.wikipedia.org/wiki/RISC-V)cpu架构预留了GOARCH值：riscv和riscv64。

Go 1.11中为调试器增加了一个新的实验功能，那就是允许在调试过程中动态调用Go函数，比如在断点处调用String方法等。[Delve](https://github.com/derekparker/delve) 1.1.0及以上版本可以使用该功能。

在运行时方面，Go 1.11使用了一个稀疏heap布局，这样就去掉了以往Go heap最大512G的限制。

通过Go 1.11编译的Go程序一般来说性能都会有小幅的提升。对于使用math/big包的程序或arm64架构上的Go程序而言，这次的提升尤为明显。

Go 1.11中最大的变化莫过于两点：

- module机制的实验性引入，以试图解决长久以来困扰Gopher们的包依赖问题；
- 增加对
[WebAssembly](https://webassembly.org/)的支持，这样以后Gopher们可以通过Go语言编写前端应用了。

Go 1.11的change很多，这是core team和社区共同努力的结果。但在我这个系列文章中，我们只能详细关注少数重要的变化。下面我们就来稍微详细地说说go module和go support WebAssembly这两个显著的变化。

## 三. go module

在Go 1.11 beta2版本发布之前，我曾经基于当时的Go tip版本撰写了一篇 [《初窥go module》](https://tonybai.com/2018/07/15/hello-go-module/)的文章，重点描述了go module的实现机制，包括[Semantic Import Versioning](https://research.swtch.com/vgo-import)、[Minimal Version Selection](https://research.swtch.com/vgo-mvs)等，因此对go module（前身为[vgo](https://github.com/golang/vgo))是什么以及实现机制感兴趣的小伙伴儿们可以先移步到那篇文章了解。在这里我将通过为一个[已存在的repo](https://github.com/bigwhite/gocmpp)添加go.mod的方式来描述go module。

这里我们使用的是[go 1.11.2版本](https://github.com/golang/go/releases/tag/go1.11.2)，repo为[gocmpp](https://github.com/bigwhite/gocmpp)。注意：我们没有显式设置GO111MODULE的值，这样只有在GOPATH之外的路径下，且当前路径下有go.mod或子路径下有go.mod文件时，go compiler才进入module-aware模式(相比较于gopath模式)。

### 1. 初始化go.mod

我们先把gocmpp clone到gopath之外的一个路径下：

```
# git clone https://github.com/bigwhite/gocmpp.git
Cloning into 'gocmpp'...
remote: Enumerating objects: 1, done.
remote: Counting objects: 100% (1/1), done.
remote: Total 950 (delta 0), reused 0 (delta 0), pack-reused 949
Receiving objects: 100% (950/950), 3.85 MiB | 0 bytes/s, done.
Resolving deltas: 100% (396/396), done.
Checking connectivity... done.
```


在应用go module之前，我们先来在传统的gopath模式下build一次：

```
# go build
connect.go:24:2: cannot find package "github.com/bigwhite/gocmpp/utils" in any of:
/root/.bin/go1.11.2/src/github.com/bigwhite/gocmpp/utils (from $GOROOT)
/root/go/src/github.com/bigwhite/gocmpp/utils (from $GOPATH)
```


正如我们所料，由于处于GOPATH外面，且GO111MODULE并未显式设置，Go compiler会尝试在当前目录或子目录下查找go.mod，如果没有go.mod文件，则会采用传统gopath模式编译，即在$GOPATH/src下面找相关的import package，因此失败。

下面我们通过建立go.mod，将编译mode切换为module-aware mode。

我们通过go mod init命令来为gocmpp创建go.mod文件：

```
# go mod init github.com/bigwhite/gocmpp
go: creating new go.mod: module github.com/bigwhite/gocmpp
# cat go.mod
module github.com/bigwhite/gocmpp
```


我们看到，go mod init命令在当前目录下创建一个go.mod文件，内有一行内容，描述了该module为 github.com/bigwhite/gocmpp。

我们再来构建一下gocmpp：

```
# go build
go: finding golang.org/x/text/transform latest
go: finding golang.org/x/text/encoding/unicode latest
go: finding golang.org/x/text/encoding/simplifiedchinese latest
go: finding golang.org/x/text v0.3.0
go: finding golang.org/x/text/encoding latest
go: downloading golang.org/x/text v0.3.0
```


由于当前目录下有了go.mod文件，go compiler将工作在module-aware模式下，自动分析gocmpp的依赖、确定gocmpp依赖包的初始版本，并下载这些版本的依赖包缓存到特定目录下（目前是存放在$GOPATH/pkg/mod下面）

```
# cat go.mod
module github.com/bigwhite/gocmpp
require golang.org/x/text v0.3.0
```


我们看到go.mod中多了一行信息：**“require golang.org/x/text v0.3.0″**。这就是gocmpp这个module所依赖的第三方包以及经过go compiler初始分析确定使用的版本(v0.3.0)。

### 2. 用于verify的go.sum

go build后，当前目录下还多出了一个go.sum文件。

```
# cat go.sum
golang.org/x/text v0.3.0 h1:g61tztE5qeGQ89tm6NTjjM9VPIm088od1l6aSorWRWg=
golang.org/x/text v0.3.0/go.mod h1:NqM8EUOU14njkJ3fqMW+pc6Ldnwhi/IjpwHt7yyuwOQ=
```


go.sum记录每个依赖库的版本和对应的内容的校验和(一个哈希值)。每当增加一个依赖项时，如果go.sum中没有，则会将该依赖项的版本和内容校验和添加到go.sum中。go命令会使用这些校验和与缓存在本地的依赖包副本元信息(比如：$GOPATH/pkg/mod/cache/download/golang.org/x/text/@v下面的v0.3.0.ziphash)进行比对校验。

如果我修改了$GOPATH/pkg/mod/cache/download/golang.org/x/text/@v/v0.3.0.ziphash中的值，那么当我执行下面verify命令时会报错：

```
# go mod verify
golang.org/x/text v0.3.0: zip has been modified (/root/go/pkg/mod/cache/download/golang.org/x/text/@v/v0.3.0.zip)
golang.org/x/text v0.3.0: dir has been modified (/root/go/pkg/mod/golang.org/x/text@v0.3.0)
```


如果没有“恶意”修改，则verify会报成功：

```
# go mod verify
all modules verified
```


### 3. 用why解释为何依赖，给出依赖路径

go.mod中的依赖项由go相关命令自动生成和维护。但是如果开发人员想知道为什么会依赖某个package，可以通过go mod why命令来查询原因。go mod why命令默认会给出一个main包到要查询的packge的最短依赖路径。如果go mod why使用 -m flag，则后面的参数将被看成是module，并给出main包到每个module中每个package的最短依赖路径（如果依赖的话）：

下面我们通过go mod why命令查看一下gocmpp module到 golang.org/x/oauth2和golang.org/x/exp两个包是否有依赖：

```
# go mod why golang.org/x/oauth2 golang.org/x/exp
go: finding golang.org/x/oauth2 latest
go: finding golang.org/x/exp latest
go: downloading golang.org/x/oauth2 v0.0.0-20181106182150-f42d05182288
go: downloading golang.org/x/exp v0.0.0-20181112044915-a3060d491354
go: finding golang.org/x/net/context/ctxhttp latest
go: finding golang.org/x/net/context latest
go: finding golang.org/x/net latest
go: downloading golang.org/x/net v0.0.0-20181114220301-adae6a3d119a
# golang.org/x/oauth2
(main module does not need package golang.org/x/oauth2)
# golang.org/x/exp
(main module does not need package golang.org/x/exp)
```


通过结尾几行的输出日志，我们看到gocmpp的main package没有对golang.org/x/oauth2和golang.org/x/exp两个包产生任何依赖。

我们加上-m flag再来执行一遍：

```
# go mod why -m golang.org/x/oauth2 golang.org/x/exp
# golang.org/x/oauth2
(main module does not need module golang.org/x/oauth2)
# golang.org/x/exp
(main module does not need module golang.org/x/exp)
```


同样是没有依赖的输出结果，但是输出日志中使用的是module，而不是package字样。说明go mod why将golang.org/x/oauth2和golang.org/x/exp视为module了。

我们再来查询一下对golang.org/x/text的依赖：

```
# go mod why golang.org/x/text
# golang.org/x/text
(main module does not need package golang.org/x/text)
# go mod why -m golang.org/x/text
# golang.org/x/text
github.com/bigwhite/gocmpp/utils
golang.org/x/text/encoding/simplifiedchinese
```


我们看到，如果-m flag不开启，那么gocmpp main package没有对golang.org/x/text的依赖路径；如果-m flag开启，则golang.org/x/text被视为module，go mod why会检查gocmpp main package到module: golang.org/x/text下面所有package是否有依赖路径。这里我们看到gocmpp main package依赖了golang.org/x/text module下面的golang.org/x/text/encoding/simplifiedchinese这个package，并给出了最短依赖路径。

### 4. 清理go.mod和go.sum中的条目：go mod tidy

经过上述操作后，我们再来看看go.mod中的内容：

```
# cat go.mod
module github.com/bigwhite/gocmpp
require (
github.com/dvyukov/go-fuzz v0.0.0-20181106053552-383a81f6d048
golang.org/x/net v0.0.0-20181114220301-adae6a3d119a // indirect
golang.org/x/oauth2 v0.0.0-20181106182150-f42d05182288 // indirect
golang.org/x/text v0.3.0
)
```


我们发现go.mod中require block增加了许多条目，显然我们的gocmpp并没有依赖到golang.org/x/oauth2和golang.org/x/net中的任何package。我们要清理一下go.mod，使其与gocmpp源码中的第三方依赖的真实情况保持一致，我们使用go mod tidy命令：

```
# go mod tidy
# cat go.mod
module github.com/bigwhite/gocmpp
require (
github.com/dvyukov/go-fuzz v0.0.0-20181106053552-383a81f6d048
golang.org/x/text v0.3.0
)
# cat go.sum
github.com/dvyukov/go-fuzz v0.0.0-20181106053552-383a81f6d048 h1:3O5zXlWvrRdioniMPz8pW+pGi+BNEFRtVhvj0GnknbQ=
github.com/dvyukov/go-fuzz v0.0.0-20181106053552-383a81f6d048/go.mod h1:11Gm+ccJnvAhCNLlf5+cS9KjtbaD5I5zaZpFMsTHWTw=
golang.org/x/text v0.3.0 h1:g61tztE5qeGQ89tm6NTjjM9VPIm088od1l6aSorWRWg=
golang.org/x/text v0.3.0/go.mod h1:NqM8EUOU14njkJ3fqMW+pc6Ldnwhi/IjpwHt7yyuwOQ=
```


我们看到：执行完tidy命令后，go.mod和go.sum都变得简洁了，里面的每一个条目都是gocmpp所真实依赖的package/module的信息。

### 5. 对依赖包的版本进行“升降级”(upgrade或downgrade)

如果对go mod init初始选择的依赖包版本不甚满意，或是第三方依赖包有更新的版本发布，我们日常开发工作中都会进行对对依赖包的版本进行“升降级”(upgrade或downgrade)的操作。在go module模式下，如何来做呢？由于go.mod和go.sum是由go compiler管理的，这里不建议手工去修改go.mod中require中module的版本号。我们可以通过[module-aware的go get命令](https://golang.org/cmd/go/#hdr-Modules__module_versions__and_more)来实现我们的目的。

我们先来查看一下golang.org/x/text都有哪些版本可用：

```
# go list -m -versions golang.org/x/text
golang.org/x/text v0.1.0 v0.2.0 v0.3.0
```


我们选择将golang.org/x/text从v0.3.0降级到v0.1.0：

```
# go get golang.org/x/text@v0.1.0
go: finding golang.org/x/text v0.1.0
go: downloading golang.org/x/text v0.1.0
```


降级后，我们test一下：

```
# go test
PASS
ok github.com/bigwhite/gocmpp 0.003s
```


我们这时再看看go.mod和go.sum：

```
# cat go.mod
module github.com/bigwhite/gocmpp
require (
github.com/dvyukov/go-fuzz v0.0.0-20181106053552-383a81f6d048
golang.org/x/text v0.1.0
)
# cat go.sum
github.com/dvyukov/go-fuzz v0.0.0-20181106053552-383a81f6d048 h1:3O5zXlWvrRdioniMPz8pW+pGi+BNEFRtVhvj0GnknbQ=
github.com/dvyukov/go-fuzz v0.0.0-20181106053552-383a81f6d048/go.mod h1:11Gm+ccJnvAhCNLlf5+cS9KjtbaD5I5zaZpFMsTHWTw=
golang.org/x/text v0.1.0 h1:LEnmSFmpuy9xPmlp2JeGQQOYbPv3TkQbuGJU3A0HegU=
golang.org/x/text v0.1.0/go.mod h1:NqM8EUOU14njkJ3fqMW+pc6Ldnwhi/IjpwHt7yyuwOQ=
golang.org/x/text v0.3.0 h1:g61tztE5qeGQ89tm6NTjjM9VPIm088od1l6aSorWRWg=
golang.org/x/text v0.3.0/go.mod h1:NqM8EUOU14njkJ3fqMW+pc6Ldnwhi/IjpwHt7yyuwOQ=
```


go.mod中依赖的golang.org/x/text已经从v0.3.0自动变成了v0.1.0了。go.sum中也增加了golang.org/x/text v0.1.0的条目，不过v0.3.0的条目依旧存在。我们可以通过go mod tidy清理一下：

```
# go mod tidy
# cat go.sum
github.com/dvyukov/go-fuzz v0.0.0-20181106053552-383a81f6d048 h1:3O5zXlWvrRdioniMPz8pW+pGi+BNEFRtVhvj0GnknbQ=
github.com/dvyukov/go-fuzz v0.0.0-20181106053552-383a81f6d048/go.mod h1:11Gm+ccJnvAhCNLlf5+cS9KjtbaD5I5zaZpFMsTHWTw=
golang.org/x/text v0.1.0 h1:LEnmSFmpuy9xPmlp2JeGQQOYbPv3TkQbuGJU3A0HegU=
golang.org/x/text v0.1.0/go.mod h1:NqM8EUOU14njkJ3fqMW+pc6Ldnwhi/IjpwHt7yyuwOQ=
```


go 1.11中的go get也是支持两套工作模式的: 一套是传统gopath mode的；一套是module-aware的。

如果我们在gopath之外的路径，且该路径下没有go.mod，那么go get还是回归gopath mode:

```
# go get golang.org/x/text@v0.1.0
go: cannot use path@version syntax in GOPATH mode
```


而module-aware的go get在前面已经演示过了，这里就不重复演示了。

在module-aware模式下，go get -u会更新依赖，升级到依赖的最新minor或patch release。比如：我们在gocmpp module root path下执行：

```
# go get -u golang.org/x/text
# cat go.mod
module github.com/bigwhite/gocmpp
require (
github.com/dvyukov/go-fuzz v0.0.0-20181106053552-383a81f6d048
golang.org/x/text v0.3.0 //恢复到0.3.0
)
```


我们看到刚刚降级回v0.1.0的依赖项又自动变回v0.3.0了（注意仅minor号变更）。

如果仅仅要升级patch号，而不升级minor号，可以使用go get -u=patch A 。比如：如果golang.org/x/text有v0.1.1版本，那么go get -u=patch golang.org/x/text会将go.mod中的text后面的版本号变为v0.1.1，而不是v0.3.0。

如果go get后面不接具体package，则go get仅针对于main package。

处于module-aware工作模式下的go get更新某个依赖(无论是升版本还是降版本)时，会自动计算并更新其间接依赖的包的版本。

### 6. 兼容go 1.11之前版本的reproduceable build: 使用vendor

处于module-aware mode下的go compiler是完全不理会vendor目录的存在的，go compiler只会使用$GOPATH/pkg/mod下(当前go mod缓存的包是放在这个位置，也许将来会更换位置)缓存的第三方包的特定版本进行编译构建。那么这样一来，对于采用go 1.11之前版本的go compiler来说，reproduceable build就失效了。

为此，go mod提供了vendor子命令，可以根据依赖在module顶层目录自动生成vendor目录：

```
# go mod vendor -v
# github.com/dvyukov/go-fuzz v0.0.0-20181106053552-383a81f6d048
github.com/dvyukov/go-fuzz/gen
# golang.org/x/text v0.3.0
golang.org/x/text/encoding/simplifiedchinese
golang.org/x/text/encoding/unicode
golang.org/x/text/transform
golang.org/x/text/encoding
golang.org/x/text/encoding/internal
golang.org/x/text/encoding/internal/identifier
golang.org/x/text/internal/utf8internal
golang.org/x/text/runes
```


gopher可以将vendor目录提交到git repo，这样老版本的go compiler就可以使用vendor进行reproduceable build了。

当然在module-aware mode下，go 1.11 compiler也可以使用vendor进行构建，使用下面命令即可：

```
go build -mod=vendor
```


注意在上述命令中，只有位于module顶层路径的vendor才会起作用。

### 7. 国内gopher如何适应go module

对于国内gopher来说，下载go get package的经历并不是总是那么愉快！尤其是get golang.org/x/xxx路径下的package的时候。以golang.org/x/text为例，在传统的gopath mode下，我们还可以通过下载github.com/golang/text，然后在本地将路径改为golang.org/x/text的方式来获取text相关包。但是在module-aware mode下，对package的下载和本地缓存管理完全由go tool自动完成，国内的gopher们该如何应对呢？

两种方法：

1. 用go.mod中的replace语法，将golang.org/x/text指向本地另外一个目录下已经下载好的github.com/golang/text

2. 使用GOPROXY

方法1显然具有临时性，本地改改第三方依赖库代码，用于调试还可以；第二种方法显然是正解，我们通过一个proxy来下载那些在qiang外的package。Microsoft工程师开源的[athens项目](https://github.com/gomods/athens)正是一个用于这个用途的go proxy工具。不过限于篇幅，这里就不展开说明了。我将在后续文章详细谈谈 go proxy的，尤其是使用athens实现go proxy的详细方案。

## 四. 对WebAssembly的支持

### 1. 简介

由于长期在**后端**浸淫，对javascript、[WebAssembly](https://webassembly.org/)等前端的技能了解不多，因此这里对Go支持WebAssembly也就能介绍个梗概。下图是对Go支持WebAssembly的一个粗浅的理解：

![img{512x368}](../../assets/69ae91fe75573bb9.png)


我们看到满足WebAssembly标准要求的wasm运行于browser之上，类比于一个amd64架构的binary program运行于linux操作系统之上。我们在x86-64的linux上执行go build，实质执行的是:

```
GOOS=linux GOARCH=amd64 go build ...
```


因此为了将Go源码编译为wasm，我们需要执行：

```
GOOS=js GOARCH=wasm go build ...
```


同时， *_js.go和 *_wasm.go这样的文件也和*_linux.go、*_amd64.go一样，会被go compiler做特殊处理。

### 2. 一个hello world级别的WebAssembly的例子

例子来自[Go官方Wiki](https://github.com/golang/go/wiki/WebAssembly)，代码结构如下：

```
/Users/tony/test/Go/wasm/hellowasm git:(master) ✗ $tree
.
├── hellowasm.go
├── index.html
└── server.go
```


hellowasm.go是最终wasm应用对应的源码：

```
// hellowasm.go
package main
import "fmt"
func main() {
fmt.Println("Hello, WebAssembly!")
}
```


我们先将其编译为wasm文件main.wasm：

```
$GOOS=js GOARCH=wasm go build -o main.wasm hellowasm.go
$ls -F
hellowasm.go index.html main.wasm* server.go
```


接下来我们从Goroot下面copy一个javascript支持文件wasm_exec.js：

```
cp "$(go env GOROOT)/misc/wasm/wasm_exec.js" .
```


我们建立index.html，并在该文件中使用wasm_exec.js，并加载main.wasm：

```
//index.html
<html>
<head>
<meta charset="utf-8">
<script src="wasm_exec.js"></script>
<script>
const go = new Go();
WebAssembly.instantiateStreaming(fetch("main.wasm"), go.importObject).then((result) => {
go.run(result.instance);
});
</script>
</head>
<body></body>
</html>
```


最后，我们建立server.go，这是一个File server：

```
//server.go
package main
import (
"flag"
"log"
"net/http"
)
var (
listen = flag.String("listen", ":8080", "listen address")
dir = flag.String("dir", ".", "directory to serve")
)
func main() {
flag.Parse()
log.Printf("listening on %q...", *listen)
err := http.ListenAndServe(*listen, http.FileServer(http.Dir(*dir)))
log.Fatalln(err)
}
```


启动该server:

```
$go run server.go
2018/11/19 21:19:17 listening on ":8080"...
```


打开Chrome浏览器，右键打开Chrome的“检查”页面，访问127.0.0.1:8080，我们将在console（控制台）窗口看到下面内容：

![img{512x368}](../../assets/40fc8c6b908aead6.png)


我们看到”Hello, WebAssembly”字样输出到console上了！

### 3. 使用node.js执行wasm应用

wasm应用除了可以运行于支持WebAssembly的浏览器上之外，还可以通过node.js运行它。

我的实验环境中安装的node版本是:

```
$node -v
v9.11.1
```


我们删除server.go，然后执行下面命令：

```
$GOOS=js GOARCH=wasm go run -exec="$(go env GOROOT)/misc/wasm/go_js_wasm_exec" .
Hello, WebAssembly!
```


我们看到通过go_js_wasm_exec命令我们成功通过node执行了main.wasm。

不过每次通过go run -exec来执行，命令行太长，不易记住和使用。我们将go_js_wasm_exec放到$PATH下面，然后直接执行go run：

```
$export PATH=$PATH:"$(go env GOROOT)/misc/wasm"
$which go_js_wasm_exec
/Users/tony/.bin/go1.11.2/misc/wasm/go_js_wasm_exec
$GOOS=js GOARCH=wasm go run .
Hello, WebAssembly!
```


main.wasm同样被node执行，并且这样执行main.wasm程序的命令行长度大大缩短了！

## 五. 小结

从Go 1.11版本开始，Go语言开始驶入“语言演化”的深水区。Go语言究竟该如何演化？如何在保持语言兼容性、社区不分裂的前提下，满足社区对于错误处理、泛型等语法特性的需求，是摆在Go设计者面前的一道难题。但我相信，无论Go如何演化，Go设计者都会始终遵循Go语言安身立命的那几个根本原则，也是大多数Gopher喜欢Go的根本原因：兼容、简单、可读和高效。

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

## 评论