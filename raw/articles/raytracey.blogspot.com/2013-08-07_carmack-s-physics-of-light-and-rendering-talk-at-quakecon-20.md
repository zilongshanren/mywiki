---
title: Carmack's "Physics of Light and Rendering" talk at QuakeCon 2013 (with Brigade
  cameo!)
url: http://raytracey.blogspot.com/2013/08/carmacks-physics-of-light-and-rendering.html
author: Sam Lapere
published: '2013-08-07'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

For the first time at QuakeCon, John Carmack showed off his talents as a lecturer as he gave a one hour talk on the Physics of Light and Rendering, which covered everything from rasterization to ray tracing and also path tracing. As the pioneer and godfather of 3D first person shooter games and the creator of the most popular 3D game engine of all time (the Quake 3 engine which is still being used in heavily modified form in all of the Call of Duty games) Carmack is still regarded as the highest authority on real-time game graphics, which makes this lecture on physically based rendering (a rendering method which until recently was strictly reserved for the academic research community and for offline production rendering) both surprising and remarkable. And when he divulges his view on the future of game graphics, you can be sure his ideas will be copied by every other game developer.

Some interesting tidbits:

- while Carmack believed that voxels were the way forward to do efficient ray tracing in the past (see

[Jon Olick's SVO research](http://www.youtube.com/watch?v=VpEpAFGplnI)for id Software at Siggraph 2008), but today he thinks ray tracing triangles is the most efficient way and all ray tracing will be against triangles, because most content creation tools are built around triangle meshes
- Carmack thinks that path tracing will be the way forward for all kinds of rendering, offline and real-time and the whole industry is moving towards it, because it's easier and much more accurate to create immersive lifelike graphics for movies and games with accurate global illumination, shadows and reflections

- Brigade gets briefly mentioned at around 1:04:00. Did a quick transcript of the Brigade fragment:

"[...] It does seem likely that the path forward is lots and lots of rays, physically accurate material definitions and approaches that are approximations of the sampling of path tracing. We can do, there are some neat demos going around today, like the Brigade path tracing demo which is real-time and it's doing simple path tracing from a parallel outdoor light and it's noisy and fizzly as it comes in, but you can stop and watch it come in more crisply. And eventually this is going to be the way things go, this is going to be the way we're gonna be rendering, but we still have maybe a couple of magnitudes before it's really competitive. I think one more order of magnitude in performance and you'll start seeing it used for some real things, but still, you have to have a good reason to step away from rasterization. But probably when we get two orders of magnitude, then you start seeing it as one of the more general tools. And the reason that it's winning in the offline world, even though it's still slower, people still care about how long their renderings take even if you're making a feature film or tv commercial, it matters for your iteration time. But the sense is that you get more out of this being understandable. [...]"

- Carmack is pushing the artists at id Software to adopt a more physically accurate material rendering system

While I don't fully agree that we need another magnitude of performance (Brigade can path trace outdoor scenes in real-time today with very little noise), it is great to see that path tracing is acknowledged by Carmack as the eventual future not only for offline rendering, but also for real-time game graphics. The future of GPU path tracers like Octane/Brigade has never been brighter.

## 18 comments:

Ray trace circuitry should solve this, not? By the way how does image quality behave when you compare Brigade with Octane? Would it be necessary for far future generation chips to

brute-force execute Octane as real time graphics or is Brigade just sufficient for photorealism?

How would this compare? because graphics is not the only cool thing to be calculated in a game.

And, have you already tried Brigade with Oculus Rift? :)

@Sam Lapere






Hi Sam, Carmacks talk was great, however, I was wondering when he'd had a look at brigade? do you guys know if he's managed to see the latest version?

@colocolo:

octane is a far more advanced path tracer, among things its spectral, ie it calculates the light response via its component frequencies rather than just a red, green, blue so for example octane can render a prism splitting a beam of white light into a rainbow of colours, whilst brigade probably cant (Sam am I wrong here)

@Sam Lapere:

Any chance we might get a really simple demo of brigade at some point? I mean just a fixed example scene to walk around in... would make for a great benchmark for GPUs

You say this "While I don't fully agree that we need another magnitude of performance (Brigade can path trace outdoor scenes in real-time today with very little noise)"


Can you show a video or something of this?

I find that there are quite a bit of noise whenever you have moving/changing lights in your previous videos.

I think the visible noise is more an artefact of the video compression (which temporally has a hard time letting go of it). As I understand it, when actually rendered to screen, it is quite a bit less noisy.


Sam, would it be possible to show a non-converged frame of a light/dark scene at some point to get a feel for the level of noise?

I don't think that Carmack has a very deep understanding of path tracing. He didn't even get the concept of biased vs unbiased right. Don't get me wrong. It's awesome that path tracing seems to trickle down to the mainstream computer graphics crowd to such an extent that even an authority like Carmack talks about it. But I don't really give a fuck about his predictions :)

colocolo: "Ray trace circuitry should solve this, not?"






Fixed function ray tracing hardware can help for acc structure building, ray traversal and intersection, but makes little sense for shading. So if you use lots of complex materials and your scene is shading bound, you still needs tons of flexible GPGPU compute cores.

"By the way how does image quality behave when you compare Brigade with Octane? Would it be necessary for far future generation chips to

brute-force execute Octane as real time graphics or is Brigade just sufficient for photorealism?"

Brigade compares very favourably to Octane in scenes with simple materials. During the past few months we have been working a lot on matching the quality of the lighting and materials of Octane and we have achieved the exact same output for lighting already. Matching Octane's materials is next. Octane's material system will always be a lot more powerful and flexible and Octane has lots of production grade features that Brigade just doesn't need, but having the exact same output in "easy" scenes offers a lot of possibilities.

"have you already tried Brigade with Oculus Rift? :) "

Yes, we have. The Rift is definitely an interesting technology and it can add an extra level of immersion if you don't care about the pixelated image.

Lensman:









Carmack hasn't seen our latest version of brigade yet. We'd be glad to give him a peek though :)

Brigade would indeed make for an amazing GPGPU benchmark, let's see what we can do there ;)

Anonymous:

send me an email

Sean:

just email me for a screenshot. Static screenshots will never do the real thing justice though: what we've discovered is that if the framerate is high enough, the way the brain perceives the image can greatly help in reducing the noise by blending several frames together. The path tracing noise at 30 fps is actually quite visually pleasing to look at.

mr hankey: "I don't think that Carmack has a very deep understanding of path tracing. He didn't even get the concept of biased vs unbiased right. Don't get me wrong. It's awesome that path tracing seems to trickle down to the mainstream computer graphics crowd to such an extent that even an authority like Carmack talks about it. But I don't really give a fuck about his predictions :)"

Your opinion about Carmack is not really relevant I guess, but I agree with you that there seems to be a massive interest from the entire offline rendering and game industry into physically based rendering and ray tracing, and Carmack's predictions have mostly turned out to be true (even though the sparse voxel octree ray tracing stuff has proven to be not very practical in real game scenarios for now). And Carmack's word is still gospel to many game developers, so you'll see his ideas popping up soon in several engines.

Hey Sam, I was wondering how brigade scales with the display resolution.

Does 4 times the resolution mean 4 times compute power or does it scale worse?

Kevin.is.an.astronaut: Brigade scales better when you render at higher resolutions due to having more coherency between pixels, e.g. 4x the resolution requires about 3-3.5x the compute power. Another nice benefit of rendering at high resolutions is that noise is much less noticeable at higher res. Because of that (and recent speed increases), I'm often running Brigade at 1080p and rarely go below 720p.

Perhaps you have seen the Nvidia lightfield HMD prototype on youtube.

What about side by side 3D or in that case lightfield tile rendering images. Do you have a clue how Brigade would behave in that case performancewise?

As i have heard lightfield rendering(or 'holographic imagery') would be more natural than normal 3D and therefore the ultimate image technique.

colocolo: rendering all the tiles would be as fast as rendering a normal image with the same number of pixels as in all the tiles together, probably faster because there's more coherency.

@Sam Lapere: Well I will have to disagree with you on the part about Carmack. It is indeed relevant to the credibility of his predictions that Carmack is very obviously no expert in monte carlo rendering methods.

@Sam Lapere: It would be interesting to combine Brigade with an eye-tracker and foveated rendering (i.e. concentrating the sampling around the gaze point), the performance savings could be enourmous.


There has been expirements done with foveated rendering with traditional rasterization, and test subjects were unable to tell the difference in quality between the foveated image and the normal one (due to the eye being less sensitive in the peripheral vision).

he has really no clue what he is talking about...

"he has really no clue what he is talking about..."


In Carmack's defense, he is coming from the real-time rasterization world, which thrives on nothing but hacks for shadows, reflections, GI, AO, ... everything. The physically based rendering paradigm shift that the whole industry is moving to is relatively new, and you can't expect anyone to become a PBRT expert in a matter of months, not even Carmack who has his hands full with 3 full-time jobs at id, OculusVR and Armidillo Aerospace.

Hey Sam,



Some questions came up in my mind recently.

I was wondering from what would brigade benefit the most from on the graphics hardware side. By that I mean: Single Precision FLOPS, Double Precision FLOPS, Memory Bandwith and so on. Does brigade use Double Precision at all? The question came to me when seeing a graphics cards comparison. The GTX Titan has around 1300 TFLOPS ind DP, while the GTX 780 only has 166.

Also I was wondering how many people are currently working on the engine code. (I know that size doesn't say much about the quality but I am just curious).

@Kevin.is.an.astronaut: agreed about DP. Therefore, price of GTX Titan isn't bad. :)

I find it funny that some of the previous posters seem to think that Carmack doesnt really have a deep understanding of path tracing. I disagree, I wouldnt be suprised if he knew a lot more about it then he had time to let on in this talk. Ultimately I think everything he said is correct. Unbiased vs biased path tracing is for example exactly that a tradeoff between physically correct and what looks ok but is faster.





I personally am very glad that path tracing is something that Carmack sees as something within 10x-100x of our current performance away from us.

Whilst brigade is very cool and incredibly fast, it isnt quite there yet, you cant for example create a triple A title like Crysis 3 with it yet on consumer grade hardware, the performance just isnt there.

I highly regard Mr Carmack's opinion on 'real' world graphics technology and its applicability.

I cant wait to see Brigade 3! Sam you big tease, mentioning it to use but not showing us anything!!! :) :) :)

Post a Comment