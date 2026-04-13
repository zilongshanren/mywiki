---
title: 'Real-time photorealistic rendering: Sponza with glossy toad in HD (720p)'
url: http://raytracey.blogspot.com/2012/06/real-time-photorealsitic-rendering.html
author: Sam Lapere
published: '2012-06-01'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Recommended to watch in 720p:

Today, I've also stumbled upon a interesting paper entitled

["Toward Evaluating Progressive Rendering Methods in Appearance Design Tasks"](http://www.cs.dartmouth.edu/cms_file/SYS_techReport/575/TR2012-715.pdf)by Ou, Karlik, Krivanek and Pellacini. The authors tested 4 progressive rendering methods (random path tracing, quasirandom path tracing, progressive photon mapping and virtual point lights rendering) and investigated how people subjectively perceive and enjoy the progressive updating of the image."Progressive rendering is becoming a popular alternative to precomputation approaches for appearance design tasks. Images created by different progressive algorithms exhibit various kinds of visual artifacts at the early stages of computation. We present a user study that investigates the effects of these artifacts on user performance in appearance design tasks. Speciﬁcally, we ask both novice and expert subjects to perform lighting and material editing tasks with the following algorithms: random path tracing, quasi-random path tracing, progressive photon mapping, and virtual point light (VPL) rendering. Data collected from the experiments suggest thatThere is no indication that quasi-random path tracing is systematically preferred to random path tracing or vice-versa; the same holds between progressive photon mapping and VPL rendering. Interestingly, we did not observe any signiﬁcant difference in user workﬂow for the different algorithms. As can be expected, experts are faster and more accurate than novices, but surprisingly both groups have similar subjective preferences and workﬂow."path tracing is strongly preferred to progressive photon mapping and VPL rendering by both experts and novices.

During the first frame updates, progressive photon mapping exhibits low frequency noise in the form of ugly splotches, while VPL rendering suffers from banding artefacts. The noise produced by path tracing on the other hand is much more easy on the eyes showing that the human visual system is more forgiving for Monte Carlo noise.

## 23 comments:

Couldn't resist posting a comment. Your very last sentence is the most biased thing in this post, and makes completely misleading conclusions. You need to think again how much the bias, which you hate so much for some reason, actually contributes to the visual characteristics of the compared algorithms. The fact that the scenes in the comparison cannot show the strengths of the different algorithms is another topic.

Hi Ilyan, to be clear I don't hate bias at all. What I care about is not how an image is rendered, but how photoreal it looks and how fast it achieves that realism. All the work I've done during the past year and a half is about creating photorealistic images in real-time, and it's easier and faster to do that with unbiased rendering. If it could be done with biased algorithms, I wouldn't hesitate to use that instead. I've looked at GPU photon mapping (a good example is Kaikai Wang's research: http://kaikaiwang.blogspot.be/2010/11/actual-indoor-scene-normal-map-more.html) and I've tried GPU based progressive photon mapping in SmallLuxGPU and Hachisuka's demo, but I found that it doesn't render the first frames as nicely as path tracing. With path tracing, you immediately get a good estimate of the final image from the very first frames, which is not the case for VPL or PPM as they both have too much initial bias. Since Brigade has to render realistic pictures in the least amount of time, using GPU path tracing is the only practical option. There also exist image reconstruction and a-trous filtering techniques which take a path traced image with only 1 sample per pixel and produce a smoothed (but biased) image which looks plausible. I don't think that's possible with VPLs after one iteration.

@Sam


get a copy of Camtasia Studio it's better than FRAPS for capturing raw AVI.

But the scenes you're showing are all very well suited to unidirectional path tracing - huge light sources, very easy and uniform predominant single-bounce indirect illumination. Try the simplest room with direct illumination focused only in a small spot (e.g. by a desk lamp shining on a desk). The path tracer will have great difficulties in this scene, and VPLs will produce a much better result. Then put some specular object in the scene. PPM will handle this better than PT. Can we then conclude, based on these examples, that PT is not good and PPM and VPLs will replace it?

Why do you optimize for the first few frames only?



That quality is still quite a bit from anything practical.

When we have a nice 50x speedup the first few frames(of frames?) doesn't matter at all.

Probably just misunderstanding your point.

Iliyan: You're right though, I'm mostly using scenes and lighting conditions that converge very fast, but that doesn't make the results less impressive to me. Brigade's target is still game rendering and you can make a completely real looking game with it if you keep the limitations of path tracing in mind and avoid difficult lighting, just like all the scenes in modern games are constructed with the limitations of rasterization in mind (for example games still rarely have mirrors while Duke Nukem 3D had a mirror in the bathroom and it was released in 1996).



As for PPM, I did some tests comparing GPU based PPM to GPU PT and PT wins hands down in the sort of scenes that Brigade is targetting.

Maybe vertex merging will come out as the final winner :)

Indeed it's correct to acknowledge that you consider scenes with simple illumination, which are well suites to unidirectional PT.


But we need to keep in mind that PT has been available for almost 30 years now, and there have been countless examples where the sampling techniques it employs fail. It's therefore too bold to claim that "biased algorithms such as VPL are on their way out and will be replaced by Monte Carlo path tracing". Note also that it's not the bias that's was considered problematic with VPLs in the tech report above - it's the sampling correlation!

Alright, your points have convinced me enough that I've removed the controversial sentence :)


It would be great if you could make a GPU implementation of your vertex merging+BDPT algorithm and release a demo so I can compare its speed with PT.

This is a paper worth looking into:





http://miloshasan.net/VirtualSphericalLights/SIGAsia09VSL.pdf

It outlines "Virtual Spherical Lights" that avoid the loss in fidelity with VPLs (clamped or otherwise) on glossy surfaces whilst maintaining extremely good rendering performance. When compared to a path tracer, the results are also very comparable.

Disclaimer: I'm not taking sides with one implementation over the other, I just thought that this would be of interest!

Here is the paper abstract:

In this paper, we aim to lift the accuracy limitations of manylight algorithms by introducing a new light type, the virtual spherical light (VSL). The illumination contribution of a VSL is computed over a non-zero solid angle, thus eliminating the illumination spikes that virtual point lights used in traditional many-light methods are notorious for. The VSL enables application of many-light approaches in scenes with glossy materials and complex illumination that could previously be rendered only by much slower algorithms. By combining VSLs with the matrix row-column sampling algorithm, we achieve high-quality images in one to four minutes, even in scenes where path tracing or photon mapping take hours to

converge.

Sean, I've read that paper also, I think the VSL technique is still a bit limited in materials compared to what you can do with path tracing (e.g. highly glossy and perfectly specular).

Thanks Sam!


It's probably telling that PT is the baseline that this technique is compared to.

Hey Sam, love what your up to here.


How might I gain access to pre-public-release versions of Brigade (especially openCL based since currently I don't have an Nvidia GPU)?

Rick, there are currently no plans to make the OpenCL version of Brigade available to the public.

Can someone put up a working copy of the brigade2 engine, the one on the website does not work, and I have contacted Jacco Bikker by email and I have not got an answer. Or is it possible that email on his site is not up to date or something like that?

Re "...there are currently no plans to make the OpenCL version of Brigade available to the public"



How sad :(. I guess I read too much into <

http://brigade.roenyroeny.com/?p=tech> , or the deal with OTOY has changed things too much since roeny put the "official" Brigade site up.

Can you say anything in the way of what the "roadmap" is?

This whole brigade thing is starting to look like the "Unlimited Detail" fiasco, different in its own way but the same in the end.

^^ Agreed. The hype does not meet the reality - unfortunately this video demonstrates that. Needs about a 50+ fold increase to be truly realtime for even a moderate game level.



And the cost to render this on a GPU cloud sufficient to make it realtime is prohibitive.

Great leaps, but still too far away to be claiming what's being claimed.

Rick, can't say anything about the roadmap, other than that the cloud will play a major role.

I really like the lighting quality on the sponza shots, really looks good.

The gamma correction was slightly changed which makes the colors much more vibrant. It works great in this scene.

Hi Sam,




Do you use a portal, because it seems that you have a very fast convergence 'into' the sponza. There are some area of the sponza that are only illuminated by indirect light !

Or you have a kind of 'ambient' occlusion term too ?

:-P

The video and shots are rendered with the MIS path tracing kernel. No portals are used, and no AO either. Brigade really is this fast. I've tried using the AO kernel, but it didn't look plausible.

Post a Comment