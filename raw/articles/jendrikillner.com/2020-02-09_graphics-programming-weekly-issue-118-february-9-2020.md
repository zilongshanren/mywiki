---
title: Graphics Programming weekly - Issue 118 — February 9, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-118/
author: Jendrik Illner
published: '2020-02-09'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article shows what needs to be considered when baking normal maps for use with separate applications
- it shows what kind of different conventions exists, what common artifacts look like and how to verify that the content pipeline is correct

![](../../assets/7391d1ce9ea0deea.png)


- the article shows a connection between “2D cross product”, Complex Numbers and 2D rotation matrices

![](../../assets/14eb680a06bd740a.png)


- the tweet shows an alternative formulation for a normal transformation matrix (required when non-uniform scaling is allowed)
- the technique uses less memory but more ALU

![](../../assets/d482cdfbb175c83e.png)


- the Unity shader breakdown explains how to dissolve a mesh using a combination of noise and height based effect

![](../../assets/115078244a2e7834.png)


- Siggraph presentation showcasing a shadow system that enables thousands of shadowed-lights in large environments
- uses a fixed size shadow map pool, each light allocates it’s the target size
- splits dynamic and static shadows, using conservative filtering for the highly sparse dynamic shadows
- presents several techniques for compression, filtering and an overview of performance

![](../../assets/82b0f06bc529a323.png)


- the article presents an overview of the Wave Function Collapse algorithm
- a tile-based algorithm for the generation of procedural structures

![](../../assets/ba1fdc9b178250e1.png)


- the article presents a comparison between techniques to solve the harsh shadow terminator problem
- offers comparison images in different situations and with and without normal mapping

![](../../assets/158fadef71242fbd.jpg)


- the article shows a breakdown on how to approximate subsurface scattering from a point light using Spherical Gaussians
- presents why spherical harmonics are not a good fit to approximate point lights

![](../../assets/96e1c03ae0934ed8.png)

Thanks to [Steven Cannavan](https://twitter.com/pedanticcoder) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.