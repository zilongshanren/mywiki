---
title: Graphics Programming weekly - Issue 215 - December 26, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-215/
author: Jendrik Illner
published: '2021-12-26'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article describes a setup to use a software rasterizer to create winter decorations for tiny projectors to make Christmas decorations
- happy christmas :)

![](../../assets/f7d1019bd8294f94.jpg)


- the post presents the importance of testing images that allow the testing of a renderer
- discusses the different kinds of test images, how to gather them and compare if they remain unchanged
- presents heuristics to judge if changes that introduce image changes are valid or problematic

![](../../assets/f315cfac13c48609.png)


- the article discusses sources of nondeterministic rendering in PBRT-3
- presents how the renderer was made deterministic
- additionally presents what advantages and debugging abilities determinism enables

![](../../assets/e0e5e5471822d0c6.png)


- the article presents the release of the kajiya experimental renderer written in Rust
- discusses the design and implementation choices, targetting the Vulkan API and Rust for shader authoring
- additionally presents a look at the future direction of the project

![](../../assets/eace8f8a158212b4.png)


- The shader video tutorial shows how to create a shader that projects textures from the top, front, and side (Triplanar projection) without UV coordinates
- implementation is shown in both Unity and Unreal visual shader authoring system

![](../../assets/51b5bc6cda9bc716.png)


- the article presents how to use barycentric coordinates to improve triplanar projections
- done by blending between smoothed and flat normals
- presents how to use virtual triangles to generate barycentric coordinates for terrains if not available on the target system

![](../../assets/9a6b2c548b88b370.png)


- video discussing the best graphical releases of the year
- presenting the most prominent innovations of the year, showing how the expectations of next-generation have evolved
- additionally discussing oddities of the year

![](../../assets/548bc0607d02a936.png)


- the article discusses why Vulkan drivers expose a single heap with multiple memory types
- explains how resource compatibility should be handled in resource allocation

![](../../assets/f3ec2b2667175f80.png)


- the post describes the differences between the new WebGPU Shading language and GLSL
- shows the explicit nature of the language
- highlighting the difficulty in translating between the languages

![](../../assets/2e15345d1a0132cd.jpg)

Thanks to [Jasper Bekkers](https://twitter.com/JasperBekkers/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.