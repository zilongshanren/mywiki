---
title: An unbiased look at real-time raytracing
url: https://c0de517e.blogspot.com/2019/03/an-unbiased-look-at-real-time-raytracing.html
published: '2019-03-30'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**Evaluating technology without hype or hate...**

That would have been the title of my blog post if I published the version I had prepared after the DXR/RTX technology finally became public last year, at GDC 2018.

But alas I didn't. It remained in my drafts folder. Siggraph came and went. Now another GDC, and I finally decided to can that and rewrite it.

Why? Not because I thought the topic wasn't interesting. Hype is easy to give in to. Fear of missing out, excitement about new toys to play with, tech for tech's sake... Hate is equally devious. Fear of change. Comfort zones, familiarity.

These are all very interesting things to think about. And you should. But can I claim I am an expert on this? I don't know, I am not a venture capitalist, and I could say I've been right a number of times, but I doubt that reaches the threshold of statistical significance.

Moreover, being old and grumpy and betting against new technologies is often an easy win. Innovation is hard!

And really, it doesn't matter much. This technology is already in the hardware, and it will stay for the future. It is backed by large companies, and more will come on board for sure. And yes, it could go the way of geometry shaders and other things that tried to work "against" the established GPU architectures, but even for these, we did spend some time to understand how they could help us...

So, let's just assume we want to do some R&D in this RTRT thing and let's ask a different question. What should we be looking for?

**The do and do not list of RTRT research.**

**DO NOT**- Think that RTRT will make things simpler, or that (technical) simplicity is an objective. In real-time rendering, the pain comes from within. There's nothing that will stop people spending one month to save 0.1ms in any renderer.

Until power is out of the equation, we will always build complex systems to achieve the ultimate quality vs performance tradeoffs. When people say that shadow maps are hard for example, they mostly mean that fast shadow maps are hard. Nobody prevents us from rendering huge, high precision maps with high-quality filtering. Even rendering from multiple light samples and doing proper area lights. We don't do it, because of performance optimization.

And that's true for all complexity in a real-time renderer. When we add raytracing to the mix we only sign for more pain, hybrid algorithms, code paths, caching schemes and so on. And that's ok. Programmer's pain doesn't really matter much in the logistics of the production of today's games.

![]() |

How much pain was spent to save fractions of ms on each?

**- Think about ray/memory/shading coherency and the GPU implications of raytracing. In other words, optimization. Right now, on high-end hardware, we can probably throw a few relatively naive raytracing effects and they will work because these GPUs are much more powerful than the consoles that constrain the scene and rendering complexity of most AAA games. They can render these scenes at obscene framerates and resolutions. So it might seem not a huge price to pay to drop back to 1080p and 60hz in order to have nicer effects. But this doesn't mean it's an efficient use of GPU power, and that won't stand long term.**

DO

DO

Performance/quality considerations are a great culler of rendering techniques. We need to think about efficient raytracing.

**DO NOT**- Focus on the "wrong" things. Specular reflections don't matter much. Perceptually they don't! Specular highlights, in general, are a strong indicator of shape and material in objects, but we are not good at spotting errors in the lighting environment that generates them. That's why cubemaps work so well. In fact, even for shiny floors and walls (planar mirrors) with objects near or in contact with them, we are fooled most of the times by relatively simple cheats. We see errors in screen-space reflections only because some times they fail catastrophically, and we're talking there about techniques that take fractions of milliseconds to compute. And reflections with raytracing are both too simple and too complex. Too simple, because they are an easy case of raytracing as rays tend to be very coherent. And too complex, because they require evaluating surface shading, which is hard to do in most engines outside screen-space and is slow as triggering different shaders with real-time raytracing is really not hardware friendly.

![]() |

**- Think about occlusion on the other hand. It's much more interesting, can be more hardware friendly, definitely is more engine friendly and most importantly it's likely to have a bigger visual impact. Correct shadows from area lights, but also correctly occluding indirect lighting, both specular and diffuse.**

DO

DO

**DO NOT**- Think that denoising will save the day. In the near future, for real-time rendering, it most likely will not. In fact in general denoising (even simple blurring that we sometimes already employ) can lift noise from high frequencies to lower ones, which under animation makes for worse artifacts.

**DO**- Invest in caching and temporal accumulation ideas. Beyond screen-space. These will likely be more effective, and useful for a wide variety of effects. Also, do think about finer-grained solutions to launch work / update caches / update on demand. For this, real-time raytracing might help indirectly, because it needs in order to be performant the ability to launch shader work from other shaders. That general ability, if implemented in hardware, and exposed to programmers, could be useful in general, and it's one of the most interesting things to think about when we think of hardware raytracing.

**DO NOT**- Make the wrong comparisons! RTX on / RTX off tells a lie, because what we can't see with "RTX off" is what the game could look like if we allocated all the power that RTX needs to pushing conventional techniques or even simply more assets. There are a lot of techniques we don't use today because we don't think they are on the right side of the quality/performance equation. We could use them, but we prefer to push more assets instead.

If you want to be persuasive about raytracing, proper comparisons should be made. And proper comparisons should also take into account that rasterization without shading (visibility only) leaves compute units available for other work to be done in parallel.

RTX hardware isn't free either! It costs chip area, even if you don't use it, but there's nothing we can do about that...

**DO NOT**- Assume that scene complexity is fixed. This is a corollary of the previous point, but we should always think at the very least, for overall visual impact, if simply pushing more stuff is better than pushing a given particular idea for "shinier" stuff, because scene complexity is far from having "peaked".

![]() |

Real-time, not quite. (frame from Avengers Infinity War)

**- Think about cases where raytracing could outperform rasterization at its own game. This is hard, because raytracing likely will always have a quite high cost, both because of the memory traffic that is required to traverse the spatial subdivision structures, and because it uses the compute units, while the rasterizer is a small piece of hardware that can operate in parallel. But, that said, raytracing could win in a couple of ways.**

DO

DO

First, because it's much more fine-grained. For example, refreshing very small areas in a shadow map could perhaps be faster with a raytracer. Another way to say this is that there are certain cases where the number of pixels we need visibility for is much smaller than the number of primitives and vertices we'd need to traverse in a rasterizer.

The second thing to think about is how raytraced visibility goes wide, using the compute units and thus, the entire GPU. The rasterizer, on the other hand, can often be the bottleneck. And even if in many cases we can overlap other work to keep the GPU busy, that is not true in all cases!

**DO**- Think about engineering costs if you want the technology to be used now. It's true that programmer's pain doesn't matter. But at the moment RTX covers a tiny slice of the market. Programmers could find their pain in completing more important tasks... Corollary: think about fallback techniques. If we're moving an effect to RTX, how will we render it on GPUs that don't support it? Will it look very different? Will it make authoring more painful? That is something we generally can't afford.

In general, be brutally honest about costs and feasibility of solutions. This is a good rule in general, but it is especially true for an emerging technology. You don't want to burn developers with techniques that look good on paper, but fail to ship.

**DO**- Establish collaborations. Real-time raytracing is probably not going to sell more copies of a game. And if it's not going to save costs and make authoring more effective, if we're talking about uses in the runtime (an exception could be for uses in the artist tools themselves, e.g. to aid lightmap baking and/or previewing). It currently targets only a small audience, and you'll gain nothing by jumping on this too early.

So, you probably should not pull your smartest R&D engineers from whatever they're doing to jump on this unless you have some very persuasive outside incentives... If not, you'll likely won't have many people to do raytracing related things.

Thus, you should probably see if you can leverage collaborations with external research groups...

## 1 comment:

Well put and interesting points. Personally I'm doing rendering and am looking forward to the great speedups we will for sure get here.

Post a Comment