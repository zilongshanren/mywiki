---
title: Graphics Programming weekly - Issue 42 — June 10, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-42/
author: Jendrik Illner
published: '2018-06-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

#
Graphics Programming weekly - Issue 42 — June 10, 2018

- this in-depth document (26 pages) covers how real-world measurement is used to achieve correct lighting in call of duty
- explanation of camera concepts
- getting relative EV differences between light and shadowed areas is more important than having absolute correct values
- how having consistent measurements between the real world and in-game allowed numerous issues to be discovered and fixed
- the exposure handling required for the sizeable dynamic range of the scene
- how to capture accurate HDR photographs, albedo textures, and specular gloss


- an in-depth overview of color, color spaces, and color transformations
- discussion of HDR standards
- ACES pipeline overview
- implementation of HDR pipeline covering
- tone curve, display mapping, UI rendering
- universal CLUT and color grading



- look at solution developed by Imageworks compensates for the energy loss in a single bounce BRDF model
- improvements to the model


- proposal of how to group vulkan resources by usage type
- designed for coloring in the
[VulkanMemoryAllocator](https://github.com/GPUOpen-LibrariesAndSDKs/VulkanMemoryAllocator)


- Apple will start to deprecate OpenGL with macOS 10.14 and OpenGL ES with iOS 12
- developers should be using Metal instead


- how to generate command buffers in parallel on the CPU
- metal can analyze data dependencies to insert GPU parallelization automatically
- explicit control is supported but requires explicit opt-in
- how to build a GPU driven rendering pipeline using indirect command buffers and argument buffers
- look at image blocks, programmable blending, tile shading, persistent thread group memory, custom multi-sample color resolve
- lessons learned from bringing Fortnite: Battle Royale to iOS


- twitter thread with advice how to learn more advanced graphics programming topics


- a tutorial that explains how to clip a polygon based on a list of lines in a pixel shader



- derivation of a ray function that implements the effects of a thin lens on rays


- looks at different file formats and discusses the difference between formats aimed at the interchange of information or consumption only
- formats covered: gltf, fbx, alembic, USD,
- a brief look at application and engine support


- video presentations from the Vulkanised conference


- a sample that shows how to use the VK_KHR_multiview Vulkan extension