---
title: 谁才是 Go 生态的“幕后之王”？—— 深度挖掘 4000 万个节点后的惊人发现
url: https://tonybai.com/2026/01/09/the-most-popular-go-dependency-is/
published: '2026-01-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 谁才是 Go 生态的“幕后之王”？—— 深度挖掘 4000 万个节点后的惊人发现

![](../../assets/d13f4515975019c3.png)


[本文永久链接](https://tonybai.com/2026/01/09/the-most-popular-go-dependency-is) – https://tonybai.com/2026/01/09/the-most-popular-go-dependency-is

大家好，我是Tony Bai。

在 Go 的世界里，我们每天都在引入各种 import。但你是否想过，整个 Go 生态系统中，究竟哪个包是被依赖次数最多的“基石”？

通常，我们会参考 GitHub Stars 或 Awesome 列表，但这往往带有主观偏差。为了寻找最客观的答案，[开发者 Thibaut Rousseau 做了一件疯狂的事](https://blog.thibaut-rousseau.com/blog/the-most-popular-go-dependency-is/)：**他下载了 Go Proxy 自 2019 年以来的所有模块元数据，构建了一个包含 4000 万个节点、4 亿条关系的巨大图谱。**

结果令人大开眼界。

![img{512x368}](../../assets/04582461cface270.png)


## 从“愚公移山”到“巧用代理”

Thibaut 最初的想法很直接：从一个种子项目列表开始，递归地克隆仓库、解析 go.mod。但他很快发现这条路行不通——克隆速度太慢，且严重依赖 GitHub。

于是，他将目光转向了 **Go Modules 生态系统的核心枢纽 —— Go Proxy**。

- index.golang.org：提供了自 2019 年以来所有发布模块的时间流。
- proxy.golang.org：提供了每个模块版本的 go.mod 文件。

通过这两个公开 API，他成功地将整个 Go 生态的元数据“搬”到了本地，构建了一个全量的、不可变的本地缓存。

## Neo4j：点亮数据之网

面对海量的依赖关系，传统的关系型数据库显得力不从心。Thibaut 选择了图数据库 **Neo4j**。

**节点 (Node)**：代表一个具体的 Go 模块版本（例如 github.com/gin-gonic/gin@v1.9.0）。**关系 (Relationship)**：代表 DEPENDS_ON（依赖于）。

通过简单的 [Cypher 查询语句](https://neo4j.com/docs/cypher-manual/current/introduction/)，复杂的依赖链变得清晰可见。例如，查询一个模块的所有**传递性依赖**（Transitive Dependencies），在 SQL 中可能需要复杂的递归 CTE，而在 Neo4j 中只需一个简单的 *1.. 语法即可搞定。

## 数据揭秘：Go 生态的真实面貌

经过数天的处理和导入，这个庞大的图谱终于呈现在眼前。让我们看看数据告诉了我们什么：

### 1. 绝对的王者：testify

在“被直接依赖次数”的榜单上，github.com/stretchr/testify 以 **259,237** 次的惊人数量遥遥领先，是第二名的两倍还多。这再次印证了测试在 Go 社区中的核心地位。

紧随其后的是：

- github.com/google/uuid (10w+)
- golang.org/x/crypto (10w+)
- google.golang.org/grpc (9.7w+)
- github.com/spf13/cobra (9.3w+)
- … …

![](../BlogImages/2026/the-most-popular-go-dependency-is-2.png)


### 2. “已归档”库的生命力：pkg/errors

最令人玩味的数据来自 github.com/pkg/errors。尽管这个库多年前就已宣布“归档”（Archived）并停止维护，且 Go 1.13 已内置了类似的错误包装功能，但数据却显示了截然相反的趋势：

- 它的使用量不降反升！
- 2019 年仅有 3 个依赖它的模块，而到了 2025 年，这个数字飙升到了
**16,001**。

这揭示了软件生态中一个残酷的现实：**旧习惯难改，且“足够好”的库拥有极其顽强的生命力。** 哪怕官方已经提供了替代方案，开发者们依然倾向于使用他们熟悉的工具。

## 小结

Thibaut 的这个项目不仅仅是一次有趣的数据分析，它为我们观察 Go 生态提供了一个全新的上帝视角。

**平均依赖数**：Go 模块平均拥有**10**个直接依赖。**数据开源**：作者不仅开源了爬虫代码 github.com/Thiht/go-stats，还大方地通过 BitTorrent 分享了**11GB**的 Neo4j 数据库转储文件。

你可以下载这份数据，自己在本地运行 Neo4j，去挖掘更多有趣的洞见。比如，看看你最喜欢的某个小众库，究竟被谁在使用？或者，去探索一下 Go 生态中那些隐秘的“单点故障”？

在这个由 4000 万个节点构成的宇宙中，还有无数的秘密等待被发现。

资料链接：https://blog.thibaut-rousseau.com/blog/the-most-popular-go-dependency-is/

**你的依赖清单**

testify 的霸榜并不意外，但 pkg/errors 的顽强生命力确实让人深思。**在你的 go.mod 中，是否也有那些“虽然已归档，但真的很好用”的库？或者，你有什么私藏的冷门好库推荐？**

**欢迎在评论区晒出你的“宝藏依赖”！** 让我们一起发现更多 Go 生态的秘密。

**如果这篇文章让你对 Go 生态有了全新的认识，别忘了点个【赞】和【在看】，并转发给你的 Gopher 朋友！**

还在为“复制粘贴喂AI”而烦恼？我的新专栏 **《 AI原生开发工作流实战》** 将带你：

- 告别低效，重塑开发范式
- 驾驭AI Agent(Claude Code)，实现工作流自动化
- 从“AI使用者”进化为规范驱动开发的“工作流指挥家”

扫描下方二维码，开启你的AI原生开发之旅。

![](../../assets/305ffd23f32ce780.png)


你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2026, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论