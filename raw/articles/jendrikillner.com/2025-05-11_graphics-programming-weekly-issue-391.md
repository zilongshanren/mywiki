---
title: Graphics Programming Weekly - Issue 391
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-391/
author: Jendrik Illner
published: '2025-05-11'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- JCGT paper presenting a technique for generating optimized samples with good spectral properties
- presents the improved results for depth of field with complex bokeh shapes
- shows how to calculate the samples and the effect on quality and performance

![](../../assets/714d292a6f4931cc.png)


- Clear explanation of reservoir sampling for selecting k random samples from data streams of unknown size
- Uses interactive visualizations to demonstrate the algorithms and its behaviour
- Additionally presents how the technique can be applied to a log processing service

![](../../assets/8461b00fbb7d9050.png)


- Comprehensive exploration of how GPUs select appropriate mipmap levels when sampling textures
- Discusses linear filtering, anisotropic filtering, trilinear filtering, and mathematical foundations with visual comparisons
- Many visual examples to visualize the equations discussed

![](../../assets/dc716d031d401efb.png)


- open access book focusing on the foundations and applications of procedural noise for texture generation
- Focuses on theory and implementation of algorithms that enable procedural texturing workflows
- Demonstrates how basic primitives can be combined to create natural-looking textures for various applications

![](../../assets/2a4fc04d83ca5f06.png)


- The paper introduces a two-Level monte carlo estimator for global illumination(GI)
- Discusses the Neural Incident Radiance Cache (NIRC) that uses a small neural network that is trained on-the-fly to learn incoming light from all directions

![](../../assets/c9b9f398860b6735.png)


- Technical deep-dive explaining the mathematical foundations of ReSTIR GI for efficient real-time path tracing
- Includes code snippets, visualizations, and mathematical derivations making the concepts more approachable
- additionally clarifies the limitations of the technique

![](../../assets/67b93c0f298ac6e0.png)


- The paper combines ReSTIR (Reservoir-based Spatio-Temporal Importance Resampling) with shadow mapping for complex lighting
- the selection strategy generates shadow maps for lights with the strongest contributions to pixels in the current camera view
- and falls back to imperfect shadow maps to provide low-resolution shadow approximations

![](../../assets/23f39d64326ae784.jpg)


- The article explores neural representations for 3D geometry
- Discusses the Neural Intersection Function that allows BVH traversal to operate as part of the raytracing pipeline
- Discusses the limitations and how Locally-Subdivided Neural Intersection Function can overcome these

![](../../assets/6a35619f64b5d0b5.png)


- The paper presents a technique for creating UV mappings directly on implicit surfaces without traditional mesh parameterization
- Uses local-uv fields that are smoothly blended to enable continuous parameterizations

![](../../assets/1d69b9bb53efa5ea.png)


- exploration of mesh shader implementation and performance benefits in modern graphics pipelines
- Provides benchmarks with different meshlet/thread group configurations and code examples for amplification and mesh shaders
- uses nvidia hardware counters to present the results of the various experiments

![](../../assets/6833318056dad8b4.png)


- The blog post discusses GPU radix sort techniques
- Starting with a classical radix sort implementation and an overview of the improved onesweep implementation
- Explains how this technique can be extended to work within a fixed memory footprint through the use of a ring buffer for look-back storage

![](../../assets/8f91c65f5ba46b8b.png)


- Blog post describes the journey implementing AMD’s FidelityFX Super Resolution 4 (FSR4) on Linux
- Presents how DXIL expresses instruction extensions
- Discusses steps required to support 8-bit float and wave matrix multiply accumulate(WMMA) required for the compute shaders

![](../../assets/e6b5c942a4932137.jpg)


- GitHub repository with minimal implementation examples for hardware-accelerated video decoding with Vulkan and DX12 for H264 videos
- Shows how to decode video streams directly on the GPU
- Demonstrates interfacing with platform-specific video APIs and synchronizing between decoder and graphics pipeline
- source code contains many comments to explain the pitfalls and undocumented behaviours

![](../../assets/0c35974698a553d8.png)


- GDC presentation from Ubisoft’s rendering team on advanced graphics techniques in Assassin’s Creed Shadows
- Discusses the GPU accessible scene representation (database), GPU driven rendering pipeline and new micropolygon rasterization
- Overview of the GI implementation, raytracing abstraction and deep-dive into the implementation
- Lastly discusses the deferred weather system

![](../../assets/75db364aa4f8e5e2.png)

Thanks to [Graham Wihlidal](https://www.wihlidal.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.