---
title: An interesting multivariable calculus example
url: https://divisbyzero.com/2012/04/18/an-interesting-multivariable-calculus-example/
author: Dave Richeson
published: '2012-04-18'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Earlier this semester in my Multivariable Calculus course we were discussing the [second derivative test](http://en.wikipedia.org/wiki/Second_partial_derivative_test). Recall the pesky condition that if is a critical point and

, then the test fails.


A student emailed me after class and asked the following question. Suppose a function has a critical point at

and

. Moreover, suppose that as we approach

along

we have

when

and

when

. Is that enough to say that the critical point is a not a maximum or a minimum? His thought process was that if we look at slices

we get curves that are concave up when

and curves that are concave down when

—surely that could not happen at a maximum or minimum.


I understood his intuition, but I was skeptical. Indeed, after a little playing around I came up with the following counterexample. The function is

The first partial derivatives are

Clearly is a critical point. The second partial derivatives are


Thus . So the second derivative test fails. But observe that when

we have


So when

and

when

. Yet it is easy to see that

is a minimum:

and

for all

. A graph of the function is shown below. You can see the concave down cross sections for

and

.


I think the functions

and

also work. They are inspired by the pitchfork bifurcation (compare with the shape of the contour

).

I actually meant

and

, but the other two also work. From the contour plots for all these functions it is clear that they use the same idea.

Great! Thanks. I haven’t checked the derivatives, but it looks good on Grapher.

I just realised that the examples I gave are closely related to the Rosenbrock function [1].

[1] http://en.wikipedia.org/wiki/Rosenbrock_function

Wow. Cool. Thanks for sharing that!