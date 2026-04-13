---
title: Look closely
url: http://c0de517e.blogspot.com/2015/03/look-closely.html
published: '2015-03-21'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The BRDF models surface roughness at a frequency bigger than wavelength, but smaller than observation scale.

In practice surfaces have details at many different scales, and we know that the BRDF has to change depending on the observation scale, that is for us the pixel projected footprint onto the surface.

Specular antialiasing of normal maps (

[from Toksvig onwards](https://hal.inria.fr/inria-00589940/document)) which is very popular nowadays models exactly the fact that at a given scale the surface roughness, in this case represented by normal maps, has to be incorporated into the BRDF. The pixel footprint is automatically considered by mipmapping.
Consider now what happens if we look at a specific frequency of surface detail. If we look at it close enough, on an interval of a fraction of the frequency wavelength, the detail it will “disappear” and the surface will look smooth, determined only by the underlying material BRDF and an average normal over such interval.

If we “zoom out” a bit though, at scales circa proportional to the detail wavelength, the surface starts gets complicated. We can’t anymore represent it over such intervals as a single normal, nor it’s easy to capture such detail in a simple BRDF, we’ll need multiple lobes or more complicated expressions.

Zoom out even more and now your observation interval covers many wavelengths, and the surface properties look like they are representable again in a statistical fashion. If you’re lucky it might be in a way that is possible to capture by the same analytic BRDF of the underlying material, with a new choice of parameters. If you are less lucky, it might require a more powerful BRDF model, but still we can reasonably expect to be able to represent the surface in a simple, analytic, statistical fashion. This reasoning by the way, also applies to normalmap specular antialiasing as well...

The question is now, in practice how do surfaces look like? At what scales do they have detail? Are there scales that we don’t consider, that is, that are not something we represent in geometry and normal maps, but that are not either representable with the simple BRDF models we do use?

**- Surfaces sparkle!**

In games nowadays, we easily look at pixel footprints of a square millimetre or so, for example that is roughly the footprint on a character’s face when seen in a foreground full body shot, in full HD resolution.

If you look around many real world surfaces, over an integration area of a square millimetre or so, a lot of materials “sparkle”, they have either multiple BRDF lobes or very “noisy” BRDF lobes.

If you look closely at most surfaces, they won’t have smooth, clear, smooth specular highlights. Noise is everywhere, often "by design" e.g. with most formica countertops, and sometimes "naturally" even in plants, soft plastics, leather and

[skin](http://gl.ict.usc.edu/Research/Microgeometry/)[notably](http://www.iryoku.com/stare-into-the-future).
Some surfaces have stronger spikes in certain directions and definitely “sparkle” visibly, even at scales we

[render](http://dl.acm.org/citation.cfm?id=2601097.2601155)[today](http://dl.acm.org/citation.cfm?id=2601097.2601186). Road asphalt is an easy and common example.
There are surfaces that have roughness at a frequency that is high enough to be represented always by a simple BRDF, but many are not. Some hard plastics (if not textured), glass, glazed ceramic, paper, some smooth paints.

*Note: Eyes can be deceptive in this kind of investigation, for example Apple’s aluminum on a macbook or iphone looks “sparkly” in real life, but its surface roughness is probably too small to matter at the scales we render.*

*This opens another can or worm that I won’t discuss, of what to do with materials that people “know” should behave in a given way, but that don’t really at the resolutions we can currently render at...*

![]() |



**- Surfaces are anisotropic!**

Anisotropy is much more frequent than one might suspect, especially for metals. We tend to think that only “brushed” finishes are really anisotropic, but when you start looking around you notice that many metals shows anisotropy, due to the methods used to shape them.

Similar artifacts are sometimes found also in plastics (especially soft or laminated) or paints.

![]() |

On the right: the metal cylinder looks isotropic, but close up reveals some structure

**- Surfaces aren’t uniform!**

At a higher scale, if you have to bet how any surface looks at the resolutions we author specular roughness maps, it will always somewhat be non-uniform pixel to pixel.

You can imagine how if it’s true that many surfaces have roughness at frequencies that would require complex, multi-lobe BRDFs to render at our current resolutions, how it is even more likely that our BRDFs won’t ever have the exact same behaviour pixel to pixel.

Another way of thinking of the effects of using simpler BRDFs driven by uniform parameters is that we are losing resolution. We are using a surface representation that is probably reasonable at some larger scale, per pixel at a scale at which it doesn’t apply. So it’s somewhat similar to doing to right thing with wrong, “oversized” pixel footprints. In other words, over-blurring.

**- Surfaces aren’t flat!**

Flat surfaces aren’t really flat. Or at least it’s rare, if you observe a reflection over smooth surfaces as it “travels” along them, not to notice subtle distortions.

Have you ever noticed the way large glass windows for example reflect? Or ceramic tiles?

This effect is at a much lower frequency of course of the ones described above, but it’s still interesting. Certain things that have to be flat in practice are, to the degree we care about in rendering (mirrors for example), but most others are not.

**- Conclusions**

My current interest in observing surfaces has been sparkled by the fact I’m testing (and have always been interested) hardware solutions for BRDF scanning, thus I needed a number of surface samples to play with, ideally uniform, isotropic, well-behaved. And I found it was really hard to find such materials!

How much does this matter,




Specular highlights are always "broken" via gloss noise,

even on fairly smooth surfaces





**perceptually**, and when? I’m not yet sure. As it's tricky to understand what needs more complex BRDFs and what can be reasonably modeled with rigorous authoring of materials.
|

[Textures from The Order 1886](http://www.polycount.com/forum/showthread.php?t=149706)Specular highlights are always "broken" via gloss noise,

even on fairly smooth surfaces

Some links:

- Also in the article:
[Survey of non-linear prefiltering](https://hal.inria.fr/inria-00589940)[Discrete stochastic microfacet models](http://www.cs.cornell.edu/projects/stochastic-sg14/)(check out the video as well)- Debevec's
[facial microgeometry](http://gl.ict.usc.edu/Research/Microgeometry/)and Jorge's[realtime approximation](http://www.iryoku.com/stare-into-the-future) [Rendering glints on high-resolution normal-mapped specular surfaces](http://www.mitsuba-renderer.org/~wenzel/papers/glints-sg14.pdf)- Further links:

## 1 comment:

Yes, both are indeed linked already in the article, even if such links might not be very apparent I realize

Post a Comment