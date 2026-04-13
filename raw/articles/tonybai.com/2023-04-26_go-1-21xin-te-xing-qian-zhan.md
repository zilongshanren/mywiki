---
title: Go 1.21新特性前瞻
url: https://tonybai.com/2023/04/26/go-1-21-foresight/
published: '2023-04-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.21新特性前瞻

![](../../assets/68220e5f69daf161.png)


[本文永久链接](https://tonybai.com/2023/04/26/go-1-21-foresight) – https://tonybai.com/2023/04/26/go-1-21-foresight

[Go 1.21版本](https://github.com/golang/go/milestone/279)正在如火如荼地开发当中，按照Go核心团队的一年两次的发布节奏来算，Go 1.21版本预计将在2023年8月发布([Go 1.20版本](https://tonybai.com/2023/02/08/some-changes-in-go-1-20/)是在2023年2月份发布的)。

本文将和大家一起看看Go 1.21都会带来哪些新特性。不过由于目前为时尚早，下面列出的有些变化最终不一定能进入到Go 1.21的最终版本中，所以切记一切变更要以最终Go 1.21版本发布时为准。

在细数变化之前，我们先来看看Go语言的当前状态。

## 1. Go语言当前状态

在[《2022年Go语言盘点》](https://tonybai.com/2022/12/29/the-2022-review-of-go-programming-language)一文中，我们提到年初Go语言的2022年终排名为12位，同时TIOBE官方编辑也提到：“在新兴编程语言中，Go是唯一一个可能在未来冲入前十的后端编程语言”。Go语言的发展似乎应验了这一预测，在今年的3月份，Go就再次进入编程语言排行榜前十：

![](../../assets/43a4a2947d261e66.png)


一个月后的四月初，TIOBE排行榜上，Go稳住了第10名的位次：

![](../../assets/b80bb70933c2c5ea.png)


在国内，在鹅厂前不久发布的《2022年腾讯研发大数据报告》中，

在国内，继Go在2021年从C++手中夺过红旗首次登顶鹅厂最热门编程语言之后，在鹅厂前不久发布的《2022年腾讯研发大数据报告》中，[Go蝉联鹅厂最热门编程语言](https://mp.weixin.qq.com/s/qk_byuLMYZWa8RwE3tq0rQ)，继续夯实在国内头部互联网公司内的优势地位：

![](../../assets/2570d4773166e2c4.png)


Go于2009年开源，在经历多年的宣传和鼓吹后，Go目前进入了平稳发展的阶段。疫情结束后，原先线上举办或取消的国内外的Go技术大会现在陆续又都开始恢复了，相信这会让更多开发人员接触到Go。像Go这样的能在世界各地持续多年举办技术大会的语言真是不多了。

接下来，我们就来聚焦到Go 1.21版本，挖掘一下这个版本都有哪些新特性。

## 2. 语言变化

目前Go 1.21版本里程碑中涉及语言变化的有大约2项，我们来看看。

### 2.1 增加clear预定义函数

Go 1.21[增加了一个clear预定义函数用来做切片和map的clear操作](https://github.com/golang/go/issues/56351)，其原型如下：

```
// $GOROOT/src/builtin.go
// The clear built-in function clears maps and slices.
// For maps, clear deletes all entries, resulting in an empty map.
// For slices, clear sets all elements up to the length of the slice
// to the zero value of the respective element type. If the argument
// type is a type parameter, the type parameter's type set must
// contain only map or slice types, and clear performs the operation
// implied by the type argument.
func clear[T ~[]Type | ~map[Type]Type1](t T)
```


clear是针对map和slice的操作函数，它的语义是什么呢？我们通过一个例子来看一下：

```
package main
import "fmt"
func main() {
var sl = []int{1, 2, 3, 4, 5, 6}
fmt.Printf("before clear, sl=%v, len(sl)=%d, cap(sl)=%d\n", sl, len(sl), cap(sl))
clear(sl)
fmt.Printf("after clear, sl=%v, len(sl)=%d, cap(sl)=%d\n", sl, len(sl), cap(sl))
var m = map[string]int{
"tony": 13,
"tom": 14,
"amy": 15,
}
fmt.Printf("before clear, m=%v, len(m)=%d\n", m, len(m))
clear(m)
fmt.Printf("after clear, m=%v, len(m)=%d\n", m, len(m))
}
```


运行该程序：

```
before clear, sl=[1 2 3 4 5 6], len(sl)=6, cap(sl)=6
after clear, sl=[0 0 0 0 0 0], len(sl)=6, cap(sl)=6
before clear, m=map[amy:15 tom:14 tony:13], len(m)=3
after clear, m=map[], len(m)=0
```


我们看到：

- 针对slice，clear保持slice的长度和容量，但将所有slice内已存在的元素(len个)都置为元素类型的零值；
- 针对map，clear则是清空所有map的键值对，clear后，我们将得到一个empty map。

### 2.2 改变panic(nil)语义

使用defer+recover捕获panic是Go语言唯一处理panic的方法，其典型模式如下：

```
package main
import "fmt"
func foo() {
defer func() {
if err := recover(); err != nil {
fmt.Printf("panicked: %v\n", err)
return
}
fmt.Println("it's ok")
}()
panic("some error")
}
func main() {
foo()
}
```


运行上面程序会输出：

```
panicked: some error
```


例子中我们向panic传入了表示panic原因的字符串，panic的参数是一个interface{}类型，可以传入任意值，当然**也可以传入nil**。

比如上面例子，当我们给foo函数的panic调用传入nil时，我们将得到下面结果：

```
it's ok
```


这可能会给开发者带去疑惑：明明是触发了panic，但函数却按照正常逻辑处理！2018年，前Go核心团队成员bradfitz就提出了一个issue：[spec: guarantee non-nil return value from recover](https://github.com/golang/go/issues/25448)，提出当开发者调用panic(nil)时，recover应该返回某种runtime error，而不是nil。这个issue在今年被纳入了Go 1.21版本，现在[该issue的实现](https://go-review.googlesource.com/c/go/+/461956)已经被merge到了主干。

新的实现在src/runtime/panic.go中定义了一个名为PanicNilError的新Error：

```
// $GOROOT/src/runtime/panic.go
// A PanicNilError happens when code calls panic(nil).
//
// Before Go 1.21, programs that called panic(nil) observed recover returning nil.
// Starting in Go 1.21, programs that call panic(nil) observe recover returning a *PanicNilError.
// Programs can change back to the old behavior by setting GODEBUG=panicnil=1.
type PanicNilError struct {
// This field makes PanicNilError structurally different from
// any other struct in this package, and the _ makes it different
// from any struct in other packages too.
// This avoids any accidental conversions being possible
// between this struct and some other struct sharing the same fields,
// like happened in go.dev/issue/56603.
_ [0]*PanicNilError
}
func (*PanicNilError) Error() string { return "panic called with nil argument" }
func (*PanicNilError) RuntimeError() {}
```


Go编译器会将panic(nil)替换为panic(new(runtime.PanicNilError))，这样我们用Go 1.21版本运行上面的程序，我们就会得到下面结果了：

```
panicked: panic called with nil argument
```


如果你的遗留代码中调用了panic(nil)(注：显然这不是一种很idiomatic的作法)，升级到Go 1.21版本后你就要小心了。如果你想保留原先的panic(nil)行为，可以用GODEBUG=panicnil=1。

有童鞋可能会质疑这违反了[Go1兼容性承诺](https://go.dev/doc/go1compat)，但实际上Go1兼容性规范保留了对语言规范中不一致或错误的修订权力，即便这种修订会导致遗留代码出现与原先不一致的行为。

## 3. 编译器与工具链

每个Go版本中，编译器和工具链的改动都不少，我们挑重点看一下：

### 3.1 一些OS的最小支持版本的更新

Go 1.21开始，go installer[支持最小macOS版本更新为10.15](https://github.com/golang/go/issues/58105)，而[最小Windows版本为Windows 10](https://go-review.googlesource.com/c/build/+/478616)。

### 3.2 低版本的go编译器将拒绝编译高版本的go module

从Go 1.21版本开始，[低版本的go编译器将拒绝编译高版本的go module](https://github.com/golang/go/issues/59033)(go.mod中go version标识最低版本) ，这也是Russ Cox策划的[Go扩展的向前兼容性](https://go.googlesource.com/proposal/+/master/design/57001-gotoolchain.md)提案的一部分。此外，[Go扩展向前兼容性](https://github.com/golang/go/issues/57001)提案感觉比较复杂，可能不会全部在Go 1.21版本落地。

### 3.3 支持WASI

Go从[1.11版本](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)就开始支持将Go源码编译为wasm二进制文件，并在支持wasm的浏览器环境中运行。

不过WebAssembly绝不仅仅被设计为仅限于在Web浏览器中运行，核心的WebAssembly语言是独立于其周围环境的，WebAssembly完全可以通过API与外部世界互动。在Web上，它自然使用浏览器提供的现有Web API。然而，在浏览器之外，之前还没有一套标准的API可以让WebAssembly程序使用。这使得创建真正可移植的非Web WebAssembly程序变得困难。[WebAssembly System Interface(WASI)](https://wasi.dev)是一个填补这一空白的倡议，它有一套干净的API，可以由多个引擎在多个平台上实现，并且不依赖于浏览器的功能（尽管它们仍然可以在浏览器中运行）。

[Go 1.21将增加对WASI的支持](https://github.com/golang/go/issues/58141)，初期先支持[WASI Preview1版本](https://github.com/WebAssembly/WASI/blob/b44552d84267af4d5899ed32364966740ef1846e/legacy/preview1/docs.md)，之后会支持WASI Preview2版本，直至最终WASI API版本发布！目前我们可以使用GOOS=wasip1 GOARCH=wasm将Go源码编译为支持WASI的wasm程序，下面是一个例子：

```
// main.go
package main
func main() {
println("hello")
}
```


下载最新go dev版本后(go install http://golang.org/dl/gotip@latest)，可以执行下面命令将main.go编译为wasm程序：

```
$ GOARCH=wasm GOOS=wasip1 gotip build -o main.wasm main.go
```


开源的wasm运行时有很多，[wazero](https://wazero.io/)是目前比较火的且使用纯Go实现的wasm运行时程序，安装wazero后，可以用来执行上面编译出来的main.wasm：

```
$curl https://wazero.io/install.sh
$wazero run main.wasm
hello
```


### 3.4 Go 1.21可能推出纯静态工具链，不再依赖glibc

使用纯Go实现的net resolver，原先DNS的问题也将被解决，这样Go团队很可能[在构建工具链的时候使用CGO_ENABLED=0构建出静态工具链](https://github.com/golang/go/issues/57007)，没有动态链接库的依赖。

### 3.5 go test -c支持为多个包同时构建测试二进制程序

Go 1.21版本之前，go test -c仅支持将单个包的测试代码编译为测试二进制程序，Go 1.21版本则[允许我们同时为多个包构建测试二进制程序](https://github.com/golang/go/issues/15513)。

下面是官方给出的例子：

```
$ go test -c -o /tmp ./pkg1 ./pkg2 ./pkg2
$ ls /tmp
pkg1.test pkg2.test pkg3.test
```


今天使用go env -w命令修改的默认环境变量会写入：filepath.Join(os.UserConfigDir(), “go/env”)。在Mac上，这个路径是\$HOME/Library/Application Support/go/env；在Linux上，这个路径是\$HOME/.config/go/env。

Go 1.21将增加一个全局层次上的go.env，放在\$GOROOT下面，目前默认的go.env为：

```
// $GOROOT/go.env
# This file contains the initial defaults for go command configuration.
# Values set by 'go env -w' and written to the user's go/env file override these.
# The environment overrides everything else.
# Use the Go module mirror and checksum database by default.
# See https://proxy.golang.org for details.
GOPROXY=https://proxy.golang.org,direct
GOSUMDB=sum.golang.org
```


我们仍然可以通过go env -w命令修改user级的env文件来覆盖上述配置，当然最高优先级的是OS用户环境变量，如果在OS用户环境变量文件(比如.bash_profile、.bashrc)中设置了Go的环境变量值，比如GOPROXY等，那么以OS用户环境变量为优先。

## 4. 标准库

我们接下来再来看看变更最多的一部分：标准库，我们将对主要变更项作简要介绍。

### 4.1 slices和maps进入标准库

[Go 1.18版本](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)泛型落地发布前的最后一刻，Rob Pike叫停了slices、maps等泛型包的入库，后来这两个包先放置在golang.org/x/exp下作为实验包。随着Go泛型日益成熟以及Go团队对泛型使用经验的增多，Go团队终于决定将[golang.org/x/exp/slices](https://github.com/golang/go/issues/57433)和[golang.org/x/exp/maps](https://github.com/golang/go/issues/57436)在Go 1.21版本中将挪入标准库。

### 4.2 log/slog加入标准库

log/slog是Go官方版结构化日志包，大致与uber的zap包相当。在我之前的一篇文章[《slog：Go官方版结构化日志包》](https://tonybai.com/2022/10/30/first-exploration-of-slog)有对slog的详尽说明，大家可以移步到那篇文章看看。不过slog的proposal依旧很多，后续slog可能会有持续改进和变更，与那篇文章中的内容可能会有一些差异。

在sync.Once的基础上，这个issue增加了三个与Once相关的”语法糖”API，用在一些对Once有需求的最常见的场景中。

Go 1.21为testing包增加了func Testing() bool函数，该函数可以用来报告当前程序是否是go test创建的测试程序。使用Testing函数，我们可以确保一些无需在单测阶段执行的函数不被执行。比如下面例子来自这个issue：

```
// file/that/should/not/be/used/from/testing.go
func prodEnvironmentData() *Environment {
if testing.Testing() {
log.Fatal("Using production data in unit tests")
}
....
}
```


### 4.5 一些变更点

[context: 增加为deadline或timeout context设置cancel原因的API](https://github.com/golang/go/issues/56661)– https://github.com/golang/go/issues/56661[unicode升级到15.0版本](https://github.com/golang/go/issues/55079)– https://github.com/golang/go/issues/55079

## 5. 参考资料

[Go 1.21 milestone](https://github.com/golang/go/milestone/279)– https://github.com/golang/go/milestone/279

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