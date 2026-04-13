---
title: Graphics Programming weekly - Issue 107 — November 17, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-107/
author: Jendrik Illner
published: '2019-11-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a new technique that uses a neural network to reconstruct foveated rendering from sparse source data

![](../../assets/0798836d5aff812d.png)


- the article provides an overview of the new API that allows users to request the underlying D3D12 resources from an application that is using the D3D9 on D3D12 layer

![](../../assets/0c737aa358a13b56.jpg)


- the article proposes a technique that uses a random texture to perturb the normals of dunes to simulate the variation caused by sand grains

![](../../assets/1ccdb226b5b8ef9e.png)


- the article provides an overview of how Vulkan descriptor set management influences CPU performance
- provides 3 possible solutions to the problem
- showing how they affect both performance and application implementation
- suggest a descriptor set caching scheme combined with using a single VkBuffer to store uniform data

![](../../assets/ceced1cd9b441296.png)


- D3D12 is adding two new flags for memory heap creation
- D3D12_HEAP_FLAG_CREATE_NOT_RESIDENT, the heap is created non-resident state to enable EnqueueMakeResident to be used for heaps
- D3D12_HEAP_FLAG_CREATE_NOT_ZEROED enables an optimization that allows non-zeroed pages to be returned

![](../../assets/80d219b6e0424cc6.png)


- the article proposes a solution for voxel rendering
- voxel scene is pre-calculated into multiple vertical slices
- each slice is represented by an image and stores all voxel in the slice
- additionally contains a logic summary on how to procedurally generate a voxel-based island

![](../../assets/b1fbe53ad7e4aeb6.jpg)


- brief article explains how to detect particle overdraw using the PowerVR profiler
- suggest to disable anisotropic filtering and use close fit meshes for particles

![](../../assets/f6165a59196c376e.png)


- the author mentions the new rendering features of Disneys’ Hyperion Renderer that have been used on Frozen 2
- contains a large selection of stills from the movie

![](../../assets/99b73fa6c914e079.jpg)


- collection of tweets showcasing a large number of effects, games and technical art resources

![](../../assets/6972998caa4beee1.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.