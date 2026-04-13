---
title: Graphics Programming weekly - Issue 77 — March 17, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-77/
author: Jendrik Illner
published: '2019-03-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

There will be no newsletter next week. I am at GDC all week. Will be returning as usual on April 1st.

- the latest update adds support to run the D3D12 game on windows 7
- user mode d3d12 implementation without win10 kernel level optimizations
- no public information about the implementation details yet

![](../../assets/129789a512273341.jpg)


- source code for the Ray Tracing Gems has been released

![](../../assets/adb23720cbe44a75.jpg)

- follow up to the post discussed in
[issue 75](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-75/) - presents a way to speed up the presented technique by 2.34x
- discussion of the rendering error using the Eric Heitz method discussed above

![](../../assets/e0d4b91cd051fda6.png)


- pix for windows now supports High-Frequency Counters
- This allows that hardware counters are sampled multiple times per draw/dispatch and allows further insight into GPU activity

![](../../assets/c2d350b23c7b6304.png)


- a ray tracing system for Wolfenstein 3D using only WebGL 1
- a hybrid approach, raytraced shadows, diffuse GI and reflections
- overview of the implementation for the different elements
- how to apply temporal stability and noise reduction filters

![](../../assets/ea0597ca0be7fe2e.png)


- explains the concepts of textures, mip-mapping, sampling
- shows the different filtering, addressing mode available on texture samplers
- describes how to use DirectXTex to load textures and upload them into GPU memory
- introduction into compute shaders and how to use them to generate mipmaps

![](../../assets/8e2084e0e537ad2d.png)


- a new low distortion mapping between squares and triangles that is also cheap to compute
- can be used for random sampling of points with a uniform density

![](../../assets/af44a8ed5ae537b4.png)

- presents 3 optimizations that can be applied to BVH to increase performance
- usage of inverse ray direction, ray traversal early-out and surface area heuristic for construction of the BVH

- the comments contain a few more tips for increased performance

Thanks to [Matt Pharr](https://pharr.org/matt) for support of this series.

You would like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.