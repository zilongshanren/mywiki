---
title: Graphics Programming weekly - Issue 342 - June 2nd, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-342/
author: Jendrik Illner
published: '2024-06-02'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a variance reduction technique for ReSTIR aimed at reducing shadow noise
- presents a comparison against existing methods
- discusses side-effects of the technique

![](../../assets/7e2e47308414c1c6.png)


- extended presentation of the I3D paper presentation discussed last week
- the paper presents an investigation into applying texture filtering after shading instead of before shading
- shows comparisons of the approaches and a background into the underlying theory
- presents guidelines on the tradeoffs and when to use different approaches

![](../../assets/c27f477d422acd35.png)


- the paper presents a way to reformulate SDS (a path with at least a specular, diffuse, specular bounce) paths into a polynomial system
- explains how to use root finding to solve the paths
- shows the presented solutions for caustics in a unidirectional ray tracer

![](../../assets/e7e8bb9feb601e3b.png)


- the article series extends the voxel rendering implementation to use path tracing
- discusses and explains the different components of the rendering equation
- additionally presents the effect of importance sampling for reduced convergence time

![](../../assets/9afee119afc9e591.jpg)


- the blog post explains the new DirectSR (Super Resolution) API
- provides a walkthrough of the API and how to integrate it into an existing engine
- provides an overview and discussion of the different exposed parameters

![](../../assets/8f2a428ac6fd2b17.png)


- the blog post introduces the ongoing work of implementing future HLSL versions directly into Clang
- discusses the expected difference between legacy and future HLSL versions
- additionally shows the first version of DXC compiled with clang and performance improvement

![](../../assets/64c6cac0dfac71ba.png)


- the latest version of Renderdoc includes a custom and improved DXIL disassembler
- additionally lists the improvements for SM6.6 feature support

![](../../assets/afaf4acd76e271ae.png)


- the paper presents a new method that aims to improve hair interpolation from a smaller number of guided hairs
- presents the theory and implementation of the technique
- compares against existing solutions in quality and performance

![](../../assets/4b411ba4859980b0.jpg)


- the blog post provides a high-level introduction to general relativity
- takes the underlying theory and shows how to convert it into code
- shows a C++ based implementation of the technique

![](../../assets/153836860f28b7ff.png)


- the blog post discusses the streaming system implementation in the Wicked Engine
- discusses how the data is provided, loading streaming processed in the background, and finalized for rendering
- additionally discussed techniques to improve streaming information, such as GPU streaming feedback buffers

![](../../assets/33ceeaaf16feaaa1.png)


- video of the I3D 2023 Paper session on Light Transport
- covers Bounded VNDF Sampling for the Smith–GGX BRDF, ZH3: Quadratic Zonal Harmonics and Interactive Rendering of Caustics using Dimension Reduction for Manifold Next-Event Estimation

![](../../assets/8d34f718690635b3.png)

Thanks to [Matt Pharr](https://pharr.org/matt) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.