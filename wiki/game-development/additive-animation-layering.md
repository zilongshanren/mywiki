---
tags: [animation, additive-blend, game-development, unity, uncharted]
date: 2026-04-19
sources: 1
---

# 叠加式动画层（Additive Animation Layering）

角色动画中一种以少量"基底动画 + 长周期叠加动画"的方式，用很低的存储成本换取看起来长而不重复的外观。Naughty Dog 在 *Uncharted: Drake's Fortune* 与 *Uncharted 2* 的 GDC 2010 动画讲座中公开了这一做法，Rune Skovbo Johansen 在 [[sources/runevision-gdc2010-animation|GDC 现场笔记]] 中复述并点评了它在 Unity 中的可复现性。

## 核心手法

基底是一帧的"静止姿态"（1-frame idle），看上去就像角色定格不动。在它之上以加法混合（additive blend）叠一段长达数十秒、随机摆动（wiggling）的全身或部分骨骼动画。因为加法层只编码**相对位移**，它不绑定到特定 idle；同一段 wiggle 可以复用在不同的 1 帧 idle、walk、run 之上，于是只用一份长周期数据就把所有"站姿/走姿"都变活了。

这是一种典型的**空间换观感**反向优化：传统做法是给每个状态都做一段几秒的循环动画，容易被眼睛识破重复；加法层让你把"重复周期"拉长到只有上层 wiggle 那么长，而下层仅占一帧。与 additive 结合的还有部分骨骼混合（partial skeleton blend）——上半身瞄准叠加下半身移动——以及 IK 的脚部修正，这些在 Unity 的 [[animation-blending|动画混合]] 体系里都能直接实现。

## 与 Locomotion / 足部贴地

Johansen 顺带指出，Uncharted 的脚部贴地处理与他自己的 Unity Locomotion System 类似：发射 raycast 找到地面高度，调整骨盆 / 根节点高度，再用 IK 收脚。这说明即便是 3A 工作室，站到不平地面上的角色动画，也靠的是工程上直截了当的几何求交 + IK 二段式方案，没有更花哨的数学。

## Sources

- [[sources/runevision-gdc2010-animation]]
