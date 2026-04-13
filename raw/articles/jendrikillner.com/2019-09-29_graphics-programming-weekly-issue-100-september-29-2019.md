---
title: Graphics Programming weekly - Issue 100 — September 29, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-100/
author: Jendrik Illner
published: '2019-09-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the presentation shows the new WIP hair rendering system
- a realtime system that is based on hair stands instead of cards
- strands are rasterized into shadow and deep opacity maps
- for performance reasons, a visibility buffer is written, and a sample deduplication pass is applied
- shading is done in a screen space pass
- shows how the different shading components have been implemented

![](../../assets/741cd61fd0ceb3a6.png)


- the article presents guided filtering as an alternative to a bilateral filter
- explains the bilateral filter logic and compares against guided filtering
- showing what the strengths and weaknesses of both approaches are

![](../../assets/61c900c2a1f4b54a.png)


- the new PIX CPU timeline view shows when a thread context switch happened and to where
- optimized shader access tracking, significant speedup when opening the pipeline view

![](../../assets/93327f67b13da42c.png)


- overview of denoising techniques in raytracing applications
- covering sampling and signal processing techniques
- additionally covers blurring kernels and spatial reprojection techniques

![](../../assets/02a803c96882f52d.jpg)


Ubisoft RedLynx is a multiplatform game development studio located in Helsinki. Along with the hugely popular Trials series, we have developed and published more than 100 games and we are a passionate team of over 140 people of 21 different nationalities. We are seeking an experienced Graphics Programmer to join our core technology team in creating impactful game experiences

![](../../assets/4cfddfae173473e2.png)


- performance comparison of a ray tracer application using native OpenGL against WebGL (Chrome, Firefox)
- The GPU performance is comparable on the D3D backend, even better at times

![](../../assets/e3e55149a2db9d0b.png)


- Unity tutorial showing how to set up a custom render pipeline
- covering how to set up the project
- cull, filter, and sort objects
- add support for multiple cameras

![](../../assets/85d250d8347f4e5c.jpg)


- overview video for the new DirectX Raytracing sample, showing a Raytraced Ambient Occlusion implementation

![](../../assets/72b0be7a99290651.png)



- provides an overview of the ocean rendering system
- the system is based around hierarchical, fully dynamic ocean data sources
- shows how to model waves, integrate shading and realistic flow patterns

![](../../assets/5c33e25e529345b2.jpg)

Thanks to Spencer Sherk for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.