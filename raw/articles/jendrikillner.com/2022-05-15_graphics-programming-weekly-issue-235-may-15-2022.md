---
title: Graphics Programming weekly - Issue 235 - May 15, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-235/
author: Jendrik Illner
published: '2022-05-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents performance advice from Nvidia for clear operations
- shows that the number of different fast clear colors per frame is hardware dependent

![](../../assets/d16c38f31a5f6a95.jpg)


- the article discusses how the AMD FidelityFX Variable Shading library was integrated into The Riftbreaker
- presents how the shading rate is selected per-tile
- it additionally suggests that classification variance cutoff values should be adjusted based on screen resolution

![](../../assets/ba60f62650092b99.jpg)


- the article compares several .obj parsers for loading speed and memory usage
- presents a comparison table of supported features

![](../../assets/9b4ce15e812d41c2.png)


- the post presents a list of articles/papers that discusses Reservoir-based Spatio-Temporal Importance Resampling
- starts from the introduction of the technique, applications of the technique to issues
- a collection of techniques that improve upon the original technique
- additionally presents remarks about the limitations of the technique

![](../../assets/e637cd206afe8b21.png)


- the article expands the capabilities of the BVH construction to support a more significant number of instances
- discusses an improved algorithm for the efficient updating of BVHs
- it closes with a look at performance and the next steps

![](../../assets/9440e9da69763daa.jpg)


- the video shows a summary of block compressed formats and why they are a good fit for GPUs
- discusses the different formats, showing strengths and weaknesses of the different BC[1-7] variations

![](../../assets/b605d732e6c46309.png)


- the video lecture contains a detailed description of Vulkan Synchronization topics
- provides visual explanations of the different concepts to make understanding easier
- discusses limitations of binary semaphores and what timeline semaphores enable

![](../../assets/36f0ab518352a4a1.png)


- the article describes a how a system can derive execution order from rendered resource dependencies
- presents how the dependencies create a graph that can then be analyzed and used for barrier placements, memory reuse
- shows how to express the API in Rust

![](../../assets/a912f070167f9676.png)


- the video tutorial explains the theory of toon shading and rim lighting effects
- presents how to implement the effect using OpenGL and GLSL

![](../../assets/7de90511ed69580b.png)

Thanks to [Leonardo Etcheverry](https://www.linkedin.com/in/leonardoetcheverry/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.