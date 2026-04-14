---
tags: [图像编辑, fragment-shader, 2d, 合成]
date: 2026-04-14
sources: 1
---

# GPU 图像编辑器的缩放与笔刷

桌面图像编辑器（GIMP / Photoshop 之类）里最容易被 GPU 彻底翻盘的两个操作，是**视图缩放平移**和**笔刷绘制**。Apoorva Joshi 做 Papaya 时拿 GIMP 作对照，在 4096×4096 图像上用直径 2048 的笔刷做对比，肉眼就能看出代差。原因不在算法巧妙，而在把这两件事搬到了 fragment shader 和纹理采样里。

## 缩放平移：把画布做成 textured quad

纯 CPU 的图像编辑器在缩放时必须主动做重采样——放大用最近邻、缩小用线性——每一帧都要把结果拷到帧缓冲去显示。GPU 方案把整张画布视作一个**纹理化的四边形**，缩放 = 改 UV / 调节 sampler 的 filter；硬件采样器是免费工作的，零 CPU 代价。整个界面（按钮、工具栏）也可以是同一批带纹理的 quad，配合 ImGui 这类立即模式 GUI 就能用 [[draw-call]] 级别的开销画完。见 [[image-resampling-filters]]。

## 笔刷：别在 CPU 上画圆

朴素笔刷算法是「以鼠标位置为中心、`n×n` 方框里做距离测试，距离 ≤ 半径的像素填色」——复杂度与笔刷面积同阶。把鼠标拖动当成**一串圆的并集**更糟，沿鼠标轨迹每隔几像素重复一次上述操作才不至于出「凹坑」。直径 2048 的笔刷在 CPU 上会直接崩掉交互帧率。

Papaya 把这整段移到一个 [[fragment-shader]]：shader 采样当前画布纹理、和笔刷形状做一次合成、输出到一张**辅助 render target**，然后交换主纹理和辅助纹理的句柄——相当于 ping-pong framebuffer。每一帧只 draw 一个全屏 quad，fragment shader 里按 UV 决定「这个像素在不在笔刷范围内」。执行时间**与笔刷大小无关**，只看屏幕分辨率。

## 为什么这套思路有效

核心观察是：图像编辑里 99% 的操作都可以写成「对画布纹理做一次局部的逐像素变换」，也就是经典的 [[fragment-shader]] 工作负载。CPU 按扫描线循环的模型天然不擅长这种事，而 GPU 的 rasterizer 本就是为此而生。代价是需要 OpenGL / D3D 绑定、需要管理 render target 生命周期、需要手写一点合成 shader——但换回来的是缩放平移 + 笔刷这两类交互动作脱离画布分辨率的性能诅咒。

## 相关

- [[fragment-shader]]
- [[image-resampling-filters]]
- [[alpha-compositing]]
- [[draw-call]]
- [[texture-encoded-state]] —— 同类思路的教程级最小示例（鼠标 brush 写时间戳到纹理）

## Sources

- [[sources/apoorvaj-zooming-and-panning]]
