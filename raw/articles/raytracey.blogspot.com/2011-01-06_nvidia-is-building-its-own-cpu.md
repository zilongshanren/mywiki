---
title: Nvidia is building its own CPU!!!
url: http://raytracey.blogspot.com/2011/01/nvidia-is-building-its-own-cpu.html
author: Sam Lapere
published: '2011-01-06'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is HUGE news!! Nvidia today announced Project Denver at CES, an ARM-based CPU core manufactured by Nvidia which will be integrated into the GPU. This high-end GPU/CPU chip will provide the killer platform for real-time path tracing and will pave the way for truly real-time (30fps, 1080p) path traced games with photorealistic quality graphics.


Bill Dally, chief scientist at Nvidia, already hinted that


Bill Dally, chief scientist at Nvidia, already hinted that

[future GPUs from Nvidia will be incorporating ARM-based CPU cores on the same chip as the GPU.](http://raytracey.blogspot.com/2010/09/kepler-and-maxwell-ray-tracing-monsters.html)Now it's official (Project Denver will first appear in the Maxwell GPU, see[http://raytracey.blogspot.com/2011/01/nvidias-project-denver-to-appear-first.html](http://raytracey.blogspot.com/2011/01/nvidias-project-denver-to-appear-first.html))! There's an interesting blog post from Bill Dally on[http://blogs.nvidia.com/2011/01/project-denver-processor-to-usher-in-new-era-of-computing/](http://blogs.nvidia.com/2011/01/project-denver-processor-to-usher-in-new-era-of-computing/). Some paragraphs which are relevant to GPU ray tracing/path tracing:"As you may have seen, NVIDIA announced today that it is developing high-performance ARM-based CPUs designed to power future products ranging from personal computers to servers and supercomputers.

Known under the internal codename “Project Denver,” this initiative features an NVIDIA CPU running the ARM instruction set, which will be fully integrated on the same chip as the NVIDIA GPU. This initiative is extremely important for NVIDIA and the computing industry for several reasons.

NVIDIA’s project Denver will usher in a new era for computing by extending the performance range of the ARM instruction-set architecture, enabling the ARM architecture to cover a larger portion of the computing space. Coupled with an NVIDIA GPU, it will provide the heterogeneous computing platform of the future by combining a standard architecture with awesome performance and energy efficiency."

"An ARM processor coupled with an NVIDIA GPU represents the computing platform of the future. A high-performance CPU with a standard instruction set will run the serial parts of applications and provide compatibility while a highly-parallel, highly-efficient GPU will run the parallel portions of programs."

I wonder what Intel's and AMD's answer will be. High-end versions of Fusion and Sandy Bridge/LRB/Knight's Ferry? Either way, it's clear that all of "the big 3" are now pursuing CPU/GPU hybrid chips. Bidirectional path tracing, Markov chain Monte Carlo rendering methods (such as Metropolis light transport and ERPT) and photon mapping will benefit enormously in performance on these hybrid architectures because, being partially sequential, these algorithms are par excellence an ideal match for these hybrid chips (but with clever parallellization tricks they can already run fast on current GPUs, see

[MLT on GPU](http://raytracey.blogspot.com/2010/12/real-time-metropolis-light-transport-on.html)and

[photon mapping on GPU](http://raytracey.blogspot.com/2010/12/gpu-accelerated-biased-and-unbiased.html)). Very complex procedural shaders will run much faster and superfast acceleration structure rebuilding (which is inherently sequential but can be parallellized to a great extent) will allow real-time ray tracing of thousands and even millions (see HLBVH paper by Pantaleoni and Luebke) of dynamic objects simultaneously. GPU and CPU will share the same memory pool, so no more slow PCIe transfers needed. Project Denver is in essence exactly what Neoptica (a think tank group of top graphics engineers acquired by Intel in 2007) had in mind (

[http://pharr.org/matt/talks/graphicshardware.pdf](http://pharr.org/matt/talks/graphicshardware.pdf)). The irony is that Neoptica's vision was intended for Larrabee, but now it's Nvidia that will make it real with the Denver project.

With Nvidia soon producing its own CPUs, competition will become fierce. From now on, Nvidia is not just a GPU company anymore, but is targetting the same PC crowd as Intel and AMD. The concepts of "GPU" and "CPU" will slowly vanish in favor of hybrid architectures, like LRB, Fusion and future Nvidia products (Keppler/Maxwell???). And there is also Imagination Technologies which will incorporate hardware accelerated ray tracing in PowerVR GPUs. Exciting times ahead! :-)

## No comments:

Post a Comment