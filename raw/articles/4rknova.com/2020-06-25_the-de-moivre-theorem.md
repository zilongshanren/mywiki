---
title: The De Moivre theorem
url: https://www.4rknova.com/blog/2020/06/25/demoivre
author: Nikolaos Papadopoulos
published: '2020-06-25'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Complex numbers

A complex number can be expressed in the form:

\[z = a + ib\] \[a, b \in \mathbb{R}\]where \(i\) is a solution of the equation:

\[x^2 = −1\]As no real number satisfies this equation, \(i\) is called an imaginary number. In this notation, \(a\) is called the real part and \(b\) is called the imaginary part of the complex number [1].

A complex number can also be express in its polar form as:

\[z = r (cos(\theta) + i sin(\theta))\] \[r, \theta \in \mathbb{R}\]# The De Moivre theorem

The De Moivre theorem is named after the French mathematician Abraham de Moivre and it is used to calculate powers of complex numbers. The formula is expressed in polar coordinates \((r,\theta)\) and states the following:

\[(\cos(x) + i\sin(x))^n = \cos(nx) + i\sin(nx)\] \[x \in \mathbb{R}, n \in \mathbb{Z}\]# Generalized cartesian form

Below, we’ll derive a generalized form that can be used in 2D cartesian representations of complex numbers.

We want to calculate the nth power of a complex number:

\[(a + ib)^n\]The first step is to convert from cartesian to polar coordinates.

\[r = \sqrt{a^2 + b ^2}\] \[\theta = \arctan{\frac{b}{a}}\]Next, the theorem is applied.

\[r = (\sqrt{a^2 + b^2})^n\] \[\theta = n \arctan{\frac{b}{a}}\]Lastly, the polar coordinates are converted back to their cartesian form.

\[\,\,\, x = r \cos(\theta) = (\sqrt{a^2 + b^2})^n \cos(n \arctan(\frac{b}{a}))\] \[\,\,\, y = r \sin(\theta) = (\sqrt{a^2 + b^2})^n \sin(n \arctan(\frac{b}{a}))\]# Power of 2

For \(n = 2\), we can simplify the formulas further, so as to avoid the expensive arctangent calculation.

The following trigonometric identities will be used:

[1] \(\,\,\, \cos(\arctan(x)) = \frac{1}{\sqrt{1 + x^2}}\)

[2] \(\,\,\, \sin(\arctan(x)) = \frac{x}{\sqrt{1 + x^2}}\)

[3] \(\,\,\, \cos(2x) = \cos^2(x) - \sin^2(x)\)

[4] \(\,\,\, \sin(2x) = 2\sin(x)\cos(x)\)

Starting with the generalized formula from above for x:

\[\,\,\, x = (\sqrt{a^2 + b^2})^2 \cos(2 \arctan(\frac{b}{a}))\]using the 3rd trigonometric identity:

\[\,\,\, x = (\sqrt{a^2 + b^2})^2 (\cos^2(\arctan(\frac{b}{a})) - \sin^2(\arctan(\frac{b}{a})))\]then using identities 1 and 2:

\[\,\,\, x = (a^2 + b^2) (\frac{1}{\sqrt{1 + (\frac{b}{a})^2}})^2 - (a^2 + b^2) (\frac{\frac{b}{a}}{\sqrt{1 + (\frac{b}{a})^2}})^2\] \[\,\,\, x = (a^2 + b^2) ((\frac{1}{1 + (\frac{b}{a})^2}) - (\frac{(\frac{b}{a})^2}{1 + (\frac{b}{a})^2}))\] \[\,\,\, x = (a^2 + b^2) (\frac{1}{\frac{a^2+b^2}{a^2}} - \frac{(\frac{b}{a})^2}{\frac{a^2+b^2}{a^2}})\] \[\,\,\, x = (a^2 + b^2) (\frac{a^2}{a^2+b^2} - \frac{b^2 a^2}{a^2(a^2+b^2)})\] \[\,\,\, x = (a^2 + b^2) (\frac{a^2}{a^2+b^2} - \frac{b^2}{a^2+b^2})\] \[\,\,\, x = a^2 - b^2\]Similarly for y:

\[\,\,\, y = (\sqrt{a^2 + b^2})^2 \sin(2 \arctan(\frac{b}{a}))\]using the 4th trigonometric identity:

\[\,\,\, y = (a^2 + b^2) 2 \sin(\arctan(\frac{b}{a}))\cos(\arctan(\frac{b}{a}))\]and again using identities 1 and 2:

\[\,\,\, y = (a^2 + b^2) 2 (\frac{\frac{b}{a}}{\sqrt{1 + (\frac{b}{a})^2}})(\frac{1}{\sqrt{1 + (\frac{b}{a})^2}})\] \[\,\,\, y = 2 (a^2 + b^2) \frac{b}{a (1 + (\frac{b}{a})^2)}\] \[\,\,\, y = 2 (a^2 + b^2) \frac{b}{a + \frac{b^2}{a}}\] \[\,\,\, y = 2 (a^2 + b^2) \frac{b}{\frac{a^2 + b^2}{a}}\] \[\,\,\, y = 2 (a^2 + b^2) \frac{ab}{a^2 + b^2}\] \[\,\,\, y = 2ab\]# Implementation

An implementation of De Moivre in GLSL is provided below.

```
vec2 DeMoivre(vec2 p, float e)
{
// Convert to polar coords
float r = sqrt(dot(p,p));
float t = atan(p.y, p.x);
// Apply DeMoivre theorem
r = pow(r, e);
t = e * t;
// Convert back to cartesian coords
return r * vec2(cos(t), sin(t));
}
```


A practical application of the De Moivre theorem exists in the domain of fractals. The popular Mandelbrot set can use the specialized ‘power of 2’ form we saw above. The Mandelbrot set was explored in a [previous blog post](https://www.4rknova.com/blog/2013/01/27/fractals-mandelbrot). By generalizing the Mandelbrot formula to use arbitrary powers, the Multibrot superset is calculated.

The visualization below shows what the Multibrot set looks like for progressively higher powers.