---
title: Graphics Programming weekly - Issue 307 - October 1st, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-307/
author: Jendrik Illner
published: '2023-10-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video shows how to sample texture lighting information stored in environment maps using importance sampling
- shows the underlying math for the different contributing elements
- also presents how to implement the technique using GSN Composer

![](../../assets/1a6c1e4641712f19.png)


- the article presents the basic steps for a toon shading implementation
- provides an overview of the different toon shading techniques
- covers toon ramps, cel-shading, lighting, and extensions such as shading ramps

![](../../assets/6d0755be01a43a6f.png)


- The paper presents a combination of Resampled Importance Sampling (RIS) and Projected Solid Angle Sampling (ProjLTC) for many area lights.
- provides a method of improving the efficiency run-time as RIS with a lower error
- shows the comparison between previous methods

![](../../assets/eb28df62e76fa0ec.jpg)


- the paper introduces a new approach to perform acceleration structure traversal and intersection tests against micro triangles texture space
- implementation is using nonlinear rays as degree-2 rational functions
- present performance and memory usage
- additionally discusses the effect of floating point precision

![](../../assets/633afaab3ca8e0e8.png)


- the blog describes how to compress the Gaussian splat SH data by using clusters and color palettes
- shows the effect on memory usage as well as quality

![](../../assets/1fa75065eb18cd3f.png)


- the article provides an in-depth discussion about how WebGPU is implemented within Chrome
- shows how the different implementation layers communicate
- presents a look at bugs found during the research process and possible attack surfaces

![](../../assets/6826e64b32ff3089.png)


- the blog post describes the importance of considering the total runtime when calculating performance characteristics
- discusses how failing to do so can skew the results towards a more positive conclusion

![](../../assets/f0de35b584db4107.png)


- the article provides a brief overview of the FSR algorithm implementation
- discusses how the frame generation interacts with the underlying native APIs as well as the state of the UE5 plugin integration

![](../../assets/e414e6656ac998d3.png)

Thanks to [Panagiotis Tsiapkolis](http://panagiotis.tsiapkolis.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.