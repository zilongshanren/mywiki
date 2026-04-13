---
title: Linus 的名言要改了：Talk is cheap, show me the Spec
url: https://tonybai.com/2025/12/12/talk-is-cheap-show-me-the-spec/
published: '2025-12-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Linus 的名言要改了：Talk is cheap, show me the Spec

![](../../assets/070bc54ee0d1d828.png)


[本文永久链接](https://tonybai.com/2025/12/12/talk-is-cheap-show-me-the-spec) – https://tonybai.com/2025/12/12/talk-is-cheap-show-me-the-spec

大家好，我是Tony Bai。

在 IT 行业，有一句被奉为圭臬的名言，出自 Linux 之父 Linus Torvalds：


“Talk is cheap, show me the code.”

(废话少说，放码过来。)

在过去的三十年里，这句话是绝对正确的。因为将人类的自然语言逻辑翻译成机器能运行的 C/C++/Go/Java 代码，是一项高难度、高成本的脑力劳动。代码，就是程序员的军功章，是能力的终极证明。

但是，站在 2025 年末的今天，当我们看着 [Claude Code](https://tonybai.com/2025/11/20/ai-native-dev-workflow/) 或 Cursor 在几秒钟内生成了数百行逻辑严密、注释清晰的代码时，你是否感觉到了一种微妙的**价值观崩塌**？

如果生产代码变得像呼吸一样简单，那么“Show me the code”还足以证明你的价值吗？

我认为，是时候修正这句话了。在 AI 原生开发时代，新的法则应该是：

**“Talk is cheap, show me the Spec.”**

**(空谈廉价，请给我看你的规范说明书。)**

![](../../assets/5b15b2fa46955458.png)


## 价值倒置：代码的通货膨胀

为什么说 Code 变得 cheap（廉价）了？这符合基本的经济学规律：**供需关系**。

**前 AI 时代：**代码的供给受限于程序员的打字速度和脑力带宽。优质代码是稀缺资源。**AI 时代：**LLM 使得代码的供给趋近于无限。只要你给指令，AI 可以不知疲倦地生成无限吨位的代码。

当一个东西的供给变得无限时，它的价值就会无限趋近于零。

现在，你随便找个实习生，配上 AI 工具，他也能给你 Show 出一大堆 Code。但这些 Code 是垃圾还是黄金？能不能跑？符不符合业务需求？

**这取决于“指令”的质量，而不是“代码”本身。**

## 权力的转移：从“实现” 到 “定义”

在传统的软件工程中，权重最高的是 **Implementation（实现）**。我们推崇那些能搞定复杂算法、能手写汇编的大神。

但在 **SDD (Spec-Driven Development)** 兴起的当下，权力中心正在向 **Definition（定义）** 转移。

**什么是 Spec (Specification)？**

在 AI 时代，请务必注意：**Spec 不再是那个单薄的 requirements.txt 或 README.md，它是广义的“全景蓝图（Blueprint）”。**

参考业界前沿的 **SDD 规范（如 spec-kit / openspec）**，一个合格的、能让 AI 准确执行的 Spec，通常包含 **“SDD 三件套”**：

-
**The Context (语境/需求) —— spec.md****定义 “What & Why”**：业务逻辑是什么？输入输出接口定义（Interface）是什么？**核心要素**：用户故事、API 契约、非功能性约束（性能/安全）、领域知识（Domain Context）。

-
**The Strategy (策略/架构) —— plan.md****定义 “How”**：为了实现上述需求，我们需要修改哪些文件？数据流怎么走？**核心要素**：技术栈选择、文件变更拓扑图、伪代码（Pseudocode）、架构决策记录（ADR）。

-
**The Execution (执行/进度) —— tasks.md****定义 “Steps”**：将大象装进冰箱分几步？**核心要素**：原子化的任务清单（Atomic Checklist）。AI 每做完一步，就勾选一项。这能极大地降低 AI 的“遗忘率”和“幻觉率”。


![](../BlogImages/2025/talk-is-cheap-show-me-the-spec-3.png)


**Code 只是这套 Spec 的“编译产物”。**

这就好比建筑行业：当砌砖机器人都普及了，“砌砖”这个动作就不值钱了。值钱的是包含**效果图（Spec）、结构图（Plan）和施工进度表（Tasks）**在内的完整**蓝图**。

我们可以用一张架构图来展示这个**“广义 Spec”**的结构：

![](../../assets/534dbe9775dccfa0.png)


**当你对 AI 说 “Show me the Spec” 时，你是在要求这三者的完整交付。** 只有这样，AI 才能从一个“只会聊天的机器人”变成一个“使命必达的工程师”。

## 新的开发范式：Show me your Spec

让我们对比一下两种开发者的对话模式：

**旧模式（Code-Centric）：**

* **A:** “这个功能怎么做？”

* **B:** “你看我这几行代码（Show Code），我用了一个递归……”

* **痛点：** 陷入细节泥潭，难以维护，AI 容易写偏。

**新模式（Spec-Centric）：**

* **A:** “这个功能怎么做？”

* **B:** “你看我的 Spec 文档（Show Spec）。我定义了数据结构，约束了异常处理流程，并列出了 5 个测试用例。然后我让 AI 实现了它。”

* **优势：** 逻辑闭环，架构清晰，AI 能够一次做对（One-shot Success）。

在这个模式下，程序员的核心竞争力，从**“How to implement”**（怎么写代码），变成了**“How to define”**（怎么定义问题）。

你能写出多么严谨、清晰、无歧义的 Spec，AI 就能给你多完美的代码。

**Spec 的精度，决定了系统的质量。**

## 小结：做架构师，别做打字员

Linus 说 “Talk is cheap”，是因为当年的 Talk 无法直接转化为生产力。

但现在的 “Spec” 不是 cheap talk，它是**可执行的指令（Executable Instructions）**。

在 AI 时代，请不要再沉迷于堆砌代码行数。

把那些繁琐的实现交给 AI。

**你应该去思考架构，去定义边界，去编写 Spec。**

下一次，当有人还在炫耀他手写了多少代码时，请淡定地告诉他：

**“Code is cheap. Talk is cheap. Show me your Spec.”**

**如何写出让 AI 听话的 Spec？**

道理大家都懂，但真到了实战中，很多人发现自己写的 Spec，AI 根本看不懂，或者生成的代码依然是一坨浆糊。

**Spec 也是一门编程语言，只不过它的编译器是 LLM。**

如果你想掌握这门**“面向 AI 的编程语言”**，学会如何编写高质量的 Prompt 和 Spec 文档，构建一套基于 **Claude Code** 的自动化流水线，欢迎关注我的极客时间专栏**《AI 原生开发工作流实战》**。

在本专栏中，我将：

**定义标准：**公开我经过实战验证的**SDD (Spec-Driven Development)**文档模板。**实战演示：**展示如何用一份详实完备的Spec，指挥 AI 完成一个项目模块的开发、测试与部署。**思维升级：**帮你完成从 Coder 到 Architect 的关键跃迁。

**别让你的才华浪费在廉价的代码实现上。扫描下方卡片，掌握定义未来的能力。**

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