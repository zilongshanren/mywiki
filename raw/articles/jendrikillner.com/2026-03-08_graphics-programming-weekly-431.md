---
title: Graphics Programming Weekly 431
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-431/
author: Jendrik Illner
published: '2026-03-08'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- The article builds up PBR theory from the physics of light
- covers electromagnetic radiation, Fresnel equations, Snell’s law, and the microfacet model, distinguishing metals from dielectrics
- derives the Cook-Torrance BRDF step by step, including the GGX Normal Distribution Function, Schlick-GGX Geometric Function, and Fresnel-Schlick approximation

![](../../assets/8f48cb39c381507c.png)


- derives fog color lerp from the volumetric rendering equation
- extends the derivation to exponential height fog by computing optical depth for an extinction coefficient

![](../../assets/e0d06aee9053b46b.jpg)


- presents a VNDF-based micro-shadowing approach that operates at the microfacet level rather than the geometric surface level
- introduces a LUT-based real-time approximation parameterized by Visibility, Roughness, as a practical alternative to per-light VNDF sampling

![](../../assets/c92ddad6ac41b1e5.png)


- explains pipeline barriers as a combination of three orthogonal aspects: execution control, cache control, and image layout transitions
- details how image layouts abstract GPU-specific compression schemes such as fast clears, delta color compression (DCC), and hierarchical depth (Hi-Z)
- demonstrates that applications rarely need to track image layouts at runtime; instead, each image has a natural default layout derived from its purpose, requiring only temporary transitions to other layouts

![](../../assets/27c4eaa70a7a09bc.png)


- NVIDIA GTC is starting March 16
[attend virtually](https://nvda.ws/4aAcg3k)for free. - Presenting the latest breakthroughs in generative AI, accelerated computing, simulation technology, and more.
- My top sessions: OpenUSD Crash Course (DLIW82272), Fundamentals of GPU-Accelerated Workflows (DLIW82265) and
[more](https://www.jendrikillner.com/gtc-2026/) - Win an RTX Pro 6000 GPU and see my full session recommendations
[here](https://www.jendrikillner.com/gtc-2026/)

![](../../assets/49e4b5d359de08c5.jpg)


- describes a compute shader implementation that calculates lighting per-texel
- uses barycentric coordinates to map every texel from UV space to world space
- supports hard shadows and proximity-based dynamic blurred shadows via ray-triangle intersection tests, combining baked and real-time lighting passes into a final texture

![](../../assets/a06a0714835318f3.png)


- describes a Vulkan voxel spring-mass simulation for GPU-accelerated audio generation that requires a massive amount of dispatches
- resolves the command buffer recording bottleneck by recording a short reusable block, dispatches with VK_COMMAND_BUFFER_USAGE_SIMULTANEOUS_USE_BIT, and submits it multiple times

![](../../assets/2c669b988c199ecd.png)


- introduces Eyot, a programming language that aims to make offloading work to the GPU simple
- compiled for both CPU and GPU with the runtime automatically handling memory allocation, kernel compilation, and scheduling

![](../../assets/307e138fa9d6deee.png)


- beginner-friendly tutorial covering UV translation, scaling, and rotation inside Godot
- shows the effects of scaling UV coordinates
- demonstrates anchoring transformations to an arbitrary pivot

![](../../assets/20903bb2417c1fad.png)


- outlines idTech8’s new geometry pipeline for DOOM: The Dark Ages
- using a triangle visibility buffer approach
- evaluates multiple shadingdispatch strategies, and shares performance guidelines
- presents how the tiled deferred lighting algorithm supports software VRS

![](../../assets/4b35c52521b52f20.png)


- introduces the wedge product as the fundamental building block of geometric algebra
- showing how it constructs basis elements from which all multivectors are formed
- explains the three key properties of the wedge product and shows how they represent linear subspaces

![](../../assets/6bd81a74ce538604.png)

Thanks to [Matt Pharr](https://pharr.org/matt/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.