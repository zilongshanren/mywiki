---
title: Graphics Programming weekly - Issue 285 - April 30th 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-285/
author: Jendrik Illner
published: '2023-04-30'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- Article discusses implementing backface culling in mesh shaders
- Compares the efficiency of three different methods: Cluster cone culling, precomputed visibility masks, and multi-cone culling
- Presents performance numbers for each technique on different scenes

![](../../assets/a51946a6c07c06a4.png)


- the article presents progress on a Rust-based home graphics engine project
- focuses on the discussion of how to integrate resource management into the Rust memory model and GPU-driven rendering considerations
- presents how to setup bindless rendering pipelines, implement frustum culling in compute shaders, and how to integrate with an ECS-based engine

![](../../assets/4a7ac63a03f591b0.png)


- the article presents improvements done to the AMD GPU profiler
- It primarily focuses on the shader/pipeline disassembly view improvement and has been updated to make it easier to navigate
- but also mesh shader and Conservative Rasterization mode have been added to support

![](../../assets/916a72b1428a7e9f.png)


- the video explains how to use partial derivatives in HLSL shaders to calculate the amount of light distortion to calculate refractions
- presents the results and implementation using UE4

![](../../assets/248243c8c6c8f499.png)


- the video tutorial explains how matrices are combined
- visually explains the operations by explaining how a robotic arm transformation is implemented
- followed up by explaining how the multiplications are implemented mathematically but always visually explaining the relationships

![](../../assets/a735bfcab9a3d743.png)


- the video explains how PVS (Potential Visibility Set) used by Quake is implemented
- visually shows how the graph is constructed and what optimizations were applied to optimize the set further

![](../../assets/2a39b81a5a28f2f2.png)


- the article explains how star wars battlefront explosion VFX has been implemented
- shows how flipbook textures are combined with LUT textures for recoloring as needed

![](../../assets/25db9d0544359102.jpg)


- the article explains a series of Interpolation and shows how they build up to cubic Quaternion interpolation
- covers Hermite Curve, Catmull-Rom Cubic, and finally, Quaternion Catmull-Rom Cubic Interpolation

![](../../assets/e989a26639f964b1.png)

Thanks to [Nathan Reed](https://www.reedbeta.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.