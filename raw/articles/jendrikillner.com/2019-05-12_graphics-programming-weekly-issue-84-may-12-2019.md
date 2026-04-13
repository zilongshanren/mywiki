---
title: Graphics Programming weekly - Issue 84 — May 12, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-84/
author: Jendrik Illner
published: '2019-05-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- describes an alternative bounding structure that is based around axis aligned triangles
- starts with 2D example and extends the concepts to 3D
- comparison against other bound object representations

![](../../assets/203d71d14645c97f.png)


- overview video of papers that will be presented at SIGGRAPH 2019

![](../../assets/db83eb2103f12098.png)

- describes the cross-platform shader pipeline
- mix of json description files for state / constants / vertex layout / …
- code generator used to generate the final shader for compilation
- cross-compilation pipeline for platforms that don’t support HLSL

![](../../assets/287303da4a0e063f.png)


- Vulkan 1.1 will be a requirement on 64-bit devices starting with Android Q
[Thermal API](https://developer.android.com/preview/features#thermal)will be added to allow games to react to thermal status changes

![](../../assets/04bd2aa32376290a.png)


- tour of TensorFlow Graphics
- allows to define 3D scenes and run training on them
- system to allow bi-directional machine learning techniques

![](../../assets/6a62c2605fe03873.jpeg)


- presents the history of 2D printing and font formats
- shows problems with implicit curve evaluations
- discussion of implicit surfaces in regards to 2D rendering

![](../../assets/742c0f69ee2e7630.png)


- interview describing the reflections that have been implemented in the
[Neon Noir Demo](https://www.cryengine.com/news/crytek-releases-neon-noir-a-real-time-ray-tracing-demonstration-for-cryengine) - merging voxel and ray tracing data
- only tracing rays for mirror-like surfaces and the beginning of rays, otherwise tracing voxels instead

![](../../assets/6d5e8f8ee6d7c6fd.png)


- a method based on stochastic light culling
- hierarchical Russian Roulette using an approximate scattering lobe
- does not support perfectly specular surfaces

![](../../assets/1fe62f452ec986c3.png)


- brief Unity example that shows how to render a basic fur look
- combination of vertex offsets and alpha blending

![](../../assets/50f0ad8aefba2a51.png)

- overview about how to design a game to run all logic in Vulkan shaders
- compute shaders to run the game logic and updating the game state
- draw management is done using a compute shader and draw indirect is used for the final draw submission

![](../../assets/eeb140ee66ecc26d.png)


- Dynamic Diffuse Global Illumination
- overview of the evolution of several indirect illumination techniques
- how the method tries to solve the problem of Irradiance Probes
- summary of the implementation and evaluation in different scene contexts

![](../../assets/738e53622c84e8e0.jpg)


- reverse-engineering the cloud rendering of The Witcher
- uses a texture based approach, including normal mapping the clouds
- uses a sky gradient to lighten the clouds close to the sun

![](../../assets/e5b274b0d6c96f4b.png)


Thanks to [Aras Pranckevicius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.