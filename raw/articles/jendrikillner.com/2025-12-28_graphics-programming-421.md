---
title: Graphics Programming 421
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-421/
author: Jendrik Illner
published: '2025-12-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- very detailed blog post that discusses the reality of modern GPU hardware
- presenting the disconnect between API models and hardware
- proposes a minimalistic modern graphics API design that reduces complexity while maintaining performance
- blog post contains an example of what such an API might look like

![](../../assets/35cff7c04d828020.png)


- announces the release of the OpenUSD Core Specification 1.0 defining formal semantics for scene descriptions
- specifies six essential pillars including grammar, composition algorithm, and compliance framework
- provides sample implementations and conformance testing tools for validating implementations

![](../../assets/667f4823e0a2f7b3.png)


- investigates behavior of ClearUnorderedAccessViewUint and ClearUnorderedAccessViewFloat functions
- reveals inconsistent type conversions across NVIDIA, AMD, and Intel GPUs for various buffer formats
- demonstrates that unsigned integer clears work differently than documented in DirectX 11

![](../../assets/85ce3240c3398f64.jpg)


- continues the series with practical solutions and sample patterns for real-time renderers
- shows shader-level techniques (sample distributions, MSAA-aware approaches) and links to Shadertoy experiments for direct testing
- covers trade-offs between artifact reduction and performance, with suggestions that are implementable in real-time

![](../../assets/d9719f3fac05ce0b.png)


- introduces an MLIR-based intermediate representation for CUDA kernel targeting tensor cores
- provides domain-specific operations for tile-based computations with Python bindings
- includes bytecode serialization format

![](../../assets/8a84eca5723608f6.jpg)


- presents a novel representation combining surfels with neural texturing for view synthesis
- achieves quality matching 3D Gaussian splatting using 9.7x fewer primitives on outdoor scenes
- aims to improve render times compared to existing methods by selectively texturing high-weight samples

![](../../assets/9d86b2e909f5c9ab.png)


- walkthrough of parallax occlusion mapping (POM) techniques for Unity
- integrating Nanite displacement for terrain rendering and how Nanite displacement changes displacement workflows
- discusses performance implications and offers tips for balancing quality vs cost in terrain shaders

![](../../assets/5988e3663e3cc09e.png)


- short talk focused on micro-optimizations to the filter kernel and their real-world impact
- examines kernel tweaks that reduce aliasing artifacts while keeping shader cost low

![](../../assets/2732359e77cb3019.png)

- sets up an initial physics framework and demonstrates simple particle dynamics
- walks through application/physics system classes and a short demo showcasing the physics update
- rendering is implmeneted using OpenGL

![](../../assets/9c3eaddcef2c5179.png)


- live stream focused on making scene loading faster by caching optimized geometry on disk and adding compression
- walks through implementing a basic scene cache, switching to memory-mapped loading, adding compression, and profiling cold/hot runs and page-fault behaviour
- practical andf focused session with profiling runs, implementation details and trade-offs for robust cache/IO design

![](../../assets/d4566912859d08fc.png)


- presents the results of replacing the screenspace raymarcher implementation with a hardware-accelerated raytracer enabling offscreen lights and more stable GI
- achieves real-time per-frame GI (no denoiser) on a 4090

![](../../assets/21780375168f9324.png)

Thanks to [Aras Pranckevicius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.