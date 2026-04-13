---
title: 'Mental note: shadowmap-space filters'
url: http://c0de517e.blogspot.com/2013/12/mental-note-shadowmap-space-filters.html
published: '2013-12-17'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

A thought I often had (and chances are many people did and will) about shadows is that some processing in shadowmap space could help for a variety of effects. This goes from blurring ideas (

[variance shadow maps and variants](http://lousodrome.net/blog/light/2012/01/23/variance-shadow-maps/)) to the idea[of augmenting shadowmaps](http://c0de517e.blogspot.ca/2012/08/service-update-cached-shadowmaps.html)(e.g. with[distance to-nearest-occluder information](http://www.dimension3.sk/2012/08/fractional-disk-soft-shadows/)).
I've always discarded these ideas though (in the back of my mind) because my experience with current-gen told me that often (cascaded) shadowmaps are bandwidth-bound. To a degree that even some caching schemes (

[rendering every other frame](http://c0de517e.blogspot.ca/2011/03/stable-cascaded-shadow-maps-ideas.html), or[tiling a huge virtual shadowmap](http://c0de517e.blogspot.ca/2012/08/service-update-cached-shadowmaps.html)) fail because the cost of re-blitting the cache in the shadowmap can exceed the cost of re-rendering.
So you really don't want to do per-texel processing on them, and it's better instead to work in screenspace, either by splatting shadows in a deferred buffer and blurring, or by doing expensive PCF only in penumbra areas and so on (i.e. with min/max shadowmap mipmaps to compute trivial-in shadow and trivial-out shadow cases and branch).

It seems though that lately caching schemes are becoming practical (probably they are already for some games on current-gen, by no mean my experience on the matter in Space Marines can be representative of all graphic loads).

In these cases it seems logical to evaluate the possibility of moving more and more processing in shadowmap space.




Just a thought.

*Then again, a reminder that a great metaheuristic for graphics is to try to reframe the same problem in a different space (screen, light, UV, local, world... pixel/vertex/object...)*Just a thought.

## No comments:

Post a Comment