---
title: Graphics Programming weekly - Issue 202 - September 26, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-202/
author: Jendrik Illner
published: '2021-09-26'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents a few examples of how GPU fixed function hardware is used for other purposes besides the intended use-case
- including examples from nanite and an example of a point list was used for histogram generation
- the author is looking for user submissions of other examples

![](../../assets/37e0cbb912b2a8cc.png)


- the article provides an introduction to more hardware level information about GPU execution
- presents an overview for Nvidia, AMD, and intel information
- discussing many topics such as occupancy, register file, cache, scalar, and vector work
- additionally presents performance pitfalls and explains why they happen

![](../../assets/819c5a92eaa1ca17.jpg)


- the article provides a summary of the new hardware features in Apple GPUs
- covering lossy compression, sparse texture support, and SIMD improvements

![](../../assets/4fd871d2e676ea3f.png)


- the video provides a paper summary from NVidia that uses differentiable rendering to simplify geometry
- shows several examples, including a Disney island vegetation reduction to less than 1% of source vertex count

![](../../assets/af1f27053474d9e9.png)


- the article presents how to use MLIR (Multi-Level IR Compiler Framework) for efficient SPIR-V code generation for convolution filters
- shows how to take the logical expression of the task and transform it into patterns that are efficiently executed on ARM Mali GPUs

![](../../assets/65f6bd2b938783f9.png)


- NVidia provides an open-source dashboard for Jupyter and a standalone Boker server
- these dashboards are python based and expose real-time graphs for metrics such as memory usage, utilization, or memory traffic
- the article shows how users can extend the dashboards

![](../../assets/b67f9d6418de807f.png)


- video tutorial that explains lambert diffuse lighting function
- additionally also covers the required coordinate space transformations,
- finally shows how to implement the lighting model into OpenGL + GLSL

![](../../assets/9e6b6b363492d50f.png)

Thanks to [Manish Mathai](https://github.com/goodbadwolf/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.