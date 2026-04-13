---
title: Graphics Programming weekly - Issue 249 - August 21, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-249/
author: Jendrik Illner
published: '2022-08-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents an overview of the composable declarative GPU authoring
- shows how chain compute dispatches, handles historical data as well as visualizes temporary results
- it additionally discusses how the tree representation allows internal composability and enables background optimizations

![](../../assets/3340b66e5a26b7d2.png)


- the article continues the series of translating DXIL to SPIR-V for use with vkd3d-proton
- the part covers how to convert structured control flow. DXIL is unstructured and needs to be converted into structured SPIR-V
- discusses the limitations, oddities and solutions developed to make the conversion work and debuggable

![](../../assets/c2757ea3f8e2fdf2.png)


- the article presents how to integrate new compilers into the compiler explorer infrastructure (which can be run locally)
- discusses the DXC and AMD Radeon™ GPU Analyzer integration
- shows the limitations of the existing integration

![](../../assets/47d6ac6fa8aa4cf7.png)


- the video tutorial presents how to write universal rendering pipeline shaders in HLSL
- shows how to implement simple diffuse & specular lighting, explaining the render pipeline as the author goes along
- it also shows how to integrate shadow rendering
- additionally presents the debugging tools available

![](../../assets/3ed580993a47df49.png)


- the article explains the underlying theory for Bézier curves and shows how the different component interacts
- presents how to express the curve mathematically so that intersections between a ray and the curve can be found
- shows how to use the information to detect if a pixel is inside or outside of a shape

![](../../assets/561495f6d939c3c0.png)


- the article discusses the different approaches that were tried during the development of lumen
- presents tradeoffs of the different techniques and how the decision was made on which one to use
- it additionally shows how the arrival of Nanite changed several variables significantly and therefore made a new evaluation of approaches necessary

![](../../assets/6baa2d4d134853e1.jpg)


- the video presents the foundation how to general ReSTIR sampling
- this allows resampling with importance sampling for arbitrary domains
- continues to show how to apply these concepts to allow ReSTIR for path-tracers
- shows how to allow reuse across paths, discusses considerations and limitations

![](../../assets/1a2803cbb6f8e758.png)


- the video shows how to implement a Truchet effect using shadertoy
- presents the whole implementation from start to finish, showing all intermediate steps
- it additionally discusses how to extend the concepts and possible future extensions

![](../../assets/8a2a68bdf0306f2f.png)


- the paper presents how to adapt multidimensional adaptive sampling for interactive real-time ray tracing
- applies the technique to stochastic effects such as motion blur, depth of field, and indirect illumination
- presents a performance comparison against Halton sampling

![](../../assets/080c5af6d6075eec.png)


- the OpenGL fog rendering series extends the previous works and implements Layered and animated fog
- explains the underlying theory before showing the implementation using GLS

![](../../assets/1d78439c71d17f3c.png)


- the video tutorial shows how to implement cartoon outlines in screen space
- discontinuities in scene depth and normals are used to detect edges
- the resulting filtered edge mask is used to apply outlines around objects

![](../../assets/3afc2d309db63e28.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.