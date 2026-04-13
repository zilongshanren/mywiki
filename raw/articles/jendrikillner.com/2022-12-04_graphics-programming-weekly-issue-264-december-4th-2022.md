---
title: Graphics Programming weekly - Issue 264 - December 4th, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-264/
author: Jendrik Illner
published: '2022-12-04'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a new method to calculate texture MIP maps that preserves compatibility with existing MIP mapping techniques
- the technique uses neural networks to optimize the transfer of material appearance under varying view distances and lighting conditions
- presents the results on two distinct BRDF models (Anisotropic GGX and Anisotropic Beckmann)

![](../../assets/31f4fa4871c7d1e0.png)


- the video provides a summary of the cloud rendering techniques covered in Horizon: Zero Dawn and the FrostBite engine papers
- shows the individual components visually and how they are combined to create the final cloud effect
- a brief discussion of performance optimization possibilities

![](../../assets/31a26c9b55d97d82.png)


- the article continues the series on spectral rendering
- this part focuses on methods to “upsample” sRGB colors to spectral representations
- presents an implementation of Spectral Primary Decomposition for Rendering with sRGB Reflectance and discusses possible improvements

![](../../assets/b2ad61ae5b265ad5.png)


- the video presents how the author developed a pong game using only a pixel shader in Unity
- shows how to use the alpha channel of the render target to store persistent state

![](../../assets/3d5c23bb686e33b3.png)


- the video focuses on the definition of a procedural terrain from a vertex shader
- presents how to combine different noises and rotate patterns to create a planet

![](../../assets/988a32e1e1522710.png)


- the video is the latest part of an OpenGL learning series that focuses on the explanation of vertex data transformation
- explains the concepts of space transformations, focusing on how to change object positions in the world through the use of a world matrix
- shows how to pass information from the C++ runtime to the OpenGL shaders

![](../../assets/2bcb3e7224bbbe48.png)


- the article explains how two implements two different types of dithering in metal shaders
- presents and compares ordered and diffusion dithering algorithms

![](../../assets/8743aee626d50e34.jpg)


- the video does a deep dive into deferred shading techniques to explain why a graphical artifact in Zelda’s Breath of the Wild appears in a specific place
- starting with a discussion of lighting techniques
- shows how the scenes are rendered, what intermediate information is stored, and how it’s used for light calculations (including many visualizations)
- finally, it concludes by showing how the error happened and why it’s localized to specific locations in the world

![](../../assets/81873528f0cec051.png)


- the article presents the library that allows C# code to be executed via HLSL, D2D1, XAML, and more
- shows the developer experience, explaining how the code is transformed for GPU execution
- presents the two execution models that showcase performance vs. ease of use

![](../../assets/72e4ca761627cb6f.png)

Thanks to [Jan-Harald Fredriksen](https://twitter.com/jhfredriksen) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.