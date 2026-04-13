---
title: 'Deferred Lighting: Stenciling is not a Win'
url: http://hacksoflife.blogspot.com/2012/11/deferred-lighting-stenciling-is-not-win.html
author: Benjamin Supnik
published: '2012-11-16'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've been meaning to write up a summary of the changes I made to X-Plane's deferred rendering pipeline for X-Plane 10.10, but each time I go to write up an epic mega-post, I lose steam and end up with another half-written draft, with no clue about what I meant to say. So in the next few posts I'll try to cover the issues a little bit at a time.


One other note from the pipeline work we did: using the stencil buffer to reject screen space for deferred lights is not a win in X-Plane.


The technique is documented quite a bit in the deferred rendering powerpoints and PDFs. Basically when drawing your deferred lights you:


The stenciling logic is exactly the same as stencil-shadow volumes, and the result is that only pixels that are within the light volume are lit; screen space both in front and behind the volume are both rejected.One other note from the pipeline work we did: using the stencil buffer to reject screen space for deferred lights is not a win in X-Plane.

The technique is documented quite a bit in the deferred rendering powerpoints and PDFs. Basically when drawing your deferred lights you:

- Use real 3-d volumetric shapes like pyramids and cubes to bound the lights.
- Use two-sided stenciling to mark only the area where there is content
*within*the light volume. A second pass over the volume then fills only this area.

For X-Plane, it's not worth it. YMMV, but in the case of X-Plane, the cost of (1) using a lot more vertices per light volume and (2) doing two passes over the light volume far outweigh the saved screen space.

For a few very pathological cases, stenciling is a win, but I really found myself having to put the camera in ridiculous place with ridiculously lopsided rendering settings to see a stencil win, even on an older GPU. (I have a Radeon 4870 in my Mac - and if it's not a win there, it's not a win on a GeForce 680. :-)

The cost of volumes is even worse for dynamic lights - our car headlights all cast spill and the light volume transform is per-frame on the CPU. Again, increasing vertex count isn't worth it.

For 10.10 we turned off the stencil optimization, cutting the vertex throughput of lights from two passes to one.

For a future version will probably switch from volumes to screen-space quads, for a nice big vertex-count win.

Finally, I have looked at using instancing to push light volumes/quads for dynamic objects. In the case of our cars, we have a relatively small set of cars whose lights are transformed a large number of times. We could cut eight vertices (two quads per car) down to a single 3x4 affine transform matrix.

Again, YMMV; X-Plane is a very geometry-heavy title with relatively stupid shaders. If there's one lesson, it's this: it is a huge win to keep instrumentation code in place. In our case, we had the option to toggle stenciling and view performance (and the effect on our stat counters at any time.

Interesting result! I guess most presentations have been targeted at consoles, and for newer hardware, compute/tile-based methods have been in focus. Are you using projected textures and shadow-mapping for the lights? That might add to the pixel-cost and bias towards reducing pixels touched.


ReplyDeleteI don't quite understand the two causes you give for stenciling not helping. Why is more vertices a problem - are they regenerated/uploaded per frame? And what are you comparing to that has less vertices, if screenspace quads are not yet implemented? The two drawcalls, and additional state-setting obviously has a performance-impact. If gl had access to create command-buffers (*cough* displaylists) this would be an obvious use-case.

We don't do shadows on our spill lights yet, which does help make them cheap. It is quite possible that for a shadowed light stencil will be a win. But the number of shadowed lights will be small, so stenciling there will not be a big cost if we go back to that approach...


DeleteSome vertices are regenerated/uploaded per frame. Even the ones that are not are still in batches that must be multiply emitted, and refound in the scene graph or the cull must now be cached in temoprary memory. The state impact could be minimized with careful code _if_ there was a win here, but with no fps win it didn't seem worth poking at, and the total vertex count for the streaming case is always going to cost more.

Unless your lights are all quite big, I do't see how stencil can ever be bad. The number of vertices to process in the vertex shader is irrelevant usually and you use LODs only if you use geometry for the actual light rendering pass, but not to limit vertex overhead but to avoid wasting quads along triangle edges. Optimizing deferred is a pain as there are many slight variations and if your number of lights is high, savings do matter. Also, hiz and histencil details are different from card to card especially when going back to more legacy devices. Overall though I'm really surprised you found stenciling to be in general bad.

ReplyDeleteI was surprised to find it too - but we're not the only game in this bucket - you'll find a mix of results in various presentations.






ReplyDeleteThe stenciling itself does not appear to be bad, but what can cost is:

- Total vertex count - particularly for _streaming_ vertices, where we're burning CPU (to push the stream) and bus bandwidth (to transfer the stream) - going to screen-space is a big bandwidth reduction in a bandwidth-constricted title.

- The GPU, when multi-passing streamed lights, has to either draw from AGP twice (bandwidth fail) or save some VRAM (VRAM pressure) - it's not free, although the VRAM cache case shouldn't be painful.

- Finally, it is more batches to draw the lights twice.

In other words, there's no way pre-stencil doesn't cost you some CPU. The CPU may or may not be huge depending on implementation details, but it's not zero, so if we're not bottlenecked on light volume fill, it's not a win.

It might be worth noting that (1) our artists have been pretty careful about light overlap - it's possible that third party content will get more aggressive and in those cases stencil would have been a win and (2) we tend to have a _lot_ of _small_ lights - tens of thousands of street lights, all casting only a few pixels. The workload may not be usual compared to FPS and racing games.

I did have one other idea to try: only stencil lights that are near the camera, e.g. as we walk the scene graph have special handling for the near quad-tree bucket. Because most of our lights are not huge in world-space, only the close buckets have any chance of generating really huge amounts of fill.

But given the complexity of our stencil buffer use (see g-buffer posts) it's not on my short list of fun things to do...the 'next' optimization is to go strictly to screen space and get our streaming vertex count down. :-)