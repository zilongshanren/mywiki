---
title: GPU architecture resources
url: https://interplayoflight.wordpress.com/2020/05/09/gpu-architecture-resources/
author: Kostas Anagnostou
published: '2020-05-09'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I am often get asked in DMs about how GPUs work. There is a lot of information on GPU architectures online, one can start with these:

[Render Hell 2.0](https://simonschreibt.de/gat/renderhell/): Easy to follow and thorough introduction with extensive list of references for further study.[Life of a triangle – NVIDIA’s logical pipeline](https://developer.nvidia.com/content/life-triangle-nvidias-logical-pipeline). High level view of the NVidia’s GPU architecture[Triangles are precious](https://gpuopen.com/presentations/2019/nordic-game-2019-triangles-are-precious.pdf). High level view of AMD’s GPU (GCN) architecture.

And then can refer to these for a more in-depth study:

[From Shader Code to a Teraﬂop: How GPU Shader Cores Work](https://courses.cs.washington.edu/courses/cse558/11wi/lectures/05_gpuArchShaderCores_BPS_2011.pdf), Kayvon Fatahalian’s seminal presentation on GPU architectures. It is also worth check out his[Parallel Computer Architecture and Programming](http://15418.courses.cs.cmu.edu/spring2017/)Stanford course.[Trip down the GPU lane with Machine Learning](https://www.slideshare.net/RenaldasZioma/trip-down-the-gpu-lane-with-machine-learning-83311744), this presentation has a machine learning twist but also a good introduction to GPU architecture[A trip through the Graphics Pipeline](https://fgiesen.wordpress.com/2011/07/09/a-trip-through-the-graphics-pipeline-2011-index/), comprehensive series of posts on how each GPU pipeline stage works.[Understanding Modern GPUs](https://traxnet.wordpress.com/2011/07/16/understanding-modern-gpus-1/), another series of blogposts on how the various GPU pipeline components work.[Low-Level GPU Documentation](http://renderingpipeline.com/graphics-literature/low-level-gpu-documentation/), a large collection of publicly available GPU documentation including NVidia, AMD and Intel[AMD GPU Open](https://gpuopen.com/games-cgi)good resource, they often share low-level posts on AMD GPUs.[Intel processor graphics: architecture and programming](https://doc.lagout.org/electronics/Intel-Graphics-Architecture-ISA-and-microarchitecture.pdf), low level presentation with a lot of details on Intel’s GPU architecture.

It is also a good idea to look for documentation about how compute shaders work, like:

[Introduction to compute shaders](https://anteru.net/blog/2018/intro-to-compute-shaders/),[More compute shaders](https://anteru.net/blog/2018/more-compute-shaders/)and[Even more compute shaders](https://anteru.net/blog/2018/even-more-compute-shaders/), a great series on compute shaders.[Compute Shaders: Optimize your engine using compute](https://www.youtube.com/watch?v=0DLOJPSxJEg), introduction to compute shaders and how do they differ from vertex and pixel shaders from a programming and a hardware perspective.[Intro to parallel programming](https://www.youtube.com/playlist?list=PLGvfHSgImk4aweyWlhBXNF6XISY3um82_), worth watching course on programming with compute shaders (CUDA, but transferable).

as they are “closer to the metal” than pixel/vertex shaders in that they require you to think in threads and often synchronise execution and manage memory.

Also posts that discuss GPU profiling and performance, such as

[The Peak-Performance-Percentage Analysis Method for Optimizing Any GPU Workload](https://devblogs.nvidia.com/the-peak-performance-analysis-method-for-optimizing-any-gpu-workload/)and also[Fixing the Hyperdrive: Maximizing Rendering Performance on NVIDIA GPUs](https://www.gdcvault.com/play/1024810/Fixing-the-Hyperdrive-Maximizing-Rendering).[GPU Performance for Game Artists](http://fragmentbuffer.com/gpu-performance-for-game-artists/)[What’s up with my branch on GPU?](https://aschrein.github.io/jekyll/update/2019/06/13/whatsup-with-my-branches-on-gpu.html)

as they often expose details about how a GPU works.

Additionally, it is worth searching for “GPU” or “performance” in the [GDC Vault](https://www.gdcvault.com/), it can often return some relevant presentations.

I am closing this nowhere near exhaustive list with a few alternative presentations of GPU architecture concepts:

[Understanding the anatomy of GPUs using Pokémon](https://www.ovh.com/blog/understanding-the-anatomy-of-gpus-using-pokemon/), which uses a trading card paradigm for GPU architecture learning[Where do GPUs come from](http://c0de517e.blogspot.com/2017/05/where-do-gpus-come-from.html), which uses a robot manufacturing pipeline paradigm to explain how GPUs work.