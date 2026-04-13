---
title: Path tracing workshop
url: http://momentsingraphics.de/PathTracingWorkshop.html
published: '2024-11-05'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Path tracing workshop

**Update 2024-11-05:** Fixed video links.
**Update 2024-12-17:** Link to the path tracing lecture.

Now that GPUs have ray tracing units, real-time path tracing is coming into reach. Applications beyond movie rendering and baking embrace it, and therefore more people need to know about it. At [Intel](https://www.intel.com/content/www/us/en/developer/topic-technology/graphics-research/overview.html), I recently offered a path tracing workshop to educate a broad audience of engineers on basics of the topic. I am happy to announce that we decided to make this workshop publicly available. If you know a few math and programming basics, you can watch 76 minutes of videos and solve some [exercises on ShaderToy](https://www.shadertoy.com/playlist/NfjSRy) as you go. In the end, you will have written your own ray tracer and a path tracer on top of it! I simplified things as much as possible, but you will really write all key aspects of the path tracer and understand why they work.

## Part 1: Ray tracing

Part 1 is about bare bones ray tracing. You learn how to use GLSL and ShaderToy. As first proper exercise, you have to compute camera rays for a virtual camera. Then you implement ray-triangle and ray-mesh intersection tests and you have got a ray tracer. It is slow, because it does not use acceleration structures but it works correctly and can render scenes without any shading as shown in [Figure 1](http://momentsingraphics.de#TeaserRayTracing).

![TeaserRayTracing](../../assets/3ec8bc3e64237d17.png)

**Figure 1:**The end result in part 1 of the workshop is a ray traced Cornell box without shading.

## Part 2: Path tracing

Part 2 is about basic path tracing. This part has a bit more theory because you need to understand concepts like radiance, the rendering equation and Monte Carlo integration. Then you learn how to generate random direction vectors in a hemisphere and use them to compute direct illumination using Monte Carlo integration. Finally, you implement path tracing and get the image in [Figure 2](http://momentsingraphics.de#TeaserPathTracing) (if you ramp up the sample count enough).

![TeaserPathTracing](../../assets/3d47ea308ec4f429.png)

**Figure 2:**The end result in part 2 of the workshop is a Cornell box with full global illumination rendered using path tracing.

## Part 3: Importance sampling?

Parts 1 and 2 take the path of least resistance to arrive at a path tracer that functions correctly. The drawback of its simple design is that it converges rather slowly. Importance sampling strategies are an excellent way to make it faster. I already wrote [a blog post](http://momentsingraphics.de/ToyRenderer4RayTracing.html) or [two](http://momentsingraphics.de/SphericalCapMIS.html) and [a](http://momentsingraphics.de/I3D2019.html) [few](http://momentsingraphics.de/HPG2021.html) [papers](http://momentsingraphics.de/Siggraph2021.html) on this subject. If things go well, there will be a part 3 covering light sampling, BRDF importance sampling and multiple importance sampling. Stay tuned!

**Update:** Part 2 of my [path tracing lectures](http://momentsingraphics.de/PathTracingLectures.html) covers the contents that I had in mind for part 3 of this workshop. The format is slightly different (no Shadertoy exercises) but if you were looking forward to part 3, you should definitely check out these lectures.

## Links

[Part 1, ray tracing (video)](https://players.brightcove.net/740838651001/default_default/index.html?videoId=6317347725112)[Part 2, path tracing (video)](https://players.brightcove.net/740838651001/default_default/index.html?videoId=6317347017112)[ShaderToys without solutions](https://www.shadertoy.com/playlist/NfjSRy)[ShaderToys with solutions](https://www.shadertoy.com/playlist/f3SSzt)[PDF slides, part 1](https://www.intel.com/content/www/us/en/content-details/763947/path-tracing-workshop-part-1-ray-tracing.html)[PDF slides, part 2](https://www.intel.com/content/www/us/en/content-details/763948/path-tracing-workshop-part-2-path-tracing.html)[Intel page, part 1 (video player broken)](https://www.intel.com/content/www/us/en/developer/videos/path-tracing-workshop-part-1.html)[Intel page, part 2 (video player broken)](https://www.intel.com/content/www/us/en/developer/videos/path-tracing-workshop-part-2.html)

**Update:** I noticed that the embedded video players on the Intel webpages for this workshop are no longer functional. Since the videos are still online on the underlying video platform, I am now linking them directly. If you also notice issues with these links, please let me know by email and I will see what I can do about it.