---
title: Graphics Programming weekly - Issue 93 — July 14, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-93/
author: Jendrik Illner
published: '2019-07-14'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- explains a renderer architecture that separates command generation from execution
- commands have an associated sort key that is used to determine the execution order
- shows how to handle materials, resource updates and some advice for debugging such a system

![](../../assets/8c5e93175795a93e.png)


- video recording of the i3D keynote discussed in detail in
[issue 88](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-88/) - additionally contains the QA that is not covered in the slides

![](../../assets/07043be808470a32.jpg)


- survey by the ASTC Khronos group to understand compression use in games

![](../../assets/b4ac5520406368bd.png)

- a paper about a new hair rendering technique
- the technique is a hybrid between strand-based rasterizer and volume-based raymarching
- example implementation is available
[here](https://github.com/CaffeineViking/vkhr)

![](../../assets/75bb02d6c10a9851.jpg)


![](../../assets/f0b694158c88fcc0.png)

- explains how to implement line lights
- using a Most Representative Point (MRP) approximation
- finds the point with the most significant contribution along the line and treats that as point light source

![](../../assets/06aab0a9fc49efc3.jpg)


- D3D12 motion estimation support exposes access to the motion estimation hardware found in supported GPUs
- resolved motion vectors are stored in 2D textures, ready to be used by other application stages
- the article presents the API

![](../../assets/e19e684f9f6b94d1.jpg)


- discusses a new renderer project aimed at providing a high-performance to enable ray tracing research
- split into layers to provide application logic, scene representation and actual render codes
- render codes are plugins that can be shared

![](../../assets/9e1ca1485a667537.jpg)


- shows how to compile the Basis command line tool
- use it to compress a texture
- and runtime code required to load it into a metal application

![](../../assets/d30d3e8c40c91a3e.png)


- the timing capture view now supports GPU workload visualization
- the article shows the different features
- overlapping GPU work on the same queue and on different queues can be visualized

![](../../assets/3415aacbb8aaf772.png)


- the article explains how to use the DXC compiler API
- compile a shader, shader reflection, and signing

![](../../assets/3102109f4862acbe.png)


- updated page with all raytracing related sessions, talks and papers from Siggraph 2019

![](../../assets/c67e9010dc7be227.png)

- Twitter thread about modern APIs
- strengths, weaknesses, opinions, and suggestions for an alternate design

![](../../assets/a44bf328e0ded60b.png)

Thanks to [Cort Stratton](https://twitter.com/postgoodism) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.