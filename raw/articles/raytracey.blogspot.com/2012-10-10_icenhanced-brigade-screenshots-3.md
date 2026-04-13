---
title: iCEnhanced Brigade screenshots (3)
url: http://raytracey.blogspot.com/2012/10/real-time-photorealistic-rendering-with.html
author: Sam Lapere
published: '2012-10-10'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

With some of the optimizations that we're working on right now, the real-time path tracing technology provided by Brigade will make this kind of realism a reality in games very soon. We're on the cusp of having truly photorealistic, cinema quality games!

## 6 comments:

Um... Does the human model have subsurface scattering?

Looks fricking amazing, good work dude!

I may be wrong, but it looks like there is a small error/significant rounding error in your triangle intersection code. If you look at the photo of the wine glass you can just make out the lines where the polygons meet - faint lines where the refraction only occurs on one of the side of the glass. It may be a model issue, but looks unusual.




BTW. is this Octane render PT with AO or is it full blown PT with colour bleeding? On a side note, Octane looks faster than Brigade for AO PT (if that is what it is)...doesn't make this Brigade redundant given the greater amount of features that Octane supports (unless of course Brigade is offered cheaper)? Maybe a side-by-side comparison of Octane and Brigade would make sense here?

Just a quick note, I do think bloom and lens flare add something to a final render, but please be careful not adding too much bloom etc. I think in the last pic from Backstreets of Asia that it is overused. In the end it actually detracts and can mask the subtle realism PT offers over rasterisation-based techniques.

Nice work though

"Just a quick note, I do think bloom and lens flare add something to a final render, but please be careful not adding too much bloom etc. I think in the last pic from Backstreets of Asia that it is overused. In the end it actually detracts and can mask the subtle realism PT offers over rasterisation-based techniques.


"

I agree.

I totally agree with the bloom stuff and the lens flare etc. etc. Those are not effects seen by the human eye, just side-effects of cameras, thus they should only be optional. The reason they are used in realtime PT demos I believe is to smooth out some of the noise.






@Antzrhere: if it has AO ( ambient occlusion ) then it's not real PT. AO is just an approximation of GI.

AFAIR octane is mostly an offline renderer ( meaning not for games ) while brigade is targeted to games.

@mirror. AO may not be real GI, but the technique of PT can still be used for simulating soft reflections and camera aperture/lens distortion/DOF alongside AO without requiring full unbiased GI. As such not all PT is equal but is different to whitted RT.

Post a Comment