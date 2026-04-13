---
title: Graphics Programming weekly - Issue 356 - September 8th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-356/
author: Jendrik Illner
published: '2024-09-08'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog post continues the discussion of the Radiance Cascades GI technique
- presents how to use information from a low number of rays to reduce the number of artifacts as much as possible
- shows the effect of the different steps and how multiple cascades are combined
- source code and interactive experiments are available

![](../../assets/13ef4d0afae64f43.png)


- the blog post presents the effects of combining multiple levels of noise
- shows this for blue noise, white noise, box noise, and many more
- additionally, it presents how the demo was made using the open-source Gigi prototyping platform

![](../../assets/267775633bbea819.png)


- the blog post presents what is required to write deterministic algorithms
- discusses algorithmic, multithreaded, and cross-platform considerations
- shows how different compiler options and standard library implementation can affect the results

![](../../assets/84ce9574f18e7f6d.png)


- the video provides a summary of how normal maps can be used to augment surface detail
- presents the derivation of the math that, such as tangent spaces, enables the augmentation
- additionally presents a method that can be used to approximately detect if a texture contains normal map information

![](../../assets/b41346cab168584e.png)


- the video presents how to combine polar coordinates, tiling, and blending to create a procedural loading indicator
- the implementation is shown using Unity and Unreal Visual shading languages

![](../../assets/8ee57616046bf6d0.png)


- the blog post provides a collection of Khronos talks that happened during SIGGRAPH 2024
- provides a link to the slides as well as the videos

![](../../assets/419f8093e1fbc5b4.png)


- the blog post discusses the EDIZ (Error Diffusion Image Zooming) algorithm for image upscaling
- presents a high-level overview of the technique
- discuss weaknesses and shortcomings
- additionally, it presents an implementation of the technique in a code sample

![](../../assets/4713714aec75023d.png)


- the article presents the authors’ findings when exploring Visibility buffers and methods to access UV derivatives
- presents the different methods, additional texture channels, ray-tracing into cached vertex transforms, and usage of LDS for short-term caching
- presents code implementations of the techniques and presents quality comparison videos

![](../../assets/5b997b880f8cf9be.png)


- the author presents his idea for a screen-space shadow technique that relies on Hierarchical Depth Buffers for each shadow-casting light
- starts with a brief overview of virtual shadow maps and the difficulties of debugging them that lead to the idea

![](../../assets/ca22763067fe006e.png)


- the release adds support for new Vulkan extensions
- exposes VK_AMD_anti_lag, VK_KHR_calibrated_timestamps, VK_KHR_pipeline_binary and others

![](../../assets/59c53162f0922fef.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.