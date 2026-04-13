---
title: Graphics Programming weekly - Issue 19 — December 3, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-19/
author: Jendrik Illner
published: '2017-12-03'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[PIX 1711.28 – GPU memory usage, TDR debugging, DXIL shader debugging, and child process GPU capture](https://blogs.msdn.microsoft.com/pix/2017/11/30/pix-1711-28/) [[wayback-archive]](https://web.archive.org/web/20171130154929/https://blogs.msdn.microsoft.com/pix/2017/11/30/pix-1711-28/)

- can track d3d12 heap usage during timing captures
- experimental TDR (Timeout Detection and Recovery) debugging support
- shader debugging for DXIL (new intermediate shader language)
- GPU captures of child processes are supported
- file IO can now handle archive files to identify individual files within

[Foliage Optimization in Unity](http://www.eastshade.com/foliage-optimization-in-unity/) [[wayback-archive]](https://web.archive.org/web/20171202035939/http://www.eastshade.com/foliage-optimization-in-unity/)

- requires your forest to be built from the ground up with your optimization strategy in mind
all assets share a single 2048x2048 texture

hex grid for grouping

- LOD and culling on the hex groups
- occlusion query against the hex groups to see if visisble (only check against terrain)

super hex grid encompassing multiple smaller hex groups,

- switch to combined model for all meshes when at the lowest LOD


[Conformal Texture Mapping](http://reedbeta.com/blog/conformal-texture-mapping/) [[wayback-archive]](https://web.archive.org/web/20171128145211/http://reedbeta.com/blog/conformal-texture-mapping/)

- how to characterize the amount of distortion in UV mapping
- conformal maps are texture mapping without distortion
- explanation of Möbius tranformations
- Holomorphic Functions: functions that are complex differentiable
- Invertibility of functions

[Compressonator V2.7 - adds cross platform support and 3D Model compression with glTF v2.0](https://gpuopen.com/compressonator-v2-7-release-adds-cross-platform-support-3d-model-compression-gltf-v2-0/) [[wayback-archive]](https://web.archive.org/web/20171128145458/https://gpuopen.com/compressonator-v2-7-release-adds-cross-platform-support-3d-model-compression-gltf-v2-0/)

- now supports loading gltf 2.0 models
- D3D12 renderer
- Realtime 3D Model diff views

[Fast Lossy Compression of 3D Unit Vector Sets](https://perso.telecom-paristech.fr/~boubek/papers/UVC/) [[wayback-archive]](https://web.archive.org/web/20171128145646/https://perso.telecom-paristech.fr/~boubek/papers/UVC/UVC.pdf)

- a new compression scheme for unorganized ray directions
- take advantage of spatially coherent vector groups for better compressibility

[Lessons Learned While Building a Vulkan Material System](http://kylehalladay.com/blog/tutorial/2017/11/27/Vulkan-Material-System.html) [[wayback-archive]](https://web.archive.org/web/20171128145718/http://kylehalladay.com/blog/tutorial/2017/11/27/Vulkan-Material-System.html)

- descriptor sets
- group descriptor by frequency of update
- SPIR-V shader reflection
- constant data requires 16 byte alignment for members
- description of the material system

[Real-time Global Illumination by Precomputed Local Reconstruction from Sparse Radiance Probes](https://users.aalto.fi/~silvena4/Projects/RTGI/index.html) [[wayback-archive]](http://web.archive.org/web/20170918150216/https://users.aalto.fi/~silvena4/Publications/Real-time_Global_Illumination_by_Precomputed_Local_Reconstruction_from_Sparse_Radiance_Probes.pdf)

- aimed at mostly static scenes with fully dynamic lights and cameras
- reconstructing the incident radiance field from a sparse set of local samples
- minimize light leaking through visibility-aware interpolation
- receiver depends only on a small constant number of nearby radiance probes

[Telltale’s move to PBS : shifting technologies and practices (part 1)](https://www.gamasutra.com/blogs/FarhanNoor/20171128/310492/Telltales_move_to_PBS__shifting_technologies_and_practices_part_1.php) [[wayback-archive]](https://web.archive.org/web/20171128225518/https://www.gamasutra.com/blogs/FarhanNoor/20171128/310492/Telltales_move_to_PBS__shifting_technologies_and_practices_part_1.php)

- heavily relied on hand-painted texture maps, including lighting
- new material system can generate maya shader for preview
- some artists had a hard time adopting the PBR model
- use of scripts to auto convert from diffuse texture to the required PBR textures
- use of simplygon to simplify models and materials to fit into memory budget

[The Poor Man’s 3D Camera](http://etodd.io/2017/11/28/poor-mans-3d-camera/) [[wayback-archive]](http://web.archive.org/web/20171129083104/http://etodd.io/2017/11/28/poor-mans-3d-camera/)

- description of the many iterations the camera design went through until finally settling on the final design

[SeamCut: Interactive Mesh Segmentation for Parameterization](https://perso.telecom-paristech.fr/~boubek/papers/SeamCut/) [[wayback-archive]](https://web.archive.org/web/20171129200517/https://perso.telecom-paristech.fr/~boubek/papers/SeamCut/SeamCut.pdf)

- interactive approach to UV unwrapping
- using mesh surface properties instead of actual connectivity on the mesh
- to place cuts and seams for good UV distribution


[Breakdown : Making the Hair on The Division](http://airship-images.com/division-hair-breakdown/) [[wayback-archive]](http://web.archive.org/web/20161120025816/http://airship-images.com:80/division-hair-breakdown/)

- combination of meshes, flowmaps and hair planes

[Quick Peek: Ambient Occlusion](http://www.snaregames.com/2017/12/01/quick-peek-ambient-occlusion/) [[wayback-archive]](https://web.archive.org/web/20171201205146/http://www.snaregames.com/2017/12/01/quick-peek-ambient-occlusion/)

- AO calculations for low poly look using surfel representation of the mesh

[Simplicial Complex Augmentation Framework for Bijective Maps](https://cs.nyu.edu/~panozzo/#publications) [[wayback-archive]](http://web.archive.org/web/20171201030900/https://cs.nyu.edu/~panozzo/)

- aims to reduce the problem from a global to a local optimization problem
- iterative algorithm until quality reaches the expected threshold
- application shown in UV mapping and mesh deformation

[Light Map in “Seal Guardian”](http://simonstechblog.blogspot.ca/2017/11/light-map-in-seal-guardian.html?m=1) [[wayback-archive]](https://web.archive.org/web/20171201205437/http://simonstechblog.blogspot.ca/2017/11/light-map-in-seal-guardian.html?m=1)

- build UV atlas, render positions into texture
- bake cube map per pixel of the light map
- stored as SH luma and average chroma in two RGBA8 textures

- Shadertweak is an iPad app that allows you to rapidly prototype fragment shaders in the Metal shading language.