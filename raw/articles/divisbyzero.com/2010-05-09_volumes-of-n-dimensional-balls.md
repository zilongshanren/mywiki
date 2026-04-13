---
title: Volumes of n-dimensional balls
url: https://divisbyzero.com/2010/05/09/volumes-of-n-dimensional-balls/
author: Dave Richeson
published: '2010-05-09'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

We all know that the area of a circle is and the volume of a sphere is

, but what about the volumes (or hypervolumes) of balls of higher dimension?


For a fun exercise I had my multivariable calculus class compute the volumes of various balls using multiple integrals. The surprising results inspired this post.

First some terminology. An *-dimensional hypersphere* (or

*) of radius*

-sphere

An *-dimensional ball* (or

*) is the region enclosed by an*

-ball

It is possible to define “volume” in —in

it is length, in

it is area, in

it is ordinary volume, and in

it is hypervolume. Let

denote the volume of the

-ball of radius

.


It turns out that the volumes of -balls satisfy the following remarkable recursion relation. (I’ll prove this relation at the end of the post.)


It is not difficult to use this recurrence relation to obtain a formula for . In particular, when

is even

and when

is odd

. (If you know what the gamma function is you can express this as a single function,

)


The volumes of the -balls in the first 15 dimensions are given in the following table.


If you look at the volumes of the unit balls you’ll see they increase at first, reaching a maximum in dimension 5. Then they decrease and tend to zero as the dimension goes to infinity. Strange!

First, what is special about dimension 5? Why is the maximum achieved in this dimension? It turns out that there is nothing special about dimension 5. Below is a [GeoGebra applet](http://users.dickinson.edu/~richesod/nballs/) that allows you to adjust the radii of the balls. As we can see, the maximum volume is not always attained by the ball in dimension 5. Indeed, as the radius increases, the maximum volume occurs in higher dimensions. As [John Moeller](http://ontopo.wordpress.com/2009/03/03/reasoning-in-higher-dimensions-hyperspheres/) points out, the powers of in the numerator try to make

an increasing function, however the factorials in the denominator always dominate in the end.


Second, what is the intuition behind this limit of zero? One way to see this is to observe that to be on the boundary of the unit -ball, we must have

, but for this to happen when

is large, most of the

‘s must be very close to zero. For example, the line

intersects the

-sphere at

. On the other hand, the corresponding corners of the hypercube that inscribes the sphere are at

,

units from the origin. Thus the sphere fills up less and less of the hypercube that contains it. (Notice that the circumscribed hypercube has volume

, while inscribed hypercube has volume

.)


My colleague informed me that this zero limit is related to the [curse of dimensionality](http://en.wikipedia.org/wiki/Curse_of_dimensionality) in statistics. Volume increases rapidly as dimension increases, so it requires many more data points to get a good estimate. As Wikipedia points out, “100 evenly-spaced sample points suffice to sample a unit interval with no more than 0.01 distance between points; an equivalent sampling of a 10-dimensional unit hypercube with a lattice with a spacing of 0.01 between adjacent points would require sample points.”


**Proof**

Now I will prove the recurrence relation that I gave above.

Clearly the relation is true for and

. Suppose

.


First recall that if a solid in -dimensional space is scaled by a factor of

, then its volume increases by a factor of

. In particular, this implies that


Observe that the intersection of the -plane with the

-ball is a disk of radius

centered at the origin (see image below). Use polar coordinates to describe points in this disk. Then the perpendicular cross section of the

-ball at the point

is an

-ball of radius

.


Thus we can compute by integrating

over the disk. We do so using polar coordinates.


Great post!

This is another good example of why you have to be careful when dealing with high-dimensional geometry. I posted a similar counter-intuitive result to do with the relative volumes of cubes and spheres a while back.

Wow, that is really excellent. Thanks for sharing the link.

This volume computation is done in the book Symmetric Bilinear Forms (By Milnor, Husemoller) as part of the full classification of indefinite integral inner product spaces (by their rank, type, and signature).

There, it is shown that there is indeed something spacial about n=5; using Minkowski’s convex body theorem, it is more natural to look at the behavior of $4/(V_n(1))^{2/n}$, which is larger than 2 for n>4, which makes the solution to the classification problem essentially different for n=5.

n=5 is “n > = 5” at the end of my previous comment.

Thanks. Very interesting. I’ll be sure to track down that reference.

Interesting post. I have to say though that comparing length to area to volume to hypervolume and so on makes little sense, IMHO it would be better to plot the fraction of the hypercube each sphere occupies.

(there is a typo in second table should be R^3 in n=3)

I agree—we’re comparing apples to oranges to bananas here (which doesn’t make it less fun to do). I like your idea. I’ll have to give that a try when I get a chance.

Thanks for catching the typo. It is fixed now.

There was a nice MathOverflow question about the volume tending to zero which attracted a lot of great answers.

Wow. Excellent. Thanks for providing that link.

Fleming’s 5.9, Functions of Several Variables has a very nice discussion of this. Not the curse of dimensionality bit, though – that was a nice tie-together.

Wait a minute.

“Volume increases rapidly as dimension increases”

Now look at your dim/vol plot.

Huh?

Yes, that’s not so clear. Here’s what I meant: a hypercube of side length

in dimension

has hypervolume

. So if

and

is large, then this volume is very large.

Ah – different object – gotcha.

That suggests a possibly interesting investigation I haven’t seen before: how does the volume of the unit n-cube or sphere vary with the *metric*. (You changing objects from sphere to cube suggested metric change to me because under other metrics, “circles” become “squares”.)

I would be curious to see a discussion of what, if anything, general could be said about the measure of typical sets as one varies the metric – especially with convergent sequences of metrics and the like. Knew I should’ve taken that functional analysis class. :P

Really interesting. Thanks.

Another Math Overflow posting that had some interesting thoughts on thinking in higher dimensions. Particularly interesting post by Terry Tao:

“For instance, the fact that most of the mass of a unit ball in high dimensions lurks near the boundary of the ball can be interpreted as a manifestation of the law of large numbers, using the interpretation of a high-dimensional vector space as the state space for a large number of trials of a random variable.”

Thanks! I’ve just started reading MathOverflow—I’ve known about it for a while, but have been too busy to dive in. It is great. Thanks for pointing this question out to me.

Re string theory– if the visible universe is a 9-d object w/ 3d of ~ (10^26)m and 6d of ~(10^-35)m, its diameter is then ~(10^-14.67)m, about the diameter of a proton. No part of our universe is any farther than this from any other part- considered hyperspatially. This may be a boring and inconsequential factoid to STists, but it’s bogglesome enough that the pop-sci press should be all over it.

For n=5, pi should be squared, not cubed.

Thanks! Fixed.

What happens when x -> ∞? In other words, what is the volume of a sphere of infinite radius and infinite dimensions? Is it still zero?

There’s a nice proof without induction that uses the gamma function directly, in Peskin & Schroder’s Quantum Theory of Fields. Remember the proof of the integral of a gaussian, using 2d in polar coords? This does the same in reverse. Take e^{-x_1^2 – … – x_n^2} and integrate over R^n. In cartesian coords you get pi^(n/2). Switch to polar coords and you get the formula for the surface area of a sphere times a Gamma function. Integrate surface area to get (hyper-) volume.

Nicely written and easy to understand, tnx! It is interesting to see that you mentioned the connection to ‘the curse of dimensionality’ in statistics and machine learning. Indeed this phenomena makes it difficult to train classifiers and regressions in highly dimensional spaces because most of the data lives in ‘the corners’ of the feature space (hypercube) instead of being at the center (within the hypersphere). I recentely wroten an intuitive explanation about this, and the link between your post and the curse of dimensionality: http://www.visiondummy.com/2014/04/curse-dimensionality-affect-classification/