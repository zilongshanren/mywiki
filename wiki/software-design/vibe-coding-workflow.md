---
tags: [ai-coding, agentic, workflow, testing]
date: 2026-04-19
sources: 1
---

# Vibe-coding Workflow

「Vibe-coding」是 2025-26 间兴起的一个描述性词：用 AI 代理（Claude Code、Cursor Composer、Aider 等）完成大部分代码编写，人类主要承担**方向、审查、测试设计**。本页把 [[apoorva-joshi]] 的 *Vibe-coding a Tax Calculator* 总结为一份可复用的工作流清单。

## 核心节奏

1. **起步用 plan mode**——把功能描述到「AI 能直接开干」的粒度，让它一次性做出草稿；抗拒在第一轮就过度审查；
2. **草稿先运行**——不试图在第一遍就合格，改后端比改前端便宜；
3. **一旦 AI 诊断出 bug，立刻让它在同一会话里写测试**——此时上下文最厚，换会话就要重新解释；
4. **以 PR 粒度 review，不以 commit 粒度**——开 sandbox 的 auto-allow，让 AI 把整个 feature 做完再看；
5. **把对账和整合测试当成 QA 核心**——Joshi 在 tax 项目上搭了 25,000 个测试用例 + 真实工资单对比。

## 为什么「AI 诊断 bug → 立刻写测试」特别重要

调 bug 时的上下文往往是临时构建的（查日志、读 stack、复现、定位 root cause）。这些信息在下一个会话全部消失。在 bug 刚被理解的窗口里写下测试，本质上是**把易失上下文固化为持久资产**。这和 TDD 的「先写测试再实现」不同——它是「先修复，立刻为修复写测试」，属于 regression prevention 的自动化版本。

## 瓶颈转换

传统开发里，写代码快意识里占比很高。Agentic 之后瓶颈迁移到：

- **任务定义**（说清楚要做什么）；
- **架构判断**（这个方案是否合理）；
- **代码审查**（catch AI 犯的偶然愚蠢）；
- **测试设计**（验证是否真对）。

所以 Joshi 说「我想的更多是 architecture 和 correctness，而不是 syntax」。这对「人工作方式」的影响大于工具本身。

## 与 [[automated-test-philosophy]] 的共振

[[evan-todd]] 的 *Testing that Works* 主张：优秀的测试不是 100% 覆盖而是「能抓到真的 regression 的测试」。vibe-coding 场景下这一条更激烈——AI 随时可能引入它自信但错的代码，**测试是最可靠的防线**。Joshi 和 Todd 的工作流共用同一条核心假设：**bug 先出现，测试紧跟固定**。

## 与 [[tactical-programming]] vs [[strategic-programming]] 的关系

Ousterhout 的 *APoSD* 把「短期见效」和「长期干净」对立。vibe-coding 天然偏 tactical：AI 做最小可行版、补测试、迭代。但因为 AI 的复用成本极低，可以用「再写一版」替代「早期架构投入」——tactical 的失败模式（复杂度累积）在 AI 辅助下稍有缓解，但也带来新的失败模式（AI 写的代码没人完全理解）。

## Sources

- [[sources/apoorvaj-vibe-coding]]
