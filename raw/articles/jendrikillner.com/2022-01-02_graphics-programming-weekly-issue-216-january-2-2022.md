---
title: Graphics Programming weekly - Issue 216 - January 2, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-216/
author: Jendrik Illner
published: '2022-01-02'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents a very detailed look at temporal anti-aliasing
- shows each component of the technique visually and explains how it solves the problem
- provides alternative solutions and presents a link to the sources of the technique

![](../../assets/5b54db0786e3fa4e.png)


- the article provides a high-level learning guide for getting started with D3D12
- providing a starting point for getting started quickly as well as detailed learning articles
- contains sources for performance advice from the different manufacturers
- additionally contains information where to find the official D3D12 specification to clarify uncertainties

![](../../assets/79957b3b06bf6b8a.png)


- the article presents a high-level view of the graphics programming world
- shows that the specialization has separated into multiple distinct sub-categories
- presents resources for getting started in the different specializations

![](../../assets/1e72b10908a66f6e.jpg)


- the article presents the characteristics of IGN(Interleaved Gradient Noise) that make it a good fit for TAA (Temporal Antialiasing Techniques)
- compares against Bayer, white and blue noise
- showing visual explanations to show the Low Discrepancy properties

![](../../assets/b02ce606f432481e.png)


- the article presents the findings of the importance of directionality and occlusion for IBL(Image-based lighting)
- presents comparisons between ray-tracing ground truth, as well as various versions of screen space GTAO( Ground Truth Ambient Occlusion)
- shows how to bake the directional aspect into Spherical harmonics
- additionally contains a follow-up post about the technical implementation details

![](../../assets/b36d5c97555694fc.png)


- the article presents a look back at the emergence of the term uber shader
- showing how a single shader that supported a flexible BRDF evaluation instead of pre-defined categories
- the comments contain an insightful discussion about the further historical developments of the term

![](../../assets/468d47e20ebf8834.png)


- the article compares different techniques to generate blue noise
- presents the quality of the generated noise
- providing ideas for future development

![](../../assets/70c237e0cb968fd9.png)


- the article provides a history of game consoles in the First Generation 1972 to modern-day consoles
- presents what new hardware was added with each generation and how constraints and programming environment evolved

![](../../assets/c0a3a6157764ebc1.jpg)


- the article presents branching on GPUs, clearing up that the cost of a branch depends on the kind
- shows shader code helpers that allow the visualization of the branching patterns
- additionally presents that extra care is required if branching around texture reads

![](../../assets/1ea34fab38e8a4b9.png)


- the blog discusses dependent texture reads and the impact on GPU performance
- shows why it affects performance and discusses tradeoffs to consider

![](../../assets/cc37c8c2ede80535.png)

- the paper presents a look at the half/single/double and quad precision for floating-point calculations
- provides an analysis of different linear algebra tasks to derive precision
- suggesting which types of tasks might be more suitable to reduced precision

![](../../assets/05802b28ae3d0b11.png)


- one-minute long video shows the impostors used for far away vegetation in Zelda Breath of the Wild

![](../../assets/434ad9148e97d342.png)

- the article shows how custom shader effects can be integrated into the UE4 pipeline
- presents a method that doesn’t require engine modification but uses undocumented private classes

![](../../assets/d5d63d74f1d89fd0.png)


- talk discusses the available memory types in D3D12/Vulkan
- discussing ways to upload data to the GPU, including the new hardware Smart Access Memory (Resizable BAR)
- shows performance advice for usage patterns for the different memory types to achieve optimal performance

![](../../assets/ca3a24c21e9900bb.png)

- the article provides a collection of advice to help with debugging GPU issues
- broken down into sub-categories based on the appearance of the bug
- additionally contains a list of helpful debug infrastructure elements that should be set up to accelerate the process

![](../../assets/674fd5c8a146119d.png)

Thanks to [Lesley Lai](https://lesleylai.info) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.