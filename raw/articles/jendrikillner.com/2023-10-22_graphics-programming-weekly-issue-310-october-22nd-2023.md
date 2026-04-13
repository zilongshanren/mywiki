---
title: Graphics Programming weekly - Issue 310 - October 22nd, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-310/
author: Jendrik Illner
published: '2023-10-22'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the in-depth article presents how to render a high-quality grid from a shader
- presents what issues occur when rendering lines commonly
- shows how to render anti-aliased lines that are free of these common artifacts
- code is provided for unreal and unity

![](../../assets/7e713171f53526ef.png)


- the article provides an overview of the methods available in UE5 to deal with Pipeline loading
- presents timings to show the effect of lacking PSO pre-loading
- discusses the new methods available and how to use them
- additionally presents what is still missing for a 100% fluent player experience

![](../../assets/5bee5bd7d8776c80.png)


- the video tutorial shows how to animate a flag using vertex shaders
- step-by-step presents how to develop the effect using Unity and Unreal Engine

![](../../assets/a9955986edfc2848.png)

- the paper introduces a method to reduce the amount of rejected rays for tracing rays following a visible normal distribution function (VNDF)
- the unbiased method improves variance for highly rough and low-anisotropy surfaces

![](../../assets/d5a94196a9ed6495.png)


- the article presents the white furnace test
- discusses what the purpose of the test is and provides a real-life example of the behavior
- additionally provides a ShaderToy example of the test and also demonstrates how incorrect sampling can be caught using the test

![](../../assets/e5abd1b380a111a8.png)


- the blog post presents how to set up a book with turnable pages
- shows how to create the art assets and shaders to enable the effect
- implementation is shown using unity visual shader graph

![](../../assets/592d6a607fd70308.png)


- the article discusses dynamic resolution scaling and its effect on memory usage
- presents findings of texture sizes/formats on Nvidia, AMD, and Intel GPUs

![](../../assets/ce6394005d29e0f6.png)


- the article presents three issues with linearly transformed cosine (LTC) Line Lights
- presents an improved routine that reduces the required usage of arc tangent calculations

![](../../assets/728f14509bc6120b.png)


- the blog post introduces the new automatic differentiation feature for the slang shading language
- provides an overview of how it’s integrated into the language
- presents a comparison between tensor and shading languages

![](../../assets/dc3ad785fa5e715c.png)


- the blog post discusses the implementation of WebGPU into the sokol-gfx library
- shows what issues had to be solved and how the author resolved them

![](../../assets/aebe57da67afc7d6.png)


- the article provides an overview of the tesselation pipeline
- explains how it fits into the rendering pipeline and what possibilities it enabled
- presents how to render cubic bezier splies using tesselation
- implementation is shown using OpenGL

![](../../assets/89f0f349af014604.png)

Thanks to [Warren Moore](https://metalbyexample.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.