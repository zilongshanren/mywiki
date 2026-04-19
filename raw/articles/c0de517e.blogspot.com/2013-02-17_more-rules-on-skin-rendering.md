---
title: More rules. On skin rendering
url: https://c0de517e.blogspot.com/2013/02/more-rules-on-skin-rendering.html
published: '2013-02-17'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**Update**: What happened to this article? Many asked me. Well, now I can tell,[THIS](http://www.iryoku.com/next-generation-life)happened. My work and Jorge's ones are not related at all, but we both worked on skin for a while, and some of stuff on this article strongly related to what he, independently, discovered. As I was aware that his article was to be presented to GDC and totally rocked, as usual, I preferred to push this offline to get a cleaner "launch window" for his work. Which you should read. Now (or as soon as the final slides go online...). Even if you were at GDC13, most of the details and most of his research could not fit into the limits of the live presentation.*---*

A year ago or so,

[I wrote an article](http://c0de517e.blogspot.ca/2011/12/three-skin-rendering-horrors-you-want.html)out of frustration almost, about skin rendering and its "horrors" in videogames. This is a follow-up to that one. It's been some years that I've been

[working on characters](http://c0de517e.blogspot.ca/2011/09/fight-night-champion-gdc.html)and skin, in a few games, for a few different companies.

I won't get into any technical detail, partly because I don't want to spill information regarding games I've done in the past, but mostly, because I don't think the specific techniques are very important.

It's what we know and how much we understand of the skin (or any other rendering element) that makes the difference, once we know the problems, what matters and what not, why things behave a given way, crafting a model for rendering is often not too hard (might be time consuming though) and closely depends on the hardware, the budgets, the art resources and the lighting we have to integrate.



**1 - Attention to detail**

I already talked about this point to an extent in the previous post, but really, this is the first thing to keep in mind. Model (in the mathematical sense), tune (with your artists, hopefully), compare (with solid references). Rinse and repeat, again and again. What is wrong? Why?

I could not explain this better than

[Jorge Jimenez](http://www.iryoku.com/open-your-eyes)[did with his work](http://www.iryoku.com/open-your-eyes), presented at Siggraph 2012, an example of how applied graphics R&D should look like. He's a great guy and is doing a great service to our craft. Don't look only at his techniques, but understand the components and the methodology.
![]() |

Actually I didn't even, so far, end up using any of his work directly in a game (-I would try though-, if I was to make another deferred lighting renderer, for a foward I still believe

[pre-integration](http://advances.realtimerendering.com/s2011/Penner%20-%20Pre-Integrated%20Skin%20Rendering%20(Siggraph%202011%20Advances%20in%20Real-Time%20Rendering%20Course).pptx), even if it's a pain to manage, has an edge) and there are some details that might be further expanded (for example I believe that for the ears something[akin to Colin Barré-Brisebois'](http://colinbarrebrisebois.com/2011/03/07/gdc-2011-approximating-translucency-for-a-fast-cheap-and-convincing-subsurface-scattering-look/)method, maybe an extension, could work better)... But his methodology is an example even greater than the excellent implementation he provides. That to me is the real deal.**2 - Get good references**

How are you going to have "attention to detail" without references... And you'll need, possibly, different references per rendering component. And I don't mean here hair, eyes, lips (these too, obviously) but diffuse, specular, subsurface... It's very hard to tune rendering looking only at a picture, in order to generate that end image there is a mixture of so many parameters, from shading to lighting to the textures and models, to things like color spaces and tonemapping.

Linear HDR photos are a starting point, but these days, at least

[decoupling specular from diffuse](http://filmicgames.com/archives/233), at least well enough to be used as a lighting reference, is not hard (doing so for texturing purposes requires much more precision and it's best done with an automated system).
Acquire references under controlled lighting. Acquire lighting together with your reference under the typical conditions you'll need your characters to be in.

Some of my go-to third-party references:

[Debevec’s research](http://www.pauldebevec.com/)is the go-to reference for all things characters. Even if you're not lucky enough to have access to a lightstage, read all his papers, look at all the screenshots. Some important examples:[Rapid Acquisition of Specular and Diffuse Normal Maps from Polarized Spherical Gradient Illumination](http://gl.ict.usc.edu/Research/FaceScanning/)[The Digital Emily project](http://gl.ict.usc.edu/Research/DigitalEmily/)[Measurement Based Synthesis of Facial Microgeometry](http://www.youtube.com/watch?v=nhiaBU3rrJc)- Acquired specular parameters
[MERL/ETH Skin Reflectance Database](http://gvi.seas.harvard.edu/ext/facescanning/index.html)[Analysis of Human Faces using a Measurement-Based](http://graphics.ucsd.edu/~henrik/papers/skin-analysis/skin-analysis.pdf)

Skin Reﬂectance Model[Acquisition of human faces using a measurement-based skin reflectance model](http://web4.cs.ucl.ac.uk/staff/t.weyrich/projects/phd/weyrich-2006-phd-lowres.pdf)- Acquired BRDFs
- More...

**3 - You'll need tonemapping**

If you want to work with real, acquired references, you'll need to understand and apply tonemapping. Skin, if you let your shading just clamp in the sRGB range, looks terribly wrong. Also, detail is completely annihilated, and your artists will mess up the tuning trying to avoid loosing too much color or detail (usually, dialing in an unrealistically low amount of specular, and/or painting a very pale diffuse). Try taking Penner's pre-integrated skin scattering formulation, and see how does it look without tonemapping...

![]() |

__Note that this is not related to HDR buffers or anything HDR. Even on an old title, without any shader cycles to spare, rendering in a 8bit buffer, at least on the skin, you'll need some tonemapping.__White-balanced Reinhard works decently in a pinch. And if you're thinking that it would be "wrong" to tonemap in the shading or so, don't. If you're rendering to an 8bit sRGB buffer, you're outputting colors out of your shader. Not any radiometric quantity, just final colors. Colors are not "right" or "wrong" they can just look right or wrong. Anything that you'll do, is "wrong" anyways, alphablending, postprocessing, whatever. So choose the good-looking "wrong" over the horribly looking one...

**4 - Understand your scales**

One of the hard parts or modeling shading is to understand at what scale the various light phenomena occur, what happens between them, and how to transition. What is the scale of the BRDF? What is the scale of textures? What of geometry?

Nowadays, especially on specular this is understood, with techniques like

[Lean and Clean](http://www.gdcvault.com/play/1014558/Spectacular-Specular-LEAN-and-CLEAN),[Toksvig mapping](ftp://download.nvidia.com/developer/Papers/Mipmapping_Normal_Maps.pdf)and so on. But that doesn't mean that we apply the right care on all materials. Often I've found that we take formulas and methods that are valid at one scale and apply them to materials which have roughness and features at a scale much different than the scale of the original BRDF. And fail to integrate these features.
For example, skin specular. Which model to use? If you look at skin, close up, it's fairly different from the assumptions of Cook-Torrance.

Again really, pay attention and use references. Look at your models at different magnifications. You'll find interesting things. For example a single KSK lobe is hardly enough to capture specular (regardless of what some papers write). Fresnel terms might need tweaking, and so on.

![]() |

**5 - Account for ALL the lighting and ALL the occlusions**

This is especially important if you work with Penner's Pre-Integrated scattering, but it's true in general. Do you have analytic lights? They will have a diffuse term, to integrate with subsurface scattering somehow. They will have a specular term. How do shadow them? The shadowing also needs to be part of the subsurface scattering, somehow (Penner provides answer for these already), and it has to occlude specular too.

Do you have ambient? You'll need the same. Ambient has specular too. Ambient contributes to SSS. And it needs to be occluded. And don't stop at that! Compare, use references and you'll find if you're missing something, or leaking something.

For example, it's usual to shadow ambient with ambient occlusion, but even in the areas occluded by the AO there is some residual lighting (a hint, generally, you will need to add some redness there as skin bounces on itself and scatters... just multiplying ambient*AO does not work well, as I wrote in the previous article).

![]() |

All this work is also why a method like UV-space or screen-space subsurface (like Jimenez method, which is the state of the art right now) is much easier to use, as it can apply SSS on all lighting you put in the scene with a single, consistent method.

## No comments:

Post a Comment