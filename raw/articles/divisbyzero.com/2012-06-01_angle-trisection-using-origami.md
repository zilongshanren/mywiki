---
title: Angle trisection using origami
url: https://divisbyzero.com/2012/06/01/angle-trisection-using-origami/
author: Dave Richeson
published: '2012-06-01'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

It is well known that it is impossible to [trisect an arbitrary angle using only a compass and straightedge.](http://en.wikipedia.org/wiki/Angle_trisection) However, as we will see in this post, it is possible to trisect an angle using origami. The technique shown here dates back to the 1970s and is due to Hisashi Abe.

Assume, as in the figure below, that we begin with an acute angle formed by the bottom edge of the square of origami paper and a line (a fold, presumably),

, meeting at the lower left corner of the square. Create an arbitrary horizontal fold to form the line

, then fold the bottom edge up to

to form the line

. Let

be the lower left corner of the square and

be the left endpoint of

. Fold the square so that

and

meet the lines

and

, respectively. (Note: this is the non-Euclidean move—this fold line cannot, in general, be drawn using compass and straightedge.) With the paper still folded, refold along

to create a new fold

. Open the paper and fold it to extend

to a full fold (this fold will extend to the corner of the square,

). Finally, fold the lower edge of the square up to

to create the line

. Having accomplished this, the lines

and

trisect the angle

.


![](../../assets/248fc06ca4cff4d3.png)


Let us see why this is true. Consider the diagram below. We have drawn in , which is the location of the segment

after it is folded,

, the fourth side of the isosceles trapezoid

, and

, the second diagonal of

. We must show that

, where

and

.


![](../../assets/c87c883771e9866a.png)


Because and

are parallel,

, and because

is the altitude of the isosceles triangle

,

. Thus

. Now,

is an isosceles trapezoid and

is an isosceles triangle, so

and

are congruent isosceles triangles. Thus

. It follows that

.


The geometric properties of origami constructions are quite interesting. Every point that is constructible using a compass and straightedge is constructible using origami. But more is constructible. As we’ve seen, it is possible to trisect any angle using origami (I’ll leave the obtuse angles as an exercise). It is possible to [double a cube](http://en.wikipedia.org/wiki/Doubling_the_cube). It is possible to [construct regular heptagons and nonagons](http://en.wikipedia.org/wiki/Constructible_polygon). In fact, where the constructability of -gons is related to

[Fermat primes](http://en.wikipedia.org/wiki/Fermat_number), the origami-constructibility of -gons is related to

[Pierpont primes](http://en.wikipedia.org/wiki/Pierpont_prime). While the [field of constructible numbers](http://en.wikipedia.org/wiki/Constructible_number) is the smallest subfield of that is closed under square roots, the field of origami-constructible numbers is the smallest subfield that is closed under square roots and cube roots. In fact, it is possible to solve any linear, quadratic, cubic, or quartic equation using origami!


There are quite a few places to read about geometric constructions using origami, but a good starting point is [this online article](http://www.langorigami.com/science/math/hja/origami_constructions.pdf) (pdf) by Robert Lang.

Reblogged this on Room 196, Hilbert's Hotel.

INTERESTING.

——————

You may refer to my relevant solutions at:http://www.stefanides.gr/Html/Classical_Problems_et_Alii_with_Web_Links.htm

Panagiotis Stefanides

quick question how do you write math in the blog?

You can embed LaTeX in a WordPress blog. Here’s a page with the details. There’s also a neat script the converts LaTeX to WordPress LaTeX. I wrote about it elsewhere on my blog.

Neusis CANNOT trisect an angle. The trisection is only an approximation by the resolution of what your eye can see.

http://www.flickr.com/photos/85937466@N02/10099206904/in/set-72157636438514124