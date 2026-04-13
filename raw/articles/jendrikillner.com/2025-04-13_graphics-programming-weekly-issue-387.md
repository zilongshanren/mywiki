---
title: Graphics Programming Weekly - Issue 387
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-387/
author: Jendrik Illner
published: '2025-04-13'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- The blog post provides a discussion how hardware and graphics APIs developed over time
- Presents performance changes as well as capabilities changes

![](../../assets/99b6743b74be574f.png)


- The article presents a detailed discussion of z-testing in modern GPU hardware
- Shows when the hardware is able to move the execution of z-testing before pixel shader invocation and when not
- Shows the impact on performance and correctness
- Closes with a table showing a summary of the various features that can affect the behavior

![](../../assets/cd7d8afb1bb18f46.png)


- The series on Monte Carlo’s related techniques continues with Monte Carlo Sampling
- Presents how to convert Pseudo-Random Numbers into samplers for more complex domains
- Covers Uniform Rejection Sampling, Non-Uniform Rejection Sampling, Inversion Sampling, Marginal Inversion Sampling
- Additionally talks about Changes of Coordinates and Sample Efficiency

![](../../assets/952b5cb1e7ebda1d.png)


- Reuse and share samples between different lanes in a shader wave, avoiding memory traffic
- Presents a method to improve the quality of stochastically-filtered magnified textures compared to traditional texture filtering

![](../../assets/a669bbbdbbf04ee2.png)


- The article presents an algebraic solution for bilinear interpolation using Barycentric coordinates to allow improved sampling across triangulated edges
- Shows an explanation of the derivation of the method
- Additionally contains the code for the implementation

![](../../assets/c05116309b0d1c98.png)


- The article presents a discussion of how to approach blurs for vector graphics
- Discusses how to rethink the approach instead of using Gaussian blurs
- Links to the implementation is provided

![](../../assets/f501bd7ae96934c9.png)

Thanks to Dirk Dörr for supporting this series

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series