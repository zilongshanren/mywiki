---
title: Graphics Programming weekly - Issue 184 — May 23, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-184/
author: Jendrik Illner
published: '2021-05-23'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article provides an overview of authoring shaders in HLSL
- shows the building blocks of the language
- additionally shows how to integrate it into the different Unity systems

![](../../assets/dc38de59ab5c22ed.png)


- the article explains what Signed Distance Fields (SDFs) are
- how they are used and what kind of effects can be achieved from a single SDF texture
- additionally shows the implementation of the effects in Unreal visual shader graph

![](../../assets/c71d2581748e33fe.png)


- the video recording from the Siggraph 2018 has been released
- covering ocean foam generation, shallow water simulation, and flowing water
- cloud rendering based around geometric shapes, blurring, and pixel shading on the projected volumes
- how to generate and simulate the 3D ropes based around parabolics
- tentacle animation driven from exported vertex animation data, with runtime partial resimulation
- brief look at the lightning implementation based on L-Systems

![](../../assets/ba2bb06257d76f2d.png)


- the blog post presents the setup of a frame for VR rendering (Oculus Quest)
- presents the techniques applied for latency reduction

![](../../assets/71b6ba8d5de78fd1.png)


- the article presents how to distribute Monte Carlo errors as blue noise in screen space
- storing precomputed permutation with runtime retargeted seeds
- includes a compute shader implementation of the retargeting pass

![](../../assets/c5674dc721963acd.png)


- the post presents an overview of different rendering pipeline architectures (Forward, deferred, visibility, …)
- discussing the different trade-offs of the techniques
- additionally clarifies the choosing the proper techniques depends on many factors and need to be analyzed for each game/team

![](../../assets/bbcbef14d2329c44.png)


- suggests using a PCG hash function as default for GPU based hash/random functionality
- brief introduction to the techniques
- additionally provides a link to a paper that goes into more detail about various techniques

![](../../assets/1e735cc1e21d3e8a.png)


- the video explains how partial derivatives are calculated in pixel shaders
- theses partial derivates are used for UV level selection
- additionally presents for what kind of effects these functions can be used

![](../../assets/22e4b545eac2ddc7.png)


- the article presents an overview of Vulkan secondary command buffers
- clarifying what restrictions exist
- shows how the extension relaxes the restrictions and allows secondary command buffers to inherit the viewport state

![](../../assets/387ae406a2fc1817.png)


- Two Minute Paper presenting an overview of Procedural Physically-based BRDF for Real-Time Rendering of Glints (covered in the week
[150](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-150/)) - shows the different demo applications and how it compares against non-realtime techniques

![](../../assets/ee0a1993d5a6adc5.png)


- the author presents his learning about Gamut Clipping
- based on the Oklab color space
- additionally provides an interactive shader toy to allow experimentation with the technique

![](../../assets/7286bef8084ab772.png)


- the post presents a divergence-free noise generation technique (such as curl noise)
- the presented technique needs only 2 gradients (curl noise needs 3)
- shows how to optimize the technique and compares it to other noise types

![](../../assets/413db933aa24717d.png)


- the article shows how to compact DXR acceleration structures
- the process is run on the GPU over a few frames
- presents how the process works, what synchronization and lifetime factors need to be considered

![](../../assets/0fcc50ef59a8d4b0.png)

Thanks to [Joakim Dahl](http://www.plane9.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.