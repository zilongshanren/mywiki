---
title: Graphics Programming weekly - Issue 350 - July 28th, 2024
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-350/
author: Jendrik Illner
published: '2024-07-28'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the paper presents a new method to apply strokes to lines in a GPU-friendly way
- presents how to lower filled and stroked Bézier paths into an Euler spiral as an intermediate representation
- tests and shows the performance of the implementation on CPU and GPUs
- video and code have been released

![](../../assets/80d0994747616e3a.png)


- the presentation recording discusses the development of the Vulkan ecosystem
- how LunarG came to deliver the Vulkan SDK, the history of the developments, and ecosystem overview
- presents a look into the development approach, improvements, and how it worked in practice

![](../../assets/c84a7312a9882d5f.png)


- the presentation covers the current state of OpenPBR and the state of integration into MaterialX
- updates on the state of support in tools
- additionally provides a look at the upcoming developments

![](../../assets/2601127a9d3ecc3b.png)


- the paper presents a concurrent binary tree (CBT) for adaptive triangulations of arbitrary (half-edge) meshes
- shows how to use a CBT as a memory management construct

![](../../assets/e4ad07508a0bfe64.jpg)


- the paper presents an approach to BVH construction based on the parallel locally- ordered clustering approach (PLOC) and PLOC++
- shows how to implement the algorithm in a single kernel launch
- explains a method to convert the binary BVH into wide BVHs where each parent can have an N number of child nodes

![](../../assets/62ef8c5ff3cee2ab.png)


- the paper presents a block-compressed geometry format
- explains the data packing applied, what can be encoded, and how to compress it
- presents memory comparisons against existing solutions
- additionally shows how hardware support with ray-tracing BVH builds might reduce memory consumption

![](../../assets/b6628d227d1194a5.png)


- the blog post provides an overview of generating a procedural world
- discusses how biomes, terrain, grass, and flowers are placed
- additionally shows how they turned the flat world into a sphere

![](../../assets/0a620e558e8f556d.jpg)


- This paper provides a deep dive into Disney’s Hyperion Renderer’s many-lights sampling system
- presents how it caches and interpolates light sampling distributions at points throughout space
- Presents how the approach allows the incorporation of learned visibility estimates into light sampling distributions

![](../../assets/3e164ebaf2a2aff2.png)


- the paper presents a voxel scene processing model that allows on-demand production of data during rendering
- presents how to overlap the work to reduce synchronization and starvation issues
- shows a way to visualize the execution of GPU cores on a dynamic timeline

![](../../assets/63bb2d87dbd541e9.png)


- AMD released a tool to help measure input to screen latency on Windows
- users can specify a region to watch for changes; if a simulated mouse event triggers a change in this region, it calculates the latency and records for later analyses

![](../../assets/859cd1de8b3c6ddd.jpg)


- the blog post provides an overview of the author’s implementation of Screen Space Indirect Lighting with Visibility Bitmask
- presents an overview of the technique, discussing tradeoffs of the implementation
- shows the results in-engine in a test scene and shows the shader implementation in GLSL

![](../../assets/4b44d2adb192fe7c.jpg)


- the video tutorial provides an overview of the normal mapping technique
- explains the limitations of vertex and interpolated vertex lighting
- followed by an explanation of how normal maps allow additional information and how to generate this required data
- finally, it provides a detailed discussion of the implementation steps using OpenGL/GLSL

![](../../assets/71f3b4c638c22192.png)

Thanks to Jhon Adams for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.