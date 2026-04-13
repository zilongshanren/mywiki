---
title: Graphics Programming weekly - Issue 187 — June 13, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-187/
author: Jendrik Illner
published: '2021-06-13'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper introduces an improvement for specular antialiasing
- normals distribution function (NDF) is filtered in orthographically projected space instead of slope space
- presents an approximation solution and provide source code
- additionally presents an isotropic NDF-filtering technique for deferred and forward rendering

![](../../assets/32cfa22274dfe477.png)


- Lumen presentations starts at
[10:00 minutes](https://youtu.be/QdV_e-U7_pQ?t=602) - presents what Lumen supports, what limitations exists
- shows an in-depth look at the implementation that uses hybrid tracing techniques
- looking at the scene representations, surface cache, and the different passes required
- additionally presents content examples, provides optimization advice, and answering user questions

![](../../assets/3d2c729fd7cbb76d.png)


- article discusses alternative approaches for geometry pipeline design
- moving more work into the pixel shaders, following the patterns of ray tracing shader
- presents performance comparison of the presented approach and limitations

![](../../assets/6d0623d3a7f2ced9.png)


- new podcast about VFX in film, TV, and games
- discussing Resident Evil Village and UE5
- how game technology is evolving and reaching a collision point between real-time and offline techniques

![](../../assets/26c30c88bb7da779.jpg)


- the video tutorial explains how to draw a line segment in pixel shaders
- shows how to derive the point to line segment formula
- additionally presents how to combine multiple lines

![](../../assets/722ae6917925dffe.png)


- the article presents a look at the implementation details of nanite GPU culling
- discusses how the compute shader cull on the sub-instance level
- shows how clusters are culled and the depth buffer from the previous frame is used

![](../../assets/48778982c13c8fad.jpg)


- the paper presents how to sample polygonal area lights proportional to linearly transformed cosines
- offers significantly reduced noise and unbiased diffuse and specular shading
- displays nearly noise-free results at 2 spp

![](../../assets/5e234076e763a0bf.jpg)


- the video explains the motivation for the bindless model and explains the concept
- presents how this can be expressed in metal using argument buffers
- explains memory residency and how this influences what resources can be used
- additionally explains what synchronization considerations need to be dealt with

![](../../assets/ca3ae3ad8ed5fcae.png)

Thanks to [Neil Bickford](https://www.neilbickford.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.