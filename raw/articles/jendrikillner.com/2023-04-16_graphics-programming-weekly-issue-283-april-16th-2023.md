---
title: Graphics Programming weekly - Issue 283 - April 16th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-283/
author: Jendrik Illner
published: '2023-04-16'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the talk discusses how the PC port approaches PSO management to reduce stutter and manage memory when the game was designed for unified memory
- how they approached ray-tracing for parity with the PS5 implementation and what extension got added to improve the quality
- detailed section on how to further debug GPU issues on PC and how to deal with super wide resolution rendering

![](../../assets/ec54792221707522.png)


- the video explains visually to read and understand 4x4 transformation matrixes
- explains the basic of matrix/vector operations
- presents how to combine the operations to allow rotations, scaling, and translations of objects using a visual approach

![](../../assets/640630c41dad1a9a.png)


- the blog post describes the approach of incrementally accumulating voxel data to augment the reprojection of the previous depth buffer
- shows images of how the depth buffer develops over time and how small sub-voxels can help to improve the results

![](../../assets/312217010e1791ef.png)


- the article describes how Godot converts SPIR-V shaders to DXIL for D3D12
- covers the old approaches (SPIRV-Cross) and why it was replaced with using Mesa’s NIR approach
- discusses what SPIR-V Specialization constants are and how a patchable DXIL is created to allow the approach with D3D12

![](../../assets/4d06b91a945ef311.jpg)


- the video presents an overview of the papers that will be presented during the I3D 2023 in Bellevue
- covering interactive Neural Radiance Fields, importance sampling for Dynamic Diffuse Global Illumination, real-time dune simulation, and many more

![](../../assets/68f1b0f9ee796672.png)


- the video presents the visual difference the overdrive (ReStir-based) raytracing implementation for Cyberpunk 2077 can achieve
- compares against the prior ray tracing implementation and the maximum rasterization quality
- shows cases where the mode makes a huge difference
- additionally presents the performance influence of the mode

![](../../assets/843f7e1d24718339.png)


- Nvidia released the Displacement Micro-Map Toolkit SDK
- provided samples and documentation explaining the capability and how to use them from Vulkan
- the technique allows the triangle to be sub-divided and displaced with a highly compressible format
- this can be raytraced to add additional detail at lower costs

![](../../assets/7ea4c3bc84414354.png)


- the tutorial shows how to render a first triangle with WebGPU
- this is using the final WebGPU spec as it is now publically available in Chrome

![](../../assets/d462c4a181a804ae.png)


- the website collects information about the API and extension availability for Web-based usage
- supports WebGL, WebGL2 and WebGPU

![](../../assets/295945670bc911b3.png)

Thanks to [Robert Wallis](https://github.com/robert-wallis) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.