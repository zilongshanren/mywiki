---
title: AMP 宣布砍掉 VS Code 插件：为什么说“人机结对编程”已死？
url: https://tonybai.com/2026/02/09/amp-kills-vscode-plugin-human-ai-pair-programming-is-dead/
published: '2026-02-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# AMP 宣布砍掉 VS Code 插件：为什么说“人机结对编程”已死？

![](../../assets/9910e66fef2997f6.png)


[本文永久链接](https://tonybai.com/2026/02/09/amp-kills-vscode-plugin-human-ai-pair-programming-is-dead) – https://tonybai.com/2026/02/09/amp-kills-vscode-plugin-human-ai-pair-programming-is-dead

大家好，我是Tony Bai。

如果一家 AI 编程工具公司，宣布砍掉它最受欢迎、用户量最大的产品入口，你会怎么想？

这听起来像是商业自杀，但这正是 AMP（从 Sourcegraph 孵化出来的 AI 编程 Agent）刚刚做出的决定。

在 [2026 年 2 月的一期播客](https://www.youtube.com/watch?v=4rx36wc9ugw)中，AMP 的创始人 Thorsten 和 Quinn 宣布：将在 60 天后，彻底关停 AMP 的 VS Code 插件和 Cursor 扩展。

要知道，在过去的两年里（2024-2025），IDE 侧边栏（Sidebar）几乎定义了 AI 编程的标准形态。无论是 GitHub Copilot、Cursor 还是早期的 AMP，我们都习惯了在编辑器里写代码，在侧边栏里和 AI “乒乓球”式地对话。

但 AMP 团队认为：这个时代结束了。

“你看着代码，AI 在侧边栏看着你，你们一来一回地对话……这种模式不是未来。对于那 1% 想要活在未来的开发者来说，侧边栏不仅不是助力，反而是枷锁。”


为什么他们敢于“烧掉桥梁”？因为一种全新的开发范式——“AI软件工厂模式（The Factory）”，正在随着 GPT-5.2 和 Claude Opus 4.5的成熟以及新版本编程大模型的发布而全面爆发。

今天，我们深度解读这份极具前瞻性的访谈，看看为什么 IDE 侧边栏必死，以及未来的软件工厂究竟长什么样。

![](../../assets/e7e1e92bcbb64dd9.png)


## Deep Mode：当 AI 学会了“深思熟虑”

要理解为什么要砍掉侧边栏，首先要理解模型能力的质变。

在 2025 年之前，主流模型（如 Claude 3.5 Sonnet）的特点是“聪明但急躁”。它们非常适合 Smart Mode：你问一个问题，它秒回一段代码；你报错，它秒回修正。这是一种高频的、实时的“结对编程”体验。

但随着 GPT-5.2 Codex 的发布，情况变了。

AMP 推出了一个新的模式：Deep Mode（深度模式）。

- 特性：这个模型不爱说话，它爱干活。它不是“懒惰”，而是“深沉”。
- 特工作流：你给它一个模糊但宏大的目标（例如“重构整个鉴权模块并适配新的安全协议”），然后你就可以走开了。
- 特时延：它可能会运行 45 分钟甚至 60 分钟。它会自主查阅文档、搜索代码、尝试方案、遇到错误、自我修正、运行测试，直到最终交付结果。

“侧边栏”完全无法承载这种体验。

想象一下，如果你在 IDE 侧边栏里发了一个指令，然后 AI 转了 45 分钟圈圈，期间你不敢关窗口，不敢切分支，这是一种多么糟糕的体验？

**结论 1：**

当 AI 的能力从“秒级补全”进化到“小时级任务”时，它必须脱离 IDE，进入后台，成为一个独立的Worker，而不是依附于编辑器的 Assistant。

## 惊人的抉择：Agent DX > Human DX

访谈中透露了一个令人细思极恐的细节，揭示了 AI 原生开发时代的价值观重构。

AMP 团队为了优化内部的开发效率，重写了他们的构建工具。

他们用 **Zig** 语言重写了 svelte-check，将其命名为 zvelt-check。这样做的目的是为了让 Agent 跑得更快，且输出的日志更结构化（便于 Agent 解析）。不过，这个新工具也破坏了 VS Code 对 Svelte 的原生支持（Human DX 下降）。人类开发者在编辑器里看到的错误提示变差了，甚至失去了一些高亮功能。

在“人类体验（Human DX）”和“智能体体验（Agent DX）”发生冲突时，AMP 选择了后者。

甚至有一半使用 NeoVim 的员工表示：“我不在乎 VS Code 体验变差，只要 Agent 跑得快就行。”

这是一个标志性的时刻。

长久以来，所有的开发者工具（CLI、Linter、Log）都是为了“让人类读懂”而设计的。我们需要漂亮的颜色、进度条、友好的报错提示。

但在 AI 时代，90% 的工具调用者将是 Agent。Agent 不需要颜色，不需要进度条，它们需要的是极致的速度、结构化的 JSON 输出、幂等的执行逻辑。

**结论 2：**

未来的工具链，将优先为 AI 优化。如果一个工具对人类不友好但对 AI 友好，它依然会被采用。我们正在主动劣化人类的开发体验，以换取 AI 生产力的十倍跃迁。

## 软件的消融：从 SaaS 到 Text

访谈中提到了一个名为 **“The Melting of Software（软件的消融）”** 的概念。这不仅影响开发工具，更影响我们构建产品的方式。

**案例 A：Ryan Florence 的健身教练**

Ryan 没有使用任何健身 App。他只是打开了 ChatGPT 的语音模式，说：“我在家里的健身房，指导我锻炼。”

AI 说：“做一组深蹲，好了叫我。”

Ryan 做完说：“好了。”

AI 说：“休息 60 秒。”

没有 UI，没有按钮，没有 App。软件消失了，只剩下服务。

**案例 B：购物清单的回归**

Torston 本想用 Agent 自动化管理 Todoist（一个著名的待办事项 App）。

但他突然意识到：*“我为什么要用 Todoist？我的购物清单只有 15 项。Agent 可以直接在一个纯文本文件里管理它。”*

如果 Agent 能读懂文本，能实时更新状态，能通过 CLI 提醒我，那我为什么还需要一个复杂的 SaaS 软件？

这指向了一个终极问题：当 Agent 能够理解非结构化数据，并能通过原子化工具（如Skills）操作一切时，传统的“应用软件”是否会大量消亡？

未来的软件，可能不再是精心设计的 GUI，而是一组 Skills（能力） + Context（上下文文件）。

- 你不需要 Google Cloud 的网页控制台，你只需要给 Agent 一个 gcloud 的 Skill。
- 你不需要 Jira 的复杂界面，你只需要一个能读写 Markdown 的 Agent。

**结论 3：**

软件正在退化为 API 和数据，中间的“交互层”正在被 Agent 接管。

## 技能（Skills）：新的抽象层

既然侧边栏死了，我们靠什么来通过 AI 开发？

答案是：**CLI + Skills**。

AMP 团队展示了他们如何在内部大量使用 Skills。

- Tmux Skill：教 Agent 如何在终端里正确使用 Tmux，如何杀掉进程（甚至包括“记得按两次 Ctrl-C”这种经验知识）。
- Google Cloud Skill：赋予 Agent 使用 Google Cloud CLI 的能力。
- BigQuery Skill：这被描述为“最神奇的体验”。你问：“多少用户用了这个功能？”，Agent 自动写 SQL，查 BigQuery，返回结果。

**Skills 是“经验的固化”。**

当你教会 Agent 解决一个问题后，让它把过程总结成一个 Skill。下次，它（以及团队里的其他 Agent）就不会再犯错。

这比在 Chat 窗口里一遍遍写 Prompt 要高效得多。

## 组织哲学：像艺术装置一样自我毁灭

为什么 AMP 敢于砍掉 VS Code 插件？这源于他们独特的公司哲学。

“我们就像一个

艺术装置（Art Installation），随时准备自我毁灭和重建。”

在这个技术每 3 个月就迭代一代的疯狂时代，“护城河”是最大的陷阱。

- GitHub Copilot 曾经是王者，Cursor 出来后它显得老了。
- Cursor 曾经是王者，Claude Code 和 AMP 出来后，编辑器模式显得老了。
- 也许 3 个月后，OpenClaw 这样的纯本地 Agent 会让现在的模式也显得老了。

AMP 的 CEO 说：“如果我们因为‘用户习惯’而保留旧功能，我们就会变成哪怕是最好的‘落伍者’。我们必须每 3 个月重新赢得我们的客户。”

**“Run towards the fire.”（向着炮火前进。）**

如果你看到某个技术趋势正在颠覆你，不要躲避，不要观望，**加入它，甚至成为颠覆自己的人。**

## 小结：给 1% 的开发者

这篇文章可能让大家感到不安。

你习惯了 VS Code，习惯了 Copilot 的自动补全，习惯了掌控一切。

但在 2026 年的视野里，**“人机结对”只是一个过渡形态**。

真正的未来属于 **Agentic System（智能体系统）**，属于 **Factory（软件工厂）**。

在那个未来里：

- 你不再是写代码的人，你是定义 Spec 的人。
- 你不再在编辑器里工作，你在终端（CLI）里指挥。
- 你不再管理代码，你
[管理智能体集群](https://tonybai.com/2026/02/08/claude-code-agent-team-mode/)。

对于那 1% 愿意走出舒适区、拥抱**“Factory Mode”**的开发者来说，你们的生产力将不再是线性的增长，而是指数级的爆发。

**侧边栏已死，工厂万岁。**

资料链接：https://www.youtube.com/watch?v=4rx36wc9ugw

**你愿意为效率牺牲体验吗？**

AMP 为了 Agent 效率主动劣化人类开发体验（Agent DX > Human DX），这一决定让你感到兴奋还是不安？如果一个工具能让你效率提升 10 倍，但代价是你再也看不清语法高亮，你会接受吗？

欢迎在评论区分享你对“AI 软件工厂”的看法！

**提前布局你的“软件工厂”**

虽然我们还不能完全抛弃编辑器，但 AMP 倡导的 Agent-Native 开发流，现在就可以开始实践。

在我的极客时间专栏**《 AI 原生开发工作流实战》**中，我们将深度对齐这种前沿理念：

- CLI First：如何脱离 IDE，使用
**Claude Code**在终端完成全流程开发？ - Skill Engineering：如何编写高质量的 Skill，让 Agent 掌握你独有的业务知识？
- Agent DX 优化：如何改造你的项目结构，让它对 AI 更友好？

不要等了。扫描下方二维码，现在就构建你的未来开发流。

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