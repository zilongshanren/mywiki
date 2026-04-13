---
title: 'Game Math: Dot Product, Rulers, And Bouncing Balls | Ming-Lun "Allen" Chou
  | 周明倫'
url: https://allenchou.net/2020/01/dot-product-projection-reflection/
author: Allen Chou
published: '2020-01-18'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

Source files and future updates are available on [Patreon](https://www.patreon.com/TheAllenChou).

You can follow me on [Twitter](https://twitter.com/TheAllenChou).

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

本文之中文翻譯[在此](https://www.allenchou.net/2020/01/dot-product-projection-reflection-chinese)

## Prerequisites

[Trignometry Basics – Sine & Cosine](http://allenchou.net/2019/08/trigonometry-basics-sine-cosine/)[Trigonometry Basics – Tangent, Triangles, And Cannonballs](http://www.allenchou.net/2019/08/tangent-triangles-cannonballs/)[Inverse Trigonometric Functions, Slope Angles, And Facing Objects](http://www.allenchou.net/2019/10/inverse-trig/)

## Overview

The dot product is a simple yet extremely useful mathematical tool. It encodes the relationship between two vectors’ magnitudes and directions into a single value. It is useful for computing projection, reflection, lighting, and so much more.

In this tutorial, you’ll learn:

- The geometric meaning of the dot product.
- How to project one vector onto another.
- How to measure an object’s dimension along an arbitrary ruler axis.

- How to reflect a vector relative to a plane.
- How to bounce a ball off a slope.

## The Dot Product

Let’s say we have two vectors, ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![](../../assets/ca006afa65a4f411.png)

The **dot product** is a mathematical operation that takes two vectors as input and returns a scalar value as output. It is the product of the **signed magnitude** of the first vector’s projection onto the second vector and the magnitude of the second vector. Think of projection as casting shadows using parallel light in the direction perpendicular to the vector being projected onto:

![](../../assets/f51719a3357cefc6.png)

We write the dot product of ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b}](../../assets/dce7ac233073ff31.png)

*a dot b*).

If the angle between the two vectors is less than 90 degrees , the signed magnitude of the first vector is positive (thus simply the magnitude of the first vector). If the angle is larger than 90 degrees, the signed magnitude of the first vector is its negated magnitude.

Which one of the vectors is “the first vector” doesn’t matter. Reversing the vector order gives the same result:

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{a} \cdot \vec{b} = \vec{b} \cdot \vec{a} \end{flalign*}](../../assets/30a60266f5134a4f.png)


If ![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b}](../../assets/dce7ac233073ff31.png)


## Cosine-Based Dot Product Formula

Notice that there’s a right triangle in the figure. Let the angle between ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/c0d24ceaa5b5d56c.png)

Recall from [this tutorial](https://allenchou.net/2019/08/trigonometry-basics-sine-cosine/) that the length of the adjacent side of a right triangle is the length of its hypotenuse multiplied by the cosine of the angle ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \lvert \vec{a} \rvert \cos{\theta}](../../assets/01632481cca73a32.png)


![](../../assets/06ff1a16ab0e2cee.png)

So the dot product of two vectors can be expressed as the product of each vector’s magnitude and the cosine of the angle between the two, which also reaffirms the property that the order of the vectors doesn’t matter:

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{a} \cdot \vec{b} = \lvert \vec{a} \rvert \lvert \vec{b} \rvert \cos{\theta} \end{flalign*}](../../assets/bb77dd5db1cc20d0.png)


If both ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b}](../../assets/dce7ac233073ff31.png)

![Rendered by QuickLaTeX.com \cos{\theta}](../../assets/d53591b39d48d80f.png)


If the two vectors are perpendicular (angle in between is ![Rendered by QuickLaTeX.com 90^\circ](../../assets/f665200c5de23ae0.png)

![Rendered by QuickLaTeX.com 90^\circ](../../assets/f665200c5de23ae0.png)

![Rendered by QuickLaTeX.com 90^\circ](../../assets/f665200c5de23ae0.png)


Since ![Rendered by QuickLaTeX.com \cos{0^\circ} = 1](../../assets/ee67ca26bc80f572.png)

![Rendered by QuickLaTeX.com \cos{180^\circ} = -1](../../assets/5a773d4879a5183a.png)

![Rendered by QuickLaTeX.com \theta = 0](../../assets/7c77f03d6fb24017.png)

![Rendered by QuickLaTeX.com \theta = 180^\circ](../../assets/aeaad8051ab76bf3.png)

![Rendered by QuickLaTeX.com \lvert \vec{a} \rvert \lvert \vec{b} \rvert](../../assets/361752b374aede4b.png)

![Rendered by QuickLaTeX.com - \lvert \vec{a} \rvert \lvert \vec{b} \rvert](../../assets/8c240daa181080fa.png)


## Component-Based Dot Product Formula

When we have two 3D vectors as triplets of floats, it isn’t immediately clear what the angle in between them are. Luckily, there’s an alternate way to compute the dot product of two vectors that doesn’t involve taking the cosine of the angle in between. Let’s denote the components of ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \vec{a} &= (a_x, a_y, a_z) \\ \vec{b} &= (b_x, b_y, b_z) \end{flalign*}](../../assets/4c9441a5aa027d0b.png)


Then the dot product of the two vectors is also equal to the sum of component-wise products, and can be written as:

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{a} \cdot \vec{b} = a_x b_x + a_y b_y + a_z b_z \end{flalign*}](../../assets/8cea86c4e6c61dce.png)


Simple, and no cosine needed!

Unity provides a function `Vector3.Dot`

for computing the dot product of two vectors:

float dotProduct = Vector3.Dot(a, b);

Here is an implementation of the function:

Vector3 Dot(Vector3 a, Vector b) { return a.x * b.x + a.y * b.y + a.z * b.z; }

The formula for computing a vector’s magnitude is ![Rendered by QuickLaTeX.com \lvert \vec{a} \rvert = \sqrt{a_x^2 + a_y^2 + a_z^2}](../../assets/1ffc13e9c125d080.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \lvert \vec{a} \rvert = \sqrt{\vec{a} \cdot \vec{a}} \end{flalign*}](../../assets/47c0dad126d9c205.png)


Recall the formula ![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b} = \lvert \vec{a} \rvert \lvert \vec{b} \rvert \cos{\theta}](../../assets/dfac780a221c54ac.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \theta = \cos^{-1}{(\frac{\vec{a} \cdot \vec{b}}{\lvert \vec{a} \rvert \lvert \vec{b} \rvert})} \end{flalign*}](../../assets/a3a8f6fbdce0b37e.png)


If ![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \vec{a} \cdot \vec{b} &= \cos{\theta} \\ \theta &= \cos^{-1}{(\vec{a} \cdot \vec{b})} \end{flalign*}](../../assets/df925c56eb58d03e.png)


## Vector Projection

Now that we know the geometric meaning of the dot product as the product of a projected vector’s signed magnitude and another vector’s magnitude, let’s see how we can project one vector onto another. Let ![Rendered by QuickLaTeX.com \vec{c} = {project}_{\vec{b}}(\vec{a})](../../assets/ce16b7dfc4116b5f.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![](../../assets/63c79315691e125f.png)

The unit vector in the direction of ![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \frac{\vec{b}}{\lvert \vec{b} \rvert}](../../assets/da576e21adaa434d.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{c}](../../assets/f80e34d6e3bd75fb.png)

![Rendered by QuickLaTeX.com \vec{c}](../../assets/f80e34d6e3bd75fb.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


Since the dot product ![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b}](../../assets/dce7ac233073ff31.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{c}](../../assets/f80e34d6e3bd75fb.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \frac{\vec{a} \cdot \vec{b}}{\lvert \vec{b} \rvert} \end{flalign*}](../../assets/3ee40892e3be8a17.png)


Multiplying this signed magnitude with the unit vector ![Rendered by QuickLaTeX.com \frac{\vec{b}}{\lvert \vec{b} \rvert}](../../assets/da576e21adaa434d.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \vec{c} = {project}_{\vec{b}}(\vec{a}) = \frac{\vec{a} \cdot \vec{b}}{{\lvert \vec{b} \rvert}^2} \: \vec{b} \end{flalign*}](../../assets/a4e515813bda8918.png)


Recall that ![Rendered by QuickLaTeX.com {\lvert \vec{b} \rvert}^2 = \vec{b} \cdot \vec{b}](../../assets/7d39973fe8ec11f2.png)


![Rendered by QuickLaTeX.com \begin{flalign*} {project}_{\vec{b}}(\vec{a}) = \frac{\vec{a} \cdot \vec{b}}{\vec{b} \cdot \vec{b}} \: \vec{b} \end{flalign*}](../../assets/7e95adfc2d32ce56.png)


And if ![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)


![Rendered by QuickLaTeX.com \begin{flalign*} {project}_{\vec{b}}(\vec{a}) = (\vec{a} \cdot \vec{b}) \: \vec{b} \end{flalign*}](../../assets/f5d59ae6058c7db4.png)


Unity provides a function `Vector3.Project`

that computes the projection of one vector onto another:

Vector3 projection = Vector3.Project(vec, onto);

Here is an implementation of the function:

Vector3 Project(Vector3 vec, Vector3 onto) { float numerator = Vector3.Dot(vec, onto); float denominator = Vector3.Dot(onto, onto); return (numerator / denominator) * onto; }

Sometimes we need to guard against a potential degenerate case, where the vector being projected onto is a zero vector or a vector with an overly small magnitude, producing a numerical explosion as the projection involves division by zero or near-zero. This can happen with Unity’s `Vector3.Project`

function.

One way to handle this is to compute the magnitude of the vector being projected onto. Then, if the magnitude is too small, use a fallback vector (e.g. the unit +X vector, the forward vector of a character, etc.):

Vector3 SafeProject(Vector3 vec, Vector3 onto, Vector3 fallback) { float sqrMag = v.sqrMagnitude; if (sqrMag > Epsilon) // test against a small number return Vector3.Project(vec, onto); else return Vector3.Project(vec, fallback); }

## Exercise: Ruler

Here’s an exercise for vector projection: make a ruler that measures an object’s dimension along an arbitrary axis.

A ruler is represented by a base position (a point) and an axis (a unit vector):

struct Ruler { Vector3 Base; Vector3 Axis; }

Here’s how you project a point onto the ruler. First, find the relative vector from the ruler’s base position to the point. Next, project this relative vector onto the ruler’s axis. Finally, the point’s projection is the ruler’s base position offset by the projected relative vector:

![](../../assets/8894b962cbb925f7.png)

Vector3 Project(Vector3 vec, Ruler ruler) { // compute relative vector Vector3 relative = vec - ruler.Base; // projection float relativeDot = Vector3.Dot(vec, ruler.Axis); Vector3 projectedRelative = relativeDot * ruler.Axis; // offset from base Vector3 result = ruler.Base+ projectedRelative; return result; }

The intermediate `relativeDot`

value above basically measures how far away the point’s projection is from the ruler’s base position, in the direction of the ruler’s axis if positive, or in the opposite direction of the ruler’s axis if negative.

If we compute such measurement for each vertex of an object’s mesh and find the minimum and maximum measurements, then we can obtain the object’s dimension measured along the ruler’s axis by subtracting the minimum from the maximum. Offsetting from the ruler’s base position by the ruler’s axis vector multiplied by these two extreme values gives us the two ends of the projection of the object onto the ruler.

void Measure ( Mesh mesh, Ruler ruler, out float dimension, out Vector3 minPoint, out Vector3 maxPoint ) { float min = float.MaxValue; float max = float.MinValue; foreach (Vector3 vert in mesh.vertices) { Vector3 relative = vert- ruler.Base; float relativeDot = Vector3.Dot(relative , ruler.Axis); min = Mathf.Min(min, relativeDot); max = Mathf.Max(max, relativeDot); } dimension = max - min; minPoint = ruler.Base+ min * ruler.Axis; maxPoint = ruler.Base+ max * ruler.Axis; }

## Vector Reflection

Now we are going to take a look at how to reflect a vector, denoted ![Rendered by QuickLaTeX.com \vec{v}](../../assets/fe0c58e4e9fa1ad9.png)

![Rendered by QuickLaTeX.com \vec{n}](../../assets/f4d4d2619671dfcd.png)


![](../../assets/e8aacdc36d3f6ee5.png)

We can decompose the vector to be reflected into a parallel component (denoted ![Rendered by QuickLaTeX.com \vec{v}_\parallel](../../assets/939aeedbea4cfe2b.png)

![Rendered by QuickLaTeX.com \vec{v}_\perp](../../assets/1902ddf4c29d8b29.png)


![](../../assets/90426688095a8f46.png)

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{v} = \vec{v}_\parallel + \vec{v}_\perp \end{flalign*}](../../assets/2bb65b210eab5835.png)


The perpendicular component is the projection of the vector onto the plane’s normal, and the parallel component can be obtained by subtracting the perpendicular component from the vector:

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{v}_\perp &= {project}_{\vec{n}}(\vec{v}) \\ \vec{v}_\parallel &= \vec{v} - \vec{v}_\perp \end{flalign*}](../../assets/71dc7da5f40536de.png)


Flipping the direction of the perpendicular component and adding it to the parallel component gives us the reflected vector off the plane.

![](../../assets/f2459092fab4e31d.png)

Let’s denote the reflection ![Rendered by QuickLaTeX.com {reflect}_\vec{n}}(\vec{v}](../../assets/a01dad2dba6a36d8.png)


![Rendered by QuickLaTeX.com \begin{flalign*} {reflect}_{\vec{n}}(\vec{v}) = \vec{v}_\parallel - \vec{v}_\perp \end{flalign*}](../../assets/11fe5bd0e63de87b.png)


If we substitute ![Rendered by QuickLaTeX.com \vec{v}_\parallel](../../assets/939aeedbea4cfe2b.png)

![Rendered by QuickLaTeX.com \vec{v} - \vec{v}_\perp](../../assets/bca3004e5fba2b1c.png)


![Rendered by QuickLaTeX.com \begin{flalign*} {reflect}_{\vec{n}}(\vec{v}) = \vec{v} - 2\vec{v}_\perp \end{flalign*}](../../assets/c3d51225f5cc9a55.png)


Unity provides a function `Vector3.Reflect`

for computing vector reflection:

float reflection = Vector3.Reflect(vec, normal);

Here is an implementation of the function using the first reflection formula:

Vector3 Reflect(Vector vec, Vector normal) { Vector3 perpendicular= Vector3.Project(vec, normal); Vector3 parallel = vec - perpendicular; return parallel - perpendicular; }

And here is an implementation using the alternative formula:

Vector3 Reflect(Vector vec, Vector normal) { return vec - 2.0f * Vector3.Project(vec, normal); }

## Exercise: Bouncing A Ball Off A Slope

Now that we know how to reflect a vector relative to a plane, we are well-equipped to simulate a ball bouncing off a slope.

We are going to use the Euler Method mentioned in a [previous tutorial](https://www.allenchou.net/2019/08/tangent-triangles-cannonballs/) to simulate the trajectory of a ball under the influence of gravity.

ballVelocity+= gravity * deltaTime; ballCenter += ballVelocity* deltaTime;

In order to detect when the ball hits the slope, we need to know how to detect when a ball penetrates a plane.

A sphere can be defined by a center and a radius. A plane can be defined by a normal vector and a point on the plane. Let’s denote the sphere’s center ![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com R](../../assets/ab9820595f7b211b.png)

![Rendered by QuickLaTeX.com \vec{n}](../../assets/f4d4d2619671dfcd.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com \vec{u}](../../assets/cd0fea837a52d7bd.png)


![](../../assets/fcb316ffa3c6838d.png)

If the sphere does not penetrate the plane, the component of ![Rendered by QuickLaTeX.com \vec{u}](../../assets/cd0fea837a52d7bd.png)

![Rendered by QuickLaTeX.com \vec{u}_\perp](../../assets/05825d1d8662c6ad.png)

![Rendered by QuickLaTeX.com \vec{n}](../../assets/f4d4d2619671dfcd.png)

![Rendered by QuickLaTeX.com R](../../assets/ab9820595f7b211b.png)


![](../../assets/b2d24696ae6cc040.png)

In other words, the sphere does not penetrate the plane if ![Rendered by QuickLaTeX.com \vec{u} \cdot \vec{n} > R](../../assets/f25bd93dec613edf.png)

![Rendered by QuickLaTeX.com R - \vec{u} \cdot \vec{n}](../../assets/a3c4ee7db51b97a2.png)


In order to correct a penetrating sphere’s position, we can simply move the sphere in the direction of the plane’s normal ![Rendered by QuickLaTeX.com \vec{n}](../../assets/f4d4d2619671dfcd.png)


// returns original sphere center if not penetrating // or corrected sphere center if penetrating void SphereVsPlane ( Vector3 c, // sphere center float r, // sphere radius Vector3 n, // plane normal (unit vector) Vector3 p, // point on plane out Vector3 cNew, // sphere center output ) { // original sphere position as default result cNew = c; Vector3 u = c - p; float d = Vector3.Dot(u, n); float penetration = r - d; // penetrating? if (penetration > 0.0f) { cNew = c + penetration * n; } }

And then we insert the positional correction logic after the integration.

ballVelocity += gravity * deltaTime; ballCenter += ballVelocity* deltaTime; Vector3 newSpherePosition; SphereVsPlane ( ballCenter, ballRadius, planeNormal, pointOnPlane, out newBallPosition ); ballPosition = newBallPosition;

We also need to reflect the sphere’s velocity relative to the slope upon positional correction due to penetration, so it bounces off correctly.

The animation above shows a perfect reflection and doesn’t seem natural. We’d normally expect some sort of degradation in the bounced ball’s velocity, so it bounces less with each bounce.

This is typically modeled as a **restitution** value between the two colliding objects. With 100% restitution, the ball would bounce off the slope with perfect velocity reflection. With 50% restitution, the magnitude of the ball’s velocity component perpendicular to the slope would be cut in half. The restitution value is the ratio of magnitudes of the ball’s perpendicular velocity components after versus before the bounce. Here is a revised vector reflection function with restitution taken into account:

Vector3 Reflect ( Vector3 vec, Vector3 normal, float restitution ) { Vector3 perpendicular= Vector3.Project(vec, normal); Vector3 parallel = vec - perpendicular; return parallel - restitution * perpendicular; }

Here is the modified `SphereVsPlane`

function that takes variable restitution into account:

// returns original sphere center if not penetrating // or corrected sphere center if penetrating void SphereVsPlane ( Vector3 c, // sphere center float r, // sphere radius Vector3 v, // sphere velocity Vector3 n, // plane normal (unit vector) Vector3 p, // point on plane float e, // restitution out Vector3 cNew, // sphere center output out Vector3 vNew // sphere velocity output ) { // original sphere position & velocity as default result cNew = c; vNew = v; Vector3 u = c - p; float d = Vector3.Dot(u, n); float penetration = r - d; // penetrating? if (penetration > 0.0f) { cNew = c + penetration * n; vNew = Reflect(v, n, e); } }

And the positional correction logic is replaced with a complete bounce logic:

ballVelocity+= gravity * deltaTime; spherePosition += ballVelocity* deltaTime; Vector3 newSpherePosition; Vector3 newSphereVelocity; SphereVsPlane ( spherePosition , ballRadius, ballVelocity, planeNormal, pointOnPlane, restitution, out newBallPosition, out newBallVelocity; ); ballPosition= newBallPosition; ballVelocity= newBallVelocity;

Finally, now we can have balls with different restitution values against a slope:

## Summary

In this tutorial, we have been introduced to the geometric meaning of the dot product and its formulas (cosine-based and component-based).

We have also seen how to use the dot product to project vectors, and how to use vector projection to measure objects along an arbitrary ruler axis.

Finally, we have learned how to use the dot product to reflect vectors, and how to use vector reflection to simulate balls bouncing off a slope.

If you enjoyed this tutorial and would like to see more, please consider supporting me on [Patreon](https://www.patreon.com/TheAllenChou). By doing so, you can also get updates on future tutorials. Thanks!

This is very a well tutorial !

The small exercises to reinforce the concepts are a big win.

Consider doing something like this on Udemy.

Cheers

b

This is a great tutorial. Thanks!