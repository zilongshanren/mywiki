---
title: Non-Square OGSSAA+FXAA
url: http://hacksoflife.blogspot.com/2012/10/non-square-ogssaafxaa.html
author: Benjamin Supnik
published: '2012-10-31'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I just finished integrating FXAA 3.11 into X-Plane 10; we were using an older FXAA implementation. Timothy Lottes pointed me at the right way to combine OGSSAA and FXAA: run the FXAA sampler in SSAA space and mix down its results on the fly. Conveniently our pipeline was pretty much ready to do this.


I've been looking for an option for OGSSAA other than 4x. One idea would be to use 1.4x1.4 scaling for 2x total fill rate costs, blurry box filtering be damned, but FXAA really needs to know where the individual pixels are.


X-Plane's main problem is temporal anti-aliasing, and most of the anti-aliasing is vertical - that is, there are a lot of long thin horizontal features in the background (roofs of buildings, roads, etc.) that are responsible for the most annoying artifacts.


So I tried an experiment: non-square OGSSAA with FXAA. And...it pretty much works. I'm sure someone has done this before, and frankly I don't have the greatest eye for anti-aliasing, but the extra vertical res really improves image stability.


Secret decoder ring to the images: images with "FX" in the name (or use_post_aa=2) in the caption have FXAA applied. The 2x/4x/8x applies to the OGSSAA sample count; the grid is shown in the pixels. 2x OGSSAA is 1x2, 4x is 2x2, and 8x is 2x4.


The pictures really don't do justice to the improvement that 2x4 gives the image in terms of temporal stability. Having 4x the vertical samples for those thin roofs makes a big difference.



































I've been looking for an option for OGSSAA other than 4x. One idea would be to use 1.4x1.4 scaling for 2x total fill rate costs, blurry box filtering be damned, but FXAA really needs to know where the individual pixels are.

X-Plane's main problem is temporal anti-aliasing, and most of the anti-aliasing is vertical - that is, there are a lot of long thin horizontal features in the background (roofs of buildings, roads, etc.) that are responsible for the most annoying artifacts.

So I tried an experiment: non-square OGSSAA with FXAA. And...it pretty much works. I'm sure someone has done this before, and frankly I don't have the greatest eye for anti-aliasing, but the extra vertical res really improves image stability.

Secret decoder ring to the images: images with "FX" in the name (or use_post_aa=2) in the caption have FXAA applied. The 2x/4x/8x applies to the OGSSAA sample count; the grid is shown in the pixels. 2x OGSSAA is 1x2, 4x is 2x2, and 8x is 2x4.

The pictures really don't do justice to the improvement that 2x4 gives the image in terms of temporal stability. Having 4x the vertical samples for those thin roofs makes a big difference.

## No comments:

## Post a Comment