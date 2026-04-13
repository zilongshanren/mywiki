---
title: Graphics Programming weekly - Issue 281 - April 2nd, 2023
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-281/
author: Jendrik Illner
published: '2023-04-02'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- the article presents an overview of use cases for mesh shaders
- shows how to implement a mesh shader implementation that breaks down a mesh into parts and culls these
- presents frustum culling and cone culling for a meshlet-based model

![](../../assets/9390e8576f0e392c.png)


- the blog post introduces the VK_EXT_shader_object extension that allows Vulkan to be used without pipeline objects
- instead, applications create shader objects for each stage (and optionally link these). All state setting is dynamic
- the article describes performance expectations that drivers need to follow if they report the feature as supported
- additionally describes how to test the feature on hardware today

![](../../assets/4426dbb331b5015a.png)


- the paper introduces a generalized ray concept into wave-optical light transport
- presents how to use the generalized concept to apply path tracing sampling techniques to wave behavior modeling
- shows how the technique compares in quality and performance to existing techniques

![](../../assets/6ac29ed4b1fcc76d.png)


- the new D3D12 SDK adds support for CPU and GPU shared heaps on iGPUs and GPUs with re-bar support
- additionally adds support for texel coordinate sampling

![](../../assets/6ab4fa5cba166e09.png)


- the article explains what function derivatives are and how they are helpful in shaders
- presents a couple of examples to show derivatives in action

![](../../assets/97b307cdc0d4738d.jpg)


- slides of the GDC talking covering Geometric Algebra have been released
- the presentation covers the building blocks of the algebra and how it connects to concepts from other algebras
- shows how common operations and primitives can be represented using Geometric Algebra concepts

![](../../assets/fc22212dc84bd1a5.png)


- the detailed video tutorial shows how to implement raytracing applications
- explains and implements concepts such as reflection, simple sky models, depth of field, lighting, and much more

![](../../assets/08e9b6c5a390eb41.png)


- the new API allows applications to disable the use of kernel WRITE_WATCH for CPU-visible GPU memory
- applications promise to track access and inform pix explicitly instead of relying on the OF
- this is required because of limitations in win10 and non-insider builds of windows 11 today that affect performance negatively

![](../../assets/749b019a631bd9b0.png)

Thanks to [Adalberto Bruno](https://www.linkedin.com/in/adalbertobruno/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.