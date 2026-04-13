---
title: GopherChina讲师专访
url: https://tonybai.com/2017/04/06/an-interview-with-me-as-a-lecturer-of-gopherchina-2017/
published: '2017-04-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# GopherChina讲师专访

今年有幸收到[GopherChina大会](http://www.gopherchina.org/)的组织者、[beego开源项目](https://beego.me/)的owner、《[Go Web编程](https://book.douban.com/subject/24316255/)》的作者[谢孟军](http://weibo.com/533452688)童鞋的邀请，以讲师身份参加今年的GopherChina大会。下面是GopherChina对我这个讲师的专访稿^0^。该专访稿将同时被发布在公众号“Go中国(微信号：golangchina)”上面，可点击[这里](https://mp.weixin.qq.com/s?__biz=MjM5OTcxMzE0MQ==&mid=2653369932&idx=1&sn=2b89c8253c759714db5dc4fccb96c6e6&chksm=bce4d6568b935f4068e2456429ca37a257ff24237533b718fc64cd445be98452757693ada141&mpshare=1&scene=1&srcid=0405G8XuCfBVfkPTz2skitFO&key=880a8f11cadd9c38c88dbfeaa37bee078b8460ae535cbcb5940e7e73f779bfb674d9e70c633715041ee796cba46e4386a598cab68296084cf1d1965ad31b7ff5c442b390931511a054b34f7dff127979&ascene=0&uin=MTYwMzM0NjYyMQ%3D%3D&devicetype=iMac+MacBookAir6%2C2+OSX+OSX+10.9.2+build(13C64)&version=11020201&pass_ticket=ubemadJo5Ju2NkXnKepVV1ToSJYfkOGXgXuETKrjwLLow4B4h2Ufk0enGSRNk9cn)阅读。

#### 1、首先介绍一下自己。

大家好！我叫白明（Tony Bai），目前是东软云科技的一名架构师，专职于服务端开发，日常工作主要使用Go语言。我算是国内较早接触Go语言的程序员兼Advocater了，平时在我的[博客](http://tonybai.com)、[微博](http://weibo.com/bigwhite20xx/)和微信公众号“iamtonybai”上经常发表一些关于Go语言的文章和Go生态圈内的信息。

在接触Go之前，我主要使用[C语言](http://tonybai.com/tag/c)开发电信领域的一些后端服务系统，拥有多年的电信领域产品研发和技术管理经验。我个人比较喜换钻研和分享技术，是《[七周七语言](http://tonybai.com/2012/05/08/translate-seven-languages-in-seven-weeks/)》一书的译者之一，并且坚持写[技术博客](http://tonybai.com/)十余年。同时我也算是一个开源爱好者，也在[github](https://github.com/bigwhite)上分享过自己开发的几个小工具。

目前的主要研究领域包括：[Go](http://tonybai.com/tag/go)、[Kubernetes](http://tonybai.com/tag/kubernetes)、[Docker](http://tonybai.com/tag/docker)和儿童编程教育等。

#### 2、回忆一下与Golang的渊源。是什么原因决定尝试Golang？自己用Go语言实现的第一个项目是什么？当时 Golang 有什么令人惊喜的表现，又有什么样的小不足，这个不足在Golang已经更新到1.8版本的时候是否已经得到改善？

众所周知，Go语言最初由[Robert Griesemer](https://github.com/griesemer), [Ken Thompson](https://en.wikipedia.org/wiki/Ken_Thompson)和[Rob Pike](https://github.com/robpike)在2007年末共同设计和实现，2009年11月份正式发布并开源，并于2012年3月份[发布了1.0版本](https://blog.golang.org/go-version-1-is-released)以及[Go1规范](https://golang.org/ref/spec)。我就是在2012年开始接触Go的，那是缘于看到一份由Rob Pike主讲的3-day [Go Course资料](http://tonybai.com/2012/08/23/the-go-programming-language-tutorial-part1/)。从那份资料里，我了解到了Go的设计理念和Go语法。

由于之前浸淫于C语言多年，深知C语言在系统编程以及服务端编程方面的强大，同时也亲身体会到C的语法“陷阱”和C手工内存管理给开发者带来的苦恼。虽然那些年市面上也有其他主流语言可供选择，但在我看来，它们给我带来的心智负担太过沉重，比如：[C++](http://tonybai.com/2004/11/09/cpp-advanced-training-part1)“宇宙无敌”的学习和使用复杂性、[Java](http://tonybai.com/tag/java)超大的资源消耗和庞大且纷繁芜杂的框架体系、动态语言（[ruby](http://tonybai.com/2005/01/05/learn-ruby)、[python](http://tonybai.com/tag/python)）无静态类型而导致运行时crash时调试的困难、函数式语言（如[Haskell](http://tonybai.com/tag/haskell)、[clisp](https://tonybai.com/tonybai.com/2011/06/21/hello-common-lisp)）的过于小众和非主流。显然它们都不是我的菜。直到Go的出现，C程序员出身的我一下子就被这门新语言迷住了。

现在想起这件事来，我当时迷上Go应该主要由于以下几点原因：

```
* 静态类型语言、接近于C的性能(对于C程序员来说，这算是某种天然继承性)
* 简洁的语法
* 内置的并发支持
* GC
* 贯穿整个语言的正交设计和组合编程思路（兼容对OO的支持）
* 工具和功能全面的标准库
```


而且这几点也是这几年持续支撑我深入学习和使用Go语言的原因。

不过由于Go1刚出来时也十分小众，并且各方面功能还在完善中，我并没有在真实项目中使用Go，这种状况一直持续到2014年末。直到那时，我才在一个小项目中使用Go实现了一个微信公众号的协议接口。当时发现：使用Go实现一些安全协议真是非常方便，因为标准库里内置了很好的支持，比如：各种aes、sha256、tls算法实现。同时，Go内置的testing framework、gofmt、Go pprof工具的表现也是让我感觉用起来十分舒服。

如果非要说当时有什么不足之处的话，那只能是Go对debugging的支持明显不足。即便是到了目前最新的[Go 1.8版本](http://tonybai.com/2017/02/03/some-changes-in-go-1-8/)，Go在debugging方面虽然有所改善，但和C这样的传统语言来说依然有很大差距。不过好在我们有“print”这个无敌调试武器，Go的这个不足对我影响微乎甚微^0^。

当然随着Go在更多规模稍大项目的使用，Go的包管理问题逐渐浮出水面，这也是整个Go社区都想改进的事情。好在目前已经有了专门的Commitee来做这件事，最新的[roadmap](https://github.com/golang/dep/wiki/Roadmap)显示[dep工具](https://github.com/golang/dep)将在Go 1.10 dev cycle并入Go tools中。

#### 3、2009年诞生至今，Go语言基本统治了云计算，作为最专业的Go语言专家，您认为这是由于它的哪些优雅的特性？Golang未来还会有什么样的改进和突破？

“作为最专业的Go语言专家”，这一称号的确不敢当。我觉得我个人只是国内Gopher普通一员，能为Go语言在国内的发展做点事情就很高兴了^0^。

Go自从[1.5版本自举](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)后，随着ssa优化、GC延迟优化的深入，Go在国内外的使用趋势确实是一片大好，尤其是Go问鼎2016年TIOBE编程语言排行榜的年度语言，让更多的程序员知道Go语言、了解Go语言和使用Go语言。在云计算成为当今IT行业常态的今天，Go在这方面已然成为一个重量级选手。从个人对Go的情感角度出发，我个人是希望Go语言能成为”21世纪的C语言”和云平台第一语言的。不过这是一个过程，需要时间，还需要依靠全世界Gopher和Go Community的共同努力才能实现的。

时代不同，语言的成长环境也有所不同。和上一代和两代的语言似乎有所不同，新一代编程语言是否能进入程序员们的法眼，是否值得程序员去投资，“背景”很重要，即所谓的[编程语言也进入了“拼爹”时代](http://tonybai.com/2012/10/08/the-new-age-of-programming-language/)。Go语言背靠Google这棵大树，又有Robert Griesemer, Ken Thompson, Rob Pike三巨头坐镇，是真正的“牛二代”，它自然就会得到不少程序员的青睐。我想这是Go吸引眼球的场外因素。

至于Go本身的语言特性，在上一个问题中，我已经做了初步阐述了，这里再补充几点：

```
* Go是一门以解决Google内部生产环境中的问题（大规模并发服务）为目标的、兼顾在语言设计层面解决一些软件工程问题的面向大规模并发服务的编程语言；
* 开发效率较高(对比主流的C、C++和Java)，且执行效率与C相比，没有数量级级别的差异；
* 编译速度超快（相对其他需编译的主流语言），无需喝咖啡等待；
* Go1兼容性的承诺。
```


Go语言到目前已经演进到1.8版本，Go 1.9开发周期已经打开。今年夏天，Go 1.9发布后，Go似乎就到了版本演进的关键节点，是继续Go1兼容（Go 1.10、Go 1.11…），还是诞生Go2规范，目前并没有明确信息。不过未来的改进和突破，我觉得还是应该建立在Go语言设计的初衷和设计原则之上，这些初衷和原则包括：

```
目标：
* 高效的静态编译语言
* 动态语言的易用性
* 类型安全和内存安全
* 对并发和通信的良好支持
* 高效、低/趋于零延迟的GC
* 高速编译
原则：
* 保持概念正交
* 保持语法简单
* 保持类型系统精炼，无type hierarchy
```


从这些年Go的发展来看，基本都是遵循以上目标和原则的。即便Go2出来，不符合上述原则的feature，也是很难加入到Go2里面的。

#### 4、之前是否有关注到Gopher China大会，对大会的风格和内容有什么样的印象？

对于中国大陆地区规模最大，最具影响力的Go大会，我是从第一届就开始关注了，虽然第一届因故没能参加^0^。在去年举行的第二届大会，我是作为早鸟观众参与的哦。而本届则有幸成为讲师。

GopherChina从诞生至今，规模日益扩大，据说今年的参会人员可能突破1000人。而且GopherChina大会从第一届就汇聚了国内一线IT厂商的精英技术人员作为讲师，并得到了Go core team的大力支持。在每一届大会都会邀请到Go team中的核心开发人员参会布道，甚至在第一届大会时还邀请到了Go三巨头之一的Robert Griesemer，极大满足了国内Gopher的求知欲。

而且就我观察，每一届GopherChina大会的主题都涵盖：语言、工程、新兴领域应用等多个环节，颇具多样性和全面性。

#### 5、作为讲师也是参会者，对于今年的Gopher China大会的哪些议题有所期待？

GopherChina每一届都是高手云集，这届也不例外。今年大会的每个议题都令我很是期待。

#### 6、现在很多企业项目都在准备转Go，对于这些项目的负责人有没有建议和经验分享？

Go语言以极易上手著称，同时Go也是一门十分简单的语言（相对于其他主流语言），C、Cpp、Java、Python等程序员转型到Go的曲线并不陡峭，因此团队整体转型为Go的门槛并不高。但还是要有几点是项目负责人需要认真考虑的：

##### (1) 确认Go适合项目的应用场景

Go不是万能的，不能为了用Go而去用Go。但Go从最初定位为一门系统语言(Sytem Programming Language)逐渐演化成为一门通用语言(General Purpose Programming Language)，说明其适应性和应用范围已经十分广泛，目前在云计算、Web开发、大数据、游戏、数据库、IDE、容器等领域均有大规模应用案例。但即便这样，仍然在有些领域的应用需要谨慎，比如嵌入式领域、比如mobile开发，虽然在这两个方面Go都做出了很大的努力，但似乎并没有较大的突破。

##### (2) 以终为始，从开始就参考Go的最佳实践

Go经过若干年的演化发展，逐渐形成了一些最佳实践，包括：项目代码组织、命名、惯用法、测试方法、错误处理、接口使用等。建议多看官方的talks、blog和世界范围内Go大会的presentation video。

##### (3) 单元测试全程保障

Go内置了单元测试框架，而单元测试是检验代码设计好坏的基础，也是代码重构的先决条件。建议项目从始至终都要优先考虑对代码编写测试代码。

##### (4) 充分利用标准库

在Go的应用实践中，你会发现Go标准库已经为你提供了大部分你要使用的功能。甚至有一些极端的Go纯粹主义者只愿意标准库中的函数和方法。Go标准库凝聚了Go team以及相关Contributor的Go代码精华，其稳定性绝对值得信赖。充分和广泛利用标准库也便于项目代码组织、构建和迁移。

##### (5) 基于go tool建立代码metric视图

对于那些性能敏感的系统，建议在内部环境基于go tool建立起代码的metric视图，监控代码变化给系统性能等带来的影响，利于问题诊断。

** 最后，请及时反馈Go语言自身问题，你的反馈是Go语言演化的动力**。

#### 7、有没有你觉得很酷的Gopher？可以回答自己哟～

在github.com/golang/go上，我经常关注[Russ Cox](https://github.com/rsc)的代码。众所周知，[Russ Cox](https://swtch.com/~rsc/)是Go核心代码提交次数最多的member，他也除三巨头之外，对Go演化影响着最大的人之一。从近两年的Go team开发活动来看，Russ Cox开发效率很高，并且提出的[proposal](https://github.com/golang/proposal/blob/master/design/12914-monotonic.md)思维之缜密和全面令人叹服。

[Dave Cheney](https://dave.cheney.net/)是另一个我经常关注的Gopher，他也是[第二届GopherChina大会](http://tonybai.com/2016/04/18/my-experience-of-gopherchina2016/)的受邀讲师。他不遗余力的“鼓吹”Go，并从Go 1.6版本开始，发起了[Go Global release party](https://github.com/golang/go/wiki/Go-1.8-Release-Party) ，成为Go Community又一个节日。他不仅是Go community中的意见领袖，同时也为Go社区贡献不少有用的工具和思想，包括：[gb](https://getgb.io)、[errors](https://github.com/pkg/errors)等。

Dmitry Vyukov，前Intel Black Belt级工程师，现Google员工，虽然他不是专职Go team的人，但他却是Go scheduler当前版本的核心实现者。虽然近两年似乎在golang的投入并不是那么多，但依然成果丰硕，[Go Execution Tracer](https://talks.golang.org/2015/dynamic-tools.slide)、[go-fuzz](https://github.com/dvyukov/go-fuzz)(据说要加入go核心)都是他的杰作。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

支持，只有支持才是访问博客的正确方式！

谢谢:)

世事无常，但这个博客定能永保辉煌！

厉害啊~