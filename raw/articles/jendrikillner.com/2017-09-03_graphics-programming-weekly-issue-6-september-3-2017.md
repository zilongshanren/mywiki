---
title: Graphics Programming weekly - Issue 6 — September 3, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-6/
author: Jendrik Illner
published: '2017-09-03'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- targeting GLSL
- uisng metamorphic testing (generating families of programs that should yield identical results)
- sucesfully used to find driver bugs and security issues

- unbiased random sampling of points in a triangle using weights and barycentric coordinates
- focusing on sampling within a single triangle
- mentions sources for triangle selection algorithms

Describe a novel representation of the light field tailored to improve importance sampling for Monte Carlo rendering. We provide a reference open source implementation.


- similar ideas to FrameGraph in frostbite
- can execute multipe per frame, frostbite can do the same
- each pass can create, read, write to GPU resource
- additionally also allows inclusing of CPU resources

- how to hide polygon structure in map generations with noisy edges

- how to achieve stable barycentric coordinate ordering independent of vertex locations

- GPU based
- Voxelization on the GPU
- Cone tracing

Quick overview of:

- Understand the problem
- Understand the data
- Understand the algorithm
- Understand the latency requirements
- Remove waste

Main focus:

- Use the hardware to full effect


- Efficient peripheral rendering is fundamental for VR rendering
- Perceptual evaluations can expose opportunities for significant speedups