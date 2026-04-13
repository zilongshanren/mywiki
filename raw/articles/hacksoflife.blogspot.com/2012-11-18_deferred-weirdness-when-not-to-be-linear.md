---
title: 'Deferred Weirdness: When Not to be Linear'
url: http://hacksoflife.blogspot.com/2012/11/deferred-weirdness-when-not-to-be-linear.html
author: Benjamin Supnik
published: '2012-11-18'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

In my previous post, I described X-Plane 10's multipass scheme for deferred rendering. Because we need to simultaneously operate in two depth domains with both deferred and forward rendered elements, the multi-pass approach gets very complicated, and much stenciling ensues.


But the real wrench in the machinery is sRGB blending. It was such a pain in the ass to get right that I can safely say it wouldn't be in the product if there was



In the sRGB world you mix


Linear color spaces refer to color spaces where the amount of photons or physical-whatever-thingies are linear. Double the RGB and you get twice as many photons. Linear spaces do not look "linear" to humans, see above about dark and dogs.


In linear space if you mix



There are two cases where we found we just absolutely had to be linear:


In both cases, linear addition of light gives us something really important: adding more light doesn't double the perceived brightness. (Try it: go into a room, turn on one light, then a second. Does the room's brightness appear to double? No!) For billboards, if a bunch of billboards "pile up" having the perceptual brightness curve taper off is a big win.But the real wrench in the machinery is sRGB blending. It was such a pain in the ass to get right that I can safely say it wouldn't be in the product if there was

*any*way to cheat around it with art.#### Color Space Blending

First: when I say "sRGB" blending, what I mean is: blending two colors in the sRGB color space. sRGB is a vaguely perceptual color space, meaning equi-distant numeric pixel values appear about equi-distant in brightness - if you saw a color ramp, it would look "even" to you. It's not! The sRGB stripe looks even to humans because we have increased visual sensitivity in the darker brightness ranges. (If we didn't, how could we stumble for the light switch and trip over the dog at night?)In the sRGB world you mix

**red**(255,0,0) and**green**(0,255,0) and get "**puke**" (128,128,0).Linear color spaces refer to color spaces where the amount of photons or physical-whatever-thingies are linear. Double the RGB and you get twice as many photons. Linear spaces do not look "linear" to humans, see above about dark and dogs.

In linear space if you mix

**red**(255,0,0) and**green**(0,255,0) you get**yellow**(186,186,0 if we translate back to sRGB space).#### When to Be Linear

There are two cases where we found we just absolutely had to be linear:

- When accumulating light from deferred lights, the addition must be linear. Linear accumulated lights look realistic, sRGB accumulated lights look way too stark with no ambiance.
- When accumulating light billboards, it turns out that linear also looks correct, and sRGB additive blending screws up the halos drawn into the billboards.

#### When to Be sRGB

The above "linear" blending cases are all additive. Positive numbers in the framebuffer represent light, adding to them "makes more light", and we want to add some kind of linear unit for physically correct lighting.But for more conventional "blending" (e.g. adding light on top takes away light underneath) linear isn't always good.

Traditional alpha blending is an easy for artists to create effects that would be too complex to simulate directly on the GPU. For example, the windows of an airplane are a witches brew of specularity, reflection, refraction, absorbtion, and the BDRF changes based on the amount of grime on the various parts of the glass. Or you can just let your artist make a translucent texture and blend it.

But this 'photo composited' style blending that provides such a useful way to simulate effects also requires sRGB blending, not linear blending. When an 'overlay' texture is blended linear the results are too bright, and it is hard to tell which layer is "on top". The effect looks a little bit like variable transparency with brightness, but the amount of the effect depends on the background. It's not what the art guys want.

#### Alpha When You Least Expect It

Besides the usual sources of "blended" alpha (blended meaning the background is darkened by the opacity of the foreground) - smoke particles, clouds, glass windows, and light billboards - X-Plane picks up another source of alpha: 3-d objects alpha fade with distance. This is hugely problematic because it requires the alpha blending you get when you put alpha through the deferred renderer to be not-totally-broken; we can't just exclude

*all*3-d from the deferred render.

I mention this now because we have to ask the question: what blending mode are we trying to get

*in*the deferred renderer (to the extent that we have any control over such things)? The answer here is again sRGB blending.

#### Faking Alpha in a GBuffer

Can we fake alpha in our deferred renderer? Sort of. We can choose to blend (or not blend) various layers of the G Buffer by writing different alphas to each fragment data component; we can gain more flexibility by using pre-multiplied alpha, which lets us run half the blending equation in shader (and thus gives us separate coefficients for foreground and background if desired.

Fake alpha in a GBuffer has real problems. We only get one 'sample' per G-Buffer, so instead of getting the blend of the lighting equation applied to a number of points in space, we get a single lighting equation applied to the blend of all of the properties of that point. But blending is better than nothing. We blend our emissive and albedo channels, our specular level, our AO, and our normal. (Our normal map is

[Lambertian Azimuth equal area](http://aras-p.info/texts/CompactNormalStorage.html)and it blends tolerably if you set your bar low.)

The only channel we don't blend for our blended fragments is eye position Z; even the slightest change to position reconstruction causes shadow maps to alias and fail - hell, shadow maps barely work on a good day.

The G-Buffer blending is all in sRGB - the albedo and emissive layers are 8-bit sRGB encoded.

#### Adding It All Up

The emission and albedo layers of the G-Buffer must be added in sRGB space. This is not ideal (because emission layers contain light) but it is necessary. Consider two layers of polygons being drawn into a G-Buffer. The bottom is heavy on albedo, the top heavy on emissive texture. As we "cross-fade" them with alpha, we are actually darkening the albedo and lightening the emission layer - two separate raster ops into two separate images. This only produces a correct sRGB blend if we know that the two layers will later be added together in sRGB. In other words:

blend(A_alb+A_lit,B_alb+B_lit,alpha)is only equal to

blend(A_alb,B_alb,alpha)+blend(A_lit,B_lit,alpha)if the blending and addition all happen in the same color space. The top equation is how "blended" geometry work in a forward renderer (albedo and emissive light summed in shader before being blended into the framebuffer) and the bottom equation is how a deferred renderer looks (blending done per layer and the light addition done later on the finished blend).

Once we add and blend in sRGB space in our deferred renderer a bunch of things do work 'right':

- Alpha textures that can't be excluded from the deferred renderer that need sRGB blending work, as do alpha fades with distance.
- We can mix & match our emissive and albedo channels the way we would in a forward renderer and not be surprised.
- Additive light from spills is still linear, since it is a separate accumulation into the HDR framebuffer.

- We cannot draw linear additive-blended "stuff" into the deferred renderer.

I will try to summarize this mess in another post.

## No comments:

## Post a Comment