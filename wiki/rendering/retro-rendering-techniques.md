---
tags: [shader, 复古, ps1, n64, 像素, unity, urp]
date: 2026-04-14
sources: 1
---

# 复古主机渲染的技术集

"PS1 / N64 look" 在 shader 圈有一组被广泛复刻的**视觉特征**——它们不是单一 effect，而是若干条独立的**硬件限制**被主动引入到现代 GPU 上的模拟。Daniel Ilett 的 *Retro Shaders Pro* 包中 Retro Terrain Lit shader 的参数列表正好是一份这些技巧的清单。

## 几何层：顶点吸附（vertex snapping）

PS1 没有浮点光栅化器，顶点坐标在齐次变换后被量化到定点栅格，于是远处几何在移动时产生特有的**抖动（vertex wobble）**。复刻方法是在 vertex shader 里把位置量化到固定网格：`round(pos * snapsPerMeter) / snapsPerMeter`。坐标系的选择决定了抖动形态：

- **Object space** 吸附——相对模型本地坐标，物体内部稳定，但世界中旋转时抖动；
- **World space** 吸附——相对场景坐标，大地稳定但单个物体移动时抖动；
- **View space** 吸附——相对相机坐标，最接近 PS1 真实表现但需要把位置先变到 view space 再量化再变回去。

## 纹理层：低色深 + dither

PS1 / N64 的颜色深度有限（PS1 15-bit color、N64 更多变）。复刻关键是**降低每通道的量化级数**（例如 32、16 级），用 `floor(col * depth + offset) / depth` 把颜色压到阶梯上，然后补一个小 offset 防止整体变暗。

色阶太粗会出现**色带（color banding）**，缓解手段是加 dither——让两级之间的像素按屏幕坐标或 UV 坐标决定"四舍五入时的阈值"，从而用高频噪点换视觉上的平滑过渡。Retro Terrain Lit 提供**屏幕空间**和**纹理空间**两种 dither 模式；前者产生稳定的点阵图案，后者跟随表面贴片。（和 [[dither-alpha-clipping|dither alpha]] 是同一种数学工具的不同应用——前者量化颜色，后者量化 alpha。）

## 采样层：nearest + N64 3-point

现代默认的双线性过滤在像素风格里会把边缘模糊掉。复刻 PS1 需要换成 **point / nearest 采样**。N64 情况更特殊——它的纹理单元只支持一种被 Nintendo 工程师称为 "**3-point bilinear**" 的近似算法：在 2×2 的四个样本里只混合其中的三个（基于三角形所在的对角线半区），结果是一种介于双线性和 nearest 之间、带有轻微三角化痕迹的采样风格。许多复古 shader 会单独提供一个 "N64 filtering mode" 选项还原这种伪影。

## 光照层：texel lit 与 vertex lit

PS1 没有像素光照，N64 和 PS2 通常用**顶点光照**再经 Gouraud 插值。复刻手段：

- **Vertex Lit** —— 在 vertex shader 里算完 Lambert，由光栅化器线性插值到片元，导致高亮点呈菱形而不是圆形；
- **Texel Lit** —— 按纹理的 texel 格子量化光照结果，让光照"跳"到最近的 texel 上，最终呈现像老 splatmap 那样的分块感；
- **Unlit** —— 干脆不做光照，纯靠贴图和顶点色决定视觉。

Retro Terrain Lit 把这四种模式 (`Lit` / `Texel Lit` / `Vertex Lit` / `Unlit`) 并列提供，并且 Texel Lit 模式使用 terrain 的第一张 splatmap (`Splat0`) 的分辨率作为光照 texel 格子的参照——这就要求开发者在导入 terrain 贴图时保证所有 splat texture 用一致分辨率。

## 整体印象

把这些限制分别 toggle 出来放在一个 shader 里，本质是把**硬件限制现象学化**——每个 option 都能回到它 1996 年对应的硬件原因。这种"可调的复古"比直接套一个 post-process 滤镜更有用，因为它让效果落在**表面几何和材质采样阶段**，而不是最后一道全屏贴花。

## 相关
- [[dither-alpha-clipping]] —— dither 在 alpha 通道上的同源用法
- [[coordinate-spaces]] —— vertex snapping 选哪个空间
- [[sampler-filter-wrap-modes]] —— point / 双线性 / 各向异性的完整对比
- [[color-quantization-retro]] —— NES/SNES/GB 整数截断量化与 Game Boy 色阶级联 lerp
- [[sources/danielilett-retro-godot-retro-lit]] —— Godot 版 Retro Lit，是同一套 PSX 技术的最小可用集：view-space vertex snap、color depth + dither、Bilinear/Point/N64 filtering、Standard/Texel/Unlit 三光照模式
- [[sources/danielilett-retro-urp-retro-lit]] —— URP 通用版 Retro Lit，在 Terrain 版基础上加 Surface Options（Opaque/Transparent/Alpha Clip/双面）、*Use Flat Shading*（无 Gouraud 插值的面着色）、Specular + Reflection Cubemap（可选复古之上的现代点缀）
- [[sources/danielilett-retro-urp-retro-vertex-lit]] —— v1.5 后作为兼容页保留：Retro Vertex Lit 的独立 shader 已被合并进 Retro Lit 的 Snapping Mode/Vertex Lit 档，参数列表是 Retro Lit 的真子集（少 Surface Options、光照四档缩成 vertex-only、Dithering 简化为 bool）
- [[procedural-retro-skybox]] —— Retro Skybox 把色深限制 + dither 搬到天空盒：cubemap 或 gradient 两档 sky base，叠一层双 Worley 噪声程序云，全部参数化
- [[noperspective-affine-texture]] —— HLSL 的 `noperspective` 关键字：一行代码开启 affine warping；Ilett 的手动实现支持 0–1 平滑过渡
- [[banjo-kazooie-vertex-color-terrain]] —— N64 的 vertex-color splat 地形：把硬件约束当美学的另一案例（Godot 复刻）

## Sources
- [[sources/danielilett-retro-terrain-lit]]
- [[sources/danielilett-retro-godot-retro-lit]]
- [[sources/danielilett-retro-urp-retro-lit]]
- [[sources/danielilett-retro-urp-retro-vertex-lit]]
- [[sources/danielilett-retro-urp-retro-skybox]]
- [[sources/danielilett-retro-shaders-pro-breakdown]] —— 作者自述完整实现细节：vertex snap 空间选择、affine warping 手动路径、LOD-cap 分辨率、dither 双模式、texel-aligned lighting (ddx/ddy)、N64 3-point filtering、VHS tracking、14 种复古色板 filter；还谈 Asset Store 命名权和差评踩坑
- [[sources/alfredbaudisch-banjo-godot-terrain]]
