---
title: Trigonometric functions and rational multiples of pi
url: https://divisbyzero.com/2010/10/28/trigonometric-functions-and-rational-multiples-of-pi/
author: Dave Richeson
published: '2010-10-28'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Recall that a real number is * algebraic* if it is the root of a polynomial with integer coefficients and that it is

*otherwise. For example*

[transcendental](http://en.wikipedia.org/wiki/Transcendental_number)[.)](https://divisbyzero.com/2010/09/28/the-transcendence-of-e/)

is a transcendental number

Today I would like to prove that a certain large class of numbers is algebraic.

We know that ,

, and

are algebraic numbers. It may not be surprising, then, that when a rational multiple of

is the argument of a trigonometric function we obtain an algebraic number.



Theorem.Ifis a rational multiple of

, then

,

,

,

,

, and

are algebraic numbers (if they are defined).


It turns out that there is a nice proof of this fact that uses two of the most celebrated results in complex analysis: [Euler’s identity](http://en.wikipedia.org/wiki/Euler's_identity)

Let be a rational multiple of

. For simplicity of calculations we will write

as a rational multiple of

:


We use Euler’s identity and DeMoivre’s formula to obtain this string of equalities.

(Note: this argument shows that is an

[th root of unity](http://en.wikipedia.org/wiki/Root_of_unity) in

The idea of the proof is to multiply out , set the real part equal to 1 and the imaginary part equal to 0. Then apply some trigonometric identities to obtain the polynomial relations.


We will illustrate with an example, but the proof of the general case is identical. Consider . Using the relationship from above we have


Setting the real parts equal we obtain

Notice that all of the exponents of are even (this will always happen because

is real if and only if

is even). We know that

, so we may replace all instances of

with

to obtain


In other words, is a root of the polynomial


Thus is algebraic. This identical argument works for the cosine of any rational multiple of

.


Now consider the imaginary part of the equation. Setting both sides equal we obtain

Notice that every term is the product of five trigonometric functions (that is, the sum of the exponents of sines and cosines is 5). If we divide through by we obtain the following expression with tangents


Thus is a root of the polynomial


and we conclude that is algebraic. Again, this same trick (dividing the imaginary part by

) works for the tangent of any rational multiple of

.


What about ? Here we use the identity

. So


which we have shown is algebraic.

Finally, since the set of algebraic numbers is a [field](http://en.wikipedia.org/wiki/Field_(mathematics)), we know that ,

, and

are algebraic. (We could also have used this field property to show that

is algebraic, since

.)


Just a basic question. Why do you subtract the 10x part of the expansion rather than add?

Are you referring to 10’s in the expansion of

? It is because one of them will have an

in front, which is -1 and the other has

which is

.

Thanks, I get it.