---
title: 使用具名返回值巧妙解决泛型函数返回零值的问题
url: https://tonybai.com/2022/05/20/solving-problems-in-generic-function-implementation-using-named-return-values/
published: '2022-05-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用具名返回值巧妙解决泛型函数返回零值的问题

![](../../assets/3245a33b438468b3.png)


[本文永久链接](https://tonybai.com/2022/05/20/solving-problems-in-generic-function-implementation-using-named-return-values) – https://tonybai.com/2022/05/20/solving-problems-in-generic-function-implementation-using-named-return-values

Go语言泛型语法特性在[Go 1.18版本](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)落地后，不出所料，在github上看到大量的基础容器类型数据结构被用泛型重写。这种重写我觉得是很正常、很自然的，并且实现良好的通用数据结构改为泛型其实也不难，有些简单的结构可能分分钟就能搞定。

Go 1.18发布后，我一直没机会写泛型，今天在做[DSL](https://tonybai.com/2022/05/10/introduction-of-implement-dsl-using-antlr-and-go)语义模型提取时，多处用到Stack结构，于是想到使用泛型简单实现了一个通用的Stack结构。

在Go中，我们可以用一个切片来定义Stack。泛型Stack类型的定义如下：

```
type Stack[T any] []T
```


这里的Stack类型就是一个带有类型参数(type parameter)的泛型类型，它的类型参数的约束(constraints)为[any](https://tonybai.com/2021/12/18/replace-empty-interface-with-any-first-after-switching-to-go-1-18)，即允许任何类型作为Stack的元素类型。

Stack是最基础的数据结构，一般来说它具有的操作方法包括：

- Push：压栈；
- Pop：弹栈；
- Top：获取栈顶元素；
- Len：获取栈内元素个数。

对于以切片为底层存储的Stack而言，压栈Push操作就相当于对切片的追加(append)操作：

```
func (s *Stack[T]) Push(v T) {
(*s) = append((*s), v)
}
```


不过，这里有两点要注意：

- 泛型类型的方法原型中，receiver部分的类型要带上类型参数，比如这里的*Stack[T]；
- 这里务必要用*Stack[T]，而不要像下面代码这样用Stack[T]，否则append方法改变的仅仅是Stack[T]的拷贝，而不是原Stack[T]类型的实例。

```
func (s Stack[T]) Push(v T) {
s = append(s, v)
}
```


我们再来看看*Stack[T]的弹栈Pop方法：

```
func (s *Stack[T]) Pop() T {
if len(*s) == 0 {
return nil
}
// Get the last element from the stack.
t := (*s)[len(*s)-1]
// Remove the last element from the stack.
*s = (*s)[:len(*s)-1]
return t
}
```


这样实现的Pop方法会提示return nil一行有错误：**cannot use nil as T value in return statement**。Go编译器错误信息提示我们：**nil不能作为T类型的值返回**。

Stack的类型参数的约束为any，即Stack的元素可以是任意类型，即可以是切片、map等复合类型，亦可以是int、string等值类型。如果将nil作为所有这些类型的零值的确不恰当。

那么当Stack为空时，应该如何返回呢？多亏[Go原生支持类型零值](https://www.imooc.com/read/87/article/2381)，我们可以声明一个类型零值并将其作为返回值返回：

```
func (s *Stack[T]) Pop() T {
if len(*s) == 0 {
var zero T
return zero // 模拟类型零值
}
// Get the last element from the stack.
t := (*s)[len(*s)-1]
// Remove the last element from the stack.
*s = (*s)[:len(*s)-1]
return t
}
```


虽然这种方法有效，但你是不是和我有一样的感觉：**不够优雅**。下面我们就来看一个更为优雅的小技巧：**利用函数的具名返回值**，看代码：

```
func (s *Stack[T]) Pop() (t T) {
if len(*s) == 0 {
return
}
// Get the last element from the stack.
t = (*s)[len(*s)-1]
// Remove the last element from the stack.
*s = (*s)[:len(*s)-1]
return
}
```


我们看到：具名返回值(named return value)一出马，一切都变得自然而然了。当然这也要归功于Go的类型零值特性。

具名返回值日常使用的不多，从使用的频度来看，Go标准库以及多数项目的代码默认选择非具名返回值(unamed return value)。当函数使用defer且在deferred函数中修改外部函数返回值时，应用具名返回值可以让代码显得更清晰一些：

```
func Foo() (a int) {
defer func() {
a = 5
}
a = 6
}
```


其他情况，看项目编码规范一致性要求以及个人喜好了。不过，Go引入泛型后，针对上述的泛型函数返回零值的情况，相信**具名返回值**将得到更多的“出镜”的机会。

本文中涉及的示例代码在[这里](https://github.com/bigwhite/experiments/tree/master/generics/stack)可以下载到：https://github.com/bigwhite/experiments/tree/master/generics/stack。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


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


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论