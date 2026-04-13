---
title: Graphics Programming weekly - Issue 44 — June 24, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-44/
author: Jendrik Illner
published: '2018-06-24'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

Graphics Programming weekly - Issue 44 — June 24, 2018
discusses problems with synchronization between unrelated work when using a single command queue
showcases how two command queues can achieve better overall utilization at the cost of longer latency

explanation of the simball environment that has been initially designed for the Maxwell Renderer
descriptions of the different object features, what they are designed to provide tests for and how it’s supposed to be used

shows how Zelda uses an FX in world space to make objects visible in high grass by adjusting the position of the effect based on the environment
fix clipping with the object by offsetting the FX towards the camera

twitter thread with a checklist of common problems that can cause objects not be rendered in OpenGL / D3D

the technique that mixes rasterization and temporal antialiasing to only ray trace pixels where a classification algorithm determines that TAA will not produce good results

C++ source code and prebuild demo application are released

The decals are projected from world space onto the mesh UV and rendered into separate per-object decal textures

optimizations to raytracer using SIMD
extending AABB tests to deal with various edge cases

a new set of SDR ODT (Output Device Transforms)
first Output Transforms that combine the RRT (Reference Rendering Transform) and ODT (Output Device Transforms) into a single transform

shows how the runtime/compile time selection feature of the Rust programming language is used to select different SSE intrinsics based on the available hardware

overview of rendering API support for the user of Roblox
Metal reaches above 60% on MacOS and D3D11 77% on Windows
on Android, Vulkan is available on 20% of devices

new sdk contains VK_KHR_get_display_properties2 and VK_KHR_draw_indirect_count extensions