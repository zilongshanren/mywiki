---
tags: [渲染, 移动gpu, 优化]
date: 2026-04-05
sources: 1
---

# HSR（Hidden Surface Removal）

**TBDR 架构特有的精确隐面消除**，在 tile 粒度做，能**完全消除 tile 内 overdraw**——前提是不被破坏。

## 工作原理

TBDR 处理 tile 时，把该 tile 的所有三角形收集到片上内存后，用精确深度比较**只保留每个 pixel 的最前 fragment** 进入 fragment shader。

## Early-Z 与 HSR 的区别

| | Early-Z | HSR |
|---|---|---|
| 架构 | 所有 GPU | 仅 TBDR |
| 粒度 | 逐 fragment | 逐 tile |
| 保守性 | 保守（hierarchical z） | 精确（逐像素） |
| 效果 | 剔除大部分 | **几乎完全消除** overdraw |

## 破坏 HSR 的代价

一个 `discard` 就可能让 HSR 完全失效——**TBDR GPU 从 1× 恢复到 4× overdraw 代价**。

草地用 alpha test cutout 是经典反面教材——**4× 性能损失**。替代方案：
- Alpha-to-Coverage
- 先 opaque pass + 后 alpha blend pass 分开
- 用短板几何替代 alpha cutout

## 实战建议

移动端优先级：
1. 从前往后排序渲染。
2. 避免 discard / alpha test。
3. Depth Pre-Pass 若 HSR 失效时的 backup。
4. 减少 fragment shader 的动态分支。

## 相关

- [[tbdr-vs-imr]]
- [[early-z-late-z]]
- [[overdraw]]
- [[fragment-shader]]

## Sources

- [[sources/rtr-day05]]
- [[sources/c0de517e-tiled-hardware-speculations]] —— Pesce + ryg 讨论 alpha test / programmable blending 在 TBDR 上的真正开销
- [[sources/gameknife-tbdr-performance-tuning]] —— PowerVR HSR 与 discard/alphaTest/alphaToCoverage 破坏机制的经典描述
