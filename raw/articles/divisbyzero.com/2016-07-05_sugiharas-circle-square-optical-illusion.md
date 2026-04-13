---
title: Sugihara’s Circle/Square Optical Illusion
url: https://divisbyzero.com/2016/07/05/sugiharas-circlesquare-optical-illusion/
author: Dave Richeson
published: '2016-07-05'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

[Update: Check out my second post in which I provide a template so you can [make your own Sugihara circle/square object out of paper](https://divisbyzero.com/2016/07/06/make-a-sugihara-circlesquare-optical-illusion-out-of-paper/).]

Kokichi Sugihara created a video called [Ambiguous Optical Illusion: Rectangles and Circles.](https://www.youtube.com/watch?v=oWfFco7K9v8) In it he shows a variety of 3-dimensional objects that look like one shape when viewed from the front but look like a different shape in the mirror behind it.

In this blog post we show how he achieved the effect. For simplicity, we will show how he made a shape that looks like a circular cylinder from the front and a square cylinder in the mirror.

The following applet shows our final product (clicking the image links to the [GeoGebra applet](http://ggbm.at/EdSp6X76)). It is a closed curve that represents the top rim of Sugihara’s shape. You can rotate the axes with your mouse. If you view the coordinate system with the positive green and blue axes lined up (1 with 1, 2 with 2, and so on), the curve will look like the unit circle in the green-red plane. If you drag the image so that the positive blue axis lines up with the negative green axis (1 with -1, 2 with -2, and so on), it will look like you are viewing a square (oriented as a diamond) in the green-red plane.


Here are screenshots showing the two views.

![circle](../../assets/621faae24a8f826b.png)

![square](../../assets/88ddda516c0329df.png)


How does it work? It is all about perspective.

To set this up mathematically, we imagine two viewers in 3-dimensional space. One viewer is at and the other is at

(in the video this second viewer is you, in the mirror). They are looking down on a curve

However, from their vantage points it looks like they are seeing two different curves in the

-plane:

and

respectively.


In our example the two observed curves are the unit circle and the square passing through the points , as shown in the

-plane below. We will have to break each of these shapes into two different curves, so we’ll have



and

Also, we could choose

to be some suitably large number greater than 1, but in fact, as we will see, taking the limit as

tends to infinity produces a lovely final expression. For now we will continue to work in generalities and will wait to insert these specifics later.


![xyplane](../../assets/733ab8354a4eccb2.png)


Our aim is now to define Let’s fix

, and let

and

be two points on the curves in the

-plane. In order for the person at

to view her shape,

must lie on the line

(see figure below). Likewise, for the person at

to see his shape,

must lie on the line

Thus,

must be the point of intersection of lines

and

(We know that the lines are not skew because they lie in the plane containing the points


and

and for appropriate choices of


and

the lines intersect and the point of intersection is below


![xyzpic](../../assets/cbad84fccfa13656.png)


It is straightforward to show that is a parametrization of the line

and

is a parametrization of

A little algebra shows shows that their point of intersection is


and thus our desired curve is

Because is a large value, we can take the limit as

goes to infinity. This yields the elegant expression


We may now plug in our functions. The portion of our curve with nonnegative -coordinates is given by


for and the other half by


for This is the curve shown in the applet.


[Update: See the comment by Joshua and my reply for a simpler way of obtaining the parametrization.]

Great! I understand it now.

This was very helpful. With your derivation as the inspiration, I think there is another nice way to see the required curve.

Consider lines between an observer at (0, a, a) and points on the plane y = – z. As a gets larger, these lines get closer to being parallel and perpendicular to the plane. This means that the observer from that position will perceive points in space closer and closer to their perpendicular projections onto that plane (a, b, c) -> (a, b-c, c-b).

Similarly, for the observer at (0, -a, a) and the plane y = z, with the projection (a, b, c) -> (a, b+c, b+c).

Joshua—Thanks for your comment. That’s a great way to think about it. Another way to think about it (which is essentially the same as your way) is to make the simplifying assumption that the vector from a point on the plane curve to the viewer’s eye is parallel to

(and

for the other viewer). Then the line from the points on the curves to the viewers’ eyes are

and

It is easy to find the point of intersection of those lines.

That is so awesome. Thanks for this great exposition.