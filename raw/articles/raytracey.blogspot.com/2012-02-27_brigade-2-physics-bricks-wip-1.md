---
title: Brigade 2 physics bricks WIP 1
url: http://raytracey.blogspot.com/2012/02/brigade-2-physics-bricks-wip-1.html
author: Sam Lapere
published: '2012-02-27'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I'm currently working on a new Brigade powered physics demo which is inspired by

[http://www.youtube.com/watch?v=bSQoJW9ajmU](http://www.youtube.com/watch?v=bSQoJW9ajmU), an awesome photorealistic physics animation rendered with OpenCL path tracing, which took only 25 seconds per HD frame to render on 2 ATI HD 4890 cards.
Although 25 seconds/frame is already extremely fast for physically based (unbiased) animation rendering, my goal is to render the same physics animation in real-time with the Brigade 2 path tracer on 2 GTX 580s.

Short WIP videos:

[http://www.youtube.com/watch?v=kDXef25LyPo](http://www.youtube.com/watch?v=kDXef25LyPo)

[http://www.youtube.com/watch?v=B-GaDZqnt6I](http://www.youtube.com/watch?v=B-GaDZqnt6I)

There's still some things to do: scale and lighting must be adjusted, the floor should have a different texture with a bump map and some specularity and the orange ball must be made into a physical rigid object, hitting the brick wall. I will also try to implement Voronoi fracture.

## 5 comments:

nice videos, great work.

Do you know if brigade 2 can bake shadow maps ? For highly moving scene like your physics demos it's useless but for some more static scene it could be breat to only resample were something moved.

Nice work. But little correction: AMD/ATI HD4890 is a single GPU card (one RV7xx).

@Ray Tracey,


Is Brigade 2 using bidirectional path tracing?

This may be realtime, but the ghosting takes away all the image quality.

You would be better imho to clear the backbuffer for each frame, and apply a post processing filter on the noisy image to get rid of it, like for example median filtering.

anonymous 1: it can't do baking, but I think you mean light caching. It would indedd be interesting.




anonymous2: thanks, post corrected

anonymous3: no, there's no bidir pt (yet). But it can do multiple importance sampling and qmc sampling.

Jan: thanks, filtering will replace the blurring/ghosting at some point. I implemented the blur myself because it was very straightforward, but implementing an edge aware filter should greatly improve things.

Post a Comment