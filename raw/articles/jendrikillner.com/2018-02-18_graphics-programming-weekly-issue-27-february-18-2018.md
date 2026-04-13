---
title: Graphics Programming weekly - Issue 27 — February 18, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-27/
author: Jendrik Illner
published: '2018-02-18'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

[Descriptor Pool Challenges in Vulkan](https://timothylottes.github.io/20180215.html) [[wayback-archive]](https://timothylottes.github.io/20180215.html)

- looking at the descriptor pool problem with multiple worker threads
- variable workload makes it difficult to correctly size the pools
- discussions of workarounds
- proposal of a flag for lock-free descriptor allocation
- looking at the AMD driver code for viability


[The Machinery Shader System (part 1)](http://ourmachinery.com/post/the-machinery-shader-system-part-1/) [[wayback-archive]](http://web.archive.org/web/20180213044543/http://ourmachinery.com/post/the-machinery-shader-system-part-1/)

- base shader system includes
- authoring shaders and render states
- system for loading/reloading shaders
- passing constants and resources from game code to the shaders

- common problems with shader systems
- design goals for the new system
- walkthrough of the shader compiler interface

[HDR games analysed](https://www.resetera.com/threads/hdr-games-analysed.23587/) [[wayback-archive]](https://web.archive.org/web/20180216221023/https://www.resetera.com/threads/hdr-games-analysed.23587/)

- analyzed HDR screenshots from Xbox one
- luminance ranges of different games visualized as heat maps
- showcases HDR settings offered in different games

[Efficient Rendering of Linear Brush Strokes](http://jcgt.org/published/0007/01/01/) [[wayback-archive]](https://web.archive.org/web/20180214191320/http://jcgt.org/published/0007/01/01/paper.pdf)

- represents the stroke as a circle continuously sliding along the stroke axis
- stamp function is being numerically integrated per pixel, allows rendering in a single pass

[Efficient Rendering of Linear Brush Strokes - my graphics research paper explained](http://apoorvaj.io/efficient-rendering-of-linear-brush-strokes.html) [[wayback-archive]](https://web.archive.org/web/20180214191405/http://apoorvaj.io/efficient-rendering-of-linear-brush-strokes.html)

- additional information and simpler explanation of the paper
- more details about the problems of modeling the brush stroke discreetly

- implementation of rendering pipeline as graph of render tasks and resources
- based on the frostbite frame graph design shown at
[GDC 2017](https://www.gdcvault.com/play/1024612/FrameGraph-Extensible-Rendering-Architecture-in)

[Determining Triangle Geometry in Fragment Shaders](http://pcwalton.github.io/2018/02/14/determining-triangle-geometry-in-fragment-shaders.html) [[wayback-archive]](http://web.archive.org/web/20180215194638/http://pcwalton.github.io/2018/02/14/determining-triangle-geometry-in-fragment-shaders.html)

- how to calculate the screen space vertex positions in a pixel shader
- using the standard derivative functions dFdx and dFdy

[Khronos Announces glTF Geometry Compression Extension Using Google Draco Technology](https://www.khronos.org/news/press/khronos-announces-gltf-geometry-compression-extension-google-draco) [[wayback-archive]](http://web.archive.org/web/20180215150154/https://www.khronos.org/news/press/khronos-announces-gltf-geometry-compression-extension-google-draco)

- extension that allows storage of compressed geometry within gltf files
- up to 12x size reduction

- responds of the ACEs leadership to the
[ACES – Retrospectives and Enhancements](https://github.com/colour-science/aces-retrospective-and-enhancements/blob/master/aces_rae_2017.pdf)document - “The broadened scope of ACES beyond its original context will be accounted for with Video Games being a strong adoption driver to be reckoned with”

- AMD CPU profiler
- new GUI
- support for Ryzen processors

- added first iOS support
- many updates and fixes