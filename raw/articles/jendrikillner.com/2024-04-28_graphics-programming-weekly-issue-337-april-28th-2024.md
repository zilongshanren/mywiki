---
title: Graphics Programming weekly - Issue 337 - April 28th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-337/
author: Jendrik Illner
published: '2024-04-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the presentation is packed with detailed information about the process of implementing shader graph support into the Nanite shading model
- starts with an overview of the system and discusses the steps taken to reach the current support level
- provides many details on the lower-level aspects and how GPU hardware influences decisions
- additionally explains how the system has been optimized on PS5 and Series X with console-level access
- also shows that work graphs for PC enable a new set of optimizations

![](../../assets/cf6f1e2c649a78e7.jpg)


- The Master Thesis is a collaboration with Remedy Entertainment and discusses the implementation of a denoising solution for direct lighting
- the focus is to find a solution that balances performance and quality to allow real-time utilization of consoles
- reviews existing solutions and provides evaluation methods to provide analysis capabilities
- discusses the implementation and tradeoffs done
- presents performance, memory, and image comparisons of the developed solution against existing solutions

![](../../assets/e0b820e3163df8e0.png)


- the start of a series of articles covering the implementation of ray tracing for a voxel system
- presents the initials of light and shadow calculations
- concludes with challenges to the reader to improve their understanding of the material

![](../../assets/972983fafc5509ee.png)


- the blog post shows how to implement Acceleration Structure compaction using D3D12
- this compaction step is run on the GPU timeline and often reduces the memory size required by 40%
- discusses the necessary API steps, GPU synchronization, and memory management strategies

![](../../assets/aac13936d430e1c7.png)


- the article provides a full explanation of the derivation of multiple-importance sampling
- explains the different components and how to combine them correctly

![](../../assets/542de76a28e765bc.png)


- the article explains how to implement a marching cube compute shader
- the implementation is shown both in Vulkan and WebGPU
- compares the performance of both implementations and finds that WebGPU performance is close to native Vulkan

![](../../assets/76b86f81177e6825.png)


- a blog post covering the effect of using C++ final on a ray-tracing demo
- the author presents the findings with several platforms, compilers, and scenes and presents the performance results

![](../../assets/87c9e8e11f2da254.png)


- this page serves as a starting point for the articles of the author
- covering topics such as BVH building series, Probability Theory, CPU Optimization series
- also contains various articles on Ray Tracing, graphics techniques, and fixed point math

![](../../assets/ff4a4a81ea938ef1.jpg)


- the article introduces how shaders from GPU Profiler captures can now be opened in the GPU Analyzer for more detailed investigation
- additionally shows UI updates and presents how instruction latency provides more information about where the latency occurs

![](../../assets/6639f77ac806ec72.png)


- the video presentation (free login required) discusses the implementation details of Path Tracing within the Alan Wake 2 technology stack
- starts with an overview of the implementation used (vertex accessing, BVH creation, dealing with dynamic geometry, etc.)
- shows how Opacity Micromaps are used for alpha-tested geometry
- from there, explain how Path tracing has been implemented, covering the whole pipeline from shading, shadows, reflections, and reconstruction techniques

![](../../assets/2d56fb504b43a163.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.