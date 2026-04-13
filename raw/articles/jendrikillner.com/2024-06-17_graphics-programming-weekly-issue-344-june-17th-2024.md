---
title: Graphics Programming weekly - Issue 344 - June 17th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-344/
author: Jendrik Illner
published: '2024-06-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the talk presents the system used by EA’s Frostbite team to test the rendering engine
- shows an overview of the current state of the system and why they are the way they are
- discusses all the complexities and difficulties
- shows the tooling available and how different tools exist for different use cases
- additionally discusses trade-offs and development approaches

![](../../assets/63b2210a699d7fc0.png)


- the video explains the concept of a BVH (bounding volume hierarchy) and presents how it increases the performance of a raytracing implementation
- shows a detailed explanation and many visualizations of the behavior of the data structure and how to build an efficient implementation
- presents different heuristics that can be used to order the data for efficient access
- shows the results and presents performance improvements

![](../../assets/ad6d2415118c4188.png)


- the article provides an interactive walkthrough into the implementation of the Raymarching algorithm
- explains the logic of signed distance functions in 2D and expands these to 3D
- presents the implementation of a simple 3D raymarching scenes
- the provided code samples are interactive and can be used to get a better understanding of the presented techniques through experimentations

![](../../assets/e802f0edcc3915df.png)


- the second path of the math tutorial series from GDC 2024 extends the dual quaternion knowledge (see last week 338 for prerequisite)
- starts by developing an intuition for plane representation (normal + distance), difference between positions and directions, and behavior under reflections
- additionally explains the understanding of homogenous concepts

![](../../assets/22be76d8b99c4d8c.png)


- the presentation presents updates done to the rendering pipeline of the internal engine used for Alan Wake 2
- focuses on explaining the technique selection and why the choices were made
- in-detail discusses the meshlet geometry pipeline and changes to the material system
- additionally discusses updates on the used transparency models

![](../../assets/5e0266b8f9a4131b.png)


- the video recordings of Noise and Reconstrictions papers from I3D have been released
- covers FAST: Filter-Adapted Spatio-Temporal Sampling for Real-Time Rendering, Filtering After Shading With Stochastic Texture Filtering, and Cone-Traced Supersampling for Signed Distance Field Rendering

![](../../assets/57015a762e38a47e.png)


- following the REAC 2024 conference, this author composes his 10 predictions on how graphics engine architecture might evolve
- looks back at the history, current developments and looks into the future
- additional discusses how mobile requirements vary and how it might indicate a future on consoles and PCs as well

![](../../assets/3c47f1a91859966a.jpg)

Thanks to [Graham Wihlidal](https://www.wihlidal.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.