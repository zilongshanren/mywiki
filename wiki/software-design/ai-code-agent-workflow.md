---
tags: [ai-coding, agent, workflow, c, 生产力]
date: 2026-04-19
sources: 1
---

# AI Code Agent 工作流（老程序员视角）

Daniel Hooper 2026 年初的实测日志：一名自述「编程 25 年、一直对 AI coding 嗤之以鼻」的 C 程序员，第一次把 Claude Code + Opus 4.5 用在自己的 *What The Fork* C 代码库上，得出一组与常见「vibe coding」鼓吹不同的结论。本页把他的结论拆成**有用的地方、失败的地方、和心态修正**三个部分，和 [[vibe-coding-workflow]]（Apoorva Joshi 的 agent-first 路径）形成对照——两个都基于真实项目，但调用 AI 的姿势几乎相反。

## 为什么这代 agent 与前几年不同

Hooper 列的三个结构性进步：

- **模型本身**（Opus 4.5、GPT-5.2-codex high）到了「能写不蠢代码」的门槛；
- **工具调用**：agent 能自己跑 build、读文件、grep 仓库，不再只是补全；
- **背景并行**：在网页版或 Linux VM 里挂几个 agent 同时跑不同任务，自己继续写代码。

这三者加起来让 auto-complete 这种「打断我阅读每个建议」的交互彻底过时。

## 实测结果

一个典型任务：**写 utf16 字符串类型 + utf16↔utf8 转换 + 审计现有字符串用法 + 重组受影响的类型**。自己干 4 小时，AI 辅助 30 分钟。这类**重复但费神、涉及多处修改**的活是 agent 的甜点。

失败模式也很清楚：

- 代码组织差（位置放错、模块边界糊）；
- **写 O(n²) 而非 O(n) 的算法**——而且 O(n) 的版本还更简单；
- 不会自发做二次优化。

但 agent 能响应**精确反馈**：Hooper 告诉它 "rewrite this in linear time"，它就改到 O(n)。Hooper 给自己的规则是：**最多一轮反馈，否则自己动手**——试图多轮纠正往往不如自己写。

## 正确的心态：键盘替代，不是大脑替代

Hooper 提出几条反「全包给 AI」的纪律：

1. **只让它做你知道怎么做的活**——未知领域用它当研究助理问「有哪些方案」、「tradeoff」、「相关论文链接」，不让它凭自己选择；
2. **Prompt 要具体**：`实现这个 feature` → **不要**；`把 user array 的查找换成 hashmap，并更新所有调用点` → **可以**；
3. **全部 review**——没有这步就不是「使用 AI」而是「把代码库交给 AI」；
4. **agent 做坏了时，读 diff 本身就有价值**——把问题加载进脑子，自己动手反而更快。

这条和 [[vibe-coding-workflow]] 的「先粗糙跑起来再迭代」刚好相反：Joshi 鼓励第一轮放手让它写全，Hooper 坚持第一轮就给精确命令。两者差异在**任务类型**：Joshi 的 tax calculator 有庞大对账测试做事后验证，Hooper 的 C 系统代码没有同级自动化 QA，只能前置控制。

## 意料之外的用法

**bug 分析**。Hooper 某处开放地址哈希集在插入 15 万条数据时冻结数秒，平均探测次数巨大。他自己怀疑 xor hash 有碰撞，换了几种算法没用。**并行让 Claude 看**——它的结论：不仅 xor hash 对当前输入有退化，更关键是最近一次改动让表允许填满到 100% 才 resize，退化成 15 万条的线性扫描。Hooper 自己写了几行修复。这类**诊断类任务**价值最高：比写 fix 的工作量大得多的是**理解 bug**。

**克服拖延**。把一直在推的活（例如「给交叉编译做一个 Linux sysroot」）扔给 agent 启动，最坏情况也把「从 0 到 1」的心理门槛翻过去了。

## 几个常见反驳的回应

- 「AI 写的代码我不懂自己的库」——所以要全部 review，且默认用「替换 X 为 Y」这种最小粒度 prompt；
- 「我喜欢编程不喜欢当 AI 经理」——把**敲键盘**的时间换给**数据/逻辑设计 + 规划 + 优化**，这是编程更有意思的部分，不是取代；
- 「这么能干为什么没看到 AI 做的产品」——已经有了，只是没人高调标注「由 AI 编写」；而且 AI 也不一定通过「产品更多」体现——可以是同样产品更少人做，或者同团队做更多 feature。

## 对老程序员的结论

> Current models are powerful but lack discernment, their greatest strength and greatest weakness is the same: they do what you tell them.

精确指挥能大幅提速，模糊指挥会烂。这与下指令给一个 intern 或律师的 paralegal 完全一样：**大脑规划留给你，机械劳作外包**。

## 相关

- [[vibe-coding-workflow]] — Apoorva Joshi 的反向做法：第一轮放手，用对账测试兜底
- [[good-software-no-double-check]] — agent 容易写出过度防御性代码的反模式
- [[automated-test-philosophy]] — Hooper 的精确-prompt 路线在缺自动化测试的场景下是必需的前置
- [[daniel-chase-hooper]]

## Sources

- [[sources/hooper-testing-ai-c]]
