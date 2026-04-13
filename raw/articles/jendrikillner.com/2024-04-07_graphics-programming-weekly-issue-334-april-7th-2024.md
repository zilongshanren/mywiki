---
title: Graphics Programming weekly - Issue 334 - April 7th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-334/
author: Jendrik Illner
published: '2024-04-07'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog post discusses how to implement a continuous LOD system for meshlet-based rendering
- shows how to calculate the error metric and structure the data for GPU access
- presents how to select the correct LOD level at runtime
- A video of the results is included

![](../../assets/b81c8a8026fab045.png)


- the presentation provides an overview of the Nanite and Lumen systems
- shows a high-level look at which parts affect performance and how performance intuition doesn’t match the classical rasterization model
- the whole presentation slide deck is done in the UE5 editor

![](../../assets/f42af034677f483a.png)


- the video explains the difference between alpha blending and dithered transparency
- shows sorting issues related to blending order and how dithered transparency solves them
- presents how to implement the technique using Unity Shader Graph
- additionally shows the limitations of the technique

![](../../assets/0bfbecf9d8e17713.png)


- the latest version adds support for Slang with Vulkan, additional extensions support, D3D12 Pixel history support, and many bug fixes

![](../../assets/ddf1ca1e100db96d.png)


- the article presents how usage patterns of copy queues to upload and download data from the GPU can significantly affect the amount of stalls
- discusses the different patterns and presents timelines to show the waits
- additionally shows how multiple copy queues interact and the importance of copy queue priorities

![](../../assets/811f0e4a6aa641b7.png)


- the blog post describes a method to apply lighting to Gaussian Splats
- shows methods to reconstruct geometry with normals and how to filter the results
- additionally discusses limitations and ideas for improvement or leveraging of existing mesh-based solutions

![](../../assets/ad5ea36a6deed59c.png)


- the latest video in the series explains how to create a Vulkan Swapchain
- explains the different presentation modes
- additionally shows how to create a view of the different images of the swap chain

![](../../assets/07f1a2af22e58f8f.png)

Thanks to [Unai Landa](https://twitter.com/unai_landa) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.