---
title: Go语言的遗产
url: https://tonybai.com/2019/11/04/the-legacy-of-go/
published: '2019-11-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言的遗产

本文是[gohugo](https://gohugo.io/)作者[Steve Francia](https://spf13.com/)在意大利佛罗伦萨举办的[GoLab](https://golab.io/)上分享的闭幕演讲讲稿的[文字版](https://spf13.com/presentation/the-legacy-of-go/)，该演讲的主题为”Go的遗产”。该演讲讨论了[Go语言](https://tonybai.com/tag/go)继承的遗产，以及它是如何尊重这些遗产的，并在最后总结了Go希望留给后来者的遗产。

![img{512x368}](../../assets/62a6430a5f501ea7.png)


**演讲胶片**

我们有责任保留好留给我们的遗产，并留下值得我们子孙后代继承的遗产 – 克里斯汀·格雷格（Christine Gregoire）


## 1. Go语言之前

![img{512x368}](../../assets/9f41318efbc3b911.png)


### 1950年

在1950年代后期，人们对每台新计算机如何产生自己独特的语言而感到不安。当时，编程语言是由硬件制造商提供的，并且因型号而异。跨计算机且保持一致的第一门编程语言是[Fortran](https://en.wikipedia.org/wiki/Fortran)，但这仍然仅适用于其制造商IBM(生产的计算机)。而后，人们成立了一个委员会，该委员会的使命就是设计第一种真正通用的、独立于机器的编程语言。

![img{512x368}](../../assets/f505dda561ade646.jpg)


图：编程语言历史Babel塔，CACM封面，1961年1月

### 1960年

1960年1月，有13位计算机科学家在巴黎举行了一次空前的会议，旨在(设计)开发出这样一种语言。美国派出了6位代表，欧洲派出了7位代表。

会议上无休止、令人振奋的讨论也让科学家们筋疲力尽。当一个人的好主意与他人的坏主意一起被抛弃时，一个人就会变得更加恼火。然而，在整个会议期间内，大家都没有懈怠，持续地努力投入着。

最终这13名科学家的思想碰撞产生了良好的化学反应 –

[Alan Perlis]。

![img{512x368}](../../assets/cff61acb0355cf7c.png)


这是一种远远超越其时代的语言，它不仅是对其前辈的一种改进，而且对其所有后继者也产生了重大影响。-

[Tony Hoare]关于编程语言设计的提示– 1973年

- 尽管发表了这一声明，但Tony Hoare和
[Niklaus Wirth](https://en.wikipedia.org/wiki/Niklaus_Wirth)还是一起创建了称为[ALGOL W](https://en.wikipedia.org/wiki/Algol_W)的[ALGOL 60](https://en.wikipedia.org/wiki/Algol_60)的后继产品。 - 进而导致Niklaus Wirth继续创建了
[Pascal](http://pascal-central.com/ppl/index.html)，Pascal编程语言最初于1970年发布。 - 接下来，
[CPL(Combined Programming Language)](https://en.wikipedia.org/wiki/CPL_%28programming_language%29)在剑桥大学独立创建，也被称为“剑桥编程语言”。 - 接下来，一种称为
[BCPL(或Basic CPL)](https://en.wikipedia.org/wiki/BCPL)的、基于CPL但比CPL更简单的编程语言诞生。 - 在美国
[贝尔实验室](https://www.bell-labs.com/)，[Ken Thompson](https://en.wikipedia.org/wiki/Ken_Thompson)和[Dennis Ritchie](https://en.wikipedia.org/wiki/Dennis_Ritchie)创建了[B语言](https://en.wikipedia.org/wiki/B_(programming_language))，主要基于BCPL。 - 在B语言发明后不久，它的后继者
[C语言](https://tonybai.com/tag/c)就诞生了。

![img{512x368}](../../assets/47d4e6fef0fb3c1a.png)


之后，原本一脉相承的语言出现了分裂：

![img{512x368}](../../assets/8b409a6349418085.png)


- C语言在美国激增，激发和促进了C++、C＃、Java以及JavaScript、Python、Perl、PHP和许多其他语言的诞生和发展。

![img{512x368}](../../assets/1486ca04d69184bd.png)


- 到2007年，存在的数十种编程语言都可以追溯到其共同祖先：Algol。

![img{512x368}](../../assets/ecd6c623fd2eba63.png)


### 1964年

我们的并发故事始于[Doug McIlroy](https://en.wikipedia.org/wiki/Douglas_McIlroy)，他在1964年提出了一些新的想法，这些想法最终演化为Unix Pipes。

当有必要以另一种方式处理数据时，我们应该有一些耦合程序的方法，例如像将花园软管拧入另一部分那样。这也是IO的方式。- Doug McIlroy


```
背后故事
在1970年至1972年的一段时间内，我不时说：“如何做这样的事情？”，然后我提出了另一个建议，另一个建议，另一个建议。有一天，我想出了一种shell语法用于支持管道使用，Ken说：“我要去实现它！”他厌倦了听到所有这些内容……[并且]他说，“要去实现它”。他没有完全按照我为管道系统调用所建议的去做。他发明了一种更好一点的东西，终于又改变了今天的样子。他在一夜之间将管道符放入了Unix（并且他做到了）……。
麦克罗伊（McIlroy）引述：布赖恩（Brian）的墙上还挂着一张纸，在那张纸上我谈到了像花园软管那样将流（stream)拧在一起。所以这个想法在我脑海中徘徊了很长时间。
同时，在Thompson和Ritchie在黑板上，草拟了一个文件系统，我正在草拟如何在黑板上进行数据处理，方法是将一系列过程串联在一起，并寻找一种将过程连接在一起的前缀表示法语言。之所以失败，是因为很容易说出“cat into grep into……”或“who into cat into grep”等等。这么说很容易，而且从一开始就很清楚，这就是您想说的。但是这些命令具有所有这些附带的参数。它们不仅具有输入和输出参数，还具有选项，并且在语法上还不清楚如何将这些选项插入以前缀表示法编写的链中，比如：cat（grep（who …））。在句法上很多人不知道如何做。所以我把这些非常漂亮的程序写在黑板上，用的语言不够强大，无法应付现实。因此，我们实际上并未这样做。
```


### 1978年

到1978年，在对多处理器进行编程的背景下，有许多提议的方法被用于通信和同步。共享内存是最常见的通信机制。

[托尼·霍尔（Tony Hoare）](https://en.wikipedia.org/wiki/Tony_Hoare)发表了一篇论文，该论文改变了一切。它比时代提前了几十年。他称他的论文为:”通讯顺序进程，communicating sequential processes”，就是大家熟知的CSP。

![img{512x368}](../../assets/d18adcae71259818.png)


- 进程(Processes)：执行单元
- 顺序(Sequential)：每个进程都作为一个普通的单线程程序运行
- 通讯(Communicating)：进程如何协调
- 没有内存共享
- 没有线程，没有互斥体

Hoare的论文提出了一种语言，每个进程（或者作为一个普通的单线程程序）按顺序执行，通过无缓冲通道(unbuffered channel)相互通信。Hoare的通信进程比典型的Unix Shell管道更通用，因为它们可以以任意模式连接。

![img{512x368}](../../assets/0f636f3c59adfb50.png)


三个语言分支因Hoare的CSP论文而诞生：[Erlang](https://www.erlang.org/) 、[Occam](https://en.wikipedia.org/wiki/Occam_(programming_language))和[Newsqueak](https://en.wikipedia.org/wiki/Newsqueak)。

- 1983年诞生的Occam最接近CSP论文（由Hoare推荐）
- Erlang在80年代后期专注于CSP的功能方面，并使用mailbox在进程之间进行通信
- Rob Pike(Newsqueak之父)追逐了并发白鲸(the concurrency white whale)长达20年

![img{512x368}](../../assets/8504087682e44ba3.png)


Go是第一种可以同时拥有欧洲和美国语言设计分支传统的语言。实际上，它已经统一了这三个分支

2016年，[黑客新闻评论（Hacker News）](https://news.ycombinator.com/)上的[一则帖子](https://news.ycombinator.com/item?id=11454563)称Go语言时停留在70年代的一种语言，这引起了一些对Go的批评……

## 2. 对过去伟大思想的复兴

![img{512x368}](../../assets/0b3468cf3d82bdd9.png)


### 编程语言发展的四波浪潮

![img{512x368}](../../assets/66304bda10f00c37.png)


- 第一波浪潮：语言扩张 – 巴别塔

特征：多样化。很久以前，语言是多种多样的，并在在思想、方法和意见等方面体现出多样性。

- 第二波浪潮：语言的标准化

特征：快速、复杂且对开发不友好。语言的标准化发生了数十年。到2000年代，事情开始停滞。他们融合为两个阵营：Java/JVM和C/CLR。C++、Java、C＃都非常相似。

- 第三波浪潮：脚本语言

特征：慢、不安全但对开发友好。脚本语言作为对上述语言的复杂性和痛苦的回应而应运而生。它们开发快速而松散，对开发人员友好，但缺乏性能和安全性。

- 第四波浪潮：恢复

特征：快速、安全、对开发人员友好

Go是对这些语言的复杂性和痛苦的一种反应，也是对脚本语言快速开发和松散本质的反应。

Go恢复了早期语言的简单性和灵活性，增加了现代语言的安全性和开发友好性。Go以一种非常真实的方式复兴了许多伟大的想法，这些想法终于准备就绪。

Go给人的感觉就像是来自60年代，70年代，80年代，90年代，00s，10年代的语言……Steve Francia 2019


**Go感觉像这样是因为它由过去60年来的许多伟大构想组成。**

![img{512x368}](../../assets/869802e58c325201.png)


现在，我想谈谈Go中的3种特定功能(简单、并发和Go的OO)以及这些思想起源的4种语言(Oberon、Newsqueak、Simula和Smalltalk)。在Go恢复它们之前，许多思想被遗忘了。

### 1988年

**简单易读的结构和语法: Oberon＆C**

[Niklaus Wirth](https://www.computerhistory.org/fellowawards/hall/niklaus-wirth/)负责Algol-W，Pascal，Modula。现在是1988年，他的最新语言是[Oberon](http://en.wikipedia.org/wiki/oberon_(programming_language))。

Oberon的程序结构，以[“hello, world”例子](https://github.com/vishaps/oberonbyexample)为例:

```
MODULE hello;
IMPORT Out;
BEGIN
Out.String("Hello, World"); Out.Ln
END hello.
```


Oberon围绕着爱因斯坦（Albert Einstein）的座右铭设计：“使事情尽可能简单，但不要过于简单。”

程序结构非常简单。

下面是Go的”hello world”程序结构：

```
package main
import "fmt"
func main（）{
fmt.Println"hello world"）
}
```


这个例子看起来应该很熟悉，它直接采用Oberon的结构。

我们再来看看Oberon的[声明结构](https://github.com/vishaps/oberonbyexample/blob/master/variables/Variables.Mod)：

```
CONST n = 42；
TYPE mystring = ARRAY 32 OF CHAR;
VAR s: mystring;
PROCEDURE squared(x:INTEGER):INTEGER;
BEGIN
RETURN x * x
END squared;
VAR b,c: INTEGER = 1,2;
```


再来看看Go的声明结构：

```
const n = 42
type mystring string
var s mystring
func squared(x int) int {
return x*x
}
var b, c int = 1, 2
```


在Go和Oberon中，声明都是从左到右（名称，类型，可选值），这恰与C相反，在C语言中，类型放在前面。

很多人看到Go后会问为什么我们要翻转C语法，他们错误地认为Go的声明结构来自C语言。它不是，它来自Oberon。

Go使用了Oberon形态，但却用C的token：

- {}代替BEGIN END
- ++，– 代替（内置）的INC和DEC
- != 代替#
- ％代替MOD
- || 代替OR
- []代替ARRAY
- 结构体代替RECORD
- *代替POINTER TO

虽然结构来自Oberon，但Go使用的token却来自C。

- 这里没有太多，这就是重点。语法和结构都很简单。
- 没有继承，没有层次。没有复杂的作用域(scope)系统。
- 它们尽可能简单，但并不过于简单。

您可以看到Go如何采用Oberon的简单结构，但是删除了笨拙的语法，并采用C语言的更加优雅和熟悉的语法替换了它们。

这样做的结果是一种非常易读的语言诞生了。

### 1989年

**并发与Newsqueak**

罗伯·派克（Rob Pike），他于1989年在贝尔实验室工作。他在这里设计了[Newsqueak](https://swtch.com/~rsc/thread/)。

[Newsqueak](https://en.wikipedia.org/wiki/Newsqueak)是一门用于研究和探索的编程语言- 它致力于在
[Sequeak](https://squeak.org/)基础上添加实用的、切实可行的并发(concurrency)支持 - Newsqueak语法上类似C
- 像CSP一样，Newsqueak使用Channel作为Process的集合点

Rob Pike的Newsqueak在语法上看起来像C，但对并发支持的更好。Squeak用于设计菜单和滚动条之类的设备，Newsqueak解决了同样的问题，但涉及范围更广：Newsqueak用于编写整个应用程序，尤其是窗口系统。

**Newsqueak-Prime Sieve pt.1**

译注：Rob Pike拿手的素数筛例子


```
counter := prog(end: int, c: chan of int) {
i: int;
for(i = 2; i<end; i++) c<-=i;
};
filter := prog(prime: int, listen, send: chan of int) {
i: int;
for(;;)
if((i=<-listen)%prime)
send<-=i;
};
```


**Newsqueak-Prime Sieve pt.2**

```
sieve := prog(c: chan of int) {
for(;;) {
prime := <-c;
print(prime, “ “);
newc := mk(chan of int);
begin filter(prime, c, newc);
c = newc;
}
};
count := mk(chan of int);
begin counter(10000, count);
sieve(count);
```


与CSP和Squeak不同，Newsqueak将channel视为一等公民：channel可以存储在变量中，可以作为参数传递给函数，甚至channel自身也可以通过channel发送。

另外”<-c(receive)”表达式也是第一次在这里介绍。

**channel和routine**

```
Go:
c := make(chan int)
c <- 1
x = <-c
go f(x)
vs.
Newsqueak:
c := mk(chan of int);
c <- = 1;
x = <-c;
begin f(x);
```


我们看到：Go的并发方法几乎与Newsqueak完全相同，channel和 goroutines的使用方式也是相同的。

**select**

Newsqueak还使用了看起来与Go的select语句非常相似的select。

```
select {
case msg1 = <-c1:
print(“received”, msg1, “\n”);
case msg2 = <-c2:
print(“received”, msg2, “\n”);
}
```


您可以清楚地看到Go并发的基础在25年前是如何在Newqueak中被建立起来的。Go采纳了这些”老想法”，并对其进行了改进，使其可以投入生产。

**Ryan Dahl: Node.js的创建者的访谈(2017)**

我喜欢Go的编程模型。使用goroutine是如此简单和有趣……如果您要构建服务器，那么我无法想象使用Go以外的任何工具。Goroutine使Go的并发变得简单。


### 1965年

**面向对象基础(Smalltalk)**

OO在C++/Java之前就已存在，在C++和Java重新定义面向对象之前。

**什么是面向对象？**

- 附加到数据对象的过程(Procedure)
- Procedure的可重用性

**Procedure+数据**

![img{512x368}](../../assets/21a3d18804c378a3.png)


[Simula](https://en.wikipedia.org/wiki/Simula)继承了Algol，并在其中添加了对象，类，继承和子类。 Simula被认为是第一种面向对象的编程语言，并且在Smalltalk和所有随后的OO语言的开发中具有重要的影响力。

Simula改变了一直以来的从Procedure的角度来看的思维方式，…他将其翻转为…面向对象的视角，即在每种类型的对象中，您都有处理它的所有方法。- Small Talk的实现者Dan Ingalls


### 1980

接下来是Smalltalk，其中一切都是对象，并且仅通过发送消息与对象进行通信。

![img{512x368}](../../assets/6feda78ee80310ba.png)


我确实发明了“面向对象”这个术语，但这是一个错误的选择，因为它没有强调消息发送这个更重要的思想。 – Alan Kay: 从A到Z的编程语言：Smalltalk-80 – 2010


### 1989年

**Procedure重用**

我们将讨论两个出版物:

如果系统的任何部分取决于另一部分的内部结构，那么复杂度会随着系统大小的平方而增加 – Dan Ingalls面向对象编程— 1989年


继承。 我们看到了继承带来的这种指数级复杂性

对于使用半新的OO语言进行编程的任何人，这应该看起来都很熟悉。关系线无处不在。 –

[SPAGHETTI CODE的诞生]

论文[《强类型面向对象编程的接口》](https://www.cs.utexas.edu/~wcook/papers/OOPSLA89/interfaces.pdf)中所提到的系统提供了Ada和Modula-2之类的语言中的模块接口的优点，同时保留了可表达性，使无类型的面向对象的语言（如Smalltalk）具有灵活性。

**Go interfaces**

```
type Point interface {
X() int
Y() int
Move(int,int)
Point Equal(Point) bool
}
```


Go团队在实现interface时并不知道到该论文的存在。由于这两种方法的明显相似性，后来与他们share了该论文。

Go采取了非常相似的方法，但是对上面论文中想法进行了改进，因为Go接口是隐式的，这使Go应用程序解耦并提供了极大的灵活性。

当您尝试分解一个复杂的问题时，您想要尝试将其分解为尽可能少的部分，并且希望它们尽可能独立。 – Dan Ingalls 面向对象编程— 1989


Go的interface和method采用尽可能独立的方式。只要添加正确的方法，任何类型都可以满足任何接口。可以在满足该接口的类型之前或之后定义一个接口。事实证明，这种方式是有效的，而且效果很好。

**Go的OO**

- method提供任何类型的消息发送机制
- 接口通过动态调度多态性提供可重用性

Go提供了像Smalltalk定义的那种面向对象编程，只是更加贴近实际，即使它不包含类，对象或继承。

- Smalltalk: OO是关于消息发送
- Go的interface允许方法像Smalltalk的消息一样自由使用，但是是在一种有类型的语言中使用

## 3. Go的设计哲学

![img{512x368}](../../assets/43eea1402d58dd3a.png)


### 2007年

**在一次耗时45分钟的C++构建过程中……**

罗勃·派克：把时钟拨回到2007年9月，当时我正在对一个巨大的谷歌C++程序做一些微小但重要的优化工作，你们都与这个庞大的程序做过交互。我得这个编译过程在我们的巨大的分布式编译集群上跑了约45分钟。我收到一条消息:为C++标准委员会服务的几位Google员工将进行一个演讲，他们将告诉我们C++ 11的新功能。

在一个小时的演讲中，我们听到了有关计划中的35个新功能的消息。……这时我问自己一个问题：”C++委员会真的相信C++的不足之处在于它没有足够的功能吗？” 当然……，简化语言而不是为其添加更多功能将是一个更大的成就。Rob Pike和他的办公室同事(Robert Griesemer、Ken Thompson)回到了办公桌前。这真的让他们开始思考…

现代实用的编程语言应该是什么样？到45分钟构建完成时，他们已经有了一个充满想法的白板。

### 语言设计的进化过程

我们从头开始构建，仅从C中借鉴了一些小东西，例如运算符和大括号，以及一些通用关键字。当然，我们还借鉴了我们所知道的其他语言的想法。- 罗伯·派克（Rob Pike)

少即是(指数级的)多 – 2012年，在谈到Go的灵感时 Rob Pike


Go的众多祖先和对Go有影响的语言：

![img{512x368}](../../assets/e327b816d09135a4.png)


我要说的是，没有哪位语言设计师比这三位语言设计师(Rob Pike, Robert Griesemer, Ken Thompson) 具有更广泛或更深的语言设计专业知识。他们对以前发生的事情有很丰富的了解，他们知道该采摘什么。他们还具有事后观察的优势(后发优势)。这是修复他们认为可以做得更好的事情的机会。

**进化不是革命**

- 原则1：大多数思想都来自先前的思想

大多数思想根本不是新事物

**进化不是革命：新语言应该巩固而不是发明新特性**

**等待良好的设计**

- 原则2：No是暂时的，Yes是永远的。

在Go的整个历史中，有很多这样的实例。通常的想法是，在设计语言时，不会出现“撤消(undo)”的情况。如果您今天说“No”，那么您明天总是可以说“Yes”，但是如果今天您说“Yes”，那么您将在很长一段时间或永远被它“困”住…。

如有疑问，请将其排除在外。- Joshua Bloch：关于设计的对话– 2002


**共识驱动的设计**

- 原则3: 应该使一切都尽可能简单，但不要过于简单。-爱因斯坦

当我们三个人开始时，这纯粹是研究。…我们从一个想法开始，即我们三个人都必须针对该语言的每个特性进行讨论，因此，无论出于何种原因，都不会在该语言中放入多余的垃圾。 – 肯·汤普森（Ken Thompson）访谈– 2011年，肯从Bell Labs学习了这种做法

有两种构建软件设计的方法。一种方法是使其变得如此简单，以至于显然没有缺陷。另一种方法是使其变得如此复杂，以至于没有明显的缺陷。 – 托尼·霍尔（Tony Hoare）皇帝的旧衣服-1981年，Go采取了第一种方法，而大多数其他语言都采用第二种方法。


**快速迭代期待并实现大规模改变**

- 最后一个原则是快速迭代的原则。

当您处于语言的设计阶段时，您将需要进行频繁且有时是巨大的更改。朝着这个期望前进，并围绕它建立您的流程。

## 4. 今天的Go

![img{512x368}](../../assets/0d1b78433c028253.png)


我们来看Go如今是如何演变的。

### 2019年

Go今天是如何继续进行演化的。

上面的4条原则在该语言的初期，在发行稳定版之前和被采用之前都非常有效。

但我们现在的处境非常不同。我们不再能够将所有贡献者都放在白板上，甚至不能放在如此大的房间中(译注：Go目前的contributor数量庞大)。

现在，我想与大家分享Go项目今天如何进行更改的。

我们的原则是“等待良好的设计”，这似乎意味着这是一种消极的活动，但这与事实相去甚远。真正的意思是，除非我们非常有信心采用正确的方法，否则我们不会接受更改。

这意味着所有问题的默认答案是“否”。“是”的成本非常高，因此需要一个压倒性的理由。

对一件事说“Yes”意味着对其他一切都说“No”。

软件复杂性的主要原因是供应商不加批判地采用了用户想要的几乎所有功能。人们似乎将复杂误解为先进。

不可理解的应该引起怀疑而不是钦佩。- Niklaus Wirth, 1995年


我们对Go进行了长期展望。为下一个[十年](https://tonybai.com/2017/09/24/go-ten-years-and-climbing/)或两个或更多个而设计。大多数项目的运行时间要短得多，因此通常会接受第一个可通过的解决方案。

随着时间的流逝，经过长时间这种训练的人们已经意识到：如果一个好主意会被接受，或者反之，不好的主意会被拒绝。

由于我们的长期观点，在为Go项目做出贡献时人们挣扎并不罕见。当他们的想法不能被接受时，许多人感到被亲自拒绝。

或更糟糕的是，人们会感到自己不合格或不称职。我记得有这种感觉。

几年前，我创建了一个网站引擎Hugo，随着时间的推移，它成为Go模板的第一用户，并在此过程中发现了几个问题。尽管如此，我感到非常没有资格报告这些问题，因为我认为创建这些库的“专家”显然比我了解更多，并且我无能为力。在第一次或第二次Gophercon上，我碰巧在午餐台上站在Russ Cox旁边，我们开始交谈。他强烈鼓励我报告这些问题，并让我知道他们多么地需要反馈。

几年后，我加入了Go团队，并从这个经验中学到了很多。我观察到的一件事是，Go团队那些加入较久的核心成员有一件事比大多数其他成员都做得更好，这可能不是您的想法。Go团队的老成员已经非常习惯于听到“不”的声音。我们团队成员的提议被拒绝的比率很高，甚至高于Go团队之外的提议。我们已经了解到，每个“No”都与拥有正确的“Yes”仅一步之遥。

因为我们经常听到“No”的声音，所以我们同情别人被拒绝的感觉。

今天我要传达给您的信息是您受到重视和需要。请继续尝试。在接下来的十年或二十年或更长的时间内，您是Go演化的关键部分。

**Go开发流程**

实验流程简化始于今年早些时候，Russ Cox谈论了我们用来对Go进行更改的流程以及它的演变方式。在演讲中，他讨论了实验的两个步骤，并简化了我们的迭代过程。

我们的过程不是为了速度而建立的，而是为了正确。我们花费大量时间进行实验和简化，然后完善自己的想法，直到它们正确为止。

你们都是Go伟大实验的一部分，并且是继续构建Go的过程的关键部分

我想与大家分享3种方法，每个人都可以为Go做出贡献。

- 使用Go -> 识别问题 -> 您遇到的事情/体验并写下来。
- 您有想法-> 编写建议 -> 纳入反馈
- 您阅读提案 -> 阅读评论 > 添加您的声音

![img{512x368}](../../assets/7d8469633f67e3f1.png)


**Go开发过程：实验 -> 简化 -> 最终交付**。通过此提炼过程，想法将准备就绪，我们将进行交付。我想对过程的这一部分及其工作原理提供更多见解。

**共识驱动的设计**

- 误解：谷歌有一小群“决策者”
- 真相：评论者之间达成共识

**关于提案过程的事实**

- 事实上，大多提案提案都很小
- 几乎所有提案的讨论最终都在参与者（评论员）之间达成了共识。
- 提案审核委员会主要进行一些“园艺劳动”（译者：社区行为培养)

您看到这不是一件非常迷人的工作。我们评论的大多数问题都要求您澄清问题或什么也不做，让对话继续进行。我们还会考虑谁在对话中丢失，并邀请他们加入对话。

当讨论似乎已经解决（赞成或反对）时，我们将关闭其中的一小部分。

让我们看一下最近的一个建议。这只是从最近提案池中随机选取的一个。

它具有一些有趣的属性：大量参与，来自9个参与者的25条评论引用用户问题（体验）。早期该issue尚无共识（由点赞决定）。

在对该想法进行讨论和完善之后，很明显已经达成了普遍共识。

它被标记为“可能接受”，并且留下足够的时间窗口允许任何人提供我们不接受的理由。

这是一组最近审核的提案。您会注意到，他们每个人都引用了之前的评论，并根据这些评论提出了建议。

在提案审核委员会中，通常会有一个人留下评论，但代表所有出席者。Russ Cox通常志愿承担了这个角色，这就是为什么所有这些issue上面都加上他的名字的原因。在大多数情况下，此窗口不会附加注释。我们觉得这个窗口虽然很少使用，但对于建立共识的过程至关重要。

### 变化是缓慢发生的

这是设计使然。这是缓慢的、谨慎和有条不紊的，以确保我们最终达到想要的目标。

**过去十年的主要里程碑**

尽管Go的变化缓慢，但增长迅速。我想了解一下过去十年中的一些主要里程碑。

![img{512x368}](../../assets/899d417e8e73eb81.png)


- 2009年, Go语言开源，Gopher诞生，Go脱离了Google的实验场；
- 2010年，获得年度TIOBE语言，Bossie奖，引入append和go tour；
- 2011年，gccgo合并到GCC中，引入gofix，YouTube在生产中采用了Go；
- 2012年，Go 1.0发布！发布Go1兼容性承诺；在Google内部发布第一项Go生产服务

![img{512x368}](../../assets/c9422881e5adc15d.png)


- 2013年，Packer，Docker，Hugo用Go编写；6个月发布周期；第一个Go大会举行（日本东京）
- 2014年，Kubernetes使用Go开发；代码仓库由Mercurial→Git；第一次美国和欧洲会议；Go项目贡献者达到500名；
- 2015年，Go编译器使用Go重写，实现自举；GC精化; Women Who Go&GoBridge born; 印度、中国第一次go大会举行；
- 2016年，支持HTTP/2和Context；第一次拉丁&中东Go大会举行；最受喜欢的5门编程语言；第一次Go用户调查；贡献者达1000名；

![img{512x368}](../../assets/e9a1dd60d3173f1b.png)


- 2017年，GC小于ms级的暂停; 引入type alias；开发人员想要使用编程语言第一名第一次）; 13次会议; 第一届贡献者峰会
- 2018年，引入Go模块；来自Go团队之外的贡献者人数首次超过Go团队；19次Go会议；Go新品牌和logo发布；PR数在github排名第四; 开发人员打算学习的语言中排名第一

## 5. Go的遗产

![img{512x368}](../../assets/b77252c193d5200a.png)


没有时间机器可以达到未来。未来的到来缓慢而又出乎意料。我们不知道Go或世界将会发生什么。但是我们确实知道我们想留下什么标记。

- 我们希望Go能够留下创新的遗产

Go向主流受众带来了创新的想法，例如goroutine，channel，简单的interface。这些想法现在正在其他语言中出现，我们为这一趋势继续感到高兴。

Go fmt于2009年推出时颇有争议。现在，大多数语言都采用了类似的方法。

也许我们最有影响力的遗产将是，我们像Go一样激励人们挑战既定的规范，并在各处寻找灵感。

- 我们希望Go留下增强信心和能力的遗产

Go使开发人员能够编写生产服务器软件而无需C和C++所需的额外专业知识，而无需现代Java的复杂性，也无需解释语言的性能成本。

Go比其他任何语言都更能使人们把他们的想法变成现实。当我第一次开始撰写Hugo时，我个人感觉到了这一点，这是Go最吸引我的地方。

其他那些也被赋予了类似的能力和信心的人，其中许多人在本次会议上谈到了Go的创造性用途，包括Florin的家庭自动化研讨会，Ron的机器人，Elias的GUI等。

- Go改变生活。

我有幸环游世界，在任何地方遇到的男人和女人，他们通常没有CS背景或学位，但能够学习Go并用它来创办公司，获得更好的工作并改善他们和他们家人的生活。

遗产不会为人们留下任何东西。它在人们身上留下了一些东西。- 彼得·斯特普尔


我们每个人都受到过往历史的影响。我们是遗产。我们被影响，我们影响别人。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

好文，感谢Tony老师！