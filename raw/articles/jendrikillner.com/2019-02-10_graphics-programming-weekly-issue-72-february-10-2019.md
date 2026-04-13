---
title: Graphics Programming weekly - Issue 72 — February 10, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-72/
author: Jendrik Illner
published: '2019-02-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

This series can now be supported on [Patreon](https://www.patreon.com/jendrikillner).
Vote on the roadmap and monthly summaries for December and January are available as reward tier.

- presents how the RGB color representation is based on human vision
- shows how to visualize the visual color range in chromaticity diagrams
- presents the Rec. 709, sRGB, Rec. 2020 and XYZ color space
- shows which color ranges can and cannot be represented in each space

![](../../assets/1080be9521841666.png)


- Crytek removed all presentations from their website
- a user has uploaded a backup copy of many presentations to his dropbox

![](../../assets/e8538770be2d261a.png)

- presents how to optimize the compaction pass in a GPU culling pipeline
- reduce memory bandwidth usage by taking advantage of shared memory and compression of data that needs to be processed
- wrap level and shuffle instructions allow further optimizations

![](../../assets/6185f123fa92c236.png)


- shows how to simplify the math for constant time sphere indexing (the technique was described in issue
[64](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-64/)

![](../../assets/8405fd5c14e65c06.png)


- enables debugging of GPU hangs with D3D12 using Nvidia aftermath
- allows trace comparison
- Support D3D12 NVAPI Metacommand enabling
[DLSS](https://news.developer.nvidia.com/dlss-what-does-it-mean-for-game-developers/)

![](../../assets/4180bc0517e6dd17.png)


- presentations from Siggraph 2015 have been published
- Deus Ex: Mankind Divided presentations covers:
- shield and skin VFX,
- parallax occlusion mapping
- hair simulation and rendering
- motion blur
- color correction that allows changing the effect depending on the distance to the camera

- Rise of the Tomb Raider presentation covers:
- volumetric lights
- sunlight shadows
- ambient occlusion
- procedural snow deformation


![](../../assets/76bf4b158632d185.png)


- overview of improvements to the system that allows D3D11 applications to be run using D3D12
- improved threading behavior
- new APIs will allow the underlying D3D12 resources to be requested from the D3D11 objects

![](../../assets/d1ab53f487f29cd2.png)


- discusses author’s view on the state of low-level graphics APIs (Vulkan, D3D12, Metal)
- presents how the abstraction level might not be the right one
- too low-level for ease of use but too high-level to guarantee predictable performance on all platforms

![](../../assets/abf53096624cb000.png)


- every few days a new preprint article from the “Ray Tracing Gems” book will be released
- requires a free Nvidia developer account

![](../../assets/c5be1d2a72f0a991.png)


- part 2 of getting started with D3D12 for programmers with D3D11 experience, part 1 discussed in week
[70](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-70/) - shows to create vertex and constant buffers
- explanation of memory management and binding model

![](../../assets/2c86dd581e9d4608.jpg)