---
title: Tone mapping & local adaption
url: http://c0de517e.blogspot.com/2016/09/tone-mapping-local-adaption.html
published: '2016-09-11'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*My friend Bart recently wrote a series of great articles on tone mapping, showing how*

[localized models](https://bartwronski.com/2016/08/29/localized-tonemapping/)can be useful in certain scenarios, and I strongly advise to head over to his blog to read that one first, which motivated me to finally dump some of my notes and small experiments on the blog...
Local tone mapping refers to the idea of varying the tone mapping per pixel, instead of applying a single curve globally on the frame. Typically the curve is adapted by using some neighborhood-based filter to derive a localized adaption factor, which can help preserve details in both bright and dark areas of the image.

At the extreme, local operators give the typical "photographic HDR" look, which looks very unnatural as it's trying to preserve as much texture information possible at the detriment of brightness perception.

![]() |

[lifehacker](http://lifehacker.com/5991508/what-is-hdr-and-when-should-i-use-it-in-my-photos)
While these techniques help display the kind of detail we are able to perceive in natural scenes, in practice the resulting image only exacerbates the fact that we are displaying our content on a screen that doesn't have the dynamic range that natural scenes have, and the results are very unrealistic.

That's why global tonemapping is not only cheaper but most often appropriate for games, as we aim to preserve the perception of brightness even if it means sacrificing detail.

We like brightness preservation so much in fact, that two of the very rare instances of videogame-specific visual devices in photorealistic rendering are dedicated to it: bloom and adaption.



Veiling glare in COD:AW



We like brightness preservation so much in fact, that two of the very rare instances of videogame-specific visual devices in photorealistic rendering are dedicated to it: bloom and adaption.

![]() |

Most of photorealistic videogames still, and understandably, borrow heavily from movies, in terms of their visual language (even more so than photography), but you will never see the heavy-handed exposure adaption videogames employ, in movies, nor you'll see what we usually call "bloom", normally (unless for special effect, like in a dreamy or flashback sequence).


Of course, a given amount of glare is unavoidable in real lenses, but that is considered an undesirable characteristic, an aberration to minimize, not a sought-after one! You won't see a "bloom" slider in lightroom, or the effect heavily used in CG movies...



An image used in the marketing of the

showing very little glare in a challenging situation


Even our eyes are subject to some glare, and they do adapt to the environment brightness, but this biological inspiration is quite weak as a justification for these effects, as no game really cares to simulate what our vision does, and even if that was done it would not





So it would seem that all is said and done, and we have a strong motivation for global tonemapping. Except that, in practice, we are still balancing different goals!

We don't want our contrast to be so extreme that nothing detail can be seen anymore in our pursuit of brightness representation, so typically we tweak our light rigs to add lights where we have too much darkness, and dim lighting where it would be too harsh (e.g. the sun is rarely its true intensity...). Following cinematography yet again.


Gregory Crewdson


How does local tone mapping factor in all this? The idea of local tone mapping is to operate the range compression only at low spatial frequency, leaving high-frequency detail intact.

One one hand this makes sense because we're more sensitive to changes in contrast at high-frequency than we are at lower frequencies, so the compression is supposed to be less noticeable done that way.


Of course, we have to be careful not to create halos, which would be very evident, so typically edge-aware frequency separation is used, for example employing


But this kind of edge-aware frequency separation can be also interpreted in a different way. Effectively what it's trying to approximate is an "intrinsic image" decomposition, separating the


So if we accept that light rigs must be tweaked compared to a strict adherence to measured real scenes, why can't we directly change the lighting intensity with tone mapping curves? And if we accept that, and we understand that local tonemapping is just trying to decompose the image lighting from the textures, why bothering with filters, when we have computed lighting in our renderers?


This is a thought that I had for a while, but didn't really put in practice, and more research is necessary to understand how exactly one should tone-map lighting. But the idea is very simple, and I did do some rough experiments with some images I saved from a testbed.


The decomposition I employ is trivial. I compute an image that is the scene as it would appear if all the surfaces where white (so it's diffuse + specular, without multiplying by the material textures) and call that my illuminance. Then I take the final rendered image, divide it by the illuminance to get an estimate of reflectance.





Of course, a given amount of glare is unavoidable in real lenses, but that is considered an undesirable characteristic, an aberration to minimize, not a sought-after one! You won't see a "bloom" slider in lightroom, or the effect heavily used in CG movies...

![]() |

[Zeiss Otus 24mm](http://lenspire.zeiss.com/en/happy-new-year/),showing very little glare in a challenging situation

Even our eyes are subject to some glare, and they do adapt to the environment brightness, but this biological inspiration is quite weak as a justification for these effects, as no game really cares to simulate what our vision does, and even if that was done it would not

[necessarily improve perceived brightness](http://graphics.stanford.edu/papers/gazehdr/gazehdr.pdf), as simulating a process that happens automatically for us on a 2d computer screen that then is seen through our eyes, doesn't trigger in our brain the same response as the natural one does!
![]() |

[Trent Parke](http://www.graphicine.com/trent-parke-summer-rain/)So it would seem that all is said and done, and we have a strong motivation for global tonemapping. Except that, in practice, we are still balancing different goals!

We don't want our contrast to be so extreme that nothing detail can be seen anymore in our pursuit of brightness representation, so typically we tweak our light rigs to add lights where we have too much darkness, and dim lighting where it would be too harsh (e.g. the sun is rarely its true intensity...). Following cinematography yet again.

![]() |

How does local tone mapping factor in all this? The idea of local tone mapping is to operate the range compression only at low spatial frequency, leaving high-frequency detail intact.

One one hand this makes sense because we're more sensitive to changes in contrast at high-frequency than we are at lower frequencies, so the compression is supposed to be less noticeable done that way.

Of course, we have to be careful not to create halos, which would be very evident, so typically edge-aware frequency separation is used, for example employing

[bilateral filters](https://people.csail.mit.edu/fredo/PUBLI/Siggraph2002/DurandBilateral.pdf)or other more advanced techniques (Adobe for example employs[local laplacial pyramids](https://hal.archives-ouvertes.fr/hal-01063419/file/2014-fast-laplacian-filter.pdf)in their products, afaik).But this kind of edge-aware frequency separation can be also interpreted in a different way. Effectively what it's trying to approximate is an "intrinsic image" decomposition, separating the

[scene reflectance from illuminance](http://www.cs.huji.ac.il/~danix/hdr/hdrc.pdf)(e.g. Retinex theory).So if we accept that light rigs must be tweaked compared to a strict adherence to measured real scenes, why can't we directly change the lighting intensity with tone mapping curves? And if we accept that, and we understand that local tonemapping is just trying to decompose the image lighting from the textures, why bothering with filters, when we have computed lighting in our renderers?

This is a thought that I had for a while, but didn't really put in practice, and more research is necessary to understand how exactly one should tone-map lighting. But the idea is very simple, and I did do some rough experiments with some images I saved from a testbed.

The decomposition I employ is trivial. I compute an image that is the scene as it would appear if all the surfaces where white (so it's diffuse + specular, without multiplying by the material textures) and call that my illuminance. Then I take the final rendered image, divide it by the illuminance to get an estimate of reflectance.

*Note that looking at the scene illuminance would also be a good way to do exposure adaption (it removes the assumption that surfaces are middle gray), even if I don't think adaption will ever by great done in screen-space (and if you do so, you should really look at the anchoring theory), better to look at more global markers of scene lighting (e.g. light probes...).*Once you compute this decomposition, you can then apply a curve to the illuminance, multiply the reflectance back in, and do some global tone mapping as usual (I don't want to do -all- the range compression on the lighting).

![]() |

The latter can compress highlights more while still having brighter mids.

I think with some more effort, this technique could yield interesting results. It's particularly tricky to understand what's a proper midpoint to use for the compression, and what kind of courve to apply to the lighting versus globally on the image, and how to do all this properly without changing color saturation (an issue in tone mapping in general), but it could have its advantages.

In theory, this lies somewhere in between the idea of changing light intensities and injecting more lights (which is still properly "PBR"), and the (bad) practices of changing bounce intensity and other tweaks that mess with the lighting calculations. We know we have to respect the overall ratios of shadow (ambient) to diffuse light, to specular highlights (and that's why tweaking GI is not great).

But other than that, I don't think we have any ground to say what's better, that's to say, what would be perceptually closer to the real scene as seen by people, for now, these are all tools for our artists to try and figure how to generate realistic images.

I think we too

[often limit ourselves by trying to emulate other medias](http://c0de517e.blogspot.ca/2016/03/beyond-photographic-realism.html). In part, this is reasonable, because trying to copy established visual tools is easier both for the rendering engineer (less research) and for the artists (more familiarity). But sooner or later we'll have to develop our own tools four our virtual worlds, breaking free of the constraints of photography and understanding what's best for perceptual realism.

**"Conclusions"**

Adding lights and changing the scenes is a very reasonable first step towards dynamic range compression: effectively we're trying to create scenes that have a more limited DR to begin with, so we work with the constraints of our output devices.

Adding fill lights also can make sense, but we should strive to create our own light rigs, there's very little reason to constrain ourselves to point or spots for these. Also, we should try to understand what could be done to control these rigs. In movies, they adapt per shot. In games we can't do that, so we have to think of how to expose controls to turn these on and off, how to change lighting dynamically.

Past that, there is tone-mapping and color-grading. Often I think we abuse of these because we don't have powerful tools to quickly iterate on lighting. It's easier to change the "mood" of a scene by grading rather than editing light groups and fill lights, but there's no reason for that to be true!

We should re-think bloom. If we use it to represent brightness, are the current methods (which are inspired by camera lenses) the best? Should we experiment with different thresholds, with maybe subtracting light instead of just adding it (e.g. bring slightly down the scene brightness in a large area around a bright source, to increase contrast...).

And also, then again, movies are graded per shot, and by masking (rotoscoping) areas. We can easily grade based on distance and masks, but it's seldom done.

Then we have all the tools that we could create beyond things inspired by cinematography. We have a perfect HDR representation of a scene. We have the scene components. We can create techniques that are impossible when dealing with the real world, and there are even things that are impractical in offline CGI which we can do easily on the other hand.

We should think of what we are trying to achieve in visual and perceptual terms, and then find the best technical tool to do so.

## No comments:

Post a Comment