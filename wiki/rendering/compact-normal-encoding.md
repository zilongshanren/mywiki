---
tags: [渲染, 延迟渲染, g-buffer, 法线压缩, 精度]
date: 2026-04-19
sources: 1
---

# G-Buffer 法线的 2 通道紧凑编码

延迟渲染的 G-Buffer 里，每像素法线至少要存眼空间（或世界空间）的一个单位向量。直觉上存 XYZ 三通道就完事，但带宽与格式预算——特别是 MRT 场景下——往往只舍得给 2 个通道。问题是：**2 通道编码如何做到「解码后在接近掠射角的表面上依然稳定」**？

## 直观办法的失败：XY+重建 Z

[[ben-supnik|Supnik]] 在 X-Plane 10 初版 G-Buffer（见 [[xplane-gbuffer-format]]）里用的是 **16-bit float 的 XY，Z 由 `sqrt(1 - x² - y²)` 在 shader 里重建**。这是最省事的路，在多数像素上也看不出问题。

但当**物体表面法线几乎垂直于光方向**（比如机翼前缘的 leading-edge light：翼面法线朝上，灯沿翼展方向——两者几乎正交），解码出来的法线微小误差直接落在 attenuation 曲线的陡峭区段，表现为**可见的条带（banding）**。特别是在 linear space 下，没有伽马曲线替你隐藏误差（见 [[linear-lighting-pipeline]]）。

解法其实直观：**多给一个 16F 通道存完整 XYZ**，条带消失——但 G-Buffer 通道是奢侈品，省不出第三个。

## Lambert Azimuthal Equal-Area Projection

[Aras Pranckevičius 的 Compact Normal Storage 综述](https://aras-p.info/texts/CompactNormalStorage.html)比较了多种 2 通道编码方案。Supnik 选了其中的 **Lambert azimuthal equal-area projection**：

把单位球面等面积投影到一个圆盘，2 通道就够，解码只要几条指令。编码式：

```
f = sqrt(8 * n.z + 8)
enc.xy = n.xy / f + 0.5
```

解码式反向即可。Lambert 投影的关键优点是 **2D 平面上每像素的量化误差均匀对应到球面上的立体角**——不像朴素的 XY 投影那样在赤道区（`z ≈ 0`）精度稀烂。

## 副作用：扛得住负的 eye-space Z

朴素的「存 XY、重建 Z = `sqrt(1 - xy²)`」隐式假设 `z ≥ 0`（观察空间下面向相机）。极端情况下——高度弯曲的切线空间法线、或者某些边缘 case——切线空间 normal map 解码出来的眼空间法线可能落到背向半球（负 Z），这时 `sqrt` 会把符号吞掉。

**Lambert 投影天然能表示整个球面**（唯一无法表示的点是 `(0, 0, -1)`，即正对相机背后的法线，艺术资产上不现实），所以「XY-only 负 Z 处理」这类 hand-waving 可以彻底删掉。

## 与 CryTek Best-Fit Normals 的对比

SebH 在评论里早就提过 [CryTek 的 best-fit normals](https://aras-p.info/texts/CompactNormalStorage.html)：用 **8 bits × 3 通道**（比 2×16F 更省），通过查表选每个方向上精度最佳的缩放因子，在 8-bit 精度下做到稳定的 specular highlight。BFN 的好处是：

- **3 通道完整存** → 没有「负 Z」或反投影奇异点；
- **8 bit 够用** → 更省带宽，配合 specular；
- **世界空间 / 眼空间自选** → 不绑死在一个坐标系。

代价是编码需要查一张 3D LUT，比 Lambert 投影的纯算术贵一些。对 X-Plane 的场景（艺术资产切线空间法线外推有限、渲染路径已经选了 16F），Lambert 是性价比刚好的点；对更 PBR、更重 specular 的现代引擎，BFN / octahedral 通常是更好的落点。

## 现代补注

2011 年之后，**octahedral encoding**（Meyer et al.）以更简单的算术和接近 BFN 的精度成为主流。Lambert azimuthal 与 octahedral 在**2 通道法线编码**这件事上属于同一类解，区别在分布函数与解码开销。本文保留 Supnik 的历史选择，是因为它演示了「G-Buffer 的法线条带为什么是问题、以及 2 通道编码应选 area-preserving 而非朴素投影」的思维链。

## 相关
- [[xplane-gbuffer-format]] —— Supnik 的原始 G-Buffer 布局（已 XY+重建）
- [[deferred-rendering]]
- [[tangent-space-normal-mapping]]
- [[color-banding]] —— 条带的一般成因
- [[linear-lighting-pipeline]] —— 为什么 linear space 下 normal 精度更敏感
- [[ben-supnik]]
- [[8-bit-normal-map-precision-limits]] —— 贴图侧 RG8 精度问题（与 G-Buffer 编码互为独立战线）

## Sources

- [[sources/supnik-gbuffer-normals-revisited]]
