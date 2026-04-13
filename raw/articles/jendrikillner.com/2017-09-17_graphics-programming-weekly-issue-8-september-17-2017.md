---
title: Graphics Programming weekly - Issue 8 — September 17, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-8/
author: Jendrik Illner
published: '2017-09-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[About GPU Family 4 - Metal 2.0](https://developer.apple.com/documentation/metal/about_gpu_family_4) [[wayback-archive]](https://web.archive.org/web/20170912203740/https://developer.apple.com/documentation/metal/about_gpu_family_4)

- tile-based deferred rendering (TBDR)
- imageblocks
- tile memory that can be acessed from the shader to create custom, tile local storage
- can be shared between compute, and rasterization

- tile shading
- new programmable stage, allow access to all data stored in tile memory

- raster order groups
- threadgroup sharing

more details can be found in the videos: [https://developer.apple.com/videos/metal/](https://developer.apple.com/videos/metal/)

[Headless Vulkan examples](https://www.saschawillems.de/?p=2719) [[wayback-archive]](https://web.archive.org/web/20170918032213/https://www.saschawillems.de/?p=2719)

- how to run compute and graphics work without creating a window

[Photoshop Blend Modes Without Backbuffer Copy](http://www.elopezr.com/photoshop-blend-modes-in-unity/) [[wayback-archive]](https://web.archive.org/web/20170918032931/http://www.elopezr.com/photoshop-blend-modes-in-unity/)

- how to use shader logic and blend modes to replicate photoshop blend modes

[Road to Anti-Aliasing in BRE: Rasterization](https://nbertoa.wordpress.com/2017/09/11/road-to-anti-aliasing-in-bre-rasterization/amp/) [[wayback-archive]](https://web.archive.org/web/20170912192550/https://nbertoa.wordpress.com/2017/09/11/road-to-anti-aliasing-in-bre-rasterization/amp/)

- explanation of rasterization algorithmn
- basic overview of display technology

- Support for persistently mapped allocations, custom memory pools, defragmentation, better support for GPU memory oversubscription

[Diffuse albedo database](http://www.patapom.com/topics/WebGL/passmwalbedo/) [[wayback-archive]](https://web.archive.org/web/20170913185607/https://gist.github.com/donmccurdy/de7ff6c44ecd76fddf1ecad170a114a8)

- provides rough albedo value references for many materials
- author description on twitter:
[https://twitter.com/Patapom2/status/907952278228914177](https://twitter.com/Patapom2/status/907952278228914177)

- USD
- OpenSubdiv
- Hydra
- also supports VR

- RTP (real-time previewer)
- presto animation system
- Pele (hair and fur simulation)

[The Artful Shape of Functions](https://bekwnn.github.io/2017/09/14/the-artful-shape-of-functions.html) [[wayback-archive]](https://web.archive.org/web/20170918013334/https://bekwnn.github.io/2017/09/14/the-artful-shape-of-functions.html)

- examples of basic math concepts that can be used to animate
- Ocean Waves: (using sin layering)
- Bezier Curve
- Gradients

[Seamless: Seam erasure and seam-aware decoupling of shape from mesh resolution](http://cragl.cs.gmu.edu/seamless/)[[wayback-archive]](https://web.archive.org/web/20170918032019/http://cragl.cs.gmu.edu/seamless/)

- techinuque to remove seams from existing textures without requiring changes to the mesh
- mesh decimation technique that is seam aware to reduce artifacts
- Seam straightening mesh processing to increase number of edges that can be collapsed

source code:
- [Texture Seam Erasure](https://github.com/zfergus/seam-erasure)
- [Seam-aware mesh decimater](https://github.com/songrun/SeamAwareDecimater)

paper: [paper](http://cragl.cs.gmu.edu/seamless/Seamless-%20Seam%20erasure%20and%20seam-aware%20decoupling%20of%20shape%20from%20mesh%20resolution%20(Songrun%20Liu,%20Zachary%20Ferguson,%20Alec%20Jacobson,%20Yotam%20Gingold).pdf)
[[wayback-archive]](https://web.archive.org/web/20170918031635/http://cragl.cs.gmu.edu/seamless/Seamless-%20Seam%20erasure%20and%20seam-aware%20decoupling%20of%20shape%20from%20mesh%20resolution%20(Songrun%20Liu,%20Zachary%20Ferguson,%20Alec%20Jacobson,%20Yotam%20Gingold).pdf)

[Normal Mapping for a Triplanar Shader](https://medium.com/@bgolus/normal-mapping-for-a-triplanar-shader-10bf39dca05a) [[wayback-archive]](https://web.archive.org/web/20170918031708/https://medium.com/@bgolus/normal-mapping-for-a-triplanar-shader-10bf39dca05a)

- quick overview of what is triplanar mapping and tangent space normals maps
- explanation of different normal mapping techniques with unity shader code
- different texture blending techniques

[More Resources for Universal Windows Platform Games with Fall Xbox One Update](https://blogs.windows.com/buildingapps/2017/09/15/resources-universal-windows-platform-games-fall-xbox-one-update/amp/) [[wayback-archive]](https://web.archive.org/web/20170918031855/https://blogs.windows.com/buildingapps/2017/09/15/resources-universal-windows-platform-games-fall-xbox-one-update/amp/)

| Category | Before | Now |
|---|---|---|
| CPU | 4 shared cores | 6 exclusive cores |
| GPU | 50% D3D11 | 100 % with D3D12 |
| RAM | 1 GB | 5GB |

[Sorting with GPUs: A Survey](https://arxiv.org/pdf/1709.02520.pdf) [[wayback-archive]](https://web.archive.org/web/20170912183651/https://arxiv.org/pdf/1709.02520.pdf)

- lists a large number of GPU sort algorithms with sources and compares them
- using a nvidia hardware model