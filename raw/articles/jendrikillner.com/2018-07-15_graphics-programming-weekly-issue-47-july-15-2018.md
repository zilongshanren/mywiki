---
title: Graphics Programming weekly - Issue 47 — July 15, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-47/
author: Jendrik Illner
published: '2018-07-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

#
Graphics Programming weekly - Issue 47 — July 15, 2018

- explanation of partial derivates in pixels shader, (ddx, ddy in HLSL or dFdx, dFdy in OpenGL)
- the rate of change for variables in a 2x2 pixel grid
- how they are calculated, how they can be used to calculate face normals from world space positions
- how branches interact with derivative calculations


- explanation of SIMD execution details for GCN
- discussing latency, throughput, and scheduling
- introduction of instructions that allow multiple SIMD lanes to exchange information
- extra requirements for pixel shaders


- a technique to rotate vectors on the GPU using only integer math
- aims to take advantage of packed operations and scalar integer operations


- Colin Barré-Brisebois is looking for feedback and open problems in real time raytracing
- this will influence the HPG 2018 keynote


- how to calculate the bounding box for quadratic and cubic Bezier splines analytically


- changing the color parts of a character at runtime using a mask texture
- detailed visual explanation of why this works for fixed colors but causes an issue when giving the option to blend between two colors
- using premultiplied colors removes the artifacts


- explanation of how blending HDR values into an SDR render target behaves regarding clipping into the [0,1] range
- shows how using non-premultiplied HDR values results in incorrect results and how this can be fixed by the use of premultiplied alpha colors


- tutorial how to write a Metal app for iOS
- end results is a spinning, constant color teapot
- deals with loading models, handling vertex data, shaders, constants and drawing


- showcase of small rendering demos that showcase volumetric rendering effects


- explanation of dark and stormy, cloudy skybox shader for unity
- source code and example assets are available


- a technique to generate quadrilateral meshes from triangulated meshes
- won the Best Paper Award at Symposium on Geometry Processing 2018
- source code available


- a library that aims to provide a thin abstraction layer on top of OpenGL, D3D11, D3D12, Vulkan, and Metal


- GLSL implementation as a starting point for a temporal antialiasing solution


- bibliography of the Real-Time Rendering 4th edition
- 1978 references