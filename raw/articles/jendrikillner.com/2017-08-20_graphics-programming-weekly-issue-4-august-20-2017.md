---
title: Graphics Programming weekly - Issue 4 — August 20, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-4/
author: Jendrik Illner
published: '2017-08-20'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- support d3d12 feature level 12_1
- HBCC supports 49-bit addressing
- on-demand paging of local memory across the PCIe bus
- all of the graphics blocks have been made clients of the L2 cache (no seperate color block caches)
- next-generation geometry (NGG) path
- Primitive shaders
- can discard primitives early, only position processing instead of whole vertex processing
- increasing maximum throughput from 4 primitives per clock to 17

- better work workload distributor
- can pack multiple small draws into a single wavefront

- support for 16 bit math
- Draw-Stream Binning Rasterizer (DSBR), a mix of tiling achitecture with intermediate-mode rendering

The most interesting part of this project compared to the other open-source Vulkan renderers so far is probably the render graph implementation.


Similar to the ideas presented in [https://www.slideshare.net/DICEStudio/framegraph-extensible-rendering-architecture-in-frostbite](https://www.slideshare.net/DICEStudio/framegraph-extensible-rendering-architecture-in-frostbite)

- discusses the Render graph implementation of Granite
- global render graph, all render components need to register with it
- gather global knowledge, optimize with that information
- render graph allocates resources and uses callbacks to execute the correct code
- can promote any texture as backbuffer source, the source texture will be presented on screen
- currently only aliases on perfect match with dimesions/formats/…
- gpu work generation
- validate, make sure everything makes sense
- traverse the graph and lay out the passes in gpu submission, starting at backbuffer and resolve dependencies starting from there
- render pass reordering: reorder so that unrelated work is between producer and consumer
- assigning physical resources to logical: aliasing resources
- merge render passes, using vulkan render pass concept
- build render pass barriers


- based on the solution discussed in
[GPU Pro 5](https://www.crcpress.com/GPU-Pro-5-Advanced-Rendering-Techniques/Engel/p/book/9781482208634) - discussed how to solve problems with the intersection code
- how to trace towards the camera
- how to trace behind surfaces
- contains source code

- use an unsteady delta frame time, set frame dt to a random value each frame
- sanity check: plot data over time. eg. log data + timestamp and plot in excel
- update anlysis, get a picture of the update order and dependencies
- 4 experiments to validate the update flow
- using timestamps to validate data dependencies

- Derivation of how to convert a color temperature to RGB values

The key to developing well performing real-time graphics applications is to know the limitations of your system, and work within those limits.


- aimed at indie developers on mobile
- simple guidelines how to calculate the budgets given a fixed GPU hardware
- how to use the MALI tools to detect how the game performs and compare it to the budget

- stb-inspired single-header library to simplify the core synchronization mechanisms in Vulkan

- deep learning overview
- how it was used to get a trained TAA

- Trying to achieve: Expressive power and flexibility, Subsecond iteration, performance
- “particle system”: collection of particles with same properties
- expressed as node-graph
- small overview of the shader system, look at
[GDC presentation](http://advances.realtimerendering.com/destiny/gdc_2017/Destiny_shader_system_GDC_2017_v.4.0.pdf) - exression evulations
- very flexible with all kinds of local and global inputs, react to collisions and more
- bytecode interpreter for expressions (CPU or GPU)
- for release, bake to shader code


- how we innovate on graphics techniques, usability, and performance
- what helps innovation:
- Easy sharing of reproducible behavior
- needsframrowkrs needs to support infrastructe but stay flexible
- heavy-weight complex engine architecture layers can be quite inhibiting to innovation

- evolution of graphics pipelines
- most innovation happens on the render pass level, not the lower levels (once the engine stabalized)
- unity’s scriptable render loop

- real time framework
- meany to help, easy to modify
- small overview of an example application