---
title: 'Game Math: Faster Re-Normalization of Unit Vectors. | Ming-Lun "Allen" Chou
  | 周明倫'
url: https://allenchou.net/2014/02/game-math-fast-re-normalization-of-unit-vectors/
author: Allen Chou
published: '2014-02-28'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

I first saw this technique in an article, [Hacking Quaternions](http://number-none.com/product/Hacking%20Quaternions/), written by [Jonathan Blow](http://number-none.com/) (author of [Braid](http://braid-game.com/)).

To normalize a vector, you divide its individual components by its length.

const Vec3 Normalize(const Vec3 &v) { const float len_sq = v.x * v.x + v.y * v.y + v.z * v.z; const float len_inv = 1.0f / std::sqrt(len_sq); return Vec3(v.x * len_inv, v.y * len_inv, v.z * len_inv); }

The bottle neck of this function is the one divided by a square root, since the square root function is generally not fast. We can do better by using a polynomial approximation of the function ![Rendered by QuickLaTeX.com f(x) = \frac{1}{\sqrt{x}}](../../assets/8b849bc9a8e83962.png)

![Rendered by QuickLaTeX.com x = 1](../../assets/83233175bd6a3be1.png)


Jonathan Blow says that it is more than enough to approximate the function with a polynomial of degree 1 (a straight line); for demonstrative purposes, however, I will show how to approximate ![Rendered by QuickLaTeX.com f(x) = \frac{1}{\sqrt{x}}](../../assets/8b849bc9a8e83962.png)

![Rendered by QuickLaTeX.com x = 1](../../assets/83233175bd6a3be1.png)

[this post](http://allenchou.net/2014/02/game-math-approximation-with-polynomial-curves/).

Our polynomial of degree 2 includes three terms:

![Rendered by QuickLaTeX.com \[ P(x) = a_0 + a_1 x + a_2 x^2 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-08317342f3d86ad352bec82c21864b5d_l3.png)



We will approximate the function around ![Rendered by QuickLaTeX.com x = 1](../../assets/83233175bd6a3be1.png)

![Rendered by QuickLaTeX.com x = 1](../../assets/83233175bd6a3be1.png)

![Rendered by QuickLaTeX.com x = 1](../../assets/83233175bd6a3be1.png)


![Rendered by QuickLaTeX.com \begin{flalign*} P(1) &= f(1) \\ P'(1) &= f'(1) \\ P''(1) &= f''(1) \\ \end{flalign*}](../../assets/31acccbb2c0536f6.png)


With ![Rendered by QuickLaTeX.com f(x) = \frac{1}{\sqrt{x}}](../../assets/8b849bc9a8e83962.png)


![Rendered by QuickLaTeX.com \begin{flalign*} a_0 + a_1 + a_2 &= 1 \\ a_1 + 2 a_2 &= \frac{-1}{2} \\ 2 a_2 &= \frac{3}{4} \\ \end{flalign*}](../../assets/4e79571c76178c99.png)


After solving the system of equations, we have:

![Rendered by QuickLaTeX.com \begin{flalign*} a_0 &= \frac{15}{8} \\ a_1 &= \frac{-5}{4} \\ a_2 &= \frac{3}{8} \\ \end{flalign*}](../../assets/9306e7364f2675da.png)


Let’s see how our approximation looks:

![sqrt_inv](../../assets/addef1f671c34076.png)


The blue curve is the original function ![Rendered by QuickLaTeX.com f(x) = \frac{1}{\sqrt{x}}](../../assets/8b849bc9a8e83962.png)

![Rendered by QuickLaTeX.com x = 1](../../assets/83233175bd6a3be1.png)


Finally, this is what our faster re-normalization function of unit vectors looks like:

inline float FastSqrtInvAroundOne(float x) { const float a0 = 15.0f / 8.0f; const float a1 = -5.0f / 4.0f; const float a2 = 3.0f / 8.0f; return a0 + a1 * x + a2 * x * x; } const Vec3 Normalize(const Vec3 &v) { const float len_sq = v.x * v.x + v.y * v.y + v.z * v.z; const float len_inv = FastSqrtInvAroundOne(len_sq); return Vec3(v.x * len_inv, v.y * len_inv, v.z * len_inv); }

The performance gain is only about 1.25x on my machine, and it’s a little bit faster using just a polynomial of degree 1. It’s not much, but it’s still beneficial to a game since this is a very commonly used function.

I also compared with the performance of [Carmack’s Inverse Square Root](http://en.wikipedia.org/wiki/Fast_inverse_square_root) and found out that both methods are about the same speed on my machine.

Hey Allen, just stumbled upon this from your tweet. I was curious what the error was like on this versus Quake’s FastInvSqrt, so I threw this together: https://plot.ly/~jason.meisel/1/?share_key=CxRuewgKmK6ZNghMEdiU5e

Not surprisingly, your function is slightly more accurate between 0.9 and 1.1. However, even at its worst, FastInvSqrt is only about 0.0022 off, while yours is practically unusable past those bounds.

Neat!

Thanks for taking your time to do the comparison. Yeah, the polynomial approximation is really limited to being used on re-normalizing unit vectors (or any thing that stays around 1.0) and nothing else.

How exactly have i to understand the graphs? If you have a vector with a large or very smalll length, then the error will be significant, wont it? So you should use the approximation if the vector is around the length one?

PS: after the grapghs you wrote, the blue curve is f(x)=1/x but it must be 1/sqrt(x) 😉

Correct. This approximation is only for re-normalizing vectors that are already nearly normalized. For instance, this approach can be used to re-normalize the front, right, and up vectors of your camera matrix every frame. Another example is re-orthogonalizing an orientation matrix, where you convert an orientation matrix to a quaternion, re-normalize the quaternion using this approach, and then convert the quaternion back to the orientation matrix.

Also, thanks for pointing out the typo. It is fixed now.