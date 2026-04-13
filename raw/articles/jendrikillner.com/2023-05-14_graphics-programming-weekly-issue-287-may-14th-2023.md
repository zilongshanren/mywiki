---
title: Graphics Programming weekly - Issue 287 - May 14th 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-287/
author: Jendrik Illner
published: '2023-05-14'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- AMD released a new research framework aimed at the rapid development of multiple rendering implementations in parallel
- The first release contains a GI implementation and a reference Path tracer

![](../../assets/350105078b706247.jpg)


- the article provides an overview of the Photon Mapping technique
- discusses the issues with ray counts from ray and path tracing methods and how photon mapping aims to reduce the number of rays
- developed to solve rendering caustics efficiently

![](../../assets/4aa4cd4f76a65a28.png)


- the paper investigates and presents the quality and performance influence of stochastic texture filtering
- stochastic texture filtering makes it possible to perform filtering outside of the lighting integral
- this could allow for the adoption of higher-order texture magnification filters as the introduced noise can be removed with temporal filtering algorithms

![](../../assets/9eb46145f5402500.png)


- the article provides a walkthrough of how to investigate a GPU hang found in Splitgate on Steam Deck
- shows how to narrow down the issue using Vulkan validation, the AMD open-source drivers, and UE source code access
- presents the complex interconnections of GPU systems

![](../../assets/3d7723a3ccd90ac6.png)


- the GDC presentation present a GI solution that aims to cache radiance into a cache hierarchy
- shows how the technique combines screen space probes with world space-level cells
- presents the implementation, quality, performance as well as limitations of the technique

![](../../assets/20111e4bdd18729a.png)


- the video tutorial expands on the terrain rendering series by adding support for calculating LOD levels for each patch
- shows how to implement the technique using OpenGL

![](../../assets/185fba1c57c7f16a.png)

Thanks to [Jan-Harald Fredriksen](https://twitter.com/jhfredriksen) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.