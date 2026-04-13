---
title: Graphics Programming weekly - Issue 139 — July 5, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-139/
author: Jendrik Illner
published: '2020-07-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- a brief summary video of the “Monte Carlo Geometry Processing: A Grid-Free Approach to PDE-Based Methods on Volumetric Domains” paper
- presents how this paper connects to light transport and provides an overview of 6 examples and a look at implementations of the technique

![](../../assets/4a536f3b84b01d5c.png)


- the paper presents an importance sampling method that is based on wrap functions that approximate a single factor
- introduces how to use the technique with several existing techniques including projected solid angle sampling, glossy BSFDs, and others

![](../../assets/12a795fd6db9eeeb.png)


- an additional explanation for the previously discussed paper containing the implementation for a rectangular area light

![](../../assets/12a795fd6db9eeeb.png)


- the article provides an overview of the WebGPU API and shows the steps necessary to render a textured, spinning cube

![](../../assets/42e98a0b475e32cf.jpeg)

- the great in-depth article explains the concepts of light with many interactive examples
- illustrates the connection between the different units, explains connected concepts such as solid-angle
- additionally explains the relationship between reflections, shadows, and color

![](../../assets/4b3788ace192e35b.png)


- the paper presents a new technique that combines techniques caustics and glint into a single framework
- the presented technique combines deterministic root finding and stochastic sampling

![](../../assets/b049710dd5007b39.jpg)


- the paper presents a neural network upsampling technique that is aimed at 16x upsampling for real-time rendering
- the neural network takes advantage of additional information such as depth values and motion vectors

![](../../assets/a3fe7ee7ef06abf7.png)


- list of computer graphics conferences, dates and links to the stream as they are all virtual this year

![](../../assets/3d3ffd81cdb0902b.png)


- Unity tutorial that shows how to implement realtime shadows for point and spotlights using a custom scriptable render pipeline

![](../../assets/9f5c17b946660f46.jpg)


- the paper presents a taxonomy of the lobes that are composed to create a BSDF
- gives a hierarchical breakdown of the different models with examples for the different branches

![](../../assets/12b72effb62ace76.png)


- the article presents how to efficiently implement render-to-texture techniques using UE4
- compares the implementation using Slate and Canvas and shows why a slate based implementation is a lot quicker

![](../../assets/c0b0db747b7ac7d5.png)


- the articles show what screenspace shadows can add to the scene, provide an example of implementation, and show how noise can reduce banding

![](../../assets/dd5e4d497b4ae3bf.png)


- the article shows how to derive the intersection between a ray and a plane

![](../../assets/ca8c1f1939d4f5ec.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.