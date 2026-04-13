---
title: 'A Decade of Metal: The Early Years (2014–2019)'
url: https://metalbyexample.com/a-decade-of-metal-early-years/
published: '2024-06-10'
source_blog: Metal by Example
source_site: https://metalbyexample.com
category: graphics
fetched: '2026-04-13'
---

## Introduction

In 2014, when Apple introduced the Metal graphics API, the landscape of computer graphics APIs was dominated by long-established standards like OpenGL. Seismic shifts were afoot, however, with the [announcement of DirectX 12](https://www.anandtech.com/show/7889/microsoft-announces-directx-12-low-level-graphics-programming-comes-to-directx/2) a few months prior and the [initiative](https://www.khronos.org/news/permalink/glnext-the-future-of-high-performance-graphics-presented-by-valve-at-gdc) that would produce [Vulkan](https://www.khronos.org/news/press/khronos-releases-vulkan-1-0-specification) starting to take shape. These parallel efforts signaled a significant shift away from the accumulated cruft of 20+ years of OpenGL and other APIs born during the fixed-function era of GPUs.

In a world where open standards are often preferred by developers, Apple’s choice to pivot to a proprietary solution was a calculated risk. Apple was aiming to evolve their closely integrated software and hardware platforms independently of input from competing industry interests, a goal that would only grow more strategically important throughout the [transition to Apple silicon](https://en.wikipedia.org/wiki/Mac_transition_to_Apple_silicon). In spite of hearing frequent complaints about Metal’s idiosyncrasies, I believe that the first decade of Metal has been a resounding success.


My own experience with Metal began shortly after it was first unveiled at WWDC 2014. Having worked at Apple for a little over a year at that time, I felt that it was time for a change of emphasis in my career, and Metal became the vehicle for that change. I left Apple at the end of June, established this blog in August, and spent the next 14 months exploring and writing about graphics on iOS. Since then, I have held positions at Apple and Meta (née Facebook) and have consulted on scads of projects as an independent contractor, but Metal has remained a through-line of my career.

So I wanted to take the opportunity, in the season of Metal’s tenth anniversary, to take a look back at the API’s history and evolution and, perhaps, steal a glimpse of its future.

## 2014 – Metal 1.0

Metal debuted as an iOS-exclusive framework with the release of iOS 8 in the fall of 2014. It offered a streamlined API that focused on reducing driver overhead, in part by requiring fixed-function state (such as alpha blending and vertex attribute layout) to be specified prior to the submission of draw calls. Metal 1.0 also included support for recording commands across multiple threads simultaneously, reducing the time spent by the CPU to prepare frames. At the time, Apple touted Metal’s ability to deliver up to 10 times better draw call performance compared to OpenGL, which was a critical improvement for rendering complex scenes with many objects.

Another crucial innovation of the era, compute shaders were also included in Metal 1. Although GPUs had been used as general-purpose processors for over a decade, the introduction of CUDA in 2007 and OpenCL 1 in 2009 unlocked a much more streamlined general-purpose programming model for GPUs. Metal’s compute shader support similarly enabled GPGPU techniques on A7 processors, and although compute performance wasn’t spectacular in these early SoCs, it improved drastically in later systems. Both graphics shaders and compute shaders are written in the Metal Shading Language, a C++ based language with custom GPU-centric features.

Although Metal was competitive feature-wise with OpenGL, it did lack some features found in its contemporary APIs, notably indirect draw commands and tessellation (and less notably, dual-source blending). These features and many more would be introduced in subsequent releases.

## 2015 – Metal on the Mac

The arrival of Metal on the Mac had been hotly anticipated for many months by the time WWDC 2015 rolled around and with it, beta versions of iOS 9 and OS X 10.11 (“El Capitan”). The sophomore release of Metal in September saw its debut on the Mac, along with a pair of new cross-platform utility frameworks: [MetalKit](https://developer.apple.com/documentation/metalkit) and [MetalPerformanceShaders](https://developer.apple.com/documentation/metalperformanceshaders).

MetalKit greatly simplified the process of getting rendered content onto the screen, thanks to the cross-platform [ MTKView](https://developer.apple.com/documentation/metalkit/mtkview) view class. MetalKit also included utilities for loading textures and interchanging mesh data with the newly introduced

[Model I/O](https://developer.apple.com/documentation/modelio)asset import-export framework.

MetalPerformanceShaders included a large variety of pre-compiled compute kernels to simplify tasks in image processing and linear algebra, presaging Metal’s future significance as the low-level API for machine learning tasks on Apple platforms.

The Metal framework itself saw a number of added features. Most significant among these was the addition of indirect dispatch and indirect draw commands, which made it easier to drive compute and render tasks with the GPU itself. Through a combination of compute kernels and draw commands, one could dynamically select the base vertex, base index, instance count, and other parameters of a draw call, enabling use cases like GPU-side frustum culling, among others. Indirect draw was an important addition as it was already present in contemporary APIs OpenGL 4.0 and OpenGL ES 3.1.

## 2016 – Feature Parity and Beyond

The 2016 release of Metal, tied to iOS 10 and macOS 10.12, brought it closer to parity with DirectX 12 with the addition of tessellation. Tessellation, a technique for dividing larger primitives called *patches* into many smaller triangles, can be used to dynamically add greater geometric detail to meshes without having to explicitly store the subdivided mesh in memory.

Metal’s approach to tessellation differs somewhat from OpenGL. In OpenGL, the vertex shader runs first, then the tessellation control shader (TCS) generates tessellation factors, per-control point attributes, and other user data. The tessellator (“tessellation engine” in GL parlance) then produces the vertices of the subdivided patch as a stream of normalized coordinates, which are processed by another programmable stage called the the tessellation evaluation shader (TES). The TES consumes the patch vertex coordinates and combines them with the previously produced control point attributes and other data to create the output stream of vertices consumed by the [primitive assembly stage](https://www.khronos.org/opengl/wiki/Primitive_Assembly).

Metal by contrast, leverages compute shaders for the first stage of the tessellation process. A compute shader can optionally be used to produce tessellation factors at whatever rate the programmer deems necessary: static, per-draw, per-patch, or any other cadence. The compute function writes the tessellation factors into a buffer so they can be consumed by subsequent patch draw calls. Issuing a patch draw call causes the fixed-function tessellator to read the tessellation factors and subdivide the patches into their constituent triangles. A programmable *post-tessellation vertex function* is then invoked to allow the programmer to interpolate patch control point attributes for each output vertex.

For a more complete introduction to tessellation in Metal, see [this article](https://metalbyexample.com/tessellation/).

Another significant introduction to Metal in 2016 was a new memory management object called a [heap](https://developer.apple.com/documentation/metal/memory_heaps). Before heaps, all Metal resources (buffers and textures) were allocated individually. With the addition of heaps, resources could be sub-allocated out of a larger region of memory. Moreover, regions of a heap could be made *aliasable*, allowing them to be reallocated to other resources more efficiently than destroying and recreating resources backed by individual allocations. Heaps would only increase in importance over time as features like argument buffers and manual hazard tracking became available.

This release of Metal also enabled dual-source blending on the Mac (it would become available on iOS in the subsequent release). Dual-source blending is an infrequently used feature used to achieve subpixel antialiasing of text (perhaps among other esoteric use cases).

## 2017 – GPU Driven Rendering Revamped

2017 was a major year for Metal. It saw the release of Metal 2.0, which included a bevy of new features in support of GPU-driven rendering. This release came along with iOS 11 and macOS 10.13, but it was really the fall’s hardware releases that made its power evident.

This was the year of the [A11 Bionic](https://mashable.com/article/inside-apple-a11-bionic-and-silicon-team), a chip that unlocked numerous efficiencies in on-tile rendering through the use of features like [imageblocks](https://developer.apple.com/videos/play/tech-talks/603) and [tile shaders](https://developer.apple.com/videos/play/tech-talks/604). The tile shader stage enabled compute work and render work to be interleaved in a single command encoder for the first time.

Metal 2 also introduced the first iteration of argument buffers, a powerful mechanism for reducing the number of API calls necessary to switch the active set of resources between draw calls. This first swipe at an argument buffer API would later be deprecated, and there were significant constraints on the number of resources that could be bound on some GPUs. Even so, argument buffers heralded a new era of GPU-driven rendering and even lower CPU overhead on the way to the promised land of fully bindless rendering.

This generation of Metal also enabled [nonuniform threadgroup sizes](https://developer.apple.com/documentation/metal/mtlcomputecommandencoder/2866532-dispatchthreads) on some hardware, which was a significant upgrade in ease of dispatching oddly shaped compute grids. It’s now taken for granted, but if you ever wrote something like `(gridSize.x + threadgroupSize.x - 1) / threadgroupSize.x`

, perhaps you can appreciate not having to fiddle with that anymore.

## 2018 – Raytracing, Take One

Raytracing was in the air in 2018. That summer, Nvidia announced their next generation architecture, Turing, which became available to consumers in the form of the GeForce 20 series of GPUs.

Raytracing arrived in Metal in the form of the `MPSRayIntersector`

class and accompanying APIs. It included support for hierarchical, instanced acceleration structures. Although this first attempt at a raytracing API would later be deprecated, it did presage future platform advancements, particularly the raytracing support that emerged in subsequent hardware generations.

Indirect command buffers (ICBs), another new feature in iOS 12 and macOS 10.14, allowed recording of commands into buffers, which could be reused. Analogous to OpenGL’s `glMultiDrawElements[Indirect]`

and DirectX’s [bundles](https://learn.microsoft.com/en-us/windows/win32/direct3d12/recording-command-lists-and-bundles), ICBs allowed programmers to record commands once and re-execute them efficiently, in significant contrast to the long-lived one-time-use command submission model.

## 2019 – A13 Bionic

Metal’s 2019 release was originally expected to be marketed as Metal 3, but the real Metal 3 wouldn’t arrive for a few more years. Instead, Metal 2.2 appeared in iOS 13 and macOS 10.15 that year. At the time, I wrote an [overview](https://metalbyexample.com/new-in-metal-3/) of the wide variety of features it introduced. This release accompanied the fall release of the A13 Bionic processor in the iPhone 11 base and flagship models, and other devices of that generation.

Looking back, I failed to appreciate the significance of [sparse](https://developer.apple.com/documentation/metal/mtlheaptype/sparse) heaps as a means of supporting texture streaming and video memory budgeting. Even today, this feature is probably underutilized by most Metal apps.

Furthermore, being able to set render and compute pipelines in argument buffers from the GPU enabled almost total decoupling of CPU and GPU work, as the GPU can now dynamically enqueue truly arbitrary work from a single compute function invocation.

This release is also when we got a first glimpse of APIs that would later be useful in the context of spatial computing. One such feature is rasterization rate maps, which allow developers to specify regions of the rendered image which should be shaded at lower resolution (so-called “variable-rate rasterization”). Most saliently in the “spatial computing” era, rasterization rate maps are used by visionOS’s Compositor Services to tune the rate at which frames are rendered on the Apple Vision Pro, a technique called *foveated rendering*.

As another boon for rendering efficiency, Metal 2.2 on iOS introduced vertex amplification, a technique for reducing the overhead of vertex stream processing when rendering to multiple render targets, as to the faces of a cube map or to separate render targets for stereo (AR, VR, etc.) rendering. Although vertex amplification could previously have been simulated with instancing, the use of built-in vertex amplification combined with the `render_target_array_index`

attribute made it easier than ever to render the same geometry through multiple viewports to multiple render destinations. (Vertex amplification would arrive on the Mac in the subsequent release.)

The innovations introduced in Metal in 2019 are well explained in a session from that year’s WWDC: [“Modern Rendering with Metal”](https://developer.apple.com/wwdc19/601). It discusses classic deferred rendering, tiled deferred rendering, and forward rendering, with an emphasis on GPU-driven rendering and techniques for reducing memory bandwidth usage.

## Outro

The first five years of Metal’s public availability saw it grow from a fairly barebones first offering to a GPU-driven rendering powerhouse, but the story had only begun. In a future article, we’ll look at subsequent generations of Metal and how it became a core technology for machine learning, spatial computing, and many more Apple platform features.

-
Apple enthusiastically supported OpenCL at the time of its debut, but Apple’s OpenCL implementation was largely left to languish after the introduction of Metal, and it was deprecated alongside OpenGL in 2018.
[↩](https://metalbyexample.com#fnref-944-1)

MikaelGood summary of the first baby steps of Metal.

Looking forward to the coming article(s).

JVThank you, Warren, for all the good work done. Please keep it up. Looking forward to future posts.