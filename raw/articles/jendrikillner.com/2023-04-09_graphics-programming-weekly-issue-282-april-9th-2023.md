---
title: Graphics Programming weekly - Issue 282 - April 9th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-282/
author: Jendrik Illner
published: '2023-04-09'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article provides a central place for matrix understanding for computer graphics
- explains storage and multiplication order, how they are expressed in HLSL and GLSL
- explains coordinate system handedness, what the left-hand/right-hand rules are
- additionally presents some questions that help to detect conventions used if applications did not document their choices

![](../../assets/87dc49447927ba9a.jpg)


- the blog post shows different sampling strategies
- presents the patterns along 1D lines, 2D squares as well as 2D circles

![](../../assets/d33392ab165cb0a3.png)


- the tutorial explains how to apply color modifications in shaders
- shows how to modify luminance, saturation, brightness, or contrast
- implementation is provided using Unity shaders

![](../../assets/ddd7f3dfcf03af6c.png)


- the long Video explains detailed how to render a Stylized grass
- covers the art creation, shader logic, performance considerations
- additionally covers how to apply movement, occlude parts if intersecting with the camera, LOD setup, and much more

![](../../assets/36b588340f7dfe99.png)


- the paper proposes a new solution to accelerate AABB when used as BVH for objects that are thin and diagonal
- the solution presented embeds a binary voxel data structure for each node and showed how to use these to reduce false positives
- additionally presents how to use a LUT to compress the voxel data

![](../../assets/3f56353d20773598.png)


- the paper introduces a new rejection method based on the PDF shape similarity between pixels for single-bounce ReSTIR
- this helps to reduce spatial resampling across shadow edges and material boundaries

![](../../assets/25b985f59e53a9a4.png)


- the article presents an overview of ReSTIR/ReGIR, explaining similarities and differences between the techniques
- shows how to set up reservoirs to allow spatial path reuse

![](../../assets/23939abc6c4b38b5.png)


- the article presents the difference between Object Normals, Tangent Normals as well as World Normals

![](../../assets/4d97a1720950de56.png)

Thanks to [Max R.R. Collada](https://twitter.com/maxandonuts) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.