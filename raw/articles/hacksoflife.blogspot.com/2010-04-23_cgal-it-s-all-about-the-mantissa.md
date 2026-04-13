---
title: 'CGAL: It''s All About the Mantissa'
url: http://hacksoflife.blogspot.com/2010/04/cgal-its-all-about-mantissa.html
author: Benjamin Supnik
published: '2010-04-23'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[no rounding errors](http://hacksoflife.blogspot.com/2009/04/why-cgal.html). It does this by using number types of variable size (using dynamically allocated memory per number!) so that it never runs out of digits. (It also maintains the numerator and denominator of fractions separately to avoid problems with repeating decimals.)

The advantage of this is that geometric algorithms that rely on precise calculations never go haywire due to rounding errors. For example, when using fixed-precision math (e.g. IEEE floats) the intersection of two near-parallel lines will be calculated inaccurately - sometimes with the intersection showing up miles from the original lines. CGAL always has more precision, so it avoids this problem.

But there is one down-side: when you perform a series of intersections, the result is exact numbers whose mantissas (the number of actual digits) have grown very long. And CGAL won't blink about making them even longer as you do more calculations.

Instead CGAL will become insanely slow.

I hit this case the other day. The first piece of processing I do is to combine a whole pile of vector data from

[OSM](http://www.openstreetmap.org/)into one integrated map. While OSM is not particularly high precision (from a bits standpoint) the resulting intersecting points are calculated "perfectly", sometimes with very large mantissas.

I then wrote a piece of code to take a city block from that OSM map and perform some calculations to find the sidewalk calculation. The problem: the four corners of the city block were already very long numbers since they were the result of a CGAL calculation. Thus a long calculation on a long calculation becomes very slow.

The original algorithm took about 36 minutes for a fully optimized build to find all sidewalks in San Diego. That is way too slow, and unusable for our project.

I the put a rounding stage in: fore each corner of the block, I would convert it to a regular 64-bit IEEE float and then back to CGAL, throwing out any "extra" precision that CGAL was saving. Note that the 64-bit float already gives me better than 1 millimeter precision, which is more than overkill for a road. The algorithm run on the "simplified" data ran in 67 seconds.

Now there is one danger: if, due to mismatched road locations in OSM or conflicting edits, some of the "blocks" were really tiny (less than 1 mm) CGAL would have correctly built that block using infinite precision, and my "rounding" would have incorrectly reshaped those blocks, perhaps turning them inside out or in some other way damaging them.

So a necessary step to productizing this 'resolution reduction' is to do a sanity check on each resulting block. Fortunately most of the time if the block contains too-small-to-use data, we don't need the data in the first place.

## No comments:

## Post a Comment