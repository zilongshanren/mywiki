---
tags: [source, raytracey, 路径追踪, Octane, 采样, 图像质量]
date: 2026-04-19
sources: 1
---

# Comparing path tracing image quality（Sam Lapere, 2010-04-23）

[[sam-lapere|Sam Lapere]] 用 [[octane-render|Octane Render]] 对三个场景（Porsche、室内、Chalet 酒店）做了**逐 spp 截图对比**，形成一张可读的经验收敛曲线。

## 摘要

博客正文几乎全是图：每个场景从 1 spp / 2 spp 开始，递进到 6 / 8 / 12 / 16 / 24 / 32 / 36 / 40 / 64 / 96 spp，用 YouTube 视频截帧。结论简洁：**8 spp 太糊看不清细节，16 spp 细节出来，32 spp 足以用于游戏**（Lapere 原话对比了 Modern Warfare 2 的低分辨率 shadow map / normal map），**64 vs 96 spp** 的差别已经被 YouTube / JPEG 压缩吃掉。作者随后贴了一张收敛曲线示意图，指出"开头噪声下降很快，后段收敛迅速变慢"——这就是 [[path-tracing-monte-carlo|Monte Carlo]] 路径追踪 1/√N 方差衰减在图上的直观表现。末尾更新还贴了 Brigade 引擎 HD 视频的 1 spp 截图，作为"实时 1 spp 就该是这个样子"的参考。

## 关键要点

- 经验阈值：**16 spp 细节回来，32 spp 游戏可用，96 spp 平台瓶颈变成压缩失真**
- 收敛呈饱和曲线——1/√N 规律的直观表现
- 这个经验值日后被 RTX 时代"1 spp + 神经降噪" vs "蛮力高 spp"两条技术路线直接继承
- Lapere 寄望 Fermi GPU 把"32+ spp 实时"带进消费卡

## 链接到的概念

- [[octane-render]]
- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[gpu-unbiased-path-tracing]]
- [[sam-lapere]]

## 原文

- 链接：http://raytracey.blogspot.com/2010/04/comparing-path-tracing-image-quality.html
- 本地：`raw/articles/raytracey.blogspot.com/2010-04-23_comparing-path-tracing-image-quality.md`
