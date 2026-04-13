---
title: Graphics Programming weekly - Issue 205 - October 17, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-205/
author: Jendrik Illner
published: '2021-10-17'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents how using HDR and 3D scan data, it’s possible to reconstruct the material BRDF parameters
- shows how to estimate the diffuse lighting, surface albedo and use this information to treat it as an optimization problem to match the original image

![](../../assets/e64770f9cf31055e.png)


- the tutorial covers a walkthrough of a foliage shader in Unity
- covering double-sided materials, translucency, normal adjustments for more natural diffuse shading, and wind deformations

![](../../assets/71f6782dc00d8d03.png)


- the in-depth video tutorial explains how to render a circle using shadertoy
- explains the required math and implementation in shader code

![](../../assets/3dcb40663bb16786.png)


- the blog introduces the topic of shader permutations and why they end up being common issues
- discussing not only the compilation side but also runtime implications
- additionally presents a list of questions that a programmer might ask when creating a new shader permutation

![](../../assets/3cc370c6881da13f.png)


- the article dives deeper into the issues related to shader permutations
- covering several possible solutions, discussing the tradeoffs of the different methods presented
- additionally presented a brief look at the future with callable shaders or function pointers
- closes with an overview table of the different methods, advantages/disadvantages, and what platform it’s supported on

![](../../assets/49663deebafeb72a.png)


- collection of Neural Radiance Field papers that will be presented at Intl. Conf. on Computer Vision
- starts with a brief summary of what Neural Radiance Fields are
- includes a small single sentence summary for the content of papers for each

![](../../assets/bea8e8380f941b6b.png)


- frame breakdown of a single frame from the game control (as video and text)
- covering shadow rendering, ray tracing passes
- denoising, tech art passes, as well as Deep Learning Super Sampling (DLSS)

![](../../assets/e4aa162ec208ec8f.jpg)


- Twitter thread asking for GPU architecture information
- the replies are full of fantastic resources

![](../../assets/83a399787e025406.png)


- the article shows how recent versions of DXC can link DXIL shaders for all shader stages
- presents the API as well as discusses existing restrictions

![](../../assets/264bee7e6fcdbca0.png)


- interview with Nick Thibieroz, Director of Game Engineering at AMD
- discussing AMD FSR objectives, design considerations, the impact of Machine Learning
- additionally provides a few pointers at what different engine integrations could be considered

![](../../assets/e66e78873616f154.png)

Thanks to [Keith O’Conor](https://twitter.com/keithoconor) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.