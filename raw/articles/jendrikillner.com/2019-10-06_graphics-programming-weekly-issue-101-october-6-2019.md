---
title: Graphics Programming weekly - Issue 101 — October 6, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-101/
author: Jendrik Illner
published: '2019-10-06'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- in-depth article that provides an overview of subsurface scattering techniques used for games
- presents the most common techniques found in games, Texture-Space Diffusion, Screen-Space Subsurface Scattering, and Pre-integrated Subsurface Scattering

![](../../assets/5db549f0fd73559d.jpg)


- the author provides an overview of problems that are encountered and make text rendering system very complex
- overview of terminology, overlapping glyphs, antialiasing, styling end emojis

![](../../assets/e53729b3444b11c3.png)


- presents a model to simulate erosion and transport simulation for sand due to wind
- the simulation can generate a large number of different dune types

![](../../assets/4e7f0d9a9cb9117c.jpg)


- the paper proposes the addition of a Traversal Shader stage to the DXR model
- this shader stage allows the programmable selection of acceleration structures
- presented use cases are stochastic LOD selection, choice of LOD levels based on ray type and improved multi-level instancing performance

![](../../assets/57379a607b3c65cf.jpg)


- the article shows how to use 16-bit floating-point types on PC hardware
- differences in handling between APIs and shader compilers
- only modern hardware supports native 16-bit instructions on PC

![](../../assets/68c2c2caba762aa9.png)



- the article describes the characteristics of Fractional Brownian Motion
- commonly used for the procedural modeling of nature

![](../../assets/a7c50f558fde257f.jpg)


- the article shows the precalculations steps that enable PBR rendering on mobile devices
- irradiance map from the environment, BRDF lookup table for Cook-Torrance model and prefiltered reflections map

![](../../assets/ba4172da5ab0a1a9.png)

Thanks to Sean McAllister for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.