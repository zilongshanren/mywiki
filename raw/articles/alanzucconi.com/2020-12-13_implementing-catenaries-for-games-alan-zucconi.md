---
title: Implementing Catenaries for Games - Alan Zucconi
url: https://www.alanzucconi.com/2020/12/13/catenary-2/
author: Alan Zucconi
published: '2020-12-13'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of the series dedicated to the catenary, the mathematical object used to model hanging wires, cables and chains. This post will show how to implement catenaries in a game engine like Unity.

- Part 1.
[The Mathematics of Catenary](https://www.alanzucconi.com/?p=9289) - Part 2.
**Implementing Catenaries for Games**

You can find the Unity package to create catenaries in Unity at the end of the post.

In the previous part of this short online course, we have introduced *catenaries*. A catenary is a mathematical objects that can be used to model chains anchored between two points.

The simplest equation for a catenary is expressed in terms of ![Rendered by QuickLaTeX.com \cosh](../../assets/8e9cdbfef75bb878.png)

*hyperbolic cosine*. Loosely speaking, that is the equivalent of the more well-known *cosine *function, but on a *hyperbola* rather than a *circle*.

The equation of a catenary is:

(1) ![Rendered by QuickLaTeX.com \begin{equation*} y=a \cosh{\left(\frac{x-p}{a}\right)}+q\end{equation*}](../../assets/f0da25c4d5a12106.png)


and has three parameter:


: the size/scale;

: the horizontal shift;

: the vertical shift.

Since many games features hanging wires and chains, getting catenaries right is pretty much critical. A friendly tool should allow to place a chains from three pieces of information:

- Two points,

and

, which the chain has to pass through; - The length of the chain between

and

is

.

We can satisfy these constraints by carefully selecting the three parameters of ([1](https://www.alanzucconi.com#id436391346)):

(2) ![Rendered by QuickLaTeX.com \begin{equation*} p=\frac{x_1+x_2-a \ln{\left(\frac{l+v}{l-v}\right)}}{2}\end{equation*}](../../assets/627fa39a1f3028b9.png)


(3) ![Rendered by QuickLaTeX.com \begin{equation*} q=\frac{y_1+y_2-l \coth{\left(\frac{h}{2a}\right)} }{2}\end{equation*}](../../assets/9f587eff547ea67d.png)


where:

(4) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{split}h & = x_2 - x_1 \\v & = y_2 - y_1 \\\end{split}\end{equation*}](../../assets/6fd311af041e82d0.png)


One major problem is ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

![Rendered by QuickLaTeX.com q](../../assets/b43061656d5cc7df.png)


The rest of this post will explore alternative ways to calculate ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)


## Finding *a*…

While it is true that there is no closed-form for ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)


(5) ![Rendered by QuickLaTeX.com \begin{equation*} \sqrt{l^2-v^2}=2 a \sinh{\left(\frac{h}{2 a}\right)}\end{equation*}](../../assets/6cdfe67803246dc3.png)


As it turns out, this is a [transcendental equation](https://en.wikipedia.org/wiki/Transcendental_equation) from which ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

[5](https://www.alanzucconi.com#id3778039334)) in such such a way that the equation looks like ![Rendered by QuickLaTeX.com a=...](../../assets/bf19469d6b3b75c6.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

[5](https://www.alanzucconi.com#id3778039334)) that allow to do that, but they will all require an infinite number of operations (such as an infinite series or an integral).

For this reason, we need a different way must be taken in order to find the value of ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)


Geometrically speaking, solving ([5](https://www.alanzucconi.com#id3778039334)) is not that complicated: equating two functions means plotting and finding the point in which they touch. This is particularly easy to visualise for ([5](https://www.alanzucconi.com#id3778039334)), since the left-hand side of the equation (![Rendered by QuickLaTeX.com \sqrt{l^2-v^2}](../../assets/46056d2a9884a775.png)

[5](https://www.alanzucconi.com#id3778039334)) (![Rendered by QuickLaTeX.com 2 a \sinh{\left(\frac{h}{2 a}\right)}](../../assets/29d19e3d5471b469.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)


The chart below plots the two sides of ([5](https://www.alanzucconi.com#id3778039334)) when ![Rendered by QuickLaTeX.com h=v=1](../../assets/87112f5addc3907c.png)

![Rendered by QuickLaTeX.com l=2](../../assets/99003fba4f73a83f.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com 0.2613328](../../assets/8f5e57f1c57ed996.png)


## Numerical Integration

In general, finding the intersections of two functions is a rather complex problems, and there are is guarantee that a single point exists. In this specific case, however, we can guarantee that exactly one solution in the range ![Rendered by QuickLaTeX.com \left(0, +\infty\right)](../../assets/cc2a714d3637256e.png)


We can prove that by studying both functions involved:


is a constant value which is the result of a square root; it means it is strictly positive;

is monotonically decreasing in the interval

, and tends to

when

tends to

.

This means that, at some point, ![Rendered by QuickLaTeX.com 2 a \sinh{\left(\frac{h}{2 a}\right)}](../../assets/29d19e3d5471b469.png)

![Rendered by QuickLaTeX.com \sqrt{l^2-v^2}](../../assets/46056d2a9884a775.png)


With this knowledge, we can already come up with a simple algorithm to estimate ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com a=0](../../assets/099e0a3b30f47f49.png)

![Rendered by QuickLaTeX.com \sqrt{l^2-v^2} \geq 2 a \sinh{\left(\frac{h}{2 a}\right)}](../../assets/f7f8d3ccecb50756.png)


const double IntervalStep = 0.01; double a = 0; do { a += IntervalStep; } while (Math.Sqrt(Math.Pow(l, 2) - Math.Pow(v, 2)) < 2 * a * Math.sinh(h/(2*a)));

The precision of this method can be increased by using a smaller increment for `a`

.

While this works, it is very slow and it can take several tens of thousands of iterations, even for a relatively small catenary.

## Bisection Method

A better approach relies on two steps. First, we can find a rough estimate using the method shown above (for instance, using `IntervalStep = 1.0;`

). This helps us finding an interval an interval in which the right value of ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)


There are many techniques to find the solution of an equation that lies in an interval. In this case, a simple and effective one is the [bisection method](https://en.wikipedia.org/wiki/Bisection_method), which many programmers will recognise as a variant of the [binary search algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm).

We can understand how it work with the help of a simple example. Let’s imagine that you are trying to find a specific word in a dictionary. Your best guess is to open the dictionary on an arbitrary page: let’s say exactly in the middle. Perhaps you have been lucky, and the word you were searching for is just there; more likely, it will not. But since al words are in order, you can now tell in which half of the dictionary you need to keep searching.

Now, you can ignore the other half and repeat the procedure again, opening the dictionary in the middle of the section you know has to contain the word. By repeating this many times, you will eventually reach to the page containing the word you are looking for. With every iteration, the binary search algorithm halves the search space. This is way more efficient than linearly searching for the desires item in a list starting from its first element.

![](../../assets/0f58fa10dcd8c145.png)


![](../../assets/0f58fa10dcd8c145.png)

The same method can be used here. We have an interval in which the solution should be (let’s call it `a_prev`

, `a_next`

), and we can iteratively split it in two halves, repeating the process until the interval size is arbitrarily small. When this is running on an actual machine, it is very unlikely we will find the exact, theoretical value of ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

[Floating-Point Arithmetic](https://www.alanzucconi.com/2020/08/03/floating-point-arithmetic/).

In our case, we know which half of the interval we should keep searching, because on one side ![Rendered by QuickLaTeX.com a \sinh{\left(\frac{h}{2 a}\right)}](../../assets/aadac7053e5843f4.png)

![Rendered by QuickLaTeX.com \sqrt{l^2-v^2}](../../assets/46056d2a9884a775.png)


const float Precision = 0.0001; double a_prev = a - IntervalStep; double a_next = a; do { a = (a_prev + a_next) / 2f; if (Math.Sqrt(Math.Pow(l, 2) - Math.Pow(v, 2)) < 2 * a * Math.sinh(h/(2*a))) a_prev = a; else a_next = a; } while (a_next - a_prev > Precision);

If we want to be extra safe, we could also add another condition to make sure that we exit after a maximum numbers of iterations.

## A Practical Example

The interactive charts below allow to play with the parameters of a catenary: one of its anchor points, ![Rendered by QuickLaTeX.com P_2](../../assets/2e2bcf5cc12d64bd.png)

![Rendered by QuickLaTeX.com l](../../assets/dacf99a2de8dda2c.png)

![Rendered by QuickLaTeX.com \sqrt{l^2-v^2}](../../assets/46056d2a9884a775.png)

![Rendered by QuickLaTeX.com 2 a \sinh{\left(\frac{h}{2 a}\right)}](../../assets/29d19e3d5471b469.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)


This is facilitated by the fact that ![Rendered by QuickLaTeX.com 2 a \sinh{\left(\frac{h}{2 a}\right)}](../../assets/29d19e3d5471b469.png)

![Rendered by QuickLaTeX.com a=0](../../assets/099e0a3b30f47f49.png)

![Rendered by QuickLaTeX.com \sqrt{l^2-v^2}](../../assets/46056d2a9884a775.png)


If you are interested in a more detailed analysis of how to solve ([5](https://www.alanzucconi.com#id3778039334)) numerically, you can have a look at [this article](https://math.stackexchange.com/questions/1000447/finding-the-catenary-curve-with-given-arclength-through-two-given-points) on StackExchange.

## From 2D to 3D…

…

## Conclusion

This post concludes our journey to explore the mathematics and implementation of catenaries in videogame.

- Part 1.
[The Mathematics of Catenary](https://www.alanzucconi.com/?p=9289) - Part 2.
**Implementing Catenaries for Games**

### Download Unity Package

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

There are two different Unity packages available for this tutorial. They contain a simple library to draw efficiently catenaries, which you can use in your games. Both packages are available through Patreon.

![](../../assets/bfda1c83d43fb59d.gif)


![](../../assets/bfda1c83d43fb59d.gif)

The [Standard package](https://www.patreon.com/posts/44985024) contains the scripts to draw catenaries in 3D and 3D, along with a test scene. The [Advanced package](https://www.patreon.com/posts/45357589/) contains support for rigged models (such as corded cables or chains), along with some advanced code to sample catenaries uniformly.

## Leave a Reply Cancel reply