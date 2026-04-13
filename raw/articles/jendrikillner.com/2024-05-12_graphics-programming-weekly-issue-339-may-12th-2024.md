---
title: Graphics Programming weekly - Issue 339 - May 12th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-339/
author: Jendrik Illner
published: '2024-05-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- AMD released documentation for the Micro engine and the RDNA 3 ISA

![](../../assets/2659b4a526c77250.png)


- the blog post presents that the Brotli-G (GPU compression library) now allows a pre-condition step that allows further file reduction
- shows how to use the feature and what image formats are currently supported

![](../../assets/218d002f8da4963f.png)


- the article continues the development of a voxel raytracer by explaining anti-aliasing and soft shadows
- presents the difference between numerical integration and stochastic integration solvers
- shows the technique with anti-aliasing first and derives soft shadows as a follow-up

![](../../assets/ee6164963cfa1490.jpg)


- the video tutorial explains the Vulkan command buffer concepts
- presents limitations that OpenGL had and how Vulkan can solve these
- shows the command buffer lifecycle, explains memory management
- presents how to use the API to operate on command buffers

![](../../assets/ea8c2f832cfbe484.png)


- the article discusses the design trade-offs for a shader graph system
- presents the complexity when integrating with modern complex shading systems
- shows how Unreal and Unity implement the ideas

![](../../assets/daccf246e41f54f8.png)


- the paper introduces the ZH3 format for spherical harmonics that fills the gap between linear and quadratic SHs
- The proposed solution improves the quality at the cost of a single extra coefficient per channel
- the source code is provided

![](../../assets/693467a92191c3d6.png)


- the blog post discusses projection methods for spherical videos
- presents issues with existing methods
- reverse engineers what apples Methods appears to be doing and how it’s able to achieve higher quality

![](../../assets/2afd017fab82d199.png)

Thanks to [Keith O’Conor](https://twitter.com/keithoconor) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.