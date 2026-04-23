---
tags: [source, bitsquid, productivity, workflow]
date: 2026-04-19
sources: 1
---

# 5 Tips for Programmer Productivity（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2012 年 1 月的短文，列出 Bitsquid 日常里他认为收益最高的五条程序员纪律。

## 摘要

五条都可以从成本收益角度推理，不是空洞劝告：(1) **Now-principle**——5 分钟以内的事立刻做，因为记下来、重排、重建上下文的开销比直接做还大；(2) **修病根不是修症状**——改 error message、加 assert、把被问到的用法写进文档，让同类问题不会重来；(3) **编译等停顿期不要切 context**——刷邮件、看网页比专注还累；用独立编辑器做相关的轻任务（补文档、review、规划）；(4) **版本控制比你以为的还该用**——配置、第三方库、sample code 全部 check in，分布式 VCS 之后建仓成本几乎为零；(5) **监控构建**——持续在所有平台 × 配置构建所有可执行，出问题第一时间知道；脚本也算 build server，存在比完善重要。

## 关键要点

- Now-principle 是 GTD two-minute rule 的工程师版，门槛放到 5 分钟。
- "修病根" 在工程上就是 [[warnings-as-errors-strategy|warning→error]] 与 [[zero-tolerance]] 的日常动作。
- 停顿期微分心破坏心流——独立编辑器是个小但关键的工具选择。
- 第三方库 check in：魔改可见、上游合并可追、patch 文件能直接发 bug report。
- Build server 在 "存在" 就有价值，先有 shell 脚本后有 Jenkins。

## 链接到的概念

- [[now-principle-productivity]]
- [[zero-tolerance]]
- [[strategic-programming]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/01/5-tips-for-programmer-productivity.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-01-05_5-tips-for-programmer-productivity.md`
