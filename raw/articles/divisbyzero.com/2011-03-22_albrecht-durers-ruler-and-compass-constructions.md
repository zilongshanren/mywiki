---
title: Albrecht Dürer’s ruler and compass constructions
url: https://divisbyzero.com/2011/03/22/albrecht-durers-ruler-and-compass-constructions/
author: Dave Richeson
published: '2011-03-22'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

[Albrecht Dürer](http://en.wikipedia.org/wiki/Durer) (1471–1528) is a famous Renaissance artist. Mathematicians probably know him best for his work * Melencolia I* which contains a magic square, a mysterious polyhedron, a compass, etc.

Today I was reading his book *Underweysung der Messung mit dem Zirckel und Richtscheyt* (*The Painter’s Manual: A manual of measurement of lines, areas, and solids by means of compass and ruler*). It was published in 1525 and was reprinted posthumously in 1538 with additional material. Our library has a nice English translation of the first edition by Walter L. Strauss (1977). The book has scans of the old German on the left and the English translations on the right. (You can see [scans of the original 1538 book online](http://www.rarebookroom.org/Control/duruwm/index.html)—see pp. 110–119 for this material.)

Dürer wrote this book as a technical manual for artists, craftsmen, etc. For example, it gave elementary instructions for how to draw regular polygons with a ruler and compass. In Dürer’s time the old works of the Greeks were just becoming available again. Dürer apparently had access to them. In fact, the book begins, “The most sagacious of men, Euclid, has assembled the foundation of geometry. Those who understand him well can dispense with what follows here.” This is an odd beginning because, although he gives some Euclidean constructions, many are new; moreover, he must have known that the vast majority of the readers knew no Euclid.

Because this is a technical manual, Dürer’s emphasis is on easy-to-draw constructions that look good—in particular, some are just good looking approximations. Many of them were known to craftsmen of the day (techniques passed down through the generations) or appeared in print earlier, but some may have been discovered by Dürer.

I was led to the book because I wanted to see his construction of the regular pentagon. He gives two constructions. One is a classical Greek construction, but it is the second that I wanted to see.

This construction has two notable features. One is that it is drawn using a rusty compass—that is, the compass is set to one opening for the entire construction. This was probably a great bonus to the artisan; I imagine that not having to continually adjust the compass made the construction fast and accurate. The second interesting fact is that it is only approximately a regular pentagon—but it is a *very good* approximation. By my calculations, the error in the height of the pentagon is less than 1%. The construction is shown below. You begin with the line segment labeled and you set the compass to this radius. I’ll leave it as an exercise to the reader to reverse engineer the construction.


Dürer never says that this is an approximation.

I found what I was looking for. But then I found more. Dürer goes on to give ruler and compass constructions of regular polygons with sides numbering 3, 4, 5, 6, 7, 8, 9, 11, and 13. As you may know, [some of these are impossible constructions](http://en.wikipedia.org/wiki/Constructible_polygon) (7, 9, 11, and 13). Hence Dürer’s constructions must be approximations.

The heptagon (7-gon) and the nonagon (9-gon) are excellent approximations. So I though I’d share them with you.

Durer’s heptagon is remarkably easy to construct. Begin with an equilateral triangle inscribed in a circle. Then half of the side of the triangle is nearly the same length as the side of the inscribed heptagon. So all we must do is bisect one side, and sweep an arc to obtain the first side of the heptagon. Then use this side to draw the rest.

The construction of the nonagon is a little more involved. Draw a circle. Then with the same opening of the compass draw three “fish-bladders” (as he calls them)—to do this you need the centers on the vertices of an inscribed equilateral triangle. Draw a radial segment inside one fish-bladder and divide it into thirds. Draw a perpendicular line at the 1/3 mark. It intersects the bladder in two points ( and

in Dürer’s diagram). Draw a circle with the same center as the large circle, passing through

and

. Then

is one side of an (approximate) nonagon inscribed in the smaller circle.


As with the pentagon, Dürer does not mention that the heptagon and the nonagon are approximations. However, he admits that the constructions of the 11-gon and the 13-gon (which I will omit) are “mechanical [approximate] and not demonstrative.”

As if that is not cool enough, Dürer tackles the famously impossible [angle trisection](http://en.wikipedia.org/wiki/Angle_trisection) and [circle squaring](http://en.wikipedia.org/wiki/Squaring_the_circle) problems.

To see his (approximate) angle trisection solution we begin with an arc of a circle and the corresponding chord. (He actually trisects the arc, but that is equivalent to trisecting the central angle.) He begins by trisecting the chord. The points in his diagram are, in order left-to-right, ,

,

, and

. Draw perpendicular lines from

and

to the arc, then swing arcs from these points (with centers

and

) down to the chord. These new points are

and

. Trisect the segments

and

. Using the points closest to

and

, sweep arcs back up to the original arc of the circle to obtain

and

. Then arcs

,

, and

are approximately equal (he does not admit to this being an approximation).


Finally we turn to his circle squaring. It is very crude. He writes “The *quadratura circui,* which means squaring the circle so that both square and circle have the same surface area, has not been demonstrated by scholars. But it can be done approximately for minor applications or small areas in the following manner.” In the first edition of the book he uses an approximation of , and in the second he uses

. He writes simply, “Draw a square and divide its diagonal into ten parts and then draw a circle with a diameter of eight of these parts.”


What a great find and an enjoyable read! By the way, I encourage you to try performing these constructions. I did so using [Geogebra](http://www.geogebra.org) and was amazed by the resulting figures.

## 3 Comments

Comments are closed.