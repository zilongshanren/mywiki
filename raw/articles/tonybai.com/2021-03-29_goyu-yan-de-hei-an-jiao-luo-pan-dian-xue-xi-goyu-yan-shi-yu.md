---
title: Go语言的“黑暗角落”：盘点学习Go语言时遇到的那些陷阱[译]（第一部分）
url: https://tonybai.com/2021/03/29/darker-corners-of-go-part1/
published: '2021-03-29'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言的“黑暗角落”：盘点学习Go语言时遇到的那些陷阱[译]（第一部分）

![](../../assets/bb5e89e582570bcf.png)


本文翻译自Rytis Bieliunas的文章[《Darker Corners of Go》](https://rytisbiel.com/2021/03/06/darker-corners-of-go/)。

译注：若干年前，Kyle Quest曾发过一篇名为

[“50 Shades of Go: Traps, Gotchas, and Common Mistakes for New Golang Devs”]的文章，仿效著名的[《C Traps and Pitfalls》]编写了50条Go语言的陷阱与缺陷，一时在Go社区广为流传。而本文是又一篇较为系统总结Go陷阱的文章，不同于50 Shades of Go的按初中高级陷阱的分类方式，本文是按类别对Go陷阱做讲解。

## 0. 简介

**这是什么**？

当初学习Go的时候，我只是看了一些入门书和[Go语言规范](https://tip.golang.org/ref/spec)。当时，我已经掌握了其他几种编程语言，然而感觉自己对Go的了解还不够，无法进行实际工作。我觉得自己对Go世界的运作方式了解地还不够深入，我可能需要趟过一些Go陷阱后才会建立起使用Go的信心。

**我是对的**。

虽然[简单是Go语言设计哲学的核心](https://www.imooc.com/read/87/article/2321)，但当你深入使用Go时，你就会发现Go语言在用它颇具创意的方式啪啪打你的脸。

由于现在我已经用Go进行了几年的生产应用，在趟过很多“坑”之后，我想我应该将这些“遇坑与填坑”的情况整理出来献给那些Go语言的新手同学们。

我的目标是在一篇文章中收集Go中各种可能会让新开发者感到惊讶的东西，也许会对Go中比较特别的功能有所启发。我希望这能为读者节省大量的Google搜索和调试时间，并可能避免一些昂贵的错误。

我认为这篇文章对于那些至少已经知道Go语法的人来说是最有用的。如果你是一个中级或有经验的程序员，已经懂得其他编程语言，并希望学习Go，那就最好不过了。

如果你发现错误或者我没有包含你最喜欢的Go surprise，请告诉我：rytbiel@gmail.com。

非常感谢[Vytautas Shaltenis](https://rtfb.lt/)的帮助，让这篇文章变得更好。

## 1. 代码格式化(Code formatting)

### 1) gofmt

在Go中，gofmt工具将许多预定好的代码格式“强加”于你的代码。gofmt对源文件进行机械性的更改，例如对包导入声明进行排序和对代码应用缩进等。这是自从切片面包诞生以来最好的事情，因为它可以节省开发人员大量无关紧要的争论所消耗的工作量。例如，它使用制表符来缩进，使用空格来对齐– 对代码风格的争论到此为止。

您可以完全不使用gofmt工具，但如果使用它，你却无法将对其所实施的代码格式化样式进行配置。该工具完全没有提供任何代码格式化选项，这才是重点。提供一种“足够好”的统一代码格式样式，它可能是没人喜欢的样式，但是Go开发人员认为**统一胜于完美**。

共享样式和自动代码格式化的好处包括：

- 无需花费任何时间在代码审查上来解决格式问题。
- 它可以使您免于与一起工作的同事争论大括号到底放在哪里，缩进使用制表符还是空格。你所有的激情和精力都可以得到更有效的利用。
- 代码更易于编写：像代码格式这样的次要工作已经有工具帮你完成。
- 代码更容易阅读：您无需从心理上解析你不熟悉的别人的代码格式。

大多数流行的IDE都具有Go插件，这些插件会在保存源文件时自动运行gofmt。

诸如goformat之类的第三方工具允许你在Go中使用自定义代码样式格式。但你真的希望那样做么？

### 2) 长代码行

Gofmt不会尝试为您分解很长的代码。有诸如golines之类的第三方工具可以做到这一点。

### 3) 大括号

在Go中，必须在行的末尾放置大括号。有趣的是，这不是gofmt强制执行的，而是Go词法分析器实现方式的副作用。有或没有gofmt，都不能将大括号放在新行上。

```
package main
// missing function body
func main()
// syntax error: unexpected semicolon or newline before {
{
}
// all good!
func main() {
}
```


### 4) 多行声明中的逗号

在初始化切片、数组、map或结构体时，Go要求在换行符前加逗号。在多种语言中都允许使用尾部逗号，并且在某些样式指南中鼓励使用逗号。在Go中，它们是强制性的。这样在重新排列行或添加新行时就无需修改不相关的行。这也意味着更少的代码审核差异噪声。

```
// all of these are OK
a := []int{1, 2}
b := []int{1, 2,}
c := []int{
1,
2}
d := []int{
1,
2,
}
// syntax error without trailing comma
e := []int{
1,
// syntax error: unexpected newline, expecting comma or }
2
}
```


结构体也使用相同规则：

```
type s struct {
One int
Two int
}
f := s{
One: 1,
// syntax error: unexpected newline, expecting comma or }
Two: 2
}
```


## 2. 包导入(Import)

### 1) 未使用的导入包

未使用导入包的Go程序无法编译。这是该语言的故意设定，因为导入包会降低编译器的速度。在大型程序中，未使用的导入包可能会对编译时间产生重大影响。

为了使编译器在开发过程中感到happy^_^，您可以通过以下方式引用该软件包：

```
package main
import (
"fmt"
"math"
)
// Reference unused package
var _ = math.Round
func main() {
fmt.Println("Hello")
}
```


### 2) goimports

更好的解决方案是使用goimports工具。goimports会为您删除未引用的导入包。更好的是，它尝试自动查找并添加缺失的包导入。

```
package main
import "math" // imported and not used: "math"
func main() {
fmt.Println("Hello") // undefined: fmt
}
```


运行goimports之后：

```
./goimports main.go
```


```
package main
import "fmt"
func main() {
fmt.Println("Hello")
}
```


大多数流行的IDE的Go插件在保存源文件时会自动运行goimports。

### 3) 下划线导入

以下划线方式导入包仅是出于对其副作用的依赖。这意味着它将创建程序包级变量并运行包的[init函数](https://medium.com/golangspec/init-functions-in-go-eac191b3860a)：

```
package package1
func package1Function() int {
fmt.Println("Package 1 side-effect")
return 1
}
var globalVariable = package1Function()
func init() {
fmt.Println("Package 1 init side effect")
}
```


导入package1：

```
package package2
import _ package1
```


这将打印消息并初始化globalVariable：

```
Package 1 side-effect
Package 1 init side effect
```


多次导入一个包（例如，在主程序包以及在其主要引用的程序包中）只运行一次该包的init函数。

下划线导入在Go运行时库中有使用。例如，导入net/http/pprof调用其init函数，该函数公开HTTP端点，这些端点可以提供有关应用程序的调试信息：

```
import _ "net/http/pprof"
```


### 4) 点导入

点导入允许在不使用限定符的情况下访问导入包中的标识符：

```
package main
import (
"fmt"
. "math"
)
func main() {
fmt.Println(Sin(3)) // references math.Sin
}
```


是否应从Go语言中完全删除点导入一直存在公开辩论。Go团队不建议在测试包以外的任何地方使用它们：

因为它使得程序可读性大大下降，我们很难知道一个Quux之类的名称是当前程序包中还是导入程序包中的顶层标识符 – https://golang.org/doc/faq


另外，如果您使用go-lint工具，那么在测试文件之外使用点导入时，它会显示警告，并且您无法轻易将其关闭。

Go团队建议在测试中使用点可以避免包的循环依赖：

```
// foo_test package tests for foo package
package foo_test
import (
"bar/testutil" // also imports "foo"
. "foo"
)
```


该测试文件不能成为foo包的一部分，因为它引用了bar/testutil，而bar/testutil又引用了foo并导致了循环依赖。

在这种情况下，首先要考虑的是，是否有一种更好的方法来构建可避免循环依赖的软件包。将bar/testutil使用的内容从foo移动到foo和bar/testutil都可以导入的第三个包可能更好，这样就可以将测试以正常方式写在foo包中。

如果重构没有意义，并且使用点导入将测试移至单独的程序包，则foo_test程序包至少可以假装为foo程序包的一部分。注意，它无法访问foo包的未导出类型和函数。

可以说，在域特定语言编程中，点导入是一个很好的用例。例如，Goa框架将其用于配置。如果没有点导入，它看起来不会很好：

```
package design
import . "goa.design/goa/v3/dsl"
// API describes the global properties of the API server.
var _ = API("calc", func() {
Title("Calculator Service")
Description("HTTP service for adding numbers, a goa teaser")
Server("calc", func() {
Host("localhost", func() { URI("http://localhost:8088") })
})
})
```


## 3. 变量

### 1) 未使用的变量

带有未使用变量的Go程序无法编译：

如果存在未使用的变量，则可能表示有bug[…] Go拒绝使用未使用的变量或导入来编译程序，并且不会为了短期的便利性去换取更高的构建速度和程序的清晰性。- https://golang.org/doc/faq


该规则的例外是全局变量和函数参数：

```
package main
var unusedGlobal int // this is ok
func f1(unusedArg int) { // unused function arguments are also ok
// error: a declared but not used
a, b := 1,2
// b is used here, but a is only assigned to, does not count as “used”
a = b
}
```


### 2) 短变量声明

声明变量的简写形式仅在函数内部起作用：

```
package main
v1 := 1 // error: non-declaration statement outside function body
var v2 = 2 // this is ok
func main() {
v3 := 3 // this is ok
fmt.Println(v3)
}
```


设置结构体字段值时，它也不起作用：

```
package main
type myStruct struct {
Field int
}
func main() {
var s myStruct
// error: non-name s.Field on the left side of :=
s.Field, newVar := 1, 2
var newVar int
s.Field, newVar = 1, 2 // this is actually ok
}
```


### 3) 变量遮蔽

令人遗憾的是，Go中允许使用变量遮蔽。您需要经常注意这一点，因为它可能导致难以发现的问题。发生这种情况是因为，为方便起见，如果至少有一个变量是新变量，Go允许使用短变量声明形式：

```
package main
import "fmt"
func main() {
v1 := 1
// v1 is not actually redeclared here, only gets a new value set
v1, v2 := 2, 3
fmt.Println(v1, v2) // prints 2, 3
}
```


但是，如果声明在另一个代码块内部，则它将声明一个新变量，从而可能导致严重的错误：

```
package main
import "fmt"
func main() {
v1 := 1
if v1 == 1 {
v1, v2 := 2, 3
fmt.Println(v1, v2) // prints 2, 3
}
fmt.Println(v1) // prints 1 !
}
```


一个更现实的示例，假设您有一个返回错误的函数：

```
package main
import (
"errors"
"fmt"
)
func func1() error {
return nil
}
func errFunc1() (int, error) {
return 1, errors.New("important error")
}
func returnsErr() error {
err := func1()
if err == nil {
v1, err := errFunc1()
if err != nil {
fmt.Println(v1, err) // prints: 1 important error
}
}
return err // this returns nil!
}
func main() {
fmt.Println(returnsErr()) // prints nil
}
```


一种解决方案是不要在嵌套代码块内使用短变量声明：

```
func returnsErr() error {
err := func1()
var v1 int
if err == nil {
v1, err = errFunc1()
if err != nil {
fmt.Println(v1, err) // prints: 1 important error
}
}
return err // returns "important error"
}
```


或者在上述示例的情况下，更好的方法是尽早退出：

```
func returnsErr() error {
err := func1()
if err != nil {
return err
}
v1, err := errFunc1()
if err != nil {
fmt.Println(v1, err) // prints: 1 important error
return err
}
return nil
}
```


也有可以提供帮助的工具。在go vet工具中曾有一个实验性的变量遮蔽检测，后来将其删除。在撰写本文时，这是您可以安装和运行该工具的方式：

```
go get -u golang.org/x/tools/go/analysis/passes/shadow/cmd/shadow
go vet -vettool=$(which shadow)
```


打印：

```
.\main.go:20:7: declaration of "err" shadows declaration at line 17
```


## 4. 运算符

### 1) 运算符优先级

Go运算符的优先级与其他语言不同：

```
Precedence Operator
5 * / % << >> & &^
4 + - | ^
3 == != < <= > >=
2 &&
1 ||
```


将其与基于C的语言进行比较：

```
Precedence Operator
10 *, /, %
9 +, -
8 <<, >>
7 <, <=, >, >=
6 ==, !=
5 &
4 ^
3 |
2 &&
1 ||
```


对于相同的表达式，这可能导致不同的结果：

```
In Go: 1 << 1 + 1 // (1<<1)+1 = 3
In C: 1 << 1 + 1 // 1<<(1+1) = 4
```


### 2) 自增和自减

与许多其他语言不同，Go没有前缀自增或自减运算符：

```
var i int
++i // syntax error: unexpected ++, expecting }
--i // syntax error: unexpected --, expecting }
```


尽管Go确实具有这些运算符的后缀版本，但Go不允许在表达式中使用它们：

```
slice := []int{1,2,3}
i := 1
slice[i++] = 0 // syntax error: unexpected ++, expecting :
```


### 3) 三元运算符

Go语言不支持三元运算符，像下面这样的代码：

```
result := a ? b : c
```


在Go中没有，你也不要费力寻找。您必须使用if-else代替。Go语言设计人员认为此运算符经常导致难看的代码，最好不要使用它。

### 4) 按位非

在Go中，XOR运算符\^被用作一元NOT运算符，而不是像许多其他语言使用〜符号。

```
In Go: ^1 // -2
In C: ~1 // -2
```


用于二元计算是，XOR运算符仍用作XOR(异或)运算符。

```
3^1 // 2
```


## 5.常量

### 1) iota

iota开始在Go中进行常量编号。但它并不非期望的“从零开始”，它是当前const块中常量的索引：

```
const (
myconst = "c"
myconst2 = "c2"
two = iota // 2
)
```


两次使用iota不会重置编号：

```
const (
zero = iota // 0
one // 1
two = iota // 2
)
```


## 6. 切片和数组

### 1) 切片和数组

在Go中，切片和数组的用途相似。它们的声明方式几乎相同：

```
package main
import "fmt"
func main() {
slice := []int{1, 2, 3}
array := [3]int{1, 2, 3}
// let the compiler work out array length
// this will be an equivalent of [3]int
array2 := [...]int{1, 2, 3}
fmt.Println(slice, array, array2)
}
```


```
[1 2 3] [1 2 3] [1 2 3]
```


切片感觉像是在顶部具有有用功能的数组。他们在实现的内部使用指向数组的指针。但是，切片要方便得多，以至于我们很少在Go中直接使用数组。

### 2) 数组

数组是有着固定大小内存的一组同类型元素的集合。不同长度的数组被认为是不同的不兼容类型。

与C语言不同，创建数组时，Go会将数组元素初始化为零值，因此我们无需再显式地执行此初始化操作。另外，与C不同的是，Go数组是值类型，它不是指向内存块第一个元素的指针。如果将数组传递给函数，则将复制整个数组。您仍然可以传递指向数组的指针以使其不被复制。

![](../../assets/a3ec6a4abfc56a2a.png)


### 3) 切片

切片是数组段的描述符。这是一个非常有用的数据结构，但可能有点不寻常。有几种可以让你掉入坑中的场景，但如果您知道切片的内部工作原理，则可以避免这些“坑”。这是Go源代码中切片的实际定义：

```
type slice struct {
array unsafe.Pointer
len int
cap int
}
```


![](../../assets/ca3b686e6a5ae89c.png)


Slice本身是一个值类型，但它使用指针引用它使用的数组。与数组不同，如果将切片传递给函数，则会获得数组指针，len和cap属性的副本（上图中的第一个块），但是数组本身的数据不会被复制，切片的两个副本都指向同一数组。当您“切片”一个切片时，也会发生同样的事情。Go会创建一个新的切片，该切片仍指向相同的数组：

```
package main
import "fmt"
func f1(s []int) {
// slicing the slice creates a new slice
// but does not copy the array data
s = s[2:4]
// modifying the sub-slice
// changes the array of slice in main function as well
for i := range s {
s[i] += 10
}
fmt.Println("f1", s, len(s), cap(s))
}
func main() {
s := []int{1, 2, 3, 4, 5}
// passing a slice as an argument
// makes a copy of the slice properties (pointer, len and cap)
// but the copy shares the same array
f1(s)
fmt.Println("main", s, len(s), cap(s))
}
```


```
f1 [13 14] 2 3
main [1 2 13 14 5] 5 5
```


![](../../assets/528f04a148ca102c.png)


如果您不知道哪个分片，则可以假设它是一个值类型，并且感到惊讶的是f1“破坏了”main中切片中的数据。

### 4) 获取包括其数据的切片的副本

要获取切片及其数据的副本，您需要做一些工作。您可以将元素手动复制到新切片或使用复制(copy)或追加(append)：

```
package main
import "fmt"
func f1(s []int) {
s = s[2:4]
s2 := make([]int, len(s))
copy(s2, s)
// or if you prefer less efficient, but more concise version:
// s2 := append([]int{}, s[2:4]...)
for i := range s2 {
s2[i] += 10
}
fmt.Println("f1", s2, len(s2), cap(s2))
}
func main() {
s := []int{1, 2, 3, 4, 5}
f1(s)
fmt.Println("main", s, len(s), cap(s))
}
```


```
f1 [13 14] 2 3
main [1 2 3 4 5] 5 5
```


### 5) 使用append扩充切片

切片的所有副本都共享同一数组，直到他们不这样做。切片最有用的属性是它可以为您自动管理数组的增长。当它需要超过现有数组容量时，它会分配一个全新的数组。如果您希望切片的两个副本共享数组，那么这也可能是陷阱：

```
package main
import "fmt"
func main() {
// make a slice with length 3 and capacity 4
s := make([]int, 3, 4)
// initialize to 1,2,3
s[0] = 1
s[1] = 2
s[2] = 3
// capacity of the array is 4
// adding one more number fits in the initial array
s2 := append(s, 4)
// modify the elements of the array
// s and s2 still share the same array
for i := range s2 {
s2[i] += 10
}
fmt.Println(s, len(s), cap(s)) // [11 12 13] 3 4
fmt.Println(s2, len(s2), cap(s2)) // [11 12 13 14] 4 4
// this append grows the array past its capacity
// new array must be allocated for s3
s3 := append(s2, 5)
// modify the elements of the array to see the result
for i := range s3 {
s3[i] += 10
}
fmt.Println(s, len(s), cap(s)) // still the old array [11 12 13] 3 4
fmt.Println(s2, len(s2), cap(s2)) // the old array [11 12 13 14] 4 4
// array was copied on last append [21 22 23 24 15] 5 8
fmt.Println(s3, len(s3), cap(s3))
}
```


![](../../assets/31a9401847d31b21.png)


### 6) nil切片

无需检查切片是否为nil值，也不必对其初始化。len，cap和append等功能在nil slice上同样可以正常工作：

```
package main
import "fmt"
func main() {
var s []int // nil slice
fmt.Println(s, len(s), cap(s)) // [] 0 0
s = append(s, 1)
fmt.Println(s, len(s), cap(s)) // [1] 1 1
}
```


空切片(empty slice)与nil切片不是同一回事：

```
package main
import "fmt"
func main() {
var s []int // this is a nil slice
s2 := []int{} // this is an empty slice
// looks like the same thing here:
fmt.Println(s, len(s), cap(s)) // [] 0 0
fmt.Println(s2, len(s2), cap(s2)) // [] 0 0
// but s2 is actually allocated somewhere
fmt.Printf("%p %p", s, s2) // 0x0 0x65ca90
}
```


如果您非常在意性能和内存使用情况，那么初始化一个空切片可能不如使用nil切片理想。

### 7) make陷阱

要创建一个新的切片，可以将make与切片类型以及切片的初始长度和容量一起使用。容量参数是可选的：

```
func make([]T, len, cap) []T
```


这样做太简单了：

```
package main
import (
"fmt"
)
func main() {
s := make([]int, 3)
s = append(s, 1)
s = append(s, 2)
s = append(s, 3)
fmt.Println(s)
}
```


```
[0 0 0 1 2 3]
```


不，这永远不会发生在我身上，我知道make创建切片的第二个参数是长度，而不是容量，我听到你说……

###

未使用的切片的数组数据

由于对数组进行切片会创建一个新的切片，但会共享底层数组，因此有可能在内存中保留比你预期更多的数据。这是一个愚蠢的例子：

```
package main
import (
"bytes"
"fmt"
"io/ioutil"
"os"
)
func getExecutableFormat() []byte {
// read our own executable file into memory
bytes, err := ioutil.ReadFile(os.Args[0])
if err != nil {
panic(err)
}
return bytes[:4]
}
func main() {
format := getExecutableFormat()
if bytes.HasPrefix(format, []byte("ELF")) {
fmt.Println("linux executable")
} else if bytes.HasPrefix(format, []byte("MZ")) {
fmt.Println("windows executable")
}
}
```


在上面的代码中，只要该format变量在范围内并且不能被垃圾回收，则整个可执行文件（可能几兆字节的数据）将必须保留在内存中。要修复它，请复制实际需要的字节。

### 9) 多维切片

目前，Go中没有这样的东西。可能某天会有，但是此时此刻您需要自己计算元素索引来手动将一维切片用作多维切片，或者使用“锯齿状”切片（锯齿状切片是切片的切片）：

```
package main
import "fmt"
func main() {
x := 2
y := 3
s := make([][]int, y)
for i := range s {
s[i] = make([]int, x)
}
fmt.Println(s)
}
```


```
[[0 0] [0 0] [0 0]]
```


第二部分见下面链接：

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，>每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需>求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足>广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖>中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

感谢分享！