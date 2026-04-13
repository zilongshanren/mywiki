---
title: 'Game Physics: Stability – Slops | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2014/01/game-physics-stability-slops/
author: Allen Chou
published: '2014-01-01'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

I previously hinted that there will be stability issues as I covered collision resolution. It is because the logic for collision resolution presented earlier is sort of “naive” in a sense that it tries to perfectly resolve all “conflicts”. Nothing is perfect. If you try to perfectly simulate a stack of boxes, you get jitters. This is when the concept of “slop” is introduced, where we become more forgiving to errors and give everything a little bit of leeway.

### Penetration Slop

As mentioned in the [previous post](http://allenchou.net/2013/12/game-physics-resolution-contact-constraints/), Baumgarte Stabilization is a technique for correcting positional errors by applying just enough impulse to push penetrating colliders apart. Without slop, if two colliders are just penetrating by a teeny bit, extra impulse is applied. This would result in unnecessary jitter and objects will hardly sit tight when they are supposed to be at rest.

The condition can be greatly improved if we allow objects to penetrate a bit before actually applying Baumgarte Stabiliation. Recall that the Baumgarte term within the bias term of the contact constraint equation is:

![Rendered by QuickLaTeX.com \[ -\frac{\beta}{\Delta t} \cdot d, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9845be1fb97bb07e87203d0d5f7f8d0a_l3.png)


where ![Rendered by QuickLaTeX.com d](../../assets/2ec4f4c38fda79cb.png)



If we allow a penetration slop, denoted ![Rendered by QuickLaTeX.com Slop_P](../../assets/4de50d83efeffc96.png)


![Rendered by QuickLaTeX.com \[ -\frac{\beta}{\Delta t} \cdot max(d - Slop_P, 0) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-980b9bd0bcd4ccf52cc0769348d5f4cb_l3.png)


The Baumgarte term can reduce to zero if the penetration depth is less than the penetration slop.

### Restitution Slop

Another place we can apply the concept of slop is restitution. With a coefficient of restitution of 0.3 between a bouncing ball and the static floor, it is going to take forever for the ball to settle on the floor if no extra care is taken. Because even when the ball is already bouncing very low, it still always gets a non-zero impulse pushing it back upwards as it hits the floor.

With restitution slop, we take away just a little bit of energy every time a collision occur, so that the bouncing ball would eventually settle on the floor, completely at rest.

Recall the restitution term within the bias term of the contact constraint equation is:

![Rendered by QuickLaTeX.com \[ C_R \, V_C, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-76c59603b31c9caaf881c14fe299a8fc_l3.png)


where ![Rendered by QuickLaTeX.com V_C](../../assets/42382fbe2f746d32.png)


![Rendered by QuickLaTeX.com \[ V_C = (-\overrightarrow{V_A} - \overrightarrow{\omega_A} \times \overrightarrow{r_A} + \overrightarrow{V_B} + \overrightarrow{\omega_B} \times \overrightarrow{r_B}) \cdot \overrightarrow{n} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-931dd210edd3712c415c2fabcfe15dda_l3.png)


If we allow a restitution slop as a tolerance of the closing speed, denoted ![Rendered by QuickLaTeX.com Slop_R](../../assets/77b0a80c35af981b.png)


![Rendered by QuickLaTeX.com \[ C_R \, max(V_C - Slop_R, 0) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7a6d47c49b331b7146c6edf03ce9b707_l3.png)


The restitution term can reduce to zero if the closing speed of two incident objects is less than the restitution slop.

### End of Slops

Here I presented two places in a physics engine where slops can be easily applied to effectively improve the simulation’s stability. I will introduce another technique called “warm starting” in later posts that is also commonly used to improve stability.

Awesome! Keep it up, this is really helping me <3