---
title: Graphics Programming 413
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-413/
author: Jendrik Illner
published: '2025-10-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- hands-on tutorial series for implementing ray tracing with Vulkan
- implements ray-query-based shadow rays with alpha-test transparency support
- includes debugging tips using RenderDoc and Nsight Graphics

![](../../assets/e6c4be3859845b40.png)


- comprehensive guide covering physically based approaches for geometry, materials, lighting, and cameras
- discusses the various material properties with real-world examples
- covers physically based lighting units, including candela, lumen, nit, and lux, with practical measurement techniques
- emphasizes the importance of physically based content for reusable assets and consistent results across lighting conditions

![](../../assets/2430a59028249319.png)


- comprehensive guide to Three.js using WebGPU
- presents three.js Shading Language (TSL) as well as WGsl for web graphics development
- provides practical examples, including displacement, glass materials, particles, and post-processing effects

![](../../assets/838b7292ad4ea7dc.png)


- video tutorial covering texture sampling in Unity shader code
- explains the concept of UV coordinates, texture samplers
- shows how to implement texture mapping into a simple shader

![](../../assets/6f1b5ee98078890f.png)


- presents a per-instance encoding technique for GPU-driven rendering with varying instance data requirements
- instances use type discriminants to allow different memory layouts within a unified buffer
- reduces memory bandwidth and footprint by eliminating unused fields
- allows different instance types to coexist efficiently in the same buffer

![](../../assets/a394eb31c6ca66ec.png)


- video exploring GPU-side input handling (late latching)
- discusses how to efficiently manage input data directly on the GPU with cache-line-sized packets
- covers practical implementation and how to avoid mid-frame cache flushes from the CPU

![](../../assets/0edf1fafca715b04.png)


- video demonstrating a write-once read-many model (WORM) for authoring compute workloads
- presents how Vulkan compute code can be written to take advantage of the cache structure to ensure no cache flushes are required
- discusses considerations when designing the data model to match hardware caches

![](../../assets/32f84d1449253b9c.png)


- explains the sharp bilinear filtering technique for scaling pixel art without blur
- solves common artifacts from nearest-neighbor and standard bilinear filtering
- Derives the mathematical formulas behind the shader implementation step by step

![](../../assets/5d42724db1c5c898.png)


- tutorial covering Euler angles and axis-angle rotation methods for 3D graphics
- explains how to stack 2D rotations for yaw, pitch, and roll transformations
- presents axis-angle rotation formula using mix, cross product, and trigonometric functions

![](../../assets/3f1c25a37be3a813.png)


- details the mathematical approach to computing distance from a point to cubic Bézier curves
- presents and compares recent algorithm improvements
- providing GLSL implementations of the presented techniques

![](../../assets/599c8cc337a82f49.png)

Thanks to Peter Kohaut for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.