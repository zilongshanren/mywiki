---
tags: [渲染, 深度缓冲, 精度, planet-engine, opengl]
date: 2026-04-27
sources: 2
---

# 对数深度缓冲（Logarithmic Depth Buffer）

标准深度缓冲以投影矩阵推导出的 `a - b/z` 函数编码深度，导致近平面附近消耗约一半的缓冲精度，而远处精度极度匮乏——对于行星尺度渲染（草叶到数十公里外的山脉同帧可见），这是完全不可接受的。对数深度缓冲把深度值的分布改成以 `log(z)` 为基础，从数学上给出"最优"方案：每单位屏幕大小变化在深度缓冲中占有相等的比例。

## 为什么对数是最优解

避免 z-fighting 的充分条件是：深度缓冲在距离 z 处的分辨率与投影图像在该距离下的几何尺寸变化同步，即分辨率应与 1/z 成正比。满足"导数正比于 1/z"的函数正是对数函数。

Outerra 的精度图表显示：24 位对数深度缓冲可以覆盖 9 个数量级的深度范围而精度平稳，而传统 32 位浮点缓冲仅在 4 个数量级后进入不可用区间。

## 顶点着色器实现（2013 年精炼版）

```glsl
// 假设 gl_Position 已由正常 MVP 矩阵计算完毕
gl_Position.z = log2(max(1e-6, 1.0 + gl_Position.w)) * Fcoef - 1.0;
gl_Position.z *= gl_Position.w;  // 消除后续透视除法
```

其中 `Fcoef = 2.0 / log2(farplane + 1.0)` 为常量或 uniform。gl_Position.w 在标准投影下等于摄像机空间正深度，无需额外计算。与早期版本相比，改用 `log2` 可直接对应 GPU 的 log2 指令，避免额外乘法；用 `max(1e-6, ...)` 钳制防止顶点跨摄像机近平面时整个三角形被错误裁剪。

## 透视插值误差与片段着色器写深度

顶点着色器算出的对数值只在顶点处精确，光栅化器对深度做**线性**插值，对数函数的非线性会导致大三角形中心处深度漂移。修复方式是从顶点着色器传出插值量 `flogz = 1.0 + gl_Position.w`，在片段着色器写：

```glsl
gl_FragDepth = log2(flogz) * Fcoef_half;  // Fcoef_half = 0.5 * Fcoef
```

写 `gl_FragDepth` 会关闭 Early-Z 优化，参见 [[conservative-depth]]。Outerra 的实测表明地形几何因细分足够密集，不需要片段写深度；仅对象部分在细分不足时开启，代价可控。

## C 系数与近平面线性化

早期版本引入常量 C 来调节精度分布，使近摄像机处呈线性（避免大三角形的插值错误而无需片段写深度）。C=0.01 时线性段约 10 米，适合第一人称视角。2013 年的优化版移除了 C，改以 `max(1e-6, ...)` 的钳制代替，因为实际工程中精度余量远超需要，线性化收益有限。

## 与 Reversed-Z 浮点深度缓冲的比较

[[reversed-z]] 配合 32 位浮点深度缓冲可达到与 24 位对数深度缓冲相近的效果，且无须修改着色器。然而：

- Reversed-Z 在 OpenGL 上因 NDC 的 -1..1 偏置问题无法完整发挥（除非使用 `glDepthRangedNV` 扩展，仅 NVIDIA 硬件支持）。
- 对数深度缓冲在所有厂商硬件上均可用，且 32 位精度约比 24 位 reversed-Z 浮点还高 20 倍。
- 32 位浮点深度格式在需要模板缓冲时带来额外带宽，而 16 位对数深度缓冲即可覆盖行星尺度，16 位整数对数可节省大量内存带宽。

## 相关

- [[z-buffer]] — 深度缓冲基础原理与精度非线性分布
- [[reversed-z]] — 翻转近远映射利用浮点精度的替代方案
- [[conservative-depth]] — ARB_conservative_depth：单调写深度时恢复 Early-Z
- [[z-buffer-custom-encoding-early-z-tradeoff]] — 更广泛的深度编码与 Early-Z 权衡讨论
- [[view-frustum-culling-ryg]] — 同出于大规模场景优化需求

## Sources

- [[sources/outerra-depth-buffer-precision]]
- [[sources/outerra-log-depth-buffer]]
