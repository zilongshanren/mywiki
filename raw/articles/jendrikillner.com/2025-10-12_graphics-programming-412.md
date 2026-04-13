---
title: Graphics Programming 412
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-412/
author: Jendrik Illner
published: '2025-10-12'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- details a GPU-driven LOD system using solid angle calculations on camera unit spheres
- projects mesh AABBs onto the unit sphere to estimate screen coverage for LOD selection
- implements bindless rendering with unified vertex/index buffer access across all LOD levels

![](../../assets/ab7362d1d333d7b4.png)


- demonstrates a technique to use JPEG textures for real-time integration using OpenGL and CUDA
- uses deferred rendering to identify required JPEG blocks before collaborative workgroup decoding
- presents the pipeline that is defined by geometry, mark, decode, and finally the resolve pass

![](../../assets/abaddcde4e3291fd.jpg)


- comprehensive overview of a 2D renderer that unifies sprites, shapes, and text in single draw calls
- presents runtime sprite atlas compilation that automatically manages texture packing for the user
- uses signed distance functions for shape rendering with unified antialiasing, rounding, and stroke support

![](../../assets/45916887aa06f1f5.png)


- tutorial covering cubemap implementation in Vulkan
- explains cubemap texture setup and sampling techniques
- demonstrates environment mapping to render a skybox around the viewer position

![](../../assets/c000beb5f9832bbb.png)

- details the process of translating SSE intrinsics to Neon for Unity’s Burst compiler
- presents optimization techniques that improved performance by 2.3x through removing allocations
- discusses challenges with instruction equivalence and shows SIMD vectorization achieving 7-15x speedups

![](../../assets/266e8015b63b4b73.png)


- video walkthrough of implementing a fluid dynamics simulation for smoke
- covers the mathematical foundations and implementation details of smoke simulation
- covers Navier-Stokes equations as well as dynamic simulation with pressure solving and velocity interpolation

![](../../assets/32e5f1ca59d07f7d.png)


- presents an improved formula for converting sRGB colors to greyscale in gamma space
- explains why the standard Rec. 709 coefficients are technically incorrect when used with gamma-corrected values
- compares alternative coefficients optimized for nonlinear color space with visual examples

![](../../assets/1c3cdcb80fbf8343.png)


- introductory video tutorial on writing shaders in Unity
- covers the fundamental concepts of shader programming for beginners
- walks through creating a basic shader from scratch

![](../../assets/5667a025939389dc.png)

- introduces a diagnostic tool for measuring WGSL shader compilation times in WebGPU
- provides complexity sliders to generate shaders of various sizes for benchmarking
- reveals significant differences between cold and warm compilation timings across browsers

![](../../assets/00cfa61141cf7941.png)


- announces the availability of recordings and materials from Slang’s SIGGRAPH 2025 sessions
- includes hands-on lab materials covering language fundamentals, modules, and automatic differentiation
- provides access to neural shading course materials as well as a session presenting how developers use the technology

![](../../assets/df55ebc41e43114e.png)


- video presentation on the Motion Fields for Interactive Character Animation paper
- discusses reinforcement learning techniques for generating responsive character movements
- present a practical implementation of the technique with an in-depth explanation

![](../../assets/a19532f97c0ec6bf.png)


- video explaining the intuition and mathematics behind Laplace transforms
- presents the transform as a tool for converting differential equations into algebraic ones
- shows visual interpretations of the mathematical concepts

![](../../assets/06380920924555cf.png)

Thanks to [Keith O’Conor](https://x.com/keithoconor) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.