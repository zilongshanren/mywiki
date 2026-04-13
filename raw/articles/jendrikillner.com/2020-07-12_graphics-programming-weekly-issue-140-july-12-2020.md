---
title: Graphics Programming weekly - Issue 140 — July 12, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-140/
author: Jendrik Illner
published: '2020-07-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article summaries the changes announced at WWDC
- Apple will transition from Intel CPUs / GPUs to custom hardware
- the article shows an architecture overview, best performance practices, new hardware, and API features
- including improved GPU debugging, shader compilation pipeline, raytracing and windows based tools

![](../../assets/75dc2ac078ea174a.png)


- a look back at how RenderMan handled blurry glossy surface reflection in 2007 for Ratatouille
- using a technique called Brick maps, a form of 3D radiance caches

![](../../assets/038d0d5aa759cffe.jpg)


- the blog post explains a CSG algorithm implementation based on using the depth and stencil buffer
- the technique is used to implement player visibility in bushes

![](../../assets/96c19ea28e637d8d.png)

- the author provides an overview of the mindset, technique, and requirements for learning graphics programming
- additionally contains a list of resources to books, videos, web, etc. about the topic

![](../../assets/ead01ed0cc33217a.jpg)


- the master thesis looks at Machine Learning techniques to discover visual issues, such as stretched textures, missing textures in a game environment

![](../../assets/cc601992810cb714.png)


- this PIX upgrade adds support for signal wait visualizations and improved buffer visualization

![](../../assets/044245751821d56a.png)

- the Unity tutorial explains how to implement a stylized skybox with sun, moon, and clouds using the visual shader graph system

![](../../assets/78d36ecf023b28c3.png)

- the article presents how to use the AMD GPU Analyzer for compute shaders
- the tool allows the collection of low-level information such as the ISA disassembly, register usage, etc

![](../../assets/062aa9698485b94d.png)


- the article explains got to use the AMD GPU ANALYZER to get low-level information about graphics workloads
- shows what additional information is required to describe the required pipeline state

![](../../assets/9d61e9ec2e32394c.png)


- the article explains how to collect GPU timestamps and synchronize the CPU and GPU timestamps

![](../../assets/6f5133ddafacb532.png)

- the article explains the basics required to render a triangle with WebGL
- focused on clarity to show only the WebGL functionality and not provide any higher-level abstractions

![](../../assets/cd9164780abee07b.png)


- explanation of the architecture of executing OpenGL on D3D12 using a Mesa-based implementation
- presents the development of the implementation and how performance was increased at each step

![](../../assets/4cfec52b23a75a73.png)


- the article explains how spectral rendering can be implemented in a DXR based path trace
- shows what needs to be adjusted from a classical path tracer
- additionally shows how to convert existing data from textures into spectral data for rendering

![](../../assets/b571e52e71d93e74.png)


- collection of tech art and VFX twitter posts, including a look at facial animation tech of the Last Of Us 2

![](../../assets/b8ee727710e6693c.png)

Thanks to [Sondre Kongsgård](https://github.com/kongsgard) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.