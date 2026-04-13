---
title: Graphics Programming weekly - Issue 299 - August 6th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-299/
author: Jendrik Illner
published: '2023-08-06'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the presentation covers an overview of many rendering techniques used in Path of Exile
- these techniques cover a large number of topics, such as flow fields, decals, subsurface raymarching, bent-normal shadows, waves, and much more
- additionally presents details about a hierarchical probe system for GI that uses multiple hierarchical levels to approximate GI information with bounded cost

![](../../assets/5d69077ac8629ed8.png)


- the paper discusses the Shadow Techniques used by Final Fantasy XVI
- presents the Tiled Deferred Shadow implementation, performance, and quality results
- the paper discusses how the Oriented Depth Bias technique can be used to replace the traditional Hardware Depth Bias
- additionally, it presents debug visualization techniques

![](../../assets/152d35a10f4f5d74.png)


Rocksteady is an award-winning developer based in London, focused on combining character-driven cinematic narrative with genre-defining gameplay to create unforgettable experiences based on legendary IP. Growing our studio in London, our multicultural team takes inspiration from the culture and history of our home in one of the most diverse cities in the world.

We’re currently looking for an technical leader in rendering, to join our experienced team of game developers as we launch the highly anticipated project Suicide Squad: Kill the Justice League, and build exciting future plans.

![](../../assets/56e95fdd667ed0ee.png)


- the first part of a 3 part series that discusses occluding contour rendering
- first part discusses the issues
- the second part presents methods to efficiently generate smooth, sensible occluding contours from a triangle mesh
- and the final part presents suggestions on what techniques to use for which problems and an overview of open research problems

![](../../assets/f790e8f2821d286f.png)


- the article presents a discussion of functions calls in shaders
- covering issues with having and not having function calls
- discusses how CUDA and ISPC support functions pointers, but GLSL doesn’t
- presenting the costs associated and possible solutions

![](../../assets/c3a7d1e2ae893d43.png)


- the blog post provides an overview of leadership topics aimed at new graphics leads
- lists lessons learned and advice separated by categories
- covering Hiring, Day to Day actions, Performance Reviews, Advocacy as well as Self-Care

![](../../assets/ebf72c4a00522e76.png)


- The paper proposes an adaptive sampling technique for efficient Monte Carlo rendering with deep-learning-based denoising
- The suggested method estimates the variance of neural network outputs with random inputs to drive adaptive sampling methods
- When combined with denoising post-correction, it significantly accelerates error convergence during rendering

![](../../assets/f6967980f0949231.png)


- the blog post presents the rendering equation and derives the meaning by following the physical units used
- explains differences and relationships between the different units

![](../../assets/4349c905ae16a25d.jpeg)


- the blog post presents the idea of using decals to drive where post-processing and object-level effects
- discusses considerations when applying the decals and how to combine them with other effects
- presents how to use the technique for post-processing shaders and object-level vertex-displacement and alpha effects

![](../../assets/529c3f6a7f8fa004.png)


- the blog post presents the announcement of the formation of an organization for fostering the standardization, development, and evolution of USD to OpenUSD

![](../../assets/2c5acb863d359d61.png)


- the article has been updated with improvements
- covers efficient, conservative projected bounds for spheres as well as AABB
- presents the implementation and discusses the performance of the presented techniques

![](../../assets/2a927b9427429955.png)


- Nvidia presents the best practices for asynchronous compute queue work scheduling
- mentions how expensive workloads need to be to see an advantage
- additionally mentions patterns that should be avoided

![](../../assets/e96ded0ddc21c626.jpg)

Thanks to [Leonardo Etcheverry](https://www.linkedin.com/in/leonardoetcheverry/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.