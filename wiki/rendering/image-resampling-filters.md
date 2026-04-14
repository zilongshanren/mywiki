---
tags: [渲染, 图像, 滤波, 信号处理]
date: 2026-04-14
sources: 1
---

# 图像重采样滤波（Image Resampling Filters）

**把一张图缩放到不同分辨率时使用的低通滤波器**。Nearest、Bilinear、Bicubic 这几个名字大家都熟，但**「同名异义」是图像处理领域的灾区**——同一个 `Bicubic` 在 Photoshop、Blender、ImageMagick 里指代的曲线和参数完全不一样。

## 三个常用滤波器

### Nearest（最邻近）

直接取最近的源像素，不做插值。**保留硬边**，但放大时锯齿明显，缩小时混叠严重。适合像素艺术或不希望产生新颜色的场景。

### Bilinear（双线性）

用两个方向上的线性插值，**4 个邻居的加权平均**。好处是便宜、连续；坏处是放大时模糊、缩小超过 2× 时几乎不抗混叠（因为只采样 4 个点）。

GPU 的 `LINEAR` 采样器就是 Bilinear——历史上 DirectX 9 时代有著名的「**半 texel 偏移**」问题：若把屏幕空间坐标直接映射到 texel 坐标而不补偿 0.5 的偏移，整张后处理结果会偏移半像素。Aras Pranckevičius 在 Blender VSE 里复现过同样的 bug：用 Bilinear 把小图放大 16 倍，整张图被偏移了半个源像素；用 Bilinear 缩小 2× 又**完全不做滤波**——这两类「off by half a pixel」错误经常互相抵消，所以可以静悄悄潜伏多年。

### Bicubic / Cubic（三次曲线）

用 4×4 邻域和某条三次曲线做插值。曲线选择很多，最常见的是 **Mitchell-Netravali 家族**：

$$k(x) = \frac{1}{6} \begin{cases} (12-9B-6C)|x|^3 + (-18+12B+6C)|x|^2 + (6-2B), & 0 \le |x| < 1 \\ (-B-6C)|x|^3 + (6B+30C)|x|^2 + (-12B-48C)|x| + (8B+24C), & 1 \le |x| < 2 \\ 0, & \text{otherwise} \end{cases}$$

参数 (B, C) 选不同值产生不同特性：

| (B, C) | 名称 | 特性 |
|---|---|---|
| (0, 0) | Catmull-Rom | 最锐利，最容易出 ringing |
| (0, 1/2) | Catmull-Rom（另一种约定） | 同上 |
| (1/3, 1/3) | 标准 Mitchell | 锐度与 ringing 的良好折中 |
| (1, 0) | Cubic B-Spline | 最平滑、几乎没有 ringing，但偏模糊 |

**Blender 内部所有「Bicubic」实际上都是 Cubic B-Spline (B=1, C=0)**——这是「无 ringing 但偏模糊」的极端选择。不同软件对 `Bicubic` 的默认参数完全不同，对照看几乎是迷宫。Aras 后来把 VSE 改成同时提供 B-Spline 和 Mitchell 两个选项。

## 缩小时的特殊问题：Box Filter

Bilinear/Bicubic 都只看固定大小的邻域（2×2 或 4×4）。**当缩小倍数大于 2× 时，源图里大部分信息根本没被采样到**，混叠严重。正确做法是用一个大小随缩小比例变化的 box（或更复杂的 Lanczos）滤波器，把多个源像素「平均」到一个目标像素。

Blender 3.5 引入了一个写死的「Subsampled 3×3」滤波器，本质就是固定大小的 box。Aras 把它改成根据缩放比例自动选择 box 大小（[#117584](https://projects.blender.org/blender/blender/pulls/117584)），缩小 4× 这种场景下质量明显提升。

## 「自动选滤波器」的策略

VSE 4.1 引入了一个 Auto 模式（[#117853](https://projects.blender.org/blender/blender/pulls/117853)），按变换矩阵自动挑：

- 没有缩放也没有旋转 → **Nearest**（避免无谓模糊）
- 放大超过 2× → **Cubic Mitchell**（锐利但低 ringing）
- 缩小超过 2× → **Box**（自适应大小，抗混叠）
- 其他情况 → **Bilinear**（便宜的默认值）

这是个值得复用的启发式：根据 [[mvp-transform|变换]] 的实际尺度来挑滤波器，而不是逼用户在 UI 里翻菜单。

## 「半 texel 偏移」与「透明边」

Bilinear 在边缘 texel 上做插值时，如果忘了夹紧到 [0, width-1]，就会和「外部」的透明像素混合，结果是图像四周出现半像素的透明边。Aras 在 Blender 里发现这个 bug 已经潜伏多年——只在 Bilinear 上出现，Bicubic 没有。修法很有趣：与其改源采样，不如**保留旋转情况下的边缘抗锯齿好处**，把「假透明边」改成只对**目标图像的边缘像素**做透明 AA（[#117717](https://projects.blender.org/blender/blender/pulls/117717)）。

## 经验教训

- **「Bicubic」是个用户友好但工程上有害的命名**——它本身只描述了曲线次数，没有指定参数。同样的话也适用于「sinc」「Lanczos」「Hermite」。文档里务必写清楚 (B, C) 或核函数表达式。
- **半像素偏差经常互相抵消**——这让单元测试很难发现它们，必须用「单像素源图放大到 16×」这种放大镜测试。
- **Filter 选择应该跟着变换走**，不应该让用户自己挑。

## 相关

- [[aliasing]]
- [[mvp-transform]]
- [[fragment-shader]]
- [[color-space]]
- [[gpu-image-editor-brush]] —— textured quad 缩放把 nearest/linear 选择交给硬件采样器
- [[unity-grabpass-blur]] —— Unity 里做全屏 Gaussian blur 的入门实现与教学取舍

## Sources

- [[sources/aras-blender-vse-image-filtering]]
