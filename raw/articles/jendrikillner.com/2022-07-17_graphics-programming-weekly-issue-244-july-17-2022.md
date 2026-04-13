---
title: Graphics Programming weekly - Issue 244 - July 17, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-244/
author: Jendrik Illner
published: '2022-07-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the GDC presentation covers how the grass is procedurally generated in compute shaders
- how vertex shader animates the blades and wind influences the shapes
- presents the LOD transitions, how shadows are processed
- it additionally covers how artists can control the effects

![](../../assets/83de0d3bc321f60c.png)


- the article presents a couple additional order-independent transparency algorithms
- provides a brief overview of Weighted Blended Order-Independent Transparency (WBOIT) as well as Moment based OIT (MBOIT)
- shows the influence of screen size, quality setting as well as render target formats on the performance of the techniques

![](../../assets/56bb6b9286df342d.png)


The Indie Stone, developers of Project Zomboid, are looking for AAA coders to join them on their quest for the ultimate zombie survival simulation.

The applicant would be in charge of maintaining and developing our game’s animation system for Project Zomboid using a custom built OpenGL engine, while also working with the animator to improve our output, systems and toolset. Initial tasks would deal with root motion, blending and masking – later moving on to integration of inverse kinematics and ragdoll physics.

The Zomboid team is small and have their fingers in a lot of pies, so there are many opportunities to get involved in other areas of the game too - depending on the applicant’s skillset.

Competitive salary and a prominent role in a tight, passionate team. Remote and flexible working, anti-crunch mindset.

![](../../assets/c1e70cae43ef992a.jpg)


- Nvidia presents best practices to achieve stable performance results on NVIDIA hardware
- it recommends not only using SetStablePowerState as it doesn’t lock memory clocks
- instead recommends using the NVidia-smi utility

![](../../assets/30c20e5d0b44a952.jpg)


- the video recording of the first day of the High-Performance Graphics conference
- covers temporally stable upscaling and denoising, variance-guided filtering for motion blur, as well as virtual blue noise lighting
- the recordings of the other days are available on youtube as well

![](../../assets/693dc3f610813f9a.png)


Double Fine Productions is looking for a full time graphics programmer to join its San Francisco based development studio. Having recently shipped the award winning Psychonauts 2, we are looking to expand our graphics and systems programming team to support the development of our future titles.

You will be responsible for developing rendering features, optimizing game performance and memory usage, and building low level systems on PC and Xbox.

Applicants should have a strong preference for working in a highly creative, innovative, and nimble development environment, where collaborating with design, audio, art, animation, tech, and other disciplines is standard.

![](../../assets/27034fe5c580ce80.png)


- the article focuses on the new capabilities added in shader model 6.7
- now supports integer border colors, dynamic programmable offset, as well as new quad all/any operations
- adds support for writing to MSAA targets via UAV as well as more relaxed uint castable texture formats (same idea as Vulkan, creation time list of allowed formats)
- it additionally adds support for raw gather instructions

![](../../assets/0c419cc616e800de.png)


- a new preview of the Agility SDK improves the enhanced barrier API support, significantly better debugging support
- as well as it allows Independent Front/Back Stencil Refs and Masks

![](../../assets/2c1e913b78f379ca.png)


- a brief summary of the main features of shader model 6.7 and what is supported by the new AMD pre-release drivers

![](../../assets/3d3fe2f62054fcdd.jpg)


- the video shows how to implement a custom material into the Rust-based Bevvy engine
- presents the necessary Rust and Shader(WGSL) code required to achieve the effect of a dissolving object

![](../../assets/032a0f1449bdeebb.png)

- the article presents a brief overview of techniques that can be used to upgrade a simple raytracer to generate results that converge quicker
- shows the effect of importance sampling and what possibilities exist

![](../../assets/5fa26705010644dd.png)


- the short paper presents the Pixar technique for Modeling Braids and Curls

![](../../assets/2bf63b89822080d0.png)

Thanks to [Jonathan Tinkham](https://zincfox.red) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.