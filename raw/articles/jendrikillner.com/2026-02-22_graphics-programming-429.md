---
title: Graphics Programming 429
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-429/
author: Jendrik Illner
published: '2026-02-22'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- comprehensive guide to implementing a render graph system using Vulkan
- explains the complete pipeline, including pass dependency recording, resource lifetime computation, graph construction using topological sorting, and automatic pass culling
- covers advanced features like texture aliasing within frames, multi-threaded command buffer recording, and automatic barrier generation between passes

![](../../assets/f99a50a7a782fab6.png)


- Vulkanised 2026 talk video and slices have been released
- presentations covering topics from machine learning, performance, system integration, and more
- additionally contains talks about developers using the API for various requirements across various platforms

![](../../assets/7e8a16671bb83ebd.jpg)


- an accessible overview aimed at hobbyists: history and practical advice for getting started with Vulkan
- highlights helper libraries and learning resources recommended for newcomers

![](../../assets/c86cbcac34766890.png)

- discusses implementing runtime mipmap generation on the GPU
- presents techniques for correct linear-space filtering using sRGB texture views and high-quality low-pass filters
- explains alpha-weighted filtering to prevent color bleeding, as well as coverage preservation techniques to maintain alpha-tested geometry visibility

![](../../assets/98e9d6eb7f224934.png)


- explores optimization techniques for GGX prefiltering in image-based lighting, targeting low-end hardware
- details how using group shared memory to compute Hammersley sequences and GGX samples to reduce per-thread work
- achieves significant performance improvements through partial loop unrolling, tangent-space math, and precomputing LODs

![](../../assets/53b512aab1cc9f6b.png)


Marmoset is looking for skilled programmers to join our team building Toolbag, our industry-leading real-time rendering and authoring application.

You’ll work with artists and developers to design, implement, and optimize rendering, baking, and texture authoring features in Toolbag. This role is ideal for someone who loves visual computing and creating powerful tools for artists. If you’re passionate about real-time graphics and love building the tools that artists rely on, we’d love to hear from you.

![](../../assets/1fa0cc86fa39e72b.png)


- GLSL shader editor designed for efficient shader development (similar to Shader Toy)
- features a built-in inspector to visualize variables and functions directly in the viewport
- includes a snippet library for common operations, custom uniform support, and a tuner for adjusting numerical values with sliders

![](../../assets/10427136e3b6cbb7.png)

- introduces HIP Threads, a C++ concurrency library that enables AMD GPU acceleration using familiar CPU threading patterns
- presents how to transition a simple example to execute on the GPU

![](../../assets/cc474453bef5daac.jpg)


- explores using DirectX Cooperative Vectors to access Tensor cores for neural network inference
- explains how matrix-multiply-accumulate operations on Tensor cores provide significant speedups for MLP evaluation compared to compute shaders
- demonstrates massive speedup, especially on large networks

![](../../assets/6ea6d79af0a85c66.png)


- presents Neural Irradiance Volume (NIV), a neural-based technique for real-time rendering of diffuse global illumination
- uses neural compression to create an adaptive representation of irradiance

![](../../assets/10b17ae1d9b2c289.png)


- presents Faster-GS, an optimized 3D Gaussian Splatting framework that consolidates strategies from prior research
- investigates underexplored aspects, including numerical stability, Gaussian truncation, and gradient approximation

![](../../assets/0040e7d5e53273a9.png)


- demonstrates “texel splatting”: rendering 3D-looking pixel art by projecting and blending texels in 3D space
- shows the visual effect of the various stages of the implementation, showing issues encountered along the way

![](../../assets/d59dd9fa0fb94a33.png)

- Introduction to SPIR-V that explains its role as a portable shader/intermediate representation for Vulkan and other APIs
- provides an explanation of the SPIR-V concepts and helps to understand them
- shows practical examples via reading and explaining the disassembly

![](../../assets/f3f699462565b1e1.png)

Thanks to [Jasper Bekkers](https://x.com/JasperBekkers) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.