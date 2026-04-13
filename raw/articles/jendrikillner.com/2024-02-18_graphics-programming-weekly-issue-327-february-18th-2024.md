---
title: Graphics Programming weekly - Issue 327 - February 18th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-327/
author: Jendrik Illner
published: '2024-02-18'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- The paper introduces a machine learning model that generates a set of PBR Textures (albedo, Roughness, Metallic)
- trained on a locked RGB model to take advantage of existing models
- discusses how the model was designed, tradeoffs, and common failure cases

![](../../assets/e0de58ab54a0d8b3.jpg)


- the article discusses the new RenderGraph implementation in Godot 4.3
- discusses the limitations of the old system and the advantages of the new system
- shows the implementation of dependency tracking, dealing with sub-resources
- additionally discusses CPU and GPU performance impact

![](../../assets/79c9390db01363f0.png)


- the blog post article discusses the implementation of a box blur shader
- presents explanation of Gaussian, Kernels, Separable blurs
- closes with a discussion of things to do and avoid when implementing a blur shader for good results

![](../../assets/03a87e090b903e21.jpg)


- the Rendering Engine Architecture Conference is looking for speakers for the 2024 edition
- post describes what kind of talks are being looked for and the formats of the talks

![](../../assets/4ee8de3caaa73bd9.png)


- the course presents an introduction to GPU compute shader algorithms
- discusses the primitives available
- how to implement parallel reduction, prefix scan, and radix sort
- additionally presents a look at optimization techniques

![](../../assets/b8172214617b12fb.png)


- the video provides a history of ant-aliasing techniques used in games
- discusses capabilities and limitations of the different AA techniques
- presents in-depth the advantages and disadvantages of temporal antialiasing techniques
- all examples are presented with videos from games that use the presented techniques

![](../../assets/3de30c9b7ba0b406.png)


- the article explains the extension method to gradient descents called Adam
- provided implementation is shown in C++

![](../../assets/dd55a81bf7c712b9.png)

Thanks to [Angel Ortiz](https://twitter.com/aortizelguero) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.