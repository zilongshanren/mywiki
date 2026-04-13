---
title: sinc and Polynomial interpolation
url: https://fgiesen.wordpress.com/2010/10/25/sinc-and-polynomial-interpolation/
published: '2010-10-25'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# sinc and Polynomial interpolation

Another short one. This one bugged me for quite a while until I realized what the answer was a few years ago. The Sampling Theorem states that (under the right conditions)

where

(the normalized sinc function). The problem is this: Where does the sinc function come from? (In a philosophical sense. It plops out of the proof sure enough, but that’s not what I mean). Fourier theory is full of (trigonometric) polynomials (i.e. sine/cosine waves when you’re dealing with real-valued signals), so where does the factor of x in the denominator suddenly come from?

The answer is a nice identity discovered by Euler:

With some straightforward algebraic manipulations (ignoring convergence issues for now) you get:


Compare this with the formula for Lagrange basis polynomials:

in other words, the sinc function is the limiting case of Lagrange polynomials for an infinite number of equidistant control points. Which is pretty neat :)

As you say, sinc(x) is an interpolation function for the integers, and it is easy to see that the translates sinc(x-k) form an orthonormal set in L^2(R). In this language, the essence of the sampling theorem is that those guys really span all bandlimited functions with frequency <= 1/2. But the Fourier transforms of those guys are just the "cut-off" Fourier basis functions

rect(f) * e^{-2 pi i n x},

and Shannon's theorem follows at once from the definition of a band-limited function.

Put slightly differently, an intuitive way of understanding Shannon's theorem is the following: Band-limited functions can be periodically continued in Fourier space, hence *their Fourier Transform* can be represented by a Fourier series cut off with a rectangular function. After transforming back, the family of sinc translates arises.