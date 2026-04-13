---
title: Graphics Programming weekly - Issue 130 — May 3, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-130/
author: Jendrik Illner
published: '2020-05-03'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the presentation provides an in-depth overview of shadow techniques for real-time applications
- discusses what shadow maps are, how they are rendered, stored and used
- provides an overview of common problems and solutions
- additionally provides an overview of more advanced techniques such as filtering and cascaded shadow maps

![](../../assets/c047bbb85c2c7195.png)


- the article presents the definition of a physically-based material that is energy conservation and reciprocity
- reciprocity is essential to be able to use bi-directional path tracing techniques
- looks at common methods such as Pre-Filtered Environment Maps, several Dielectric Material implementations presenting if they are reciprocal and/or energy-conserving and explaining why

![](../../assets/fa82a94c06e8b156.jpg)


- the article presents how to implement a prefix sum using Vulkan compute shaders
- looking at memory model, dynamic allocations and subgroup controls

![](../../assets/e0f96d4c42966d2e.png)

- the Unity tutorial explains how to use the depth texture to apply a localized toon shading effect
- shows how to sample the depth texture, unpack the data and use it in a shader

![](../../assets/4f651a75316c0302.png)

- new Nvidia extension for D3D12 that provides shaders the possibility to query timestamps from within a shader
- the article explains how to use this technique to visualize the performance of TraceRay( … ) with a heatmap
- shows how to enable the extension in C++ and how to integrate it into a shader
- comparable to the
[VK_KHR_shader_clock](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VK_KHR_shader_clock.html)extension

![](../../assets/26cba10ad68151aa.png)


- next part in the Unity Tutorial series about implementing a custom scriptable rendering pipeline
- adds support for more complex materials such as details maps and normal mapping

![](../../assets/79dece19b1d9a58a.jpg)


- the video provides an overview of Variable Rate Shading (VRS)
- present an overview of VRS implementation in Wolfenstein New Blood and Gears: Tactics for performance and quality
- discusses considerations in how difference workload affect the performance gains that can be expected from VRS

![](../../assets/e72698b70bfdb341.png)


- the article presents an alternative execution model that would be able to improve upon Timeout Detection and Recovery mechanism found in the OS
- after 2 seconds the OS will terminate GPU processes and cause a device lost event
- the proposal is to make the OS GPU process-aware which allows applications to start independent GPU processes that would behave similarly to CPU processes

![](../../assets/9e56e09228092f23.png)


- the article provides an overview of the WebGPU API
- covers the state of the implementation on Firefox and presents the next steps currently in progress

![](../../assets/8d7147f7aacfd5be.png)


- the article presents the Wrapped lighting technique to emulate subsurface scattering
- the method is aimed for use with forward shading on the Oculus Quest

![](../../assets/e0b5e21be2a48caf.png)


- this part of the article on volumetric rendering shows how to model a volume using an SDF inside of shadertoy

![](../../assets/dbb23da6d4c08a75.jpg)

- the second part of the article presents how to render the volumetrics
- calculation absorption, Self-shadowing, quality improvements, and a few optimizations

![](../../assets/787df118563ab767.jpg)


- Twitter thread about the complexities of different light measuring units
- provides a UE4 tool to simply conversion between units

![](../../assets/940469bb96707e8e.png)

Thanks to [Daniel Fortes](https://www.danielfortes.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.