---
title: Graphics Programming weekly - Issue 43 — June 17, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-43/
author: Jendrik Illner
published: '2018-06-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

Graphics Programming weekly - Issue 43 — June 17, 2018
how to use two Vulkan queues to enable optimal scheduling for compute-shader based post-processing
discussion how fragment → compute can introduce bubbles on the hardware
uses two software queues with semaphore synchronization to overlap early work in the frame of the following frame with the post-processing work of the previous frame

explanation of to use Monte Carlo integration to calculate the area under a curve
extending the system to deal with non-uniform random numbers distributions
convergence can be faster when using a distribution that is a closer match to the signal that is being sampled

timing capture now visualizes fence signal and wait
fences can be named
shader edit and continue workflow improvements
shader resource tracking for DXIL shader

shader playground added support for slang
a shader language that extends HLSL to make it more modular and extensible
ability to shows the control flow graph in GraphViz ‘dot’ form for SPIRV

using lookup tables to precompute the endpoints better compression results
different number of lookup tables allow tradeoffs in performance, quality and memory usage

talks from Microsoft at GDC are online

discusses the history and design of their in-house procedural texture generation tool

discussion of the photogrammetry workflow
camera used to capture, tools to generate the mesh and normals
using unity Unity’s DeLighting tool to remove shadows are even present on an overcast day
Tree assets are created with a mix of scans, 3ds max plugins, and quixel megascans assets
a fluid solver is used to calculate the flow map for the wind, shape exploration and VFX generation

overview of all the post effects that can be found in PostFX v2
code is on github

explains the basic of path tracing used in his D3D12 path tracer

discusses engines, frameworks, abstraction layers that support metal

QT adds support for vulkan on macOS through MolenVK