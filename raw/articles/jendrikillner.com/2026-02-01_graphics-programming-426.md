---
title: Graphics Programming 426
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-426/
author: Jendrik Illner
published: '2026-02-01'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- details improvements to RADV’s ray tracing pipeline compilation in Mesa 26.0, introducing function calls to the compiler stack
- presents how separately compiling any-hit and intersection shaders instead of inlining them into megashaders dramatically reduces compilation times
- Additionally, it can resolve pipeline stutter in Unreal Engine games

![](../../assets/50c8261525e112e2.png)


- explains complex numbers from a geometric algebra perspective
- demonstrates key properties with an example-driven lecture

![](../../assets/ff9c9d5100fb7884.png)


- tutorial showing a simple auto material that layers terrain materials based on slope angle, part of an ongoing Terrain Shaders series
- covers implementation details and references earlier episodes for implementation details

![](../../assets/7a1feeed27e911f5.png)


- SIGGRAPH’s Thesis Fast Forward, where Ph.D. students present research pitches
- includes a range of topics such as Monte Carlo PDE solvers, robust winding-number/SDF algorithms, point-cloud reconstruction, and more

![](../../assets/57652713a8523a94.png)


- practical tutorial on texel density: what it is, how to choose appropriate densities for different player POVs, and set targets
- presents how to measure real-world references, visualizing texel density in UE5
- additionally presents a Maya texturing workflow with recommendations and scale references

![](../../assets/64a3cd28e39b5832.png)


- presents a workflow design approach for maintaining game documentation spatially within the game engine itself
- demonstrates how in-game documentation avoids the common problem of external documentation becoming outdated, enabling developers to instantly verify metrics, test systems, and debug assets without searching through external documents
- additionally covers techniques for automated testing and the generation of these documentation levels

![](../../assets/0ac85b9e08b45864.png)


- annual survey looking for feedback from Vulkan developers to improve the SDK and ecosystem
- asks about developer role and experience, target platforms, SDK usage, and other ecosystem pain points to guide future work and priorities
- closes Feb 25, 2026

![](../../assets/fe6dd5d523c2b2b5.png)


- implements a complete surfel-based global illumination pipeline in WebGPU, including surfelization, spatial acceleration structures, ray tracing, and temporal filtering
- employs advanced techniques such as surfel-guided light sampling to reduce noise, multi-scale mean estimators for temporal stability, and radial depth atlases to prevent light leaking through thin geometry

![](../../assets/5110cca114f33da7.png)


- provides an updated overview of Vulkan support on Apple platforms through layered implementations on Metal, comparing MoltenVK and the newer fully conformant KosmicKrisp
- details the structure for packaging Vulkan applications on macOS and iOS, including proper placement of the Vulkan loaders

![](../../assets/613db0f7389aa349.jpg)


- compares texture format options for WebGPU applications, weighing traditional image formats (WebP, AVIF), GPU block-compressed formats (BC7, ASTC), and universal formats (Basis Universal)
- introduces spark.js as a solution for real-time GPU transcoding
- This allows developers to ship efficient compressed web formats while transcoding to block-compressed GPU textures at runtime

Thanks to [Nathan Reed](https://www.reedbeta.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.

![](../../assets/6581f2f2af1501f0.png)