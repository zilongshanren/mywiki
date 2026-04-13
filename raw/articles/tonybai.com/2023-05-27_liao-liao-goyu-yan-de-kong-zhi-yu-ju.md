---
title: 聊聊Go语言的控制语句
url: https://tonybai.com/2023/05/27/control-flow-statement-in-go/
published: '2023-05-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 聊聊Go语言的控制语句

![](../../assets/34f7fcf7fc5c49d0.png)


[本文永久链接](https://tonybai.com/2023/05/27/control-flow-statement-in-go) – https://tonybai.com/2023/05/27/control-flow-statement-in-go

在高级编程语言中，控制流语句(control-flow statement)是一类用于控制程序执行流程的语句，以下简称为**控制语句**。它们可以根据条件或循环执行相应的代码块，或者跳转到指定位置执行代码。

常见的控制语句包括：

- 条件语句：根据条件执行不同的代码块，如if语句、switch语句等。
- 循环语句：根据条件重复执行相应的代码块，如for语句、while语句等。
- 跳转语句：跳转到指定位置执行代码，如break、goto语句。
- 异常处理语句：处理程序运行过程中出现的异常，如try-catch语句、throw语句等。

控制语句是编程语言中实现程序逻辑的重要手段，它们可以帮助程序员实现复杂的算法和逻辑。不同的编程语言支持的控制语句的种类和用法可能会有所不同，但它们的基本作用都是相似的，即控制程序的执行流程。

Go语言中的控制语句语法**在主流编程语言中算是极少的了**！掐指算来，主要的包括if、for和switch。当然goto、defer、panic/recover语句也应归类于控制语句，并且后面这些控制语句也都是Go语言实现程序逻辑的重要手段。但后面这几个并非本篇讲述的重点，在这篇文章中，我将聚焦于**Go的if、for和switch语句**。

## 1. if语句

首先我们先来看看if语句。

if语句用于根据一个条件执行相应的代码块，是Go语言中最常用的控制语句。

if语句的基本语法如下：

```
if condition {
// code block
} else if condition {
// code block
} else {
// code block
}
```


关于if语句，我主要说下面三点：

### 1.1 隐式代码块(block)

我们看下面代码：

```
func bar() {
if a := 1; false {
} else if b := 2; false {
} else if c := 3; false {
} else {
println(a, b, c)
}
}
```


看完这段代码后，你觉得这段代码可以被正常编译吗？如果可以，那么它会输出什么信息呢？Go编译器告诉我们：上面这段可以正常编译并运行！但很多人会质疑：**为何在第一个if语句中声明的变量a、第二个if中的变量b以及第三个if中的变量c，在最后的else语句中都可以有效访问呢**？

要想解答这个问题，必须要搞清楚if语句的隐式代码块和作用域规则。上述代码等价于下面代码：

```
func bar() {
{ // 等价于第一个if的隐式代码块
a := 1 // 变量a作用域始于此
if false {
} else {
{ // 等价于第一个else if的隐式代码块
b := 2 // 变量b的作用域始于此
if false {
} else {
{ // 等价于第二个else if的隐式代码块
c := 3 // 变量c作用域始于此
if false {
} else {
println(a, b, c)
}
// 变量c的作用域终止于此
}
}
// 变量b的作用域终止于此
}
}
// 变量a作用域终止于此
}
}
```


通过这段展开后的代码，我们可以清楚地看到第一段代码中的最后的else语句实质上是一个最内层的else，变量a、b、c的作用域范围是可以覆盖到else的。

注：极客时间的

[《Go语言第一课》专栏]的[第11讲]对代码块与作用域有着更为全面的讲解，欢迎大家订阅学习。

### 1.2 使用自用变量

在Go中使用if语句时，开发者常常纠结于到底使用下面哪种形式：

```
if a, ok := foo(); a < 10 && ok{ //使用if表达式自用变量
}
vs.
a, ok := foo()
if a < 10 && ok {
}
```


这里建议采用第一种，即“使用if表达式自用变量”，而不是在if外部定义临时变量。因为前者除了简洁，可读性略好的优点外，还有一点优势，那就是将a放在if隐式代码块中，将变量a的作用域限制到最小范围，这样可以避免不同代码段中变量命名相同而引起的冲突问题。进而让代码实现更加清晰和易于理解。

上述代码还有一个可能让初学者疑惑的点，那就是a < 10 && ok的运算符优先级问题，是(a < 10) && ok 还是 a < (10 && ok)，为了避免给后续代码阅读者带去理解上的困惑，建议使用小括号明确求值时的计算顺序。

### 1.3 happy path原则

Go语言中，if语句使用的一个惯例就是遵循happy path(快乐路径)原则，所谓happy path是指通过将缩进程度降到最低，避免if语句或else-if语句的过度嵌套，使代码更易读和可维护。遵循快乐路径原则可以让你的代码变得更容易阅读和理解，执行的流程也变得更加清晰。

happy path意味着代码要尽量左对齐，减少嵌套，如下图所示：

![](../../assets/83e696a984f9e8fe.png)


注：上图中原始素材来自于网络。


在编码实践中，要满足happy path有几个技巧：

- 减少else、else if的使用；
- 避免if语句的嵌套使用；
- 快速返回。在if语句的body中使用return从函数中返回，而不是继续后续的处理。

注：极客时间的

[《Go语言第一课》专栏]的[第18讲]对if语句做了更为全面的讲解，欢迎大家订阅学习。

## 2. for语句

印象中，for语句在使用频度方面是仅次于的if语句的控制流语句了。这里谈谈Go对于循环语句的支持的特点。

### 2.1 仅此一种for循环

Go信奉“做一件事只有一种方法”，不知道这是不是Go仅提供一种形式for语句的最初原因(相较于其他主流编程语言提供while、loop、do…while等)。

Go经典的for语句有如下一些典型使用形式：

```
// 最常规的for循环
for i := 0; i < 10; i++ {
fmt.Println(i)
}
// 模拟while循环
i := 0
for i < 10 {
fmt.Println(i)
i++
}
// 死循环
for {
// do something
}
```


### 2.2 for range不是可有可无

如果说go只有for语句，也不够准确，go还有一个for range变体。不过这个for range变体不是可有可无的，有些遍历没有for range无法完成，比如：

```
// 遍历map
for k, v := range aMap {
}
// 遍历string中的字符(非字节遍历)
for i, r := range s {
// rune
}
```


### 2.3 带label与不带label的continue和break

在Go语言中，for循环语句中可以使用带label的continue和break语句，也可以使用我们通常认知中的不带label的continue和break语句。不过它们之间的差别应该牢记：

- 不带label的continue和break语句

不带label的continue和break语句只能用于当前for循环语句中，它们的作用范围仅限于当前循环体内部。当执行continue语句时，会跳过本次循环，直接进入下一次循环；当执行break语句时，会结束当前循环，直接跳出循环体。

- 带label的continue和break语句

带label的continue和break语句可以用于多层嵌套的for循环语句中，它们可以跳出指定的循环体。当执行带label的continue语句时，会跳过指定的循环体中的本次循环，直接进入下一次循环；当执行带label的break语句时，会结束指定的循环体，直接跳出循环。

下面是一个使用带label的break语句的示例：

```
package main
import "fmt"
func main() {
outerLoop:
for i := 1; i <= 3; i++ {
for j := 1; j <= 3; j++ {
if i == 2 && j == 2 {
// 跳出指定循环体
fmt.Println("跳出外层循环")
break outerLoop
}
fmt.Printf("i=%d, j=%d\n", i, j)
}
}
}
```


在这个例子中，我们使用带label的break语句跳出了外层循环，从而避免了继续执行外层循环。如果使用不带label的break语句，仅会跳出内层循环，而不会跳出外层循环。

### 2.4 坑

虽然Go只有一种for语句形式，但可能遇到的“坑”却并不少，这里列出一些典型的“坑”：

- 循环变量重用

看一下下面代码：

```
func main() {
var m = []int{1, 2, 3, 4, 5}
for i, v := range m {
go func() {
time.Sleep(time.Second * 3)
fmt.Println(i, v)
}()
}
time.Sleep(time.Second * 10)
}
```


你预期的输出是什么呢？实际输出是什么呢？在go playground中执行一下，得到如下结果：

```
4 5
4 5
4 5
4 5
4 5
```


为什么会输出这个结果呢？我将上述代码做一个等价变换你就明白了：

```
func main() {
var m = []int{1, 2, 3, 4, 5}
{
i, v := 0, 0
for i, v = range m {
go func() {
time.Sleep(time.Second * 3)
fmt.Println(i, v)
}()
}
}
time.Sleep(time.Second * 10)
}
```


我们看到：i, v两个变量不是在每次循环时重新声明，而是在整个循环过程中只定义了一份，这就是为何所有goroutine输出的都是“4 5”的原因。[Go团队针对这个问题正在设计优化方法](https://github.com/golang/go/discussions/56010)，在后续的Go版本中，这个坑可能会被自然“修复”。

- range表达式副本

我们再来看一段代码：

```
func main() {
var a = [5]int{1, 2, 3, 4, 5}
var r [5]int
fmt.Println("original a =", a)
for i, v := range a {
if i == 0 {
a[1] = 12
a[2] = 13
}
r[i] = v
}
fmt.Println("after for range loop, r =", r)
fmt.Println("after for range loop, a =", a)
}
```


在你的预期中，上面程序的输出结果是这样的：

```
original a = [1 2 3 4 5]
after for range loop, r = [1 12 13 4 5]
after for range loop, a = [1 12 13 4 5]
```


不过实际运行一下，你会看到真正的输出是这样的：

```
original a = [1 2 3 4 5]
after for range loop, r = [1 2 3 4 5]
after for range loop, a = [1 12 13 4 5]
```


究其原因，是因为参数range循环的是a的副本，我们用a’来表示，将上面代码等价变换为下面后，就更容易理解了：

```
for i, v := range a' { //a'是a的一个值拷贝
if i == 0 {
a[1] = 12
a[2] = 13
}
r[i] = v
}
```


这样变换后，我们知道for range遍历的是a的副本，对a的修改不会影响后续的遍历。

因此，当使用数组、切片作为range后的待遍历的容器集合时，要十分小心。

- break未跳出for

当for与switch语句联合使用时，也要注意避坑，看一下下面代码：

```
func main() {
var sl = []int{5, 19, 6, 3, 8, 12}
var firstEven int = -1
// find first even number of the interger slice
for i := 0; i < len(sl); i++ {
switch sl[i] % 2 {
case 0:
firstEven = sl[i]
break
case 1:
// do nothing
}
}
println(firstEven)
}
```


执行这个代码，输出结果为12，与我们预期的第一个偶数6不符。原因是什么呢？从输出结果为12来看，应该是break并未跳出for循环，导致循环继续进行到最后。

记住：Go语言规范中明确规定，不带label的break语句中断执行并跳出的，是同一函数内break语句所在的最内层的for、switch或select。所以，上面这个例子的break语句实际上只跳出了switch语句，并没有跳出外层的for循环，这也就是程序未按我们预期执行的原因。

注：极客时间的

[《Go语言第一课》专栏]的[第19讲]对for语句做了更为全面的讲解，欢迎大家订阅学习。

## 3. switch语句

最后聊聊switch语句。在Go语言中，switch语句也是一种常用的控制流语句，它可以根据不同的条件执行不同的代码块：

```
switch expression {
case value1:
// 执行代码块1
case value2:
// 执行代码块2
default:
// 执行默认代码块
}
```


由于Go switch语句执行语义不会默认执行下一个case，因此上述switch语句等价于一个多个if-else的语句，但从可读性上来说，比多层的if else更易理解，可读性更好。在这样的场景下，我们是推荐使用switch替代多个if-else语句的。

### 3.1 case语句求值顺序

switch语句通常会有很多表达式，这些表达式的求值顺序是有明确规定的，即从switch表达式开始求值，然后各个case语句的求值顺序是从上到下，从左到右的。记住这个顺序，有助于你分析switch语句的执行语义。

### 3.2 switch case的灵活性

Go switch语句在语法语义方面相对于其先祖C语言的Switch语句来说，做了很多优化，结果是更加灵活，坑几乎填平，主要的优化包括：

-
switch支持任何值的case比较，而不像C语言只能用int或枚举

-
支持case表达式列表


```
package main
import "fmt"
func main() {
num := 3
switch num {
case 1, 3, 5: // case支持表达式列表
fmt.Println("奇数")
case 2, 4, 6:
fmt.Println("偶数")
default:
fmt.Println("其他")
}
}
```


- 不会默认执行下一个case语句

C语言中那种默认执行下一个case语句的执行语义导致我们需要在每个case中都使用break跳出switch，Go修复了这个语义，看下面这个例子：

```
package main
import "fmt"
func main() {
num := 2
switch num {
case 1:
fmt.Println("第一个 case 块")
case 2:
fmt.Println("第二个 case 块")
case 3:
fmt.Println("第三个 case 块")
}
}
```


这个例子只会输出“第二个 case 块”，不会执行case 3中的代码。

如果要显式告知执行下一个case代码块，需要使用fallthrough。显然Go将常见执行逻辑作为默认语义，即每个case执行完跳出；而C语言恰做反了。

### 3.3 type switch

这个是其他语言所没有的，又或者说是Go特有的，type switch是针对接口类型表达式的特殊语法，语法格式也比较固定：

```
var x interface{} = 3
switch i := x.(type) {
case nil:
// x 的类型为 nil
println(i) // 输出x中存储的动态类型值
case int:
// x 的类型为 int
case string:
// x 的类型为 string
default:
// x 的类型为其他类型
}
```


如果不需要接口变量中存储的动态类型值的话，也可以简化为：

```
var x interface{} = 3
switch x.(type) {
case nil:
// x 的类型为 nil
case int:
// x 的类型为 int
case string:
// x 的类型为 string
default:
// x 的类型为其他类型
}
```


注：极客时间的

[《Go语言第一课》专栏]的[第20讲]对switch语句做了更为全面的讲解，欢迎大家订阅学习。

## 4. 小结

Go语言的控制流语句虽然种类不那么丰富，但足够帮助开发者实现各种不同类型的程序逻辑了。在编写代码时，需要根据具体的需求选择合适的控制语句，并注意遵循使用各种控制语句的惯例和规范，避免掉入各种“坑”中。

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