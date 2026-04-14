---
tags: [rendering, shader, unity, 2d, fog, sprite]
date: 2026-04-14
sources: 1
---

# BLUK 风格的 2D 雾精灵着色器

一种面向 2D/伪 3D 手游的廉价「氛围化」着色器配方，典型代表是 2017 年前后在 iOS/Android 上流行的 BLUK 一类游戏：场景里是彩色 2D 雾、带 alpha 的精灵柱体、视差滚动，整体看上去像水彩远景。[[harry-alisavakis]] 在他博客早期的 *How I'd do it: BLUK visuals* 一文里把这种观感拆成了一套可参数化的 [[fragment-shader]] 技巧。

核心思路是把精灵世界坐标到相机的距离当成驱动信号。着色器在顶点阶段把 `mul(unity_ObjectToWorld, vertex)` 存到 `worldPos`，到片元阶段计算 `distance(worldPos, _WorldSpaceCameraPos)` 并除以 `_MaxCamDist` 得到 `[0, 1]` 的 `distFactor`。距离越远，`distFactor` 越接近 1，先用一次 `lerp(texcol, _SkyColor, distFactor)` 给整张精灵蒙上一层天空色，达到「越远越融入地平线」的观感——等价于一个廉价的距离相关单色雾，但只作用在 2D 精灵而不走场景雾那套体积计算。

第二步是精灵下沿的竖向渐变。作者定义 `gradientFactor = distFactor / 3` 作为渐变起点的 UV.y 阈值，再做一次 `lerp(_SkyColor, intercol, (uv.y - gradientFactor) / (1 - gradientFactor))`，使得精灵底部平滑融入天空色。渐变的「起始高度」被距离调制——远处物体的融化起点更高，视觉上等于远处柱体几乎只剩顶端，强化大气透视感。一个常见的坑是透明通道被二次 lerp 污染，作者用 `finalCol.a = texcol.a` 和一个阈值判断 `if (uv.y < gradientFactor) finalCol = _SkyColor` 一起堵住边缘黑带。

配套的两个脚本都很小：一个 `SkyColorManager` 每帧把一个公共 `skyColor` 同步到相机 `backgroundColor` 和材质参数；一个 `ParallaxingScript` 挂在相机上，遍历所有子物体按 `(farClip - z) / farClip` 反向平移，位置越深的背景移动越慢，避免和物理系统冲突。整套方案的重点不是复杂的图形学，而是把一个「美术要调试的氛围」映射成一两个着色器参数，让美术改一个 color 就能整屏改天色，是技术美术把体力活工具化的典型范例。

## 相关

- [[fragment-shader]]
- [[shaderlab-hlsl-basics]]
- [[unity-image-effect-basics]]
- [[harry-alisavakis]]

## Sources

- [[sources/halisavakis-bluk-2d-fog-sprite]]
