---
tags: [unity, urp, shader-graph, 彩虹, 视角相关, 卡牌]
date: 2026-04-19
sources: 1
---

# Holofoil 卡牌彩虹 shader

真实 Pokémon 卡的 holo 表面不是单纯的 rainbow 贴图——**彩虹反射随视角移动**是它的魂。Ilett 在 Shader Graph 里完整重建了这个效果：包含「视角相关条纹」「Hue 循环 / Color Ramp 双路径」「Holo Mask 定义哪些区域发光」「Heightmap 刻出细节凹凸」四个独立控制维度，是一个相当有嚼劲的 Shader Graph 练习。

## 视角相关条纹的数学

条纹方向 `_HoloDirection` 是一个 2D 单位向量，含义是「在 tangent 空间里条纹沿哪个方向铺」。扩成 3D 时 z=0（因为条纹贴着卡表面）。然后：

```
streak_raw = dot(viewVectorTangent, holoDirectionTangent)   // 视角法线差
streak     = sin((streak_raw + holoOffset) * holoDensity + uniformRotation)
```

- **`View Vector`** 在 tangent 空间里的 dot(HoloDirection) 给出"当前像素的视线和条纹方向的夹角余弦"——视线正对条纹方向时为 1，垂直时为 0。这是条纹**沿卡面不同位置有不同值**的原因，形成空间上的明暗切换。
- **`_HoloOffset`** 是手动偏移，挪动条纹起点。
- **`_HoloDensity`** 乘在 `streak_raw` 上，控制条纹间距（被乘完才 `sin`，所以是频率倍增）。
- **`uniformRotation`** 是另一个 dot 的结果：`dot((cameraPos - objectPivot), holoDirection)` 经过 tangent transform + `_HoloRotationScrollSpeed`。它的关键是**每个像素都拿到相同值**（camera 和 pivot 的 offset 与具体 pixel 无关），这样整束条纹**均匀平移**而不被拉伸。

最终 `sin` + `saturate` 把值压到 `[0, 1]`，作为"条纹强度"。把 density 和 rotation speed 拆开的理由 Ilett 强调过：若想加粗/变细条纹但不改变它们移动的速度，就必须走两条独立的数学路径。

## 条纹 → 彩虹的两条路

拿到 `streak`（`[0, 1]` 的标量）后，要把它映射到 rainbow。Graph 里做了一个 **`Use Color Ramp` Boolean Keyword** 分两路：

- **Off**：`Hue` 节点，输入全饱和红色（`(1, 0, 0)`），以 `streak + noise` 为 offset 在 HSV 空间里 rotate hue，output 是从红→橙→黄→绿→青→蓝→紫的完整循环。`Range = Normalized` 时 `streak ∈ [0, 1]` 覆盖一整个色相轮。
- **On**：采样一张 `_HoloColorRamp` 横条 ramp 贴图，用 `streak + noise` 作为 u 坐标——这样艺术家可以手工设计非线性的彩虹分布（比如「蓝偏多，红偏少」）。

**`Shader Feature`** 关键字只在 material 静态切换（编译成两份变体）；如果想在运行时切换得用 **`Multi Compile`**，代价是 Unity 编译全部变体（这是"compiling shader variants"慢的元凶之一）。

## 噪声 + Holo Mask 给表面纹理

光是条纹还太规整。Ilett 叠了两层：

- **`Simple Noise`** 以 object-space XY 为 UV（用 world space 会让卡旋转时噪声跟着动破坏沉浸感），`Scale = _HoloNoiseScale`，加上一个 `_Time.y * _HoloAnimSpeed` 让整片噪声缓慢漂移。把噪声值和 `streak` 相加再喂给 `Hue` offset，条纹变成"有颗粒感的条纹"。
- **`_HoloMask`** —— 一张黑白贴图，R 通道决定该像素「是否是 holo 区域」。把前面所有彩虹计算结果乘以 mask.r，就能做出 Pokémon 卡常见的「局部闪、局部哑光」外观（Bulbapedia 上 Cracked Ice、Cosmos、Sheen 都是不同 mask 图案）。

最后 `Lerp(baseColor, rainbowColor, holoMask)` 把基础卡面颜色和彩虹混合，输出 `Base Color`。

## Heightmap → Normal 刻出 etched 细节

Special Illustration Rare 级别的卡面有物理压痕。Shader Graph 的 `Normal From Height` 节点直接把高度图转成 tangent-space 法线：

- `_Heightmap` R 通道乘以 `_HeightmapStrength * 0.002`（节点很敏感，直接用 slider 值会过曝），接进 `Normal From Height`（Tangent 模式）；
- 结果接 `Normal` 输出。

这条线完全独立于彩虹计算，只是给 normal 加细节——配合 URP 的 Smoothness + PBR lighting 让那些刻线在转动卡时反光。

## 性能脚注：Transform 是 expensive 节点

Unity 6 的 Shader Graph 开 Heatmap 模式后能看到 `Transform` 节点是亮白色（最贵），因为它底层是一次 matrix multiply——Ilett 用的 world→tangent transform 每像素跑一次。对于卡牌这种小片元，可以接受；量大的话考虑在 vertex shader 里做 transform 再插值到 fragment。

## 相关

- [[stencil-parallax-card-layers]] —— 同教程的第一半，两者组合才是完整卡牌效果
- [[classic-shader-noise]]
- [[fresnel-edge-highlight]] —— 同样是视角相关 dot(V, N)，相邻思路
- [[spectral-zucconi-rainbow]] —— 光谱而非 HSV 的彩虹生成，光学严谨度更高

## Sources

- [[sources/danielilett-holofoil-cards]]
