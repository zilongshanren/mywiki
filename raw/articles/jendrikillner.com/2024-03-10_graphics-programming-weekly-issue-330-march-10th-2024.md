---
title: Graphics Programming weekly - Issue 330 - March 10th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-330/
author: Jendrik Illner
published: '2024-03-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents a method for efficiently calculating the Cumulative Distribution Function or CDF, for image-based lighting
- explains the underlying prefix sum algorithms
- shows how to improve the initial implementation for improved GPU performance
- the implementation is provided using CUDA

![](../../assets/4c9c7ab75c542590.png)


- the article provides a brief overview of the rendering engine architecture of the indie game Solar Storm
- presents how the systems are designed around immediate mode principles
- shows how the world is built up, shaders are created, and objects submitted for rendering
- additionally presents a quick look at post-processing and performance

![](../../assets/52739982caf939a1.png)


- the blog post provides a walkthrough of the author’s implementation of grass rendering using compute shaders + indirect draw
- shows how the instances are generated, animated, and culled, as well as how LODs have been added
- code samples are presented using Vulkan

![](../../assets/328220055a122114.png)


- the article presents how to implement screen space reflections using a single shader pass
- starts from a basic technique description and presents how to resolve common issues
- each step and improvements are visually represented
- the source code for a Unity shader is provided

![](../../assets/e991ff8d47bac006.png)


- the article provides an in-depth look at the Smooth-Minimum operator and its characteristics
- shows that many varieties exist, and they all have different strengths and weaknesses
- presents examples of all and discusses when to use the different variations

![](../../assets/80cbb9f4519905ad.jpg)


- the article provides an in-depth look at the hardware details of the Snapdragon 8+ Gen 1 GPUs
- shows the hardware design, compute throughput, performance, cache performance, and much more

![](../../assets/942e137586d2547d.png)


- the video tutorial explains the concepts related to GPU hardware detection
- shows how to enumerate connected GPUs, what capabilities they support, and how to pick the hardware that matches the application requirements

![](../../assets/faceaebe164e940d.png)

Thanks to [Cort Stratton](https://twitter.com/postgoodism) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.