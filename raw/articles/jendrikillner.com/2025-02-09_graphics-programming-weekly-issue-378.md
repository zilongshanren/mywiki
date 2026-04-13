---
title: Graphics Programming Weekly - Issue 378
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-378/
author: Jendrik Illner
published: '2025-02-09'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- The blog post announces the release of the Mega Geometry SDK
- This entry provides a summary of the various samples and libraries

![](../../assets/de2bc3cffcf33a43.png)


- Nvidia released a beta version of Neural Texture Compression
- A neural network is used to compress all textures of a PBR set together
- This can either be decompressed at sample time or be transcoded into BC during texture load
- The readme provides a brief explanation and example data

![](../../assets/3e63ace246a235f3.png)


- The paper introduces turning 3D Gaussian Splatting from unstructured into structured structure using spherical UV mapping
- The paper presents how the mapping allows existing models to better operate on the image formats
- Shows improvements in compression and quality

![](../../assets/6bb7d41ec3959a8f.jpg)


- This blog post introduces the release of the AMD Dense Geometry Compression Format SDK
- The format aims to be the equivalent to what BC/ETC is for textures but instead for geometry
- Explains limitations of the current solution and how the format aims to overcome it
- The SDK contains how to compress, view, and decompress the data (both on the CPU and GPU)

![](../../assets/e12efaeaace70fdb.png)


- The video tutorial presents how to implement a world space-based effect that allows blending between different world rendering styles
- Implementation is done using a mix of visual shading language as well as HLSL
- Presents simple shapes as well as texture-driven outlines

![](../../assets/5959546a7eaf1f7d.png)


- The blog post provides a high-level discussion of why Unreal Engine games commonly encounter micro stutter related to shader loading
- Discusses the various systems Unreal Engine contains and introduces new methods to reduce the problem
- Additionally, it discusses available debug options that should help developers verify the efficiency and introduce solutions during development

![](../../assets/5eb2c82e739778c4.png)


- The video visually explains the most common mathematical concepts that are encountered in game development
- Covers interpolation, trigonometry, vectors, dot-product, matrices, quaternions
- Presents each concept with practical and visual examples

![](../../assets/4ff6572e401e6a95.png)


- The article discusses a technique that uses Stable Diffusion to generate a tileset
- Discusses how to drive the model to generate the transition tiles between a known set of materials
- Presents the limitations and issues with the developed model

![](../../assets/6339acf032296ff2.png)


- The article presents a simplified model for Vulkan and D3D12 Extended Barriers
- Discusses both textures and buffers and how different hardware interacts with them
- The code for the implementations is available

![](../../assets/a9f12f3d29fb6565.png)


- The article presents a series of post-processing effects that build upon the same underlying techniques
- Each effect is explained and presented with detailed visualizations
- Additionally, each effect is demonstrated as a real-time implementation that can be interacted with directly on the website

![](../../assets/cbe9d9c8d5f7cee5.png)


- This video tutorial series covers the implementation of a Vulkan renderer
- In this episode, you will learn how to create, load, and sample a texture

![](../../assets/cac59ebdfe7c221b.png)

Thanks to [Angel Ortiz](https://x.com/aortizelguero) for supporting this series

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series