---
title: 'My toy renderer: Overview'
url: http://momentsingraphics.de/ToyRendererOverview.html
published: '2021-06-24'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# My toy renderer: Overview

**Update 2022-06-01:** Added the post on animations.

Alongside my [latest](http://momentsingraphics.de/Siggraph2021.html) [papers](http://momentsingraphics.de/HPG2021.html) I released the underlying renderer as open source. It is a real-time deferred renderer with ray traced shadows based on [Vulkan](https://www.vulkan.org/) and written in C. As I wrote it, I had the liberty to try some unconventional designs and techniques. So I did, because that is an excellent way to learn new things. It also became the basis for our work on [vertex-blend attribute compression](http://momentsingraphics.de/I3D2022.html).

Most of these things worked out nicely. I'm writing this blog post series in hopes that others may learn from it as well. And maybe some others want to toy with this code base. Here is an overview of all posts in the series:

[Part 1: Keep it simple](http://momentsingraphics.de/ToyRenderer1KeepItSimple.html)- This post laments long compile times, explains why I chose C over other programming languages, some fundamental design choices and how the renderer interacts with Vulkan.
[Part 2: Scene management](http://momentsingraphics.de/ToyRenderer2SceneManagement.html)- Here I explain how I get scenes from Blender onto the GPU while keeping load times short.
[Part 3: Rendering basics](http://momentsingraphics.de/ToyRenderer3RenderingBasics.html)- The renderer uses a visibility buffer
[[Burns2013]](http://momentsingraphics.de#_Burns2013), the Frostbite BRDF for all surfaces[[Lagarde2015]](http://momentsingraphics.de#_Lagarde2015), Monte Carlo integration with stratified random numbers[[Ahmed2020]](http://momentsingraphics.de#_Ahmed2020)and linearly transformed cosines[[Heitz2016]](http://momentsingraphics.de#_Heitz2016). This post motivates these choices and highlights some interesting aspects of my implementation. [Part 4: Ray tracing](http://momentsingraphics.de/ToyRenderer4RayTracing.html)- Ultimately, the purpose of this whole project is to demonstrate importance sampling strategies for polygonal and linear lights. This post describes these techniques and alternative approaches.
[Part 5: Animations](http://momentsingraphics.de/ToyRenderer5Animations.html)- More recently, I repurposed the renderer to compare different techniques for
[compression of vertex-blend attributes](http://momentsingraphics.de/I3D2022.html). This post explains how I support animations in the model file format and use them in the renderer.

The series is not supposed to be a complete documentation of the renderer but it should make it easier to familiarize yourself with the code base. The code has plenty of comments and I did my best to keep it as clear as possible, especially for those familiar with Vulkan and GLSL. It also has very few dependencies, making it easy to compile and to play with it. If you do, you can get some neat renderings such as [Figure 1](http://momentsingraphics.de#Attic2SPP).

![Attic2SPP](../../assets/7ec05b6938738748.webp)

**Figure 1:**An

[attic from BlendSwap (CC-BY)](https://www.blendswap.com/blend/25057)rendered with ray traced shadows at two samples per pixel using my

[importance sampling for polygonal lights](http://momentsingraphics.de/Siggraph2021.html). This frame renders in 1.5 ms on an RTX 2080 Ti at 1440².

## Downloads

[Source code on Github (one branch per paper)](https://github.com/MomentsInGraphics/vulkan_renderer)[Renderer source code with polygonal lights](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-code_and_data.zip)[Renderer source code with linear lights](http://momentsingraphics.de/Media/HPG2021/peters2021-brdf_importance_sampling_for_linear_lights-code_and_data.zip)[Additional scenes (bistro)](http://momentsingraphics.de/Media/Siggraph2021/peters2021-brdf_importance_sampling_for_polygonal_lights-bistro.zip)[Renderer with animations](http://momentsingraphics.de/Media/I3D2022/peters2022_permutation_coding_supplemental.zip)

## References

[ Ahmed, Abdalla G. M. and Wonka, Peter (2020). Screen-Space Blue-Noise Diffusion of Monte Carlo Sampling Error via Hierarchical Ordering of Pixels. ACM Transactions on Graphics (proc. SIGGRAPH Asia), 39(6). ][Official version](https://doi.org/10.1145/3414685.3417881) | [Author's version](http://abdallagafar.com/publications/zsampler/)

[ Burns, Christopher A. and Hunt, Warren A. (2013). The Visibility Buffer: A Cache-Friendly Approach to Deferred Shading. Journal of Computer Graphics Techniques, 2(2):55-69.
][Official version](http://jcgt.org/published/0002/02/04/)

[ Heitz, Eric and Dupuy, Jonathan and Hill, Stephen and Neubelt, David (2016). Real-time Polygonal-light Shading with Linearly Transformed Cosines. ACM Transactions on Graphics (proc. SIGGRAPH), 35(4). ][Official version](https://doi.org/10.1145/2897824.2925895) | [Author's version](https://eheitzresearch.wordpress.com/415-2/)

[ Lagarde, Sébastian and de Rousiers, Charles (2015). Physically Based Shading in Theory and Practice: Moving Frostbite to PBR. ACM SIGGRAPH 2014 Courses, article 23.
][Author's version](https://seblagarde.files.wordpress.com/2015/07/course_notes_moving_frostbite_to_pbr_v32.pdf)