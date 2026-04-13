---
title: Graphics Programming weekly - Issue 179 — April 18, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-179/
author: Jendrik Illner
published: '2021-04-18'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents comprehensive coverage of BVH hierarchies, especially focused on ray tracing
- provides an overview of the basics, compare many state of the art algorithms for construction and traversal
- provides a comprehensive overview of existing hardware and frameworks
- additionally presents the most common techniques and recommendations for the different algorithms to be used

![](../../assets/0793e94492d49f06.png)


- the video tutorial presents how to render and animate a newton’s cradle with SDFs
- implementation is done using shader toy

![](../../assets/af3f41493ff5f191.png)


- the article presents the difference between ddx/y ddx/y_fine
- presents the history of these instructions in HLSL and how different hardware/API behaves
- shows example use cases on how fine and coarse rasterization affect seamless sphere mapping
- additionally presents how fine derivatives can be used for quad-level communication

![](../../assets/9af21760533b1392.png)


Marmoset is the developer of Toolbag, an industry standard 3D rendering and authoring suite. We’re looking for experienced programmers to work on challenging problems in rendering, texture authoring, baking, and more. If you’re interested in pushing a GPU as far as it can go, we’d like to meet you.

![](../../assets/d57aaa68be34d014.png)


- Vulkan API now exposes video support
- extended the concept of the queue to support decode/encode queues with different extensions for several codecs
- the article presents a walkthrough of the API through the usage of an encoder example

![](../../assets/1e756a38bdf1efc7.jpg)


- the article presents an overview of why filtering for pixel art at non-integer values is vital to prevent artifacts
- provides an overview of numerous filters and links to resources
- additionally provides a demo application to compare the different filters

![](../../assets/ca3ec02be7333a23.png)


- the paper presents a machine learning-based approach that uses differential rendering to approximate several simplifications effects simultaneously
- presents a model that can jointly optimize over shape, appearance, and animation parameters

![](../../assets/5fdf0fc6a82666c3.png)


- the article provides an overview of shader assembly reading
- focuses on GCN instructions
- provides a brief overview of the hardware, the different operations, and how small changes can make significant differences in generated code

![](../../assets/0a0917d8ce35fcdf.png)


- the article presents two common approaches to fullscreen passes
- using PIX shows why using a single large triangle is more efficient and describes why this is the case

![](../../assets/3a438d56a76fc6d9.jpg)

Thanks to [Top-OR](http://top-or.de/projects) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.