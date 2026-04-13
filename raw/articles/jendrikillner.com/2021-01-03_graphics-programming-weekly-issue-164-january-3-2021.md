---
title: Graphics Programming weekly - Issue 164 — January 3, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-164/
author: Jendrik Illner
published: '2021-01-03'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video tutorial explains the fundamentals of texture mapping in ShaderToy
- describes how to apply a texture map to a 3D cube, sphere using tri-planar mapping
- additionally describes how to animate a second texture set onto a sphere as well as displacement mapping

![](../../assets/f3b7f3b24139199f.png)


- this Unity tutorial aimed at beginners presents a starter guide for compute shaders
- shows how to convert CPU based random cube generation tp GPU
- demonstrates how much quicker even a simple GPU based version can be

![](../../assets/6a09efb6943ff781.png)


- the paper presents a new technique of on-the-fly quantization for unorganized sets of unit vectors
- approach detects groups of windows that are then uniformly mapped onto the whole sphere surface before unit vector quantization is applied
- the presented technique can archive better results than octahedral quantization with only 16 bits

![](../../assets/fc3db414f99af7bc.png)


- tutorial series about creating a custom scriptable render pipeline in Unity
- decoupling the render resolution from the target resolution to allow variable resolution at runtime
- presents how to deal with post FX and the difference between upscaling with different color spaces

![](../../assets/46cb3768be718d7b.jpg)


- the Unity tutorial provides a starting point for how to use tessellation shaders
- example shows to tessellate a simple terrain

![](../../assets/e181de3978239285.png)


- collection of articles that provide a breakdown of various games
- contains links from analyses since 2015 from multiple authors

![](../../assets/3254c267b6e81b27.jpg)


- the article shows the steps required to use star databases to enable the correct rendering of stars
- covers data parsing, dealing with different time reference frames, color conversion
- provides sources and code for the implementation

![](../../assets/f06686e6b9c88cf9.png)


- Collection of impressive screenshots from Games (mostly PC, a few from PS4 Pro)

![](../../assets/d3ea7644cef01269.png)


- the paper presents an implementation of a hash-based Owen scrambling for Sobol sampling with nested uniform shuffling to enable multidimensional padding
- presents practical considerations for use cases and provides an example implementation

![](../../assets/3fd3b16c9ceb3775.png)

Thanks to Dirk Dörr for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.