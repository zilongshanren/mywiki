---
title: Graphics Programming weekly - Issue 233 - May 1, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-233/
author: Jendrik Illner
published: '2022-05-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the post presents a method for reducing the size of visibility output buffers and the effect on performance
- shows that it’s more efficient to recalculate ray differentials than it is to rely on hardware differentials to be stored in additional channels

![](../../assets/c8012457ee577a09.png)


- the article presents how to update a BVH tree for an animated mesh
- introduces the refitting technique to allow fast adjustments of an existing BVH tree for changing triangle data

![](../../assets/4c6e91840c1f77ee.jpg)


- the article presents a walkthrough of how to use GPU Trace Analysis and GPU Profiler to identify performance issues in a shader
- presents examples of cases that show different limits

![](../../assets/0f1df659d913db07.jpg)


- the paper presents a database of 63 optimized and regularized SDF functions of varying complexity
- additionally, a tool for viewing and inspection is provided

![](../../assets/044da0bae5462808.png)


- the article discusses the complexities of implementing ExecuteIndirect from a driver’s perspective
- presents what kind of functionality is affected and how it affects driver maintainability
- presents a look at the capabilities of VK_NV_device_generated_commands

![](../../assets/5dea87df4b499f56.png)


- the video on how to implement ray-casting from the cursor position into a 3D world to allow the movement of objects
- discusses the necessary mathematical transformations
- presents how to implement the technique using OpenGL

![](../../assets/21ac06bebe953f5f.png)


- the blog post presents the new capabilities of the agility SDK
- new optional features allow the reduction of alignment requirements
- it additionally clarifies the copy behavior between resources of different dimensionality

![](/img/posts/graphics-programming-weekly-233/dx12.jpg)


- the thread explains the history of the PS1 hardware and how it defined the look of the games of the generation

![](/img/posts/graphics-programming-weekly-233/tomb_raider.jpg)


- a collection of news from the graphics windows development world
- covering PIX, OpenGL on ARM, Dynamic Refresh Rate, as well as win11 updates

![](/img/posts/graphics-programming-weekly-233/dx12.jpg)

Thanks to [Dominik Lazarek](https://twitter.com/Omme) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.