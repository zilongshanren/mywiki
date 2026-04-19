---
tags: [source, software-design, ai-coding, workflow]
date: 2026-04-19
sources: 1
---

# Vibe-coding a Tax Calculator（Apoorva Joshi）

[[apoorva-joshi]] 2026 年 2 月的短文反思。他用 Claude Code（Opus 4.6）两个晚上做出 [taxman.dk](https://taxman.dk) 这个丹麦税计算器，并分享 AI agentic coding 时的工作哲学。

## 摘要

作者先交代起因：丹麦税规则复杂（利息扣除、养老金贡献），网上没有好用的计算器，就自己写。在 Claude Code 里用 plan mode 描述高层需求，让 AI 一次性打出草稿，然后在后续对话里逐步加测试、修 bug。他总结了几条方法论：

1. **AI 断出 bug 当下就让它写测试**——此时上下文最丰富，换个会话就要重新 explain；
2. **开 sandbox + auto-allow**——把审查粒度从 per-commit 抬高到 per-PR，让自己能做其他事；
3. **瓶颈是人的注意力**——只要不是撞到模型能力天花板，应该把自己的时间用在架构与正确性审查、而不是看每行代码；
4. **25,000 个测试用例 + 工资单对账**——严肃 QA 让 vibe-coded 代码能真用。

他的感受句是：「两个晚上做完；没有 AI 我不会做这个，倒不是难，是这投入产出比换不回来。AI 把这个计算改变了。」

## 关键要点

- **AI 适合 scaffold + 单元执行**，不适合 judge 全局架构——后者仍是人的工作。
- **在 AI 发现 bug 的瞬间让它同时写测试**——context window 的短期记忆是最贵的资产。
- 从「每 commit review」切到「**每 PR review**」是高 agentic coding 的关键节奏调整。
- 真正让「vibe-coded」可用的不是 AI 多聪明，而是**大量测试 + 真实对账**。

## 链接到的概念

- [[vibe-coding-workflow]]
- [[automated-test-philosophy]]

## 原文

- 链接：https://apoorvaj.io/vibe-coding-a-tax-calculator
- 本地：`raw/articles/apoorvaj.io/2026-02-13_vibe-coding-a-tax-calculator.md`
