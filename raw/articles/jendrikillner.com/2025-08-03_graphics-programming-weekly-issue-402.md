---
title: Graphics Programming Weekly - Issue 402
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-402/
author: Jendrik Illner
published: '2025-08-03'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- presents an improved technique for silhouette sampling in physically based differentiable rendering
- introduces new rejection test methods using bounding boxes in dual space and dual quadrics
- achieves significant variance reduction compared to previous edge sampling approaches

![](../../assets/f6cdca9ebcab97a0.jpg)


- explains techniques for implementing anti-aliasing with signed distance functions (SDFs)
- compares linear, smoothstep, and smootherstep transitions for both pixel-wise AA and blur effects
- demonstrates how to use numerical derivatives with fwidth() to maintain consistent AA regardless of perspective
- additionally presents the effect of color space choices

![](../../assets/ca975e63bfd96ae1.png)


- Video showing detailed implementation of Dear ImGui into a Vulkan graphics engine
- covers setup process including descriptor management, render pass integration, and input handling
- presents how to use the system to allow parameter adjustments

![](../../assets/7b053933f47bf8da.png)


- details the Studio’s Blender-based asset pipeline using Godot
- explains their DCC-centric approach using glTF as the exchange format with collection exports for asset management
- discusses custom extension code that handles automated export/import workflow and proper asset separation

![](../../assets/9634e1861c1eb11c.jpg)


- SIGGRAPH 2025 will feature a full day dedicated to OpenUSD sessions and hands-on labs
- For the first time, NVIDIA will offer OpenUSD certification in person (free for attendees)
- Sessions will explore how leading companies are leveraging OpenUSD for applications in simulation, robotics, and Industrial AI.

![](../../assets/0d27834255a3103c.png)


- Introduces the Driver Experiments feature in the Radeon Developer Panel for debugging GPU issues
- explains how to use the “Force NonUniformResourceIndex” experiment to detect missing shader qualifiers
- details the experiments that allow disabling of color and depth compression to identify render target barrier issues

![](../../assets/dd60dddd4a9a6444.png)


- explains why ternary operators and if statements don’t cause branch instructions for simple value selection
- demonstrates through disassembly that these operations use conditional moves rather than actual branching

![](../../assets/5ab7cbf026a94fd1.png)


- proposes a screen-space approach similar to SSAO that samples and blends material properties from nearby surfaces
- demonstrates how understanding the core concept of ideas can lead to innovative solutions

![](../../assets/96681a016d2eab11.png)


- presents a modification to classic Perlin noise, allowing directional control over the pattern generation
- includes implementation details with ShaderToy examples showing practical applications
- demonstrates how the technique can be used for creating oriented textures and controlled flow patterns

![](../../assets/cd097121c54208ed.png)


- introduces a technique that combines stratified sampling with golden ratio sequence ordering
- creates sampling patterns that maintain good quality at any sample count and across sequence boundaries
- compares error convergence with standard white noise

![](../../assets/25051607d1d5ba08.png)


- Third episode in a game optimization series focusing on strategic performance planning during pre-production
- discusses establishing performance budgets across the target platforms
- How to develop optimization strategies before production
- explains how to identify potential bottlenecks early through prototyping and setting clear technical constraints

![](../../assets/1740a4888f15dde0.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.