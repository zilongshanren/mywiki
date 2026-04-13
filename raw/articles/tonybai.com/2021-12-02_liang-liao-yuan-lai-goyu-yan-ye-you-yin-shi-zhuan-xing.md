---
title: 惊了！原来Go语言也有隐式转型
url: https://tonybai.com/2021/12/02/go-has-implicit-type-convertion/
published: '2021-12-02'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 惊了！原来Go语言也有隐式转型

![](../../assets/0d0a7e60c085cfd7.png)


[本文永久链接](https://tonybai.com/2021/12/02/go-has-implicit-type-convertion) – https://tonybai.com/2021/12/02/go-has-implicit-type-convertion

我的极客时间专栏[《Go语言第一课》上线](https://mp.weixin.qq.com/s/xg_jnbRPqaolNksNLjStRw)后收到了很多学员的反馈，大家提出了很多显然是经过认真思考的高水平问题。有些时候我也会被这些问题所“难倒”，比如昨天我在后台看到的这个问题。

![](../../assets/bc68d3046d62ce4d.png)


我把这个问题整理为下面代码文本，方便大家copy和重现问题：

```
package main
type MyInt int
type MyMap map[string]int
func main() {
var x MyInt
var y int
x = y // 会报错: cannot use y (type int) as type MyInt in assignment
_ = x
var m1 MyMap
var m2 map[string]int
m1 = m2 // 不会报错
m2 = m1 // 不会报错
}
```


结合上面代码，我将这位学员的问题重新描述一下：**MyInt与int是不同的两个类型，MyMap与map[string]int也是不同的两个类型，为何将int型变量赋值给MyInt型变量时需要做显式转型，而将map[string]int变量赋值给MyMap型变量就不需要显式转型呢**？

我们知道：Go是强调类型安全的静态编译型语言，在Go语言中，不同类型变量是不能在一起进行混合计算的，这是因为Go希望开发人员明确知道自己在做什么，这与C语言的“信任程序员”原则完全不同，因此你需要[以显式的方式通过转型统一参与计算各个变量的类型](https://time.geekbang.org/column/article/426740)。 比如：上面问题中MyInt虽然底层类型(underlying type)是int，但MyInt与int是两个不同的类型，因此它们之间的相互赋值需要通过显式转型来进行，否则Go编译器将报错，这个没有任何疑问。

估计此时大家也都会异口同声的问：那“m1 = m2”呢？为何这一句不需要显式转型呢？MyMap的底层类型是map[string]int，但MyMap与map[string]int也是两个不同的类型啊！千万不要告诉我：int与map[string]int这两个原生类型的待遇有不同！

事实上这个问题的关键就在于**int与map[string]int的确有不同**。

在Go中，我们定义一个类型一般通过type关键字进行，比如：

```
type T1 int
type T2 T1
```


在Go中，使用上述类型声明语句定义的类型T1、T2被称为**defined type**，中文称为“具定义类型”。在type alias加入Go之前，这种类型还被称为named type（具名类型），顾名思义，**这个类型是有名字的**。这个其实也很好理解。但**问题的关键是Go语言的原生类型是否都是defined type**。

好在[Go语言规范](https://go.dev/ref/spec)中对各个内置的原生类型做了明确规定：

- 所有数值类型都是defined type；(这里面就包含int)
- 字符串类型string是defined type；
- 布尔类型bool是defined type。

就这些，没了？没了！这就**意味着map、数组、切片、结构体、channel等原生复合类型(composite type)都不是defined type**。

我们离真相越来越近了！我们再回到最初的问题中。int与MyInt都是defined type，因此它们两者之间相互赋值是需要显式转型的。map[string]int不是defined type，MyMap是defined type，那么它们直接的赋值是怎么规定的呢？

Go语言规范中[关于Assignability的规则](https://go.dev/ref/spec#Assignability)中有下面这一条规定：

```
x's type V and T have identical underlying types and at least one of V or T is not a defined type.
如果x的类型V与类型T具有相同的底层类型，并且V和T至少有一个不是defined type，那么x可以赋值给类型T的变量。
```


我们用问题中的代码来套一下这个规则。我们有一个MyMap类型的变量m1，MyMap类型与map[string]int类型具有相同的底层类型map[string]int，并且map[string]int类型不是一个defined type，那么我们可以将m1直接赋值给map[string]int类型的变量m2，反之亦可。

到这里，上面的问题算是解答完毕了。我们再来扩展一下，看一些Go其他原生但非defined type的类型赋值的例子，例子中这些赋值都不会报编译错误：

```
package main
type MyMap map[string]int
type MySlice []byte
type MyArray [10]int
type MyStruct struct {
a int
b string
}
type MyChannel chan int
func main() {
var m1 MyMap
var m2 map[string]int
m1 = m2 // 不会报错
m2 = m1 // 不会报错
var sl1 MySlice
var sl2 []byte
sl1 = sl2 // 不会报错
sl2 = sl1 // 不会报错
var arr1 MyArray
var arr2 [10]int
arr1 = arr2 // 不会报错
arr2 = arr1 // 不会报错
var s1 MyStruct
var s2 struct {
a int
b string
}
s1 = s2 // 不会报错
s2 = s1 // 不会报错
var c1 MyChannel
var c2 chan int
c1 = c2 // 不会报错
c2 = c1 // 不会报错
}
```


对于上面这种在底层类型相同且至少有一个类型不是defined type的两个类型变量间赋值的情况，是不是很眼熟。没错，它和[Go的无类型常量隐式转型](https://time.geekbang.org/column/article/442791)十分相似，虽然背后的原理是不同的：

```
type MyInt int
const a = 1234
var n MyInt = a
```


Go总体来说是推崇显式哲学的，那怎么来理解这种隐式转型呢？我觉得至少有两点：

首先这种转型更多是在编译器保证类型安全性的前提下进行的，不会出现溢出或未定义行为。

其次，这种隐式转型一定程度减少了代码输入，对开发体验的提升有帮助。

最后，感谢[《Go语言101》](https://gfw.go101.org/article/101.html)作者老貘兄在这个问题上给予我的点拨，国内在Go语言语法细节上理解最到位最深入的人非老貘兄莫属^_^。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强，欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


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


微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论