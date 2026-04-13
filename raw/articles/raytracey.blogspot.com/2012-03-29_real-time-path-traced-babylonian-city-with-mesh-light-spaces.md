---
title: Real-time path traced Babylonian city with mesh light + spaceship test
url: http://raytracey.blogspot.com/2012/03/real-time-path-traced-babylonian-city.html
author: Sam Lapere
published: '2012-03-29'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The first scene demonstrates a moving mesh light flying over the city scene from the previous post. Mesh lights are a notorious source of noise in path tracing, but Brigade handles them pretty nicely (all videos and screenshots rendered with 2 GTX 580 GPUs) :






**850k triangles rendered at 10-30 fps and 1280x720p render resolution**:[http://www.youtube.com/watch?v=8__UhcVRDeI](http://www.youtube.com/watch?v=8__UhcVRDeI)(be sure to watch this at 720p)


__UPDATE: video with sun__


Diffuse:

Glossy:



These tests undeniably show that real-time high-res path tracing of highly detailed and complex scenes is possible today using just one or two GPUs. This is a major breakthrough and very hard to believe, most people were thinking this would be at least 10 years away. To be honest, I have a hard time believing it as well. I'm constantly OMGWTF when loading up a new model and seeing it in all its path traced glory :-)

Stay tuned for my next blogpost, in which I will show a highly detailed modern city.

## 23 comments:

Again, very impressive!

How does the city scene perform with lots of lights like street lanterns?

Thanks. More mesh lights also means more noise, but you can optimize this by limiting the importance of lights according to things like distance and size. Brigade has a clever way to deal with multiple lights, you can see it in action in this video: http://www.youtube.com/watch?v=Qdw1HvzKt1M

Nice! how many triangles on the spaceship?

The spaceship model contains 849,000 triangles. You can always see the amount of triangles in screenshots in the upper left corner (denoted as "primitives")

How does it handle dynamic tesselation with displacement mapping ? I'm also curious about detailed dynamic fur/hair rendering, facial animation, cloth rendering and matrix palette skinning of complex models. What about dense vegetation and trees dynamically responding to the environment like wind or detailed waves near the beach ?

What do you hope to achieve with your animations, do you seriously think anybody will try to use your rendering engine for a game ? I don't want to be disrespectful as the static renderings look nice, but the animations are far from the rendering quality gamers have grown used to on their seven years old console hardware.

You can nearly make a game from that. Like fixed-camera adventure games or slow plateformers.


It is a shame that Kepler is so disappointing, that would mean waiting for a long long time again + the inertia of people updating their hardware.

Have you already thought of using prioritised lighting for managing multi-lighting. Like prioritising computing to do all hits close to the the lights first and far later on following frames ?

Or even prioritising lights by their powers ?

Kepler isn't disappointing its quite good for gaming, it's just the GK104 is not design for GPU Compute, you'll have to wait for the Nvidia conference in May to see GK110 it will be a compute beast

Dynamism is an interesting topic... As far as I know, moving objects in your videos are implemented by re-sending the modified geometry to the GPU. Are there any estimations of how the rendering speed scales with number of dynamic objects/their polycount, CPU speed, bandwidth, etc.? Or is it possible to have parts of BVH with locally defined transformation matrix?

I'm not the expert, but I assume a BVH is invariant under affine transformation, so it should be easy to shoot rays taking into account the object transformation.

The real challenge probably is objects with deforming complex geometry, as then the BVH has to be recalculated for each frame.

Anonymous (6th comment): the main point here is cinema quality global illumination in real-time, which is seriously lacking in games, even in the most recent ones that have real-time GI hacks like Crysis 2 and Battlefield 3. With my experiments, I'm showing that we're actually not that far off from real-time photorealistic lighting. You're free to dislike my videos of course :)





MrPapillon: agreed, this tech would be awesome for a Riven-style adventure/puzzle game. On prioritising lights: Brigade actually does that already in some way, based on distance, visibility etc.

Anonymous (comment 8): despite the lackluster reviews, the GTX 680 might be good for CUDA path tracing after all: http://www.tml.tkk.fi/~timo/HPG2009/index.html and GK110 should be even better. Good times ahead :D

Dima: the BVH is split between static and dynamic geometry, only the dynamic geometry is updated and transferred to the GPU every frame. There is a noticeable impact on performance with higher number of dynamic objects, but better alternatives are underway.

Anonymous (comment 10): deforming geometry is entirely possible, check out this amazing video posted yesterday by one of Brigade's developers: http://www.youtube.com/watch?v=KRnsLmnN1TE

I didn't say I dislike your videos, knowing the way how it is done, it is quite impressive. GI is something very desirable to have, but the basics need to be there in the first place, being impeccable noise free rendering at high resolution and frame rate. The older Arauna CPU ray tracer did not have any noise. So why not start with a noise free rendered image and add subtle GI lighting modulations on top of this ?

Contrary to current game engines, which try to achieve higher graphical fidelity by adding hacks and approximations with rasterization, Brigade uses a top-down approach: it starts from a slow-to-compute but very high quality physically correct image rendered with an elegant and conceptually very simple algorithm (path tracing) and adds optimizations to make it run in real-time with the least possible noise.


Rest assured, the team behind Brigade is working on implementing state-of-the art noise filters which should make these real-time path traced animations completely noise-free. In the mean-time, be prepared to see more noisy/blurry renders :)

Also I would add that Anonymous is comparing old rasterization techs with very young real-time ray tracing ones.

Imagine the same efforts that are currently put on rasterization by the industry rebranched to raytracing.

Look at all new techs in history of mankind and you will see that their initial implementations are most of the time incomplete.

At least Intel has put a lot of effort into real-time ray tracing. If a multi-bilion $ giant can't pull it off, you are certainly very brave to prove them wrong. And ray tracing has been around for a very long time, long before there were GPUs. There have been many hardware ray-tracers around too... Lasting success of new technology depends on economical viability, and GPUs won that. And good for you guys that GPUs did as they have now evolved into cheap flexible powerful compute devices that can be used to tackle many problems, including ray/path tracing. So basically you are trying to beat GPU graphics by using a GPU, isn't that ironically ?

And don't get me wrong, I really like what you try to attempt, as all I like to follow all kinds of creative approaches to better graphics.

All that Intel has shown with their real-time ray tracing demos is Whitted-style ray tracing which is just plain ugly and can not compete with the graphics in modern rasterized games. I never believed in that approach. Ray tracing only gets interesting when you add global illumination with path tracing and the CPU is just bog slow at that.



When GPUs started to overtake CPUs in ray tracing around 2008, it was just a matter of time before GPU path tracers popped up. The best GPU path tracers are now 10 - 20x faster than their CPU counterparts, Brigade is one of them.

While GPUs are now extremely fast at path tracing, dedicated ray tracing hardware on the GPU would be even better. I hope the IHVs will realize this (Imagination Technologies already does).

I'm sure Intel also has been looking into path tracing:

http://software.intel.com/en-us/articles/embree-highly-optimized-visibility-algorithms-for-monte-carlo-ray-tracing/

Check out the video linked at the bottom.

In that video, Embree is demonstrated on a machine with 40 CPU cores to achieve the same rendering speed you have on 1 GPU with a highly optimized GPU renderer like Octane. You can buy 8 high end GPUs for the price of that system.

On Siggraph 2011 I have shown that even for large scenes (not fitting into GTX 480 1.5 gigs memory, I mean Boeing 777) path tracing is 18x faster on GPU than on 6 core i7 with 3.46GHz. 250ms vs 4600ms for 2 bounce path tracing. Why? Because CPU L2-L3 caches are too small compared to GPU main memory (which is considered as cache). And I can say that consumer GPU is much cheaper than a 6 core.


Kirill

Thanks for this info and numbers Kirill. Didn't expect an out-of-core pathtracer like CentiLeo to be actually that fast on the GPU. Very interesting, hope to see more of it soon.

And you will see. Although we are very small team, but work hard. For potential sceptics, it is not a demo for demo, it might be a product, which supports what people want to see in a renderer.

Intel has a 50 core processor in the making, which looks like a good fit for path tracing too:

http://www.eetimes.com/electronics-news/4230654/Intel-unveils-1-TFLOP-s-Knight-s-Corner

Knight's Corner (aka Larrabee done right) most probably will be a beast for path tracing, but it will cost you an arm and a leg.

Post a Comment