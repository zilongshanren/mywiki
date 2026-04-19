---
tags: [渲染, 路径追踪, 折射, 介质, ior, hyperion]
date: 2026-04-19
sources: 1
---

# 嵌套介质（Nested Dielectrics）

**Nested dielectrics**（Schmidt & Budge 2002）是路径追踪里处理「一个介质体套在另一个介质体里」的经典技巧：在每条 ray 维护一个 priority/medium 栈，ray 进入或离开 surface 时根据 IoR 与优先级决定当前介质是什么、该用什么折射法线。这在双面玻璃内装水、水下装气泡、冰里裹内容物等场景是标配。

## 学术版很简单

Yining Karl Li 2019 年在个人 hobby renderer [Takua](https://blog.yiningkarlli.com/2019/05/nested-dielectrics.html) 里实现过，相关博客把算法讲得很清楚。原始论文的栈式算法在玩具渲染器里几十行就能写完。

## 生产版的代价在别处

Zootopia 2 里 Nick、Judy、Gary De'Snake 穿过城市水管的序列，需要渲染「角色 → 水 → 双面玻璃 → 外部森林/城市环境」这样嵌套 4 层的几何。要做到艺术指导要求的效果，水管里真的建了水几何体（用于气泡、水花、浑浊度）。为此在 Hyperion 里把标准 nested dielectrics 改了一版。

工程难点不在算法本身，而在——

- **和生产渲染器一堆高级特性共存**：per-light AOV、光路改写、可见性 override、折射下的 [[path-guiding-production]] 都要能正确工作。
- **和 [[wavefront-path-tracing]] 架构配合**：介质栈要在 wavefront 调度下以紧凑形式存活。
- **性能与鲁棒性**：玩具渲染器的不会做的边角——ray self-intersection、极薄膜、同 IoR 相邻体——都要在实拍级体量下稳定。

## 相关

- [[hyperion-renderer]]
- [[wavefront-path-tracing]]
- [[path-guiding-production]]

## Sources

- [[sources/yiningkarlli-zootopia-2]]
