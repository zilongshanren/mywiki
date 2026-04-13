---
title: Graphics Programming weekly - Issue 151 — September 27, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-151/
author: Jendrik Illner
published: '2020-09-27'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the post explains the experiences on porting the game from PS4 to PC using Vulkan
- part 1 of 3 focuses on optimize shader pipeline compilation and descriptor allocation
- the descriptor allocation is based around dynamic indexing into large arrays for each resource type

![](../../assets/f7cded386a36813d.png)


- part two of the series provides on porting Detroit: become human offers an overview of indexing considerations using the VK_EXT_descriptor_indexing extension
- shows the AMD ISA disassembly related to sampling textures and how much extra work is required when texture indexing is not uniform

![](../../assets/fd57569df135a540.jpg)


- the last part of the series briefly explains how they used scalarization to optimize shader, split command list recording onto multiple threads
- looks at memory management in more detail, detailing the AMD libraries and tools available for memory management

![](../../assets/8878b0fbb83bc01d.png)


- the author explains his approach for the design of an aurora shader challenge
- provides an illustrated walk through how to start from a simple effect and incrementally improve towards the expected look

![](../../assets/ef3a4dc71a20baae.jpeg)


- the articles explains how The Machinery implementing for rendering the outline of selected objects has been archived
- this is implemented as a screenspace effect using the object ID and depth buffer to detect the shape of the objects
- presents how to improve visual stability when TAA is used

![](../../assets/26ea931eb734109d.png)


- the blog post provides an overview of the different API layering implementations (Vulkan on Metal, D3D11on12, etc..)
- Vulkan Portability Initiative exposes a new extension (VK_KHR_portability_subset) that allows these layers to mark features as unsupported
- progress on updating the conformance testing and device capabilities emulators to make them aware of these constraints

![](../../assets/bff4efa8ae3aaafb.jpg)


- beginner-focused tutorial explains how to store normals, noise, and positional data in textures
- explains what kind of effects can be archived with this data
- the example effects are implemented using ShaderGraph in Unity

![](../../assets/2dd79873d6c63ad8.png)


- video presentation from the X.Org Developer Conference provides an overview of the Vulkan vendor-neutral API extension

![](../../assets/16225df314eda386.jpg)


- collection all entries for a tech art challenge with the theme Retro shaders
- the entries show a large variety of effects and implementations using different engines

![](../../assets/06a9e4ca69ccc10a.png)


- the author presents a look back at the last 5 years of the
[GpuDB](https://db.thegpu.guru) - a useful website to gather information about different GPUs and compare them

![](../../assets/129c3db16bb02f2d.png)


- the article explains the basic of the tiled GPU architectures used on mobile
- uses this information to explain the importance of using the correct load and store operations for Vulkan render passes
- additonally covers foveated rendering extension and how to structure rendering with multiple render passes

![](../../assets/f0be7c7ce5b83a80.png)

Thanks to [Warren Moore](http://metalbyexample.com/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.