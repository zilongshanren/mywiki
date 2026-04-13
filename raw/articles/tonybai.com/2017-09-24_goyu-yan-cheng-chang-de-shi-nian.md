---
title: Go语言：成长的十年
url: https://tonybai.com/2017/09/24/go-ten-years-and-climbing/
published: '2017-09-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言：成长的十年

[Go语言](http://tonybai.com/tag/golang)之父，Google大神[Rob Pike](https://en.wikipedia.org/wiki/Rob_Pike)代表Go语言的另外两位缔造者[Robert Griesemer](https://github.com/griesemer)和[Ken Thompson](https://en.wikipedia.org/wiki/Ken_Thompson)在自己的博客上发表了一篇名为[《Go: Ten years and climbing》](https://commandcenter.blogspot.co.uk/2017/09/go-ten-years-and-climbing.html)的文章，用以纪念Go语言从最初的设计idea起到目前的十年发展。笔者读完后，也是深有感触，因此在这里粗略翻译一下全文，希望能有更多的程序员加入到Gopher行列中来。

译文全文如下：

![img{512x368}](../../assets/cb05df1ee9df9c64.jpg)


Drawing Copyright ©2017 [Renee French](http://reneefrench.io/)

本周是创建Go语言十周年的纪念日。

记得第一次关于这门语言设计的讨论是在2007年9月20日，一个周四的下午。进而在第二天的下午两点，我、Robert Griesemer以及Ken Thompson在谷歌山景城总部43#楼的一间名为Yaounde的会议室里又组织进行了一场有关这门语言设计的会议。这门语言的名字诞生于9月25日，在第一封有关语言设计的mail中可以看到一些关于命名的设计考量：

```
Subject: Re: prog lang discussion
From: Rob 'Commander' Pike
Date: Tue, Sep 25, 2007 at 3:12 PM
To: Robert Griesemer, Ken Thompson
i had a couple of thoughts on the drive home.
1. name
'go'. you can invent reasons for this name but it has nice properties.
it's short, easy to type. tools: goc, gol, goa. if there's an interactive
debugger/interpreter it could just be called 'go'. the suffix is .go
...
```


(将语言命名为Go这事儿值得一提；“golang”来自于这门语言的web站点地址（因为go.com当时已经是迪斯尼的一个web站点了），但却不是语言的恰当名字。)

Go项目将2009年11月10日，即Go项目正式开源的那天作为其官方生日。最初Go项目托管在code.google.com上，几年后迁移至GitHub。不过，现在我们要回到最初的语言概念构建阶段，即那之前的两年，这可以让我们做更进一步地回顾，以更久远的视角，见证一些语言早期的历史事件。

Go开发过程中的第一个惊喜是收到下面这封mail信息：

```
Subject: A gcc frontend for Go
From: Ian Lance Taylor
Date: Sat, Jun 7, 2008 at 7:06 PM
To: Robert Griesemer, Rob Pike, Ken Thompson
One of my office-mates pointed me at http://.../go_lang.html . It
seems like an interesting language, and I threw together a gcc
frontend for it. It's missing a lot of features, of course, but it
does compile the prime sieve code on the web page.
```


Ian Lance Taylor的加入以及第二个编译器实现(gccgo)在带来震惊的同时，也伴随着喜悦。这对Go项目来说不仅仅是鼓励，更是一种对可行性的证明。有了语言的第二个实现对确定语言规范和标准库的过程是至关重要的，同时也有助于Go保证其高可移植性的[承诺](https://golang.org/doc/go1compat)。

虽然Ian的办公室离我们不远，但在看到这封mail之前我们从未谋面。不过，从那之后，Ian Lance Taylor便成为了Go语言及工具设计和实现的核心人物。

Russ Cox也是在2008年加入到刚成立不久的Go语言开发团队的。随着他的加入，他的一些天赋也随即在语言设计和实现中展现出来。Russ发现Go method的通用性意味着一个函数也可以拥有自己的方法，这直接导致了[http.HandlerFunc](https://golang.org/pkg/net/http/#HandlerFunc)的出现，这是一个我们所有人都未曾想到的结果。Russ还在当时设计的基础上提出了一些更泛化的想法，比如[io.Reader](https://golang.org/pkg/io/#Reader)和[io.Writer](https://golang.org/pkg/io/#Writer)接口，奠定了所有I/O库的整体结构。

Jini Kim是我们最初的产品经理，他招来了安全专家Adam Langley来帮助我们将Go推向Google外面的世界。Adam为我们做了许多不为外人所知的事情，包括创建最初[golang.org站点](https://golang.org/)的web页面以及[build dashboard](https://build.golang.org/)。不过他最大的贡献当然要属cryptographic库了。起先，对于我们中的一部分人来说，这个库无论是规模还是复杂度，和其他库比起来都不成比例。但是就是这个库在后期成为了很多重要的网络和安全软件的基础，并且成为了Go语言开发历史的关键组成部分。像[Cloudflare](https://www.cloudflare.com/)这样的网络基础设施提供商就重度依赖Adam在Go项目中的工作，Internet也因此变得更好。因此，我们由衷感谢他的工作。

事实上，许多公司在早期使用Go进行开发，尤其是初创公司。其中一些公司成为了云计算的巨头，其中就有一家这样的公司，它现在叫[Docker](https://www.docker.com/)。这家公司使用Go语言，并催化出计算领域的容器行业，进而导致了像[Kubernetes](https://kubernetes.io/)这样的项目出现。今天我们可以说Go是容器语言，这是另一个我们完全没有预料到的结果。

不过，Go语言在云计算领域起到作用更大。2015年3月，Donnie Berkholz在为[RedMonk](https://redmonk.com/)撰写的一篇文章中宣称：[Go是“云计算基础设施新兴语言”](http://redmonk.com/dberkholz/2014/03/18/go-the-emerging-language-of-cloud-infrastructure/)。几乎与此同时，[Apcera](https://www.apcera.com/)的Derek Collison说：Go已经是云计算语言了。在那个时候，这也许还不是事实。但Berkholz所使用的“新兴”一词却恰如其分的表明了Go在当时的地位。

今天，Go已经成为云计算语言。想象一下：一个只有10岁的年轻编程语言已经成为这样一个规模庞大且不断发展的行业的主导者，这样的成功以前只是存在于在想象中。如果你觉得“主导”这个词太过强势的话，让我们来看看中国互联网行业。一段时间以来，Go在中国地区大量使用的数据一度让我们误认为[Google趋势图](https://trends.google.com/trends/explore?q=golang)出现了某些错误，但是凡是去过中国，参加过中国区Go语言大会的人都可以证实：Google趋势图的数据是真的，Go在中国的使用非常火爆！

简而言之，Go语言的十年发展为我们带来了许多里程碑。 最令人惊讶的是我们现在的位置：[保守估计](https://research.swtch.com/gophercount)表明至少有50万Go程序员。 当前面那封为Go命名的邮件发送时，憧憬能有有五十万gopher的想法听起来会感觉很荒唐。 但就在此时此刻这里，我们不仅有了50w gopher，并且数量还在持续增长。

说到gophers，很高兴看到来自[Renee French](http://reneefrench.io/)想法的吉祥物Go Gopher(地鼠)，不仅成为了一个非常受人喜爱的作品，而且也是世界各地Go程序员的象征。许多各个地区顶级的Go大会都被称为GopherCons，因为他们聚集了来自世界各地的gophers。

Gopher大会正在迅速发展。[第一次大会](https://www.youtube.com/playlist?list=PLE7tQUdRKcyb-k4TMNm2K59-sVlUJumw7)的举办只不过是三年前的事情，但今天在全世界各地有很多这样的Go大会。并且还有无数小的本地“[聚会(meetups)](https://www.meetup.com/topics/golang/)”。在任何某一天，世界上某个地方都会有不止一个gopher群体在进行有关Go的分享。

回顾过去十年的Go设计和开发，Go社区的发展是惊人的。会议和聚会的数量、长长的且不断增加的Go项目贡献者名单、大量用Go实现的开放源代码存储库、使用Go的公司数量等等，细思恐(吃惊)极！

对于我们三个人，Robert, Rob和Ken，当初只是想让我们的编程生活更轻松一些，而如今，我们难以置信地、欣慰地看到我们的工作已经开始起作用了。

未来十年会带来什么呢？

*- Rob Pike, with Robert Griesemer and Ken Thompson*

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论