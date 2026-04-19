---
tags: [rendering, shader, post-processing, retro, color-quantization, pixelation]
date: 2026-04-14
sources: 1
---

# 复古色彩量化与像素化

**颜色量化**（color quantization）是把连续的 `[0,1]` RGB 值映射到一个稀疏的离散集合上，制造老主机那种"颜色数有限"的视觉。配合**像素化下采样**与 [[crt-shader-effects|CRT 扫描线]] / [[bloom-threshold-blur-composite|Bloom]]，就能拼出 NES / SNES / Game Boy 的 snapshot 滤镜——Daniel Ilett 的 *Image Effects Part 5* 用三只 shader 分别示范这三种机器的风格。

## 数学技巧：靠整数截断做阶梯

核心一行：

```hlsl
int r = (tex.r - EPSILON) * N;     // N = 每通道级数
return r / (N - 1.0);
```

把 `[0,1]` 乘以 `N` 后转 `int` 会自然**向下截断**——`3.999` 变 `3`——所以每通道被量化为 `{0, 1, ..., N-1}` 共 `N` 级，再除以 `N-1` 还原到 `[0,1]`。`EPSILON = 1e-10` 是为了避免 `1.0 * N` 刚好命中 `N` 再被截断成 `N` 而越界（只想要 `0..N-1` 这 `N` 个值）。

这是一种**无 `if`**的量化，完全可以写进 [[unity-image-effect-basics|image effect]] 的 fragment shader 里。

## NES / SNES / Game Boy 三种风格差异

| 机型 | 真实限制 | Shader 近似 |
|---|---|---|
| **NES** | YIQ 色彩空间，64 色调色板（实际 54），每帧可见少 | RGB 每通道 4 级 → 64 色 |
| **SNES** | 15-bit 色，256 同时显示 + 加减混合 | RGB 每通道 6 级 → 216 色 |
| **Game Boy** | 4 级灰（GBP）或 4 级绿（GB） | 先算亮度 `lum = dot(tex, (0.3, 0.59, 0.11))`，再量化到 4 级，最后用 `lerp` 链式选色 |

NES 的真实调色板在 YIQ 空间、查表式映射，shader 里纯粹用 RGB 每通道 4 级做近似是"作弊但够用"。SNES 的 6 级比 NES 的 4 级明显更丰富，但仍远少于真机的 32768 色——画面会呈现明显的**色带**（color banding）但感觉正好就是"那种老电视的饱和色调"。

Game Boy 的特别之处在于它先**算亮度**再量化成 4 级整数 `gb ∈ {0,1,2,3}`，然后用经典的**级联 `lerp` + `saturate`** 选色：

```hlsl
col = lerp(_GBDarkest, _GBDark,   saturate(gb));
col = lerp(col,        _GBLight,  saturate(gb - 1));
col = lerp(col,        _GBLightest, saturate(gb - 2));
```

这是 GPU 编程里"**避免 if 的多路选择习语**"——每个 `saturate(gb - k)` 问一次"gb 是不是 ≥ k+1"，把结果丢给 `lerp` 切换。`_GBDarkest` 到 `_GBLightest` 四个色可暴露为 Properties 让用户改成 DMG 绿、Pocket 灰、BGB 蓝等任何 palette。

## 像素化下采样必须配 FilterMode.Point

仅有颜色量化不够"像素"——NES 的另一半味道是**低分辨率**。通用做法：

1. `RenderTexture temp = GetTemporary(width/pixelSize, height/pixelSize, ...)`
2. `Graphics.Blit(src, temp)` —— 这里发生下采样（默认双线性插值）
3. 把**自定义的量化 shader**跑在这张 temp 上
4. `Graphics.Blit(temp, dst, mat)` —— 上采样回屏幕

关键细节是 **`temp.filterMode = FilterMode.Point`**。否则上采样时默认 bilinear 会把像素边缘糊成渐变，丢掉硬边块状感。这种"缩小 → 处理 → 放大并用 point sampling"的模式几乎是所有像素 post-process 的标配。

## 相关
- [[crt-shader-effects]] —— 扫描线 / 荧光粉 / glitch 叠在量化之后的典型链
- [[retro-rendering-techniques]] —— PS1/N64 复古技术清单，和本页的 NES/SNES/GB 同源哲学
- [[dither-alpha-clipping]] —— dither 可以缓解色带，和量化是互补关系
- [[unity-image-effect-basics]]
- [[image-effect-colour-transform]]
- [[color-banding]]
- [[sampler-filter-wrap-modes]] —— FilterMode.Point 的位置
- [[color-quantization-kmeans]] —— 另一种颜色量化思路：连续空间里用 K-Means 找 k 个主色而非每通道砍级数，互补场景
- [[sources/danielilett-retro-urp-crt-post-process]] —— URP 全屏 CRT 的 Custom RGB Sliders 模式用整数滑块直接指定 R/G/B 每通道级数，是色阶量化的 UI 极简表达；并暴露 Custom Luminance / RGB / RGB+Intensity 三种自定义 ramp 采样模式
- [[procedural-retro-skybox]] —— Retro Skybox 把 Color Depth + Color Depth Offset（防整体变暗）+ Screen/Texture/Off Dithering 这一套复古量化搬到天空盒上
- [[sources/danielilett-retro-urp-retro-skybox]] —— 天空盒版 PSX 色深量化 + 程序噪声云
- [[pixelate-postfx]] —— 空间维度的量化，NES 风格需和色阶量化串联
- [[sources/danielilett-snapshot-pro-posterize]] —— 三通道独立级数 + `Power Ramp` gamma 的通用化 per-channel posterize
- [[sources/danielilett-snapshot-pro-pixelate]] —— 单参数 Pixelate override，空间量化工具

## Sources
- [[sources/danielilett-image-effects-retro-crt]]
- [[sources/danielilett-snapshot-pro-snes]] —— Pro 版把每通道色阶量化做成 Volume override，只暴露 `Banding Levels` 一个滑块，N=6 近 SNES、N=4 近 NES
