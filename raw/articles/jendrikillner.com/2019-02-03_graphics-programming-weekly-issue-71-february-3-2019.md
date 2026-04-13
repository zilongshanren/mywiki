---
title: Graphics Programming weekly - Issue 71 — February 3, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-71/
author: Jendrik Illner
published: '2019-02-03'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

The results of the survey have been published [here](https://www.jendrikillner.com/post/graphics-programming-weekly-survey-2018-results/)

- discusses screen space reflection and planar reflections techniques
- presented technique for reflections uses ray-marching against the terrain height map to calculate the reflections
- show that the technique could be extended to trace against signed distances fields to add reflection for other objects too

![](../../assets/2e37c6ce396d72f5.jpg)


- show how a projection matrix is formed
- explains GPU clipping and how it relates to the projection matrix
- many videos explain the significance of each component visually
- provides a calculator to help gain a more intuitive understanding

![](../../assets/a203fab119f3aecc.png)


- twitter thread discussing mip-map selection algorithms
- comparison between the custom shader implementation and hardware solution

![](../../assets/cd82970906006f4f.png)


- introduction into physically based shading
- presents how light is reflected and refracted when it comes into contact with surfaces
- shows how metal and dielectrics (non-metals, insulators) interact with light differently and how this forms the visual perception of different materials

![](../../assets/030bce614953cd6f.png)


- presents a technique to distribute an infinite sequence of points on the surface of an arbitrary triangle evenly

![](../../assets/17c18c91565b9ff4.png)


- the article points out that albedo textures are commonly stored in sRGB color space and need to be converted into linear color space before using in shading
- achieved using the correct SRGB texture format
- comparison images present the differences between sRGB and non-sRGB color formats

![](../../assets/c9ae6c444acc2ddf.png)


- thesis presentation covering snow rendering
- presents the visual features of snow with real-world reference pictures
- an overview of existing techniques
- defines 4 defining characteristics for snow shading and develops a BRDF from them

![](../../assets/ce355d0984ab319b.png)


- a short post that shows how to make an object appear infinitely large without clipping artifacts
- adjusts the vertex position in the vertex shader so that they are mapped onto the far plane

![](../../assets/b159a9333e53c704.png)


- extends the custom scriptable rendering pipeline, the previous part was covered in
[issue 66](https://www.jendrikillner.com/post/graphics-programming-weekly-issue-66/) - now adds support for directional shadows, such as sun shadows
- shows how to deal with common shadow artifacts
- implements cascaded shadow mapping for the main directional light

![](../../assets/d8d0fb44d556ca0d.jpg)


- weekly series with twitter posts about tech art techniques and ideas

![](../../assets/66667c523daf39bf.png)


- summary of resource about getting started with tech art
- mainly unity shader focused


- new PIX for windows version
- performance counters are now supported on AMD Radeon 7 GPUs and NVIDIA Turing GPUs
- more consistent and reliable timing data on all GPUs

![](../../assets/90f2c23fdeae914b.png)