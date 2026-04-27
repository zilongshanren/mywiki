---
tags: [source, graphics, multi-gpu, deferred-rendering, game-engines]
date: 2026-04-27
sources: 1
---

# Multi-GPU Game Engine（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel|Wolfgang Engel]] 2015 年 5 月发表的文章，探讨在高端仿真或游戏场景中将延迟渲染管线拆分到 4–8 颗消费级 GPU 上运行的架构思路。

## 摘要

文章以战场仿真为背景，描述了一种在 DirectX 12 / Vulkan（及更早的 CUDA）下可行的多 GPU 流水线拆分方案：GPU0 负责 Z prepass + G-Buffer 填充，GPU1 负责延迟光照与阴影，GPU2 负责粒子与植被，GPU3 负责屏幕空间材质（皮肤等）与 PostFX，GPU4 以上处理物理与 AI。各 GPU 依次消费前一个 GPU 的输出，形成一条串行管线，代价是引入 2–3 帧延迟。文章还给出了 CPU 核心数与 GPU 数的经验比（每 GPU 约需 2–4 个 CPU 核心）、RAM 与 VRAM 的配比建议，以及 4K 分辨率下 G-Buffer 约 500–1 GB 的内存估算。Engel 本人在文章结尾注释，这份草稿写于两年前，当时 G-Buffer 仍是合理方案，但随着高分辨率显示器普及，他已在评论区指向 Visibility Buffer 作为后继替代。

## 关键要点

- 管线按渲染阶段切分：G-Buffer → 光照/阴影 → 粒子/植被 → PostFX，每阶段分配独立 GPU
- 多 GPU 串行可并行执行但会引入 2–3 帧渲染延迟；60 fps / 120 fps 下基本不可感知
- G-Buffer 也可以在多颗 GPU 之间进一步横向拆分（Z prepass / diffuse-normal / terrain 各自一颗）
- CPU-GPU 配比经验：每颗 GPU 需 2–4 个 CPU 核心；RAM 至少为 GPU 显存总量的 2 倍
- 4K 四张 32-bit 渲染目标约占 126 MB，含 MSAA 可接近 500 MB–1 GB
- Engel 事后承认 G-Buffer 在 4K 下因带宽瓶颈已不再适合，转向 [[visibility-buffer|Visibility Buffer]]

## 链接到的概念

- [[multi-gpu-rendering]]
- [[deferred-rendering]]
- [[visibility-buffer]]
- [[async-compute]]
- [[people/wolfgang-engel]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2015/05/multi-gpu-game-engine.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2015-05-31_multi-gpu-game-engine.md`
