---
title: Graphics Programming weekly - Issue 131 — May 10, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-131/
author: Jendrik Illner
published: '2020-05-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the final part of raytracing series
- presents what denoising techniques are and why they are required
- presents a comparison in multiple scenes, explaining how neural network technique is trained

![](../../assets/3af795406bb22943.png)


- the article presents an overview of the Nvidia GPU architecture and how they developed over time
- shows changes done to the hardware, discussing the strengths and weaknesses of the design

![](../../assets/cdb14ea7703facac.png)


- presents a technique that combines singed distance fields and ray marching to render static volumetric clouds
- the signed distance field is used to only use ray-marching once inside the cloud volume

![](../../assets/2762ab7d0b3e58f2.png)


- the paper presents how to apply the monte-carle methods to geometry processing

![](../../assets/eae0d122552620ac.png)


- the paper presents an overview of ray sorting techniques and introduces a new method for ray sorting of secondary rays

![](../../assets/cb35061c60d77daa.png)


- this paper presents the results of testing done into human perception, comparing test-cases for perceived quality differences between resolution and framerate
- proposes a model for prediction to enable an application to dynamically adjust framerate and resolution based on the findings to achieve the highest perceived visual quality

![](../../assets/116ef44cd0491335.png)


- the Video presents an overview of a shader technique implementing the behavior of leaves in Animal Crossing
- this technique is based around storing individual pivots for multiple leaves and applying dynamic effects based on this
- implementation with blender and Godot is shown

![](../../assets/fdc79a3be84f40db.png)


- the author presents his view on WebGPU for use in native applications
- showing why it could be an excellent offer for many types of developers if it can deliver on its promises

![](../../assets/3a08f6c8250b3e51.png)


- collection of resource links to presentations, papers and articles focusing on the details of GPU architectures

![](../../assets/6fef594c1e22a0f0.png)


- a brief overview on how to get started with CUDA
- programming model and required components

![](../../assets/0e6ea659716ae178.png)


- a tool to generate meshlets for use with compute based culling algorithms or mesh shaders
- explains the difference between Bounding Spheres and Visibility Cones and how to use them for culling parts of meshes more efficiently

![](../../assets/b5ba0b6d2630af4c.jpg)

Thanks to [Jens Hartmann](http://top-or.de/projects) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.