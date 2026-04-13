---
title: 一文告诉你如何帮助测试Go语言Beta公测版或RC候选发布版
url: https://tonybai.com/2021/08/11/how-to-test-go-beta-or-rc/
published: '2021-08-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一文告诉你如何帮助测试Go语言Beta公测版或RC候选发布版

![](../../assets/67d87a5ce042f467.png)


[本文永久链接](https://tonybai.com/2021/08/11/how-to-test-go-beta-or-rc) – https://tonybai.com/2021/08/11/how-to-test-go-beta-or-rc

Go 1.17已经发布到[RC2版本](https://golang.google.cn/dl/go1.17rc2.linux-amd64.tar.gz)！正式版最早将在8月中旬发布，最迟也不会晚于月底。对于喜欢尝鲜的Gopher而言，在体验Go 1.17的新特性的同时，也不要忘了为Go语言项目做做贡献！贡献什么呢？其实很简单，就是在尝鲜的同时，对Go语言的Beta公测版以及RC发布候选版进行测试，并把遇到的问题提交到[Go语言项目官方issue列表](https://github.com/golang/go/issues)中去。

那么如何对Go语言的Beta公测版或RC发布候选版进行测试呢？别急，这就是本文要告诉你的内容。

本文翻译自Go语言项目“编外”核心开发者、现Tailscale工程师[Josh Bleecher Snyder](https://github.com/josharian)的文章[《How to test a Go beta or RC》](https://commaok.xyz/post/test-beta/)。

在[Go发布周期](https://github.com/golang/go/wiki/Go-Release-Cycle)的这个时间阶段，[Go团队希望全世界的Go开发者们帮助测试Go的Beta公测版和RC发布候选版](https://groups.google.com/forum/#!forum/golang-announce)。

请帮忙吧! 这很简单，很快速，也很重要。

这是一篇关于如何测试(Beta和RC)，测试什么，以及为什么测试的文章。

### 1. 安装

预发布版(pre-releases)可以用go get下载。例如：

```
$ go install golang.org/dl/go1.17beta1@latest
$ go1.17beta1 download
$ go1.17beta1 test your/favorite/package
```


完整的预发布版本列表可在https://pkg.go.dev/golang.org/dl页面查看。

### 2. Beta公测版

Beta公测版是对新版本的早期观察。它们有时会有已知的错误。严重的错误是不常见的，但也不是没有。新的API可能仍然会因反馈而改变。你不应该在生产中使用Beta版。

以下是你在处理Go Beta版时应该做的事情，我们按简单快速到相当复杂进行排序。即使您只做了第一项或第二项，也是很有帮助的!

- 在本地运行你的测试。调查并
[报告任何新的故障](https://golang.org/issue/new)。 - 阅读
[版本发布说明](https://tip.golang.org/doc/go1.17)。如果你看到任何有关该版本的异常情况，请[提交一个issue](https://golang.org/issue/new)来讨论。 - 在本地运行你的基准测试。调查并报告性能退步情况。
- 如果你有一个暂存服务器，CI，或者任何你可以运行更多测试的地方，请在那里使用预发布版本，并提交你遇到的任何问题。
- 查看
[API的差异](https://github.com/golang/go/blob/master/api/go1.17.txt)。如果你看到任何有关的问题，请提交一个issue来讨论。

### 3. 发布候选版本(Release candidiates, RC)

候选版本通常没有已知的严重bug。(Google在他们的真实服务器上测试候选版本。) API应该是稳定的。

处理Go RC版本的事情和处理beta版本的事情是一样的。只是如果你有足够的带宽和手段，你可能想尝试在生产中运行它，在一个小的服务器子集上。

### 4. 我没有那么多时间

有一到两个Beta版和一到两个RC版的情况并不罕见。那将需要大量的测试。如果你只有少量的时间来帮助Go实现无错误的发布，那该怎么办？

如果你只能做一件事，**用第一个beta版在本地运行你的测试**。这只需要几分钟的时间。错误越早被发现，它们就越有可能被修复，而且修复得很好。

如果你能多做一点，**请尽早阅读 版本发布说明**。无论如何，你都可能会在发布时阅读它们。通过提早阅读，你仍然有机会修复你看到的任何问题。

### 5. 为什么要测试Beta版和RC版？

编程语言，以及它们的工具和社区，是一种复杂的存在。人们以奇妙的、不寻常的方式使用它们。而编程语言也是软件，你知道这意味着什么。尽管Go的贡献者们尽了最大的努力，Go问题追踪器中还是有不少沮丧的程序员，他们发现新版本对他们不适用时已经太晚了：一个微妙的行为变化，一个罕见的性能退步，一个不太合适的API设计。

一旦版本发布，修复这些问题就变得更加困难，有时甚至不可能。安全问题会得到及时的修复，但其他问题，即使是关键性的bug，也会在一个月后的下一个版本中才会得到修复。非关键性的bug要到下一个Go大版本才会被修复，最早也要6个月后。而且在很多情况下，由于[Go 1的兼容性承诺](https://tip.golang.org/doc/go1compat)，我们可能会被永远困在这个问题上。

Beta版和RC是我们Go社区发现问题的唯一的机会，我们还有时间去真正解决它们。

### 6. 奖励

考虑将Go的”tip”版本添加到你的CI中吧。这对尽早发现问题特别有帮助，但它确实增加了相当多的工作。在提交问题之前，你需要检查[Go官方构建仪表板](https://build.golang.org/)并进行一些调查，以确定发现的问题是否值得报告。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


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