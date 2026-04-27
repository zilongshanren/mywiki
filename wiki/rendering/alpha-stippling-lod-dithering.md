---
tags: [渲染, LOD, alpha, dithering, gta-v]
date: 2026-04-27
sources: 1
---

# Alpha Stippling / LOD Dithering（Alpha 点画抖动 LOD 过渡）

Alpha Stippling 是一种在不透明几何体切换 LOD 时产生平滑视觉过渡的技术，核心手段是在过渡期按棋盘格图案丢弃约一半像素，使模型看起来像半透明物体，从而掩盖 LOD 模型切换的突兀感。

## 工作原理

在像素着色器中，根据像素屏幕坐标计算 `(x + y) % 2 == 0` 的条件（或结合 alpha 阈值检查），丢弃不满足条件的片段。由于 GPU 以 2×2 像素为最小着色单位（quad），点画丢弃无法节省着色计算，但能以固定的填充率代价换取 LOD 切换时的视觉平滑性。

[[sources/adrian-gta-v-graphics-1|GTA V]] 将使用点画绘制的网格记录在漫反射 G-Buffer 的 alpha 通道中。渲染透明物体之后，执行一个单独的"Dithering Smoothing"后处理 pass，读取 alpha 通道标记，对每个被点画的像素最多采样 2 个邻居像素，重建平滑颜色。该修复 pass 代价固定，与场景几何复杂度无关。

## 限制

点画不能与多重采样抗锯齿（MSAA）完美配合，因为 MSAA 在 sub-pixel 级别运作，而点画工作在完整像素级别。GTA V 的修复 pass 也并非完美——在某些情况下仍可见棋盘格残影。

## 适用场景

Alpha Stippling 广泛用于植被（树木、草丛）和远景建筑的 LOD 过渡，尤其适合 LDR 或 G-Buffer deferred 管线中无法对不透明几何体直接使用 alpha blending 的情形。在 Forward 管线中也可通过类似手段实现，配合 [[fizzle-lod-fading]] 等技术一起使用。

## Sources

- [[sources/adrian-gta-v-graphics-1]]
