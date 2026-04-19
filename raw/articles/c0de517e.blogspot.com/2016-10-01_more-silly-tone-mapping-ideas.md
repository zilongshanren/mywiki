---
title: More (silly) tone-mapping ideas
url: https://c0de517e.blogspot.com/2016/10/more-silly-tone-mapping-ideas.html
published: '2016-10-01'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

[previous post](http://c0de517e.blogspot.ca/2016/09/tone-mapping-local-adaption.html)I'll show here two more tone-mapping tricks. They are both "silly" in a way, they were done quickly and mostly while waiting for more important things to build, so they are far from "production quality".

They both are somewhat inspired by photography (but make no effort at all to simulate photographic effects, rather, they take inspiration from observing how certain things work), and I believe they could all be part (including the ideas of the previous post) of a single tone-mapping operator.

All dynamic range compression algorithms have trade-offs and artifacts, so I believe it's not unwise to layer various methods each doing just a bit of compression, to achieve an overall larger reduction.

**"Adaptive ND-Filter"**

*The idea of doing this test came from a discussion with my Italian friend Manuele Bonanno, as we were chatting about Bart's TM post (which I linked in the previous article).*

In landscape photography is not uncommon to use graduated neutral density filters. A ND filter reduces all wavelengths of light equally, darkening the image without shifting colors, and can be used for particular effects like very long exposures or to be able to use wide lens apertures in daylight.

A graduated ND filter does the same but using a gradient, and it's used typically to darken the sky (top half) relative to the other elements of the image.

![]() |

The interesting thing to notice is that even if in photography these filters are made with a fixed gradient, in practice the effect is smooth enough that it can make a big difference on the final image without being noticeable.

Our vision system is not good at detecting very low-frequency gradients in images, so after a given spatial frequency we can "cheat" liberally without being able to see artifacts.

How to apply this in computer graphics is rather obvious: let's just blur everything a lot and use that as a base for a localized tone-mapping operator (in the test below, I just scale the exposure by the blurred version of the image a bit, then apply global TM as usual).

Doing local tone-mapping with a gaussian blur average usually yields pretty strong haloing artifacts (and a lot of photographic HDR toning software actually is plagued by such halos), and my previous article tried to show an alternative that is both stupidly cheap and that can't result in haloing (as it's not using neighboring operators at all).

![]() |

![]() |

The "insight" here is that you can also prevent haloing if you use gaussian blur, but you blur enough not to be at frequencies where haloing shows. And, of course, if you have a good quality bloom/veil effect, you can re-use the image pyramids from that almost directly. Just remember to apply a -neutral- (grayscale) ND!

![]() |

Used tastefully and in a temporally stable way I think it can work, and indeed my colleague

[Michal](https://michaldrobot.com/)confirmed that he know of titles doing something similar.

I did a quick test using

[COD:AW](https://www.callofduty.com/ca/en/advancedwarfare)and the effect indeed works really well, actually even better indoors than outdoors often, reducing the amount of "auto-exposure" needed (which we don't push very far typically anyways).

**Film Grain**

What? Film grain is not about dynamic range, right? It's usually an artistic effect, at best it can be seen as a dithering method that can help avoiding Mach band artifacts. Right?

![]() |

Well, not really. If you look at an actual photo you'll notice that grains mostly show in midtones, or rather, that pure whites and pure blacks either saturate grains or have no grains exposed, and thus appear as solid regions.

![]() |

This means that if we look at a thresholded version of a good film scan we can see a spatial dithering in the threshold.

We have some black areas that have black grains but are not fully saturated with black, and then we have "blacker than black" areas where the same black grains appear spatially clustered to create an entirely saturated region (and the same happens in the highlights as well).

This suggests that we can use dithering patterns not only to get more precision in the midtones, but also to extend a bit the range of highlights and shadows. If a dither pattern is symmetric and equally distributed around zero (as it should be), sometimes it will add luminosity and sometimes it will subtract it.

So if an area is white, but not whiter-than-white, the times the pattern subtracts it will create darker pixels. In areas that are constantly whiter than the intensity of the dither, even after subtraction, we will still end up with a full white, and we will see saturated areas.

The image above is a quick test of the theory. On the left, it uses just the simple, old good Reinhard tone-mapping (with black and white levels used to get contrast). The image on the right uses the exact same tone-mapping but also adds som RGB film grain.

If you look at the shadows and the highlights you can notice that there is a bit more detail visible in the film-grain version (e.g. count the number of visible beams in the glass ceiling).

This is just a quick test, I tweaked the film grain actually to be less intense in the midtones (around 0.5) than near the extremes (0 and 1) to be able to push it a bit further without being too intense over the entire image. It can certainly be done in much better ways, but as far as silly experiments go, I'm rather happy.

If you really wanted to be cheating, you could even just add grain in the shadows, which would definitely be a hack as you're adding energy but hey... it's not that we don't routinely do that (e.g. bloom/veil usually doesn't redistribute energy, it just adds it...)

P.s.

[real film grain](http://cool.conservation-us.org/coolaic/sg/emg/library/pdf/vitale/2007-04-vitale-filmgrain_resolution.pdf)is actually not easy to emulate (and I'm not trying to, here). This is the only

[attempt I know of](http://www.dctsystems.co.uk/Text/Grain2.pdf).

## No comments:

Post a Comment