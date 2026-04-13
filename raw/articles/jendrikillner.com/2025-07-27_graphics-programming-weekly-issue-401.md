---
title: Graphics Programming Weekly - Issue 401
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-401/
author: Jendrik Illner
published: '2025-07-27'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- Second episode in a game optimization series covering the graphics pipeline and different rendering approaches
- explains the stages of the graphics rendering pipeline
- discusses the differences between deferred and forward shading and how they impact performance characteristics

![](../../assets/72236bcd23b31851.png)


- Technical breakdown of a 258-character shader that creates glowing, fluid particles using raymarching and turbulence techniques
- explains how the compact code handles raycasting, 3D rotation, camera displacement, and particle distribution

![](../../assets/3d0125bcfe2bd4f0.png)


- describes how to diagnose stuttering issues in Trackmania using profiling tools without access to the source code
- uses Superluminal profiler to identify patterns and library calls to track down performance bottlenecks
- demonstrating how performance analysis can work without debug symbols

![](../../assets/3fc8840502adf6af.png)


- SIGGRAPH 2025 paper presenting a neural approach for estimating spatially varying light selection distributions in many-light scenarios
- uses a neural network trained to predict light selection distributions based on local information
- integrates with light hierarchy techniques and introduces residual learning to accelerate convergence during training

![](../../assets/5d6992701febb341.png)


- Educational breakdown of how AI image and video generation systems function under the hood
- explains the mathematical and algorithmic foundations behind diffusion models and neural networks used for content generation
- tries to explain and develop intuitions into the process from noise to coherent images, covering training methodologies and inference techniques

![](../../assets/e829fb476be4bbf4.png)


Here at JECO, we’re building automated optimisation tools for all software, on any device, starting with video games - saving hours of developer time, costs and carbon emissions. We’re currently looking for purpose-driven and talented Intermediate C++ Programmers to join our team and work on developing our industry-first tools.

![](../../assets/bf7eaf1cf1859bfa.png)


- announces Mozilla’s release of WebGPU support on Windows in Firefox 141, bringing modern GPU access to the web
- built on the WGPU Rust crate, providing a unified interface to Direct3D 12, Metal, and Vulkan across platforms
- discusses ongoing performance improvements

![](../../assets/0042465d500e210d.png)


- interview with LLVM and Swift creator Chris Lattner discussing GPU programming languages and their design challenges
- explores the evolution of GPU programming models and the unique constraints that influence language design for parallel computing
- focuses on the work on the Mojo programming language that allows CPU+GPU execution without CUDA

![](../../assets/d1f41c46e7643881.png)


- The Graphics Programming Conference in Breda for November 18th-20th, 2025, has announced its first set of talks
- covers topics ranging from real-time path tracing and volumetric rendering to GPU particle systems and mobile game optimization
- There are still a couple of days left to submit a talk

![](../../assets/758d0cb465dac929.png)

Thanks to [Nathan Reed](https://www.reedbeta.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.