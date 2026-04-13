---
title: Graphics Programming weekly - Issue 172 — February 28, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-172/
author: Jendrik Illner
published: '2021-02-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the Video provides a 90-minute in-depth look at the rendering architecture used in CryEngine
- providing an overview of the abstraction layers
- discusses API abstractions, draw call generations, interactions with the higher-level rendering pipeline
- provides an overview of the different rendering stages of the pipeline
- covering GBuffer, shadows, tile shading, tone mapping, post-processing
- additionally provides an overview of the shader system

![](../../assets/13fb339639f88831.png)


- the article presents two methods to hide water from the inside of boats
- the first method uses an invisible inside mesh for the ship to draw depth before the water to block it from rendering
- second method involves using the stencil buffer to mask out parts of the water
- presents difficulties with either technique and how to deal with them
- source code for use with Unity is provided

![](../../assets/28864f350d35b49f.png)


- the article presents an alternative way to pack PBR textures into a single 4 channel texture
- albedo information stored as a gradient with gradient reconstruction, normals stored as height derivates, and linear smoothness
- presents how this was integrated into Unity
- shows the setup tested on a 6 material blend setup and presents performance comparison against the classical packing

![](../../assets/1c884f39163abaef.png)


- the article shows how the Vulkan extensions enable bindless indexing on Android
- presents an overview of dynamic indexing (and restrictions), update after bind, and GPU based validation

![](../../assets/2893bf14e6d0cba9.png)


- the article presents how the bindless binding model has been integrated into The Machinery
- shows the setup, lifetime management as well as integration with the shader system

![](../../assets/eae435876678fa91.png)


nDreams is an award-winning independent developer and publisher, delivering world-leading interactive virtual reality experiences. We recently launched Phantom: Covert Ops, a stealth action game redefined for VR, and we couldn’t be more proud of what the team have achieved. We are seeking a Principal Graphics Programmer to join our growing team and help build the systems that let our artists and designers breathe life in to the VR experiences we create. We can’t wait to show you what we’re working on next …

![](../../assets/7db5822dbf184812.png)


- 10h Video online class about shader development
- whole series covers an entire spectrum from basics, over lighting, mesh deformation, skyboxes, and image-based lighting
- provides assignment and discusses different approaches to solve it

![](../../assets/19c235091facb384.jpg)


- the article presents the buffer_device_address (BDA) extension for Vulkan
- this extension adds pointer support for Vulkan resources
- allows users to request the virtual memory address of each resource, operate on it, and even resolve it from within shaders
- shows how to use a pointer in a shader
- additionally covers debugging advice and how this is handled inside of SPIR-V

![](../../assets/f6eb000801fca124.jpg)


- provides an idea on how to maintain a pixel art style with dynamic lighting in a 3D environment
- technique uses position and UV derivatives to quantize the lighting results onto the center of the texel

![](../../assets/af8f9e7f76b0e221.png)


- the video tutorial shows how to generate a grass mesh using a compute shader
- animate the grass from the vertex shader to apply movement

![](../../assets/f0fa4c137b628cc9.png)


- the video tutorial shows how to implement a dissolve shader for 2D sprites using the Visual Shader language of Godot

![](../../assets/135a980ce5897cdf.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.