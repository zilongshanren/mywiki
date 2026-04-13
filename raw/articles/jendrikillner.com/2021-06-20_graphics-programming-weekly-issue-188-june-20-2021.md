---
title: Graphics Programming weekly - Issue 188 — June 20, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-188/
author: Jendrik Illner
published: '2021-06-20'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a method for importance sampling linear lights such as fluorescent tubes
- rendering unbiased, nearly noise-free diffuse and specular shading by sampling a linearly transformed cosine (LTCs)

![](../../assets/aeb23774bd43e3d4.png)


- article describes how AMD Smart Access Memory allows applications full access to GPU local memory
- provides information on how the memory is exposed
- additionally provides performance advice on the usage

![](../../assets/38ebf0a3ae5b25cb.jpg)


- the article provides an introductory overview of HDR concepts
- covering color spaces, color primaries, Transfer functions
- presents the integration into our machinery
- additionally covers blending, precision, and other common issues

![](../../assets/aef99e4ba661d228.png)


- the paper presents a polarizing filter function for specularly reflected light
- support for direct and image-based light sources
- presents integration into Falcor rendering framework

![](../../assets/d2b0a407429317c3.png)


- the article shows an overview of new features and changes presented at WWDC21
- covering raytracing integration into tile memory, motion blur, shadows, and improvements to raytracing debugging
- additionally presents bindless binding, improved debugging tools as well as texture compression library

![](../../assets/db68e6b5f6dd0be1.png)


- the post shows how the Mali hardware operates and exposes multiple graphics queues
- presents how to run multiple graphics and compute workloads in parallel
- discussing performance and hardware considerations

![](../../assets/bedf66fc8e2ea4f5.jpg)


- the blog presents a comparison between color’s luminance and lightness
- shows that colors with the same luminance are perceived differently (The Helmholtz–Kohlrausch Effect)
- presents different models that can express this
- closing by presenting a few ideas the author thinks the models could be used to improve results

![](/img/posts/graphics-programming-weekly-188/LightnessHeader.png)


- the video presents an overview of all blend modes supported from the shader graph node
- shows the equation for each blend mode and discusses the effect

![](../../assets/e0ca581dc4c747bf.png)

Thanks to [Neil Bickford](https://www.neilbickford.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.