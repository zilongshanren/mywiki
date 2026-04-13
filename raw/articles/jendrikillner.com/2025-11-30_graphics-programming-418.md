---
title: Graphics Programming 418
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-418/
author: Jendrik Illner
published: '2025-11-30'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- announces the multi-vendor Vulkan extension VK_EXT_ray_tracing_invocation_reorder for Shader Execution Reordering (SER) to reduce divergence in ray tracing workloads
- explains how SER uses hit objects to separate ray traversal from shader invocation and allows the GPU to reorder invocations for improved coherence
- provides best practices, GLSL/Slang code examples, and how to profile with NVIDIA and AMD tools

![](../../assets/ff20650a57dfa79d.png)


- benchmarks Shader Execution Reordering (SER) using the Evolve pipeline path tracing benchmark across NVIDIA, AMD, and Intel GPUs
- tests reordering strategies based on material index and material properties mask to improve wave coherence
- shows significant performance improvements on NVIDIA hardware, while AMD and Intel showed minimal or no improvement

![](../../assets/dc391fb12940aae5.png)


- implements a spatial hash structure to cache and accelerate ray-traced ambient occlusion for static scenes
- presents hash functions using PCG and xxhash32 with position and normal quantization to create cells that accumulate AO samples
- discusses distance-based cell sizing, conflict resolution via linear probing, and temporal management to handle hashmap capacity limits

![](../../assets/20b4302c5ac83f80.png)


- announces AMD GI-1.2 as part of the Capsaicin Framework v1.3
- extends the ray path by adding 2nd bounce hash grid cells to capture light from further bounces
- presents the algorithm steps for radiance accumulation and filtering

![](../../assets/8b00856c6d339ec2.png)


- video presentation covering the fundamentals of ray tracing
- covers the overview of the Vulkan API
- presents and explains ambient occlusion as a practical use case

![](../../assets/34643c9c18f61261.png)

- compares RGB rendering against spectral rendering using various illuminant types from white light to monochromatic spectra
- demonstrates how spectral rendering accurately handles color shifts under different light sources
- discusses the advantages of spectral rendering for production workflows

![](../../assets/e672b537155f7b42.png)


- describes a lighting workflow for the Quest 2 that uses Lumen for fast iteration and GPU Lightmass for final bakes
- presents techniques to fake light shafts without volumetric fog using Geometry Script-generated meshes and bloom effects without Mobile HDR
- covers solutions to enable dynamic shadows on PC while keeping static lighting on mobile hardware

![](../../assets/b3ceb3bfcd5d0eb3.png)


- demonstrates using Android’s RuntimeShader API to simulate soft shadows projected by the user’s finger onto the UI
- models the finger as a 3D capsule and computes soft shadow visibility by calculating the spherical caps’ intersection
- provides the complete AGSL shader implementation, including optimized trigonometric functions

![](../../assets/0d5fe275c2909662.png)


- provides a collection of 2D axis-aligned bounding box (AABB) functions for SDF primitives to enable culling and pruning
- covers triangles, oriented boxes, segments, pies, quadratic and cubic Bezier curves, parabolas, cut disks, eggs, stars, and vesica segments
- includes Shadertoy demos for each primitive

![](../../assets/e57f05e7f4825ba3.png)


- first video in a series introducing geometric algebra as a framework for manipulating geometric objects through algebraic calculations
- provides an overview of applications, advantages over traditional linear algebra approaches, and common educational pitfalls
- covers the distinction between parallel and orthogonal components and sets up the foundation for deeper exploration

![](../../assets/4d5c8846eb2cfa6a.png)


- explains the new VK_EXT_custom_resolve Vulkan extension that allows custom shaders for resolving multisample images
- describes how the extension enables combining resolve operations with post-processing like tone-mapping in a single shader
- covers the dynamic rendering support via vkCmdBeginCustomResolveEXT

![](../../assets/727f11a522399078.jpg)


- provides a comprehensive guide to all D3D12 documentation sources
- covers the primary Microsoft documentation, Functional Specification, DirectX-Specs, etc

![](../../assets/5602017e15d8d052.png)


- official trailer showcasing the technical papers presented at SIGGRAPH Asia 2025
- previews the latest research in computer graphics and interactive techniques
- presents a short overview of the various papers presented

![](../../assets/458ec2cc630286b3.png)

- conference program has been released
- Combined passes for the Shading Languages Symposium + Vulkanised are available
- Early bird ticket sales are still available

![](../../assets/97978ce65cf6b79e.jpg)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.