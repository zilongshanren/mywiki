---
title: Graphics Programming weekly - Issue 15 — November 5, 2017
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-15/
author: Jendrik Illner
published: '2017-11-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- explanation of GPUs
- overview of GPU execution model
- latency hiding
- register usage

- many compiler internals
- optimizations and trade-offs that need to be considered

- uniformity hoisting

- compiler is able to extract constants and run as part of low frequency kernels
- saves power and performance
- even hoisting a single add is a win on apple hardware


[Screen Space Ray-Traced Global Illumination: Toughest Challenge in Real-Time 3D](https://80.lv/articles/ssrtgi-toughest-challenge-in-real-time-3d/) [[wayback-archive]](http://web.archive.org/web/20171101123158/https://80.lv/articles/ssrtgi-toughest-challenge-in-real-time-3d/)

- use technqiues from Screen Space Reflections for
- ambient occlusion
- secondary diffuse light bounces
- self-illumination of emission objects
- bent normal calculation
- average direction of ambient light that is not occluded


- high level overview of the implementation and results
- demo at:
[SIGGRAPH 2017 Real Time Live](https://youtu.be/hpuEdXn_M0Q?t=1497)

[Lighting with Unreal Engine Masterclass (Summary)](http://www.tomlooman.com/lighting-with-unreal-engine-jerome/) [[wayback-archive]](https://web.archive.org/web/20171030154339/http://www.tomlooman.com/lighting-with-unreal-engine-jerome/)

- writeup of the static lighting information provided as part of the
[Lighting with Unreal Engine Masterclass | Unreal Dev Day Montreal 2017](https://www.youtube.com/watch?v=ihg4uirMcec)

- full frame breakdown
- dynamic environment probes, distributed across frames
- occlusion direction + angle in GBuffer
- vector in direction of least occlusion (“bent-normals”)

- optics
- anamorphic flare
- physically based lens flare

- 4 frame temporal AA

- physically based glass shader

[Vulkan: Descriptor Sets Management](http://ourmachinery.com/post/vulkan-descriptor-sets-management/) [[wayback-archive]](https://web.archive.org/web/20171106124823/http://ourmachinery.com/post/vulkan-descriptor-sets-management/)

- resource binders of the engine mapped to resource descriptor
- these are blueprints
- copied into descriptor pools during rendering

- these pools will be released when the GPU is done rendering the frame
- reduce fragmentation and lower tracking overhead

[Animating Noise For Integration Over Time](https://blog.demofox.org/2017/10/31/animating-noise-for-integration-over-time/amp/) [[wayback-archive]](https://web.archive.org/web/20171106124856/https://blog.demofox.org/2017/10/31/animating-noise-for-integration-over-time/amp/)

- analysis of white noise, blue noise and Interleaved Gradient Noise for reconstruction of image
- experimenting with golden ratio addition to create changing noise without having to regenerate it
- which seems to be an ok approximation


[Deep Illumination: Approximating Dynamic Global Illumination with Generative Adversarial Network](https://arxiv.org/pdf/1710.09834.pdf) [[wayback-archive]](https://web.archive.org/web/20171106125135/https://arxiv.org/pdf/1710.09834.pdf)

- machine learning technique
- trained with mapping from GBuffer + direct illumination to -> indirect illumination

[What every systems programmer should know about lockless concurrency](https://assets.bitbashing.io/papers/lockless.pdf) [[wayback-archive]](http://web.archive.org/web/20171105181042/https://assets.bitbashing.io/papers/lockless.pdf)

- great overview of concurrency building blocks
- hardware level overview
- how to use C++11 to ensure correctness

[Practical applications of the dot product](https://medium.com/vertices-and-faces/practical-applications-of-the-dot-product-c5503c2e454e) [[wayback-archive]](http://web.archive.org/web/20171106035545/https://medium.com/vertices-and-faces/practical-applications-of-the-dot-product-c5503c2e454e)

- Projecting a vector onto a vector
- Finding the orthogonal component of a vector to another vector
- Finding the shortest distance from a point to a segment
- With interactive demos

- discussion of problem space
- overview of GPU formats
- ETCS1
- DXT1

- .basis will be an khronos standard
- encoder takes non-uniform texture arrays and compresses these
- mips / cubemaps / video frames / … all handled the same way


[Showing the Correctness of Quaternion Rotation](https://erkaman.github.io/posts/quaternion_rotation.html) [[wayback-archive]](https://web.archive.org/web/20171106125318/https://erkaman.github.io/posts/quaternion_rotation.html)

- algebraic proof for quaternion rotation