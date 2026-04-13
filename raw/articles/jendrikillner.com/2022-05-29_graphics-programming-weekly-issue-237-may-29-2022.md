---
title: Graphics Programming weekly - Issue 237 - May 29, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-237/
author: Jendrik Illner
published: '2022-05-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents how to use compute-shader based Variable Rate shading techniques to reduce the cost of raytracing
- shows how to decide on the shading rate per-tile
- compares a thread based rejection efficiency against wave-based rejection

![](../../assets/39c4b13591dc5afa.png)


- the article extends the BVH constructed over the last couple of posts to implement a more complete raytracer using it
- shows how to extend the barycentric coordinates to implement texture sampling and generate per-pixel normals
- it additionally shows how to implement reflections and recursive raytracing

![](../../assets/e3af7df5afbf9592.jpg)


- the detailed post presents the basis knowledge required for a single image deconvolution (remove blur) filter
- it discusses the theory, algebraic, and frequency domain approaches
- it additionally shows how to combine all the elements to create filters for linear deconvolution

![](../../assets/07851fc12b196bd9.png)


- the blog post presents that PIX is now supported on Arm devices
- additionally, Qualcomm added a plugin to allow hardware counter collection on many devices

![](../../assets/c4d7384e3e1db8ee.png)


- the video tutorial presents how to implement shadow mapping using OpenGL
- shows the necessary theory underlying the technique
- then proceeds to show the different aspects of the implementation
- additionally, it presents common problems of the algorithm and how to resolve them

![](../../assets/7d70c1296aca4e07.png)


- the paper presents the idea of the usage of a meshlet atlas for texture space shading
- the presented technique is based on meshlets and transforms per-meshlet information into texture space where shading for the samples will take place
- shows how to use meshlets as the basis for texture space management to use the available texture space efficently
- additionally compares quality and performance against other methods

![](../../assets/300f5ed0467651a9.png)


- the blog post describes the different methods WebGPU offers to upload data from the CPU to the GPU
- shows different use patterns and what the advantages/disadvantages of each method are

![](../../assets/6a358c4c9437f035.png)


- the article presents a frame breakdown of the PC version of Elden Ring
- shows the different passes, from color passes to post-processing, and finally UI composition

![](../../assets/a1e4b7cf8fcbf3ae.png)

Thanks to [Ken Russell](https://twitter.com/gfxprogrammer) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.