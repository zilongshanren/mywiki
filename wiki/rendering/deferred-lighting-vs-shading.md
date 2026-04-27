---
tags: [渲染, 延迟渲染, deferred-lighting, g-buffer, 光照, 带宽]
date: 2026-04-27
sources: 1
---

# Deferred Lighting 与 Deferred Shading 的区别

**Deferred Shading** 和 **Deferred Lighting**（又称 Light Pre-Pass）同属延迟渲染家族，但光照和材质的耦合方式不同，导致带宽消耗、光源数量上限和材质复杂度潜力上的明显差异。

## 核心区别

在标准 [[deferred-rendering|Deferred Shading]] 中，G-Buffer 写入完整的材质属性（albedo、法线、roughness、metallic、AO……），光照 pass 一次性读入所有材质信息并输出最终颜色。光照和材质计算在同一 pass 发生，无法分离。

Deferred Lighting（Light Pre-Pass）把管线拆成三段：

1. **几何 pass**：只写最小 G-Buffer——深度、法线（含高光信息），不写 albedo。
2. **光照 pass**：只读深度 + 法线，输出 diffuse/specular 强度到独立的 light/shadow buffer；此 pass 完全不涉及材质颜色。
3. **材质 pass**：重新提交几何，将 albedo 与 light buffer 相乘，同时可以在此 pass 用全部材质属性做复杂着色（皮肤、车漆、布料等）。

## 带宽与光源数量

在 XBOX 360 / PS3 时代，每帧为每个光源读取 G-Buffer，G-Buffer 体积直接决定可用光源数量。Deferred Shading 的 fat G-Buffer 可能有 4-5 个 RT；Deferred Lighting 的光照 pass 只读两个 RT（深度 + 法线），大幅减少每光源带宽消耗，实测可支撑更多动态光源，这是 Engel 等人迁移的核心动机。

现代 PC 上带宽压力已缓解，Deferred Shading 凭借更少的几何 pass 重提交反而更常见；但在移动端和主机等带宽敏感环境中，Light Pre-Pass 仍有一席之地（参见 [[tiled-light-prepass]]）。

## 材质多样性的代价

Deferred Shading 的材质计算被迫嵌入光照 pass，所有光源都必须执行材质逻辑，当光源重叠时重复计算代价高。Deferred Lighting 将材质留在最后一 pass，每像素只执行一次，更适合需要高代价材质模型（次表面散射、各向异性反射、多层材质）的场景——但代价是几何必须两次提交，draw call 翻倍。

## 现代演变

随着 Visibility Buffer 管线（参见 [[visibility-buffer]]）的兴起，传统 Deferred Shading 和 Deferred Lighting 的划分已不再是讨论的中心，两者都被归入「write-gbuffer」家族，与 thin-gbuffer + compute shading 路线形成对比。

## 相关

- [[deferred-rendering]] — 延迟渲染总页，包含 Deferred Shading 详细布局
- [[tiled-light-prepass]] — Crystal Dynamics ROTR 的 thin G-Buffer 实现
- [[visibility-buffer]] — 更现代的替代方案
- [[rendering-pipeline-taxonomy]] — Pesce 的管线分类框架
- [[multiple-render-targets]] — G-Buffer 的硬件基础

## Sources

- [[sources/humus-deferred-lighting-recap]]
