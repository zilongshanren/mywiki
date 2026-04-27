---
tags: [渲染, 球谐, 面光源, LTC, 镜面反射, 实时渲染]
date: 2026-04-27
sources: 1
---

# 线性变换球谐（LT-SH）

**线性变换球谐（Linearly Transformed Spherical Harmonics，LT-SH）** 是一种用于在实时渲染中计算**多边形面光源高光分量**的技术，由 Jan Allmenröder 在 Christoph Peters 的指导下研究完成（学士论文，2020）。

## 核心思路

LT-SH 的出发点是两项先行工作的组合：

1. **Laurent Belcour（2017）**的多边形 SH 积分方法——将球谐展开在多边形立体角上积分，得到一个封闭形式的表达式。
2. **线性变换余弦（LTC）**——通过一个线性变换把任意 BRDF lobe 映射到可解析积分的余弦 lobe 空间，是目前实时面光源渲染的主流方法之一。

把两者结合：将 SH 展开通过与 LTC 类似的线性变换来近似任意形状的 specular lobe，再对多边形作解析积分。结果中，**每个 SH 系数的贡献可以分别积分，然后与旋转后的 BRDF 系数逐项相乘**，给出比纯 LTC 更高的高光重建质量。

## 与 LTC 的对比

| 维度 | LTC | LT-SH |
|---|---|---|
| 质量 | 中等，高光形状近似 | 更高，SH 系数捕捉更多细节 |
| 性能 | 实时可用 | 当前实现明显更慢 |
| 实现复杂度 | 低 | 高（依赖 Falcor 框架演示代码） |

## 局限与现状

截至 2020 年，LT-SH 尚处研究阶段，未见商业引擎采用。其主要瓶颈是性能：SH 系数需要为每个多边形灯预计算，运行时的积分和乘法开销高于 LTC。如何将其降到实时可用范围，仍是开放问题。

## 相关

- [[spherical-harmonics]] — SH 基础理论
- [[spherical-integration]] — 球面积分框架
- [[physically-based-shading]] — 面光源渲染的大背景
- [[projected-solid-angle-sampling]] — 同为 Peters 研究线的立体角相关工作

## Sources

- [[sources/peters-lt-spherical-harmonics]]
