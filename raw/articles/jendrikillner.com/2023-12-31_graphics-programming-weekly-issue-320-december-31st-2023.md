---
title: Graphics Programming weekly - Issue 320 - December 31st, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-320/
author: Jendrik Illner
published: '2023-12-31'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents how different shader constructs are converted into instruction on RDNA2
- shows the impact on code generation that small changes can have
- what can be optimized by today’s compilers and what cannot be optimized

![](../../assets/1cfa8ca2cef82eec.png)


- the article discusses a technique that calculates the transformation required between a known base and target position
- applies this technique to a 3D cloth simulation to calculate the shading tangent and normals

![](../../assets/819defe0e9a048db.png)


- the article discusses how to generate LODs using a meshlet-based Directed Acyclic Graph approach
- talks about the data structure, the approach, and implementation details of the model
- mentions considerations for choosing meshlet sizes as well as LOD selection using the graph

![](../../assets/2e43e718ea4630f5.png)


- the video provides a great visual breakdown of the rendering pipeline
- covers how scenes are represented, how the source triangles are transformed, rasterized, and shaded to finally appear on screen
- additionally provides a small overview of more recent techniques such as ray-tracing and DLSS

![](../../assets/2e31ccebda56fbc3.png)


- the article provides an overview of different heuristics to choose from when building a BVH for raytracing
- compares the ray tracing performance of the heuristics in a test scene
- additionally provides ideas for future research in the area

![](../../assets/9fd46ec0036eb3c7.png)


- the article provides a walkthrough of the practical tweaks and tricks used to implement a ReStir-based global illumination system into a research framework
- discusses the caching strategies, light leaking improvements, and performance optimizations

![](../../assets/50510444c2c9807b.png)


- the article provides insights into how to convert OpenImageDenoise into HLSL compute shaders
- shows a high-level overview of the technique
- presents a couple of steps to reduce the performance cost

![](../../assets/45bfd218ef69ebfc.png)

Thanks to [Giuseppe Modarelli](https://twitter.com/gmodarelli) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.