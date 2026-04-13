---
title: Path tracing lectures
url: http://momentsingraphics.de/PathTracingLectures.html
published: '2024-12-19'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Path tracing lectures

Earlier this year, I prepared [lectures on path tracing](https://www.tudelft.nl/ewi/over-de-faculteit/afdelingen/intelligent-systems/computer-graphics-and-visualization/education/path-tracing-lecture) for master students at [TU Delft](https://graphics.tudelft.nl/). We decided to make recorded versions of these lectures available to the general public. I also wrote a simple Vulkan [path tracer](https://github.com/MomentsInGraphics/path_tracer) for illustrations in the lectures, which is open source now. You can watch the lectures on YouTube (113 minutes) to learn about basic principles of path tracing and all the importance sampling strategies that go into the path tracer. Then you can dig into the code to see how they are implemented. The first lecture is similar in scope to part 2 of my [path tracing workshop](http://momentsingraphics.de/PathTracingWorkshop.html). It ends with a naive path tracer. Part 2 dives into importance sampling strategies that achieve considerably lower noise at the same computational cost: BRDF importance sampling, light sampling and the combination of these two strategies using multiple importance sampling and next-event estimation. These contents are similar to what I had in mind for part 3 of the path tracing workshop.

Compared to the workshop, the format is a bit different here: There are no Shadertoy exercises but the lectures provide fairly specific guidelines for an implementation and the [lecture website](https://www.tudelft.nl/ewi/over-de-faculteit/afdelingen/intelligent-systems/computer-graphics-and-visualization/education/path-tracing-lecture) has links to the code for each step. If you have a bit of experience with computer graphics or were able to follow my [path tracing workshop](http://momentsingraphics.de/PathTracingWorkshop.html), following these lectures should not be a problem.

The [path tracer](https://github.com/MomentsInGraphics/path_tracer) itself can be thought of as solid baseline but nothing more. It is kept simple and there are many reasonable ways to extend it: Currently, all surfaces must use the [Frostbite BRDF](http://momentsingraphics.de/ToyRenderer3RenderingBasics.html#The_Frostbite_BRDF) and light sources must be spherical. In terms of sampling strategies, [stratification](http://momentsingraphics.de/ToyRenderer3RenderingBasics.html#Stratified_random_numbers_blue_noise_), path guiding or ReSTIR could help to accelerate convergence. And there is no denoiser, only progressive rendering. On the other hand, the implementation is pretty well-optimized and the GLSL code should be quite easy to read and comprehend after watching the lectures. The code base is new but similar in spirit to my [previous toy renderer](http://momentsingraphics.de/ToyRendererOverview.html). It uses C, Vulkan, GLFW and the same [model file format](http://momentsingraphics.de/ToyRenderer2SceneManagement.html). [Nuklear](https://github.com/Immediate-Mode-UI/Nuklear) took the place of [Dear ImGui](https://github.com/ocornut/imgui/). Eventually, I might implement a few more advanced techniques in a branch or write a few blog posts about certain aspects.

## Links

[TU Delft webpage with all lecture materials](https://www.tudelft.nl/ewi/over-de-faculteit/afdelingen/intelligent-systems/computer-graphics-and-visualization/education/path-tracing-lecture)[Path tracer source code (github)](https://github.com/MomentsInGraphics/path_tracer)[Older path tracing workshop with Shadertoy exercises](http://momentsingraphics.de/PathTracingWorkshop.html)

## Images

![Slide](../../assets/a54b78896bda5054.png)

**Figure 1:**A slide from part 2 of the lecture.

![Render](../../assets/c4edbfd49a2da7b5.png)

**Figure 2:**A rendered image from the path tracer.