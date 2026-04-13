---
title: Go 1.20中值得关注的几个变化
url: https://tonybai.com/2023/02/08/some-changes-in-go-1-20/
published: '2023-02-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.20中值得关注的几个变化

![](../../assets/a7f47a2163501125.png)


[本文永久链接](https://tonybai.com/2023/02/08/some-changes-in-go-1-20) – https://tonybai.com/2023/02/08/some-changes-in-go-1-20

美国时间2023年2月1日，唯一尚未退休的Go语言之父[Robert Griesemer](https://github.com/griesemer)代表Go核心开发团队在[Go官博撰文正式发布了Go 1.20版本](https://go.dev/blog/go1.20)。就像[Russ Cox在2022 GopherCon大会](https://www.youtube.com/watch?v=v24wrd3RwGo)所说的那样：** Go2永不会到来，Go 1.x.y将无限延续**！

注：似乎新兴编程语言都喜欢停留在1.x.y上无限延续，譬如已经

[演化到1.67版本的Rust]^_^。

在[《Go，13周年》](https://tonybai.com/2022/11/11/go-opensource-13-years/)之后，Go 1.20新特性在开发主干冻结(2022.11)之前，我曾写过一篇《[Go 1.20新特性前瞻](https://tonybai.com/2022/11/17/go-1-20-foresight)》，对照着[Go 1.20 milestone](https://github.com/golang/go/milestone/250)中内容，把我认为的主要特性和大家简单过了一遍，不过那时Go 1.20毕竟没有正式发布，前瞻肯定不够全面，某些具体的点与正式版本可能也有差异！现在Go 1.20版本正式发布了，其[Release Notes](https://go.dev/blog/go1.20)也补充完整了，在这一篇中，我再来系统说说Go 1.20版本中值得关注的那些变化。对于在[前瞻一文](https://tonybai.com/2022/11/17/go-1-20-foresight)中详细介绍过的特性，这里不会再重复讲解了，大家参考前瞻一文中的内容即可。而对于其他一些特性，或是前瞻一文中着墨不多的特性，这里会挑重点展开说说。

按照惯例，我们依旧首先来看看Go语法层面都有哪些变化，这可能也是多数Gopher们最为关注的变化点。

## 一. 语法变化

Go秉持“大道至简”的理念，对Go语法特性向来是“不与时俱进”的。自从[Go 1.18大刀阔斧的加入了泛型特性](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)后，Go语法特性就又恢复到了之前的“新三年旧三年，缝缝补补又三年”的节奏。Go 1.20亦是如此啊！Release Notes说Go 1.20版本在语言方面包含了四点变化，但看了变化的内容后，我觉得真正的变化只有一个，其他的都是修修补补。

### 1. 切片到数组的转换

唯一算是真语法变化的特性是支持**切片类型到数组类型(或数组类型的指针)的类型转换**，这个特性在[前瞻一文](https://tonybai.com/2022/11/17/go-1-20-foresight)中系统讲过，这里就不赘述了，放个例子大家直观认知一下就可以了：

```
// https://github.com/bigwhite/experiments/blob/master/go1.20-examples/lang/slice2arr.go
func slice2arrOK() {
var sl = []int{1, 2, 3, 4, 5, 6, 7}
var arr = [7]int(sl)
var parr = (*[7]int)(sl)
fmt.Println(sl) // [1 2 3 4 5 6 7]
fmt.Println(arr) // [1 2 3 4 5 6 7]
sl[0] = 11
fmt.Println(arr) // [1 2 3 4 5 6 7]
fmt.Println(parr) // &[11 2 3 4 5 6 7]
}
func slice2arrPanic() {
var sl = []int{1, 2, 3, 4, 5, 6, 7}
fmt.Println(sl)
var arr = [8]int(sl) // panic: runtime error: cannot convert slice with length 7 to array or pointer to array with leng th 8
fmt.Println(arr) // &[11 2 3 4 5 6 7]
}
func main() {
slice2arrOK()
slice2arrPanic()
}
```


有两点注意一下就好：

- 切片转换为数组类型的指针，那么该指针将指向切片的底层数组，就如同上面例子中slice2arrOK的parr变量那样；
- 转换的数组类型的长度不能大于原切片的长度(注意是长度而不是切片的容量哦)，否则在运行时会抛出panic。

### 2. 其他的修修补补

- comparable“放宽”了对泛型实参的限制

下面代码在Go 1.20版本之前，比如Go 1.19版本中会无法通过编译：

```
// https://github.com/bigwhite/experiments/blob/master/go1.20-examples/lang/comparable.go
func doSth[T comparable](t T) {
}
func main() {
n := 2
var i interface{} = n // 编译错误：interface{} does not implement comparable
doSth(i)
}
```


之前，comparable约束下的泛型形参需要支持严格可比较(strictly comparable)的类型作为泛型实参，哪些是严格可比较的类型呢？Go 1.20的语法规范做出了进一步澄清：如果一个类型是可比较的，且不是接口类型或由接口类型组成的类型，那么这个类型就是**严格可比较的类型**，包括：

```
- 布尔型、数值类型、字符串类型、指针类型和channel是严格可比较的。
- 如果结构体类型的所有字段的类型都是严格可比较的，那么该结构体类型就是严格可比较的。
- 如果数组元素的类型是严格可比较的，那么该数组类型就是严格可比较的。
- 如果类型形参的类型集合中的所有类型都是严格可比较的，那么该类型形参就是严格可比较的。
```


我们看到：例外的就是接口类型了。接口类型不是“严格可比较的(strictly comparable)”，但未作为类型形参的接口类型是可比较的(comparable)，如果两个接口类型的动态类型相同且值相等，那么这两个接口类型就相等，或两个接口类型的值均为nil，它们也相等，否则不等。

Go 1.19版本及之前，作为非严格比较类型的接口类型是不能作为comparable约束的类型形参的类型实参的，就像上面comparable.go中示例代码那样，但Go 1.20版本开始，这一要求被防控，接口类型被允许作为类型实参赋值给comparable约束的类型形参了！不过这么做之前，你也要明确一点，如果像下面这样两个接口类型底层类型相同且是不可比较的类型（比如切片)，那么代码将在运行时抛panic：

```
// https://github.com/bigwhite/experiments/blob/master/go1.20-examples/lang/comparable1.go
func doSth[T comparable](t1, t2 T) {
if t1 != t2 {
println("unequal")
return
}
println("equal")
}
func main() {
n1 := []byte{2}
n2 := []byte{3}
var i interface{} = n1
var j interface{} = n2
doSth(i, j) // panic: runtime error: comparing uncomparable type []uint8
}
```


Go 1.20语言规范借此机会还进一步澄清了结构体和数组两种类型比较实现的规范：对于结构体类型，Go会按照结构体字段的声明顺序，逐一字段进行比较，直到遇到第一个不相等的字段为止。如果没有不相等字段，则两个结构体字段相等；对于数组类型，Go会按数组元素的顺序，逐一元素进行比较，直到遇到第一个不相等的元素为止。如果没有不相等的元素，则两个数组相等。

- unsafe包继续添加“语法糖”

继[Go 1.17版本](https://tonybai.com/2021/08/17/some-changes-in-go-1-17)在unsafe包增加Slice函数后，Go 1.20版本又增加三个语法糖函数：SliceData、String和StringData：

```
// $GOROOT/src/unsafe/unsafe.go
func SliceData(slice []ArbitraryType) *ArbitraryType
func String(ptr *byte, len IntegerType) string
func StringData(str string) *byte
```


值得注意的是由于string的不可更改性，String函数的参数ptr指向的内容以及StringData返回的指针指向的内容在String调用和StringData调用后不允许修改，但实际情况是怎么样的呢？

```
// https://github.com/bigwhite/experiments/blob/master/go1.20-examples/lang/unsafe.go
func main() {
var arr = [6]byte{'h', 'e', 'l', 'l', 'o', '!'}
s := unsafe.String(&arr[0], 6)
fmt.Println(s) // hello!
arr[0] = 'j'
fmt.Println(s) // jello!
b := unsafe.StringData(s)
*b = 'k'
fmt.Println(s) // kello!
s1 := "golang"
fmt.Println(s1) // golang
b = unsafe.StringData(s1)
*b = 'h' // fatal error: fault, unexpected fault address 0x10a67e5
fmt.Println(s1)
}
```


我们看到：unsafe.String函数调用后，如果我们修改了传入的指针指向的内容，那么该改动会影响到后续返回的string内容！而StringData返回

的指针所指向的内容一旦被修改，其结果要根据字符串的来源而定了。对于由可修改的底层数组“创建”的字符串(如s)，通过StringData返回的指

针可以“修改”字符串的内容；而对于由字符串字面值初始化的字符串变量(如s1)，其内容是不可修改的(编译器将字符串底层存储分配在了只读数据区)，尝试通过指针修改指向内容，会导致运行时的段错误。

## 二. 工具链

### 1. Go安装包“瘦身”

这些年，Go发布版的安装包“体格”是越来越壮了，动辄100多MB的压缩包，以go.dev/dl页面上的go1.xy.linux-amd64.tar.gz为例，我们看看从Go 1.15版本到Go 1.19版本的“体格”变化趋势：

```
Go 1.15 - 116MB
Go 1.16 - 123MB
Go 1.17 - 129MB
Go 1.18 - 135MB
Go 1.19 - 142MB
```


如果按此趋势，Go 1.20势必要上到150MB以上。但Go团队找到了“瘦身”方法，那就是：[从Go 1.20开始发行版的安装包不再为GOROOT中的软件包提供预编译的.a文件了](https://github.com/golang/go/issues/47257)，这样我们得到的瘦身后的Go 1.20版本的size为**95MB**！相较于Go 1.19，Go 1.20的安装包“瘦”了三分之一。安装包解压后这种体现更为明显：

```
➜ /Users/tonybai/.bin/go1.19 git:(master) ✗ $du -sh
495M .
➜ /Users/tonybai/.bin/go1.20 git:(master) ✗ $du -sh
265M .
```


我们看到：Go 1.20占用的磁盘空间仅为Go 1.19版本的一半多一点而已。 并且，Go 1.20版本中，GOROOT下的源码将像其他用户包那样在构建后被缓存到本机cache中。此外，go install也不会为GOROOT下的软件包安装.a文件。

### 2. 编译器

#### 1) PGO(profile-guided optimization)

Go 1.20编译器的一个最大的变更点是引入了PGO优化技术预览版，这个在前瞻一文中也有[对PGO技术的简单介绍](https://tonybai.com/2022/11/17/go-1-20-foresight)。说白了点，PGO技术就是在原有compiler优化技术的基础上，针对程序在生产环境运行中的热点关键路径再进行一轮优化，并且针对热点代码执行路径，编译器会放开一些限制，比如[Go决定是否对函数进行内联优化的复杂度上限默认值是80](https://tonybai.com/2022/10/17/understand-go-inlining-optimisations-by-example)，但对于PGO指示的关键热点路径，即便函数复杂性超过80很多，也可能会被inline优化掉。

之前持续性能剖析工具开发商Polar Signals曾发布一篇文章[《Exploring Go’s Profile-Guided Optimizations》](https://www.polarsignals.com/blog/posts/2022/09/exploring-go-profile-guided-optimizations/)，专门探讨了PGO技术可能带来的优化效果，文章中借助了Go项目中自带的测试示例，这里也基于这个示例带大家重现一下。

我们使用的例子在Go 1.20源码/安装包的\$GOROOT/src/cmd/compile/internal/test/testdata/pgo/inline路径下：

```
$ls -l
total 3156
-rw-r--r-- 1 tonybai tonybai 1698 Jan 31 05:46 inline_hot.go
-rw-r--r-- 1 tonybai tonybai 843 Jan 31 05:46 inline_hot_test.go
```


我们首先执行一下inline目录下的测试，并生成用于测试的可执行文件以及对应的cpu profile文件供后续PGO优化使用：

```
$go test -o inline_hot.test -bench=. -cpuprofile inline_hot.pprof
goos: linux
goarch: amd64
pkg: cmd/compile/internal/test/testdata/pgo/inline
cpu: Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
BenchmarkA-8 1348 870005 ns/op
PASS
ok cmd/compile/internal/test/testdata/pgo/inline 1.413s
```


接下来，我们对比一下不使用PGO和使用PGO优化，Go编译器在内联优化上的区别：

```
$diff <(go test -run=none -tags='' -timeout=9m0s -gcflags="-m -m" 2>&1 | grep "can inline") <(go test -run=none -tags='' -timeout=9m0s -gcflags="-m -m -pgoprofile inline_hot.pprof" 2>&1 | grep "can inline")
4a5,6
> ./inline_hot.go:53:6: can inline (*BS).NS with cost 106 as: method(*BS) func(uint) (uint, bool) { x := int(i >> lWSize); if x >= len(b.s) { return 0, false }; w := b.s[x]; w = w >> (i & (wSize - 1)); if w != 0 { return i + T(w), true }; x = x + 1; for loop; return 0, false }
> ./inline_hot.go:74:6: can inline A with cost 312 as: func() { s := N(100000); for loop; for loop }
```


上面diff命令中为Go test命令传入-run=none -tags=”" -gcflags=”-m -m”是为了仅编译源文件，而不执行任何测试。


我们看到，相较于未使用PGO优化的结果，PGO优化后的结果多了两个inline函数，这两个可以被inline的函数，一个的复杂度开销为106，一个是312，都超出了默认的80，但仍然可以被inline。

我们来看看PGO的实际优化效果，我们分为在无PGO优化与有PGO优化下执行100次benchmark，再用benchstat工具对比两次的结果：

```
$go test -o inline_hot.test -bench=. -cpuprofile inline_hot.pprof -count=100 > without_pgo.txt
$go test -o inline_hot.test -bench=. -gcflags="-pgoprofile inline_hot.pprof" -count=100 > with_pgo.txt
$benchstat without_pgo.txt with_pgo.txt
goos: linux
goarch: amd64
pkg: cmd/compile/internal/test/testdata/pgo/inline
cpu: Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
│ without_pgo.txt │ with_pgo.txt │
│ sec/op │ sec/op vs base │
A-8 874.7µ ± 0% 872.6µ ± 0% -0.24% (p=0.024 n=100)
```


注：benchstat的安装方法：\$go install golang.org/x/perf/cmd/benchstat@latest


我们看到，在我的机器上(ubuntu 20.04 linux kerenel 5.4.0-132)，PGO针对这个测试的优化效果并不明显(仅仅有0.24%的提升)，Polar Signals原文中的提升幅度也不大，仅为1.05%。

Go官方Release Notes中提到benchmark提升效果为3%~4%，同时官方也提到了，这个仅仅是PGO初始技术预览版，后续会加强对PGO优化的投入，直至对多数程序产生较为明显的优化效果。个人觉得目前PGO尚处于早期，不建议在生产中使用。

Go官方也增加针对[PGO的ref页面](https://go.dev/doc/pgo)，大家重点看看其中的FAQ，你会有更多收获！

#### 2) 构建速度

Go 1.18泛型落地后，Go编译器的编译速度出现了回退(幅度15%)，Go 1.19编译速度也没有提升。虽然编译速度回退后依然可以“秒杀”竞争对手，但对于以编译速度快著称的Go来说，这个问题必须修复。Go 1.20做到了这一点，让Go编译器的编译速度重新回归到了Go 1.17的水准！相对Go 1.19提升10%左右。

我使用github.com/reviewdog/reviewdog这个库实测了一下，分别使用go 1.17.1、go 1.18.6、go 1.19.1和Go 1.20对这个module进行go build -a构建(之前将依赖包都下载本地，排除掉go get环节的影响)，结果如下：

```
go 1.20：
$time go build -a github.com/reviewdog/reviewdog/cmd/reviewdog
go build -a github.com/reviewdog/reviewdog/cmd/reviewdog 48.01s user 7.96s system 536% cpu 10.433 total
go 1.19.1：
$time go build -a github.com/reviewdog/reviewdog/cmd/reviewdog
go build -a github.com/reviewdog/reviewdog/cmd/reviewdog 54.40s user 10.20s system 506% cpu 12.757 total
go 1.18.6：
$time go build -a github.com/reviewdog/reviewdog/cmd/reviewdog
go build -a github.com/reviewdog/reviewdog/cmd/reviewdog 53.78s user 9.85s system 545% cpu 11.654 total
go 1.17.1：
$time go build -a github.com/reviewdog/reviewdog/cmd/reviewdog
go build -a github.com/reviewdog/reviewdog/cmd/reviewdog 50.30s user 9.76s system 580% cpu 10.338 total
```


虽然不能十分精确，但总体上反映出各个版本的编译速度水准以及Go 1.20相对于Go 1.18和Go 1.19版本的提升。我们看到Go 1.20与Go 1.17版本在一个水平线上，甚至要超过Go 1.17(但可能仅限于我这个个例)。

#### 3) 允许在泛型函数/方法中进行类型声明

Go 1.20版本之前下面代码是无法通过Go编译器的编译的：

```
// https://github.com/bigwhite/experiments/blob/master/go1.20-examples/tools/compiler/local_type_decl.go
package main
func F[T1 any]() {
type x struct{} // 编译错误：type declarations inside generic functions are not currently supported
type y = x // 编译错误：type declarations inside generic functions are not currently supported
}
func main() {
F[int]()
}
```


[Go 1.20改进了语言前端的实现](https://github.com/golang/go/issues/47631)，通过unified IR实现了对在泛型函数/方法中进行类型声明(包括定义type alias)的支持。

同时，Go 1.20在[spec](https://go.dev/ref/spec#Type_parameter_declarations)中还明确了[哪些使用了递归方式声明的类型形参列表是不合法的](https://github.com/golang/go/issues/40882)：

```
type T1[P T1[P]] … // 不合法: 形参列表中作为约束的T1引用了自己
type T2[P interface{ T2[int] }] … // 不合法: 形参列表中作为约束的T2引用了自己
type T3[P interface{ m(T3[int])}] … // 不合法: 形参列表中作为约束的T3引用了自己
type T4[P T5[P]] … // 不合法: 形参列表中，T4引用了T5 并且
type T5[P T4[P]] … // T5引用了T4
type T6[P int] struct{ f *T6[P] } // 正确: 虽然引用了T6，但这个引用发生在结构体定义中而不是形参列表中
```


#### 4) 构建自举源码的Go编译器的版本选择

Go从Go 1.5版本开始实现自举，即使用Go实现Go，那么自举后的Go项目是谁来编译的呢？最初对应编译Go 1.5版本的Go编译器版本为Go 1.4。

以前从源码构建Go发行版，当未设置GOROOT_BOOTSTRAP时，编译脚本会默认使用Go 1.4，但如果有更高版本的Go编译器存在，会使用更高版本的编译器。

Go 1.18和Go 1.19会首先寻找是否有go 1.17版本，如果没有再使用go 1.4。

Go 1.20会寻找当前Go 1.17的最后一个版本Go 1.17.13，如果没有，则使用Go 1.4。

将来，Go核心团队计划一年升级一次构建自举源码的Go编译器的版本，例如：Go 1.22版本将使用Go 1.20版本的编译器。

#### 5) cgo

Go命令现在在没有C工具链的系统上会默认禁用了cgo。更具体来说，当CGO_ENABLED环境变量未设置，CC环境变量未设置以及PATH环境变量中没有找到默认的C编译器（通常是clang或gcc）时，CGO_ENABLED会被默认设置为0。

### 3. 其他工具

#### 1) 支持采集应用执行的代码盖率

在前瞻一文中，我提到过Go 1.20将对代码覆盖率的支持扩展到了应用整体层面，而不再仅仅是unit test。这里使用一个例子来看一下，究竟如何采集应用代码的执行覆盖率。我们以gitlab.com/esr/loccount这个代码统计工具为例，先修改一下Makefile，在go build后面加上-cover选项，然后编译loccount，并对其自身进行代码统计：

```
// /home/tonybai/go/src/gitlab.com/loccount
$make
$mkdir mycovdata
$GOCOVERDIR=./mycovdata loccount .
all SLOC=4279 (100.00%) LLOC=1213 in 110 files
Go SLOC=1724 (40.29%) LLOC=835 in 3 files
asciidoc SLOC=752 (17.57%) LLOC=0 in 5 files
C SLOC=278 (6.50%) LLOC=8 in 2 files
Python SLOC=156 (3.65%) LLOC=0 in 2 files
... ...
```


上面执行loccount之前，我们建立了一个mycovdata目录，并设置GOCOVERDIR的值为mycovdata目录的路径。在这样的上下文下，执行loccount后，mycovdata目录下会生成一些覆盖率统计数据文件：

```
$ls mycovdata
covcounters.4ec45ce64f965e77563ecf011e110d4f.926594.1675678144659536943 covmeta.4ec45ce64f965e77563ecf011e110d4f
```


怎么查看loccount的执行覆盖率呢？我们使用go tool covdata来查看：

```
$go tool covdata percent -i=mycovdata
loccount coverage: 69.6% of statements
```


当然, covdata子命令还支持其他一些功能，大家可以自行查看manual挖掘。

#### 2) vet

Go 1.20版本中，go工具链的vet子命令增加了两个十分实用的检测：

- 对loopclosure这一检测策略进行了增强

具体可参见https://github.com/golang/tools/tree/master/go/analysis/passes/loopclosure代码

- 增加对2006-02-01的时间格式的检查

注意我们使用time.Format或Parse时，最常使用的是2006-01-02这样的格式，即ISO 8601标准的时间格式，但一些代码中总是出现2006-02-01，十分容易导致错误。这个版本中，go vet将会对此种情况进行检查。

## 三. 运行时与标准库

### 1. 运行时(runtime)

Go 1.20运行时的调整并不大，仅对GC的内部数据结构进行了微调，这个调整可以获得最多2%的内存开销下降以及cpu性能提升。

### 2. 标准库

标准库肯定是变化最多的那部分。前瞻一文中对下面变化也做了详细介绍，这里不赘述了，大家可以翻看那篇文章细读：

- 支持wrap multiple errors
- time包新增DateTime、DateOnly和TimeOnly三个layout格式常量
- 新增arena包

… …

标准库变化很多，这里不能一一罗列，再补充一些我认为重要的，其他的变化大家可以到[Go 1.20 Release Notes](https://go.dev/doc/go1.20)去看：

#### 1) arena包

前瞻一文已经对arena包做了简要描述，对于arena包的使用以及最佳适用场合的探索还在进行中。著名持续性能剖析工具[pyroscope](https://pyroscope.io/)的官方博客文章[《Go 1.20 arenas实践：arena vs. 传统内存管理》](https://pyroscope.io/blog/go-1-20-memory-arenas/)对于arena实验特性的使用给出了几点好的建议，比如：

- 只在关键的代码路径中使用arena，不要到处使用它们
- 在使用arena之前和之后对你的代码进行profiling，以确保你在能提供最大好处的地方添加arena。
- 密切关注arena上创建的对象的生命周期。确保你不会把它们泄露给你程序中的其他组件，因为那里的对象可能会超过arena的寿命。
- 使用defer a.Free()来确保你不会忘记释放内存。
- 如果你想在arena被释放后使用对象，使用arena.Clone()将其克隆回heap中。

pyroscope的开发人员认为arena是一个强大的工具，也支持标准库中保留arena这个特性，但也建议将arena和reflect、unsafe、cgo等一样纳入“不推荐”使用的包行列。这点我也是赞同的。我也在考虑如何基于arena改进我们产品的协议解析器的性能，有成果后，我也会将实践过程分享出来的。

#### 2) 新增crypto/ecdh包

密码学包(crypto)的主要maintainer [Filippo Valsorda](https://filippo.io/)从google离职后，[成为了一名专职开源项目维护者](https://words.filippo.io/full-time-maintainer/)。这似乎让其更有精力和动力对crypto包进行更好的规划、设计和实现了。[crypto/ecdh包就是在他的提议下加入到Go标准库中的](https://github.com/golang/go/issues/52221)。

相对于标准库之前存在的crypto/elliptic等包，crypto/ecdh包的API更为高级，Go官方推荐使用ecdh的高级API，这样大家以后可以不必再与低级的密码学函数斗争了。

#### 3) HTTP ResponseController

以前HTTP handler的超时都是http服务器全局指定一个的：包括ReadTimeout和WriteTimeout。但有些时候，如果能在某个请求范围内支持这些超时（以及可能的其他选项）将非常有用。Damien Neil就创建了这个[增加ResponseController的提案](https://github.com/golang/go/issues/54136)，下面是一个在HandlerFunc中使用ResponseController的例子：

```
http.HandleFunc("/foo", func(w http.ResponseWriter, r *http.Request) {
ctl := http.NewResponseController(w, r)
ctl.SetWriteDeadline(time.Now().Add(1 * time.Minute)) // 仅为这个请求设置deadline
fmt.Fprintln(w, "Hello, world.") // 这个写入的timeout为1-minute
})
```


#### 4) context包增加WithCancelCause函数

context包新增了一个WithCancelCause函数，与WithCancel不同，通过WithCancelCause返回的Context，我们可以得到cancel的原因，比如下面示例：

```
// https://github.com/bigwhite/experiments/blob/master/go1.20-examples/library/context.go
func main() {
myError := fmt.Errorf("%s", "myError")
ctx, cancel := context.WithCancelCause(context.Background())
cancel(myError)
fmt.Println(ctx.Err()) // context.Canceled
fmt.Println(context.Cause(ctx)) // myError
}
```


我们看到通过context.Cause可以得到Context在cancel时传入的错误原因。

## 四. 移植性

Go对新cpu体系结构和OS的支持向来是走在前面的。Go 1.20还新增了对freebsd在risc-v上的实验性支持，其环境变量为GOOS=freebsd, GOARCH=riscv64。但Go 1.20也将成为对下面平台提供支持的最后一个Go版本：

- Windows 7, 8, Server 2008和Server 2012
- MacOS 10.13 High Sierra和10.14 (我的安装了10.14的mac os又要在go 1.21不被支持了^_^)

近期Go团队又有了新提案：[支持WASI(GOOS=wasi GOARCH=wasm)](https://github.com/golang/go/issues/58141)，WASI是啥，它是WebAssembly一套与引擎无关(engine-indepent)的、面向非Web系统的WASM API标准，是WebAssembly脱离浏览器的必经之路！一旦生成满足WASI的WASM程序，该程序就可以在任何支持WASI或兼容的runtime上运行。不出意外，该提案将在Go 1.21或Go 1.22版本落地。

本文中的示例代码可以在[这里](https://github.com/bigwhite/experiments/blob/master/go1.20-examples)下载。

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