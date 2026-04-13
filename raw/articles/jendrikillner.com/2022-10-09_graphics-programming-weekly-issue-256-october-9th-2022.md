---
title: Graphics Programming weekly - Issue 256 - October 9th, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-256/
author: Jendrik Illner
published: '2022-10-09'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video provides a walkthrough of ray tracing fundamentals
- explaining the required concepts, such as BRDF and energy preservation, to understand the rendering equation
- discusses patterns that cause raytracing techniques to require a large number of calculations
- explains what the ReSTIR technique is and how it allows a significant reduction in the calculations required by taking advantage of spatial and temporal reuse

![](../../assets/f3a846acbf74e77e.png)


- the paper introduces a progressive technique to cache material evaluations at runtime
- presents the implementation details of updating a fixed-size hash table on the GPU
- additionally shows the performance of the method and presents the effect of different cache sizes

![](../../assets/5391e89b46ce0f05.png)


- the article discusses recent AlphaTensor’s discovery on matrix multiplication
- explains what the algorithm applies to and how it compares to existing techniques
- clarifies the performance results reported in articles

![](../../assets/8da60f2bc44f38ef.png)


- the Twitter thread summarises the real-time distance field generator used by AMD research work
- can maintain the scene representation in < 0.5 ms each frame

![](../../assets/00e845b13aef70f0.png)


Double Fine Productions is looking for a full time graphics programmer to join its San Francisco based development studio. Having recently shipped the award winning Psychonauts 2, we are looking to expand our graphics and systems programming team to support the development of our future titles.

You will be responsible for developing rendering features, optimizing game performance and memory usage, and building low level systems on PC and Xbox.

Applicants should have a strong preference for working in a highly creative, innovative, and nimble development environment, where collaborating with design, audio, art, animation, tech, and other disciplines is standard.

![](../../assets/27034fe5c580ce80.png)


- the paper presents a method to extend a mesh BVH with additional data so that it can be shared between multiple LODs
- presents how to store the fused BVHs
- shows performance and memory impact of using a different number of LODs

![](../../assets/642ac728536ed61b.png)


- the paper presents a method that combines distance field tracing with hardware ray tracing
- distance field generation is described in the “Real-time distance field builder Twitter thread” above
- describes when to choose between hardware ray tracing and where to fall back to distance field

![](../../assets/b44d2e14919c2ebc.png)


- a collection of Twitter posts about a large variety of tech artist topics
- breakdowns of techniques, tree animation breakdowns, and a showcase of effects

![](../../assets/04435afa9ccc0b32.png)


- the article presents an overview of ongoing Nanite developments the developer noticed in the UE5.1 preview
- appears to start adding support for programmable pixel shader evaluation to allow masked materials
- additionally, initial support for vertex modifications and existing culling limitations

![](../../assets/bd18e0b1a0f1b706.png)


- the blog post discusses a numerical method for fluid flow to simulate wind flow over terrain
- discusses the underlying theory and how to mathematically express the simulation
- shows how to implement the method using compute shaders in OpenGL

![](../../assets/7537e3efb7c76c14.jpg)

Thanks to [Denis Gladkiy](https://play.google.com/store/apps/developer?id=Piggybank+Software) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.