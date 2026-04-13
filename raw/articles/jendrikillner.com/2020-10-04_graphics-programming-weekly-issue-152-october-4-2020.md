---
title: Graphics Programming weekly - Issue 152 — October 4, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-152/
author: Jendrik Illner
published: '2020-10-04'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the video shows the history of light transport techniques and presents how they perform in complex test cases
- leading up to “Specular Manifold Sampling for Rendering High-Frequency Caustics and Glints” and how it makes aims to make state of the art a more accessible

![](../../assets/b65957c2203b4030.png)


- links to the papers from I3D 2020
- the winners for best-award are “Passthrough+: Real-time Stereoscopic View Synthesis for Mobile Mixed Reality”, “Local Optimization for Robust Signed Distance Field Collision” and “Real-Time Stochastic Lightcuts”

![](../../assets/157d395247241c11.png)


- SIGGRAPH 2020 presentation that provides an overview of Variance-Aware Path Guiding
- paper proposes to treat the problem as an error minimization problem using relMSE ( relative mean squared error )
- shows existing techniques that could be improved from the proposed solution

![](../../assets/0d870bd95501ccf4.png)


- the blog post discusses the development of a GPU based grass rendering system
- provides an overview of the approach taken and provides videos for the different stages of implementation

![](../../assets/87488e9728cb8d60.png)


- the video shows the Ray Tracing implementation and uses it to explain the considerations when designing a raytracing solution
- explains the steps raytracing requires and how changes in each step influence the total reflection budget

![](../../assets/e0839148c698589c.png)


- breakdown shows how a Stylised Water Shader was implemented in Unity
- the post focuses on the overall look -presents the different layers of the technique and what these contribute to the final look of the water

![](../../assets/caf4286d000472b8.png)


- the paper presents extensions to the
[probe based irradiance-field-with-visibility representation](http://jcgt.org/published/0008/02/01/) - These extensions include a self-shadow bias, introduction of heuristics to speed transitions, re-use for recursive glossy reflection, probe state machines as well as multiresolution cascaded volumes

![](../../assets/121af090e5dc7506.png)


- the blog post presents a comparison between the usage of different color spaces on the results of path tracing
- compare Rec709 and ACEScg color space, providing the mathematical approximations for the color conversions required

![](../../assets/88e2ed734beff3c2.png)


- the 13ths part of the scriptable render pipeline tutorial explains how to add color grading to the Unity pipeline
- presents several techniques to adjust the visual look of the scene
- shows different color space, how to convert them, and optimize the conversion steps with LUTs

![](../../assets/86a3b301b52aaf5a.jpg)


- the article presents a table of HLSL and GLSL compute shader semantics and how they the meanings maps between local and global references

![](../../assets/6db610cfe483b1e2.png)


- tutorial explains the new unified AMD interface for the GPU Profiler Memory Visualizer
- shows how to use the different workflows

![](../../assets/ef9ac51bfe15ad08.png)

Thanks to [Adalberto Bruno](https://www.linkedin.com/in/adalbertobruno/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.