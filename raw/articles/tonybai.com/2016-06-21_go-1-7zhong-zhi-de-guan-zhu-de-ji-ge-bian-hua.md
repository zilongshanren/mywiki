---
title: Go 1.7中值得关注的几个变化
url: https://tonybai.com/2016/06/21/some-changes-in-go-1-7/
published: '2016-06-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.7中值得关注的几个变化

### 零、从Release Cycle说起

从Go 1.3版本开始，Golang核心开发Team的版本开发周期逐渐稳定下来。经过[Go 1.4](http://tonybai.com/2014/11/04/some-changes-in-go-1-4/)、[Go1.5](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)和[Go 1.6](http://tonybai.com/2016/02/21/some-changes-in-go-1-6/)的实践，大神[Russ Cox](https://github.com/rsc)在[Go wiki](https://github.com/golang/go/wiki)上大致定义了[Go Release Cycle](https://github.com/golang/go/wiki/Go-Release-Cycle)的一般流程：

- 半年一个major release版本。
- 发布流程启动时间：每年8月1日和次年2月1日（真正发布日期有可能是这个日子，也可能延后几天）。
- 半年的周期中，前三个月是Active Development，then 功能冻结（大约在11月1日和次年的5月1日）。接下来的三个月为test和polish。
- 下一个版本的启动计划时间：7月15日和1月15日，版本计划期持续15天，包括讨论这个major版本中要实现的主要功能、要fix的前期遗留的bug。
- release前的几个阶段版本：beta版本若干（一般是2-3个）、release candidate版本若干（一般是1-2个）和最后的release版本。
- major release版本的维护是通过一系列的minor版本体现的，主要是修正一些导致crash的严重问题或是安全问题，比如major release版本Go 1.6目前就有go 1.6.1和go 1.6.2两个后续minor版本发布。

在制定下一个版本启动计划时，一般会由Russ Cox在[golang-dev group](https://groups.google.com/forum/#!forum/golang-dev)发起相关讨论，其他Core developer在讨论帖中谈一下自己在下一个版本中要做的事情，让所有开发者大致了解一下下个版本可能包含的功能和修复的bug概况。但这些东西是否能最终包含在下一个Release版本中，还要看Development阶段feature代码是否能完成、通过review并加入到main trunk中；如果来不及加入，这个功能可能就会放入下一个major release中，比如SSA就错过了Go 1.6（由于Go 1.5改动较大，留给Go 1.6的时间短了些）而放在了Go 1.7中了。

个人感觉Go社区采用的是一种“民主集中制”的文化，即来自Google的Golang core team的少数人具有实际话语权，尤其是几个最早加入Go team的大神，比如[Rob Pike](https://github.com/robpike)老头、Russ Cox以及[Ian Lance Taylor](https://github.com/ianlancetaylor)等。当然绝大部分合理建议还是被merge到了Go代码中的，但一些与Go哲学有背离的想法，比如加入泛型、增加新类型、改善错误处理等，基本都被Rob Pike老头严词拒绝了，至少Go 1兼容版本中，大家是铁定看不到的了。至于Go 2，就连Go core team的人也不能不能打包票说一定会有这样的新语言规范。不过从Rob Pike前些阶段的一些言论中，大致可以揣摩出Pike老头正在反思Go 1的设计，也许他正在做Go 2的语言规范也说不定呢^_^。这种“文化”并不能被很多开源开发者所欣赏，在[GopherChina 2016](http://tonybai.com/2016/04/18/my-experience-of-gopherchina2016/)大会上，大家就对这种“有些独裁”的文化做过深刻了辩论，尤其是对比[Rust](https://www.rust-lang.org/)那种“绝对民主”的文化。见仁见智的问题，这里就不深入了。个人觉得Go core team目前的做法还是可以很好的保持Go语言在版本上的理想的兼容性和发展的一致性的，对于一门面向工程领域的语言而言，这也许是开发者们较为看重的东西；编程语言语法在不同版本间“跳跃式”的演进也许会在短时间内带来新鲜感，但长久看来，对代码阅读和维护而言，都会有一个不小的负担。

下面回归正题。Go 1.7究竟带来了哪些值得关注的变化呢？马上揭晓^_^。(以下测试所使用的Go版本为[go 1.7 beta2](https://github.com/golang/go/releases/tag/go1.7beta2))。

### 一、语言

Go 1.7在版本计划阶段设定的目标就是改善和优化(polishing)，因此在Go语言(Specification)规范方面继续保持着与Go 1兼容，因此理论上Go 1.7的发布对以往Go 1兼容的程序而言是透明的，已存在的代码均可以正常通过Go 1.7的编译并正确执行。

不过Go 1.7还是对Go1 Specs中关于“Terminating statements”的说明作了一个extremely tiny的改动：

```
A statement list ends in a terminating statement if the list is not empty and its final statement is terminating.
=>
A statement list ends in a terminating statement if the list is not empty and its final non-empty statement is terminating.
```


Specs是抽象的，例子是生动的，我们用一个例子来说明一下这个改动：

```
// go17-examples/language/f.go
package f
func f() int {
return 3
;
}
```


对于f.go中f函数的body中的语句列表（statement list），所有版本的go compiler或gccgo compiler都会认为其在”return 3″这个terminating statement处terminate，即便return语句后面还有一个“;”也没关系。但Go 1.7之前的gotype工具却严格按照go 1.7之前的Go 1 specs中的说明进行校验，由于最后的statement是”;” – 一个empty statement，gotype会提示：”missing return”：

```
// Go 1.7前版本的gotype
$gotype f.go
f.go:6:1: missing return
```


于是就有了gotype与gc、gccgo行为的不一致！为此Go 1.7就做了一些specs上的改动，将statements list的terminate点从”final statement”改为“final non-empty statement”，这样即便后面再有”;”也不打紧了。于是用go 1.7中的gotype执行同样的命令，得到的结果却不一样：

```
// Go 1.7的gotype
$gotype f.go
没有任何错误输出
```


gotype默认以源码形式随着Go发布，我们需要手工将其编译为可用的工具，编译步骤如下：

```
$cd $GOROOT/src/go/types
$go build gotype.go
在当前目录下就会看到gotype可执行文件，你可以将其mv or cp到$GOBIN下，方便在命令行中使用。
```


### 二、Go Toolchain（工具链）

Go的toolchain的强大实用是毋容置疑的，也是让其他编程语言Fans直流口水的那部分。每次Go major version release，Go工具链都会发生或大或小的改进，这次也不例外。

#### 1、SSA

[SSA](https://en.wikipedia.org/wiki/Static_single_assignment_form)（Static Single-Assignment），对于大多数开发者来说都是不熟悉的，也是不需要关心的，只有搞编译器的人才会去认真研究它究竟为何物。对于Go语言的使用者而言，SSA意味着让编译出来的应用更小，运行得更快，未来有更多的优化空间，而这一切的获得却不需要Go开发者修改哪怕是一行代码^_^。

在Go core team最初的计划中，SSA在Go 1.6时就应该加入，但由于Go 1.6开发周期较为短暂，SSA的主要开发者Keith Randall没能按时完成相关开发，尤其是在性能问题上没能达到之前设定的目标，因此merge被推迟到了Go 1.7。即便是Go 1.7，SSA也只是先完成了x86-64系统。

据实而说，SSA后端的引入，风险还是蛮大的，因此Go在编译器中加入了一个开关”-ssa=0|1″，可以让开发者自行选择是否编译为SSA后端，默认情况下，在x86-64平台下SSA后端是打开的。同时，Go 1.7还修改了包导出的元数据的格式，由以前的文本格式换成了更为短小精炼的二进制格式，这也让Go编译出来的结果文件的Size更为small。

我们可以简单测试一下上述两个优化后对编译后结果的影响，我们以编译github.com/bigwhite/gocmpp/examples/client/例：

```
-rwxrwxr-x 1 share share 4278888 6月 20 14:20 client-go16*
-rwxrwxr-x 1 share share 3319205 6月 20 14:04 client-go17*
-rwxrwxr-x 1 share share 3319205 6月 20 14:05 client-go17-no-newexport*
-rwxrwxr-x 1 share share 3438317 6月 20 14:04 client-go17-no-ssa*
-rwxrwxr-x 1 share share 3438317 6月 20 14:03 client-go17-no-ssa-no-newexport*
其中：client-go17-no-ssa是通过下面命令行编译的：
$go build -a -gcflags="-ssa=0" github.com/bigwhite/gocmpp/examples/client
client-go17-no-newexport*是通过下面命令行编译的：
$go build -a -gcflags="-newexport=0" github.com/bigwhite/gocmpp/examples/client
client-go17-no-ssa-no-newexport是通过下面命令行编译的：
$go build -a -gcflags="-newexport=0 -ssa=0" github.com/bigwhite/gocmpp/examples/client
```


对比client-go16和client-go17，我们可以看到默认情况下Go 17编译出来的可执行程序(client-go17)比Go 1.6编译出来的程序(client-go16)小了约21%，效果十分明显。这也与Go官方宣称的file size缩小20%~30%de 平均效果相符。

不过对比client-go17和client-go17-no-newexport，我们发现，似乎-newexport=0并没有起到什么作用，两个最终可执行文件的size相同。这个在ubuntu 14.04以及darwin平台上测试的结果均是如此，暂无解。

引入SSA后，官方说法是：程序的运行性能平均会提升5%~35%，数据来源于官方的[benchmark](https://golang.org/test/bench/go1/)数据，这里就不再重复测试了。

#### 2、编译器编译性能

Go 1.5发布以来，Go的编译器性能大幅下降就遭到的Go Fans们的“诟病”，虽然Go Compiler的性能与其他编程语言横向相比依旧是“独领风骚”。最差时，Go 1.5的编译构建时间是Go 1.4.x版本的4倍还多。这个问题也引起了Golang老大Rob Pike的极大关注，在Russ Cox筹划Go 1.7时，Rob Pike就极力要求要对Go compiler&linker的性能进行优化，于是就有了Go 1.7“全民优化”Go编译器和linker的上百次commit，至少从目前来看，效果是明显的。

Go大神[Dave Cheney](http://dave.cheney.net/)为了跟踪开发中的Go 1.7的编译器性能情况，建立了三个benchmark：[benchjuju](https://github.com/davecheney/benchjuju)、[benchkube](https://github.com/davecheney/benchkube)和[benchgogs](https://github.com/davecheney/benchgogs)。Dave上个月最新贴出的一幅性能对比图显示：编译同一项目，Go 1.7编译器所需时间仅约是Go 1.6的一半，Go 1.4.3版本的2倍；也就是说经过优化后，Go 1.7的编译性能照比Go 1.6提升了一倍，离Go 1.4.3还有一倍的差距。

![img{}](../../assets/b7abf076c803b8b2.jpg)


#### 3、StackFrame Pointer

在Go 1.7功能freeze前夕，Russ Cox将[StackFrame Pointer](https://github.com/golang/go/issues/15840)加入到Go 1.7中了，目的是使得像Linux Perf或Intel Vtune等工具能更高效的抓取到go程序栈的跟踪信息。但引入STackFrame Pointer会有一些性能上的消耗，大约在2%左右。通过下面环境变量设置可以关闭该功能：

```
export GOEXPERIMENT=noframepointer
```


#### 4、Cgo增加C.CBytes

[Cgo](http://tonybai.com/2012/09/26/interoperability-between-go-and-c/)的helper函数在逐渐丰富，这次Cgo增加C.CBytes helper function就是[源于开发者的需求](https://github.com/golang/go/issues/14838)。这里不再赘述Cgo的这些Helper function如何使用了，通过一小段代码感性了解一下即可：

```
// go17-examples/gotoolchain/cgo/print.go
package main
// #include <stdio.h>
// #include <stdlib.h>
//
// void print(void *array, int len) {
// char *c = (char*)array;
//
// for (int i = 0; i < len; i++) {
// printf("%c", *(c+i));
// }
// printf("\n");
// }
import "C"
import "unsafe"
func main() {
var s = "hello cgo"
csl := C.CBytes([]byte(s))
C.print(csl, C.int(len(s)))
C.free(unsafe.Pointer(csl))
}
执行该程序：
$go run print.go
hello cgo
```


#### 5、其他小改动

- 经过Go 1.5和Go 1.6实验的
[go vendor机制](http://tonybai.com/2015/07/31/understand-go15-vendor/)在Go 1.7中将正式去掉GO15VENDOREXPERIMENT环境变量开关，将vendor作为默认机制。 - go get支持git.openstack.org导入路径。
- go tool dist list命令将打印所有go支持的系统和硬件架构，在我的机器上输出结果如下：

```
$go tool dist list
android/386
android/amd64
android/arm
android/arm64
darwin/386
darwin/amd64
darwin/arm
darwin/arm64
dragonfly/amd64
freebsd/386
freebsd/amd64
freebsd/arm
linux/386
linux/amd64
linux/arm
linux/arm64
linux/mips64
linux/mips64le
linux/ppc64
linux/ppc64le
linux/s390x
nacl/386
nacl/amd64p32
nacl/arm
netbsd/386
netbsd/amd64
netbsd/arm
openbsd/386
openbsd/amd64
openbsd/arm
plan9/386
plan9/amd64
plan9/arm
solaris/amd64
windows/386
windows/amd64
```


### 三、标准库

#### 1、支持subtests和sub-benchmarks

表驱动测试是golang内置testing框架的一个最佳实践，基于表驱动测试的思路，Go 1.7又进一步完善了testing的组织体系，增加了[subtests和sub-benchmarks](https://github.com/golang/proposal/blob/master/design/12166-subtests.md)。目的是为了实现以下几个Features：

- 通过外部command line(go test –run=xx)可以从一个table中选择某个test或benchmark，用于调试等目的；
- 简化编写一组相似的benchmarks；
- 在subtest中使用Fail系列方法(如FailNow，SkipNow等)；
- 基于外部或动态表创建subtests；
- 更细粒度的setup和teardown控制，而不仅仅是TestMain提供的；
- 更多的并行控制；
- 与顶层函数相比，对于test和benchmark来说，subtests和sub-benchmark代码更clean。

下面是一个基于subtests文档中demo改编的例子：

传统的Go 表驱动测试就像下面代码中TestSumInOldWay一样：

```
// go17-examples/stdlib/subtest/foo_test.go
package foo
import (
"fmt"
"testing"
)
var tests = []struct {
A, B int
Sum int
}{
{1, 2, 3},
{1, 1, 2},
{2, 1, 3},
}
func TestSumInOldWay(t *testing.T) {
for _, tc := range tests {
if got := tc.A + tc.B; got != tc.Sum {
t.Errorf("%d + %d = %d; want %d", tc.A, tc.B, got, tc.Sum)
}
}
}
```


对于这种传统的表驱动测试，我们在控制粒度上仅能在顶层测试方法层面，即TestSumInOldWay这个层面：

```
$go test --run=TestSumInOldWay
PASS
ok github.com/bigwhite/experiments/go17-examples/stdlib/subtest 0.008s
```


同时为了在case fail时更容易辨别到底是哪组数据导致的问题，Errorf输出时要带上一些测试数据的信息，比如上面代码中的：”%d+%d=%d; want %d”。

若通过subtests来实现，我们可以将控制粒度细化到subtest层面。并且由于subtest自身具有subtest name唯一性，无需在Error中带上那组测试数据的信息：

```
// go17-examples/stdlib/subtest/foo_test.go
func assertEqual(A, B, expect int, t *testing.T) {
if got := A + B; got != expect {
t.Errorf("got %d; want %d", got, expect)
}
}
func TestSumSubTest(t *testing.T) {
//setup code ... ...
for i, tc := range tests {
t.Run("A=1", func(t *testing.T) {
if tc.A != 1 {
t.Skip(i)
}
assertEqual(tc.A, tc.B, tc.Sum, t)
})
t.Run("A=2", func(t *testing.T) {
if tc.A != 2 {
t.Skip(i)
}
assertEqual(tc.A, tc.B, tc.Sum, t)
})
}
//teardown code ... ...
}
```


我们故意将tests数组中的第三组测试数据的Sum值修改错误，这样便于对比测试结果：

```
var tests = []struct {
A, B int
Sum int
}{
{1, 2, 3},
{1, 1, 2},
{2, 1, 4},
}
```


执行TestSumSubTest：

```
$go test --run=TestSumSubTest
--- FAIL: TestSumSubTest (0.00s)
--- FAIL: TestSumSubTest/A=2#02 (0.00s)
foo_test.go:19: got 3; want 4
FAIL
exit status 1
FAIL github.com/bigwhite/experiments/go17-examples/stdlib/subtest 0.007s
```


分别执行”A=1″和”A=2″的两个subtest：

```
$go test --run=TestSumSubTest/A=1
PASS
ok github.com/bigwhite/experiments/go17-examples/stdlib/subtest 0.007s
$go test --run=TestSumSubTest/A=2
--- FAIL: TestSumSubTest (0.00s)
--- FAIL: TestSumSubTest/A=2#02 (0.00s)
foo_test.go:19: got 3; want 4
FAIL
exit status 1
FAIL github.com/bigwhite/experiments/go17-examples/stdlib/subtest 0.007s
```


测试的结果验证了前面说到的两点：

1、subtest的输出自带唯一标识，比如：“FAIL: TestSumSubTest/A=2#02 (0.00s)”

2、我们可以将控制粒度细化到subtest的层面。

从代码的形态上来看，subtest支持对测试数据进行分组编排，比如上面的测试就将TestSum分为A=1和A=2两组，以便于分别单独控制和结果对比。

另外由于控制粒度支持subtest层，setup和teardown也不再局限尽在TestMain级别了，开发者可以在每个top-level test function中，为其中的subtest加入setup和teardown，大体模式如下：

```
func TestFoo(t *testing.T) {
//setup code ... ...
//subtests... ...
//teardown code ... ...
}
```


Go 1.7中的subtest同样支持并发执行：

```
func TestSumSubTestInParalell(t *testing.T) {
t.Run("blockgroup", func(t *testing.T) {
for _, tc := range tests {
tc := tc
t.Run(fmt.Sprint(tc.A, "+", tc.B), func(t *testing.T) {
t.Parallel()
assertEqual(tc.A, tc.B, tc.Sum, t)
})
}
})
//teardown code
}
```


这里嵌套了两层Subtest，”blockgroup”子测试里面的三个子测试是相互并行(Paralell)执行，直到这三个子测试执行完毕，blockgroup子测试的Run才会返回。而TestSumSubTestInParalell与foo_test.go中的其他并行测试function（如果有的话）的执行是顺序的。

sub-benchmark在形式和用法上与subtest类似，这里不赘述了。

#### 2、Context包

Go 1.7将原来的golang.org/x/net/context包挪入了标准库中，放在$GOROOT/src/context下面，这显然是由于context模式用途广泛，Go core team响应了社区的声音，同时这也是Go core team自身的需要。Std lib中net、net/http、os/exec都用到了context。关于Context的详细说明，没有哪个比Go team的一篇”[Go Concurrent Patterns：Context](https://blog.golang.org/context)“更好了。

### 四、其他改动

Runtime这块普通开发者很少使用，一般都是Go core team才会用到。值得注意的是Go 1.7增加了一个runtime.Error（接口），所有runtime引起的panic，其panic value既实现了标准error接口，也实现了runtime.Error接口。

Golang的GC在1.7版本中继续由[Austin Clements](https://github.com/aclements)和Rick Hudson进行打磨和优化。

Go 1.7编译的程序的执行效率由于SSA的引入和GC的优化，整体上会平均提升5%-35%（在x86-64平台上）。一些标准库的包得到了显著的优化，比如：crypto/sha1, crypto/sha256, encoding/binary, fmt, hash/adler32, hash/crc32, hash/crc64, image/color, math/big, strconv, strings, unicode, 和unicode/utf16，性能提升在10%以上。

Go 1.7还增加了对[使用二进制包（非源码）构建程序](http://tonybai.com/2015/03/09/understanding-import-packages/)的实验性支持（出于一些对商业软件发布形态的考虑），但Go core team显然是不情愿在这方面走太远，不承诺对此进行完整的工具链支持。

标准库中其他的一些细微改动，大家尽可以参考Go 1.7 release notes。

本文涉及到的example代码在[这里](https://github.com/bigwhite/experiments/tree/master/go17-examples)可以下载到。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

关注GO的发展

写得好，谢谢！

赞 尤其是一些refer

赞一个