---
title: Go 1.22引入的包级变量初始化次序问题
url: https://tonybai.com/2024/03/29/the-issue-in-pkg-level-var-init-order-in-go-1-22/
published: '2024-03-29'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.22引入的包级变量初始化次序问题

![](../../assets/00cb382ecbb1ad0a.png)


[本文永久链接](https://tonybai.com/2024/03/29/the-issue-in-pkg-level-var-init-order-in-go-1-22) – https://tonybai.com/2024/03/29/the-issue-in-pkg-level-var-init-order-in-go-1-22

细心的朋友可能已经注意到，从春节后，我的博客就“停更”了！实际上，这一情况部分是因为工作上的事务繁忙，另一部分则是因为我将工作之外的闲暇时间更多地投入到一本即将于今年中下旬出版的书的撰写了：在之前的积累基础上，我花了两个多月的时间完成了初稿。

当然，我也深切地怀念博客写作所带来的乐趣和与读者的互动。正巧，今天一位学员在[《Go语言第一课》专栏](http://gk.link/a/10AVZ)留言给了我一个恢复下笔的机会。借此，我也准备恢复一下博客写作的节奏。

另外预告一下：我和我的技术团队

合作翻译的一本Go语言入门书最早也将于2024年4月份上市，敬请期待！

在[《Go语言第一课》专栏](http://gk.link/a/10AVZ)的[第8讲](https://time.geekbang.org/column/article/432021)中，我曾系统讲解了Go包的初始化次序，以及Go包内包级变量、常量、init函数等的初始化次序。讲这些的初衷就是希望Go初学者能先了解一下Go程序的执行次序，这样在后续阅读和理解Go代码的时候，就好比拥有了“通往宝藏的地图”，可以直接沿着Go代码执行次序这张“地图”去阅读和理解Go代码，而不会在庞大的代码库中迷失了。

相对于早期的Go版本，Go包的初始化次序在[Go 1.21版本](https://go.dev/doc/go1.21)开始会有所变化，这个可以看我的[《Go 1.21中值得关注的几个变化》](https://tonybai.com/2023/08/20/some-changes-in-go-1-21)一文了解详情。

不过除了Go包的初始化次序得以明确之外，Go在1.22版本中的包级变量初始化次序也发生了一些“变化”，但[Go 1.22的Release Notes](https://go.dev/doc/go1.22)压根没提到Go包内的变量初始化次序会有变化。究竟这些变化是有意为之，还是由于代码变更而引入的新问题呢？我们还得从近期[《Go语言第一课》专栏](http://gk.link/a/10AVZ)的一位读者提出的问题讲起！

## 1. Go 1.22的输出结果与专栏文章中不同！

原专栏中的代码较多，为方便起见我又写了一段简化版的代码，可以等价地反映问题。下面的代码用于演示包级变量、常量和init函数的初始化次序：

```
// initorder.go
package main
import (
"fmt"
)
var (
v0 = constInitCheck()
v1 = variableInit("v1")
v2 = variableInit("v2")
)
const (
c1 = "c1"
c2 = "c2"
)
func constInitCheck() string {
if c1 != "" {
fmt.Println("main: const c1 has been initialized")
}
if c1 != "" {
fmt.Println("main: const c2 has been initialized")
}
return ""
}
func variableInit(name string) string {
fmt.Printf("main: var %s has been initialized\n", name)
return name
}
func init() {
fmt.Println("main: first init func invoked")
}
func init() {
fmt.Println("main: second init func invoked")
}
func main() {
// do nothing
}
```


使用Go 1.22版本之前的版本，比如[Go 1.21版本](https://tonybai.com/2023/08/20/some-changes-in-go-1-21/)，运行该程序的输出结果如下：

```
$go run initorder.go
main: const c1 has been initialized
main: const c2 has been initialized
main: var v1 has been initialized
main: var v2 has been initialized
main: first init func invoked
main: second init func invoked
```


这个输出结果也是专栏文章中的输出结果，即包级元素的初始化顺序是：常量 -> 变量 -> init函数。三个变量的初始化次序是v0 -> v1 -> v2。

但专栏的一位读者在使用最新Go 1.22版本运行上述程序后，却提出了如下问题：

![](../../assets/5c89be65ab0ab818.png)


总结一下这个问题的两个关键点如下：

- Go 1.22版本运行上述程序的输出结果与文章中的结果不一致
- 将const声明block搬移到var声明block的前面后，使用Go 1.22版本的输出结果与文章中的一致

我们先来复现一下问题。我使用Go 1.22.0运行上面的initorder.go，得到下面结果：

```
$go run main.go
main: var v1 has been initialized
main: var v2 has been initialized
main: const c1 has been initialized
main: const c2 has been initialized
main: first init func invoked
main: second init func invoked
```


该输出结果确如读者所说，与文中的输出顺序不一致了，变量的初始化次序变为了v1 -> v2 -> v0。这会让很多读者误以为包内元素的初始化次序变成了“变量 -> 常量 -> init函数”。是否真的如此了呢？我们下面来初步分析一下。

## 2. 原因初步分析

[Go语言规范](https://go.dev/ref/spec)中对[包内变量初始化次序的说明](https://go.dev/ref/spec#Package_initialization)是这样的（截至2024.03）：

Within a package, package-level variable initialization proceeds stepwise, with each step selecting the variable earliest in declaration order which has no dependencies on uninitialized variables. More precisely, a package-level variable is considered ready for initialization if it is not yet initialized and either has no initialization expression or its initialization expression has no dependencies on uninitialized variables. Initialization proceeds by repeatedly initializing the next package-level variable that is earliest in declaration order and ready for initialization, until there are no variables ready for initialization. Multiple variables on the left-hand side of a variable declaration initialized by single (multi-valued) expression on the right-hand side are initialized together: If any of the variables on the left-hand side is initialized, all those variables are initialized in the same step. For the purpose of package initialization, blank variables are treated like any other variables in declarations.


粗略翻译后大致意思如下：

在包内，包级变量初始化逐步进行，每一步都会选择声明顺序中最早的且不依赖于未初始化变量的那个变量。更准确地说，如果包级变量尚未初始化并且没有初始化表达式或其初始化表达式不依赖于未初始化的变量，则认为该变量具备初始化条件。通过重复初始化声明顺序中最早且具备初始化条件的下一个包级变量来进行初始化，直到没有具备初始化条件的变量为止。由右侧单个（多值）表达式初始化的变量声明左侧的多个变量会一起初始化：如果左侧的任何变量被初始化，则所有这些变量都会被初始化在同一步骤中。出于包初始化的目的，空变量也被视为与声明中的任何其他变量一样。


按照Go语言规范的描述，我们来理论推导一下v0、v1和v2的初始化次序：

```
var (
v0 = constInitCheck()
v1 = variableInit("v1")
v2 = variableInit("v2")
)
```


- 第一轮：待初始化的包级变量集合{v0, v1, v2}。在这一轮，我们按声明顺序逐一看一下这三个变量。

v0未初始化，其声明语句的右侧有初始化表达式(initialization expression)，且这个初始化表达式式(constInitCheck)不依赖未初始化的变量（仅仅依赖两个常量c1和c2），因此按照Spec描述，v0具备初始化条件，会先进行初始化，于是constInitCheck会被调用。

- 第二轮：待初始化的包级变量集合{v1, v2}。

按声明顺序，先看v1。和v0一样，其声明语句的右侧有初始化表达式，且这个初始化表达式式（variableInit)不依赖未初始化的变量，因此按照Spec描述，v1具备初始化条件，会进行初始化，于是variableInit会被调用。

- 第三轮：待初始化的包级变量集合{v2}。

这个没啥可推导的了，初始化v2就是了！

这样，包级变量的声明次序就应该是v0 -> v1 -> v2。这个理论推导结果显然与Go 1.22版之前的输出结果是一致的。但与Go 1.22版本的输出结果有悖。

那么Go 1.22版本为什么没有将v0作为第一个具备初始化条件的变量对其进行初始化呢？v0有初始化表达式constInitCheck，该函数没有依赖任何未初始化的包级变量，但该函数内部依赖了两个常量c1和c2：

```
func constInitCheck() string {
if c1 != "" {
fmt.Println("main: const c1 has been initialized")
}
if c1 != "" {
fmt.Println("main: const c2 has been initialized")
}
return ""
}
```


我们大胆地猜测一下：Go 1.22版本将**c1和c2当成了“未初始化的变量”了**！还记得读者问题的第二个关键点吗：“将const声明block搬移到var声明block的前面后，使用Go 1.22版本的输出结果便与文章中的一致”。按照Go 1.22的逻辑，将常量声明放到前面后，按顺序常量先被初始化了。这样到v0时，v0具备初始化的条件就成立了，于是v0就可以先被初始化了。

## 3. “一波三折”的issue

为了证实上述推测，我在github.com/golang/go提了[issue 66575](https://github.com/golang/go/issues/66575)，并对上述问题做了阐述，不过该issue被Go团队的年轻成员[Sean Liao](https://github.com/seankhliao)“闪电”关闭了。

好在几个小时后，Go大神[Keith Randall](https://github.com/randall77)看到了这个issue，并支持了我的猜测！他还闪电般地找出了[导致Go 1.22版本出现此问题的commit](https://go-review.googlesource.com/c/go/+/517617)，并给出了[fix方案：cmd/compile: put constants before variables in initialization order](https://go-review.googlesource.com/c/go/+/575075)。fix方案的思路就是将所有常量的初始化放到变量之前。

该[fix merge到主干](https://github.com/golang/go/commit/8f618c1f5329bd81912f8f776cb8bf028c750687)后，Gobot自动关闭了该issue。

但严谨的Keith Randall随后reopen了该issue，并圈了Go语言之父的[Robert Griesemer](https://github.com/griesemer)，希望后者确定一下是否需要更新一下Go spec。

目前该issue已经被加入[Go 1.23 milestone](https://github.com/golang/go/milestone/212)，并会在Go 1.23 fix。

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

这个问题也困扰了好久。。。

这位年轻成员Sean Liao有点草率了

观察过sean liao回复的若干个issue，基本都是以close为第一选择:)，感觉考虑问题的确不够全面，可能的确是因为在go团队混得时间不长的原因吧。初始化次序的问题，官方已经决定恢复到Go 1.22之前的状态了。并且在Go 1.22.5还是Go 1.22.6就fix了。