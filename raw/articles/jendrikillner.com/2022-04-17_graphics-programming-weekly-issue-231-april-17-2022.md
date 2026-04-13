---
title: Graphics Programming weekly - Issue 231 - April 17, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-231/
author: Jendrik Illner
published: '2022-04-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- a collection of papers to be presented at Eurographics 2022
- a large number of topics are covered, including terrain authoring, spherical harmonic lighting, radiance transfers

![](../../assets/c8b0476f9b1c7faf.png)


- the GDC presentations talk about the implementation of the Deferred Texturing
- developed to reduce the vegetation rendering cost
- a very detailed look at the different implementation stages
- how it integrates into the Decima rendering pipeline and a look at the performance improvements achieved
- it additionally presents how to implement a variable rate solution on hardware without native support

![](../../assets/9497ab1c486cb5fc.png)


- the paper presents a new approach to compressing vertex data at a fixed bit-rate
- the paper presents error analysis, compares against existing solutions in terms of prevision and performance
- up to 13 per-vertex skinning weights can be compressed into 64bits with included code

![](../../assets/66dba10950d6285c.png)


- the article presents a detailed look at how different D3D12 ConstantBuffer patterns are mapped into SPIR-V
- shows how the patterns are mapped onto the hardware in RDNA2 ISA
- discusses how non-uniform resource influences the code generation
- additionally discusses quirks/limitations of ByteAddressBuffers and RWStructuredBuffer

![](../../assets/9f554355041f38a6.png)


- the article presents a summary of different methods to express rotations
- presents interactive visualizations of the methods
- shows the behavior of linear interpolation, discussing the limitations of the methods
- it additionally shows the mathematical derivation of the methods

![](../../assets/58ac663bda4d374b.png)


- the video presents an overview of the challenges in shader development
- discussing how Slang can address these challenges
- shows the decisions made to adjust the project development to prioritize adoption over publication from the start
- a brief look at how it matches into raytracing shaders and a look at upcoming developments

![](../../assets/f8200a0d3d4530af.png)


- AMD released a library to enable applications that use Heterogeneous-Computing Interface for Portability (HIP) to access ray tracing hardware
- this enables general C++ GPGPU computing workloads to take advantage of raytracing shaders on Nvidia and AMD GPUs

![](../../assets/d2e4fc2f91cd225f.jpg)


- the article describes how to construct a BVH from a collection of triangles
- axis-aligned bounding boxes are used as the foundation of the structure
- shows how to build and traverse the BVH

![](../../assets/f2f95077aacc57c3.jpg)


- the paper introduces an LTC (Linearly Transformed Cosines) approximation to anisotropic GGX using 4D lookup textures
- the demonstration video shows the importance of anisotropy for metal surfaces
- example code is provided

![](../../assets/da01319fea112fd8.jpg)


- the blog posts demonstrate how to implement ReSTIR (Spatiotemporal reservoir resampling)
- presents the implementation for Lambertian diffuse
- shows how to extend the concepts also to support specular sampling
- additionally presents the author’s technique to combine the influences

![](../../assets/1e75534bc8dfd86c.png)


- the article provides a showcase of the importance of a projection solver for a real-time fluids
- presents the Jacobi method and compares it against the Multigrid algorithm

![](../../assets/d67493ebcb4d2216.png)


- the video explains the concept of refraction and existing techniques to implement the effect
- covers how to draw transparent objects and how it’s expressed in the rendering pipeline
- shows the importance of drawing order when using rasterization and presents techniques for order-independent transparency
- presents alpha testing and limitations with mipmapping alpha testing
- it additionally covers solutions to ensure that objects look correctly under minification

![](../../assets/95ed45087cbd2407.png)


- the visual graph provides a visual representation of the different passes from the fluid simulation of the iOS application
- provides short overviews of the implementation of the different passes
- it additionally provides a visual representation of the visible state of the textures involved at the different stages of the pipeline

![](../../assets/85182e0b44c6419f.png)

Thanks to [Nathan Reed](https://www.reedbeta.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.