---
title: Graphics Programming weekly - Issue 267 - December 25th, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-267/
author: Jendrik Illner
published: '2022-12-25'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog posts describes how Hierarchical Z-Buffer (HZB) Occlusion Culling uses a depth buffer to improve culling efficiency
- describes two possible solutions that can be used to solve the problem that a depth buffer of the view is required to accelerate the rasterization of the same view
- focuses on a technique that uses information about which objects have been visible in the previous frame to accelerate the current

![](../../assets/5c3e48391d0cf618.png)


- summary of two Siggraph talks by the author covering Ghost of Tsushima
- the talks cover Lighting, Atmosphere, Tonemapping as well as PBR Shading in Ghost of Tsushima

![](../../assets/c5c2e801bb28e48f.jpg)


- the post announces that the new edition of PBR will be released on March 28, 2023
[chapter 11 - Volume Scattering](https://pub-49ca6a23a58a46ef9cf5a5b34413a7ba.r2.dev/pbr-4ed-chap11.pdf)and[Chapter 14, Light Transport: Volume Rendering](https://pub-49ca6a23a58a46ef9cf5a5b34413a7ba.r2.dev/pbr-4ed-chap14.pdf)are available as PDF download already

![](../../assets/1300b72be9caed33.jpg)


- the stream covers the implementation and exploration of triangle culling into a GPU culling pipeline
- discusses trade-offs of different techniques and locations in the pipeline
- shows the effects of different culling techniques on the number of primitives that need rasterization

![](../../assets/708aacc737767194.png)


- Intel released a Path tracing workshop of 76 minutes of videos and ShaderToy exercises
- shows how to implement a ray tracer, the path tracer
- how to speed up the algorithms through the use of importance sampling

![](../../assets/2131631f2b92e37a.png)


- a new version of rust-GPU that allows Rust code to generate SPIR-V has been released
- this release adds support for raytracing
- additional contains many new APIs such as support for ByteAddressableBuffer or debug_printf

![](../../assets/a2aa52cdcd18d54b.png)


- the video presents how to implement Bezier Interpolation
- shows how curves are defined, visualizing how the factors are combined to create the final curve
- all implementations are presented in ShaderToy

![](../../assets/619eaa1e41d300f8.png)

- the article continues the series by covering an overview of raytracing techniques
- covers the Path Tracing Equations, Direct Lighting (single and multiple lights), Indirect Illumination
- Additionally covers high-level approaches such as Bidirectional Path Tracing and Metropolis Ray Tracing

![](../../assets/28ca1be8eb51bef4.png)


- the article presents metrics to calculate to judge the optimal size for meshlets
- compares the AMD and Nvidia limits to see how they might affect the choices

![](../../assets/c5527504d7a690a5.png)


- the video presents how to integrate a compute shader into the Rust-based bevy engine
- shows how to integrate the compute pass into the render graph system
- additionally shows how to read back simulation results back to the CPU

![](../../assets/4162b34069c11892.png)

- the article provides an explanation of deferred shading
- discusses the issues with forward shading and how deferred shading can solve them
- shows how deferred shading can be implemented, including techniques to reduce memory and bandwidth usage for the technique

![](../../assets/1a915daf7e128c95.png)


- the article presents how to use wave intrinsics to reduce the number of atomic operations required when compacting sparse arrays into packed arrays
- presented technique is based on FidelityFX’s SSSR implementation

![](../../assets/f1ca1d487957a8a5.png)

Thanks to [Vivitsu Maharaja](https://twitter.com/vivitsum) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.