---
tags: [渲染, pbr, brdf, 标准, 材质]
date: 2026-04-19
sources: 1
---

# OpenPBR

**OpenPBR** 是 ASWF（Academy Software Foundation）主持、Adobe / Autodesk / ILM 等联合推进的**开放式 uber-shader 标准**，目标是给游戏、离线渲染、DCC 工具之间提供一套互通的物理材质定义。前身是 Adobe Standard Material 和 Autodesk Standard Surface 的合并产物，维护者包括 Jamie Portsmouth（Autodesk Arnold）、Peter Kutz（Adobe）等。

标准本身是一个 BRDF 层叠规格：diffuse + specular + coat + sheen + transmission + subsurface + emission + thin-film，加上一组能量守恒的组合规则。和 Disney Principled（见 [[physically-based-shading|PBS]]）相比，OpenPBR 更偏严格——coat darkening、coat rough-specular 吸收、金属 roughness 重映射都是解析推导而非艺术家 tweak。

## 2025 年进展

在 [[sources/selfshadow-pbs-siggraph-2025|SIGGRAPH 2025 PBR 课程]] 上，Peter Kutz 专门讲了 OpenPBR 的几个新特性：

- **Coat darkening** 的解析推导（有基底 specular 时的变暗计算），并给了参考实现 Listing 2——视角相关吸收、alpha 通道处理都在后续修订版里补齐。
- **金属参数拟合表**新增 brass 和 steel（配合 RGB 预乘 F0/F82 的 Gulbrandsen parametrisation）。
- 课程笔记随后几个月仍在勘误（v1.1 → v1.2 → v1.3），反映规范还在持续打磨。

## 相关

- [[physically-based-shading]]
- [[microfacet-brdf]]
- [[stephen-hill]]
- [[neural-materials]]

## Sources

- [[sources/selfshadow-pbs-siggraph-2025]]
