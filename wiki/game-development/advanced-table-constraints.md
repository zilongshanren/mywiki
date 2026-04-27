---
tags: [constraint-solving, algorithms, wfc, procedural-generation, game-development]
date: 2026-04-27
sources: 1
---

# 高级表约束算法

高级表约束算法是 [[game-development/arc-consistency]] 技术的进阶扩展，核心目标是高效处理覆盖**多个变量**的广义弧相容（Generalized Arc Consistency，GAC）问题。在 WFC 等约束驱动生成器中，当约束从"相邻两格兼容"扩展到"某区域内必须满足特定模式"时，二元弧相容已不足够，需要 GAC 算法族的支持。

## AC-5 通用框架

AC-5 最重要的贡献不是一个具体算法，而是对算法结构的抽象：通过替换三个抽象操作（`Initialize`、`ArcCons`、`LocalArcCons`），可以在同一个主循环框架下派生出 AC-3、AC-4 乃至更高级的算法。这种分离让算法分析更清晰，也让实现可以按需组合。

粗粒度（coarse）算法在每次调用时重扫全部值，不使用局部变化信息；细粒度（fine）算法则仅处理"被删除的具体值"，将增量更新负担精确绑定到实际变化量。二者的优劣因问题特性而异：粗粒度在约束条件频繁变化时反而更高效，因为维护增量结构的开销可能超过重扫的代价。

## 可逆数据结构与回溯

约束求解器通常嵌套在回溯搜索中，这意味着任何算法存储的数据结构都必须支持高效的状态回退。主要策略有四种：全量复制（仅适用于极小规模）、持久化数据结构（少见）、设计成回溯后天然有效的结构、以及 **trailing**（记录每次修改以便逆序撤销）。

**Sparse Set** 是最典型的可逆结构：用两个互为逆映射的数组（`Dyn` 与 `Map`）加上一个 `Size` 指针存储集合。删除一个元素只需将其与 `Dyn[Size-1]` 互换并将 `Size` 减一；回溯时仅需恢复 `Size`，`Dyn` 和 `Map` 无需改动。

## 主要算法谱系

| 算法 | 类型 | 核心思路 |
|---|---|---|
| AC-3 | 粗粒度 | 循环扫描所有值和约束 |
| AC-4 / GAC4 | 细粒度 | 支持计数 + 静态有效元组列表 |
| GAC2001 / GAC3rm | 粗粒度 | 每个值存一个（最小）有效元组作为"残差支持"，避免重扫 |
| AC-6 | 细粒度 | 每个值存最小有效元组，以另一变量的值为索引建立逆向索引 |
| STR2 | 粗粒度 + 广义 + 动态 | Sparse Set 管理有效元组列表，运行时删除失效元组 |
| STR3 | 细粒度 + 广义 + 动态 + 索引 | STR2 + AC6 + watched literals，达到路径最优过滤 |
| MDDc | 粗粒度 + 广义 + 压缩 | 多值决策图（MDD）存储约束，Sparse Set 增量遍历 |

STR3 被 Boris 认为是最值得在 [[game-development/debroglie-wfc-library]] 中集成的算法，因为它在已有细粒度通知机制的基础上只需较小改动，且实现出奇地简单。

## Sources

- [[sources/boris-advanced-table-constraints]]
- [[sources/boris-arc-consistency]]
