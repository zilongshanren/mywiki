---
title: Graphics Programming weekly - Issue 276 - February 26th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-276/
author: Jendrik Illner
published: '2023-02-26'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents an overview of 10 aspects to consider when approaching solving a computer graphics problem
- discusses the importance of understanding the working space, data representation, as well as time constraints
- presents how to take advantage of generic data science techniques (such as data visualization/exploration, Numerical optimization, …) to gain new insights
- additionally shows how ground truth and Machine learning techniques can be combined to develop an intuition of the limits of a given solution

![](../../assets/1e6cecf3d15c4e26.png)


- the talk describes to setup a bindless rendering pipeline using Vulkan, D3D12, and HLSL shaders
- shows how to set up the CPU side management to allow GPU side validation
- describes the emulations required for Vulkan

![](../../assets/c45d14f0f2ad4007.jpg)


- the article continues a series of understanding the Robust Monte Carlo Methods for Light Transport Simulation master thesis
- this article focuses on the understanding of multiple-importance sampling
- explains the insights required to better understand the balance heuristic especially

![](../../assets/3dc4c5aae64b96e4.jpg)


- the article provides a calculator that generates offsets and weights for a separable Gaussian blur filter
- allows the specification of a couple of settings (radius, sigma, filtering mode, …) and generates GLSL code
- explains the underlying logic and shows how to implement the filter in GLSL

![](../../assets/2847a5e6639e3ebc.png)


- the article describes the error handling techniques that are available when using WebGPU
- defaults will print detailed errors to the console, but developers can define scopes to collect information from the program and attach additional information to objects
- additionally presents how to collect detailed information from shader compilation errors

![](../../assets/b26d9a28aa8fa326.png)


- the official website collects the links to the videos and slides of the talks presented at the Vulkanised 2023 conference
- not all talks have slides at this time

![](../../assets/5bce2b4eaf26e852.jpg)


- the article presents issues with the ARM/mali GPU device IDs and how they relate to GPU performance for game setting tweaking
- shows how that reusing the same ID for multiple chips with large performance delta makes it challenging to identify capabilities correctly

![](../../assets/93be929fe410d7f1.png)

Thanks to [Aras Pranckevicius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.