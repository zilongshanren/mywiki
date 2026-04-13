---
title: 'Game Math: Precise Control over Numeric Springing | Ming-Lun "Allen" Chou
  | 周明倫'
url: https://allenchou.net/2015/04/game-math-precise-control-over-numeric-springing/
author: Allen Chou
published: '2015-04-08'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

Source files are on [GitHub](https://github.com/TheAllenChou/numeric-springing)

Check out [this post](http://allenchou.net/2015/04/game-math-numeric-springing-examples/) if you want to see more visual examples of numeric springing.

Numeric springing is a very powerful tool for procedural animation. You specify the initial value, initial velocity, target value, and some spring-related parameters; the result is a smooth springing effect. You can apply this technique to all sorts of numeric properties, some common ones being position, rotation, and scale of an object.

![spring](../../assets/d85f4810a40e49be.gif)



### The Common But Designer-Unfriendly Way

Here is a common, yet designer-unfriendly, implementation of numeric springing. Let ![Rendered by QuickLaTeX.com x_i](../../assets/7e4a7ea629624066.png)

![Rendered by QuickLaTeX.com v_i](../../assets/ba3aca2418e63cb0.png)

![Rendered by QuickLaTeX.com i](../../assets/9b7bac1935101c87.png)

![Rendered by QuickLaTeX.com k](../../assets/f9d2296505080664.png)

![Rendered by QuickLaTeX.com d](../../assets/2ec4f4c38fda79cb.png)

![Rendered by QuickLaTeX.com h](../../assets/dcca12480ea32cad.png)

![Rendered by QuickLaTeX.com x_t](../../assets/45ec5c93b4bc1cde.png)


![Rendered by QuickLaTeX.com \begin{flalign*} v_{i+1} &= d v_i + h k (x_t - x_i) \\ x_{i+1} &= x_i + h v_{i+1} \\ \end{flalign*}](../../assets/b8034fba3dc5e5d9.png)


Let’s dissect this implementation.

The difference between the target value and the current value ![Rendered by QuickLaTeX.com (x_t - x_i)](../../assets/eaf06e00554d5f67.png)

![Rendered by QuickLaTeX.com k](../../assets/f9d2296505080664.png)


The new velocity ![Rendered by QuickLaTeX.com v_{i+1}](../../assets/b5eff3037f9353a1.png)

![Rendered by QuickLaTeX.com v_i](../../assets/ba3aca2418e63cb0.png)

![Rendered by QuickLaTeX.com d](../../assets/2ec4f4c38fda79cb.png)


That seems all reasonable and good, but just **what exactly** are the values for ![Rendered by QuickLaTeX.com k](../../assets/f9d2296505080664.png)

![Rendered by QuickLaTeX.com d](../../assets/2ec4f4c38fda79cb.png)

![Rendered by QuickLaTeX.com k](../../assets/f9d2296505080664.png)

![Rendered by QuickLaTeX.com d](../../assets/2ec4f4c38fda79cb.png)


### We Can Be Exact

Now let’s take a look at the differential equation for a damped spring system centered around ![Rendered by QuickLaTeX.com x = x_t](../../assets/209e062e878f6462.png)


![Rendered by QuickLaTeX.com \[ \frac{\mathrm{d}^2 x}{\mathrm{d} t^2}} + 2 \zeta \omega \frac{\mathrm{d} x}{\mathrm{d} t}} + \omega^2 (x - x_t) = 0 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-718f51c540bea215dcd95035ab866442_l3.png)


I won’t go into details as to how this equation is derived. All you really need to know is that ![Rendered by QuickLaTeX.com \omega](../../assets/a6481661bed5b147.png)

![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)


![Rendered by QuickLaTeX.com \omega](../../assets/a6481661bed5b147.png)

**angular frequency** of the oscillation. An angular frequency of ![Rendered by QuickLaTeX.com 2\pi](../../assets/8536ab24b2361d28.png)


![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)

**damping ratio**. A damping ratio of zero means there is no damping at all, and the oscillation just continues indefinitely. A damping ratio between zero and one means the spring system is **underdamped**; oscillation happens, and the magnitude of oscillation decreases exponentially over time. A damping ratio of 1 signifies a **critically damped** system, where this is the point the system stops showing oscillation, but only converging to the target value exponentially. Any damping ratio above 1 means the system is **overdamped**, and the effect of springing becomes more draggy as the damping ratio increases.

Here’s a figure I borrowed form [Erin Catto](https://twitter.com/erin_catto)‘s [presentation](http://box2d.org/files/GDC2011/GDC2011_Catto_Erin_Soft_Constraints.pdf) on soft constraints, to show you the comparison of undamped, underdamped, critically damped, and overdamped systems.

![damping ratios](../../assets/f046926c7fb65c84.png)


Below are the equations for simulating a damped spring system using the [implicit Euler method](http://en.wikipedia.org/wiki/Backward_Euler_method).

![Rendered by QuickLaTeX.com \begin{flalign*} x_{i+1} &= x_i + h v_{i+1} \\ v_{i+1} &= v_i - h (2 \zeta \omega v_{i+1}) - h \omega^2 (x_{i + 1} - x_t) \\ \end{flalign*}](../../assets/4213bbe58adc73ad.png)


Solving ![Rendered by QuickLaTeX.com x_{i+1}](../../assets/6766d8a96afa210e.png)

![Rendered by QuickLaTeX.com v_{i+1}](../../assets/b5eff3037f9353a1.png)

![Rendered by QuickLaTeX.com x_i](../../assets/7e4a7ea629624066.png)

![Rendered by QuickLaTeX.com v_i](../../assets/ba3aca2418e63cb0.png)

[Cramer’s rule](http://en.wikipedia.org/wiki/Cramer%27s_rule), we get:

![Rendered by QuickLaTeX.com \begin{flalign*} x_{i+1} &= \frac{\Delta_x}{\Delta} \\ v_{i+1} &= \frac{\Delta_v}{\Delta}, \\ \end{flalign*}](../../assets/38f51226194126e3.png)


where:

![Rendered by QuickLaTeX.com \begin{flalign*} \Delta &= (1 + 2 h \zeta \omega) + h^2 \omega^2 \\ \Delta_x &= (1 + 2 h \zeta \omega) x_i + h v_i + h^2 \omega^2 x_t \\ \Delta_v &= v_i + h \omega^2 (x_t - x_i) \\ \end{flalign*}](../../assets/f9bd80e37bc21897.png)


Below is a sample implementation in C++. The variables `x`

and `v`

are initialized once and then passed into the function by reference every frame, where the function keeps updating their values every time it’s called.

/* x - value (input/output) v - velocity (input/output) xt - target value (input) zeta - damping ratio (input) omega - angular frequency (input) h - time step (input) */ void Spring ( float &x, float &v, float xt, float zeta, float omega, float h ) { const float f = 1.0f + 2.0f * h * zeta * omega; const float oo = omega * omega; const float hoo = h * oo; const float hhoo = h * hoo; const float detInv = 1.0f / (f + hhoo); const float detX = f * x + h * v + hhoo * xt; const float detV = v + hoo * (xt - x); x = detX * detInv; v = detV * detInv; }

### Designer-Friendly Parameters

Now we have our formula and implementation all worked out, what parameters should we expose to the designers from our spring system so that they can easily tweak the system?

Inspired by the aforementioned presentation by Erin Catto, I propose exposing the **oscillation frequency** ![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

**fraction of oscillation magnitude reduced** ![Rendered by QuickLaTeX.com p_d](../../assets/a5f8ae98f1873fe9.png)

**specific duration** ![Rendered by QuickLaTeX.com t_d](../../assets/c37c3979e53ed7d3.png)


Mapping ![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

![Rendered by QuickLaTeX.com \omega](../../assets/a6481661bed5b147.png)

![Rendered by QuickLaTeX.com 2 \pi](../../assets/949c5e35a55ff142.png)


![Rendered by QuickLaTeX.com \[ \omega = 2 \pi f \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-109c8a04a391e93cb704b748548102f8_l3.png)


Mapping ![Rendered by QuickLaTeX.com p_d](../../assets/a5f8ae98f1873fe9.png)

![Rendered by QuickLaTeX.com t_d](../../assets/c37c3979e53ed7d3.png)

![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)


First you need to understand that the oscillation magnitude decreases exponentially with this curve:

![Rendered by QuickLaTeX.com \[ y(t) = e^{-\zeta \omega t} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-05d2c7c2c4aeb9d8f87a5ebef5513f1b_l3.png)


After plugging in ![Rendered by QuickLaTeX.com p_d](../../assets/a5f8ae98f1873fe9.png)

![Rendered by QuickLaTeX.com t_d](../../assets/c37c3979e53ed7d3.png)


![Rendered by QuickLaTeX.com \[ y(t_d) = e^{-\zeta \omega t_d} = p_d \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1c00cce65cd4a886bee2b415e7e36a80_l3.png)


So we can solve for ![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)


![Rendered by QuickLaTeX.com \[ \zeta = \frac{\ln (p_d)}{-\omega t_d} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-37e5d1175bdf64b450c5d8d64a82ceb3_l3.png)


For example, if we want the oscillation to decrease by 90% (![Rendered by QuickLaTeX.com p_d = 0.1](../../assets/aba315df1494f1bd.png)

![Rendered by QuickLaTeX.com t_d = 0.5](../../assets/630eb8fe254dd04c.png)

![Rendered by QuickLaTeX.com \omega = 4 \pi](../../assets/f3ae12a826db4fd5.png)


![Rendered by QuickLaTeX.com \[ \zeta = \frac{\ln (0.1)}{-4 \pi \cdot 0.5} = 0.367 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-4b85a9139c0b17f57fd3c0ea613bdfef_l3.png)


### Conclusion

Numeric springing is a very powerful tool for procedural animation, and now you know how to precisely control it. Given the desired oscillation frequency and percentage of oscillation magnitude reduction over a specific duration, you can now compute the exact angular frequency ![Rendered by QuickLaTeX.com \omega](../../assets/a6481661bed5b147.png)

![Rendered by QuickLaTeX.com \zeta](../../assets/086183b8ddf30a04.png)


By the way, let’s look at the animated example shown above again:

![spring](../../assets/d85f4810a40e49be.gif)


This animation was created with ![Rendered by QuickLaTeX.com \omega = 8 \pi](../../assets/d0976eef95e0a3b0.png)

![Rendered by QuickLaTeX.com \zeta = 0.23](../../assets/e96b57a58815a957.png)


Hey Allen, thanks for writing this article. It’s leads helping the tweens in my game. One suggestion: the code snippet having abbreviated argument names like x, v, xt, etc made the article and especially the spring function much harder to parse. I think it would help new readers understand quickly if those function had full names.

Thanks for the feedback. I’m glad you find it helpful.

And yes, I did consider using variable names that are more descriptive; however, I decided that it’s more important to have the code nicely formatted without line-wrapping in the blog post, so I kept the variable names short. I think the comments above the function explaining the variables should be enough.

Pingback: Precise Control over Numeric Springing |

Hi Allen, thanks for the post! I just wanted to add one cent to this. If the oscillator has a maximum amplitude of M at start t=0 (in the post M=1), then we just need to multiply Pd by M.

Can you explain? I thought Pd already specifies the percentage of reduction (regardless of M), so M is reduced to Pd * M after duration td. Or am I missing something?

What I meant is that in the post |x(0)| = 1, but what if I want |x(0)| = M, then |x(td)| = Pd*M. However, now that I think more about it, it is better to leave x(t) to be in [-1,1] as it is in your post, and use its value to whatever amplitude we need outside (just like we do with easing functions). Sorry for the confusion :/

Actually, it’s only the figure that says |x(0)| = 1. The equations I showed don’t require |x(0)| = 1. Perhaps I should have clarified that.

wait, but we have explicitly x(t) = exp(-zwt), and from here we have x(t=0) = exp(0) = 1 , or am I missing something?

Yeah. That’s a typo. I meant to write y(t) = exp(-zwt), representing the oscillation reduction percentage (fixed now).