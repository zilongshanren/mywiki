---
title: Graphics Programming weekly - Issue 279 - March 19th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-279/
author: Jendrik Illner
published: '2023-03-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog post discusses designs and considerations for occlusion Culling techniques
- lists limitations of existing techniques for fully dynamic worlds
- discusses two prototypes covering screen-space depth reprojection as well as world space voxelization
- presents weaknesses of the techniques, open issues, and next steps

![](../../assets/616d6cbb8e414ff4.png)


- the article discusses the implementation of the GPUI library
- shows how to derive SDFs for rectangles and how to apply drop shadows using separable blurs
- additionally covers how font rendering is implemented by using the OS and GPU caching

![](../../assets/311d7170caf68c85.png)


- the Twitter thread discusses different methods to upload per-draw call GPU data
- presents how to use Metal, Vulkan, and WebGL 2.0
- additionally presents pointers on how to apply it for D3D12

![](../../assets/582e7b2bb6b739ea.png)


- the article presents different use cases of Fourier Transforms from a user perspective
- explains what to use them for and how
- presents strengths/weaknesses of the library design and how it affects the workloads

![](../../assets/f78cb8b5ea670620.png)


- the video tutorial explains the effect of iridescence, why it happens, and how to replicate it
- then uses the principles to implement a soap bubble shader using both Unity and Unreal
- shader implementation is shown using the Visual Shader language

![](../../assets/fb4e730f6efae96b.png)


- the article discusses how to implement a lighting model as found in the Legend of Zelda: The Wind Waker
- presents how to set up the blueprint as well as the shader logic required for the effect

![](../../assets/72e09ea184d657f2.jpg)


- the article discusses the basics of Convolutional Neural Networks
- the series aim is to explore the denoising implementation of the Intel Open Image Denoise library

![](../../assets/7507db198b5ff05b.png)


- the article shows how to implement SSAO using WebGL 2
- provides a high-level overview of the steps required and how to implement these
- discusses limitations of the technique as well as parts where forward and deferred shading paths would diverge

![](../../assets/c27be3ad78c8881e.png)

Thanks to [Joakim Dahl](http://www.plane9.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.