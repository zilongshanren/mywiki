---
tags: [渲染, 图像质量, 渲染哲学, 艺术指导]
date: 2026-04-27
sources: 1
---

# 图像质量哲学：少而精 vs 多而全

实时渲染领域存在两种对立的图像质量观。一种是**功能驱动**的思路：实现一张尽可能完整的技术清单（SSAO、SSR、体积雾、全局光照……），每加一项都是进步。另一种是**感知驱动**的思路：关注最终图像在正常观看条件下给人的感受，为此可以主动**减少**功能，但要确保每一处细节都达到自律的标准。

[[angelo-pesce]] 在分析《教团：1886》（*The Order: 1886*，Ready at Dawn，2015）时将第二种思路阐述得最为系统。这款游戏没有 SSAO，没有 SSR，没有常见的屏幕空间特效，却被普遍认为是那个时代图像质量最高的游戏之一——Pesce 认为这正是原因，而非尽管如此。

## 核心原则

**不能"看出来"是什么技术，是基本质量门槛。**

任何一项渲染技术如果让受过训练的眼睛能识别出它的实现方式，就已经失败了。可以说"这是景深"，但如果能说"这是 separable 高斯模糊的景深"，那已经是问题。同理，SSAO 在移动时的接缝、SSR 的边界淡出、EVSM 的 peter-panning——这些都是技术暴露自己的时刻。The Order 的设计选择是：与其付出工程代价让这些技术的缺陷不那么明显，不如直接不用它们。

**遮挡比光源更重要，漏光比缺光更糟糕。**

摄影中很早就有这个共识：加光很难，减光（让光不漏到不该漏的地方）反而是精准控制的关键。Specular 高光强度极高，AO 等无方向性方法无法有效遮挡它——因此 specular leaking 是图像质量最难隐藏的问题之一。Bent normals（弯曲法线方向烘焙到光照探针/法线图）是一种低成本的遮挡近似，其性价比往往高于增加更复杂的 realtime 遮挡方案。

**"稳定性"是被忽视的维度。**

抗锯齿讨论通常集中在边缘质量；但 The Order 的图像稳定性来自整体协作：4× MSAA、后处理管线对剩余 shimmering 的主动压制（motion blur 有时甚至充当 specular shimmer 的"掩蔽者"），以及对所有频率的一致态度——能超采样的就超采样，无法超采样的就移入噪声。

**Baking 仍有不可替代的价值。**

用 realtime 方案替换 baked 解法来解决 authoring 问题是一种方向性错误：authoring 问题应当由更好的工具解决，而非在运行时做不必要的计算。对于场景静态部分，baked lightmap + probe 组合依然是精度/成本比最高的选项。

## 与 Forward+ 的关系

The Order 基于 Forward+ 引擎（[[forward-plus-rendering]]）。Pesce 注意到，专门针对 PS4 优化的 Forward+ 管线与"旧世代 + 若干高端 PC 特效"的组合相比，在质量上反而更统一——因为每个子系统都在同一个假设集上设计，没有为旧硬件兼容而引入的妥协。这支持了一个更广泛的结论：平台专属性（目标明确）比功能数量更能推动图像质量。

## 相关

- [[realtime-quality-vs-quantity]] — 质量 vs 数量的更一般讨论
- [[forward-plus-rendering]] — The Order 所用管线
- [[atmospheric-perspective]] — 大气散射作为"场景角色"
- [[physically-based-shading]] — PBR 材质自律的反面教材（金属过度应用）
- [[rendering-perception-psychology]] — 感知驱动渲染的认知科学背景
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-order-1886-rendering]]
