---
title: Graphics Programming weekly - Issue 336 - April 21st, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-336/
author: Jendrik Illner
published: '2024-04-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a method that allows existing non-differentiable rasterizers to be made differentiable
- explains the underlying technique and how to derive per-pixel stochastic gradient estimation
- shows how to use the concepts to implement a 3D assets optimization system

![](../../assets/dd8fa31c7de13933.png)


- the article introduces a specialization for the isotropic distribution of visible normals for GGX-Smith
- discusses the limitations and implementation
- source-code for HLSL and GLSL is provided

![](../../assets/79f0e6e13ae43c07.png)


- a collection of summaries about color science aimed at computer graphics artists
- provides a summary of the physics of color, the human vision, as well as the representation in computer graphics
- additionally discusses color transformation onto displays

![](../../assets/e1fc905253c85609.png)


- the paper introduces an object space shading method based on per-half-edge texturing (Htex)
- presents a comparison against existing and shows how a Htex based method helps to reduce texturing seams
- implementation of ReSTIR GI in object space using Unity is provided

![](../../assets/c4b4aaa5656c245c.png)


- the video explains how to use OpenGL tessellation shaders to implement a dynamic level of detail for mesh based terrain system
- explains how to setup the data for usage with the shaders
- presents the shader and C++ code implementation required

![](../../assets/7b37122aa4938356.png)


- the video presents techniques to represent light shafts
- explains an overview of two existing approaches
- present an approximation technique that uses 2D planes combined with shadow map sampling and temporal filtering

![](../../assets/e3623b66c11a419b.png)

Thanks to [Joakim Dahl](http://www.plane9.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.