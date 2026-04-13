---
title: 'Game Math: Approximation with Polynomial Curves | Ming-Lun "Allen" Chou |
  周明倫'
url: https://allenchou.net/2014/02/game-math-approximation-with-polynomial-curves/
author: Allen Chou
published: '2014-02-27'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

### Polynomials

A polynomial is an expression consisting of linear combination of products of variables raised to non-negative integer powers. In this post, I will specifically focus on polynomials of a single variable, namely polynomials of the form:

![Rendered by QuickLaTeX.com \[ P(x) = a_0 + a_1 x + a_2 x^2 + \dots + a_n x^n = \sum_{i = 0}^{n}{a_i x^i} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-61ca4bbf82483ea7b6dc192c882e7d78_l3.png)


The polynomial above are said to have __degree__ ![Rendered by QuickLaTeX.com n](../../assets/97eb473973e93376.png)

![Rendered by QuickLaTeX.com a_n](../../assets/b850edfc20e1a078.png)


### Polynomial Curves

We can create curves with polynomials by using the equation ![Rendered by QuickLaTeX.com y = P(x)](../../assets/bd8eb48d2d851c08.png)


For instance, we can create a parabola with ![Rendered by QuickLaTeX.com y = x^2](../../assets/4dbd066024113c34.png)


![parabola](../../assets/878d1922c5865fb0.png)



Or a down-facing parabola shifted from the origin: ![Rendered by QuickLaTeX.com y = -(x - 0.5) ^ 2 + 1](../../assets/a54a12c3366d86c6.png)


![parabola2](../../assets/74d297f800ade3c8.png)


### Approximating Curves with Polynomial Curves

For games, some mathematical functions are so expensive that it is beneficial to approximate them using polynomial curves. In general, the higher the degree of polynomial we use to approximate the function, the better the approximation will be.

So we have a function that we want to approximate, ![Rendered by QuickLaTeX.com y = f(x)](../../assets/d77c2906dbd29d1d.png)

![Rendered by QuickLaTeX.com n](../../assets/97eb473973e93376.png)

![Rendered by QuickLaTeX.com P(x) = a_0 + a_1 x + a_2 x^2 + \dots + a_n x^n](../../assets/248dcd40b7e636b8.png)

![Rendered by QuickLaTeX.com a_i](../../assets/dfe573b8d6630ef4.png)

![Rendered by QuickLaTeX.com (n + 1)](../../assets/bdc9ea663f767d6f.png)

![Rendered by QuickLaTeX.com (n + 1)](../../assets/bdc9ea663f767d6f.png)


How do we get the ![Rendered by QuickLaTeX.com (n + 1)](../../assets/bdc9ea663f767d6f.png)

![Rendered by QuickLaTeX.com f(x)](../../assets/45cfff1d70bd2498.png)

![Rendered by QuickLaTeX.com x = 0](../../assets/49204072d5e08c02.png)

![Rendered by QuickLaTeX.com x = 1](../../assets/83233175bd6a3be1.png)


![Rendered by QuickLaTeX.com \[ \begin{aligned} P(0) = f(0) \\ P(1) = f(1) \\ \end{aligned} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7ea85ba884e125787e74675aaa536e05_l3.png)


Sometimes matching the points on the function curve is not enough. We might want to also match the slopes of the curve at certain points. Say we also want to match the function curve’s slopes at ![Rendered by QuickLaTeX.com x = 0](../../assets/49204072d5e08c02.png)

![Rendered by QuickLaTeX.com x = 1](../../assets/83233175bd6a3be1.png)


![Rendered by QuickLaTeX.com \[ \begin{aligned} \left.{\frac{\mathrm{d} P}{\mathrm{d} x}}\right|_{x = 0} = \left.{\frac{\mathrm{d} f}{\mathrm{d} x}}\right|_{x = 0} \\ \left.{\frac{\mathrm{d} P}{\mathrm{d} x}}\right|_{x = 1} = \left.{\frac{\mathrm{d} f}{\mathrm{d} x}}\right|_{x = 1} \end{aligned} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-feccfba4aac732c2261f9e29aa38275e_l3.png)


Four equations means four __conditions__ for our approximation. In order to satisfy ![Rendered by QuickLaTeX.com n](../../assets/97eb473973e93376.png)

![Rendered by QuickLaTeX.com (n - 1)](../../assets/050e13f3dd44598d.png)

![Rendered by QuickLaTeX.com n](../../assets/97eb473973e93376.png)


In this case, we need a cubic polynomial, ![Rendered by QuickLaTeX.com P(x) = a_0 + a_1 x + a_2 x^2 + a_3 x^3](../../assets/4bcb6e438bed0d2e.png)


Let’s pick the exponential function, ![Rendered by QuickLaTeX.com f(x) = e^x](../../assets/0d00f9c9bdc3c719.png)

![Rendered by QuickLaTeX.com P(x)](../../assets/d21028278837967e.png)

![Rendered by QuickLaTeX.com a_0](../../assets/67d48dbf36253f67.png)

![Rendered by QuickLaTeX.com a_1](../../assets/128281ca0b54d6bf.png)

![Rendered by QuickLaTeX.com a_2](../../assets/c52bc92ba5384f15.png)

![Rendered by QuickLaTeX.com a_3](../../assets/2ae622ba433e9743.png)


![Rendered by QuickLaTeX.com \begin{flalign*} P(0) &= a_0 = f(0) = 1 \\ P(1) &= a_0 + a_1 + a_2 + a_3 = f(1) = e \\ \left.{\frac{\mathrm{d} P}{\mathrm{d} x}}\right|_{x = 0} &= a_1 = \left.{\frac{\mathrm{d} e^x}{\mathrm{d} x}}\right|_{x = 0} = 1 \\ \left.{\frac{\mathrm{d} P}{\mathrm{d} x}}\right|_{x = 1} &= a_1 + 2 a_2 + 3 a_3 = \left.{\frac{\mathrm{d} e^x}{\mathrm{d} x}}\right|_{x = 1} = e \end{flalign*}](../../assets/4b305b9e46670b5a.png)


After removing all the noise, we get:

![Rendered by QuickLaTeX.com \begin{flalign*} a_0 &= 1 \\ a_0 + a_1 + a_2 + a_3 &= e \\ a_1 &= 1 \\ a_1 + 2 a_2 + 3 a_3 &= e \end{flalign*}](../../assets/bbc2db00a5477959.png)


We can then solve this system of equations and obtain the coefficients:

![Rendered by QuickLaTeX.com \begin{flalign*} a_0 &= 1 \\ a_1 &= 1 \\ a_2 &= 2e - 5 \\ a_3 &= -e + 3 \end{flalign*}](../../assets/1272cf04e7f8f75b.png)


And here’s the polynomial that we’ll use to approximate ![Rendered by QuickLaTeX.com y = f(x) = e^x](../../assets/2bbe1545d8568f0b.png)


![Rendered by QuickLaTeX.com \[ P(x) = 1 + x + (2e - 5) x^2 + (-e + 3) x^3 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-896a7ac5bc90b2373f9915da622ec981_l3.png)


Let’s see how close we are by plotting ![Rendered by QuickLaTeX.com y = e^x](../../assets/26cbc69d6d9daf83.png)

![Rendered by QuickLaTeX.com y = P(x)](../../assets/bd8eb48d2d851c08.png)


![exponential match](../../assets/bacca9df2b114d1c.png)


The blue curve is the exponential curve, and the red curve is the polynomial approximation. They are almost identical between ![Rendered by QuickLaTeX.com x = 0](../../assets/49204072d5e08c02.png)

![Rendered by QuickLaTeX.com x = 1](../../assets/83233175bd6a3be1.png)

![Rendered by QuickLaTeX.com x = 0](../../assets/49204072d5e08c02.png)

![Rendered by QuickLaTeX.com x = 1](../../assets/83233175bd6a3be1.png)


The approximating polynomial will be accurate around the points you choose for the conditions (in this example, ![Rendered by QuickLaTeX.com x = 0](../../assets/49204072d5e08c02.png)

![Rendered by QuickLaTeX.com x = 1](../../assets/83233175bd6a3be1.png)


### Approximation with Polynomial Curves

This is how you would approximate a function with polynomial curves. In general, the more accurate you want the polynomial curve to be, the higher the degree of the polynomial will be, and the more coefficients you’ll have to solve for.