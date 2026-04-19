---
tags: [source, unity, urp, shader, lit, pbr]
date: 2026-04-19
sources: 1
---

# Shader Toolbox for URP - Base Lit（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Shader Toolbox for URP* 撰写的 **Base Lit** 参数手册——pack 内所有效果 shader 共享的 PBR 基线。

## 摘要

Base Lit 是 URP 内置 **Lit** 的近似克隆，Ilett 把它作为 Shader Toolbox 里所有效果 shader（Bubble / Dissolve / Glass / Glitter / Mesh Explosion / Stochastic Lit 等）共享的基线 shader——每个效果都在这份参数表面基础上叠加特定功能。Surface Options 段暴露标准 Opaque/Transparent 切换、Front/Back/Both 渲染面、Alpha Clip + 阈值、Receive Shadows。Lit Properties 段是完整 PBR 控件：*Workflow Mode*（Metallic / Specular 双工作流切换，决定后续字段）、*Base Color* + *Base Texture*（tiling/offset 作为整套 Lit 贴图的主时序）、*Metallic* 或 *Specular Color*、*Smoothness* 带 *Convert From Roughness* 开关（处理 DCC 导出 roughness 的常见坑）、*Normal Map* + 强度、*Heightmap*（带性能代价警告）、*Ambient Occlusion*、*Emission Color*。整体是 URP Lit 参数表面的 1:1 复刻，没有算法创新；存在意义是**给 pack 里其他 shader 一个稳定的继承基础**，避免每个效果 shader 重写 Surface Options / Lit Properties 两段样板。

## 关键要点

- 不是新算法，而是 pack 里的 **base class**：所有效果 shader 继承它的 Surface Options + Lit Properties
- *Workflow Mode* 的 Metallic/Specular 切换是 URP Lit 的既定行为——只是 UI 字段变化，两种路径在数学上等价
- *Convert From Roughness* 解决 DCC → Unity 时常见的"粗糙度贴图塞 smoothness 槽反了"问题——Ilett 把它默认暴露是合理的新手缓冲
- *Heightmap* 的"增加性能代价"警示暗示它用 parallax mapping 而非 real displacement，在 fragment 阶段做 POM 循环
- 作为 Toolbox 其他 shader 的参考页——任何效果 shader 的 Surface Options + Lit Properties 段都可以引回到这里

## 链接到的概念

- [[physically-based-shading]]
- [[normalised-blinn-phong-shader]]
- [[dither-alpha-clipping]]
- [[tangent-space-normal-mapping]]

## 原文

- 链接：https://danielilett.com/shader-toolbox/default-lit/
- 本地：`raw/articles/danielilett.com/2026-01-01_shader-toolbox-for-urp-base-lit.md`
