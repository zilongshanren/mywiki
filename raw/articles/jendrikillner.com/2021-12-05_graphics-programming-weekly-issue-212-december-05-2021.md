---
title: Graphics Programming weekly - Issue 212 - December 05, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-212/
author: Jendrik Illner
published: '2021-12-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video tutorial introduces swizzle operations
- shows how to emulate functionality in Unity that is available natively in UE

![](../../assets/0259a8b3c9ca0fa7.png)

- the article presents the shader multiply/add operation (fma/mad)
- discusses how it’s mapped onto the hardware and allows more efficient and precise operations
- shows example use cases, discussing the impact on the precision of the calculation results

![](../../assets/1fb695826440f941.png)


- the tutorial describes the capturing process for image-based lighting
- IBL probes are omnidirectional representations of lighting information captured from high dynamic range images of a location
- shows how to capture the images and set up the pipeline to integrate the captures into the renderer
- explains how all captured with different exposures are combined into a single IBL probe

![](../../assets/809ddbf7f95e532a.png)


- the article describes the hardware characteristics of the PS1 renderer
- shows a visual demonstration of the effect of sub-pixel rasterization and perspective correct interpolation
- additionally shows how to emulate the hardware shortcomings to create a PS1 style look on today’s hardware

![](../../assets/e39d95d6d8a98c1e.png)


- the paper introduces a combination of tile-based stochastic light culling and reservoir sampling
- this reduces the variance for lights close to surfaces such as common in Virtual Point Lights (VPLs) based indirect illumination systems

![](../../assets/3551a642443a65f2.png)


- the article shows how gradients differ with different color spaces
- compares sRGB, linear, and Oklab color spaces

![](../../assets/fa43f625cbcb944b.png)


- the article presents the Vulkan SDK layer architectures
- introduces how to enable Arm performance warning layer
- additionally shows how to run the layer on RenderDoc captures to gather information

![](../../assets/4f940971521025a6.jpg)


- the article provides an overview of use cases for ray tracing
- discussing disk and memory space-saving, shadows, reflection
- also mentions the effects on user-generated content

![](../../assets/c5d681326f5a9eca.png)


- the article discusses the importance of asserts for debugging a renderer
- shows how asserts are implemented in PBRT
- additionally presents an example from the PBRT development where asserts helped to catch a performance issue

![](../../assets/ebfc75d5959924dc.jpg)


- the article explains what information GPUView and Radeon GPU Profiler show
- shows how items are progressing through the queue over time
- additionally shows how to see how utilized the GPU is over time

![](../../assets/f498b505e238e7f5.png)


- the article provides an overview of the bloom technique and implementations
- comparing the technique implemented by UE and Call of Duty and how the suggested solution is a combination
- shows how to integrate a custom implementation into the UE4 codebase

![](../../assets/1bde3f7ef44fd4bb.jpg)


- the video tutorial provides an overview of the skinning animation technique
- explaining the process of how data is authored, animated, and encoded in a GPU friendly format
- additionally shows how to set up, compile and use Assimp to parse the initial skinning poses

![](../../assets/b4701d3e07279081.png)

Thanks to [atyuwen](http://atyuwen.github.io/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.