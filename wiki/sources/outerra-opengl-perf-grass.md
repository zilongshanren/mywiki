---
tags: [source, graphics, opengl, draw-call, instanced-rendering, procedural]
date: 2026-04-19
sources: 1
---

# OpenGL rendering performance test #1 — Procedural grass（Outerra Blog）

[[outerra-team]] 2016 年 1 月的文章，是一组 OpenGL 三角形吞吐系统测试的第一篇，面向「完全程序化、零 per-instance 数据」的草叶渲染场景（从 `gl_InstanceID` + `gl_VertexID` 算位置，贴少量查找纹理）。

## 摘要

测试 256×256 的草 tile（约 32.7 万三角形），每片草叶 7 顶点 5 三角；覆盖 `glDrawArrays`、`glDrawArrays` strip、`glDrawElements` strip、`glDrawElements` list 以及 geometry shader 五种路径，并横扫 1–65536 blades/instance 的所有 instance 规模，测不同 GPU 架构下的吞吐曲线。结论是 **indexed triangle list** 整体最优，**instance 内 mesh 大小 5k-20k 三角形是跨厂最安全的甜点**。NVIDIA 在小 mesh 上被 CPU driver overhead 压死；AMD GCN 1.1+ 在 mesh 小于 1k 时性能异常低，到 5k 有突然翻倍的拐点。Geometry shader 的性能大致等价于「小 mesh instanced VS」，AMD 新卡上尤其差，并会随 fragment shader interpolant 数量进一步衰减。测试源码与 binaries 公开（`github.com/hrabcak/draw_call_perf`），Outerra 也收用户提交的结果来完善图表。

## 关键要点

- **甜点**：5k-20k tri/instanced draw，两家 GPU 都能吃满。
- **Indexed list 优于 strip**：不需要退化顶点跨越草叶。
- **NVIDIA 小 mesh 受 CPU 驱动限制**；**AMD 新架构小 mesh 性能异常低 + 5k 突跳 + 20k 后又掉**。
- **GS 不如 instanced VS**，除非 GS 内部做早剔除。
- **GS 吞吐会因 FS interpolants 增加而下降**（NVIDIA 敏感）。
- **Randomized blade index**（反转 bit）在老架构上微幅提升，现代 GPU 不敏感。

## 链接到的概念

- [[opengl-draw-call-batching-sweet-spot]]
- [[draw-call]]
- [[batching]]
- [[gpu-driven-grass-tiles]]

## 原文

- 链接：https://outerra.blogspot.com/2016/01/procedural-rendering-performance-test-1.html
- 本地：`raw/articles/outerra.blogspot.com/2016-01-31_opengl-rendering-performance-test-1-procedural-grass.md`
