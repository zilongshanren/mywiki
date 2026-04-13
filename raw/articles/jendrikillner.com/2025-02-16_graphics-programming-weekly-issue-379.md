---
title: Graphics Programming Weekly - Issue 379
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-379/
author: Jendrik Illner
published: '2025-02-16'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- The article provides a step-by-step tutorial that presents how to create the head of Rick using a pixel shader.
- Introduces the necessary SDF operations slowly and shows how to combine them with animation.
- Each step is presented as interactive shader challenges that can be edited to learn along the way.

![](../../assets/a8a19a499be2a71d.png)


- The video tutorial presents how to combine specular, diffuse, and ambient lighting to create a custom shading model.
- Presents the various stages, how to ensure correct vector spaces, and the effect of various parameters.
- The implementation is shown using Unity and Unreal visual shader graphs.

![](../../assets/181dfe5fac1b6584.png)


- The paper presents an analytic approximation for the CIE 1931 color space and the more modern CIE 170-1:2006.
- Shows the approximation process and how it compares against existing approximations.
- Source code is available in C++ and Python.

![](../../assets/0dfc058733d2a059.png)


- The article provides a deep dive into getting Surface-Stable Fractal Dither running on a simple 1-bit display console.
- Presents a breakdown of how the dithering algorithm is created from various passes.
- Discusses various software rasterization methods and how they compare to the GPU reference implementation.
- Additionally, it presents several applied optimization steps and how they affect performance.

![](../../assets/609025b0a80cf01b.png)


- The article discusses a small trick used by Anno 1800 that always aligns the sun’s direction relative to the camera.
- Presents how much it affects the scene’s beauty as it prevents worst-case lighting setups.

![](../../assets/0a5538a4fd515729.png)


- The presentation covers a complete walkthrough on using WebGPU from JavaScript.
- Starts by explaining the basics and proceeds from a high-level overview into the implementation details.
- Covers the full rendering pipeline, including shader authoring.

![](../../assets/4d7a5349d64266ee.png)


- The talk introduces a novel sphere tracing algorithm tailored for harmonic functions.
- The method allows for larger step sizes than traditional ray marching.
- Demonstrates applications in visualizing surfaces reconstructed from point clouds and polygon soups without requiring linear solves or mesh extraction.
- Expands visualization capabilities to handle nonplanar polygons with holes and complex mathematical objects such as knots and links.

![](../../assets/b0b288a5e6c8e6cf.png)


- The blog post describes how LunarG optimized the startup time of GPU Assisted Validation.
- Combines driver hints and more fine-grained validation code and moves logic to later stages in the application lifecycle.

![](../../assets/311edeb958afaa1c.jpg)


- The article provides a detailed walkthrough of optimizing a 4096x4096 matrix multiplication for RDNA3.
- Shows how to calculate theoretical expectations for performance and compares against all tested implementations.
- Presents how a highly optimized routine can be 50x faster than a naive implementation.
- Always present hardware performance captures and explain how to understand them and optimize the bottlenecks observed.

![](../../assets/a4f773f6b3f63542.jpg)


- The blog post introduces the Vulkan Safety Critical Emulation stack.
- Shows how the stack interacts between the user code and driver code.
- Is meant to guide developers in developing applications by emulating SC constraints on consumer hardware.
- The source code for the stack is open source.

![](../../assets/51bdd8bc8bf89847.png)

Thanks to [Cort Stratton](https://mastodon.gamedev.place/@cort) for supporting this series

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series