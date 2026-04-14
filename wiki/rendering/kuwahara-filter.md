---
tags: [rendering, shader, post-processing, stylized, non-photo-realistic, convolution]
date: 2026-04-14
sources: 1
---

# Kuwahara 滤镜：保边的油画效果

**Kuwahara 滤镜**是一种最早在医学影像里被提出来**保边去噪**的非线性滤波器，后来被图形圈拿来当"油画/笔刷"风格化滤镜用——因为它的副产品正是平坦色块、锐利的块状过渡，跟真正的油画笔触非常像。Daniel Ilett 的 *Image Effects Part 6* 用它实现了 Super Mario Odyssey Snapshot Mode 里的 Oil Painting 效果。

## 算法骨架

和 [[image-convolution-kernel|普通卷积核]]的区别是：Kuwahara 不是对整个 N×N 窗口做线性加权，而是把窗口**切成四个重叠的 (r+1)×(r+1) 子区域**（r = (N-1)/2，中央十字行列属于多个区域）：

```
+------+------+
|  A   |  B   |
+------+------+
|  C   |  D   |
+------+------+
```

然后分别算每个子区域的颜色**均值**和**方差**，挑**方差最小**的那个区域——它是四个候选里最"均匀"、最不像跨越边界的那个——把它的均值写回中心像素。

这个非线性选择正是保边的来源：窗口横跨一条边时，跨边的子区域方差会比两侧内部的子区域大得多，算法自动避开跨边区域，只采样"这一侧"的颜色，于是边缘两侧各自变成平滑的色块，而边本身不会被糊开。

## 把方差也在 shader 里算

均值和方差的实现直接搬经典公式：

```hlsl
mean     = sum / samples;
variance = abs(squareSum / samples - mean * mean);  // mean of squares − square of mean
```

由于颜色是 RGB 向量，`variance` 也是一个三维向量，通常取 `length(variance)` 作为单个"方差分数"用于跨区域比较。计算均值和方差一起进行 —— 在同一个 for 循环里维护 `sum` 和 `squareSum` 两个累加器，只扫一遍窗口。

Ilett 把四个区域抽成一个 `calcRegion(int2 lower, int2 upper, int samples, float2 uv)` 函数，返回一个 `struct region { float3 mean; float variance; };`——把 shader 里常见的"复杂的每像素运算"组织成"每区域小函数 + 四次调用"可读得多。

## 四路选择用 step + lerp，不写 if

选最小方差的区域用 GPU 的反 `if` 习语：

```hlsl
float3 col = regionA.mean;
float  minVar = regionA.variance;
float t;
t = step(regionB.variance, minVar);     // regionB < minVar 吗？
col    = lerp(col,    regionB.mean,     t);
minVar = lerp(minVar, regionB.variance, t);
// C, D 同理
```

`step(a, b)` 返回 `b >= a ? 1 : 0`，所以 `step(Bvar, minVar)` 就是"B 的方差 ≤ 当前最小值"的布尔开关。用它来驱动 `lerp` 就能在不分化的情况下替换 `col` 和 `minVar`。这种写法和 [[color-quantization-retro|Game Boy 色阶选择]]用的 `lerp+saturate` 习语同源，都是"把多路选择编译成线性插值 + 常数切换"。

## 性能与使用场景

每像素要扫四个 `(r+1)×(r+1)` 的子窗口——相比 [[separable-gaussian-blur|可分离高斯]]的 `2N`，这里是 `4*(r+1)²` 次采样且**不可分离**（区域边界依赖方差比较，无法横竖拆）。3x3 窗口每像素 36 次采样、5x5 窗口 100 次，代价明显高于普通卷积。

主观效果上 Kuwahara 在**纹理杂乱、对比度高**的场景里工作得最好——每一笔都能"找到"一个稳定色块，画面看起来真的像手绘。场景越平坦、对比越低，滤镜就越接近普通的均值滤波。后续的改进（Papari 2007 广义 Kuwahara、anisotropic Kuwahara）用椭圆加权或梯度对齐的区域来减少笔触方向的机械感，但基础思想都是这一套"多区域方差最小 → 选均值"。

## 相关

- [[image-convolution-kernel]]
- [[separable-gaussian-blur]]
- [[unity-image-effect-basics]]
- [[color-quantization-retro]]
- [[watercolour-shader-experiments]] —— 另一种风格化笔触后处理
- [[sobel-edge-detection]] —— 与之互补的边缘保留思路

## Sources

- [[sources/danielilett-image-effects-kuwahara]]
