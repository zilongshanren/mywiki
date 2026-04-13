---
title: Graphics Programming weekly - Issue 340 - May 19th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-340/
author: Jendrik Illner
published: '2024-05-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents an investigation into applying texture filtering after shading instead of before shading
- shows comparisons of the approaches and a background into the underlying theory
- presents guidelines on the tradeoffs and when to use different approaches

![](../../assets/cd1b7a851831356a.png)


- the author presents his view on shading languages and the (lack of) evolution
- discusses the shortcomings and issues arising from them
- shows an outlook on why the concept of shading language is outdated and should be retired

![](../../assets/57777f9112f1c859.png)


- the paper introduces a path-guiding method that utilizes an irradiance voxel data structure
- the presented method is a spatial distribution
- shows an evaluation of static and dynamic scenes, containing quality and performance

![](../../assets/5263c60a59adbe93.png)


- the paper introduces Area ReSTIR that extends ReSTIR to be able to be applied to sub-pixel details
- presents how to allow the reservoir to integrate with the area for the lens and film
- shows the technique applied to depth of field and antialiasing

![](../../assets/9519b8a919fbe4c6.jpg)


- the article continues the series that covers the implementation of a voxel raytracer
- this week explains the concept of noise patterns and presents the effects using soft shadows
- explains white noise, blue noise, and stratification
- additionally, it shows how to temporally apply noise to allow temporal accumulation

![](../../assets/5b88b67eac83baba.png)


- the paper presents an improved version of a BSDF developed for micro grain materials
- shows how it explicitly models height-normal dependencies to summarize shadowing and masking inside the porous layer

![](../../assets/51ef224bb96c5bf5.png)


- the video presents how different types of noise for random number generation can affect the results
- discusses Randomness/fairness when generating random numbers
- present how different noises affect stochastic rendering techniques and suggest solutions to common problems
- discusses FAST noise generator utility and available pre-generated noise patterns

![](../../assets/48b7fa4d8c523d8c.png)


- the article provides an excellent overview of the different ways to create root signatures in D3D12
- starts with a brief overview of what a root signature is and how it’s used
- then discusses different methods to author, create, decompile, and use the concept
- presents a brief discussion on how root signatures are used and how other engines handle it

![](../../assets/4af59e1e9eb970c1.png)


- the article discusses how to implement cluster-based mesh rendering using mesh shaders
- discusses how to set mesh shaders using Vulkan
- extends the pipeline to use task shaders to execute LOD selection and frustum culling
- presents performance numbers and how wave utilization is essential

![](../../assets/6fe70730476b4fab.png)


- the paper introduces a new neural method to compress BVH for raytracing workloads
- shows how the technique is designed to be integrated into existing raytracing pipelines
- presents a comparison against existing solutions on memory and performance

![](../../assets/1ab389b90257caa0.png)

Thanks to [Angel Ortiz](https://twitter.com/aortizelguero) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.