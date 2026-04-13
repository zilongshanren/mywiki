---
title: Graphics Programming weekly - Issue 220 - January 30, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-220/
author: Jendrik Illner
published: '2022-01-30'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents the flow of data when a CPU generated value is accessed from an HLSL shader
- explaining the differences between the available approaches as well as the implications on memory lifetime

![](../../assets/3bf3261e8d427eca.png)


- the article provides a summary of the Lumen implementation found in UE5 (Unreal Engine 5)
- discusses the offline and runtime stages of Lumen (dynamic GI solution)
- shows the Acceleration Structure tracing approach as well as probe placement
- presents how the scene is represented using MeshCard (Proxy) approximations and distance fields
- additionally shows a detailed walkthrough of all the logical stages that compose the system

![](../../assets/c18d699c1a79cf00.png)


- the article provides a summary of the features that are mandatory in Vulkan 1.3
- (removing requirement of render passe, better pipeline creation control, as well as direct buffer addressing support and more )
- additionally introduces the new Vulkan roadmap, this will provide guidance on what hardware/software support the group will focus on
- the 2022 roadmap will require bindless support as well as more consistent subgroup operation support

![](../../assets/0295c96d881933ef.png)


You are helping our core team to develop cutting-edge 3D data optimization technology, being used in production pipelines to process millions of 3D data sets each year, fully-automatically. You are performing research on 3D mesh processing, texture baking, UV mapping, optimization algorithms and ML-based algorithms for 3D data optimization and QA.

![](../../assets/e1093cad59141f24.jpg)


- the article explains the history and evolution of the mesa shader compiler (internal representation) NIR
- discusses the historical reasons and experience of using it instead of LLVM
- presents problems and advantages over a CPU focused IR system

![](../../assets/b238fa35921836f0.png)


- the new version of the Nsight Compute allows a better understanding of memory traffic and cache eviction decisions
- additionally adds new guided optimization support that detects unfused floating-point operations as well as uncoalesced memory access

![](../../assets/f1e975763d10ffb4.png)


- the article why randomly tracing rays leads to noisy results
- presents the mental model to improve this in a simple scene

![](../../assets/867f793cb17ea453.png)


- the presentation contains a collection of best practices when working with WebGPU
- covering compressed textures, debug label usage, data uploading, pipeline creation as well as bind group usage

![](../../assets/689885dacefd4112.png)


- the video explains the derivation of Cosine Interpolation
- discusses how the individual components are derived and how they are connected for the final result

![](../../assets/d5a8764ce4c21cad.png)

Thanks to [Marius Horga](http://metalkit.org/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.