---
tags: [source, 渲染, 法线贴图, derivative-map, 性能]
date: 2026-04-27
sources: 1
---

# Derivative Maps vs Normal Maps（Rory Driscoll / CodeItNow）

[[people/rory-driscoll]] 发表于 2012 年 1 月的基准对比文章，在 AMD Radeon 6750M 上实测 derivative map 与 normal map 的质量、性能和内存消耗。

## 摘要

文章使用预计算导数贴图（PD map）与传统法线贴图做对比，排除了 `ddx`/`ddy` 方案的质量问题。质量上两者极为接近，normal map 可能保留略多细节，但 derivative map 已达到可用水准。性能测试在延迟渲染 G-buffer pass 中进行：无扰动 1.08 ms、normal map 1.37 ms、derivative map 1.36 ms，差别几乎可以忽略；其中 derivative map 多出的 5 条 ALU 指令被少一个顶点插值器的带宽节省大致抵消。内存方面，由于省去了切线向量，测试顶点格式节省约 27% 的网格空间。文章还报告了一些视觉 artifact，后续确认是 mipmap 生成 bug 与 FXAA 叠加导致，非 derivative map 本身的问题（见后续 artifact 文章）。

## 关键要点

- 帧时：NM 1.37 ms，DM 1.36 ms（AMD 6750M，shader model 5）
- DM 有 9 条纹理指令（NM 有 4 条），但 5 条 ddx/ddy + resinfo 几乎免费（与 ALU 并行）
- DM 只额外多 5 条 ALU 指令，被插值器减少抵消
- 网格内存节省 ~27%（省去 tangent 向量）
- 当时报告的 artifact 后来定位为 mipmap 生成 bug，与 DM 无关

## 链接到的概念

- [[rendering/derivative-map]]
- [[rendering/tangent-space-normal-mapping]]
- [[rendering/compact-vertex-format]]

## 原文

- 链接：https://www.rorydriscoll.com/2012/01/15/derivative-maps-vs-normal-maps/
- 本地：`raw/articles/rorydriscoll.com/2012-01-15_derivative-maps-vs-normal-maps.md`
