---
title: Go 1.13中值得关注的几个变化
url: https://tonybai.com/2019/10/27/some-changes-in-go-1-13/
published: '2019-10-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.13中值得关注的几个变化

2019年对于[Go语言](https://golang.org)来说也是一个重要的年份，因为在2019年的11月10日，[Go](https://tonybai.com/tag/go)即将迎来其[开源10周年](https://tonybai.com/2017/10/24/go-evolution-for-ten-years-an-interview-by-osc)的纪念日。在这个重要日子的前夕，在GopherCon 2019大会后，Go项目组在2019.9.4日发布了[Go 1.13版本](https://tip.golang.org/doc/go1.13)。

![img{512x368}](../../assets/c0d5410a29f23802.png)


这是自2017年GopherCon大会上[Russ Cox](https://swtch.com/~rsc/)做[“Toward Go 2″](https://blog.golang.org/toward-go2)主题演讲以来Go项目发布的第四个版本（前三个分别是：[go 1.10](https://tonybai.com/2018/02/17/some-changes-in-go-1-10)、[go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)和[go 1.12](https://tonybai.com/2019/03/02/some-changes-in-go-1-12/))。

Go2是这两年Go项目的核心主题。Go项目组也一直在摸索着向Go2演化的节奏和过程规范，并已经从[Go 1.11版本](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)起做出了实质性的动作：添加[go module机制](https://tonybai.com/2019/06/03/the-practice-of-upgrading-major-version-under-go-module/)、[错误处理优化](https://tonybai.com/2019/10/18/errors-handling-in-go-1-13/)、[泛型讨论和多次草案的发布](https://github.com/golang/go/issues/15292)等。Russ Cox这段时间还在自己的博客上撰写了[一系列有关Go proposal流程究竟该如何改进的探索性文章](https://research.swtch.com/proposals)，这与当年[vgo](https://github.com/golang/vgo/)“放大招”前的节奏有些相似:)。

回归正题，我们来说[Go 1.13](https://tip.golang.org/doc/go1.13)这个版本。Go 1.13延续了对之前版本添加的Go2特性：[Go module](https://tonybai.com/2018/07/15/hello-go-module/)的优化；并且从该版本开始，Go项目组开启了Go2中呼声也很高的[错误处理](https://github.com/golang/proposal/blob/master/design/go2draft-error-handling-overview.md)的优化。下面我们详细来看看Go 1.13中值得关注的几个变化。

## 1. 语言

Go 1.13中，Go语言规范有了一些小变化。

Go在设计伊始就和多数C-Family语言一样继承了[C语言](https://tonybai.com/tag/c)关于**数字字面量(number literal)**的语法形式，和1978年发布的[K&R C](https://en.wikipedia.org/wiki/K%26R_C)一样，Go仅支持十进制、八进制、十六进制和十进制形式的浮点数的数字字面量形式，比如：

```
a := 53 //十进制
b := 0700 // 八进制，以"0"开头
c := 0xaabbcc // 十六进制 以"0x"开头
c1 := 0Xddeeff // 十六进制 以"0X"开头
f1 := 10.24 // 十进制浮点数
f2 := 1.e+0 // 十进制浮点数
f3 := 31415.e-4 // 十进制浮点数
```


这些数字字面量语法应该说是够用的，但是和其他语言在进化过程中添加的其他数字字面量表达形式相比，又显得有些不足。于是Go设计者决定在Go 1.13版本中增加Go对数字字面量的表达能力，在这方面对Go语言做了如下补充：

-
增加二进制数字字面量，以0b或0B开头

-
在保留以”0″开头的八进制数字字面量形式的同时，增加以”0o”或”0O”开头的八进制数字字面量形式

-
增加十六进制形式的浮点数字面量，以0x或0X开头的、形式如0×123.86p+2的浮点数

-
为提升可读性，在数字字面量中增加数字分隔符”_”，分隔符可以用来分隔数字(起到分组提高可读性作用，比如每3个数字一组)，也可以用来分隔前缀与第一个数字。


```
a := 5_3_7
b := 0o700
b1 := 0O700
b2 := 0_700
b3 := 0o_700
c := 0b111
c1 := 0B111
c2 := 0b_111
f1 := 0x10.24p+3
f2 := 0x1.Fp+0
f3 := 0x31_415.p-4
```


注：截至目前，有些第三方工具依然无法识别数字字面量中的分隔符，会误报其为语法错误。


Go 1.13中关于语言规范方面的另一个变动点是**取消了移位操作(>>的<<)的右操作数仅能是无符号数的限制**，以前必须的强制到uint的转换现在不必要了：

```
var i int = 5
fmt.Println(2 << uint(i)) // before go 1.13
fmt.Println(2 << i) // in go 1.13 and later version
```


不过值得注意的是：[go 1.12版本](https://tonybai.com/2019/03/02/some-changes-in-go-1-12)在go.mod文件中增加了一个go version的指示字段，用于指示该module内源码所使用的 go版本。Go 1.13的发布文档强调了**只有在go.mod中的go version指示字段为go 1.13(以及以后版本)时，上述的语言特性变更才会生效**，否则就会报类似下面的错误：

```
// github.com/bigwhite/experiments/go1.13-examples/number_literal.go
$go run number_literal.go
# command-line-arguments
./number_literal.go:23:7: underscores in numeric literals only supported as of -lang=go1.13
./number_literal.go:24:7: 0o/0O-style octal literals only supported as of -lang=go1.13
./number_literal.go:25:8: 0o/0O-style octal literals only supported as of -lang=go1.13
./number_literal.go:26:8: underscores in numeric literals only supported as of -lang=go1.13
./number_literal.go:27:8: underscores in numeric literals only supported as of -lang=go1.13
./number_literal.go:28:7: binary literals only supported as of -lang=go1.13
./number_literal.go:29:8: binary literals only supported as of -lang=go1.13
./number_literal.go:30:8: underscores in numeric literals only supported as of -lang=go1.13
./number_literal.go:31:8: hexadecimal floating-point literals only supported as of -lang=go1.13
./number_literal.go:32:8: hexadecimal floating-point literals only supported as of -lang=go1.13
./number_literal.go:32:8: too many errors
// github.com/bigwhite/experiments/go1.13-examples/shift_with_signed_operand.go
$go run shift_with_signed_operand.go
# command-line-arguments
./shift_with_signed_operand.go:8:16: invalid operation: 2 << i (signed shift count type int, only supported as of -lang=go1.13)
```


当然，如果repo下没有go.mod或者单独在某个没有go.mod的目录下使用go 1.13编译器运行上面代码，则是无问题的。

## 2. Go module机制的继续优化以及行为变化

Go module自[Go 1.11版本](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)加入Go以来收到了[Go社区的大量反馈](https://github.com/golang/go/wiki/Modules)，Go核心团队也针对这些反馈对Go module机制进行了持续地优化。在Go 1.13中，Go module的一些改变如下：

### 1) GO111MODULE=auto的行为变化

在Go 1.12版本中，GO111MODULE默认值为auto，在auto模式下，GOPATH/src下面的repo以及在GOPATH之外的repo依旧使用GOPATH mode，不使用go.mod来管理依赖；在Go 1.13中，module mode优先级提升，GO111MODULE的默认值依然为auto，但在这个auto下，无论是在GOPATH/src下还是GOPATH之外的repo中，只要目录下有go.mod，go编译器都会使用go module来管理依赖。

### 2) [GOPROXY](https://tonybai.com/2018/11/26/hello-go-module-proxy/)有默认初值并支持设置成多个代理的列表

之前版本中，GOPROXY这个环境环境变量默认值为空，go编译器都是直接与类似github.com这样的代码托管站点通信并获取相关依赖库的数据的；一些第三方GOPROXY服务发布后，迁移到go module的gopher们发现：大多数情况下通过proxy获取依赖包数据的速度要远高于直接从代码托管站点获取，因此GOPROXY总是会配置上一个值。Go核心团队也希望Go世界能有一个像nodejs那样的中心化的module仓库为大家提供服务，于是在Go 1.13中将https://proxy.golang.org作为GOPROXY环境变量的默认值之一，这也是Go官方提供的GOPROXY服务。

同时GOPROXY支持设置为多个proxy的列表(多个proxy之间采用逗号分隔)，Go编译器会按顺序尝试列表中的proxy以获取依赖包数据，但是当有proxy server服务不可达或者是返回的http状态码不是404也不是410时，go会终止数据获取。

Go 1.13中，GOPROXY的默认值为https://proxy.golang.org,direct。当官方代理返回404或410时，Go编译器会尝试直接连接依赖module的代码托管站点以获取数据。

由于国内无法访问Go官方的proxy，因此我一般会将我的工作环境下的GOPROXY设置为：

```
export GOPROXY=https://goproxy.cn,自己在国外主机使用athens搭建的代理,direct
```


### 3) GOSUMDB

我们知道go会在go module启用时在本地建立一个go.sum文件，用来存储依赖包特定版本的加密校验和。同时，Go维护下载的软件包的缓存，并在下载时计算并记录每个软件包的加密校验和。在正常操作中，go命令对照这些预先计算的校验和去检查某repo下的go.sum文件，而不是在每次命令调用时都重新计算它们。

在日常开发中，特定module版本的校验和永远不会改变。每次运行或构建时，go命令都会通过本地的go.sum去检查其本地缓存副本的校验和是否一致。如果校验和不匹配，则go命令将报告安全错误，并拒绝运行构建或运行。在这种情况下，重要的是找出正确的校验和，确定是go.sum错误还是下载的代码是错误的。如果go.sum中尚未包含已下载的module，并且该模块是公共module，则go命令将查询Go校验和数据库以获取正确的校验和数据存入go.sum。如果下载的代码与校验和不匹配，则go命令将报告不匹配并退出。

Go 1.13提供了GOSUMDB环境变量用于配置Go校验和数据库的服务地址（和公钥），其默认值为”sum.golang.org”，这也是Go官方提供的校验和数据库服务(大陆gopher可以使用sum.golang.google.cn)。

出于安全考虑，建议保持GOSUMDB开启。但如果因为某些因素，无法访问GOSUMDB（甚至是sum.golang.google.cn），可以通过下面命令将其关闭：

```
go env -w GOSUMDB=off
```


GOSUMDB关闭后，仅能使用本地的go.sum进行包的校验和校验了。

### 4）面向私有模块的GOPRIVATE

有了GOPROXY后，公共module的数据获取变得十分easy。但是如果依赖的是企业内部module或托管站点上的private库，通过GOPROXY（默认值）获取显然会得到一个失败的结果，除非你搭建了自己的公私均可的goproxy server并将其设置到GOPROXY中。

Go 1.13提供了GOPRIVATE变量，用于指示哪些仓库下的module是private，不需要通过GOPROXY下载，也不需要通过GOSUMDB去验证其校验和。不过要注意的是GONOPROXY和GONOSUMDB可以override GOPRIVATE中的设置，因此设置时要谨慎，比如下面的例子：

```
GOPRIVATE=pkg.tonyba.com/private
GONOPROXY=none
GONOSUMDB=none
```


GOPRIVATE指示pkg.tonybai.com/private下的包不经过代理下载，不经过SUMDB验证。但GONOPROXY和GONOSUMDB均为none，意味着所有module，不管是公共的还是私有的，都要经过proxy下载，经过sumdb验证。前面提到过了，GONOPROXY和GONOSUMDB会override GOPRIVATE的设置，因此在这样的配置下，所有依赖包都要经过proxy下载，也要经过sumdb验证。不过这个例子中的GOPRIVATE的值也不是一无是处，它可以给其他go tool提供私有module的指示信息。

## 3. Go错误处理优化迈出第一步

Go核心团队早在一年前就提出了关于go错误处理的[多个proposal](https://github.com/golang/proposal/blob/master/design/go2draft-error-handling-overview.md)，其中涉及解决if err != nil 大量重复问题的，有解决错误包装(wrap)问题的，有解决error value比较问题的。在Go 1.13中，Go核心团队落实了后两个：

-
通过标准库增加了errors.Is和As函数来解决error value比较问题

-
增加errors.Unwrap来解决error unwrap问题。


并且Go通过在fmt.Errorf中新增的”%w”动词来协助Gopher快速创建一个包装错误，创建的error变量实现了下面接口：

```
interface { // 一个匿名接口
Unwrap() error
}
```


关于Go 1.13中错误处理的改进，Go官方发表了一篇博客[《Go 1.13中的错误处理》](https://tonybai.com/2019/10/18/errors-handling-in-go-1-13/)给出了十分详尽的说明，这里就不赘述了。

## 4. 性能

个人觉得Go 1.13中能带来性能提升的变动主要有三个：

第一个就是defer的性能提升。

defer语法让Gopher在进行资源(文件、锁)释放的过程变动优雅很多，也不易出错。但在性能敏感的应用中，defer带来的性能负担也是Gopher必须要权衡的问题。在Go 1.13中，Go核心团队对defer性能做了大幅优化，官方给出了在大多数情况下，defer性能提升30%的说法。

这里可以来验证一下：我们使用Go 1.13和Go 1.12.7两个版本运行同一个benchmark(macos 1.6G 8核 16G内存)：

```
// github.com/bigwhite/experiments/go1.13-examples/defer_benchmark_test.go
package defer_test
import "testing"
func sum(max int) int {
total := 0
for i := 0; i < max; i++ {
total += i
}
return total
}
func foo() {
defer func() {
sum(10)
}()
sum(100)
}
func BenchmarkDefer(b *testing.B) {
for i := 0; i < b.N; i++ {
foo()
}
}
```


go 1.13下的benchmark结果：

```
$go test -bench . defer_benchmark_test.go
goos: darwin
goarch: amd64
BenchmarkDefer-8 17341530 67.3 ns/op
PASS
ok command-line-arguments 1.245s
```


go 1.12.7下的benchmark结果：

```
$go test -bench . defer_benchmark_test.go
goos: darwin
goarch: amd64
BenchmarkDefer-8 20000000 76.5 ns/op
PASS
ok command-line-arguments 1.618s
```


我们看到性能的确有提升，但没有到30%这么大幅度，也许这仅仅是一个个例吧。

第二个是优化后的逃逸分析(escape analysis)让编译器在选择究竟将变量分配在stack上还是heap上的时候更加精确。在老版本里分配到heap上的变量，在Go 1.13中可能就会分配到stack上，从而减少内存分配的次数，一定程度上减轻gc的压力，达到性能提升的目的。

第三个是sync包中Mutex、RWMutex的方法的inline化带来的性能提升，官方说法是10%。我们同样来benchmark一下：

```
// github.com/bigwhite/experiments/go1.13-examples/mutex_benchmark_test.go
package mutex_test
import (
"sync"
"testing"
)
func sum(max int) int {
total := 0
for i := 0; i < max; i++ {
total += i
}
return total
}
func foo() {
var mu sync.Mutex
mu.Lock()
sum(10)
mu.Unlock()
}
func BenchmarkMutex(b *testing.B) {
for i := 0; i < b.N; i++ {
foo()
}
}
```


Go 1.13下的结果：

```
$go test -bench . mutex_benchmark_test.go
goos: darwin
goarch: amd64
BenchmarkMutex-8 43395768 26.4 ns/op
PASS
ok command-line-arguments 1.182s
```


Go 1.12.7下的结果：

```
$go test -bench . mutex_benchmark_test.go
goos: darwin
goarch: amd64
BenchmarkMutex-8 50000000 28.4 ns/op
PASS
ok command-line-arguments 1.457s
```


从结果看，提升在7%左右，约等于10%吧。

## 5. 其他变化

简单罗列一些我认为值得关注的小变化：

-
Go 1.13现在支持Android 10了；对MacOS的支持需要至少10.11版本；

-
godoc不再和go、gofmt放入go release版中，需要godoc的，需要单独从golang.org/x/tools/cmd/godoc中下载安装；

-
crypto/tls默认开启tls 1.3支持；

-
unicode包支持的unicode标准从10.0版本升级到

[Unicode 11.0版本](http://www.unicode.org/versions/Unicode11.0.0/)

## 6. 小结

Go 1.13版本的发布标志着Go向着Go2的目标又迈出了坚实的一步，Go的演化节奏也是恰到好处：

-
go module已经落地成型，逐渐打磨到成熟；

-
错误处理：迈出阶段性的一步，后续持续改进

-
Go generics: 是Go2最大的”挑战”。我们看到在GopherCon 2019大会上，

[Ian Lance Taylor](https://github.com/ianlancetaylor)带来的有关Go generics的[proposal的改进](https://github.com/golang/proposal/blob/master/design/go2draft-contracts.md)正在被越来越多Gopher所认可。

不过按照go team的行事风格，任何一个proposal都会经历”实验，简化和发布”的步骤，Go generics还有很长的路要走，让我们共同期待！

本文中涉及的样例源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go1.13-examples)获取到。

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

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论