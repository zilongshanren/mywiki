---
tags: [source, graphics, opengl, draw-call, instanced-rendering]
date: 2026-04-19
sources: 1
---

# OpenGL rendering performance test #2 — Blocks（Outerra Blog）

[[outerra-team]] 2016 年 2 月的文章，接上一篇 grass test，这次测的是「有 per-instance 数据 + 部分程序化」的楼房 block 渲染：每 block 128 bytes 数据（早期来自 OpenStreetMap footprint，后改为合成数据保持密度），backface culling 开启。

## 摘要

相比 grass test，这一组的重点是**有 per-instance buffer 访问、且有真正背面可剔的 3D 几何**后 instanced draw 的吞吐曲线会如何变化。AMD GCN 1.1+（380/390X）在 5k 三角形/instance 处仍然出现接近翻倍的突跳；NVIDIA 关闭背面剔除时掉约 30%，AMD 关闭后几乎不掉（说明瓶颈在 prim assembly 之前，不在 raster）。跨测试比较显示 **NVIDIA 更喜欢 grass 那种「少 per-instance 数据、复杂 VS」的 workload**，AMD 对两种差别不大。最终结论：**两家都在 5-20k 三角形/instance 达到最佳表现**。

## 关键要点

- **AMD 5k 突跳现象在 blocks 场景依然存在**——不是 grass 场景的特例。
- **NVIDIA 禁 cull 掉 30%，AMD 禁 cull 几乎不掉**——两家瓶颈位置不同。
- **NVIDIA 偏好低 per-instance 数据 + 复杂 VS**；AMD 两者均衡。
- 小 mesh（< 40 tri/instance）AMD 新卡表现依旧糟糕，和 GS 慢的原因同源。
- 开源 benchmark 链接同 #1。

## 链接到的概念

- [[opengl-draw-call-batching-sweet-spot]]
- [[draw-call]]
- [[batching]]

## 原文

- 链接：https://outerra.blogspot.com/2016/02/opengl-rendering-performance-test-2.html
- 本地：`raw/articles/outerra.blogspot.com/2016-02-06_opengl-rendering-performance-test-2-blocks.md`
