---
title: Graphics Programming Weekly - Issue 406
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-406/
author: Jendrik Illner
published: '2025-08-31'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- presents the Siggraph 2025 course collection on advances in real-time rendering techniques for games
- discusses latest advances in ray tracing, global illumination, and hybrid rendering pipelines for interactive applications
- Slides for most talks have been released

![](../../assets/39475bbdc4b7107b.png)


- presents a stochastic approach to tile-based lighting
- discusses probabilistic light sampling techniques that maintain visual quality while reducing computational overhead
- demonstrates implementation details for integrating stochastic methods with existing tile-based deferred rendering pipelines

![](../../assets/5a4443c23c52b561.png)


- presents techniques for implementing level-of-detail systems for grass rendering
- demonstrates the creation of grass impostors using custom shaders that replicate albedo, ambient occlusion, and normal maps without geometry
- shows how to implement smooth transitions between high-detail grass meshes and performance-optimized impostor representations

![](../../assets/5b5a5643aa6822cb.png)


- presents shader techniques for creating realistic metallic foil sticker effects using reflection and refraction
- discusses texture mapping approaches for simulating the characteristic rainbow iridescence of holographic materials
- shader code is included
- additionally contains a real-time implementation in the browser that allows experimentation

![](../../assets/b7e9eb4f35341ba6.png)


- presents techniques for transforming cubic voxel worlds into spherical geometries using quad sphere mapping
- discusses map distortion artifacts and how to overcome them for a Minecraft-like world
- provides visual explanations of the issues and how to resolve them

![](../../assets/b707e4621cb62660.jpg)


- presents the mix() function used for linear interpolation between values
- discusses practical applications, including color blending, texture transitions, and animation smoothing
- demonstrates various practical use-cases

![](../../assets/27402ad7ced61e55.png)


- video tutorial demonstrating how to use Microsoft PIX to analyze game GPU performance
- shows the necessary steps to set up the system
- presents a first brief walkthrough of a GPU frame in Unity and Unreal using PIX

![](../../assets/7ca9454b9f9b7921.png)


- explores strategies for maximizing GPU VALU utilization and overall throughput by identifying and removing bottlenecks
- discusses when to use different shader types (pixel vs compute) based on workload characteristics and hardware limitations

![](../../assets/482b07521c58173f.png)


- announces the Graphics Programming Conference tickets are on sale now
- Many sessions are also already announced

![](../../assets/6b92d6f0b862a605.png)


- presents a curated collection of programming newsletters covering various development topics (mine is included as well)
- discusses newsletters focusing on graphics programming, game development, and rendering techniques

![](../../assets/9c7aed5b5fcb687b.jpg)

Thanks to [Angel Ortiz](https://x.com/aortizelguero) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.