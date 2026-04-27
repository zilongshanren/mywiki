---
tags: [source, 渲染, compute-shader, gpu, amd, gcn, 性能优化]
date: 2026-04-27
sources: 1
---

# GDC 2014 – Compute Shader Optimizations（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel]] 在 2014 年 GDC Sony 展台发表的 15 分钟演讲预告帖，覆盖针对 AMD Radeon 6770、7750、7850 三款 GPU 的 compute shader 优化测量结果。

## 摘要

Engel 与 Confetti 团队在为 AAA 游戏优化 PostFX compute pipeline 过程中积累了一组实操经验，这次演讲把其中的 GPU 并行减少（parallel reduction）等核心模式以跨代对比的方式呈现。文章本身是演讲预告，核心内容后来以博客系列补全。演讲不针对 PS4，面向 PC AMD GPU。主要优化主题包括：TGSM 的顺序访问与 bank layout、何时展开循环（loop unrolling）、地址算术与循环指令的 overhead、利用 wavefront 跳过内存屏障、数据预取进 shared memory、以及 shared memory 中的数据打包。

## 关键要点

- TGSM（线程组共享内存）的 bank 布局决定了顺序访问的效率，随机访问会引发 bank conflict
- 循环展开在 AMD GCN 上有条件地有益，但地址算术和循环指令本身有不可忽略的 overhead
- Wavefront 级别的可见性在某些条件下可以省去显式内存屏障（`GroupMemoryBarrierWithGroupSync`）
- 预取数据进 LDS（Local Data Share）可以隐藏全局内存延迟
- 将多个小值打包进 shared memory 可以减少 LDS 寄存器压力和带宽
- 对比两代 AMD GPU 的数字清楚地说明哪些经验规则在当代 GPU 上仍然成立

## 链接到的概念

- [[rendering/gcn-compute-tgsm-patterns]]
- [[computer-systems/gcn-architecture]]
- [[computer-systems/gcn-wave-occupancy]]
- [[rendering/async-compute]]
- [[rendering/gpgpu-compute-simt-model]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2014/03/gdc-2014-compute-shader-optimizations.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2014-03-13_gdc-2014-compute-shader-optimizations.md`
