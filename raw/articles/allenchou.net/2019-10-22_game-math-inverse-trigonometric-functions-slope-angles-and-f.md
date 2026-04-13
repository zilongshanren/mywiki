---
title: 'Game Math: Inverse Trigonometric Functions, Slope Angles, And Facing Objects
  | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2019/10/inverse-trig/
author: Allen Chou
published: '2019-10-22'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

Source files and future updates are available on [Patreon](https://www.patreon.com/TheAllenChou).

You can follow me on [Twitter](https://twitter.com/TheAllenChou).

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

本文之中文翻譯[在此](http://www.allenchou.net/2019/10/inverse-trig-chinese/)

## Prerequisites

## Overview

At this point, we have learned about the three basic trigonometric functions: sine, cosine, and tangent. Now, we are going to take a look at their **inverse functions**, as well as how they can be utilized in games.

In this tutorial, you’ll learn:

- The inverse functions of the three basic trigonometric functions.
- How to compute the angle of a slope given a desired slope value.

- The domains and ranges of inverse trigonometric functions.
- The special convenience inverse trigonometric function
.**atan2** - How to make an object face towards the mouse cursor.

## Inverse Functions

A function can be treated like a black box that takes some input and gives you some output. If a function ![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

![Rendered by QuickLaTeX.com x](../../assets/4a5eb3d3e5b045d0.png)

![Rendered by QuickLaTeX.com y](../../assets/450e84e6a4b5edb0.png)

![Rendered by QuickLaTeX.com y = f(x)](../../assets/d77c2906dbd29d1d.png)

*y equals f of x*). Meanwhile, if a function can take an output of ![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

**inverse **of ![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

![Rendered by QuickLaTeX.com f^{-1}](../../assets/c745738d6228b43c.png)

*f inverse*).

In other words, if the function ![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

![Rendered by QuickLaTeX.com x](../../assets/4a5eb3d3e5b045d0.png)

![Rendered by QuickLaTeX.com y](../../assets/450e84e6a4b5edb0.png)

![Rendered by QuickLaTeX.com y = f(x)](../../assets/d77c2906dbd29d1d.png)

![Rendered by QuickLaTeX.com f^{-1}](../../assets/c745738d6228b43c.png)

![Rendered by QuickLaTeX.com y](../../assets/450e84e6a4b5edb0.png)

![Rendered by QuickLaTeX.com x](../../assets/4a5eb3d3e5b045d0.png)

![Rendered by QuickLaTeX.com x = f^{-1}(y)](../../assets/f38aa98dc7409b9a.png)


An example of a function verses its inverse is a function that **adds one** to its input and a function that **subtracts one** from its input. Let ![Rendered by QuickLaTeX.com Add1(x)](../../assets/709b89728c15e452.png)

![Rendered by QuickLaTeX.com x](../../assets/4a5eb3d3e5b045d0.png)

![Rendered by QuickLaTeX.com Sub1(y)](../../assets/22b601737787249a.png)

![Rendered by QuickLaTeX.com y](../../assets/450e84e6a4b5edb0.png)

![Rendered by QuickLaTeX.com x=2](../../assets/9a535d89ab250d82.png)

![Rendered by QuickLaTeX.com Add1(x)](../../assets/709b89728c15e452.png)


![Rendered by QuickLaTeX.com \begin{flalign*} y = Add1(2) = 3 \end{flalign*}](../../assets/14222a0631079a2a.png)


Now, if we feed ![Rendered by QuickLaTeX.com y=3](../../assets/aa808b09cc1ef481.png)

![Rendered by QuickLaTeX.com Sub1(y)](../../assets/22b601737787249a.png)

![Rendered by QuickLaTeX.com x=2](../../assets/9a535d89ab250d82.png)


![Rendered by QuickLaTeX.com \begin{flalign*} x = Sub1(3) = 2 \end{flalign*}](../../assets/e1d829ac4d98513f.png)


## Inverse Trigonometric Functions

We already know that trigonometric functions take an angle as input and produce a number as output. We can feed the output of a trigonometric function (a real number) into its inverse function, and the inverse function would spit out the original input to the trigonometric function (an angle **in radians**). For example, ![Rendered by QuickLaTeX.com \sin\frac{\pi}{2} = 1](../../assets/517f620245cc5eaa.png)

![Rendered by QuickLaTeX.com \sin^{-1}1 = \frac{\pi}{2}](../../assets/e684aa67dcd730d6.png)


Inverse trigonometric functions have special names. Rather than “sine inverse”, the inverse of sine, written as ![Rendered by QuickLaTeX.com \sin^{-1}](../../assets/7f51f326d5904549.png)

**arcsine**. Similarly, ![Rendered by QuickLaTeX.com cos^{-1}](../../assets/5554394ff92918e9.png)

![Rendered by QuickLaTeX.com tan^{-1}](../../assets/be9d0fb7e2f42803.png)

**arccosine** and **arctangent**, respectively. In Unity, here’s how you’d call these three inverse trigonometric functions:

float sinAngle = Mathf.Asin(sinValue); // arcsine float cosAngle = Mathf.Acos(cosValue); // arccosine float tanAngle = Mathf.Atan(tanValue); // arctangent

## Slope Angles

As a quick example, if we know the ratio of vertical rise versus horizontal offset of a hill in a game level, how do we compute the angle of the slope? Using the illustration below, how do we compute ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

![Rendered by QuickLaTeX.com H](../../assets/90b95e98f0a12951.png)


![](../../assets/b560c156ab7eb34c.png)

The goal is to express ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

![Rendered by QuickLaTeX.com H](../../assets/90b95e98f0a12951.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

![Rendered by QuickLaTeX.com H](../../assets/90b95e98f0a12951.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \tan\theta = \frac{V}{H} \end{flalign*}](../../assets/4f5016468dd3ee3c.png)


Next, we can obtain ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com \frac{V}{H}](../../assets/15098bb515667137.png)

![Rendered by QuickLaTeX.com \tan^{-1}](../../assets/1eac89c2a029a376.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \theta = \tan^{-1}\frac{V}{H} \end{flalign*}](../../assets/1fb9b2f647f2a6af.png)


Alternatively, we can view the equation above as the result of taking the arctangent of both sides of the previous equation. Generally, ![Rendered by QuickLaTeX.com f^{-1}(f(x))](../../assets/87147348e28ce36a.png)

![Rendered by QuickLaTeX.com x](../../assets/4a5eb3d3e5b045d0.png)

![Rendered by QuickLaTeX.com f(f^{-1}(x))](../../assets/eb10d7c3c3a1e207.png)

![Rendered by QuickLaTeX.com y](../../assets/450e84e6a4b5edb0.png)


The angle ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

[an earlier tutorial](http://www.allenchou.net/2019/08/trigonometry-basics-sine-cosine/), we can convert the angle’s unit to degrees by multiplying it with ![Rendered by QuickLaTeX.com \frac{180}{\pi}](../../assets/84b185e1a825b906.png)


So, we can make a little interactive program that allows the user to move a point that forms a slope with the origin, and use the point’s coordinates ![Rendered by QuickLaTeX.com (X, Y)](../../assets/20a6cdca242db178.png)


And here’s the code:

Vector3 point = p.transform.position; // compute slope angle in radians float angleRad = Mathf.Atan(point.y / point.x); // convert to degrees // Mathf.Rad2Deg is a constant equal to 180.0f / Pi float angleDeg = angleRad* Mathf.Rad2Deg; text = angleDeg + &amp;amp;quot;°&amp;amp;quot;;

## Domains And Ranges

When using inverse trigonometric functions, it’s important to understand their **domains** and **ranges**.

The domain of a function is the collection of all valid values as input, and the range of a function is the collection of all possible output values.

For example, the domain of ![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com [-1, 1]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-96395345c57f8928c42918c656dd1364_l3.png)

![Rendered by QuickLaTeX.com [0, 10)](../../assets/372bff49385780c2.png)


The inverse of a function should simply have a domain and range equal to the range and domain, respectively, of the corresponding function, right? For inverse trigonometric functions, that’s not the case.

Trigonometric functions are periodic, which means multiple different input values can result in the same output value. For ![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)


Let’s use ![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \sin\frac{\pi}{2}](../../assets/c206c4977b549dcf.png)

![Rendered by QuickLaTeX.com \sin\frac{5\pi}{2}](../../assets/600a57d5fde6b1d2.png)

![Rendered by QuickLaTeX.com \sin^{-1}1](../../assets/28dd9b69dffd964f.png)

![Rendered by QuickLaTeX.com \frac{\pi}{2}](../../assets/fb4adb336c085ad9.png)

![Rendered by QuickLaTeX.com \frac{5\pi}{2}](../../assets/79933e887ef34138.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)


Since the ranges of ![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com [-1, 1]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-96395345c57f8928c42918c656dd1364_l3.png)

![Rendered by QuickLaTeX.com \sin^{-1}x](../../assets/617d5e481ebb6b34.png)

![Rendered by QuickLaTeX.com \cos^{-1}x](../../assets/f9efbcca7770ab29.png)

![Rendered by QuickLaTeX.com [-1, 1]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-96395345c57f8928c42918c656dd1364_l3.png)

![Rendered by QuickLaTeX.com \sin^{-1}x](../../assets/617d5e481ebb6b34.png)

![Rendered by QuickLaTeX.com \cos^{-1}x](../../assets/f9efbcca7770ab29.png)

![Rendered by QuickLaTeX.com [\frac{-\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9774586f3753f3cf9ff0dc4a325ab8c8_l3.png)

![Rendered by QuickLaTeX.com [0, \pi]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-2a4bfe6466ef28b78e984d6d1442a1ba_l3.png)

![Rendered by QuickLaTeX.com \pi](../../assets/4b60fce59d6919ef.png)


Hence, ![Rendered by QuickLaTeX.com \sin^{-1}1](../../assets/28dd9b69dffd964f.png)

![Rendered by QuickLaTeX.com \frac{\pi}{2}](../../assets/fb4adb336c085ad9.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com [\frac{-\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9774586f3753f3cf9ff0dc4a325ab8c8_l3.png)


As for ![Rendered by QuickLaTeX.com \tan^{-1}x](../../assets/5556d89e8d9563b1.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com \tan^{-1}x](../../assets/5556d89e8d9563b1.png)

![Rendered by QuickLaTeX.com \tan^{-1}x](../../assets/5556d89e8d9563b1.png)

![Rendered by QuickLaTeX.com [\frac{-\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9774586f3753f3cf9ff0dc4a325ab8c8_l3.png)

![Rendered by QuickLaTeX.com \sin^{-1}x](../../assets/617d5e481ebb6b34.png)


## The **Atan2** Convenience Function

Lets say we have a point ![Rendered by QuickLaTeX.com P=(P_x, P_y)](../../assets/5daa083b44a2c4e5.png)

![Rendered by QuickLaTeX.com P_x > 0](../../assets/dc7cdc0ad30cc85b.png)

![Rendered by QuickLaTeX.com P_y > 0](../../assets/db65c9cbbc32a7ba.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com +x](../../assets/9661260881fee50f.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)


![](../../assets/d2651ff0474ce7cd.png)

We know that ![Rendered by QuickLaTeX.com \tan\theta = \frac{P_y}{P_x}](../../assets/8830b2889b322bca.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com \theta = \tan^{-1}\frac{P_y}{P_x}](../../assets/bba1f2628a808a8e.png)

![Rendered by QuickLaTeX.com P_x](../../assets/72c34ba1ade40d99.png)

![Rendered by QuickLaTeX.com P_y](../../assets/93a6993515ec6215.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com [0, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-d1fd87d1f660fa4bc822942855f1726f_l3.png)

![Rendered by QuickLaTeX.com [-\frac{\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7acc7e9164fd8c9bce79d25371045b45_l3.png)


This this is what the computation looks like in code:

float angle = Mathf.Atan(p.y / p.x);

What if ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P_x > 0](../../assets/dc7cdc0ad30cc85b.png)

![Rendered by QuickLaTeX.com P_y < 0](../../assets/89c3666522523a26.png)

![Rendered by QuickLaTeX.com \frac{P_y}{P_x}](../../assets/cebf49cfeccffff7.png)

![Rendered by QuickLaTeX.com \tan^{-1}\frac{P_y}{P_x}](../../assets/ea66b1bd5a77642a.png)

![Rendered by QuickLaTeX.com [\frac{-\pi}{2}, 0]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1f29f195f2dea4f7e5d0cfb2b3fcef74_l3.png)

![Rendered by QuickLaTeX.com [-\frac{\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7acc7e9164fd8c9bce79d25371045b45_l3.png)


![](../../assets/ad5522a269070f85.png)

Problems arise when we have ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P_x < 0](../../assets/b949a23d550b1e81.png)

![Rendered by QuickLaTeX.com P_y > 0](../../assets/db65c9cbbc32a7ba.png)

![Rendered by QuickLaTeX.com \frac{P_y}{P_x}](../../assets/cebf49cfeccffff7.png)

![Rendered by QuickLaTeX.com P_2=(P_{2x}, P_{2y})](../../assets/5cdc6027719e5189.png)

![Rendered by QuickLaTeX.com \frac{P_{2y}}{P_{2x}}](../../assets/6b8b05298debb862.png)

![Rendered by QuickLaTeX.com \frac{P_{4y}}{P_{4x}}](../../assets/a1cdf71fa1faa0fa.png)

![Rendered by QuickLaTeX.com P_4=(P_{4x}, P_{4y})](../../assets/9b2536dbb626658a.png)

![Rendered by QuickLaTeX.com (P_{2x}, P_{2y}) = (-P_{4x}, -P_{4y})](../../assets/a956dba7ede7ce21.png)


The two points ![Rendered by QuickLaTeX.com P_2](../../assets/509d0e95df32a230.png)

![Rendered by QuickLaTeX.com P_4](../../assets/7c9ee61a5b4042ff.png)

![Rendered by QuickLaTeX.com \frac{P_{2y}}{P_{2x}} = \frac{P_{4y}}{P_{4x}}](../../assets/f7f4fcbddee770b8.png)


![](../../assets/2fad48e3d0c7fe69.png)

Also seen in the figure above is that the coordinate ratios of points ![Rendered by QuickLaTeX.com P_2](../../assets/509d0e95df32a230.png)

![Rendered by QuickLaTeX.com P_4](../../assets/7c9ee61a5b4042ff.png)

![Rendered by QuickLaTeX.com P_1](../../assets/777e18c079fee59b.png)

![Rendered by QuickLaTeX.com P_3](../../assets/d959e4b624cccb47.png)

**sharp angles** (angles less than 90 degrees) between the line segments connecting the origin & the points and the X axis are identical.

The ratio ![Rendered by QuickLaTeX.com \frac{P_{2y}}{P_{2x}}](../../assets/6b8b05298debb862.png)

![Rendered by QuickLaTeX.com \frac{-P_{4y}}{-P_{4x}}](../../assets/72cc2a4dbd9b1110.png)

![Rendered by QuickLaTeX.com \frac{P_{4y}}{P_{4x}}](../../assets/a1cdf71fa1faa0fa.png)

![Rendered by QuickLaTeX.com \frac{P_{2y}}{P_{2x}}](../../assets/6b8b05298debb862.png)

![Rendered by QuickLaTeX.com \tan^{-1}\frac{P_{2y}}{P_{2x}}](../../assets/a8960b7159bbb7ab.png)

![Rendered by QuickLaTeX.com \tan^{-1}\frac{P_{4y}}{P_{4x}}](../../assets/d25d8c6f89160686.png)


When we pass in ![Rendered by QuickLaTeX.com \frac{P_{2y}}{P_{2x}}](../../assets/6b8b05298debb862.png)

**astute angle** (angle larger than 90 grees) shown in the figure below, not the red negative sharp ones. We always want to start measuring angles from the +X direction.

![](../../assets/2e3caa86f066cc39.png)

In order to do so, before combining ![Rendered by QuickLaTeX.com P_{x}](../../assets/72d0960b6391476f.png)

![Rendered by QuickLaTeX.com P_{y}](../../assets/cc01d06dd0eac8b7.png)

![Rendered by QuickLaTeX.com P_x](../../assets/72c34ba1ade40d99.png)

![Rendered by QuickLaTeX.com P_y](../../assets/93a6993515ec6215.png)

![Rendered by QuickLaTeX.com [-\frac{\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7acc7e9164fd8c9bce79d25371045b45_l3.png)


// range of this function is (-pi, pi] float FixedUpAtan(float py, float px) { if (px > 0.0f) // normal, no fix-up needed { // &amp;amp;quot;normal&amp;amp;quot; // py > 0.0f : first quadrant // py < 0.0f : fourth quadrant return Mathf.Atan(py / px); } else if (px < 0.0f) // fix-up needed { if (py > 0.0f) // second quadrant return Math.PI + Mathf.Atan(py / px); else if (py < 0.0f) // third quadrant return -Math.PI + Mathf.Atan(py / px); else // angle on negative X axis return 2.0f * Mathf.PI; } else // infinity { if (py > 0.0f) return 0.5f * Mathf.PI; // ratio is positive infinity else if (py < 0.0f) return -0.5f * Mathf.PI; // ratio is negative infinity else return 0.0f; // degenerate input (the origin) } }

That seems like quite a lot of work. Luckily, almost all standard math libraries in any programming languages provide a convenience function called **atan2**, which has a full 360-degree range of ![Rendered by QuickLaTeX.com (-\pi, \pi]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1a2076e8b5cb430a7530c947d8828532_l3.png)

**Atan2** in different libraries may have different ordering of the two arguments, but based on what I’ve seen, Y followed by X is pretty common.

I often see a misconception that **atan2** is just an alternative to the arctangent function and doesn’t do anything extra that arctangent cannot do. This is actually incorrect. The arctangent function only takes a single value as input, and its output range is ![Rendered by QuickLaTeX.com [\frac{-\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9774586f3753f3cf9ff0dc4a325ab8c8_l3.png)

**atan2** takes **two** values as input (![Rendered by QuickLaTeX.com P_y](../../assets/93a6993515ec6215.png)

![Rendered by QuickLaTeX.com P_x](../../assets/72c34ba1ade40d99.png)

![Rendered by QuickLaTeX.com (-\pi, \pi]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1a2076e8b5cb430a7530c947d8828532_l3.png)


## Facing An Object Towards The Mouse Cursor in 3D

Lastly, let’s look at a classic example of facing an object towards the mouse cursor.

First, find the intersection between the ray under the mouse cursor and the ground plane. Then, place an object at that intersection, creating the effect of the object following the mouse cursor in 3D. This object is our look target.

Camera cam = Camera.current; Vector3 mouse= Input.mousePosition; Ray ray = cam.ScreenPointToRay(mouse); float rayDist; plane.Raycast(ray, out rayDist); sphere.position = ray.GetPoint(rayDist);

Next, let’s use our old friend UFO Bunny from [Boing Kit](https://assetstore.unity.com/packages/tools/particles-effects/boing-kit-dynamic-bouncy-bones-grass-water-and-more-135594) again. When un-rotated, her forward vector is in the +X direction, and her left vector is in the +Z direction. We want to face her towards the look target.

![](../../assets/54574d2d8321a11a.png)

Then, let UFO Bunny be the origin, and calculate the coordinates of the look target relative to her:

Vector3 coord = sphere.transform.position - ufoBunny.transform.position;

Now, let’s mark up the scene with an angle ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/52acccf095b69268.png)

As shown before, the angle ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

**atan2** function:

float thetaRad = Mathf.atan2(coord.z, coord.x); // in radians

Recall this figure:

![](../../assets/d2651ff0474ce7cd.png)

This figure shows the XY plane, and as ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)


Now that we have the rotation axis and the desired rotation angle, we can finally construct a **quaternion** representing such rotation. Quaternions will also be covered in later tutorials. For now, we just need to know that quaternion is a type of data Unity uses to represent object rotation.

float thetaDeg = thetaRad * Mathf.Rad2Deg; // in degrees float axis = Vector3.down; // (0, -1, 0) == -Y axis Quaternion rot = Quaternion.AngleAxis(thetaDeg, axis); ufoBunny.transform.rotation = rot;

And here’s our final result:

Note: Unity already provides helper functions like `Quaternion.LookRotation`

and `Transform.LookAt`

that can achieve the same effect. But the purpose of this tutorial is to help understand inverse trigonometric functions.

## Summary

In this tutorial, we have been introduced to the inverse trigonometric functions, how they relate to their corresponding trigonometric functions, and their domains and ranges.

Also, we have seen that the arctangent function doesn’t have a full 360-degree range, but a convenient utility function **atan2** does.

Lastly, we have learned how to use the **atan2** function to implement the classic example of facing an object towards the mouse cursor.

If you enjoyed this tutorial and would like to see more, please consider supporting me on [Patreon](https://www.patreon.com/TheAllenChou). By doing so, you can also get updates on future tutorials. Thanks!

I’m learning about Inverse Functions in school! Very cool to see them applied in programming.