---
title: Go语言中常见的几种反模式[译]
url: https://tonybai.com/2021/03/31/common-anti-patterns-in-go/
published: '2021-03-31'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言中常见的几种反模式[译]

![](../../assets/50a12ce452eeffc9.png)


本文翻译自Saif Sadiq的文章[《Common anti-patterns in Go》](https://deepsourcehq.hashnode.dev/common-anti-patterns-in-go)。

众所周知，编码是一门艺术，就像每个拥有精湛艺术并为之感到骄傲的工匠一样，我们作为开发人员也为我们编写的代码感到自豪。为了获得最佳效果，艺术家不断寻找可提高其手艺的方法和工具。同样，作为开发人员，我们也在不断提高自己的技能，并对”如何写出好的代码”这个最重要的问题的答案保持好奇。

弗雷德里克·布鲁克斯（Frederick P. Brooks）在他的书[《人月神话》](https://book.douban.com/subject/26358448/)中写道：

“程序员和诗人一样，工作时只是稍稍脱离了纯粹的思维定式。他在空气中建造他的城堡，通过发挥想象力进行创作。很少有一种创作媒介是如此灵活，如此容易打磨和重做，如此容易实现宏大的概念结构”。


![](../../assets/84cb2122e4312b81.jpeg)



这篇文章试图探索上面漫画中大问号的答案。编写良好代码的最简单方法是避免在我们编写的代码中包含反模式。

### 0. 什么是反模式

一个简单的反模式示例就是编写一个API，而无需考虑该API的使用者如何使用它，如下面的示例1所述。意识到反模式并有意识地避免在编程时使用它们，这无疑是朝着更具可读性和可维护性的代码库迈出的重要一步。在本文中，让我们看一下Go中一些常见的反模式。

**当编写代码时没有未来的因素做出考虑时，就会出现反模式**。反模式最初可能看起来是一个适当的问题解决方案，但是，实际上，随着代码库的扩大，这些反模式会变得模糊不清，并给我们的代码库添加“技术债务”。

反模式的一个简单例子是，在编写API时不考虑API的消费者如何使用它，就如下面例1那样。意识到反模式，并在编程时有意识地避免使用它们，肯定是迈向更可读和可维护的代码库的重要一步。在这篇文章中，我们来看看Go中常见的几种反模式。

### 1. 从导出函数(exported function)返回未导出类型(unexported type)的值

在Go中，要导出(export)任何一个字段(field)或变量(variable)，我们都需要确保其名称是以大写字母开头。导出(export)它们的动机是使它们对其他包可见。例如，如果要使用math包中的Pi函数，我们将其定义为math.Pi。而使用math.pi将无法正常工作，并且会报错。

以小写字母开头的名称（结构字段，函数或变量）不会被导出，并且仅在定义它们的包内可见。

使用返回未导出类型值的导出函数或方法可能会令人沮丧，因为其他包中的该函数的调用者将不得不再次定义一个类型才能使用它。

```
// 反模式
type unexportedType string
func ExportedFunc() unexportedType {
return unexportedType("some string")
}
// 推荐
type ExportedType string
func ExportedFunc() ExportedType {
return ExportedType("some string")
}
```


### 2. 空白标识符的不必要使用

在各种情况下，将值赋值给空白标识符是不需要，也没有必要的。如果在for循环中使用空白标识符，Go规范中提到：

如果最后一个迭代变量是空白标识符，则range子句等效于没有该标识符的同一子句。


```
// 反模式
for _ = range sequence {
run()
}
x, _ := someMap[key]
_ = <-ch
// 推荐
for range something {
run()
}
x := someMap[key]
<-ch
```


### 3. 使用循环/多次append连接两个切片

将多个切片附加到一个切片时，无需遍历切片并一个接一个地附加(append)每个元素。相反，使用一个append语句执行此操作会更好，更有效率。

例如，下面的代码段通过迭代遍历元素逐个附加元素来连串连接sliceOne和sliceTwo：

```
for _, v := range sliceTwo {
sliceOne = append(sliceOne, v)
}
```


但是，由于我们知道append是一个[变长参数函数](https://www.imooc.com/read/87/article/2424)，我们可以使用零个或多个参数来调用它。因此，可以仅使用一个append函数调用来以更简单的方式重写上面的示例，如下所示：

```
sliceOne = append(sliceOne, sliceTwo…)
```


### 4. make调用中的冗余参数

该make函数是一个特殊的内置函数，用于分配和初始化map、slice或chan类型的对象。为了使用make初始化切片，我们必须提供切片的类型、切片的长度以及切片的容量作为参数。在使用make初始化map的情况下，我们需要传递map的大小作为参数。

但是，make的这些参数已经具有默认值：

- 对于channel，缓冲区容量默认为零（不带缓冲）。
- 对于map，分配的大小默认为较小的起始大小。
- 对于切片，如果省略容量，则容量参数的值默认为与长度相等。

所以，

```
ch = make(chan int, 0)
sl = make([]int, 1, 1)
```


可以改写为：

```
ch = make(chan int)
sl = make([]int, 1)
```


但是，出于调试或方便数学计算或平台特定代码的目的，将具名常量与channel一起使用不被视为反模式。

```
const c = 0
ch = make(chan int, c) // 不是反模式
```


### 5. 函数中无用的return

return在没有返回值的函数中作为最终语句不是一种好习惯。

```
// 没用的return，不推荐
func alwaysPrintFoofoo() {
fmt.Println("foofoo")
return
}
// 推荐
func alwaysPrintFoo() {
fmt.Println("foofoo")
}
```


但是，具名返回值的return不应与无用的return相混淆。下面的return语句实际上返回了一个值。

```
func printAndReturnFoofoo() (foofoo string) {
foofoo := "foofoo"
fmt.Println(foofoo)
return
}
```


### 6. switch语句中无用的break语句

在Go中，switch语句不会自动fallthrough。在像C这样的编程语言中，如果前一个case语句块中缺少break语句，则执行将进入下一个case语句中。但是，人们发现，fallthrough的逻辑在switch-case中很少使用，并且经常会导致错误。因此，包括Go在内的许多现代编程语言都将switch-case的默认逻辑改为不fallthrough。

因此，在一个case case语句中，不需要将break语句作为最终语句。以下两个示例的行为相同。

反模式：

```
switch s {
case 1:
fmt.Println("case one")
break
case 2:
fmt.Println("case two")
}
```


好的模式：

```
switch s {
case 1:
fmt.Println("case one")
case 2:
fmt.Println("case two")
}
```


但是，为了在Go中switch-case中实现fallthrough机制，我们可以使用fallthrough语句。例如，下面给出的代码段将打印23。

```
switch 2 {
case 1:
fmt.Print("1")
fallthrough
case 2:
fmt.Print("2")
fallthrough
case 3: fmt.Print("3")
}
```


### 7. 不使用辅助函数执行常见任务

对于一组特定的参数，某些函数具有一些特定表达方式，可以用来简化效率，并带来更好的理解/可读性。

例如，在Go中，要等待多个goroutine完成，可以使用sync.WaitGroup。通过将计数器的值-1直至0，以表示所有goroutine都已经执行完毕：

```
wg.Add(1) // ...some code
wg.Add(-1)
```


但使用sync包提供的辅助函数wg.Done()可以使代码更简单并容易理解。因为它本身会通知sync.WaitGroup所有goroutine即将完成，而无需我们手动将计数器减到0。

```
wg.Add(1)
// ...some code
wg.Done()
```


### 8. nil切片上的冗余检查

nil切片的长度为零。因此，在计算切片的长度之前，无需检查切片是否为nil切片。

例如，下面的nil检查是不必要的。

```
if x != nil && len(x) != 0 { // do something
}
```


上面的代码可以省略nil检查，如下所示：

```
if len(x) != 0 { // do something
}
```


### 9. 太复杂的函数字面量

可以删除仅调用单个函数且对函数内部的值没有做任何修改的函数字面量，因为它们是多余的。可以改为在外部函数直接调用被调用的内部函数。

例如：

```
fn := func(x int, y int) int { return add(x, y) }
```


可以简化为：

```
add(x, y)
```


译注：原文少了简化后的代码，这里根据译者的理解补充的。


### 10. 使用仅有一个case语句的select语句

select语句使goroutine等待多个通信操作。但是，如果只有一个case语句，实际上我们不需要使用select语句。在这种情况下，使用简单send或receive操作即可。如果我们打算在不阻塞地发送或接收操作的情况处理channel通信，则建议在select中添加一个default case以使该select语句变为非阻塞状态。

```
// 反模式
select {
case x := <-ch: fmt.Println(x)
}
// 推荐
x := <-ch
fmt.Println(x)
```


使用default:

```
select {
case x := <-ch:
fmt.Println(x)
default:
fmt.Println("default")
}
```


### 11. context.Context应该是函数的第一个参数

context.Context应该是第一个参数，一般命名为ctx.ctx应该是Go代码中很多函数的（非常）常用参数，由于在逻辑上把常用参数放在参数列表的第一个或最后一个比较好。为什么这么说呢？因为它的使用模式统一，可以帮助我们记住包含该参数。在Go中，由于变量可能只是参数列表中的最后一个，因此建议将context.Context作为第一个参数。各种项目，甚至Node.js等都有一些约定，比如错误先回调。因此，context.Context应该永远是函数的第一个参数，这是一个惯例。

```
// 反模式
func badPatternFunc(k favContextKey, ctx context.Context) {
// do something
}
// 推荐
func goodPatternFunc(ctx context.Context, k favContextKey) {
// do something
}
```


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