---
title: Graphics Programming weekly - Issue 291 - June 11th 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-291/
author: Jendrik Illner
published: '2023-06-11'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the presentation covers the development story of the Far Cry shader system
- shows how over multiple games, the architecture was iteratively improved to solve the D3D12 transitions
- focuses on how the PSO design was approached by making all PSO information known during build time
- presents techniques to reduce PSO hitching by skipping draw calls, introducing optional variations, and allowing fallbacks

![](../../assets/8e19fd183fd90629.png)


- the talk covers how the author designed a new rendering architecture aimed at mobile hardware
- presents how an iterative API Design was utilized
- covering the resulting solution and reasons for the design decisions
- much in-depth advice to consider for the best performance in different mobile GPUs

![](../../assets/5fb874bb953f4eb5.png)


- the article presents how a LUT (Look Up Table) can be used to apply a color transformation to convert a daytime scene into a nighttime
- presents how to express a color transformation into a texture and how to apply it from a shader
- discusses implementation considerations and how to reduce color banding

![](../../assets/577f589e04627449.jpg)


- slides covering Screen Space Indirect Lighting with Visibility Bitmask
- presents how bitmasks are used to track visibility along the visibility horizon
- show how this allows you to handle objects with thickness better
- additionally shows performance and image results

![](../../assets/b5b002448dda7bd1.png)


- the blog post covers a high-level overview of topics covering Diablo IV graphics techniques
- discusses the guiding principles, the interaction with tech art
- shows how HDR enables an improvement in visual quality
- additionally provides an overview of resolution/refresh rates on consoles as well as graphics options

![](../../assets/cb19b08ab8b845e5.png)


- the presentation presents how to convert the D3D12 shader for use with metal
- presents a shader converter tool that converts DXIL into metal shader IR
- this tool also supports the conversion of tesselation shaders into mesh shaders
- additionally presents performance pitfalls and advice to bind resources to the pipeline efficiently

![](../../assets/0e0282fa41d40bcf.png)


- the 2-hour interview discusses the history of the development of Graphics APIs
- discusses the origins of APIs, how OpenGl and Direct3D came to be
- tradeoffs, design decisions, and many insights into the history of computer graphics

![](../../assets/88ebc079f216ef5c.png)


- the keynote presents an overview of the state of the art in neural rendering
- covering image reconstruction, texture compression, mesh simplification, and others
- presents a look at what might be coming next in research and open areas for further development

![](../../assets/2b47cd0f09797300.png)

Thanks to [Marius Horga](http://metalkit.org/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.