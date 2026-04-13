---
title: Graphics Programming weekly - Issue 251 - September 5, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-251/
author: Jendrik Illner
published: '2022-09-05'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the short video provides a great visual introduction to distance functions and ray marching
- presents how to express shapes using implicit surfaces
- showing techniques to combine different shapes and animate them

![](../../assets/770bf22b1100a026.png)


- the article shows the Grid-Based Reservoirs sampling technique for dynamic lights in participating media
- this enables the temporal reuse of samples among neighboring rays
- shows the different stages of the implementation and how different sampling and noise distributions change the results

![](../../assets/48fabb169136b330.png)


- mesh shader support has been added to Vulkan through VK_EXT_mesh_shader
- the article compares the API against D3D12 and the previous Nvidia extension
- Khronos additionally provides several queryable attributes that developers can use to tune the algorithms for the hardware capabilities and requirements

![](../../assets/5b890c567ff3152c.jpg)


- the video starts with a visual overview of rasterization, raytracing, and hybrid rendering techniques
- the talk focuses on how intel hardware is designed to efficiently support raytracing
- contains benchmark comparisons of expected performance compared to an RTX3060

![](../../assets/aa5d400fe7db7e3c.png)


- the article presents a method to generate Progressive blue noise samples that follow the image content
- shows the implementation in python
- discusses the effects of different parameters and how they can be used for the required results

![](../../assets/e33085fd91e34084.png)


- the video presents how to implement two VHS effects, interlacing lines and YIQ color grading, in a post-processing effect
- walkthrough of the effect is provided in both Unreal and Unity

![](../../assets/b47cd77da44f89ab.png)


- the blog presents the idea of using a simple neural network to encode diffuse indirect light for a scene
- discusses the various steps in the experiment
- presents the final results and discusses weaknesses of the approach

![](../../assets/dc06b0eb16975bb7.png)


- second year of the spectral rendering Siggraph course
- focusing on the practical aspects of spectral rendering
- shows the limitations of RGB and discusses the advantages of spectral rendering and workflows

![](../../assets/98e33f48c9894b17.png)


- a collection of tweets about tech art, VFX, and related topics
- showcases of in-progress developments and experiments

![](../../assets/3067d17a5e3b25cd.png)

Thanks to [Giuseppe Modarelli](https://twitter.com/gmodarelli) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.