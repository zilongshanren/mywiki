---
title: Graphics Programming weekly - Issue 98 — September 15, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-98/
author: Jendrik Illner
published: '2019-09-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- interview discussing the details of the Gear 5 implementation
- all post-processing and UI rendering is done post-upscaling in the output resolution
- using
[Relaxed Cone Stepping](https://developer.nvidia.com/gpugems/GPUGems3/gpugems3_ch18.html)for extra details instead of parallax occlusion mapping - a mix of shadow maps and ray-traced distance field shadows

![](../../assets/901a395f012c1880.jpg)


- tutorial explaining how to implement a Caustics effect in unity
- uses a tileable texture, that is sampled multiple times
- slight offsets in RGB sample locations allow for color shifting across channels

![](../../assets/27d773ff2b483959.png)


- the article presents an overview of performance methodology to detect performance issues earlier
- including the building of test scenes, early clarification of constraints and constant checking of assumptions
- setting budgets early simplifies expectations and possibilities

![](../../assets/f757fbcfeb1a47fd.jpg)


Ubisoft RedLynx is a multiplatform game development studio located in Helsinki. Along with the hugely popular Trials series, we have developed and published more than 100 games and we are a passionate team of over 140 people of 21 different nationalities. We are seeking an experienced Graphics Programmer to join our core technology team in creating impactful game experiences

![](../../assets/4cfddfae173473e2.png)


- overview of the state of WebGPU in safari
- Web Shading Language is a new text-based shader language, now supported
- presents compile-time and size comparisons against SPIR-V based implementations

![](../../assets/911abc94e6b73546.png)


- looks at the behavior of texture sampling in divergent code flows on different hardware
- undefined behavior that is handled very differently depending on the GPU hardware

![](../../assets/b67f7e0bf77b8745.png)


- GPU assisted validation for VK_EXT_buffer_device_address
- SPIRV-opt can now retarget shaders to use RelaxedPrecision without requiring source-level changes

![](../../assets/8da14ae11d540da6.png)


- the paper discusses the design of the Mitsuba 2 renderer
- based on a combination of generic algorithms and composable compile-time transformations
- demonstrates the approach with Polarized light transport, coherent Markov Chain Monte Carlo (MCMC) exploration, caustic design in heterogeneous media with multiple scattering

![](../../assets/53b1777e01690a6c.jpg)


- collection of tech art tweets, many gifs, and videos showing a large variety of effects and art styles

![](../../assets/12cbaa6bc3790290.png)


- the paper proposes a new weighting heuristic for multiple importance sampling
- taking into account variance estimations
- shows how to integrate the solution into Bidirectional path tracing

![](../../assets/7e0821a9b2630e12.jpg)


- the paper presents novel integral formulations for volumetric transmittance
- it enables the use of Monte Carlo estimator variance analysis
- comparison of different estimators for different scenarios

![](../../assets/e9a2b5199a197532.jpg)

Thanks to [Bruno Opsenica](https://bruop.github.io) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.