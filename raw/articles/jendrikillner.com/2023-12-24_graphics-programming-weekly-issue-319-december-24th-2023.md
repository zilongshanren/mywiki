---
title: Graphics Programming weekly - Issue 319 - December 24th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-319/
author: Jendrik Illner
published: '2023-12-24'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog post is the beginning of a series covering mesh shaders and how they map to the RDNA hardware
- explains the classical pipeline and how the mesh shading pipeline differs
- presents which AMD hardware stages are used to implement the stages
- additional presents how amplification shaders can be used to represent dynamic workloads

![](../../assets/82827e173b0268dc.png)


- the article provides an in-depth look at understanding shader occupancy on RDNA hardware
- shows what occupancy is, what factors could limit it, and how to observe the actual occupancy
- presents how to improve occupancy
- additionally, it presents pointers to detect cases when more occupancy might not be beneficial

![](../../assets/03cc1975c8094ce2.png)


- the article presents techniques to help identify the performance cost of shaders created from unreal shader graphs
- shows how to see the generated instructions
- additionally, it presents a couple of examples to optimize the generated shaders

![](../../assets/1ded01e674691ce0.png)


- the article presents a shader function that uses wave intrinsic to calculate interpolation of the result of lane-dependent calculations across lanes
- shows step-by-step how the shader is structured
- additionally presents how to take advantage of SPIR-V inline to further improve the generated code

![](../../assets/2faf12fec2cf8183.png)


- the article provides an overview of the implementation of a render graph implementation
- presents how the implementation uses versioned resources to structure the order of render passes
- shows how the execution order of the render graph is established
- additionally, it discusses how unused render passes are removed

![](../../assets/6d7fc1cc500a51ce.png)


- the blog discusses the implementation of Vulkan video decoding to get the first frame of a video
- shows the steps necessary, from loading a file to unpacking the mp4 to actually decoding a first frame
- discusses pitfalls encountered along the way
- additionally, it presents a collection of other resources used to get to the stage

![](../../assets/8c5e7f5924558ae5.png)


- the paper presents a retelling of the Surface Gradient Bump Mapping Framework paper from the author’s perspective
- shows what normal maps are, how they encode information, and what the difference between object and tangent space is
- discusses issues with blending normals from different sources and how the alternative representation can achieve better-blending results

![](../../assets/f17f1804df8ad036.png)


- the blog post discusses how GPU-based animation for large crowds is implemented
- presents how the animations are structured, driven on the GPU, and acceleration structures for ray-tracing are generated
- additionally presents how skeleton instancing can be used to reduce animation costs while still allowing object variations

![](../../assets/b0f4efe69ecdc2b7.png)


- year-end video that discusses the standout graphical games of the year
- presents demonstrations of the effects of the game-nominated
- shows the top 3 picks for best-looking games of the year and presents the reasoning for the choices

![](../../assets/4db227e2864fe6da.png)

Thanks to [Lesley Lai](https://lesleylai.info) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.