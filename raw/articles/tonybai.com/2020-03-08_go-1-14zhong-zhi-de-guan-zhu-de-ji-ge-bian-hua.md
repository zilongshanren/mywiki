---
title: Go 1.14中值得关注的几个变化
url: https://tonybai.com/2020/03/08/some-changes-in-go-1-14/
published: '2020-03-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.14中值得关注的几个变化

可能是得益于2020年2月26日[Go 1.14的发布](https://blog.golang.org/go1.14)，在2020年3月份的[TIOBE编程语言排行榜](https://tiobe.com/tiobe-index/)上，Go重新进入TOP 10，而去年同期Go仅排行在第18位。虽然[Go语言](https://tonybai.com/tag/go)以及其他主流语言在榜单上的“上蹿下跳”让这个榜单的权威性饱受质疑:)，但Go在这样的一个时间节点能进入TOP 10，对于Gopher和Go社区来说，总还是一个不错的结果。并且在一定层度上说明：[Go在努力耕耘十年](https://tonybai.com/2019/11/09/go-opensource-10-years/)后，已经在世界主流编程语言之林中牢牢占据了自己的一个位置。

![img{512x368}](../../assets/6d30fef23964c3d5.png)


Go自从宣布[Go1 Compatible](https://tip.golang.org/doc/go1compat.html)后，直到这次的Go 1.14发布，Go的语法和核心库都没有做出不兼容的变化。这让很多其他主流语言的拥趸们觉得Go很“无趣”。但这种承诺恰恰是Go团队背后努力付出的结果，因此Go的每个发布版本都值得广大gopher尊重，**每个发布版本都是Go团队能拿出的最好版本**。

下面我们就来解读一下Go 1.14的变化，看看这个新版本中有哪些值得我们重点关注的变化。

## 一. 语言规范

和其他主流语言相比，Go语言的语法规范的变化那是极其少的（广大Gopher们已经习惯了这个节奏:)），偶尔发布一个变化，那自然是要引起广大Gopher严重关注的:)。不过事先说明：**只要Go版本依然是1.x，那么这个规范变化也是backward-compitable的**。

Go 1.14新增的语法变化是：[嵌入接口的方法集可重叠](https://github.com/golang/proposal/blob/master/design/6977-overlapping-interfaces.md)。这个变化背后的朴素思想是这样的。看下面代码(来自[这里](https://github.com/golang/go/issues/6977))：

```
type I interface { f(); String() string }
type J interface { g(); String() string }
type IJ interface { I; J } ----- (1)
type IJ interface { f(); g(); String() string } ---- (2)
```


代码中已知定义的I和J两个接口的方法集中都包含有`String() string`

这个方法。在这样的情况下，我们如果想定义一个方法集合为Union(I, J)的新接口`IJ`

，我们在Go 1.13及之前的版本中只能使用第(2)种方式，即只能在新接口`IJ`

中重新书写一遍所有的方法原型，而无法像第(1)种方式那样使用嵌入接口的简洁方式进行。

Go 1.14通过支持[嵌入接口的方法集可重叠](https://github.com/golang/proposal/blob/master/design/6977-overlapping-interfaces.md)解决了这个问题：

```
// go1.14-examples/overlapping_interface.go
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
在go 1.13.6上运行：
$go build overlapping_interface.go
# command-line-arguments
./overlapping_interface.go:14:2: duplicate method String
但在go 1.14上运行：
$go build overlapping_interface.go
// 一切ok，无报错
```


不过对overlapping interface的支持仅限于接口定义中，如果你要在struct定义中嵌入interface，比如像下面这样：

```
// go1.14-examples/overlapping_interface1.go
package main
type I interface {
f()
String() string
}
type implOfI struct{}
func (implOfI) f() {}
func (implOfI) String() string {
return "implOfI"
}
type J interface {
g()
String() string
}
type implOfJ struct{}
func (implOfJ) g() {}
func (implOfJ) String() string {
return "implOfJ"
}
type Foo struct {
I
J
}
func main() {
f := Foo{
I: implOfI{},
J: implOfJ{},
}
println(f.String())
}
```


虽然Go编译器**没有直接指出结构体Foo中嵌入的两个接口I和J存在方法的重叠**，但在使用Foo结构体时，下面的编译器错误肯定还是会给出的：

```
$ go run overlapping_interface1.go
# command-line-arguments
./overlapping_interface1.go:37:11: ambiguous selector f.String
```


对于结构体中嵌入的接口的方法集是否存在overlap，go编译器似乎并没有严格做“实时”检查，这个检查被延迟到为结构体实例选择method的执行者环节了，就像上面例子那样。如果我们此时让Foo结构体 override一个String方法，那么即便I和J的方法集存在overlap也是无关紧要的，因为编译器不会再模棱两可，可以正确的为Foo实例选出究竟执行哪个String方法：

```
// go1.14-examples/overlapping_interface2.go
.... ....
func (Foo) String() string {
return "Foo"
}
func main() {
f := Foo{
I: implOfI{},
J: implOfJ{},
}
println(f.String())
}
运行该代码：
$go run overlapping_interface2.go
Foo
```


## 二. Go运行时

### 1. 支持异步抢占式调度

在[《Goroutine调度实例简要分析》](https://tonybai.com/2017/11/23/the-simple-analysis-of-goroutine-schedule-examples)一文中，我曾提到过这样一个例子：

```
// go1.14-examples/preemption_scheduler.go
package main
import (
"fmt"
"runtime"
"time"
)
func deadloop() {
for {
}
}
func main() {
runtime.GOMAXPROCS(1)
go deadloop()
for {
time.Sleep(time.Second * 1)
fmt.Println("I got scheduled!")
}
}
```


在只有一个`P`

的情况下，上面的代码中deadloop所在goroutine将持续占据该`P`

，使得main goroutine中的代码得不到调度(GOMAXPROCS=1的情况下)，因此我们无法看到`I got scheduled!`

字样输出。这是因为Go 1.13及以前的版本的抢占是”协作式“的，只在有函数调用的地方才能插入“抢占”代码(埋点)，而deadloop没有给编译器插入抢占代码的机会。这会导致GC在等待所有goroutine停止时等待时间过长，从而[导致GC延迟](https://github.com/golang/go/issues/10958)；甚至在一些特殊情况下，导致在STW（stop the world）时死锁。

Go 1.14采用了基于系统信号的异步抢占调度，这样上面的deadloop所在的goroutine也可以被抢占了：

```
// 使用Go 1.14版本编译器运行上述代码
$go run preemption_scheduler.go
I got scheduled!
I got scheduled!
I got scheduled!
```


不过由于系统信号可能在代码执行到任意地方发生，在Go runtime能cover到的地方，Go runtime自然会处理好这些系统信号。但是如果你是通过`syscall`

包或`golang.org/x/sys/unix`

在Unix/Linux/Mac上直接进行系统调用，那么一旦在系统调用执行过程中进程收到系统中断信号，这些系统调用就会失败，并以**EINTR错误**返回，尤其是低速系统调用，包括：读写特定类型文件(管道、终端设备、网络设备)、进程间通信等。在这样的情况下，我们就需要自己处理**EINTR错误**。一个最常见的错误处理方式就是重试。对于可重入的系统调用来说，在[收到EINTR信号后的重试是安全的](http://man7.org/linux/man-pages/man7/signal.7.html)。如果你没有自己调用syscall包，那么异步抢占调度对你已有的代码几乎无影响。

Go 1.14的异步抢占调度在windows/arm, darwin/arm, js/wasm, and plan9/*上依然尚未支持，Go团队[计划在Go 1.15中解决掉这些问题](https://github.com/golang/go/issues/36365)。

### 2. defer性能得以继续优化

在[Go 1.13](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)中，defer性能得到理论上30%的提升。我们还用那个例子来看看go 1.14与go 1.13版本相比defer性能又有多少提升，同时再看看使用defer和不使用defer的对比：

```
// go1.14-examples/defer_benchmark_test.go
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
func Bar() {
sum(100)
sum(10)
}
func BenchmarkDefer(b *testing.B) {
for i := 0; i < b.N; i++ {
foo()
}
}
func BenchmarkWithoutDefer(b *testing.B) {
for i := 0; i < b.N; i++ {
Bar()
}
}
```


我们分别用Go 1.13和Go 1.14运行上面的基准测试代码：

```
Go 1.13:
$go test -bench . defer_benchmark_test.go
goos: darwin
goarch: amd64
BenchmarkDefer-8 17873574 66.7 ns/op
BenchmarkWithoutDefer-8 26935401 43.7 ns/op
PASS
ok command-line-arguments 2.491s
Go 1.14:
$go test -bench . defer_benchmark_test.go
goos: darwin
goarch: amd64
BenchmarkDefer-8 26179819 45.1 ns/op
BenchmarkWithoutDefer-8 26116602 43.5 ns/op
PASS
ok command-line-arguments 2.418s
```


我们看到，Go 1.14的defer性能照比Go 1.13还有大幅提升，并且已经与不使用defer的性能相差无几了，这也是Go官方鼓励大家在性能敏感的代码执行路径上也大胆使用defer的原因。

![img{512x368}](../../assets/05633d82cb89611d.png)


### 3. internal timer的重新实现

鉴于go timer[长期以来性能不能令人满意](https://github.com/golang/go/issues/6239)，Go 1.14几乎重新实现了runtime层的timer。其实现思路遵循了[Dmitry Vyukov几年前提出的实现逻辑](https://github.com/golang/go/issues/6239#issuecomment-206361959)：将timer分配到每个P上，降低锁竞争；去掉timer thread，减少上下文切换开销；使用netpoll的timeout实现timer机制。

```
// $GOROOT/src/runtime/time.go
type timer struct {
// If this timer is on a heap, which P's heap it is on.
// puintptr rather than *p to match uintptr in the versions
// of this struct defined in other packages.
pp puintptr
}
// addtimer adds a timer to the current P.
// This should only be called with a newly created timer.
// That avoids the risk of changing the when field of a timer in some P's heap,
// which could cause the heap to become unsorted.
func addtimer(t *timer) {
// when must never be negative; otherwise runtimer will overflow
// during its delta calculation and never expire other runtime timers.
if t.when < 0 {
t.when = maxWhen
}
if t.status != timerNoStatus {
badTimer()
}
t.status = timerWaiting
addInitializedTimer(t)
}
// addInitializedTimer adds an initialized timer to the current P.
func addInitializedTimer(t *timer) {
when := t.when
pp := getg().m.p.ptr()
lock(&pp.timersLock)
ok := cleantimers(pp) && doaddtimer(pp, t)
unlock(&pp.timersLock)
if !ok {
badTimer()
}
wakeNetPoller(when)
}
... ...
```


这样你的程序中如果大量使用time.After、time.Tick或者在处理网络连接时大量使用SetDeadline，使用Go 1.14编译后，你的应用将得到timer性能的[自然提升](https://github.com/golang/go/commit/6becb033341602f2df9d7c55cc23e64b925bbee2)。

![img{512x368}](../../assets/cd08ceef2d719592.png)


## 三. Go module已经production ready了

Go 1.14中带来的关于[go module](https://tonybai.com/2019/12/21/go-modules-minimal-version-selection/)的最大惊喜就是Go module已经production ready了，这意味着关于go module的运作机制，go tool的各种命令和其参数形式、行为特征已趋稳定了。笔者从[Go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)引入[go module](https://tonybai.com/2018/07/15/hello-go-module/)以来就一直关注和使用Go module，尤其是[Go 1.13](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)中增加go module proxy的支持，使得中国大陆的gopher再也不用为获取类似`golang.org/x/xxx`

路径下的module而苦恼了。

Go 1.14中go module的主要变动如下：

a) module-aware模式下对vendor的处理：如果go.mod中go version是go 1.14及以上，且当前repo顶层目录下有vendor目录，那么go工具链将默认使用vendor(即-mod=vendor)中的package，而不是module cache中的($GOPATH/pkg/mod下)。同时在这种模式下，go 工具会校验vendor/modules.txt与go.mod文件，它们需要保持同步，否则报错。

在上述前提下，如要非要使用module cache构建，则需要为go工具链显式传入`-mod=mod`

，比如：`go build -mod=mod ./...`

。

b) 增加GOINSECURE，可以不再要求非得以https获取module，或者即便使用https，也不再对server证书进行校验。

c) 在module-aware模式下，如果没有建立go.mod或go工具链无法找到go.mod，那么你必须显式传入要处理的go源文件列表，否则go tools将需要你明确go.mod。比如：在一个没有go.mod的目录下，要编译一个hello.go，我们需要使用go build hello.go(hello.go需要显式放在命令后面），如果你执行`go build .`

就会得到类似如下错误信息：

```
$go build .
go: cannot find main module, but found .git/config in /Users/tonybai
to create a module there, run:
cd .. && go mod init
```


也就是说在没有go.mod的情况下，go工具链的功能是受限的。

d) go module支持subversion仓库了，不过subversion使用应该很“小众”了。

要系统全面的了解go module的当前行为机制，建议还是通读一遍[Go command手册](https://tip.golang.org/cmd/go/)中关于module的说明以及官方[go module wiki](https://github.com/golang/go/wiki/Modules)。

## 四. 编译器

Go 1.14 go编译器在-race和-msan的情况下，默认会执行`-d=checkptr`

，即对unsafe.Pointer的使用进行[合法性检查](https://github.com/golang/go/issues/34964)，主要检查两项内容：

- 当将unsafe.Pointer转型为
`*T`

时，T的内存对齐系数不能高于原地址的

比如下面代码：

```
// go1.14-examples/compiler_checkptr1.go
package main
import (
"fmt"
"unsafe"
)
func main() {
var byteArray = [10]byte{'a', 'b', 'c'}
var p *int64 = (*int64)(unsafe.Pointer(&byteArray[1]))
fmt.Println(*p)
}
```


以-race运行上述代码：

```
$go run -race compiler_checkptr1.go
fatal error: checkptr: unsafe pointer conversion
goroutine 1 [running]:
runtime.throw(0x11646fd, 0x23)
/Users/tonybai/.bin/go1.14/src/runtime/panic.go:1112 +0x72 fp=0xc00004cee8 sp=0xc00004ceb8 pc=0x106d152
runtime.checkptrAlignment(0xc00004cf5f, 0x1136880, 0x1)
/Users/tonybai/.bin/go1.14/src/runtime/checkptr.go:13 +0xd0 fp=0xc00004cf18 sp=0xc00004cee8 pc=0x1043b70
main.main()
/Users/tonybai/go/src/github.com/bigwhite/experiments/go1.14-examples/compiler_checkptr1.go:10 +0x70 fp=0xc00004cf88 sp=0xc00004cf18 pc=0x11283b0
runtime.main()
/Users/tonybai/.bin/go1.14/src/runtime/proc.go:203 +0x212 fp=0xc00004cfe0 sp=0xc00004cf88 pc=0x106f7a2
runtime.goexit()
/Users/tonybai/.bin/go1.14/src/runtime/asm_amd64.s:1373 +0x1 fp=0xc00004cfe8 sp=0xc00004cfe0 pc=0x109b801
exit status 2
```


checkptr检测到：转换后的int64类型的内存对齐系数严格程度要高于转化前的原地址(一个byte变量的地址)。int64对齐系数为8，而一个byte变量地址对齐系数仅为1。

- 做完指针算术后，转换后的unsafe.Pointer仍应指向原先Go堆对象

```
compiler_checkptr2.go
package main
import (
"unsafe"
)
func main() {
var n = 5
b := make([]byte, n)
end := unsafe.Pointer(uintptr(unsafe.Pointer(&b[0])) + uintptr(n+10))
_ = end
}
```


运行上述代码：

```
$go run -race compiler_checkptr2.go
fatal error: checkptr: unsafe pointer arithmetic
goroutine 1 [running]:
runtime.throw(0x10b618b, 0x23)
/Users/tonybai/.bin/go1.14/src/runtime/panic.go:1112 +0x72 fp=0xc00003e720 sp=0xc00003e6f0 pc=0x1067192
runtime.checkptrArithmetic(0xc0000180b7, 0xc00003e770, 0x1, 0x1)
/Users/tonybai/.bin/go1.14/src/runtime/checkptr.go:41 +0xb5 fp=0xc00003e750 sp=0xc00003e720 pc=0x1043055
main.main()
/Users/tonybai/go/src/github.com/bigwhite/experiments/go1.14-examples/compiler_checkptr2.go:10 +0x8d fp=0xc00003e788 sp=0xc00003e750 pc=0x1096ced
runtime.main()
/Users/tonybai/.bin/go1.14/src/runtime/proc.go:203 +0x212 fp=0xc00003e7e0 sp=0xc00003e788 pc=0x10697e2
runtime.goexit()
/Users/tonybai/.bin/go1.14/src/runtime/asm_amd64.s:1373 +0x1 fp=0xc00003e7e8 sp=0xc00003e7e0 pc=0x1092581
exit status 2
```


checkptr检测到转换后的unsafe.Pointer已经超出原先heap object: b的范围了，于是报错。

不过目前Go标准库依然[尚未能完全通过checkptr的检查](https://github.com/golang/go/issues/34972)，因为有些库代码显然违反了[unsafe.Pointer的使用规则](https://tip.golang.org/pkg/unsafe/#Pointer)。

[Go 1.13](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)引入了新的Escape Analysis，Go 1.14中我们可以通过`-m=2`

查看详细的逃逸分析过程日志，比如：

```
$go run -gcflags '-m=2' compiler_checkptr2.go
# command-line-arguments
./compiler_checkptr2.go:7:6: can inline main as: func() { var n int; n = 5; b := make([]byte, n); end := unsafe.Pointer(uintptr(unsafe.Pointer(&b[0])) + uintptr(n + 100)); _ = end }
./compiler_checkptr2.go:9:11: make([]byte, n) escapes to heap:
./compiler_checkptr2.go:9:11: flow: {heap} = &{storage for make([]byte, n)}:
./compiler_checkptr2.go:9:11: from make([]byte, n) (non-constant size) at ./compiler_checkptr2.go:9:11
./compiler_checkptr2.go:9:11: make([]byte, n) escapes to heap
```


## 五. 标准库

每个Go版本，变化最多的就是标准库，这里我们挑一个可能影响后续我们编写单元测试行为方式的变化说说，那就是testing包的T和B类型都增加了自己的[Cleanup方法](https://tip.golang.org/pkg/testing/#T.Cleanup)。我们通过代码来看一下Cleanup方法的作用：

```
// go1.14-examples/testing_cleanup_test.go
package main
import "testing"
func TestCase1(t *testing.T) {
t.Run("A=1", func(t *testing.T) {
t.Logf("subtest1 in testcase1")
})
t.Run("A=2", func(t *testing.T) {
t.Logf("subtest2 in testcase1")
})
t.Cleanup(func() {
t.Logf("cleanup1 in testcase1")
})
t.Cleanup(func() {
t.Logf("cleanup2 in testcase1")
})
}
func TestCase2(t *testing.T) {
t.Cleanup(func() {
t.Logf("cleanup1 in testcase2")
})
t.Cleanup(func() {
t.Logf("cleanup2 in testcase2")
})
}
```


运行上面测试：

```
$go test -v testing_cleanup_test.go
=== RUN TestCase1
=== RUN TestCase1/A=1
TestCase1/A=1: testing_cleanup_test.go:8: subtest1 in testcase1
=== RUN TestCase1/A=2
TestCase1/A=2: testing_cleanup_test.go:12: subtest2 in testcase1
TestCase1: testing_cleanup_test.go:18: cleanup2 in testcase1
TestCase1: testing_cleanup_test.go:15: cleanup1 in testcase1
--- PASS: TestCase1 (0.00s)
--- PASS: TestCase1/A=1 (0.00s)
--- PASS: TestCase1/A=2 (0.00s)
=== RUN TestCase2
TestCase2: testing_cleanup_test.go:27: cleanup2 in testcase2
TestCase2: testing_cleanup_test.go:24: cleanup1 in testcase2
--- PASS: TestCase2 (0.00s)
PASS
ok command-line-arguments 0.005s
```


我们看到：

-
Cleanup方法运行于所有测试以及其子测试完成之后。

-
Cleanup方法类似于defer，先注册的cleanup函数后执行（比如上面例子中各个case的cleanup1和cleanup2）。


在拥有Cleanup方法前，我们经常像下面这样做：

```
// go1.14-examples/old_testing_cleanup_test.go
package main
import "testing"
func setup(t *testing.T) func() {
t.Logf("setup before test")
return func() {
t.Logf("teardown/cleanup after test")
}
}
func TestCase1(t *testing.T) {
f := setup(t)
defer f()
t.Logf("test the testcase")
}
```


运行上面测试：

```
$go test -v old_testing_cleanup_test.go
=== RUN TestCase1
TestCase1: old_testing_cleanup_test.go:6: setup before test
TestCase1: old_testing_cleanup_test.go:15: test the testcase
TestCase1: old_testing_cleanup_test.go:8: teardown/cleanup after test
--- PASS: TestCase1 (0.00s)
PASS
ok command-line-arguments 0.005s
```


有了Cleanup方法后，我们就不需要再像上面那样单独编写一个返回cleanup函数的setup函数了。

此次Go 1.14还将对unicode标准的支持从unicode 11 升级到 unicode 12 ，共增加了554个新字符。

## 六. 其他

超强的[可移植性](http://tonybai.com/2017/06/27/an-intro-about-go-portability/)是Go的一个知名标签，在新平台支持方面，Go向来是“急先锋”。Go 1.14为64bit RISC-V提供了在linux上的实验性支持(GOOS=linux, GOARCH=riscv64)。

rust语言已经通过[cargo-fuzz](https://github.com/rust-fuzz/cargo-fuzz)从工具层面为fuzz test提供了基础支持。Go 1.14也在这方面[做出了努力](https://github.com/golang/go/issues/14565)，并且Go已经在向[将fuzz test变成Go test的一等公民](https://github.com/golang/go/issues/19109)而努力。

## 七. 小结

Go 1.14的详细变更说明在[这里](https://tip.golang.org/doc/go1.14)可以查看。整个版本的milestone对应的issue集合在[这里](https://github.com/golang/go/milestone/95?closed=1)。

不过目前Go 1.14在特定版本linux内核上会出现crash的问题，当然这个问题源于这些内核的一个已知bug。在[这个issue](https://github.com/golang/go/issues/37436#issuecomment-591327351)中有关于这个问题的详细说明，涉及到的Linux内核版本包括：5.2.x, 5.3.0-5.3.14, 5.4.0-5.4.1。

本篇博客涉及的代码在[这里](https://github.com/bigwhite/experiments/tree/master/go1.14-examples)可以下载。

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

不错不错

请问Go的 -race 是编译期的静态检查吗？我发现：

package main

import “unsafe”

func main() {

d := make([]byte, 4)

ip := unsafe.Pointer(uintptr(unsafe.Pointer(&d[0])) + uintptr(4+20))

print(ip)

}

可以检测通过，而：

package main

import “unsafe”

func main() {

n := 4

d := make([]byte, n)

ip := unsafe.Pointer(uintptr(unsafe.Pointer(&d[0])) + uintptr(n+20))

print(ip)

}

就是通不过的。

如果使用-race选项，go 1.14编译器会在代码中插入对unsafe.Pointer使用合规的检查，这些插入的代码将在程序运行时起作用。你评论中的两份代码我没看出有啥本质区别啊（手动捂脸）。

checkptr 对齐那个，发现和文章描述的不一致，查了一回才发现https://github.com/golang/go/commit/229247d33b717ce7729e43a8fde3a095e376cf3d 这里就改了