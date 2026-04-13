---
title: 计算重现性：一些挑战
url: https://tonybai.com/2019/11/19/computational-reproducibility-some-challenges/
published: '2019-11-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 计算重现性：一些挑战

近期，有人对科学结果的[可重现性](https://www.nature.com/collections/prbfkwmwvz)进行了讨论，并得出了一些让人沮丧的结论。[一项研究表明](https://www.insidehighered.com/news/2018/08/30/study-raises-new-questions-about-reproducibility-research)：这种可重现性只有62％。

在某些领域，情况可能更糟。任何依赖于计算的结果都面临着其编程环境不断变化的巨大风险：十年前编写的程序如果没有更改，今天构建成功的机会几乎微乎其微，更不用说运行或正确运行了。

这种担忧并不普遍，但正在增长。一个标志就是** 十年重现性挑战**的创建，该挑战要求研究人员重新运行他们的旧代码（十年或以上，按计算标准非常旧的代码），并查看它是否仍然有效。

**您还能找到你的旧代码吗？** 这本身就是一个挑战。

我们鼓励任何对计算有兴趣的研究人员接受挑战。上面的链接包含了有关此次挑战活动如何进行的详细信息。结果肯定令人大开眼界。即使您不提交结果，该练习也很有价值。

尽管人们都希望结果不要像某些人所预期的那样令人沮丧，但也很少有人会期望获得令人满意的结果。值得花点时间考虑一下为什么计算可重现性是一个问题。计算方法(Computational method)会随着系统，语言，库，方法甚至部署技术的不断变化而偏离。某些更改是必要的，因为这样可以解决库设计不佳导致的安全问题。某些功能确实可以实现，例如转向网络服务器；但是很多改变可以归结为改变本身，也就是“进步”。

本周是2009年11月10日宣布Go编程语言为开源项目的[10周年纪念日](https://tonybai.com/2019/11/09/go-opensource-10-years/)，因此在本周初我就想到了这个话题。但也许更重要的日期是2012年3月28日，因为那是Go版本1.0宣布的日子。

Go 1.0如此重要的原因在于，它带来了一个[承诺](https://golang.org/doc/go1compat)，即用户的程序在不确定的将来无需任何修改便可以继续进行编译和运行。从变革考虑，这一承诺恰是反对变革的坚不可摧的堡垒。 Go 1.0远非完美无缺-许多事情本来可以做得更好，其中包括我们当时甚至还不满意的一些事情-但对稳定的承诺远远弥补了此类不足。

为什么没有更多的计算项目像Go做出这样的保证？特别是编程语言？尽管没有Go程序可以参加十年挑战赛，但是如果参与七年挑战赛，与其他大多数语言相比，Go程序获得成功的机会要高得多。

这不仅涉及承诺的兼容性，你还必须交付它。曾经有无数次提议对Go进行更改的建议可以很容易被接受，但是最终因会破坏现有程序，或者至少有这样做的可能而导致被拒绝。真正兼容性的保护墙是有约束力的，但它也有机会做一些事情。它促进了Go生态系统的发展，使社区得以繁荣发展，有助于确保可移植性，并且将许多程序的维护开销降低到几乎为零。

随着对[Go 2.0](https://blog.golang.org/go2-here-we-come)的努力不断发展，兼容性前景依然存在。它实在是太重要了以致于我们不能屈服，尤其是考虑到其到目前为止已经取得的进展。

[语义版本控制（semver）](https://semver.org/)有帮助，但这还不够。必须将其部署在所有内容，包括的工具中，并严格遵守其兼容性属性。

所以这是我自己的十年挑战：找出一些已有十年历史的代码，如果可以的话，立即尝试运行。做任何必要的使其重新构建并运行。如果很容易就做到，那就太好了。如果不是，请反思存在的困难，造成这些困难的变化以及这些变化是否值得。他们能得到更好的管理吗？

系统和语言设计师面临的更大挑战：帮您的用户，并编纂您的兼容性规则。您可能不愿像Go开发人员那样僵化，但是您应该让您的社区清楚您提供的保证并兑现他们的保证。

如果您愿意，也许十年后，我们可以再次进行此练习，并获得更好的结果。

本文翻译自Rob Pike的文章：[“Computational reproducibility: Some challenges”](https://commandcenter.blogspot.com/2019/11/computational-reproducibility-some.html)。

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

## 评论