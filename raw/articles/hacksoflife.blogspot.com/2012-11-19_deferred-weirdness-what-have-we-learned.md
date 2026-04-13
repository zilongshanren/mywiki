---
title: 'Deferred Weirdness: What Have We Learned?'
url: http://hacksoflife.blogspot.com/2012/11/deferred-weirdness-what-have-we-learned.html
author: Benjamin Supnik
published: '2012-11-19'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

To paraphrase the famous Nike Tiger Woods ad, "...and, did you learn anything?"


X-Plane is more of a platform than a game - we support content that comes from third parties, is not updated in synchronization with the engine itself, is sometimes significantly older than the current engine code, and is typically created by authors who have limited or no access to the engine developers.


The easiest, quickest, most efficient way to make deferred rendering work is to set the rules first and customize the content creation process around them. X-Plane's platform status makes this impossible, and most of the nuttiness in our deferred pipeline comes from bending the new engine to work with old content.


We have a number of design problems that are all "difficult" in a deferred engine:


Coping with any one of these problems is quite doable within a deferred renderer, but coping with all three at once becomes quite chaotic. Having to maintain two blending equations (sRGB and linear) is particularly painful.X-Plane is more of a platform than a game - we support content that comes from third parties, is not updated in synchronization with the engine itself, is sometimes significantly older than the current engine code, and is typically created by authors who have limited or no access to the engine developers.

The easiest, quickest, most efficient way to make deferred rendering work is to set the rules first and customize the content creation process around them. X-Plane's platform status makes this impossible, and most of the nuttiness in our deferred pipeline comes from bending the new engine to work with old content.

We have a number of design problems that are all "difficult" in a deferred engine:

- A wide Z buffer range means we need to render twice.
- Content is often permeated with alpha but still needs to be part of a deferred render.
- Some content must be linearly blended, some must be sRGB blended, and there isn't any wiggle room.

(This sits on top of the typical problems of being geometry bound on solid stuff and fill-rate bound on particles.)

So if there's a "learn from our fail"* in this, it might be: try to limit your design problem to only one "rough edge" in the deferred renderer if possible - it's not hard to put a few hacks into a deferred renderer but keeping several of them going at once is juggling.

* I should say: I'm just being snarky with "learn from our fail" - I consider our deferred rendering solution a

*success*in that it provides our users with the benefits of deferred rendering (huge numbers of lights, better geometric complexity, soft particles, and there are other techniques we're just starting to experiment with) while supporting legacy content with very little modification.

The code is under stress because it does a lot, and while it's cute for me as a graphics programmer to go "oh my life would be easier if I could ignore alpha, color space, and go drink margaritas on the beach", the truth is that the code adds a lot of value to the product by provingg a lot of features at once.

I just don't want to have to touch it ever again. :-)

## No comments:

## Post a Comment