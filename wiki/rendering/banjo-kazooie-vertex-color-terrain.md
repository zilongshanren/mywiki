---
tags: [shader, 复古, n64, 地形, vertex-color, godot, 渲染]
date: 2026-04-19
sources: 1
---

# Banjo-Kazooie N64 风格的 vertex-color 地形混合

N64 时代为了在极度受限的带宽和显存下做出富有层次的地形，《Banjo-Kazooie》把**颜色变化编码到顶点本身**——同一张低分辨率 tiling 纹理靠每个顶点的 vertex color 加权相乘，就能在大地图上拉出草地到泥土、阳光到阴影的平滑渐变，不需要额外 lightmap 或多层纹理采样。Alfred Baudisch 在 Godot 里复刻了这一套风格：用 Visual Shader 把 vertex color（甚至 vertex color alpha）作为 splat 权重，混合少数几张 tiling 纹理，就能得到"眼睛看到的是绘画感、GPU 吃到的是单次采样"的效果。

## 核心思路

和 [[terrain-splatmap-shader-graph]] 里 Unity URP 用 `_Control` RGBA 控制四层的约定不同，N64 风格的做法更暴力：

- **vertex color 的 RGB** 直接当作乘色项（tint），表达烘焙好的光照与色彩变化；
- **vertex color 的 alpha**（或 RGBA 四个通道）当作 splat 权重，混合 2~4 张 tiling 细节纹理（decal blending）。

这样地形 mesh 本身已经携带足够信息，片元 shader 里只需：`finalColor = mix(texA, texB, vColor.a) * vColor.rgb`。带宽压力几乎为零，美术方可以直接在 Blender 里像"涂色"一样编辑顶点色来调整地貌。

## Runtime 动态 splat paint

Baudisch 顺着这个架构再往前走一步——**游戏运行时**动态给 mesh "涂泥/洗泥"。最简实现也是用 vertex colors：在 CPU 端对被笔刷覆盖的顶点修改 vColor.a，GPU 下一帧就会按新的权重混合。比传统的运行时写 splat map 贴图便宜得多（不需要动态 RT、不需要笔刷烘焙成纹理），代价是精度受限于 mesh 的顶点密度——适合 low-poly stylized 地形，不适合追求细节的现代 PBR 场景。

## 为什么这个风格值得复刻

vertex-color 地形是典型的 [[retro-rendering-techniques|复古渲染]] 路径：它**不是在模拟 N64 看起来像什么**，而是**把 N64 当年真正的技术约束当作美学底层**——低密度 mesh + per-vertex 插值 + 少量 tiling texture 的组合自带那种"几何是块的、颜色是流动的"的视觉特征。只要数据通路走这条，不需要后处理 CRT/抖色也能得到识别度。

工具链上，这套流程跑在 Godot 的 [[godot-visual-shaders|Visual Shader]] + Blender 的 vertex paint 模式里特别顺——两边都原生支持 mesh 顶点色编辑与读取，不需要自己维护 splat 贴图资产。

## 相关

- [[terrain-splatmap-shader-graph]] —— Unity URP 下的经典 splatmap 做法对比
- [[retro-rendering-techniques]]
- [[compact-vertex-format]]
- [[vertex-shader-basics]]

## Sources

- [[sources/alfredbaudisch-banjo-godot-terrain]]
