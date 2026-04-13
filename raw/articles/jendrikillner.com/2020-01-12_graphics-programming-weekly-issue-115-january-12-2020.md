---
title: Graphics Programming weekly - Issue 115 — January 12, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-115/
author: Jendrik Illner
published: '2020-01-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article shows an overview of deferred shading techniques
- alternative structures and methods for optimizations are presented
- using compute shader for conservative rasterization for spot and sphere lights

![](../../assets/eaf592b9458f72d4.jpg)


- new release of AMD profiler that introduces a new pipeline overview view and adds new overlays for the wave occupancy view

![](../../assets/7d6876c605138ccc.png)


- the article shows how to use RenderDoc to identify issues and how to alleviate them
- most advice is not Occulus specific and talks about shader complexity, LOD, culling, and empty draws

![](../../assets/00adb812d8ff899f.png)


- a short Unity tutorial that explains inverse lerp function
- a function that given value in an input range returns a normalized 0-1 value
- additionally shows how to combine lerp and inverse lerp to allow range remapping

![](../../assets/42cfae9ab0b57a65.png)


- the latest Nvidia driver update introduce Variable Rate Supersampling for D3D11 + MSAA applications
- driver side implementation that allows games to render with higher quality in the center of the screen
- the article presents and compares MSAA and SSAA

![](../../assets/799ad4b912f18654.png)


- the second part of a shadertoy video tutorial
- the tutorial extends the scene to render multiple parallax layers of mountain ranges
- how to draw a moon

![](../../assets/cd12c27b2699de16.png)

- this video tutorial shows how to derive the signed distance field for a line segment

![](../../assets/2702bf4df571b391.png)

- next part in Unity tutorial series about the rendering of sand
- adds support for sparkling based on microfacets based on a texture with precomputed random values

![](../../assets/2d569f74497995d9.png)


- a brief summary of mipmapping
- shows how mipmapping causes details in glitter effect of sand to be lost in the distance
- proposes a manual mipmapping strategy where the texture coordinates are adjusted to keep a constant texel density

![](../../assets/4c32b86a5b6f5f30.jpg)


- the article presents how to write an outline shader for Unity
- uses color, normal and depth information
- implemented as a post-processing effect

![](../../assets/5b799618a403d7f4.png)


- the Unity tutorial shows how alpha to coverage allows improved edges on vegetation
- how to implement alpha to coverage into a shader
- shows how to adjust mipmap calculation to preserve small details with this method

![](../../assets/7eba42bf8ad92117.png)


- update to Vulkan database shows the first driver version an extension/feature has been introduced
- a more natural way to compare extension support across different platforms

![](../../assets/d0b70959d1cacb02.png)


- the article shows how to use the WebGPU API to implement everything required to render a colored triangle
- this includes shader loading, mesh creation and command generation

![](../../assets/b2bc061a0a95bcd2.png)

- Twitter thread about the authors’ recommendations about learning graphics programming

![](../../assets/1549609dd0e6ce71.png)

Thanks to Stephen Hill for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.