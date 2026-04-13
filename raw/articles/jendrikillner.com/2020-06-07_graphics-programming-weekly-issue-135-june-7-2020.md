---
title: Graphics Programming weekly - Issue 135 — June 7, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-135/
author: Jendrik Illner
published: '2020-06-07'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article discusses how to classify GPGPU work into the critical sequential work and the total amount of work done across all workers
- presents how this division is useful to talk and understand the performance of algorithms

![](../../assets/9c9a043407fab891.png)


- the article presents how RGBE 8888 should be encoded and decoded correctly
- explains the reasoning and shows how the encoding format works

![](../../assets/08d12081433f03a5.png)


- part 2 of path tracing implementation series, adding Glossy reflection Anti-Aliasing, tone mapping, and camera exposure

![](../../assets/04441a4a5e514044.png)


- Podcast episode with Arisa Scott (Unity), Eric Haines (NVIDIA), Mike Hardison (Blizzard Entertainment), Mohen Leo (ILM)
- discussing the evolution of real-time technology and upcoming techniques

![](../../assets/ae893a77b05a5e72.jpg)


- the article explains how to use to distribute points onto the surface of a sphere

![](../../assets/56a011f3e3d8e952.jpg)


- new Vulkan SDK now contains the Microsoft Shader Compiler
- GFXReconstruct is a new layer and tool that will replace
[vktrace](https://github.com/LunarG/VulkanTools), it allows recording and playback of Vulkan commands

![](../../assets/a0e3e7c54a7adcfd.png)


- this guide is designed to explain SPIR-V, what to use it for and present an overview of the internals
- additionally provides instructions for tooling and extension mechanism

![](../../assets/c4ab3ef36b18be41.png)


- Shader guide that explains how to write Unity shaders that are compatible with the Universal Render Pipeline
- highlighting differences between the built-in pipeline and Universal Render Pipeline

![](../../assets/824b5bc3874830d5.png)


- the article shows problems of floating-point precision in the model export pipeline

![](../../assets/f19173f6ba3bfee1.png)


- the presentation explains what Ambient Occlusion is, and provides an overview of different algorithms used to implement the effect

![](../../assets/b790debb15843e37.png)

- presents a method to implement a Cubism effect, similar to what can be seen in “Spider-Man: Into the Spider-Verse”
- provides a Unity implementation

![](../../assets/5c1e6d36aeb1610a.jpeg)

- the article presents Contrast Adaptive Sharpening and how it’s used in EVE to make details on ships and planet surfaces clearer

![](../../assets/9b55e8ee3b55903c.png)


- Unity tutorial that shows to mix Normal map correctly
- considerations to export normal maps to take the most advantage of the BC compresses precision

![](../../assets/7a21c6eb492e0bce.png)

Thanks to [Graham Wihlidal](https://www.wihlidal.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.