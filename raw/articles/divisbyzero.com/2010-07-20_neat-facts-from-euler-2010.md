---
title: Neat facts from Euler 2010
url: https://divisbyzero.com/2010/07/20/neat-facts-from-euler-2010/
author: Dave Richeson
published: '2010-07-20'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I had the wonderful honor of being the keynote speaker at the 9th annual meeting of the [Euler Society](http://www.eulersociety.org/). I spoke today about [my book](http://eulersgem.com). It is now the end of the second day of this 2.5 day conference. I thought I’d post a few of the many interesting things that I learned.

1. Larry D’Antonio shared this quote from Kant (*Physical Monadology*, 1756):

But how in this business can metaphysics be reconciled with geometry [mathematics], when it appears easier to mate griffins with horses than to unite transcendental philosophy with geometry [mathematics]?


(Apparently the expression “mating griffins and horses” goes back to Virgil’s 8th *Ecologue* and is supposed to signify the impossible, since griffins view horses as prey. When the two do mate their offspring is a [hippogriff](http://en.wikipedia.org/wiki/Hippogriff)—a creature that was recently reintroduced in the *Harry Potter* series.)

2. Let be the set of all nontrivial powers (listed without repeats). Christian Goldbach discovered the following summation:


.


Euler gave a “proof” of this in [ Variae observationes circa series infinitas](http://www.math.dartmouth.edu/~euler/pages/E072.html) and extended it in a number of interesting directions. Bruce Burdick gave a talk in which he showed Euler’s slick proof—it begins with Euler taking

[English translation](http://webs2002.uab.es/lbibiloni/Euler/EulerObservat.pdf)or on Ed Sandifer’s

[How Euler Did It](http://www.maa.org/editorial/euler/How%20Euler%20Did%20It%2016%20Goldbachs%20series.pdf)site. Then Bruce showed how to make Euler’s proof rigorous.

3. The [zeta function](http://en.wikipedia.org/wiki/Riemann_zeta_function) has the following property:

.


Quote of the Day from Bruce Petrie: “In the 18th century, existence proofs didn’t exist.”


5. Tom Osler spoke about oblique angle diameters for curves. The definition is a little wordy, so I’ll describe it for a parabola. Take any line parallel to the axis of symmetry of a parabola (this line is an oblique angle diameter). Draw the tangent line to the parabola where it meets the line. Then draw any line parallel to this tangent line that meets the parabola twice. This line segment is always bisected by the oblique angle diameter (in the diagram below FD is the same length as DC).

[It turns out that every conic section has an infinite family of oblique angle diameters. For the parabola it is any line parallel to the axis of symmetry. For an ellipse and a hyperbola it is any line through the origin.](https://divisbyzero.com/wp-content/uploads/2010/07/screen-shot-2010-07-20-at-9-08-26-pm.png)

Euler had a lot to say about this, but he had a very slick proof that if a curve has two oblique angle diameters units apart, then it is possible to find infinitely many simply by repeatedly translating one of the given ones by

units.


6. In this same paper Euler discusses a neat fact about triangles with vertices on a conic section. I’ll describe it for the ellipse. If you pick a point on an ellipse ( on the ellipse below) and draw the tangent line to the ellipse through

, then draw a line from the center (

below) to the ellipse parallel to the tangent line and it meets at the point

, then the area of triangle

does not depend on the point

. In particular, if the ellipse has the form

, then the area is

.