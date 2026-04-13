---
title: Go 1.18版本正式发布了
url: https://tonybai.com/2022/03/16/go-1-18-released/
published: '2022-03-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.18版本正式发布了

![](../../assets/2688857ef1ee7423.png)


[本文永久链接](https://tonybai.com/2022/03/16/go-1-18-released) – https://tonybai.com/2022/03/16/go-1-18-released

美国时间2022年3月15日，Go核心团队官宣了[Go 1.18版本正式版的发布](https://go.dev/blog/go1.18)！这是一个万众期待的版本，因为在这个版本中，Go核心团队做了Go语言开源以来的最大一次语法特性变更 – [增加了对泛型(generics)的支持](https://mp.weixin.qq.com/s/ur1eiZl4PKbF1PqELAdfKg)！下面是对[Go官博文章](https://go.dev/blog/go1.18)的全文翻译，供大家参考！

今天，Go团队很高兴地发布了Go 1.18，你可以通过访问[下载页面](https://go.dev/dl/)获得该版本。

![](../../assets/60fc510fa807388b.png)


Go 1.18是一个真正的大版本，包括新功能特性、性能改进和我们对语言的最大改变。可以说Go 1.18的部分设计始于十年前我们首次发布Go语言的那个时候也并不夸张。

### 泛型(Generics)

在Go 1.18版本中，我们引入了[对使用参数化类型的泛型代码的新支持](https://go.dev/blog/why-generics)。支持泛型是Go最常被要求添加的功能特性，我们很自豪能够提供大多数用户目前需要的泛型支持。随后的版本将继续为一些更复杂的泛型用例提供额外支持。我们鼓励你使用我们的[泛型教程](https://go.dev/doc/tutorial/generics)来了解这个新功能，并探索使用泛型来优化和简化你的代码的最佳方法。[Go 1.18版本发布说明](https://go.dev/doc/go1.18)中有关于在Go 1.18中使用泛型的更多细节。

### 模糊测试(Fuzzing)

伴随着Go 1.18版本的发布，Go成为第一个将[模糊测试(Fuzzing)](https://mp.weixin.qq.com/s/5qnIUz3plQG65FVnbPZVLw)完全集成到其标准工具链中的主要语言。与泛型一样，模糊测试的设计已经持续存在了很长时间，我们很高兴能在这个版本中与Go生态系统分享它。请查看我们的[模糊测试教程](https://go.dev/doc/tutorial/fuzz)，以帮助你开始使用这个新功能。

### 工作区(Workspaces)

今天，Go module几乎已被普遍接纳和采用，Go用户在我们的年度调查中报告了非常高的满意度分数。在我们2021年的用户调查中，用户反馈go module的最常见的挑战是跨多个module工作。在Go 1.18中，我们通过新的[Go工作区模式(Go workspace mode)](https://mp.weixin.qq.com/s/AGAz8dti8IwfVntOvBTUTg)解决了这一问题，这使得[在多个module中工作变得简单](https://go.dev/doc/tutorial/workspaces)。

### 20%的性能改进

苹果M1、ARM64和PowerPC64用户肯定会欢欣鼓舞! 由于[Go 1.17的寄存器ABI调用约定](https://mp.weixin.qq.com/s/AkJoXLlpSmw5vMZDpXoq5w)扩展到这些架构，Go 1.18的CPU性能提升幅度高达20%。为了强调这个版本的性能提升幅度，我们将**20%的性能改进**作为了第四个最重要的标题

关于1.18中的所有内容的更详细描述，请查阅[Go 1.18发布说明](https://go.dev/doc/go1.18)。

Go 1.18是整个Go社区的一个巨大的里程碑。我们要感谢每一位提交错误、发送修改、编写教程或以任何方式帮助Go 1.18成为现实的Go用户。没有你们，我们无法做到这一点。谢谢你们。

享受Go 1.18吧!

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/311cf32e055e496a.png)


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

刚从别的站看到了1.18发布，就想着，你应该更新了，没想到更新的真快。哈哈。

拼的就是手速，哈哈。

坐等1.18值得关注的几个变化

嗯嗯，会有的