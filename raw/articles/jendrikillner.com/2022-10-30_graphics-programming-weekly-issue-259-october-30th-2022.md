---
title: Graphics Programming weekly - Issue 259 - October 30th, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-259/
author: Jendrik Illner
published: '2022-10-30'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a mesh computation compiler that separates mesh operations from the data partitioning
- the system partitions meshes into sub-patches and reorganize mesh data so that attributes can be accessed from local on-chip memory
- presents performance results and compares against RXmesh, another system that tries to optimize mesh access patterns

![](../../assets/58dc6cdd6c3ff80f.png)


- the video shows the importance of color profiles
- presents how in the absence of profiles, applications are free to interpret the results
- shows how the most reliable way to get consistent results across applications is to convert from authoring color space into sRGB
- additionally shows how to inspect color profiles

![](../../assets/663e2b747e8d5041.png)


As a 3D Engineer at Threedy, you develop our core system’s algorithms and data structures, always optimizing data representations for efficient and cutting-edge 3D data streaming and visual computing.

![](../../assets/2365cbc531701a1a.png)


- the video presents a new upsampling technique developed by intel (Temporally Stable Real-Time Joint Neural Denoising and Supersampling)
- presents a comparison against previous techniques
- shows that the technique can significantly improve denoising and also upscale the image to higher output resolutions

![](../../assets/e49c6cf6017a832a.png)


- the tutorial presents how to rotate a texture in 2D space
- explains rotation matrices, how to rotate around different positions of the plane
- additionally presents the necessary steps to integrate into Unity for demonstration

![](../../assets/2794518fd9fccb37.png)


- the article describes a possible solution to generate a color palette with neighboring colors being most different from each other
- presents issues with some possible solutions
- it additionally presents ideas about weaknesses of the offered solution and possible improvements

![](../../assets/8fe74e78fb91ecab.png)

Thanks to [Marius Horga](http://metalkit.org/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.