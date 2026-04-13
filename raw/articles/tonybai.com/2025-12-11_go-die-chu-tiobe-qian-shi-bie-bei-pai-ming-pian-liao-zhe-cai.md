---
title: Go 跌出 TIOBE 前十？别被排名骗了，这才是它的真实地位
url: https://tonybai.com/2025/12/11/is-golang-still-a-growing-programming-language/
published: '2025-12-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 跌出 TIOBE 前十？别被排名骗了，这才是它的真实地位

![](../../assets/cbb5df573c36d81f.png)


[本文永久链接](https://tonybai.com/2025/12/11/is-golang-still-a-growing-programming-language) – https://tonybai.com/2025/12/11/is-golang-still-a-growing-programming-language

大家好，我是Tony Bai。

Go 语言是否已经触到了天花板？在 Python 借力 AI 狂飙突进、Rust 备受追捧的今天，Go 的位置究竟在哪里？近日，[Twitch工程师 Melkey](https://tonybai.com/2025/07/04/everything-i-did-to-become-an-expert-in-golang) 结合 [JetBrains](https://tonybai.com/2025/11/14/the-go-ecosystem-in-2025/)、Stack Overflow 以及 GitHub 的最新数据，发布了[一份关于 Go 语言现状的深度分析](https://www.youtube.com/watch?v=QjGduiCFHY4)。结论或许并不全是“好消息”，但却极其真实地反映了 Go 在工业界的稳固地位。

![](../../assets/eea4f3d68dbb3fdb.png)


## 谁在用 Go？—— “云原生土著”的画像

[JetBrains 的年度报告](https://tonybai.com/2025/11/14/the-go-ecosystem-in-2025/)揭示了 Go 开发者的主要分布领域。数据显示，排名前三的应用场景分别是：

**Web 服务（无 GUI）****网站后端****云服务与基础设施**

Melkey指出，尤其是第三点——**云服务**，最能代表 Go 的核心竞争力。这与行业内的普遍印象高度一致：专业的 Go 开发者往往不仅仅是在编写业务逻辑，更多时候是在与 Kubernetes 集群、微服务架构、CI/CD 管道以及各类 CLI 工具打交道。

如果说 Python 是数据科学的通用语，那么 Go 已经牢牢确立了自己作为**“ 云时代 C 语言”**的地位——它是构建现代基础设施的首选工具。

## 新手不再爱 Go？—— 一个值得注意的信号

在解读 Stack Overflow 2025 开发者调查时，Melkey敏锐地发现了一个略显尴尬的趋势。

虽然在所有受访者中，Go 的使用率约为 **16.4%**，但在**“正在学习编程的人”**（Learning to Code）这一群体中，Go 的排名出现了显著下滑。绝大多数编程新手的入门首选依然是 Python 或 JavaScript。

然而，这并不意味着 Go 的衰落。相反，数据显示，在**“专业开发者”**群体中，Go 的使用率上升到了 **17%**。

Melkey分析认为，这意味着 Go 正逐渐成为一种**“第二语言”**。它不再是很多人的“初恋”语言，而是开发者在掌握了编程基础后，为了追求高性能、高并发和工程化能力而进阶选择的“成熟伴侣”。

## 薪资高，但别被“头衔”骗了

分享中提到，在美国，Go 开发者的年薪上限可达 **50 万美元**，平均薪资也极具竞争力。

但Melkey对此提出了冷静的见解。他指出，如果在 LinkedIn 等招聘平台上搜索，会发现纯粹招募“Golang Developer”的岗位并没有想象中那么多。大多数高薪岗位实际上招募的是**“资深后端工程师”**或**“云基础设施专家”**。

这传递了一个明确的信号：市场不缺会写 if err != nil 的程序员，缺的是懂分布式系统、懂架构、能解决复杂问题，并且**恰好使用 Go 作为工具**的工程师。真正值钱的不是 Go 的语法，而是用 Go 解决工程问题的能力。

## TIOBE 排名下滑 vs GitHub 活跃度上升

数据层面出现了一个有趣的“冲突”。

在老牌的 TIOBE 指数2025年11月份数据中，Go 从去年的第 7 名下滑至今年的 **第 11 名**，跌出了前十。这似乎是一个危险的信号。

![](../../assets/4257e421da491149.png)


但如果转向 GitHub 的数据，Go 依然是**开源项目活动增长最快的前三名语言**（仅次于 Python 和 TypeScript）。GitHub 的趋势图显示，Go 的生态活跃度保持着陡峭的上升曲线，没有减速迹象。

Melkey认为，TIOBE 可能反映了大众搜索的热度，但 GitHub 反映的是**开发者用脚投票**的结果。Go 的生态依然在蓬勃发展，只是不再像早期那样具有话题性和炒作度，而是进入了成熟期和深耕期。

## AI 时代：Go 是“铲子商”，不是“淘金者”

在 AI 席卷全球的当下，Go 的位置在哪里？Melkey给出了精准的定位：**“Go 在构建 AI 基础设施方面表现出色，但缺乏原生的机器学习解决方案。”**

Melkey结合自己在 Twitch 构建 ML 基础设施的经历印证了这一点：在 AI 领域，Python 用于模型训练（得益于 PyTorch, TensorFlow 等库），而 Go 则用于**部署模型、构建大规模并发的推理服务**以及搭建底层的 **ML 基础设施**。

Go 不会取代 Python 成为 AI 训练的语言，但在 AI 落地、服务化、工程化的“最后一公里”，Go 是绝对的主力。

## 小结：Go 的未来是“稳态”

![](../../assets/1d5f5ee63021dfec.png)


基于上述数据，Melkey给出了自己的最终结论：

**Go 不会消失，但也别指望它能像火箭一样再次爆发式增长。**

它不会取代 Python 或 TypeScript 成为统治一切的通用语言。它正在进入一个**“稳态”**。在云原生、后端服务和基础设施领域，Go 已经建立了坚不可摧的壁垒。对于追求职业发展的工程师而言，它依然是一个稳定、高效且回报丰厚的选择。

Go 的未来，或许不再是“无处不在”，但注定是**“不可或缺”**。

资料链接：https://www.youtube.com/watch?v=QjGduiCFHY4

**你的体感如何？**

数据是宏观的，但体感是微观的。

在你所在的公司或团队，Go 语言的使用是在扩张还是收缩？你认为 Go 在 AI 时代最大的机会是什么？

欢迎在评论区分享你的观察，让我们一起拼凑出更真实的 Go 生态图景！

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


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论