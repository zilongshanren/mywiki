---
title: Graphics Programming weekly - Issue 49 — July 29, 2018
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-49/
author: Jendrik Illner
published: '2018-07-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

#
Graphics Programming weekly - Issue 49 — July 29, 2018

- explanation of frame stuttering
- provides videos and frame by frame comparisons of what is causing the stutter
- explains how the discrepancy between measured time and actual present time causes the studdering issue
- current state of graphics API ecosystem in solving this problem



- shadertoy implementations of multiple noise types
- the comments describe improvements and possible optimizations to the used noise types



- shadow technique for local area lights
- based on the generation of view independent point clouds from dynamic triangle meshes and the rendering of multiple depth maps simultaneously
- proposes two different implementations
- performance and quality comparison against PCSS (percentage closer soft
shadows) and Multi-view rasterization (MVR)



- part 3 of the series about Grassmann for computer graphics
- combines the concepts of bi-vectors / tri-vectors with dual vectors
- explaining use cases


- explains how GPUs are able to execute multiple execution streams to hide memory latency
- how the different workloads of CPU and GPU lead to differences in the design of caches



- added support for visualizing the content of DirectX Raytracing shader tables
- able to detect invalid data in the table and warn about it


- explanation of a geometry shader in Unity that converts a triangle mesh into camera facing quad particles



- explains how to calculate luminance and a very brief overview of the human vision



- look at image shaders that modify brightness, contrast, exposure, gamma or saturation using Metal


- overview of water rendering starting from the early 90s to the early 2000s