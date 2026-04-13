---
title: Linear Interpolation - Alan Zucconi
url: https://www.alanzucconi.com/2021/01/24/linear-interpolation/
author: Alan Zucconi
published: '2021-01-24'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will explore one of the most used Mathematical tools in Game Development: linear interpolation! This first post will focus on its Mathematical definition and implementation. The following parts of this series will explore how to extend linear interpolation to non-linear mappings, and how to use them to correct colour curves.

- Part 1:
**Linear Interpolation** - Part 2:
[Piecewise Interpolation](https://www.alanzucconi.com/?p=12846) - Part 3:
[Color Curve Correction](https://www.alanzucconi.com/?p=12877)

You can find a link to download the C# scripts and the Unity package used at the end of this post.

## Linear Interpolation

One of the most useful—and somewhat underrated—functions in Game Development is **lerp**. Shorthand for **linear interpolation**, you can imagine lerp as a way to “blend” or “move” between two objects, such as points, colours and even angles.

Virtually every software comes with a function to perform linear interpolation. Unity, for instance, has several; the most well-known being being `Mathf.Lerp`

. It takes two numbers, namely ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com b](../../assets/0bcd696a7c0431b0.png)

![Rendered by QuickLaTeX.com t](../../assets/50e9745164dcf617.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


The result is simple: when ![Rendered by QuickLaTeX.com t=0](../../assets/6c6cee41bddf42e5.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com t=1](../../assets/09d4c8cafd13cdb0.png)

![Rendered by QuickLaTeX.com b](../../assets/0bcd696a7c0431b0.png)

![Rendered by QuickLaTeX.com t=0.5](../../assets/9a78c8e0d7e2b2a8.png)

![Rendered by QuickLaTeX.com \frac{a+b}{2}](../../assets/01f3d85885933f35.png)


In a nutshell, the parameter ![Rendered by QuickLaTeX.com t](../../assets/50e9745164dcf617.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com b](../../assets/0bcd696a7c0431b0.png)

![Rendered by QuickLaTeX.com \left[0, 1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ac0ef5000a04390b73f0f437f914143d_l3.png)

![Rendered by QuickLaTeX.com \left[a, b\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b86fa516b1e81febd67b558baea849a8_l3.png)


(1) ![Rendered by QuickLaTeX.com \begin{equation*} c = a + \left(b-a\right)*t\end{equation*}](../../assets/f6dfda162ef6a3e5.png)


This equation might seem confusing at first, but it has a very simple geometrical interpretation, as seen in the diagram below. The value of ![Rendered by QuickLaTeX.com t](../../assets/50e9745164dcf617.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com b-a](../../assets/38a058081613537b.png)

![Rendered by QuickLaTeX.com 0](../../assets/621a9e9e59af40e4.png)

![Rendered by QuickLaTeX.com b-a](../../assets/38a058081613537b.png)

![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)


![](../../assets/77bd2317aa5d6416.png)


![](../../assets/77bd2317aa5d6416.png)

### Inverse Lerp

Some libraries also feature a complementary function; `Mathf.InverseLerp`

, in case of Unity. As the name suggests, inverse lerp does exactly the opposite of what lerp does: it remaps a number in the interval ![Rendered by QuickLaTeX.com \left[a, b\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b86fa516b1e81febd67b558baea849a8_l3.png)

![Rendered by QuickLaTeX.com \left[0, 1\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-ac0ef5000a04390b73f0f437f914143d_l3.png)


(2) ![Rendered by QuickLaTeX.com \begin{equation*} t = \frac{c - a}{b-a}\end{equation*}](../../assets/21421cb2fa30a8d8.png)


A degenerate case can occur when ![Rendered by QuickLaTeX.com a=b](../../assets/d39ab74b9d1ee2b5.png)

![Rendered by QuickLaTeX.com t=0.5](../../assets/9a78c8e0d7e2b2a8.png)


Even ([2](https://www.alanzucconi.com#id1789463290)) can be interpreted geometrically. In this case, the exact same operations of lerp are preformed, but in reverse:

![](../../assets/398c84aab8117aa6.png)


![](../../assets/398c84aab8117aa6.png)

### Linear Mapping

With these two functions, it is possible to remap any arbitrary value ![Rendered by QuickLaTeX.com x \in \left[a, b\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-50e38ece4e9fc11fd1b0861bd6d294ca_l3.png)

![Rendered by QuickLaTeX.com \left[c, d\right]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-9e601090d7c25be74cf47eec386330bb_l3.png)


(3) ![Rendered by QuickLaTeX.com \begin{equation*} y = c + \frac{d-c}{b-a} \left(x - a\right)\end{equation*}](../../assets/1fd388192074229d.png)


which, once again, has a very immediate geometrical interpretation:

![](../../assets/fb72a68a0a032428.png)


![](../../assets/fb72a68a0a032428.png)

Some libraries wrap those two functions into one; Arduino, for instance, calls this [map](https://www.arduino.cc/reference/en/language/functions/math/map/). No equivalent function is present in Unity, but it can be easily implemented like this:

float y = Mathf.Lerp(c, d, Mathf.InverseLerp(x, a, b));

Or, slightly more efficiently, like this:

public static float Lerp (float x0, float x1, float y0, float y1, float x) { float d = x1 - x0; if (d == 0) return (y0 + y1) / 2; return y0 + (x - x0) * (y1 - y0) / d; }

Linear interpolation is indeed *linear* because it creates a *linear relationships* between between the input and output intervals. If we look at lerp as a mathematical function plotted in the cartesian plane (below), it is easy to see that it represents the equation of a line that passes between ![Rendered by QuickLaTeX.com \left(a, c\right)](../../assets/c834a59a35e5742c.png)

![Rendered by QuickLaTeX.com \left(b, d\right)](../../assets/e5ce2993d2c0c3e4.png)


![](../../assets/5e57e83a04988c7e.png)


![](../../assets/5e57e83a04988c7e.png)

### ⭐ Recommended Unity Assets

## Lerping Everything…

For instance, lerping between two points means moving along the shortest path that connected them. On the other hand, lerping between two colours means blending

### Points

So far, we only interpolated two numbers. But nothing stops us from interpolating two points. In this case, the easiest way to do so is to interpolate the individual X and Y coordinate:

Vector2 Lerp (Vector2 a, Vector2 b, float t) { return new Vector2 ( Mathf.Lerp(a.x, b.x, t), Mathf.Lerp(a.y, b.y, t) ); }

Unity comes with both `Vector2.Lerp`

and `Vector3.Lerp`

which, as expected, allow to interpolate between points in 2D and 3D. Lerping between points, regardless of their dimension, is equivalent to moving along the line that connected them.

While lerp is inherently linear, it can actually be used to create curves. Successive interpolations on a series of points results in a family of shapes known as Bézier curves (pronounced: /ˈbɛz.i.eɪ/, [BEH-zee-ay](https://www.alanzucconi.com/2021/01/11/gamedev-pronunciation-guide/)).

Vector2 Bezier (Vector2 p0, Vector2 p1, Vector2 p2, Vector2 p3, float t) { // Lerp between the control points Vector2 a = Vector2.Lerp(p0, p1, t); Vector2 b = Vector2.Lerp(p1, p2, t); Vector2 c = Vector2.Lerp(p2, p3, t); // Lerp between the lerped points Vector2 d = Vector2.Lerp(a, b, t); Vector2 e = Vector2.Lerp(b, c, t); // Lerped between the lerped points (again!) return Vector2.Lerp(d, e, t); }

![](../../assets/2fa4c4fe2e8d64e7.gif)


![](../../assets/2fa4c4fe2e8d64e7.gif)

[The Ever so Lovely Bézier Curve](https://acegikmo.medium.com/the-ever-so-lovely-b%C3%A9zier-curve-eb27514da3bf) by Shader Witch [Freya Holmér](https://twitter.com/FreyaHolmer) is possibly the most accessible article on the topic (and the source of the animation above).

### Colours

Another very common way in which lerp is used is to blend colours. Conceptually, you can imagine lerping between colours as mixing different amounts of paint. Lerping between red and blue with ![Rendered by QuickLaTeX.com t=0.8](../../assets/689d62da3b2c5103.png)


![](../../assets/5ec8e37dd2ff90fb.png)


![](../../assets/5ec8e37dd2ff90fb.png)

The easiest way to interpolate between colours is to interpolate the single red, green and blue components independently:

Color Lerp (Color a, Color b, float t) { return new Color ( Mathf.Lerp(a.r, b.r, t), Mathf.Lerp(a.g, b.g, t), Mathf.Lerp(a.b, b.b, t), Mathf.Lerp(a.a, b.a, t) ); }

That is exactly how `Color.Lerp`

works in Unity. While this technically works, it often yields rather poor results. This is because the RGB colour space is good to store colours, but not so much to manipulate them in a way that makes sense, *perceptually*.

Learning how to properly interpolate between colours is a dark art, which is heavily discussed in [The Secrets of Colour Interpolation](https://www.alanzucconi.com/2016/01/06/colour-interpolation/). You can play with the swatches below to see for yourself what difference it makes to lerp between different colour spaces.

### Rotations

The last aspect that this first post is going to discuss, is about angles and rotations. From what we covered so far, one might be tempted to lerp between angles in order to perform rotations. That is actually not going to work; or at least, not always, and not as you expect.

The reason is that angles are “looping”, and being able to take that into account requires a non-linear operator. Let’s make a simple example: lerping between 90° and 180° should work as intended, giving you a nice angle that goes from 90 to 180. However, lerping from 350° to 10° will not! There are two ways to reach 10 from 350: going up, or going down. The linear interpolation does not know that it is working with angles, and it will take the longer path, decreasing the angle from 350 to 10.

One way to fix this is to use quaternions instead. Quaternions are an alternative—and somewhat safer—way or representing and working with angles in 3D. But they are also incredibly counterintuitive and difficult to grasp.

Unity comes with its own way to lerp between quaternions, called `Quaternion.Slerp`

. The term *slerp* stands for **spherical linear interpolation**. In a nutshell, slerp allows to lerp between any two points on a sphere, rather than a flat plane. A future series will delve into the absolute madness that are quaternions; luckily for you, this is not that series.

## What’s Next…

The second part of this series will see how the linear interpolation can be extended to non-linear functions.

- Part 1:
**Linear Interpolation** - Part 2:
[Piecewise Interpolation](https://www.alanzucconi.com/?p=12846) - Part 3:
[Color Curve Correction](https://www.alanzucconi.com/?p=12877)

### Download Unity Package

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

The [Standard package](https://www.patreon.com/posts/46612886) contains the script to perform piecewise linear interpolation. It uses extension methods which allows to easily interpolated numbers, vectors, colours and even quaternions! The [Advanced package](https://www.patreon.com/posts/46613014), instead, contains a test scene which also shows how to correct colour curves.

## Leave a Reply Cancel reply