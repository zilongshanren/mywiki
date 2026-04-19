---
tags: [source, meta, ai-assisted, software-engineering]
date: 2026-04-19
sources: 1
---

# My transition to AI-driven software engineering（Chris Wellons / nullprogram）

[[chris-wellons]] 发表于 2026 年 3 月的文章，回顾离开旧雇主后完全转入 AI 驱动编码的工作方式，并以自己的 Quilt.cpp 项目为例拆解方法论。

## 摘要

作者 2026 年 2 月离职，加入一家积极采用 AI 的公司。他明确宣告“在职业工作中我已经不再亲手写代码”，角色像经理——协调一支由多个 AI agent 组成的团队。文章的技术重点在 [[quilt-cpp-ai-driven-clone|Quilt.cpp]]：一个约 9KLoC 的 Quilt 源码管理工具 C++ 克隆，内置 diff/patch，Windows 下 ~1.6MB 单文件 EXE，四天完成。方法论是 AI 先按原版文档与 man page 生成 conformance 测试套件并对原版验证，再由另一个 AI 写代码通过测试；用 `_GLIBCXX_DEBUG` 与 sanitizers 做护栏。作者解释为何选 C++ 而非 C：AI 写 C 仍会出 [[c-memory-safety-even-for-ai|内存安全问题]]，即便用 arena/slice 技术；C++ 里的 `std::from_chars` 等替代 libc 的做法让 AI 更不容易出错。还提到：“前沿 AI 对 CMake 非常强”，这促使他改变立场把 CMake 和 Ninja 加入 w64devkit。工具上个人用 Claude Code（吐槽 Anthropic 软件 Windows 支持糟糕，bug 多于行业平均），公司付费用 Cursor + GPT-5.4。规则：永远用最聪明的模型。

## 关键要点

- AI 协作的核心瓶颈从“写代码”变成了“表达需求”——steering problem
- [[ai-driven-conformance-clone|克隆既有工具的方法论]]：先让 AI 按文档生成对原版验证过的测试集，再另起 agent 让它过测试
- AI 在 C++ 上比 C 更可靠；即便配合 arena+counted string，AI 也写不好 C
- AI + CMake + CTest 是杀手组合：让 AI 闭环调试
- Claude Code 性价比高但 Windows 支持糟；Cursor 更健壮，公司愿付 ~$250/月
- 离开自建 agent 的想法：开源 agent 尚不够打；作者更新补充 OpenCode 可用
- “廉价 dumber 模型反而更贵，因为更多 token + 更多人工清理时间”

## 链接到的概念

- [[quilt-cpp-ai-driven-clone]]
- [[ai-driven-conformance-clone]]
- [[c-memory-safety-even-for-ai]]
- [[vibe-coding-workflow]]

## 原文

- 链接：https://nullprogram.com/blog/2026/03/29/
- 本地：`raw/articles/nullprogram.com/2026-03-29_null-program.md`
