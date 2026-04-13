---
title: Graphics Programming weekly - Issue 10 — October 1, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-10/
author: Jendrik Illner
published: '2017-10-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[real-time-rendering: an overview for artists](https://jesshiderue4.wordpress.com/real-time-rendering-an-overview-for-artists/) [[wayback-archive]](https://web.archive.org/web/20170930104713/https://jesshiderue4.wordpress.com/real-time-rendering-an-overview-for-artists/)

- overview of
- pbr
- render pipeline
- draw calls
- culling
- optimizations


[Design Patterns for Low-Level Real-Time Rendering](http://schd.ws/hosted_files/cppcon2017/e5/DesignPatternsForLowLevelRealTimeRendering.pptx) [[wayback-archive]](https://web.archive.org/web/20171002002353/http://schd.ws/hosted_files/cppcon2017/e5/DesignPatternsForLowLevelRealTimeRendering.pptx)

- overview
- GPU/CPU memory systems
- command lists
- GCN resource descriptors

- ring buffer
- both GPU and CPU
- returning CPU pointer for upload
- GPU for binding memory

- gpu work scheduling

[Physical Cameras in Stingray](http://bitsquid.blogspot.ca/2017/09/physical-cameras-in-stingray.html?m=1) [[wayback-archive]](https://web.archive.org/web/20171002002439/http://bitsquid.blogspot.ca/2017/09/physical-cameras-in-stingray.html?m=1)

- controlled by the same parameters a real world camera
- camera body
- sensor size
- iso sensitivity
- shutter speed

- lens
- focal length
- focus range
- aperture diameters

- allows override with artistic choices
- real world validation setup

[Compact Cube Meshes, and Compact Cube Meshes in Unity](https://yave.handmade.network/blogs/p/2629-compact_cube_meshes,_and_compact_cube_meshes_in_unity#13159) [[wayback-archive]](https://web.archive.org/web/20171002001832/https://yave.handmade.network/blogs/p/2629-compact_cube_meshes,_and_compact_cube_meshes_in_unity#13159)

- storing data in per-face data structures instead of vertices
- calculate face index in vertex shader and reconstruct vertex data

[Debug Draw with Cached Meshes & Vertex Shaders in Unity](http://allenchou.net/2017/09/debug-draw-with-cached-meshes-vertex-shaders-in-unity/) [[wayback-archive]](https://web.archive.org/web/20171002001957/http://allenchou.net/2017/09/debug-draw-with-cached-meshes-vertex-shaders-in-unity/)

- how to implement debug drawing using only Debug.DrawLine
- using cached meshes, with vertex shader modifications if possible
- dynamic batching breaks object space vertex shaders

[Microfacet-based Normal Mapping for Robust Monte Carlo Path Tracing](https://jo.dreggn.org/home/2017_normalmap.pdf) [[wayback-archive]](http://web.archive.org/web/20170930021904/https://jo.dreggn.org/home/2017_normalmap.pdf)

- solution for energy loss, backfacing normals
- model is symmetric, while classical normal maps are not
- adds some extra computational complexity compared to “classical” normal mapping

[Triangle Reordering for Efficient Rendering in Complex Scenes](http://www.jcgt.org/published/0006/03/03/) [[wayback-archive]](https://web.archive.org/web/20171002002553/http://www.jcgt.org/published/0006/03/03/paper.pdf)

- reduce overdraw and optimize vertex cache reuse
- uses keyframe animated model, breaking down into clusters and multiple index buffers
- optimize for different view directions
- select “best-fit” index buffer based on the view at runtime

[Half Tile Offset Streaming World Grids](https://blog.demofox.org/2017/09/30/half-tile-offset-streaming-world-grids/amp/) [[wayback-archive]](https://web.archive.org/web/20171001000156/https://blog.demofox.org/2017/09/30/half-tile-offset-streaming-world-grids/)

- proposes offsetting grid tiles by half a tile to reduce memory required in a streaming world

[Half-edge data structure considered harmful](https://sandervanrossen.blogspot.ca/2017/09/half-edge-data-structure-considered.html?m=1) [[wayback-archive]](http://web.archive.org/web/20171002002943/https://sandervanrossen.blogspot.ca/2017/09/half-edge-data-structure-considered.html?m=1)

- list possible problems with a half-edge data structure
- and a possible alternative (‘connected triangle’)