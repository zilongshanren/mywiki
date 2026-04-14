---
tags: [source, rendering, shader, unity, stylized, kuwahara, post-processing]
date: 2026-04-14
sources: 1
---

# Image Effects Part 6 — Painting Joy（Daniel Ilett）

[[daniel-ilett]] 于 2019 年 5 月发表的系列第 6 篇，用 [[kuwahara-filter|Kuwahara 滤镜]]实现 Super Mario Odyssey Snapshot Mode 的 Oil Painting（油画）效果——这是一种原本用于医学影像**保边去噪**的非线性滤波器，副产品正好是油画般的色块与笔触。

## 摘要

文章开头解释 Kuwahara 与普通 [[image-convolution-kernel|卷积]]的本质差异：它把一个 N×N 窗口切成四个重叠的 `(r+1)×(r+1)` 子区域（中心十字行列同时属于多个区域），分别计算每个区域颜色的**均值**和**方差**，然后挑方差最小的那个区域的均值作为中心像素的输出。这一步非线性选择是它保边的来源——窗口横跨边界时，跨边子区域方差大、自然被避开；算法等价于在边的每一侧各走一个纯色块，边缘不被糊开。实现上作者定义一个 `struct region { float3 mean; float variance; };` 和一个 `calcRegion(int2 lower, int2 upper, int samples, float2 uv)` 函数，把四个区域的扫描封装成一次函数调用。`calcRegion` 内部维护 `sum` 和 `squareSum` 两个累加器，在同一趟 for 循环里一次性算出均值和方差 (`variance = (squareSum/n) - mean*mean`)，再用 `length()` 把 3D 方差向量压成一个比较分数。主 fragment 里分别对 A/B/C/D 四个区域调 `calcRegion`，然后用 **`step + lerp`** 链式选最小方差——`step(Bvar, minVar)` 返回"B ≤ 当前最小"的 0/1 开关，丢进 `lerp` 就能在不分支的前提下替换 `col` 和 `minVar`。这种习语和前一篇 Game Boy 的色阶选择一脉相承。作者强调这个 shader 对"**纹理杂乱、对比度高**"的场景效果最好——画面越平坦越接近普通均值滤波、越没有油画感。实测每像素需要 `4 * (r+1)²` 次采样（3x3 窗口就是 36 次），代价明显高于可分离高斯。

## 关键要点

- **Kuwahara 滤镜**把 N×N 窗口分成四个重叠子区域，算各自的均值和方差，用最小方差区域的均值作为输出。
- 非线性"最小方差选择"是**保边**的来源：跨边的子区域方差大，自动被排除。
- 均值和方差在**同一趟循环**里算：维护 `sum` 和 `squareSum`，方差 = `squareSum/n - mean²`。
- 三通道的方差是向量，用 `length()` 压成标量才能跨区域比较。
- 用 `struct region { float3 mean; float variance; }` 让多返回值在 HLSL 里好看。
- 四路最小值选择用 **`step + lerp`** 代替 `if`，和 [[color-quantization-retro|Game Boy 色阶]]是同一个习语。
- 每像素采样数 `4 * (r+1)²`，**不可分离**（区域边界依赖方差比较），比高斯贵得多。
- 画面**纹理越杂乱对比越高**，Kuwahara 效果越明显——用在平坦场景会退化为均值滤波。
- 后续改进：Papari 2007 广义 Kuwahara、anisotropic Kuwahara 用椭圆加权减少笔触机械感。

## 链接到的概念

- [[kuwahara-filter]]
- [[image-convolution-kernel]]
- [[separable-gaussian-blur]]
- [[unity-image-effect-basics]]
- [[color-quantization-retro]]

## 原文

- 链接：https://danielilett.com/2019-05-18-tut1-6-smo-painting/
- 本地：`raw/articles/danielilett.com/2019-05-18_image-effects-part-6-painting-joy.md`
