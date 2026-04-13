---
title: Graphics Programming weekly - Issue 176 — March 28, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-176/
author: Jendrik Illner
published: '2021-03-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a method that allows a 5−7× reduction in memory footprint compared to indexed triangle meshes
- this is archived by converting vertices into vertex grids and using compressed displacement vectors to compress the vertex data
- the additional work required to decompress the data adds around 15% of overhead

![](../../assets/5e7dd83b15c393a0.png)


- the blog posts provides an easy to understand summary of the Vulkan Synchronization
- additionally includes information about what parts of the API have changed with Synchronization2

![](../../assets/f52ccf28cb90b740.png)


- the article presents experiments with spectral rendering to find an importance sampled wavelength sampling approximation
- presents comparisons of the different approximations

![](../../assets/6c690058554eb95c.png)


- the paper presents a technique to allow path tracing through sparse volumes
- based on NanoVDB with unbiased multiple scattering volume path tracing and neural denoising
- able to render Disney Clouds in 60 ms

![](../../assets/33fbc1898b1c4586.jpg)


- video recording of the SIGGRAPH 2020 was released
- the paper presents how to use a neural representation to infer additional results such as reflections and global illumination

![](../../assets/a9f95052f8186041.png)


- open-source release of a tool to generate meshlets (for use with mesh shaders, GPU based culling, etc)
- additionally can generate bounding sphere and visibility cones

![](../../assets/5f2e694748785882.jpg)


- Vulkan Ray tracing tutorials have been updated
- added new tutorials on how to use vkCmdTraceRaysIndirectKHR and how to ray cast ambient occlusion using ray queries

![](../../assets/0a4655d8ee81e247.png)


- the paper presents a technique to discover a potentially visible set (PVS) of triangles visible from a region of space
- this technique uses ray shooting guided by Adaptive Border Sampling and Reverse Sampling
- provides an overview of how the method was implemented using Vulkan hardware Raytracing

![](../../assets/ada5955052107503.jpg)


- the video tutorial explains how to generate a procedural stylized lawn shader
- uses a combination of noises to create the shading
- additionally adds support for sparking based on view angle

![](../../assets/5265fb6c270223df.png)


- the Twitter thread presents a breakdown of the Valheim rendering pipeline (implemented using Unity)
- shows the different rendering passes, what shaders are expensive, and usage patterns responsible for suboptimal performance
- additionally provides pointers at possible improvements

![](../../assets/0ab632b03e9d4ed1.png)


- collection of tech art tweets
- covering art style demonstration, material creation, destruction, and much more

![](../../assets/37c3a9cf316e1502.png)


- the tutorial explains an approach how to implement cutting walls into 3D walls
- used method uses a screenspace projected sphere that is placed on walls using raycasting
- implementation walkthrough is using visual scripting in Unity

![](../../assets/e812c4d9b0b3599d.jpg)

Thanks to [Vivitsu Maharaja](https://twitter.com/vivitsum) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.