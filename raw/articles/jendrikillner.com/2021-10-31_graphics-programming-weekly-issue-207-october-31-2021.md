---
title: Graphics Programming weekly - Issue 207 - October 31, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-207/
author: Jendrik Illner
published: '2021-10-31'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the videos for the excellent SIGGRAPH 2021 Rendering Engine Architecture course have been released
- covering Unity / Roblox / Activision rendering architectures
- as well as the Activision geometry rendering architecture

![](../../assets/8d30422be2de3c9e.png)


- the article shows that out of bounds access reduced rendering performance by 25x
- shows how to use NSight Graphics to help investigate performance issues

![](../../assets/fde345627262fa99.png)


- the article discusses the Binomial and Gaussians filter
- presents what a Binomial filter is and how it compares against a gaussian
- additionally provides details about how a Gaussian filter behaves with different kernel sizes

![](../../assets/55e023ecd0925c9f.png)


- the article covers a few high-level points on how command buffers allow parallelization of CPU rendering work
- provides best practices, and pitfalls to watch out for

![](../../assets/01f4ec4ce49da4ac.png)


- the blog post provides recommendations for memory management using D3D12 on
- provides information on how to receive information about the available budget and manage residency
- provides suggestions on which resource should be allocated together
- additionally provides information on tiled resource usage

![](../../assets/4556a66db684bdaa.png)


- the article provides information about what practices are recommended for getting good mesh shader performance and what are not
- additionally mentions how the Vulkan extension allows potentially less usage of shared memory

![](../../assets/70eab4bdc997fb39.png)


- short 1-minute video that explains how masking with disabled depth testing allows the eyebrows to be drawn above the hair at all times

![](../../assets/07e35b28e7f5763c.png)

Thanks to [Nathan Reed](https://reedbeta.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.