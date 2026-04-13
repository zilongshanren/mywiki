---
title: Graphics Programming weekly - Issue 48 — July 22, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-48/
author: Jendrik Illner
published: '2018-07-22'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

#
Graphics Programming weekly - Issue 48 — July 22, 2018

- the history behind the release of the Disney datasets of large-scale scenes
- comparison of the scene rendered using Disney’s renderer and PBRT 3


- paper discussing the software implementation of the rasterization pipeline using compute shaders
- using a dynamic approach that adjusts to the workload dynamically
- comparison within environments taken from games to evaluate the pipeline overhead
- showcase of what kind of effects are possible with a software approach
- custom primitive rendering
- programmable blending
- adaptive supersampling

- in-depth performance comparison against hardware and other software approaches


- follow up series of 2012’s GPU Pro 3 model
- dynamic, real-time atmospheric model without pre-calculations
- explains aerial perspective and the Chapman approximation to optical depth


- showcase different ways to visualize a 2d flow field
- presentation of an algorithm that allows the creation of loopable animations from vector fields


- summary of “Conservative Z-Prepass for Frustum-Traced Irregular Z-Buffers” paper
- explanation of irregular z-buffer and conservative shadow maps and how they are combined


- mathematical derivations of importance sampling for GGX, Beckmann, and Blinn-Phong


- part 2 of the Metal tutorial
- adding support for depth buffers, some simple lighting with textures
- extending the application to support multiple lights, objects, and materials with some basic animations


- explanation of Vulkan render passes example
- how to create Render passes
- manage shader bindings for input attachments and how to use them from within the GPU shader


- start of a series about graphics engine architecture
- core design goals and pillars for the author’s graphics engine
- embrace concepts introduced in modern graphics APIs
- make job-based multi-threaded execution a first class citizen
- define a clear, small API, but be open towards extension



- a new vertex cache optimization algorithm that is able to improve cache usage on NVidia hardware by taking advantage of vertex batch sizes


- summary of the “Revisiting The Vertex Cache: Understanding and Optimizing Vertex Processing on the modern GPU” paper


- shader showcase of different waterfall effects


- explains what color inversion is and how to implement it using metal


- tutorial on how to use multi-pass shaders in unity to implement an outline drawing effect
- first pass object is drawn like usual
- in the second pass drawn with front face culling and slightly scaled up to define the outline