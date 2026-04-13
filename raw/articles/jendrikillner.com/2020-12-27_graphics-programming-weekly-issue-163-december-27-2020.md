---
title: Graphics Programming weekly - Issue 163 — December 27, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-163/
author: Jendrik Illner
published: '2020-12-27'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article provides an overview of considerations when developing a graphics technique for video games
- presents how game design, workflow, performance, artist controllability, … affect the possible solution space
- provides a case studio from the vegetation system from The Witcher 2

![](../../assets/895386d38708b4f7.png)


- the article presents how to implement frustum culling and the effects on CPU and GPU performance

![](../../assets/924c12c852e3d3e6.png)


- the blog post provides a look back at the evolution of graphics technology and how they affect game production
- author expresses his view on how ray tracing will repeat history and complexity will continue to increase as we want to archive more complex goals

![](../../assets/947b7249abf272d1.jpg)


- the blog posts takes a look at the RNDA ISA and presents how ray tracing has been implemented in AMD hardware
- look at the instructions to accelerate ray/triangle and ray/BVH intersection logic in hardware

![](../../assets/9210f8b8a8d2f3b7.png)


- the article presents a new perceptual color space
- illustrates how the color space conversion is used and how it was derived
- color space is designed to use D65 white point (easier interop with Rec202 and sRGB) with even transitions when used in blending

![](../../assets/4706b30d029184e6.png)


- the article presents an overview of D3D12 aliasing barriers, Discard/Clear semantics, and how they interact with resource states
- presents three approaches to the problem
- it appears no way exists that doesn’t trigger debug-runtime errors and archives optimal performance

![](../../assets/96988457b738486f.png)

Thanks to [Jonathan Tinkham](https://zincfox.red) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.