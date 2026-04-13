---
title: Graphics Programming weekly - Issue 99 — September 22, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-99/
author: Jendrik Illner
published: '2019-09-22'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents what kind of artifacts happen when reconstructing normals from world space positions
- suggests how to reduce the artifacts by selecting triangles that are most likely to have originated from the same object
- additionally shows how to use compute shaders and group shared memory to optimize the reconstruction

![](../../assets/7d3be5ce586c8a6d.png)


- the paper presents a method that allows SDFs to be combined with techniques such as linear skinning
- this is achieved by calculating a triangle mesh hull for the SDF, applying the transformation to the hull and using this to trace
- tracing linearly in transformed space follows a non-linear trace in untransformed space

![](../../assets/07385b5d663401a0.png)


- overview of what has been improved in the latest apple GPU architecture and metal
- sparse textures, what it is, use cases and explanation of how to use it
- rasterization rate maps, mask that allows defining non-linear mapping between virtual and physical render targets
- vertex amplification specifies which vertex calculations can be shared between multiple viewports and which ones are unique per viewport
- better argument buffers, allow access to 500k textures and multiple levels of indirection

![](../../assets/a65fb9968f51a02f.png)


- the paper presents a new scheme that allows selectively combining different Monte Carlo rendering algorithms
- allow the use of less computational complex algorithms for more straightforward light transport cases and more sophisticated algorithms for more complicated cases
- enables to reduce the overall amount of noise in the same render time

![](../../assets/05b6d817917644cb.jpg)


- the article explains how vertex shaders in “Our Machinery” engine is handled
- all vertex data is explicitly loaded in the vertex shader
- shows how a more flexible skinning variation can be implemented

![](../../assets/4db1376a1e144206.png)


Ubisoft RedLynx is a multiplatform game development studio located in Helsinki. Along with the hugely popular Trials series, we have developed and published more than 100 games and we are a passionate team of over 140 people of 21 different nationalities. We are seeking an experienced Graphics Programmer to join our core technology team in creating impactful game experiences

![](../../assets/4cfddfae173473e2.png)


- excerpt from the
[Siggraph talk](https://developer.nvidia.com/siggraph/2019/video/sig918-vid)talk - overview of the mesh shading demo
- culling implement in task shader
- frustum calling also is done in the meshlet shader stage, since only parts of the model could be visible on screen

![](../../assets/bda86da7f9098678.png)


- DRED can now include PIX markers
- additional string events can be attached to markers
- debugger extension has been updated to provide access to the information

![](../../assets/a5ec45fbead376e8.jpg)


- the presentation explains how lightmap baking has been implemented in
[Wicked Engine](https://github.com/turanszkij/WickedEngine) - how to ray trace with D3D11 compute and/or pixel shaders
- discusses artifacts, limitations, UV packing, texture formats, and filtering
- the resulting system is an object space shading system

![](../../assets/6b320aa49ec86a5f.png)


- Metaballs2 demo has been updated
- the demo shows how to use mesh shaders and now provides a compute shader fallback version
- allows switching between both implementations
- compute shaders require extra memory to store intermediate results

![](../../assets/e02542f1ea718d26.jpg)

Thanks to [Jon Greenberg](https://twitter.com/Jontology) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.