---
title: defer函数参数求值简要分析
url: https://tonybai.com/2018/03/23/the-analysis-of-the-param-evaluation-of-defer-functions/
published: '2018-03-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# defer函数参数求值简要分析

### 一. 引子

书接上文，在发表了[《对一段Go语言代码输出结果的简要分析》](https://tonybai.com/2018/03/20/the-analysis-of-output-results-of-a-go-code-snippet/)一文之后，原问题提出者又有了新问题，这是一个典型Gopher学习Go的历程，想必很多Gopher们，包括我自己都遇到过的。我们先来看看这段代码(来自原问题提出者)：

```
// https://play.golang.org/p/dOUFNj96EIQ
package main
import "fmt"
func main() {
var i int = 1
defer fmt.Println("result =>",func() int { return i * 2 }())
i++
}
```


这里显然有坑！初学者的常规逻辑一般是：defer是在main函数退出后执行，退出前i已经做了+1操作，值变成了2，这样一来defer后的Println应该输出：**result => 4** 才对！实际输出结果呢？

```
result => 2
```


**这怎么可能？**

实际上不光是defer这样，即使用go关键字替换掉defer，输出的结果也是一样的：**result => 2**：

```
package main
import (
"fmt"
"time"
)
func main() {
var i int = 1
go fmt.Println("result =>",func() int { return i * 2 }())
i++
time.Sleep(3*time.Second)
}
```


### 二. defer function分析

那么究竟为什么输出的是2，而不是4呢？因为无论是go关键字还是defer关键字，在代码执行到它们时，**编译器都要为它们后面的函数准备好函数调用的参数堆栈，要确定的参数值和参数类型大小**。这样一来就得去求值：对它们后面的函数的参数进行[求值](https://tonybai.com/2015/08/27/understanding-go-statements-evaluating-order/)。

以本文第一个defer那个例子为例！我们需要为defer后面的函数进行[参数求值](https://tonybai.com/2015/08/27/understanding-go-statements-evaluating-order/)：

```
defer fmt.Println("result =>",func() int { return i * 2 }())
```


此时defer后面的函数是Println，这里Println有两个输入参数：”result =>”和func() int {return i * 2}()，前者就是一个字符串常量值，而后者是一个函数调用，我们需要对该函数调用进行求值。而在此时，i依然为1，因此Println的第二个参数的求值结果为2，于是上面defer的调用就等价于：

```
defer fmt.Println("result =>",2)
```


因此，无论最终i的值变成了多少，defer最终的输出都是：**result => 2**。go关键字后面的参数亦是如此。其实这个过程与为普通函数的调用做准备是一样的，也要先对函数的参数进行求值，之后再进入函数体，只不过defer将进入函数执行的过程推迟到defer的调用方退出之前了。

搞清楚这个defer原理后，我们如果想在defer函数执行时输出4，那么使用一个闭包函数即可：

```
// https://play.golang.org/p/Eux7zpSr7O8
package main
import "fmt"
func main() {
var i int = 1
defer func() {
fmt.Println("result =>", func() int { return i * 2 }())
}()
i++
}
```


这里我们看到defer 后面是一个不带任何参数的匿名函数，所谓的对参数求值也是无值可求。在main函数退出前，defer后面的匿名函数真正执行时i的值已经是2，因此闭包函数中的Println输出4。

### 三. defer method分析

defer后面除了可以跟着普通函数调用外，还可以使用方法调用(method)：

```
defer instance.Method(x,y)
```


这可能又会让初学者有些迷惑，多数又是Method的receiver类型以及go自动对instance的Method调用解引用或求地址的问题，我们“趁热打铁”，再来基于上一篇文章[《对一段Go语言代码输出结果的简要分析》](https://tonybai.com/2018/03/20/the-analysis-of-output-results-of-a-go-code-snippet/)中的例子做些修改，看看将go关键字换成defer会是一种什么情况：

```
//https://play.golang.org/p/T8CdRfEn2h4
package main
import (
"fmt"
)
type field struct {
name string
}
func (p *field) print() {
fmt.Println(p.name)
}
func main() {
data1 := []*field{{"one"}, {"two"}, {"three"}}
for _, v := range data1 {
defer v.print()
}
data2 := []field{{"four"}, {"five"}, {"six"}}
for _, v := range data2 {
defer v.print()
}
}
```


这段代码运行起来输出：

```
six
six
six
three
two
one
```


有了[《对一段Go语言代码输出结果的简要分析》](https://tonybai.com/2018/03/20/the-analysis-of-output-results-of-a-go-code-snippet/)一文中的思路作为基础，对上面这段代码的分析也就不难了。没错，还是按照我上一篇的“等价转换”思路去思考，将method转换为function后，再分析。上面的代码可以**等价变换**为下面代码：

```
https://play.golang.org/p/a-vOSz4N3jb
package main
import (
"fmt"
)
type field struct {
name string
}
func print(p *field) {
fmt.Println(p.name)
}
func main() {
data1 := []*field{{"one"}, {"two"}, {"three"}}
for _, v := range data1 {
defer print(v)
}
data2 := []field{{"four"}, {"five"}, {"six"}}
for _, v := range data2 {
defer print(&v)
}
}
```


接下来，我们就利用defer的“参数实时求值”原理，对上面的代码作分析：

data1的三次迭代：defer的参数求值完后，defer print(v)调用分别变成了：

- defer print(&field{“one”})
- defer print(&field{“two”})
- defer print(&field{“three”})

data2的三次迭代，defer的参数求值完后，defer print(v)调用分别变成了：

- defer print(&v)
- defer print(&v)
- defer print(&v)

于是在main退出前，defer函数按defer被调用的反向顺序执行：

- print(&v)
- print(&v)
- print(&v)
- print(&field{“three”})
- print(&field{“two”})
- print(&field{“one”})

而此刻：v中存储的值为field{“six”}，于是前三次print均输出”six”。

### 四. 小结

defer虽然带来一些性能损耗，但defer的适当使用可以让程序的逻辑结构变得更为简洁。

[《对一段Go语言代码输出结果的简要分析》](https://tonybai.com/2018/03/20/the-analysis-of-output-results-of-a-go-code-snippet/)一文发出后，出乎意料地收到一些反馈，其实很多Go初学者希望能看到一些像这样的入门，但又“较真”的，最好再涉及点底层实现的文章。以后有精力会多多关注这一点的。欢迎大家来本站继续交流，从各位朋友提出的问题中，我也能收获到灵感^0^。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

谢谢解惑，十分感谢，能否加您微信？可以的话，麻烦您给我发邮件，谢谢

冒昧说一句，现在go1.16.2的版本上执行，其结果是result => 4 。

我搞错了，不好意思。多谢你的博客。

ok。欢迎多多交流。