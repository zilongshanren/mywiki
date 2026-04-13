---
title: Graphics Programming weekly - Issue 175 — March 21, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-175/
author: Jendrik Illner
published: '2021-03-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a Geometric glint anti-aliasing method that is compatible with LEAN mapping
- this is archived by using mipmapping on the tabulated slope distribution function (SDF) of the microfacet BRDF
- a slope correlation coefficient is additionally introduced to make it compatible with normal mapping

![](../../assets/1332eae474ea3003.png)


- the article provides an overview of the first steps required to implement screen space reflection into an OpenGL based renderer
- shows what artifacts can be expected and what the author tried to improve but didn’t work out

![](../../assets/eef95dd0d5c56416.png)


Deep Silver Dambuster Studios is looking for a Rendering Programmer to join our Engineering Department to work on our high-end graphics pipeline.

You will be contributing towards the development of the upcoming AAA title, Dead Island, using Unreal engine.

For this role, we are looking for a regular level programmer (two years’ experience) or a very strong graduate with relevant qualifications and interests.

Experience with DXR and compute are a must, as you will be heavily involved in raising our visual bar on high-end platforms using the latest rendering technologies.

![](../../assets/18e544060e1c2609.jpg)


- the article provides an introduction to Compressive Sensing
- presents the basis of the underlying theory that allows the reconstruction from a limited set of data point
- explains the fundamentals of the frequency domain

![](../../assets/c71f4127b2c90cd8.png)


- the article describes provides a brief overview of AutoHDR
- the feature allows SDR games to be transformed to HDR transparently to the underlying game
- additionally shows how to enable a split-screen feature that will render the game with SDR one half and HDR for the other

![](../../assets/37e634576d12274b.png)


- the video tutorial shows how to change grass to cast shadows using Unity
- this presents how to generate double-sided grass geometry and output depth in the shadow pass

![](../../assets/cf20a908d68e781c.png)


- the blog post describes how blue noise can help to improve converge of ray tracing results
- explains how to transform white noise into blue noise using a compute shader (code provided)
- presents the limitations of the presented solution

![](../../assets/833bca387b6d769b.png)


- the tutorial aimed at Unity beginners explained how shaders are set up and structured
- additionally provides a brief look at visual shader creation experience in Unity and Unreal Engine

![](../../assets/d2504df63566e99c.png)


- the article series provides information about the role of color in data visualization
- shows what kind of scales exits, how different colors should be used and how the way data is presented provides a further understanding of the underlying data
- covers color scales, qualitative, quantitative, sequential, diverging as well as classed and unclassed scales

![](../../assets/979dbd930c744b7a.png)



- the article presents how soft shading for foliage was implemented
- using a combination of spherical normal generation and gradient remapping
- additionally covers how to add wind to the tree

![](../../assets/e5a944d5bc6f3a7c.png)


- the paper presents a novel approach to screen space ambient occlusion that accounts for occluded geometry through the use of a stochastic depth map
- Stochastic-Depth map is created through a global random that will discard pixels based on a tweakable cutoff value and store the results into separate samples per pixel

![](../../assets/6ef7d854597e05bf.png)

Thanks to Stephen Hill for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.