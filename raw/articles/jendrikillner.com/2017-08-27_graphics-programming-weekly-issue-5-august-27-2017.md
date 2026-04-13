---
title: Graphics Programming weekly - Issue 5 — August 27, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-5/
author: Jendrik Illner
published: '2017-08-27'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[The vulkan device simulation layer](https://www.saschawillems.de/?p=2485)

- useful to simulate less capable GPUs by returning lower device limits via queries
- pre-build device simulation layer
- how to set it up and use it


[Vulkan SPIR-V shader size reduction using spirv-opt](https://www.lunarg.com/wp-content/uploads/2017/08/SPIR-V-Shader-Size-Reduction-Using-spirv-opt_v1.0.pdf)

- disusses which and how to order spirv-opt passes to reduce spir-v size up to 60 % (still 40 % bigger then dx byte code)


[Beginners Guide to Vulkan](https://www.khronos.org/blog/beginners-guide-to-vulkan)

- list of vulkan tutorials aimed at beginners


[Improving Vulkan Breakout - Comparing Uniform Data Transfer Methods In Vulkan](http://kylehalladay.com/blog/tutorial/vulkan/2017/08/30/Vulkan-Uniform-Buffers-pt2.html)

- compares different methods of updating constants and their associated gpu cost


[NVIDIA TESLA V100 GPU ARCHITECTURE- whitepaper](https://images.nvidia.com/content/volta-architecture/pdf/Volta-Architecture-Whitepaper-v1.0.pdf)

- new tensor cores designed for machine learning
- mixed precision 4x4 matrix multiplies and add
- exposed in cuda

- unified L1 data cache and shared memory
- 128 KB, configurable split between cache and shared memory

- can excute float and int instruction simultaneously
- better link between CPU and GPU memory system
- copy engine can now handle page faults without causing fatal faults
- independent thread scheduling, diverge at sub-wrap granuality
- better support for multiple applications using the same GPU


[Radeon GPU Profiler (RGP) v1.0.2](https://github.com/GPUOpen-Tools/Radeon-GPUProfiler/releases)

- new version released, adding support for vega
- navigation improvements
- UI and stability improvements


[MTuner - Now open source](https://github.com/milostosic/MTuner)

- MTuner is a C/C++ memory profiler and memory leak finder for Windows, PS4, PS3, etc.
- previously a paid product, now open source


[Comparison of OpenGEX, Collada, and glTF](http://opengex.org/comparison.html)

- good overview of all aspects of OpenGEX, collada and glTF
- list weakness of glTF from his perspective, make sure to read the next link for an alternative view


[A small defense of glTF 2.0 on its comparison against OpenGEX](https://godotengine.org/article/small-defense-gltf)

- provides an alternative few to the previously mentioned link
- the author sees many design decisions as strengths instead of weaknesses
- also mentions missing transforms tracks in glTF


[Antialiasing Complex Global Illumination Effects in Path-space](https://belcour.github.io/blog/slides/2017-covariance-filtering/slides.html#/)

- idea: limit materials frequency to reduce noise
- reformulation of anti-aliasing in freyuency domain
- overview of antiliasing method and implementation details
- and results


[Last Month on DirectX Shader Compiler (2017-08-24)](https://blogs.msdn.microsoft.com/marcelolr/2017/08/25/last-month-on-directx-shader-compiler-2017-08-24/)

- starting support for true 16 bit floats
- spir-v improvements
- better pix support


[Emotion Challenge: Building a New Photoreal Facial Performance Pipeline for Games - activision](https://research.activision.com/t5/Publications/Emotion-Challenge-Building-a-New-Photoreal-Facial-Performance/ba-p/10360541)

- pipeline overview
- how to aquire material, challenges
- transform into game ready rig


[Fluxed Animated Boundary Method](https://disney-animation.s3.amazonaws.com/uploads/production/publication_asset/146/asset/splash_v12.pdf)

- method to control particles based simulations (water) to create art directed results