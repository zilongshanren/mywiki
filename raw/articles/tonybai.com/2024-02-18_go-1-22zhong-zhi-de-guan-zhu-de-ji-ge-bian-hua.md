---
title: Go 1.22中值得关注的几个变化
url: https://tonybai.com/2024/02/18/some-changes-in-go-1-22/
published: '2024-02-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.22中值得关注的几个变化

![](../../assets/53e5c095c3592998.png)


[本文永久链接](https://tonybai.com/2024/02/18/some-changes-in-go-1-22) – https://tonybai.com/2024/02/18/some-changes-in-go-1-22

美国时间2024年2月6日，正当中国人民洋溢在即将迎来龙年春节的喜庆祥和的气氛中时，[Eli Bendersky](https://github.com/eliben)代表Go团队在Go官博发文“[Go 1.22 is released!](https://go.dev/blog/go1.22)”，正式向世界宣告了Go 1.22版本的发布！

![](../../assets/f8255f7eb3c13eee.png)


注：大家可以从Go官网下载Go 1.22的第一个版本go 1.22.0，也可以在

[Go playground]上选择Go 1.22版本在线体验Go 1.22的语法。

记忆中，这似乎是Eli Bendersky首次代表Go团队撰写Go版本发布的文章，文章短小且言简意赅，会让大家误以为Go 1.22版本没有太多的功能点变更，其实不然。读过我之前写的“[Go 1.22新特性前瞻](https://tonybai.com/2023/12/25/go-1-22-foresight/)”一文的童鞋都知道Go 1.22中有很多重要且影响深远的值得我们关注的变化。在这篇文章中，我们就再来介绍一下这些变化，供大家参考。

## 0. 插播“旧闻”：Go再次进入Top10，并刷新有史以来的最高排名

TIOBE编程语言排行榜发布2024年2月编程语言排名的时间恰逢中国人民的传统佳节春节期间，因此它的这次排名发布“淹没”在了“龙年大吉”的喜庆气氛当中了。年后开工，大家翻看这条“旧闻”时，才发现在这次排名中，Go再一次回到Top10，位列第8名，刷新了Go打榜一来的历史最好位次。

![](../../assets/57c533f7fe34a3a1.png)


单看这一次进入top10似乎没有什么，因为2023年4月份，Go也跻身过top10，排名第10。但如果从Go打榜以来的历史曲线来看，如下图：

![](../../assets/33fee560cf672dfc.png)


我们看到了“翘尾”，我们看到了Go迈过“低谷”后的爬升！这与我在[《Go语言第一课专栏》](http://gk.link/a/10AVZ)的结课语[《和你一起迎接Go的黄金十年》](https://time.geekbang.org/column/article/486536)中预判：**Go即将迎来自己的黄金十年** 愈来愈吻合了！

不过，我在《[2023年Go语言盘点：稳中求新，稳中求变](https://tonybai.com/2023/12/31/the-2023-review-of-go-programming-language/)》一文中提到过TIOBE index作为世界最知名的编程语言排行榜，却存在其“不靠谱”的特性，比如这一期排名中，上古时代的编程语言Fortran从去年同期的第24位上升至第11位，仅比PHP落后一位，另一门古老的COBOL语言也从去年同期的第30位上升至第19位，仅仅比大热的Rust语言落后一位。

因此，对于TIOBE的排名，大家既要了解，也无需过于看重^_^。

言归正传，我们来说说Go 1.22版本的变化。

## 1. 语言变化

Go 1.22对语言语法做了两处变更，一个是[Go 1.21版本](https://tonybai.com/2023/08/20/some-changes-in-go-1-21/)中的试验特性loopvar在Go 1.22中转正落地；另一个也和for循环有关，那就是for range新增了对整型表达式的支持。两者相比较，还是第一个变化loopvar带来的影响更大一些。为什么呢？因此这是**Go语言发展历史上第一次真正的填语义层面的“坑”**，而且修改的是一个在Go源码中最常用的控制结构的执行语义，这很大可能会带来break change。[Go101教程](https://go101.org/)的作者[老貘](https://github.com/go101)将之成为[Go历史上最大的向后兼容性破坏版本](https://twitter.com/go100and1/status/1755598141351677983)。

注：

[Go 1.21版本]有一个对panic(nil)的语义修正，但我估计很少会有人写出panic(nil)这样的代码。

这次语义修改用一句话表达就是：**将经典三段式for循环语句以及for range语句中的用短声明形式定义的循环变量从整个循环定义和共享一个，变为每个迭代定义一个**。

这里借用Go官博文章中那个例子再说明一下这个语义变化：

```
// go1.22-examples/lang/loopvar/main.go
package main
import (
"fmt"
"time"
)
func main() {
done := make(chan bool)
values := []string{"a", "b", "c"}
for _, v := range values {
go func() {
time.Sleep(time.Second)
fmt.Println(v)
done <- true
}()
}
// wait for all goroutines to complete before exiting
for _ = range values {
<-done
}
}
```


我们用Go 1.22.0版本之前的版本，比如Go 1.21.0，来运行该示例：

```
$go run main.go
c
c
c
```


我们看到：由于v是整个循环中各个迭代共享的一个变量，所以在每个迭代新创建的goroutine中输出的v都是循环结束后v的最终值c。

如果我们用go 1.22.0来运行上述示例，我们将得到：

```
// 输出的值的顺序与goroutine调度有关
$go run main.go
b
c
a
```


注：关于Go 1.22版本之前的for range的坑，我的极客时间专栏

[《Go语言第一课》]专栏有图文并茂的原理讲解，欢迎订阅阅读。

那么，loopvar这一语义填“坑”究竟会对你的代码造成怎样的影响呢？在Russ Cox[关于loopvar语义变更的设计文档](https://go.googlesource.com/proposal/+/master/design/60078-loopvar.md)中提到了：只有go.mod中的go version在go 1.22.0及以后的时候才会生效，这是一个渐进式过渡的过程，因此目前无论是开源项目还是商业项目，只要go.mod中的go version还没有更新为大于等于go 1.22.0，那么for循环依然会保留短声明定义的变量的原语义，这样这些项目都不会受到影响。

不过，如果是直接在脚本中通过go run xxx.go形式运行某个go源码的，且当前工作目录以及父目录下没有go.mod文件的，go 1.22.0会采用新的loopvar语义，这点大家要注意了。

此外，当你将go.mod中的go version升级到go 1.22.0或更高版本时，也要注意语义变更可能带来的问题。在升级go version之前，可以用Go 1.22版本之前的go vet对项目源码进行一次静态分析，对于go vet提示：“loop variable v captured by func literal”的地方务必注意逐个确认。

注：Go 1.22版本中的go vet已经移除了在go version >= 1.22.0时，对“loop variable v captured by func literal”情况进行警告的功能。


关于Go 1.22中for range支持后面接整型表达式的“语法糖”新特性以及[函数迭代器的实验特性](https://go.dev/wiki/RangefuncExperiment)，这里就不细说了，大家可以看看“[Go 1.22新特性前瞻](https://tonybai.com/2023/12/25/go-1-22-foresight/)”一文中的说明。

## 2. 编译器、运行时与工具链

在编译器、运行时和工具链这些方面，Go 1.22的正式版本与“[Go 1.22新特性前瞻](https://tonybai.com/2023/12/25/go-1-22-foresight/)”一文中使用的Go 1.22rc1版本几乎没有差异，这里挑主要内容介绍一下，其他一些内容可以参考[前瞻](https://tonybai.com/2023/12/25/go-1-22-foresight)一文。

Go 1.22版本继续在编译上优化PGO(profile-guided optimization)， 基于PGO的构建可以比以前版本实现更高比例的调用去虚拟化(devirtualize)。在Go 1.22中，官⽅给出的PGO带来的性能提升数字是2%~14%，这应该是基于Google内部一些典型的Go程序测算出来的。

注：如果你对PGO优化还不是很了解，可以看看“

[深入理解Profile Guided Optimization(PGO)]”这篇文章。

Go 1.22版本编译器现在可以更多运⽤devirtualize和inline。在Go编译器中，devirtualize是一种编译优化技术，旨在消除“虚函数”调用的开销。“虚函数”是指在面向对象编程中，通过基类指针或引用调用的函数。在Go中所谓虚函数调用指的就是通过接口类型变量进行的方法调用。由于是动态调用，基于接口的方法调用需要在运行时进行查找和分派，这可能导致一定的性能损失。

而Go编译器在进行devirtualize优化时，会尝试根据程序的上下文信息和类型信息，确定方法调用的具体对象实例。如果编译器能够确定调用的具体实例，则会将通过接口的方法调用替换为直接调用具体对象实例的方法，从而消除运行时的开销，使得通过接口类型变量进行方法调用的性能得到优化提升。

Go 1.22版本中的运行时可以使基于类型的垃圾收集的元数据更接近每个堆对象，从而将Go程序的CPU性能（延迟或吞吐量）提高了1-3%。这一变化还支持通过重复数据删除冗余元数据，进而将大多数Go程序的内存开销减少了大约1%。

在工具链方面，有三个主要改变这里提一下：

- go work支持vendor

在Go 1.22版本中，通过go work vendor可以将workspace中的依赖放到vendor⽬录下，同时在构建时，如果workspace下有vendor⽬录，那么默认的构建是go build -mod=vendor，即基于vendor的构建。

- go mod init不再care其他vendor工具的配置文件

go mod init不再尝试将其他vendor工具（例如Gopkg.lock ）的配置文件导入到go module依赖文件(go.mod)中了，也就是说从Go 1.22版本开始，go module出现之前的那些gopath时代的依赖管理工具正式退出并成为历史了。

- 改进go test -cover的输出

对于没有自己的测试文件的包，go test -cover在go 1.22版本之前会输出：

```
? mymod/mypack [no test files]
```


但在Go 1.22版本之后，会报告覆盖率为0.0%：

```
mymod/mypack coverage: 0.0% of statements
```


## 3. 标准库

这里列举一下标准库值得关注的重大变化，大家可以与[前瞻](https://tonybai.com/2023/12/25/go-1-22-foresight)一文相互参考着阅读。

### 3.1 math/rand/v2：标准库的第一个v2版本包

Go 1.22中新增了math/rand/v2包，这里之所以将它列为Go 1.22版本标准库的⼀次重要变化，是因为这是标准库第一次为某个包建⽴v2版本，按照Russ Cox的说法，这次math/rand/v2包的创建，算是为标准库中的其他可能的v2包“探探路”，找找落地路径。关于math/rand/v2包相对于原math/rand包的变化有很多，具体可以参考[issue 61716](https://go.dev/issue/61716)中的设计与讨论。

### 3.2 增强http.ServeMux表达能力

在Go 1.22版本中，http.ServeMux的表达能力得到了大幅提升，从原先只支持静态路由，到新版本中支持如下一些特性：

- “/index.html”路由将匹配任何主机和方法的路径”/index.html”；
- “GET /static/”将匹配路径以”/static/”开头的GET请求；
- “example.com/”可以与任何指向主机为”example.com”的请求匹配；
- “example.com/{$}”会匹配主机为”example.com”、路径为”/”的请求，即”example.com/”；
- “/b/{bucket}/o/{objectname…}”匹配第一段为”b”、第三段为”o”的路径。名称”bucket”表示第二段，”objectname”表示路径的其余部分。

并且新版ServeMux在路由匹配性能方面也不输众多开源http路由框架太多，后续建立Go web或api类新项目时，可以考虑首选新版ServeMux来进行路由匹配了，减少对外部的一个依赖。

关于新版http.ServeMux的具体使用方法，其作者Jonathan Amsterdam（也是[log/slog](https://tonybai.com/2022/10/30/first-exploration-of-slog)的作者）在官博发表了一篇名为“[Routing Enhancements for Go 1.22](https://go.dev/blog/routing-enhancements)”的文章，大家可以详细参考。

关于标准库的其他一些变化，大家可以参考[前瞻](https://tonybai.com/2023/12/25/go-1-22-foresight)一文以及更详细的[Go 1.22的发布说明文档](https://go.dev/doc/go1.22)。

## 4. 小结

综上，Go 1.22版本对语言、编译器、工具链、运行时和标准库都有一定程度的改进和创新，遗留代码通过Go 1.22版本的重新编译便可以得到一定程度的性能上的自然提升，这也体现了[Go语言在稳中求新、稳中求变](https://tonybai.com/2023/12/31/the-2023-review-of-go-programming-language)的特点。

不过这里还要提醒各位Go开发者，在升级Go 1.22版本时务必注意潜在的向后兼容性问题，尤其是loopvar语义带来的变化影响。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go1.22-examples)下载。

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

## 评论