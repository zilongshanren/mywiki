---
title: 理解unsafe-assume-no-moving-gc包
url: https://tonybai.com/2023/04/16/understanding-unsafe-assume-no-moving-gc/
published: '2023-04-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 理解unsafe-assume-no-moving-gc包

![](../../assets/a6a192ad0b6e2dc7.png)


[本文永久链接](https://tonybai.com/2023/04/16/understanding-unsafe-assume-no-moving-gc) – https://tonybai.com/2023/04/16/understanding-unsafe-assume-no-moving-gc

## 1. 背景

在之前的[《Go与神经网络：张量计算》](https://t.zsxq.com/0dTyxkwRb)一文中，不知道大家是否发现了，所有例子代码执行时，前面都加了一个环境变量ASSUME_NO_MOVING_GC_UNSAFE_RISK_IT_WITH，就像下面这样：

```
$ASSUME_NO_MOVING_GC_UNSAFE_RISK_IT_WITH=go1.20 go run tensor.go
```


这是怎么回事儿呢？如果不加上这个环境变量会发生什么呢？我们来试试：

```
// https://github.com/bigwhite/experiments/blob/master/go-and-nn/tensor-operations/tensor.go
$go run tensor.go
panic: Something in this program imports go4.org/unsafe/assume-no-moving-gc to declare that it assumes a non-moving garbage collector, but your version of go4.org/unsafe/assume-no-moving-gc hasn't been updated to assert that it's safe against the go1.20 runtime. If you want to risk it, run with environment variable ASSUME_NO_MOVING_GC_UNSAFE_RISK_IT_WITH=go1.20 set. Notably, if go1.20 adds a moving garbage collector, this program is unsafe to use.
goroutine 1 [running]:
go4.org/unsafe/assume-no-moving-gc.init.0()
/Users/tonybai/Go/pkg/mod/go4.org/unsafe/assume-no-moving-gc@v0.0.0-20220617031537-928513b29760/untested.go:25 +0x1ba
exit status 2
```


我们看到，程序panic了！我们看到panic的错误信息提到了go4.org/unsafe/assume-no-moving-gc这个包，显然是这个包在“作祟”，那么assume-no-moving-gc这个包究竟是做什么的呢？究竟有何功用？为何gorgonia.org/tensor会依赖这个包？这超出了[《Go与神经网络：张量计算》]那篇文章的范畴，所以我并未提及。在这篇文章中，我就和大家一起来理解一下unsafe-assume-no-moving-gc这个包。

## 2. unsafe-assume-no-moving-gc究竟是什么包？

unsafe-assume-no-moving-gc这个包的canonical import path是go4.org/unsafe/assume-no-moving-gc，显然它是go4.org这个组织开源的包。我们看看go4.org的主页(如下图)：

![](../../assets/4434de561e2a5e38.png)


这个站点主页非常“简陋”，最大的价值在于解释了go4的来历：**gopher的谐音**。go4.org开源了一些Go包，这个在其官方github站点可以看到：

![](../../assets/7741d7440a2bfb4d.png)


项目不多，Star数也不多，但随便翻看一个项目的contributor，我们能看到前Googler、前Go核心团队成员、net/http包的设计者[Brad Fitzpatrick(bradfitz)](https://github.com/bradfitz)以及Go runtime的核心贡献者[Josh Bleecher Snyder(josharian)](https://github.com/josharian)。现在这两人似乎都在初创公司[tailscale](https://tailscale.com/)任职，做基于[wireguard协议](https://tonybai.com/2020/03/29/hello-wireguard/)的远程安全控制平台(简单理解就是VPN平台)。tailscale汇集了一撮Go语言的原核心开发，go4.org就是他们开源的一些misc go包。而[unsafe-assume-no-moving-gc这个包](https://github.com/go4org/unsafe-assume-no-moving-gc)就是其中之一。

那么这个包究竟是做什么的呢？我们接着往下看。

## 3. unsafe-assume-no-moving-gc的工作原理

unsafe-assume-no-moving-gc是一个非常简单的包：

```
$tree unsafe-assume-no-moving-gc -F
unsafe-assume-no-moving-gc
├── LICENSE
├── README.md
├── assume-no-moving-gc.go
├── assume-no-moving-gc_test.go
├── go.mod
└── untested.go
0 directories, 6 files
```


除了test源文件外，它的源文件只有两个assume-no-moving-gc.go和untested.go。打开这两个源文件，你会发现这个包甚至都没有提供任何API。那这个包究竟是做什么用的呢？下面是这个包的README：

![](../../assets/cb8fa5241b48c880.png)


大致的理解就是如果你的代码中使用了Go中的unsafe tip，那么**你的程序可以正常工作的前提是Go运行时垃圾回收器不是一个带迁移机制的回收器(collector)**。

所谓带迁移机制的collector，即在GC回收时可能将某些heap object挪到其他内存地址上。你的程序如果导入unsafe-assume-no-moving-gc这个包，就可以在Go GC支持迁移机制时以“程序启动崩溃”的行为提醒你。

我们来看一个例子：

```
// main.go
package main
import (
"fmt"
_ "go4.org/unsafe/assume-no-moving-gc"
)
func main() {
fmt.Println("unsafe-assume-no-moving-gc demo")
}
```


go mod tidy后，使用Go 1.20版本运行该源文件：

```
$go mod tidy
go: finding module for package go4.org/unsafe/assume-no-moving-gc
go: downloading go4.org/unsafe/assume-no-moving-gc v0.0.0-20230221090011-e4bae7ad2296
go: downloading go4.org v0.0.0-20230225012048-214862532bf5
$go run main.go
unsafe-assume-no-moving-gc demo
```


由于目前最新[Go 1.20.x版本](https://tonybai.com/2023/02/08/some-changes-in-go-1-20/)的GC并非带迁移机制的GC，因此使用Go 1.20跑上面程序不会导致panic。

我们将unsafe-assume-no-moving-gc包回退到以前的版本，比如：v0.0.0-20230221090011-e4bae7ad2296，然后再run一遍main.go：

```
$go get go4.org/unsafe/assume-no-moving-gc@v0.0.0-20201222180813-1025295fd063
go: downgraded go4.org/unsafe/assume-no-moving-gc v0.0.0-20230221090011-e4bae7ad2296 => v0.0.0-20201222180813-1025295fd063
$go run main.go
panic: Something in this program imports go4.org/unsafe/assume-no-moving-gc to declare that it assumes a non-moving garbage collector, but your version of go4.org/unsafe/assume-no-moving-gc hasn't been updated to assert that it's safe against the go1.20 runtime. If you want to risk it, run with environment variable ASSUME_NO_MOVING_GC_UNSAFE_RISK_IT_WITH=go1.20 set. Notably, if go1.20 adds a moving garbage collector, this program is unsafe to use.
goroutine 1 [running]:
go4.org/unsafe/assume-no-moving-gc.init.0()
/Users/tonybai/Go/pkg/mod/go4.org/unsafe/assume-no-moving-gc@v0.0.0-20201222180813-1025295fd063/untested.go:24 +0x1ba
exit status 2
```


从输出的panic error信息中，我们看到go4.org/unsafe/assume-no-moving-gc尚未被升级到可以信任go 1.20版本的版本，因此以Go 1.20运行该程序可能有风险。如果你能确认不会存在问题，可以用ASSUME_NO_MOVING_GC_UNSAFE_RISK_IT_WITH=go1.20这个环境变量来避免panic，比如下面这个输出：

```
$ASSUME_NO_MOVING_GC_UNSAFE_RISK_IT_WITH=go1.20 go run main.go
unsafe-assume-no-moving-gc demo
```


那么unsafe-assume-no-moving-gc包是怎么做到上述“检测”的呢？其诀窍就在untested.go这个源文件中。我们下载go4.org/unsafe/assume-no-moving-gc源码，并将其“回退”到1025295fd063这个commit时刻：

```
$git checkout 1025295fd063
Note: checking out '1025295fd063'.
... ...
HEAD is now at 1025295 flesh out package doc
```


查看untested.go：

```
// Copyright 2020 Brad Fitzpatrick. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.
// +build go1.18
package assume_no_moving_gc
import (
"os"
"runtime"
"strings"
)
func init() {
dots := strings.SplitN(runtime.Version(), ".", 3)
v := runtime.Version()
if len(dots) >= 2 {
v = dots[0] + "." + dots[1]
}
if os.Getenv(env) == v {
return
}
panic("Something in this program imports go4.org/unsafe/assume-no-moving-gc to declare that it assumes a non-moving garbage collector, but your version of go4.org/unsafe/assume-no-moving-gc hasn't been updated to assert that it's safe against the " + v + " runtime. If you want to risk it, run with environment variable " + env + "=" + v + " set. Notably, if " + v + " adds a moving garbage collector, this program is unsafe to use.")
}
```


这个文件有两个特点：

- 使用了build constraint：// +build go1.18，这意味着在你使用Go 1.18及更高版本时，该源文件才会参与编译。
- 包含了init函数，你的代码在导入assume_no_moving_gc包时，该init函数会执行，产生“副作用”。

注：关于build constraint的用法，参见go help buildconstraint。


这样，我们使用go 1.20版本运行上面main.go时，由于go 1.20版本大于go 1.18版本，untested.go将被编译且其中的init函数将被执行，如果env这个常量(“ASSUME_NO_MOVING_GC_UNSAFE_RISK_IT_WITH”)所对应的环境变量没有设置，那么init函数将走到panic，从而导致程序退出并输出panic信息。

现在我们将assume_no_moving_gc包的版本切换回最新版本，最新版本的untested.go中的build constraint如下：

```
//go:build go1.21
// +build go1.21
```


这意味着你使用Go 1.21或以上版本时，untested.go文件才会被编译，如果我们使用go 1.20版本运行main.go，我们便不会“触发”untested.go中init函数的副作用，于是main.go得以正常运行。

注：截至go 1.20版本，Go GC依然不会挪动heap object。


在理解unsafe-assume-no-moving-gc包之前，我就该包的功用“咨询”了ChatGPT，ChatGPT的回答如下：

![](../../assets/bfaa6530d536c87b.png)


可以看出，ChatGPT基本上是一本正经地“胡说八道”。

## 4. 小结

unsafe-assume-no-moving-gc只针对GC对heap object的迁移，而不会保证栈地址的迁移，我们知道，Go中栈地址是会变的，因为goroutine的初始栈才2KB，一旦超出这个范围，Go runtime就会对栈进行扩展，即分配一个更大的地址范围作为goroutine的栈，然后将原栈上的变量迁移到新栈中，这样原先栈上变量的地址就都会发生变化。

不过，如果你的Go源码中采用了unsafe tips，依赖了heap object的地址，那么这里建议你导入unsafe-assume-no-moving-gc包。但要注意，随着go最新版本的发布，你要及时更新依赖的unsafe-assume-no-moving-gc的版本。否则当用户使用最新版本go时，依赖你的包的程序就会以panic来提醒。

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

No related posts.

## 评论