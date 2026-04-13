---
title: Graphics Programming weekly - Issue 284 - April 23rd, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-284/
author: Jendrik Illner
published: '2023-04-23'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- a collection of papers from the I3D 2023 presentation
- contains links to the papers and related material where available

![](../../assets/594c260075c9f8d8.png)


- the GDC talk explains how Quaternions and Dual Quaternions work and how they affect objects under transformation
- starts by building an understanding of Quaternions, shows the advantages and limitations
- followed by an extension to cover Dual Quaternions, explaining what problems they solve and how they compare to 4x4 transformation matrices

![](../../assets/e1d01de0a300a3ad.png)


- the GDC presentation discusses the new sky rendering model developed for GT7
- presents the physical foundations and how to simulate them in an offline rendering system
- followed by how the sky method has been adjusted to be used in real-time through heavy use of LUT
- discusses how to control the method through simplified parameters
- additionally covers how they approached cloud rendering

![](../../assets/64c28564ff014a5c.png)


- the short tutorial presents how the FXAA algorithm is implemented
- presents how the algorithm works in simple terms

![](../../assets/d9297b046f7465ad.png)


- the article discusses techniques to calculate Bézier that use fewer segments than the existing original path
- presents the importance of an error metric and discusses different available options

![](../../assets/491c8260ed0cfd34.png)


- the latest version released from the Open MaterialX standards adds support for MaterialX Graph Editor and support for Metal shader generation
- also adds support for coated emissive surfaces and bitangent input vectors

![](../../assets/a110e3c68959e2e2.png)


- the article presents several different methods to convert between 32 and 16-bit floating point formats
- discusses the implementation, issues, and considerations with each technique

![](../../assets/e527524114992db7.png)


- the tutorial explains how to use WebGPU to use compute shaders to calculate the MIP maps for textures
- presents the implementation of a one MIP level at a time technique

![](../../assets/7b9aac11e3c9f5ce.png)


- the article presents how to introduce custom shader nodes into the Godot Visual shader graph
- shows an example of how to color an object following the UVs

![](../../assets/99308c5987573306.png)


- the article introduces two new interactive playgrounds for integer and floating point numbers
- allows experimenting with how different numbers are encoded into the underlying bit patterns

![](../../assets/7a2bb0193c64b6a8.png)

Thanks to [Lesley Lai](https://lesleylai.info) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.