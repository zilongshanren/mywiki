---
tags: [rendering, subsurface-scattering, bssrdf, offline-rendering, path-tracing]
date: 2026-04-27
sources: 1
---

# 次表面散射的工程实现（SSS Practical Implementation）

次表面散射（Subsurface Scattering，SSS）让光线穿透物体表面、在内部散射后从不同位置射出，是皮肤、蜡、玉石等材质真实感的关键。其数学描述从标准渲染方程扩展到 BSSRDF，增加了两个位置积分维度，使重要性采样比 BRDF 复杂得多。

## BSSRDF 基础模型

可分离 BSSRDF 将函数分解为三部分：入射 Fresnel 项、空间扩散剖面 `S_p(po, pi)`、出射 Fresnel 项。`S_p` 只依赖两点距离，与具体几何形状无关——称为"扩散剖面"（diffusion profile）。Disney 的近似扩散剖面（Generalized Burley）可以解析采样，有完美的重要性采样 PDF。

## 位置采样：盘投影法

PBRT 3 的标准方法：在着色点法线方向上方随机采样圆盘上一点，发出短光线找到物体表面交叉点。当几何体复杂时，一次短光线可能命中多个表面，PBRT 随机均匀选一个并用 `P_Disney × P_uniform(X|R)` 作为联合 PDF。

**问题**：`P_uniform` 是条件概率，高效的 Disney PDF 被低效的均匀选择稀释，容易在复杂几何内部产生极低 PDF 路径 → 萤火虫。

## 萤火虫消除：三项关键改进

**1. 相邻 SSS 退化为 Lambert**

若当前路径的上一弹射已经是 SSS，则当前交叉点改用 Lambert BRDF。这避免了光线在多层 SSS 几何体内部多次弹射，消除了绝大多数低概率逃逸路径。代价是引入微小偏差（bias），实践中几乎不可见。

**2. 评估所有交叉点**

在启用第一项优化后，每次采样的交叉点数目受控，可以对所有命中的交叉点全部求值（而非随机选一）。这消除了 `P_uniform` 的效率问题，在相同渲染时间内基本消除萤火虫。

**3. 移除内置 Fresnel，用 `S ≈ Sp/π`**

PBRT 在 BSSRDF 内硬编码 Fresnel，导致 mean free path → 0 时无法平滑退化为 Lambert（出现边界线）。改为 `S(po,pi,ωo,ωi) ≈ Sp(po,pi)/π`，可以证明当 mfp → 0 时 Monte Carlo 估计值恰好等于 Lambertian 反射，实现平滑过渡。

## 材质系统扩展

为支持 BSSRDF 与多种 BRDF 的自由混合，需将二者统一为"散射单元（Scattering Unit）"，用"散射事件（Scattering Event）"替代旧的 BSDF 结构，分别持有 BRDF 数组和 BSSRDF 数组。这样可以实现多层 SSS 混合（例如皮肤渲染中的多层扩散剖面）以及 SSS 与高光 BRDF 的叠加。

## 性能优化要点

- **K 近邻专用接口**：在 BVH/KD-Tree 等加速结构中实现一次性返回 K 个最近交叉点的接口，避免朴素做法的重复遍历，纯 SSS 场景性能提升约 14%
- **SSS 后不需要 MIS**：次级 BSDF 是 Lambert，无尖峰，只需对光源采样即可，省去一条 shadow ray
- **mean free path 为 0 时静默退化为 Lambert**：利用材质混合系统，可逐通道检测并跳过 SSS 评估

## Sources

- [[sources/graphics-guy-sss-practical-tips]]
