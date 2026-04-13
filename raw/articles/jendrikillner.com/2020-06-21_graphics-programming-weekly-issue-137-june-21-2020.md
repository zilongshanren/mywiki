---
title: Graphics Programming weekly - Issue 137 — June 21, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-137/
author: Jendrik Illner
published: '2020-06-21'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- a lightweight and efficient method to render layered materials with anisotropic interfaces
- based around GGX BRDF lobes approximations when aligned with the tangent frame

![](../../assets/cc459766c58113f3.png)


- overview of two new libraries developed by Oculus and Qualcomm to expose low-level profiling information designed for tile-based architectures
- Ovrgpuprofiler is a CLI application that provides access to assembled real-time metric details based on the low-level information

![](../../assets/f0c2c06c24e87b1f.png)


- the article presents how to use stochastic LOD selection for a DXR based ray-tracer
- the given technique uses a combination of ray and instance mask to influence the ray selection
- discusses the importance of selecting consistent LODs between rays and shows a performance comparison

![](../../assets/4579ca0a75cb0dbb.png)


- the article explains how Oodle Texture can prepare BC textures in such a way that secondary compressions stages (such as zlib) will be able to compress it further
- shows what Rate-Distortion Optimization is and presents considerations regarding the importance of error estimators

![](../../assets/86ae84d2a10a284a.png)

- the article presents CUDA for WSL 2, how to use it and additionally shows how it cooperates with container workloads

![](../../assets/7c6db6ad14a5489a.png)

- the paper presents to Welch’s statistical t-test can be used to detect bias even with low sample counts
- presents techniques to visualize and analyze the test results

![](../../assets/b3b2e93575fb34e2.png)

- the article contains the answers to some common question viewers of the Ray Tracing Essentials webinar had

![](../../assets/3d490e2b05b952e3.jpg)


- an extensive collection resource covering various aspects of GPU optimizations

![](../../assets/4e53817e203ad866.png)

- the article presents how to create a running rat animation using a vertex shader
- this is archived by using UV partitioning to apply different animations to different body parts

![](../../assets/55002278f274053a.png)

- the first part of a WebGPU series shows the necessary steps required to render the first triangle

![](../../assets/2c98be786d6414dd.png)

- this tutorial explains how to bind resources and uses this to add basic camera movement support

![](../../assets/e3ae2cf2163eddc7.png)

- the paper presents a technique that allows Cumulative Distribution Functions that cannot be inverted to still offer an analytical and exact solution
- shows the method at the example of a unit square, stratified sampling of a truncated disk and torus

![](../../assets/3dabc729b043732d.png)


- overview of cross-platform raytracing abstraction in “The Forge” and a summary of performance numbers on different platforms

![](../../assets/dbe5aae7445753ea.png)

- the paper presents the sky and atmosphere model developed by Epic Games that support dynamic viewpoints between planet surface and space
- support different weather and planetary atmospheric settings without high dimensional lookup tables

![](../../assets/4ee9192220ec2b47.png)


- the video tutorial explains UV animation, extending this to support varying animations between pixels using flow maps
- uses the presented technique to implement a movement of a planet atmosphere using the Godot engine

![](../../assets/2b5f66f8b1993c8a.png)

Thanks to [Angel Ortiz](https://twitter.com/aortizelguero) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.