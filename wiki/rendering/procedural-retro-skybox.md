---
tags: [shader, 复古, psx, skybox, 程序化云, 天空盒, unity, urp]
date: 2026-04-19
sources: 1
---

# 复古风程序天空盒

**复古天空盒**把 [[retro-rendering-techniques|PSX/N64 look]] 里那套「降色深 + dither」量化思路从 mesh 搬到天空盒上，再叠一层程序噪声云，整体参数化。[[daniel-ilett|Daniel Ilett]] 的 *Retro Shaders Pro* Retro Skybox 是它最完整的一个商业化落地——从 URP 内建 Skybox (Cubemap) shader 改出来的版本，额外暴露分辨率限制、每通道色深、dither 模式、以及两段 Worley 噪声合成的云层。

## Sky base：cubemap 或 gradient 二选一

底层天空颜色有两套来源可切：

- **Cubemap 模式**：给一个标准 cubemap，shader 按视方向采样；这一路是 Unity 内置 Skybox (Cubemap) 的复刻。*Base Color* 作为乘子可以整体染色，*Rotation* 绕 y 轴转任意角度——美术无需重新烘焙 cubemap 就能对齐太阳方向。
- **Gradient 模式**：不用贴图，两端颜色 *Ground Color*（地平线下）和 *Sky Color*（天顶）加一个 *Color Mix Power* 控制它们的混合曲线。Power 越大，两端界面越硬；越小，混合越平滑。本质是把 `smoothstep(horizon, zenith, viewDir.y)` 做成可调曲线。

*Resolution Limit* 把最终采样分辨率向下 round 到最近的 2 的幂——输入 196 实际取 128——这是像素艺术里「降分辨率不如降到整格」的通用做法，避免非整数缩放带来亚像素噪点。

## 复古量化：色深 + offset + dither

天空盒最容易暴露 [[color-banding|色带]]：从地平线到天顶的平滑渐变，在 [[color-quantization-retro|PS1 15-bit color]] 的阶梯上会变成一圈圈可见的色环。Retro Skybox 的解法是三件套：

- **Color Depth**：每通道允许多少个离散值。PNG 原生是 256，PS1 大约落在 32 级——量化公式 `floor(c * depth) / depth`。
- **Color Depth Offset**：给量化结果加一个 `[0, 1/depth)` 的偏移常数。原因是 `floor` 总是向下取整，会让整体偏暗；小常数把均值拉回中间，防止整个画面变灰。
- **Dithering Mode**：Screen space / Texture space / Off 三档。和 [[dither-alpha-clipping|alpha dither]] 同源的 Bayer 矩阵技术，用高频噪点把相邻阶梯的边界打碎成噪声带，视觉上换回平滑过渡。Screen space 的点阵稳定、随相机移动滑过去；Texture space 会跟随视方向，看起来附着在天空上。

这些参数和 [[sources/danielilett-retro-urp-retro-lit|Retro Lit]] 的颜色段一一对应——把同一套量化工具在不同 shader 间复用，是这个 pack 设计的一致性优势。

## 程序云：两段噪声的组合态

*Use Clouds* 开启后，shader 在采样 sky base 之上叠一层程序噪声。它的机制透露几个点：

- **两段噪声**：*Cloud Sizes* 是两个值，驱动两份独立的噪声图，然后通过 *Combine Mode*（add / subtract / multiply / divide）合成。两段组合是分形噪声 /多尺度叠加的简化实现——两份不同尺度的 pattern 叠起来就能从「单调斑块」进化为「具有层次的云团」。用 divide 这种非常规操作可以做出条纹或纤细丝状的怪形云。
- **Cloud Height Threshold**：两个值控制「高度衰减曲线」——第一个是 0% 不透明的截断高度，第二个是 100% 不透明高度。之间的区域平滑过渡。视角越贴近地平线看到的云越多，天顶稀疏。这是对真实大气视差的粗暴近似。
- **Cloud Density Threshold**：对生成的噪声值做阈值。第一个阈值以下完全剔除（`clip`），第二个阈值以上完全不透明——两者之间按 `smoothstep` 过渡。和 [[texture-dissolve|dissolve shader]] 的边缘带算法是同一数学工具（噪声 + 双阈值 smoothstep），只是语境换成了云而不是溶解边缘。
- **Cloud Velocity**：把 UV 按时间扫描。2D 矢量控制云朝哪个方向飘。
- **Cloud Color**：给生成的云层整体染色；配合 sky gradient 可以把 golden hour 的橘色云一起做出来。

## 为什么「程序云 + 量化」会特别像真古董

把这两个东西合在一起的视觉效果非常强：**一是**生成的云本来是高频的连续噪声，被低色深阶梯切割后边界变成色带，反而像某种低分辨率印刷物；**二是** dither 让色带抖动起来，最终视觉上是一种介于数字和打印品之间的质感——和 90 年代 RPG 开场动画里的天空非常像。这不是偶然：它们都经过同一种量化瓶颈。

## 相关

- [[retro-rendering-techniques]] —— 复古渲染技术集合
- [[color-quantization-retro]] —— 同一套 Color Depth + Offset 量化逻辑
- [[dither-alpha-clipping]] —— dither 在 alpha 通道上的同源用法
- [[color-banding]] —— 量化引入色带的根因
- [[classic-shader-noise]] —— Perlin / Worley / fBm 的手写骨架
- [[daniel-ilett]]

## Sources

- [[sources/danielilett-retro-urp-retro-skybox]]
