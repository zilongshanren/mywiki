---
title: 'Order Independent Transparency: Endgame'
url: https://interplayoflight.wordpress.com/2022/07/10/order-independent-transparency-endgame/
author: Kostas Anagnostou
published: '2022-07-10'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

In the past 2 posts ([part 1](https://interplayoflight.wordpress.com/2022/06/25/order-independent-transparency-part-1/), [part 2](https://interplayoflight.wordpress.com/2022/07/02/order-independent-transparency-part-2/)), I discussed the complexity of correctly sorting and rendering transparent surfaces and I went through a few OIT options, including per pixel linked lists, transmission function approximations and the role rasteriser order views can play in all this. In this last post I will continue and wrap up my OIT exploration discussing a couple more transmittance function approximations that can be used to implement improved transparency rendering.

As a reminder, this is what a transmittance function could look like

![](../../assets/f983bd1f0ad18438.png)


![](../../assets/f983bd1f0ad18438.png)

to extract the total transmittance at each surface point and correctly composite its colour.

Extracting the transmittance function is not trivial though and we discussed techniques to calculate it using 2 geometry passes, one to define it and one to use it to composite the transparent surfaces.

One technique that makes no attempt to approximate the transmittance function is [Weighted Blended Order-Independent Transparency](https://jcgt.org/published/0002/02/09/) (WBOIT). Instead, it replaces the transmittance function with a weight function w(z,a):

which acts as an estimator of occlusion at each depth (something that the transmittance function provides exactly). The weight function should ideally take the alpha value into account as well, to better resolve overlapping surfaces with varying opacity.

These are a few weight functions from the paper, but other monotonically decreasing functions could do, depending on the scene content:

WBOIT needs a single geometry pass, accumulating the weighted premultiplied surface colour Ci in one rendertarget and the surface transmittance in a second. Then it performs a screen space pass to resolve the composited surface colour, normalise it in case the weight function approximation was not accurate enough and combine it with the background colour C0. If you notice in the above function, the total transmittance accumulation is exact which means that the background is occluded correctly by the transparent surfaces.

In general this is a cheap way, both in terms of memory and rendering cost, to approximate OIT and can work convincingly if you can provide a weight function that matches the scene’s transparent content well, something that is not always easy. The authors discuss [implementations of the technique](http://casual-effects.blogspot.com/2015/03/implemented-weighted-blended-order.html) if you’d like to experiment further with it.

The last OIT technique I investigated was Moment based OIT (MBOIT). It was independently introduced twice in the same year at [I3D 2018](https://momentsingraphics.de/I3D2018.html) and [HPG 2018](https://briansharpe.files.wordpress.com/2018/07/moment-transparency-av.pdf). This approach uses a series of moments to approximate the transmittance function, building upon the idea of [Moment Shadow Mapping](http://momentsingraphics.de/Media/I3D2015/MomentShadowMapping.pdf). Moments in general are quantities that describe the shape of a graph of a function. Two well known moments are the mean value and variance of a distribution for example. In this case we use moments based on the scene depth, more specifically a series of depth powers.

As many transmittance function approximation techniques, MBOIT requires two geometry rendering passes, one to calculate the moments and a second to use those moments, reconstruct transmission at each point and blend the transparent surfaces.

While rendering the transparent meshes during the first pass, we calculate powers of the z distance of the surface. For example, for a 4 moments approximation we would need this vector of powers for depth:

We have already defined transmittance function as the product of the individual transmittance value over distance

MBOIT transfers this to logarithmic space to convert the product into a summation and calls it absorbance A(z):

Having the absorbance and the depth powers at hand we can calculate and store this approximation of the transmittance function

Worth noticing that for N moments we will need N+1 channels, and that the first element, the zeroth moment b0, holds the total absorbance for a specific pixel, the one we will eventually use to blend the background colour with. To store the moments I used a rendertarget with a single channel for the zeroth moment and one or two 4 channel rendertargets for the rest of the moments (for 4 or 8 moments approximation). Also, I accumulated the moments with additive blending.

During the second geometry pass we use the moments to reconstruct the transmittance at a specific depth (effectively undoing the conversion to logarithmic space, we performed above)

and then use that function to composite the surface colour in an OIT fashion as discussed in the [first post](https://interplayoflight.wordpress.com/2022/06/25/order-independent-transparency-part-1/).

To wrap it up, we perform a screen space pass to blend the composited surfaces with the background colour, using the zeroth moment which, as discussed, can be used to reconstruct the total transmittance at a pixel.

I won’t spend much time discussing code, I used the [sample code](https://momentsingraphics.de/I3D2018.html) from the MBOIT paper, it is sufficient to give a feel of how the technique works. I also used the path that uses hardware bending to accumulate the moments and not the one that uses ROVs.

What I will do is discuss some results and performance cost. For reference, this is normal hardware blending, with the all transparency sorting artifacts, rendering at 1.37ms for a 1080p resolution.

![](../../assets/a8a0b6bb0efbaac9.png)


![](../../assets/a8a0b6bb0efbaac9.png)

![](../../assets/cf27a0c2bf7a6f54.png)


![](../../assets/cf27a0c2bf7a6f54.png)

MBOIT with 8 moments, again 32 bits/channel, at 13.1ms.

![](../../assets/ed6ae83417015962.png)


![](../../assets/ed6ae83417015962.png)

The cost of the technique is quite high though, driven mainly by the full fat rendertargets. Switching to 16bits per channel helps performance a lot.

MBOIT with 4 moments, at 16 bit per channel, the cost now drops to 3.5ms.

![](../../assets/06640b2b78b3b4da.png)


![](../../assets/06640b2b78b3b4da.png)

Similar gains we notice for the 8 moments, which now cost 6.2 ms. If there is any impact on the visuals it is not noticeable with this content.

![](../../assets/bf7e44b31fa96cd0.png)


![](../../assets/bf7e44b31fa96cd0.png)

![](../../assets/cfc1cfc4d8e32745.png)


![](../../assets/cfc1cfc4d8e32745.png)

An advantage of using moments to approximate the transmittance function is that they are filterable, meaning we can render them at a lower screen resolution and use them to reconstruct transmittance at a higher resolution. The following is accumulating the 4 moments at 960×560 during the first pass and compositing transparency at full res during the second.

![](../../assets/574376560308b4c8.png)


![](../../assets/574376560308b4c8.png)

![](../../assets/f07d86c71af700c5.png)


![](../../assets/f07d86c71af700c5.png)

Speaking of biasing, MBOIT, unlike other OIT techniques we discussed, has some levers like the “biasing” I mentioned and “overestimation” to tune it better to specific content. Also, before I close the MBOIT subject, there is also the option to use trigonometric moments instead of power ones to improve the transmittance function reconstruction, but from a quick experiment I made I didn’t see a noticeable difference so this will need some more investigation.

It is also worth mentioning [an older experiment](https://twitter.com/KostasAAA/status/1482405821963247619?s=20&t=Ogg3s6Xx4CTqWpR5iO3mUA) I made, using [interleaved gradient noise](https://blog.demofox.org/2022/01/01/interleaved-gradient-noise-a-different-kind-of-low-discrepancy-sequence/) during the opaque pass to randomly discard pixels

![](../../assets/dc31a4fe488d4b92.png)


![](../../assets/dc31a4fe488d4b92.png)

![](../../assets/36cd16b650f9a3f9.png)


![](../../assets/36cd16b650f9a3f9.png)

And with that we reached the end of the OIT exploration. If we can draw one conclusion is that transparency is a complicated and expensive problem to solve correctly. We didn’t even talk about other effects that accompany transparency, like refraction of transparent surfaces (as opposed to refracting the background only). None of the techniques I presented can fully solve this, in all likelihood a more traditional distortion accumulation would have to complement the geometry pass which will be used to refract the background later.

After all this I don’t feel like I got a good answer of what is the best approach to render transparency, it is a decision that should be made on a case by case basis, based on the requirements of the content and restrictions of the engine. If the meshes are sortable and you don’t care about material batching one should start with that. It is a cheap solution and will help OIT techniques (like MLAB) if you decide to use one. Then, factors like memory, tolerance to visual errors and hardware support will all factor in the decision of what OIT is best for a particular case. Hybrids are certainly a viable solution, for COD Treyarch developed [an OIT method](https://research.activision.com/content/dam/atvi/activision/atvi-touchui/research/tech-reports/docs/PracticalOIT.pdf) that mixes per pixel arrays for transparent meshes (not unlike the PPLL we discussed) with software rasterisation for particles. There is a smorgasbord of [OIT methods](http://cwyman.org/papers/hpg16_oitContinuum.pdf) for one to explore and consider for their game.

To wrap it up, it is worth considering if raytracing will eventually fix this, as is the expectation with a lot of hard rasterisation problems. This would be particularly appealing as no extra structures or memory would be required to store fragments or nodes. To my knowledge, the only mechanism DXR provides for “sorting” surfaces is the closest hit shader. So the idea then would be to raycast from the camera, use the closest hit shader to retrieve the closest transparent surface, composite its colour and then make its position (with some bias) the origin of another ray and again use the closest hit shader to retrieve the next closest surface, iterating in the ray generation shader until no hits are returned any more. I can imagine refraction being easy with such a scheme and also the ability to terminate a ray if the accumulated opacity exceeds a threshold that makes is practically “opaque”. What I don’t know is the performance impact of such an approach as I haven’t added support for DXR to the toy engine yet. An investigation for another time then.