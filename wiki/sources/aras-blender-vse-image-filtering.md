---
tags: [source, 渲染, 图像, 滤波]
date: 2026-04-14
sources: 1
---

# I accidentally Blender VSE（Aras Pranckevičius / aras-p.info）—— 图像滤波部分

[[aras-pranckevicius]] 发表于 2024 年 2 月的文章，回顾他「意外」开始为 Blender Video Sequence Editor 做性能优化的最初两个月。原文是技术 + 个人叙事的混合，本摘要只关注其中**图像重采样滤波**这部分有持久参考价值的内容（其余如 ffmpeg 多线程、音频重采样、draw call 批处理是过程经验，不录入概念页）。

## 摘要

Aras 在 Blender VSE 的图像变换/滤波代码里发现了几类「**off by half a pixel**」错误：用 Bilinear 把图放大 16 倍会让整张图整体偏移半个源像素；用 Bilinear 缩小 2× 又**根本不做滤波**。这种错误经常互相抵消，所以可以静悄悄潜伏多年。修完之后他又发现 Blender 内部所有「Bicubic」其实指的都是 Cubic B-Spline (B=1, C=0)——「无 ringing 但偏模糊」的极端选项；他补充了 Mitchell-Netravali (B=C=1/3) 作为可选项。原本写死大小的「Subsampled 3×3」box filter 也被改成根据缩放比例自适应，缩小 4× 时质量明显提升。最后，VSE 4.1 引入了 **Auto 滤波模式**：根据变换矩阵自动挑 Nearest/Bilinear/Cubic Mitchell/Box。

文章顺带提到一些过程经验：把 draw call 从「一次画两个三角形」改成批量提交，让时间轴绘制从 ~15 FPS 到 60+ FPS（这是教科书式的 [[draw-call|draw call]] 病例，但故事讲得简单）；用 `libswscale` 的 `sws_scale_frame` + 手动初始化上下文来开启多线程 RGB↔YUV 转换；把 Audaspace 音频重采样器加一个新的「medium」质量挡，用更小核大小拿到 3× 速度但谱图几乎不掉；把 Glow/Wipe/Gamma Cross/Gaussian Blur 几个 effect 多线程化或简化掉过度优化的查表。

## 关键要点

- **Bilinear 滤波的「半 texel 偏移」是个跨越十几年的老坑**。DirectX 9 时代每个图形程序员都踩过；现代离线图像管线里仍在出现。
- **「Bicubic」是模糊命名**——同一个名字在 Photoshop、Blender、ImageMagick 里指的曲线参数不同。文档应当写清 Mitchell-Netravali (B, C) 或核函数表达式。
- **缩小 > 2× 时 Bilinear/Bicubic 都失效**——必须用一个大小随缩放比例变化的 box（或 Lanczos）滤波器。
- **Auto 滤波模式**是个值得借鉴的 UX 启发式：根据 [[mvp-transform|变换矩阵]] 自动挑滤波器，而不是让用户在菜单里翻。
- 时间轴 UI 慢的原因是「一次只画两个三角形」——这是教科书 [[draw-call|draw call 开销]] 案例。
- `libswscale` 的多线程接口是「设计糟糕 API」的典型：要先 `sws_alloc_context` 自己手动设置一堆 `av_opt_set_int`，再用 `sws_scale_frame`（不是 `sws_scale`），然后 `AVFrame` 字段还得初始化得「足够正确」否则会 crash。
- 文章末尾一段值得记住：「**我能在业余时间做到的工作量，在大公司同样的时间可能只能做到 30%**」——这是组织复杂度和 [[continuous-design|持续设计]] 摩擦的间接观察。

## 链接到的概念

- [[image-resampling-filters]]
- [[aliasing]]
- [[draw-call]]
- [[batching]]
- [[mvp-transform]]

## 原文

- 链接：https://aras-p.info/blog/2024/02/06/I-accidentally-Blender-VSE/
- 本地：`raw/articles/aras-p.info/2024-02-06_i-accidentally-blender-vse-aras-website.md`
- 上采样滤波交互对比：https://aras-p.info/img/misc/upsample_filter_comp_2024
