---
title: Graphics Programming weekly - Issue 26 — February 11, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-26/
author: Jendrik Illner
published: '2018-02-11'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[The Peak-Performance Analysis Method for Optimizing Any GPU Workload](https://devblogs.nvidia.com/the-peak-performance-analysis-method-for-optimizing-any-gpu-workload/) [[wayback-archive]](http://web.archive.org/web/20180207042627/https://devblogs.nvidia.com/the-peak-performance-analysis-method-for-optimizing-any-gpu-workload/)

- how to use GPU counters to detect interactions between different hardware blocks
- discussion of case studies
- walkthrough of analysis, code examples to show optimizations and discussion of results

[Pre-Multiplied Alpha](https://github.com/dtrebilco/PreMulAlpha) [[wayback-archive]](https://web.archive.org/web/20180211164530/https://github.com/dtrebilco/PreMulAlpha)

- reduces color bleeding in alpha blending
- can represent Additive, Alpha Blend, and Multiply blend modes
- can vary the blend mode per-pixel, can be used to pre-combine effects

[SRV handling in D3D12 - twitter thread](https://twitter.com/rygorous/status/962473993109258240) [[wayback-archive]](https://web.archive.org/web/20180211164250/https://twitter.com/rygorous/status/962473993109258240)

- how to design for descriptor tables in D3D12
- goal is to only set a few root constants to point to the correct data

[Vulkan ASKs : Swapchain](https://timothylottes.github.io/20180206.html) [[wayback-archive]](https://web.archive.org/web/20180211204309/https://timothylottes.github.io/20180206.html)

- proposed vulkan extensions to improve swapchain and present interactions

[Profiling: Measurement and analysis](https://engineering.riotgames.com/news/profiling-measurement-and-analysis) [[wayback-archive]](http://web.archive.org/web/20180206220201/https://engineering.riotgames.com/news/profiling-measurement-and-analysis)

- overview of profiler types
- visualization of the memory layout and how it causes performance problems
- how to detect cache misses with CodeXL

[HLSLexplorer](http://astralcode.blogspot.ca/2018/02/hlslexplorer-is-out.html) [[wayback-archive]](https://web.archive.org/web/20180211204234/http://astralcode.blogspot.ca/2018/02/hlslexplorer-is-out.html)

- small tool that takes HLSL code, passes it to the shader compiler and shows the d3d11 shader disassembler output
- allows to select compiler flags and see the effects on the assembly
- similar to
[Pyramid](https://github.com/jbarczak/Pyramid), allows to see the native GPU disassembly as well

[A new microflake model with microscopic self-shadowing for accurate volume downsampling](https://hal.archives-ouvertes.fr/hal-01702000) [[wayback-archive]](https://web.archive.org/web/20180211164123/https://hal.archives-ouvertes.fr/hal-01702000)

- technique to preserve anisotropic attenuation and self shadowing when downsampling volume representations
- allows silhouettes of LODs to be better preserved

- showcase of a photogrammetry nature scene render in UE4