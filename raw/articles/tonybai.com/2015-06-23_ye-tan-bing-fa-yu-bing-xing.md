---
title: 也谈并发与并行
url: https://tonybai.com/2015/06/23/concurrency-and-parallelism/
published: '2015-06-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈并发与并行

在一般人的眼中，“并行”就是并行，即你干你的，我干我的，两个“并行”的执行过程可能是两条毫无瓜葛的平行线，也可能是有交叉，但瞬即分开的两条线。不 过在程序员的世界里，有关“并行”的概念却有两个单词：Concurrency和Parallelism，对应的比较主流的中文翻译为并发 (Concurrency)和并行(Parallelism)。

之前一直使用C、Python进行Coding，对Concrrency和Parallelism的异同并不十分关心，也未求甚解。但switch to [golang](http://tonybai.com/tag/go)后，尤其是学习2012年Rob Pike的一个talk slide：“[Concurrency is not Parallelism](http://talks.golang.org/2012/waza.slide)（译作：并发不是并行）"后，感觉之前对于“并行”的理解还未到火候。

golang的Author们对文档还是非常看重的。按照目前golang的age来说，其文档的充分性相对于其他语言已经是相对较好的了。golang 的 author们还时不时放出一些blog、talk和slide，以帮助大家编写出more idiomatic的[golang](http://golang.org)程序。Rob Pike的“并发不是并行”就是golang官方站点上的一个talk slide（中文版在[这里](http://http: //www.vaikan.com/docs/Concurrency-is-not-Parallelism) ）。

[Rob Pike](https://en.wikipedia.org/wiki/Rob_Pike)是Golang大神，这里先列出他在talk中对于并发与并行的学术阐释和理解：

【Concurrency并发】

Programming as the composition of independently executing processes. (Processes in the general sense, not Linux processes. Famously hard to define.)

将相互独立的执行过程综合到一起的编程技术。(这里是指通常意义上的执行过程，而不是Linux进程。很难定义。)

Concurrency is about dealing with lots of things at once.

并发是指同时处理很多事情。

Concurrency is about structure.

并发关乎结构。

Concurrency provides a way to structure a solution to solve a problem that may (but not necessarily) be parallelizable.

并发提供了一种方式让我们能够设计一种方案将问题(非必须的)并行的解决。

Concurrency is a way to structure a program by breaking it into pieces that can be executed independently.

并发是一种将一个程序分解成小片段独立执行的程序设计方法。

【Parallelism并行】

Programming as the simultaneous execution of (possibly related) computations.

同时执行(通常是相关的)计算任务的编程技术。

Parallelism is about doing lots of things at once.

并行是指同时能完成很多事情。

Parallelism is about execution.

并行关乎执行。

【小结】

They are Not the same, but related.

它们不相同，但相关。

怎么样？看上上面的论述是不是一头雾水啊。Rob Pike也觉得这些概念以及描述过于抽象，于是给了一个具体的“地鼠推车运书”的例子，不过当你看完这个例子后，可能会变得更加糊涂，至少我有这种感觉-**地鼠凌乱综合症**^_^。这是因为这个例子隐含的结合了Go语言goroutine调度的三个概念：P（虚拟processor上下文）、M(内核线程)和G（Goroutine对象）。如果仅仅从理解并行和并发的差异来说，我们可以抛开go语言，用生活中的例子感觉更适合些。

下面我们就来一个例子来说说明一下并发与并行，从一个程序的设计演进角度来阐述。

问题：说的是一个Gopher早起后的生活，Gopher早起后，有三个任务（或者称为三件事情）要完成：洗漱、早餐、着装。我们来设计一个程序，帮助Gopher高效正确的完成这三件事。

如果你是程序员，要完成这个场景，你可能会这么设计你的程序：

**program1:**

最简单的思路：这个gopher一件一件事情去完成：

main:

call 洗漱

call 早餐

call 着装

这里我们**把Gopher看做是一颗cpu**，它按程序逻辑，顺序执行洗漱、早餐和着装三件事。即如下图那样：

![](../../assets/d72b0e30f69c9879.png)


现在我们玩个克隆游戏，我们clone出一个与这个Gopher一模一样的Gopher，且两个gopher之间存在着某种超宇宙联系，一个Gopher行为的结果都能反应到另外一个gopher上。我们让这两个Gopher一起来做这三件事情，看看是否能够提速。

遗憾的是，两个Gopher都要从洗漱做起。一个Gopher占用了卫生间开始洗漱，另外一个Gopher只能等着，而没法去做早餐或是着装。当那个 Gopher完成洗漱，后面的这个Gopher由于超联系也同步完成了洗漱，进入下一个环节：早餐。过程还是一样的，只能一个Gopher在餐厅准备早 餐。也就是说这两个Gopher没有一起做事，而是一个做，一个赋闲。因此我们看到两个Gopher并没有加快事情完成的步伐，从过程上来看，即便有更多 的Gopher，也依旧无法提速。我们需要对程序做些改造。

注：首尾相连的红线的总长度 = 完成时间。

**program2:**

main:

pthread_create(洗漱)

pthread_create(早餐)

pthread_create(着装)

waitAll

Gopher来执行一遍新程序。由于建立了三个逻辑执行体，因此Gopher在三个执行体间切换，从Gopher的角度去看，Gopher的执行路径如下图：

![](../../assets/752e1ba2b6f754b0.png)


Program2-1

Gopher不再像上面Program1那样顺序执行了，而是在三个活动间切换，但总时长依旧没有下降。

为了验证该程序在多Gopher下是否有效率提升，我们再玩一次克隆游戏，这次clone出另外两个Gopher，三个Gopher一起来执行该程序，一个可能的执行路径见下图：

![](../../assets/728ea019f70d69ec.png)


Program2-2

每个Gopher绑定一个逻辑执行体，整体完成的总时长下降为原来的三分之一。这次三个Gopher都没有赋闲，真正做到你干你的，我干我的，一起做。

**program3:**

虽然在program2中，多个Gopher一起工作提升了效率，但那是极限么，还能提高么？我们试想一下三个活动：洗漱、早餐和着装的难易不同，耗时不 同。一个可能的结果是Gopher1完成了洗漱，但Gopher2才准备了一半早餐，Gopher3刚选完上衣。这时Gopher1便开始空闲，无法帮助 Gopher2和Gopher3继续提高效率。我们再试试重新组合一下要完成的任务，让每个Gopher都能执行不同的活动环节。

main:

c chan job

for i = 0; i < 3; i++ {

go gopherworker(c)

}

for j := range jobs {

c <- j

}

… …

gopherworker(c chan job):

for {

select {

case <-c:

… …

}

以下是一个可能的执行路径图：

![](../../assets/e88c8f2f4e8b3ea5.png)


到了这里，不知道你是否通过上面程序演进的过程悟道些什么，例子里我通篇没有提到并发或并行。

但从例子可以看出，并发和并行是两个阶段的事情。并发在程序的设计和实现阶段，并行在程序的执行阶段。

在Program1之前，我们只有问题，并无方案。

Program1方案让我们可以解决问题，但从Program1的执行结果来看，Program1并不能并行执行。原因是在设计和实现阶段程序就是按照顺序思路进行的，这就好比底子没打好，在平房的地基上永远不能盖50层的大楼。

Program2-1方案的执行结果与Program1相同，但Program2在设计和实现阶段采用的理念却与Program1完全不同，如果说 Program1打的是平房的地基，那么Program2打的就是大厦的地基，虽然Program2-1上依旧盖的是平房（单Gopher执行）。但 Program2-2显然就是在这样的地基上盖的摩天大楼了（多Gopher执行）。Program2的结构使得Program2在多Gopher下提升 了效率，实现了运行时并行。

Program3更进一步，在设计和实现阶段就本着充分高效的利用多个Gopher的理念，并最终实现了执行阶段的并行。

因此我们在编程语言层面更多谈并发，Golang对外宣传时永远用的是支持并发，而不是支持并行。设计实现阶段好比打地基，不同水准的地基决定了你在这个地基上面是只能盖平房，还是盖高层，还是能盖摩天大楼。

我们再回过头来重温Rob Pike大神关于两者的阐述：“并发关乎结构，并行关乎执行”，是不是感觉意味深长啊，大神就是大神，一句话就能抓住本质。

[go 1.5](https://github.com/golang/go/blob/master/doc/go1.5.txt)之前默认情况下，Go程序都是不能并行的，因为Go将GOMAXPROCS默认设置为1，这样你仅仅能利用一个内核线程。Go 1.5及以后[GOMAXPROCS被默认设置为所运行机器的CPU核数](http://golang.org/s/go15gomaxprocs)，如果你的机器是多核的，你的Go程序就有可能在运行期是并行的，前提是你在设计程 序时就充分运用了并发的设计理念，否则就会像Program1那样，即便有1w颗CPU，你也只能利用上一颗。

© 2015, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

操作系统原理书上 介绍过这两个概念的区别

没看懂

确实精辟

感謝解釋，

將程式碼解釋成實際例子！