---
title: 'John Carmack: "Eventually ray tracing will win"'
url: http://raytracey.blogspot.com/2011/08/john-carmack-eventually-ray-tracing.html
author: Sam Lapere
published: '2011-08-13'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Aaah, delightful August... Holiday, warm, sunny, relaxing, enjoying mountains and beaches alternated with reports from QuakeCon, Siggraph and High Performance Graphics :-)

John Carmack has said some interesting things about ray tracing during the Q&A following his QuakeCon keynote this year (which was mostly about the practical problems of working with MegaTextures in a production environment). I made a transcript of the relevant Q&A portion which can be seen in its entirety on youtube:

[http://www.youtube.com/watch?v=00Q9-ftiPVQ#t=18m30s](http://www.youtube.com/watch?v=00Q9-ftiPVQ#t=18m30s)"I expect, as we look at next-gen console and broad enough adoption of PC stuff, that there will be some novelty games that are all raytraced or all voxeled on there. But when you look at the top end triple A titles, I do not expect that transition happening in that timeframe but I keep looking at it.

There’s a lot of these things that we look at every five years on and on and eventually… you know I do think that some form of raytracing, of forward tracing or reversed tracing rather than forward rendering will eventually win because there’s so many things that just get magically better there. There’s so much crap that we deal with in rasterisation with, okay let’s depth fade or fake our atmospheric stuff using environment maps, use shadows. And when you just say “well just trace a ray” a lot of these problems vanish. But one interesting thing that people say “look real-time raytracing on current hardware”, that’s what I did in OpenCL recently and I did some interesting work with that. But the real truth is, you don’t just trace one ray it goes sixty frames per second.

To do the things that people want to see out of ray tracing, you’re gonna need to trace a dozen rays on there if you want your soft reflections or even sharp reflections if you got bump mapping on there and not to look like a mess of noise on there, you start needing an order of magnitude more rays than that. And most people still avert their gaze from the whole problem of dynamic geometry. There’s some interesting work that goes on with very rapid GPU assisted KD tree construction that’s starting to look at some of that, but it’s still a long ways off. It’s always the problem of fighting against an entrenched incumbent where we’re doing polygon… Vertex fragment polygon based rasterizers are so far and away the most successful parallel computing architecture ever it’s not even funny. I mean all the research projects and everything else just haven’t added up to one fraction of the value that we get out of that. And there’s a lot of work, lots of smart people, lots of effort and lots of great results coming out of it.Eventually ray tracing will win, but it’s not clear exactly when it’s gonna be."

There is also a brand new video and interview with Carmack on PCPer where he's rambeling about voxels, ray tracing and Larrabee, Fusion, GPUs with ARM cores (Project Denver/Maxwell):

From the article:

"On the topic of ray tracing, a frequently debated issue on PC Perspective, Carmack does admit to finding its uses quite surprising and has spent some time building ray tracing engines for development testing. He seemed surprised by the results in his initial attempt to replace rasterization with a ray tracing engine, getting as much as60 FPS at 720p resolutions on a Fermi-based NVIDIA graphics card.When performance dropped below the targeted frame rate he was able to either produce an image of a lower resolution and display that or use previous frames to sort of “blend” them for a smoother image. The issue though is the delta between a tech demo and fully implemented gaming engine – demos deal with static models, there is no character animation, etc. And while the fact that it runs at 60 FPS at 720p sounds impressive, if you were drawing that with a traditional rasterization engine it would be running at 1000 FPS!"

A transcript of the PCPer interview with Carmack (with some in-depth thoughts about ray tracing) can be found here:

[http://www.pcper.com/reviews/Editorial/John-Carmack-Interview-GPU-Race-Intel-Graphics-Ray-Tracing-Voxels-and-more/Intervi](http://www.pcper.com/reviews/Editorial/John-Carmack-Interview-GPU-Race-Intel-Graphics-Ray-Tracing-Voxels-and-more/Intervi)There's also new interesting research material from HPG, mainly about ray tracing: active thread compaction for GPU path tracing (Wald) (performance boost is much less than initially thought), improving SIMD efficiency for GPU Monte Carlo rendering with stream compaction (van Antwerpen), 10x faster HLBVH (Garanzha), raytraced moblur (Grünschloss), VoxelPipe (Pantaleoni), CUDA rasterization (Laine):

- Posters:

## No comments:

Post a Comment