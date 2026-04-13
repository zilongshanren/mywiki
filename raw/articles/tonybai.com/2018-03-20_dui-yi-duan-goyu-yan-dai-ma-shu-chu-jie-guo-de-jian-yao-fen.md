---
title: 对一段Go语言代码输出结果的简要分析
url: https://tonybai.com/2018/03/20/the-analysis-of-output-results-of-a-go-code-snippet/
published: '2018-03-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 对一段Go语言代码输出结果的简要分析

年后事情实在是多，各种被催进度，于是好长一段时间未更博客了，自责中….。今天蹦出来热热身^0^！

中午在微博私信中看到一封来自某Gopher的咨询，他贴了一段代码，并表示对代码的输出结果的不解，希望我能帮他分析一下。他的代码如下：

```
//testslicerange.go
package main
import (
"fmt"
"time"
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
go v.print()
}
data2 := []field{{"four"}, {"five"}, {"six"}}
for _, v := range data2 {
go v.print()
}
time.Sleep(3 * time.Second)
}
```


在[go playground](https://play.golang.org/p/DHRZcm2oNGx)上，其输出结果为(在我的多核mac，[Go 1.10](http://tonybai.com/2018/02/17/some-changes-in-go-1-10/)上面程序与此稍有不同，输出的item相同，只是前后顺序有不同)：

```
one
two
three
six
six
six
```


虽然这位Gopher并没有明确说明他的疑惑究竟是什么？但从上述的输出结果来看，他一定是想问：为什么对data2的迭代输出的是三个”six”，而不是four、five、six？

好了，我来分析一下。首先，我要对这个程序做个**等价变换**，变换后的程序源码如下：

```
//testslicerange-transform.go
package main
import (
"fmt"
"time"
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
go print(v)
}
data2 := []field{{"four"}, {"five"}, {"six"}}
for _, v := range data2 {
go print(&v)
}
time.Sleep(3 * time.Second)
}
```


这里我把field结构体的method：print，换成了普通的以field指针作为第一个参数的函数print，这个变换是等价的，因为go中的method本质上就是以method的receiver作为第一个参数的普通function，即：

```
instance.method(x,y) <=> function(instance, x,y)
```


因此，执行上述的变换后的testslicerange-transform.go，得到的结果与testslicerange.go是一致的：

```
one
two
three
six
six
six
```


这样变换以后，问题是不是豁然开朗了，你可以很清楚地看到使用go关键字启动一个新goroutine时是如何绑定参数的：

```
- 迭代data1时，由于data1中的元素类型是field指针，因此赋值后v就是元素地址， 每次调用print时传入的参数(v)实际上也是各个field元素的地址；
- 迭代data2时，由于data2中的元素类型是field（非指针），因此赋值后v是元素的copy，每次传入的&v实际上是v的地址，而不是被copy的元素的地址；
```


剩下的就是for range常见的那个”坑”的问题（在我的[《关于Go，你可能不注意的7件事》](https://tonybai.com/2015/09/17/7-things-you-may-not-pay-attation-to-in-go/)一文中有详尽说明），那就是v在整个for range过程只有一个，data2迭代完成之后，**v是元素”six”的copy**。

这样，一旦启动的各个child goroutine在main goroutine执行到Sleep时才被[调度](https://tonybai.com/2017/06/23/an-intro-about-goroutine-scheduler/)执行，那么最后的三个goroutine在打印&v时，打印的也就都v

中存放的值”six”了。而前三个child goroutine各自传入的是元素(“one”、”two”、”three”)的地址，打印的就是”one”、”two”、”three”。

那么原程序如何修改一下才能让其按期望输出(“one”、”two”、”three”, “four”, “five”, “six”)呢？我们来改一下：只需将field method的receiver type由*field改为field即可。

```
// testslicerange1.go
package main
import (
"fmt"
"time"
)
type field struct {
name string
}
func (p field) print() {
fmt.Println(p.name)
}
func main() {
data1 := []*field{{"one"}, {"two"}, {"three"}}
for _, v := range data1 {
go v.print()
}
data2 := []field{{"four"}, {"five"}, {"six"}}
for _, v := range data2 {
go v.print()
}
time.Sleep(3 * time.Second)
}
```


上述程序在[go playground](https://play.golang.org/p/zrjMf6OQtqm)上的输出为：

```
one
two
three
four
five
six
```


至于为什么，可以参考我的分析思路，自行分析一下。

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

多谢解惑，看完对method的本质理解更深了。（虽然也翻了好几遍go spec，但自己思考时没有意识到[instance.method(x,y) function(instance, x,y)]这样的转换，还是理解不够深入）

再有一点是go func的执行，虽然go routine的执行时机不确定，但func的入参值是在执行go func时就确定的。类似的例子还有这个：https://play.golang.org/p/dOUFNj96EIQ

另外，对于 data1 := []*field{{“one”}, {“two”}, {“three”}} ，{“one”}明明是field类型的常量，但可以隐式转换为*field类型，翻了go spec 没找到解答的位置，真是无法释怀。

defer关键字一定是对后面的函数的参数即时进行参数求值的，你可以对比一下这个：https://play.golang.org/p/Eux7zpSr7O8

我也在最新spec中找了一下：

关于method 本质的描述之一：The type of a method is the type of a function with the receiver as first argument.

关于对receiver自动deference或auto take address，可以参见下面的spec中的描述：

As with selectors, a reference to a non-interface method with a value receiver using a pointer will automatically dereference that pointer: pt.Mv is equivalent to (*pt).Mv.

As with method calls, a reference to a non-interface method with a pointer receiver using an addressable value will automatically take the address of that value: t.Mp is equivalent to (&t).Mp.

我再详细说一下吧。

你的例子中的代码：

package main

import “fmt”

func main() {

var i int = 1

defer fmt.Println(“result =>”,func() int { return i * 2 }())

i++

//prints: result => 2 (not ok if you expected 4)

}

当代码执行到defer时，需要对defer后面的function进行参数求值，而后面的function是Println，就需要对Println的参数进行求值，于是执行了那个匿名函数。匿名函数是一个闭包函数，此时i=1，于是求值结果是2，相当于defer fmt.Println(“result =>”,2)

而我改变的这个例子：

package main

import “fmt”

func main() {

var i int = 1

defer func() {

fmt.Println(“result =>”, func() int { return i * 2 }())

}()

i++

//prints: result => 2 (not ok if you expected 4)

}

同样执行到defer，对defer后面的函数的参数求值，发现没有参数，于是跳过。当main返回前，执行defer，这时func中println参数中的闭包函数求值，此时i=2了，于是输出4.

golang的语法特性很有趣，多谢细致解答~

这个有意思了，没有解读，完全没有头绪， 我居然还在在思考 return 和 defer的顺序…

惭愧惭愧

您好，我是开发者头条的运营。您的《对一段 Go 语言代码输出结果的简要分析》已被我们平台用户推荐到首页。感谢您的辛苦创作，为了让更多读者认识您，我们邀请您来开发者头条分享。与创作不同，您仅需复制粘贴文章链接即可完成分享。您可以在各大应用市场搜索 “开发者头条” 找到我们的应用，欢迎了解。期待您的分享。

for _, v := range data2 {

go print(&v)

}

感谢作者分析的如此详细，我再加一点我的理解，这块有问题的一个重要原因是不是for执行太快，go 启动协程慢，速度不匹配，这样导致最后一个协程启动时拿到的地址是最后一个循环变量的地址，如果这块加个延迟也可以获取正确结果：

for _, v := range data2 {

go print(&v)

time.Sleep(1 * time.Second)

}

当然了，这种做法不可能用到实际中，只是分析分析

嗯，和goroutine调度顺序有关系。

修改一下上面评论

“这样导致最后一个协程启动时拿到的地址是最后一个循环变量的地址”

为

“这样导致这些协程启动时拿到的变量地址都是最后一个循环变量的地址”