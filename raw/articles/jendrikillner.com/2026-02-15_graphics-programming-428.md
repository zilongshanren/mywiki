---
title: Graphics Programming 428
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-428/
author: Jendrik Illner
published: '2026-02-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- blog post that looks back at Khronos Group’s 25-year history of enabling graphics programming across platforms
- traces the evolution from OpenGL and OpenGL ES through WebGL, Vulkan, and OpenXR to modern standards like Slang for neural rendering
- closes with a look at the next years of collaboration

![](../../assets/75c0018d68d5e43b.jpg)


- comprehensive walkthrough of implementing halftone effects as shaders from basic circular dot grids to advanced variants
- explores multichannel halftoning with RGB and CMYK color separation
- presents techniques for breaking grid constraints, enabling surface tension effects
- additionally shows how to integrate interactivity

![](../../assets/065a29cc844e2481.png)


- recording of a live stream showing a walkthrough on how to update a Vulkan app to use the new Descriptor Heaps extension
- showing the necessary definitions in the spec and how to integrate it into an application

![](../../assets/8b03617856c0085e.png)

- tutorial on using the Vulkan compute‑shader pipeline to render a Shadertoy‑style by integrating compute work into the application
- walk-through covers all the required pieces of the API and how they interact
- full source code is available

![](../../assets/e1a419b82ac7d49e.png)

- explores using small multilayer perceptrons (MLPs) to encode graphics data like radiance, irradiance, depth, and BRDF information
- compares MLP-based encoding against traditional methods like Spherical Harmonics
- discusses trade-offs in storage size and quality, as well as implementation challenges

![](../../assets/d4dc2c74bedfbb22.png)


- documents insights from building an immediate-mode GUI library
- covering interactions and layout logic as well as rendering constraints
- presents a tile-based SDF-based renderer to dispatch specialized shaders for improved occupancy

![](../../assets/76f6fa639696df1c.png)


- presents an updated Sponza glTF model with cleaned-up uncompressed PNG textures
- compares AVIF texture compression with runtime GPU compression via Spark against precompressed KTX formats
- demonstrates memory and quality comparisons

![](../../assets/70be16476e39a407.png)


- announces the formation of a Ecma Technical Committee to standardize HLSL as a cross-platform shader language
- traces HLSL’s evolution from DirectX 9, DXC, Clang integration, and the importance of Google’s SPIRV code generation contributions
- commits to public development on GitHub with conformance test suite

![](../../assets/d9b786f62e55cd1f.jpg)


- details progress on Clang HLSL implementation, including improved root signature diagnostics
- explains the rationale behind standardizing HLSL through Ecma TC 57 to address cross-platform shader build pipeline complexity and quality issues
- announces new features to combine Cooperative Vector and Wave Matrix capabilities for efficient neural network evaluation in shaders

![](../../assets/7fbbf65ef897bfac.png)


- implements AMD’s FidelityFX Single Pass Downsampler for Apple Metal API, generating depth pyramid mipmaps in one compute pass
- explains threadgroup organization with 16×16 threads processing 64×64 pixels using threadgroup memory to avoid device memory round-trips

![](../../assets/84d6e1f801403e31.png)


- presents an adaptive sampling and denoising pipeline designed for less than one sample per pixel path tracing systems
- introduces stochastic sample placement formulation enabling gradient estimation
- demonstrates consistent improvements over uniform sparse sampling, particularly in reconstructing specular highlights and shadow boundaries using tonemapping-aware training

![](../../assets/c2bfc70b838152f1.png)


- analyzes Michael Abrash’s hand-crafted x86 assembly optimizations in Quake’s software renderer
- details key techniques including FPU pipeline parallelization, hiding multiplication latency, self-modifying code, and overlapping FDIV with integer pipelines

![](../../assets/7b03feec106d718b.png)


- derives mathematical equations for estimating stopping/starting times and distances from critical spring damper character movement systems
- uses Lambert W function (product logarithm) to solve for stopping times from spring parameters
- presents methods to fit spring half-life parameters from measured animation data, including “true half-life” definition based on exact halfway-point timing

![](../../assets/5c19ea07ba658901.png)

Thanks to [Aras Pranckevicius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.