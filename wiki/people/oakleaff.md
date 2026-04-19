---
tags: [人物, 作者, gamemaker, shader, 渲染]
date: 2026-04-19
sources: 1
---

# Oakleaff

**Oakleaff**（拼写带双 f 因为 "Oakleaf" 到处被抢注）是 GameMaker 社区的业余 3D/shader 开发者，自 2004 年起以 GM 作为爱好平台，专门"和 GM 的 3D 功能死磕"。在 GM Shaders 发表过 volumetric fog + cascaded shadow 的客座教程。他的项目以在 GM 里把 AAA 风格的 3D 渲染效果**简化到可用**为主要特色，GitHub 上有若干开源 demo。

## 代表作

- **Volumetric Fog + Cascaded Shadow demo**（客座 GM Shaders 2024-04）：一个完整的屏幕空间 raymarch 体积雾 + 3 级 cascade shadow 实现，用 Perlin 密度 + Blue Noise 抖动 + 1/4 分辨率 + Gaussian blur 做经济版 volumetric。见 [[volumetric-fog-raymarch-shadows]]。

## 风格

和 [[xor-shader-artist|Xor]] 的"minimal 可跑示例"不同，Oakleaff 偏工程化：整个项目在 GitHub 开源，代码风格完整。教程里提供了完整 shader 源、uniform list、step-by-step 可视化（noisy → 加 blue noise → 加 blur → 加 color，一步步演进到最终效果）。

## 相关

- [[volumetric-fog-raymarch-shadows]]
- [[xor-shader-artist]] —— GM Shaders 博主、给他提供了发声平台
- [[shadow-mapping-basics]]
- [[volumetric-raymarching-intro]]

## Sources

- [[sources/oakleaff-volume-shadows]]
