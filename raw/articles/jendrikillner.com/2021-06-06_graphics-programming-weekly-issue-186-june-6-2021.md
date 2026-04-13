---
title: Graphics Programming weekly - Issue 186 — June 6, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-186/
author: Jendrik Illner
published: '2021-06-06'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- interview discussing the demo project, lessons learned, discussions about future directions, and many insights into the design considerations
- overview of nanite is starting at
[52:15](https://youtu.be/TMorJX3Nj6U?t=3135) - presents an overview of the system, hierarchical LOD cluster selection, data compression
- presents in-game debug views and further looks at the demo content

![](../../assets/201ae4e35413adb5.png)


- the article presents the fundamentals of the WebGPU API required to draw a colored triangle
- also provides an overview of the WebGPU Shading Language (WGSL)

![](../../assets/aabc483d5f707994.png)


- the talk provides an overview of compute shaders
- comparison of different technologies (Cuda, OpenCL, Compute shaders)
- shows the execution model, explaining common terminology, and hardware variations

![](../../assets/27e5aaf27ea1c38f.png)

- the article discusses the implementation of ray-tracing support into the open-source RADV driver
- discusses what RDNA hardware supports and how to emulate it without hardware support

![](../../assets/247db3a89e1f91cb.png)


- the blog post presents a history of sampling techniques, how it was used and how it changed over time
- presents different use cases, strengths, and weakness
- the author additionally provides a look at how the field might develop in the future

![](../../assets/996d1923d254d083.png)


We are looking for a Rendering Engineer with experience in developing high-quality, high-performance software: in games or otherwise.

This role will suit someone who is keen to take the next step forward in their career and in interactive tech. We are working on core immersive technology that spans the full range of XR, and this is an opportunity to help shape the future of spatial computing.

Simul is an established leader in real-time graphics middleware; the company’s customers include Bandai Namco, Microsoft Game Studios, Sony, and Ubisoft. In 2020, Simul won the TIGA 2020 Best Technical Innovation Award for our work on trueSKY, the leading real-time weather SDK. We have a culture of agile development focused on quality, performance and precision. We believe in equal opportunity and a diverse, inclusive and supportive workplace.

You will be:

- Researching and developing new immersive technologies,
- Working in an agile team,
- Finding and fixing bugs and performance issues,
- Profiling and optimizing CPU, GPU and network code,
- Representing Simul at technical and non-technical events, in-person and online.

The benefits Simul offers are:

- Flexible remote working,
- Regular salary reviews and career progression,
- 22 days holiday + bank holidays,
- Dedicated self-development time.

![](../../assets/ff7737dd6e745c46.png)


- the article presents how printf is supported in Vulkan Shaders
- what extensions are required, how to integrate them into the shader pipeline
- additionally shows how to actually print the messages in application code

![](../../assets/c1f53f6bcbf70550.png)


- the article provides an overview of compute shader terminology and how they differ between APIs
- how resources are bound, synchronization and memory models

![](../../assets/18c48393206087be.png)


- the article discusses continues exploration in compressing a set of textures
- presents how to use neural network for compression
- showing techniques that can be used to improve compression discoverability
- additionally presents ideas on how this can be further developed and used for other use cases

![](../../assets/bc6f32a42e6451d3.png)


- the video tutorial shows how to implement refraction into a shadertoy
- explains the index of refraction, how different materials create different effects
- additionally shows how to deal with rays that don’t leave an object

![](../../assets/7f43011f965b1c7f.png)

- the master thesis presents a SPIR-V based instrumentation framework
- shows how to use instrumentation to gather information about the execution of ray tracing shaders
- additionally presents RayScope, a system for the visualization of collected instrumentation data
- shows examples of problems that the system helped to identify

![](../../assets/a0c5a05c0f583a19.png)


- the article provides an analysis of the Nanite cluster algorithm
- presents how clusters are generated, hierarchical tree structure, and LOD selection
- shows where in the engine code the relevant code can be found

![](../../assets/60a83d41c4fe1921.png)

Thanks to [Steven Cannavan](https://twitter.com/pedanticcoder) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.