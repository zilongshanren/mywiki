---
title: Graphics Programming weekly - Issue 301 - August 20th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-301/
author: Jendrik Illner
published: '2023-08-20'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the slides cover the difficulties of VR and what is required for a good user experience
- presents what hardware features the PS5 GPU supports to improve the results
- shows how raytracing was integrated into the rendering pipeline and an overview of the overall rendering pipeline
- covers how the sky rendering was implemented, introducing the mie approximations used
- additionally presents how multiple weather skys are implemented using multiple sets of lookup textures that are blended

![](../../assets/a4c427ebcf7d9f55.png)


- the article discusses the concept of focal length, presenting how different definitions of focal length are used for other aspects
- explains the underlying optics concepts to clarify the meaning
- discusses Nominal focal length, Pinhole focal length as well as Effective focal length

![](../../assets/4bf7dbb1020ebb80.png)


- the video explains how mirror balls enable the representation of 360-degree views
- focuses on the derivation of the mathematics of the approach and how to deal with projection bling spots
- additionally presents several demos and use cases of mirror sphere projections

![](../../assets/29a5244cf757a00c.png)


- the article presents how to use MTLFunctionStitchingGraph to allow the creation of a final shader from multiple pre-compiled pieces at runtime
- shows how to express that functions will be stitched at shader compile time, how to load and stitch the shaders from the API
- combines everything to show how to use the stitched graph to apply image processing operations

![](../../assets/fe2efef45678278b.jpg)


Do you want the chance to work with clients like Google, Microsoft, Activision, Qualcomm and other AAA studios??

This is an opportunity to join a world-leader in advanced real-time graphics who are working at the cutting-edge of the game industry.

- Bachelor’s degree in Computer Science or equivalent
- Experience with DirectX 12, Vulkan, Metal, or other current rendering API
- 2+ years professional graphics programming experience

Please apply with your resume attached by replying to [jiayi.zhuo@theforge.dev](mailto:jiayi.zhuo@theforge.dev)

![](../../assets/f555d89e1324ae06.png)


- the blog post gives insights into debugging crashes originating on the GPU
- presents what API level tools are available to track down the range of possible draw calls
- further expands from there to show how barriers can help to reduce the search space
- additionally shows how on AMD + Linux native hardware information is available to improve the debugging experience

![](../../assets/a813e28ae38003a6.png)


- AMD released a new tool to help with debugging GPU crashes
- the article provides a brief overview of the tool, what information is available, and how it’s to be interpreted
- additionally discusses the limitations and usage tips

![](../../assets/08f5eae06363606f.png)


- extensive bibliography of more than 3000 rendering papers
- collected by Wojciech Jarosz from papers, conferences, and own research findings

![](../../assets/8e29e712623fdc49.png)


- a combination of three conference presentations recordings from the sony creator event
- the videos cover VR, Ray tracing, and sky simulation in Gran Turismo 7
- Screen space shadows by Bend Studio, as well as ML Research by Haven Studios

![](../../assets/fddda93ce1865f29.png)


- the latest version of DXC switches the default HLSL version to 2021
- this article presents what number of cases where default behavior changed
- shows what changed and how the code needs to be adjusted. Presenting quick solutions and more ideal solutions to deal with the changed behaviors

![](../../assets/33d1d22ec5ae8329.jpg)


- release of a small header helper to implement a basic assert for GPU shader code
- will trigger a GPU memory exception on purpose to halt the execution
- helper is meant to be used together with Radeon GPU Detective

![](../../assets/5bc240109c40c026.png)

Thanks to [Giuseppe Modarelli](https://twitter.com/gmodarelli) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.