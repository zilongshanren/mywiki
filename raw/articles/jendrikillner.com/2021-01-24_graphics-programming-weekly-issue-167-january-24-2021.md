---
title: Graphics Programming weekly - Issue 167 — January 24, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-167/
author: Jendrik Illner
published: '2021-01-24'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the author provides an overview of anti-aliasing solutions
- what problems temporal techniques have, look at alternative solutions
- and experience trying to avoid using temporal techniques in a game production

![](../../assets/2a3fe923274a75bf.png)


- the article discusses the progress on an open-source graphics stack for Apple M1
- provides insights into how Apple GPU commands are expressed on the lowest level

![](../../assets/5b0763e4597ebb46.png)


- the video from GDC 2018 was released
- the talk presents different iterations of a system to allow particles emission from everything in the world
- contains many examples, pro/cons of several techniques
- shows how to unfold meshes so that particles can be emitted in a view independent fashion
- additionally provides insights into particle workflows

![](../../assets/bc8926dc20451bdb.png)


- the presentation provides an overview of the rendering pipeline from mesh creation to screen output
- focuses on the RDNA2 architecture, presenting what each piece of hardware in the pipeline is called and the function it serves
- providing insights into why specific workloads can achieve better performance than others

![](../../assets/42483740f7bce25c.png)


- talk provides an overview of the Crytek rendering pipeline
- how a Micro-G buffer is used to reduce the bandwidth required
- encoding, reconstruction errors, and performance comparison
- how the raytracing is implemented using compute shaders
- BVH data structures, using interlaced ray tracing for ray count reduction
- data optimizations for BVH objects

![](../../assets/df298707053eabd0.png)


- the article explains the process of porting the NAP creative coding Framework to Vulkan
- focuses on presenting the high-level concepts and considerations instead of API details
- presents synchronization, main API objects, frame setup, descriptor set management, mesh and texture handling as well as coordinate space conversions

![](../../assets/d2f140fdd2ba419c.jpg)


- the tutorial shows how to create procedural fractals
- enable color and position modifications
- present performance comparisons

![](../../assets/4604c5f1f2b3e17b.jpg)


- the article presents how a sand dune wallpaper was implemented using WebGL
- demonstrates how the scene was composed, dust particle implementation, wind simulation as well as texture
- source code is available

![](../../assets/04ee14b2006a199b.png)


- shows why normals need to be recalculated if a mesh shape is changed in a vertex shader
- presents how to re-calculate the normals by applying the same offsets to approximate neighbors and recalculating the normal from this
- simplified video version of
[How to Calculate Shader Graph Normals](https://gamedevbill.com/shader-graph-normal-calculation/)

![](../../assets/c954222ec9edffeb.png)

Thanks to [Vivitsu Maharaja](https://twitter.com/vivitsum) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.