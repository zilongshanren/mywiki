---
title: Graphics Programming weekly - Issue 185 — May 30, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-185/
author: Jendrik Illner
published: '2021-05-30'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents an overview of the Nanite Rendering pipeline using RenderDoc
- shows how meshes are rasterized with adaptive cluster LODs
- pipeline is based around visibility buffers, presents how materials are handled and integrated into the GBuffer
- presents how a material depth buffer is used to speed up the material shading step

![](../../assets/e3edaa45ed4aea29.png)


- the paper presents an improved normalization for the Smith–GGX BRDF visible normal distribution function (VNDF)
- previous methods cause brightening bias because of the mismatch between shading normals and geometry normals

![](../../assets/010a5a8d7c97bbe4.png)


- the video tutorial shows how to implement the MIP selection algorithm using shader code
- shows the effect of texture bias and presents possible use cases

![](../../assets/d85b4955098266a5.png)


- the paper presents a new algorithm for the semi-regular quadrangulation of arbitrary input surfaces
- focuses on ensuring that all feature-lines are represented as patch boundaries

![](../../assets/83d1ae44b151063e.jpg)


- the article presents a proof of concept stage technique to render grass using a screen-space ray-tracing based technique
- shows how the entities are derived during the shading step from tracing into a grass area

![](../../assets/ab3b453571e0cf3e.png)


- introductory Siggraph class about ray tracing
- including an opening interview with Peter Shirley
- overview of rendering equation and 2d shadertoy implementation

![](../../assets/8ff87f16feebab88.png)


- the article presents triangle grids
- discussing what a triangle grid is, why to use them and how to use it

![](../../assets/220c1b11ccd23b7a.png)

Thanks to [Graham Wihlidal](https://www.wihlidal.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.