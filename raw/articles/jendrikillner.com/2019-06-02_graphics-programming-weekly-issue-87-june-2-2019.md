---
title: Graphics Programming weekly - Issue 87 — June 2, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-87/
author: Jendrik Illner
published: '2019-06-02'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- presents how ray tracing is integrated into the High Definition Render Pipeline (HDRP)
- a brief overview of the Unity raytracing API integration
- shows how different effects have been implemented
- including optimizations and performance results

![](../../assets/046f248d25a0bf66.png)


- shows how to use HLSL to write a raytracing implementation using the Nvidia Vulkan extension
- uses recently added DXC support to compile the shaders
- updated docker image to provide the shader compiler support

![](../../assets/208da66b8bc464af.png)


- presents how the Unity demo was made
- overview of skin/hair/eye/teeth shading
- facial animations used scanned information, at runtime need to resolve positions for hair
- details about how the tentacles were created for the different use cases
- based on Hermite splines, signed distance fields and divergence-free noise and skinning

![](../../assets/3e065ebd7be12d35.jpg)


- overview of the deferred decal solution
- uses bindless resource binding model
- decals are part of lighting shader and don’t modify the Gbuffer
- presents use-cases, common problems, and optimizations for deferred decals
- includes a lot of code samples to explain the concepts

![](../../assets/a2dcffbe9673acb7.png)


- a new release, range profiler provides detailed metric graph about the performance of the application
- rules can be written to trigger custom performance warnings
- ray tracing acceleration structures can be exported and inspected independently

![](../../assets/9c1e8ad28b5957ea.png)


- summary of the Quake II path tracing implementation
- presented in 3 video parts with notes
- covering Path Tracing theory, denoising and the path tracer implementation

![](../../assets/c2489a19f57e46f5.png)


- Nvidia helper library to simplify the integration of Variable Rate Shading
- the user only needs to provide eye positions and select performance presets
- the library creates/updates/manages the required API resources

![](../../assets/be87ac94141efe2a.png)


- the author presents what makes a graphics system paper
- papers that introduce new systems and are not necessarily introducing new discoveries
- provides what paper authors and reviewers should focus on

![](../../assets/1b61b48a05abf8f7.png)


- new point based shadowing algorithm for local area lights
- better quality than single view and less performance required than multi-view solutions
- generate a multi-viewpoint pointset for the area light
- projecting points into many depth buffers at once

![](../../assets/4f680182e18bdd81.png)


- tutorial series covering Unity’s scriptable render pipeline
- explains how to combine real-time lighting with baked shadows

![](../../assets/9a6ee100162fe7d9.jpg)


- presentations that talks about the state of rendering
- how did we get to today’s state and what might be the next steps
- ideas about challenges, workflow, and research
- meant to challenge ideas and start a discussion

![](../../assets/3ba5ce038cb29daa.png)


- new representation approach for spectra
- shows use in offline raytracing and real-time D3D12 application
- a variable number of momements can be used to match quality and performance constraints
- the source provided in C++, HLSL, and Python

![](../../assets/7d5c1730f68b440d.jpg)

Thanks to [Matt Pharr](https://pharr.org/matt) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.