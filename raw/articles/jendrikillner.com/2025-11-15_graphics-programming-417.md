---
title: Graphics Programming 417
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-417/
author: Jendrik Illner
published: '2025-11-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- SIGGRAPH 2025 presentation on stochastic tile-based lighting techniques implemented in HypeHype
- cover motivations for the technique and how it compares against other solutions
- detailed discussion of the implementation
- covers how it interactics with other effects such as shadows

![](../../assets/e5b6b1808e4e4135.png)


- presents techniques for implementing spectral rendering in real-time applications using Monte Carlo integration
- describes importance sampling strategies for wavelength selection based on illuminant spectra and color matching functions
- demonstrates that spectral rendering introduces only modest overhead compared to RGB rendering

![](../../assets/00858045aace8e73.png)


- explains the mathematical foundations of tangent space and its role in normal mapping
- details how UV coordinates define the orientation of the tangent frame on surfaces
- presents the construction of the TBN matrix and its application in transforming texture-space normals to surface space

![](../../assets/51c8e383ac45fb1e.png)


- discusses techniques to hide or reduce visible tiling patterns in terrain shaders
- presents shader based solutions
- additionally discusess alternative art authoring solutions

![](../../assets/e1de49b867223200.png)


- introductory video for a course on neural shading techniques
- first part of an 11 video part series exploring what neural shaders are, what hardware they provide access to

![](../../assets/c897ad464f0b9d09.png)

- introduces a new Vulkan Drivers tab in the Vulkan Configurator (vkconfig)
- provides a graphical interface to add additional drivers, force specific physical devices, and reorder device enumeration
- streamlines multi-GPU testing and debugging by eliminating manual JSON configuration and environment variable tweaks

![](../../assets/59a13f30f1ff13a6.png)


- video tutorial covering descriptor indexing in Vulkan
- explains how to access shader resources dynamically without binding individual descriptors
- demonstrates the modern approach to managing textures and buffers in Vulkan applications

![](../../assets/bd2efc223ee749c3.png)


- demonstrates how to use Nsight Graphics GPU Trace to profile and optimize RTX Mega Geometry
- shows detailed view of the available performance counter
- provides practical workflow for analyzing shader performance and identifying bottlenecks

![](../../assets/b37a79a124ad8003.png)


- tiny dependency-free C99 library (~700 LOC) for lossless compression of GPU-compressed texture blocks (BC1, BC3, BC4, BC5)
- exploits spatial patterns, endpoint deltas, and Morton-ordered indices specific to BC formats achieving compression ratios of 1.5x-6x
- features deterministic bit-exact reconstruction with no malloc or external dependencies

![](../../assets/27196db549b5c97d.png)


- deep dive into GPU performance details and why GPUs are effective for neural network training
- contains high level overview of gpu achitecture
- identifies common bottlenecks (memory bandwidth, kernel-launch overhead, CPU–GPU imbalance) and how to overcome them

![](../../assets/6d14fe3461d4ff20.png)


- tutorial on implementing Graph Neural Networks from scratch
- provides step-by-step explanation of GNN architecture and components
- covers fundamental concepts and practical implementation details

![](../../assets/ecae6ab1a3c633bd.png)

Thanks to [Graham Wihlidal](https://www.wihlidal.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.