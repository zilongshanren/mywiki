---
title: Graphics Programming weekly - Issue 246 - July 31, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-246/
author: Jendrik Illner
published: '2022-07-31'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the presentation introduces compute-shaders, explaining the software and hardware concepts
- expands upon the basis to explain execution patterns, memory, and cache hierarchies
- texture reading/writing patterns as well as common mistakes

![](../../assets/ca1ed9b4c3054b0b.png)


- new tool from AMD to provide more insights into the performance of raytracing applications
- show much memory is used, if redundant information is stored, all geometric axis aligned, etc
- video presentation covering the information available is linked

![](../../assets/9b30f28757292c81.jpg)


- the article presents an Nvidia API extension that allows multiple buffer swaps (between windows and applications) to be synchronized
- shows the D3D12 API and discusses the usage, conditions for correct usage as well as limitations

![](../../assets/dfab16a727acd9fa.png)


- Nvidia has updated the performance best practices for RTX usage
- contains new recommendations enabled with shader model 6.6, updated guidelines for inline ray tracing
- and many more minor updates across the categories

![](../../assets/12725e3d92d7907c.jpg)


- the detailed article explains the different memory pools available and how they differ between different types
- shows how D3D12 exposes the memory management
- discussing strategy for texture and buffer uploads
- presents performance numbers for CPU and GPU reads/writes and uploads to different memory types

![](../../assets/4c6b00e67ae22a9d.png)


- the article discusses the Rust shades crate that allows writing Rust domain-specific language that can be used to generate GLSL code
- explains the motivation, implementation as well as open issues
- it additionally provides a comparison against other solutions

![](../../assets/e9900d9988a0f6ce.png)


- the article presents a derivation of a light attenuation function to separately control the maximum intensity and radius
- function is designed to reach zero influence to be used with clustered shading

![](../../assets/c3796c83b76e34c1.png)


- the article aimed at beginners explains how images are applied to 3D objects
- presents what UV (Texture coordinates are) and how to visualize them
- shows how to explore the relationship between mesh and UV coordinates from Unity shaders

![](../../assets/ffb90fe72eba9d38.png)


- the article presents an overview of barycentric coordinates
- shows that barycentric can be interpreted as a distance field
- derives how to render wireframe line rendering from these distances

![](../../assets/13841da0f1d6e4ef.png)


- the article provides an overview of font rendering
- looks at the different levels that cover glyph evaluation, line layouts, and antialiasing
- presents rasterization constraints, how to cache glyphs for efficient rendering
- additional covers how to deal with sub-pixel positioning

![](../../assets/c59022bf7bfe7935.png)


- the presentation video discusses the LOD generation used in Cyberpunk 2077 (3D models and materials)
- discusses the different algorithms that were used for different types of models and materials
- provides an overview of the pipeline and infrastructure integration

![](../../assets/cd94a7007ae9d8ae.png)


- slides for the GDC presentation talking about the deferred texturing solution has been released
- summary in
[week 231](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-231/)

![](../../assets/1cebcf06697687c9.jpg)


- a growing collection of graphics samples and libraries for the zig programming language
- the provided samples cover how to use the released libraries

![](../../assets/377a3b9e315ca6a8.png)

Thanks to [Michael Hazani] for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.