---
title: Graphics Programming weekly - Issue 347 - July 7th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-347/
author: Jendrik Illner
published: '2024-07-07'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video explains visually step-by-step how the Radiance Cascades technique aims to solve Global Illumination
- explains the underlying idea based on observations of linear and angular resolution
- presents results and also shows what the limitations are

![](../../assets/889db70a0f0f5774.png)


- X thread with a collection of Spatial Indexing Algorithms
- covers the pros/cons and what the techniques are typically used for

![](../../assets/343997608d2361f4.png)


- the video presents how the “Lossless Scaling” mod generates in-between frames for smoother game output
- explains that the mode only uses color output without any additional meta-data or motion vectors
- compares the technique against FSR 3.1 and DLSS 3.7

![](../../assets/598ca548e7fd42a1.png)


- the video tutorial presents how to create a signed distance field for a circle
- the implementation is shown using Unity and Unreal
- additionally presents a first overview of different shapes this series will be targeting to create

![](../../assets/e6bd47edf8c650e8.png)


- the keynote presentation discusses the Use.GPU technology
- presents issues of graphics technology and how the author aims to improve the authoring
- discusses how the React style has been applied to GPU app authoring
- provides a walkthrough of the implementation logic and examples
- shows how to compose shaders

![](../../assets/76642b50728d61be.png)


- the paper presents a new method to apply strokes to lines in a GPU-friendly way
- presents how to lower filled and stroked Bézier paths into an Euler spiral as an intermediate representation
- tests and shows the performance of the implementation on CPU and GPUs

![](../../assets/69231411a3b6e005.png)


- the paper introduces a unified BRDF that allows a consistent expression of smooth to highly rough porous behavior materials
- compares the results against ground-truth
- The presented solution might be approximated for real-time usage

![](../../assets/41ee6d3f986edad7.png)


- the blog post describes a couple of available shader intrinsics that allow the different threads of a shader wave to cooperate
- starts with simple techniques and increasing complexity

![](../../assets/e7512376e9a34ce9.png)

Thanks to [Jasper Bekkers](https://twitter.com/JasperBekkers/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.