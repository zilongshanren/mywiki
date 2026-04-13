---
title: Graphics Programming weekly - Issue 293 - June 25th 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-293/
author: Jendrik Illner
published: '2023-06-25'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper introduces a method that enables micro-poly geometry for raytracing workloads
- geometry is preprocessed, clusters formed and simplified into a compressed hierarchical level of detail representation
- presents how using clusters enables fast BVH building
- in the appendix discusses in detail how to select clusters to be guaranteed crack-free between different clusters

![](../../assets/9e633c3692397830.png)


- the blog post announces the first public release of a new D3D12 feature called Work Graphs
- shows how this feature enables GPU shaders to spawn further GPU work from the GPU timeline
- presents an overview of the spec
- additionally, it discusses which samples are available at this time

![](../../assets/c03ca592cf5abd33.png)


- the AMD guide provides a more in-depth look at the practical use of D3D12 Work Graphs
- presents how to get started and the building blocks of the programming model
- additionally, it presents a section on tips & tricks to help during the development (guides for tracking down issues, best practices, etc.)

![](../../assets/139e62f30d10d6ca.jpg)


- the blog post announces support for the new d3d12 work graphs feature in the preview version
- shows the first level of debug support and discusses what is coming in the future

![](../../assets/877d3d41b09c482a.png)


- another part of the glTF rendering series
- part focuses on how to interpret the scene hierarchy and flatten it for rendering

![](../../assets/00ec8b9e5b48f3bf.png)


- the video tutorial presents a walkthrough on the integration of a real-time fluid simulation
- shows how the physical model is translated into shader code
- implementation is shown using Unity C# and shader code

![](../../assets/9e28242406ae042e.png)

Thanks to [Erika](https://twitter.com/rrika9) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.