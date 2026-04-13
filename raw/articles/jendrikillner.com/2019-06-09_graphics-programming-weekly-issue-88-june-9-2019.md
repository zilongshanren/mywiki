---
title: Graphics Programming weekly - Issue 88 — June 9, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-88/
author: Jendrik Illner
published: '2019-06-09'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the presentation explains the stages a triangle is passing through while being processed for rendering
- starts with a brief look at the software layers
- provides more details on lower-level hardware layers

![](../../assets/2b480b84f9dcf12c.png)


- Windows Version 1903 adds a new variable refresh rate option
- enable VRR in older D3D11 games if the hardware supports it

![](../../assets/17f6c6faf750a0b6.png)


- beginner level explanation of the rendering pipeline for games
- explains how game worlds are defined, and models are converted into something that can be seen on the screen

![](../../assets/8375a50713f744af.jpg)


- explains what a Vulkan pipeline cache is, why developers want to use it
- presents best-practices

![](../../assets/b6bc08a84a9ceeda.png)


- keynote from I3D presenting the challenges modern open world games such as FarCry need to solve
- presents an in-depth case study for Multiscattering BRDFs & Area Lights
- research investigation, implementation combinations with other techniques

![](../../assets/f7ce1ce820a94689.jpg)


- part 1 of article series about Global Illumination
- overview of terms and concepts required to understand Global Illumination solutions

![](../../assets/78c0c02f2b2ef625.jpg)


- a paper about Dynamic Diffuse Global Illumination solution
- builds on the terms explained in the previous article
- presents an overview of the problems the technique tries to solve
- provides implementation details

![](../../assets/e346436d8cf735ce.png)


- collection of best practices and pitfalls when using Vulkan on Nvidia hardware
- many of the guidelines should apply to other hardware manufacturers too

![](../../assets/20855144aa4b1b90.png)


- the article presents a comparison between two different sampling strategies for environment maps
- tested on three environment maps with very different characteristics

![](../../assets/a87e47a96f40a275.png)


- presents an overview of what requirements need to be met on AMD to enable color compression on render targets
- and what causes DCC to be disabled
- look at barriers and copy queue usage

![](../../assets/110f31062c626d93.png)


- presentation with a collection of options and debug modes that help with debugging
- provide a safe mode to disable optimizations and use API validation layers
- overview of tools available and APIS to add more debug information

![](../../assets/725a0f4309d7484f.png)

Thanks to [Max R.R. Collada](https://twitter.com/maxandonuts) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.