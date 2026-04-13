---
title: Go语言随机测试工具go-fuzz
url: https://tonybai.com/2015/12/08/go-fuzz-intro/
published: '2015-12-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言随机测试工具go-fuzz

在[Go 1.5](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)发布时，前Intel Black Belt级工程师，现Google工程师Dmitry Vyukov同时发布了Go语言随机测试工具[go-fuzz](https://github.com/dvyukov/go-fuzz)。在 [GopherCon2015](https://github.com/gophercon/2015-talks)大会上，Dmitry Vyukov在其名为“[Go Dynamic Tools]”的presentation中着重介绍了[go-fuzz](https://github.com/dvyukov/go-fuzz/blob/master/slides/go-fuzz.slide)。

go-fuzz是一款随机测试(Random testing)工具。对于随机测试想必很多人都比较陌生，我也不例外。至少在接触go-fuzz之前，我从未在[golang](http://tonybai.com/tag/go)或其他编程语言中使用过类似的测试工具(c/c++开发者可以使用[afl-fuzz](http://lcamtuf.coredump.cx/afl/))。按照[维基百科](https://en.wikipedia.org/wiki/Fuzz_testing)的说法：随机测试就是指半自动或自动地为程序提供非法的、非预期、随机的数据，并监控程序在这些输入数据 下的crash、内置断言、内存泄露等情况。随机测试的研究始于1988年的[Barton Miller](http://www.cs.wisc.edu/~bart/fuzz)，到目前为止已经有许多理论支撑，不过这里不会涉及，有兴趣的、想深入的朋友可以跟随维基百科中的链接自行学习。

在开始go-fuzz之前，我们需要认识到随机测试的位置和意义：

* 首先它是软件测试技术的一个重要分支，与单元测试等互为补充；

* 其次随机测试不是什么银弹，它有其适用的范围。随机测试最适合那些处理复杂输入数据的程序，比如文件格式解析、网络协议解析、人机交互界面入口等。

* 最后，并非所有编程语言都有类似的工具支撑，gopher很幸运，Dmitry Vyukov为我们带来了go-fuzz。

接下来就让我们回到go-fuzz这个正题上来。

### 一、Why go-fuzz

go-fuzz之所以吸引眼球，源于Dmitry Vyukov在使用go-fuzz对go标准库以及其他第三方开源库进行测试后的“惊人的战果”。Dmitry在其slide中展示了这些战果：

```
60 tests
137 bugs in std lib (70 fixed)
165 elsewhere (47 in gccgo, 30 in golang.org/x, 42 in freetype-go, protobuf, http2, bson)
```


Dmitry Vyukov的go-fuzz实际上也是基于前面提到的[afl-fuzz](http://lcamtuf.coredump.cx/afl/)的逻辑 的基础上设计和实现的。不同的是在使用的时候，afl-fuzz对于每个input case都会fork一个process，而go-fuzz则是通过将input case中的data传给一个Fuzz函数：

```
func Fuzz(data []byte) int
```


这样就无需反复重启程序。

go-fuzz进一步完善了go开发测试工具集，很多一线公司(比如cloudflare)已经开始使用go-fuzz来测试自己的产品，提高产品质量了。

### 二、原理

Dmitry在其slide中将go-fuzz的工作流程归纳如下：

```
-> 生成随机数据
-> 输入给程序
-> 观察是否有crash
-> 如果发现crash，则获益
之后开发者根据crash的结果，尝试fix bug，并
添加针对这个bug的单元测试case。
```


go-fuzz一旦运行起来，将会是一个infinite loop(一种遗传算法)，该loop的伪代码在slide也有给出：

```
Instrument program for code coverage
Collect initial corpus of inputs //收集初始输入数据语料(位于workdir的corpus目录下)
for {
//从corpus中读取语料并随机变化
Randomly mutate an input from the corpus
//执行Fuzz，收集覆盖范围
Execute and collect coverage
//如果输入数据提供了新的coverage，则将该数据存入语料库(corpus)
If the input gives new coverage, add it to corpus
}
```


go-fuzz内部实现了多种对初始语料库中输入数据的mutation策略：

```
* Insert/remove/duplicate/copy a random range of random bytes.
* Bit flip.
* Swap 2 bytes.
* Set a byte to a random value.
* Add/subtract from a byte/uint16/uint32/uint64 (le/be).
* Replace a byte/uint16/uint32 with an interesting value (le/be).
* Replace an ascii digit/number with another digit/number.
* Splice another input.
* Insert a part of another input.
* Insert a string/int literal.
* Replace with string/int literal.
```


### 三、使用方法

#### 1、安装go-fuzz

使用go-fuzz需要安装两个重要工具：go-fuzz-build和go-fuzz，通过标准go get就可以安装它们：

```
$ go get github.com/dvyukov/go-fuzz/go-fuzz
$ go get github.com/dvyukov/go-fuzz/go-fuzz-build
```


对于国内用户而言，由于go-fuzz并未使用go 1.5引入的[vendor机制](http://tonybai.com/2015/07/31/understand-go15-vendor/)， 而其依赖的一些包却在墙外，因此可能会遇到些麻烦。

go get自动安装两个工具到$GOROOT/bin或$GOPATH/bin，因此你需要确保你的Path环境变量下包含了这两个路径。

#### 2、带有fuzz test的项目组织

假设我们的待测试的go包名为foo，路径为$GOPATH/src/github.com/bigwhite/fuzzexamples/foo。为了应用go- fuzz，我们一般会在foo下创建fuzz.go源文件，其内容模板如下：

```
// +build gofuzz
package foo
func Fuzz(data []byte) int {
... ...
}
```


go-fuzz在构建用于执行fuzz test的驱动binary文件时，会搜索带有”+build gofuzz” directive的源文件以及其中的Fuzz函数。如果foo包下没有该文件，你在执行go-fuzz-build时，会得到类似如下的错误日志：

```
$go-fuzz-build github.com/bigwhite/fuzzexamples/foo
failed to execute go build: exit status 2
# go-fuzz-main
/var/folders/2h/xr2tmnxx6qxc4w4w13m01fsh0000gn/T/go-fuzz-build641745751/src/go-fuzz-main/main.go:10: undefined: foo.Fuzz
```


有些时候待测试包内功能很多，一个Fuzz函数不够，我们可以参考go-fuzz中example中的目录组织形式来应对：

```
github.com/bigwhite/fuzzexamples/foo/fuzztest]$tree
.
├── fuzz1
│ ├── corpus
│ ├── fuzz.go
│ └── gen
│ └── main.go
└── fuzz2
├── corpus
├── fuzz.go
└── gen
└── main.go
... ...
```


这其中的fuzz1、fuzz2…. fuzzN各自为一个go-fuzz单元，如果要应用go-fuzz，则可像下面这样执行：

```
$ cd fuzz1
$ go-fuzz-build github.com/bigwhite/fuzzexamples/foo/fuzztest/fuzz1
$ go-fuzz -bin=./foo-fuzz.zip -workdir=./
.. ...
$ cd fuzz2
$ go-fuzz-build github.com/bigwhite/fuzzexamples/foo/fuzztest/fuzz2
$ go-fuzz -bin=./foo-fuzz.zip -workdir=./
```


每个go-fuzz单元下有一套”固定”目录组合：

```
├── fuzz1
│ ├── corpus
│ ├── fuzz.go
│ └── gen
│ └── main.go
```


corpus为存放输入数据语料的目录，在go-fuzz执行之前，可放入初始语料；

fuzz.go为包含Fuzz函数的源码文件；

gen目录中包含手工生成初始语料的main.go代码。

在后续的示例中，我们会展示细节。

#### 3、go-fuzz-build

go-fuzz-build会根据Fuzz函数构建一个用于go-fuzz执行的zip包(PACKAGENAME-fuzz.zip)，包里包含了用途不同的三 个文件：

```
-rw-r--r-- 1 tony staff 3902136 12 31 1979 cover.exe
-rw-r--r-- 1 tony staff 3211816 12 31 1979 metadata
-rw-r--r-- 1 tony staff 5031496 12 31 1979 sonar.exe
```


按照作者slide中的说法，各个二进制程序的功能如下：

cover.exe – coverage instrumented binary

sonar.exe – sonar instrumented binary

metadata – coverage and sonar metadata, int and string literals

不过对于使用者来说，我们不必过于关心它们，点到为止。

#### 4、执行go-fuzz

一旦生成了foo-fuzz.zip，我们就可以执行针对fuzz1的fuzz test。

```
$ cd fuzz1
$ go-fuzz -bin=./foo-fuzz.zip -workdir=./
2015/12/08 17:51:48 slaves: 4, corpus: 8 (1s ago), crashers: 0, restarts: 1/0, execs: 0 (0/sec), cover: 0, uptime: 3s
2015/12/08 17:51:51 slaves: 4, corpus: 9 (2s ago), crashers: 0, restarts: 1/3851, execs: 11553 (1924/sec), cover: 143, uptime: 6s
2015/12/08 17:51:54 slaves: 4, corpus: 9 (5s ago), crashers: 0, restarts: 1/3979, execs: 47756 (5305/sec), cover: 143, uptime: 9s
... ...
```


如果corpus中没有初始语料数据，那么go-fuzz也会自行生成相关数据传递给Fuzz函数，并且采用遗传算法，不断基于corpus中的语料生成新的输入语料。go-fuzz作者建议corpus初始时放入的语料越多越好，而且要有足够的多样性，这样基于这些初始语料施展遗传算法，效果才会更加。go-fuzz会将一些语料持久化成文件放在corpus中，以供下次restart使用。

前面说过，go-fuzz是一个infinite loop，上面的测试需要手工停下来。go-fuzz会在workdir中创建另外两个目录：crashers和suppressions。顾名思义，crashers中存放的是代码crash时的相关数据，包括引起crash的case的输入二进制数据、输入的数据的字符串形式(xxx.quoted)以及基于这个数据的输出数据(xxx.output)。suppressions中保存着crash时的stack trace信息。

### 四、一个简单示例

[gocmpp](https://github.com/bigwhite/gocmpp)是一个cmpp协议库的go实现，这里打算用其中的unpack做一个最简单的fuzz test demo。

gocmpp中的每种协议包都实现了Packer接口，其中的Unpack尤其适合fuzz test。由于协议包众多，我们在gocmpp下专门建立fuzztest目录，用于存放fuzz test的代码，将各个协议包的fuzz test分到各个子目录中：

```
github.com/bigwhite/gocmpp/fuzztest]$tree
.
├── fwd
│ ├── corpus
│ │ └── 0
│ ├── fuzz.go
│ └── gen
│ └── main.go
└── submit
├── corpus
│ ├── 0
├── fuzz.go
└── gen
└── main.go
```


先说说每个fuzz test单元(比如fwd或submit)下的gen/main.go，这是一个用于生成初始语料的可执行程序，我们以submit/gen/main.go为例：

```
package main
import (
"github.com/dvyukov/go-fuzz/gen"
)
func main() {
data := []byte{
0x00, 0x00, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x01, 0x74, 0x65, 0x73, 0x74, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x02, 0x31, 0x33, 0x35, 0x30, 0x30, 0x30, 0x30, 0x32, 0x36, 0x39, 0x36, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x39, 0x30, 0x30, 0x30, 0x30,
0x31, 0x30, 0x32, 0x31, 0x30, 0x00, 0x00, 0x00, 0x00, 0x31, 0x35, 0x31, 0x31, 0x30, 0x35, 0x31,
0x33, 0x31, 0x35, 0x35, 0x35, 0x31, 0x30, 0x31, 0x2b, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x39, 0x30, 0x30, 0x30, 0x30,
0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x01, 0x31, 0x33, 0x35, 0x30, 0x30, 0x30, 0x30, 0x32, 0x36, 0x39, 0x36, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1e, 0x6d, 0x4b, 0x8b, 0xd5, 0x00, 0x67, 0x00, 0x6f, 0x00,
0x63, 0x00, 0x6d, 0x00, 0x70, 0x00, 0x70, 0x00, 0x20, 0x00, 0x73, 0x00, 0x75, 0x00, 0x62, 0x00,
0x6d, 0x00, 0x69, 0x00, 0x74, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
}
gen.Emit(data, nil, true)
}
```


在这个main.go中，我们借用submit包的单元测试中的数据作为fuzz test的初始语料数据，通过go-fuzz提供的gen包将数据输出到文件中：

```
$cd submit/gen
$go run main.go -out ../corpus/
$ll ../corpus/
total 8
drwxr-xr-x 3 tony staff 102 12 7 22:00 ./
drwxr-xr-x 5 tony staff 170 12 7 21:42 ../
-rw-r--r-- 1 tony staff 181 12 7 22:00 0
```


该程序在corpus下生成了一个文件“0”，作为submit fuzz test的初始语料。

接下来我们看看submit/fuzz.go：

```
// +build gofuzz
package cmppfuzz
import (
"github.com/bigwhite/gocmpp"
)
func Fuzz(data []byte) int {
p := &cmpp.Cmpp2SubmitReqPkt{}
if err := p.Unpack(data); err != nil {
return 0
}
return 1
}
```


这是一个“最简单”的Fuzz函数实现了，根据作者对Fuzz的规约，Fuzz的返回值是有重要含义的：

```
如果此次输入的数据在某种程度上是很有意义的，go-fuzz会给予这类输入更多的优先级，Fuzz应该返回1；
如果明确这些输入绝对不能放入corpus，那让Fuzz返回-1；
至于其他情况，返回0。
```


接下来就是go-fuzz-build和go-fuzz登场了，这与前面的介绍差不多：

```
$cd submit
$go-fuzz-build github.com/bigwhite/gocmpp/fuzztest/submit
$ls
cmppfuzz-fuzz.zip corpus/ fuzz.go gen/
```


在submit目录下执行go-fuzz：

```
$go-fuzz -bin=./cmppfuzz-fuzz.zip -workdir=./
2015/12/07 22:05:02 slaves: 4, corpus: 1 (3s ago), crashers: 0, restarts: 1/0, execs: 0 (0/sec), cover: 0, uptime: 3s
2015/12/07 22:05:05 slaves: 4, corpus: 3 (0s ago), crashers: 0, restarts: 1/0, execs: 0 (0/sec), cover: 32, uptime: 6s
2015/12/07 22:05:08 slaves: 4, corpus: 7 (1s ago), crashers: 0, restarts: 1/5424, execs: 65098 (7231/sec), cover: 131, uptime: 9s
2015/12/07 22:05:11 slaves: 4, corpus: 9 (0s ago), crashers: 0, restarts: 1/5424, execs: 65098 (5424/sec), cover: 146, uptime: 12s
... ...
2015/12/07 22:09:11 slaves: 4, corpus: 9 (4m0s ago), crashers: 0, restarts: 1/9860, execs: 4033002 (16002/sec), cover: 146, uptime: 4m12s
^C2015/12/07 22:09:13 shutting down...
```


这个测试非常耗cpu啊！一小会儿功夫，我的Mac Air的风扇就开始呼呼转起来了。不过我的Unpack函数并未在fuzz test中发现问题，crashers后面的数值一直是0。

go-fuzz目前似乎还不支持vendor机制，因此如果你的包像gocmpp一样使用了vendor，那需要在go-fuzz-build和go-fuzz前面加上一个GO15VENDOREXPERIMENT=”0″(如果你之前开启了GO15VENDOREXPERIMENT)，就像这样：

```
$ GO15VENDOREXPERIMENT="0" go-fuzz-build github.com/bigwhite/gocmpp/fuzztest/submit
```


如果不关闭vendor，你可能会得到类似如下的[错误](https://github.com/dvyukov/go-fuzz/issues/109)：

```
can't find imported package golang.org/x/text/transform
```


© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

在fuzz.go中添加一个panic 就可以有crasher了

在执行

“`go-fuzz-build github.com/bigwhite/gocmpp/fuzztest/submit“`

时，程序报错：

/usr/local/go/src/runtime/cgo/cgo.go:34:8: could not import C (no metadata for C)

/usr/local/go/src/net/cgo_linux.go:12:8: could not import C (no metadata for C)

typechecking of github.com/bigwhite/gocmpp/fuzztest/submit failed

请问这是什么原因呢？

我用go 1.17安装了最新的go-fuzz和go-fuzz-build，在macos上没有遇到你这个问题。我翻了一下go-fuzz项目的issue，有一个和你遇到的问题相似：https://github.com/dvyukov/go-fuzz/issues/291。不知道你用的是什么版本的go，在什么平台上运行的。

您好，我使用的是1.14 版本， 我在该链接https://github.com/golang/go/issues/14565看到，go-fuzz-build无法在不依赖c编译器的情况下运行，问题的原因可能是没有安装c语言的编译器，我安装了gcc之后，报错便消失了。