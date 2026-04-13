---
title: The Limits of 8-bit Normal Maps
url: http://hacksoflife.blogspot.com/2011/05/limits-of-8-bit-normal-maps.html
author: Benjamin Supnik
published: '2011-05-07'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[something that will go wrong](http://hacksoflife.blogspot.com/2010/12/yet-another-this-is-our-gbuffer-format.html), it's only a matter of time before

[I find it myself](http://hacksoflife.blogspot.com/2011/02/g-buffer-normals-revisited.html). In this case the issue was running out of normal map precision and it was a matter of having an art asset sensitive to normal maps.

Well, our artists keep making newer and weirder art assets, and once again normal maps are problematic. In particular, when you really tighten up specular hilights, the angular precision per pixel of 8-bit normal maps makes it very difficult to create "small" effects without seeing the quantization of the map.

I made this graph to illustrate the problem:

![](../../assets/5bb183522f25d8e6.png)


![](../../assets/5bb183522f25d8e6.png)

So what is this? This equation (assuming I haven't screwed it up) shows the fall-off of specular light levels as a function of the "displacement" of the non-tangent channels of a normal map. Or more literally, for every pixel of red you add to move the normal map off to the right, how much less bright does the normal become?

In this case, our light source is hitting our surface dead on, we're in 8-bit, and I've ignored

[linear lighting](http://hacksoflife.blogspot.com/2010/11/gamma-and-lighting-part-2-working-in.html)(which would make the problems here worse in some cases, better in others). I've also ignored having specularity being "cranked" to HDR levels - since we do this in X-Plane the effects are probably 2x to 3x worse than shown. Units to the right is added dx and dy vectors, and each unit vertically is a loss of brightness value.

Three fall-off curves are shown based on exponents ^128, ^1024, and ^4096. (The steepest and thus most sensitive one is ^4096). You can think of your specular exponent as an "amplifier" that "zooms in" on the very top of the lighting curve, and thus amplifies errors.

So to read this: for the first minimal unit of offset we add to the normal map, we lose about two minimal units of brightness. In other words, even at the top of the curve, with an exponent of ^1024, specular hilights will have a "quantized" look, and a smooth ramp of color is not possible. It gets a lot worse - add that second unit of offset to the normal map and we lose eight units of color!

(By comparison, the more gentle 2^128 specular hilight) isn't as bad - we lose six units of brightness for five of offset, so subtle normal maps might not look too chewed up.)

This configuration could be worse - at least we have higher precision near zero offset. With tangent space normal maps, large areas of near constant normals tend to be not perturbed very much - because if there is a sustained area of the perceived surface being "perpendicular" to the actual 3-d mesh, the author probably should have built the feature in 3-d. (At least, this is true for an engine like X-Plane that doesn't have displacement mapping.)

What can we do?

- Use some form of
[normal map compression](http://sebh-blog.blogspot.com/2010/08/cryteks-best-fit-normals.html)that takes advantage of the full bit-space of RGB. - Throw more bits at the problem, e.g. use RG16. (This isn't much fun if you're using the A and B channels for other effects that only need 8 bits.)
- Use the blue channel as an exponent (effectively turning the normal map into some kind of freaky 8.8 floating point). This is something we're looking at now, so I'll have to post back as to whether it helps. The idea is that we can "recycle" the dynamic range of the RG channels when close to dark using the blue channel as a scalar. This does not provide good normal accuracy for highly perturbed normals; the assumption above is that really good precision is needed most with the least offset.
- Put some kind of global gamma curve on the RG channels. This would intentionally make highly perturbed normals worse to get better results at low perturbations. (I think we're unlikely to productize this, but it might in some cases provide better results using only 16 bits.)
- Tell our artists "don't do that". (They never like hearing that answer.)

How did things go with the exponent approach?

ReplyDelete