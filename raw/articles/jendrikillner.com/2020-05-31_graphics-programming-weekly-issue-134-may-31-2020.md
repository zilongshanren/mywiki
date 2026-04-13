---
title: Graphics Programming weekly - Issue 134 — May 31, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-134/
author: Jendrik Illner
published: '2020-05-31'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- A tutorial that shows a practical walkthrough on how to implement a path tracer in shadertoy
- focuses on the generation of renderings instead of physical correctness

![](../../assets/b93e583a927319a6.png)


- the articles present how the VRS (Variable Rate Shading) implementation was approached
- offers performance and quality considerations
- shows how the shading rate was adjusted dynamically

![](../../assets/f548d2158043ed6c.png)


- This Unity tutorial explains how to implement a Civilization VI style fog of war system
- shows how to render the hex grid, use a compute shader to generate visibility masks and combine all parts for the final result

![](../../assets/b7a2c031231a437e.jpg)


- the articles describe the design of the new geometry (import) pipeline of the Magnum engine
- the new design focuses on the reduction of load time and extra flexibility to handle any GPU understood format

![](../../assets/6454e3e91927e2f0.png)


- A global illumination system developed by Activision
- the system is based on a static light baking approach with runtime support for dynamically changing lights and geometry

![](../../assets/b37559aed85731dd.png)


- the articles presents different approaches on how to implement a ring progression effect
- compares rendering quality, anti-aliasing, performance, and setup work for each method
- proves Unity source code for all presented solutions

![](../../assets/7ccf989ad953ba06.png)


- authors notes on the Survey of Temporal Antialiasing Techniques talk from the Eurographics 2020 virtual conference
- discussing TAA, how it works, how different implementations compare, weaknesses and possible future improvements

![](../../assets/e9b49091443c29cb.png)


- the next part in a Unity tutorial series on the scriptable render pipeline
- this part adds support for point lights, Spot Lights, static light baking and per-object lights

![](../../assets/3b938491e9e80e58.jpg)


- the article explains how the GPU based picking system in “Our Machinery” has been implemented
- presented solution writes a small UAV from the pixel shader to record the closes picked object
- shows how to make sure that the closes object is atomically returned

![](../../assets/9afde8da92f0e761.png)


- the article shows how the portal rendering effect in The Witcher 3 has been implemented
- shows the Reverse engineered HLSL shader implementation

![](../../assets/9bb8c57639c35148.jpg)


- a GI algorithm based around tracing Virtual point lights (VPLs), converting clusters of VPLs into probability distributions and storing these into hierarchical trees

![](../../assets/41ddea1a681a3597.png)

Thanks to [Dominik Lazarek](https://twitter.com/Omme) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.