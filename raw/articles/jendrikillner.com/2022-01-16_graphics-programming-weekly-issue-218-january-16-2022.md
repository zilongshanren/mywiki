---
title: Graphics Programming weekly - Issue 218 - January 16, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-218/
author: Jendrik Illner
published: '2022-01-16'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents a deep dive into a gather related artifact
- discusses texture filtering, how fixed point is involved and how many bits of sub-pixel precision is used on different GPU vendors
- shows the necessary parts in the Vulkan and D3D spec to understand why an offset is required to match the hardware behavior

![](../../assets/fd7259e5dd78905e.png)


- the paper presents a multi-resolution hash table of trainable feature vectors
- the presented system focuses on the task-independent encoding of relevant details and can be applied to a variety of tasks
- shows the ideas applied Gigapixel images, Neural SDF, NeRF, as well as Neural volumes

![](../../assets/135d92a8cdd1ddf5.png)


- the video improves the tri-planar projection shader (allows texture mapping without UVs)
- shows how to make sure that texture directions are correct on all sides of the projection
- additionally shows how to convert the node graphs into a single node to make it usable from other shaders more easily

![](../../assets/978c44da990f2551.png)


- introduction to a university course that covers the fundamental concepts of real-time rendering on the GPU
- the course is project-based, explaining the concepts and applying them in OpenGL examples

![](../../assets/8e460b465948193e.png)


- the video explains how to derive the Lagrange Interpolation functions
- presents how to use desmos to visualize the derivation process

![](../../assets/ed5d252f4a895e92.png)


- an extensive collection of a large variety of tech art tweets collected into a single post
- contains VFX, demos, art showcases, and a large number of exciting demonstrations
- also contains an example that visualizes GPU execution patterns

![](../../assets/4f6683bb04651de8.png)


- Two Minute Papers video summary of the Weatherscapes: Nowcasting Heat Transfer and Water Continuity paper
- shows a new model to simulate weather effects using the microphysics of water

![](../../assets/17259d9add55e439.png)


- the tutorial shows how to use the VK_KHR_dynamic_rendering extension in Vulkan
- shows the steps required to load the extension, use it, and how it affects related components such as pipeline creation

![](../../assets/19fe8d0f78e54ea8.jpg)


- the first part of a shader coding course (6 hours!) focusing on textual shaders using Unity
- explaining the fundamentals of the rendering pipeline, focusing on applicable knowledge across engines

![](../../assets/fe527efb1de1a98c.png)

Thanks to [Panagiotis Tsiapkolis](http://panagiotis.tsiapkolis.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.