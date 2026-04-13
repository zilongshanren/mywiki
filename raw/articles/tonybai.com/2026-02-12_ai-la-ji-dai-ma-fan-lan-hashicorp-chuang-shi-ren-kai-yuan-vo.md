---
title: AI 垃圾代码泛滥？HashiCorp 创始人开源 Vouch：重构开源信任机制
url: https://tonybai.com/2026/02/12/ai-garbage-code-hashicorp-founder-vouch-rebuilding-open-source-trust/
published: '2026-02-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# AI 垃圾代码泛滥？HashiCorp 创始人开源 Vouch：重构开源信任机制

![](../../assets/0009c77dfd9a5613.png)


[本文永久链接](https://tonybai.com/2026/02/12/ai-garbage-code-hashicorp-founder-vouch-rebuilding-open-source-trust) – https://tonybai.com/2026/02/12/ai-garbage-code-hashicorp-founder-vouch-rebuilding-open-source-trust

大家好，我是Tony Bai。

在生成式 AI 大模型以及AI Coding Agent（如Claude Code等）极大地降低了代码编写门槛的今天，开源维护者的防线正面临崩溃。当“看起来像样但毫无逻辑”的 AI 垃圾代码（AI Slop）充斥 PR 列表时，传统的“来者不拒”模式已不再适用。为此，HashiCorp 创始人 Mitchell Hashimoto 开源了新工具 [Vouch](https://github.com/mitchellh/vouch)，试图将开源治理从“验证代码”回归到“验证人”。

![](../../assets/04582461cface270.png)


## 开源治理的新危机：当贡献变得太容易

在过去二十年的开源黄金时代，社区奉行的是“信任但验证（Trust and Verify）”的原则。这一原则建立在一个隐含的前提上：**贡献代码是有成本的**。理解代码库、编写逻辑、提交 PR，这些努力本身就是一个自然的过滤器，筛掉了大多数低质量的贡献。

然而，2024 年以来的 AI 浪潮打破了这一平衡。

Mitchell 在 Vouch 的发布文档中直言不讳地指出：

“不幸的是，随着 AI 工具的出现，人们可以轻而易举地创建出

看起来合理但质量极低的贡献，而无需任何真正的理解。”

这种被称为 “AI Slop（AI 垃圾）” 的内容，正在消耗维护者宝贵的精力。维护者不再是在审核代码逻辑，而是在进行一场分辨“对方是不是人类”的图灵测试。

## Vouch 的解法：重构信任机制

面对危机，Mitchell 没有选择更复杂的自动化测试，而是选择了一种复古且激进的社会学解法——Vouch（担保）。

Vouch 的核心逻辑非常简单：如果要参与项目（提交 PR、评论等），你必须先获得信任。

### 1. 显式信任白名单

Vouch 不再假设陌生人是善意的，而是要求**显式授权**。它通过一个扁平的文本文件（默认名为 VOUCHED.td），记录了所有被信任用户的列表。

- Vouched（已担保）：被允许参与项目的用户。
- Denounced（已谴责）：明确被屏蔽的用户（例如提交恶意代码或滥用 AI 的人）。

GitHub Actions 会自动检查 PR 提交者是否在名单中。如果不在，PR 可能会被自动关闭，并将那些“低成本的 AI 投机者”拒之门外。

### 2. 并非技术门槛，而是“社交投名状”

这是否会让新手望而却步？Mitchell 在 FAQ 中给出了否定的回答。

获取信任并不需要你先修复一个复杂的 Bug，你需要做的仅仅是**像一个正常人类一样交流**。

“基本上：像在任何正常的人类社交环境中一样介绍你自己，你就能获得担保。”


一个真诚的 Issue 评论：“嗨，我是开发者 X，我想修复 Y 问题，我的思路是 Z”，远比一个冷冰冰的、由 AI 生成的一键 PR 更能赢得维护者的信任。

## 技术实现：Trustdown 与去中心化

Vouch 的设计体现了极简的 Unix 哲学和去中心化思想：

- Trustdown (.td) 格式：信任列表不是数据库，而是一个简单的文本文件。它易于阅读，易于 Diff，完全基于 Git 进行版本控制。
- 基于 Nushell：Vouch 的核心逻辑是用 Nushell 实现的，这意味着它没有复杂的依赖，是一个纯粹的 CLI 工具。
- 信任网络（Web of Trust）：这是 Vouch 最具野心的愿景。项目 A 可以配置 Vouch 去读取项目 B 的信任列表。这意味着，如果你在
**Ghostty**（Mitchell 的终端项目）中获得了信任，你在其他引用了 Ghostty 列表的项目中也将自动获得信任。

这种机制有望在开源界建立起一个跨项目的“信任联邦”，让优质贡献者畅通无阻，让 AI 垃圾制造者寸步难行。

## 小结

Vouch 的出现，标志着开源治理的一个转折点。在 AI 能够无限量生成代码的时代，“人”的信誉变得前所未有的重要。

Vouch 不是为了制造精英主义的壁垒，而是为了保护维护者的热情。它提醒我们：开源的本质不是代码的堆砌，而是人与人之间的协作与信任。

vouch开源项目仓库地址：https://github.com/mitchellh/vouch

**你支持这种“验证人”的做法吗？**

面对 AI 生成的代码洪流，你认为 Vouch 这种显式白名单模式是保护了维护者，还是会阻碍新手加入？在你的开源项目中，是否也曾遇到过让你头大的“AI 垃圾 PR”？

欢迎在评论区分享你的看法或应对策略！

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