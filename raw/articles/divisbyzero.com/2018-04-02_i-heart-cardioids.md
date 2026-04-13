---
title: I Heart Cardioids
url: https://divisbyzero.com/2018/04/02/i-heart-cardioids/
author: Dave Richeson
published: '2018-04-02'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Roll a circle around another circle of the same radius. A marked point on the first circle traces a curve called a *cardioid*. (In the figure below we rolled the orange circle around the red circle to draw the green cardioid.) This beautiful heart-shaped curve shows up in some of the most unexpected places. Grab a cup of coffee and we’ll show you some.

![cardioid3](../../assets/16a3ed39255bf0e6.png)


We do not know who discovered the cardioid. In 1637 Étienne Pascal—Blaise’s father—introduced the relative of the cardioid, the limacon, but not the cardioid itself. Seven decades later, in 1708, Philippe de la Hire computed the length of the cardioid—so perhaps he discovered it. In 1741, Johann Castillon gave the cardioid its name.

Got your coffee? Turn on the flashlight feature of your phone and shine the light into the cup from the side. The light reflects off the sides of the cup and forms a caustic on the surface of the coffee. This caustic is a cardioid.

![cardioid6](../../assets/dd66b2ef0f26ea27.png)


The Mandelbrot set is one of the most beautiful images in all of mathematics. It is the set of complex numbers *c* such that the number 0 does not diverge to infinity under repeated iterations of the function *f c*(

*z*)=

*z*

2+

*c*. The Mandelbrot set consists of a heart-shaped region with infinitely many circles, spiny antennae, and other heart-shaped regions growing off of it. That main heart-shaped region? It’s a cardioid.

![cardioid4](../../assets/3cd862f554ee4dc4.jpg)


Cardioids even show up in audio engineering. Sometimes engineers need a uni-directional microphone—one that is very sensitive to sounds directly in front of the microphone and less sensitive to sounds next to or behind it. When they do, they reach for a *cardioid microphone.* The microphone is so-named because the graph of the sensitivity of the microphone in polar coordinates is a cardioid.

In this blog post, we present a few favorite places that cardioids appear. In particular, we will look how we can use lines to construct the curved cardioid. At the end of the blog post, we provide a template that you can use to make your own cardioid. And we provided printable pages that can be used to make a cardioid flip book.

**The Envelope of a Family of Curves**

A common kids math doodle is to draw a set of coordinate axes and then draw line segments from (0,10) to (1,0), from (0,9) to (2,0), and so on. This procedure magically produces a suite of lines that, when viewed together, has what appears to be a curved boundary. This curve is called the *envelope* of the family of lines.

![envelope](../../assets/ccaf7089501a1a3c.png)


Let *C t* denote a family of curves parametrized by

*t.*We can represent them as

*F*(

*x,y,t*)=0 for some function

*C*joins (0,11-

t*t*) to (

*t*,0), so it corresponds to

*F*(

*x,y,t*)= yt+(11-

*t*)(

*x-t*)=0.

Let us look at some features of this envelope. First, each line *C t* is tangent to the curve. Second, if we take two nearby lines

*C*and

t*C*, their point of intersection is near the curve, and taking the limit as

t+hIn the following definition we let denote the partial derivative of

*F* with respect to *t*.

**Definition.** Let be a differentiable function. The

*envelope* of the set of curves *F*(*x,y,t*)=0 is the set of points (*x,y*) such that both *F*(*x,y,t*)=0 and *F t*(

*x,y,t*)=0 for some value of

*t.*

This is a mysterious definition. Why does it produce the envelope? For a fixed *t* and any the curves

*F*(*x,y,t*)=0 and *F*(*x,y,t+h*)=0 (that is, *C t* and

*C*) cross at a point near the envelope. Solving this pair of equations for

t+h*x*and

*y*is equivalent to solving

*F*(

*x,y,t*)=0 and

*x*and

*y.*Then, as

*F*(

*x,y,t*)=0 and

*x*and

*y.*

Returning to our “kids doodle” example, *F t*(

*x,y,t*)=

*y-x*-11+2

*t*. If we set this expression equal to 0, solve for

*t*, and substitute it into

*F*(

*x,y,t*)=0, we obtain the equation (

*x+y*-11)

2-4

*xy*=0, which is a parabola opening along the line

*y=x*. We can see this curve more clearly if we extend our figure beyond 1 through 10.

![envelope2](../../assets/4e323425936aae10.png)


**A Cardioid as an Envelope of Lines**

It turns out that we can construct the cardioid as the envelope of curves, and we can do so in a number of different ways. For instance, pick a point *P* on a circle (the blue circle below, say). Draw circles with centers on the original circle that pass through *P.* The envelope of these circles is a cardioid.

![cardioid2](../../assets/c91d896e6e086219.png)


But we will focus on a different example. Begin with a circle (the red circle below). Mark a certain number of evenly spaced points around the circle, *N,* say, and number them consecutively starting at some point *P*: 0, 1, 2,…, *N*-1. Then for each *n,* draw a line between points *n* and 2*n* (mod *N*). In our example, *N*=54, so we would join points 5 and 10, 19 and 38, and 31 and 8 (since 8 is 62 mod 54). The envelope of these lines is a cardioid.

![cardioid](../../assets/d5fe8834af12ba4e.png)


Let’s see why this is the case. Suppose our circle has center (1,0) and radius 3 and that *P*=(4,0). Now, starting at *P,* find points *t* and 2*t* radians around the circle from *P,* and draw the line segment joining them. We will show show that the envelope of all such lines is the cardioid with polar equation

The two points on the circle—corresponding to *t* and 2*t*—have coordinates and

The line joining them is

After some some algebra and some applications of double angle formulas, we can express this line as

In particular, the expression on the left is our function

*F*(*x,y, t*). Taking the partial derivative of *F* with respect to *t* we obtain

Now, we want to show that the *x* and *y* coordinates at which *F*(*x,y,t*)=*F t*(

*x,y,t*)=0 is a point on the cardioid

*t*and substitute these expressions for

*x*and

*y*in

*F*and

*F*, we obtain 0. (The tedious calculations require both algebra and further applications of the double angle formula.) Thus, the cardioid is the envelope of this family of lines.

t![cardioid8](../../assets/b671a52f8e13b098.png)


**Back to the Coffee Cup**

It turns out that this analysis explains the cardioid in the coffee cup. We can view the caustic as an envelope of lines. As we see below, if we draw lines emanating from a single point *P* on the circle and allow them to reflect off the circle (the angle of incidence equalling the angle of reflection), then the cardioid is the envelope of these lines.

![cardioid5](../../assets/739d73eb84770e35.png)


If the light source is located at point *P,* then a beam of light will reflect off a point *Q* on the circle and strike the circle again at *R* (see figure below). Since arc *PQ* equals arc *QR* arc *PR* is twice arc *PQ.* But then segment *QR* is a line that we would have drawn in the previous construction.

![cardioid7](../../assets/f924ec5db893a043.png)


[Update: When I wrote this post I debated to myself whether to include the following info. Thanks to the nudge by Rick Wicklin in the comments, I decided to add it.] The coffee cup example requires one final comment. In practice, the light source is not at the edge of the coffee cup, but rather, far away. So the rays of light are roughly parallel when they reach the cup. In this case, the curve won’t be a cardioid, but its cousin—a *nephroid*. This is the envelope of lines one obtains by joining *n* and 3*n*. In particular, as we see below, arc *QR* is twice arc *PQ*. (So in our numbering, *n*=0 sits at the point *P*.)![nephroid](../../assets/f7327e53ab49de48.png)


**Draw Your Own Cardioid**

[This printable pdf](https://divisbyzero.com/wp-content/uploads/2018/04/60points.pdf) has a circle with 60 numbered points. Connect each number *n* to the number 2*n* mod 60 to obtain a cardioid. For a little extra fun, try connecting *n* to 3*n* or 4*n* or 5*n* to see what shapes you obtain.

**Flip Book**

[This 12-page pdf](https://divisbyzero.com/wp-content/uploads/2018/04/flipbooksmall.pdf) is a printable flip book. Print the pages double-sided. The pages are designed so that the mathematical figure is on one side and the flip book page number is on the reverse side. Cut out each page, put in numerical order, and secure with a binder clip. Flip through the pages and see the animation in action!

![flip](../../assets/bb94ae9d7c534c1c.jpg)


Beautiful post!

Wonderful description of the elementary properties of caustics in a coffee cup. You might be interested (or already know) that if you assume the light rays are coming from infinity (thus are parallel) then the caustic is called a “nephroid,” which is a cousin of the cardiod. More than 20 years ago (1996), Vic Reiner and I wrote a computer lab for a senior-level course in algebraic geometry at U Minnesota. The lab, called the “Nephroid Lab”, is still available on the internet: http://www.geom.uiuc.edu/~fjw/calc-init/nephroid/ Check it out!

Thanks for the comment and the link! I updated my post with this info.

I didn’t know about the coffee cup. This one was very interesting to me. Thank you!