---
tags: [source, raytracey, OptiX, Fermi, 路径追踪]
date: 2026-04-19
sources: 1
---

# Design Garage: stunning Nvidia tech demo using raytracing（Sam Lapere, 2010-04-10）

[[sam-lapere|Sam Lapere]] 对 NVIDIA OptiX 团队 *Design Garage* 演示的感想笔记，同时抛出一张"理想 GPU 光追算法组合"清单。

## 摘要

博客本身很短：OptiX 团队把 *Design Garage* 做得相当漂亮，作者期望它能演进到更高级的算法——**双向路径追踪（BDPT）**、**Metropolis Light Transport（MLT）**、以及**随机渐进光子映射（SPPM）**——并认为三者组合几乎可以通吃 99.9% 的光照场景。他特别点名 SPPM（Hachisuka & Jensen）适合 GPU：**渐进式**（像路径追踪一样"最终收敛到正确解"）、**显存占用远小于普通 photon mapping**、能自然处理 DOF / 运动模糊 / 焦散；当时已有一份 GLSL 原型（Toshiya Hachisuka 的 `gpusppm`）在 HD4870 上跑到 **40 M photons/s**。

## 关键要点

- OptiX 的 *Design Garage* 被 Lapere 视作 [[gpu-unbiased-path-tracing|2010 GPU 无偏渲染爆发]]在 NVIDIA 侧的旗帜
- Lapere 判断理想组合 = BDPT + MLT + SPPM（前两个擅长复杂间接光，SPPM 擅长焦散）
- SPPM 对 GPU 友好：memory 小、渐进收敛、无偏
- 文章主要价值是**时间戳 + 技术口径**：看 2010 年一线 GPU 渲染观察者对"下一步算法"的预期

## 链接到的概念

- [[gpu-unbiased-path-tracing]]
- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[sam-lapere]]

## 原文

- 链接：http://raytracey.blogspot.com/2010/04/design-garage-stunning-nvidia-tech-demo.html
- 本地：`raw/articles/raytracey.blogspot.com/2010-04-10_design-garage-stunning-nvidia-tech-demo-using-raytracing.md`
