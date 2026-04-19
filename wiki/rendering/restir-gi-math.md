---
tags: [渲染, 全局光照, 路径追踪, 实时光追, ReSTIR, 采样]
date: 2026-04-19
sources: 1
---

# ReSTIR GI 的数学：Primary Sample Space 与路径 initial candidate

ReSTIR GI（NVIDIA 2021）把 [[restir-di-math|ReSTIR DI]] 的时空复用思想推广到全局光照。[[graphics-guy-notes|Jiayin Cao]] 在 Zorah（RTX 50 demo）里和 Daqi Lin 一起把 ReSTIR PT（后续的路径级泛化）实装进 NvRTX 版 Unreal Engine，随后写了 "Understanding The Math Behind ReSTIR GI" 补齐几处论文里一笔带过的关键细节。本页归拢其中数学要点。

## Primary Sample Space (PSS)：把积分换到单位超立方体

GI 比 DI 复杂的根本原因是 `L_l(ω_i)` 没有闭式解——渲染方程在间接光上是无限维积分。要在不同 domain 间迁移样本，PSS 是必要工具：

每个 Monte Carlo 样本都源于一组 `u_i ∈ [0,1)`，再由 sampling PDF 映射成 `x_i`。于是可以把

$$\int f(x) \, dx \approx \frac{1}{N}\sum \frac{f(x_i)}{p_x(x_i)}$$

重写为在单位立方体上对 `f(x(u))/p_x(x(u))` 的积分。**结论**：原域积分与 PSS 域积分在 MC 估计器下等价，这是 ReSTIR GI 能把邻居像素的路径"搬到"当前像素的理论基础。

## Per-Initial-Candidate Target Function

论文里不起眼的一条：**RIS 的每个初始候选可以使用不同的 target function**，推导显示无偏性不依赖 target function 的一致性。这条性质对 ReSTIR GI 非常有用——邻居路径与本像素路径的 shading context 不同，天然会用不同 target function。顺带还解释了 [[restir-di-math|ReSTIR DI]] 里 visibility reuse（前半段无阴影 target、后半段阴影 target）为何合法。

## Initial Candidate 到底是什么：不是"路径树"那么简单

把 GI 的渲染方程按 bounce 数拆成 `L_k`（长度恰为 k 的路径贡献），则

$$L_{GI} = \sum_{k\ge 2} L_k$$

一个朴素想法：把 initial candidate 定义成**整棵路径树**（长度 2 到 M_max 的所有路径集合），对应的 proposal PDF 就是产生整棵树的 PDF。但这里有陷阱：路径树中 k 阶路径与 k+1 阶路径**高度相关**（k 阶是 k+1 阶的前缀），因此"整棵树的 PDF"不是各条路径 PDF 的简单乘积。

作者在 GRIS 框架下把它讲清楚：initial candidate 应视为一条路径的最长形式（因为共享前缀），resample 时使用 **shift mapping**（把邻居路径搬到当前像素的积分域）并附带 **Jacobian 修正**。这样做既保持 O(M) 的路径生成成本，又在数学上落入 GRIS "允许不同 domain 的 RIS" 框架。

## Target Function 选择

论文提了两种 target function：

1. `L(x_2 → x_1)`——从二阶 bounce 返回的 radiance；
2. `L_l(ω_i) f(x_1, ω_i, ω_o) cos θ_i`——完整 shading 项。

两者都满足无偏性要求，差别在于收敛速度。选择更有效的 target function 通常需要同时权衡 evaluate 成本与与真实 integrand 的匹配程度。

## 典型 ReSTIR 结构（DI/GI/PT 通用）

- Initial sampling：按场景相关的 proposal PDF 产生候选（DI 是光源点，GI 是一条后续路径，PT 是 path tree 里的一条 selected path）。
- Temporal resampling：合并上一帧对应像素的 reservoir。
- Spatial resampling：若干轮合并邻居 reservoir。
- Final evaluation：用选出的高质量候选 + UCW（unbiased contribution weight）算最终贡献。

ReSTIR 的结构性强到可以套用在任何具有时空相干性的采样问题上——不必是图形。

## Zorah 的工程背景

Zorah 是 NVIDIA RTX 50 旗舰 demo，在 NvRTX 版 UE 里跑 ReSTIR PT。Greenhouse 等关卡的所有间接光 bounce 都在实时路径追踪中动态求值。代码位于 NvRTX experimental branch（启用 Megageo = Ray Traced Nanite）。

## Sources

- [[sources/graphics-guy-restir-gi-math]]
