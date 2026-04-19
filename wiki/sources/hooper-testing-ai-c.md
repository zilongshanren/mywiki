---
tags: [source, ai-coding, agent, c]
date: 2026-04-19
sources: 1
---

# Testing AI For C Programming（Daniel Hooper）

[[daniel-chase-hooper]] 2026 年 1 月的文章，一个自述「编程 25 年、此前一直不屑 AI coding 炒作」的 C 程序员，第一次在自己的 *What The Fork* 代码库上系统测试 Claude Code + Opus 4.5，给出与「vibe-code 万能派」不同的结论。

## 摘要

作者把 agent 当作「可以替代键盘但不能替代大脑」的工具：只在自己已经知道怎么做的任务上用它省打字时间，未知领域用它做研究助理（「有哪些选项」「tradeoff」「给我论文链接」）。最成功的 case：写 utf16 类型 + 转换 + 审计用法 + 重组类型，自己 4 小时，AI 辅助 30 分钟。最让他意外的使用法是**bug 诊断**——15 万条数据往开放地址哈希集插入时冻结，他怀疑 xor hash，换算法都没用；把问题扔给 Claude 并行分析后，agent 指出真正原因是最近一次改动让表允许 100% 填满才 resize，退化成线性扫描。Hooper 自己写了几行 fix。文章也点名 agent 的弱点：代码组织差、偶尔写 O(n²) 而非同样简单的 O(n)——但能响应精确反馈一次修复。他的纪律是「最多一轮反馈，否则自己写」。结尾回击三条常见反驳（不懂自家库、不想当 AI 经理、没看到 AI 做的产品），并以「do what you tell them」概括 agent 的根本性质。

## 关键要点

- 三个结构性进步让这代 agent 不同：模型质量、工具调用、背景并行
- 甜点任务：重复但费神的机械劳作（类型重构、字符串审计）
- 失败模式：代码组织差、O(n²) vs O(n) 的算法选择
- 最多一轮反馈原则——超过就自己写
- Bug 诊断价值最高：找 bug 原因比写 fix 更费时间
- 宜使用的 prompt 粒度：`把 user array 改成 hashmap 并更新调用点`，不是 `实现这个 feature`
- 与 [[vibe-coding-workflow]] 的 Joshi 路线对照：Hooper 前置控制，Joshi 后置测试兜底
- 背景 agent 心法：复制项目目录 × N，每个 agent 推自己的分支

## 链接到的概念

- [[ai-code-agent-workflow]]
- [[vibe-coding-workflow]]
- [[good-software-no-double-check]]
- [[automated-test-philosophy]]

## 原文

- 链接：<https://danielchasehooper.com/posts/code-agents/>
- 本地：`raw/articles/danielchasehooper.com/2026-01-07_testing-ai-for-c-programming.md`
