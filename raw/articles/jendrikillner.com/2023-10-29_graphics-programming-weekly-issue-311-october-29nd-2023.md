---
title: Graphics Programming weekly - Issue 311 - October 29nd, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-311/
author: Jendrik Illner
published: '2023-10-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- part 2 of the animated flag series extends the effect from the previous video
- adds support for allowing the flag to be rotated
- additionally shows how to recalculate the normals for improved lighting

![](../../assets/67c1ef82c13be919.png)


- the talk presents an overview of linear algebra
- covering topics from the basics of vectors, complex numbers, operations between vectors, and more
- shows how intuition developed connects to geometric algebra

![](../../assets/b82f362edf38c4d0.png)


- the blog post introduces a new series about machine learning that aims to connect different disciplines
- provides an introduction to machine learning and shows how it can be expressed in shader code

![](../../assets/3c582496cac11ffd.png)


- the blog post describes the The Marschner Hair Shading Model
- focuses on high-level information and develops an intuition for the model
- additionally provides corrections and extensions for ideas from the original paper

![](../../assets/f90b7cf5af1986d6.png)


- the article presents the importance of tone mapping to reduce color clamping
- shows visual examples of different tone mapping implementations

![](../../assets/ef1c56a784dcce33.jpg)


- the article presents the types of checks available by the NVIDIA Compute Sanitizer
- shows how to use sanitizers to detect memory access errors, uninitialized device global memory access, thread synchronization hazard detection, and more
- each example is provided with source code to the issue and how the sanitizer helps to detect it

![](../../assets/b964a4d74fef1059.png)


- the article presents a collection of recommendations for descriptor usage on Nividia using D3D12 and Vulkan
- discusses what are best practices, what should be avoided, as well as pitfalls to avoid

![](../../assets/9cee8a92a70aca0a.jpg)


- the video presents how shaders are translated between HLSL and the target shading languages
- explains the limitations of existing solutions and why a custom solution was developed
- shows how DXC is used as a frontend and the steps necessary to convert to GLSL

![](../../assets/7ef3a9d68d5889ae.png)


- the video presents an overview of the RE ENGINE graphics stack
- shows how shaders/material are authored, how raytracing has been deeply integrated and optimized
- additionally presents how bindless allowed reduced CPU overhead and shows limitations, risks, and GPU performance impact of the approach
- briefly covers mesh shaders and visibility buffers

![](../../assets/93a29fd58f4422ba.png)

Thanks to [Warren Moore](https://metalbyexample.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.