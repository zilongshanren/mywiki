---
title: 小心go.mod中的go directive
url: https://tonybai.com/2020/03/09/take-care-of-the-go-directive-in-go-dot-mod/
published: '2020-03-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 小心go.mod中的go directive

在撰写《[Go 1.14中值得关注的几个变化](https://tonybai.com/2020/03/08/some-changes-in-go-1-14/)》这篇文章时，我使用的试验环境为我的2019款 MacPro，OS版本：10.14.6。我通过下载 `https://dl.google.com/go/go1.14.darwin-amd64.tar.gz`

并解压的方式安装的Go 1.14版本。在我的工作环境中，我通常通过变更`GOROOT`

的方式来使用不同的Go版本。但在进行Go 1.14新增的overlapping interface的实验时，我遇到了一个问题。本文记录的就是这个问题的发现和解决过程，以备自己备忘，也希望能给广大Gopher带来启发。

## 1. 问题现象

在我进行overlapping interface试验时，我使用go 1.14编译器编译下面的代码：

```
// https://github.com/bigwhite/experiments/blob/master/go1.14-examples/overlapping_interface.go
package foo
type I interface {
f()
String() string
}
type J interface {
g()
String() string
}
type IJ interface {
I
J
}
```


但出乎意料的是我得到了如下的结果：

```
$go build overlapping_interface.go
# command-line-arguments
./overlapping_interface.go:14:2: duplicate method String
```


我一脸懵逼啊！我靠！[Go 1.14](https://tip.golang.org/doc/go1.14)的新增的[overlapping interface机制](https://github.com/golang/proposal/blob/master/design/6977-overlapping-interfaces.md)居然不好用！之后我的第一反应就是检查是不是我的当前窗口中GOROOT设置有误，结果：GOROOT设置完全没错！

于是我又切换到一个Ubuntu 18.04环境下，同样用Go 1.14版本(for linux)编译上述代码，这回编译很顺利，没有报出像MacOS那样的错误。

接下来进入胡思乱想状态:) 难道是Go team在打包go1.14.darwin-amd64.tar.gz是忘记了这个功能？…. …..

## 2. 问题分析过程

我首先到[go项目的issue列表](https://github.com/golang/go/issues/)查是否有人遇到与我相同的问题，居然没找到，基本肯定是我自己环境的问题了。于是提了[一个issue](https://github.com/golang/go/issues/37728)，看看有谁能帮忙分析一下原因。

不久，Go核心开发团队的[Keith Randall](https://github.com/randall77)提供了一些信息和诊断思路。首先他在他自己的Mac环境无法重现该问题，并也怀疑是不是我的安装方式和环境变量设置的问题。

于是，我尝试了更换一种Go 1.14的安装方式来重新安装Go 1.14 for MacOS:

```
$go get golang.org/dl/go1.14
go: finding golang.org/dl latest
go: downloading golang.org/dl v0.0.0-20200302224518-306f3096cb2f
go: extracting golang.org/dl v0.0.0-20200302224518-306f3096cb2f
$go1.14 download
Downloaded 0.0% ( 14448 / 124931758 bytes) ...
Downloaded 0.3% ( 391280 / 124931758 bytes) ...
... ...
Downloaded 92.5% (115554516 / 124931758 bytes) ...
Downloaded 100.0% (124931758 / 124931758 bytes)
Unpacking /Users/tonybai/sdk/go1.14/go1.14.darwin-amd64.tar.gz ...
Success. You may now run 'go1.14'
$go1.14 env
GO111MODULE="on"
GOARCH="amd64"
GOBIN=""
GOCACHE="/Users/tonybai/Library/Caches/go-build"
GOENV="/Users/tonybai/Library/Application Support/go/env"
GOEXE=""
GOFLAGS=""
GOHOSTARCH="amd64"
GOHOSTOS="darwin"
GOINSECURE=""
GONOPROXY=""
GONOSUMDB=""
GOOS="darwin"
GOPATH="/Users/tonybai/Go"
GOPRIVATE=""
GOPROXY="https://goproxy.cn,direct"
GOROOT="/Users/tonybai/sdk/go1.14"
GOSUMDB="off"
GOTMPDIR=""
GOTOOLDIR="/Users/tonybai/sdk/go1.14/pkg/tool/darwin_amd64"
GCCGO="gccgo"
AR="ar"
CC="clang"
CXX="clang++"
CGO_ENABLED="1"
GOMOD="/dev/null"
CGO_CFLAGS="-g -O2"
CGO_CPPFLAGS=""
CGO_CXXFLAGS="-g -O2"
CGO_FFLAGS="-g -O2"
CGO_LDFLAGS="-g -O2"
PKG_CONFIG="pkg-config"
GOGCCFLAGS="-fPIC -m64 -pthread -fno-caret-diagnostics -Qunused-arguments -fmessage-length=0 -fdebug-prefix-map=/var/folders/cz/sbj5kg2d3m3c6j650z0qfm800000gn/T/go-build236598550=/tmp/go-build -gno-record-gcc-switches -fno-common"
```


我使用renew后的go1.14再来编译最初那段包含了overlapping interface的代码：

```
➜ /Users/tonybai/Go/src/github.com/bigwhite/experiments/go1.14-examples git:(master) $go1.14 version
go version go1.14 darwin/amd64
➜ /Users/tonybai/Go/src/github.com/bigwhite/experiments/go1.14-examples git:(master) $go1.14 build overlapping_interface.go
# command-line-arguments
./overlapping_interface.go:14:2: duplicate method String
```


问题依旧！

为了给Keith Randall提供更多有用信息，我在build时传入`-x -v`

参数：

```
➜ /Users/tonybai/Go/src/github.com/bigwhite/experiments/go1.14-examples git:(master) $go1.14 build -x -v overlapping_interface.go
WORK=/var/folders/cz/sbj5kg2d3m3c6j650z0qfm800000gn/T/go-build369480074
command-line-arguments
mkdir -p $WORK/b001/
cat >$WORK/b001/importcfg << 'EOF' # internal
# import config
EOF
cd /Users/tonybai/Go/src/github.com/bigwhite/experiments/go1.14-examples
/Users/tonybai/sdk/go1.14/pkg/tool/darwin_amd64/compile -o $WORK/b001/_pkg_.a -trimpath "$WORK/b001=>" -p command-line-arguments -lang=go1.12 -complete -buildid 00YuEePKlhV_qKTnJcVK/00YuEePKlhV_qKTnJcVK -goversion go1.14 -D _/Users/tonybai/Go/src/github.com/bigwhite/experiments/go1.14-examples -importcfg $WORK/b001/importcfg -pack -c=4 ./overlapping_interface.go
# command-line-arguments
./overlapping_interface.go:14:2: duplicate method String
```


一段时间后，眼尖的Keith Randall发现了蛛丝马迹：`-lang=go 1.12`

。在我提供的上面build日志中，**“-lang=1.12″**被传给了Go 1.14 compiler，于是虽然贵为go 1.14版本编译器，但它也只能按照[go 1.12版本](https://tonybai.com/2019/03/02/some-changes-in-go-1-12/)的语法规范对我的代码进行检查和编译，这就是“罪魁祸首”，没跑了！

## 3. 问题解决

但是”-lang=1.12″怎么就凭空出现传给了Go 1.14编译器了呢？我查了所有编译器相关的环境变量，也没看到哪里设置了-lang=1.12。正当我处于迷茫状态时，突然`go.mod`

这个文件名浮现在我的脑海中：go.mod中除了module名、一堆require、replace语句之外，还有[go 1.12](https://tip.golang.org/doc/go1.12#modules)引入的`go`

指示信息(directive)! 顿悟！！！

上面所有的go build执行都是在我本地的`/Users/tonybai/go/src/github.com/bigwhite/experiments/go1.14-examples`

下执行的。而`github.com/bigwhite/experiments`

这个repo的顶层go.mod文件内容如下：

```
module github.com/bigwhite/experiments
go 1.12
```


在[Go 1.12的release note](https://tip.golang.org/doc/go1.12)中，我们看到这样一段说明：

```
The go directive in a go.mod file now indicates the version of the language used by the files within that module.
go.mod文件中的go指示器指示该当前module中文件使用的Go语言版本。
```


当前，我的go.mod中go指示器指示的版本为go 1.12，那么即便是使用Go 1.14版本编译器编译该module下的文件，使用的也是go 1.12的语法。

**解决方法**：[升级go.mod中的go指示器版本为go 1.14](https://github.com/bigwhite/experiments/commit/52de27c32e03e092e7f64a91bd7abd46708933f1)。升级后问题迎刃而解。

## 4. 小结

目前仅仅在使用比go.mod中go指示器版本低的go编译器对module下源文件进行编译，在报错的时候才会给出版本不匹配的提示。但是如果使用比go指示器版本高的编译器编译，即便出错，也没有警告提示。因此，在升级go版本时，**要小心维护go.mod中的go directive，使其与你使用的go compiler版本匹配**。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

直接手动改go mod文件吗 有没有啥命令更改go directive

有啊。go mod edit -go=1.14 go.mod 可以将go.mod中go version改为go 1.14

非常感谢