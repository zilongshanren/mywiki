---
title: Graphics Programming weekly - Issue 270 - January 15th, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-270/
author: Jendrik Illner
published: '2023-01-15'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the new AMD hardware guide for RDNA3 has been released
- covers the shader execution model, the various wave execution models
- as well as how the shader core interacts with the memory hierarchy

![](../../assets/1f6ce4f9e19fc87f.png)


- the article shows techniques implement conservative techniques to project bounding boxes and spheres into screen-space
- these techniques are optimized for use in culling use cases as it affects the meaning of near-z clipping
- presents trade-offs between the techniques in terms of computational cost and culling efficiency

![](../../assets/b310be8b54b4de59.png)


- the article describes how the Use.GPU level of abstraction is continuing to evolve
- presents how scene management can be natively expressed as part of the same pass-based architecture
- shows how the same high-level logic allows switching between deferred and forward rendering easily
- additionally discusses strange limitations in the graphics APIs that make switching work between texture formats, pixel shaders, and compute shaders more difficult

![](../../assets/ab6507cfa92282e6.jpg)


YOU are looking to revolutionize the world of 3D in industrial environments and enjoy working in a highly innovative team?

Develop next-gen rendering technology, create high-performance pipelines and write complex real-time shaders. We are guaranteed to have interesting topics for YOU!

![](../../assets/2365cbc531701a1a.png)


- the article provides an overview of Tangen Space Encodings
- covers how to use Octahedral Encoding and further compress it with Tangent Angle
- from there, develops the suggested Diamond Encoding technique that extends the Octahedral approach into the tangent angle space
- additionally provides a brief section on rethinking how tangent space encoding might be better expressed on a mesh(let) level on modern hardware

![](../../assets/842acd043271f96a.png)


- the article presents the Meta Quest exclusive features of the RenderDoc fork
- the extensions allow the visualization of the tiled-based hardware binning into screen tiles and how they are executed
- allows drawing call tracing to gather the latency of draw calls
- additionally allows the collection of hardware statistics of shaders through KHR_pipeline_executable_properties

![](../../assets/1a5df23073abc9d3.png)


- during the Vulkanised 2023 conference in Munich, a full-day tutorial will take place
- this post explains the target audience of the course and the associated price

![](../../assets/832b4d1327887372.jpg)


- the article aims to develop an intuition for FFT (Fast Fourier Transform) and how it’s underlying the math of waves
- provides a large number of interactive examples to experiment with the effects of different parameters
- contains a high-level introduction to complex numbers and how they relate to rotation and scaling

![](../../assets/11281ec36f0338b9.png)


- the author describes the personal experience with GLSL and HLSL gained through moving AnKi 3D between the shading languages
- mentions why HLSL seems like a better bet for the long-term future
- also mentions shortcomings of using HLSL when developing Vulkan applications

![](../../assets/72a5e3947fccea3f.png)


- the blog post explains how to improve the precision when encoding min-max per tile
- the author suggests storing only one as an absolute value and a delta to reconstruct the other

![](../../assets/3d5387306197fd40.png)


- the article covers how Wave Matrix Multiply Accumulate (WMMA)
- presents how to use the intrinsics available in the HIP framework to accelerate the matrix operations typically found in machine learning work

![](../../assets/c5c849f69c5ce42d.png)

Thanks to Peter Kohaut for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.