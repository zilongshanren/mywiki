---
title: Graphics Programming weekly - Issue 80 — April 14, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-80/
author: Jendrik Illner
published: '2019-04-14'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- vulkan extension that allows progress markers to be inserted into the Vulkan command stream
- these can be used to detect the range of draw commands that have caused a GPU device error
- a short overview of how it is used in X-Plane

![](../../assets/a5768fd22be9df86.png)


- a brief overview of the rasterization process
- look at the logical rendering pipeline model
- presents the different components that are used to implement pipeline in hardware
- implementation details about the different stages

![](../../assets/caaa7f9c60c41978.png)


- Ray Tracing Gems is now also available as a free Kindle version

![](../../assets/c89416dfcb1ec661.jpg)


- presents an overview of the general flow of a frame of the game
- a more detailed look at the acceleration structures used for the raytraced GI implementation

![](../../assets/3fb038c35c84751a.png)


- looks at the composition of transparent objects, lens flares and at terrain tessellation
- presents more images from the acceleration structures and problems discovered with it

![](../../assets/e2a4156105cad549.png)



- all GDC content from Nvidia is now available for download (free login required)

![](../../assets/5bdd203082b7e737.jpg)


- shows which tools are available to look at the shader disassembly for AMD GPUs
- presents the instructions generated for a simple shader and overview of some of the instructions used
- shows the effect of code changes to the code generation

![](../../assets/5f82a7151819b201.png)


- preprint of I3D paper that will be presented in May
- AO calculations are split into large-scale interactions based on sphere approximations
- finer details are created using linear interpolation from key points on the spheres
- both components are trained against ground truth data

![](../../assets/218f3672897b328c.png)


- overview of the latest extensions added to Vulkan on Nvidia GPUs
- mesh shader motivation, execution model and how to use them
- barycentric coordinates extension
- subgroup overview and tensor core access
- texture space shading
- derivatives in compute shaders

![](../../assets/0ba15a0187e5cd27.png)


- discusses the authors’ thoughts about abstraction levels in graphics APIs
- presents the motivation for the design of the granite engine API

![](../../assets/547b660331c892f5.png)

Thanks to [Cort Stratton](https://twitter.com/postgoodism) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.