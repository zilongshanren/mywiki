---
title: 拆解 Claude Code：Coding Agent 终于“能用”背后的架构真相
url: https://tonybai.com/2026/01/08/how-claude-code-works/
published: '2026-01-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 拆解 Claude Code：Coding Agent 终于“能用”背后的架构真相

![](../../assets/bfe3ec515ca3e046.png)


[本文永久链接](https://tonybai.com/2026/01/08/how-claude-code-works) – https://tonybai.com/2026/01/08/how-claude-code-works

大家好，我是Tony Bai。

在过去两年里，我们见证了 AI Coding Agent的尴尬童年：从最初笨拙的 Copy-Paste，到 Cursor 的 VS Code Fork 革命，再到如今 Claude Code 这种 CLI Coding Agent的出现。

为什么以前的 Agent 总是卡在“演示很酷，实战很废”的怪圈里？而 Claude Code 究竟做对了什么，让它突然变得如此顺手？

答案可能出乎意料的枯燥：**不是魔法，是更好的模型加上更“傻瓜”的架构。**

这不是一篇 Anthropic 的官方通稿。本文基于 PromptLayer 创始人 Jared Zoneraich 的深度逆向工程与[实战分享](https://www.youtube.com/watch?v=RFKCzGlAU6Q)。我们扒开了 Claude Code 的外衣，试图还原 Coding Agent 从“玩具”进化为“神器”的技术跃迁路径。

![img{512x368}](../../assets/f209dd925a924415.png)


## 架构哲学：删繁就简

如果你在 2024 年开发过 Agent，你一定画过那种复杂的 **DAG（有向无环图）**：

- “如果用户想退款，跳到节点 A；如果想查询，跳到节点 B……”
- 为了防止幻觉，我们设计了无数个分类器（Classifiers）和路由（Routers）。

结果呢？我们得到了一张维护噩梦般的蜘蛛网。

![](../../assets/697d7ddd9b80e0d8.png)


Claude Code（以及 Gemini Cli、CodeX 等新一代Cli Coding Agent）的架构哲学可以用 Python 之禅概括：**Simple is better than complex.**

它们抛弃了复杂的 DAG，拥抱了 **Master While Loop**。

![](../../assets/c3803a108f7b3c6c.png)


我们再用更为详细一些的伪代码来诠释这个master loop：

```
# Claude Code 的核心逻辑伪代码
messages = [...]
while True:
response = model.generate(messages)
if not response.tool_calls:
break
for tool in response.tool_calls:
result = execute_tool(tool)
messages.append(format_result(result))
```


就这么简单。**Give it tools, and get out of the way.**

![](../../assets/00662e581730f2a3.png)


这种架构的自信来源于模型能力的提升。现在的模型（如 Claude 4.5 Sonnet）已经足够聪明，能够自己决定“我需要先 grep 一下代码，发现不对，再 ls 一下目录，最后 edit 文件”。它不需要你预设路径，它需要的是**自由探索的空间**。

![](../../assets/eb1290c00e61bdde.png)



## 工具箱揭秘：Bash 即正义 (The Tools)

Claude Code 的工具箱极其精简，但每一个都切中要害。Jared 在逆向分析后发现，这套工具集本质上是在**模拟一个人类高级工程师在终端里的行为**。(注：按照Jared的说法，这些工具箱中的工具可能随Claude Code的版本的变化而不同!)

![](../../assets/5287068b04caf0d2.png)


### Bash: The Universal Adapter

如果只保留一个工具，那就是 **Bash**。

- 它能跑脚本、能运行测试、能安装依赖、甚至能重启服务。
- 它是 Agent 与数字世界交互的通用接口。
- 最重要的是，LLM 训练数据里有海量的 Bash 语料，模型天生就是 Bash 高手。

![](../../assets/49ff690e1a8c1f0c.png)


### Edit: Unified Diff

Claude Code 没有选择全量重写文件（Rewrite），而是选择了 **Diff**。

**省 Token**：只输出修改的几行，上下文窗口压力骤减。**速度快**：更少的输出意味着更低的延迟。**容错高**：就像老师批改作文划红线一样，基于上下文的 Diff 修改比凭空重写整段代码更容易命中，也更容易被人类 Review。

![](../../assets/3f816b8360b0a1a8.png)


### Grep & Glob > RAG

还记得那些为了让 Agent 理解代码库而建立的复杂向量数据库（Vector DB）吗？Claude Code 说：**不需要**。

它直接使用 grep 和 glob。这不仅是因为现在的 Context Window 够大，更是因为这符合工程师的直觉。当你接手一个新项目时，你不会先在大脑里建立一个向量索引，你会先 ls 看看目录结构，然后 grep 关键字。**模拟人类的行为，往往是最佳策略。**

### Sub-Agents (Tasks)

当任务太复杂，上下文快爆了怎么办？Claude Code 引入了 **Task** 工具。

它可以启动一个子 Agent（Sub-agent），拥有独立的上下文，去执行特定的任务（比如“阅读完所有文档并总结 API 用法”），然后只将最终结果返回给主 Agent。这有效地解决了 Context 污染问题。

![](../../assets/d7105df4a290e88e.png)


## 核心心法：相信模型，放弃微操

在传统软件工程中，我们习惯于通过代码控制一切：if 条件 A 发生，执行 B。但在构建 Coding Agent 时，这种“控制欲”往往是最大的敌人。

Jared 分享了一个极具启发性的**失败案例**：

为了让 Agent 更好地操作 PromptLayer 的网页后台，他曾试图进行“人工辅助”——给网页上的每个按钮都加上了详细的 Title 和标签，试图告诉 Agent “点击这里会发生什么”。

结果呢？**Agent 的表现反而变差了。**

为什么？因为额外的信息变成了噪音，分散了模型的注意力。模型原本可以通过“观察-尝试-纠错”的循环自己搞定任务，但人类的“硬编码微操”反而限制了模型的泛化能力。

### Exploration > Hardcoding

Claude Code 的设计哲学是：**当你有疑问时，相信模型(rely on the model)。**

**不要预设所有边缘情况**：以前我们会写一堆正则来解析输出，现在？直接把错误扔回给模型：“你报错了，修好它。”

![](../../assets/acd7cda587a7bd7b.png)


**探索即纠错**：模型不仅能写代码，还能读懂报错信息。Claude Code 之所以强大，不是因为它一次就能写对，而是因为它在 Master Loop 中具备了**自我修复（Self-Correction）**的能力。

**工程师的直觉是“把路铺好”，但 AI 时代的直觉应该是“给它地图，让它自己走”。**

## 那些“不起眼”但天才的细节

### Constitution: CLAUDE.md

不需要复杂的微调，也不需要向量库。Claude Code 依靠项目根目录下的 CLAUDE.md 来理解项目规范。

这本质上是 **Prompt Engineering 的胜利**。它让配置变得透明、可读、可由用户（甚至 Agent 自己）随时修改。

### System Prompt 解密：像老板一样下指令

Jared 分享了基于泄露信息的 Claude Code System Prompt 核心原则，这些原则非常值得我们借鉴：

**Concise Output（极简输出）**：除非用户要求细节，否则输出不要超过 4 行。**No “Here is…”（拒绝废话）**：不要说“好的，这是您的代码…”，直接给代码。Just do it.**Action over Text（行动至上）**：能用工具（Tool）解决的，别用文字解释。**Style Match（风格一致）**：严格匹配项目现有的代码风格。**No Comments（拒绝注释）**：除非用户要求，否则不要画蛇添足地加注释。**Parallelism（并行执行）**：鼓励并行运行命令，大规模搜索，并使用 TodoWrite 跟踪进度。

![](../../assets/52e494282257cce9.png)


这些指令的目的只有一个：**让 Agent 看起来更像一个干练的 Senior Engineer，而不是一个啰嗦的 Chatbot。**

### Skills: 可扩展的 “System Prompt”

随着任务变复杂，System Prompt 会越来越长，甚至超过 Context 限制。Claude Code 引入了 **Skills** 机制。

你可以把它理解为**按需加载的“技能包”**。Agent 会根据当前任务，决定是否加载额外的上下文或能力。

**典型应用场景：**

**Documentation Updates**：加载特定的文档写作风格指南。**Design Style Guide**：在写前端代码时，加载 UI 设计规范。**Deep Research**：加载深度搜索和总结的能力。**DOCX/Excel Processing**：甚至可以加载处理办公文档的技能（Jared 提到这是很多人没想到的用法）。

### To-Do Lists: 提示词驱动的结构化

当你让 Claude Code 干活时，它往往会先列一个 To-Do List(是不是又和人类干活的方式类似呢)。

有趣的是，这**不是**代码里写死的逻辑，而是 System Prompt 诱导出来的行为。

- 它给用户一种“确定性”的心理安全感。
- 它支持
**断点续传**：即使程序 Crash 了，重新把 To-Do List 喂给模型，它也能知道下一步该干嘛。

![](../../assets/4f36cb4dd6a37c43.png)


### Thinking Knobs

Think, Think Hard, Ultra Think。

这不仅仅是噱头，这是把 **Inference-Time Compute（推理时计算）** 变成了一个可调节的参数。对于复杂的重构，你可以让它“多想一会儿”；对于简单的 Bug fix，直接干就是了。

![](../../assets/5be353b3ffb95ae0.png)


## 市场格局：没有全局最优解

在 Coding Agent 的战场上，没有唯一的王者，只有不同的流派（The “AI Therapist” Problem）。

**Claude Code**：**CLI 极简主义**。简单、直观，适合不想离开终端的开发者。**Cursor**：**UI 速度流**，极致的响应速度。它利用用户数据飞轮，让体验越来越丝滑。**OpenAI CodeX**：**内核硬核派(rust实现)**。更关注底层的沙箱安全（Kernel-level Sandboxing），适合企业级、高安全要求的场景。**Sourcegraph Amp**：**Web 协作流**。主打**Handoff（接力）**机制，在一个 Agent 搞不定时，无缝切换到另一个 Context 或模型(无需用户选择)，像接力赛一样解决问题。

## 核心启示：Claude Code 教给我们的 5 条构建法则

在演讲的最后，Jared 总结了 Claude Code 成功的 5 个核心要素。对于任何想要构建 Agent 或由 AI 驱动的应用的开发者来说，这 5 条法则就是当下的“金科玉律”。

### Trust in the model (相信模型)

不要试图用传统的代码逻辑去“微操”模型。

**反直觉**：工程师总想把所有路都铺好（比如给网页按钮加详细标签）。**新常识**：模型的泛化能力和纠错能力远超你的硬编码规则。当遇到不确定性时，给它目标，让它自己去探索，而不是给它僵化的步骤。

### Simple design wins (简单致胜)

架构越简单越好。

**拒绝复杂**：不要搞几百个节点的 DAG（有向无环图），不要搞复杂的路由网络。**拥抱简单**：一个死循环（While Loop）加上强大的模型，往往能击败精心设计的复杂架构。正如 Python 之禅所说：“Simple is better than complex.”

### Bash is all you need (Bash 足矣)

在工具选择上，不要重新发明轮子。

**通用接口**：Bash 是在这个星球上运行代码最通用的接口，也是 LLM 训练数据中最丰富的语料之一。**少即是多**：与其开发 50 个专用的 Tool（比如 create_file, delete_file, git_commit…），不如只给它一个 bash 工具。模型知道怎么用 touch, rm, git。

### Context management matters (上下文管理是关键)

这是目前 Agent 最大的隐形杀手（The Boogeyman）。

**瓶颈**：无论模型多聪明，上下文窗口一旦被垃圾信息填满，智商就会直线下降。**策略**：必须把“上下文清洗”作为架构的一等公民。利用 Summarization（摘要）、Handoff（接力）或 Sub-agents（子智能体）机制，时刻保持主线程的清爽。

### Different perspectives for different problems (不同问题，不同视角)

没有“万能药”。Coding Agent 领域不存在全局最优解（Global Maxima）。

**Claude Code**：赢在 CLI 交互和复杂的 Git/环境管理，适合“不想离开终端”的场景。**Cursor**：赢在 UI 速度和代码补全，适合“快速编写”的场景。**CodeX**：赢在底层沙箱安全。**结论**：不要试图寻找一个能打败所有人的 Agent，而是要构建最适合特定场景（User Persona）的 Agent。

![](../../assets/6739b0b87c559843.png)


## 小结

Claude Code 的出现，标志着 Coding Agent 进入了**“实用主义”**时代。它不再是炫技的玩具，而是通过做减法（Less RAG, Less DAG, Less Guardrails），回归了软件工程的本质。

未来，我们或许不再直接调用 LLM 的 API，而是直接调用一个 Headless 的 run_agent() SDK，让它在后台默默地帮我们修 Bug、写文档、提 PR。

**最好的工具，就是当你感觉不到它存在的时候。**

资料来源：Jared Zoneraich “How Claude Code Works” – https://www.youtube.com/watch?v=RFKCzGlAU6Q

**你的 Agent 构建心得**

Claude Code 的“极简架构”给我们上了一课。**你在尝试构建 AI Agent 时，是否也曾陷入过“过度设计”的陷阱？对于“Bash is all you need”这个观点，你认同吗？**

**欢迎在评论区分享你的踩坑经历或架构思考！** 让我们一起探索 Agent 开发的最佳路径。

**如果这篇文章为你揭开了 Claude Code 的神秘面纱，别忘了点个【赞】和【在看】，并转发给你的架构师朋友！**

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