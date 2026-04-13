---
title: Graphics Programming weekly - Issue 180 — April 25, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-180/
author: Jendrik Illner
published: '2021-04-25'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- 64-bit integer atomics are now supported
- some new capability bits got introduced as not all views, sources support it on all hardware
- dynamic resources allow indexing into a single array of descriptors,
- explains what helper lanes are and how they relate to lanes and quads
- compute shader derivatives and how they are derived from thread group layout
- Wave Size attribute allows shaders to specialize shaders for wave sizes

![](../../assets/5a76bf92cecd9bcf.png)


- the tutorial provides a walkthrough of a raymarching supermassive black hole shader
- implementation is an approximated physically-based done using Unity
- author presents the sources, approximations done and discusses limitations

![](../../assets/150be221b7b9b4a3.png)


- Talk discusses how the performance of the ray-traced direct illumination was greatly improved
- presents an overview of what ReSTIR importance sampling algorithm
- shows to the memory coherence and bandwidth was reduced through pre-randomization of input lists
- additionally discusses how the number of rays could be reduced by decoupling shading, reuse, and visibility

![](../../assets/5a85b189807a0126.png)


- explains shadow denoising process
- broken down into 5 blocks that are explained individually
- shadow mask creation, local neighborhood, occlusion, reproject, and spatial filters
- first covers the functionality of these blocks
- afterward shows optimizations applied to each stage

![](../../assets/644c7116e93587b5.png)


- overview of Variable Rate Shading (VRS), what is supported with Tier 1 and 2
- edge detection run as part of the tone mapping step, generating two shading images (default and conservative)
- VRS shading rate image is also read in compute shaders for reduced shading rate for compute shaders
- presents performance numbers

![](../../assets/e8bf2bee2ba34591.png)


- visual representation that shows why inverted depth buffer range with floating-point formats improves precision

![](../../assets/6ff9a943c0ab0006.png)


- list of posters presented at I3D
- covering Linearly Transformed Spherical Harmonics, Style-Preserving Pixel Art Magnification, Rendering of Many Lights with Grid-Based Reservoirs and others

![](../../assets/0de033419f762ad7.jpg)


- part 5 of beginner-focused shader tutorial series
- focuses on data types, representation of color
- shows how to output constant colors in Unity shaders code, visual shader graph, and unreal engine

![](../../assets/97ea2e3e95407a16.png)


- the Graphics Codex online textbox is now a free
- covering an extensive range of topics, model of light, Rendering equation, camera, material models, path tracing, parallel architectures, and much more
- additionally contains many references to further sources on the topics

![](../../assets/ae273833f89e1d83.jpg)


- the paper presents a method that uses the AABS from hardware raytracing shaders to apply decals and lights
- uses a zero-length ray to collect all overlapping decals/lights per pixel
- compares performance against deferred decals

![](../../assets/1afe17cccf6a46cb.png)

Thanks to [Unai Landa](https://twitter.com/unai_landa) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.