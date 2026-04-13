---
title: Graphics Programming weekly - Issue 265 - December 11th, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-265/
author: Jendrik Illner
published: '2022-12-11'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog post explains two new extensions that have been added to Vulkan to improve interaction with windowing systems
- applications can now better be sure when to release swap chains, clean up the deletion flow as well as added additional flags to open the opportunity for driver optimizations during swap chain resize operations

![](../../assets/b7026fd6136cc258.png)


- the in-depth article explains the mathematics behind the original ReStir and an in-depth analysis of why it works
- covers the preliminary knowledge required (Multiple)Importance Sampling, Sample Importance Resampling (SIR), Resampled Importance Sampling (RIS) as well, as Weighted Reservoir Sampling (WRS))
- uses the information to develop a mental framework for understanding ReStir (Reservoir Spatio-Temporal Importance Resampling), how it works and why it’s an unbiased technique

![](../../assets/0f22bb6f65057306.png)


- the article presents how to integrate a custom toon shading model into UE5.1
- explains the necessary C++ modifications and shader work to integrate it
- presents the complexity and limitations connected to the integration

![](../../assets/3a733e31c233a58c.png)


- the video presents a walkthrough of how to replicate a Truchet Weave pattern using ShaderToy
- covering how to define an SDF for a Grid, Truchet, or Weave pattern and combine everything for the final result

![](../../assets/f0b8b17ffcf67356.png)


- the blog post explains how to build a cumulative distribution function (CDF) to accelerate the sampling of lights in a real-time ray tracer
- explains the high-level concept of a CDF and shows how to implement this on the GPU
- presents how to optimize the implementation to better take advantage of GPU hardware and utilize wave instructions for further optimizations

![](../../assets/f5975bdf2af53e62.png)


- the detailed video explains splines and concepts derived/extended from these
- covering Bézier Curves and Bézier Splines, explaining the underlying mathematics and concepts
- provides an in-depth explanation of the concepts of continuity, yet again in a large number of contexts
- with this information, the video dives deeper into extended concepts such as Hermite Spline, B-Spline, NURBS, and color splines (to name a few)

![](../../assets/1665373e69c27d9e.png)


- the tutorial explains how to implement area lighting using OpenGL
- implements the “Linearly Transformed Cosines” technique as published originally in 2016

![](../../assets/8d85c23ab6f48330.png)


- the presentation focuses on how to approach the implementation of abstract code/math expressions to make it easier to work with
- presents the importance of breaking down more complex expressions into sub-expression and visualizing individual components
- shows the approaches by implementing randomized water puddle placement, a Gerstner Waves simulation, as well as using flow maps to displace water around obstacles

![](../../assets/c5f5aa523131c756.png)


- slides and videos for the Neural Volumetric Rendering for Computer Vision have been released
- covering the fundamentals of Neural Radiance Fields (NeRFs), how to apply them to Volumetric data sources
- additional presents existing challenges as well as a brief walkthrough of a NeRFs workflow

![](../../assets/9a34362d16711553.png)


- the article provides a detailed look into a frame breakdown from the Decima engine-powered Death Stranding
- shows how the frame is rendered in a large number of compute passes, showing what resources are used in each pass and how it’s combined
- includes an overview of a large number of post-processing effects and how they appear to be implemented and combined to create the desired look

![](../../assets/0086897d6bb05561.png)

Thanks to [Graham Wihlidal](https://www.wihlidal.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.