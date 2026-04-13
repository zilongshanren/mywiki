---
title: Go泛型真的要来了！最早在Go 1.17版本支持
url: https://tonybai.com/2020/06/18/the-go-generics-is-coming-and-supported-in-go-1-17-at-the-earliest/
published: '2020-06-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go泛型真的要来了！最早在Go 1.17版本支持

Go官博今晨发表了Go核心团队两位大神[Ian Lance Taylor](https://github.com/ianlancetaylor)和Go语言之父之一的[Robert Griesemer](https://github.com/griesemer)撰写的文章[“The Next Step for Generics”](https://blog.golang.org/generics-next-step)，该文介绍了Go泛型(Go Generics)的最新进展和未来计划。

2019年中旬，在[Go 1.13版本](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)发布前夕的[GopherCon 2019大会](https://www.gophercon.com)上，[Ian Lance Taylor](https://github.com/ianlancetaylor)代表Go核心团队做了[有关Go泛型进展的介绍](https://blog.golang.org/why-generics)。自那以后，Go团队对原先的[Go Generics技术草案](https://github.com/golang/proposal/blob/master/design/go2draft-contracts.md)做了进一步精化，并编写了相关工具让社区gopher体验满足这份设计的Go generics语法，返回建议和意见。经过一年多的思考、讨论、反馈与实践，Go核心团队决定在这份旧设计的基础上**另起炉灶**，撰写了一份[Go Generics的新技术提案：“Type Parameters”](https://github.com/golang/proposal/blob/master/design/go2draft-type-parameters.md)。与上一份提案最大的不同在于使用**扩展的interface类型**替代**“Contract”**用于对类型参数的约束。

**parametric polymorphism((形式)参数多态)**是Go此版泛型设计的基本思想。和Go设计思想一致，这种参数多态并不是通过像面向对象语言那种子类型的层次体系实现的，而是通过显式定义结构化的约束实现的。基于这种设计思想，该设计不支持[模板元编程(template metaprogramming)](https://code.fandom.com/wiki/Template_metaprogramming])和编译期运算。

注意：虽然都称为泛型(generics)，但是Go中的泛型(generics)仅是用于狭义地表达带有类型参数(type parameter)的函数或类型，这与其他编程语言中的泛型(generics)在含义上有相似性，但不完全相同。


从目前的情况来看，该版设计十分接近于最终接受的方案，因此作为Go语言**鼓吹者**这里就和大家一起看看最早将于Go 1.17版本(2021年8月)中加入的Go泛型支持究竟是什么样子的。由于目前关于Go泛型的资料仅限于[这份设计文档](https://github.com/golang/proposal/blob/master/design/go2draft-type-parameters.md)以及一些关于这份设计的讨论贴，本文内容均来自这些资料。另外**最终加入Go的泛型很可能与目前设计文档中提到的有所差异**，请各位小伙伴们了解。

### 1. 通过为type和function增加类型参数(type parameters)的方式实现泛型

Go的泛型主要体现在类型和函数的定义上。

- 泛型函数(generic function)

Go提案中将带有**类型参数(type parameters)**的函数称为泛型函数，比如：

```
func PrintSlice(type T)(s []T) {
for _, v := range s {
fmt.Printf("%v ", v)
}
fmt.Print("\n")
}
```


其中，函数名PrintSlice与函数参数列表之间的**type T**即为**类型参数列表**。顾名思义，该函数用于打印元素类型为T的切片中的所有元素。使用该函数的时候，除了要传入要打印的切片实参外，还需要为**类型参数**传入实参（一个类型名)，这个过程称为**泛型函数的实例化**。见下面例子：

```
// https://go2goplay.golang.org/p/rDbio9c4AQI
package main
import "fmt"
func PrintSlice(type T)(s []T) {
for _, v := range s {
fmt.Printf("%v ", v)
}
fmt.Print("\n")
}
func main() {
PrintSlice(int)([]int{1, 2, 3, 4, 5})
PrintSlice(float64)([]float64{1.01, 2.02, 3.03, 4.04, 5.05})
PrintSlice(string)([]string{"one", "two", "three", "four", "five"})
}
```


运行该示例：

```
1 2 3 4 5
1.01 2.02 3.03 4.04 5.05
one two three four five
```


但是这种每次都显式指定类型参数实参的使用方式显然有些复杂繁琐，给开发人员带来心智负担和不好的体验。Go编译器是聪明的，大多数使用泛型函数的场景下，编译器都会根据函数参数列表传入的实参类型自动推导出类型参数的实参类型(type inference）。比如将上面例子改为下面这样，程序依然可以输出正确的结果。

```
// https://go2goplay.golang.org/p/UgHqZ7g4rbo
package main
import "fmt"
func PrintSlice(type T)(s []T) {
for _, v := range s {
fmt.Printf("%v ", v)
}
fmt.Print("\n")
}
func main() {
PrintSlice([]int{1, 2, 3, 4, 5})
PrintSlice([]float64{1.01, 2.02, 3.03, 4.04, 5.05})
PrintSlice([]string{"one", "two", "three", "four", "five"})
}
```


- 泛型类型(generic type)

Go提案中将带有**类型参数(type parameters)**的类型定义称为泛型类型，比如我们定义一个底层类型为切片类型的新类型：Vector：

```
type Vector(type T) []T
```


该Vector(切片)类型中的元素类型为T。和泛型函数一样，使用泛型类型时，我们首先要对其进行实例化，即显式为**类型参数**赋一个实参值（一个类型名）：

```
//https://go2goplay.golang.org/p/tIZN2if1Wxo
package main
import "fmt"
func PrintSlice(type T)(s []T) {
for _, v := range s {
fmt.Printf("%v ", v)
}
fmt.Print("\n")
}
type Vector(type T) []T
func main() {
var vs = Vector(int){1, 2, 3, 4, 5}
PrintSlice(vs)
}
```


泛型类型的实例化是必须显式为**类型参数**传参的，编译器无法自行做类型推导。如果将上面例子中main函数改为如下实现方式：

```
func main() {
var vs = Vector{1, 2, 3, 4, 5}
PrintSlice(vs)
}
```


则Go编译器会报如下错误：

```
type checking failed for main
prog.go2:15:11: cannot use generic type Vector(type T) without instantiation
```


这个错误的意思就是：未实例化(instantiation)的泛型类型Vector(type T)无法使用。

### 2. 通过扩展了的interface类型对类型参数进行约束和限制

#### 1) 对泛型函数中类型参数的约束与限制

有了泛型函数，我们来实现一个“万能”加法函数：

```
// https://go2goplay.golang.org/p/t0vXI6heUrT
package main
import "fmt"
func Add(type T)(a, b T) T {
return a + b
}
func main() {
c := Add(5, 6)
fmt.Println(c)
}
```


运行上述示例：

```
type checking failed for main
prog.go2:6:9: invalid operation: operator + not defined for a (variable of type T)
```


什么情况！这么简单的一个函数，Go编译器居然报了这个错误：**类型参数T未定义“+”这个操作符运算**。

在此版Go泛型设计中，泛型函数只能使用类型参数所能实例化出的任意类型都能支持的操作。比如上述Add函数的类型参数**type T**没有任何约束，它可以被实例化为任何类型。那么这些实例化后的类型是否都支持“+”操作符运算呢？显然不是。因此，编译器针对示例代码中的第六行报了错！

对于像上面Add函数那样的没有任何约束的类型参数实例，Go允许对其进行的操作包括：

- 声明这些类型的变量；
- 使用相同类型的值为这些变量赋值；
- 将这些类型的变量以实参形式传给函数或从作为函数返回值；
- 取这些变量的地址；
- 将这些类型的值转换或赋值给interface{}类型变量；
- 通过类型断言将一个接口值赋值给这类类型的变量；
- 在type switch块中作为一个case分支；
- 定义和使用由该类型组成的复合类型，比如：元素类型为该类型的切片；
- 将该类型传递给一些内置函数，比如new。

那么，我们要让上面的Add函数通过编译器的检查，我们就需要限制其类型参数所能实例化出的类型的范围。比如：仅允许实例化为**底层类型(underlying type)**为整型类型的类型。上一版Go泛型设计中使用**Contract**来定义对类型参数的约束，不过由于Contract与interface在概念范畴上有交集，让Gopher们十分困惑，于是在新版泛型设计中，Contract这个关键字被移除了，取而代之的是语法扩展了的interface，即我们使用interface类型来修饰类型参数以实现对其可实例化出的类型集合的约束。我们来看下面例子：

```
// https://go2goplay.golang.org/p/kMxZI2vIsk-
package main
import "fmt"
type PlusableInteger interface {
type int, int8, int16, int32, int64, uint, uint8, uint16, uint32, uint64
}
func Add(type T PlusableInteger)(a, b T) T {
return a + b
}
func main() {
c := Add(5, 6)
fmt.Println(c)
}
```


运行该示例：

```
11
```


如果我们在main函数中写下如下代码：

```
f := Add(3.65, 7.23)
fmt.Println(f)
```


我们将得到如下编译错误：

```
type checking failed for main
prog.go2:20:7: float64 does not satisfy PlusableInteger (float64 not found in int, int8, int16, int32, int64, uint, uint8, uint16, uint32, uint64)
```


我们看到：该提案扩展了interface语法，新增了类型列表(type list)表达方式，专用于对类型参数进行约束。以该示例为例，如果编译器通过类型推导得到的类型在PlusableInteger这个接口定义的类型列表(type list)中，那么编译器将允许这个类型参数实例化；否则就像**Add(3.65, 7.23)**那样，推导出的类型为float64，该类型不在PlusableInteger这个接口定义的类型列表(type list)中，那么类型参数实例化将报错！

注意：定义中带有类型列表的接口将无法用作接口变量类型，比如下面这个示例：

```
// https://go2goplay.golang.org/p/RchnTw73VMo
package main
type PlusableInteger interface {
type int, int8, int16, int32, int64, uint, uint8, uint16, uint32, uint64
}
func main() {
var n int = 6
var i PlusableInteger
i = n
_ = i
}
```


编译器会报如下错误：

```
type checking failed for main
prog.go2:9:8: interface type for variable cannot contain type constraints (int, int8, int16, int32, int64, uint, uint8, uint16, uint32, uint64)
```


我们还可以用interface的原生语义对类型参数进行约束，看下面例子：

```
// https://go2goplay.golang.org/p/hyTbglTLoIn
package main
import (
"fmt"
"strconv"
)
type StringInt int
func (i StringInt) String() string {
return strconv.Itoa(int(i))
}
type Stringer interface {
String() string
}
func Stringify(type T Stringer)(s []T) (ret []string) {
for _, v := range s {
ret = append(ret, v.String())
}
return ret
}
func main() {
fmt.Println(Stringify([]StringInt{1, 2, 3, 4, 5}))
}
```


运行该示例：

```
[1 2 3 4 5]
```


如果我们在main函数中写下如下代码：

```
func main() {
fmt.Println(Stringify([]int{1, 2, 3, 4, 5}))
}
```


那么我们将得到下面的编译器错误输出：

```
type checking failed for main
prog.go2:27:2: int does not satisfy Stringer (missing method String)
```


我们看到：只有实现了Stringer接口的类型才会被允许作为实参传递给Stringify泛型函数的类型参数并成功实例化。

我们还可以结合interface的类型列表(type list)和方法列表一起对类型参数进行约束，看下面示例：

```
// https://go2goplay.golang.org/p/tchwW6mPL7_d
package main
import (
"fmt"
"strconv"
)
type StringInt int
func (i StringInt) String() string {
return strconv.Itoa(int(i))
}
type SignedIntStringer interface {
type int, int8, int16, int32, int64
String() string
}
func Stringify(type T SignedIntStringer)(s []T) (ret []string) {
for _, v := range s {
ret = append(ret, v.String())
}
return ret
}
func main() {
fmt.Println(Stringify([]StringInt{1, 2, 3, 4, 5}))
}
```


在该示例中，用于对泛型函数的类型参数进行约束的SignedIntStringer接口既包含了类型列表，也包含方法列表，这样类型参数的实参类型既要在SignedIntStringer的类型列表中，也要实现了SignedIntStringer的String方法。

如果我们将上面的StringInt的底层类型改为uint：

```
type StringInt uint
```


那么我们将得到下面的编译器错误输出：

```
type checking failed for main
prog.go2:27:14: StringInt does not satisfy SignedIntStringer (uint not found in int, int8, int16, int32, int64)
```


#### 2) 引入comparable预定义类型约束

由于Go泛型设计选择了不支持运算操作符重载，因此，我们即便对interface做了语法扩展，依然无法表达类型是否支持**==**和**!=**。为了解决这个表达问题，这份新设计提案中引入了一个新的预定义类型约束：**comparable**。我们看下面例子：

```
// https://go2goplay.golang.org/p/tea39NqwZGC
package main
import (
"fmt"
)
// Index returns the index of x in s, or -1 if not found.
func Index(type T comparable)(s []T, x T) int {
for i, v := range s {
// v and x are type T, which has the comparable
// constraint, so we can use == here.
if v == x {
return i
}
}
return -1
}
type Foo struct {
a string
b int
}
func main() {
fmt.Println(Index([]int{1, 2, 3, 4, 5}, 3))
fmt.Println(Index([]string{"a", "b", "c", "d", "e"}, "d"))
pos := Index(
[]Foo{
Foo{"a", 1},
Foo{"b", 2},
Foo{"c", 3},
Foo{"d", 4},
Foo{"e", 5},
}, Foo{"b", 2})
fmt.Println(pos)
}
```


运行该示例：

```
2
3
1
```


我们看到Go的原生支持比较的类型，诸如整型、字符串以及由这些类型组成的复合类型(如结构体)均可以直接作为实参传给由comparable约束的类型参数。comparable可以看成一个由Go编译器特殊处理的、包含由所有内置可比较类型组成的type list的interface类型。我们可以将其嵌入到其他作为约束的接口类型定义中：

```
type ComparableStringer interface {
comparable
String() string
}
```


只有支持比较的类型且实现了**String**方法，才能满足ComparableStringer的约束。

#### 3) 对泛型类型中类型参数的约束

和对泛型函数中类型参数的约束方法一样，我们也可以对泛型类型的类型参数以同样方法做同样的约束，看下面例子：

```
// https://go2goplay.golang.org/p/O-YpTcW-tPu
// Package set implements sets of any comparable type.
package main
// Set is a set of values.
type Set(type T comparable) map[T]struct{}
// Make returns a set of some element type.
func Make(type T comparable)() Set(T) {
return make(Set(T))
}
// Add adds v to the set s.
// If v is already in s this has no effect.
func (s Set(T)) Add(v T) {
s[v] = struct{}{}
}
// Delete removes v from the set s.
// If v is not in s this has no effect.
func (s Set(T)) Delete(v T) {
delete(s, v)
}
// Contains reports whether v is in s.
func (s Set(T)) Contains(v T) bool {
_, ok := s[v]
return ok
}
// Len reports the number of elements in s.
func (s Set(T)) Len() int {
return len(s)
}
// Iterate invokes f on each element of s.
// It's OK for f to call the Delete method.
func (s Set(T)) Iterate(f func(T)) {
for v := range s {
f(v)
}
}
func main() {
s := Make(int)()
// Add the value 1,11,111 to the set s.
s.Add(1)
s.Add(11)
s.Add(111)
// Check that s does not contain the value 11.
if s.Contains(11) {
println("the set contains 11")
}
}
```


运行该示例：

```
the set contains 11
```


这个示例定义了一个数据结构：Set。该Set中的元素是有约束的：必须支持可比较。对应到代码中，我们用comparable作为泛型类型Set的类型参数的约束。

#### 4) 关于泛型类型的方法

泛型类型和普通类型一样，也可以定义自己的方法。**但泛型类型的方法目前不支持除泛型类型自身的类型参数之外的其他类型参数了**。我们看下面例子：

```
// https://go2goplay.golang.org/p/JipsxG7jeCN
// Package set implements sets of any comparable type.
package main
// Set is a set of values.
type Set(type T comparable) map[T]struct{}
// Make returns a set of some element type.
func Make(type T comparable)() Set(T) {
return make(Set(T))
}
// Add adds v to the set s.
// If v is already in s this has no effect.
func (s Set(T)) Add(v T) {
s[v] = struct{}{}
}
func (s Set(T)) Method1(type P)(v T, p P) {
}
func main() {
s := Make(int)()
s.Add(1)
s.Method1(10, 20)
}
```


在这个示例中，我们新定义的Method1除了在参数列表中使用泛型类型Set的类型参数T之外，又接受了一个类型参数P。执行该示例：

```
type checking failed for main
prog.go2:18:24: methods cannot have type parameters
```


我们看到编译器给出错误：**泛型类型的方法不能再有其他类型参数**。目前提案仅是暂时不支持额外的类型参数(如果支持，会让语言规范和实现都变得异常复杂)，Go核心团队也会听取社区反馈的意见，直到大家都认为支持额外类型参数是有必要的，那么后续会重新添加。

#### 5) type *T Constraint

上面我们一直采用的对类型参数的约束形式是：

```
type T Constraint
```


假设调用泛型函数时某类型A要作为T的实参传入，A必须实现Constraint(接口)。

如果我们将上面对类型参数的约束形式改为：

```
type *T Constraint
```


那么这将意味着类型A要作为T的实参传入，*A必须满足Constraint(接口)。并且Constraint中的所有方法(如果有的话）都仅能通过*A实例调用。我们来看下面示例：

```
// https://go2goplay.golang.org/p/g3cwgguCmUo
package main
import (
"fmt"
"strconv"
)
type Setter interface {
Set(string)
}
func FromStrings(type *T Setter)(s []string) []T {
result := make([]T, len(s))
for i, v := range s {
result[i].Set(v)
}
return result
}
// Settable is a integer type that can be set from a string.
type Settable int
// Set sets the value of *p from a string.
func (p *Settable) Set(s string) {
i, _ := strconv.Atoi(s) // real code should not ignore the error
*p = Settable(i)
}
func main() {
nums := FromStrings(Settable)([]string{"1", "2"})
fmt.Println(nums)
}
```


运行该示例：

```
[1 2]
```


我们看到Settable的方法集合是空的，而*Settable的方法集合(method set)包含了Set方法。因此，*Settable是满足Setter对FromStrings函数的类型参数的约束的。

而如果我们直接使用type T Setter，那么编译器将给出下面错误：

```
type checking failed for main
prog.go2:30:22: Settable does not satisfy Setter (missing method Set)
```


如果我们使用type T Setter并结合使用FromStrings(*Settable)，那么程序运行会panic。

https://go2goplay.golang.org/p/YLe2d78aSz-

### 3. 性能影响

根据这份技术提案中关于泛型函数和泛型类型实现的说明，Go会使用基于接口的方法来编译泛型函数(generic function)，这将优化编译时间，因为该函数仅会被编译一次。但是会有一些运行时代价。

对于每个类型参数集，泛型类型(generic type)可能会进行多次编译。这将延长编译时间，但是不会产生任何运行时代价。编译器还可以选择使用类似于接口类型的方法来实现泛型类型，使用专用方法访问依赖于类型参数的每个元素。

### 4. 小结

Go泛型方案的即将定型即好也不好。Go向来以简洁著称，增加加泛型，无论采用什么技术方案，都会增加Go的复杂性，提升其学习门槛，代码可读性也会下降。但在某些场合(比如实现container数据结构及对应算法库等)，使用泛型却又能简化实现。

在这份提案中，Go核心团队也给出如下期望：

```
We expect that most packages will not define generic types or functions, but many packages are likely to use generic types or functions defined elsewhere
我们期望大多数软件包不会定义泛型类型或函数，但是许多软件包可能会使用在其他地方定义的泛型类型或函数。
```


并且提案提到了会在Go标准库中增加一些新包，已实现基于泛型的标准数据结构(slice、map、chan、math、list/ring等)、算法(sort、interator)等，gopher们只需调用这些包提供的API即可。

另外该提案的一大优点就是**与Go1兼容**，我们可能永远不会使用Go2这个版本号了。

go核心团队提供了可实践该方案语法的playground：https://go2goplay.golang.org/，大家可以一边研读技术提案，一边编写代码进行实验验证。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

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

博主,

那么这将意味着类型A要作为T的实参传入，A必须满足Constraint(接口)。并且Constraint中的所有方法(如果有的话）都仅能通过A实例调用。

以及

我们看到Settable的方法集合是空的，而Settable的方法集合(method set)包含了Set方法。因此，Settable是满足Setter对FromStrings函数的类型参数的约束的。

这两个地方的星号被页面解析错了吧？

感谢提醒。的确被markdown插件转换错了。在星号前加上反斜线解决了。看来这个问题由来已久了，看来以后写文章时不能“偷懒”了。该加“\”的地方不能落下。

感觉go的泛型还是不够灵活，对接口的条件限制完全可以在编译期检测出来，把这个任务交给程序员感觉有些多余了

比如：

func Add(type T)(a, b T) T {

return a+b

}

调用Add(5,6)和调用Add(“hello”, “world”)，或者调用Add(5, “hello”)，编译期实例化的时候编译器完全有能力检测出哪些合法，哪些不合法呀，这样可以减轻开发者很大一部分工作量，不明白为什么不这么设计

还是不喜欢这个设计，尤其是不用更多人习惯的 这点

还有其中一个例子不靠泛型也没问题：

“`

func Stringify(type T Stringer)(s []T) (ret []string) {

for _, v := range s {

ret = append(ret, v.String())

}

return ret

}

“`

完全可以直接写

“`

func Stringify(s []Stringer) (ret []string) {

for _, v := range s {

ret = append(ret, v.String())

}

return ret

}

“`

觉得 Go 太过于执着简单反而让自己变得一点也不简单

“习惯的”后方有加 < 与 > ，看来没被转译

博主要小心被恶意注入 JS

很像rust的泛型绑定约束。

挺搞的，竟然选了小括号，方便了工具而让人类去承受混淆

最新的变化是选择了方括号[]。