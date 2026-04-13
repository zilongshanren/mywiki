---
title: Graphics Programming weekly - Issue 304 - September 10th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-304/
author: Jendrik Illner
published: '2023-09-10'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- The presentation covers the development of a new material model based on Slaps, Operators, and Trees
- explains what these three concepts represent and the issues they aim to resolve
- shows the implementation details, data storage, and integration into the rendering pipeline
- additionally presents how to integrate visualization for tool purposes

![](../../assets/e093e2fe19a6e426.png)


- The article provides an overview of ray tracing rendering concepts
- shows a summary of different methods such as Ray Marching, Cone tracing, and photon mapping
- discusses how it fits into the rendering pipeline as well as what phenomenons it enables to be simulated

![](../../assets/c805b99ee216b1f4.jpg)


- The blog post describes a brief overview of the Gaussian Splatting technique
- how it compares to previous techniques
- additionally discusses memory and performance of the demo application

![](../../assets/e64157d3bc800f6a.jpg)


- The article discusses a technique to implement atomic min/max operations on HLSL (that doesn’t support it natively)
- presents how to map floats into uints and reverse the mappings

![](../../assets/5e977f692c422ff5.png)


- The blog post shows the importance of thinking in gradients
- Consider acceptable input domains and output ranges to prevent errors and unexpected results
- Utilize periodic functions, trigonometry, dot products, and exponentiation for various shader effects and measurements

![](../../assets/3c02883dbad9cceb.jpg)


- The article introduces how to encrypt/decrypt are methods to allow reversible changes to data
- shows how to generate cheaper models than cryptographical methods to solve specific problems
- expands the concepts to present a method that allows grouping and shuffling in a stateless manner
- provides source code for a couple of examples of the presented techniques

![](../../assets/dfb811f3acbcd3f9.png)


- The video presents a comparison of 3D Gaussian Splatting for Real-Time Radiance Field Rendering against Instant NeRF techniques
- discusses a summary of the technique and how it can achieve the results without using any neural networks

![](../../assets/6d1b7eef983762c2.png)


- The video provides a discussion of ocean simulation and shading
- presents an overview of the theory, mathematics, and practical considerations for implementation
- additionally presents a look at the shading models for water surfaces

![](../../assets/a11199c31cfbb5ce.png)


- The article presents a brief discussion of Aliasing in computer graphic
- presents how the sampling patterns cause the artifact
- additionally presents techniques to resolve the artifacts

![](../../assets/51167c83adb9ca21.png)


- The presentation provides a detailed look at how the rendering API for HypeHype was rewritten for a modern mobile architecture
- discusses a large spectrum of topics from API design approach, memory API, data update frequency
- shows in detail how the draw operations are represented for the most efficient rendering performance
- presents performance numbers on PC and various mobile hardware

![](../../assets/e8f5340cc6ed01c1.png)


- The presentation covers the terrain rendering methods used in previous Call of Duty and shows the shortcomings
- discusses how the new method virtual texturing method improves upon the issues
- shows the implementation details as well as new capabilities that have been enabled

![](../../assets/8bd19e009749703d.png)


- The article presents the steps necessary to use the GFXReconstruct on Android
- how to capture the information and replay it at a later date

![](../../assets/035d6a7efaa88894.png)

Thanks to [Bruno Opsenica](https://bruop.github.io) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.