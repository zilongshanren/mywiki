---
title: Graphics Programming Weekly - Issue 392
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-392/
author: Jendrik Illner
published: '2025-05-18'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- presents a technique for computing signed distance functions (SDFs) from implicit surfaces
- ensures the shape of the surface is maintained during the conversion
- the proposed solution uses neural networks to minimize loss functions characterizing the SDF

![](../../assets/af29d43c41e156ed.png)


- Eric Haines shares updates on the Journal of Computer Graphics Techniques (JCGT)
- presents the updates behind the scenes that allowed nine papers to be published so far this year
- maintains “Diamond Open Access” with authors retaining copyright under Creative Commons licensing

![](../../assets/0eef60c8041c5e00.jpg)


- details GPU optimizations that improved path tracing performance in Indiana Jones
- presents how Opacity MicroMaps (OMMs) reduced overhead for alpha tested geometry and which issues they ran into during the integration
- additionally mentions that compaction of Bottom-Level Acceleration Structures (BLASs) halved the memory consumption for vegetation meshes

![](../../assets/880400089ba503b7.png)


- builds upon upsampling via multisampling by adding a temporal component
- renders a 4x MSAA image at 1080p and upsamples to 4K using a 4-frame jitter pattern
- presents a detailed look at the sample distribution, implementation and discusses quality and limitations

![](../../assets/0e7ef8e630bf8386.jpg)


- Eurographics 2025 tutorial on Order-Independent Transparency (OIT) techniques
- covers traditional approaches (exact, approximate, and hybrid) and deep learning-based methods
- compares performance, accuracy, and practical applications for rendering transparent objects

![](../../assets/62d9a7d8265aed20.png)


- describes a technique that applies lighting to color palettes instead of individual texels
- enables normal mapping and directional lighting effects on limited N64 hardware
- shows techniques to hide inherent limitations with the technique

![](../../assets/c640dd7906c1ff31.png)


- the article presents a walkthrough on how to render a 3D terrain using SDFs
- discusses how to generate the terrain, apply texturing and shading
- interactive source code examples are provided

![](../../assets/4021932ba0edef03.png)


- video covering how to setup a test to measure the performance of lighting models
- presents how different features of the shading model affect the performance
- shows the visual results of the different combinations

![](../../assets/486b5f20673ba92f.png)


- presents a walkthrough of research building a unified neural denoising and supersampling technique
- shows the development steps, integration into existing rendering pipelines and results in various test scenes
- discusses challenges in preserving texture details, reducing flickering, and handling disocclusions

![](../../assets/bc3b12d721df6ab1.png)


- introduces an efficient method for simplifying tree-based analytical Signed Distance Fields (SDFs)
- leverages the Lipschitz property to create simplified equivalents for specific regions of space
- proposes a new technique for sphere tracing of complex SDFs composed of thousands of animated primitives
- the included video visualizes the technique and shows results on various test cases

![](../../assets/89042060eaae2419.jpg)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.