---
title: Graphics Programming weekly - Issue 7 — September 10, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-7/
author: Jendrik Illner
published: '2017-09-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Which Compute ID for me?](https://dickyjim.wordpress.com/2017/09/05/which-compute-id-for-me/amp/) [[wayback-archive]](https://web.archive.org/web/20170911051237/https://dickyjim.wordpress.com/2017/09/05/which-compute-id-for-me/amp/)

- easy to read overview of how compute shader ids are calculated for 1D and 2D processing
- provides examples

- explanation of specular light calculations for area lights (Sphere, disk, rectangle, tube light)
- uses the Representative point method
- light vector points to the closest point on the light mesh, relative to the reflection vector

[Introduction to the Jacobian and its use in graphics](https://mehdins.wordpress.com/2017/09/04/introduction-to-the-jacobian-and-its-use-in-graphics/) [[wayback-archive]](https://web.archive.org/web/20170911052112/https://mehdins.wordpress.com/2017/09/04/introduction-to-the-jacobian-and-its-use-in-graphics/)

The Jacobian is the key showing us how a region changes under a transformation.


- Gives 4 examples with derivations:
- In 1D, the substitution
- Cartesian to Polar
- Specular microfacet BRDF
- Volume preserving ball/cube mapping


[Demo with non-linearly quantized moment shadow maps and more](http://momentsingraphics.de/?p=175) [[wayback-archive]](https://web.archive.org/web/20170911052336/http://momentsingraphics.de/?p=175)

- demo for the non-linearly quantized moment shadow maps paper released earlier this year

[Improving a renderer](http://trevorius.com/scrapbook/uncategorized/improving-a-renderer/) [[wayback-archive]](https://web.archive.org/web/20170911052443/http://trevorius.com/scrapbook/uncategorized/improving-a-renderer/)

- overview of the effects that went into a 64k demo
- provides links to papers and code samples for some of them

[D_GGX in mediump/half float](https://gist.github.com/romainguy/a2e9208f14cae37c579448be99f78f25) [[wayback-archive]](https://web.archive.org/web/20170911052514/https://gist.github.com/romainguy/a2e9208f14cae37c579448be99f78f25)

- restructure GGX calculations so that they can be performed in half precision (16 bit float instead of 32)

- a number of projects aimed to help the learning process for computer graphics
- to be used in combination with
[Graphics Codex](http://graphicscodex.com)

[Skinning in a Compute Shader](https://turanszkij.wordpress.com/2017/09/09/skinning-in-compute-shader/amp/) [[wayback-archive]](https://web.archive.org/web/20170911052726/https://turanszkij.wordpress.com/2017/09/09/skinning-in-compute-shader/amp/)

- code example about how he does skinning in a compute shader
- interesting discussion about mobile gpus on twitter:
[https://twitter.com/turanszkij/status/906603939239473153](https://twitter.com/turanszkij/status/906603939239473153)

[Last Week on DirectX Shader Compiler (2017-09-09)](https://blogs.msdn.microsoft.com/marcelolr/2017/09/10/last-week-on-directx-shader-compiler-2017-09-09/) [[wayback-archive]](https://web.archive.org/web/20170911052801/https://blogs.msdn.microsoft.com/marcelolr/2017/09/10/last-week-on-directx-shader-compiler-2017-09-09/)

- overview of what a few of the optimizer passes do and how to use the tools to see the effects