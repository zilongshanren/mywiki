---
title: Specular Hilites Have Their Own Depth
url: http://hacksoflife.blogspot.com/2020/04/specular-hilites-have-their-own-depth.html
author: Benjamin Supnik
published: '2020-04-16'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I just noticed this effect while I was brushing my teeth. The faucet in the sink is:




And...then I noticed that they didn't have the same parallax. Close one eye, then the other, and the


In other words, the specular hilites are


If you take a step back and think about this, it's completely logical. An image of yourself a mirror appears twice as far away as the mirror itself, and if you draw an optical diagram, this is not surprising. Twice as much eye separation parallax is 'washed out' by distance on the full optical path as to the surface of the mirror.


Interestingly, X-Plane's VR system correctly simulates this. We do per-pixel lighting calculations separately on each eye using a camera origin (and thus transform stack and light vector) specific to each eye. When I first coded this, I thought it was odd that the lighting could be "inconsistent" between eyes, but it never looked bad or wrong.


Now I realized that that inconsistency is literally a depth queue.




- Chrome (or stainless steel) or some other reflective "metal" and
- Reasonably glossy and
- Kinda dirty.

And...then I noticed that they didn't have the same parallax. Close one eye, then the other, and the

*relative*placement of the specular hilites with regards to the calcium deposits changes.In other words, the specular hilites are

*farther away*than the surface they reflect in.If you take a step back and think about this, it's completely logical. An image of yourself a mirror appears twice as far away as the mirror itself, and if you draw an optical diagram, this is not surprising. Twice as much eye separation parallax is 'washed out' by distance on the full optical path as to the surface of the mirror.

Interestingly, X-Plane's VR system correctly simulates this. We do per-pixel lighting calculations separately on each eye using a camera origin (and thus transform stack and light vector) specific to each eye. When I first coded this, I thought it was odd that the lighting could be "inconsistent" between eyes, but it never looked bad or wrong.

Now I realized that that inconsistency is literally a depth queue.

## No comments:

## Post a Comment