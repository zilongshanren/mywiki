---
title: Graphics Programming weekly - Issue 126 — April 5, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-126/
author: Jendrik Illner
published: '2020-04-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- collection of Vulkan tutorials for the VK_KHR_ray_tracing extension
- the tutorial starts from a working .obj rendering using rasterization and then integrates raytracing
- additional topics covered are Anti-Aliasing, handling thousands of Objects, Transparency, Reflections, Animation, Callable Shader and Ray Query

![](../../assets/cd662341840e00c6.png)


- the article shows how Nsight was used for debugging a frame stutter bug in the Vulkan raytracing implementation of Wolfenstein: Youngblood

![](../../assets/572ec3409b958666.png)

- the post presents how to use Nsight to apply the Peak-Performance method to determine a performance problem in Wolfenstein: Youngblood (Vulkan)
- shows how to detect being memory-bound and how to reduce the texture memory being access in a hit shader

![](../../assets/e394b38e5bf0aa45.png)


- this Unity tutorial explains how to implement a burning effect for paper
- this tutorial builds on previous parts of the series

![](../../assets/ca7457b058ed10e5.png)

- part 1 of rust graphics programming series using the rust gfx hal
- gfx-hal is a graphics abstraction layer on top of D3D12, Vulkan and metal
- this in-depth tutorial covers everything required from the setup of the application, window, shader, etc. needed to render the first triangle into a window

![](../../assets/901ff8db52860ec3.png)


- the second part of the tutorial series extends the example so that Vulkan push constants can be used to render multiple triangles with varying settings
- settings that can be modified include color, position, and scale

![](../../assets/69d075d22114aa7c.png)


- the article presents a method that allows validation of a physical camera model against ground truth data

![](../../assets/83694fa65e88cf60.png)

- collection of links and graphics community news such as ACM Digitial library being free, I3D posponed, …

![](../../assets/8561646a5e3f1b5e.png)

- the article shows how to use quadratic interpolation for depth aware upsampling
- the presented use-case presented is volumetric clouds

![](../../assets/9e0a267f876dd4c0.png)


- the GTC talks provide an overview of Deep Learning Super Sampling
- presents an overview of the challenges for upscaling the results of realtime rendering
- shows a history of existing techniques and compares the qualities of different methods
- includes a section on how to integrate the technique into Unreal Engine 4

![](../../assets/4b2c350a3a48f043.png)


- his Unity tutorial shows one way of blending meshes that are close to the terrain with the terrain colors
- the presented approach uses a separate depth texture to record the terrain depth and uses this to calculate the distance of a pixel to the terrain

![](../../assets/c47924b48a4717fa.png)


- the article presents a breakdown of the rendering stages found in the PC version of Batman: Arkham Knight
- the game uses a hybrid approach between forward and deferred rendering based on the distance to the camera
- lighting is done in a computer shader using checkerboard pattern with upscaling
- rain is using GPU based particles

![](../../assets/a7848d2f386d1055.jpg)


- the GTC presentation explains how the technique aims to replace existing indirect lighting techniques
- provides an overview of how the method combines ray tracing, fast irradiance updates, and a moment-based depth scheme to enable realtime GI without baking information offline

![](../../assets/ca0a0518ec1a1756.png)


- ACM tech talk with Ed Catmull & Richard Chuang happening on Tuesday, April 14

![](../../assets/e6981b88c1f8bcde.jpg)


- the paper presents a new technique to speed up the rendering of complex, layered materials
- the model doesn’t rely on any precomputation

![](../../assets/4fd4fdb837756954.jpg)


- the article presents a method for direct construction of tileable isotropic blue noise
- the technique is based on improved Correlated Shuffling

![](../../assets/8968e55fd8d1a856.png)


- A twitter thread that explains what barycentric coordinates are and how they are commonly used in computer graphics to interpolate data
- provides animated graphics to explain the concepts more visually

![](../../assets/e64080d95f1a1587.png)

Thanks to Sean McAlliste for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.