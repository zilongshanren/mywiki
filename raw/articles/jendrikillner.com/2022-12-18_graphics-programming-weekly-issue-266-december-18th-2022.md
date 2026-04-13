---
title: Graphics Programming weekly - Issue 266 - December 18th, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-266/
author: Jendrik Illner
published: '2022-12-18'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- This article provides an overview of the Render Pipeline SDK design and implementation
- it shows how the SDK can reduce the complexity of render graph implementations
- presents that it’s able to manage resource barriers and transient memory
- additionally presents a demonstration of the performance effects that could be observed from real game workloads
- video version is available

![](../../assets/3379b8512b00fcda.png)


- the article provides an overview and history of raytracing
- it covers different styles of raytracing, common elements
- additionally provides a brief on how different phenomena can be simulated

![](../../assets/3877928f00e11e04.png)


- the video is the start of a new video series to render a height map using OpenGL
- shows how to load and render a terrain from a textural heightmap

![](../../assets/010f212d35940057.png)


- the video tutorial shows how to implement a shader in Godot that mixes two textures into a single material based on the normal directions of the mesh
- explains all the necessary vector space transformations, how to unpack normals as well as combine normals

![](../../assets/17a4d5626f88c7d2.png)


- the video discusses new features in Cuda 12 and a look at future developemnts
- covering Dynamic Parallelism (GPU side task launching), lazy loading to reduce load time and memory usage
- additionally covers updates to the CUDA compiler, math library updates as well as compability updates

![](../../assets/c129222b30878601.png)


- the article presents a technique to improve the look of a particle based fluid system
- uses Metaballs to more smoothly blend the particles together as well as simple Refraction model
- implementation is provided in GLSL for Game Maker

![](../../assets/729beb54a8db867a.png)


- the article explains how the oneAPI API can be used to target intel, nvidia and AMD GPUs
- presents a high level explanation of the technical implementation and goals for the future

![](../../assets/42c70e219ff63230.jpg)

Thanks to [Jon Greenberg](https://twitter.com/Jontology) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.