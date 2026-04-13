---
title: Graphics Programming weekly - Issue 94 — July 21, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-94/
author: Jendrik Illner
published: '2019-07-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- presents Axis-Aligned-Bounding-Tetrahedron (AABT) and Axis-Aligned-Bounding-Octahedron (AABO) as alternative approaches to axis-aligned Bounding Boxes (AABB) to build acceleration structures
- displays the data structures in 2D and extends into 3D
- showing results and possible proposals for more research into the topic

![](../../assets/7c5faefece0802dd.png)


- frame breakdown of a single frame in the Anki engine
- clustered deferred engine
- discussing shadows, Screen space ambient occlusion, global illumination, Volumetric lighting/fog, reflections, tone mapping, and compositing

![](../../assets/99a2d84123234c23.png)


- the article explains what wavefront path tracing is
- how it enables efficient path tracing on GPUs
- implementation provided in
[Lighthouse 2](https://github.com/jbikker/lighthouse2/blob/master/README.md)

![](../../assets/09c9e9e262030048.jpg)


- provides an overview of Vulkan pipeline caching
- list of possible problems that can be encountered
- different driver behavior and IO issues require user code validation
- shows the system used by Roblox to validate the cache

![](../../assets/9a116a7d87bde6da.png)


- slides for the High-Performance Graphics 2019 conference are now available
- topics include raytracing, 3D text rendering, denoising, many light techniques, shadows, VR and more

![](../../assets/6941c529d8595fa0.png)


- A Shadertoy that shows the different components the define physically based rendering
- with explanations and demos of the separate components

![](../../assets/c69e151c0531f2f3.png)

- GPU based validation in Vulkan has been updated
- now supports more cases, the article explains which are currently supported
- the whitepaper provides more details

![](../../assets/a3f9fbc38a572f93.jpg)


- Radeon GPU Analyzer can now compile compute shaders to the target ISA without having to have the GPU installed in the host machine
- the article explains how the shader compiler pipeline works and the different ways to express the required information

![](../../assets/568ea5beaff4106f.jpg)


- an article explains the dot product and how it relates to the plane equation

![](../../assets/25b12acbac04dfc6.png)


- shows how the dot product and axis define matrices
- dot products can be used to decompose effects onto the axis
- 3 axis represents a 3x3 matrix

![](../../assets/e7aed80ae766fddb.png)


- the article shows that with the inverse-transformation applied to a ray origin and direction
- intersection tests can be done against the untransformed geometry

![](../../assets/5ff4e8183c9833de.png)

Thanks to [Stephen Hill](https://twitter.com/self_shadow) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.