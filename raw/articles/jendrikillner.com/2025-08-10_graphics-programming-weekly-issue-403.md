---
title: Graphics Programming Weekly - Issue 403
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-403/
author: Jendrik Illner
published: '2025-08-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- introduces FSR Redstone, AMD’s upcoming suite of ML-powered neural rendering techniques
- includes Neural Radiance Caching for real-time global illumination, ML Ray Regeneration for restoring details from low sample counts, Super Resolution (FSR 4), including frame generation

![](../../assets/28f60a9190b58cd3.jpg)


- Siggraph course covering GPU Work Graphs for D3D12
- starts with an in-depth look at graphics and API history and remaining limitations that work graphs aim to solve
- provides detailed tutorials and examples for using the API and understanding related concepts
- additionally explains how the driver implementation maps it onto the hardware

![](../../assets/06bf836887749cce.png)


- 2025 editions of SIGGRAPH courses on physically based shading
- covers topics including OpenPBR implementation details, spectral rendering in RGB, strand shading for hair/fur/feathers, and neural materials
- additionally features talks on EON rough diffuse reflection, tone mapping in Gran Turismo 7, and bridging the gap between offline and real-time rendering
- Slides are already available

![](../../assets/30db519e79e0ec88.jpg)


- presents Disney Animation’s solution for handling massive Ptex datasets (1.5 TB) in GPU ray tracing using only 2 GB of GPU VRAM
- employs a fast LRU eviction scheme and caps GPU cache size to maintain zero-stall experience while preserving texture detail

![](../../assets/8b80f7dba7d1d8fa.png)


- introduces VK_AMDX_dense_geometry_format, a provisional Vulkan extension for using pre-compressed DGF data in acceleration structure builds
- eliminates performance and memory costs of separate decoding steps by providing DGF data directly to the GPU
- improves BLAS build time and reduces memory footprint on hardware with native DGF support

![](../../assets/707ba35367fa6bb2.jpg)


- NVIDIA AI Research Leaders present the latest breakthroughs in computer graphics and Physical AI
- Topics will include advancements in data generation, and their impact across industries from media to manufacturing

![](../../assets/cb249d1680d961eb.jpg)


- announces KosmicKrisp, LunarG’s new Vulkan driver for Apple hardware built within the Mesa 3D framework
- targets Vulkan 1.3 conformance level

![](../../assets/0eb5c9db2ac0f574.png)


- announces the first-ever Shading Languages Symposium scheduled for February 12-13, 2026, in San Diego, California
- Representative for GLSL, HLSL, MSL, OSL, Slang, SPIR-V, and WGSL will be in attendance
- Call for submission is open

![](../../assets/c2071a05abb2c138.jpg)


- explores a technique for “warping” probe data to approximate lighting information at different spatial locations
- describes an algorithm that uses planes and ray intersections to reproject cubemap data, similar to parallax mapping but applied to spherical probes
- presents a ShaderToy implementation that demonstrates the concepts

![](../../assets/b2fd860d03c35229.jpg)


- video tutorial demonstrating five different techniques for creating compelling skyboxes in Unity
- covers various approaches from basic cubemap setups to more advanced procedural and dynamic skybox implementations
- provides practical tips for achieving high-quality atmospheric effects and environment lighting in Unity projects

![](../../assets/44245ea8f8e21820.jpg)


- video emphasizing the importance of profiling and analysis before starting on the implementing of performance optimizations
- discusses methodologies for identifying performance bottlenecks rather than making assumptions
- provides guidance on using profiling tools and data-driven approaches to make informed optimization decisions

![](../../assets/c66f754c9aeac95a.jpg)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.