---
title: 'Game Math: Trigonometry Basics – Sine & Cosine | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2019/08/trigonometry-basics-sine-cosine/
author: Allen Chou
published: '2019-08-26'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

Source files and future updates are available on [Patreon](https://www.patreon.com/TheAllenChou).

You can follow me on [Twitter](https://twitter.com/TheAllenChou).

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

本文之中文翻譯[在此](http://allenchou.net/2019/08/trigonometry-basics-sine-cosine-chinese/)

## Overview

Trigonometry is a very essential building block to a huge portion of game math. That’s why I’ve chosen this topic for the first tutorial of my new Gamedev Tutorials series. Having a solid understanding of basic of trigonometry can go a long way for game development. It is used extensively in game problem solving.

In this tutorial you’ll learn:

- A geometric interpretation of two basic trigonometric functions: sine & cosine.
- The comparison of two different angle units: degrees & radians.
- Some basic properties of sine & cosine.
- How to move and arrange things in a circular fashion:

- How to move things in a spiral fashion:

- How to create simple harmonic motion:

- How to create damped spring motion:

- How to create pendulum motion:

- How to generate hovering motion:

## Geometric Interpretation of Sine & Cosine

Let’s look at the **unit circle**, a circle with a radius of 1 centered at the origin.

![](../../assets/eaaac7db3cc32708.png)

Now pick a point ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


What’s shown here is actually a way to geometrically express the 2 basic trigonometric functions: ![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com (X, Y)](../../assets/20a6cdca242db178.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com (\cos\theta, \sin\theta)](../../assets/a390ac661a350c78.png)


So, to recap, the two trigonometry function ![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


Since ![Rendered by QuickLaTeX.com \sin](../../assets/9c2a44c14ab4d230.png)

![Rendered by QuickLaTeX.com \cos](../../assets/98a85ef943f513f7.png)

![Rendered by QuickLaTeX.com \sin(\theta)](../../assets/949e34d87281021e.png)

![Rendered by QuickLaTeX.com \cos(\theta)](../../assets/cda467841df79800.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)


![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com [-1, 1]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-96395345c57f8928c42918c656dd1364_l3.png)


If the angle ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


If we compare the plots side-by-side in the form of angle-vs-value, we can see they are the same periodic curve in a wave-like shape, but offset by a fourth from each other.

![](../../assets/18d681fedbe297e0.png)

The period of these functions is ![Rendered by QuickLaTeX.com 360^\circ](../../assets/0e2e0f15c6dd959f.png)

![Rendered by QuickLaTeX.com \sin450^\circ](../../assets/110b72ef72cc0801.png)

![Rendered by QuickLaTeX.com \sin90^\circ](../../assets/9bd7559da0ce0d0b.png)

![Rendered by QuickLaTeX.com 360^\circ](../../assets/0e2e0f15c6dd959f.png)

![Rendered by QuickLaTeX.com 90^\circ](../../assets/f665200c5de23ae0.png)


## Degrees v.s. Radians

The angle passed into the trigonometric functions can be in two different units: **degrees** and **radians**. Most people are familiar with degrees and its upper-little-circle notation. For instance, the right angle (90 degrees) is written as ![Rendered by QuickLaTeX.com 90^\circ](../../assets/f665200c5de23ae0.png)

![Rendered by QuickLaTeX.com \sin90^\circ](../../assets/9bd7559da0ce0d0b.png)

![Rendered by QuickLaTeX.com \sin90](../../assets/6ebc520f1c82e39d.png)

**radians**.

![Rendered by QuickLaTeX.com 180^\circ](../../assets/831c30544c8a897a.png)

![Rendered by QuickLaTeX.com \pi](../../assets/4b60fce59d6919ef.png)

![Rendered by QuickLaTeX.com \pi](../../assets/4b60fce59d6919ef.png)

![Rendered by QuickLaTeX.com \frac{180^\circ}{\pi} \approx 57.3^\circ](../../assets/10e780b96c29b4c5.png)

![Rendered by QuickLaTeX.com 60^\circ](../../assets/b4b5c2ed05db9651.png)

![Rendered by QuickLaTeX.com \sin1](../../assets/716267115524b1c9.png)

![Rendered by QuickLaTeX.com 0.84](../../assets/ab74ed44b4d08644.png)

![Rendered by QuickLaTeX.com \sin60^\circ \approx 0.87](../../assets/f290eef32a1a19ec.png)


Here are some common degree-to-radian mappings:

![Rendered by QuickLaTeX.com \begin{alignat*} \ 30^\circ &= \frac{\pi}{6} \hspace{10 mm} &45^\circ &= \frac{\pi}{4} \hspace{10 mm} &60^\circ &= \frac{\pi}{3} \\ \ 90^\circ &= \frac{\pi}{2} \hspace{10 mm} &180 ^\circ &= \pi \hspace{10 mm} &360^\circ &= 2\pi \\ \end{alignat*}](../../assets/9d57afb952da39c6.png)


In Unity, the ![Rendered by QuickLaTeX.com \sin](../../assets/9c2a44c14ab4d230.png)

![Rendered by QuickLaTeX.com \cos](../../assets/98a85ef943f513f7.png)

`Mathf.Sin`

and `Mathf.Cos`

, respectively. Beware that these functions take input in radians, so if you want to compute ![Rendered by QuickLaTeX.com \cos45^\circ](../../assets/02ffb4a29baf24c0.png)


// this is actually cosine of 45 radians! float cos45Deg = Mathf.Cos(45.0f);

45 radians is about ![Rendered by QuickLaTeX.com 2578^\circ](../../assets/253f7cbe48985718.png)

![Rendered by QuickLaTeX.com 360^\circ](../../assets/0e2e0f15c6dd959f.png)

![Rendered by QuickLaTeX.com 2578^\circ](../../assets/253f7cbe48985718.png)

![Rendered by QuickLaTeX.com 360^\circ](../../assets/0e2e0f15c6dd959f.png)

![Rendered by QuickLaTeX.com 58^\circ](../../assets/d073d6de3332ee62.png)

![Rendered by QuickLaTeX.com 2578^\circ](../../assets/253f7cbe48985718.png)

![Rendered by QuickLaTeX.com 45^\circ](../../assets/73d9208cfc67b668.png)


To compute ![Rendered by QuickLaTeX.com \cos45^\circ](../../assets/02ffb4a29baf24c0.png)


// covert to radians float cos45Deg = Mathf.Cos(45.0f * Mathf.PI / 180.0f);

Or use constants that help convert between degrees and radians.

float cos45Deg = Mathf.Cos(45.0f * Mathf.Deg2Rad);

In tools like the Unity editor, expressing angles in degrees is more user friendly, because most people can immediately picture what a ![Rendered by QuickLaTeX.com 45^\circ](../../assets/73d9208cfc67b668.png)


One useful thing about radians is that it trivializes calculating arc length from a given radius and angle. Let’s say we want to calculate the length of an arc of ![Rendered by QuickLaTeX.com 30^\circ](../../assets/98401b57c754a8b7.png)

![Rendered by QuickLaTeX.com \frac{\pi}{6}](../../assets/e03058110d50c28f.png)


![](../../assets/3cd0fd52f9823d30.png)

If computed using degrees, first the whole circumference is calculated using the formula ![Rendered by QuickLaTeX.com radius \times 2\pi](../../assets/45e2ab53f27a7fa8.png)

![Rendered by QuickLaTeX.com 30^\circ](../../assets/98401b57c754a8b7.png)

![Rendered by QuickLaTeX.com 360^\circ](../../assets/0e2e0f15c6dd959f.png)


![Rendered by QuickLaTeX.com \begin{flalign*} arc &= radius \times 2\pi \times \frac{30^\circ}{360^\circ} \\ &= 2 \times 2\pi \times \frac{1}{12} \\ &= \frac{\pi}{3} \\ \end{flalign*}](../../assets/5a94d91d9f77df5d.png)


When using radians, the arc length formula is simply **radius times angle in radians**:

![Rendered by QuickLaTeX.com \begin{flalign*} arc &= radius \times \frac{\pi}{6} \\ &= 2 \times \frac{\pi}{6} \\ &= \frac{\pi}{3} \\ \end{flalign*}](../../assets/351abe181556d3b9.png)


The circle’s circumference formula agrees nicely with the arc length formula in radians. Since one full circle is basically an arc with an angle of ![Rendered by QuickLaTeX.com 2\pi](../../assets/8536ab24b2361d28.png)

![Rendered by QuickLaTeX.com radius \times 2\pi](../../assets/45e2ab53f27a7fa8.png)


## Basic Properties of Sine & Cosine

Now let’s look at some basic properties of sine & cosine that can come in handy in future mathematical derivations.

Since ![Rendered by QuickLaTeX.com (cos\theta, sin\theta)](../../assets/9c75288dcd3d852d.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

[Pythagorean theorem](https://en.wikipedia.org/wiki/Pythagorean_theorem) states that the distance of the point ![Rendered by QuickLaTeX.com (X, Y)](../../assets/20a6cdca242db178.png)

![Rendered by QuickLaTeX.com \sqrt{X^2 + Y^2}](../../assets/e18d7a71dc0f274a.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \sin^2\theta + \cos^2\theta = 1 \\ \end{flalign*}](../../assets/69f922f21ad21c3d.png)


The squares of ![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \sin^2\theta](../../assets/714cd4302fb2c1ba.png)

![Rendered by QuickLaTeX.com \cos^2\theta](../../assets/112a1883da16f06e.png)

![Rendered by QuickLaTeX.com (\sin(\theta))^2](../../assets/b45c67e49e4728a2.png)

![Rendered by QuickLaTeX.com (\cos(\theta))^2](../../assets/a06cf5c8da9446f1.png)


Recall the side-by-side comparison of the sine and cosine plots.

![](../../assets/18d681fedbe297e0.png)

You can see that the cosine curve basically is the sine curve shifted to the left by ![Rendered by QuickLaTeX.com 90^\circ](../../assets/f665200c5de23ae0.png)

![Rendered by QuickLaTeX.com \frac{\pi}{2}](../../assets/fb4adb336c085ad9.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \sin\theta &= \cos(\theta - \frac{\pi}{2}) \\ \cos\theta &= \sin(\theta + \frac{\pi}{2}) \\ \end{flalign*}](../../assets/44800f18b898b86f.png)


## Moving in Circles & Spirals

Now that we’ve seen that ![Rendered by QuickLaTeX.com (cos\theta, sin\theta)](../../assets/9c75288dcd3d852d.png)


The code below moves an object around a circle at a constant rate:

obj.transform.position = new Vector3 ( Radius * Mathf.Cos(Rate * Time.time), Radius * Mathf.Sin(Rate * Time.time), 0.0f );

The code below moves 12 objects around a circle at a constant rate, and the objects are equally spaced out around the circle:

float baseAngle = Rate * Time.time + angleOffset; for (int i = 0; i < 12; ++i) { float angleOffset = 2.0f * Mathf.PI * i / 12.0f; aObj[i].transform.position = new Vector3 ( Radius * Mathf.Cos(baseAngle + angleOffset), Radius * Mathf.Sin(baseAngle + angleOffset), 0.0f ); }

Combining circular motion with movement in the Z direction, we can create a spiral motion in 3D:

obj.transform.position = new Vector3 ( Radius * Mathf.Cos(Rate * Time.time), Radius * Mathf.Sin(Rate * Time.time), ZSpeed * Time.time );

## Simple Harmonic Motion (S.H.M.)

We’ve seen this plot of cosine versus angle:

![](../../assets/17b0cb4fdc15a91a.png)

What if we plug cosine into the X coordinate of an object?

float x = Mathf.Cos(Rate * Time.time); obj.transform.position = Vector3(x, 0.0f, 0.0f);

This is what we get:

This kind of oscillating motion that matches a sine-shaped curve, a.k.a. sinusoid, is known as simple harmonic motion, or S.H.M.

Since ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com \cos0= 1](../../assets/6efa4cf83ebcb6d3.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \sin0 = 0](../../assets/75fd38cce75bea33.png)


The input angle passed in to the sine and cosine functions are called the **phase**. Typically, if the phase passed in is a constant multiple of time, many people write it as ![Rendered by QuickLaTeX.com \sin \omega t](../../assets/cb6217bc6a3ee6ec.png)

![Rendered by QuickLaTeX.com \omega](../../assets/a6481661bed5b147.png)

**angular frequency** (in **radians per second**), and ![Rendered by QuickLaTeX.com t](../../assets/2095d761bc925f10.png)

![Rendered by QuickLaTeX.com \sin2\pi t](../../assets/bd68f0b77220d099.png)


What if we scale this motion by an exponentially decreasing factor?

float s = Mathf.Pow(0.5f, Decay * Time.time); float x = Mathf.Cos(Rate * Time.time); obj.transform.position = Vector3(s * x, 0.0f, 0.0f);

Now the object moves in a **damped spring motion**:

## Pendulum Motion

Instead of plugging a sinusoid into an object’s X coordinate, what if we plug it into the angle for the circular motion example above?

float baseAngle = 1.5f * Mathf.PI; // 270 degrees float halfAngleRange = 0.25f * mathf.PI; // 45 degrees float c = Mathf.Cos(Rate * Time.time); float angle = halfAngleRange * c + baseAngle; obj.transform.position = new Vector3 ( Radius * Mathf.Cos(angle), Radius * Mathf.Sin(angle), 0.0f );

The object now moves in a **pendulum motion**:

We can treat this as the circular motion’s angle being in a simple harmonic motion.

## Hovering Motion

As a bonus example, here is UFO Bunny, a character from [Boing Kit](https://assetstore.unity.com/packages/tools/particles-effects/boing-kit-135594), my bouncy VFX extension for Unity.

![](../../assets/12cbada0961cf888.png)

We can apply staggered simple harmonic motion to her X, Y, and Z coordinates separately.

Vector3 hover = new Vector3 ( RadiusX * Mathf.Sin(RateX * Time.time + OffsetX), RadiusY * Mathf.Sin(RateY * Time.time + OffsetY), RadiusZ * Mathf.Sin(RateZ * Time.time + OffsetZ) ); obj.transform.position = basePosition + hover;

And this creates a hovering motion.

And the hover offset can be used to compute a tilt rotation. This is beyond the scope of this tutorial, so I’ll just leave the code and results here.

obj.transform.rotation = baseRotation * Quaternion.FromToRotation ( Vector3.up, -hover + 3.0f * Vector3.up );

## Summary

That’s it!

We have seen how ![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)


Also, we have seen the difference between the two angle units: degrees and radians.

Finally, we now know how to moves things in circles and spirals, as well as oscillating things in simple harmonic motion, damped spring motion, pendulum motion, and hove motion.

I hope this tutorial has helped you get a better understanding of the 2 basic trigonometric functions: sine & cosine.

In the next tutorial, I will introduce one additional basic trigonometric function: **tangent**, as well as talk about more applications of all these 3 functions.

Until then!

If you enjoyed this tutorial and would like to see more, please consider supporting me on [Patreon](https://www.patreon.com/TheAllenChou). By doing so, you can also get updates on future tutorials. Thanks!

Awesome man.

I’ve spent the better part of 20 years designing and programming games, and in all this time this is the first time I’ve properly ‘grokked’ sin, cosine, and radians. Incredibly concise, to the point, and easy to understand with practical examples demonstrating the actual function and use of the methods.

One small comment, for whatever reason I was confused for a while by “You can see that the cosine curve basically is the sine curve shifted to the left by 90^\circ, or \frac{\pi}{2}.”. It might be slightly more clear for dotards such as myself if you explicitly state that this is in radians, even if you did earlier state that omitting degrees implies this.

Good point. I’ve added the explicit units. Thanks.

I’m going to provide some blunt feedback on this, and I hope it is taken in the spirit it is intended, which is to help you improve. Background: I’m always looking for simple explanations of advanced ideas to show my primary school aged children – I want to introduce my kids to those ideas early but without the stress and hassle of doing worked problems.

This is an excellent summary but a terrible tutorial. It’s such an excellent summary that I’ve bookmarked it. It’s such a terrible introduction/tutorial that there is no way I’m exposing my kids to it until they have a solid grasp of those 2 functions. If you haven’t seen this stuff before this tutorial would be incredibly confusing. If you have, you realize what an elegant and conscise summary and demo you’ve constructed.

Thanks for the feedback! I will keep this in mind when writing future tutorials.

Awesome! Keep it going!

Finally I was able to learn how to use SIN and COS.

Great tutorial!

Awesome article! Thanks a lot.