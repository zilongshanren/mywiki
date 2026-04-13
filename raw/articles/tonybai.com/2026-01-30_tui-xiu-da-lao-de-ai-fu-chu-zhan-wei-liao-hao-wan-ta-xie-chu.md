---
title: “退休”大佬的 AI 复出战：为了“好玩”，他写出了火遍全网的 Moltbot
url: https://tonybai.com/2026/01/30/clawdbot-author-peter-steinberger-full-interview/
published: '2026-01-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# “退休”大佬的 AI 复出战：为了“好玩”，他写出了火遍全网的 Moltbot

![](../../assets/0c9519a706fa507a.png)


[本文永久链接](https://tonybai.com/2026/01/30/clawdbot-author-peter-steinberger-full-interview) – https://tonybai.com/2026/mm/dd/clawdbot-author-peter-steinberger-full-interview

大家好，我是Tony Bai。

在硅谷，每天都有无数个 AI 项目诞生，它们大多有着精美的 Landing Page，有着宏大的融资计划，PPT 里写满了“颠覆行业”。

但最近，一个名为 **Clawdbot**（现已因商标原因更名为 **Moltbot**）的项目，却以一种完全不同的姿态闯入了大众视野。没有融资，没有团队，甚至没有商业计划书。它仅仅是一个“退休(财务自由)”的软件大佬，为了给自己“找乐子”而写的一堆代码。

然而，就是这样一个项目，在 GitHub 上一夜之间狂揽 **3.2w+ Star**，甚至让很多非技术圈的人都跑去 Apple Store 抢购 Mac Mini 来运行它。

它的作者是 **Peter Steinberger**，著名的 PDF SDK 提供商 PSPDFKit 的创始人。在卖掉公司退休四年后，他因为 AI 找回了当年的热血。

在最近的[一次深度访谈](https://www.youtube.com/watch?v=qyjTpzIAEkA)中，Peter 毫无保留地分享了他开发 Moltbot 的全过程。这不仅是一个关于工具的故事，更是一份关于**“在 AI 时代，个人开发者如何打破大厂垄断，重塑人机交互”**的珍贵启示录。

![](../../assets/5b15b2fa46955458.png)


## 从 Burnout 到 Addiction：找回失去的 Mojo

故事的开始并不美好。

四年前，Peter 卖掉了自己经营了 13 年的公司。长期的创业压力让他彻底 **Burnout（职业倦怠）**。

“那感觉就像有人把我的 Mojo（魔力/精力）吸干了一样。” 他回忆道。在那之后的三年里，他对编程完全提不起兴趣，哪怕只是坐在电脑前都觉得是一种折磨。

直到 2025 年 4 月，一切改变了。

Peter 开始接触早期的 AI 工具，特别是 Claude Code 的 Beta 版。那一刻，他感到了久违的兴奋。

“如果你错过了前几年 AI 比较‘智障’的阶段，直接上手现在的工具，你会觉得——**这简直太棒了（Pretty Awesome）！**”

这种兴奋迅速转化为了一种“成瘾（Addiction）”。

但这是一种积极的成瘾。他开始熬夜写代码，甚至会在凌晨 4 点给朋友发消息讨论 AI 的新发现。为了给自己找点乐子，他甚至搞了一些极其荒谬的实验：

比如，他做了一个**“全球最贵的闹钟”**。

他让运行在伦敦服务器上的 AI Agent，通过 SSH 远程登录到他家里的 MacBook，然后自动调大音量来叫醒他。

“这听起来很疯狂，甚至有点杀鸡用牛刀，但这就是我的初衷——**Have Fun（玩得开心）**。”

Peter 认为，学习新技术的最好方式，就是把它当成玩具。当你不再为了 KPI 或融资而写代码，而是为了让 AI 帮你订一份外卖、回一条消息而折腾时，创造力才会真正涌现。

## 技术哲学：CLI 是 Agent 的母语

Moltbot 之所以能打败众多商业化的 AI 助理，核心在于 Peter 对软件架构有着极其深刻的第一性原理认知：

**“Don’t build for humans, build for models.”（别为人构建，为模型构建。）**

如果你仔细观察现在的软件世界，你会发现所有的 GUI（图形界面）、按钮、下拉菜单，本质上都是为了适应人类极其有限的带宽（Bandwidth）和注意力而设计的。我们需要视觉引导，因为我们记不住命令。

但 AI 不需要这些。

AI 读得懂 Unix 手册，AI 记得住所有参数。

因此，Moltbot 采用了极其激进的 **CLI-First（命令行优先）** 策略。

Peter 解释道：“你知道什么东西最能 Scale（扩展）吗？是 CLI。你可以写 1000 个小工具，只要它们都有 –help 文档，Agent 就能瞬间学会如何使用它们。”

在 Moltbot 的架构里，所有的能力都被封装成了原子化的 CLI 工具：

- 想控制 Sonos 音箱？写个 CLI。
- 想看家里的摄像头？写个 CLI。
- 想查 Google 地图？写个 CLI。

Agent 就像一个万能的系统管理员，它通过组合这些 CLI，获得了在数字世界和物理世界中“行动”的能力。这比那些试图用鼠标点击模拟人类操作的 RPA（自动化流程）要高效、稳定一万倍。

## 打破围墙：数据的解放运动

Moltbot 最让极客们热血沸腾的，是它对 **Big Tech Walled Gardens（大厂围墙花园）** 的宣战。

现在的互联网巨头，都希望把你锁在他们的 App 里。WhatsApp 不开放 API，Spotify 不让你导出数据，外卖软件不让你自动化下单。

但在 Peter 看来，**AI 是打破这些围墙的终极武器。**

以 WhatsApp 为例。官方没有给个人开发者提供 API，如果你用商业 API 发太多消息，还会被封号。

Peter 的做法是：**Hack Everything。**

他直接通过 Hack 桌面端协议，让 Moltbot 能够接管他的 WhatsApp。当他在旅途中收到朋友的语音消息（比如推荐餐厅）时，Moltbot 会自动：

- 下载语音文件（哪怕它是 Opus 格式）。
- 调用 ffmpeg 转码。
- 调用 Whisper 识别文字。
- 调用 OpenAI 提取餐厅名字和地址。
- 自动添加到他的 Google Maps 待去清单中。

这一切都在后台静默发生。当 Peter 打开地图时，餐厅已经在那了。

**“App 终将消亡（Melt away）。”** Peter 在访谈中抛出了这个震聋发聩的观点。

“为什么我还需要一个专门的 Fitness Pal 来记录卡路里？我只需要拍一张汉堡的照片发给我的 Agent。它知道我在麦当劳，它知道汉堡的热量，它会自动更新我的健康数据库，并建议我晚上多跑 2 公里。”

在 [Agentic Commerce 时代](https://tonybai.com/2026/01/14/google-ucp-agentic-commerce-architecture-revolution)，用户不再需要在一个个孤立的 App 之间跳来跳去。**所有的 App 都将退化为 Agent 可调用的 API（或被 Hack 成 API）。**

## 本地优先：隐私与红利的博弈

Moltbot 的另一个标签是 **Local-first（本地优先）**。

虽然 Peter 自己也用 OpenAI 和 Anthropic 的模型（因为它们目前确实最聪明），但他花了大量精力去适配本地模型（如 MiniMax 2.1）。

为此，他甚至给自己的 Mac Studio 拉满了 512GB 的内存。

为什么要这么折腾？

除了“好玩”，还有一个现实的考量：**Red Tape（繁文缛节）**。

“如果你是一个公司，你想让 AI 访问你的 Gmail，你需要经过极其漫长的合规审核，甚至需要收购一家有牌照的公司。这太荒谬了。”

但如果你在**本地**运行 Agent，这一切都不复存在。

- 数据在你的硬盘里。
- 模型在你的显卡里。
- 操作在你的系统里。

没有人能阻止你读取自己的邮件，没有人能禁止你分析自己的聊天记录。

Peter 甚至预言，AI Agent 的普及将直接带动高性能硬件（如 Mac Mini）的销量。**“This is the liberation of data.（这是数据的解放。）”**

## 商业与开源：为爱发电，拒绝收编

随着 Moltbot 的爆火，无数 VC 挥舞着支票找上门，甚至有大厂想直接收购整个项目（或者招安 Peter）。

对此，Peter 的态度非常潇洒：**“I built this for me.（我是为我自己造的。）”**

他已经财务自由，不需要再为了融资去写 PPT，不需要为了增长去牺牲用户体验。

“代码本身已经不值钱了（Code is not worth that much anymore）。在这个 AI 时代，你完全可以把我的代码删了，让 AI 几个月再写一个新的。”

真正值钱的，是**Idea（想法）**，是**Community（社区）**，是**Brand（品牌）**。

他更倾向于将 Moltbot 运作成为一个非营利基金会（Foundation）。他希望这成为一个属于所有人的、开放的、可 hack 的游乐场，而不是某个大厂封闭生态的一部分。

## 小结：去构建你的 Loop

在访谈的最后，Peter 对所有开发者发出了呼吁：

**“Don’t just watch. Build your own agentic loop.”**

（别只是看，去构建你自己的智能体闭环。）

Moltbot 只是一个开始。它证明了，一个拥有**长期记忆（Memory）**、**工具使用能力（Tools）**和**自主性（Autonomy）**的个人 Agent，能爆发多么惊人的能量。

在这个时代，限制你的不再是技术门槛，而是你的**想象力**。

去写几个 CLI，去 Hack 几个 API，去给你的 AI 装上“手脚”和“记忆”。

未来，属于那些敢于用 AI 重塑生活的人！

资料链接：https://www.youtube.com/watch?v=qyjTpzIAEkA

**你的“好玩”项目**

Peter 的故事告诉我们，技术最原本的动力是乐趣。如果给你无限的时间和算力，你最想用 AI 为自己做一个什么“好玩”的工具？是全自动点餐助

手，还是你的专属游戏陪练？

欢迎在评论区分享你的脑洞！别管它有没有商业价值，有趣就够了。

如果这篇文章点燃了你久违的代码热血，别忘了点个【赞】和【在看】，并转发给你的极客朋友，一起搞点事情！

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