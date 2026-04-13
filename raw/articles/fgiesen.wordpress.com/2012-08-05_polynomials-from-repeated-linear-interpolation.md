---
title: Polynomials from repeated linear interpolation
url: https://fgiesen.wordpress.com/2012/08/05/polynomials-from-repeated-linear-interp/
published: '2012-08-05'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Polynomials from repeated linear interpolation

It’s fairly well-known that Bezier curves can be evaluated using repeated linear interpolation – de Casteljau’s algorithm. It’s also fairly well-known that a generalization of this algorithm can be used to evaluate B-Splines: de Boor’s algorithm. What’s not as well known is that it’s easy to construct interpolating polynomials using a very similar approach, leading to an algorithm that is, in a sense, halfway between the two.

In the following, I’ll write for linear interpolation. I’ll stick with quadratic curves since they are the lowest-order curves to show “interesting” behavior for the purposes of this article; everything generalizes to higher degrees in the obvious way.


### De Casteljau’s algorithm

De Casteljau’s algorithm is a well-known algorithm to evaluate Bezier Curves. There’s plenty of material on this elsewhere, so as usual, I’ll keep it brief. Assume we have three control points . In the first stage, we construct three constant (degree-0) polynomials for the three control points:





These are then linearly interpolated to yield two linear (degree-1) polynomials:



which we then interpolate linearly again to give the final result

Note I give the construction of the full polynomials here; the actual de Casteljau algorithm gets rid of them immediately by evaluating all of them as soon as they appear (only ever doing linear interpolations). Anyway, the general construction rule we’ve been following is this:

### De Boor’s algorithm

De Boor’s algorithm is the equivalent to de Casteljau’s algorithm for B-Splines. Again, there’s plenty of material out there on it, so I’ll keep it brief: We again start with constant functions for our data points. This time, the exact formulas depend on the degree of the spline we’ll be using. I’ll be using the degree (quadratic) here. We’ll also need a

*knot vector* which determines where our knots are; knots are (very roughly) the t’s corresponding to the control points. I’ll be using slightly different indexing from what’s normally used to make the similarities more visible, and ignore issues such as picking the right set of control points to interpolate from:





Then we linearly interpolate based on the knot vector:



and interpolate again one more time to get the results:

The general recursion formula for de Boor’s algorithm (with this indexing convention, which is non-standard, so do **not** use this for reference!) is this:

### Interpolating polynomials from linear interpolation

There’s multiple constructions for interpolating polynomials; the best-known are probably the [Lagrange polynomials](http://en.wikipedia.org/wiki/Lagrange_polynomial) (which form a basis for the interpolating polynomials of degree n for a given set of *nodes* ) and the

[Newton polynomials](http://en.wikipedia.org/wiki/Newton_polynomials) (since polynomial interpolation has unique solutions, these give the same results, but the Newton formulation is more suitable for incremental evaluation).

What’s less well known is that interpolating polynomials also obey a simple triangular scheme based on repeated linear interpolation: Again, we start the same way with constant polynomials




and this time we have associated nodes and want to find the interpolating polynomial

such that

,

,

. Same as before, we first try to find linear functions that solve part of the problem. A reasonable choice is:




Note the construction here. is a linear polynomial that interpolates the data points

, and we get it by interpolating between two simpler (degree-0) polynomials that interpolate only

and

, respectively: we simply make sure that at

, we use

, and at

, we use

. All of this is easiest to visualize when

, but it in facts works with them in any order.

is constructed the same way.


To construct our final interpolating polynomial, we use the same trick again:

Note this one is a bit subtle. We linearly interpolate between two polynomials that both in turn interpolate ; this means we already know that the result will also pass through this point. So

is taken care of, and we only need to worry about

and

– and for each of the two, one of our two polynomials does the job, so we can do the linear interpolation trick again. The generalization of this approach to higher degrees requires that we make sure that both of our input polynomials at every step interpolate all of the middle points, so we only need to fix up the ends. But this is easy to arrange – the general pattern should be clear from the construction above. This gives us our recursive construction rule:


All of this is, of course, not new; in fact, this is just [Neville’s algorithm](http://en.wikipedia.org/wiki/Neville%27s_algorithm). But in typical presentations, this is derived purely algebraically from the properties of Newton interpolation and divided differences, and it’s not pointed out that the linear combination in the recurrence is, in fact, a linear interpolation – which at least to me makes everything much easier to visualize.

### The punchline

The really interesting bit to me though is that, starting from the exact same initial conditions, we get three different important interpolation / approximation algorithms that differ only in how they choose their interpolation factors:

de Casteljau:

Neville:

de Boor:

I think this quite pretty. B-Splines with the right knot vector (e.g. [0,0,0,1,1,1] for the quadratic curves we’ve been using) are just Bezier Curves, that bit is well known. But what’s less well known is that Neville’s Algorithm (and hence regular polynomial interpolation) is just another triangular linear interpolation scheme that fits inbetween the two.

OK, so convert each method to weighted sums of basis functions. Basis functions can be converted between each other, and Fourier analysis is just projecting functions to a sinusoidal basis so there’s Spectral Analysis, which leads into Generalized Sampling and Shannon’s Information theory. Basis functions also lead to Wavelets and, if you relax the self-similarity preconditions, you’re into the world of Frames. It’s all part of the same thing!

The connection from anything polynomial to Fourier Analysis is far more direct though: Just go from real polynomials p(x) to the complex domain p(z) and substitute z=exp(-it). Presto trigonometric polynomials (which are really just finite Fourier series).

You didn’t quite spell it out. But the real punchline is that the substitution establishes a relationship between complex power series on the unit circle and Fourier series. With only a little work, it gives you an extremely weak but still practically useful part of the convergence theory for Fourier series. Namely, if the complex-valued function defined on the unit circle has an analytic continuation to the entire unit disk, then we know from complex analysis 101 that this extended function has a convergent power series expansion around the origin, and hence the original function on the unit circle has a convergent Fourier expansion.

By the way, another way you see this relationship between complex power series and Fourier series is in Cauchy’s integral formula for calculating derivatives (and hence coefficients of power series). It integrates around a circle and it should look really familiar–it’s completely analogous to the formula for calculating Fourier coefficients where you integrate over a sinusoidal period.