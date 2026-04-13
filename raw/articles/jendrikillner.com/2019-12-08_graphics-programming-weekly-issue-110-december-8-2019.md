---
title: Graphics Programming weekly - Issue 110 — December 8, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-110/
author: Jendrik Illner
published: '2019-12-08'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article shows the possibility of using Bezier Triangles to store arbitrary and use this as a lookup structure for GPUs
- shows how to calculate Barycentric Coordinates
- provide the foundation for Bezier curve creation
- extends this to a triangle formation

![](../../assets/427fe49c85517b94.png)


- new PIX version allows the creation of custom buffer formats and saves/restore those
- can now start applications in a suspended state, this will enable workloads leading up to the first frame to be captured

![](../../assets/abca75c31c227649.png)


- collection of tweets showcasing a large number of effects, games and technical art resources
- contains gifs that explain the length of a vector, dot and cross product

![](../../assets/26d55acd7567437e.png)


- new GPU architecture by Imagination Technologies (PowerVR)
- promises a 2.5x performance increased while using 60% less power and providing no thermal throttling problem
- now uses MAD 128-thread wide ALU
- improved multi-tasking systems allow timing guarantees for parallel GPU work

![](../../assets/d55a917755c10a29.png)


- the article presents an overview of the Taichi programming language
- a data-oriented language that separates computations from data structures
- programmers can write algorithms as if the data structure was dense
- compiler and runtime will deal with the extra complexity introduced by sparse data structures
- can generate CPU and GPU instructions

![](../../assets/2d0ffc91b68723f6.jpg)


- the article describes the Visible GGX distribution (vGGX) sampling method
- mathematically proves that this results in the required probability density

![](../../assets/54c6311194d11e35.png)


- begins with an overview of RenderDoc functionality
- shows what window are provided by the UI, what features they expose
- how to take a frame capture of a game
- and a basic look at how to start investigating the capture

![](../../assets/3813049642214110.jpg)


- part 2 of the grass shader, part 1 was discussed in issues
[105](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-105/) - will extend the shader with tesselation, better lighting, and shadows
- additionally shows how this can be extended to support trampling

![](../../assets/613c8d04bebae19b.png)


- the article provides an overview of matrices
- introduces the idea of viewing matrices as spaces and the importance of frame of reference
- with this knowledge presents the different types of linear transformation and how they influence the space
- additionally covers translations, homogeneous coordinates, and projection matrices

![](../../assets/7de9fbe78d1dc996.jpeg)


- part of Rust game programming series
- the article shows how to call D3D11 from Rust
- shows how to create a d3d11 device, swap chain and present the back buffer to the window

![](../../assets/b31ce89b76ab4bf2.png)

Thanks to Spencer Sherk for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.