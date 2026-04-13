---
title: Graphics Programming weekly - Issue 155 — November 1, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-155/
author: Jendrik Illner
published: '2020-11-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the second part of the blog post series covering raytracing implementation with compute shaders presents the results of splitting the acceleration structure into two levels
- presents an overview of the implementation, performance comparison
- additionally shows that two-level separation provides additional flexibility advantages

![](../../assets/b3e6921c4dd64e6d.png)


- Vulkan extension for Variable Rate Shading (VRS) has been released as
[VK_KHR_fragment_shading_rate](https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VK_KHR_fragment_shading_rate.html) - adds the necessary API and SPIR-V extensions

![](../../assets/6ca1132253988c8f.jpg)


- latest PIX update adds support for visualizing the GPU execution of command list from a single ExecuteCommandLists call
- adds support for showing the resources that belong to each descriptor in a heap

![](../../assets/e5c52d213f143d2d.png)



- the author presents an overview of his raytracer setup
- explains the problems encountered and the current state
- provides an overview of how to trace the Ptex textures on the GPU

![](../../assets/5bc4b75bdd490918.png)


- the Unity article explains how to integrate multiple cameras into a scriptable render pipeline
- shows how to use it for split-screen, overlay camera (including correct blending), and in-game UI
- additionally shows how to filter objects for one viewport

![](../../assets/fdcac5aac930e5a4.jpg)


- the shader tutorial explains how to stylized toon glass shader
- shows the breakthrough of the individual component and what they contribute to the final result

![](../../assets/f17e1ee386ddb1d1.png)

Thanks to [Angel Ortiz](https://twitter.com/aortizelguero) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.