---
title: Graphics Programming weekly - Issue 275 - February 19th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-275/
author: Jendrik Illner
published: '2023-02-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the author presents his impression from the Vulkanied conference
- presents an overview of the topics covered, what discussions revealed during panel discussions, and what are common issues

![](../../assets/ef6275968446308f.jpg)


- the playlist of video recordings of the talks presented at the Vulkanised 2023 in Munich
- covers a large number of topics such as Mesh Shader best practices, source-level shader debugging, performance optimizations
- ranges from mobile and desktop to virtual reality

![](../../assets/912ced41b5a23c1e.jpg)


- the article presents a breakdown of how Teardown is being rendered
- shows all stages of the pipeline required for the final frame
- shows how the G-Buffer is drawn, how details are applied to the voxel
- additionally presents how the weather effects, lighting, as well as denoising are implemented
- additionally covers many more steps of the frame pipeline

![](../../assets/fef4c63c27429fe8.png)


- the article provides an overview of different techniques to adjust object colors from objects
- shows how to implement the presented techniques using Unity visual shader language as well as in HLSL

![](../../assets/f8777bd7bde02dff.png)


- the video tutorial explains how to implement ray-sphere intersection testing
- discusses the mathematic derivation of the technique
- shows how to implement the intersection testing using GLSL in shadertoy

![](../../assets/c2d5cb6e3ca6f66a.png)


- the paper presents a technique to approximate hair lighted by an environment map, direct lighting, or a global illumination
- build around the modeling of obstruction around each hair using spherical harmonics instead of requiring deep opacity maps

![](../../assets/53506c3d742fb707.png)


- the blog post continues the series on float compression techniques
- investigates how SIMD instruction sets can be used to optimize
- presents how it affects the results

![](../../assets/3f52c10c1adb8e11.png)


- the video discusses the difference between Parallax Occlusion and normal mapping
- presents how to optimize the implementation to adjust the steps only for cases where precision is required
- implementation is shown in both Unity and Unreal

![](../../assets/1b51b8958b604e70.png)

Thanks to [Aras Pranckevicius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.