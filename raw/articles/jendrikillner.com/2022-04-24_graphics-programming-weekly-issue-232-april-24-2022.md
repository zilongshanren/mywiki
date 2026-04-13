---
title: Graphics Programming weekly - Issue 232 - April 24, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-232/
author: Jendrik Illner
published: '2022-04-24'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents an overview of the shader compilation pipeline in Wicked Engine
- presents how to track header dependencies when using the DXC shader compiler and how to detect changes to trigger recompilation
- presents pointers on how to unify Vulkan and D3D12 shaders as much as possible

![](../../assets/31389160cd482b9d.png)


- the Sponza rendering scene has been updated
- it now contains 4K PBR texture sets and high-resolution geometry
- optional packages such as curtains, ivy, trees, and emissive candles are available too
- additionally, a fully rigged and animated knight model has also been released

![](../../assets/cc8bce27404a8d4e.jpg)


- the article presents the screen space solution for Global Illumination
- presents the four steps of the process and how the individual results combine
- code examples for different steps are provided

![](../../assets/d1e8522263431953.png)


- the article presents the authors’ first experience with writing a compute shader to implement a Gaussian blur
- presents the different stages of the experiment, presenting performance numbers for different work sizes and execution patterns
- this shows how writing pixel shaders can outperform unoptimized compute shaders by a large margin

![](../../assets/9fbdf55a36f29acb.png)


- the article presents how to use a Surface Area Heuristic (SAH) to improve the quality of the BVH generation
- shows how much speedup can be achieved with the use of the heuristics
- it additionally covers additional performance optimizations through ordering changes and the usage of SSE

![](../../assets/070e8f70fe2bc3bc.jpg)


- the article presents improvements to the new profiler version
- contains support for raytracing performance counters and inline raytracing
- additionally, searching in the ISA of the pipeline is directly supported now

![](../../assets/d0e60ffbcdce4578.jpg)


- the article presents how to reduce the time required for the presented BVH build from seconds to milliseconds
- shows an alternative split plane and binning algorithms to speed up the process

![](../../assets/cd6511dca9a9f30f.jpg)


- the video tutorial explains how to modify UVs from a shader graph in both Unity and Unreal Engine 5
- explains the concepts step by step and presents the results

![](../../assets/3e37aff0ead4a451.png)

- the talk presents the Slang Shading language
- presents how generics and interfaces are implemented in an efficient way for GPU execution
- shows how the language has been deeply integrated into the Falcor material model
- explains the building blocks for cleaner parameter binding logic across APIs

![](../../assets/52d638ab7ee03c7b.png)

- program for the ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games has been released
- the conference will take place Tuesday, May 3, through Thursday, May 5, in a virtual setting

![](../../assets/a257a036a8ac0cf6.png)

- the Digital Foundry video analyses the performance of the UE5 Engine
- presents a comparison between hardware-accelerated and software only Lumen in terms of performance and quality
- shows how CPU limited the demo tends to be

![](../../assets/21be3533e5993815.png)

- the video provides an overview of tessellation shader concepts
- shows how to implement a basic tesselation shader using OpenGL
- the example presented shows how to adjust the tessellation level of a plane dynamically around the curser

![](../../assets/b37a4bf5af9a256f.png)

- the article introduces standard terms and concepts used in compiler literature
- applies the concept to start explaining the conversion from unstructured control flow into structured control flow
- discusses common patterns and issues found in the DXIL generated from DXC

![](../../assets/48127f079d232fd6.png)

Thanks to [Leonardo Etcheverry](https://www.linkedin.com/in/leonardoetcheverry/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.