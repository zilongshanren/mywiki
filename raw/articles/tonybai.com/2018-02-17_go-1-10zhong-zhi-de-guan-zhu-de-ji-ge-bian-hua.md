---
title: Go 1.10中值得关注的几个变化
url: https://tonybai.com/2018/02/17/some-changes-in-go-1-10/
published: '2018-02-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.10中值得关注的几个变化

又到了Go语言新版本的发布时间窗口了！这次的主角是[Go 1.10](https://tip.golang.org/doc/go1.10)。

![img{512x368}](../../assets/1efb1da213abc8c7.png)


曾几何时， 这是很多Gopher在[Go 1.8](http://tonybai.com/2017/02/03/some-changes-in-go-1-8/)、[Go 1.9](http://tonybai.com/2017/07/14/some-changes-in-go-1-9/)时猜测是否存在的那个版本，毕竟minor version即将进化到两位数。从Go语言第一封设计mail发出到现在的[十年间](http://tonybai.com/2017/09/24/go-ten-years-and-climbing/)，尤其是Go语言经历了近几年的爆发式增长，基本奠定了云原生第一语言的位置之后，人们对Go语言有了更多新的、更为深刻的认知，同时对这门编程语言也有了更多的改进和优化的期望。Go2在Gopher心中的位置日益提升，直到[Russ Cox](https://swtch.com/~rsc/)在[GopherCon 2017](https://github.com/gophercon/2017-talks)上公布了Go core team对[Go2的开发策略](https://blog.golang.org/toward-go2)，我们才意识到：**哦，Go1还将继续一段时间，甚至是一段很长的时间。2018年2月，我们将迎来Go 1.10版本**。

从[Go 1.4版本](http://tonybai.com/2014/11/04/some-changes-in-go-1-4/)开始，我自己都没想到我能将**“Go x.x中值得关注的几个变化”**这个系列一直写到Go 1.10。不过现在看来，这个系列还会继续，以后可能还有Go 1.11、Go 1.12…，甚至是进化到Go2之后的各个版本。

Go从[1.0版本发布](https://blog.golang.org/go-version-1-is-released)之日起，便遵守着自己**“变与不变”**的哲学。不变的是对Go对[“Go1 promise of compatibility”](https://tip.golang.org/doc/go1compat.html)的严格遵守，变化的则是对语言性能、运行时、GC、工具以及标准库更为精细和耐心地打磨。这次发布的Go 1.10依然延续着这种理念，将重点的改进放在了运行时、工具以及标准库上。接下来，我就和大家一起看看即将发布的Go 1.10都有哪些值得重点关注的变化。

## 一、语言

[Go language Spec](https://golang.org/ref/spec)是当前[Go语言](http://tonybai.com/tag/go)的唯一语言规范标准，虽然其严谨性与那些以ISO标准形式编写成的语言规范（比如：C语言、C++语言的规范）还有一定差距。因此，对go spec的优化，就是在严谨性方面下功夫。当前spec的主要修订者是Go语言三个设计者之一的[Robert Griesemer](https://github.com/griesemer)，他在Go 1.10周期对spec**做了较多语言概念严谨性方面的改进**。

### 1、显式定义Representability（可表示性）

在[Properties of types and values](https://tip.golang.org/ref/spec#Properties_of_types_and_values)章节下，Robert Griesemer显式引入了一个新的术语[Representability](https://tip.golang.org/ref/spec#Representability)，这里译为**可表示性**。这一术语的[引入](https://github.com/golang/go/commit/b40831b115e46e9de719bddccf2d27d7d4940756#diff-94792ed6b8d17736ee79af0ca532d6fe)并未带来语法的变化，只是为了更精确的阐释规范。Representability的定义明确了当规范中出现“a constant x is representable by a value of type T”时成立的几种条件，尤其是针对浮点类型和复数类型。这里摘录（不翻译）：

```
A constant x is representable by a value of type T if one of the following conditions applies:
- x is in the set of values determined by T.
- T is a floating-point type and x can be rounded to T's precision without overflow. Rounding uses IEEE 754 round-to-even rules but with an IEEE negative zero further simplified to an unsigned zero. Note that constant values never result in an IEEE negative zero, NaN, or infinity.
- T is a complex type, and x's components real(x) and imag(x) are representable by values of T's component type (float32 or float64).
```


### 2、澄清未指定类型的常量作为shift(移位)非常量位操作的左操作数时在某些特定上下文中的类型

虽然不及ISO标准规范严谨，但凡是language spec，理解起来都是有门槛的。这个[改进针对的是那些未指定类型的常量](https://github.com/golang/go/commit/9690d245d56d547c40dac269140dcddc6eb80904#diff-94792ed6b8d17736ee79af0ca532d6fe)，在作为shift非常量位操作的左操作数时，在shift表达式结果作为下标表达式中的下标、切片表达式下标或者make函数调用中的size参数时，这个常量将被赋予int类型。我们还是看个例子更加直观：

```
// go1.10-examples/spec/untypedconst.go
package main
var (
s uint = 2
)
func main() {
a := make([]int, 10)
a[1.0<<s] = 4
}
```


上面的例子中，重点看**a[1.0 << s] = 4**这一行，这一行恰好满足了几个条件：

- 1.0 << s 是一个shift表达式，且作为slide表达式的下标；
- shift表达式所移动的位数为s，s是一个变量，非常量，因此这是一个非常量位的移位操作；
- 1.0是未指定类型的常量(untyped const)，且作为shift表达式左操作数

在Go 1.9.2下面，上面的程序编译结果如下：

```
// go 1.9.2编译器build：
$go build untypedconst.go
# command-line-arguments
./untypedconst.go:9:7: invalid operation: 1 << s (shift of type float64)
```


在Go 1.9.2下，1.0这个常量被compiler赋予了float64类型，导致编译出错。在Go 1.10下，根据最新的spec，1.0被赋予了int型，编译则顺利通过。

但一旦脱离了下标这个上下文环境，1.0这个常量依旧会被compiler识别为float64类型，比如下面代码中1.0<<s作为Println的参数就是不符合语法的：

```
// go1.10-examples/spec/untypedconst.go
package main
import "fmt"
var (
s uint = 2
)
func main() {
a := make([]int, 10)
a[1.0<<s] = 4
fmt.Println(1.0<<s)
}
// go 1.10rc2编译器build：
$go build untypedconst.go
# command-line-arguments
./untypedconst.go:12:17: invalid operation: 1 << s (shift of type float64)
./untypedconst.go:12:17: cannot use 1 << s as type interface {} in argument to fmt.Println
```


### 3、明确预声明类型(predeclared type)是defined type还是alias type

Go在[1.9版本](http://tonybai.com/2017/07/14/some-changes-in-go-1-9/)中引入了alias语法，同时引入defined type(以替代named type)和alias type，并使用alias语法对某些predeclared type的实现进行了调整。在Go 1.10 spec中，Griesemer进一步[明确了哪些predeclared type是alias type](https://github.com/golang/go/commit/4a2391e7c965f7ed4d1ec189087293c1f6bae43c#diff-94792ed6b8d17736ee79af0ca532d6fe)：

```
目前内置的predeclared type只有两个类型是alias type:
byte alias for uint8
rune alias for int32
```


其余的predeclared type都是defined type。

### 4、移除spec中对method expression: T.m中T的类型的限制

这次是spec落伍于compiler了。Go 1.9.2就可以顺利编译运行下面的代码：

```
//go1.10-examples/spec/methodexpression.go
package main
import "fmt"
type foo struct{}
func (foo)f() {
fmt.Println("i am foo")
}
func main() {
interface{f()}.f(foo{})
}
```


但在Go 1.9.2的spec中，对Method expression的定义如下：

```
Go 1.9.2 spec:
MethodExpr = ReceiverType "." MethodName .
ReceiverType = TypeName | "(" "*" TypeName ")" | "(" ReceiverType ")" .
```


Go 1.9.2的spec说，method expression形式:T.m中的T仅能使用Typename，而非上述代码中type实现。Go 1.10的spec中[放开了对method expression中T的限制](https://github.com/golang/go/commit/f2d52519e1fad35566afb46ef521934cf0f5e5fd#diff-94792ed6b8d17736ee79af0ca532d6fe)，使得type的实现也可以作为T调用method，与编译器的实际实现行为同步：

```
Go 1.10rc2 spec:
MethodExpr = ReceiverType "." MethodName .
ReceiverType = Type .
```


不过目前Go 1.10 rc2 compiler还存在[一个问题](https://github.com/golang/go/issues/22444)，我们看一下下面的代码：

```
//go1.10-examples/spec/methodexpression1.go
package main
func main() {
(*struct{ error }).Error(nil)
}
```


使用Go 110rc2构建该源码，得到如下错误：

```
$go build methodexpression1.go
# command-line-arguments
go.(*struct { error }).Error: call to external function
main.main: relocation target go.(*struct { error }).Error not defined
main.main: undefined: "go.(*struct { error }).Error"
```


该问题目前已经有[issue](https://github.com/golang/go/issues/22444)对应，状态还是Open。

## 二、工具

Go语言有着让其他主流编程语言羡慕的工具集，每次Go版本更新，工具集都会得到进一步的加强，无论是功能还是从开发者体验方面，都有提升。

### 1、默认的GOROOT

继[Go 1.8版本](http://tonybai.com/2017/02/03/some-changes-in-go-1-8/)引入默认的GOPATH后，Go 1.10版本为继续改进Go工具的开发者体验，进一步降低新手的使用门槛，引入了默认GOROOT：即开发者无需显式设置GOROOT环境变量，go程序会自动根据自己所在路径推导出GOROOT的路径。这样一来，Gopher们就可以将下载的Go预编译好的安装包解压放置到任意本地路径下，唯一要做的就是将go二进制程序路径放置到PATH环境变量中。比如我们将go1.10rc2的安装包解压到下面路径下：

```
➜ /Users/tony/.bin/go1.10rc2 $ls
AUTHORS LICENSE VERSION blog/ lib/ robots.txt
CONTRIBUTING.md PATENTS api/ doc/ misc/ src/
CONTRIBUTORS README.md bin/ favicon.ico pkg/ test/
```


在设置为PATH后，我们通过go env命令查看go自动推导的GOROOT以及其他相关变量的值：

```
$go env
GOARCH="amd64"
GOBIN=""
GOCACHE="/Users/tony/Library/Caches/go-build"
GOEXE=""
GOHOSTARCH="amd64"
GOHOSTOS="darwin"
GOOS="darwin"
GOPATH="/Users/tony/go"
GORACE=""
GOROOT="/Users/tony/.bin/go1.10rc2"
GOTMPDIR=""
GOTOOLDIR="/Users/tony/.bin/go1.10rc2/pkg/tool/darwin_amd64"
GCCGO="gccgo"
CC="clang"
CXX="clang++"
CGO_ENABLED="1"
CGO_CFLAGS="-g -O2"
CGO_CPPFLAGS=""
CGO_CXXFLAGS="-g -O2"
CGO_FFLAGS="-g -O2"
CGO_LDFLAGS="-g -O2"
PKG_CONFIG="pkg-config"
GOGCCFLAGS="-fPIC -m64 -pthread -fno-caret-diagnostics -Qunused-arguments -fmessage-length=0 -gno-record-gcc-switches -fno-common"
```


从输出结果看到，go正确找到了安装路径，并得到了GOROOT信息。

### 2、增加GOTMPDIR变量

在上面的go env命令输出内容中，我们发现了一个陌生的变量：GOTMPDIR，其值默认为空串。这个[GOTMPDIR变量](https://go-review.googlesource.com/c/go/+/75475)是Go 1.10新引入的变量，用于设置Go tool创建和使用的临时文件的路径的。有人可能会说：这个变量看似没什么必要，直接用系统的/tmp路径就好了啊。但是在/tmp路径中编译和执行编译后的程序至少有两点问题，[这些问题](https://github.com/golang/go/issues/8451)实际上在go的issues历史中已经存在许久了：

- 有些机器上/tmp路径下被设置了
[无执行权限(set noexec)](https://github.com/golang/go/issues/8451) - 有些机器上/tmp下空间有限

我们知道默认情况下，go build和go run都会在/tmp下设置一个临时WORK目录来编译源码和执行编译后的程序的，从下面的一个最简单的helloworld源码的编译执行过程输出(WORK变量)，我们就能看到这点：

```
// on ubuntu 16.04
# go run -x hello.go
WORK=/tmp/go-build001434392
mkdir -p $WORK/b001/
... ...
mkdir -p $WORK/b001/exe/
cd .
/root/.bin/go1.10rc2/pkg/tool/linux_amd64/link -o $WORK/b001/exe/hello -importcfg $WORK/b001/importcfg.link -s -w -buildmode=exe -buildid=fcYMWp_1J2Xqgzc_Vdga/UpnEUti07R2GzG8dUU3x/MLkSlJVesZhf2kQUaDUU/fcYMWp_1J2Xqgzc_Vdga -extld=gcc /root/.cache/go-build/9f/9f34be2dbcc3f8a62dd6efd6d35be18ecdcbc49e3c8b52b003ecd72b6264e19e-d
$WORK/b001/exe/hello
```


我个人就遇到过由于IaaS供应商提供的系统盘（不允许定制和修改）过小，导致系统盘空间满，使得Go应用构建和执行失败的问题。我们来设置一下GOTMPDIR，看看效果。我们将GOTMPDIR设置为~/.gotmp，生效后，重新build上面的那个helloworld代码：

```
# go build -x hello.go
WORK=/root/.gotmp/go-build452283009
mkdir -p $WORK/b001/
cat >$WORK/b001/importcfg << 'EOF' # internal
... ...
mkdir -p $WORK/b001/exe/
cd .
/root/.bin/go1.10rc2/pkg/tool/linux_amd64/link -o $WORK/b001/exe/a.out -importcfg $WORK/b001/importcfg.link -buildmode=exe -buildid=kO-wBNzMZmfHCKzMDziw/jCGBCt7bcrS5NEN-cR4H/8-du6iTQz8uPH3UC-FtB/kO-wBNzMZmfHCKzMDziw -extld=gcc $WORK/b001/_pkg_.a
/root/.bin/go1.10rc2/pkg/tool/linux_amd64/buildid -w $WORK/b001/exe/a.out # internal
mv $WORK/b001/exe/a.out hello
rm -r $WORK/b001/
```


可以看到，go tool转移到我们设置的GOTMPDIR下构建和执行了。

### 3、通过cache实现增量构建，提高go tools性能

Go语言具有较高的编译性能是Go语言最初设计时就确定下来的目标，Go编译器的性能在[Go 1.4.3版本](http://tonybai.com/2014/11/04/some-changes-in-go-1-4/)达到顶峰，这虽然是得益于其使用C语言实现，但更重要的是其为高性能构建而定义的便于依赖分析的语言构建模型，同时避免了像C/C++那样的重复多次扫描大量头文件的负担。随着[Go自举的实现](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)，使用Go语言实现的go compiler性能有较大下降，但即便这样，其编译速度在主流编程语言中仍然是数一数二的。在经过了[Go 1.6](http://tonybai.com/2016/02/21/some-changes-in-go-1-6/)到[Go1.9](http://tonybai.com/2017/07/14/some-changes-in-go-1-9/)等多个版本对compiler的优化后，go compiler的编译速度已经[恢复到Go 1.4.3 compiler的2/3左右](https://dave.cheney.net/2016/11/19/go-1-8-toolchain-improvements)或是更为接近的水平。在[Go 1.9版本](http://tonybai.com/2017/07/14/some-changes-in-go-1-9/)引入并行编译后，Go team在提升工具性能方面的思路发生了些许变化：不再是一味地进行代码级的性能优化，而是选择通过Cache，重复利用中间结果，实现增量构建，来减少编译构建所用的时间。因此，笔者觉得这个功能是**本次Go 1.10最大的变化之一**。

#### 1) 概述

Go 1.10版本以前，我们经常通过go build -i来加快Go项目源码的编译速度，其原因在于go build -i首次执行时会将目标所依赖的package安装到$GOPATH/pkg下面(.a文件)，这样后续执行go build时，构建过程将不会重新编译目标文件的依赖包，而是直接链接首次执行build -i时安装的依赖包，以实现加速编译！以gocmpp/examples/client为例，第二次构建所需时间仅为首次构建的四分之一左右：

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp/examples/client git:(master) ✗ $time go build -i client.go
go build -i client.go 1.34s user 0.34s system 131% cpu 1.274 total
➜ $GOPATH/src/github.com/bigwhite/gocmpp/examples/client git:(master) ✗ $time go build -i client.go
go build -i client.go 0.38s user 0.16s system 116% cpu 0.465 total
```


只有当目标文件的依赖包的源文件发生变化时（比对源文件的修改时间与.a文件的修改时间作为是否重新编译的判断依据），才会重新编译安装这些依赖包。这有些像[Makefile](http://tonybai.com/2011/05/19/use-command-line-vars-of-make/)的原理：make工具会比较targets文件和prerequisites文件的修改日期，如果prerequisites文件的日期要比targets文件的日期要新，或者target不存在的话，那么，make就会执行后续定义的命令。

不过即便这样，依然至少有两个问题困扰着Go team和广大Gopher：

-
基于时间戳的比对，并不“合理”


当某个目标文件的依赖包的源文件内容并未真正发生变化，但“修改时间”发生变化了，比如：添加了一行，保存了；然后又删除了这一行，保存。在这样的情况下，理想的操作是不需要重新编译安装这个依赖包，但目前的go build -i机制会**重新编译并安装这个依赖包**。 -
**增量构建**并未实现“常态化”

以前版本中，默认的不带命令行参数的go build命令是不会安装依赖包的，因此每次执行go build，都会重新编译一次依赖包的源码，并将结果放入临时目录以供最终链接使用。也就是说最为常用的go build并未实现增量编译，社区需要常态化的“增量编译”，进一步提高效率。

Go 1.10引入cache机制来解决上述问题。从1.10版本开始，go build tool将维护一个package编译结果的缓存以及一些元数据，缓存默认位于操作系统指定的用户缓存目录中，其中数据用于后续构建重用；不仅go build支持“常态化”的增量构建，go test也支持在特定条件下缓存test结果，从而加快执行测试的速度。

#### b) go build with cache

我们先来直观的看看go 1.10 build带来的效果，初始情况cache为空：

以我的一个小项目gocmpp为例，用go 1.10第一次build该项目：

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $time go build
go build 1.22s user 0.43s system 175% cpu 0.939 total
```


我们再来构建一次：

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $time go build
go build 0.12s user 0.16s system 155% cpu 0.182 total
```


0.12s vs. 1.22s！通过cache进行的build将构建时间压缩为原来的1/10！为了弄清楚go build幕后行为，我们清除一下cache(go clean -cache)，再重新build，这次我们通过-v -x 输出详细构建过程：

首次编译的详细输出信息：

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $go build -x -v
WORK=/var/folders/2h/xr2tmnxx6qxc4w4w13m01fsh0000gn/T/go-build735203690
github.com/bigwhite/gocmpp/vendor/golang.org/x/text/encoding/internal/identifier
mkdir -p $WORK/b033/
cat >$WORK/b033/importcfg << 'EOF' # internal
# import config
EOF
cd $(GOPATH)/src/github.com/bigwhite/gocmpp/vendor/golang.org/x/text/encoding/internal/identifier
/Users/tony/.bin/go1.10rc2/pkg/tool/darwin_amd64/compile -o $WORK/b033/_pkg_.a -trimpath $WORK/b033 -p github.com/bigwhite/gocmpp/vendor/golang.org/x/text/encoding/internal/identifier -complete -buildid iZWJNg2FYmWoSCXb640o/iZWJNg2FYmWoSCXb640o -goversion go1.10rc2 -D "" -importcfg $WORK/b033/importcfg -pack -c=4 ./identifier.go ./mib.go
/Users/tony/.bin/go1.10rc2/pkg/tool/darwin_amd64/buildid -w $WORK/b033/_pkg_.a # internal
cp $WORK/b033/_pkg_.a /Users/tony/Library/Caches/go-build/14/14223040d851359359b0e531555a47e22f5dbd4bf434acc136a7c70c1fc3663f-d # internal
github.com/bigwhite/gocmpp/vendor/golang.org/x/text/transform
mkdir -p $WORK/b031/
cat >$WORK/b031/importcfg << 'EOF' # internal
# import config
packagefile bytes=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/bytes.a
packagefile errors=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/errors.a
packagefile io=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/io.a
packagefile unicode/utf8=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/unicode/utf8.a
EOF
.... ....
cd $(GOPATH)/src/github.com/bigwhite/gocmpp
/Users/tony/.bin/go1.10rc2/pkg/tool/darwin_amd64/compile -o $WORK/b001/_pkg_.a -trimpath $WORK/b001 -p github.com/bigwhite/gocmpp -complete -buildid 6LaoHtjkFhandbEhv7zD/6LaoHtjkFhandbEhv7zD -goversion go1.10rc2 -D "" -importcfg $WORK/b001/importcfg -pack -c=4 ./activetest.go ./client.go ./conn.go ./connect.go ./deliver.go ./fwd.go ./packet.go ./receipt.go ./server.go ./submit.go ./terminate.go
/Users/tony/.bin/go1.10rc2/pkg/tool/darwin_amd64/buildid -w $WORK/b001/_pkg_.a # internal
cp $WORK/b001/_pkg_.a /Users/tony/Library/Caches/go-build/e0/e02a5fec0835ca540b62053fdea82589e686e88bf48f18355ed38d41ad19f334-d # internal
```


再次编译的详细输出信息：

```
$go build -x -v
WORK=/var/folders/2h/xr2tmnxx6qxc4w4w13m01fsh0000gn/T/go-build906548554
```


我们来分析一下。首次构建时，我们看到gocmpp依赖的每个包以及自身的包都会被编译，并被copy到/Users/tony/Library/Caches/go-build/下面的某个目录下，包括最终的gocmpp包也是这样。第二次build时，我们看到仅仅输出一行信息，这是因为go compiler在cache中找到了gocmpp包对应的编译好的缓存结果，无需进行实际的编译了。

前面说过，go 1.10 compiler决定是否重新编译包是content based的，而不是依照时间戳比对来决策。我们来修改一个gocmpp包中的文件fwd.go，删除一个空行，再恢复这个空行，保存退出。我们再来编译一下gocmpp:

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $go build -x -v
WORK=/var/folders/2h/xr2tmnxx6qxc4w4w13m01fsh0000gn/T/go-build857409409
```


可以看到go compiler并没有重新编译任何包。如果我们真实改变了fwd.go的内容，比如删除一个空行，保存后再次编译：

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $go build -x -v
WORK=/var/folders/2h/xr2tmnxx6qxc4w4w13m01fsh0000gn/T/go-build437927548
github.com/bigwhite/gocmpp
mkdir -p $WORK/b001/
cat >$WORK/b001/importcfg << 'EOF' # internal
# import config
packagefile bytes=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/bytes.a
packagefile crypto/md5=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/crypto/md5.a
packagefile encoding/binary=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/encoding/binary.a
packagefile errors=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/errors.a
packagefile fmt=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/fmt.a
packagefile github.com/bigwhite/gocmpp/utils=/Users/tony/Test/GoToolsProjects/pkg/darwin_amd64/github.com/bigwhite/gocmpp/utils.a
packagefile io=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/io.a
packagefile log=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/log.a
packagefile net=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/net.a
packagefile os=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/os.a
packagefile strconv=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/strconv.a
packagefile strings=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/strings.a
packagefile sync=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/sync.a
packagefile sync/atomic=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/sync/atomic.a
packagefile time=/Users/tony/.bin/go1.10rc2/pkg/darwin_amd64/time.a
EOF
cd /Users/tony/Test/GoToolsProjects/src/github.com/bigwhite/gocmpp
/Users/tony/.bin/go1.10rc2/pkg/tool/darwin_amd64/compile -o $WORK/b001/_pkg_.a -trimpath $WORK/b001 -p github.com/bigwhite/gocmpp -complete -buildid trn5lvvRTk_UP3LcT5CC/trn5lvvRTk_UP3LcT5CC -goversion go1.10rc2 -D "" -importcfg $WORK/b001/importcfg -pack -c=4 ./activetest.go ./client.go ./conn.go ./connect.go ./deliver.go ./fwd.go ./packet.go ./receipt.go ./server.go ./submit.go ./terminate.go
/Users/tony/.bin/go1.10rc2/pkg/tool/darwin_amd64/buildid -w $WORK/b001/_pkg_.a # internal
cp $WORK/b001/_pkg_.a /Users/tony/Library/Caches/go-build/7a/7a5671578ed30b125257fd16d0f0b8ceaefd0acc3e44f082ffeecea9f1895499-d # internal
```


Go compiler发现了内容的变动，对gocmpp包的变动内容进行了重新compile。

#### c) 缓存目录探索

在增加cache机制时，go tools增加了GOCACHE变量，通过go env GOCACHE查看变量值：

```
$go env GOCACHE
/Users/tony/Library/Caches/go-build
```


如果未重设环境变量GOCACHE，那么默认在Linux上，GOCACHE=”~/.cache/go-build”; 在Mac OS X上，GOCACHE=”/Users/UserName/Library/Caches/go-build”。在 OS X上，我们进入$GOCACHE目录，映入眼帘的是：

```
➜ /Users/tony/Library/Caches/go-build $ls
00/ 18/ 30/ 48/ 60/ 78/ 90/ a7/ bf/ d7/ ef/
01/ 19/ 31/ 49/ 61/ 79/ 91/ a8/ c0/ d8/ f0/
02/ 1a/ 32/ 4a/ 62/ 7a/ 92/ a9/ c1/ d9/ f1/
03/ 1b/ 33/ 4b/ 63/ 7b/ 93/ aa/ c2/ da/ f2/
04/ 1c/ 34/ 4c/ 64/ 7c/ 94/ ab/ c3/ db/ f3/
05/ 1d/ 35/ 4d/ 65/ 7d/ 95/ ac/ c4/ dc/ f4/
06/ 1e/ 36/ 4e/ 66/ 7e/ 96/ ad/ c5/ dd/ f5/
07/ 1f/ 37/ 4f/ 67/ 7f/ 97/ ae/ c6/ de/ f6/
08/ 20/ 38/ 50/ 68/ 80/ 98/ af/ c7/ df/ f7/
09/ 21/ 39/ 51/ 69/ 81/ 99/ b0/ c8/ e0/ f8/
0a/ 22/ 3a/ 52/ 6a/ 82/ 9a/ b1/ c9/ e1/ f9/
0b/ 23/ 3b/ 53/ 6b/ 83/ 9b/ b2/ ca/ e2/ fa/
0c/ 24/ 3c/ 54/ 6c/ 84/ 9c/ b3/ cb/ e3/ fb/
0d/ 25/ 3d/ 55/ 6d/ 85/ 9d/ b4/ cc/ e4/ fc/
0e/ 26/ 3e/ 56/ 6e/ 86/ 9e/ b5/ cd/ e5/ fd/
0f/ 27/ 3f/ 57/ 6f/ 87/ 9f/ b6/ ce/ e6/ fe/
10/ 28/ 40/ 58/ 70/ 88/ README b7/ cf/ e7/ ff/
11/ 29/ 41/ 59/ 71/ 89/ a0/ b8/ d0/ e8/ log.txt
12/ 2a/ 42/ 5a/ 72/ 8a/ a1/ b9/ d1/ e9/ trim.txt
13/ 2b/ 43/ 5b/ 73/ 8b/ a2/ ba/ d2/ ea/
14/ 2c/ 44/ 5c/ 74/ 8c/ a3/ bb/ d3/ eb/
15/ 2d/ 45/ 5d/ 75/ 8d/ a4/ bc/ d4/ ec/
16/ 2e/ 46/ 5e/ 76/ 8e/ a5/ bd/ d5/ ed/
17/ 2f/ 47/ 5f/ 77/ 8f/ a6/ be/ d6/ ee/
```


熟悉git原理的朋友一定觉得这个目录组织结构似曾相识！没错，在每个git项目的./git/object目录下，我们也能看到下面的结果：

```
.git/objects git:(master) $ls
00/ 0c/ 18/ 24/ 30/ 3c/ 48/ 54/ 60/ 6c/ 78/ 84/ 90/ 9c/ a8/ b4/ c0/ cc/ d8/ e4/ f0/ fc/
01/ 0d/ 19/ 25/ 31/ 3d/ 49/ 55/ 61/ 6d/ 79/ 85/ 91/ 9d/ a9/ b5/ c1/ cd/ d9/ e5/ f1/ fd/
02/ 0e/ 1a/ 26/ 32/ 3e/ 4a/ 56/ 62/ 6e/ 7a/ 86/ 92/ 9e/ aa/ b6/ c2/ ce/ da/ e6/ f2/ fe/
03/ 0f/ 1b/ 27/ 33/ 3f/ 4b/ 57/ 63/ 6f/ 7b/ 87/ 93/ 9f/ ab/ b7/ c3/ cf/ db/ e7/ f3/ ff/
04/ 10/ 1c/ 28/ 34/ 40/ 4c/ 58/ 64/ 70/ 7c/ 88/ 94/ a0/ ac/ b8/ c4/ d0/ dc/ e8/ f4/ info/
05/ 11/ 1d/ 29/ 35/ 41/ 4d/ 59/ 65/ 71/ 7d/ 89/ 95/ a1/ ad/ b9/ c5/ d1/ dd/ e9/ f5/ pack/
06/ 12/ 1e/ 2a/ 36/ 42/ 4e/ 5a/ 66/ 72/ 7e/ 8a/ 96/ a2/ ae/ ba/ c6/ d2/ de/ ea/ f6/
07/ 13/ 1f/ 2b/ 37/ 43/ 4f/ 5b/ 67/ 73/ 7f/ 8b/ 97/ a3/ af/ bb/ c7/ d3/ df/ eb/ f7/
08/ 14/ 20/ 2c/ 38/ 44/ 50/ 5c/ 68/ 74/ 80/ 8c/ 98/ a4/ b0/ bc/ c8/ d4/ e0/ ec/ f8/
09/ 15/ 21/ 2d/ 39/ 45/ 51/ 5d/ 69/ 75/ 81/ 8d/ 99/ a5/ b1/ bd/ c9/ d5/ e1/ ed/ f9/
0a/ 16/ 22/ 2e/ 3a/ 46/ 52/ 5e/ 6a/ 76/ 82/ 8e/ 9a/ a6/ b2/ be/ ca/ d6/ e2/ ee/ fa/
0b/ 17/ 23/ 2f/ 3b/ 47/ 53/ 5f/ 6b/ 77/ 83/ 8f/ 9b/ a7/ b3/ bf/ cb/ d7/ e3/ ef/ fb/
```


这里猜测go 1.10使用的应该是与git一类内容摘要算法以及组织存储模式。在前面的build详细输出中，我们找到这一行：

```
cp $WORK/b001/_pkg_.a /Users/tony/Library/Caches/go-build/7a/7a5671578ed30b125257fd16d0f0b8ceaefd0acc3e44f082ffeecea9f1895499-d # internal
```


这行命令是将gocmpp包复制到cache下，我们到cache的7a目录下一查究竟：

```
➜ /Users/tony/Library/Caches/go-build/7a $tree
.
└── 7a5671578ed30b125257fd16d0f0b8ceaefd0acc3e44f082ffeecea9f1895499-d
0 directories, 1 file
```


我们用nm命令查看一下该文件：

```
$go tool nm 7a5671578ed30b125257fd16d0f0b8ceaefd0acc3e44f082ffeecea9f1895499-d|more
1c319 T %22%22.(*Client).Connect
2e279 T %22%22.(*Client).Connect.func1
3fc22 R %22%22.(*Client).Connect.func1·f
1c79f T %22%22.(*Client).Disconnect
1c979 T %22%22.(*Client).RecvAndUnpackPkt
1c807 T %22%22.(*Client).SendReqPkt
1c8e2 T %22%22.(*Client).SendRspPkt
1e417 T %22%22.(*Cmpp2ConnRspPkt).Pack
... ...
```


这个文件的确就是gocmpp.a文件。通过比对该文件size与go install后的文件size也可以证实这一点：

```
➜ /Users/tony/Library/Caches/go-build/7a $
-rw-r--r-- 1 tony staff 445856 Feb 15 22:34 7a5671578ed30b125257fd16d0f0b8ceaefd0acc3e44f082ffeecea9f1895499-d
vs.
➜ $GOPATH/pkg/darwin_amd64/github.com/bigwhite $ll
-rw-r--r-- 1 tony staff 445856 Feb 15 23:27 gocmpp.a
```


也就是说go compiler将编译后的package的.a文件求取摘要值后，将.a文件存储在$GOCACHE下的某个目录中，这个目录名即为摘要值的前两位（比如”7a”），.a文件名字被换成其摘要值，以便后续查找并做比对。

cache目录下还有一个重要文件：log.txt，这个文件是用来记录缓存管理日志的，其内容格式如下：

```
//log.txt
... ...
1518705271 get 7533a063cd8c37888b19674bf4a4bb7e25fa422041082566530d58538c031516
1518705271 miss b6b9f996fbd14e4fd43f72dc4f9082946cddd0d61d6c6143c88502c8a4001666
1518705271 put b6b9f996fbd14e4fd43f72dc4f9082946cddd0d61d6c6143c88502c8a4001666 7a5671578ed30b125257fd16d0f0b8ceaefd0acc3e44f082ffeecea9f1895499 445856
1518705271 put f5a641ca081a0d2d794b0b54aa9f89014dbb6ff8d14d26543846e1676eca4c21 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 0
1518708456 get 899589360d856265a84825dbeb8d283ca84e12f154eefc12ba84870af13e1f63
1518708456 get 8a7fcd97a5f36bd00ef084856c63e4e2facedce33d19a5b557cc67f219787661
```


该日志文件更多的用途是帮助Russ Cox对其开发的cache进行调试和问题诊断的。当然，如果您对于cache的机制原理也很精通，那么也可以让log.txt帮你诊断涉及cache的问题。

#### d) go test with cache

go 1.10版的go test也会维护一个cache，这个cache缓存了go test执行的测试结果。同时在go 1.10中，go test被分为两种执行模式：local directory mode和package list mode，在不同模式下，cache机制的介入是不同的。

local directory mode，即go test以整个当前目录作为隐式参数的执行模式，比如在某个目录下执行”go test”，go test后面不带任何显式的package列表参数（当然可以带着其他命令行flag参数，如-v）。在这种模式下，cache机制不会介入，go test的执行过程与go 1.10版本之前没有两样。还是以gocmpp这个项目为例，我们以local directory mode执行go test：

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $go test
PASS
ok github.com/bigwhite/gocmpp 0.011s
```


如果缓存机制介入，输出的test结果中会出现cached字样，显然上面的go test执行过程并没有使用test cache。

package list mode，即go test后面显式传入了package列表，比如：go test math、go test .、go test ./…等，在这种模式下，test cache机制会介入。我们连续两次在gocmpp目录下执行go test .：

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $go test .
ok github.com/bigwhite/gocmpp 0.011s
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $go test .
ok github.com/bigwhite/gocmpp (cached)
```


如果你此时想进一步看看go test执行的详细输出，你可以会执行go test -v .：

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $go test -v .
=== RUN TestTypeString
--- PASS: TestTypeString (0.00s)
=== RUN TestCommandIdString
--- PASS: TestCommandIdString (0.00s)
=== RUN TestOpError
--- PASS: TestOpError (0.00s)
... ...
=== RUN TestCmppTerminateRspPktPack
--- PASS: TestCmppTerminateRspPktPack (0.00s)
=== RUN TestCmppTerminateRspUnpack
--- PASS: TestCmppTerminateRspUnpack (0.00s)
PASS
ok github.com/bigwhite/gocmpp 0.017s
```


你会发现，这次go test并没有使用cache。如果你再执行一次go test -v .：

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $go test -v .
=== RUN TestTypeString
--- PASS: TestTypeString (0.00s)
=== RUN TestCommandIdString
--- PASS: TestCommandIdString (0.00s)
=== RUN TestOpError
--- PASS: TestOpError (0.00s)
... ...
=== RUN TestCmppTerminateRspPktPack
--- PASS: TestCmppTerminateRspPktPack (0.00s)
=== RUN TestCmppTerminateRspUnpack
--- PASS: TestCmppTerminateRspUnpack (0.00s)
PASS
ok github.com/bigwhite/gocmpp (cached)
```


test cache又起了作用。似乎cache对于go test .和go test -v .是独立的。没错，release note中给出的go test cache的介入条件如下：

- 本次测试的执行程序以及命令行（及参数）与之前的一次test运行匹配；（这就能解释为何go test -v .没有使用go test .执行的cache了）；
- 上次测试执行时的文件和环境变量在本次没有发生变化；
- 测试结果是成功的；
- 以package list node运行测试；
- go test的命令行参数使用”-cpu, -list, -parallel, -run, -short和 -v”的一个子集时

就像前面我们看到的，cache介入的go test结果不会显示test消耗的时间，而是以(cached)字样替代。

绝大多数Gopher都是喜欢test with cache的，但总有一些情况，cache是不受欢迎的。其实前面的条件已经明确告知gopher们什么条件下test cache是可以不介入的。**一个惯用的关闭test cache的方法**是使用-count=1：

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $go test -count=1 -v .
=== RUN TestTypeString
--- PASS: TestTypeString (0.00s)
=== RUN TestCommandIdString
--- PASS: TestCommandIdString (0.00s)
=== RUN TestOpError
--- PASS: TestOpError (0.00s)
... ...
=== RUN TestCmppTerminateRspPktPack
--- PASS: TestCmppTerminateRspPktPack (0.00s)
=== RUN TestCmppTerminateRspUnpack
--- PASS: TestCmppTerminateRspUnpack (0.00s)
PASS
ok github.com/bigwhite/gocmpp 0.012s
```


go 1.10中的go test与之前版本还有一个不同，那就是go test在真正执行test前会自动对被测试的包执行go vet，但这个vet只会识别那些最为明显的问题。并且一旦发现问题，go test将会视这些问题与build error同级别，阻断test的执行，并让其出现在test failure中。当然gopher可以通过go test -vet=off关闭这个前置于测试的vet检查。

### 4. pprof

go tool pprof做了一个较大的改变：增加了Web UI，以后可以和go trace一起通过图形化的方法对Go程序进行调优了。可视化的pprof使用起来十分简单，我们以gocmpp为例，试用一下go 1.10的pprof，首先我们生成cpu profile文件：

```
➜ $GOPATH/src/github.com/bigwhite/gocmpp git:(master) ✗ $go test -run=^$ -bench=. -cpuprofile=profile.out
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/gocmpp
BenchmarkRecvAndUnpackPkt-4 1000000 1534 ns/op
BenchmarkCmppConnReqPktPack-4 1000000 1398 ns/op
BenchmarkCmppConnReqPktUnpack-4 3000000 450 ns/op
BenchmarkCmpp2DeliverReqPktPack-4 1000000 1156 ns/op
BenchmarkCmpp2DeliverReqPktUnpack-4 3000000 567 ns/op
BenchmarkCmpp3DeliverReqPktPack-4 1000000 1173 ns/op
BenchmarkCmpp3DeliverReqPktUnpack-4 3000000 465 ns/op
BenchmarkCmpp2FwdReqPktPack-4 1000000 2079 ns/op
BenchmarkCmpp2FwdReqPktUnpack-4 1000000 1276 ns/op
BenchmarkCmpp3FwdReqPktPack-4 1000000 2507 ns/op
BenchmarkCmpp3FwdReqPktUnpack-4 1000000 1286 ns/op
BenchmarkCmpp2SubmitReqPktPack-4 1000000 1845 ns/op
BenchmarkCmpp2SubmitReqPktUnpack-4 1000000 1251 ns/op
BenchmarkCmpp3SubmitReqPktPack-4 1000000 1863 ns/op
BenchmarkCmpp3SubmitReqPktUnpack-4 2000000 656 ns/op
PASS
ok github.com/bigwhite/gocmpp 26.621s
```


启动pprof web ui：

```
$go tool pprof -http=:8080 profile.out
```


pprof会自动打开默认浏览器，进入下面页面：

![img{512x368}](../../assets/e75c2238855049b6.png)


在view菜单中，我们可以看到”top”、”graph”、”peek”、”source”和”disassemble”几个选项，这些选项可以帮助你在各种视图间切换，默认初始为graph view。不过目前view菜单中并没有”Flame Graph(火焰图)”选项，要想使用Flame Graph，我们需要使用原生的pprof工具，该工具可通过go get -u github.com/google/pprof获取，install后原生pprof将出现在$GOROOT/bin下面。

使用原生pprof启动Web UI：

```
$pprof -http=:8080 profile.out
```


原生pprof同样会自动打开浏览器，进入下面页面：

![img{512x368}](../../assets/0cbd9d4eafa31802.png)


原生的pprof的web ui看起来比go 1.10 tool中的pprof更为精致，且最大的不同在于VIEW菜单下出现了”Flame Graph”菜单项！我们点击该菜单项，一幅Flame Graph便呈现在眼前：

![img{512x368}](../../assets/873f74ea40f412c2.png)


关于如何做火焰图分析不是这里的主要任务，请各位Gopher自行脑补。更多关于Go性能调优问题，可以参考[Go官方提供的诊断手册](https://tip.golang.org/doc/diagnostics.html)。

## 四、标准库

和之前的每次Go版本发布一样，标准库的改变是多且细碎的，这里不能一一举例说明。并且很多涉“专业领域”的包，比如加解密，需要一定专业深度，因此这里仅列举几个“通用”的变化^0^。

### 1、strings.Builder

strings包增加一个新的类型：Builder，用于在“拼字符串”场景中替代bytes.Buffer，由于使用了一些unsafe包的黑科技，在用户调用Builder.String()返回最终拼成的字符串时，避免了一些重复的、不必要的内存copy，提升了处理性能，优化了内存分配。我们用一个demo来看看这种场景下Builder的优势：

```
//go1.10-examples/stdlib/stringsbuilder/builer.go
package builder
import (
"bytes"
"strings"
)
type BuilderByBytesBuffer struct {
b bytes.Buffer
}
func (b *BuilderByBytesBuffer) WriteString(s string) error {
_, err := b.b.WriteString(s)
return err
}
func (b *BuilderByBytesBuffer) String() string{
return b.b.String()
}
type BuilderByStringsBuilder struct {
b strings.Builder
}
func (b *BuilderByStringsBuilder) WriteString(s string) error {
_, err := b.b.WriteString(s)
return err
}
func (b *BuilderByStringsBuilder) String() string{
return b.b.String()
}
```


针对上面代码中的BuilderByBytesBuffer和BuilderByStringsBuilder进行Benchmark的Test源文件如下：

```
//go1.10-examples/stdlib/stringsbuilder/builer_test.go
package builder
import "testing"
func BenchmarkBuildStringWithBytesBuffer(b *testing.B) {
var builder BuilderByBytesBuffer
for i := 0; i < b.N; i++ {
builder.WriteString("Hello, ")
builder.WriteString("Go")
builder.WriteString("-1.10")
_ = builder.String()
}
}
func BenchmarkBuildStringWithStringsBuilder(b *testing.B) {
var builder BuilderByStringsBuilder
for i := 0; i < b.N; i++ {
builder.WriteString("Hello, ")
builder.WriteString("Go")
builder.WriteString("-1.10")
_ = builder.String()
}
}
```


执行该Benchmark，查看结果：

```
$go test -bench . -benchmem
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/experiments/go1.10-examples/stdlib/stringsbuilder
BenchmarkBuildStringWithBytesBuffer-4 100000 108471 ns/op 704073 B/op 1 allocs/op
BenchmarkBuildStringWithStringsBuilder-4 20000000 122 ns/op 80 B/op 0 allocs/op
PASS
ok github.com/bigwhite/experiments/go1.10-examples/stdlib/stringsbuilder 13.616s
```


可以看到StringsBuilder在处理速度和分配优化上都全面强于bytes.Buffer，真实的差距就在Builder.String这个方法上。

### 2、bytes包

bytes包的几个方法Fields, FieldsFunc, Split和SplitAfter在底层实现上有变化，使得外部展现的行为有所变化，我们通过一个例子直观的感受一下：

```
// go1.10-examples/stdlib/bytessplit/main.go
package main
import (
"bytes"
"fmt"
)
// 来自github.com/campoy/gotalks/blob/master/go1.10/bytes/fields.go
func desc(b []byte) string {
return fmt.Sprintf("len: %2d | cap: %2d | %q\n", len(b), cap(b), b)
}
func main() {
text := []byte("Hello, Go1.10 is coming!")
fmt.Printf("text: %s", desc(text))
subslices := bytes.Split(text, []byte(" "))
fmt.Printf("subslice 0: %s", desc(subslices[0]))
fmt.Printf("subslice 1: %s", desc(subslices[1]))
fmt.Printf("subslice 2: %s", desc(subslices[2]))
fmt.Printf("subslice 3: %s", desc(subslices[3]))
}
```


我们先用Go 1.9.2编译运行一下该demo:

```
$go run main.go
text: len: 24 | cap: 32 | "Hello, Go1.10 is coming!"
subslice 0: len: 6 | cap: 32 | "Hello,"
subslice 1: len: 6 | cap: 25 | "Go1.10"
subslice 2: len: 2 | cap: 18 | "is"
subslice 3: len: 7 | cap: 15 | "coming!"
```


我们再用go 1.10rc2运行一下该demo：

```
$go run main.go
text: len: 24 | cap: 32 | "Hello, Go1.10 is coming!"
subslice 0: len: 6 | cap: 6 | "Hello,"
subslice 1: len: 6 | cap: 6 | "Go1.10"
subslice 2: len: 2 | cap: 2 | "is"
subslice 3: len: 7 | cap: 15 | "coming!"
```


对比两次输出结果中cap那一列，你会发现go 1.10输出的结果中的**每个subslice(除了最后一个)的len与cap值都是相等的**，而不是将原slice剩下所有cap都作为subslice的cap。这个行为的改变是出于安全的考虑，防止共享一个underlying slice的各个subslice的修改对相邻的subslice造成影响，因此限制它们的capacity。

在Fields, FieldsFunc, Split和SplitAfter这几个方法的具体实现上，Go 1.10使用了我们平时并不经常使用的”[Full slice expression](https://golang.org/ref/spec#Slice_expressions)“，即：a[low, high, max]来指定subslice的cap。

## 五、性能

对于静态编译类型语言Go来说，性能也一直是其重点关注的设计目标，这两年来发布的Go版本，几乎每个都给Gopher们带来惊喜。谈到Go性能，Gopher们一般关心的有如下这么几个方面：

### 1、编译性能

Go 1.10的编译性能正如我们前面所说的那样，最大的改变在于cache机制的实现。事实证明cache机制的使用在日常开发过程中，会很大程度上提升你的工作效率，越是规模较大的项目越是如此。

### 2、目标代码的性能

这些年Go team在不断优化编译器生成的目标代码的性能，比如在[Go 1.7版本](http://tonybai.com/2016/06/21/some-changes-in-go-1-7/)中引入ssa后端。Go 1.10延续着对目标代码生成的进一步优化，虽说动作远不如引入ssa这么大。

### 3、GC性能

GC的性能一直是广大Gopher密切关注的事情，Go 1.10在减少内存分配延迟以及GC运行时的负担两个方面做了许多工作，但从整体上来看，Go 1.10并没有引入传说中的[TOC(Transaction Oritented Collector)](https://groups.google.com/forum/#!topic/golang-dev/WcZaqTE51ZU)，因此宏观上来看，GC变化不是很大。Twitter上的GC性能测试“专家”[Brian Hatfield](https://twitter.com/brianhatfield)在对Go 1.10rc1的[GC测试](http://tonybai.com/2017/07/04/setup-go-runtime-metrics-for-yourself/)后，也表示与Go 1.9相比，变化不是很显著。

## 六、小结

Go 1.10版本又是一个Go team和Gopher社区共同努力的结果，让全世界Gopher都对Go保持着极大的热情和期望。当然Go 1.10中的变化还有许多许多，诸如：

- 对Unicode规范的支持升级到
[10.0](http://www.unicode.org/versions/Unicode10.0.0/)； - 在不同的平台上，Assembler支持更多高性能的指令；
- plugin支持darwin/amd64等；
- gofmt、go doc在输出格式上进一步优化和提升gopher开发者体验；
- cgo支持直接传递go string到C代码中;

… …

很多很多！这里限于篇幅原因，不能一一详解了。通读一遍[Go 1.10 Release Note](https://golang.org/doc/go1.10)是每个Gopher都应该做的。

以上验证在mac OS X, go 1.10rc2上测试，demo源码可以在[这里下载](https://github.com/bigwhite/experiments/tree/master/go1.10-examples)。

## 七、参考资料

[Go 1.10 Release Notes](https://golang.org/doc/go1.10)[The State of Go by campoy](https://speakerdeck.com/campoy/the-state-of-go-1-dot-10)[Go 1.10](https://blog.gopheracademy.com/advent-2017/go-1.10/)[pprof user interface](https://rakyll.org/pprof-ui/)[cmd/go content-based staleness submitted](https://groups.google.com/forum/#!topic/golang-dev/EZtZsJG35ZM)[Go 1.10 cmd/go: build cache, test cache, go install, go vet, test vet](https://groups.google.com/forum/#!topic/golang-dev/qfa3mHN4ZPA)

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：http://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/71dbd0d64d261ba9.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

你好, strings.Builder 和 bytes.Buffer 的 String 方法, 差距确实很大，但拼接的过程中，

WriteString等方法，测试bytes.Buffer效率更高，说 strings.Builder全面强于bytes.Buffer不恰当吧

代码：

package main

import (

“bytes”

“strings”

“testing”

)

var (

by = “123456789123456789123456789123456789″

)

func BenchmarkBuffer(b *testing.B) {

buf := &bytes.Buffer{}

for i := 0; i < b.N; i++ {

buf.WriteString(by)

buf.WriteString("123")

// buf.String()

}

}

func BenchmarkBuilder(b *testing.B) {

buf := &strings.Builder{}

for i := 0; i < b.N; i++ {

buf.WriteString(by)

buf.WriteString("123")

// buf.String()

}

}

输出:

$ go test -benchmem -bench=.*

goos: darwin

goarch: amd64

BenchmarkBuffer-4 20000000 70.0 ns/op 83 B/op 0 allocs/op

BenchmarkBuilder-4 30000000 155 ns/op 205 B/op 0 allocs/op

PASS

ok _/Users/apple/go/playground/benchmark 6.463s

不过 bytes.Buffer 的String方法确实很耗时, 可达到数秒…….

嗯，差距其实就在String方法上。