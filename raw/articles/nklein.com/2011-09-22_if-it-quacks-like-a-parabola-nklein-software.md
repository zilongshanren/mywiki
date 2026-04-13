---
title: 'If it quacks like a parabola… :: nklein software'
url: http://nklein.com/2011/09/if-it-quacks-like-a-parabola/
author: Pat
published: '2011-09-22'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I am working on a game idea that involves [(special) relativistic mechanics](http://en.wikipedia.org/wiki/Special_relativity#Relativistic_mechanics) instead of [classical mechanics](http://en.wikipedia.org/wiki/Classical_mechanics). Working out the details that I needed was easy enough if I assumed that:

- ships had a maximum speed at which they could move relative to my base frame
- ships could instantly go from stopped to maximum speed or vice-versa

I didn’t like those assumptions at all. So, I started playing with the equations for relativity. In classical mechanics, the rate-of-change of velocity equals the force you’re applying divided by your mass: .


In special relativity, your mass increases with velocity. So, that equation becomes: (assuming units where the speed of light is 1 unit of distance per 1 unit of time and

is your rest-mass).


For the purposes of this post, I’m going to assume the simplest initial conditions: you start motionless and at the origin. For ease of notation, let . Solving the above differential equation to get a formula for velocity and solving the resulting differential equation to get the distance

you’ve travelled in my base frame by time

, the answer comes out to:

.


I have solved this problem at least thirty times in the past two months. Sometimes I used the simple initial conditions as above. Sometimes I did it in all of its gory details (including the messy case where the applied force is not aligned with the current velocity).

I got the same answer (well, plus the extra mess when I did the full-on problem) every way that I tried it.

So, why did I do it over and over again?

If this were classical mechanics, the end equation would have been . And, I know that for low velocities, the classical mechanics answer should be almost identical to the special relativity answer. And, there was no way that I thought

.


I knew what the graph looked like when

. It is a straight line. It doesn’t look much like the parabola

at all.


My assumption was that since was a straight line for

, then

would be a straight line shifted up one unit and bent (concave-down) a little bit like the graph of

is bent.


Boy was I wrong. Here is a plot of the two together (created with [fooplot](http://fooplot.com/index.php?&type0=0&type1=0&type2=0&type3=0&type4=0&y0=%28-1%2Bsqrt%281%2B%28x%29%5E2%29%29&y1=0.5%20*%20x%5E2&y2=&y3=&y4=&r0=&r1=&r2=&r3=&r4=&px0=&px1=&px2=&px3=&px4=&py0=&py1=&py2=&py3=&py4=&smin0=0&smin1=0&smin2=0&smin3=0&smin4=0&smax0=2pi&smax1=2pi&smax2=2pi&smax3=2pi&smax4=2pi&thetamin0=0&thetamin1=0&thetamin2=0&thetamin3=0&thetamin4=0&thetamax0=2pi&thetamax1=2pi&thetamax2=2pi&thetamax3=2pi&thetamax4=2pi&ipw=1&ixmin=0&ixmax=0.3&iymin=0&iymax=0.05&igx=0.1&igy=0.01&igl=1&igs=0&iax=1&ila=1&xmin=0&xmax=0.3&ymin=0&ymax=0.05)). The red line is the classical mechanics version. The black line is the relativistic version. Here, the force is such that the body is accelerating at a rate of the speed of light per second

so they’ve already gotten up to around 28,000 miles per second before you can see any separation in the graphs here.

Definitely, I can see the resemblance. Now, to fix my intuition about square-roots.

Interestingly, the

looks eerily close to an approximation that I once saw for two-dimensional distance. Doing a little algebra, one comes up with

.

The 2-D distance approximation formula was that

. The relativity/classical approximation above seems to be

for this early portion where

.

I really like the idea of a game where the speed of light is 1 m/s or whatever. It’s basically a Gamow’s “Mr. Tompkins in Wonderland”, the game. It took me an embarrassing long time to find the name of this work considering I work in a building named in his honor. If you haven’t read it, it might give a good foundation for all of the concepts involved without reading something more in depth. There is a copy at http://www.arvindguptatoys.com/arvindgupta/tompkins.pdf. I think the tricky bit will be the time dilation effects and the finite information propagation time.

If your curious, the approximation $\sqrt{1+a^2t^2} \approx 1+\frac{a^2 t^2}{2} – \frac{(a^2 t^2)^2}{8} + \cdots$ is a Taylor expansion for small $a^2 t^2$. I’m sure about that min/max stuff or where it came from. Remember that at a large enough value of $a^2 t^2$, the 1 under the square root becomes negligible and this should basically equal $at$ (a straight line like your intuition told you), not $a^2 t^2$.

I will check out “Mr. Tompkins”. Thanks.

And, yes, I knew that for big enough t, it had to be almost a straight line (with slope speed-of-light). I was just thinking that given what

looks like compared to

would be relevant for

compared to

. And, so I thought that I was ending up with an equation where the instantaneous velocity at the start is unbounded and eventually comes down to the speed-of-light. I should have doubted my intuition long before the 30-th derivation.