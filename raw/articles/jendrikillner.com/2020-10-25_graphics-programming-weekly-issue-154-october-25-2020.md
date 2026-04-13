---
title: Graphics Programming weekly - Issue 154 — October 25, 2020
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-154/
author: Jendrik Illner
published: '2020-10-25'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the articles explains the pitfalls encountered when implementing Screen Space reflections
- discusses special cases for a 2D game and presents what fallback options have been used if the information is not available

![](../../assets/64c570bf0d485b2c.png)


- the blog post provides an overview of ambient occlusion and what it approximates
- provides interactive examples to show the effect of screen space ambient occlusion
- additionally provides interactive examples to show the impact of different parameters for Ray-Traced Ambient Occlusion

![](../../assets/08186135be0c09bc.jpg)



- the presentation explains how the raytracing for shadows has been implemented into Call of Duty
- covering acceleration structure separation, performance, denoising implementation, and supporting multiple local area lights

![](../../assets/145a8fc461d2124f.jpg)


- the paper presents a new framework for layering and compositing of bump maps from different sources
- presents how to use the framework with different techniques, including volumes, decals, dealing with multiple UV sets, etc..
- demo
[code](https://github.com/mmikk/surfgrad-bump-standalone-demo)provided

![](../../assets/e309221c2fa61795.png)


- the article presents how the precision HiZ tracing logic (used for screen space reflection) can be increased
- additionally also makes the technique more generalized

![](../../assets/271bb7cae1532e39.jpg)


- the blog post explains the history of RLSL (Rust Like Shading Language)
- and how rust-gpu is the spiritual successor

![](../../assets/97df2dab13e78816.jpg)


- First public release of Rust-gpu, a new SPIR-V backend for the Rust
- post explains the motivation, current state, and planned scope

![](../../assets/edf06fe194e4b3a7.jpg)


- the article provides a brief overview of scalarization and suggests an alternative approach

![](../../assets/ccab699716171b9c.png)

Thanks to [Keith O’Conor](https://twitter.com/keithoconor) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.