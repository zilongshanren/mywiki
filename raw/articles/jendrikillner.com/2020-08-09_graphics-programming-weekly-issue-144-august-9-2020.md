---
title: Graphics Programming weekly - Issue 144 — August 9, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-144/
author: Jendrik Illner
published: '2020-08-09'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- Vulkan SDK release contains a graphics vkconfig tool to allow users to configure layer settings
- can be enabled to control which layers are active, filter error messages, etc
- the SDK now also contains Vulkan Synchronization validation and distributes the DXC compiler for PC, Mac, and Linux

![](../../assets/c695648529c762cd.png)


- the Unity tutorials show how to implement a fire effect using a camera facing quad with shader based noise to wrap a noise texture to create the look

![](../../assets/8e0a97f2b7365a00.png)


- the Siggraph 2020 talk presents the derivation of a point light attenuation that eliminates the singularity as the distance approaches 0
- achieves this by treating point lights as simplified spherical lights
- provides comparisons against other solutions

![](../../assets/7a7e2ef393f277cd.jpg)


- the article shows an overview of what vertex displacement mapping techniques are and how to generate data using Mudbox for use with Unity

![](../../assets/464de5e70a65c2f3.png)


- the article an overview of the complexities with Pipeline management in D3D12 and Vulkan applications
- showing why many AAA release include long shader compilation steps at application startup time

![](../../assets/6ed9a7a2245f0318.png)


- the article shows the theory of perspective projects and discuses perspective distortion

![](../../assets/e78202ea10144747.png)


- the Unity tutorial shows how to write a simple fullscreen heat haze shader an apply in the different rendering pipelines

![](../../assets/84169097a9cc2e49.png)


- the article provides at the authors work of the last 8 years
- this provides a great insight into how large scale engines evolve overtime to solve new requirements and improve

![](../../assets/50447a5328899675.png)



- this video tutorial shows how to implement an Overwatch magical shield effect
- a transparent material with pulsating energy effects
- the effect is achieved in Unity using the visual amplify node graph system

![](../../assets/b1eaf2b6db39e04e.png)

Thanks to Spencer Sherk for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.