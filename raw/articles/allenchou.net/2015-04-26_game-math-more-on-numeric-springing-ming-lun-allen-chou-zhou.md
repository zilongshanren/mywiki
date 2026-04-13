---
title: 'Game Math: More on Numeric Springing | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2015/04/game-math-more-on-numeric-springing/
author: Allen Chou
published: '2015-04-26'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

Source files are on [GitHub](https://github.com/TheAllenChou/numeric-springing)

Previously, I talked about [numeric springing](http://allenchou.net/2015/04/game-math-precise-control-over-numeric-springing/) and provided [some examples](http://allenchou.net/2015/04/game-math-numeric-springing-examples/).

I have been saving up miscellaneous topics I would like to discuss about numeric springing, and now I have enough to write another post. Here are the topics:

- Using The Semi-Implicit Euler Method
- Numeric Springing vs. Tweening
- Half-Life Parameterization


### Using The Semi-Implicit Euler Method

Recall the differential equation for a damped spring:

![Rendered by QuickLaTeX.com \[ \frac{\mathrm{d}^2 x}{\mathrm{d} t^2}} + 2 \zeta \omega \frac{\mathrm{d} x}{\mathrm{d} t}} + \omega^2 (x - x_t) = 0 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-718f51c540bea215dcd95035ab866442_l3.png)


And the equations for simulating such system obtained by the [implicit Euler method](http://en.wikipedia.org/wiki/Backward_Euler_method):

![Rendered by QuickLaTeX.com \begin{flalign*} x_{i+1} &= \frac{\Delta_x}{\Delta} \\ v_{i+1} &= \frac{\Delta_v}{\Delta}, \\ \end{flalign*}](../../assets/38f51226194126e3.png)


where:

![Rendered by QuickLaTeX.com \begin{flalign*} \Delta &= (1 + 2 h \zeta \omega) + h^2 \omega^2 \\ \Delta_x &= (1 + 2 h \zeta \omega) x_i + h v_i + h^2 \omega^2 x_t \\ \Delta_v &= v_i + h \omega^2 (x_t - x_i) \\ \end{flalign*}](../../assets/f9bd80e37bc21897.png)


I presented the equations obtained by the implicit Euler method, because they are **always stable**. We can obtain a different set of equations that can also be used to simulate a damped spring system by the [semi-implicit Euler method](http://en.wikipedia.org/wiki/Semi-implicit_Euler_method):

![Rendered by QuickLaTeX.com \begin{flalign*} v_{i+1} &= (1 - 2 h \zeta \omega) v_i + h \omega^2 (x_t - x_i) \\ x_{i+1} &= x_i + h v_{i+1} \\ \end{flalign*}](../../assets/5435d8bc8a6e5068.png)


The equations obtained by the semi-implicit Euler method involve much less arithmetic operations, compared to the equations obtained by the implicit Euler method. There is a catch: the equations obtained by the semi-implicit Euler method **can be unstable** under certain configurations and the simulation will blow up over time. This can happen when you have a large ![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)

![Rendered by QuickLaTeX.com \omega](../../assets/a6481661bed5b147.png)

![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)

![Rendered by QuickLaTeX.com \omega](../../assets/a6481661bed5b147.png)

![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)

![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)

![Rendered by QuickLaTeX.com \omega](../../assets/a6481661bed5b147.png)

![Rendered by QuickLaTeX.com 10\pi](../../assets/a0eae02d81c322af.png)


So, if your choice of ![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)

![Rendered by QuickLaTeX.com \omega](../../assets/a6481661bed5b147.png)


Here’s a sample implementation:

/* x - value (input/output) v - velocity (input/output) xt - target value (input) zeta - damping ratio (input) omega - angular frequency (input) h - time step (input) */ void SpringSemiImplicitEuler ( float &x, float &v, float xt, float zeta, float omega, float h ) { v += -2.0f * h * zeta * omega * v + h * omega * omega * (xt - x); x += h * v; }

### Numeric Springing vs. Tweening

Numeric springing and tweening (usually used with the famous [Robert Penner’s easing equations](http://robertpenner.com/easing/)) might seem very similar at first, as they are both techniques to procedurally animate a numeric value towards a target value; however, they are actually fundamentally different. Tweening requires a pre-determined duration; numeric springing, on the other hand, does not have such requirement: numeric springing provides a simulation that goes on indefinitely. If you were to interrupt a procedural numeric animation and give it a new target value, numeric springing would handle this gracefully and the animation would still look very natural and smooth; it is a non-trivial task to interrupt a tweened animation, set up a new tween animation towards the new target value, and prevent the animation from looking visually jarring.

Don’t get me wrong. I’m not saying numeric springing is absolutely superior over tweening. They both have their uses. If your target value can change dynamically and you still want your animation to look nice, use numeric springing. If your animation has a fixed duration with no interruption, then tweening seems to be a better choice; in addition, there are a lot of different easing equations you can choose from that look visually interesting and don’t necessarily have a springy feel (e.g. sine, circ, bounce, slow-mo).

### Half-Life Parameterization

Previously, I proposed a parameterization for numeric springing that consisted of 3 parameters: the **oscillation frequency** ![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

**fraction of oscillation magnitude reduced** ![Rendered by QuickLaTeX.com p_d](../../assets/a5f8ae98f1873fe9.png)

**specific duration** ![Rendered by QuickLaTeX.com t_d](../../assets/c37c3979e53ed7d3.png)


I have received various feedback from forum comments, private messages, friends, and colleagues. The most suggested alternative parameterization was the half-life parameterization, i.e. you specify the duration when the oscillation magnitude is reduced by 50%. So here I’ll show you how to derive ![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)


I’ll use ![Rendered by QuickLaTeX.com \lambda](../../assets/9c8bfcca431ca886.png)

[Chemistry](http://en.wikipedia.org/wiki/Exponential_decay) and [the game](http://en.wikipedia.org/wiki/Half-Life_%28video_game%29).

As previously discussed, the curve representing the oscillation magnitude decreases exponentially with this curve:

![Rendered by QuickLaTeX.com \[ y(t) = e^{-\zeta \omega t} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-05d2c7c2c4aeb9d8f87a5ebef5513f1b_l3.png)


By definition, half-life is the duration of reduction by 50%:

![Rendered by QuickLaTeX.com \[ y(\lambda) = e^{-\zeta \omega \lambda} = 0.5 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-ee182efbee307775314e71ce19f9112f_l3.png)


So we have:

![Rendered by QuickLaTeX.com \[ \zeta \omega = \frac {-\ln (0.5)} {\lambda} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-b32e6589bcceb988fd0fedd256b4f38a_l3.png)


Once we decide the desired ![Rendered by QuickLaTeX.com \lambda](../../assets/9c8bfcca431ca886.png)

![Rendered by QuickLaTeX.com \omega](../../assets/a6481661bed5b147.png)

![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)


![Rendered by QuickLaTeX.com \[ \zeta = \frac {-\ln (0.5)} {\omega \lambda} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-f558789c87be3b57b9cd34f393f909b1_l3.png)


And here’s a sample implementation:

void SpringByHalfLife ( float &x, float &v, float xt, float omega, float h, float lambda ) { const float zeta = -ln(0.5f) / (omega * lambda); Spring(x, v, xt, zeta, omega, h); }

Here’s a graph showing ![Rendered by QuickLaTeX.com \lambda = 0.5](../../assets/2ba0c3b913464a63.png)

![Rendered by QuickLaTeX.com \omega = 4 \pi](../../assets/f3ae12a826db4fd5.png)


![underdamped](../../assets/52aa6061591a8d79.png)


### Conclusion

I’ve discussed how to implement numeric springing using the faster but less stable semi-implicit Euler method, the difference between numeric springing versus tweening, and the half-life parameterization of numeric springing.

I hope this post has given you a better understanding of various aspects and applications of numeric springing.