---
title: Nvidia, DLSS5 and breaking rendering.Are we cooked yet? (no/but...)
url: https://c0de517e.com/028_dlss5.htm
author: Angelo Pesce
published: '2026-04-13'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

**Some history.**
Before delving into wild, ignorant and thus likely incorrect (but hopefully fun) speculations on the technology behind DLSS5 - it's worth taking a minute at a higher level.

People know NV - obviously - as the hardware giant they are. But a lot of their "moat" has always been also on the software side - arguably mastering the two dimensions, HW and SW, better than any of its peers.

CUDA is the obvious example - obvious today, in the era of big-ML driving never-seen-before hardware investments - but it started almost two decades ago, immediately when it was clear the GPUs could do more than graphics (even CuDNN is 10+ years old already!).

I'm old enough to remember the CUDA landing page, with infinite examples of speedup gains from porting CPU code to GPU, and the era of "cheap" papers investigating GPGPU.

A truly fascinating intuition, to be studied in business books.

![Remember the "cudazone" and NV boasting about speedups?](../../assets/0d19dfbb0fe5fd60.png)

Remember the "cudazone" and NV boasting about speedups?
Even before and beyond CUDA though, NV software investments paid dividends. In graphics, primarily through the superiority (and willingness to invest in custom, per-game hacks) of their drivers. But also tools (for a while, Nsight was quite unique and arguably the best) - and to some degree, graphics "middleware": GameWorks.

But none of these components was fundamental. And I doubt that in AAA anyone saw GameWorks as a resource - the pattern was mostly that you'd develop your game, primarily for consoles, and then if you were big enough someone at NV would offer support and more to integrate some NV-only (or best-on-NV) features through GameWorks.

I'd wager that, at least prior to consoles starting to support raytracing, most big RTX ports were also similar. Subsidized, integrated late and discarded when the development of the next title started. If you really wanted to invest in a given technology, you'd do it yourself.

![Circa 2014...](../../assets/7db5133ee8df4469.png)

Circa 2014...
This started changing with DLSS. Did you notice? No game studio ever trained their own temporal upscaler. And not that this was not key technology - AAA game rendering is mostly a collection of stochastic integrators.

Temporal techniques are fundamental to all rendering stages - and big studios invested a ton in "conventional" upsamplers. Jorge's

[filmic SMAA](https://www.iryoku.com/publications/) is probably even today among the state of the art - and it took a TON of work at the time (I know well - as I helped a bit too), on top of all the previous years of research he did on similar techniques.

DLSS is the first time NV created something that game studios really needed, and could not produce themselves.

It's a foothold in rendering pipelines...

**Enter DLSS5.**
The first "revolution" of DLSS5 - IF successful, is then that even more of the game pipeline gets under control of a hardware vendor.

Games would be significantly different with or without NV hardware - and not (just) because of the hardware (tensor cores etc) but because of a software investment.

Maybe, some games - from smaller studios - might even rely on it as their "primary" visual target, i.e. authoring against it.

In the grand scheme of things, it's not huge. Because gaming is not huge for NV anymore. But in our small "niche" - it's potentially huge!

NV carving out, gradually, more rendering space - under their direct control.

Did you notice, btw, that DLSS is already its own thing? AFAIU, you don't really link it to your game, statically. It's a system with its own "life" - including "over the air" automated updates of the ML models utilized (NV NGX)...

What did not really happen with RTX (somewhat even "despised" by gamers, now too attached to resolution and FPS targets to allow these numbers to go down for hard-to-understand visual gains) - might happen here.

Probably not today. CUDA took a decade plus. DLSS took multiple iterations to be excellent. But one day? Could be...

And if it ever happens, I don't think it would be easy for anyone else to catch up. I'd bet that already today, for "conventional" DLSS, the amount of data and compute required for the training is something hard to come by outside "big AI" companies. i.e., out of the reach of game studios or console makers.

Moreover, DLSS does create some sort of "dependence", as it's not cheap, it encroaches on the real-time rendering budget. It can create dependence.

**Stochastic speculations.**
Now for the fun part - how does this work? Of course, I have no idea! That's

[where](https://c0de517e.blogspot.com/2020/12/hallucinations-re-rendering-of.html) the

[fun is](https://c0de517e.blogspot.com/2020/05/some-thoughts-on-unreal-5s-nanite-in.html)!

In fact, other than reading the original announcement, I didn't really try to seek out all the public information out there. No spoilers!

Every time you want to dissect some graphics technique, you should start by observing its artifacts. So, I downloaded all the screenshots from the showcase on/off games: EA FUT, Hogwarts Legacy, Starfield, Assassin's Creed, RE: Requiem and the Zorah tech demo.

What can we learn from these? What stood out to me:

1) DLSS5 seems to strictly respect the original geometry and texture data. It's pixel exact - edges don't move around at all - down to aliasing/post-processing artifacts.

![](../../assets/c59124c7ad751de6.png)

2) It "reuses" the original rendered shadows. It does not take/infer a g-buffer and compute lighting ex novo - instead, it operates like an automated photo retoucher over the original image - if it "thinks" that some shadows should not be there, it just lightens them, again respecting the original image quite strictly.

![](../../assets/d3dfccf53822c22e.png)

3) It is temporally stable but does seem to have "screenspace" artifacts - especially when adding shadows, they are akin to SSAO - can't see outside the screen, behind objects.

![](../../assets/2b5f3322637e8b02.png)

4) OTOH, it knows the visible geometry precisely. When it adds these "AO-like" shadows, they are precise, even when the original rendered image does not have obvious depth hints (see for example the subtle shadow between the leg and the shorts, added to EA FUT - in the image above).

5) Faces are another story. There, it can be more heavy handed, and it seems that somehow it's trained specifically for them? On some screenshots it's even possible to see a "halo" effect around them - like if a retoucher went a bit too fast and did not precisely isolate the hair.

![](../../assets/d53358ab13986218.png)

**Deductions.**
Could this be strictly an image2image model, specialized for a singular purpose? In terms of AI capabilities, I think it could.

Generalist vision models nowadays are so powerful they can analyze and infer a lot from an image. You can take Google's Nano Banana, prompt it to generate depth/normal/albedo/metalness from an input image, and the results can be quite impressive.

![Image to Gbuffer...](../../assets/26730688e962fa3b.png)

Image to Gbuffer...
Furthermore, you can ask to describe the lighting setting in said image, then open a separate conversation - feed back the g-buffer and lighting description, and ask to return a rendered image back.

![...and back.](../../assets/f4625ffa0982de10.png)

...and back.![Another example.](../../assets/87124c80c4263ef1.png)

Another example.
...all this to say, that yes, a transformer nowadays can understand the structure of a scene and re-light it. In fact, I am quite certain that these models were explicitly trained with some amount of synthetic images to produce things like depth and normals, as this almost "world model" understanding of the scene is likely to help them in general when performing editing tasks.

And of course, you can take an image editing model and just prompt it to "upgrade" the lighting - to some degree of success.

![Asking a "local" qwen edit instance (4080 16gb) to upgrade lighting.](../../assets/baee59de8319070f.png)

Asking a "local" qwen edit instance (4080 16gb) to upgrade lighting.
But none of these models are precise, and I doubt they could ever be from pixels alone. If we look at the state of the art of specialized image to depth models, even if the results are quite impressive, they are not pixel perfect.

![Depth Anything 3 and Marigold - image 2 depth.](../../assets/104ac224944c4d43.png)

Depth Anything 3 and Marigold - image 2 depth.
So yes, obviously I think DLSS5 takes depth as input, but that's not shocking, there's no post-effect that does not, really. I'd go a bit further though, and speculate that it's working off full g-buffers.

I did some quick googling, and apparently all the games showcased were on deferred rendering engines. More than that, most of them seemed even to already have integrated (NVIDIA's hands?) RTX and DLSS Ray Reconstruction.

And guess what? DLSS Ray Reconstruction already accepts as inputs

[a ton of different channels](https://github.com/NVIDIA-RTX/Streamline), much more scene detail than even a conventional g-buffer.

Who knows, it might even be that RTX/DLSS integration is part of how the data pipeline works for NV - they already happen to have many games where DLSS "syphons" a lot of data - easier to plug into that than ask game studios to help by providing frames and intermediate buffers etc - or solely relying on "synthetic" data out of their own test scenes and renderers.

At the same time, as we observed that shadows are not recomputed, I think this operates still strictly in screenspace, does not take in shadowmaps, cubemaps etc, and even less, mesh/geometry data.

Looking at DLSS5 behavior, I would not be shocked if it's "simply" a U-Net/transformer that takes g-buffers and the final frame and outputs either a residual - a "corrective", similar to a dodge/burn mark in photographic retouching, or steers some parametric filter kernel to do similar operations.

I imagine as part of this, it will output some "memory" or feature map to tell next frames about what it did/"thought", and preserve coherency.

I'd wager, because why not at this point, that it's this sort of "restraint" on what it's "allowed" to do, that is both key to preserve the "pixel-perfect" original geometry/texture, and helps keep overall consistency on camera movements - as opposed to some sort of incrementally built approximation/memory of the 3d world.

**Conclusions?**
I guess one thing I did not yet do is to comment on what I think of DLSS5 overall.

Well.

**Right now**, and from what I could see, I'm

**not too impressed**. The lighting quality improvement is questionable - similar to RTX effects, I feel that in many cases if you stripped the images of the "on/off" labels, I'm not sure people would even always prefer the effect of DLSS5 "on".

For fun, I tried to hand-tune some of the "off" images (no DLSS5) using only "curves" (i.e. global color changes) and a touch of "highlights" (in gimp, but the same exists in most software from photoshop to instagram) correction, the latter a simple local filter. The end images are still different - but it's hard to tell what's "better".

![Which is on? Which is off? Does it matter?](../../assets/d43345be59657bed.png)

Which is on? Which is off? Does it matter?
Note that here I did not have access to the HDR images, or the depth/normals! I'd wager that you could write some simple set of hand-made heuristics (AO with some direction bias, tonemapping adjustments, perhaps with a pinch of locality), and gradient-descent their parameters to match DLSS5 quite well. In fairness, DLSS5 has to work over any possible game, whilst my adjustments were done ad-hoc. At the same time, this was all on cherry-picked (by NVIDIA) cases, adding much more computational expense than what I'm doing - and - in some cases using games that are not known for the very best lighting quality to begin with (open world etc...).

OTOH, the (much more maligned - over the internet) improvements on faces on the other hand are really quite neat. That is a much more difficult thing to get right anyways; arguably, we have not cracked photorealistic real-time faces in general, probably we don't even have the full shading theory solved yet (see for example

[the "correctives" employed](https://www.iryoku.com/publications/) in "The Callisto Protocol" character rendering). And consider also that we are much better at detecting even slight mistakes on face appearance than environment lighting...

![Same pre-adjusment of colors and highlights. Delta after mild blurring.](../../assets/aed6fbdadad7f3d1.png)

Same pre-adjusment of colors and highlights. Delta after mild blurring.
Now the difference is clear, and it's

**clearly an improvement**. The shadowing is definitely more correct - not just different. The BRDF itself seems to be changed, we have highlights that did not exist at all in the original image, not even a hint of them. And the BRDF change does seem to "know" about things - the extra eye highlight in the RE image is particularly telling - DLSS "knows" that eyes are shiny (ok, could have gotten that from a gbuffer maybe) - and seems to have made some guess about lighting direction and "softness" - things that go beyond what can be done with simple adjustments.

It even seems that it's adding - when neeed - texture details (skin pores), whilst still preserving the art "continuity".

I imagine (/hope - it would be exciting) it's the very same architecture at play, but allowing it to be more... opinionated. And as I said, I would not be surprised if it was also custom-trained specifically for faces, as you can generate some synthetic ground truths with very expensive path traced subsurface scattering etc.

Overall, though, I feel the reason DLSS5 is interesting lies much more in a potential future than its present.

If I'm even in the ballpark of right, should we call a system like the one I described, truly "neural rendering"? I would say it looks more like a neural photoshop. And if that's fair... today... imagine a future where the invasion and integration of neural techniques in the rendering pipeline become even more deep. Could it achieve both better lighting and be cheaper computationally?

I guess we'll see.