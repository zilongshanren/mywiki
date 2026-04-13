---
title: Go，5周年
url: https://tonybai.com/2014/11/12/go-5-years/
published: '2014-11-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go，5周年

2014年11月10日（美国当地时间），[Golang](http://tonybai.com/tag/golang)的[官方博客](http://blog.golang.org) 放出了Andrew Gerrand的一篇博文《[Half a decade with Go](http://blog.golang.org/5years)》来纪念Go语言发布五周年。文章按时间顺序简要描述了Golang这五年来发展的 点点滴滴，并让全世界Gopher看到了Go可期的光明未来。考虑到这篇文章在墙外，不便于国内Gopher阅读，这里给出中文翻译版，希望能给中国大陆 的Gophers带来些帮助！

五年前，我们启动了Go语言项目。我们准备发布第一版时的一幕仿佛就发生在昨天似的：我们的官方站点用的是一种可爱的黄色色调，我们将Go语言称为一门 “系统编程语言”，你需要使用分号作为语句结束标志，使用Makefile来构建你的代码。我们不知道Go语言是否能被大家接受。人们会分享我们的目标和 愿景吗？人们会发现Go语言有用吗？

![](../../assets/1dbad5354f6cd54b.png)


起初，我们的发布引起了一阵关注。Google发布了一门新的编程语言，每个人都渴望探究它一番。一些程序员因为Go相对保守的功能特性集合而选择了放 弃，Go给他们的第一印象就是：没有什么新鲜玩意儿！但另外一小群程序员则看到了这个为软件工程师量身定做的生态系统的开端。这少数人将组成Go语言社区 的核心。

![](../../assets/1c49fbaef35b9c73.jpg)


第一版发布后，我们花了些时间向社区传达Go语言背后的目标和设计理念。Rob Pike在官方的《[Go at Google: Language Design in the Service of Software Engineering](http://talks.golang.org/2012/splash.article)》一文中对此进行了生动地表达，并 在其个人博客文章《[Less is exponentially more](http://commandcenter.blogspot.com.au/2012/06/less-is- exponentially-more.html)》中做了进一步的阐述。Andrew Gerrand的《[Code that grows with grace](http://vimeo.com/53221560)》(Slides在[这里](http://talks.golang.org/2012 /chat.slide))和《[Go for Gophers](https://www.youtube.com/watch?v=dKGmK_Z1Zl0)》(Slides在[这里](http://http: //talks.golang.org/2014/go4gophers.slide))对Go的设计哲学又给出了更有深度和技术性的说明。

随着时间的推移，积少成多。这个项目的转折点出现在2012年3月Go 1发布时。Go 1为程序员们提供了可以信赖的稳定的语言和标准库。到2014年，Go项目拥有了上百的核心贡献者，其生态圈中拥有了数不尽的[第三方库和工具](https://godoc.org/) ，并由成千上万的开发者维护着。正在发展壮大的社区拥有许多极具热情的成员（或者就如我们所称呼 的：Gophers）。今天，就我们目前的统计分析，Go社区的成长速度远远超出了我们的预期。

Gophers们在哪里可以得到这些呢？全世界目前有很多有关Go语言的“大事”发生。今年我们看到了几个专门的Go技术大会：在丹佛和巴黎举行的首次[ GopherCon](http://blog.golang.org/gophercon)和[dotGo](http://www.dotgo.eu/)大 会。FOSDEM的[Go DevRoom](http://blog.golang.org/fosdem14)以及在东京举行的一年两次的[GoCon](http://https: //github.com/GoCon/GoCon)。每次会上来自全球各地的Gophers们都踊跃地展示他们开发的Go项目。对于Go语言开发组来 说，我们很高兴能满足这些分享我们愿景和兴奋的程序员的需求。

在世界各地，还有数十个社区驱动运行的“Go用户组”。如果你还没有造访过你当地的用户组，可以考虑去尝试一下。如果你当地尚没有这类用户组，也许你可以考虑[发起一个](https://blog.golang.org/getthee-to-go-meetup)？

今天，Go在云端找到了用武之地。Go出现在了工业向云计算转型的时刻。并且我们兴奋地看到Go正在快速成为这个运动的一个重要组成部分。简单、高效、内 置并发原语和现代的标准库让Go语言尤其适合云端软件开发（毕竟它就是为此而设计的）。一些重量级的开源云项目，诸如Docker和Kubernetes 都是用Go语言实现的，一些运作基础设置的公司，诸如Google、CloudFlare、Canonical、Digital Ocean、Github、Heroku以及微软也都在使用Go语言开发一些重量级的项目。

那么将来会怎样呢？我们认为2015年将是Go语言大爆发的一年。

[Go 1.4](http://tonybai.com/2014/11/04/some-changes-in-go-1-4/)，除了其新增的[特性和bug修正](http://tip.golang.org/doc/go1.4)外，它为实现一个新的低延迟垃圾收集器以及支 持在移动终端上运行Go奠定了基础。 预计Go1.4将在2014年12月1日正式发布。我们期望在Go 1.5中能出现新GC的身影，Go 1.5预计在2015年6月1日发布，它将使Go适合更加广泛的应用开发。我们迫不及待的想看到哪些领域的开发者会接受它。

接下来会有更多的Go大事发生。11月15日，[GothamGo](http://gothamgo.com/)将在纽约如期举行。2014年1月31日到 2月1日，布鲁塞尔将举行另一次Go DevRoot at FOSDEM。2015年2月19日到21日，在印度班加罗尔将举行[GopherCon India](http://www.gophercon.in/)大会。最初的GopherCon将在2015年7月份回到丹佛。2015年11月 [dotGo](http://www.dotgo.eu/)大会将再次来到巴黎。

Go团队将向届时到场的所有gophers表示衷心的感谢。为Go语言的下一个五年！

为了庆祝Go诞生5周年，在未来的一个月里，[Gopher Academy](http://blog.gopheracademy.com/)将会发布一系列由知名Go users撰写的文章，务必要去看看哦。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

不错

想不想一起做Golang社区？ http://gopher-china.org 我在筹备中。 Github组织：https://github.com/Gopher-China 合伙一起搞？ 我QQ：517946367

golanghome.com 已经有了啊

我知道啊，然后呢？ 那只是一个go语言版的v2ex啊。能不能做得更好一些？

“`我们将Go语言称为一门 “系统编程语言”，你需要使用分号作为语句结束标志，使用Makefile来构建你的代码。“`应该是终结了写代码需要用分号结束一行和使用 Makefile 来编译的时代.

似乎不是这样吧。作者描述的时当初发布第一版go时的情形，当时go语言还需要分号结尾，用makefile编译，而不是像目前这样“先进”。

哦. 是的.