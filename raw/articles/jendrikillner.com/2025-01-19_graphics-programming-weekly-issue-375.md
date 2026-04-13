---
title: Graphics Programming Weekly - Issue 375
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-375/
author: Jendrik Illner
published: '2025-01-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- The article explains spectral radiometric quantities.
- Presents how it relates to human perception to create photometric quantities.
- Additionally covers techniques to efficiently deal with spectral rendering implementations.

![](../../assets/76da64322ec412a3.png)


- The Vulkan example presents how to use the VK_KHR_dynamic_rendering_local_read and VK_KHR_dynamic_rendering extensions to replace the need for render passes.
- Explains how dynamic rendering compares to Vulkan 1.0.
- Shows how local reads can be used to implement a deferred renderer with a composition pass.

![](../../assets/54b6b98f057e2d63.png)


- The video provides a high-level introduction to compute shaders with OpenGL.
- Shows how to apply the concepts to the implementation of a particle system.
- Explains how to implement the shader, connect it to OpenGL, and execute the work.

![](../../assets/808d4c7f1819db0e.png)


- The blog post calls out that color spaces such as CIELAB don’t offer perceptual brightness for all colors.
- Explains how certain colors appear brighter to humans than others at the same hue.

![](../../assets/667125570cbce2ff.png)


- The blog post provides examples of how different HLSL implementations cause very different codegen results.
- Shows that unintuitive implementations can be required to allow the compiler to map to native instructions.
- Suggests that compiler pattern matching hinders performance and it could be beneficial to expose native instructions as intrinsics.

![](../../assets/f658454e8e4ea2d7.png)


- NVIDIA released an interactive and free course about learning OpenUSD concepts.
- Structured into modules, the course combines written guides and video tutorials for a comprehensive learning experience.
- Hands-on Jupyter notebooks let you explore practical examples and deepen your understanding of key topics.
- Just released: Applied Concepts courses on composition arcs, asset structure principles, and data exchange pipelines.

![](../../assets/d3576a8e7539046c.png)


- The video provides an overview of the Mega Geometry technique by Nvidia.
- Aims to solve the issue of streaming clusters into acceleration structures without BVH rebuilds.
- Discusses new possibilities of the presented demos.
- Currently an Nvidia-only API.

![](../../assets/652b2043106258ae.png)


- The video recording of a talk that discusses Compact Poisson Filters to allow fluid simulations for interactive applications.
- Explains the solver technique and implementation steps in detail.
- Presents performance and demos of the technique.

![](../../assets/833b98181bbd7882.png)


- The blog post explains how to implement a dissolve shader.
- Presents examples of different methods for the implementation and compares them visually.
- Additionally provides examples of the technique when applied to particles.

![](../../assets/a46e5f6089c0a47a.png)


- Collection of blue sky posts covering tech art.
- Contains videos and pictures of in-progress projects.
- Additionally contains a number of links to tutorials and posts covering a variety of topics.

![](../../assets/f0d6aadde2012f8e.png)


- The blog post discusses different classes of HLSL instructions and associated costs on RDNA hardware.
- Presents how many instructions are required for the various patterns.
- Additionally presents insights into other patterns that can affect the performance of generated code.

![](../../assets/a9afd9ad171110de.png)

Thanks to [Jasper Bekkers](https://x.com/JasperBekkers/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.