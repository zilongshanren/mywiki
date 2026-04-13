---
title: Graphics Programming Weekly - Issue 395
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-395/
author: Jendrik Illner
published: '2025-06-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- announces the latest SIGGRAPH course on physically based shading, featuring new research and practical advice from film and game production
- covers topics such as energy-conserving models, spectral rendering, neural materials, and production hair shading
- includes the course timetable and presenter list

![](../../assets/f05292ee8d79fc2b.png)


- introduces the VK_KHR_video_decode_vp9 extension for Vulkan, enabling hardware-accelerated VP9 video decoding
- explains why VP9 is one of the simpler codecs to implement and recommends it for getting started
- supported by major GPU vendors and open-source drivers, with SDK and sample updates coming soon

![](../../assets/845427f277aa28c8.jpg)


- presents a Vulkan extension that simplifies image layout management by allowing VK_IMAGE_LAYOUT_GENERAL to be used in most cases
- reduces the need for explicit image layout transitions to simplify synchronization
- discusses how some hardware doesn’t distinguish between image layouts, so not using the specific layouts doesn’t cause performance issues

![](../../assets/5848c374ef6f53af.png)


- presents formulas for efficiently computing partial derivatives of any order for spherical harmonics
- shows that intermediate results from the standard evaluation can be reused, reducing the computation cost significantly
- includes links to a poster, supplemental document, and code for practical use

![](../../assets/ee444cc4877bf9f4.png)


- explores the optimization of Voronoi noise in Blender by switching from an older Jenkins hash to a faster PCG3D hash
- highlights challenges with Open Shading Language (OSL) lacking unsigned integers and bit casts and how these were worked around
- concludes with lessons learned about hash functions, code maintenance, and shading language limitations

![](../../assets/aa7f751af1a5a7f2.png)


- analyzes Mario Kart World’s HDR implementation on Switch 2, revealing it uses static tone mapping and SDR color gamut
- details the pitfalls of SDR-first pipelines and how they limit dynamic range and color volume
- offers recommendations for developers to adopt HDR-first workflows and dynamic tone mapping for better results

![](../../assets/a83e07340bdb56b6.jpg)


- provides a comprehensive walkthrough of implementing volumetric lighting using raymarching and post-processing
- covers coordinate system transformations, depth-based stopping, shadow mapping, and shaping light with SDFs
- explores light scattering and multi-light setups with interactive demos and code examples
- discusses practical applications and artistic effects achievable with these techniques in 3D scenes

![](../../assets/3fb73934bdc12010.jpg)


- presents an approach to real-time text rendering on the GPU, focusing on quality and subpixel anti-aliasing
- discusses a system that rasterizes glyph curves directly to an atlas with temporal accumulation
- provides code samples, visual comparisons, and practical advice for high-quality, efficient text rendering

![](../../assets/ce557821c88fb4a4.png)


- the videos break down what aliasing is and why it happens when sampling signals
- presents how this can lead to distorted or misleading results
- shows a walkthrough with intuitive visualizations and concrete examples to show how high-frequency signals can appear misleading if sampled at a too-low frequency

![](../../assets/b0202c981fd789f2.png)


- the video presents an overview of the WebGPU API
- discussing the capabilities of the API, supported platforms, and limitations
- additionally provides guidelines to follow for best performance

![](../../assets/c493682f4ba92a13.png)


- the video presents an overview of GPU architecture
- explaining overhead in GPU processing
- how indirect drawing allows more flexibility and enables more workloads to be executed efficiently
- additionally discusses vertex optimizations for efficient rasterization

![](../../assets/1cd90a07294763d0.png)

Thanks to [Mike Turitzin](https://miketuritzin.com/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.