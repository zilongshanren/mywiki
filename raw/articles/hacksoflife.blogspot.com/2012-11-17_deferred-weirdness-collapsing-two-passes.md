---
title: 'Deferred Weirdness: Collapsing Two Passes'
url: http://hacksoflife.blogspot.com/2012/11/deferred-weirdness-collapsing-two-passes.html
author: Benjamin Supnik
published: '2012-11-17'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

X-Plane's deferred pipeline changed a lot in our 10.10 patch, into a form that I hope is final for the version run, because I don't want to have to retest it again. We had to fix a few fundamental problems.


Our first problem was to collapse two drawing passes. X-Plane needs more precision than the Z buffer provides. Consider the case where you are in an airplane in high orbit, in your 3-d cockpit. The controls are a lot less than 1 meter away, but the far end of the planet below you might be millions of meters away. With the near and far clip planes so far apart (and the near clip plane so close) there's no way we avoid Z thrash.


X-Plane traditionally solves this with two-pass rendering. Because an airplane cockpit is sealed, we can draw the entire outside world in one coordinate space, blast the depth buffer, and then draw the interior cockpit with reset near/far clip planes. The depth fragments of the cockpit are thus farther than parts of the scenery (in raw hardware depth buffer units) but the depth clear ensures clean ordering.


(This technique breaks down if something from the outside world needs to appear in the cockpit - we do some funny dances as the pilot exits the airplane and walks off around the airport to transition, and you can create rendering errors if you know what to look for and have nothing better to do.)




So when we first put in deferred rendering, we did the quickest thing that came to mind: two full deferred rendering passes.


(Driver writers at NVidia: please stop bashing your heads on your desks - we're trying to


Suffice it to say, two full deferred passes was a bit of a show-stopper; deferred renderers tend to be bandwidth bound, and by consuming



Unfortunately, I didn't find a non-linear Z buffer approach I liked. Logarithmic Z in the vertex shader clips incorrectly, and any Z re-encoding in the fragment shader bypasses early-Z optimizations. X-Plane has some meshes with significant over-draw so losing early Z isn't much fun.



There was a second performance problem that tied into the issue of bandwidth: X-Plane's cloud system is heavy on over-draw and really taxes fill rate and ROPs, and in the initial pipeline it went down into an HDR surface, costing 2x the memory bandwidth. So we needed a solution that would put particle systems into an 8-bit surface if possible.




Our first problem was to collapse two drawing passes. X-Plane needs more precision than the Z buffer provides. Consider the case where you are in an airplane in high orbit, in your 3-d cockpit. The controls are a lot less than 1 meter away, but the far end of the planet below you might be millions of meters away. With the near and far clip planes so far apart (and the near clip plane so close) there's no way we avoid Z thrash.

X-Plane traditionally solves this with two-pass rendering. Because an airplane cockpit is sealed, we can draw the entire outside world in one coordinate space, blast the depth buffer, and then draw the interior cockpit with reset near/far clip planes. The depth fragments of the cockpit are thus farther than parts of the scenery (in raw hardware depth buffer units) but the depth clear ensures clean ordering.

(This technique breaks down if something from the outside world needs to appear in the cockpit - we do some funny dances as the pilot exits the airplane and walks off around the airport to transition, and you can create rendering errors if you know what to look for and have nothing better to do.)

#### The Dumb Way

So when we first put in deferred rendering, we did the quickest thing that came to mind: two full deferred rendering passes.

(Driver writers at NVidia: please stop bashing your heads on your desks - we're trying to

*help*you sell GPUs! :-)Suffice it to say, two full deferred passes was a bit of a show-stopper; deferred renderers tend to be bandwidth bound, and by consuming

*twice*as much of it as a normal, sane game, we were destined to have half the framerates of what our users expected.#### No Z Tricks

Unfortunately, I didn't find a non-linear Z buffer approach I liked. Logarithmic Z in the vertex shader clips incorrectly, and any Z re-encoding in the fragment shader bypasses early-Z optimizations. X-Plane has some meshes with significant over-draw so losing early Z isn't much fun.

#### Particle + HDR = Fail

There was a second performance problem that tied into the issue of bandwidth: X-Plane's cloud system is heavy on over-draw and really taxes fill rate and ROPs, and in the initial pipeline it went down into an HDR surface, costing 2x the memory bandwidth. So we needed a solution that would put particle systems into an 8-bit surface if possible.

#### One Last Chainsaw

One last chainsaw to throw into the mix as we try to juggle them: our engine supports a "post-deferred" pass where alpha, lighting effects, particles, and other G-buffer-unfriendly stuff can live; these effects are forward rendered on top of the fully resolved deferred rendering. We have these effects both outside of the airplane*and*inside the airplane!#### Frankenstein is Born

The resulting pipeline goes something like this:- We have a G-Buffer, HDR buffer, and LDR buffer all of the same size, all sharing a common Z buffer. The G-Buffer stores depth in eye space in half-float meters, which means we can clear the depth buffer and not lose our G-Buffer resolve.
- Our interior and exterior coordinate systems are exactly the same
*except*for the near/far clip planes of the projection matrix. In particular, both the interior and exterior drawing phases are the same in eye space and world space.

- We pre-fill our depth buffer with some simple parts of the cockpit, depth-only,with the depth range set to the near clip plane. This is standard depth pre-fill for speed; because the particle systems in step 4 will be depth tested, this means we can pre-occlude a lot of cloud particles with our cockpit shell.
- We render the outside solid world to the G-Buffer.
- We draw the volumes of our volumetric heat blur effects, stencil only, to "remember" which pixels are actually exposed (because our depth buffer is going to get its ass kicked later).
- We draw the blended post-gbuffer outside world into the LDR buffer, using correct alpha to get an "overlay" ready for later use. (To do this, set the alpha blending to src_alpha,1-src_alpha,1,1-src_alpha.) This drawing phase has to be early to get correct Z testing against the outside world, and has the side effect of getting our outside-world particles into an LDR surface for performance.
- We draw our light billboards to our HDR buffer.
- We clear the depth buffer and draw the inside-cockpit solid world over the G-Buffer. We set stenciling to mark another bit ("inside the cockpit") in this pass.
- We draw the heat markers again, using depth-fail to erase the stencil set, thus 'clipping out' heat blur around the solid interior. This gets us a heat blur stencil mask for later that is correct for both depth buffers. (Essentially we have used two stenciling paths to 'combine' two depth tests on two depth buffers that were never available at the same time.)
- We go back to our HDR buffer and blit a big black quad where the stencil marks us as "in-cockpit". This masks out exterior light billboards from step 5 that should have been over-drawn by the solid cockpit (that went into the G-Buffer). This could be done better with MRT, but would add a lot of complexity to already-complex configurable shaders.
- We "mix down" our G-Buffer to our HDR buffer. Since this is additive, light billboards add up the way we want, in linear space.
- We draw another stenciled black quad on our LDR buffer to mask out the particles from step 4.
- Finally, we render in-cockpit particles and lights directly into the LDR buffer.

A few observations on the beast:

- That's a lot of MRT changes, which is by far the weakest aspect of the design. We don't ever have to multi-pass over any surface except the depth buffer, but we're still jumping around a lot.
- The actual number of pixels filled is pretty tame.
- Night lighting is
*really*sensitive to color space, and we picked up a few steps by insisting that we be in exactly the right color space at all times. Often the difference between a good and bad looking light is in the 0-5 range of 8-bit RGB values! When lights are rendered to a layer and that layer is blended, we have to be blending in linear color space*both*when we draw our lights*and*when we composite the layer later!

Have you considered to use a Floating Point Depth Buffer (with reversed z trick). It is fine in our case where view distances are up to 100 km. However it is said that it's insufficient for a planet system renderer.


ReplyDeletehttp://outerra.blogspot.com/2009/12/floating-point-depth-buffer.html

Not carefully - we use 24/8 depth-stencil. I need to investigate whether separating out stencil is hardware supported for FBOs and how similar the performance is. Log depth definitely had the precision we need; I'll have to look at inverse-floating point more carefully...

ReplyDeleteReverse FP actually has a slightly better precision than a 24bit logarithmic depth buffer, when set up properly. But apart from the potential issue with increased GPU memory/bandwidth when using stencil, there's also purely OpenGL-specific problem with setting up the reverse FP depth buffer on AMD/ATI and perhaps Intel too. I'm preparing a larger blog post about it all, while also nagging AMD OpenGL devs about a way to resolve it. Which should be possible since it works in DirectX on their HW ...

ReplyDeleteon Nvidia there is still a problem as well.

DeleteglDepthRange clamps its parameters even if the spec (4.2+) states the opposite. Have checked 306.97 and 306.63-beta drivers, but still no luck. Forced to use glDepthRangedNV.

I have received a reply from AMD guys that the spec change is kind of formal - in 4.2+ it was changed from clamp-on-specification to clamp-on-use model. Besides, I was told AMD HW simply does not support arbitrary clamp values, so it won't work regardless. But here we don't need arbitrary ones, just an ability to enable the DirectX clamping mode, which I believe must work.

Delete