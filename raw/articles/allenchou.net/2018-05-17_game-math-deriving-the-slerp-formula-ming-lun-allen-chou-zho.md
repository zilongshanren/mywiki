---
title: 'Game Math: Deriving the Slerp Formula | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2018/05/game-math-deriving-the-slerp-formula/
author: Allen Chou
published: '2018-05-17'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

It occurred to me that the entire time I’ve been working with [quaternions](http://allenchou.net/2014/04/game-math-quaternion-basics/), I have never read or learned about the derivation of the formula for [slerp](http://allenchou.net/2014/04/game-math-quaternion-basics/#slerp), spherical linear interpolation. I just learned the final formula and have been using it.

Upon a preliminary search I couldn’t seem to immediately find a straightforward derivation, either (at least not one that fits in the context of game development). So I thought it might be a fun exercise to derive it myself.

As it turns out, it is indeed fun and could probably serve as an interesting trigonometry & vector quiz question!

A quick recap: slerp is an operation that interpolates between two vectors along the shortest arc (in any dimension higher than 1D). It takes as input the two vectors to interpolate between plus an interpolation parameter:

![Rendered by QuickLaTeX.com \[ Slerp(\overrightarrow{a}, \overrightarrow{b}, t) = \frac{sin((1-t)\Omega)}{sin\Omega} \overrightarrow{a} + \frac{sin(t\Omega)}{sin\Omega} \overrightarrow{b}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-838c4e593e55b17a77dcd748567fb659_l3.png)


where ![Rendered by QuickLaTeX.com \Omega](../../assets/6ccca86ab1ee1829.png)


![Rendered by QuickLaTeX.com \[ \Omega = \frac{cos^{-1}(\overrightarrow{a} \cdot \overrightarrow{b})}{||\overrightarrow{a}|| \, ||\overrightarrow{b}||} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-248904bb5f68842746e18920e2851064_l3.png)


If the interpolation parameter ![Rendered by QuickLaTeX.com t](../../assets/2095d761bc925f10.png)

![Rendered by QuickLaTeX.com t](../../assets/2095d761bc925f10.png)

![Rendered by QuickLaTeX.com 0.25](../../assets/357c0ae4019f5bcb.png)

![Rendered by QuickLaTeX.com \overrightarrow{a}](../../assets/f9dc43643f8775de.png)

![Rendered by QuickLaTeX.com \overrightarrow{b}](../../assets/175f1baaf6f2df62.png)

![Rendered by QuickLaTeX.com \overrightarrow{a}](../../assets/f9dc43643f8775de.png)

![Rendered by QuickLaTeX.com 0.25\Omega](../../assets/2618f23b65e5c38f.png)

![Rendered by QuickLaTeX.com \overrightarrow{b}](../../assets/175f1baaf6f2df62.png)

![Rendered by QuickLaTeX.com 0.75\Omega](../../assets/62cafeeed316c490.png)


In the context of game development, slerp is typically used to interpolate between orientations represented by quaternions, which can be expressed as 4D vectors. In this case the shortest arc slerp interpolates across lies on a 4D hypersphere.

As mentioned before, this formula can be used on any vectors in any dimension higher than 1D. So it can also be used to interpolate between two 3D vectors along a sphere, or between two 2D vectors along a circle.

In the context of game development, we almost exclusively work with unit quaternions. So in my derivation, I make the assumption that the vectors we are working with are all unit vectors. The flow of the derivation should be pretty much the same even if the vectors are not unit vectors.

Without further ado, here’s the derivation.

### The Derivation

Let ![Rendered by QuickLaTeX.com \overrightarrow{c}](../../assets/e87b96c5f2ed1196.png)


![Rendered by QuickLaTeX.com \[ \overrightarrow{c} = Slerp(\overrightarrow{a}, \overrightarrow{b}, t) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-181820cbc931879fa737bdb8c9c9ea38_l3.png)


And let ![Rendered by QuickLaTeX.com \Omega](../../assets/6ccca86ab1ee1829.png)

![Rendered by QuickLaTeX.com \overrightarrow{a}](../../assets/f9dc43643f8775de.png)

![Rendered by QuickLaTeX.com \overrightarrow{b}](../../assets/175f1baaf6f2df62.png)


Knowing that the angle between ![Rendered by QuickLaTeX.com \overrightarrow{a}](../../assets/f9dc43643f8775de.png)

![Rendered by QuickLaTeX.com \overrightarrow{c}](../../assets/e87b96c5f2ed1196.png)

![Rendered by QuickLaTeX.com t\Omega](../../assets/70e5288330fc1ad2.png)

![Rendered by QuickLaTeX.com \overrightarrow{b}](../../assets/175f1baaf6f2df62.png)

![Rendered by QuickLaTeX.com \overrightarrow{c}](../../assets/e87b96c5f2ed1196.png)

![Rendered by QuickLaTeX.com (1-t)\Omega](../../assets/3449cfda1606a5ee.png)


![](../../assets/0ce96fbebb7b4949.png)



Here’s the strategy. We build a pair of orthogonal axes ![Rendered by QuickLaTeX.com \hat{x}](../../assets/f383f914ab71354e.png)

![Rendered by QuickLaTeX.com \hat{y}](../../assets/dfdf0819009e9fb1.png)

![Rendered by QuickLaTeX.com \overrightarrow{a}](../../assets/f9dc43643f8775de.png)

![Rendered by QuickLaTeX.com \overrightarrow{b}](../../assets/175f1baaf6f2df62.png)

![Rendered by QuickLaTeX.com \overrightarrow{c}](../../assets/e87b96c5f2ed1196.png)


![Rendered by QuickLaTeX.com \[ \overrightarrow{c} = cos(t\Omega) \hat{x} + sin(t\Omega) \hat{y} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-b565654e80ddc81d9b8570dc5d9f8159_l3.png)


Since ![Rendered by QuickLaTeX.com \overrightarrow{a}](../../assets/f9dc43643f8775de.png)

![Rendered by QuickLaTeX.com \hat{x} = \overrightarrow{a}](../../assets/4f51b2c5b7eca3d5.png)

![Rendered by QuickLaTeX.com \hat{y}](../../assets/dfdf0819009e9fb1.png)

![Rendered by QuickLaTeX.com \overrightarrow{b}](../../assets/175f1baaf6f2df62.png)

![Rendered by QuickLaTeX.com \hat{x}](../../assets/f383f914ab71354e.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \hat{y} &= Normalize(\overrightarrow{b} - proj_{\hat{x}}(\overrightarrow{b})) \\ &= Normalize(\overrightarrow{b} - (\overrightarrow{b} \cdot \hat{x}) \hat{x}) \\ &= Normalize(\overrightarrow{b} - (\overrightarrow{b} \cdot \overrightarrow{a}) \overrightarrow{a}) \\ &= Normalize(\overrightarrow{b} - cos\Omega \, \overrightarrow{a}) \\ &= \frac{\overrightarrow{b} - cos\Omega \, \overrightarrow{a}}{ || \overrightarrow{b} - cos\Omega \, \overrightarrow{a} || } \\ &= \frac{\overrightarrow{b} - cos\Omega \, \overrightarrow{a}}{\sqrt{(\overrightarrow{b} - cos\Omega \, \overrightarrow{a}) \cdot (\overrightarrow{b} - cos\Omega \, \overrightarrow{a})}} \\ &= \frac{\overrightarrow{b} - cos\Omega \, \overrightarrow{a}}{\sqrt{\overrightarrow{b} \cdot \overrightarrow{b} + (\overrightarrow{a} \cdot \overrightarrow{a}) cos^2\Omega - 2(\overrightarrow{a} \cdot \overrightarrow{b})cos\Omega}} \\ &= \frac{\overrightarrow{b} - cos\Omega \, \overrightarrow{a}}{\sqrt{1 + cos^2\Omega - 2cos^2\Omega}} \\ &= \frac{\overrightarrow{b} - cos\Omega \, \overrightarrow{a}}{\sqrt{1 - cos^2\Omega}} \\ &= \frac{\overrightarrow{b} - cos\Omega \, \overrightarrow{a}}{\sqrt{sin^2\Omega}} \\ &= \frac{\overrightarrow{b} - cos\Omega \, \overrightarrow{a}}{sin\Omega} \\ \end{flalign*}](../../assets/e11691f3e61ff9bc.png)


Now plug ![Rendered by QuickLaTeX.com \hat{x}](../../assets/f383f914ab71354e.png)

![Rendered by QuickLaTeX.com \hat{y}](../../assets/dfdf0819009e9fb1.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \overrightarrow{c} &= cos(t\Omega) \hat{x} + sin(t\Omega) \hat{y} \\ &= cos(t\Omega) \overrightarrow{a} + sin(t\Omega) \frac{\overrightarrow{b} - cos\Omega \, \overrightarrow{a}}{sin\Omega} \\ &= (cos(t\Omega) - \frac{sin(t\Omega) \, cos\Omega}{sin\Omega}) \overrightarrow{a} + \frac{sin(t\Omega)}{sin\Omega} \overrightarrow{b} \\ &= \frac{sin\Omega \, cos(t\Omega) - cos\Omega \, sin(t\Omega)}{sin\Omega} \overrightarrow{a} + \frac{sin(t\Omega)}{sin\Omega} \overrightarrow{b} \\ &= \frac{sin((1-t)\Omega)}{sin\Omega} \overrightarrow{a} + \frac{sin(t\Omega)}{sin\Omega} \overrightarrow{b} \end{flalign*}](../../assets/5a175bcd1903f1ce.png)


And voila! We have our slerp formula.

*Edit: Eric Lengyel has pointed out there’s another way to derive the slerp formula using similar triangles, presented in his Mathematics for 3D Game Programming and Computer Graphics, 3rd ed., Section 4.6.3.*