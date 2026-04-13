---
title: Graphics Programming Weekly - Issue 389
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-389/
author: Jendrik Illner
published: '2025-04-27'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- this paper introduces a framework that extends PBR materials to handle transparent surfaces like glass and windows
- addresses limitations of traditional reflection models that struggle with highly specular and transparent materials
- combines advantages of physically-based methods with efficiency by focusing on intrinsic image decomposition
- provides deterministic, interpretable control for material editing while maintaining physical plausibility

![](../../assets/765fb6aa3328095d.png)


- This tutorial demonstrates techniques for implementing efficient custom lighting models
- targets low-powered mobile devices, or augmented reality headsets
- part of an ongoing series exploring custom lighting techniques
- shows which features to remove for more efficient calculations

![](../../assets/ec3924b414f0030b.png)


- this paper explores alternative scene representations using transparent polyhedra (octahedra and tetrahedra) with triangular faces
- presents a differentiable rasterizer that efficiently runs on GPUs, enabling end-to-end gradient-based optimization with real-time rendering
- achieves comparable quality to state-of-the-art volumetric methods like 3D Gaussians while requiring significantly fewer primitives
- the bounded nature of these primitives creates natural compatibility with traditional mesh-based tools for downstream applications

![](../../assets/73d0e96cb7e4e3bc.png)


- this research introduces Gaussian-enhanced Surfels (GESs), combining 2D opaque surfels for coarse geometry with 3D Gaussians for fine details
- the novel two-pass rendering approach is entirely sorting-free, eliminating the computational bottleneck of Gaussian sorting
- achieves both ultra-fast frame rates and avoids the popping artifacts commonly seen in other real-time radiance field rendering methods
- includes extensions like Mip-GES for anti-aliasing, Speedy-GES for faster rendering, and 2D-GES for compact storage

![](../../assets/1bbf241d7253723f.png)


- This video explores the technical reasons behind the distinctive visual appearance of PlayStation 1 games. Especially explaining the effects of the Silent Hill series
- focuses on explaining projection from world into projection space, vertex shading, color quantization etc.
- Explains the hardware limitations that led to the characteristic polygon wobbling and texture warping

![](../../assets/b3617aabf52a575c.png)


- this animated video breaks down essential machine learning and AI concepts in a visual, accessible way
- uses animations to explain complex algorithms and mathematical foundations behind modern AI systems
- helps viewers develop an intuitive understanding of key AI concepts without requiring advanced mathematical background

![](../../assets/d55bfc6849d37173.png)

Thanks to [Manish Mathai](https://github.com/goodbadwolf/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.