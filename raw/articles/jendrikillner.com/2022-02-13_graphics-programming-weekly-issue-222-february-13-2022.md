---
title: Graphics Programming weekly - Issue 222 - February 13, 2022
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-222/
author: Jendrik Illner
published: '2022-02-13'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the blog post presents the new features of shader model 6.7
- improved texture operations such as Raw Gather (unmodified retrieval of the 4 samples from bilinear sampling)
- writable MSAA textures, quad-level operations
- additionally introduces programmable offsets for load and store from runtime variables instead of compile-time constants

![](../../assets/bab8b0ce0733eeec.jpg)


- the article provides an overview of the development process of using a texture-based imposter system using raymarching
- shows the different steps in the development process, quality improvements along the way
- additionally discusses what ideas the author tried, what did and didn’t work, and discusses why they didn’t work

![](../../assets/ff909a8a6cc90706.png)


- Video lecture series of the real-time rendering course at TU Wien
- this part covers how to use hardware-accelerated ray tracing from Vulkan
- covers everything required to render a static scene, accelerations, ray traversal, shader bindings as well as processing hits
- additionally presents ray queries to allow ray tracing from any shader stage and discusses the limitations

![](../../assets/baf88e876d14c940.png)


- the article discusses a problem with effects caused by loss of floating-point precision when game-time is growing
- presents a method to reset periodic timers cleanly and still allow for continuous motion
- the suggested solution uses integer multipliers with required precision to make resetting motions natural from an effect tweaking perspective

![](../../assets/d2386824b568dd79.png)


You are helping our core team to develop cutting-edge 3D data optimization technology, being used in production pipelines to process millions of 3D data sets each year, fully-automatically. You are performing research on 3D mesh processing, texture baking, UV mapping, optimization algorithms and ML-based algorithms for 3D data optimization and QA.

![](../../assets/e1093cad59141f24.jpg)


- a collection of tweets about tech art, VFX, and related topics
- showcases of in-progress developments and experiments

![](../../assets/74f32cba1428c02c.png)


- video introduction tutorial to shader programming with OpenGL
- provides a conceptual overview of how to author, load, and use shaders GLSL shaders from OpenGL
- discusses vertex transformations required project vertices onto the screen
- shows how to access information from the CPU in shaders
- presents multiple examples to show the practical usage

![](../../assets/accc7725391ce688.png)


- the video session explains Texture set up for usage from GPU shaders
- covering texture types, addressing, tiling, texture filtering
- shows how to access the data from the GPU and the necessary OpenGL setup steps
- additionally provides an overview of the Mesh Color technique and how to represent it as texture maps

![](../../assets/91fddc7e2d861953.png)


- the article provides an overview of using raytracing to generate ambient occlusion
- recaps of ambient occlusion techniques for rasterization, high-level representation of raytracing based implementation

![](../../assets/9561aa0f85d4824b.png)


- a roundup of WebGPU topics discussed at the January meetup
- contains references to best practices, new extensions as well as community work showcases
- additionally contains information about the state of support across browsers

![](../../assets/86a65f9c36f8668e.png)

Thanks to [Mike Turitzin](https://miketuritzin.com) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.