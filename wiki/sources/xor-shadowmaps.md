---
tags: [source, 渲染, 阴影, 光照, shader]
date: 2026-04-14
sources: 1
---

# GM Shaders: Shadowmaps（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2024 年 3 月的一篇长教程，是他为后续 **volumetric shadows** 系列做的 3D 阴影入门打底。对 GameMaker 用户来说意义特别大——主流 shadow mapping 教程几乎不覆盖 GM。

## 摘要

一篇从零讲完 hard shadow + soft shadow + Phong 光照的完整教程。核心流程：

1. **Depth map**：从光源视角渲染场景，把 `gl_Position.z` 写到 `R32F` surface。只有当光源或投射者移动时才需要更新——跨帧可缓存。
2. **Hard shadow**：把像素变换到 shadow projection space，除以 `w` 得 uv 和深度，采样 shadow map 做比较。必须加 **bias**（`~0.001` 起调）防止 shadow acne；用 `1 / max(-normal.z, 0.1)` 做 slope-scaled bias 更准。可以用 `shadow_hard` 的 fade 版本把硬边软化一点。
3. **Edge vignette**：shadow map 范围有限，超出部分用 `(1 - suv*suv)` 做边缘衰减，并用 `proj.z > 0` 排除光源背面。
4. **Soft shadow**：PCF 家族。便宜版是 2×2 bicubic 插值；漂亮版是黄金角 Fibonacci 圆盘采样——从 blue noise 取起始方向，每次乘黄金角 `mat2` 旋转，半径用 `sqrt(i)` 做面积均匀的分布。注意大半径软阴影会踩穿 texture cache，是性能杀手。
5. **Phong 光照**：把法线变到 shadow-space 后，`-normal.z` 直接是朝光的系数，省掉 dot。diffuse 用 `0.5 - 0.5*normal.z` 的半兰伯特平滑版，specular 用 `reflect(eye, normal).z` 的高次幂。整个过程在 linear RGB 里做，最后 gamma 回 sRGB。

完整代码在 [GM_Shadows](https://github.com/XorDev/GM_Shadows)。

## 关键要点

- **Shadow map 的本质**：从光源看一次深度，再回到主渲染里做深度比较。
- **Float depth surface** 比 bit-packed RGBA8 精度高，插值平滑。
- **Bias 的两难**：太小→shadow acne，太大→peter-panning；slope-scaled bias 是标准做法。
- **Edge vignette** 比 texture repeat 干净得多，还能兼做 spotlight cone。
- **Soft shadow = 多个 hard sample 的平均**（PCF），不能直接模糊 shadow map。
- **Blue noise 起始方向** + **黄金角旋转** + **sqrt 半径分布** = 好看的软阴影采样内核。
- **性能陷阱**：大半径软阴影是 cache 不友好的。
- **Phong 在 shadow-space 里做** 可以省点积，因为光的方向变成恒定的 -Z。
- 进阶：[LearnOpenGL Shadow Mapping](https://learnopengl.com/Advanced-Lighting/Shadows/Shadow-Mapping)、Microsoft 的 [cascaded shadow maps](https://learn.microsoft.com/en-us/windows/win32/dxtecharts/cascaded-shadow-maps)。
- 和 [[cached-shadowmaps]] 的组合非常自然：shadow map 不必每帧重绘。

## 链接到的概念

- [[shadow-mapping-basics]]
- [[cached-shadowmaps]]
- [[poisson-disk-sampling]]
- [[color-space]]
- [[z-buffer]]
- [[reversed-z]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/shadowmaps
- 代码：https://github.com/XorDev/GM_Shadows
- 本地：`raw/articles/mini.gmshaders.com/2024-03-23_gm-shaders-shadowmaps.md`
