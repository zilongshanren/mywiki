---
title: 'Bad ideas don''t require much explanation: Caching Stable Cascaded Shadowmaps'
url: http://c0de517e.blogspot.com/2011/09/bad-ideas-dont-require-much-explanation.html
published: '2011-09-27'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Note:

Ok, some explanation (as I was asked recently about this). The idea is that for static CSM and static objects, you just shift every frame your fixed "window" into an "infinite" plane. So why don't we just do that in the actual CSM? We can shift the old data (or just implicitly shift by wrapping around and keeping an origin marker in the shadowmap coordinates) and just render the tiny strip that corresponds to the part of the window that is novel (corresponding to the intersection between the old clip volume and the new one).

Culling is easy too, it's just a boolean test between the two volumes. The only real issue is that the near-far planes change every frame in a stable CSM, thus the old shadow zbuffer data would be in a different coordinate space than the new one (not only a shift but also a change in the projection matrix).

This can be solved in a number of ways, the worse is to "reinterpret" the old values in the new projection as that loses precision. The best would probably be to write an index in the stencil part and use that index to address an array keeping the last 256 near-far values for the previous frames. 256 values will go pretty fast, so you might need to re-render the entire shadowmap when you're out of them... But really I think there could be stupid tricks to avoid that, like adding some "borders" to the CSM and shifting it every N-texels instead of every single one. Or computing the near-far for volumes that are snapped at shadowmap-sized positions, so every actual shadowmap rendered would at worse interesect four of them, thus requiring a maximum of four stencil indices...

Let me say that again. Our stable CSM shadow is just a fixed-size, shifting window inside a infinite projection plane aligned with our light direction, with a near-far clip that corresponds to the min-max interesection between the projection window and the entire scene. Now we can imagine that we precompute the near-far values (we won't but, let's imagine) in a grid sized as the shadow window. Then, no matter how we shift the window in this infinite plane, it will intersect only four (maxium) near-far precomputed grid cells... Thus, four values in the stencil are all that we need to index cached z-values.

## No comments:

Post a Comment