---
title: Graphics Programming weekly - Issue 312 - November 5th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-312/
author: Jendrik Illner
published: '2023-11-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- Nvidia released a sample that explains how to render Micro-Mesh using both the Vulkan extension and classical compute shaders
- presents how to read the necessary data all the way to render it
- shows how to rasterize and ray trace the data

![](../../assets/bdcce89df8d3cfc4.jpg)


- the blog post describes the first public release of the Open Physically-Based Rendering model
- the model is built upon MaterialX by Adobe and Autodesk
- the early release that is looking for feedback from the community before the final release in 2024

![](../../assets/5ceb890afdf3f227.jpeg)


- the article presents the story of the development of a cloud shader that uses raymarching to render a cloud space
- starts with raytracing, and the reformation of tracing density as the starting point
- from there, expand the example step by step to implement more advanced capabilities
- all intermediate stages are presented as interactive examples

![](../../assets/65bb64c4ca3f3ec4.png)


- the article discusses the implementation details of an efficient method to compute roots of Polynomial functions with high degrees
- presents an overview of the underlying method (Bracketed Newton bisection) and the implementation issues related to performance and precisions
- shows how to use Nvidia’s Nsight to identify the performance issues and how to resolve the register spilling problem to improve performance significantly

![](../../assets/88212009c85b6c2e.png)


- the blog post discusses the changes in the latest significant PIX release
- improved application performance, vastly improved raytracing debugging capabilities, and much more
- also lists breaking changes introduced in the accompanying WinPixEventRuntime

![](../../assets/98b3ece32e959692.png)


- the video shows the visual fidelity of the PC version of Alan Wake 2
- presents how the different levels of raytracing affect the visual results
- contains many insights into what limitations can be resolved with raytracing and what can still be improved
- additionally presents a brief look at the DSSL upsampling logic being used

![](../../assets/d4fe8fd08320b3ef.png)


- the video discusses the nature of hair and the aspects that make it a complex topic to reproduce
- presents how hair can be represented as shells and builds up the technique step by step
- additionally presents what issues the technique has and workarounds to reduce the visual impact of the limitations

![](../../assets/ec45ff78479a1841.png)


- the video provides a beginner-level view of how a camera orientation can be represented and transform vertices from the 3D world onto the screen
- explains the concept in OpenGL terms and shows the necessary library calls to create the matrix

![](../../assets/05c1c752f9ae2ef6.png)

Thanks to [atyuwen](http://atyuwen.github.io/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.