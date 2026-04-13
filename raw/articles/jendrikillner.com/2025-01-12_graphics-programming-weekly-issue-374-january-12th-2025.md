---
title: Graphics Programming weekly - Issue 374 - January 12th, 2025
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-374/
author: Jendrik Illner
published: '2025-01-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- A detailed discussion of the rendering color pipeline in Unreal Engine
- Explains color spaces, color encoding, and various stages of color conversion
- Presents post-processing effects and the importance of proper color handling

![](../../assets/b569bb6a63ff2b11.png)


- An explanation of radiometry concepts such as Radiance, Solid angle, Irradiance, Radiant flux, and Radiant energy
- Ties these concepts together in the context of a renderer’s camera

![](../../assets/958601a1dd3265a5.png)


- A look at various techniques to generate mipmaps for vegetation textures
- Discusses the problem of losing coverage and shape with classical downsampling techniques
- Compares various techniques and suggests their pros and cons

![](../../assets/e655486193e12fe3.png)


- An overview of techniques defining a WebGPU implementation
- Provides a high-level overview of the shader pipeline, culling, shadow rendering, and more
- Discusses light implementation, skybox, screen space reflection, etc.
- Source code is available

![](../../assets/76b6644168c6a3c1.png)


- A detailed discussion on the complexity of image format loading and display
- Insights into the image format landscape and tone mapping HDR formats correctly
- Additional topics include cursor rendering and optimizations

![](../../assets/bdd100e93fb6bb44.png)


- NVIDIA released an interactive and free course about learning OpenUSD concepts
- Structured into modules, the course combines written guides and video tutorials for a comprehensive learning experience.
- Hands-on Jupyter notebooks let you explore practical examples and deepen your understanding of key topics.
- Just released: Applied Concepts courses on composition arcs, asset structure principles, and data exchange pipelines

![](../../assets/d3576a8e7539046c.png)


- An overview of different MSAA modes in the Metal API
- How to adjust the MTKView wrapper to create a memoryless MSAA target
- Shows the effect of this change on memory usage

![](../../assets/1a00269a26260275.png)


- Challenges developers face when implementing DRS on PC
- Covers hardware and OS interaction, latency, and user input variability
- Briefly discusses approaches to solving these issues on PC

![](../../assets/fd3bc67f5436a404.png)


- Video tutorial on implementing uniform buffers in a Vulkan application
- Explanation based on code changes from previous iterations
- Shows how to use the concepts to implement a 3D flythrough camera

![](../../assets/caf63887fd6097ed.png)


- Announcement of Cooperative Vector Support extensions for D3D
- Exposes hardware-accelerated matrix by vector operations
- Enables access to Tensor Cores with neural shading in new RTX50 series GPUs

![](../../assets/9d99b5a2b8513a74.png)


- Discusses updates to the Reflex 2 system
- Explains how changing camera views are applied by reprojecting the camera into the new camera space
- Shows how unfilled areas are filled through neural reprojection techniques

![](../../assets/5ab8fc2bd10095f5.jpg)

Thanks to Stephen Hill for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.