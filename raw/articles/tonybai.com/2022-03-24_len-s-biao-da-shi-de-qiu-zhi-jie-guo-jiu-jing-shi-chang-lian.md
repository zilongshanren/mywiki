---
title: len(s)表达式的求值结果究竟是常量还是变量？我来告诉你
url: https://tonybai.com/2022/03/24/the-result-of-a-len-expression-is-constant-or-variable/
published: '2022-03-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# len(s)表达式的求值结果究竟是常量还是变量？我来告诉你

![](../../assets/cb5a436d20a5c3f7.png)


[本文永久链接](https://tonybai.com/2022/03/24/the-result-of-a-len-expression-is-constant-or-variable) – https://tonybai.com/2022/03/24/the-result-of-a-len-expression-is-constant-or-variable

**len**是[Go预定义标识符](https://go.dev/ref/spec#Predeclared_identifiers)，同时也是Go内置的预定义函数，通过go doc工具我们能查到len函数的doc如下：

```
$go doc builtin.len
package builtin // import "builtin"
func len(v Type) int
The len built-in function returns the length of v, according to its type:
Array: the number of elements in v.
Pointer to array: the number of elements in *v (even if v is nil).
Slice, or map: the number of elements in v; if v is nil, len(v) is zero.
String: the number of bytes in v.
Channel: the number of elements queued (unread) in the channel buffer;
if v is nil, len(v) is zero.
For some arguments, such as a string literal or a simple array expression,
the result can be a constant. See the Go language specification's "Length
and capacity" section for details.
```


对于len函数，即便是Go初学者也不会陌生，因为在日常Go开发中，len是一个高频使用的函数。len的参数主要是复合数据类型的变量，比如数组(包括执行数组的指针类型)、切片、字符串、channel等，返回的结果是这些复合数据变量的长度(length)，是一个int类型的值。太多细节我就不说了，大家可能也都很熟悉。我要说的是，关于len函数的一个大家可能不熟悉的或不太在意的地方，那就是len(s)表达式在什么时候的求值结果为一个常量(constant)，什么时候的求值结果为变量。别忽视这个细节，这很可能让你的程序输出你意想不到的结果，下面我就来举例说明。

这个例子来自于[《Go 101》](https://go101.org)的作者老貘的[在推特上发的一个go quiz](https://twitter.com/go100and1/status/1505022780277870592)，其问题原貌是这样的：

```
package main
func f() int { return 1 }
var x = [8]int{f()}
var p byte = ( 1 << len([8]int{f()}) ) / 2
var q byte = ( 1 << len(x) ) / 2
func main() {
println(p, q)
}
```


问上面的例子的输出结果是什么！

来给你五分钟思考一下！… …

好了，思考时间结束！估计你已经在[Go playground](https://go.dev/play/)或Go编译器上运行过这个quiz并已经得到正确答案了：**0 128**。

不论你是自己推导出来的，还是通过运行源码得到的结果，现在你来告诉我上述quiz输出**0 128**的原因！

我估计很多人和我最初一样，也是“丈二和尚摸不着头脑”！

- len的返回值不是int么？为什么赋值给类型为byte的p或q没有报编译错误？
- 为什么p是0，而q是128呢？

… …

下面是我的分析，大家参考一下，看看能否回答你的疑问：

首先一点，p、q的唯一不同是q变量声明的右侧的表达式直接使用的是数组x的长度：len(x)，而p变量声明的右侧表达式中len函数的参数为[8]int{f()}，这是一个临时数组且包含了带有函数调用的元素赋值操作。显然这个差异决定了最终结果的不同。

**针对Go语言细节上的疑问， Go官方的语言spec才是最权威的参考资料**。打开Go language spec，定位到

**Length and capacity**一节，我们看到其中关于len(s)表达式求值结果的说明如下：

```
The expression len(s) is constant if s is a string constant. The expressions len(s) and cap(s) are constants if the type of s is an array or pointer to an array and the expression s does not contain channel receives or (non-constant) function calls; in this case s is not evaluated. Otherwise, invocations of lenand cap are not constant and s is evaluated.
```


这段话的大致含义是，对于len(s)这个表达式来说，

- 如果s是一个字符串常量，那么len(s)表达式也是一个常量(constant)；
- 如果s是一个数组或指向数组的指针并且
**表达式s中不包含channel接收调用或非常量(non-constant)的函数调用**，那么len(s)表达式是常量，这种情况下我们无需对s进行求值。 - 其余情况，len(s)表达式的结果都不是常量，都需要对s进行求值(evaluate)。

怎么理解第二条中的“非常量函数调用”呢？Go spec中给了一个例子：

```
var z complex128
const (
c4 = len([10]float64{imag(2i)}) // imag(2i) is a constant and no function call is issued
c5 = len([10]float64{imag(z)}) // invalid: imag(z) is a (non-constant) function call
)
```


例子中，c4和c5两个声明的右侧都是对数组进行的len函数调用。c4中的len(s)中的s为[10]float64{imag(2i)}，这是一个数组，它包含一个imag函数调用，但由于imag的参数为一个常量，因此[imag的调用返回也是常量](https://go.dev/ref/spec#Constants)，不是一次non-constant的函数调用，因此，c4声明语句右侧的len表达式实质是一个常量。

c5中的len(s)中的s为[10]float64{imag(z)}，这同样是一个数组，并同样包含了imag函数调用，不同的是imag的参数为一个complex128类型的变量，因此imag函数这次调用是一次non-constant的函数调用，返回值不能作为常量，于是针对这样的s，len表达式的值也不会是常量，于是len表达式的值不能作为常量c5的初始值。

有了上面的知识准备后，我们再来看上面的quiz中的变量p和q。我们先来看变量q：

```
var x = [8]int{f()}
var q byte = ( 1 << len(x) ) / 2
```


我们看到变量q右边的初值表达式中的len函数的参数为数组x，且该表达式(x)中不包含任何函数调用，这符合len(s)是常量的条件，于是len(x)就是一个常量，这也就意味着上面q的声明语句等价于下面的语句：

```
var q byte = ( 1 << 8 ) / 2
```


等价语句的等号右侧就是一个无类型的整型字面值常量，**这个常量值在编译期就完成了计算**，值为128，类型为byte的变量q可以存储下128这个数值，于是q就等于128（关于无类型常量的特性，在我的[“Go语言第一课”](http://gk.link/a/10AVZ)中有详细讲解）。

我们再来看看变量p：

```
var p byte = ( 1 << len([8]int{f()}) ) / 2
```


我们这里的len表达式中包含了一个f()的函数调用，f()是否是non-constant函数调用呢？用下面的代码测试一下就知道了：

```
func f() int { return 1 }
const (
b byte = imag(2i) // ok
c byte = f() // 编译器错误：f() (value of type int) is not constant
)
```


我们看到f()不是一个像imag那样的常量函数调用，因此p变量声明中的len(s)不是一个常量。那么该len(s)表达式在给变量p赋值时就需要有一个表达式求值的过程。

那么( 1 << len([8]int{f()}) ) / 2这个表达式的求值过程又是如何的呢？这是一个左移操作符(<<)，该操作符左边的操作数为无类型常量1，那么在这个表达式的求值过程中，1的类型究竟是什么呢？是无类型常量的默认类型int还是等号左边的变量类型byte呢？

我们又要求助于go spec了，go spec中[关于左移/右移表达式有一段说明](https://go.dev/ref/spec#Operators)如下：

```
The right operand in a shift expression must have integer type or be an untyped constant representable by a value of type uint. If the left operand of a non-constant shift expression is an untyped constant, it is first implicitly converted to the type it would assume if the shift expression were replaced by its left operand alone.
```


其大致意思是shift表达式中的右操作数必须是一个整型类型或是一个可由uint类型值表示的无类型常量。如果一个非常量的shift表达式的左操作数是一个无类型常量，它会被首先隐式转换为一种类型，什么类型呢？就是将整个shift表达式用左操作数替换后左操作数的类型。

最后这句太绕口，我们举个例子说明一下，下面例子来自go spec：

```
var s uint = 33
var j int32 = 1<<s
```


变量j的声明语句的右侧为shift表达式，且该shift表达式是一个非常量的shift表达式，其中无类型常量1的类型怎么确定呢？按照上面说法，该表达式中1的类型等价于下面语句中1的类型：

```
var j int32 = 1 // 用shift表达式的左操作数(1)替换整个shift表达式(1 << s)后
```


我们看到1是无类型常量，它的最终类型取决于语句左侧的变量类型，于是1的类型为int32，最终1<<s的类型也就为int32(go spec: Arithmetic operators apply to numeric values and yield a result of the same type as the first operand)。

好了，我们再回到变量p中的shift表达式。该表达式也不是常量shift表达式。这样其中1的类型就等价于下面语句中1的类型：

```
var p byte = 1
```


即1这个无类型常量的类型为byte，于是 1 << len([8]int{f()})在左移8bit后溢出，结果是0，于是变量p的右侧表达式求值为0，p值也就为0。

Go语言虽然以简单著称，但Go中的语法细节也并不少。[老貘的这道go quiz题目](https://twitter.com/go100and1/status/1505022780277870592)非常考验大家对Go语言语法细节把握的功力！

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/85dcf3b32b884fe1.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


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

## 评论