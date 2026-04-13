---
title: Graphics Programming weekly - Issue 338 - May 5th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-338/
author: Jendrik Illner
published: '2024-05-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the GDC talk presents a great explanation of Quaternions and expands the concepts to cover dual quaternions
- presents interactive and visual examples of the different components and operations involved
- shows issues and limitations with matrix interpolations and how quaternions and dual quaternions can solve these limitations

![](../../assets/689845e04c8e9341.png)


- this blog post covers how to extend a raytracer in a voxel world with support for reflections
- expands perfect reflection to allow for refraction
- contains challenges for the reader to develop their understanding further

![](../../assets/79728a8c9016d88c.png)


- the paper introduces a method for view synthesis of facial expression captures in 3D views not captured
- the presented solution is running at real-time rates without relying on machine learning techniques
- achieved using a layered mesh for view-dependent information and mixing this with view-independent RGBA texture video
- the included paper presents a summary of the technique, compares it against existing solutions, and discusses the limitations of the approach

![](../../assets/4781d9dfb978df6d.png)


- the video presents a summary of all the papers that will be presented at the I3D Conference 2024
- shows a brief summary of a couple of seconds for each paper
- papers cover an extensive range of topics, from ML techniques, VR research, upcoming display technologies, new filtering approaches, and much more

![](../../assets/021746da3599054b.png)


- the paper discusses a generative model that is trained to generate multiple types of noise and blend between them
- presents the network architecture, how it has been implemented and improved
- shows many examples of the generated results

![](../../assets/ca8227b8521e67bf.jpg)


- the paper presents a framework to shape rendering noise to optimize samples for perceptual quality and denoising performance
- shows how sampling patterns can be optimized to take advantage of knowledge about post-processing spatial and temporal filtering characteristics
- demonstrates how to use the framework on example applications

![](../../assets/c0239fbf4b2f8063.png)


- the video shows the limitations of Nanite from an artist’s perspective
- presents the debug views to explain why vegetation scenes are more difficult for the system to process
- discusses possible solutions through the use of procedural generations and fallback LODs

![](../../assets/1b6c58b82b0da0cc.png)


- the Godot engine is switching the definition of near/far plane, with the near plane now mapping to a depth of 1 and the far plane to 0
- this post explains common patterns that are affected by this change
- additionally provides links to explain why this new mapping allowed significantly improved depth buffer precision

![](../../assets/e419e659cde3925e.png)

Thanks to John Burton for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.