---
title: Graphics Programming weekly - Issue 183 — May 16, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-183/
author: Jendrik Illner
published: '2021-05-16'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article provides an overview of raytracing in rendering pipelines, how it has developed over time in the game development
- how it has been integrated into metro exodus
- shows the effect of the different components and how it affects the final rendering

![](../../assets/61b7de82905aeef8.png)


- the blog post discusses how to combine raytraced and shadows from shadow maps
- detect areas where shadow map resolution is too low to represent the edges and trace rays instead
- presents different methods, compares performance and quality
- additionally presents a summary and comparison against the AMD hybrid raytracing shadows technique

![](../../assets/1ab4d9b83b293862.png)


- the blog post presents a performance comparison of Naga (rust based shader translation library) vs. SPIRV-Cross in Dota2
- measures CPU time taken for shader translation in Dota2 from SPIRV to MSL (Metal shading language)
- takes around 1ms per shader stage

![](../../assets/7ac34fc09f842a74.jpg)


Remote from the USA or paid relocation to Montana (no work visa sponsorship)

Are you passionate about the outdoors? Want to combine that passion with your mobile graphics expertise?

We’re looking for a talented Senior Software Engineer with 3D graphics and mobile experience to help us take our off-pavement mobile GPS experience to the next level. [(more information)](https://www.onxmaps.com)

You’ll be our second hire on this new and exciting team focused on a greenfield, cross-platform 3D map viewer. You will work closely with our lead engineer on this project to create a beautiful and efficient 3D map viewing experience for millions of loyal customers.

As our second hire, you’ll work on our core 3D engine (written in C++) and serve as our mobile graphics subject matter expert.

If you’re a linear algebra wiz, love maps, have mobile development experience and can wrangle quaternions in your sleep, this job might be just what you’re looking for.

![](../../assets/6b7e27fba580c373.jpg)


- Radeon Rays v4.1 (ray intersection library for D3D12 and Vulkan) is now open source

![](../../assets/618f2741608926ba.jpg)


- the article discusses a technique for parallel processing of stack-based operations
- designed for a clip stack in the usage of a compute-centric 2D GPU renderer
- single-pass process with bounded memory usage within a thread group

![](../../assets/1b5af128c36dc553.png)


- the video presents an explanation on mipmaps, presenting what effects it has on the visual appearance
- explains how to use unity to automatically generate mipmaps
- shows how to generate custom mipmaps
- additionally provides some ideas on how to use custom generated mipmaps to achieve water caustics implementation

![](../../assets/5d1ae3154d3ad0ab.png)


- part 3 of the newton cradle tutorial series
- shows how to implement reflections using raymarching; this enables the object to be reflected in itself
- implementation is done using ShaderToy

![](../../assets/25f896ff7916afda.png)


- 4-minute trailer presenting a brief look at many papers that will be presented as part of SIGGRAPH 2021

![](../../assets/8d65d4f2252cd9c8.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.