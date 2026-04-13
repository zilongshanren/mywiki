---
title: A Geometric Proof of Brooks’s Trisection?
url: https://divisbyzero.com/2017/03/30/a-geometric-proof-of-brookss-trisection/
author: Dave Richeson
published: '2017-03-30'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

[UPDATE: we have a proof! I included it at the end of the blog post.]

Yesterday I was looking at a few methods of angle trisection.

For instance, I made [this applet](https://www.geogebra.org/m/D3QfcXFy) showing how to use the “cycloid of Ceva” to trisect an angle. (It is based on Archimedes’s *neusis* [marked straightedge] construction.)

I also found David Alan Brook’s *College Mathematics Journal *article “[A new method of trisection](http://www.jstor.org/stable/27646440).” He shows how you can use the squared-off end of a straightedge (or equivalently, a carpenter’s square) to trisect an angle. (This is a different carpenter’s square construction than [the one I wrote about recently](https://divisbyzero.com/2016/03/11/a-trisectrix-from-a-carpenters-square/).)

To perform the trisection of (see figure below), bisect the segment

at

Then draw the segment

perpendicular to

. Draw a circle with center

and radius

Next, arrange the carpenter’s square so that one edge goes through

, one edge is tangent to the circle, and the vertex,

, sits on

. Then

.


![brookstrisect](../../assets/827685469653fdb1.png)


I made [an applet](https://ggbm.at/XdF3Dr86) to illustrate this trisection.

Brooks’s proof used trigonometry. My question is: Is there a *geometric proof* that I spent a little while working on it yesterday and couldn’t find one. If you can, let me know!


UPDATE: We have a proof! Thank you Marius Buliga!

In the proof we are referring to the figure below. Let and

Then it suffices to show that

Let

be the point of tangency. Draw segment

and extend

to

on

Then draw segments


and

Because

lines

and

are parallel, and hence

is a parallelogram. This implies that

is the midpoint of the diagonal

so

Moreover, Because

is the hypotenuse of the right triangle

and

is the median,

We see that

so

Finally, because

is a chord of the circle,

that is,


![brookstrisectproof](../../assets/57263f64cc3f8abd.png)


Update 2: [Andrew Stacey](https://twitter.com/mathforge) just sent me an another proof:

In the proof we are referring to the figure below. Let and

Then it suffices to show that

Let

be the point of tangency of the carpenter’s square and the circle. Because


Construct

Because

is a tangent line and

is a radius of the circle,

Because


and

are parallel. Thus

Construct a point

so that

is a parallelogram. Notice that


and

are collinear. Let

be the midpoint of

. Construct the line segment

and the circle with center

and radius

. Note that the circle passes through



and

—the first three because

and the fourth because

and

is a diameter of the circle. Because

is parallel to


Finally,

is a central angle and

is an inscribed angle and both cut off the same arc of the circle; thus


![brookstrisectproof2](../../assets/53d956afb6df1fac.png)


I think there is no such proof, because there can’t be.

https://en.wikipedia.org/wiki/Angle_trisection

It is impossible to trisect an arbitrary angle with a compass and straightedge, but if you allow certain other tools—like the carpenter’s square in this case—then angle trisection is possible. There is a proof that this works, but it uses trigonometry, not geometry.

@pepe: as Dave says, this proof uses a tool different from straightedge and compass. In other words, without the carpenter’s square you cannot construct right angle BFG with the given constraints.

BF || GC and the segments BD and DC have equal lengths. Now denote by J the intersection of the lines FD and GC. Then BFCJ is a parallelogram so the segments FD and DJ have equal length. The triangle FJG is right, therefore DG and FD have equal lengths. So the angles ABF, DFG and DGF are all equal. Use the triangle DCG to prove that the angle DCG is twice the angle DGF.

Very nice! Thank you. I’ll update my post in a few minutes!

Sorry for the double comment, i thought the computer ate my first one :) Very nice post and construction. From the proof I suspect the construction fails in interesting ways in hyperbolic or elliptic geometry.

Denote by J the intersection of the lines FD and GC. The angles BFG and FGC are right, so BF is parallel with GC. Then BFCJ is a parallelogram, so FD and DJ have equal lengths. The triangle FJG is right so FD and DG have equal lengths, therefore the angles DFG and DGF are equal. Use that HGC is straight and the triangle DCG to prove that the angle DCG is twice the angle DGF.

Hi, random amateur reader here.

I found it interesting to notice that it’s not the use of a carpenter’s square, specifically, that is needed in order to perform this construction — it’s the ability to find the point ‘F’, subject to the constraint that angle BFJ is a right angle. A carpenter’s square is one tool for doing that, but any method of ‘inverting’ the problem “BFJ is a right angle. solve for F” will do.

You can do this by binary-searching for the position of F on the line segment ED – but this amounts to constructing an infinite series of points and taking their limit, and that’s equivalent to allowing yourself to compute 1/3 of an angle by using an infinite series of bisections like 1/3 = 1/4+1/16+1/256…, which is a known way of trisecting angles anyway. Infinite series approximations are not allowed, of course, in normal compass+straightedge constructions, so this doesn’t clash with the impossibility proof.