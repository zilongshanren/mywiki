---
tags: [人物, 作者, planet-engine, 程序化地形]
date: 2026-04-19
sources: 11
---

# Outerra Team（Brano Kemen / Ladislav "Angrypig" Kralik）

Outerra（Anteworld）是斯洛伐克出品的**全球尺度行星引擎**，由 Brano Kemen（Twitter `@cameni`）与 Ladislav "Angrypig" Kralik 长期开发。引擎核心是一个把整颗地球按 quad-sphere 映射、在运行时以 fractal 细分增强基础 DEM（SRTM/NasaDEM）并在 double precision 下渲染的系统，常被 simulator 社区用来做航空/地面载具的世界。

他们的 blog（outerra.blogspot.com）从 2008 年起陆续公布**真实地形数据处理**（SRTM 30m/90m vs NasaDEM、bathymetric 合并）、**OpenGL 性能实测**（procedural grass / building block 的 draw call 吞吐曲线、纹理绑定批处理）、**行星尺度渲染数值问题**（fp64 GLSL 缺失三角函数用 Remez 补齐、[[logarithmic-depth-buffer|对数深度缓冲]]的完整精度推导）与**球面地形剔除**（仿射剪切空间内的精确视锥测试）等一手经验，是行星/地形引擎领域少有的把实测数据和推导过程都贴出来的团队。

## 相关

- [[planet-terrain-dem-pipeline]] —— 基于 SRTM/NasaDEM 的全球地形数据处理与 fractal resample 策略
- [[opengl-draw-call-batching-sweet-spot]] —— 5k-20k 三角形 per instanced draw 的跨厂吞吐最优区间
- [[fp64-sincos-minimax]] —— GLSL 下用 Remez minimax 补齐 fp64 sin/cos
- [[faster-math-functions]] —— Robin Green 讲的同类方法论
- [[draw-call]]
- [[procedural-grass-rendering]] —— 2012 年两阶段 canopy + 几何着色器草叶生成方案
- [[logarithmic-depth-buffer]] —— 行星尺度深度精度完整推导与实现
- [[sphere-mapped-terrain-culling]] —— 球面 tile 仿射剪切空间视锥剔除
- [[opengl-texture-bind-batching]] —— NVIDIA 纹理绑定性能陷阱与 bind group 解法
- [[fiber-based-job-scheduler]] —— Outerra jobmaster 异步 I/O 调度器

## Sources

- [[sources/outerra-srtm-30m-evaluation]]
- [[sources/outerra-opengl-perf-grass]]
- [[sources/outerra-opengl-perf-blocks]]
- [[sources/outerra-fp64-sincos]]
- [[sources/outerra-nasadem-comparison]]
- [[sources/outerra-procedural-grass]]
- [[sources/outerra-sphere-terrain-culling]]
- [[sources/outerra-depth-buffer-precision]]
- [[sources/outerra-log-depth-buffer]]
- [[sources/outerra-texture-bind-perf]]
- [[sources/outerra-async-job-scheduler]]
