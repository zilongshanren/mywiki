---
tags: [source, unity, urp, shader, stochastic, tiling]
date: 2026-04-19
sources: 1
---

# Shader Toolbox for URP - Stochastic Lit（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Shader Toolbox for URP* 撰写的 **Stochastic Lit** 参数手册——用随机 UV 偏移三次采样打散可见 tiling 的 Lit 变体。

## 摘要

Stochastic Lit 的参数表面几乎和 [[sources/danielilett-toolbox-urp-base-lit|Base Lit]] 完全一致（Surface Options + Lit Properties 全量继承）——没有额外的 Stochastic Properties，因为随机化参数是 hardcoded 的。差别在底层采样：每张贴图（Base Texture / Normal Map / Heightmap / AO / Emission）都被替换成"3 次带随机偏移的采样加权混合"实现，目的是打散大面积平铺时肉眼可见的 tiling 周期感。教程明确提示："this effect is more expensive, as three texture samples are used per texture"——完整 Lit 一般有 5 张贴图，等于 15 次采样，相当于 3× 默认成本。这是 [[stochastic-texture-sampling|Heitz-Neyret by-example noise]] 思想的轻量实现，适用远处大面积材质（地形、墙面、道路），不适合 hero object 或移动端 bandwidth 敏感场景。

## 关键要点

- **参数表面和 Base Lit 一样**——随机化是隐式 hardcoded 的实现细节，美术不需要手调噪声偏移
- **每贴图 3 次采样**的基线意味着总采样次数 ≈ 3 × 原 Lit；bandwidth-bound 硬件上约 3× 成本
- 教程**没展开混合算法**——大概率是简单加权平均而非 [[stochastic-texture-sampling|histogram-preserving blending]]；前者对 albedo 够用但会让 detail/normal 变模糊，后者成本更高但对比度保持更好
- **适用场景权衡**：远处大面积平铺 → 值得（tiling 可见性高），近处 hero object → 浪费，移动端 → 谨慎
- 可叠加于 [[triplanar-mapping|triplanar]] 之上解决"UV unwrap + tiling"双重问题（9 次采样/通道）
- 和 UV scale mixing / detail texture / megatexture 等方案是同一类问题的不同解——stochastic 的价值在"中等成本、无需额外美术资产"

## 链接到的概念

- [[stochastic-texture-sampling]]
- [[triplanar-mapping]]
- [[sampler-filter-wrap-modes]]
- [[two-texture-sampling-tricks]]
- [[texture-swizzle-nested-tiling]]

## 原文

- 链接：https://danielilett.com/shader-toolbox/stochastic-lit/
- 本地：`raw/articles/danielilett.com/2026-01-01_shader-toolbox-for-urp-stochastic-lit.md`
