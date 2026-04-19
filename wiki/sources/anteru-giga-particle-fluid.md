---
tags: [source, 渲染, 粒子, 流体, 光线投射, 体渲染]
date: 2026-04-19
sources: 1
---

# Interactive Rendering of Giga-Particle Fluid Simulations（HPG 2014）

Reichl、[[matthaeus-chajdas|Chajdas]]、Schneider（KAUST）、Westermann（TUM）发表于 **High Performance Graphics 2014** 的论文。目标：**每时间步几亿粒子的流体模拟**的交互可视化。

## 摘要

作者描述一套粒子基流体模拟的交互渲染系统，单时间步支持数以亿计的粒子。核心贡献：

1. **二值体素表示 + 随机抖动**：粒子位置用 binary voxel 存，加上随机 jitter 大幅降低内存和带宽开销。
2. **构造嵌入在 front-to-back GPU ray-casting 里**：避免耗时的预处理，工作量被限制在"视线实际看到"的范围。
3. **高速渲染**：对球体做 ray-cast，并把 total-variation-based image de-noising 模型扩展用于按边界条件对流体表面做平滑。
4. **规则体素结构**使 ray-sphere intersection 和 **foam particle 分类**都能在 GPU runtime 高效完成；foam 粒子通过从 binary 表示重建密度，做**体渲染**。

系统设计允许**scrub 高分辨率动画流体**在交互帧率下。

## 关键要点

- **binary voxel + jitter** 替代常规 SPH particle grid：几亿粒子可压缩到可渲染的内存预算。
- **front-to-back ray-cast 和数据结构构造融合**：免去一次全场预处理 pass。
- **total-variation de-noising** 用作流体表面平滑的规范——把图像处理里经典的各向异性扩散思路搬到体表面重建。
- Foam 粒子走**体渲染**而非几何化——这个"同一份粒子，主体 surface + 外围 volumetric"的分层思想后来在游戏水体（如 UE Niagara fluid）也常见。

## 链接到的概念

- [[matthaeus-chajdas]]

## 原文

- 链接：<https://anteru.net/research/interactive-rendering-of-giga-particle-fluid-simulations>
- 项目页：<https://www.in.tum.de/cg/research/publications/2014/interactive-rendering-of-giga-particle-fluid-simulations/>
- 本地：`raw/articles/anteru.net/2025-02-16_interactive-rendering-of-giga-particle-fluid-simulations.md`
