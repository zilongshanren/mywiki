---
tags: [渲染, 透明, alpha, 采样, mipmap]
date: 2026-04-19
sources: 1
---

# 预乘 Alpha 如何消除 Bilinear "Tree Ring"

"Tree ring"（树环）是 X-Plane 这类**大量 alpha-blended 树精灵**的游戏里常见的视觉 bug：树叶边缘出现一圈与背景无关的杂色。Ben Supnik 指出，**预乘 alpha 是这类 ring 的数学解**。

## Bug 成因：透明像素下有"垃圾"RGB

纹理里一个像素是**完全透明**（α=0）时，它的 RGB 通道理论上没有任何意义——渲染时不会被看见。但**纹理文件里必须存点什么**：

- Photoshop 默认在 alpha=0 处填**白色**（或当前画笔颜色）。
- 美术通常不会去关心这些「不可见像素」的 RGB 值。

当 GPU 用 **bilinear filtering** 在半透明/不透明交界处采样时，采样器会**按通道**把 4 个 texel 线性插值。一个边缘像素是：

- RGB = 75% 绿（不透明树叶） + 25% 白（透明像素的遗留色）= **稍微发白的绿**
- α = 75% 不透明 + 25% 透明 = 0.75（合理）

结果：树叶边缘出现一圈白色／杂色的光晕——ring。错的不是 alpha，是 RGB 已经被 filtering 搅成"绿 + 垃圾"。

## 传统对策：在透明区"补色"

X-Plane 的历史做法是**手工保证 alpha=0 区域的 RGB 值与邻近可见像素接近**（"more green"），这样插值出来的颜色仍然是"更暗的绿"。

缺点：

- 美术需要反复手工处理每张贴图。
- Photoshop 工作流不会自动这样做——alpha=0 的像素用什么颜色对设计师是不可见的。
- 版本控制和修改都很脆。

## 预乘 Alpha：数学上自动正确

如果纹理是**预乘**的，alpha=0 的像素 RGB 按定义就是 `0 * anything = (0, 0, 0)`。现在 bilinear 插值：

- RGB = 75% 预乘绿 + 25% **0** = **0.75 × 原绿**
- α = 0.75

这是**数学上正确的"75% 绿"**——预乘 alpha 边缘变暗，符合 [[alpha-compositing|Porter-Duff over]] 的定义。不需要美术做任何事，不需要特殊工具。

> 核心观察：**预乘把 `alpha 乘法`放在 `bilinear 插值`**之前；而非预乘里 alpha 乘法放在之后。插值和乘法**不可交换**——这是数学本质。

## 为什么不全面转预乘

Supnik 给出的主要阻力是**块压缩（[[bc7-solid-color-blocks|BC1/BC3/BC7]]）**的精度预算：

- 非预乘树贴图里，大部分 RGB 像素都是"同一个绿"——压缩器把 4×4 块内少量颜色端点塞得很准。
- 预乘后，RGB = `α × 绿`，α 在边缘处连续变化，把端点间的「色差」变成「亮度差」——压缩器必须同时表达颜色和**由 alpha 带来的暗度变化**，色彩精度被稀释。

理论上最优的压缩器应该 **α-aware**：拿不透明部分做主 fit，忽略透明部分。现实里的 BCn 压缩器做不到。

## X-Plane 实际上的退路：`discard` 替代 blend

Supnik 坦言即便想上预乘也晚了——积累的资产量大。而真正的树杀手其实还不是这个 ring，是 **Z-buffer 与半透明不兼容**：如果开 alpha blending，Z 写得不干净，后面的建筑会被穿模（"blue rings"）。

他们的选择是**完全关掉 blending，用 alpha test**（`if (a < 0.5) discard;`）——变成纯二值透明。保留 bilinear filtering 让边缘不是方块阶梯，但不靠 alpha 混合——因此 ring 的问题依然存在，只是被"非 0 即 1 的 alpha"掩盖。配合 [[dither-alpha-clipping|dither alpha clipping]] 是类似思路。

## 离线缓存预乘 dds？

评论区问：能不能在 X-Plane 启动时把纹理预乘完缓存在硬盘、按 `(路径, 分辨率, mtime)` 哈希索引？Supnik 回答**不值得**：X-Plane 发布时已经把资产压成 DDS（预压缩的正确产物），缓存引入额外不可靠性（缓存脏了 = 视觉 bug 很难 debug）。大多数时候 ship 预处理好的资产比 runtime 聪明更划算。

## 相关
- [[alpha-compositing]]
- [[alpha-blending]]
- [[srgb-premultiplied-alpha-compression]]
- [[dither-alpha-clipping]]
- [[ben-supnik]]
- [[bc7-solid-color-blocks]]

## Sources
- [[sources/supnik-premultiplication-pros-cons]]
