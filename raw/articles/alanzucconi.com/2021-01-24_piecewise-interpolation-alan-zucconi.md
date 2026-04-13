---
title: Piecewise Interpolation - Alan Zucconi
url: https://www.alanzucconi.com/2021/01/24/piecewise-interpolation/
author: Alan Zucconi
published: '2021-01-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of the tutorial dedicated to one of the most used Mathematical tools in Game Development: linear interpolation! In this part, we will explore how to extend the concept of linear interpolation to non-linear mappings. The final part will explore how to use them to correct colour curves.

- Part 1:
[Linear Interpolation](https://www.alanzucconi.com/?p=12843) - Part 2:
**Piecewise Interpolation** - Part 3:
[Color Curve Correction](https://www.alanzucconi.com/?p=12877)

You can find a link to download the C# scripts and the Unity package used at the end of this post.

## Introduction

In the first part of this series, we introduced a mathematical technique known as **linear interpolation**—*lerp* for short—which can be rather handy for game developers and programmers in general. From “blending” colours to “moving” between points, lerp is a very well known and loved tool that is present—in one form or another—in virtually all libraries and engines.

In its most basic form, lerp takes a number from ![Rendered by QuickLaTeX.com \left[0, 1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ac0ef5000a04390b73f0f437f914143d_l3.png)

![Rendered by QuickLaTeX.com \left[a, b\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b86fa516b1e81febd67b558baea849a8_l3.png)

**inverse lerp**. However, we can generalise linear interpolation so that it remaps a number ![Rendered by QuickLaTeX.com x \in \left[a, b\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-50e38ece4e9fc11fd1b0861bd6d294ca_l3.png)

![Rendered by QuickLaTeX.com \left[c, d\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-9e601090d7c25be74cf47eec386330bb_l3.png)

**map**, but in this tutorial we will keep call referencing it a a more generalised version of lerp.

The lerping equation is also rather simple:

(1) ![Rendered by QuickLaTeX.com \begin{equation*} y = c + \frac{d-c}{b-a} \left(x - a\right)\end{equation*}](../../assets/1fd388192074229d.png)


and has a very well known geometrical interpretation. The original interval ![Rendered by QuickLaTeX.com \left[a, b\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b86fa516b1e81febd67b558baea849a8_l3.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com \left[0, 1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ac0ef5000a04390b73f0f437f914143d_l3.png)

![Rendered by QuickLaTeX.com \left[c, d\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-9e601090d7c25be74cf47eec386330bb_l3.png)


![](../../assets/fb72a68a0a032428.png)


![](../../assets/fb72a68a0a032428.png)

Equation ([1](https://www.alanzucconi.com#id2728864646)) easily translates to the following function, giving us an easy and efficient way to lerp between numbers from any two arbitrary intervals:

public static float Lerp (float x0, float x1, float y0, float y1, float x) { float d = x1 - x0; if (d == 0) return (y0 + y1) / 2; return y0 + (x - x0) * (y1 - y0) / d; }

## Easing Curves

One of linear interpolation’s biggest strength—its simplicity—is also one of its worst limitations. As the name suggest, lerp can only be used to link two objects with a *linear *relationship. Geometrically, this means that lerp can only represents linear functions.

The diagram below shows how lerping from ![Rendered by QuickLaTeX.com \left[a, b\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b86fa516b1e81febd67b558baea849a8_l3.png)

![Rendered by QuickLaTeX.com \left[c, d\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-9e601090d7c25be74cf47eec386330bb_l3.png)

![Rendered by QuickLaTeX.com \left(a, c\right)](../../assets/c834a59a35e5742c.png)

![Rendered by QuickLaTeX.com \left(b, d\right)](../../assets/e5ce2993d2c0c3e4.png)


![](../../assets/5e57e83a04988c7e.png)


![](../../assets/5e57e83a04988c7e.png)

This becomes apparent if you move an object lerping between its start and target positions. Because the movement is movement is linear, the object will start and stop moving very suddenly, resulting in a non-realistic behaviour.

Ones easy way to fix this is to use the so-called **easing curves** of functions. Those are mathematical functions that takes a number between ![Rendered by QuickLaTeX.com \left[0, 1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ac0ef5000a04390b73f0f437f914143d_l3.png)

![Rendered by QuickLaTeX.com \left[0, 1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ac0ef5000a04390b73f0f437f914143d_l3.png)


Linear interpolation always passes through the interval ![Rendered by QuickLaTeX.com \left[0, 1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ac0ef5000a04390b73f0f437f914143d_l3.png)


Easing curves are very popular in UX and web design, where they can be used to create smooth and reactive movements.

The table below, from [1ucasvb’s lab](https://1ucasvb.tumblr.com/post/44666043888/easing-functions-are-an-immensely-useful-tool-for), shows some common ones, and the overall effect they have on lerp:

![](../../assets/d3c4c267ee54c091.gif)


![](../../assets/d3c4c267ee54c091.gif)

### ⭐ Recommended Unity Assets

## Piecewise Interpolation

Thanks to easing curves, linear interpolation can be used to create some more nuanced movements. However, this does not solve all of the problems that we might encounter, or the many problems that lerp can solve.

Linear interpolation only models a single line. But it is possible to approximate any arbitrary curve with a series of linear segments. The diagram below shows a curve (solid grey) being approximated with four segments. Each segment is linear, meaning that by using lerp on four different segments we can have a rough approximation of the original curve:

![](../../assets/b791123e235c93f0.png)


![](../../assets/b791123e235c93f0.png)

This techniques is known as **piecewise linear interpolation**, although sometimes **multilinear interpolation** is used as well (not to be confused with [multivariate interpolation](https://en.wikipedia.org/wiki/Multivariate_interpolation), which is linear interpolation in a higher dimension).

Piecewise interpolation can be a good way to approximate non-linear functions that would otherwise be impossible to model with lerp alone. This has many applications. For instance, it can be used to replace a very expensive function with a relatively inexpensive linear approximation. All that is needed is to sample the value of the function at some points ![Rendered by QuickLaTeX.com x_i](../../assets/71a60f5d247cb117.png)

![Rendered by QuickLaTeX.com y_i](../../assets/a35915d5ac6b958c.png)


### Construction

Let’s imagine that we have a function `F`

that we want to approximate with piecewise interpolation. What we need is to store the values at which the function was sampled (`float[] Xs`

) and its results (`float[] Ys`

). The snipped below samples the function `F`

every `xStep`

, in the interval between `xMin`

and `xMax`

:

float[] Xs new float[N]; float[] Ys new float[N]; // Samples the function F in the [xMin, xMax] interval float xStep = (xMax - xMin) / (N-1); for (float x = xMin; x <= xMax; x += xStep) { Xs[i] = x; Ys[i] = F(x); }

The arrays `Xs`

and `Ys`

is really all we need to perform piecewise interpolation.

Additionally, nothing stops us from using intervals of different lengths on the X axis. This means that if such an uniform sampling is underperforming in certain parts of the function, we can increase its precision where needed and use fewer points where the function is relatively well behaved.

### Implementation

Once `Xs`

and `Ys`

are available, performing piecewise interpolation means taking an arbitrary value `x`

and finding in which segment it is contained. This means finding the `index`

inside the array so that `Xs[index-1] <= Xs[index]`

.

There are countless way to do this. The naïve one is to loop through `Xs`

, stopping when `x > Xs[index]`

. However, it is not the most efficient way; in fact, it can potentially loop through the entire array. When there is the risk that an algorithm will loop through the entire length of an array to perform its task, it is said that it has a **liner complexity**. The [Big O notation](https://en.wikipedia.org/wiki/Big_O_notation#:~:text=Big%20O%20notation%20is%20a,a%20particular%20value%20or%20infinity.&text=In%20computer%20science%2C%20big%20O,as%20the%20input%20size%20grows.) is often used to summarise this: ![Rendered by QuickLaTeX.com \mathcal{O}\left(n\right)](../../assets/21591445bac158bc.png)


However, we can take advantage of the fact that the values inside `Xs`

are sorted. After all, when you are searching for a word in a dictionary, you do not leaf through the pages starting from the cover! An efficient approach to find an value inside an array is to use the so-called **binary search**. In a nutshell, at every step it splits the array into two parts, and focuses on the one that should contain the value:

![](../../assets/0f58fa10dcd8c145.png)


![](../../assets/0f58fa10dcd8c145.png)

With every new iteration, binary search reduces the search space in half. If the value is not present in the array, it will continue to subdivide until it reaches a single element. The number of steps is, therefore, logarithmic in the length of the array. This is because ![Rendered by QuickLaTeX.com \log_2 \left( n\right)](../../assets/9a1eae0d55397026.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com 2](../../assets/74857f8384da7ff4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

**logarithmic complexity**; or ![Rendered by QuickLaTeX.com \mathcal{O}\left(\log{n}\right)](../../assets/1292507855e760f5.png)


Luckily for us, C# has a good implementation of the binary search algorithm: [Array.BinarySearch](https://docs.microsoft.com/en-us/dotnet/api/system.array.binarysearch?view=net-5.0#System_Array_BinarySearch__1___0_____0_):

int index = Array.BinarySearch(Xs, s);

The returned `index`

is the exact position in the array `Xs`

where the value `x`

was found. If not found, the method returns a negative number which, according to the official .NET documentation:

The index of the specified

`value`

in the specified`array`

, if`value`

is found; otherwise, a negative number.If

`value`

is not found and`value`

is less than one or more elements in`array`

, the negative number returned is the bitwise complement of the index of the first element that is larger than`value`

.If

`value`

is not found and`value`

is greater than all elements in`array`

, the negative number returned is the bitwise complement of (the index of the last element plus 1).

This allows us to design a simple function to finally perform piecewise interpolation:

public static float Lerp (float[] Xs, float[] Ys, float x) { // Finds the right interval int index = Array.BinarySearch(Xs, x); // If the index is non-negative // an exact match has been found! if (index >= 0) return Ys[index]; // If the index is negative, it represents the bitwise // complement of the next larger element in the array. index = ~index; // index == 0 => result smaller than Ys[0] if (index == 0) return Ys[0]; // index == Ys.Length => result greater than Ys[Ys.Length-1] if (index == Ys.Length) return Ys[Ys.Length - 1]; // else => result between Ys[index-1] and Ys[index] // Lerp return Lerp ( Xs[index - 1], Xs[index], Ys[index - 1], Ys[index], x ); }

### Inverting Functions

There is another vey useful case for the piecewise linear interpolations: inverting functions. Let’s imagine a function ![Rendered by QuickLaTeX.com F](../../assets/43336663814e94d2.png)

![Rendered by QuickLaTeX.com y=F\left(x\right)](../../assets/bf1d6a1be08cab2d.png)

![Rendered by QuickLaTeX.com F](../../assets/43336663814e94d2.png)

![Rendered by QuickLaTeX.com F^{-1}](../../assets/a263fe4687af5096.png)

*not* ![Rendered by QuickLaTeX.com \frac{1}{F}](../../assets/b0ef41846838386d.png)

![Rendered by QuickLaTeX.com F^{-1}\left(y\right)=x](../../assets/2f44af88f51817be.png)


Inverting a function is highly non-trivial and computationally expensive. Not all functions admit an inverse, while some are not in a *closed-form* (meaning that they cannot be calculated with a finite number of “standard” operations).

Geometrically speaking, however, inverting a functions is easy. All we need to do is to flip the X and Y axes! For this reason, if `Lerp(Xs, Ys, x)`

is the piecewise approximation for ![Rendered by QuickLaTeX.com F](../../assets/43336663814e94d2.png)

`Lerp(Ys, Xs, y)`

is the piecewise approximation for ![Rendered by QuickLaTeX.com F^{-1}](../../assets/a263fe4687af5096.png)


In all fairness, things are a bit more complicated. In fact, for this to work it is necessary that even the produced `Ys`

are sorted. If not, function cannot be inverted as there would be multiple possible answers for a single value.

## Gradient Interpolation

One very interesting applications of piecewise linear interpolation is the creation of colour gradients. The original code presented above was designed for `float`

s, so a few small changes are required:

public static Color Lerp (float[] Xs, Color[] Cs, float x) { ... // Color Lerp return Color.Lerp ( Xs[index - 1], Xs[index], Cs[index - 1], Cs[index], x ); }

In the code above, the array of `float`

s has been replaced with an array of `Color`

s.

Now, it is easy to create a hue gradient just with an array of colours and their positions:

Color[] Cs = new Color[] { Color.red, // 0° Color.yellow, // 60° Color.green, // 120° Color.cyan, // 180° Color.blue, // 240° Color.purple, // 300° Color.red, // 360° }; float[] Xs = new float[] { 0, 60, 120, 180, 240, 300, 360 }; Color c = Lerp (Xs, Cs, 30); // Between red and yellow

![](../../assets/9878367f99f1faf7.png)

## What’s Next…

The third and final part of this series will show how piecewise linear interpolation can be used to correct colour curves and gradients.

- Part 1:
[Linear Interpolation](https://www.alanzucconi.com/?p=12843) - Part 2:
**Piecewise Interpolation** - Part 3:
[Color Curve Correction](https://www.alanzucconi.com/?p=12877)

### Download Unity Package

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

The [Standard package](https://www.patreon.com/posts/46612886) contains the script to perform piecewise linear interpolation. It uses extension methods which allows to easily interpolated numbers, vectors, colours and even quaternions! The [Advanced package](https://www.patreon.com/posts/46613014), instead, contains a test scene which also shows how to correct colour curves.

## Leave a Reply Cancel reply