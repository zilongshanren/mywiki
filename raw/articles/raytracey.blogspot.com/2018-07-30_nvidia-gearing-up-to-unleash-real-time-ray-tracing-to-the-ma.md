---
title: Nvidia gearing up to unleash real-time ray tracing to the masses
url: http://raytracey.blogspot.com/2018/07/nvidia-gearing-up-to-unleash-real-time.html
author: Sam Lapere
published: '2018-07-30'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

In the last two months, Nvidia roped in several high profile, world class ray tracing experts (with mostly a CPU ray tracing background):


[Matt Pharr](http://pharr.org/matt/blog/2018/05/27/nvidia-bound.html)One of the authors of the Physically Based Rendering books (

[www.pbrt.org](http://www.pbrt.org/), some say it's the bible for Monte Carlo ray tracing). Before joining Nvidia, he was working at Google with Paul Debevec on Daydream VR, light fields and Seurat (

[https://www.blog.google/products/google-ar-vr/experimenting-light-fields/](https://www.blog.google/products/google-ar-vr/experimenting-light-fields/)), none of which took off in a big way for some reason.

Before Google, he worked at Intel on Larrabee, Intel's failed attempt at making a GPGPU for real-time ray tracing and rasterisation which could compete with Nvidia GPUs) and ISPC, a specialised compiler intended to extract maximum parallelism from the new Intel chips with AVX extensions. He described his time at Intel in great detail on his blog:

[http://pharr.org/matt/blog/2018/04/30/ispc-all.html](http://pharr.org/matt/blog/2018/04/30/ispc-all.html)(sounds like an awful company to work for).

Intel also bought Neoptica, Matt's startup, which was supposed to research new and interesting rendering techniques for hybrid CPU/GPU chip architectures like the PS3's Cell


[Ingo Wald](https://ingowald.blog/2018/07/27/joining-nvidia/)Pioneering researcher in the field of real-time ray tracing from the Saarbrücken computer graphics group in Germany, who later moved to Intel and the university of Utah to work on a very high performance CPU based ray tracing frameworks such as Embree (used in Corona Render and Cycles) and Ospray.

His PhD thesis "

[Real-time ray tracing and interactive global illumination](http://www.sci.utah.edu/~wald/PhD/wald_phd.pdf)" from 2004, describes a real-time GI renderer running on a cluster of commodity PCs and hardware accelerated ray tracing (OpenRT) on a custom fixed function ray tracing chip (SaarCOR).

Ingo contributed a lot to the development of high quality ray tracing acceleration structures (built with the surface area heuristic).


[Eric Haines](http://erich.realtimerendering.com/)Main author of the famous

[Real-time Rendering](http://www.realtimerendering.com/blog/)blog, who worked until recently for Autodesk. He also used to maintain the

[Real-time Raytracing Realm](http://www.realtimerendering.com/resources/RTNews/demos/overview.htm)and

[Ray Tracing News](http://www.realtimerendering.com/resources/RTNews/html/)

What connects these people is that they all have a passion for real-time ray tracing running in their blood, so having them all united under one roof is bound to give fireworks.

With these recent hires and initiatives such as





















[RTX](https://developer.nvidia.com/rtx)(Nvidia's ray tracing API), it seems that Nvidia will be pushing real-time ray tracing into the mainstream really soon. I'm really excited to finally see it all come together. I'm pretty sure that ray tracing will very soon be everywhere and its quality and ease-of-use will soon displace rasterisation based technologies (it's also the reason why I started[this blog exactly ten years ago](http://raytracey.blogspot.com/2008/08/ruby-voxels-and-ray-tracing.html)).**Senior Real Time Ray Tracing Engineer****NVIDIA, Santa Clara, CA, US****Job description**
Are you a real-time rendering engineer looking to work on real-time ray tracing to redefine the look of video games and professional graphics applications? Are you a ray tracing expert looking to transform real-time graphics as we lead the convergence with film? Do you feel at home in complex video game codebases built on the latest GPU hardware and GPU software APIs before anybody else gets to try them?

At NVIDIA we are developing the most forward-looking real-time rendering technology combining traditional graphics techniques with real-time ray tracing enabled by NVIDIA's RTX technology. We work at all levels of the stack, from the hardware and driver software, to the engine and application level code. This allows us to take on problems that others can only dream of solving at this point

We are looking for Real Time Rendering Software Engineers who are passionate about pushing the limits of what is possible with the best GPUs and who share our forward-looking vision of real-time rendering using real-time ray tracing.

In this position you will work with some of the world leading real-time ray tracing and rendering experts, developer technology engineers and GPU system software engineers. Your work will impact a number of products being worked on at NVIDIA and outside NVIDIA. These include the NVIDIA Drive Constellation autonomous vehicle simulator, NVIDIA Isaac virtual simulator for robotics, and NVIDIA Holodeck collaborative design virtual environment. Outside NVIDIA our work is laying the foundation for future video games and other rendering applications using real-time ray tracing. The first example of this impact is the NVIDIA GameWorks Ray Tracing denoising modules and much of the technology featured in our NVIDIA RTX demos at GDC 2018.

**What You Will Be Doing**- Implementing new rendering techniques in a game engine using real-time ray tracing with NVIDIA RTX technology
- Improving the performance and quality of techniques you or others developed
- Ensuring that the rendering techniques are robust and work well for the content needs of products using them

**What We Need To See**- Strong knowledge of C++
- BS/MS or higher degree in Computer Science or related field with 5+ years of experience
- Up to date knowledge of real-time rendering and offline rendering algorithms and research
- Experience with ray tracing in real-time or offline
- Knowledge of the GPU Graphics Pipeline and GPU architecture
- Experience with GPU Graphics and Compute programming APIs such as Direct3D 11, Direct3D 12, DirectX Raytracing, Vulkan, OpenGL, CUDA, OpenCL or OptiX
- Experience writing shader code in HLSL or GLSL for these APIS.
- Experience debugging, profiling and optimizing rendering code on GPUs
- Comfortable with a complex game engine codebase, such as Unreal Engine 4, Lumberyard, CryEngine or Unity
- Familiar with the math commonly used in real-time rendering
- Familiar with multi-threaded programming techniques
- Can do attitude, with the will to dive into existing code and do what it takes to accomplish your job
- Ability to work well with others in a team of deeply passionate individuals who respect each other

## No comments:

Post a Comment