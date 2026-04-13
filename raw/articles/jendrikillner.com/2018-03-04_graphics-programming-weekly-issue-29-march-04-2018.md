---
title: Graphics Programming weekly - Issue 29 — March 04, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-29/
author: Jendrik Illner
published: '2018-03-04'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Rendering in Camera Space(ish)](http://pharr.org/matt/blog/2018/03/02/rendering-in-camera-space.html) [[wayback-archive]](http://web.archive.org/web/20180304031506/http://pharr.org/matt/blog/2018/03/02/rendering-in-camera-space.html)

- shows effects of floating point precision loss far away from the origin
- transforms rendering to be relative to the camera position in the world instead of the origin of the world
- this makes rendering precision independent from the position in the world

[Vertex Formats Part 1: Compression](http://www.yosoygames.com.ar/wp/2018/03/vertex-formats-part-1-compression/) [[wayback-archive]](https://web.archive.org/web/20180304214334/http://www.yosoygames.com.ar/wp/2018/03/vertex-formats-part-1-compression/)

- overview of pros/cons for 16 bit position encoding formats
- considerations for UVs
- storing normals with
[QTangents](http://www.crytek.com/cryengine/presentations/spherical-skinning-with-dual-quaternions-and-qtangents)encoding

[Vertex Formats Part 2: Fetch vs Pull](http://www.yosoygames.com.ar/wp/2018/03/vertex-formats-part-2-fetch-vs-pull/) [[wayback-archive]](https://web.archive.org/web/20180304214358/http://www.yosoygames.com.ar/wp/2018/03/vertex-formats-part-2-fetch-vs-pull/)

- description of pull and fetch model
- extra flexibility when using the fetch model
- performance implications on different hardware architectures

[A level of detail method for blocky voxels](https://0fps.net/2018/03/03/a-level-of-detail-method-for-blocky-voxels/) [[wayback-archive]](https://web.archive.org/web/*/https://0fps.net/2018/03/03/a-level-of-detail-method-for-blocky-voxels/)

- small overview of Progressively Ordered Primitive (POP) buffer
- a way to encode LODs for models
- how to deal with LOD transition boundaries

[Screen-filling Rasterization using Screen-aligned Quads and Triangles](https://www.cginternals.com/en/blog/2018-01-10-screen-aligned-quads-and-triangles.html) [[wayback-archive]](http://web.archive.org/web/20180228031819/https://www.cginternals.com/en/blog/2018-01-10-screen-aligned-quads-and-triangles.html)

- comparison of 3 techniques (quad, triangle, nvidia fill_rectangle extension)
- explanation of the problems with the quad approach
- why the triangle or extension approach should be preferred

[Bringing Vulkan to Apple’s Platforms: Khronos Group Announces Open Source MoltenVK 1.0 & SDKs](https://www.anandtech.com/show/12465/khronos-group-extends-vulkan-portability-with-opensource) [[wayback-archive]](http://web.archive.org/web/20180226184027/https://www.anandtech.com/show/12465/khronos-group-extends-vulkan-portability-with-opensource)

- MoltenVK is open source, collaboration with valve
- a library for translating Vulkan to Apple’s Metal
- DOTA 2 is using this layer to run on macOS

- open source implementation of vulkan using metal on iOS and macOS

[Conservative rasterization in Vulkan](https://www.saschawillems.de/?p=2778) [[wayback-archive]](https://web.archive.org/web/20180304214430/https://www.saschawillems.de/?p=2778)

- example how to use conservative rasterization extension with vulkan
- shows results for a triangle render with/without the extension

[Deconstructing the water effect in Super Mario Sunshine](http://blog.mecheye.net/2018/03/deconstructing-the-water-effect-in-super-mario-sunshine/) [[wayback-archive]](http://web.archive.org/web/20180304054516/http://blog.mecheye.net/2018/03/deconstructing-the-water-effect-in-super-mario-sunshine/)

- how the water effect was implemented in the fixed function hardware of the GameCube
- based on scrolling textures
- each mip level is manually created to approximate separate effects based on camera distance

[Real-Time Rendering of Wave-Optical Effects on Scratched Surfaces](http://3dgraphics.guru/publication/real-time-iridescenet-scratches/) [[wayback-archive]](https://web.archive.org/web/20180304063057/http://3dgraphics.guru/publication/real-time-iridescenet-scratches/)

- model to simulate microscopic scratches on metal
- for spherical and polygonal light sources

[Implicit Surface Modeling](http://www.gradientspace.com/tutorials/2018/2/20/implicit-surface-modeling) [[wayback-archive]](http://web.archive.org/web/20180227044152/http://www.gradientspace.com/tutorials/2018/2/20/implicit-surface-modeling)

- explanation of implicit surfaces using signed distance fields
- how to apply operators to combine multiple shapes
- how to use the techniques with the
[C# - geometry3Sharp](https://github.com/gradientspace/geometry3Sharp)library

[Depth of Field - Unity Tutorial](http://catlikecoding.com/unity/tutorials/advanced-rendering/depth-of-field/) [[wayback-archive]](https://web.archive.org/web/20180304063232/http://catlikecoding.com/unity/tutorials/advanced-rendering/depth-of-field/)

- in-depth tutorial
- explanation of what depth of field is
- different bokeh effects
- simulating camera focus, separating background and foreground objects

[Unreal Engine 4 Cel Shading Tutorial](https://www.raywenderlich.com/186872/unreal-engine-4-cel-shading-tutorial) [[wayback-archive]](https://web.archive.org/web/20180304063216/https://www.raywenderlich.com/186872/unreal-engine-4-cel-shading-tutorial)

- cel shading uses multiple bands of color instead of a continuous gradient
- effect based on the lighting information in a post processing shader
- using a lookup table to control the amount of bands

- new and more flexible API, not backwards compatible
- reduced memory usage