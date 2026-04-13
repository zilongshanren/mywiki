---
title: Graphics Programming Weekly 433
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-433/
author: Jendrik Illner
published: '2026-03-22'
source_blog: Graphics Programming Weekly — Jendrik Illner
source_site: https://www.jendrikillner.com/
category: Blogs
fetched: '2026-04-13'
---

- presents an analytic approach to rendering localized fog volumes with varying density using radial density functions bounded by geometric primitives
- derives closed-form antiderivatives for each density function
- linear transforms applied to the ray allow volumes to be arbitrarily scaled and rotated

![](../../assets/c36f3cebb9c6abba.png)


- uses 2D SDFs in a ShaderGraph shader to procedurally draw pool balls
- presents how to apply the ball numbercorrectly on both the front and back of the sphere

![](../../assets/4a795b430ed5b241.jpg)


- Eric Lengyel reflects on 10 years of the Slug algorithm for GPU text rendering directly from Bézier curve data, detailing evolutionary simplifications since the 2017 JCGT paper
- introduces “dynamic dilation” for antialiasing without any manually-tuned constant
- announces that the Slug algorithm patent is permanently dedicated to the public domain with reference HLSL shaders—including dynamic dilation—released on GitHub under the MIT license

![](../../assets/37dd4740ff95f4f8.png)


- WebGPU/WGSL port of Eric Lengyel’s Slug text rendering algorithm
- implements the CPU-side pipeline that extracts Bézier curves, and partitions them into vertical and horizontal bands;
- the WGSL shaders then evaluate the bands to rasterize glyphs on the GPU

![](../../assets/e9674334e4cbaed6.png)


- CVPR 2026 paper presenting a parallelised CUDA implementation of differentiable geodesics on 3D mesh surfaces
- proposes two differentiation methods: an Extrinsic Proxy for fast gradient approximation and Geodesic Finite Differences for higher-accuracy
- demonstrates the technique in different applications

![](../../assets/08cabebc1337f2b8.png)


- AMD releases Smoldr, an open-source scripting tool for running DirectX 12 compute and raytracing shaders without writing any C++
- a plain-text script defines HLSL sources, buffers, root signatures, pipelines, and dispatches;
- basic verifications commands allow verifying and printing output values for testing

![](../../assets/88ea2bb12220367c.png)


- White paper has been updated to reflect improvements introduced in Vulkan SDK 1.4.335
- Vulkan Configurator can now export a tested layer configuration directly into all supported formats, unifying layer configuration behaviour

![](../../assets/854881eb4bc8c57a.jpg)


- deep dive into the graphics features of Apple’s M5 and A19 GPUs targeting games and pro app workflows
- covers hardware design updates including universal texture compression support and an upgraded hardware ray tracing unit
- introduces new profiling tools to help developers identify and exploit performance opportunities on M5 GPUs

![](../../assets/e52dceac20bdd905.png)


- explores making an AMD GPU control an NVMe device directly, bypassing the CPU for I/O submission and data placement into VRAM
- discussins and presents the kernel-level paths to allow access to the required pages from DMA and GPU shader access
- documents the cache coherency challenges encountered

![](../../assets/6ba46d408b89c079.png)


- overview of meshoptimizer, covering the full offline mesh processing pipeline
- covers mesh shader meshlet generation, mesh simplification for LOD hierarchies, specialized mesh compression
- additionally talks about cluster_load.h, a component for hierarchical continuous LOD

![](../../assets/5a63dd06b4c870c7.png)


- video showing how to add rain effects (puddles, raindrops, ripples) to a Unity terrain shader
- adapts the built-in rain floor subgraph for the needs of the trrain
- improves puddle by modulating the puddle mask with terrain height data

![](../../assets/e6b9210c2c05d7be.png)


- Digital Foundry’s first hands-on look at DLSS 5
- demos across Resident Evil Re:Verse, Starfield, Oblivion Remastered, and Assassin’s Creed Shadows
- currently runs on dual RTX 5090 GPUs in demo form; goal is reduce hardware requirements

![](../../assets/506e1774c879a2bc.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.