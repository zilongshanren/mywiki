---
tags: [source, constraint-solving, algorithms, wfc, procedural-generation]
date: 2026-04-27
sources: 1
---

# Arc Consistency Explained（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 8 月的技术文章，系统讲解弧相容（Arc Consistency）算法 AC-3 与 AC-4，以及它们在 WFC 约束求解器中的应用。

## 摘要

WFC 的底层是约束满足问题（CSP）求解器，其传播步骤依赖弧相容算法。文章从约束满足问题基础（变量、域、约束、表约束）讲起，定义**弧相容**：对某约束中变量 x 的值 a，若域内不存在任何 y 的值 b 使 (a,b) 满足约束，则 a 可从 x 的域中删除。AC-3（Mackworth & Mohr，1977）用工作列表驱动：每当某变量域收缩，将其相关弧加回列表，重复直至无值可删。AC-4（Mohr & Henderson，1986）则引入**支持计数**（support count）数据结构：为每个值维护其在约束中的支持对数量，支持计数归零时立即触发删除，避免 AC-3 每次都重新扫描全部候选对。Boris 指出 AC-4 在 WFC 实现中表现好，但初始化开销大，且回溯时需要恢复计数器，后续更新算法在此处有所改进。

## 关键要点

- 弧相容：删除域内不可能有支持的值，是 CSP 求解的传播核心
- AC-3：工作列表 + 按弧方向检查，简单高效，但每次重扫所有候选对
- AC-4：支持计数表，每次仅处理被删值的影响，理论上更快但初始化重
- Maintaining Arc Consistency（MAC）：将弧相容作为猜测-传播-回溯循环的传播步骤
- WFC 本质上就是 MAC 框架：Observation 步猜测，AC-4 传播约束

## 链接到的概念

- [[game-development/arc-consistency]]
- [[game-development/wave-function-collapse]]

## 原文

- 链接：https://www.boristhebrave.com/2021/08/30/arc-consistency-explained/
- 本地：`raw/articles/boristhebrave.com/2021-08-30_arc-consistency-explained.md`
