---
title: Tangent lines to the sine function with rational slope
url: https://divisbyzero.com/2014/08/27/tangent-lines-to-the-sine-function-with-rational-slope/
author: Dave Richeson
published: '2014-08-27'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Today I was wondering the following thing (I won’t bore you with how I ended up with this question):

Are there any rational values of for which the line

is tangent to the graph of


Clearly the answer is yes: But my gut feeling was that this was the only such

After some head scratching, I obtained the following proof.


Suppose they are tangent at . Then the point of tangency is

Moreover, the slope of the tangent line is

. Thus,

must satisfy the two equations:


and


.


Using a trig identity,

.


So,

Note that is an algebraic number—it is the root of a polynomial with integer coefficients.


In 1882 [Ferdinand von Lindemann famously proved](http://en.wikipedia.org/wiki/Lindemann-Weierstrass_theorem) that is transcendental (that is, non-algebraic) for every non-zero algebraic number

and a similar proof holds for the sine and cosine functions.


Thus, because and

is algebraic, it must be the case that

. In particular,


This concludes the proof.