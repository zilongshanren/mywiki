---
tags: [source, 渲染, 纹理, gpu, ptex, 流送, hyperion]
date: 2026-04-19
sources: 1
---

# SIGGRAPH 2025 Talk — A Texture Streaming Pipeline for Real-Time GPU Ray Tracing（Yining Karl Li / Code & Visuals）

[[yining-karl-li]] 2025 年 8 月对 SIGGRAPH 2025 talk（合著人 Mark Lee、Nathan Zeichner）的个人配套博客，讲 Disney Animation 自家实时 GPU 路径追踪预览渲染器的纹理流送系统。

## 摘要

Disney Animation 纹理工作流 100% 基于 Ptex，于是他们的 GPU 纹理流送系统必须围绕 Ptex 设计：tens of thousands 个 Ptex 文件规模下，还要零停顿、帧率稳定，即使 GPU cache 被强制全清也不掉帧。这是团队第二次做 GPU Ptex 流送——Joe Schutte 的第一代原型验证了不少想法（比如用 cuckoo hash 做 key 存储），二代由 Mark Lee 主写，Nathan Zeichner 让系统同时服务 CUDA/Optix 路径追踪预览与 Hydra Storm 的内部 fork。作者借 Mythical Man-Month 第 11 章强调「plan to throw one away」的价值，并从 Moonray（Lee et al. 2017）与他自己 2018 年博客总结出一条关键决策：随机路径追踪下，与其在 Ptex 里实现硬派跨面各向异性滤波，不如「点采样 + 两层 MIP 线性插值」。

## 关键要点

- 不用硬件 texturing，全部在 CUDA 里按原始 Ptex face 内存块管；无预处理、无离线 atlas、无 MIP 预构建。
- GPU cache 总量被刻意 cap 得很小，用快速 LRU 驱逐应对溢出。
- 早期 McDonald & Burley 2011 要走 OpenGL/DX 纹理路径；Pixar RTP / Kim et al. 2011 走 atlas 路径，但 atlas 方案在 MIP 生成时会跨不相邻 face 漏色。
- 打破「Ptex 非相干访问一定慢」的通行假设：Hyperion 的相干性收益其实来自 sorted deferred shading（[[wavefront-path-tracing]]），不是 Ptex 本身；Disney GPU 预览用 depth-first integrator，二次 bounce 访问完全非相干也能跑在交互帧率。
- 避开 second-system effect 的一个好例子：小、快、易维护，并不是再造一个巨物。

## 链接到的概念

- [[ptex-gpu-streaming]]
- [[hyperion-renderer]]
- [[wavefront-path-tracing]]

## 原文

- 链接：https://blog.yiningkarlli.com/2025/08/texture-streaming-pipeline-for-real-time-gpu-ray-tracing.html
- 本地：`raw/articles/blog.yiningkarlli.com/2025-08-10_siggraph-2025-talk-a-texture-streaming-pipeline-for-real-tim.md`
