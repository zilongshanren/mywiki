---
title: 为什么你的 AI Agent 总是像个智障？来自 Manus 大佬的 2 年血泪避坑指南
url: https://tonybai.com/2026/03/18/why-ai-agents-act-stupid-manus-expert-pitfall-guide/
published: '2026-03-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 为什么你的 AI Agent 总是像个智障？来自 Manus 大佬的 2 年血泪避坑指南

![](../../assets/8616aea2606f6d62.png)


[本文永久链接](https://tonybai.com/2026/03/18/why-ai-agents-act-stupid-manus-expert-pitfall-guide) – https://tonybai.com/2026/03/18/why-ai-agents-act-stupid-manus-expert-pitfall-guide

大家好，我是Tony Bai。

如果你在过去一年里跟风写过 AI Agent（智能体），你大概率经历过这样的绝望时刻：

你兴致勃勃地给大模型挂载了二三十个精心编写的 Function Calling（函数调用）工具，比如 read_file, search_web, execute_python……你期待它能像钢铁侠的贾维斯一样运筹帷幄。

结果呢？面对稍微复杂一点的任务，你的 Agent 瞬间退化成一个“智障”。

它要么在几十个工具里疯狂迷失，选错了参数导致系统报错；要么陷入无限死循环，把你的 Token 烧个精光，最后无辜地吐出一句：“抱歉，我无法完成该任务。”

我们总以为是自己的 Prompt 没写对，或者是大模型还不够聪明。

直到前些日子，一位名叫 MorroHsu 的顶级实战派大佬（在被 Meta 收购前，他是现象级 AI 产品 Manus 的后端技术负责人）在 Reddit 上[抛出了一篇长文](https://www.reddit.com/r/LocalLLaMA/comments/1rrisqn/i_was_backend_lead_at_manus_after_building_agents)。

在过去两年里，他以后端负责人的身份参与构建了包括 Manus、agent-clip 等在内的多个顶尖 Agent。在被大模型的各种奇葩幻觉折磨了无数遍之后，他得出了一个极其震撼、甚至有些反直觉的血泪结论：

**别再瞎折腾繁琐的 Typed Function Calls（类型化函数调用）了！给大模型一堆乱七八糟的 API，就是它变“智障”的罪魁祸首。大模型最需要的，仅仅是 50 年前的 Linux 命令行（CLI）。**

今天，我们就来看看这位 Manus 前后端大佬的 2 年避坑心法。看看为什么最前沿的 AI，反而需要最古老的 Unix 哲学来拯救。

![](../../assets/1d8cffbff45e84f2.png)


## 为什么给 AI 几百个工具，它反而成了“智障”？

目前主流的 Agent 框架（如 LangChain），都在教我们怎么给大模型塞满工具箱。你塞的工具越多，系统看起来越庞大。

但 MorroHsu 指出了这背后的致命逻辑错误：**工具选择的认知过载（Cognitive Load）。**

大模型每次行动前，都要在几十个有着不同数据结构（Schemas）的工具中艰难地做选择题：*“我到底该用哪一个？参数填什么？”* 上下文的注意力被极大地分散了，准确率直线断崖式下跌。

大佬的解法粗暴且优雅：**废弃所有花里胡哨的工具，只给大模型提供唯一的一个函数：run(command=”…”)。**

为什么？因为大模型天生就是个 Linux 高手！

大模型的训练语料库里，充斥着 GitHub 上数十亿行的代码、README.md 中的安装指南、以及 Stack Overflow 上的报错日志。这些语料中，密密麻麻全是 CLI 命令行。

如果你让它去调用你发明的 read_log_file(path) API，它还要去猜测你的参数定义；但如果你让它去找日志里的错误，它会凭着肌肉记忆毫不犹豫地写出：

run(command=”cat /var/log/app.log | grep ‘ERROR’ | tail -n 20″)

你看，CLI 本身就是大模型最熟悉的母语。**不要发明新的轮子去教大模型做事，直接把它最熟悉的世界交给它。**

## 50年前的“管道”魔法，完美解决了 Agent 编排难题

如果只有一个 run 命令，AI 遇到复杂任务怎么办？

这就引出了 50 年前 Unix 操作系统的伟大设计哲学：**一切皆文件。**

Unix 的先驱们设计了大量只做一件事的小工具（cat, grep, sort），然后通过**管道（Pipe |）**将它们串联成无比强大的工作流。

而这，完美契合了大模型的核心本质——大模型只能理解文本输入和文本输出！

在传统的 Function Calling 中，为了完成“下载数据 -> 过滤错误 -> 排序前 10 条”这个任务，你的 Agent 可能需要连续调用 3 个不同的自定义函数，经历 3 轮耗时极长的 LLM 推理，中间稍微错一步就满盘皆输。

但在 CLI 模式下，AI 只需要通过一次组合调用就能秒杀：

run(command=”curl -sL $URL | grep ’500′ | sort | head 10″)

这种强大的“组合编排能力（Composition）”，不是什么 AI 领域的最新黑科技，而是 Unix 管道原生自带的降维打击。

## 把大模型当人看，设计“防智障”导航系统

当然，光把命令行扔给大模型，它依然会因为瞎猜而犯错。MorroHsu 总结了三个极其硬核的实战设计技巧，教你如何打造一个“防智障”的 Agent 导航系统：

**绝招 1：渐进式发现（Progressive Discovery）**

不要一开始就把所有命令的长篇大论全塞给大模型，那会瞬间撑爆它的上下文窗口。

只要告诉大模型：*“你可以运行 run(“command”)。遇到不懂的，运行 command –help”*。

大模型其实非常懂得自我探索。当它发现报错时，它会自动去查阅说明书。这种“按需发现”的能力，极大地节省了宝贵的 Token。

**绝招 2：把报错变成“向导”**

这是最具启发性的一点！当大模型敲错命令时，千万别只返回一个冷冰冰的 exit code 127 或者 command not found。大模型无法像人类那样去 Google 搜索错误原因，它只会陷入瞎猜的死循环。

你必须在 stderr（标准错误输出）里加上向导信息。

传统报错：cat: photo.png: binary file

给 AI 的防智障报错：[Error] cat: photo.png is a binary image. Use ‘see photo.png’ instead.

不要试图阻止大模型犯错，而是要让它的每一次犯错，都成为指向正确道路的路标。

**绝招 3：双层架构（物理隔离幻觉）**

大模型的上下文是极其脆弱的。MorroHsu 分享了一个惨痛的真实案例：

一个用户上传了一张系统架构图，Agent 试图用 cat 命令读取它。结果 182KB 的乱码二进制字节流瞬间冲入了大模型的上下文。大模型当场“失了智”，开始不停地胡言乱语、重试、陷入死循环……足足浪费了 20 次推理的钱。

为了解决这个问题，必须在底层 Unix 执行和大模型展示层之间，建立一道**“二进制守卫（Binary Guard）”**和**“截断溢出守卫（Overflow Mode）”**。

当探测到命令输出超过 200 行，或者包含二进制乱码时，系统绝不把原数据返回给大模型，而是强制拦截并返回提示：

*“— 输出已截断。请使用 grep 或 tail 命令进行搜索。—”*

这就像给大模型戴上了一副防护眼镜，彻底杜绝了上下文被垃圾数据污染、导致智力下降的可能。

## 小结：化繁为简，才是架构的最高境界

目前，全网依然在乐此不疲地比拼谁的 Agent 框架更庞大、谁支持的 Tool Call 种类更多。但 原 Manus 大佬的这套“返璞归真”的血泪总结，给我们狠狠敲响了警钟。

**最前沿的 AI，其实最需要最古老的系统智慧。**

将 Unix 哲学的精髓（文本流、组合管道、小而美）与大模型的文本处理能力完美结合，放弃给 AI 制造复杂的隔离层和几十个脆弱的 API 接口，这才是真正属于“顶级工程师”的架构审美。

正如他在文末所言：“CLI 并非银弹，对于强类型校验和高安全性要求极高的场景，Typed API 依然不可或缺。**但在广袤的智能体自主探索宇宙中，命令行，就是大模型所需要的全部。**”

资料链接：https://www.reddit.com/r/LocalLLaMA/comments/1rrisqn/i_was_backend_lead_at_manus_after_building_agents

**今日互动探讨：**

你在写 Agent 时，是喜欢用框架提供的一大堆 Tool Calls，还是像这位大神一样，直接让大模型写代码/写命令去执行？在实战中你的 AI 发生过哪些最搞笑的“智障/幻觉”行为？

欢迎在评论区分享你的血泪避坑史！

还在为“复制粘贴喂AI”而烦恼？我的新专栏 **《 AI原生开发工作流实战》** 将带你：

- 告别低效，重塑开发范式
- 驾驭AI Agent(Claude Code)，实现工作流自动化
- 从“AI使用者”进化为规范驱动开发的“工作流指挥家”

扫描下方二维码，开启你的AI原生开发之旅。

![](../../assets/305ffd23f32ce780.png)


**原「Gopher部落」已重装升级为「Go & AI 精进营」知识星球，快来加入星球，开启你的技术跃迁之旅吧！**

我们致力于打造一个高品质的 **Go 语言深度学习** 与 **AI 应用探索** 平台。在这里，你将获得：

**体系化 Go 核心进阶内容:**深入「Go原理课」、「Go进阶课」、「Go避坑课」等独家深度专栏，夯实你的 Go 内功。**前沿 Go+AI 实战赋能:**紧跟时代步伐，学习「Go+AI应用实战」、「Agent开发实战课」、「Agentic软件工程课」、「Claude Code开发工作流实战课」、「OpenClaw实战分享」等，掌握 AI 时代新技能。**星主 Tony Bai 亲自答疑:**遇到难题？星主第一时间为你深度解析，扫清学习障碍。**高活跃 Gopher 交流圈:**与众多优秀 Gopher 分享心得、讨论技术，碰撞思想火花。**独家资源与内容首发:**技术文章、课程更新、精选资源，第一时间触达。

衷心希望「Go & AI 精进营」能成为你学习、进步、交流的港湾。让我们在此相聚，享受技术精进的快乐！欢迎你的加入！

![img{512x368}](../../assets/46c6ee234c360d9a.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2026, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论