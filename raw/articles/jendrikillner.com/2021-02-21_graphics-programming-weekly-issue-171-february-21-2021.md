---
title: Graphics Programming weekly - Issue 171 — February 21, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-171/
author: Jendrik Illner
published: '2021-02-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article shows a few ways of doing bilinear upsampling and downsampling
- explains why it’s essential to follow the same convention everywhere and verify that no unintended shifts are introduced
- suggests that the same half-pixel offset convention as used by GPUs should also be followed in CPU code
- discussing the different tradeoffs for performance/aliasing/smoothing

![](../../assets/d58c5ce5c68a0857.png)


- the Twitter thread presents details about how the outline rendering has been implemented
- based on several different outline classification types are combined as a post-process
- the edge detection for outlines is additionally leveraged for SMAA improvements

![](../../assets/85518b5186e0fd1d.jpg)


- the paper presents a new technique to generate more accurate motion vectors for shadows, glossy reflections, and occlusions
- the key idea is to detect and track the source of the effect (for example, the object blocking the light) and use the change of the source to adjust the back-projection accordingly

![](../../assets/44934eb44578ea2b.png)


nDreams is an award-winning independent developer and publisher, delivering world-leading interactive virtual reality experiences. We recently launched Phantom: Covert Ops, a stealth action game redefined for VR, and we couldn’t be more proud of what the team have achieved. We are seeking a Principal Graphics Programmer to join our growing team and help build the systems that let our artists and designers breathe life in to the VR experiences we create. We can’t wait to show you what we’re working on next…

![](../../assets/7db5822dbf184812.png)


- the article presents Separating Axis Theorem for OBB (oriented bounding box) against the view Frustum
- additionally covers how to use Intel ISPC to generate the SSE accelerated version of the algorithm
- presents performance comparison with/without SEE and compares against the previous implementation from part 1

![](../../assets/b0022cba787a98fd.png)


- the blog post presents an overview of Vulkan extensions added as part of Android R
- lists the extensions, what problem it solves and how it works
- covering uniform alignment rules, separate depth stencil views, SPIR-V support, loop control, 16-bit subgroup operations as well as imageless framebuffers

![](../../assets/f28f2800db2a3047.png)


- the article presents how to use 3 parallel work queues in OpenCL to read, write and process a GPU kernel at the same time
- presents source code for buffer creation, queue creation, and synchronization

![](../../assets/d02ec4d744506178.png)


- article presents how to integrate a custom shading model into the Unity rendering pipeline
- implements the Minnaert shading model
- this model makes the surface seem darker from certain viewing/lighting direction

![](../../assets/d2571b130a80b317.png)


- the blog post discusses the different memory types and how applications should use them
- provides overviews on what is reported on Intel, Nvidia, and AMD hardware
- additionally explains how integrated and external GPUs expose different available memory

![](../../assets/d44c4123d06ab1ac.png)


- the AMD driver now supports the new Vulkan synchronization extension
- post provides a brief overview of how the capabilities of the extension allow the drivers to be more efficient in reducing GPU cache flushes and stalls

![](../../assets/3716d385251748ef.png)

Thanks to [Jan-Harald Fredriksen](https://twitter.com/jhfredriksen) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.