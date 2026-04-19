---
tags: [source, unity, urp, shader, dissolve, vfx]
date: 2026-04-19
sources: 1
---

# Shader Toolbox for URP - Dissolve（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Shader Toolbox for URP* 撰写的 **Dissolve** 参数手册——通用溶解 VFX，以 plane 或 point 为几何 origin。

## 摘要

Dissolve 在 [[sources/danielilett-toolbox-urp-base-lit|Base Lit]] 的表面基础上加 Dissolve Properties：*Origin Type* 切换 **Plane** 或 **Point** 两种模式——Plane 以一个平面（*Cutoff Point* 在平面上 + *Cutoff Direction* 为法线）为参照、Point 以一个空间点（*Cutoff Point*）为中心向外辐射；*Cutoff Height* 是从 plane/point 出发、开始溶解的距离；*Flip Direction* 反转溶解方向（plane 模式到另一侧，point 模式变成"向内收拢"）；*Noise Scale* + *Noise Strength* 让 cutoff 边界呈现撕裂/烧蚀的噪声轮廓而非规则切面；*Glow Color* + *Glow Thickness* 控制边缘发光带——和 [[texture-dissolve|Ronja 的教程]]里 `smoothstep(isVisible - glow_range, isVisible, ...)` 是同一套数学；*Use World Space* 切换所有几何计算在世界/物体空间；*Use Emission* 决定 glow 走 Emission 还是 Base Color（前者配 Bloom 得到烧焦边）。随 pack 附带 **DissolvePlane.cs** 脚本——把一个 Transform 当 plane，每帧把 `transform.position` 和 `transform.up` 推给 material 的 `_CutoffPoint` / `_CutoffDirection`，美术只需拖个 Empty 到场景里就能用 Gizmo 编辑 plane。

## 关键要点

- **Plane vs. Point 两档**扩展了 [[texture-dissolve|经典 dissolve]]：传统教程多是噪声纹理 cutoff，这里 cutoff 由几何参数驱动——允许 plane 从下往上扫过场景、从中心向外爆炸等关卡级效果
- **DissolvePlane.cs** 是典型的 shader-authoring helper：让 Transform 而非 material 参数成为美术操作入口
- *Use World Space* 是重要选项：世界空间下溶解平面跟随场景坐标（刀刃切过场景），物体空间下跟随对象自身（object 移动时 plane 不动）
- Glow 边缘是 dissolve 视觉冲击力的主要来源——光靠 `clip` 出来的硬边不够美术；噪声 + glow 是标准配方
- Shader Toolbox 的 dissolve 本质是 [[texture-dissolve|Ronja texture-dissolve]] 的几何驱动版本：变量从"贴图灰度"换成了"到 plane/point 的距离"

## 链接到的概念

- [[texture-dissolve]]
- [[fizzle-lod-fading]]
- [[bloom-threshold-blur-composite]]
- [[dither-alpha-clipping]]

## 原文

- 链接：https://danielilett.com/shader-toolbox/dissolve/
- 本地：`raw/articles/danielilett.com/2026-01-01_shader-toolbox-for-urp-dissolve.md`
