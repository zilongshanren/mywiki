---
title: Go泛型语法又出“幺蛾子”：引入type set概念和移除type list中的type关键字
url: https://tonybai.com/2021/04/07/go-generics-use-type-sets-to-remove-type-keyword/
published: '2021-04-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go泛型语法又出“幺蛾子”：引入type set概念和移除type list中的type关键字

[本文永久链接](https://tonybai.com/2021/04/07/go-generics-use-type-sets-to-remove-type-keyword) – https://tonybai.com/2021/04/07/go-generics-use-type-sets-to-remove-type-keyword

![](../../assets/c64e2fc4fe12f75d.png)


近日，Go泛型语法负责人之一的[Ian Lance Taylor发布了一个issue](https://github.com/golang/go/issues/45346)，说明go团队想引入新的type set概念，并去除[原Go泛型方案](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)中置于interface定义中的type list中的type关键字。

对于Go泛型来龙去脉不是很了解的童鞋，可以先去看看我看看我之前的文章：[《能力越大，责任越大” – Go语言之父详解将于Go 1.18发布的Go泛型》](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)。在那篇文章的结尾，Go设计团队对自己的Go泛型设计方案中的几个方面给出了自己的满意度评价，其中唯一让团队感觉还不是很完美的就是“Type lists in interfaces”：

![](../../assets/81599afbc44859a8.png)


### 1. 何为Type lists in interfaces

我们先来说说何为Type lists in interfaces！当前Go泛型方案使用interface类型用于表达对类型参数(type parameters)的约束(constraints)，比如：

```
type MyC1 interface {
M1()
}
func F1[T MyC1](t T) {
}
```


在上述代码中，我们使用interface MyC1作为类型参数(type parameters)的约束，对于F1函数而言，所有满足MyC1接口的类型都可以作为其类型参数的实参传入：

```
type MyT1 string
func(t1 *MyT1) M1() {}
var t1 = new(MyT1)
F1(t1)
```


*MyT1实现了MyC1接口，于是我们可以将其实例(t1)传给F1。Go泛型的自动类型推导会将T的实参置为*MyT1。

完整程序如下：

```
// https://go2goplay.golang.org/p/WPCvmwkxcEL
package main
import (
"fmt"
)
type MyC1 interface {
M1()
}
func F1[T MyC1](t T) {
fmt.Printf("%T\n", t)
}
type MyT1 string
func (t1 *MyT1) M1() {
}
func main() {
var t1 = new(MyT1)
F1(t1) // *main.MyT1
}
```


对于自定义类型，通过实现接口的方法集合即可满足接口，对于类型参数可以是原生类型的情况，我们无法通过这种方式实现，于是Go团队将type list加入到interface接口中，**仅用作泛型类型参数的约束检查**：

```
type MyC2 interface {
type int, int32, int64
}
func F2[T MyC2](t T) {
fmt.Printf("%T\n", t)
}
func main() {
var t2 string
F2(t2) // string
}
```


而MyMC2中的：

```
type int, int32, int64
```


就是所谓的”type list”。

如果一个interface定义中既有method也有type list，那么要满足这个interface类型，则作为类型参数实参的类型既必须在type list中（或其underlying type在type list中），又必须实现接口类型的所有方法：

```
// https://go2goplay.golang.org/p/rE8mGH0lHWm
package main
import (
"fmt"
)
type MyC3 interface {
M3()
type int, string, float64
}
func F3[T MyC3](t T) {
fmt.Printf("%T\n", t)
}
type MyT3 string
func (t3 MyT3) M3() {
}
func main() {
t3 := MyT3("hello")
F3(t3) // main.MyT3
}
```


细心的童鞋会发现：拥有type list的interface仅能用于做为类型参数的约束，而不能像普通interface类型那样使用：

```
// https://go2goplay.golang.org/p/mJoEYrceBSL
package main
type MyC3 interface {
M3()
type int, string, float64
}
func main() {
var i3 MyC3 // type checking failed for main
// prog.go2:9:9: interface contains type constraints (int, string, float64)
_ = i3
}
```


这种gap(缝隙)始终让Go核心团队的开发人员感到“不爽”，那么能否将两者融合在一起呢？即放开对包含type list的interface类型仅能做constraint的限制，让其和普通interface一样使用。这次引入的type set应该是解决这个问题的一个前提。但在这个新proposal中，核心团队还没有将这个问题作为重点，只能算作是为以后留个作业吧。

### 2. 引入type set概念

[Ian Lance Taylor发布的这个issue](https://github.com/golang/go/issues/45346)主要就是想**引入type set概念，并用新语法等价替代 原泛型proposal中的type list，新语法去除了原type list中的type关键字**。

于是go团队试图这样来做：

```
// 当前的type list
type SignedInteger interface {
type int, int8, int16, int32, int64
}
// type set理念下的新语法
type SignedInteger interface {
~int | ~int8 | ~int16 | ~int32 | ~int64
}
```


我们看到新语法中去掉了原先type list中的type关键字，类型间的间隔也由逗号改为了管道符|。按该proposal的原意，管道符(在布尔代数中也表示或)更接近于type list的原意，即可以是int，或int8或….。如果仅仅是变成了如下改进的语法：

```
type SignedInteger interface {
int | int8 | int16 | int32 | int64
}
```


估计大家也没多大意见。但是偏偏引入了“~”这个前缀。~int与int有什么区别呢？要搞清楚区别就要先来看看Ian新引入的type set概念了。

什么是type set(类型集合)？Ian给出了此概念的定义：

- 每个类型都有一个type set。
- 非接口类型的类型的type set中仅包含其自身。比如非接口类型T，它的type set中唯一的元素就是它自身：{T}；
- 对于一个普通的、没有type list的普通接口类型来说，它的type set是一个无限集合。所有实现了该接口类型所有方法的类型都是该集合的一个元素，另外由于该接口类型本身也声明了其所有方法，因此接口类型自身也是其Type set的一员。
- 空接口类型interface{}的type set中则是囊括了所有可能的类型；
- 这样一来我们来试试用type set概念重新陈述一下一个类型T实现一个接口类型I：即当类型T是接口类型I的type set的一员时，T便实现了接口I;
- 对于使用嵌入接口类型组合而成的接口类型，其type set就是其所有的嵌入的接口类型的type set的交集。proposal中的举例：type O2 interface{ E1; E2 } ，则02这个接口类型的type set是E1和E2两个接口类型的type set的交集。
- 一个拥有一个method的接口类型，比如：

```
type MyInterface1 interface {
MyMethod()
}
```


可以看成嵌入一个仅包含MyMethod的接口类型的接口类型：

```
type MyInterface interface {
MyMethod()
}
type MyInterface1 interface {
MyInterface
}
```


- 因此，一个带有自身Method的嵌入其他接口类型的接口类型，比如：

```
type 03 interface {
E1
E2
MyMethod03()
}
```


它的type set可以看成E1、E2和E3(type E3 interface { MyMethod03})的type set的交集。

### 3. 替换type list的新语法方案

我们再回到前面提到的新语法方案：

```
// type set 新语法
type SignedInteger interface {
~int | ~int8 | ~int16 | ~int32 | ~int64
}
```


Go开发团队给那些用于作为约束或被嵌入到作为约束的接口类型中的接口类型的定义做了重新描述，称这类接口类型的定义中可以嵌入一些额外的结构，被称为**interface elements**，其组成如下图：

![](../../assets/21b4c3bfd0449c97.png)


- 图中MyInterface是一个仅用于约束或嵌入到作为约束的接口类型中的类型；
- MyInterface除了拥有自己的方法列表(M1、M2)外，还可以嵌入额外的结构：interface elements，就是T1|T2|~T3|T4…|Tn那一行，这一行即替代了原先方案中的type list;
- interface elements这一行有三个值得关注的事情：
- T1、T2、T4、Tn这些仅代表type set仅为自身的类型；
- ~T3的type set 为所有underlying type为T3的类型，~T3被称为approximation elements;
- 管道符将这些类型连接在一起，共同构成一个union element，该union element的type set为所有这些类型的type set的并集。


好了现在一切都建立在type set这个概念上。那么当上述接口类型作为类型参数的约束时，要想满足该约束，可以作为类型参数的实参，那么传入的类型应该在作为约束的接口类型的type set中。

有了前面关于type set以及接口嵌入的type set的铺垫，作为约束的接口类型的理解就容易多了。无论是单纯的接口类型还是使用嵌入其他接口组合而成的接口类型，亦或是既包括嵌入也拥有自己的method list的接口类型。

### 4. 问题

Ian的issue一发出就得到了社区的重点关注，并引来的激烈的讨论，但从头看到尾，似乎大家都有些“跑题”，关于这个proposal的真正疑问在于approximation elements身上：

- 是否有必要单独拿出approximation elements这个概念

我们回顾一下当前泛型语法作为约束的接口定义所使用的type list语法，看看当前的type list语法中各个类型是否是仅代表自身？

```
// https://go2goplay.golang.org/p/5VbaSCQ8-Dq
package main
import (
"fmt"
)
type S1 struct {
Name string
Age int
}
type S2 S1
type MyC4 interface {
type struct {
Name string
Age int
}, int
}
func F4[T MyC4](t T) {
fmt.Printf("%T\n", t)
}
type MyInt int
func main() {
var t1 = S1{"tony", 17}
F4(t1) // main.S1
var t2 = S2{"tony", 17}
F4(t2) // main.S2
var n MyInt = 3
F4(n) // main.MyInt
}
```


我们看到作为约束的接口类型MyC4的type list中有两个类型：一个匿名struct和int。之后我们分别使用S1、S2和MyInt作为类型参数的实参，居然都通过了！也就是说当前的type list中的类型按照type set的概念解释，都属于approximation element，只要是underlying type在type list中，那么就可以作为类型参数的实参，通过约束检查。

那就是说：

我们是否可以只将：

```
type I1 interface {
type int, string, float64
... ...
}
```


换成：

```
type I1 interface {
int | string | float64
... ...
}
```


而无需~这个符号呢？

- 如果~符号是必要的，可否不用~符号？

Go语言中没有使用~运算符，但这个符号在其他主流语言，比如C中是位运算符，而且代表的“非”这个运算符。因此将其用在类型T前面，打眼一看，以为其含义是“不是类型T的类型”。而新proposal则将其用于表示approximation element。这让很多gopher提出异议，希望换一个符号，比如T+等。但目前尚无定论。

### 5. 小结

能力有限，以上一些对该proposal的理解可能有误，欢迎交流指正。

type set并没有改变什么，只是完成了对interface与实现interface的重新解释。 但是对于后续将interface element用于普通interface类型定义可能有重大的意义。当前的带有interface element的interface类型仅能用于作为泛型类型参数的约束，这与普通interface之间的gap早晚要“填上”，不过这已经不是这个proposal要解决的事情。

从泛型提出到如今，我已经感到泛型的引入极大增加了复杂性 ，即便没有滥用泛型，没有耍奇技淫巧，泛型的引入也让go复杂性陡增。就像这个proposal，认真阅读并理解还是需要花费不少时间和精力的。

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

## 评论