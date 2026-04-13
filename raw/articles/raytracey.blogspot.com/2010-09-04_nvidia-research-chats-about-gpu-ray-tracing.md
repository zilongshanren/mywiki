---
title: Nvidia research chats about GPU ray tracing
url: http://raytracey.blogspot.com/2010/09/nvidia-research-chats-about-gpu-ray.html
author: Sam Lapere
published: '2010-09-04'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://blogs.nvidia.com/ntersect/2010/08/gpu-technology-coference-live-chat-with-bill-dally-and-david-luebke.html](http://blogs.nvidia.com/ntersect/2010/08/gpu-technology-coference-live-chat-with-bill-dally-and-david-luebke.html)). Below are some of the questions and answers related to GPU ray tracing and rendering:

Are there any plans to add fixed function raytracing hardware to the GPU?

David Luebke:

Fixed-function ray tracing hardware: our group has definitely done research in this area to explore the "speed of light", but my sense at this time is that we would rather spend those transistors on improvements that benefit other irregular algorithms as well.

ray-triangle intersection maps well to the GPU already, it's basically a lot of dot products and cross products. ray traversal through an acceleration structure is an interesting proxy for lots of irregular parallel computing workloads : there is abundant parallelism but it is branchy and hard to predict. Steps like Fermi's cache and unified memory space are great examples of generic hardware improvements that benefit GPU ray tracing as well as many other workloads (data mining, tree traversal, collision detection, etc)

When do you think real-time ray tracing of dynamic geometry will become practical for being used in games?

David Luebke:ray tracing in games: I think Jacopo Pantaleoni's "HLBVH" paper at High Performance Graphics this year will be looked back on as a watershed for ray tracing of dynamic content. He can sort 1M utterly dynamic triangles into a quality acceleration structure at real-time rates, and we think there's more headroom for improvement. So to answer your question, with techniques like these and continued advances in GPU ray traversal, I would expect heavy ray tracing of dynamic content to be possible in a generation or two.

Currently there is a huge interest in high quality raytracing on the GPU. The number of GPGPU renderers has exploded during the last year. At the same time there are critics saying that GPU rendering is still not mature enough to be used in serious work citing a number of limitations such as not enough memory, shaders are too simple and that you can only do brute force path tracing on the GPU, which is very inefficient compared to the algorithms used in CPU renderers. What is your take on this? Do you think that these limitations are going to be solved by future hardware or software improvements and how soon can we expect them?

David Luebke:re offline renderers - I do think that GPU performance advantages are becoming too great for studios to ignore. You can definitely get way past simple path tracing. I know of a whole bunch of studios that are doing very deep dives. Stay tuned!

Do you think rasterization is still going to be used in 10 years?

David Luebke:re rasterization: yes, forward rasterization is a very energy-efficient way to solve single-center-of-projection problems (like pinhole cameras and point light shadow maps) which continue to be important problems and subproblems in rendering. So I think these will stick around for at least another 10 years

There have been a lot of papers about reyes style micropolygon rasterizing at past graphics conferences with the feasibility of hardware implementation. Do you think this is a good idea?

David Luebke:re: micropolygons - I think all the work on upolys is incredibly interesting. I still have some reservations about whether upolys are REALLY the final answer to rendering in the future. They have many attractive attributes, like the fact that samples are glued to parametric space and thus have good temporal coherence, but they seem kind of ... heavyweight to me. There may be simpler approaches.

am I wrong in thinking that game graphics are limited more by the artist than the graphics or are the game companies just trying to reach a broader market?

David Luebke:you are not wrong! game developers are limited by artists, absolutely. But this translates to graphics - better graphics means simpler, more robust, easier to control and direct graphics. A good example is cascaded shadow maps, used very widely in games today. These are notoriously finicky and artists have to keep a lot of constraints in their head when designing levels etc. Looking forward, increased GPU performance and programmability both combine to make simpler approaches - like ray tracing - practical. On the flip side, graphics is certainly not solved and there are many effects that we can't do at all in real-time today, so you will continue to see games push forward on graphics innovation, new algorithms, new ways to use the hardware

UPDATE:


[Some tech websites such as xbitlabs, have taken the comment from the live chat about rasterization out of context](http://www.xbitlabs.com/news/video/display/20100903130512_Rasterization_Method_of_Rendering_Will_Live_On_for_Another_Decade_Nvidia.html), stating that we will have to wait at least another 10 years before ray tracing will be used in games. Apparently, they didn't read the answers from David Luebke very well. The way I understood it, is that rasterization will be used in conjunction with ray tracing techniques, both integrated in novel rendering algorithms such as image space photon mapping. From the ISPM paper:Image Space Photon Mapping (ISPM) rasterizes a light-space bounce map of emitted photons surviving initial-bounce Russian roulette sampling on a GPU. It then traces photons conventionallyon the CPU. Traditional photon mapping estimates final radiance by gathering photons from a k-d tree. ISPM instead scatters indirect illumination by rasterizing an array of photon volumes. Each volume bounds a filter kernel based on the a priori probability density of each photon path. These two steps exploit the fact that initial path segments from point lights and final ones into a pinhole camera each have a common center of projection.

So ray tracing in games will definitely show up well within 10 years and according to Luebke you can expect "heavy ray tracing of dynamic content to be possible in a generation or two". Considering that Fermi was a little bit behind schedule, I would expect Nvidia's next generation GPU to come around March 2011 (on schedule), and the generation after that around September 2012. So only 2 years before real-time raytracing is feasible in games ;-D.



## No comments:

Post a Comment