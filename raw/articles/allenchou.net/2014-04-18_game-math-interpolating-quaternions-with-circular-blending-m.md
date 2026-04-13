---
title: 'Game Math: Interpolating Quaternions with Circular Blending | Ming-Lun "Allen"
  Chou | 周明倫'
url: https://allenchou.net/2014/04/game-math-interpolating-quaternions-with-circular-blending/
author: Allen Chou
published: '2014-04-18'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

While processing data for skeletal animations, we are usually faced with a series of discrete samples of positions and orientations. The positional samples are typically stored as a series of 3D vectors, and the orientational samples are typically stored as a series of quaternions. The most straightforward way to interpolate between positional samples is using piece-wise lerp (linear interpolation), and the counterpart for orientational samples is using piece-wise slerp (spherical linear interpolation). For more information on slerp, please see my [previous post](http://allenchou.net/2014/04/game-math-quaternion-basics/) on quaternion basics.

The samples are sometimes too far apart, and we can see the visual artifact of discontinuous change in the first-order derivative of interpolation, i.e. the interpolation is not smooth at sample points.

In this post, I will present to you a technique for interpolating orientational samples in a smooth fashion called circular blending. I leaned about this technique from the [MAT 351](https://www.digipen.edu/coursecatalog/#MAT351) class at [DigiPen](https://www.digipen.edu/), taught by professor Matthew Klassen.

Let’s say we are given a series of quaternions:

![Rendered by QuickLaTeX.com \[ q_0, q_1, q_2, ..., q_n \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9383fc1b85b43b6d30f2570418e4d4b0_l3.png)


Let ![Rendered by QuickLaTeX.com q_i](../../assets/9ecc29bbee8e4270.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)

![Rendered by QuickLaTeX.com t](../../assets/2095d761bc925f10.png)

![Rendered by QuickLaTeX.com 0 \le t \le 1](../../assets/e65c8f1cae0d9317.png)

![Rendered by QuickLaTeX.com r_i(t)](../../assets/a3a34d86e4f614cd.png)

![Rendered by QuickLaTeX.com q_i](../../assets/9ecc29bbee8e4270.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)


If we are just using the straightforward slerp approach, we get:

![Rendered by QuickLaTeX.com \[ r_i(t) = Slerp(q_i, q_{i + 1}, t) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5f7073c8f74df33fc311442bdb828218_l3.png)


This is a ![Rendered by QuickLaTeX.com C^0](../../assets/bced1f61ac19e8ef.png)


Circular blending gives us a nice ![Rendered by QuickLaTeX.com C^1](../../assets/9b274e875c162dbd.png)



### Theory

In order to interpolate between two quaternions ![Rendered by QuickLaTeX.com q_i](../../assets/9ecc29bbee8e4270.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)

![Rendered by QuickLaTeX.com q_{i - 1}](../../assets/d2cef773b452c7e2.png)

![Rendered by QuickLaTeX.com q_{i + 2}](../../assets/e671c593492f12ba.png)


![circular blending 0](../../assets/3ae7510920ac7c8b.png)


If we just use piece-wise slerp, this is what the curve will look like:

![circular blending 1](../../assets/54a76e982d7297a7.png)


We can easily see the abrupt change of slope at sample points.

To prepare for circular blending between ![Rendered by QuickLaTeX.com q_i](../../assets/9ecc29bbee8e4270.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)

![Rendered by QuickLaTeX.com q_{i-1}](../../assets/bfda25d163ca3818.png)

![Rendered by QuickLaTeX.com q_i](../../assets/9ecc29bbee8e4270.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)

![Rendered by QuickLaTeX.com q_i](../../assets/9ecc29bbee8e4270.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)

![Rendered by QuickLaTeX.com q_{i + 2}](../../assets/e671c593492f12ba.png)

![Rendered by QuickLaTeX.com C^1_i](../../assets/d4245b36a2b1bf74.png)

![Rendered by QuickLaTeX.com C^2_i](../../assets/9d0e6b02849375a8.png)

![Rendered by QuickLaTeX.com q_i](../../assets/9ecc29bbee8e4270.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)

![Rendered by QuickLaTeX.com r^1_i(t)](../../assets/d3da310768ecc7c2.png)

![Rendered by QuickLaTeX.com r^2_i(t)](../../assets/05328cefd1aef746.png)

![Rendered by QuickLaTeX.com r^1_i(0) = r^2_i(0) = q_i](../../assets/6e5b5a30b66f8821.png)

![Rendered by QuickLaTeX.com r^1_i(1) = r^2_i(1) = q_{i + 1}](../../assets/2082f8b2993caf2a.png)


![circular blending 2](../../assets/92a0345b261f357b.png)


The formula for circular blending between ![Rendered by QuickLaTeX.com q_i](../../assets/9ecc29bbee8e4270.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)


![Rendered by QuickLaTeX.com \[ r_i(t) = Slerp(r^1_i(t), r^2_i(t), t) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-41dd9f96441177f0ec89755590e8ddaf_l3.png)


It is as simple as taking the slerp between the two arcs connecting ![Rendered by QuickLaTeX.com q_i](../../assets/9ecc29bbee8e4270.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)

![Rendered by QuickLaTeX.com r^1_i(t)](../../assets/d3da310768ecc7c2.png)

![Rendered by QuickLaTeX.com q_i](../../assets/9ecc29bbee8e4270.png)

![Rendered by QuickLaTeX.com r^2_i(t)](../../assets/05328cefd1aef746.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)


![circular blending 3](../../assets/c979864ddf6d3b6b.png)


So why does this give us a ![Rendered by QuickLaTeX.com C^1](../../assets/9b274e875c162dbd.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)

![Rendered by QuickLaTeX.com q_{i + 2}](../../assets/e671c593492f12ba.png)

![Rendered by QuickLaTeX.com q_{i + 3}](../../assets/bdf6f4fb83e7ac74.png)

![Rendered by QuickLaTeX.com C^2_{i + 1}](../../assets/1f4d15a18bd3b4d3.png)


![circular blending 4](../../assets/ee97e60fdf56bd86.png)


Notice how the arc ![Rendered by QuickLaTeX.com r^1_{i + 1}(t)](../../assets/8c21e1056a7f0b75.png)

![Rendered by QuickLaTeX.com r_{i + 1}](../../assets/7e7ac7f93852e877.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)

![Rendered by QuickLaTeX.com r^1_{i + 1}(t)](../../assets/8c21e1056a7f0b75.png)

![Rendered by QuickLaTeX.com r^2_i](../../assets/0815e921589fb5c0.png)

![Rendered by QuickLaTeX.com q_{i + 1}](../../assets/65af8f811114f00c.png)


Now let’s look at how we can find these circles and the desired arcs.

### Details & Derivation

Given three points, ![Rendered by QuickLaTeX.com q_0](../../assets/d06d111afd011678.png)

![Rendered by QuickLaTeX.com q_1](../../assets/3e4c130f547249d5.png)

![Rendered by QuickLaTeX.com q_2](../../assets/ea181efa4d91fa24.png)

![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com r(t)](../../assets/1214603af4afb13d.png)

![Rendered by QuickLaTeX.com q_1](../../assets/3e4c130f547249d5.png)

![Rendered by QuickLaTeX.com q_2](../../assets/ea181efa4d91fa24.png)

![Rendered by QuickLaTeX.com r(0) = q_1](../../assets/9d2821997b6b71b4.png)

![Rendered by QuickLaTeX.com r(1) = q_2](../../assets/26e9441389c091f7.png)


![circular blending 5](../../assets/b835ce5f71ffd688.png)


Let ![Rendered by QuickLaTeX.com \overrightarrow{v_1}](../../assets/36a80ec6df0ac2c9.png)

![Rendered by QuickLaTeX.com q_0](../../assets/d06d111afd011678.png)

![Rendered by QuickLaTeX.com q_1](../../assets/3e4c130f547249d5.png)

![Rendered by QuickLaTeX.com \overrightarrow{v_2}](../../assets/5c6aebfa67431f43.png)

![Rendered by QuickLaTeX.com q_0](../../assets/d06d111afd011678.png)

![Rendered by QuickLaTeX.com q_2](../../assets/ea181efa4d91fa24.png)

![Rendered by QuickLaTeX.com m_1](../../assets/7e7085e1f3f6098f.png)

![Rendered by QuickLaTeX.com q_0](../../assets/d06d111afd011678.png)

![Rendered by QuickLaTeX.com q_1](../../assets/3e4c130f547249d5.png)

![Rendered by QuickLaTeX.com m_2](../../assets/f03a4ba3d80bb406.png)

![Rendered by QuickLaTeX.com q_0](../../assets/d06d111afd011678.png)

![Rendered by QuickLaTeX.com q_2](../../assets/ea181efa4d91fa24.png)


![circular blending 6](../../assets/6e5612758dea914b.png)


If we draw the bisectors of ![Rendered by QuickLaTeX.com \overrightarrow{v_1}](../../assets/36a80ec6df0ac2c9.png)

![Rendered by QuickLaTeX.com \overrightarrow{v_2}](../../assets/5c6aebfa67431f43.png)

![Rendered by QuickLaTeX.com \overrightarrow{v_1}](../../assets/36a80ec6df0ac2c9.png)

![Rendered by QuickLaTeX.com \overrightarrow{v_2}](../../assets/5c6aebfa67431f43.png)

![Rendered by QuickLaTeX.com \overrightarrow{n_1}](../../assets/f7b657a424c9ac9c.png)

![Rendered by QuickLaTeX.com \overrightarrow{n_2}](../../assets/f3570c074da947c5.png)


![circular blending 7](../../assets/777ddcd52faad083.png)


To find ![Rendered by QuickLaTeX.com \overrightarrow{n_1}](../../assets/f7b657a424c9ac9c.png)

![Rendered by QuickLaTeX.com \overrightarrow{n_2}](../../assets/f3570c074da947c5.png)


![Rendered by QuickLaTeX.com \[ \overrightarrow{n_1} = \overrightarrow{v_2} - proj_{\overrightarrow{v_1}}(\overrightarrow{v_2}) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-2e62c51c7f27a459ce9297b4970305f8_l3.png)


![Rendered by QuickLaTeX.com \[ \overrightarrow{n_2} = \overrightarrow{v_1} - proj_{\overrightarrow{v_2}}(\overrightarrow{v_1}) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-6a10148e1682136e0273b1e29647f634_l3.png)


where ![Rendered by QuickLaTeX.com proj_{\overrightarrow{a}}(\overrightarrow{b})](../../assets/67220603314e98b7.png)

![Rendered by QuickLaTeX.com \overrightarrow{b}](../../assets/175f1baaf6f2df62.png)

![Rendered by QuickLaTeX.com \overrightarrow{a}](../../assets/f9dc43643f8775de.png)


Now we have the parameterized formula for the two bisectors, ![Rendered by QuickLaTeX.com b_1(s)](../../assets/e84c5ab1fb2040d6.png)

![Rendered by QuickLaTeX.com b_2(t)](../../assets/63b7870079bb079a.png)


![Rendered by QuickLaTeX.com \[ b_1(s) = m_1 + s \overrightarrow{n_1} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9aadc5c659b29209a270cc7e15f505c7_l3.png)


![Rendered by QuickLaTeX.com \[ b_2(t) = m_2 + t \overrightarrow{n_2} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-ac0f8e30a725dbb19f3301b086724121_l3.png)


The center of the circle ![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com (s, t)](../../assets/031a1b44ebd63087.png)


![Rendered by QuickLaTeX.com \[ m_1 + s \overrightarrow{n_1} = m_2 + t \overrightarrow{n_2} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-40cc10dcb89fba393a91fd27a08e339d_l3.png)


If we rearrange the equation, we get:

![Rendered by QuickLaTeX.com \[ s \overrightarrow{n_1} - t \overrightarrow{n_2} = m_2 - m_1 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-f8361eec8cfcebd74ab79d6930b9aee3_l3.png)


Remember that we are working with quaternions, so the vectors ![Rendered by QuickLaTeX.com \overrightarrow{n_1}](../../assets/f7b657a424c9ac9c.png)

![Rendered by QuickLaTeX.com \overrightarrow{n_2}](../../assets/f3570c074da947c5.png)

![Rendered by QuickLaTeX.com (m_2 - m_1)](../../assets/8468a2763e3870a2.png)

[Cramer’s Rule](http://en.wikipedia.org/wiki/Cramer's_rule) to solve for ![Rendered by QuickLaTeX.com (s, t)](../../assets/031a1b44ebd63087.png)

![Rendered by QuickLaTeX.com (s, t)](../../assets/031a1b44ebd63087.png)

![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com s](../../assets/907867aaeb5a72e5.png)

![Rendered by QuickLaTeX.com t](../../assets/2095d761bc925f10.png)


Now that we have the center of the circle ![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com r(t)](../../assets/1214603af4afb13d.png)

![Rendered by QuickLaTeX.com r(0) = q_1](../../assets/9d2821997b6b71b4.png)

![Rendered by QuickLaTeX.com r(1) = q_2](../../assets/26e9441389c091f7.png)


![Rendered by QuickLaTeX.com \[ r(t) = C + R(cos(t\theta)\overrightarrow{u} + sin(t\theta)\overrightarrow{v}), \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9438d6ba72849396db38764fd4a7a80d_l3.png)


where ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com q_1](../../assets/3e4c130f547249d5.png)

![Rendered by QuickLaTeX.com q_2](../../assets/ea181efa4d91fa24.png)

![Rendered by QuickLaTeX.com \theta = cos^{-1}(q_1 \cdot q_2)](../../assets/d8ecb92a69da5b0b.png)

![Rendered by QuickLaTeX.com R](../../assets/ab9820595f7b211b.png)

![Rendered by QuickLaTeX.com \overrightarrow{u}](../../assets/a23129b79b2ff210.png)

![Rendered by QuickLaTeX.com \overrightarrow{v}](../../assets/c9c37f3eca61b6ea.png)


Finding ![Rendered by QuickLaTeX.com \overrightarrow{u}](../../assets/a23129b79b2ff210.png)

![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com q_1](../../assets/3e4c130f547249d5.png)


![Rendered by QuickLaTeX.com \[ \overrightarrow{u} = \frac{q_1 - C}{|q_1 - C|} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-ebe70a8db21e5448915599bcb0e0e09c_l3.png)


As for finding ![Rendered by QuickLaTeX.com \overrightarrow{v}](../../assets/c9c37f3eca61b6ea.png)

![Rendered by QuickLaTeX.com \overrightarrow{w}](../../assets/0b584edc1c35a62f.png)

![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com q_2](../../assets/ea181efa4d91fa24.png)


![Rendered by QuickLaTeX.com \[ \overrightarrow{w} = \frac{q_2 - C}{|q_2 - C|} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5085c4f2c68f847243d788276f00cc2f_l3.png)


and then we can find ![Rendered by QuickLaTeX.com \overrightarrow{u}](../../assets/a23129b79b2ff210.png)

![Rendered by QuickLaTeX.com \overrightarrow{w}](../../assets/0b584edc1c35a62f.png)

![Rendered by QuickLaTeX.com \overrightarrow{u}](../../assets/a23129b79b2ff210.png)


![Rendered by QuickLaTeX.com \[ \overrightarrow{v} = \frac{\overrightarrow{w} - proj_{\overrightarrow{u}}(\overrightarrow{w})}{|\overrightarrow{w} - proj_{\overrightarrow{u}}(\overrightarrow{w})|} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-058b0cc502295894f6fefb213d592c92_l3.png)


Visually, here’s the whole picture:

![circular blending 8](../../assets/fc6e7c7f584df399.png)


We are done! We have found the circle that passes through the three points, as well as the parameterized arc ![Rendered by QuickLaTeX.com r(t)](../../assets/1214603af4afb13d.png)

![Rendered by QuickLaTeX.com r(0) = q_1](../../assets/9d2821997b6b71b4.png)

![Rendered by QuickLaTeX.com r(1) = q_2](../../assets/26e9441389c091f7.png)


One last thing. You might wonder what we should do if the three points are collinear. There’s no way we can find a circle with finite radius that passes through three collinear points! Remember that we are working with unit quaternions here. Three different unit quaternions would never be collinear because they lie on three different spots on the 4D unit hypersphere, just as three different points on a 3D unit sphere would never be collinear. So we are good.

### Demo

Finally, let’s look at a video comparing the results of piece-wise slerp and circular blending in action.

Interesting idea, but why not simply use Catmull-Rom splines? The math is simpler, plus game engines will likely have spline interpolation code already. One could even consider Hermite splines with user-controlled tangents, as is usually done for other animation curves, though I’m not sure how useful this would really be with quaternion.

Yes, the math for Catmull-Rom splines is indeed simpler. I hope I’m not giving the wrong impression that circular blending is superior than any other interpolation techniques; I just wanted to present one of the techniques that can be used to smoothly interpolate quaternions.