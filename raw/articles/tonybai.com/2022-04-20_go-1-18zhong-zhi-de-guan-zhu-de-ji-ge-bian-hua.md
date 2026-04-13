---
title: Go 1.18中值得关注的几个变化
url: https://tonybai.com/2022/04/20/some-changes-in-go-1-18/
published: '2022-04-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.18中值得关注的几个变化

![](../../assets/dae6547a519bb5df.png)


[本文永久链接](https://tonybai.com/2022/04/20/some-changes-in-go-1-18) – https://tonybai.com/2022/04/20/some-changes-in-go-1-18

从3月23日开始，我居家办公了20+天。这期间我本来是应该有时间写下这篇综述类文章的，但是封了两天后，抢菜、带娃的事情就开始困扰着我。我实在没有下笔写下这篇文章的心思。4月13日终于解封了，上班后的气象就是不一样，人也精神了很多，于是这篇文章也被提上了日程。希望新冠疫情早日结束吧，希望每个人都能在晴朗的户外享受那春日的暖意。


2022年3月15日，Go团队在官方博客上官宣了[Go 1.18正式版的发布](https://tonybai.com/2022/03/16/go-1-18-released)。Go 1.18这个网红版本终于落地了。泛型的加入让Go 1.18成为继[Go 1.0(首个正式版)](https://go.dev/blog/go1)、[Go 1.5(实现自举、去C代码、新版GC)](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)、[Go 1.11(引入Go module)](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)版本之后的又一**里程碑版本**。

泛型是Go语言开源以来**最大的语法特性变化**，其改动和影响都很大，Go核心团队尽管很努力了，但Go 1.18正式版本的发布时间还是延迟了一个月。不过好消息是加入泛型语法的Go 1.18继续保持了[Go1兼容性](https://go.dev/doc/go1compat)，这本身就是Go团队的胜利，同样也是Go社区的幸运。

相较于之前的版本，Go 1.18版本改动很大，[bug略多](https://github.com/golang/go/milestone/254)。好在发布一个月后，各种喧嚣都归于安静。笔者写稿时，[Go 1.18.1已经发布](https://groups.google.com/g/golang-announce/c/oecdBNLOml8)，修正了许多问题，当然也包括一些与Go泛型有关的问题。

下面我们就来看看**Go 1.18版本中值得关注的变化**，我这里使用的版本为Go 1.18.1。

我们就先从泛型说起。

### 一. Go语法变化

#### 1. 泛型：史上最复杂Go语法特性

以往Go发布大版本，Go语法变化一栏的内容总是寥寥无几，甚至是因没有变化而一笔带过。

更有甚者，从Go1.0到Go 1.17的语法变化屈指可数：

- Go 1.1版本：增加
[“method value”语法](https://go.dev/ref/spec#Method_values)； - Go 1.2版本：增加
[Full slice expression](https://go.dev/ref/spec#Slice_expressions)：a[low: high: max]； [Go 1.4版本](https://tonybai.com/2014/11/04/some-changes-in-go-1-4/)：新增for range x {…}形式的for-range语法；[Go 1.5版本](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)：支持省略map类型字面量（literal）中的key的类型；[Go 1.9版本](https://tonybai.com/2017/07/14/some-changes-in-go-1-9/)：新增了[type alias语法](https://go.dev/ref/spec#Type_declarations)；[Go 1.13版本](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)：增加以0b或0B开头的二进制数字字面量、以“0o”或“0O”开头的八进制数字字面量、以0x或0X开头是的十六进制形式的浮点数字面量以及支持在数字字面量中通过数字分隔符“_”提高可读性；[Go 1.17版本](https://tonybai.com/2021/08/17/some-changes-in-go-1-17)：支持从切片到数组指针的转换。

我们看到，十年来，Go在纯语法层面的变化只有上面这么几个。而Go 1.18引入的泛型的复杂性足以超过上述版本的语法变化之和。面对新增加的泛型特性，即便是有着多年Go编程经验的Gopher，也会有一种**“二次学艺”**的感觉。这是因为**Go泛型是Go诞生以来最复杂、最难读和理解的语法特性**，当然泛型的复杂性不仅仅对Go语言生效，对其他具有泛型语法特性的编程语言来说，泛型也都是最复杂的语法。有志者可以去挑战一下C++的泛型：template。还有那本尤为烧脑的Andrei Alexandrescu 的[《C++设计新思维: 泛型编程与设计模式之应用》](https://book.douban.com/subject/1119904/)，英文书名是[《Modern C++ Design: Generic Programming and Design Patterns Applied》](https://book.douban.com/subject/1755195/)。

![](../../assets/ff029cccda9b1dd1.jpg)


同样也是因为泛型的复杂性，Go团队在[Go 1.18的发布说明文档](https://go.dev/doc/go1.18)中保留了在将来的版本中因修复Go泛型bug而对Go 1.18版本编译的程序带来破坏的权力。当然Go团队也承诺将尽可能地减少任何此类破坏，但不能保证此类破坏为零。

另外，Go 1.18的泛型实现并非完全版，有很多使用上的约束。这些约束很大可能将在后续的Go版本中逐步取消掉。并且Go 1.18中的实现与[Type Parameter Proposal的design文档](https://go.googlesource.com/proposal/+/refs/heads/master/design/43651-type-parameters.md)有一定差异，Go官方建议以[Go语言的规范](https://go.dev/ref/spec)为准。

#### 2. 泛型的主要语法点

前面也说了，Go泛型是Go开源以来在语法层面最大的一次变动，Go泛型的最后一版技术提案长达数十页，我们要是把其中的细节都展开细讲，那都可以自成一本小册子了。在这篇综述类文章中，我仅对Go泛型的主要语法点做简要说明。在日后文章中，我们再深入到泛型的语法细节，做逐一细致剖析。

关于Go泛型的主要语法点，其实在Go官博的[“Go泛型介绍”](https://tonybai.com/2022/03/25/intro-generics)中都有提及：

泛型在Go语言中增加了三个新的重要内容：

- 函数和类型新增对
**类型形参(type parameters)**的支持。 - 将接口类型定义为类型集合，包括没有方法的接口类型。
- 支持类型推导，大多数情况下，调用泛型函数时可省略类型实参(type arguments)。

下面我们分别来看看。

##### 类型形参(type parameter)

类型形参是在函数声明、方法声明的receiver部分或类型定义的类型参数列表中，声明的（非限定）类型名称。类型参数在声明中充当了一个未知类型的占位符（placeholder），在泛型函数或泛型类型实例化时，类型形参会被一个类型实参(type argument)替换。

为了让你更好地理解类型参数究竟如何声明，它又起到了什么作用，我们以函数为例，对普通函数的参数与泛型函数的类型参数作一下对比：

我们知道，普通函数的参数列表是这样的：

```
func Foo(x, y aType, z anotherType)
```


这里，x, y, z是形参（parameter）的名字，也就是变量，而aType，anotherType是形参的类型，也就是类型。

我们再来看一下泛型函数的类型参数（type parameter）列表：

```
func GenericFoo[P aConstraint, Q anotherConstraint](x,y P, z Q)
```


这里，P，Q是类型形参的名字，也就是类型，aConstraint，anotherConstraint代表类型参数的约束（constraint），我们可以理解为对类型参数可选值的一种限定。

在类型参数列表中修饰类型参数的就是约束（constraint）。那什么是约束呢？我们继续往下看。

##### 约束（constraint）

约束（constraint）规定了一个类型实参（type argument）必须满足的条件要求。如果某个类型满足了某个约束规定的所有条件要求，那么它就是这个约束修饰的类型形参的一个合法的类型实参。

在Go泛型中，我们**使用interface类型来定义约束**。为此，Go接口类型的定义也进行了扩展，我们既可以声明接口的方法集合，也可以声明可用作类型实参的类型列表。

下面是一个约束定义与使用的示例：

```
type C1 interface {
~int | ~int32
M1()
}
type T struct{}
func (T) M1() {
}
type T1 int
func (T1) M1() {
}
func foo[P C1](t P)() {
}
func main() {
var t1 T1
foo(t1)
var t T
foo(t) // 编译器报错：T does not implement C1
}
```


在这段代码中，C1是我们定义的约束，它声明了一个方法M1，以及两个可用作类型实参的类型(~int | ~int32)。我们看到，类型列表中的多个类型实参类型用“|”分隔。

在这段代码中，我们还定义了两个自定义类型T和T1，两个类型都实现了M1方法，但T类型的底层类型为struct{}，而T1类型的底层类型为int，这样就导致了虽然T类型满足了约束C1的方法集合，但类型T因为底层类型并不是int或int32而不满足约束C1，这也就会导致foo(t)调用在编译阶段报错。不过，我这里还要建议你：做约束的接口类型与做传统接口的接口类型最好要分开定义，除非约束类型真的既需要方法集合，也需要类型列表。

为了让大家更好理解这种对接口类型的扩展，Go引入了类型集合(type set)来解释这一切。[“Go泛型介绍”](https://tonybai.com/2022/03/25/intro-generics)中有对type set的图解，这里就不赘述了，大家可以点击链接移步阅读。

##### 类型具化(instantiation)与类型推导(type inference)

像上面例子中main函数对foo(t1)的调用就利用到了类型具化和类型推导两个特性。

foo是一个泛型函数，它的函数声明中带有一个由C1约束的类型形参P，而用类型实参T1初始化P的过程就是类型具化。不过大家也注意到了，我们没有使用：foo[T1](t1)，而是省略了显式对P进行初始化，直接使用了foo(t1)，这就是Go类型推导带来的便利。Go编译器会根据传入的实参的类型，进行类型实参(type argument)的自动推导。自动类型推导使得人们在编写调用泛型函数的代码时可以使用一种更为自然的风格。

##### 泛型类型(generic type)

除了函数可以携带类型参数变身为“泛型函数”外，类型也可以拥有类型形参而化身为“泛型类型”，比如下面代码就定义了一个向量泛型类型：

```
type Vector[T any] []T
```


这是一个带有类型参数的类型定义，类型参数位于类型名的后面，同样用方括号括起。在类型定义体中可以引用类型参数列表中的参数名（比如T）。类型参数同样拥有自己的约束，如上面代码中的any。

在Go 1.18中，any是interface{}的别名，也是一个预定义标识符，使用any作为类型参数的约束，代表没有任何约束。关于如何使用any以及使用any的注意事项，请移步到我之前的文章[《切换到Go 1.18后的第一件事：将interface{}全部替换为any》](https://tonybai.com/2021/12/18/replace-empty-interface-with-any-first-after-switching-to-go-1-18)。

下面是另一个泛型类型的定义：

```
type Tree[T interface{}] struct {
left, right *Tree[T]
value T
}
func (t *Tree[T]) Lookup(x T) *Tree[T] { ... }
var stringTree Tree[string]
```


在上面这个例子中，泛型类型Tree存储了类型参数T的值。泛型类型也可以有方法，比如本例中的Lookup。为了使用一个泛型类型，它必须被实例化，比如：Tree[string]是一个用类型实参string来实例化Tree的例子。

##### 当前泛型实现的不足

泛型对Go项目的影响是方方面面的，在一个版本迭代周期内将泛型的全部特性都实现的确难了一些。因此，Go 1.18当前的Go泛型实现尚不完整，尚有限制，根据Go 1.18的发布说明文档，限制包括下面几点：

- Go编译器不能处理泛型函数或方法中的类型声明，Go团队希望在未来的版本中提供对该功能的支持。

```
func GenericsFoo[T any](s T) T {
type bar int // type declarations inside generic functions are not currently supported
var a bar
println(a)
return s
}
```


- Go编译器不支持预定义的函数real、imag和complex处理泛型类型实参。Go团队希望在未来的版本中取消这一限制。

```
package main
import (
"golang.org/x/exp/constraints"
)
func GenericsFoo[T constraints.Complex](s T) T {
n := real(s) // s (variable of type T constrained by constraints.Complex) not supported as argument to real for go1.18 (see issue #50937
println(n)
i := complex(s, s) // invalid argument: arguments have type T, expected floating-point
_ = i
return s
}
func main() {
var i = complex(1.0, 2.0) // 1+2i
GenericsFoo(i)
}
```


- Go编译器只支持在参数类型为P的值x上调用方法m，前提是：m必须是由P的约束接口显式声明的。同样地，method valuex.m和method expression P.m也只有在P明确声明了m的情况下才会被支持。即使P类型集合中的所有类型都实现了m，但如果没有显示声明m，那么也不支持在x上调用m。Go团队希望在未来的版本中删除这一限制。

```
package main
type C interface {
T | T1 // T和T1都实现了M1方法
}
func GenericsFoo[P C](p P) {
p.M1() // p.M1 undefined (type P has no field or method M1)
}
type T struct{}
func (T) M1() {}
type T1 struct{}
func (T1) M1() {}
func main() {
GenericsFoo(T{})
}
```


- Go编译器目前不支持访问一个结构字段x.f，其中x是类型参数类型，即使类型参数的类型集合中的所有类型都有一个字段f。Go团队可能会在未来的版本中取消这一限制。

```
package main
type C interface {
T | T1 // T和T1的类型定义中都包含名为Name的字段
}
func GenericsFoo[P C](p P) {
_ = p.Name // p.Name undefined (type P has no field or method Name)
}
type T struct {
Name string
}
type T1 struct {
Name string
}
func main() {
GenericsFoo(T{})
}
```


- 目前Go编译器不允许将类型参数或指向类型参数的指针作为结构体类型嵌入字段(未命名字段)。同样，也不允许在一个接口类型中嵌入一个类型参数。目前Go团队还不确定这些限制在未来版本是否会被放开。

```
package main
type F[T any, P any] struct {
Name string
*T //embedded field type cannot be a (pointer to a) type parameter
P // embedded field type cannot be a (pointer to a) type parameter
}
type MyInterface interface{}
type GenericsInterface[I MyInterface] interface {
M1()
I // cannot embed a type parameter
}
func main() {
var f F[string, string]
_ = f
}
```


- Go编译器不支持在包含1个以上类型元素的union类型定义中包含一个具有非空方法集的接口类型。这是否会在未来版本中被允许，Go团队目前还不确定。

```
package main
type MyInterface interface {
M1()
}
type GenericsInterface interface {
~int | MyInterface | float64 // cannot use main.MyInterface in union (main.MyInterface contains methods)
}
func main() {
}
```


另外一个大家广为关注的是，普通类型的方法声明中不支持类型参数：

```
package main
type F struct{}
func (F) M1[T any](t T){} // syntax error: method must have no type parameters
func main() {
var f F[string]
f.M1("hello")
}
```


不过这不是实现层面的限制，而是Go泛型技术草案就是这么定的。至于后续是否能支持在方法中使用类型参数还不确定。不过上述问题可以通过带有类型参数的泛型类型来“缓解”。

泛型类型可以有自己的方法，在泛型类型的方法声明中receiver中使用与类型声明相同的类型参数，这个类型参数也可以在方法的普通参数列表中使用，如下面例子：

```
package main
type F[T any] struct{}
func (F[T]) M1(t T) {} // ok
func main() {
var f F[string]
f.M1("hello")
}
```


##### 官方维护的泛型包

Go 1.18可以说仅提供了一个Go泛型的最小版本，除了语法，外加两个预定义类型：comparable和any。原本想在标准库中加入的constraints、slices和maps泛型包，因Go老父亲[Rob Pike的一条comment](https://github.com/golang/go/issues/48918)而被暂时搁置了。Rob Pike的理由很简单，[Go泛型](https://tonybai.com/2021/04/07/go-generics-use-type-sets-to-remove-type-keyword/)是Go诞生以来最大的一次语言变化，Go 1.18版本承载了太多的change，容易出错。并且Go核心开发团队也没有使用新泛型的经验，他建议Go核心开发团队应该多等待、观察和学习，不要把步子迈得太大，[Go应该按照自己的节奏稳步前进](https://tonybai.com/2021/10/28/expectations-for-generics-in-go-1.18)。

于是前面提到的三个包被放在了golang.org/x/exp下面了：

```
golang.org/x/exp/constraints
golang.org/x/exp/slices
golang.org/x/exp/maps
```


待时机成熟，这些包会像当年http2包一样进入到Go标准库中。

##### Go工具链对泛型语法的支持情况

Go泛型出炉后，Go官方维护的Go工具链上的工具都基本确定了支持泛型语法的计划。到Go 1.18发布时，gofmt/goimports、go vet、gopls(从v0.8.1版本开始支持)都实现了对泛型的支持。

不过这里除了gofmt是与Go安装包一起发布的，其他工具都需要自己安装和升级到最新版本。否则一旦使用到泛型语法或新增的像any、comparable等预定义标识符，你的编辑器就会给出各种错误提示。

如果你和我一样使用[vim+vim-go+goimports+gopls](https://tonybai.com/2016/09/08/upgrade-vim-go/)，那么要想编辑器支持go 1.18，可使用下面命令升级工具版本来支持go 1.18的泛型：

```
$go install golang.org/x/tools/cmd/goimports@latest
$go install golang.org/x/tools/gopls@latest
```


当然Go社区还有很多工具尚未及时赶上步伐，这个要给Go社区一定的时间。

关于Go泛型语法的细节以及实现原理，我会逐渐在后续文章中进行专门讲解。

讲完泛型这个大部头儿后，接下来，我们再来看看Go编译器与Go module的变化。

### 二. Go编译器与Go module变化

#### 1. 修正的语法bug

我们知道在Go函数内声明变量后，如果未使用，Go编译器会报错。但Go 1.18版本之前，[Go编译器对于下面例子中的变量p是不会报错的](https://github.com/golang/go/issues/49214)，即便在main中没有使用。

Go 1.18修正了这个问题，如果用Go 1.18编译该例子，会出现注释中的编译器错误。

```
package main
func main() {
p := true // go 1.18会报错：p declared but not used，但Go 1.18之前的版本不会。
func() {
p = true
}()
}
```


同时，gopls和go vet也都会针对上述问题给出错误提示。

#### 2. 在AMD64平台上引入architectural level

众所周知，Go语言在目标代码的优化上还有很大的提升空间。在Go 1.18版本中，Go引入一个算是优化的措施，即[在AMD64平台上引入architectural level的概念](https://github.com/golang/go/wiki/MinimumRequirements#amd64)。level越高，可用指令越新，编译出的使用新指令的代码的性能可能有一定提升。

Go 1.18通过GOAMD64这个环境变量来指示编译器采用的level，默认使用v1版本。这个版本在生产的代码中使用了所有x86-64 cpu都支持的指令。说白了，就是使用最基本的指令，兼容性好，但性能也是最差的。

GOAMD64环境变量的另外三个候选值为v2、v3、v4。版本越高，兼容性越差，但性能可能因使用新指令而得到提升。

- GOAMD64=v2: 所有v1版指令, 外加CMPXCHG16B, LAHF, SAHF, POPCNT, SSE3, SSE4.1, SSE4.2, SSSE3；
- GOAMD64=v3: 所有v2版指令, 外加AVX, AVX2, BMI1, BMI2, F16C, FMA, LZCNT, MOVBE, OSXSAVE；
- GOAMD64=v4: 所有v3版指令, 外加AVX512F, AVX512BW, AVX512CD, AVX512DQ, AVX512VL。

在优化的道路，Go团队一直在努力，这不Go编译器现在还可以inline带有range循环或带有label的循环语句的函数了。

#### 3. 丰富了SBOM信息

这些年来，关于软件供应链的安全问题频发，软件供应链已然成为IT安全领域的一个热点。Go作为云原生平台、中间件以及服务的头部开发语言，其自身安全性以及构建出的软件的安全性就变得至关重要了。Go在安全方面的投入也是逐渐增大，手段也在逐渐增多与丰富。SBOM(软件物料清单)作为缓解软件供应链攻击的重要防护手段，Go在1.13版本就提供了相关支持，在Go 1.18版本中，Go更是丰富了提供的SBOM信息，这方面的详情可参见之前的文章：[《聊聊Go语言的软件供应链安全》](https://tonybai.com/2022/03/14/software-supply-chain-security-in-go)。

#### 4. Go泛型给compiler带来的负面影响

Go泛型的引入增加了Go语言的表达力，但也对Go编译器带来了不小的负面影响，其中最大的影响就是编译速度。从Go 1.18发布说明文档来看，Go 1.18的编译速度要比Go 1.17版本下降15%，并且即便你在代码中完全没有使用泛型语法，这个性能下降也是有的。所以[这也是Go团队在Go 1.19中要重点解决的问题](https://github.com/golang/go/issues/49569)。

#### 5. go module变化

从[Go 1.16版本](https://tonybai.com/2021/02/25/some-changes-in-go-1-16)开始，Go module已进入成熟期。不过依然有一些小问题需要修复，其中一个就是go.mod和go.sum究竟哪个命令有权修改。Go 1.18明确了能修改go.mod, go.sum的命令只有三个：go get, go mod tidy和go mod download。这样开发人员就可以放心的在项目根目录下执行go工具链提供的其他命令了。

#### 6. 引入Go workspace(工作区)

Go module的引入大大改善了Go包依赖与构建问题。但目前Go module在软件协作开发过程中仍存在导致体验差的两个问题，并且这两个问题在原有go module机制下面很难得到根本解决。这两个问题是：

- 对依赖包进行自行修改，并基于本地修改后的依赖包进行构建；
- 依赖本地尚未发布的module。

原有的go module replace机制在协作的情况下，体验较差，给开发人员带去一定额外的心智负担。于是Go开发者Michael Matloob在2021年4月提出的一个[名为“Multi-Module Workspaces in cmd/go”的proposal](https://github.com/golang/proposal/blob/master/design/45713-workspace.md)。这个proposal引入一个go.work文件用于开启Go工作区模式。go.work通过use指示符设置一些本地路径，这些路径下的go module构成一个工作区(workspace)，**Go命令可以操作这些路径下的go module，也会优先使用工作区中的go module**。同时，go.work是本地环境相关的，无需提交到代码仓库中，每个开发者可以根据自己的开发环境设置拥有仅属于自己的go.work文件。

关于Go工作区机制，我在[《Go 1.18新特性前瞻：Go工作区模式》](https://tonybai.com/2021/11/12/go-workspace-mode-in-go-1-18)一文中有详细介绍，大家可以移步到那篇文章认真阅读。不过那篇文章是在Go 1.18 beta1版发布之前写的，当时的一些go.work的内容，比如像directory指示符在Go 1.18正式版中已经发生了变化，这个大家要注意一下。

看完编译器，我们再来简单说说其他工具链。

### 三. Go工具链变化

#### 1. go fuzzing

Go工具链侧最大的变化莫过于引入对fuzzing的原生支持。Fuzzing，又叫fuzz testing，中文叫做模糊测试或随机测试。其本质上是一种自动化测试技术，更具体一点，它是一种基于随机输入的自动化测试技术，常被用于发现处理用户输入的代码中存在的bug和问题。

在具体实现上，Fuzzing不需要像单元测试那样使用预先定义好的数据集作为程序输入，而是会通过数据构造引擎自行构造或基于开发人员提供的初始数据构造一些随机数据，并作为输入提供给我们的程序，然后监测程序是否出现panic、断言失败、无限循环等。这些构造出来的随机数据被称为**语料(corpus)**。另外Fuzz testing不是一次性执行的测试，如果不限制执行次数和执行时间，Fuzz testing会一直执行下去，因此它也是一种持续测试的技术。

Go 1.18将fuzz testing纳入了go test工具链，与单元测试、性能基准测试(https://www.imooc.com/read/87/article/2439)等一起成为了Go原生测试工具链中的重要成员。

go fuzzing test的测试用例与普通的测试用例(TestXxx)、性能基准测试(BenchmarkXxx)等一样放在xx_test.go中，只不过用例对应的函数名样式换为了FuzzXxx了。一个简单的Fuzzing test用例如下：

```
func FuzzXxx(f *testing.F) {
// 设置种子语料(可选)
// 执行Fuzzing
f.Fuzz(func(t *testing.T, b []byte) {
//... ...
})
}
```


关于Go Fuzzing test，我在[《Go 1.18新特性前瞻：原生支持Fuzzing测试》](https://tonybai.com/2021/12/01/first-class-fuzzing-in-go-1-18) 有十分全面系统的说明，大家可以移步到那篇文章阅读了解。

这里需要大家额外注意的是，Fuzzing测试虽然写法上与单元测试、benchmark test很像，也很简单，但Fuzzing测试是持续运行的，不会停下来的，因此就像Go 1.18版本说明中提示的那样：Fuzzing测试会消耗大量的内存，在运行时可能会影响你的机器性能。还要注意的是，在运行时，模糊引擎会将扩大测试范围的数值写入\$GOCACHE/fuzz内的模糊缓存目录。目前对写入模糊缓存的文件数量或总字节数没有限制，所以它可能会占用大量的存储空间（可能是几个GB甚至更多）。因此建议找一台专门的高配机器来跑fuzzing test。

#### 2. go get

在Go module构建模式下，go get回归本职工作，专注于获取go module以及对应的依赖module。不再执行编译和安装工作。这样一来，原本被go get剥夺了光环的go install在module-aware模式下重新拿回本属于自己的职能：安装指定版本或latest版本的module和可执行文件。

最后，我们再来看看其他的一些小变化。

### 四. 其他的minor变化

#### 1. gofmt支持并发

“gofmt的代码风格不是某个人的最爱，而是所有人的最爱”。gofmt代码风格已经成为Go开发者的一种共识，融入到Go语言的开发文化当中了。Go 1.18为Go开发人员带来了支持并发的gofmt，毫无疑问，其最大的好处就是快，尤其是在多核cpu上，gofmt可以利用更多的算力快速完成代码风格的格式化。

#### 2. 内置函数append对切片的扩容算法发生变化

我们都知道append操作切片时，一旦切片已满(len==cap)，append就会重新分配一块更大的底层数组，然后将当前切片元素copy到新底层数组中。通常在size较小的情况下，append都会按2倍cap扩容，size大的情况，比如已经是1024了，那么Go 1.17不会double分配。Go 1.18中的算法有一定变化，目的是使得在一个门槛值前后的变化更丝滑。具体算法大家看下面\$GOROOT/src/runtime/slice.go中的growslice函数中的部分逻辑：

```
func growslice(et *_type, old slice, cap int) slice {
... ...
newcap := old.cap
doublecap := newcap + newcap
if cap > doublecap {
newcap = cap
} else {
const threshold = 256
if old.cap < threshold {
newcap = doublecap
} else {
// Check 0 < newcap to detect overflow
// and prevent an infinite loop.
for 0 < newcap && newcap < cap {
// Transition from growing 2x for small slices
// to growing 1.25x for large slices. This formula
// gives a smooth-ish transition between the two.
newcap += (newcap + 3*threshold) / 4
}
// Set newcap to the requested cap when
// the newcap calculation overflowed.
if newcap <= 0 {
newcap = cap
}
}
}
... ...
}
```


另外从代码来看，和Go 1.17以1024作为大小分界不同，Go 1.18使用256作为threshold。这个大家要注意。

#### 3. 新增net/netip包

Go 1.18标准库在net下面新增加了netip包。这源于原Go核心开发者[Brad Fitzpatrick](https://github.com/bradfitz)在其[创业项目tailscale中遇到的问题](https://tailscale.com/blog/netaddr-new-ip-type-for-go/)。Brad发现标准库中现有的表示IP相关信息的net.IP有如下这么多不足：

![](../../assets/0ddf71cde7f5a200.png)


于是[Brad提议新增一个占用较少的内存、不可变的并且是可比较的、可作为map key的IP的新表示](https://github.com/golang/go/issues/46518)，这就是netip.Addr以及围绕netip.Addr的一系列类型与方法。

关于netip包的内容还不少，大家可以查看[netip包的ref](https://pkg.go.dev/net/netip)来详细了解这个包。

#### 4. 两个重要的安全变化

安全问题日益严重，Go标准库也在紧跟安全趋势的步伐。

在Go 1.18中，tls client默认将使用TLS 1.2版本。当然如果你要显式将Config.MinVersion设置为VersionTLS10，TLS 1.0和1.1依然可以使用。

此外，Go 1.18中crypto/x509包默认将拒绝使用SHA-1哈希函数签名的证书(自签发的除外)。通过GODEBUG=x509sha1=1可以临时支持SHA-1，但从Go 1.19版本开始，SHA-1将被永久踢出。

#### 5. strings包和bytes包新增Cut函数

strings包和bytes包都增加了实用函数Cut(注：strings和bytes包保持API一致性的传统由来已久)。以字符串为例，Cut函数的语义就是将一个输入字符串中的某一段字符串“切掉”。Cut函数的原型如下：

```
func Cut(s, sep string) (before, after string, found bool)
```


如果没找到要切掉的部分，则最后的返回值为false，before为原字符串s，而after则为”"。

```
var s = "hello, golang"
b, a, f := strings.Cut(s, "java")
fmt.Printf("before=%s, after=%s, found=%t\n", b, a, f) // before=hello, golang, after=, found=false
```


如果找到了要切掉的部分，则最后的返回值为true，before为“被切掉部分”的前面的字符串，after则为“被切掉部分”的后面的字符串。

```
b, a, f = strings.Cut(s, "lang")
fmt.Printf("before=%s, after=%s, found=%t\n", b, a, f) // before=hello, go, after=, found=true
```


如果输入字符串中有多个与要切掉的部分匹配的字串，Cut函数只会切掉第一个匹配的字串。

```
b, a, f = strings.Cut(s, "o")
fmt.Printf("before=%s, after=%s, found=%t\n", b, a, f) // before=hell, after=, golang, found=true
```


#### 6. runtime/pprof精确性提升

Go 1.18 runtime/pprof在Linux上采用每线程定时器来驱动采样，目的就是提升在高负荷下采样数据的精确性，减少[数据丢失或不准的情况](https://github.com/golang/go/issues/35057)。

#### 7. sync包新增Mutex.TryLock, RWMutex.TryLock和RWMutex.TryRLock

Go团队在社区的强烈要求下，还是在sync包中加上了Mutex.TryLock, RWMutex.TryLock和RWMutex.TryRLock。但说实话，我个人尚未遇到非要使用TryLock的场景。Go团队在TryLock方法的注释中也给出了使用提示：**请注意，虽然TryLock的正确使用确实存在，但它们是罕见的，而且使用TryLock的使用往往是mutex在特定使用中更深层次问题的标志**。

尽量不要用就完了！

### 五. 小结

从上面内容来看，Go 1.18还真是一个大改动的版本。很多变化都值得后续细致学习和探索。Go 1.18由于引入泛型，我个人还是建议暂缓将其用于生产环境。就像go module引入后，经历go 1.11~go 1.16才逐渐成熟，Go泛型的成熟想必也要至少2-3个版本。在这个阶段，先把精力放在对泛型的学习上以及如何利用泛型改善我们的代码上，但也要注意：泛型大幅提高了代码的复杂性，使用泛型的代码在可读性方面必然有下降，大家不要滥用泛型，更不要显然像c++ template使用的那种奇技淫巧中去。那就与[Go语言的设计哲学](https://time.geekbang.org/column/article/426740)背道而驰了。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

outlook邮箱没有收到文件更新提醒哎，最近收到过《姥姥》的那篇

我看了后台mail的发送，似乎都发出去了。但实际是否收到了，目前我也没法确认。

如果担心mail接收有问题，一个简单的办法：如果2周以上没收到mail，那就到主页来看一眼:)