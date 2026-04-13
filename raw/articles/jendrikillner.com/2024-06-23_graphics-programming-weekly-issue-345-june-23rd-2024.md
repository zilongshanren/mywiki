---
title: Graphics Programming weekly - Issue 345 - June 23rd, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-345/
author: Jendrik Illner
published: '2024-06-23'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the GDC video presents a discussion of the new work graph features for D3D (also a Vulkan AMD-specific extension exists)
- explains the issue with the current ExecuteIndirect model
- shows an overview of the API model and how it aims to solve the challenges
- presents an overview of a compute shader rasterizer and a runtime GPU scattering system based on the technology
- additionally discusses the support level

![](../../assets/39b305ed8156233b.png)


- the first blog in a series about CPU optimizations
- this part presents how different implementations of max between floats can generate very different code
- presents the effect of branch misprediction on performance and how to use the AMD profiler to detect through hardware counters

![](../../assets/c22241cb9917512c.jpg)


- the video recording of I3D 2024 sessions covers the following papers
- Efficient Particle-Based Fluid Surface Reconstruction Using Mesh Shaders and Bidirectional Two-Level Grids, ShaderPerFormer: Platform-independent Context-aware Shader Performance Predictor
- Transforming a Non-Differentiable Rasterizer into a Differentiable One with Stochastic Gradient Estimation
- these papers cover a focus on performance from an academic focus

![](../../assets/437bf113448b08c2.png)


Grinding Gear Games are seeking experienced C++ Gameplay and UI Programmers to join our incredibly talented team. We’re after programmers to help design and implement gameplay and UI elements for Path of Exile using modern C++.

![](../../assets/c0f5d7d121e31f1a.png)


- the talk provides an overview of the experimental Triangle Visibility Buffer 2.0 implementation
- The presented approach uses only compute shaders to write the visibility buffer
- discusses the pipeline design, different approaches based on triangle sizes, and how performance compares
- additionally presents which features are still missing compared to hardware rasterization

![](../../assets/ca580409ae0c4f28.png)


- the paper presents a method that aims to unify microfacets and volumes for light transport purposes
- the paper shows that both can be expressed as stochastic implicit surfaces (SIS) and, more specifically, Gaussian process implicit surfaces (GPIS)
- discusses the derivation, representation generation, and tracing aspects of GPIS
- additionally discusses limitations regarding performance and quality

![](../../assets/3a6510920e1ea2b3.jpg)


- the blog post presents why the author suggests using box plots over bar charts as the default way to represent performance
- shows annotated examples of how box plots can express a lot of helpful information in a concise form

![](../../assets/844fed6c8d6c0f98.png)

Thanks to [Jon Greenberg](https://twitter.com/Jontology) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.