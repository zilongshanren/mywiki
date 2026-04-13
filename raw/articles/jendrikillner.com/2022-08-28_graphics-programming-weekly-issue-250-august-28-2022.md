---
title: Graphics Programming weekly - Issue 250 - August 28, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-250/
author: Jendrik Illner
published: '2022-08-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- presents why and when a quad is being drawn as two triangles can cause discontinuities along the edge
- the paper presents a geometry shader implementation of generalized barycentric coordinates for quads
- this concept was introduced in 2004 for CPU rasterization when hardware support was not available

![](../../assets/bd1184761daa2c4d.png)


- the paper introduces an adaptation of the Heitz and Neyret texture tiling technique
- the original technique required offline preprocessing to enable histogram-preserving tiling
- the new method removes the requirement and presents the implementation in shader code only
- presents how to apply the technique for color and normal maps

![](../../assets/d323e43ade91489f.png)


- the blog post provides an insight into how the apple metal driver is separated into components
- shows how it’s possible to call internal APIs and reconstruct hardware behavior
- presents a discussion of OpenGL clip space mapping and limitations of different emulation behaviors

![](../../assets/ba8de96d16a41193.png)


- the video tutorial explains how to implement an outline effect in Unity
- presents how to detect edges using the depth buffer, create an outline at the edges
- it additionally shows how to adjust the effect so that objects behind objects get a separate show-through-wall effect

![](../../assets/24398878651d749d.png)


- the talk discusses the issues artist encounter and how Nanite goals are designed to resolve them
- presents a large number of topics Brian Karis had researched along the way
- shows a brief overview of the techniques, shortcomings, and reasons why they failed
- discusses how to structure long-term research, focusing on challenges of the field and the importance of coding like a scientist

![](../../assets/5b0f59ce646de369.png)


- the paper introduces two convolutional neural networks (CNN) based techniques that can detect LOD transitions and the quality of that transition
- two models are presented to solve these two issues separately
- discusses the issue with the current approaches and how the presented techniques could be used to support artists

![](../../assets/9ffbbd3e9e7472ac.png)

Thanks to [Daniel Fortes](https://www.danielfortes.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.