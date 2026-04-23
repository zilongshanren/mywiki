---
tags: [渲染, 路径追踪, GPU, 非偏置渲染, 产品]
date: 2026-04-19
sources: 1
---

# Octane Render

Octane 是 Refractive Software（后被 OTOY 收购）于 2010-01 推出的**GPU 无偏路径追踪器**，作者为前 LuxRender 主程。它是 [[gpu-unbiased-path-tracing|2010 GPU 非偏置渲染器爆发]]里最具代表性的消费级产品：单张 GTX 260 就能跑出可用的 preview。

## 采样收敛曲线

[[sam-lapere|Sam Lapere]] 2010-04 的博客拿 Octane 渲染 Porsche Carrera、室内、Chalet 三个场景，手工截图对比 1/2/6/8/12/16/24/32/36/40/64/96 spp，得出经验判断：

- **1–2 spp**：只看得出大面积色块
- **8 spp**：噪声压过细节
- **16 spp**：细节开始出来
- **32 spp**：够用——Lapere 原话"for a game imo"
- **64 vs 96 spp**：YouTube / JPEG 压缩已经吃掉差异

收敛呈明显的**饱和曲线**：开头几帧噪声快速下降，后半程提升速度大幅衰减（由路径追踪 1/√N 的方差衰减本质决定，见 [[path-tracing-monte-carlo]]）。这个经验数字值得记：它跟后来 RTX 时代"1 spp + 神经网络降噪" vs 老派 "32 spp brute force" 的两条技术路线直接对应。

## 产品定位

Octane 跟 Arion 一样强调**同一个 render core 同时做 preview 与 final frame**——与传统离线渲染（preview 是光栅化，final 切到 photon mapping）形成鲜明对比。这是 2010 那一波 GPU 无偏渲染器的共同卖点。Octane 后来进入 OTOY 体系，延续到今天。

## 相关

- [[gpu-unbiased-path-tracing]]
- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[otoy-cloud-rendering]]
- [[sam-lapere]]

## Sources

- [[sources/raytracey-path-tracing-quality-comparison]]
