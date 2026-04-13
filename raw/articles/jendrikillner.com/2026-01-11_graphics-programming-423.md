---
title: Graphics Programming 423
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-423/
author: Jendrik Illner
published: '2026-01-11'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- discusses Sebastian Aaltonen’s “No Graphics API” article
- examines which graphics-specific functions might be stripped and the implications for multi-device/multi-process setups
- highlights practical concerns (write-combining memory pitfalls, deadlock avoidance, and 32-bit compatibility)

![](../../assets/ced30a796ff2fb77.png)


- introduces Shader2Human, a lightweight HLSL/GLSL library that exposes debugging tools directly from shaders
- provides macros and helpers to make shader diagnostics and rapid iteration easier without heavy capture tooling
- slides walk through usage patterns and examples for faster shader development

![](../../assets/ee4995ba9f32c95a.jpg)


- tutorial on GPU memory concepts, covers movement between VRAM and compute units, and the role of memory speed, interface width and bandwidth
- explains memory-bound vs compute-bound operations via arithmetic intensity and practical tinygrad benchmarks, with concrete optimization guidelines
- includes hands-on examples and timing tips for accurate GPU benchmarking and optimization

![](../../assets/8efbefd754cb026e.png)


- demonstrates how lightweight neural networks can be integrated into CPU-based production path tracers to improve memory, speed, and image quality under low-latency constraints
- discusses practical inference considerations on CPU and the trade-offs when bringing ML into offline rendering pipelines

![](../../assets/94ed742c4481deed.png)


- investigates a seam artifact in HDRP’s LD preconvolution caused by reusing identical sample sequences per pixel combined with local-frame singularities at cube-face boundaries
- suggests practical fixes and recommends decorrelation as a pragmatic patch

![](../../assets/ca134977b9d8735f.png)


- presents a low-memory approach for globally sorting mostly-ordered event streams
- leverages data patterns (nearly sorted streams, local disorder) to prefetch and hide I/O, making global sorting cheaper
- discusses comparisons to k-way lazy merge and proposes a hybrid JIT-sort fallback

![](../../assets/afab132f029a113a.png)


- GPC 2025 archive with session descriptions and slides from a wide range of real-time graphics talks
- inluding Shader2Human (shader debugging), Blender Cycles architecture, real-time path tracing, neural shading, profiling & platform optimization talks

![](../../assets/d69546b0aa75297d.jpg)


- showcases an SDF-based engine for high-fidelity, non-destructive world edits
- covers architecture & optimizations:
- discusses ray-marching performance issues, physics/collision integration, terrain as SDF and practical trade-offs versus triangle meshes

![](../../assets/796430e255dffa34.png)


- practical tutorial on implementing indirect rendering in Vulkan, covering vertex/index/uniform buffer offsets, indirect buffers, and vkCmdDrawIndirect
- demonstrates a new pipeline class and shows how to enable indirect rendering

![](../../assets/26df1c8bb0c22d3d.png)


- walkthrough of programmatic audio analysis: techniques for computing FFTs, spectrograms and extracting features from audio signals
- includes code examples and visualizations to illustrate frequency vs time behaviour and practical tips for real-time analysis

![](../../assets/a56a79c26be129c5.png)

Thanks to [Eric Haines](http://erichaines.com/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.