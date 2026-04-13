---
title: Graphics Programming weekly - Issue 360 - October 6th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-360/
author: Jendrik Illner
published: '2024-10-06'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents a detailed look at the quality aspects that relate to animation
- shows the importance of sampling rate for human motion
- presents the impact of data precision on animation playback
- additionally, it presents a detailed discussion of animation data sets and develops what is required for high-quality research results

![](../../assets/57319412a7783074.png)


- the presentation provides an overview of the difficulties related to the composition of GPU graphics techniques
- presents how Use.GPU tries to solve the problems by making composition a first-class design goal
- presents how implementation details require completely different implementations
- shows solutions to the problems discussed

![](../../assets/bb9dea0c8c7ffeba.png)


- the paper proposes the use of tetrahedrons as primitives for volume rendering using mesh shaders
- uses mesh shaders to compute the depths of the front and back faces at the same time when interpolating vertex attributes and passing both depths to the rasterizer stage
- additionally presents how to use the same idea to implement SDF tracing

![](../../assets/122f47d9379db395.png)


General Arcade, a porting and co-development studio that has worked with a wide range of clients, from indies to AAA developers and publishers, including Larian, From Software, Capcom, Devolver Digital, TinyBuild, and others, is seeking a Software Engineer with a rendering emphasis.

This is a great opportunity to work with a passionate engineering team on cutting-edge industry technologies.

![](../../assets/c3ef79290c0765d3.png)


- the paper proposes an anisotropic specular image-based lighting method that can serve as a drop-in replacement for bent normal techniques
- derives an analytic formula to determine the two closest and two farthest points from the reflected direction on an approximation of the BRDF confidence region boundary
- compares the method against bent normal technique and ground truth using the GGX specular BRDF

![](../../assets/d73635e937c962ba.png)


- the blog post introduces the new Driver Experiments
- this tool allows developers to enable/disable hardware features as well as optimization flags
- the post explains what features are exposed and what these options control

![](../../assets/f53a4d5068f52dee.png)


- This paper presents an approximation of the importance based on spherical Gaussians (SGs) for light clusters
- Each light cluster is represented as an SG light and analytically approximates the product integral of the SG light and a BRDF
- presents how to use the method to reduce the MC variance for many light scenes

![](../../assets/cc1b400d4bb6ab23.png)


- the video presents how to implement the rendering of a shader-based continuous grid system
- explains how to generate the grid from a shader, deal with antialiasing, vary the grid sizes with distances, and much more
- the implementation is shown and provided using OpenGL

![](../../assets/cae4364192b61606.png)

Thanks to [Manish Mathai](https://github.com/goodbadwolf/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.