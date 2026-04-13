---
title: Graphics Programming Weekly - Issue 397
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-397/
author: Jendrik Illner
published: '2025-06-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a work graph-based procedural system for generating and rendering trees entirely on the GPU
- shows how the model used to generate the tree structure
- presents how this is mapped onto the work graph execution logic
- additionally discusses how seasonal effects and wind effects are integrated

![](../../assets/1c2b29bba717ea36.png)


- introduces Importance Deep Shadow Maps (IDSM), a real-time algorithm for rendering shadows of semi-transparent objects
- adaptively distributes shadow samples based on camera importance
- achieves significant speedups over hardware ray tracing while maintaining visual fidelity

![](../../assets/aa1ff6313f09ebf6.png)


- an article discusses optimizing a CUDA-based ray tracer to outperform Vulkan/RTX implementations on the same hardware
- demonstrates how aggressive inlining, branchless material evaluation, and custom RNGs yield significant speedups
- provides benchmarks and practical advice for optimizing ray tracing performance
- additionally, it presents a discussion of how to interpret the results

![](../../assets/9a9dadcdf34c9c8b.png)


- provides an introduction to profiling and optimizing applications on AMD GPUs for ROCm workloads
- outlines key tools in the ROCm ecosystem for tracing, counter collection, and kernel analysis

![](../../assets/2f2e777e12a39f84.jpg)


- provides an in-depth analysis of Nvidia’s Blackwell GPU architecture
- compares Blackwell’s design, memory subsystem, and compute performance to AMD’s RDNA4
- discusses architectural tradeoffs, cache design, and the implications for high-end GPUs

![](../../assets/0edc061c69a9f5b3.png)


- announces Mozilla’s plan to ship WebGPU in Firefox 141 on Windows
- notes that WebGPU is already enabled in Firefox Nightly and will expand to other platforms

![](../../assets/db371bf2162bfb7f.png)


- virtual meet-up that will introduce the Slang shader reflection API
- going to highlight common pitfalls and best practices for accessing shader metadata

![](../../assets/6752449466689c05.png)


- the very detailed presentation discusses the geometry rendering pipeline on the RE ENGINE
- covers meshlet rendering, software rasterization, visibility buffers, shadow rendering, and more
- additionally contains Questions and Answers documents from the audience and developers

![](../../assets/d4cc3689c8ca1848.jpg)


- the video discusses the alignment requirements for Buffers in Vulkan
- explains why a validation error message appears and how to resolve it
- shows why the problem happens and how to resolve it in practice

![](../../assets/19f47b2b3d4a1ba5.png)


- video recording of I3D paper presentations
- covering Hierarchical Neural Skinning Deformation with Self-supervised Training for Character Animation, Foveated Animations for Efficient Crowd Simulation
- Aokana: A GPU-Driven Voxel Rendering Framework for Open World Games as well as Transform-Aware Sparse Voxel Directed Acyclic Graphs

![](../../assets/7c524141949690a8.png)

Thanks to [JanHaraldFredriksen](https://x.com/jhfredriksen) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.