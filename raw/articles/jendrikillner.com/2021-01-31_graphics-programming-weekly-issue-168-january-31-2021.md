---
title: Graphics Programming weekly - Issue 168 — January 31, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-168/
author: Jendrik Illner
published: '2021-01-31'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper introduces a new method for Mip level selection, including anisotropic filtering in a raytracer
- presented technique is not based on screen space derivatives
- extends the technique to apply to textures with different dimensions
- shows how ray cones can be used to select LOD for shading too

![](../../assets/08ea1f54e878385c.png)


- the article presents an introduction to Gamut Clipping (mapping colors outside of the target color space back into valid colors)
- presents different approaches for mapping techniques
- shows how to apply these for the Oklab color space and presents comparisons of the results
- code is provided

![](../../assets/6dbd213b1c6c79c5.png)


- first part of a three-part series that focuses on optimizing a CUDA workload
- articles present the methodology, how to use the Nsight provided information to iteratively optimize the application

![](../../assets/7a6b5f8e15fbe8db.png)


- the article presents how to reduce memory usage of bottom level acceleration structure (BLAS)
- instead of using placed resources for each BLAS, it is recommended to sub allocate from one larger structure

![](../../assets/e45f3d594ee6a05d.png)


Ubisoft RedLynx is a multiplatform game development studio located in Helsinki. Along with the hugely popular Trials series, we have developed and published more than 100 games and we are a passionate team of over 140 people of 21 different nationalities. We are seeking an experienced Graphics Programmer to join our core technology team in creating impactful game experiences.

![](../../assets/4cfddfae173473e2.png)


- the Unity video tutorial shows how to implement rim lighting (an effect that only applies to the edges of a model)

![](../../assets/e127f8bce2834bd1.png)


- Video lectures for the Introduction to Computer Graphics Course at the University of Utah
- more classes will be released over the next few weeks

![](../../assets/e8060e0971f3a91e.png)


- the paper presents a deep neural network to generate signed distance functions using a fixed network and sparse oct-tree
- the network also generates the level of detail representations
- shows real-time reconstruction and rendering with ray tracing

![](../../assets/87458c5e1c59a4df.png)


- the article presents an overview of UV mapping
- showing different mapping techniques, problems, and uses cases

![](../../assets/413c0374b5b7a62e.png)


- updated tools adds support for inline raytracing and capturing applications that are not frame-based

![](../../assets/a5e0ad2fedd9ba2e.png)

Thanks to [Bruno Opsenica](https://bruop.github.io) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.