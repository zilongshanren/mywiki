---
title: Graphics Programming weekly - Issue 103 — October 20, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-103/
author: Jendrik Illner
published: '2019-10-20'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article describes how the architecture of mobile GPUs is different from PC
- shows why load/store operations have a significant impact on mobile
- present a demo application to profile the various load and store operation

![](../../assets/2d036cb32510f135.png)


- the tutorial shows the steps necessary to render a single triangle using the D3D12 API

![](../../assets/a4545f5e75ec236d.jpg)



- excerpt of Siggraph 2019 talk that proposes averaging of neighboring rays into cells
- using a jittered access + filtering to remove artifacts of discretization

![](../../assets/48211632abd137c5.png)


- the article shows how to use the Radeon GPU Analyzer to generate hardware native ISA disassembly, provide resource and register usage statistics

![](../../assets/462ce47ec811a503.png)


- the article describes a demo scene effect that uses a 2D height map on a flat 2D shaded object to simulate the appearance of 3D voxels

![](../../assets/d4276216ae40e8b1.png)


- next part of tutorial series shows how to extend a sphere tracing implementation in Unity to use the depth buffer correctly
- shows the necessary shader state changes and how to calculate custom depth output in a pixel shader

![](../../assets/2ea76c22888f0a41.png)



- part 1 of a Unity tutorial series about the sand rendering in Journey
- show visually the contribution of the different shading components

![](../../assets/4ce7f3b125b4eba4.png)

Thanks to [Michael Riegger](https://www.linkedin.com/in/michael-riegger-33b55a11/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.