---
tags: [渲染, 头发, 体积渲染, ray-marching, 实时, EGSR]
date: 2026-04-27
sources: 1
---

# 实时混合头发渲染（发丝光栅化 + 体积光线步进）

注意：本页描述 EGSR 2019 论文的**发丝/体积混合**方案，与另一个 [[hybrid-hair-rendering|延迟/前向混合头发渲染]] trick（Wronski，CD Projekt Red）是不同的技术路线，两者均使用"混合"一词但方向不同。

## 问题背景

头发渲染的规模问题在实时渲染中长期是挑战：人头超 10 万根，动物毛发超百万根。基于发丝的渲染（strand-based）在近距离质量高，但面对百万发丝时几何和着色开销极大；基于体积的渲染（volume-based）成本低，但缺乏发丝细节和精确的各向异性高光。

## Jansson et al. 的混合方案

[[matthaeus-chajdas|Chajdas]]、Jansson 等（EGSR 2019）将两种方法合并：

**直接可见部分（光栅化路径）**：正面、近距离的发丝直接光栅化，保留完整的发丝几何和各向异性着色。

**遮挡与 LOD 部分（体积路径）**：内部遮挡区域和远距离 LOD 退化后，用同一套体积数据结构做 ray-marching。体积表示是发丝密度场，不是显式几何。

**双重复用体积**：同一个体积表示不仅用于 LOD ray-marching，还被复用来实时计算**全局阴影**（发丝间自阴影）和**环境光遮蔽（AO）**。这是方案的核心价值之一——以预先构建体积的一次性代价，换取阴影和 AO 的近乎免费。

**无预处理**：体积可以在每帧从当前发丝状态实时构建，适合物理模拟驱动的动态头发。

## 与其他方案的对比

| 方案 | 优点 | 缺点 |
|---|---|---|
| 纯发丝光栅化 | 质量最高 | 百万根时几何开销爆炸 |
| 纯体积 ray-marching | 成本低 | 缺发丝细节、高光不准 |
| TressFX / AMD | 完整 forward OIT | 成本高，pipeline 侵入强 |
| **本方案** | 无预处理、drop-in、自阴影 AO | 近/远边界处理有复杂度 |

## 相关

- [[hybrid-hair-rendering]] — 不同的"混合"方案（延迟/前向管线层面）
- [[hair-shader-anisotropic]]
- [[matthaeus-chajdas]]

## Sources

- [[sources/anteru-realtime-hybrid-hair]]
