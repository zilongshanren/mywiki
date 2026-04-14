---
tags: [渲染, 后处理, hdr, 色调映射, 算法]
date: 2026-04-14
sources: 1
---

# Exposure Fusion（曝光融合）

**Exposure Fusion**（Mertens 等人，2007）是一种把多张不同曝光的图像融合成一张「细节完整且无 halo」结果的算法。它原本用于多帧 HDR 摄影，但在实时渲染里同样可以把单张 HDR 渲染结果合成多张「合成曝光」（synthetic exposures），再融合得到 [[local-tonemapping]] 效果。

## 核心思路：在 Laplacian 金字塔上分尺度融合

直接用 per-pixel 权重融合三张曝光的结果会非常丑——所有图像看起来又泛白又过饱和。直接用 Gaussian 模糊权重再融合则会出现明显的 halo。

Exposure Fusion 的关键洞察是：

> **改变曝光的频率，应当和图像内容本身的频率相关**。

在平坦区域，曝光要在大尺度上慢慢渐变；在有强边缘的区域，曝光切换要在边缘附近完成，把变化藏在边缘里。

实现方式出乎意料地干净：

1. 为每张曝光建一个 [[laplacian-pyramid]]
2. 为每张曝光构造一个权重图（per-pixel 衡量该曝光在该像素是否「曝得好」）
3. 为权重图建一个 Gaussian 金字塔
4. **在金字塔每一层，用对应层的 Gaussian 权重去 blend 对应层的 Laplacian**
5. 自上而下重建出最终图像

由于高频 Laplacian 是用相对锐利的高分辨率权重 blend，而低频 Laplacian 是用大半径权重 blend，曝光过渡自然地获得了「大尺度上柔和、小尺度上锐利」的特性。结果几乎没有 halo，也没有 bilateral 滤波的振铃。

## 权重的来源

Mertens 原论文用三个度量：**对比度**、**饱和度**、**曝光适当性**（亮度接近 0.5 的程度）。Wronski 在实现里指出实际只用「曝光适当性」就够了，其余两个会让效果偏向饱和、戏剧化的「toxic HDR」风格。

## 算法步骤（实时版本）

1. 用不同曝光值对同一张 HDR 图做全局 tonemapping，得到 N 张 LDR 合成曝光
2. 计算每张的亮度图（gamma 后的 luminance 是简陋但够用的近似）
3. 为每张亮度图建 Laplacian 金字塔到某一层
4. 计算每张的「曝光适当性」权重，建 Gaussian 金字塔
5. 在最粗一层，用 Gaussian 权重 blend 最粗的 Gaussian 亮度
6. 自下往上累加每一层的 Laplacian × 对应权重
7. 把得到的目标亮度回到原图，再走剩余的 color grading

## 关键参数

- **Coarsest mip level**：构建到第几层金字塔。层数越浅越接近 per-pixel blend；层数越深动态范围压缩越强，但容易产生 fake-HDR 的洗白感。
- **Shadows / Highlights**：合成曝光相对中间曝光的偏移量，提供艺术控制。
- **Exposure preference sigma**：权重对「亮度接近 0.5」的偏好强度。极端值会产生不连续伪影。
- **可选的 local contrast boost**：把 Laplacian 的幅度乘进权重里，能在不洗白的前提下增强局部对比——和 Lightroom 的「Clarity」滑块本质相同。

## 局限

- 行为依赖图像的频率内容：同样的「shadows = +1」在边缘多的场景和无边缘场景下亮起的程度不同，调参较反直觉。
- 推到极限会出现伪影；增加合成曝光数能缓解，但成本升高。
- 算法本身设计成 LDR→LDR 的合成，套到完整 HDR 管线里需要小心处理。

## GPU 实现

[[bartosz-wronski|Bart Wronski]] 给了一个 ~300 行（含 GUI）的 WebGL demo：

- 多张合成曝光打包到同一张 texture
- Laplacian 金字塔不需要单独存储，算成相邻 Gaussian 层之差就行
- 主要成本是 tonemap 多次（可以用一个简化代理 operator 而不是真正的 ACES）
- 整张算法可以在 1/4 × 1/4 分辨率上跑完，再用 [[guided-filter]] / joint bilateral 升采样到全分辨率——HDRNet、Pixel Portrait Mode、HDR+ 都用这套思路

预估：在上一代主机上 < 1ms。

## 相关

- [[local-tonemapping]]
- [[laplacian-pyramid]]
- [[guided-filter]]
- [[color-space]]
- [[bartosz-wronski]]

## Sources

- [[sources/bartwronski-exposure-fusion]]
