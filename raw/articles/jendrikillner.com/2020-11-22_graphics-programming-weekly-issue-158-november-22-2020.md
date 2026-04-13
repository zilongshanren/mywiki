---
title: Graphics Programming weekly - Issue 158 — November 22, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-158/
author: Jendrik Illner
published: '2020-11-22'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog posts describes how APITrace can intercept D3D12 applications (even complex AAA games such as Assassin’s Creed Valhalla)
- presents how the layer deals with Persistent Memory Mapping, Capturing and Replaying Descriptors, Fences, and Synchronization
- additional describes what issues are still left unsolved

![](../../assets/1ef8728ad7e17999.png)


- the dev vlog explains how the 2D billboard based clouds are implemented
- cloud volumes are generated in Blender, directional light information is baked into textures using single color lights along the principal coordinate system axis
- these directions are blended at runtime to integrate into the in-game PBR lighting system

![](../../assets/3ed8499a19e76356.png)


- the devlog presents a walkthrough of the implementation of a toon shader
- contains a comparison between a toon shading model and a more realistic model
- the implementation is done using the Unity Universal Render Pipeline (URP) and ShaderGraph

![](../../assets/eb7f374e30f6df09.png)


- the video tutorial explains how to take an input mesh and use a compute shader to generate additional geometry
- provides an overview of compute shader concepts, showing the HLSL based implementation and how to integrate it into the Unit rendering pipeline
- additional explains how to use DrawIndirect to draw the results directly from the GPU timeline

![](../../assets/2ff2650f7dbbb68a.png)


- the article presents three different approaches to archive a fire effect using Unity
- show a sprite-based flipbook effect, procedural shape generation for a toon, and more realistic shape
- the implementation is done in ShaderGraph

![](../../assets/3833b33453825eb9.png)


- unrolled Twitter thread presenting an overview of differences between D3D12 and Vulkan
- the aim of the comparison is to be able to support both APIs

![](../../assets/9c2813d359711096.png)


Thanks to [Denis Gladkiy](https://play.google.com/store/apps/developer?id=Piggybank+Software) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.