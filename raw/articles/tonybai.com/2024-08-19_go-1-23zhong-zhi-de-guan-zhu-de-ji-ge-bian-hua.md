---
title: Go 1.23中值得关注的几个变化
url: https://tonybai.com/2024/08/19/some-changes-in-go-1-23/
published: '2024-08-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.23中值得关注的几个变化

![](../../assets/4ad1f0eee4cad75b.png)


[本文永久链接](https://tonybai.com/2024/08/19/some-changes-in-go-1-23) – https://tonybai.com/2024/08/19/some-changes-in-go-1-23

距离上一次[Go 1.22版本发布](https://tonybai.com/2024/02/18/some-changes-in-go-1-22)又过去六个月了，我们如期迎来了[Go 1.23版本的发布](https://mp.weixin.qq.com/s/IpDUOe0AUDKW2PYCWmvLYw)。

对于Go项目乃至整个Go社区而言，这个版本还有一点额外的意义，那就是这是[Russ Cox](https://github.com/rsc)作为Tech lead，领导Go团队发布的最后一个Go版本了。

8月2日，Russ Cox在[golang-dev google group](https://groups.google.com/g/golang-dev/c/0OqBkS2RzWw)上发文，在领导了Go项目12年后，决定[辞去Tech Lead](https://mp.weixin.qq.com/s/2Sy6K_dU1j3tZZiyyfCTDQ)，并将这一角色“传位”给[Austin Clements](https://github.com/aclements)，后者是现任Go core领域(围绕编译器工具链、运行时和发布)的Leader。Cherry Mui将递补，成为Go core领域的新Leader。

注：除了Go core外，Go项目下面还有两个领域的子团队，分别是由Roland Shoemaker领导的Go安全团队（Go Security）和由Rob Findley、Hana Kim共同领导的Go工具链和IDE支持团队。


![](../../assets/02386d4b5c5d4491.png)


注：Austin曾在Google担任实习生，在攻读博士学位期间参与了Go项目的早期工作。后来(2014年)，他加入了Go 团队，与

[Rick Hudson]合作完成了[Go的并发垃圾回收]。他还曾参与了当前的抢占式调度器和链接器的开发工作。现在，他领导着Go的编译器/运行时团队。– 来自[golang.design]

长相有些神似“马特达蒙”的Russ Cox经常活动于GopherCon之类的技术大会上，照片和视频比较多，但Austin和Cherry似乎都很神秘，很少出镜。Cherry Mui居然还是一个巾帼女汉子。如果你和我一样，不是很了解Austin，可以看看这个[Austin在GopherCon 2020上的这个视频](https://www.youtube.com/watch?v=1I1WmeSjRSw)。

在Russ Cox的领导下，Go如今已经成为云原生领域的基石语言，在我的《[都2024年了，当初那个“Go，互联网时代的C语言”的预言成真了吗？](https://tonybai.com/2024/08/17/go-the-c-language-of-the-internet-era-come-true/)》那篇文章中，我谈到Go建立了云原生时代的整体技术栈，地位媲美单机时代的C语言。Go在各大编程语言排行榜的位次也一直在提升，今年[Go在TIOBE上最高已经冲到了第七名](https://mp.weixin.qq.com/s/1tNis1guPjSRkvpklgrRIg)。在语法特性和工具链方面，Russ Cox带领Go团队先后实现了Go module、Go泛型等重要变化的落地。Go已经证明了自己的成功。

但俗话说：“船大难掉头”！随着Go语言的成熟，用户的不断增多，生态的不断扩大，如何把控好Go这艘大船，持续在正确的方向上航行，便逐渐成为了摆在Go团队面前的一个极具挑战性的问题。另外，在Go演进的过程中，质疑声也从来就没有中断过，尤其是在Go module、Go泛型等提案落地的过程中。Go 1.23引入的自定义函数iterator也曾一度将Go抛上风口浪尖，一些人批评[Go忘记了简单的原则，正在走向错误的演进方向上](https://itnext.io/go-evolves-in-the-wrong-direction-7dfda8a1a620)。甚至还出现了Go已经过了流行的顶峰的观点：

![](../../assets/2289a1890ba05cd1.png)


这些也同样是Russ Cox留给Austin Clements等新一代决策层的“课题”。

言归正传！让我们来看看Go 1.23版本都有哪些重要的变化吧！

注：在两个多月，我曾写了一篇《

[Go 1.23新特性前瞻]》，如果当时的新变化的实现与如今Go 1.23正式版是一致的，在本文中我就不会再详细说明了，大家可以移步那篇文章了解。

## 1. 语言变化

Go 1.23中最大的语言变化就是将Go 1.22中引入的试验特性：[range-over-func](https://go.dev/wiki/RangefuncExperiment)变为了正式特性。我么就先从这个变化说起。

### 1.1 自定义函数迭代器

一旦你接受了泛型，迭代器就会不可避免地出现 — https://changelog.com/gotime/325


迭代器(iterator)是一个用于遍历集合类型的基本语言构造，例如切片、数组、map等。它是一种获取集合中的下一个item的机制，并会检查集合中是否还有其他内容，如果没有了，它会停止继续迭代。这种语言构造并非Go专属的，我们在许多语言中都能找到它，比如：Python、Java等。

[Go 1.18版本加入了泛型支持](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)，有了泛型后，各种使用泛型实现的集合类型便如“雨后春笋”般出现了。但Go的for range原生并不支持对这些集合类型的迭代，于是对自定义函数迭代器类型的需求便自然而然的出现了。

Go 1.23支持自定义迭代器后，for range的语法规格变为如下形式：

![](../../assets/17a02e56e919cb0f.png)


我们看到：for range继[Go 1.22增加对整型表达式的支持](https://tonybai.com/2023/12/25/go-1-22-foresight)后，在Go 1.23中又增加了对三种形式的自定义函数迭代器的支持。下面是Go spec中关于带有单个参数(fibo)和带有两个参数的函数迭代器(Walk)的示例：

```
// fibo generates the Fibonacci sequence
fibo := func(yield func(x int) bool) {
f0, f1 := 0, 1
for yield(f0) {
f0, f1 = f1, f0+f1
}
}
// print the Fibonacci numbers below 1000:
for x := range fibo {
if x >= 1000 {
break
}
fmt.Printf("%d ", x)
}
// output: 0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987
// iteration support for a recursive tree data structure
type Tree[K cmp.Ordered, V any] struct {
left, right *Tree[K, V]
key K
value V
}
func (t *Tree[K, V]) walk(yield func(key K, val V) bool) bool {
return t == nil || t.left.walk(yield) && yield(t.key, t.value) && t.right.walk(yield)
}
func (t *Tree[K, V]) Walk(yield func(key K, val V) bool) {
t.walk(yield)
}
// walk tree t in-order
var t Tree[string, int]
for k, v := range t.Walk {
// process k, v
}
```


初看这个示例，for range的形式很简洁，且循环体内部对获得的item的处理也没有受到任何影响。函数迭代器的复杂性更多放在了提供迭代器的集合类型的作者那里了。作为要提供自定义迭代器的集合类型作者，你需要弄清楚迭代器的运作原理，尤其要记住要满足何种函数签名，才能更好地提供迭代器的实现，这的确会带来一些复杂性，并且初期编写时，你可能会反复参考[Go Spec文档](https://go.dev/ref/spec)。至于迭代器的运作原理和典型使用方法，在不久前写的一篇《[Go 1.23中的自定义迭代器与iter包](https://tonybai.com/2024/06/24/range-over-func-and-package-iter-in-go-1-23/)》中，我对Go 1.23新增的迭代器做了一个系统的梳理，感兴趣的童鞋可以移步那篇文章阅读，这里就不另花笔墨了。

### 1.2 别名中增加泛型参数

但凡涉及type alias的提案或多或少都会有一定的争议，这次也不例外。Matthew Dempsky于2021年提出的issue: [spec: generics: permit type parameters on aliases](https://github.com/golang/go/issues/46477)历经多年，几百次的讨论，才最终在Go 1.23中作为实验性特性引入。也许也正是这种缓慢而稳定的方法才是Go标准库和Go社区发展过程中真正令人印象深刻的地方。不过，目前除了这个issue中的内容，尚未有类似experimental wiki之类的资料可循。

那什么是带有类型参数的type alias呢？我们看看下面这个示例：

```
// go1.23-examples/lang/generic_type_alias.go
package main
import "fmt"
type MySlice[T any] = []T
func main() {
// 使用int类型实例化MySlice
intSlice := MySlice[int]{1, 2, 3, 4, 5}
fmt.Println("Int Slice:", intSlice)
// 使用string类型实例化MySlice
stringSlice := MySlice[string]{"hello", "world"}
fmt.Println("String Slice:", stringSlice)
// 使用自定义类型实例化MySlice
type Person struct {
Name string
Age int
}
personSlice := MySlice[Person]{
{Name: "Alice", Age: 30},
{Name: "Bob", Age: 25},
}
fmt.Println("Person Slice:", personSlice)
}
```


我们需要Go 1.23.0及以上版本可以编译该程序，并且还需要在命令前加上：GOEXPERIMENT=aliastypeparams。

执行上述程序的结果如下：

```
$GOEXPERIMENT=aliastypeparams go build generic_type_alias.go
$./generic_type_alias
Int Slice: [1 2 3 4 5]
String Slice: [hello world]
Person Slice: [{Alice 30} {Bob 25}]
```


怎么理解带有类型参数的类型别名呢？参考Russ Cox在issue的comment给出的理解，我们可以将其看成是一种“类型宏”(类似c中的#define)，以该示例为例：

```
type MySlice[T any] = []T
```


就是**在任何出现MySlice[T]的地方，将其换成[]T**。我们再看一个复杂的例子：

```
// go1.23-examples/lang/pairs.go
package main
import "fmt"
// 使用多个类型参数的类型别名
type Pair[T, U any] = struct {
First T
Second U
}
// 使用Pair类型别名
func MakePair[T, U any](first T, second U) Pair[T, U] {
return Pair[T, U]{First: first, Second: second}
}
// 交换Pair中的元素
func SwapPair[T, U any](p Pair[T, U]) Pair[U, T] {
return Pair[U, T]{First: p.Second, Second: p.First}
}
func main() {
// 创建一个int和string的Pair
intStringPair := MakePair(42, "Answer")
fmt.Printf("Int-String Pair: %+v\n", intStringPair)
// 创建一个float64和bool的Pair
floatBoolPair := Pair[float64, bool]{First: 3.14, Second: true}
fmt.Printf("Float-Bool Pair: %+v\n", floatBoolPair)
// 使用自定义类型
type Person struct {
Name string
Age int
}
personStringPair := MakePair(Person{Name: "Alice", Age: 30}, "Developer")
fmt.Printf("Person-String Pair: %+v\n", personStringPair)
// 交换Pair中的元素
swappedPair := SwapPair(intStringPair)
fmt.Printf("Swapped Int-String Pair: %+v\n", swappedPair)
// 使用类型推断
inferredPair := MakePair("Hello", 123)
fmt.Printf("Inferred Pair: %+v\n", inferredPair)
}
```


我们可以在任何出现Pair[T, U any]的地方将其换为

```
struct {
First T
Second U
}
```


编译运行上述代码，可得到如下结果：

```
$GOEXPERIMENT=aliastypeparams go run pairs.go
Int-String Pair: {First:42 Second:Answer}
Float-Bool Pair: {First:3.14 Second:true}
Person-String Pair: {First:{Name:Alice Age:30} Second:Developer}
Swapped Int-String Pair: {First:Answer Second:42}
Inferred Pair: {First:Hello Second:123}
```


Russ Cox还提到，利用该aliastypeparams机制，还可以用于缩短命名，比如：

```
type lexer[T any] = func(string, int) (T, int, bool)
```


当然Go 1.9引入type alias是为了重构，而aliastypeparams机制也可以很好的帮助重构，比如下面这个定义：

```
type T1[X, Y any] = T2[X, Y, defaultZ]
```


即如果已经有了T1[X, Y]，然后意识到需要另一个参数，并将其泛型化为T2[X, Y, Z]，这时使用上面的语句可以保持旧代码的正常运行。

此外，如果类型别名的约束更严格呢，比如下面的类型别名定义：

```
type MySlice[T any] = []T
type YourSlice[T comparable] = MySlice[T]
```


这里YourSlice的类型参数约束要求是comparable，比MySlice的any更严格，我们来看一下这个comparable会有效么？

```
// go1.23-examples/lang/strict_alias.go
package main
import "fmt"
type MySlice[T any] = []T
type YourSlice[T comparable] = MySlice[T]
func main() {
// 使用int类型实例化MySlice
intSlice := MySlice[int]{1, 2, 3, 4, 5}
fmt.Println("Int Slice:", intSlice)
intsliceSlice := YourSlice[[]int]{
[]int{1, 2, 3},
[]int{4, 5, 6},
}
fmt.Println("IntSlice Slice:", intsliceSlice)
}
```


我们知道int切片类型是不满足comparable的，但这个示例代码在目前Go 1.23.0版本是可以正常编译运行的。

最后，该aliastypeparameter实验特性会将类型别名定义局限在同一个包中，尚不支持跨多个包使用。

## 2. 工具链

在工具链方面，Go 1.23的变化都很实用！我们逐一挑重点变化来看一下。

### 2.1 Telemetry(遥测)

Go Telemetry是一个用于Go工具链程序收集性能和使用数据的系统。它适用于Go团队维护的开发者工具，如go cmd、gopls和govulncheck。

Russ Cox关于Go telemetry的构思始于2023年2月，他先是在个人博客发表一系列关于Go telemetry的思路和设计方案，然后又[在Go项目建立disscusion](https://github.com/golang/go/discussions/58409)和社区探讨这个idea。

在2023年GopherCon大会上，Russ Cox代表Go团队做了名为“Go Changes”的主题演讲，明确了[Go的演进将是基于数据驱动](https://tonybai.com/2023/12/10/go-changes/)的，而数据来源除了来自官方的年度用户调查、用户交谈、对已发布的go module的代码阅读分析之外，Go团队计划在Go工具链中加入Telemetry。telemetry可以帮助Go团队改进Go语言和工具，了解Go工具链使用情况和问题并提供比GitHub问题或年度用户调查更详细、及时的数据。

随着Go 1.23的发布，telemetry作为go cmd的sub command正式落地。

Go Telemetry由telemetry模式控制，有三种可能的值：

- local(默认): 收集数据并存储在本地计算机上，但不上传；
- on: 收集数据，并可能根据采样上传；
- off：不收集也不上传数据。

你可以通过go env GOTELEMETRY查看当前模式。你可以通过go telemetry on|off|local来选择使用哪种模式。

Go Telemetry使用计数器来收集数据，它主要有两类计数器：

- 基本计数器：记录命名事件的次数
- 栈计数器：记录事件次数和发生时的调用栈

计数器数据写入本地文件系统(存储路径可通过go env GOTELEMETRYDIR查看)的内存映射文件中：

```
// 在我的macOS上
$go env GOTELEMETRYDIR
/Users/tonybai/Library/Application Support/go/telemetry
```


大约每周一次，计数器数据会被汇总成报告，存储在本地目录中。如果启用了上传(on)，只有经过批准的计数器子集会被上传到telemetry.go.dev。

访问telemetry.go.dev网站可以查看由公开上传数据合并的报告和生成的图表。这些报告和图表可以帮助Go团队了解工具的使用情况、性能表现，从而进行有针对性的改进。

为了Go演进路线的精准，这里也呼吁大家多多支持。当下载Go 1.23版本后，简单地执行“go telemetry on”，你就可以为Go做贡献了：

```
$go telemetry on
Telemetry uploading is now enabled and data will be periodically sent to
https://telemetry.go.dev/. Uploaded data is used to help improve the Go
toolchain and related tools, and it will be published as part of a public
dataset.
For more details, see https://telemetry.go.dev/privacy.
This data is collected in accordance with the Google Privacy Policy
(https://policies.google.com/privacy).
To disable telemetry uploading, but keep local data collection, run
“go telemetry local”.
To disable both collection and uploading, run “go telemetry off”.
```


### 2.2 实用的go命令变化

- go env -changed

go env子命令增加一个-changed命令行选项，可以用于查看当前Go环境中设置的Go环境变量值与默认值有差异的项的值，包括使用go env -w写入的，或是通过系统环境变量设置的。

在我的环境中，我可以看到下面的几个go环境变量的值的自定义设定：

```
$go env -changed
GONOPROXY='xxxxx'
GONOSUMDB='xxxxx'
GOPRIVATE='xxxxx'
GOPROXY='https://goproxy.cn'
GOSUMDB='off'
```


- go mod tidy -diff

go mod tidy增加了一个“dry-run”方式，通过-diff命令行选项，可以使得go mod tidy只打印（以unified diff的格式）更新信息，但不做实际的更新（即修改go.mod和go.sum），比如在我的以前的一个代码目录下执行该命令：

```
$go mod tidy -diff
go: downloading google.golang.org/protobuf v1.25.0
go: downloading github.com/golang/protobuf v1.4.3
go: downloading google.golang.org/genproto v0.0.0-20200806141610-86f49bd18e98
go: downloading golang.org/x/net v0.0.0-20201021035429-f5854403a974
go: downloading golang.org/x/sys v0.0.0-20200930185726-fdedc70b468f
go: downloading github.com/google/go-cmp v0.5.6
go: downloading golang.org/x/xerrors v0.0.0-20200804184101-5ec99f83aff1
go: downloading golang.org/x/text v0.3.3
go: downloading github.com/golang/protobuf v1.5.2
go: downloading google.golang.org/protobuf v1.27.1
go: downloading golang.org/x/sys v0.0.0-20210119212857-b64e53b001e4
diff current/go.mod tidy/go.mod
--- current/go.mod
+++ tidy/go.mod
@@ -8,12 +8,12 @@
)
require (
- github.com/golang/protobuf v1.4.3 // indirect
+ github.com/golang/protobuf v1.5.2 // indirect
golang.org/x/net v0.0.0-20201021035429-f5854403a974 // indirect
- golang.org/x/sys v0.0.0-20200930185726-fdedc70b468f // indirect
+ golang.org/x/sys v0.0.0-20210119212857-b64e53b001e4 // indirect
golang.org/x/text v0.3.3 // indirect
google.golang.org/genproto v0.0.0-20200806141610-86f49bd18e98 // indirect
- google.golang.org/protobuf v1.25.0 // indirect
+ google.golang.org/protobuf v1.27.1 // indirect
)
replace google.golang.org/grpc v1.40.0 => /Users/tonybai/Go/src/github.com/grpc/grpc-go
diff current/go.sum tidy/go.sum
--- current/go.sum
+++ tidy/go.sum
@@ -7,13 +7,16 @@
github.com/client9/misspell v0.3.4/go.mod h1:qj6jICC3Q7zFZvVWo7KLAzC3yx5G7kyvSDkc90ppPyw=
github.com/cncf/udpa/go v0.0.0-20191209042840-269d4d468f6f/go.mod h1:M8M6+tZqaGXZJjfX53e64911xZQV5JYwmTeXPW+k8Sc=
github.com/cncf/udpa/go v0.0.0-20201120205902-5459f2c99403/go.mod h1:WmhPx2Nbnhtbo57+VJT5O0JRkEi1Wbu0z5j0R8u5Hbk=
-github.com/cncf/xds/go v0.0.0-20210312221358-fbca930ec8ed/go.mod h1:eXthEFrGJvWHgFFCl3hGmgk+/aYT6PnTQLykKQRLhEs=
+github.com/cncf/udpa/go v0.0.0-20210930031921-04548b0d99d4/go.mod h1:6pvJx4me5XPnfI9Z40ddWsdw2W/uZgQLFXToKeRcDiI=
+github.com/cncf/xds/go v0.0.0-20210922020428-25de7278fc84/go.mod h1:eXthEFrGJvWHgFFCl3hGmgk+/aYT6PnTQLykKQRLhEs=
+github.com/cncf/xds/go v0.0.0-20211001041855-01bcc9b48dfe/go.mod h1:eXthEFrGJvWHgFFCl3hGmgk+/aYT6PnTQLykKQRLhEs=
+github.com/cncf/xds/go v0.0.0-20211011173535-cb28da3451f1/go.mod h1:eXthEFrGJvWHgFFCl3hGmgk+/aYT6PnTQLykKQRLhEs=
github.com/davecgh/go-spew v1.1.0/go.mod h1:J7Y8YcW2NihsgmVo/mv3lAwl/skON4iLHjSsI+c5H38=
github.com/envoyproxy/go-control-plane v0.9.0/go.mod h1:YTl/9mNaCwkRvm6d1a2C3ymFceY/DCBVvsKhRF0iEA4=
github.com/envoyproxy/go-control-plane v0.9.1-0.20191026205805-5f8ba28d4473/go.mod h1:YTl/9mNaCwkRvm6d1a2C3ymFceY/DCBVvsKhRF0iEA4=
github.com/envoyproxy/go-control-plane v0.9.4/go.mod h1:6rpuAdCZL397s3pYoYcLgu1mIlRU8Am5FuJP05cCM98=
github.com/envoyproxy/go-control-plane v0.9.9-0.20201210154907-fd9021fe5dad/go.mod h1:cXg6YxExXjJnVBQHBLXeUAgxn2UodCpnH306RInaBQk=
-github.com/envoyproxy/go-control-plane v0.9.9-0.20210512163311-63b5d3c536b0/go.mod h1:hliV/p42l8fGbc6Y9bQ70uLwIvmJyVE5k4iMKlh8wCQ=
+github.com/envoyproxy/go-control-plane v0.10.2-0.20220325020618-49ff273808a1/go.mod h1:KJwIaB5Mv44NWtYuAOFCVOjcI94vtpEz2JU/D2v6IjE=
github.com/envoyproxy/protoc-gen-validate v0.1.0/go.mod h1:iSmxcyjqTsJpI2R4NaDN7+kN2VEUnK/pcBlmesArF7c=
github.com/ghodss/yaml v1.0.0/go.mod h1:4dBDuWmgqj2HViK6kFavaiC9ZROes6MMH2rRYeMEF04=
github.com/golang/glog v0.0.0-20160126235308-23def4e6c14b/go.mod h1:SBH7ygxi8pfUlaOkMMuAQtPIUF8ecWP5IEl/CR7VP2Q=
@@ -28,14 +31,18 @@
github.com/golang/protobuf v1.4.0/go.mod h1:jodUvKwWbYaEsadDk5Fwe5c77LiNKVO9IDvqG2KuDX0=
github.com/golang/protobuf v1.4.1/go.mod h1:U8fpvMrcmy5pZrNK1lt4xCsGvpyWQ/VVv6QDs8UjoX8=
github.com/golang/protobuf v1.4.2/go.mod h1:oDoupMAO8OvCJWAcko0GGGIgR6R6ocIYbsSw735rRwI=
-github.com/golang/protobuf v1.4.3 h1:JjCZWpVbqXDqFVmTfYWEVTMIYrL/NPdPSCHPJ0T/raM=
github.com/golang/protobuf v1.4.3/go.mod h1:oDoupMAO8OvCJWAcko0GGGIgR6R6ocIYbsSw735rRwI=
+github.com/golang/protobuf v1.5.0/go.mod h1:FsONVRAS9T7sI+LIUmWTfcYkHO4aIWwzhcaSAoJOfIk=
+github.com/golang/protobuf v1.5.2 h1:ROPKBNFfQgOUMifHyP+KYbvpjbdoFNs+aK7DXlji0Tw=
+github.com/golang/protobuf v1.5.2/go.mod h1:XVQd3VNwM+JqD3oG2Ue2ip4fOMUkwXdXDdiuN0vRsmY=
github.com/google/go-cmp v0.2.0/go.mod h1:oXzfMopK8JAjlY9xF4vHSVASa0yLyX7SntLO5aqRK0M=
github.com/google/go-cmp v0.3.0/go.mod h1:8QqcDgzrUqlUb/G2PQTWiueGozuR1884gddMywk6iLU=
github.com/google/go-cmp v0.3.1/go.mod h1:8QqcDgzrUqlUb/G2PQTWiueGozuR1884gddMywk6iLU=
github.com/google/go-cmp v0.4.0/go.mod h1:v8dTdLbMG2kIc/vJvl+f65V22dbkXbowE6jgT/gNBxE=
-github.com/google/go-cmp v0.5.0 h1:/QaMHBdZ26BB3SSst0Iwl10Epc+xhTquomWX0oZEB6w=
github.com/google/go-cmp v0.5.0/go.mod h1:v8dTdLbMG2kIc/vJvl+f65V22dbkXbowE6jgT/gNBxE=
+github.com/google/go-cmp v0.5.5/go.mod h1:v8dTdLbMG2kIc/vJvl+f65V22dbkXbowE6jgT/gNBxE=
+github.com/google/go-cmp v0.5.6 h1:BKbKCqvP6I+rmFHt06ZmyQtvB8xAkWdhFyr0ZUNZcxQ=
+github.com/google/go-cmp v0.5.6/go.mod h1:v8dTdLbMG2kIc/vJvl+f65V22dbkXbowE6jgT/gNBxE=
github.com/google/uuid v1.1.2/go.mod h1:TIyPZe4MgqvfeYDBFedMoGGpEw/LqOeaOT+nhxU+yHo=
github.com/grpc-ecosystem/grpc-gateway v1.16.0/go.mod h1:BDjrQk3hbvj6Nolgz8mAMFbcEtjT1g+wF4CSlocrBnw=
github.com/pmezard/go-difflib v1.0.0/go.mod h1:iKH77koFhYxTK1pcRnkKkqfTogsbg7gZNVY4sRDYZ/4=
@@ -43,6 +50,7 @@
github.com/rogpeppe/fastuuid v1.2.0/go.mod h1:jVj6XXZzXRy/MSR5jhDC/2q6DgLz+nrA6LYCDYWNEvQ=
github.com/stretchr/objx v0.1.0/go.mod h1:HFkY916IF+rwdDfMAkV7OtwuqBVzrE8GR6GFx+wExME=
github.com/stretchr/testify v1.5.1/go.mod h1:5W2xD1RspED5o8YsWQXVCued0rvSQ+mT+I5cxcmMvtA=
+github.com/stretchr/testify v1.7.0/go.mod h1:6Fq8oRcR53rry900zMqJjRRixrwX3KX962/h/Wwjteg=
go.opentelemetry.io/proto/otlp v0.7.0/go.mod h1:PqfVotwruBrMGOCsRd/89rSnXhoiJIqeYNgFYFoEGnI=
golang.org/x/crypto v0.0.0-20190308221718-c2843e01d9a2/go.mod h1:djNgcEr1/C05ACkg1iLfiJU5Ep61QUkGW8qpdssI0+w=
golang.org/x/crypto v0.0.0-20200622213623-75b288015ac9/go.mod h1:LzIPMQfyMNhhGPhUkYOs5KpL4U8rLKemX1yGLhDgUto=
@@ -69,8 +77,9 @@
golang.org/x/sys v0.0.0-20190215142949-d0b11bdaac8a/go.mod h1:STP8DvDyc/dI5b8T5hshtkjS+E42TnysNCUPdjciGhY=
golang.org/x/sys v0.0.0-20190412213103-97732733099d/go.mod h1:h1NjWce9XRLGQEsW7wpKNCjG9DtNlClVuFLEZdDNbEs=
golang.org/x/sys v0.0.0-20200323222414-85ca7c5b95cd/go.mod h1:h1NjWce9XRLGQEsW7wpKNCjG9DtNlClVuFLEZdDNbEs=
-golang.org/x/sys v0.0.0-20200930185726-fdedc70b468f h1:+Nyd8tzPX9R7BWHguqsrbFdRx3WQ/1ib8I44HXV5yTA=
golang.org/x/sys v0.0.0-20200930185726-fdedc70b468f/go.mod h1:h1NjWce9XRLGQEsW7wpKNCjG9DtNlClVuFLEZdDNbEs=
+golang.org/x/sys v0.0.0-20210119212857-b64e53b001e4 h1:myAQVi0cGEoqQVR5POX+8RR2mrocKqNN1hmeMqhX27k=
+golang.org/x/sys v0.0.0-20210119212857-b64e53b001e4/go.mod h1:h1NjWce9XRLGQEsW7wpKNCjG9DtNlClVuFLEZdDNbEs=
golang.org/x/text v0.3.0/go.mod h1:NqM8EUOU14njkJ3fqMW+pc6Ldnwhi/IjpwHt7yyuwOQ=
golang.org/x/text v0.3.3 h1:cokOdA+Jmi5PJGXLlLllQSgYigAEfHXJAERHVMaCc2k=
golang.org/x/text v0.3.3/go.mod h1:5Zoc/QRtKVWzQhOtBMvqHzDpF6irO9z98xDceosuGiQ=
@@ -105,10 +114,14 @@
google.golang.org/protobuf v1.23.0/go.mod h1:EGpADcykh3NcUnDUJcl1+ZksZNG86OlYog2l/sGQquU=
google.golang.org/protobuf v1.23.1-0.20200526195155-81db48ad09cc/go.mod h1:EGpADcykh3NcUnDUJcl1+ZksZNG86OlYog2l/sGQquU=
google.golang.org/protobuf v1.24.0/go.mod h1:r/3tXBNzIEhYS9I1OUVjXDlt8tc493IdKGjtUeSXeh4=
-google.golang.org/protobuf v1.25.0 h1:Ejskq+SyPohKW+1uil0JJMtmHCgJPJ/qWTxr8qp+R4c=
google.golang.org/protobuf v1.25.0/go.mod h1:9JNX74DMeImyA3h4bdi1ymwjUzf21/xIlbajtzgsN7c=
+google.golang.org/protobuf v1.26.0-rc.1/go.mod h1:jlhhOSvTdKEhbULTjvd4ARK9grFBp09yW+WbY/TyQbw=
+google.golang.org/protobuf v1.26.0/go.mod h1:9q0QmTI4eRPtz6boOQmLYwt+qCgq0jsYwAQnmE0givc=
+google.golang.org/protobuf v1.27.1 h1:SnqbnDw1V7RiZcXPx5MEeqPv2s79L9i7BJUlG/+RurQ=
+google.golang.org/protobuf v1.27.1/go.mod h1:9q0QmTI4eRPtz6boOQmLYwt+qCgq0jsYwAQnmE0givc=
gopkg.in/check.v1 v0.0.0-20161208181325-20d25e280405/go.mod h1:Co6ibVJAznAaIkqp8huTwlJQCZ016jof/cbN4VW5Yz0=
gopkg.in/yaml.v2 v2.2.2/go.mod h1:hI93XBmqTisBFMUTm0b8Fm+jr3Dg1NNxqwp+5A1VGuI=
gopkg.in/yaml.v2 v2.2.3/go.mod h1:hI93XBmqTisBFMUTm0b8Fm+jr3Dg1NNxqwp+5A1VGuI=
+gopkg.in/yaml.v3 v3.0.0-20200313102051-9f266ea9e77c/go.mod h1:K4uyk7z7BCEPqu6E+C64Yfv1cQ7kz7rIZviUmN+EgEM=
honnef.co/go/tools v0.0.0-20190102054323-c2f93a96b099/go.mod h1:rf3lG4BRIbNafJWhAfAdb/ePZxsR/4RtNHQocxwk9r4=
honnef.co/go/tools v0.0.0-20190523083050-ea95bdfd59fc/go.mod h1:rf3lG4BRIbNafJWhAfAdb/ePZxsR/4RtNHQocxwk9r4=
$echo $?
1
```


我们看到，**如果有更新的包，该命令还会返回一个非0值(echo $?)以作为提示**。

- go.mod中增加godebug指示符(directive)

从Go 1.23版本开始，你可以在go.mod/go.work文件中使用godebug指示符，其语法格式如下(包括单行和块状)：

```
godebug default=go1.21
godebug (
panicnil=1
asynctimerchan=0
)
```


default: 是一个特殊的键，用于指定未明确设置的GODEBUG值应该采用哪个Go版本的默认值，例如: default=go1.21。除default键之外的其他键值对则用于明确设置特定的GODEBUG选项。

Go支持多种方式设置GODEBUG，包括在使用go命令时伴随使用GODEBUG环境变量、使用go.mod中的godebug以及在源文件中使用//go:debug指示符。它们之间的优先级关系是：**go.mod中的设置优先于Go工具链的默认值，但可以被源文件中的//go:debug指令覆盖**。

更多关于godebug机制的内容，大家可以查看[godebug的官方参考文档](https://go.dev/doc/godebug)。

## 3. 编译器与运行时

- 开启PGO情况下，编译速度的提升

Go从[1.20版本](https://tonybai.com/2023/02/08/some-changes-in-go-1-20/)引入PGO优化技术，到目前PGO已经得到了进一步的优化，但PGO的引入也带来了编译时间的显著开销，对于一些大型项目，在开启PGO的情况下，编译时间甚至增加了100%。Go 1.23版本针对PGO的构建成本做了大幅优化，使得PGO带来的编译开销仅仅相对于非PGO增加个位数级百分比的变化。

- 限制对linkname的使用

在Go语言中，//go:linkname指令可以用来链接到标准库或其他包中的未导出符号。比如我们想访问runtime包中的一个未导出函数，例如runtime.nanotime。这个函数返回当前时间的纳秒数。我们可以通过//go:linkname指令链接到这个符号。下面我用一个示例来演示一下这点：

```
// go1.23-examples/compiler/golinkname/main.go
package main
import (
"fmt"
_ "unsafe" // 必须导入 unsafe 包以使用 //go:linkname
)
// 声明符号链接
//
//go:linkname nanotime runtime.nanotime
func nanotime() int64
func main() {
// 调用未导出的 runtime.nanotime 函数
fmt.Println("Current time in nanoseconds:", nanotime())
}
```


运行该示例：

```
$go run main.go
Current time in nanoseconds: 397501409223055
```


这种做法一般不推荐，因为它可能导致程序不稳定，并且未来版本的Go可能会改变内部实现（比如nanotime被改名或被删除），破坏你的代码。

Go团队意识到了这种不规范的行为，在Go 1.23中，Go团队明确了//go:linkname的使用规范。

Go 1.23链接器现在禁止使用//go:linkname指令来引用标准库中未标记有//go:linkname的内部符号，并且链接器也禁止从汇编代码中引用这些符号。

不过，为了向后兼容，在一些大型开源代码库中发现的存量//go:linkname用法仍然受支持，为此，Go在标准库和runtime库中为支持linkname的函数增加了//go:linkname标记，以上面示例中的runtime.nanotime为例，在Go 1.23中其源码注释如下：

```
// runtime/time_nofake.go
// Exported via linkname for use by time and internal/poll.
//
// Many external packages also linkname nanotime for a fast monotonic time.
// Such code should be updated to use:
//
// var start = time.Now() // at init time
//
// and then replace nanotime() with time.Since(start), which is equally fast.
//
// However, all the code linknaming nanotime is never going to go away.
// Do not remove or change the type signature.
// See go.dev/issue/67401.
//
//go:linkname nanotime
//go:nosplit
func nanotime() int64 {
return nanotime1()
}
```


对于没有标记//go:linkname的标准库内部符号，要在外部通过go:linkname引用默认都将被禁止。不过，考虑到调试和实验目的，你也可以通过使用-checklinkname=0这个链接器命令行选项来禁用这个检查：

```
$go env -w GOFLAGS=-ldflags=-checklinkname=0 // 全局生效
```


## 4. 标准库

标准库的变化永远是大头儿，这里仅列出重要的变化。

### 4.1 Timer/Ticker变化

timer/ticker的stop/reset问题一直困扰Go团队，Go 1.23的两个重要fix期望能从根本上解决这个问题：

- Timer/Ticker的GC不再需要Stop(
[issue 61542](https://github.com/golang/go/issues/61542))

程序不再引用的Timer和Ticker将立即有资格进行垃圾回收，即使它们的Stop方法尚未被调用。Go的早期版本直到触发后才会收集未停止的Timer，并

且从未收集未停止的Ticker。

- Timer/Ticker的Stop/Reset后不再接收旧值(
[issue 37196](https://github.com/golang/go/issues/37196))

与Timer或Ticker关联的计时器channel现在改为无缓冲的了，即容量为0 。此更改的主要效果是Go现在保证任何对Reset或Stop方法的调用，调用之前不会发送或接收任何陈旧值。 Go的早期版本使用带有缓冲区的channel，因此很难正确使用Reset和Stop。此更改的一个明显效果是计时器channel的len和cap现在返回0而不是1，这可能会影响轮询长度以确定是否在计时器channel上接收的程序。通过GODEBUG设置asynctimerchan=1可恢复异步通道行为。

### 4.2 structs包

Go语言的结构体布局实际上受到平台布局和对齐规则的严格限制，这种限制可能导致在某些平台上出现权衡或潜在问题，同时阻碍了可以节省内存和提高垃圾回收性能的字段重排优化。

为了解决某些平台(如WASM和ppc64le)的特殊对齐需求，提高跨平台兼容性，并为未来的结构体优化留下空间，[David Chase提案增加HostLayout指示符类型](https://github.com/golang/go/issues/66408)。

具体来说就是引入一个新的包，包含一个零size的类型HostLayout：

```
// $GOROOT/src/structs/hostlayout.go
type HostLayout struct {
_ hostLayout // prevent accidental conversion with plain struct{}
}
```


该类型可用作结构体字段来控制编译器对结构体类型的布局方式。被标记为HostLayout的结构体字段将按照主机的C ABI期望的方式进行内存布局。HostLayout不会影响包含它的结构体内部其他结构体类型字段的布局，也不会影响包含它的结构体所在的更上层结构体的布局。按照惯例，HostLayout应该作为一个名为”_”的字段类型，放在结构体定义的开始位置，比如：

```
type T struct {
_ structs.HostLayout
x, y int
}
```


注：关于结构体对齐，可以参考

[《Go语言第一课》]专栏的[第17讲：复合数据类型：用结构体建立对真实世界的抽象]。

### 4.3 新增unique包、iter包、函数迭代器相关函数

Go标准库还新增了unique包，并在maps、slices中增加了函数迭代器的实用函数，具体内容大家可以参考我之前的文章《[Go 1.23新特性前瞻](https://tonybai.com/2024/05/30/go-1-23-foresight/)》。

至于关于新增的iter包的用法，可以参考《[Go 1.23中的自定义迭代器与iter包](https://tonybai.com/2024/06/24/range-over-func-and-package-iter-in-go-1-23/)》一文，这里就不赘述了！

## 5. 小结

Go 1.23版本在Russ Cox的带领下取得了丰硕的成果，为开发者带来了众多令人瞩目的语言特性、工具链优化以及编译器和运行时改进。

然而，随着Russ Cox的卸任，从Go 1.24版本开始，我们将迎来新一代Go决策层的领导。他们将如何引领Go语言的未来发展？是否会带来新的方向和变化？让我们拭目以待，共同见证Go语言的持续进化。

不过这里还要提醒各位Go开发者，在升级Go 1.23版本时务必注意潜在的向后兼容性问题，尤其是//go:linkname、time.Timer/Ticker的变化可能带来的影响。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go1.23-examples)下载。

## 6. 参考资料

[What’s new in Go 1.23](https://changelog.com/gotime/325)– https://changelog.com/gotime/325[Go 1.23 Release Notes](https://go.dev/doc/go1.23)– https://go.dev/doc/go1.23[Go 1.23 is released](https://go.dev/blog/go1.23)– https://go.dev/blog/go1.23[Go spec](https://go.dev/ref/spec)– https://go.dev/ref/spec

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论