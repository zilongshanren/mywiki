---
tags: [source, raytracey, Fermi, OptiX, 路径追踪, GPU]
date: 2026-04-19
sources: 1
---

# Fermi: a raytracing BEAST（Sam Lapere, 2010-03）

[[sam-lapere|Sam Lapere]] 发表于 2010 年 3 月末的短博，记录了 Fermi 架构（GTX 480）在 NVIDIA OptiX 路径追踪演示 *Design Garage* 里的代际跨越——AnandTech 实测比 GTX 285 快约 **870%**。

## 摘要

AnandTech 跑了 NVIDIA 刚发布的 OptiX 演示 *Design Garage*（路径追踪渲染的跑车场景），得到 GTX 480 vs GTX 285 **8.7 倍**的提升——这在同一 API / 同一工作负载的世代对比里是罕见的数量级跳跃。Lapere 把这个数字当作对 [[gpu-unbiased-path-tracing|2010 GPU 非偏置渲染器浪潮]]的硬件侧佐证：Fermi 的 L1/L2 缓存、更宽的 warp 调度与 ECC 支持让不规则光线追踪负载第一次在消费卡上跑得动。他也顺手期盼有人拿 OptiX 做一个"低分辨率、可交互路径追踪的小游戏"。

## 关键要点

- *Design Garage* 是 NVIDIA 首批公开的 OptiX demo，跑车 + 路径追踪，完成度像半个产品
- GTX 480 vs GTX 285 在该负载上 870% 提升——Fermi 对光线追踪的改进不是渐进而是断层
- Lapere 对 OptiX 的评价：像 2008 年 ATI Ruby demo 之后最亮眼的 tech demo
- 文章主要意义是**时间戳**：把 Fermi 发布、OptiX 对外、GPU 路径追踪商业产品化这三件事绑在同一时点

## 链接到的概念

- [[gpu-unbiased-path-tracing]]
- [[path-tracing-basics]]
- [[sam-lapere]]

## 原文

- 链接：http://raytracey.blogspot.com/2010/03/fermi-raytracing-beast.html
- 本地：`raw/articles/raytracey.blogspot.com/2010-03-27_fermi-a-raytracing-beast-and-fyc-fuck-you-charlie.md`
