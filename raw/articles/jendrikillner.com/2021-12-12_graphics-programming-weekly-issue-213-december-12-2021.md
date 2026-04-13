---
title: Graphics Programming weekly - Issue 213 - December 12, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-213/
author: Jendrik Illner
published: '2021-12-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a technique that performs reservoir-based spatiotemporal importance resampling in world space
- caches in the cells of a hash grid built on the GPU along the path vertices

![](../../assets/b7fb81524bf5943e.png)



- the article shows how to write data into an offscreen target and process it in a full-screen pass
- additionally provides a walkaround for missing multi-channel output

![](../../assets/ea9e8aa9b86cb4c6.png)


- Microsoft released the spec for the Enhanced D3D12 barrier API
- discusses the problems with the current API
- presents how the new API resolves these problems, expected behavior as well as open issues

![](../../assets/5324650dec7a94e4.jpg)


- the blog post provides an introduction to the new enhanced barrier preview for D3D12
- presents how developers can test the API at this time

![](../../assets/85731955ebfcce6e.png)


- the paper presents an analysis of multiple scattering BRDF models
- shows the microfacet distribution function is most important for smooth materials
- shadowing and masking term increases with roughness
- shows how a mix of lambert and GGX can approximate a large number of materials

![](../../assets/8d03a8c3ddb871fb.png)


- the article presents the new features released as part of the DXC update for December
- added support for templates, overloadable operators, bitfield members for data types
- additionally also introduces Operator Short-Circuiting as well

![](../../assets/7a851e7aca1863f3.jpg)


- the blog post presents the video encoding API that has been added to d3d12
- supports H264 and HEVC
- shows how the API exposes the hardware and fits into D3D12 design

![](../../assets/85731955ebfcce6e.png)


- the article presents an overview of tesselation shaders
- shows how to implement the necessary steps to implement drawing of a tesselated sphere using Metal

![](../../assets/006d2dfc7f146604.png)


- the article presents how to implement 3D mesh rasterization in a WebGPU compute shader
- additionally provides additional steps to get a better understanding of the implementation

![](../../assets/b1073253571460cd.png)

Thanks to [Mike Turitzin](https://miketuritzin.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.