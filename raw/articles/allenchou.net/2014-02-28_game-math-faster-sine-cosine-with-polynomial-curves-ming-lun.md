---
title: 'Game Math: Faster Sine & Cosine with Polynomial Curves | Ming-Lun "Allen"
  Chou | 周明倫'
url: https://allenchou.net/2014/02/game-math-faster-sine-cosine-with-polynomial-curves/
author: Allen Chou
published: '2014-02-28'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

We have seen how to approximate a function using polynomials in [this post](http://allenchou.net/2014/02/game-math-approximation-with-polynomial-curves/). A good candidate for polynomial approximation would be the sine function, for it is used a lot in games and is not a cheap function to call. This is essentially the same task as approximating the consine curve, since the cosine curve is just a shifted sine curve.

The sine curve is periodic, so will just focus on the domain ![Rendered by QuickLaTeX.com x \in [0, 2\pi)](../../assets/bc3f352107c981f5.png)


![sine](../../assets/c26164920692c5d2.png)


We will first try to match a quarter of the sine curve, a downward “hill”.

![hill](../../assets/5276b8c678ccfa7f.png)



We will impose four conditions, the positions and slopes of the hill top and the hill bottom. This means we have to use a polynomial of degree 3 (a cubic curve) to match this hill.

![Rendered by QuickLaTeX.com \[ P(x) = a_0 + a_1 x + a_2 x^2 + a_3 x^3 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-971d211fb409adee1d57593075aad260_l3.png)


And we get these equations from the four conditions:

![Rendered by QuickLaTeX.com \begin{flalign*} P(0) &= 1 \\ P(\frac{\pi}{2}) &= 0 \\ P'(0) &= 0 \\ P'(\frac{\pi}{2}) &= -1 \\ \end{flalign*}](../../assets/acf008542fbf2891.png)


where ![Rendered by QuickLaTeX.com f'(x)](../../assets/705dd9a37225a283.png)

![Rendered by QuickLaTeX.com f(x)](../../assets/45cfff1d70bd2498.png)


So here’s the system of equations we have to solve in order to obtain the coefficients of the polynomial:

![Rendered by QuickLaTeX.com \begin{flalign*} a_0 &= 1 \\ a_0 + \frac{\pi}{2} a_1 + \frac{\pi^2}{4} a_2 + \frac{\pi^3}{8} a_3 &= 0 \\ a_1 &= 0 \\ a_1 + \pi a_2 + \frac{3 \pi^2}{4} a_3 &= -1 \\ \end{flalign*}](../../assets/e3b2d5e75f463c41.png)


After solving the system of equations, we get:

![Rendered by QuickLaTeX.com \begin{flalign*} a_0 &= 1 \\ a_1 &= 0 \\ a_2 &= \frac{2}{\pi} - \frac{12}{\pi^2} \\ a_3 &= \frac{16}{\pi^3} - \frac{4}{\pi^2} \\ \end{flalign*}](../../assets/b887088273137948.png)


Let’s do a quick check by plotting the polynomial curve along with the original hill curve on the same figure:

![double hill](../../assets/f39ce9def51f8b15.png)


The blue curve is the original hill curve, and the red curve is our polynomial. It looks like they are about the same. Good.

The final step is to copy this hill four times, and piece them together so they make up an approximation of the sine curve.

![sines](../../assets/3e12fdce90351a91.png)


The blue curve is the original sine curve, and the red curve is our four hill curves pieced together. Looking good.

Here’s the C++ code for implementing the faster sine with the polynomial we just derived:

#define PI (3.1415926535f) #define HALF_PI (0.5f * PI) #define TWO_PI (2.0f * PI) #define TWO_PI_INV (1.0f / TWO_PI) inline float Hill(float x) { const float a0 = 1.0f; const float a2 = 2.0f / PI - 12.0f / (PI * PI); const float a3 = 16.0f / (PI * PI * PI) - 4.0f / (PI * PI); const float xx = x * x; const float xxx = xx * x; return a0 + a2 * xx + a3 * xxx; } float FastSin(float x) { // wrap x within [0, TWO_PI) const float a = x * TWO_PI_INV; x -= static_cast<int>(a) * TWO_PI; if (x < 0.0f) x += TWO_PI; // 4 pieces of hills if (x < HALF_PI) return Hill(HALF_PI - x); else if (x < PI) return Hill(x - HALF_PI); else if (x < 3.0f * HALF_PI) return -Hill(3.0f * HALF_PI - x); else return -Hill(x - 3.0f * HALF_PI); }

And the cosine curve is just the sine curve shifted by ![Rendered by QuickLaTeX.com \frac{\pi}{2}](../../assets/fb4adb336c085ad9.png)


float FastCos(float x) { return FastSin(x + HALF_PI); }

The performance gain is about 3.5x on my machine. This is probably not as impressive as some other hacks you may find on the internet, but it’s faster than the original sine function nonetheless. Besides, you get to practice approximating a function using polynomials!

By the way, it is not a good idea to approximate the tangent function using polynomial approximation, because there are points in the function that have infinite slopes. Trying to approximate such functions near the points of infinite slope with polynomials would produce polynomials that fluctuate in grate magnitude. You may approximate the tangent function using the trigonometric identity ![Rendered by QuickLaTeX.com tan \theta = \frac{sin \theta}{cos \theta}](../../assets/66b1341c9e534b53.png)

![Rendered by QuickLaTeX.com sin \theta](../../assets/1e60c78a18dac7b3.png)

![Rendered by QuickLaTeX.com cos \theta](../../assets/3ef35c2a1d122abf.png)


One thing about using LUTs- when they get big they are BAD for cache misses …. OK on small SRAM micros where there is no cache.

For such crucial operations like sine/cosine, I’d get rid of those branches. Maybe something

like this:

The branches were removed, but at the expense of more mults/adds. I don’t know if these mults by 0/1 will be optimized, need to read the generated code/measure etc, but that’s just the idea.

Very nice post though, obtaining complex functions like trig with just a few mults/adds is great! 🙂

I did a quick test on my machine using your code. Looks like the extra multiplications are not faster than the 4 branches. The branch-less implementation is only about 1.5x faster than

`std::sin`

on my machine.I wonder how this compares to a lookup table. http://en.wikipedia.org/wiki/Lookup_table#Computing_sines

I will try implementing the LUT version and compare the results in later posts. Thanks for the input!

Wrapping x is

`std::fmod`

, shouldn’t line 21 be`x -= static_cast(a) * TWO_PI`

?VC++’s implementation of

`std::fmod`

is just about the same speed as`std::sin`

on my machine, so I avoided using it. And yes, line 21 should be`x -= static_cast`(a) * TWO_PI

. Thanks for pointing it out.