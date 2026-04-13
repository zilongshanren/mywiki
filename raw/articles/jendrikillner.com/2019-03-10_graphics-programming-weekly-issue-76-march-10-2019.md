---
title: Graphics Programming weekly - Issue 76 — March 10, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-76/
author: Jendrik Illner
published: '2019-03-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- a new technique for continuous level of detail generation of point clouds, designed for VF applications
- additive point storage, each point is assigned to one level
- compute shader used to iterate over all points, time-sliced over multiple frames, and builds a new vertex buffer that only contains required points
- each point is classified into distinct LOD levels + a random factor, this makes it possible to allow the set to be changed continuously
- points have a blend zone to reduce aliasing, in this zone point sizes are adjusted so that they gradually are blended to the final extent as the camera approaches the points

![](../../assets/fce4ea5e6c905992.png)


- explains how the lightning effect in The Witcher 3 has been implemented
- based on a tree-like mesh that is expanded based on the normals and additive blending

![](../../assets/8d65395461958333.jpg)


- explanation of half-pel filters
- shows properties of different filters common in video compression and how they perform when applied multiple times
- common filters are “unstable” when executed multiple times
- the feedback loop causes the results to be oversharpened until the results become unrecognizable
- presents a filter that does not have a feedback loop problem and converges to a slightly softened but stable result

![](../../assets/4dc9c2d06dcb8ed4.png)


- survey about the Vulkan memory allocator library
- how it is used, how the experience is and what features are you used or are missing

![](../../assets/3b77d50723fb4362.png)


- getting started guide that shows how to use the bgfx library
- initialize the library and render a cube to the window

![](../../assets/2ea427ad2bad6fd7.jpg)


- overview of the state of graphics APIs in Rust
- presents wgpu-rs, a higher level API based on the
[WebGPU](https://www.w3.org/community/gpu/)API that is being designed for use in the browser

![](../../assets/420ea722a1f0de93.png)


- overview of particle system samples that have been created with the Visual Effect Graph in Unity
- including small video demonstrations of most effects

![](../../assets/b71c62d692b7ba5d.png)


- an unofficial updated version of Ray Tracing Gems with fixes for the errors found in the original book

![](../../assets/6d8e025f97f0ecfb.jpg)


- presents how to find a GPU crash on a low-end Vulkan device
- caused by a GPU driver timeout, requiring the work to be split into smaller submits

![](../../assets/609e9dabaf08c304.png)


- overview of all sessions AMD is involved with during GDC 2019
- will later also include links to the slides as they become available

![](../../assets/3be12d82581a82fa.png)

Thanks to [Aras Pranckevicius](https://aras-p.info/) for support of this series.

You would like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.