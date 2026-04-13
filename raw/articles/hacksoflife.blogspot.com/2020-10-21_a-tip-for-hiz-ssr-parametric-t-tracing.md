---
title: A Tip for HiZ SSR - Parametric 't' Tracing
url: http://hacksoflife.blogspot.com/2020/10/a-tip-for-hiz-ssr-parametric-t-tracing.html
author: Benjamin Supnik
published: '2020-10-21'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

HiZ tracing for screen space reflections is an optimization where the search is done using a hierarchial Z-Buffer (typically stashed in a mip-chain) - the search can take larger skips when the low-res Z buffer indicates that there could not possibly be an occluder. This changes each trace from O(N) to O(logN).

The technique was published in [GPU Pro 5](https://www.amazon.com/GPU-Pro-Advanced-Rendering-Techniques/dp/1482208636), but as best I can tell, the author found out after writing the article that he couldn't post working sample code. The result is a tough chapter to make heads or tales of, because some parts of the algorithm simply say "see the sample code". This [forum thread](https://www.gamedev.net/forums/topic/658702-help-with-gpu-pro-5-hi-z-screen-space-reflections/) is actually pretty useful, as is [this](https://www.jpgrenier.org/ssr.html).

The article builds a ray that is described parametrically in "Z" space, starting at the near clip plane (0.0 screen-space Z, must be a DX programmer ;-) and going out to 1.0.

If your app runs using reverse-float Z and you reverse this (starting the march at 1 and going in the -Z direction), you're going to get a ton of precision artifacts. The reason: our march has the lowest precision at the start of the march. In reverse-float Z there's a lot of hyper-Z (screen-space) depth "wasted" around the near clip plane - that's okay because it's the 'good' part of our float range, which gets better with distance. But in our case, it's going to make our ray testing a mess.

The technique is also presented tracing only near occluders and tracing only away from the camera - this is good if you view a far away mountain off a lake but not good if you view a building through a puddle from nearly straight down.

As it turns out, *all* of these techniques can be addressed with one restructure: *parametrically *tracing the ray using a parametric variable "t" instead of the actual Z buffer.

In this modification, the beginning of the ray cast is always at t = 0.0, and the end of the ray-cast (a full Z unit away) is always at t = 1.0, regardless of whether that is in the positive or negative Z direction - our unit is normalized so that its Z magnitude is either +1.0 or -1.0, which saves us a divide when intersecting with Z planes.

What does this solve? A few things:

- The algorithm has high precision at the beginning of the trace because t has small magnitude - we want this for accurate tracing of close occluders and odd angles.
- The algorithm is fully general whether the ray is cast toward or away from the camera - no conditional code inside the search loop. Lower 't' is always "sooner" in the ray cast.
- We can now march
*around*an occluder if we can attribute a min and max depth to it, by seeing if the*range*of t within a search cell overlaps the*range*of t in our min-max Z buffer. This is fully general for "in front" and "behind" a cast and for "toward" and "away".

## No comments:

## Post a Comment