---
title: Graphics Programming weekly - Issue 81 — April 21, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-81/
author: Jendrik Illner
published: '2019-04-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- explains how to create a layering parallax effect to simulate the inside of a marble using ray marching

![](../../assets/2663f86f4436207d.png)


- presents how memory, object lifetime and command buffers are managed
- resource lifetime is bound to a frame context
- frame context tracks which resources can be deleted once the frame has been consumed

![](../../assets/6d67be7cb094eb35.png)


- shows the Cooperative Matrix extension for Vulkan
- the extension enables matrix multiplications to be computed across a subgroup
- enables better shader optimizations and allows the use of tensor cores on Turing GPUs

![](../../assets/3f5dd94977195440.png)


- using a Forward+ rendering pipeline and raytracing for shadows
- presents a frame breakdown of the main rendering passes
- acceleration structure for skinned objects is updated via UAV writes from a vertex shader

![](../../assets/fbf5a1154aef86a6.png)


- shows the different spaces that are typically involved in 3D rendering
- how to transform between the different spaces
- visually shows the effect of the transformations

![](../../assets/ab57f511d94d603d.png)


- series on rendering of volumetric clouds
- shows how to sample the sky lighting contribution
- using a sampling scheme that places more samples in the bright sections of the sky

![](../../assets/ed933ae73db7b414.png)


- Flax engine now fully supports a Vulkan backend
- better performance than the D3D12 implementation

![](../../assets/a50862912c69846c.jpg)


- D3D12 is starting to allow GPU drivers to implement shader optimization in a background thread
- provides an API to control the driver behavior

![](../../assets/21209d3417f81090.jpg)


- presents how the snow simulation has been implemented and how it was optimized for Intel GPUs
- supports dynamic melting and build up of snow
- tesselation stage is used to generate the snow mesh

![](../../assets/cdf0d686981052de.jpg)


- presents the shader binding model used by granite
- user binds resources to sets and bind points on a per-resource basis
- Vulkan descriptor set management is not exposed to the user

![](../../assets/6d67be7cb094eb35.png)

Thanks to [Nathan Reed](http://reedbeta.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.