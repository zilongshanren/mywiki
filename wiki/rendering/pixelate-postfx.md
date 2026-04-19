---
tags: [rendering, post-processing, retro, pixelate, unity]
date: 2026-04-19
sources: 1
---

# Pixelate 后处理

**Pixelate** 是把屏幕图像的有效分辨率降到更低、再拉回原分辨率的后处理。数学上等价于两步：先把 `_MainTex` 按 `uv = floor(uv * gridSize) / gridSize` 量化采样坐标，再用 **point filter** 放大回原尺寸。结果是"每个输入像素覆盖一块 N×N 的输出块"——马赛克，或者说把画面强行塞进一台低分屏的视觉。

## 和 color quantization 的区别

[[color-quantization-retro|Color Quantization]] 量化的是**颜色**（每通道几级），**空间**维度保留；Pixelate 量化的是**空间**（每 N×N 一个样本），颜色维度保留。两者是正交的风格化操作。NES 风格的完整复刻通常需要**两者串联**：先 Pixelate 到原生分辨率（如 256×240），再做 color quantization 到目标调色板。

这也是为什么 [[sources/danielilett-snapshot-pro-snes]] 的 SNES 色阶量化 override **不包含下采样**——下采样要靠 camera `FilterMode.Point` 或独立 Pixelate 后处理配合。

## 参数设计

Daniel Ilett 的 *Snapshot Shaders Pro* Pixelate 只暴露一个参数 `Pixel Size` —— 输出"大像素"的尺寸（像素数）。等价的 `gridSize` 是 `screenHeight / pixelSize`（或 width，取决于想保正方像素还是保屏幕比例）。

更花哨的变体会把 `Pixel Size` 做成可随 UV 变化的 map（中心低、边缘高，产生"望远镜取景器"观感），或加入 dithering 打破硬边。Pro 版只留一个旋钮是产品哲学：风格化后处理的 UI 极简。

## 实现细节

采样侧：`uv = floor(uv * gridSize) / gridSize` 要把量化中心**偏移到格子中心** `+ 0.5/gridSize`，否则格与格交界会偏向左下像素；同时需要在 shader 端或 RT 端设 `FilterMode.Point`，否则 GPU 会自动做 bilinear 把格子边缘晕开。

## 相关

- [[color-quantization-retro]] —— 颜色维度的量化，和 Pixelate 正交
- [[crt-shader-effects]] —— 复古链常把 Pixelate + Scanlines + RGB 子像素叠在一起
- [[texel-pixel-conversion]] —— `floor` / `+0.5` 的偏移问题
- [[mipmap-moire-scanline]]
- [[retro-rendering-techniques]]

## Sources

- [[sources/danielilett-snapshot-pro-pixelate]]
