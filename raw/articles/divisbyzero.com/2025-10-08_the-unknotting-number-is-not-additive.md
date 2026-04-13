---
title: The Unknotting Number is Not Additive
url: https://divisbyzero.com/2025/10/08/the-unknotting-number-is-not-additive/
author: Dave Richeson
published: '2025-10-08'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

On June 30, 2025, Mark Brittenham and Susan Hermiller uploaded a preprint to the arXiv called “[Unknotting number is not additive under connected sum](https://arxiv.org/abs/2506.24088)” (and an updated version on September 15, 2025). In it, they surprised the mathematical community by giving a counterexample to a long-standing conjecture in knot theory. The story was picked up by publications like * Scientific American* and

*and by math YouTuber*

[Quanta](https://www.quantamagazine.org/a-simple-way-to-measure-knots-has-come-unraveled-20250922/)[Matt Parker](https://www.youtube.com/watch?v=Dx7f-nGohVc).

The conjecture is easy to understand, although we need a few definitions first.

** (Mathematical) knot**: We can think of a mathematical knot as a loop of string sitting in three-dimensional space. In other words, if we took a piece of string, tied a knot, and then glued the two ends together, we’d get a mathematical knot.

**Knot projection:** Given any mathematical knot, we draw a two-dimensional version of it in the plane. It is like the shadow of the knot, but with breaks in the knot to indicate which strand is on top and which is on the bottom.

** Unknotting number:** If we have the projection of a knot, we can change some crossings (change which strand is over and which is under) to make it unknotted (called the unknot). To compute the unknotting number of a knot

*K*,

*u*(

*K*), we look at all possible projections and find the fewest number of crossing changes we must make to obtain the unknot.

**Connected sum:** Given two knots, *J* and *K*, we can cut each knot at one point and join the cut ends to form a new, larger knot, *J*#*K*. This is called the connected sum of the knots.

Below, we see a knot called the (2,7) [torus knot](https://en.wikipedia.org/wiki/Torus_knot) and its mirror image (left), and their connected sum on the right.

![](../../assets/68355ca473fa66a6.jpg)


![](../../assets/68355ca473fa66a6.jpg)

Although unknotting numbers are notoriously difficult to compute, we know that the unknotting number of a (*p,q*) torus knot is (p-1)(q-1)/2. So, the (2,7) torus knots above have unknotting number (2 – 1)(7 – 1)/2 = 3. It is not difficult to check that by changing three crossings of the projections shown above, the (2,7) torus knot becomes the unknot. It turns out that changing two crossings does not suffice in this projection or any projection.

Likewise, changing 3 + 3 = 6 crossings of the connected sum will yield the unknot. In fact, it will always be the case that *u*(*J*#*K*) ≤* u*(*J*) +* u*(*K*). The question is: are these equal? An “old” conjecture (which was implicit in an article 88 years ago), states:

**Conjecture: **If *J* and *K* are knots, then *u*(*J*#*K*) =* u*(*J*) +* u*(*K*).

In their preprint, Brittenham and Hermiller disprove the conjecture by giving a counterexample! Moreover, the counterexample is precisely the one I’ve shown above! The connected sum of the torus knot with its mirror image has unknotting number 5, which is clearly less than 3 + 3.

That said, we can’t simply change the five crossings in the above projection to obtain the unknot. We must produce a different projection first. But what is it?

I looked for the answer online and found this [arXiv preprint](https://arxiv.org/abs/2507.14265) by Chao Wang and Yimu Zhang, which gives the details. They provide the projection and the crossings that must be changed. However, the projection has 56 crossings (far more than the original 14!). They assert, but do not show, that the resulting knot—after the five crossings are changed—is the unknot. They end by writing, “We prefer to leave it to the readers as an interesting game.”

Never good at resisting a good [nerd sniping](https://xkcd.com/356/), I decided to take them up on the challenge. I’m embarrassed to admit how long it took me to confirm their work, but I did it. Here is my redrawn version of the knot projection—the connected sum of the (2,7) torus knot and its mirror image. The circled crossings are the five that must be changed.

![](../../assets/d4827cce72b7c5b6.jpg)


![](../../assets/d4827cce72b7c5b6.jpg)

After having done so, here’s the resulting projection. Wang and Zhang claim that it is the unknot!

![](../../assets/8be08ee68f34ffe3.jpg)


![](../../assets/8be08ee68f34ffe3.jpg)

Without further ado, here are my drawings. This first sequence shows how I get from the usual projection of the connected sum to the projection in which the crossings must be made. The red strands show the part of the projection that has changed from the previous projection.

![](../../assets/f03c79b8c65fbc20.jpg)


![](../../assets/f03c79b8c65fbc20.jpg)

![](../../assets/af102cd9a248bdd2.jpg)


![](../../assets/af102cd9a248bdd2.jpg)

![](../../assets/0f363c71134a8f35.jpg)


![](../../assets/0f363c71134a8f35.jpg)

Thus, the final image above is the knot we claim is the unknot. The following sequence of steps shows that it is indeed the unknot.

![](../../assets/42180306d1aae366.jpg)


![](../../assets/42180306d1aae366.jpg)

![](../../assets/e6053dfd2ae6facc.jpg)


![](../../assets/e6053dfd2ae6facc.jpg)

![](../../assets/8a34e8baec710f4a.jpg)


![](../../assets/8a34e8baec710f4a.jpg)

![](../../assets/0a3a542c022f92f0.jpg)


![](../../assets/0a3a542c022f92f0.jpg)

![](../../assets/f4d4e5a382ed8f68.jpg)


![](../../assets/f4d4e5a382ed8f68.jpg)

Ta da!!!