---
title: Graphics Programming weekly - Issue 274 - February 12th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-274/
author: Jendrik Illner
published: '2023-02-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper proposes an expansion of Horizon-based indirect illumination by using visibility bitmasks instead of horizon angles
- stores (occluded / un-occluded) of N sectors uniformly distributed around the hemisphere slice instead
- meant to improve results for thin surfaces

![](../../assets/8eb17c00531bfca7.png)


- the post provides a walkthrough of how to implement raymarching for volumetric clouds
- provides an implementation using shadertoy
- additionally discusses further issues and further steps

![](../../assets/5707e7312af2c41f.png)


- the short tutorial shows how to recreate photoshop blend modes using GLSL shader code
- contains a link to a GLSL implementation of additional blend mode implementations

![](../../assets/0a7f06d87c2d2976.png)


- the article presents how to implement a software triangle rasterizer
- discusses how to evaluate if pixels are inside a triangle
- covers how to deal with edge cases, how to improve constant precision through the use of a fixed-point number representation
- additionally presents performance optimizations

![](../../assets/40fb25a4cb81f98c.png)


- the tutorial explains the basics of compute shader usage with Vulkan by implementing a compute-shader-based particle system
- shows how to load compute shaders, bind resources and interact with graphics resources
- additionally covers how the hardware executes compute shaders by explaining concepts such as workgroups and invocations

![](../../assets/c5183518dbb6b4de.png)


- a collection of tech art tweets covering topics such as procedural modeling, volumetric motion blur, skin shader, VFX and visual shader WIP reports

![](../../assets/f5a874829557b993.png)


- the video tutorial explains how to apply textures to a terrain system
- provides a recap of texture mapping techniques and how to apply textures based on the height of the terrain
- expands upon the techniques to tile texture across the terrain
- additionally shows how to use mipmapping and how it improves the quality of the results

![](../../assets/a4acb2440bbef4ba.png)

Thanks to Wiktor Czosnowski for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.