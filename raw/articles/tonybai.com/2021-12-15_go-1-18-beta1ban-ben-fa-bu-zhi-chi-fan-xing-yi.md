---
title: Go 1.18 Beta1版本发布，支持泛型[译]
url: https://tonybai.com/2021/12/15/go-1-18-beta1/
published: '2021-12-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.18 Beta1版本发布，支持泛型[译]

![](../../assets/8888557ddf5446e6.png)


[本文永久链接](https://tonybai.com/2021/12/15/go-1-18-beta1) – https://tonybai.com/2021/12/15/go-1-18-beta1

北京时间今天凌晨，美国时间12月14日，Go核心团队技术负责人Russ Cox在Go官博发表文章[《Go 1.18 Beta 1 is available, with generics》](https://go.dev/blog/go1.18beta1)，正式宣布Go 1.18的第一个预览版Go 1.18 beta1发布！Go团队这次少见的通过官博来发布一个beta版本，足以证明Go团队对Go 1.18版本的重视，毕竟Go 1.18是[Go自诞生以来](https://time.geekbang.org/column/article/426265)最大的一次语法变动，Go团队希望Go社区的gopher们广泛参与公测，在Go 1.18版本发布之前尽可能多地找出版本中存在的bug。

这里简单翻译一下这篇官博，正文如下。

我们刚刚发布了Go 1.18 Beta 1，你可以通过访问[下载页面](https://go.dev/dl/#go1.18beta1)获得该版本。

Go 1.18的正式发布还需要几个月的时间。这是Go 1.18的第一个预览版，目的是让你试一试，用一用，并让我们知道你遇到了什么问题。Go 1.18 Beta 1代表了Google的整个Go团队和世界各地的Go贡献者的大量工作，我们很高兴听到你的想法。

Go 1.18 Beta 1是第一个预览版，包含Go对[使用参数化类型(parameterized type)的泛型代码](https://go.dev/blog/why-generics)的新支持。泛型是Go 1发布以来最重要的变化，当然也是我们有史以来最大的单一语言变化。对于引入这类影响较大的新特性，期待新用户发现新的错误是很常见的，泛型特性也不例外；我们一定要以适当的谨慎态度对待它们。另外，某些微妙的情况，例如特定种类的递归泛型，已经被推迟到未来的版本。也就是说，我们知道一些早期采用者已经相当满意，如果你有你认为特别适合泛型的用例，我们希望你能试一试。我们已经发布了一个[关于如何开始使用泛型的简短教程](https://go.dev/doc/tutorial/generics)，并在上周的[GopherCon上做了一个演讲](https://www.youtube.com/watch?v=35eIxI_n5ZM&t=1755s)。你甚至可以[在Go开发分支模式下的Go playground上尝试泛型](https://go.dev/play/?v=gotip)。

Go 1.18 Beta1 增加了[对编写基于模糊测试的内置支持](https://tonybai.com/2021/12/01/first-class-fuzzing-in-go-1-18)，以自动查找导致程序崩溃或返回无效答案的输入。

Go 1.18 Beta1增加了一个新的[“Go工作区模式”](https://tonybai.com/2021/11/12/go-workspace-mode-in-go-1-18)，让你可以同时处理多个Go module，这对大型项目来说是一个重要的使用案例。

Go 1.18 Beta 1包含一个扩展的go version -m命令，它现在可以记录编译器flag等构建细节。程序可以使用[debug.ReadBuildInfo](https://pkg.go.dev/runtime/debug@master#BuildInfo)查询自己的构建细节，现在也可以使用新的[debug/buildinfo包](https://pkg.go.dev/debug/buildinfo@master)从其他二进制文件读取构建细节。这一功能旨在为任何需要为Go二进制文件制作软件材料清单（SBOM）的工具奠定基础。

今年早些时候，[Go 1.17](https://tonybai.com/2021/08/17/some-changes-in-go-1-17)增加了一个新的[基于寄存器的调用约定](https://tonybai.com/2021/08/20/using-register-based-calling-convention-in-go-1-17/)，以加快X86-64系统上的Go代码。Go 1.18 Beta1将这一功能扩展到了ARM64和PPC64，使其速度提高了20%之多。

感谢所有为这个测试版做出贡献的人，特别是感谢谷歌的团队，他们多年来一直在为实现泛型而不懈努力。这是一条漫长的道路，我们对结果非常满意，我们希望你也喜欢它。

更多细节请参见[Go 1.18的完整发布说明草案](https://tip.golang.org/doc/go1.18)。

像往常一样，特别是对于测试版，如果你发现任何问题，[请提交一个问题](https://go.dev/issue/new)。

我们希望你喜欢测试这个测试版，并希望你在2021年的剩余时间里都有一个安逸的生活。节日快乐!

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强，欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论