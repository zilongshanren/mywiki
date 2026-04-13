---
title: Graphics Programming weekly - Issue 50 — August 5, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-50/
author: Jendrik Illner
published: '2018-08-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

#
Graphics Programming weekly - Issue 50 — August 5, 2018

- great in-depth discussion of the full PBR rendering pipeline, documentation for the
[Filament engine](https://github.com/google/filament)
- base BRDF model, extended with support for clear coat layer, anisotropic surfaces, and cloth
- explanation of lighting units and implementations for directional, point and spotlights
- providing GLSL code snippets
- a short overview of the clustered forward shading implementation
- information about how to validate a PBR implementation


- physically based shading model implemented using D3D11, D3D12, Vulkan and OpenGL 4.5
- each backend is implemented in a single .h and .cpp file


- shows algorithms for generating random points within a sphere
- contains interactive visualizations that make it easy to see the quality of the distribution



- breakdown of a burning shader implemented in Unreal Engine
- uses flow maps and world space positioned spheres to influence the fire


- part two of the series providing an introduction to vertex shaders
- shows how to add a custom vertex shader to a basic unity shader, sample textures, pass data from vertex to pixel shader and modify vertex positions



- summary of the paper: “View-warped Multi-view Soft Shadows for Local Area Lights ” discussed in
[last weeks](/post/graphics-programming-weekly-issue-49) issue
- a real-time technique for soft shadows



- shows how to measure Cuda copy performance using the tools contained in the SDK
- how to speed up the application with the collected performance information



- the article discusses how to calculate the central axis from a 3D mesh
- the axis is computed as maximal perpendicular to the area-weighted surface normal of the mesh



- explains how to use MSAA when using Vulkan
- how to detect the supported sample count, set up the render targets and make the necessary adjustments to the render passes
- shows how to enable sample shading to further improve quality on the inside of polygons


- twitter thread that provides a large number of links to information about volume rendering



- provides the Vulkan specification in a chunked version
- the original specification is one large HTML file that causes usability issues


- AMD provides a XML file that offers the possibility to map from external driver version to the contained Vulkan driver version


- Xenko, a C# based game engine has been released as open source with an MIT license



- collection of many 3D graphics research papers for a large number of different topics (sorted by topic)



- OpenGL ES implementation using Vulkan
- licensed as LGPL v3