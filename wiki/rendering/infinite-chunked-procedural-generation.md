---
tags: [程序化生成, 无限世界, 分块算法, 确定性]
date: 2026-04-19
sources: 2
---

# 无限世界的分块程序化生成

Boris The Brave 围绕 Sylves 的「无限程序化生成」系列，反复打磨的一个核心要求：给定一个无限大的程序化生成规则，能否**按 chunk 求值**，同时保证最终结果**不依赖**于 chunk 划分方式？这是无限开放世界、无限地图工具、以及 WFC 类求解器工程化时躲不过去的问题。

## 约束

天真的「一次生成一个元素、全局判重」做法在无限域失败，因为没有全局顺序可供遍历。想把问题工程化，三件事必须成立：

- **确定性**：同一坐标处的输出只取决于坐标本身（以及全局种子），与先算哪块、后算哪块无关。
- **局部依赖**：一个 chunk 的输出只能依赖**有限多**个邻近 chunk——否则没法按需延迟求值。
- **可并行**：chunk 之间没有串行写入的依赖环。

## 技术组合

Boris 的实际做法是把算法**相 (phase) 化**。每个 phase 的 chunk 独立求值；下一个 phase 的 chunk 只依赖若干相邻的上一 phase chunk。这种「局部有界依赖」是整个套路的骨架。几个具体实例：

- **无限均匀点分布**：基于坐标哈希的 [[probabilistic-algorithms|泊松点过程]]——每个 chunk 内采样一批点，密度和分布都与 chunk 大小无关。
- **[[poisson-rect-process]]**：在点过程基础上赋矩形和 sort order，再按「局部最大保留」过滤，得到无重叠随机矩形铺层。
- **Infinite Modifying in Blocks**（同一思路的更早表述）：先独立生成，再按邻域规则后处理。

通用模板：**Phase 1 独立生成候选；Phase 2 按有限邻域裁剪**。只要候选的「最大影响半径」有上界，Phase 2 就能按 chunk 走。

## 工程意义

这类算法让「无限世界」可以做成纯函数式查询 `f(coord) -> value`——viewport 移动时只要把暴露出来的新 chunk 求值一下。它也是 Sylves 把 [[poisson-disk-sampling]]、WFC、布局生成等工具搬到**无限域**上的底层技术路线。

## Sources

- [[sources/boristhebrave-infinite-grids]]
- [[sources/boristhebrave-poisson-rect-process]]
