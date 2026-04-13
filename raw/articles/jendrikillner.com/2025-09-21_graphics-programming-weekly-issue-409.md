---
title: Graphics Programming Weekly - Issue 409
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-409/
author: Jendrik Illner
published: '2025-09-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- comprehensive technical breakdown of Solari, a real-time raytracing system integrated into Bevy 0.17
- discusses the motivation and development history
- implements ReSTIR Direct and global illumination with a world-space irradiance cache
- uses DLSS Ray Reconstruction for denoising and upscaling
- presents a look at the performance of the various implementation steps

![](../../assets/b3b2a3ac1f4ce2fd.png)


- explains how triple buffering improves frame pacing and throughput by preventing GPU stalls when VSync is enabled
- provides practical implementation examples for Vulkan, DirectX 12, and OpenGL
- briefly mentions the disadvantages of the techniques and common pitfalls

![](../../assets/5b7107cffbefd956.png)


- blog post introduces a library for implementing cubic Bézier curve representation in just 28 bytes
- provides comparisons in time and quality against other implementations

![](../../assets/a9373f8813f40849.png)


At Astrobotic, we’re building the future of space robotics, from lunar landers to autonomous systems- and simulation is central to that mission. We’re seeking engineers with strong skills in C++, graphics, and simulation to develop high-fidelity environments that enable spacecraft testing and mission operations.

![](../../assets/571b3f59475ae6b0.png)


- presents techniques for reducing BLAS builds for cluster-based continuous level of detail systems
- discusses BLAS Sharing, Caching, and Merging
- releases the implementation of the techniques with a detailed discussion of the implementation choices
- additionally presents performance and memory profiling results

![](../../assets/22a64098c6ac459f.png)


- video exploring the foundational principles and methodologies behind Euclidean geometry
- examines how Euclid’s systematic approach to mathematical proofs laid the groundwork for modern mathematical reasoning

![](../../assets/a5cf219c6fb010ab.png)


- introductory video covering fundamental color theory concepts for beginners
- explains color relationships, harmony principles, and practical applications in design and digital art
- provides accessible guidance on using the color wheel and understanding color interactions for improved visual compositions

![](../../assets/be974946155aca42.png)


- detailed analysis of how increasing vertex shader exports affects rendering performance on NVIDIA GPUs and AMD integrated GPUs
- demonstrates that drawcall costs can significantly increase when exporting more data to the vertex shader stage
- uses Nsight Graphics profiling to show how bottlenecks and memory allocation patterns impact vertex-to-pixel data flow

![](../../assets/601370886fa97e4f.png)


- introduces robust-kbench, a comprehensive benchmark for evaluating CUDA kernel performance and correctness across varied scenarios
- presents an agentic framework that uses large language models to discover, verify, and optimize CUDA kernels automatically

![](../../assets/95c62cd3e3924339.png)

Thanks to Stephen Hill for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.