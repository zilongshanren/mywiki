---
title: Graphics Programming weekly - Issue 85 — May 19, 2019
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-85/
author: Jendrik Illner
published: '2019-05-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- shader tutorial aimed at beginners that teaches shader fundamentals using Panda3D and GLSL
- starting with the basics of coordinate spaces, and GLSL shaders
- shows how to implementing texturing, lighting, normal mapping
- additionally outlining, fog, bloom, screen space ambient occlusion, depth of field and several stylization techniques

![](../../assets/ebce1b25d1ae4f71.png)


- explains tone mapping terms and how the human vision perceives changes in luminance
- the viewing environment has a significant influence on the perceived dynamic range
- shows how different display technologies deal with bright pixels and what artifacts they produce
- FreeSync provides information about the HDR capabilities of a connected to monitor to the application to be able to adjust the tone mapper accordingly

![](../../assets/99b988d4a274b6b8.png)


- paper on path trace denoising
- aimed at interactive scenarios with 1 sample per pixel
- using linear regression and temporal anti-aliasing combined with many problem-domain specific improvements

![](../../assets/07c3ead7fb45557a.png)


- Vertex Descriptors in Metal allow the programmer to describe the memory layout of vertices
- shader compiler inserts the necessary fetch logic to read the data correctly
- this allows decoupling of vertex memory layout from the usage in shaders

![](../../assets/79e1b86c8124596f.png)


- shows how to implement Asymmetric Projection
- adjust the projection on a render-to-texture in 3D space so that it appears as if the viewer is looking through a portal into another 3D space

![](../../assets/3b581debe6755c3d.png)


- the new version adds support for hardware-level tracing on an instruction level
- now shows the ISA inside of the pipeline view too
- support for user markers have been added
- a small overview of how to interpret the provided data

![](../../assets/2879f8425e38713b.png)


![](../../assets/3e7df82ca63aa009.png)

- the tutorial shows how to use BGFX running on Linux
- initialize BGFX, load shaders, and models and draw a cube on screen

![](../../assets/085ab83f83e23bf8.png)


- example project for a course teaching the basics of shader development using Unity
- covers vertex, pixel, surface shaders
- additionally talks about Shader Graphs and post-processing

![](../../assets/7dddf3e6d83c2c8b.png)


- collection of VFX tweets of the week
- tutorials, demos, and showcases of great looking effects

![](../../assets/719bfff246a7a764.png)


- presents what kind of approximations are still required to be done in Physically Based Rendering
- opens the question that we should start looking at the approximations to determine where to focus on for the next generation of visuals

![](../../assets/ad99c41fff6fce43.jpg)


- proposal of requirements that would allow WebGPU to be used as a common cross-platform abstraction

Thanks to [Deepak Surti](http://www.deepaksurti.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.