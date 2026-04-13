---
title: Graphics Programming weekly - Issue 273 - February 5th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-273/
author: Jendrik Illner
published: '2023-02-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the start of a series of blog posts that explores the space of compressing floating point data
- this post explains the source of the data and patterns of the underlying data
- series compares a large number of techniques, compression solutions, and libraries

![](../../assets/ef03750d30b99096.jpg)


- short tutorial explains the concept of normal maps and how it influences the lighting computations
- shows how to interpret the meaning of the colors
- additionally shows the importance of normal map orientation

![](../../assets/e7d5cb48e67a92a9.jpg)


- the article explains how to create a shader in Unity that gives an object a subsurface scattering effect
- shows what effect subsurface scattering has on the lighting model
- presents how to integrate it into the standard surface shader

![](../../assets/6048f1e19317b62d.png)


- the blog post explains how to convert a one-dimension threadIndex from compute shader into a 2D coordinate
- shows how to use Quad-wide Shuffle Operations to reduce reliance on group-shared memory

![](../../assets/1bf4c67c39f29ac7.png)


- the video tutorial shows how to adjust Unity and Unreal Shading models to be more fitting for Sand rendering
- shows how to adjust textures sources for efficient usage from shaders

![](../../assets/2151f5ac2822475b.png)


- the article presents a summary of what was discussed at the WebGL / WebGPU meetup
- lists new extensions coming for WebGL and the state of WebGPU rollout
- shows how the most significant obstacle for ThreeJS to adopt WebGPU is the requirement of WGSL shader language

![](../../assets/ce500bcab0c11bf2.png)


- the paper presents an alternative way to deal with the instability of generative adversarial networks (cGANs)
- suggests replacing the reconstruction loss with the energy distance
- paper contains a one-page summary of the technique

![](../../assets/e369c43e471b4823.png)


- the article presents a look back at the Shadowman game implementation for the PS2
- describes how to implement and optimize the four-point light setup while staying within PS2 limitations

![](../../assets/0dafb224e33b06f3.png)

Thanks to [Top-OR](http://top-or.de/projects) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.