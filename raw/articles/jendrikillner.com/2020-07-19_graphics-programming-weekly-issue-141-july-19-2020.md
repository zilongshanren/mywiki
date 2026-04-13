---
title: Graphics Programming weekly - Issue 141 — July 19, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-141/
author: Jendrik Illner
published: '2020-07-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article shows how to improve performance of fullscreen compute shader passes by tiling thread workloads to take advantage of memory locality
- test cases show an example improvement of 1.47x on memory bound workloads

![](../../assets/9021f231d2831179.png)


- a twitter thread that visually explains what the Fresnel effect is and how it affects the appearance of different objects

![](../../assets/ffe5ed88d55a6796.png)

- the blog post presents how the shadow move technique was implemented in Killer Instinct: Season 3
- the effect uses information from the previous frame in offscreen render targets combined with movement noise, flow maps, and trail renders attached to bones

![](../../assets/ab046299ee0f2a35.png)


- the blog post provides an overview of mipmapping, Colour Bleeding, and pre-multiplied alpha

![](../../assets/7895de363e768261.png)


- the short blogpost shows an artists material setup that uses a small 16x16 LUT as indirection table into PBR materials

![](../../assets/ec6fad803ab3008b.png)

- the article discusses what memory aliasing exposed from Vulkan and D3D12 is and how it can be used to reduce memory usage
- provides an example implementation of an algorithm that implements a resource aliasing allocator

![](../../assets/a96440660983aaa4.png)

- Towards Fully Ray-Traced Games: Addressing System-Level Challenges (Holger Gruen, Intel)
- Generalized Light Portals
- Efficient Adaptive Deferred Shading with Hardware Scatter Tiles
- Post-Render Warp with Late Input Sampling Improves Aiming Under High Latency Conditions

![](../../assets/18b7d7bd8ec196ec.png)

- Neural Denoising for Path Tracing of Medical Volumetric Data
- High-Performance Image Filters via Sparse Approximations
- FLIP: A Difference Evaluator for Alternating Images
- Evaluation of Graphics-based General Purpose Computation Solutions for Safety Critical Systems: An Avionics Case Study
- Euclid NIR GPU: Embedded GPU-accelerated Near-Infrared Image Processing for On-board Space Systems.
- Fast Eye-Adaptation for High Performance Mobile Applications. (Morteza Mostajab, Theodor Mader)

![](../../assets/99ebf0912cca1401.png)


- Porting PBRT to the GPU While Preserving its Soul
- Quadratic Approximation of Cubic Curves
- Using Hardware Ray Transforms to Accelerate Ray/Primitive Intersections for Long, Thin Primitive Types
- Sub-Triangle Opacity Masks for Faster Ray Tracing of Transparent Objects
- Improved Triangle Encoding for Cached Adaptive Tessellation
- Iterative GPU Occlusion Culling with BVH
- Ray-casting inspired visualisation pipeline for multi-scale heterogeneous objects

![](../../assets/f7a6484b8d388339.png)


- the paper presents a technique that uses late input latching and wrapping wrap render results to match camera rotations based on ideas from VR

![](../../assets/75a861b57b87c295.png)


- the article provides an overview of the performance that can be expected from several Unity Engine shaders
- the provided information is from the Mali OpenGL ES shader compiler

![](../../assets/0aafacae9df9fe9d.png)


- the article presents many techniques for rendering broad outlines for 3D objects
- provides performance and quality comparisons of the different techniques
- the final result is a flood fill based approach

![](../../assets/df977c58b51fb2ca.png)


- this Unity tutorial explains how to implement a rain effect on the surface of objects using a technique that is used on a tri-planar mapping
- droplets on flat surfaces and streaks when angled
- this is implemented using the Amplify Shader Editor

![](../../assets/87543c95b140c74b.png)

Thanks to [Trevor Black](https://trevord.black) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.