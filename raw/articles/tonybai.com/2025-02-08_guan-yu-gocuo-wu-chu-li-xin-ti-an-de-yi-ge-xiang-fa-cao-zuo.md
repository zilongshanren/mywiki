---
title: 关于Go错误处理新提案的一个想法：?操作符这样用行不行
url: https://tonybai.com/2025/02/08/personal-idea-about-using-question-mark-operator-in-go-error-handling-new-proposal/
published: '2025-02-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 关于Go错误处理新提案的一个想法：?操作符这样用行不行

![](../../assets/2aff1d212be56d57.jpeg)


[本文永久链接](https://tonybai.com/2025/02/08/personal-idea-about-using-question-mark-operator-in-go-error-handling-new-proposal) – https://tonybai.com/2025/02/08/personal-idea-about-using-question-mark-operator-in-go-error-handling-new-proposal

## 0. 背景

Ian Taylor在关闭了[旨在消除Go错误处理样板代码的issue](https://github.com/golang/go/issues/71203)之后，又另起了一个“同名”的[discussion](https://github.com/golang/go/discussions/71460)。错误处理真不愧是Go社区**呼声最高**的问题，几天之内又收到了近500条回复！不过到目前为止，依然没有形成统一和高赞的意见。

关于error handling的样板代码过多，其实**我个人是可以接受的，即便不做出任何改变也是ok的**，估计Go社区与我有相同看法的也不在少数。比如就有人引用了[Rob Pike的权威观点](https://go.dev/talks/2015/simplicity-is-complicated.slide#9)，并认为Go应该按照Rob大神的思路，保持Go语法稳定：


![](../../assets/3708361f97a47f26.png)



不过自然也会有另外一批人强烈希望错误处理的样板代码得到改进。

Ian Taylor在discussion中明确了该提案的目标是**引入一种新语法，在不影响控制流清晰度的前提下，减少正常情况下检查错误所需的代码量**。


[Ian最初的Proposal](https://mp.weixin.qq.com/s/c9Bd3M5WZ-UpCuo9lslewA)由于隐式声明变量err以及可选代码块等问题而备受“批评”，并且似乎该proposal违反了他自己提出的目标。


今天在discussion中看到一位名为[Mukunda Johnson的gopher的评论](https://github.com/golang/go/discussions/71460#discussioncomment-12084482)，我觉得**很有道理**。其核心观点就是：**尽量保持Go的传统语法形式**。他还给出了期望中的语法示例：

```
// 当前错误处理样板代码过多的示例
f, err := open(file)
if err != nil {
return err
}
defer f.Close()
if err = binwrite(f, signature); err != nil {
return err
}
if err = binwrite(f, header); err != nil {
return err
}
if err = binwrite(f, zeroSegment); err != nil {
return err
}
for _, s := range segments {
if err = binwrite(f, s); err != nil {
return err
}
}
if err = binwrite(f, footer); err != nil {
return err
}
vs.
// 使用新语法改进后的代码
f, err := open(file)?
defer f.Close()
binwrite(f, signature)?
binwrite(f, header)?
binwrite(f, zeroSegment)?
for _, s := range segments {
binwrite(f, s)?
}
binwrite(f, footer)?
```


这给了我很大启发：我们可以引入?语法，但是如果结合原先err变量的声明形式岂不是更好！比如：

```
f, err := open(file)?
```


岂不是要比下面两种形式更好！

```
f := open(file)?
或
f := open(file)? err { }
```


通过仅引入一个问号（?）操作符，并避免引入过多的新语法形式，却能解决60%的错误处理样板问题。根据[jba对Go开源代码中错误处理的抽样统计](https://github.com/golang/go/issues/71203#issuecomment-2585915103)，超过60%的错误处理都是直接返回err，而没有对err进行任何修饰。此外，显式声明err可以最大程度地避免隐式声明带来的问题，同时提升代码的可读性。

因此，基于**尽量使用已有Go代码风格、最大程度避免隐式声明，并仅解决最常见的错误处理样板代码**的原则，下面我基于Ian提案的错误处理改进语法，谈点自己关于新？操作符使用的想法，大家看看是否可行。

## 1. 对于最常见的未经修饰的错误处理代码

```
err := SomeFunction2()
if err != nil {
return err
}
或是
if err := SomeFunction2(); err != nil {
return err
}
```


我们使用下面的新语法做等价替代：

```
err := SomeFunction2() ?
```


如果声明的错误变量名为err，也可省略赋值操作符左侧代码，从而简化为：

```
SomeFunction2() ? // 这里略带隐式
```


## 2. 如果函数返回值有多个，甚至有多个错误变量的情况

比如下面代码：

```
a, b, err0, err1, err2 := SomeFunction3()
if err2 != nil {
return err2
}
```


我们可以将其改写为：

```
a, b, err0, err1, err2 := SomeFunction3()?
```


其语义是如果err2不为nil，返回err2，但前提要保证赋值语句的左侧的最后一个变量err2必须是实现error接口的类型的变量。

如果是像下面这样在err2 != nil时有多个返回值，又该如何处理呢？

```
a, b, err0, err1, err2 := SomeFunction3()
if err2 != nil {
return a, b, err2
}
```


对于这种情况，我认为可以不在新方案的考虑范围之内，现在怎么写，请继续这么写。如果非要解决，请继续看后面支持可选代码块的情况。

实现以上两种情况，就能解决60%以上的错误样板代码问题了！

## 3. 对于对返回的error值进行修饰的情况

对于像下面两种对返回的error变量进行修饰的情况：

```
r, err := SomeFunction()
if err != nil {
return fmt.Errorf("something failed: %v", err)
}
```


和

```
if err := SomeFunction2(); err != nil {
return fmt.Errorf("something else failed: %v", err)
}
```


我的第一想法是**保持现状** ，不在新方案考虑范围之内。

不过如果非要在新方案中解决，那就需要引入可选代码块(optional block)了！比如：

```
r, err := SomeFunction() ? {
return fmt.Errorf("something failed: %v", err)
}
err := SomeFunction2() ? {
return fmt.Errorf("something else failed: %v", err)
}
```


和Ian的原proposal中语法不同，这里我们依然显式声明了err，当然你也可以不用err这个名字，由于是显式声明，你用任何名字均可，比如：

```
r, e := SomeFunction() ? {
return fmt.Errorf("something failed: %v", e)
}
myErr := SomeFunction2() ? {
return fmt.Errorf("something else failed: %v", myErr)
}
```


这将避免隐式声明带来的诸多问题！

基于可选代码块，我们也可以处理一下前面提到的返回多个值的情况。下面代码

```
a, b, err0, err1, err2 := SomeFunction3()
if err2 != nil {
return a, b, err2
}
```


可以改写为：

```
a, b, err0, err1, err2 := SomeFunction3() ? {
return a, b, err2
}
```


这里加入可选代码块后，我建议开发人员负责显式调用return，而不是由?操作符来自动return，也就是说**完全将控制权交给你**。如果你没有在可选代码块中调用return，那么代码在执行完可选代码块中的代码后，还会继续向下执行。可选代码块相当于一个error handler，而不带可选代码块的情况，默认的error handler其实就是一个return err，伪代码类似这样：

```
err := SomeFunction2() ?
<=>
err := SomeFunction2() ? {
return err
}
```


这样解释后，你是不是觉得在语义层面，不带可选代码块与带有可选代码块的情况就统一和一致了呢！

本质上来说，?+可选代码块仅是**让你少敲了个if以及err != nil**。

## 4. 综合示例

Mukunda Johnson给出的示例其实已经可以很好地展示?操作符+显式声明err方案带来的消除样板代码的效果，这里再回顾一下(这里没用到可选代码块，因此代码显得格外清晰)：

```
f, err := open(file)?
defer f.Close()
binwrite(f, signature)?
binwrite(f, header)?
binwrite(f, zeroSegment)?
for _, s := range segments {
binwrite(f, s)?
}
binwrite(f, footer)?
```


此外，在原discussion中，另外一个gopher提出的示例，我们也可以用上面的想法改写一下：

```
// 最常见的情况
SomeFunc() ?
// 多个返回值，最后一个为error变量
a, err1 := SomeFunction2() ?
// 返回前对err进行修饰
err := SomeFunc() ? {
return fmt.Errorf("oh no: %w", err)
}
// 显式声明避免变量遮蔽
err := SomeFunc() ? {
otherErr := OtherFunc() ? {
err = errors.Wrap(err, otherErr) // 在可选代码块中没有显式调用return，代码还会继续向后执行
}
return fmt.Errorf("oh no: %w", err)
}
```


## 5. 小结

再来简单总结一下上面想法中的语法形式的优势：

- 与传统Go语法形式几乎一致，尽量避免引入过多新语法形式，在不使用可选代码块的时候，只是多了一个问号（?）。
- 显式声明err变量，最大程度避免隐式声明带来的问题。
- 专注解决最常见的错误处理样板情景，其他场景保持当前写法即可。
- 即便引入可选代码块，本质上与不用可选代码块的语法在语义层面也是统一和一致的。

这一语法方案保留了原Ian提案中的优势，并能消除一些缺点，如变量遮蔽和隐式声明等。不过，仍然有些原proposal中的劣势问题无法完全消除，但这些问题显然不是主要关注点。

需要注意的是，以上想法目前仅停留在形式讨论层面，技术层面是否可行尚不确定。

大家认为我的想法可行吗？希望大家能提出更具建设性的意见^_^。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2025年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。并且，2025年将在星球首发“Go陷阱与缺陷”和“Go原理课”专栏！此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格6$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

“`golang

// T?

if T ==nil { return T }

// f() ?

if x := f(); x == nil {

return x

}

// x1 := f() ?

if x1, x := f(); x == nil {

return x

}

// x1,x2 := f() ?

if x1, x2, x := f(); x == nil {

return x

}

// x1 := f() ? { return errors.New(“new error”) }

if x1, x := f(); x == nil {

return errors.New(“new error”)

}

// x1 := f() ? x { return errors.Wrap(x, “wrap error”) }

if x1, x := f(); x == nil {

return errors.Wrap(x, “wrap error”)

}

// x1 := f() ? x { log.Print(x) }

if x1, x := f(); x == nil {

log.Print(x)

}

“`

感觉还是结合着 err 会好一点

“`go

func foo() (int, error) {

return 1, errors.New(“error”)

}

var x int

x = foo() ? {

// nothing

}

fmt.Println(x)

“`

赋值的顺序是怎样，这里是输出 1 还是 0

还有就是有关指针

“`go

var x *int

*x = foo() ? // returns the error

// not reached

“`