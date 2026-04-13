---
title: Graphics Programming weekly - Issue 214 - December 19, 2021
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-214/
author: Jendrik Illner
published: '2021-12-19'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents alternative mesh structures to generate grid structures
- shows why two-right angle triangles are problematic under motion transformation
- discusses Rhombuses and Hexagons as alternatives

![](../../assets/cae4063e8be4cb1d.jpg)


- the article introduces a technique and generated textures that enable the use of Spatiotemporal blue noise
- the article discusses the importance of Spatiotemporal blue noise, presents comparisons against existing techniques
- additionally presents several use cases for the presented technique

![](../../assets/2ca9a1910921f345.png)


- the article discusses Spatiotemporal blue noise in more depth
- showing best practices for several scenarios
- additionally shows how to extend the provided blue noise texture for other use-cases

![](../../assets/5ccd7ba8b61bba2d.png)


- the second part of the game of life shadertoy implementation focuses on the improvement of the visuals
- additionally adds the ability to interact with the simulation using the mouse

![](../../assets/ce8ee71e666223e3.png)


- the video of the Vulkan lecture series introduces the stages of the graphics, compute, and raytracing pipe using Vulkan
- explains the stages, how the order is maintained as well as how the stages are essential for a correct understanding of synchronization
- providing an overview of the new Synchronization2 system in Vulkan and how it differs from the previous iteration

![](../../assets/14426e3b2585c362.png)


- the author presents the design for a composable GLSL system based on the idea of closure
- discusses the difference of binding models, how to connect CPU and GPU components in a composable system
- shows how the runtime being aware of all GPU data enables rendering only if any data changes could generate a different image

![](../../assets/bb66a1a7148ca3f7.png)


- the article discusses advice for new research on how to effectively read research papers
- written from the perspective of machine learning, but the lessons apply to computer graphics as well

![](../../assets/5296ed73e155094e.jpg)


- a collection of tweets covering a large variety of tech art topics such as
- interior mapping, shading for 2d games, VFX showcases, as well as a rule-based terrain texturing system

![](../../assets/1e8dd94ee57f014c.png)


- the article describes how to use a Vulkan bindless setup for 2D sprite batching
- presents how to pass the necessary texture index into the shaders
- shows the importance of nonuniform qualifier at texture sample time
- additionally presents how to integrate the technique into imGUI

![](../../assets/e5b0f206a21c1c35.png)

Thanks to [Ken Russell](https://twitter.com/gfxprogrammer) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.