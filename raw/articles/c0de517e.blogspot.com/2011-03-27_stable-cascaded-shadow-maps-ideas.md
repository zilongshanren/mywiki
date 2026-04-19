---
title: Stable Cascaded Shadow Maps - Ideas
url: https://c0de517e.blogspot.com/2011/03/stable-cascaded-shadow-maps-ideas.html
published: '2011-03-27'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

**Stable CSM intro**

A "stable" cascade is nothing else than a fixed projection of your entire world on a giant texture, of which we render a fixed window that fits around the projection of view frustum each frame, making sure that we always slide this fixed window by an integral number of texels each frame.

As we have to be sure that the "window" will fit the frustum in all cases, to determine its size a way is to fit the frustum in a sphere and then size the window using the radius of such sphere.

Implementing CSM, especially on consoles is not that easy. For an open world game you'll notice that you need quite a lot of resolution to get decent results, and cascade rendering can become quickly a problem. On 360 from what I've seen, resolving big shadowmaps from EDRAM to the shared memory is very expensive too, so it becomes important to pack the shadowmaps aggressively. Some random "good" ideas are:

- Render shadows to a deferred shadow buffer, enabling the possibility of rendering one cascade at a time. It also makes way easier to cross-fade cascades and possible rendering shadows at half-res (that is a good idea... upsampling with bilateral filtering or similar). It's possible to use hi-stencil and hi-z (on ps3, also depth range) in various ways to accelerate this.
- Tune cascade shadow filtering to try to match filter size across different resolutions (that's to say, filter less far cascades).
- Shadow a pixel using the best cascade that contains that pixel, instead of relying of the frustum split planes (this makes a bit harder to fade between cascades, but not too much). Use scissors or clipping planes to avoid rendering stuff that is already rendered in previous cascades into more coarse ones. Microsoft has a pair of
[nice](http://msdn.microsoft.com/en-us/library/ee416307(v=vs.85).aspx)[articles](http://msdn.microsoft.com/en-us/library/ee416324(v=vs.85).aspx).

- Compute light near-far planes to be tight around the frustum but avoid culling objects before the near plane (a.k.a. "pancake": clamp depth in the vertex shader, it's not a big deal as the projection is orthographic but it can screw self shadowing of such clipped objects, you need to give a bit of "buffer" space to the near plane). The downside is that you get more raster pressure as the hi-z will not reject the objects that are compressed on the near plane... you can solve that either by giving a small linear range for the pancaked objects or marking and using stencil/hi-stencil where they get drawn.
- Cull small objects aggressively from distant cascades. Avoid rendering objects in far cascades if they were rendered completely in the previous ones.

- Pack shadowmaps! Do not render things behind the frustum and maximize the area in front of it!
[This](http://the-witness.net/news/?p=113)and[this](http://sebastiansylvan.wordpress.com/2010/04/24/improving-shadow-map-utilization-for-cascaded-shadow-maps/)articles have some good ideas. You can also pack two shadowmaps into a two-channel 16-bit target if double-depth fill is not giving you a big speedup.

**Crysis**

I'm playing Crysis 2. Nice game, starts a bit weak with a too forced story but it improves A LOT later on. Graphically is great as I'm sure you've all noticed, ok long story short, I still probably love Modern Warfare and Red Dead a bit more but it does not disappoint. Somewhat the art direction on Crysis 2 looks a bit "hyperrealistic" to me most of the times with very soft and exaggerated ambient fill, even more accentuated by the huge bloom. But well, technically is impressive and it is surely a good game.

Now of course if you're a rendering engineer, first thing you do with such a game is to walk slowly everywhere and check out the rendering techniques. And so did I. Some notes:

- Lods pop noticeably, small objects are faded out pretty aggressively. Still during "normal" gameplay it's not too evident.
- DOF is pretty smart. It seems to filter with a "ring" pattern that I guess is both an optimization and a way to simulate bokeh. It looks like what you get from a catadioptric mirror lens, but it's reasonable also because most lenses will have a sharp out of focus either before of after the focal plane, as the bokeh shape of one is the inverse of the other (so if a lens has a nice gaussian-like out of focus after the focal plane, it will get an harsh negative-gaussian one before). It also manages to blur correctly objects before the focal plane, kudos for that.
- Huge screenspace bloom/lens flares.
- Motion blur (camera only?)
- Decent post-filtering AA, even if with some defects (ghosting of objects in motion), not the best I've seen but good.
- Shadows. Stable CSM. A weird circular filter is applied to them. No fading between cascades. A dithering pattern that seems to be linked to the light space.
**Far cascades are updated every other frame.**

Ok. So the last item caught my attention. How to do that? Well, it's not that hard if you think about it. If you observe the update of the CSM, you'll notice that even when you rotate the view your far cascades move only by a few texels, so we could just add a bit of space there and assume that updating these cascaded every other frame won't create problems.

**Caching**

But what if we want to be accurate? Well it turns out it's not really hard at all! We know what is the window we rendered last frame, and where we should render this frame. Most of the new frame is already rendered in the last one, we could just shift the data in the right place.

It turns out, we don't even need that, if we want to apply this incremental update only once and then re-render, we can just shift our "zero" of the shadowmap uv and wrap. We still need to render the new data and resolve it, but that is only a few texels wide border! Even culling the objects to render only the ones that fall in that border is really trivial.

Really, we could do an incremental update for every cascade... forever! If it wasn't for two things: moving objects and the fact that we can't fix our cascade (light) near/far z, but we usually to maximize the resolution need to fit it each frame (or so).

We could alleviate the latter problem by having the "shifting" shader also re-range the "cached" last frame data into the new near/far range. The moving objects one can be solved by having them rendered into a separate buffer or a copy of the buffer. Both solutions though need more memory and bandwidth (resolve time on 360) so they can be good only if that is not already a major bottleneck (that's to say, if you packed your cascaded well).

## 8 comments:

Just a quick comment, the following is an invalid optimization:



"Avoid rendering objects in far cascades if they were rendered completely in the previous ones."

In the situation where you look in the direction of the lightvec, objects rendered into near cascades will cast shadows into the far cascades, and are thus needed for all cascades.

mg: no it's ok if you render the shadows using the "best" cascade and not the split planes, as suggested.

That is true assuming earlier cascades' far plane extend past the entire frustum, not just their "slice".


If you do put the far plane at the end of the slice then you could indeed have objects entirely in slice 0 cast shadows into slice 1.

If I understand the specific problem being discussed here, the "use the highest map" heuristic makes the implicit assumption that you are (in light space) culling shadows to the full bounds of entire split's "shadow map", not to the bounds of the "eye-frustum slice" (which is a subset of the map).





That is, it assumes that every single pixel of the split shadow map is defined and valid.

What that implies is that sometimes you cull in and draw a boatload of extra junk into your split's shadow map (inside the map, but outside the eye-frustum split, projected into light space) that you usually don't ever need, which costs you perf.

The alternative is that you tightly cull to the bounds of your eye-frustum split projected into light space, which avoids rendering all this extra junk. And you don't use this "use the highest map" optimization, but rather select maps purely based on frustum split distances.

Of course in either case, you back off your light-space near plane forward toward the light than the closest eye-frustum split vertex (projected into light space) so that you can grab out-of-frustum shadow casters that cast into the view frustum.

Dark Helmet - yes and no. You can still cull each cascade using the extruded frustum planes of the split, you just exclude the far plane. Also if you avoid rendering objects that were fully included in a given cascade in lower-res ones, overall you can get some savings. But it's true that it's a tricky thing to balance, I don't think I know the "perfect" solution or can prove a given strategy is always better.

Ah!, thanks. I think I see now. Ignore the eye-space split far plane, and clip by the bounds of the split's shadow map instead.



So in the worst case (light rays orthogonal to view direction), you get a little extra distance coverage in the higher res splits.

And in the best case (light rays parallel to view direction), you end up with everything toward the center of the eye view being in the high-res map regardless of distance, but as you get out toward the edges (in XY) of the same eye view, you step down progressively to the low-res maps.

Look at SDSM Sample Distribution Shadow maps.


What it does basically, is analyzing the content of the ZBuffer with Cuda/OpenCL/DirectCompute) to find optimal (tight) cascade bounds.

It improves resolution greatly, see for yourself...

Post a Comment