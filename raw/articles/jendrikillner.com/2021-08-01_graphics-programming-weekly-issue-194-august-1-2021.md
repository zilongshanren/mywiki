---
title: Graphics Programming weekly - Issue 194 - August 1, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-194/
author: Jendrik Illner
published: '2021-08-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- presents how all ray-tracing based effects were implemented in the game Control
- opaque and transparent reflections, near field indirect diffuse illumination, contact shadows, and denoiser tweaks

![](../../assets/dfd81c06b5b6e8cc.jpg)


- extension of the previously presented Decoupled Visibility Multisampling technique
- underlying idea is to see 8xMSAA as a 2x2 group of pixels with 2xMSAA each
- using the sample information for TAA upsampling

![](../../assets/f263c2b3e7e788ae.jpg)


- part of the series that discusses how GPU support for the Moana Island scene was added to pbrt-v4
- presents an overview of ptex approaches chooses by others and shows the currently basic Ptex approximation used
- shows a comparison between the CPU and GPU version
- additionally discusses performance and optimizations

![](../../assets/7346316527ff816b.png)


- the blog discusses Vulkan usage for GPGPU workloads, in particular for machine learning
- presents the varying requirements for machine learning and how Vulkan can be used to satisfy them
- discusses how it interacts with the business aspects (OEM, platform holders, …)
- additionally shows the authors view onto the current challenges and future developments

![](../../assets/005a574235c2d0a3.jpg)


Threedy is a young Fraunhofer spin-off with a considerable number of high-profile customers in the german automotive sector.

We develop the Visual-Computing-as-a-Service platform instant3Dhub to enable our customers to leverage the true value of their 3D data in industrial applications – any data, any device, any size.

instant3Dhub has a strong focus on CAD data visualization, from browser-based to mixed reality applications and delivers out-of-the-box collaboration and augmented reality features.

We are looking for graphics programming enthusiasts to support our core development team for the 3D streaming with a focus on the evolution of our web frontend build on WebGL.

![](../../assets/2365cbc531701a1a.png)


- a Bachelor thesis that presents a method for GPU based silhouette generation from Polyhedral lights
- uses an algorithm based on binary space partitioning for storing precomputed silhouettes for every point in the scene
- additionally presents how to use Silhouettes for Solid Angle Sampling

![](../../assets/f2794c5222da7a9d.png)


- GDC talk presents a walkthrough of the technical creation aspects of the demo
- shows UE5 was used, discussing nanite limitations and how the different systems can be combined
- additionally, art pipeline implications and findings
- presenting performance numbers of lumen, nanite, upsampling, virtual textures, virtual shadow maps, …

![](../../assets/31bcc323505e6f5e.png)


- the post compares different Color Matching Function (CMF) for use with spectral rendering techniques
- provides an analytical approximation for the CIE 2006 CMF and provides how to calculate the D65 white point

![](../../assets/052dc73b34676c32.png)


- the article presents an overview of numerous techniques that can be used to implement lighting for a 2D game
- discusses pros/cons of each technique
- additionally shows limitations of the techniques

![](../../assets/3ed480c904a9e040.png)


- the Vulkan hardware database has been updated
- texture format view now has a breakdown of what tiling mode is supported for each format
- improved filtering, cleaned up data and color space added for surface formats

![](../../assets/cb0e16f3419a4423.png)

Thanks to [Erika](https://twitter.com/rrika9) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.