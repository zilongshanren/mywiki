---
tags: [source, rendering, cpu-gpu, 输入滞后, vsync]
date: 2026-04-19
sources: 1
---

# What no one told you about the videocard: lagging 1 frame behind（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen|Joost van Dongen]] 2011 年 10 月的文章，讲他在 Awesomenauts 做性能调优时发现的一件事：自己（以及他问过的多数资深图形程序员）对 CPU/GPU 时序的直觉是错的。

## 摘要

文章分两层讲同一件事。第一层是"错觉"：读完 OpenGL Red Book 后他以为 `SwapBuffers` 里 CPU 在等当前帧 GPU 完成——于是 CPU/GPU 互相空等很浪费。他实测 PS3/Xbox360/PC 都看到 CPU 在 swap 里长时间 block，据此写了多线程优化结果 FPS 完全没动。第二层是"真相"：实际 GPU 永远落后 1 帧，`SwapBuffers` 里等的是**前一帧**的 GPU 完成；GPU-bound 情况下 GPU 一直有活干，CPU 优化无益——他那套多线程是在对着已经不瓶颈的部分优化。代价是输入滞后至少 +1 帧，但换来 FPS 大幅提升值得。驱动侧的 "Max Prerendered Frames" 会把落后帧数加到 2–3 帧，30fps 下能到 100 ms 输入滞后。fence 可以显式限制落后不超过 1 帧。VSync 让这层延迟更复杂，triple buffer 只在帧时间抖动大时才有用。

## 关键要点

- **先定瓶颈**：优化前必须知道是 CPU-bound 还是 GPU-bound，Awesomenauts 当时是 GPU-bound，CPU 多线程毫无 FPS 收益。
- **GPU 天然落后 1 帧**：`SwapBuffers` 等的是前一帧完成；驱动层 CPU/GPU pipelining 默认开启。
- **输入滞后的成因**：game state → screen 中间多 1 帧 GPU 管线；默认接受换 FPS。
- **Max Prerendered Frames**：NVIDIA 面板默认 3 帧，30fps 下 ≈100 ms 滞后；Ogre 用户 / Wine 下 Proun 的长输入滞后都是这个原因。
- **fence**：DirectX/OpenGL 高级功能，显式卡死"GPU 落后不超过 N 帧"。
- **不要 glFinish() 实现 VSync**：那会退回到错觉模型里 CPU/GPU 互相空等的糟糕版本。
- **triple buffering 只在抖动下有用**：恒定 FPS 下只增加滞后不增加吞吐。

## 链接到的概念

- [[cpu-gpu-pipelining-input-lag]]
- [[frame-pipeline-latency]]
- [[frames-in-flight]]
- [[bottleneck-analysis]]
- [[gpu-fence-timeline-semaphore]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2011/10/what-no-one-told-you-about-videocard.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-10-23_what-no-one-told-you-about-the-videocard-lagging-1-frame-beh.md`
