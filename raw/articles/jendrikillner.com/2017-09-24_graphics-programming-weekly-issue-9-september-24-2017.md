---
title: Graphics Programming weekly - Issue 9 — September 24, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-9/
author: Jendrik Illner
published: '2017-09-24'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Real-time Global Illumination by Precomputed Local Reconstruction
from Sparse Radiance Probes](https://users.aalto.fi/~silvena4/Projects/RTGI/index.html) [[wayback-archive]](https://web.archive.org/web/20170918150303/https://users.aalto.fi/~silvena4/Publications/Real-time_Global_Illumination_by_Precomputed_Local_Reconstruction_from_Sparse_Radiance_Probes.pdf)

- realtime global illumination technique
- using local precomputed data so that no long-range interactions is required between probes and receivers
- receiver depends only on a constant number of nearby probes

[Simple Parallel Rendering](http://ourmachinery.com/post/simple-parallel-rendering/) [[wayback-archive]](https://web.archive.org/http://ourmachinery.com/post/simple-parallel-rendering/)

- high level overview of how to structure object traversal for parrallel rendering

[Simple printf functionality for GLSL](https://github.com/msqrt/shader-printf) [[wayback-archive]](https://web.archive.org/web/20170925060552/https://github.com/msqrt/shader-printf)

- easy to use implementation of printf style debugging in GLSL

[Vulkan Shader Sample](https://sopyer.github.io/b/post/vulkan-shader-sample/) [[wayback-archive]](https://web.archive.org/web/20170925060714/https://sopyer.github.io/b/post/vulkan-shader-sample/)

- tutorial about getting vulkan shaders working and implementation of raytracing shadertoy in vulkan

[PIX 1709.18.004](https://blogs.msdn.microsoft.com/pix/2017/09/19/pix-1709-18-004/) [[wayback-archive]](https://web.archive.org/web/20170925060919/https://blogs.msdn.microsoft.com/pix/2017/09/19/pix-1709-18-004/)

- Dr. PIX “Bandwidth” page is now enabled on AMD and Intel
- Access tracking for bindless resources
- PIX knows what data was read or written via dynamic indexing now

- more performance warnings

[Deep Scattering: Rendering Atmospheric Clouds with Radiance-Predicting Neural Networks](https://tom94.net/data/publications/kallweit17deep/kallweit17deep.pdf) [[wayback-archive]](https://web.archive.org/web/20170925060959/https://tom94.net/data/publications/kallweit17deep/kallweit17deep.pdf)

- use Neural Networks to render clouds in 9 minutes instead of 36 hours

sample visible points of the cloud and, extract a hierarchical 3D descriptor of the cloud geometry with respect to the shading location and the light source. The descriptor is input to a deep neural network that predicts the radiance function for each shading configuration


- now open source

- proof-of-concept library which generates shader code from C#
- can generate HLSL, GLSL

[radeonsi: out-of-order rasterization on VI+](http://nhaehnle.blogspot.ca/2017/09/radeonsi-out-of-order-rasterization-on.html?m=1) [[wayback-archive]](https://web.archive.org/web/20170925061049/http://nhaehnle.blogspot.ca/2017/09/radeonsi-out-of-order-rasterization-on.html?m=1)

- explanation of out-of-order rasterization
- examples of cases where it can be used to gain a performance win

[Normals Compression](https://www.shadertoy.com/view/llfcRl) [[wayback-archive]](https://web.archive.org/web/20170925061123/https://www.shadertoy.com/view/llfcRl)

- Shadertoy that shows multiple ways to encode surface normals

- Linux GPU profiler similar to GPUView on Windows
- system level profiler that shows hardware execution
- can integrate custom markers and plots
- code:
[https://github.com/mikesart/gpuvis](https://github.com/mikesart/gpuvis)

[godot 3 renderer design explained](https://godotengine.org/article/godot-3-renderer-design-explained) [[wayback-archive]](http://web.archive.org/web/20170925013219/https://godotengine.org/article/godot-3-renderer-design-explained)

- aim is to have a really simple 3D renderer that is powerfull to common user needs
- rendering is seperated from the rest, running in seperate thread
- using a high level abstraction model
- to allow the backends to customize how techniques are implemented
- using a custom shader language
- short description of all passes

[CRYENGINE 5.4.0](http://docs.cryengine.com/display/SDKDOC1/CRYENGINE+5.4.0) [[wayback-archive]](https://web.archive.org/web/20170925061247/http://docs.cryengine.com/display/SDKDOC1/CRYENGINE+5.4.0)

- terrain system upgrades
- vulkan support
- subtance integration
- and much more