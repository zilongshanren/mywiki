---
title: Beautiful theorems about dynamical systems on the plane
url: https://divisbyzero.com/2011/01/12/beautiful-theorems-about-dynamical-systems-on-the-plane/
author: Dave Richeson
published: '2011-01-12'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I was reading through some papers written by my Ph.D. advisor ([John Franks](http://www.math.northwestern.edu/people/facultyProfiles/john.franks.html)) from the early 1990’s and was reminded of a few beautiful results about the dynamics of planar homeomorphisms. So I thought I’d share them here.

For those of you who are not familiar with the terminology, a *planar homeomorphism* is a bijective function for which

and

are continuous. A simple example of a planar homeomorphism is a translation, such as

.


We will look at these homeomorphisms as *discrete dynamical systems*. That is, we are interested in orbits of points: For simplicity we write

for

(

compositions of

). Intuitively you can think of the point

hopping around the plane as we repeatedly apply the function

.


A point is a

*fixed point* of if

and

is a periodic point if


From here onward I will assume (without saying it explicitly) that the homeomorphisms are *orientation-preserving*. This means that the image of a circle oriented clockwise is a closed curve oriented clockwise. A translation is always orientation preserving, but the reflection is orientation reversing.


To warm up, let’s give a theorem of [Brouwer’s](http://www-history.mcs.st-and.ac.uk/Biographies/Brouwer.html).

** Theorem** [Brouwer]. If has a periodic point, then it has a fixed point.


In fact, this theorem can be strengthened considerably. Roughly speaking, if has just about any type of recurrent behavior, then it must have a fixed point.


Here are two examples:

** Theorem** [[Barge](http://www.math.montana.edu/faculty/mbarge.html), Franks ([1993](http://www.amazon.com/Topology-Computation-Proceedings-Smalefest/dp/0387979328))]. If there are disjoint arcs (or disjoint disks) such that

for all

, and some iterate of

intersects

, some iterate of

intersects

, etc., and some iterate of

intersects

, then

has a fixed point.


In 2002 [Jim Wiseman](http://ecademy.agnesscott.edu/~jwiseman/) and I [gave a short proof](http://www.math.uiuc.edu/~hildebr/ijm/summer02/final/richeson.html) of the following result:

** Theorem**. If the orbit of every point intersects the unit disk , then there is a fixed point in the disk. (Actually, the hypotheses of this theorem are so strong that it holds when

is not invertible and when the space is

.)


The meta-contrapositive of this collection of theorems is that if there is no fixed point, then there is no recurrent behavior. In fact, as Brouwer discovered, if has no fixed point then

behaves like a translation.


An open connected set is a

*domain of translation* for if its boundary is

, where

is a proper embedding of

that separates

and

(as in the image below).


![](../../assets/51416de6299ab90a.jpg)


** Theorem** [Brouwer’s plane translation theorem] If has no fixed points, then every point is contained in some domain of translation.


See Franks ([1992](http://journals.cambridge.org/action/displayAbstract?fromPage=online&aid=2143652)) for a short proof of the theorem. Apparently Brouwer wrote several papers on the plane translation theorem (1909-1919), and since 1920 others have had to go back and clean up the statement and the proof of his theorem. As Brouwer discovered, one has to be very careful with the topology of the plane. For instance, one pathological example that sent Brower back to the drawing board was the [Lakes of Wada](http://en.wikipedia.org/wiki/Lakes_of_Wada) (isn’t that a great name?). In 1917 Takeo Wada discovered that it is possible to find three disjoint connected open sets in the plane that all have the same boundary! Here’s [a picture of three such sets](http://www.math.univ-brest.fr/perso/yves.coudene/Plykin3.jpg).

Now, consider the iterates of a set ,

, and keep track of which sets

are disjoint from

. Call this collection of integers

,

; that is,


.


** Theorem** [Barge, Franks]. If has no fixed points and

is an open or closed connected set, then

is closed under addition.


For example, if and

, then

for

,

,

, etc.


An immediate consequence of this theorem is that if and

are disjoint (i.e.,

), then so are

and

for all

(i.e.,

). In particular it follows that:


**Corollary**. If and

are disjoint, then

and

are disjoint for all

.


In particular, if we added to the the image below, then they would all be disjoint.


![](../../assets/1bcdf1fcaeb82830.jpg)


Franks and Barge also prove a converse to this theorem.

** Theorem** [Barge, Franks]. Suppose is a set of positive integers that is closed under addition. Then there is a translation

and an open topological disk

such that

.


Two-dimensional dynamical systems is a fascinating area of mathematics. These are only a few of the many beautiful theorems.

Isn’t it “such that T(D)=E” instead of “such that E(D)=D” in the last theorem.

No, that’s correct. I could have been more precise by writing

rather than

.

So, the open disk D in the last theorem should be unbounded in general, something like an infinite centipede, isn’t it?

For closed disks the theorem is failing (at least for translations), but do you know some results about the set E(D) in this case, refining the fact that it is closed under adition? For example, in the case of translation the complement of E(D) should be finite, as D is bounded.

si-top