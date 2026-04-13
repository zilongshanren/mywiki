---
title: 'Game Math: Trigonometry Basics – Tangent, Triangles, And Cannonballs | Ming-Lun
  "Allen" Chou | 周明倫'
url: https://allenchou.net/2019/08/tangent-triangles-cannonballs/
author: Allen Chou
published: '2019-08-31'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

Source files and future updates are available on [Patreon](https://www.patreon.com/TheAllenChou).

You can follow me on [Twitter](https://twitter.com/TheAllenChou).

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

本文之中文翻譯[在此](http://allenchou.net/2019/09/tangent-triangles-cannonballs-chinese/)

## Prerequisite

## Overview

In the [previous tutorial](http://allenchou.net/2019/08/trigonometry-basics-sine-cosine/), we have learned about two basic trigonometric functions: sine & cosine. This time, we are going to look at another basic trigonometric function: tangent. Together, these three functions form the basis of trigonometry, and they can be used to solve all sorts of geometric problems that arise in game development.

In this tutorial, you’ll learn:

- A geometric interpretation of another basic trigonometric function: tangent.
- The relationships among sine, cosine, and tangent.
- How to use tangent to create smooth intro and outro motion.

- How to relate angles and sides of right triangles using trigonometric functions.
- How to simulate a cannonball, given an initial speed and an elevation angle.
- How to draw predicted trajectories even before firing the cannonball.

- How to place cannonball targets, given a horizontal distance and an elevation angle.

![](../../assets/825f655807c2490f.png)

## Geometric Interpretation of Tangent

Let’s look at the unit circle from the last tutorial, with a point ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)


Recall that the coordinates ![Rendered by QuickLaTeX.com (X, Y)](../../assets/20a6cdca242db178.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com (\cos\theta, \sin\theta)](../../assets/a390ac661a350c78.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

**slope** of the line segment between ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)


The slope of a line is its ratio of vertical change versus horizontal change. For example, let’s look at this line segment:

![](../../assets/b34fff32455b8764.png)

To move from point ![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com \frac{2}{3}](../../assets/627f54537ffac34d.png)


And for a line segment that goes “downhill” like this:

![](../../assets/a7a2875a50b458e0.png)

The slope would be ![Rendered by QuickLaTeX.com \frac{-2}{3}](../../assets/1d1e638e20df8e10.png)


Now, back to the unit circle figure:

We see that moving from the origin to ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com \frac{\sin\theta}{\cos\theta}](../../assets/f9e6e88a475b17d4.png)

![Rendered by QuickLaTeX.com \tan\theta = \frac{\sin\theta}{\cos\theta}](../../assets/75252588076cb604.png)


But that’s just a mathematical expression. Here’s where ![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)


Let’s just look at the portion of this tangential line that is between ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)


![](../../assets/57a2ee7aa01e50e3.png)

The angles ![Rendered by QuickLaTeX.com \angle ABP](../../assets/2322e18a282b421a.png)

![Rendered by QuickLaTeX.com \angle APD](../../assets/501362fc817ef786.png)

![Rendered by QuickLaTeX.com \angle PAB = \angle PAD = \theta](../../assets/a3b87106ce8f51b0.png)

![Rendered by QuickLaTeX.com \overline{AB}](../../assets/01731d67b55d82ca.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)


Now, split the figure into two triangles:

![](../../assets/704d38a5dd782f60.png)

Since all internal angles of a triangle add up to ![Rendered by QuickLaTeX.com 180^\circ](../../assets/831c30544c8a897a.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com 90^\circ](../../assets/f665200c5de23ae0.png)

![Rendered by QuickLaTeX.com \angle APB](../../assets/194985a69e6859a7.png)

![Rendered by QuickLaTeX.com \angle ADP](../../assets/ebbe60f9f75d0ec5.png)

![Rendered by QuickLaTeX.com 180^\circ - \theta - 90^\circ](../../assets/0f6e06a47b085ff2.png)


If two triangles have identical sets of angles, then they are **similar**, i.e. if you proportionally scale, rotate, and/or flip one of them, it can become identical to the other one.

When two triangles are similar, the ratio between the lengths of two sides from one triangle equals to the ratio between the lengths of the corresponding sides of the other triangle. Thus:

![Rendered by QuickLaTeX.com \begin{flalign*} \frac{\overline{BP}}{\overline{AB}} = \frac{\overline{DP}}{\overline{AP}} \end{flalign*}](../../assets/14cd90c5ba3f6d72.png)


We know that the coordinates of ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com (\cos\theta, \sin\theta)](../../assets/a390ac661a350c78.png)

![Rendered by QuickLaTeX.com \overline{AB} = \cos\theta](../../assets/8f87b230a143085e.png)

![Rendered by QuickLaTeX.com \overline{BP} = \sin\theta](../../assets/a675e5d40d6ad3bc.png)

![Rendered by QuickLaTeX.com \overline{AP}](../../assets/f8fcf9c44fc38692.png)

![Rendered by QuickLaTeX.com \overline{AP}=1](../../assets/63da667cf2d77044.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \frac{\sin\theta}{\cos\theta} = \frac{\overline{DP}}{1} \end{flalign*}](../../assets/e2c8dfc13592fbd4.png)


And we know that ![Rendered by QuickLaTeX.com \tan\theta = \frac{\sin\theta}{\cos\theta}](../../assets/75252588076cb604.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \tan\theta = \overline{DP} \end{flalign*}](../../assets/15a52a4f57f60b58.png)


We have found the visual representation of ![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)


![](../../assets/c2b3dede1434c7a0.png)

The absolute value of ![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

*absolute value*, because depending on the signs of ![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)


## The Tangent Curve

We’ve seen the plots for ![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/b09117852d9c1c33.png)

And now let’s add ![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)


![](../../assets/966a7142b9ff96d9.png)

Notice how, unlike ![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com [-1, 1]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-96395345c57f8928c42918c656dd1364_l3.png)

![Rendered by QuickLaTeX.com \tan = \frac{\sin\theta}{\cos\theta}](../../assets/fe81b30ffa997615.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com \pi](../../assets/4b60fce59d6919ef.png)

![Rendered by QuickLaTeX.com 2\pi](../../assets/8536ab24b2361d28.png)


Another thing worth noting is the relationships among the signs of the three basic trigonometric functions. Since ![Rendered by QuickLaTeX.com \tan\theta = \frac{\sin\theta}{\cos\theta}](../../assets/75252588076cb604.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)


Now, let’s try plugging the tangent curve over time into the X coordinate of an object:

float tan = Mathf.Tan(Rate * Time.time); obj.transform.position = Vector3(tan, 0.0f, 0.0f);

The object comes in fast from the ![Rendered by QuickLaTeX.com -X](../../assets/bc53dc5a0893e950.png)

![Rendered by QuickLaTeX.com +X](../../assets/d93ba145fc5d93c3.png)


We can utilize this motion to create effects like these falling stars:

float tan = Mathf.Tan(Rate * Time.time); obj.transform.position = center + moveDirection * tan;

The acceleration and deceleration are kind of subtle. We can further amplify the effect by raising the tangent function to a power of, say, 3:

float tan = Mathf.Tan(Rate * Time.time); float tan3 = tan * tan * tan; obj.transform.position = center + moveDirection * tan3;

## Trigonometric Functions, Angles, And Triangles

So we’ve seen how the three basic trigonometric functions relate to the unit circle. Now we’re going to take a look at their relationships with triangles. They are called trigonometric functions, after all. Specifically, we’re going to look at **right triangles** (triangles with a right angle).

First, let’s get the terminologies out of the way. Here is a right triangle with an angle marked up as ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/6a395c84bdb60098.png)

The side of the triangle between ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

**adjacent side**, since it is adjacent to ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

**opposite side**, because it is across from ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

**hypotenuse**:

![](../../assets/e0fb30a9e568cf70.png)

And here is how the three basic trigonometric functions relate to **the lengths** of the triangle sides:


length of the **opposite side**divided by length of the**hypotenuse**.

length of the **adjacent side**divided by length of the**hypotenuse**.

length of the **opposite side**divided by length of the**adjacent side**.

Or, in mathematical form:

![Rendered by QuickLaTeX.com \begin{alignat*} \ \sin\theta &= \frac{opposite}{hypotenuse} \:\:\: \ \cos\theta &= \frac{adjacent}{hypotenuse} \:\:\: \ \tan\theta &= \frac{opposite}{adjacent} \end{alignat*}](../../assets/ab82570623242ea7.png)


These equations could be a bit too much to remember. Here’s a common verbal mnemonic that might help: **soh-cah-toa** (**s**ine is the **o**pposite side divided by the **h**ypotenuse, **c**osine is the **a**djacent side divided by the **h**ypotenuse, and **t**angent is the **o**pposite side divided by the **a**djacent side).

I did not learn this verbal mnemonic in Taiwan (my math classes were taught in Mandarin). What I learned was a visual mnemonic that I’m quite fond of: Write the **initials** of sine, cosine, and tangent in cursive, along with the right triangle as shown below (please forgive my ugly handwriting).

![](../../assets/9536ab2b1bb6bb0f.png)

When you write an initial, the corresponding function equals the length of the **first side you write past** dividing the length of the **second side you write past**:

![](../../assets/c0baca9152c6c30c.png)


length of the **hypotenuse**dividing length of the**opposite side**.

length of the **hypotenuse**dividing length of the**adjacent side**.

length of the **adjacent side**dividing length of the**opposite side**.

When describing fractions in Mandarin, instead of saying “A divided by B”, we say “B dividing A”. That’s why this mnemonic orders the divisor before the dividend in its wording. This ordering might not be intuitive to native English speakers, but if you find it useful, then great!

Now back to the equations:

![Rendered by QuickLaTeX.com \begin{alignat*} \ \sin\theta &= \frac{opposite}{hypotenuse} \:\:\: \ \cos\theta &= \frac{adjacent}{hypotenuse} \:\:\: \ \tan\theta &= \frac{opposite}{adjacent} \end{alignat*}](../../assets/ab82570623242ea7.png)


Whatever the size of the right triangle, the equations above always hold true, because ratios between two sides are independent of the absolute lengths of individual sides.

If we scale the triangle so that the hypotenuse is of length 1, then we can fit it back into our unit circle figure, with ![Rendered by QuickLaTeX.com (X, Y)](../../assets/20a6cdca242db178.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)


![](../../assets/0fc83ee3bd9f8322.png)

And the equations above agree nicely with the coordinates of ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com (X, Y) = (\cos\theta, \sin\theta)](../../assets/3eca1acc51d00e08.png)


![Rendered by QuickLaTeX.com \begin{alignat*} \ \sin\theta &= \frac{Y}{1} &&= Y \:\:\:\: \ \cos\theta &= \frac{X}{1} &&= X \:\:\:\: \ \tan\theta &= \frac{Y}{X} &&= \frac{\sin\theta}{\cos\theta} \end{alignat*}](../../assets/4f18870dc35df963.png)


Knowing the equations for trigonometric functions in terms of lengths of right triangle sides, for any given right triangle with an angle ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


Let ![Rendered by QuickLaTeX.com J](../../assets/401c663f919c1f99.png)

**j**acent side, ![Rendered by QuickLaTeX.com S](../../assets/fd14bbf347776f9d.png)

**s**ite side, and ![Rendered by QuickLaTeX.com H](../../assets/90b95e98f0a12951.png)

**h**ypotenuse:

![](../../assets/fd3315fdf8743788.png)

If we know the length of the hypotenuse (![Rendered by QuickLaTeX.com H](../../assets/90b95e98f0a12951.png)

![Rendered by QuickLaTeX.com J = H \cos\theta](../../assets/d60036c596c452d6.png)

![Rendered by QuickLaTeX.com S = H \sin\theta](../../assets/4553e9b8a754a1b3.png)


![](../../assets/f494989ca6bbf1bc.png)

If we know the length of the adjacent side (![Rendered by QuickLaTeX.com J](../../assets/401c663f919c1f99.png)

![Rendered by QuickLaTeX.com S = J \tan\theta](../../assets/312459264f26be6a.png)

![Rendered by QuickLaTeX.com H = \frac{J}{\cos\theta}](../../assets/a628140252396b9c.png)


![](../../assets/2b93873446a413fb.png)

If we know the length of the opposite side (![Rendered by QuickLaTeX.com S](../../assets/fd14bbf347776f9d.png)

![Rendered by QuickLaTeX.com J = \frac{S}{\tan\theta}](../../assets/3b533028aa8c84c9.png)

![Rendered by QuickLaTeX.com H = \frac{S}{\sin\theta}](../../assets/085940b003f781ca.png)


![](../../assets/f3d8f3af0f8bb980.png)

## Simulating Cannonballs & Predicting Trajectories

Finally, it’s time for practical examples! Let’s see how we can simulate cannonballs when given an initial speed, a horizontal angle, and an elevation angle. Also, let’s find out how we can display the predicted trajectories even before firing the cannon.

But before all that, here’s a very quick recap on some basic terminologies in motion dynamics. An object’s **position** is where the object is physically located. An object’s **velocity** is the rate of change in its position (typically expressed as change of position per second). An object’s **acceleration** is the rate of change in its velocity (typically expressed as change of velocity per second).

The [Euler Method](https://en.wikipedia.org/wiki/Euler_method) is a quick and easy algorithm for simulating object movement: For each moving object, we store its velocity vector along with its position. For each update, or **time step**, we change the velocity by acceleration times **delta time** (the time difference between each update), and then we change the position by velocity times delta time:

velocity += acceleration * deltaTime; position += velocity * deltaTime;

To simulate gravity at ground level and at human scale, we let the acceleration be a constant downward-pointing vector. Here’s an example of how an object would move in 2D under the influence of gravity when starting off with an initial velocity pointing up and to the right, simulated using the Euler Method:

If we simulate the entire trajectory within a single frame by performing multiple time steps, and draw a little dot once every several iterations, we can get ourselves a nice indicator of the predicted trajectory:

velocity = initialVelocity; position = initialPosition; for (int i = 0; i < NumIterations; ++i) { velocity += acceleration * deltaTime; position += velocity * deltaTime; if (i % IterationsPerDot != 0) continue; DrawDot(position); }

Now, let’s compute the **initial velocity** of a cannonball if it is fired from the cannon at an initial speed ![Rendered by QuickLaTeX.com K](../../assets/f6ac230548b6e4a9.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com \phi](../../assets/c5571bad897bf9dc.png)

![Rendered by QuickLaTeX.com +Z](../../assets/dd8570719a10e427.png)

![Rendered by QuickLaTeX.com +X](../../assets/d93ba145fc5d93c3.png)


![](../../assets/6b625b6f2e7bdbee.png)

To compute the initial velocity, we need to first compute a **unit vector** (vector of length 1) in the same direction. Once we have that unit vector, we can simply multiply all its components by a the desired speed ![Rendered by QuickLaTeX.com K](../../assets/f6ac230548b6e4a9.png)


The diagram below shows the a unit vector in the ![Rendered by QuickLaTeX.com +X](../../assets/d93ba145fc5d93c3.png)

![Rendered by QuickLaTeX.com +Y](../../assets/0977a46715c2053b.png)

![Rendered by QuickLaTeX.com +Z](../../assets/dd8570719a10e427.png)

![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com +Z](../../assets/dd8570719a10e427.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com \phi](../../assets/c5571bad897bf9dc.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)


![](../../assets/8d3c54da8ee7e179.png)

The goal is to find ![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)

![Rendered by QuickLaTeX.com K](../../assets/f6ac230548b6e4a9.png)


One is a horizontal unit circle diagram with ![Rendered by QuickLaTeX.com +X](../../assets/d93ba145fc5d93c3.png)

![Rendered by QuickLaTeX.com +Z](../../assets/dd8570719a10e427.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/c1862d1ce5111059.png)

And the other one is a vertical unit circle diagram with ![Rendered by QuickLaTeX.com +Y](../../assets/0977a46715c2053b.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)

![Rendered by QuickLaTeX.com \phi](../../assets/c5571bad897bf9dc.png)


![](../../assets/c9a67b3797d2608a.png)

If we view the first (horizontal) unit circle diagram from a different angle, we’ll get a familiar view of a flat unit circle:

![](../../assets/1e2ca3b02e5ba75f.png)

We’ve done this math before. The component of ![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com +Z](../../assets/dd8570719a10e427.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com +X](../../assets/d93ba145fc5d93c3.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com V_h = (\sin\theta, 0, \cos\theta)](../../assets/9f80d89f88a74aa9.png)


Now, view the second (vertical) unit circle diagram from a different angle that gives us the same familiar view of a flat unit circle:

![](../../assets/574a3d22084701be.png)

It’s the same drill. The component of ![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com \cos\phi](../../assets/3007bdb5ea502e67.png)

![Rendered by QuickLaTeX.com +Y](../../assets/0977a46715c2053b.png)

![Rendered by QuickLaTeX.com \sin\phi](../../assets/226fa89660a77033.png)

![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)


![Rendered by QuickLaTeX.com \begin{flalign*} V_i &= \cos\phi \cdot V_h + \sin\phi \cdot (0, 1, 0) \\ &= (\cos\phi \sin\theta, \: \sin\phi, \: \cos\phi \cos\theta) \end{flalign*}](../../assets/52b42f6459f9206d.png)


Multiplying ![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)

![Rendered by QuickLaTeX.com K](../../assets/f6ac230548b6e4a9.png)


![Rendered by QuickLaTeX.com \begin{flalign*} V_i &= K \cdot (\cos\phi \sin\theta, \: \sin\phi, \: \cos\phi \cos\theta) \\ &= (K \cos\phi \sin\theta, \: K \sin\phi, \: K \cos\phi \cos\theta) \end{flalign*}](../../assets/40089914cd52771f.png)


And the corresponding code is:

Vector3 ComputeInitialVelocity() { float sinTheta = Mathf.Sin(HorizontalAngle); float cosTheta = Mathf.Cos(HorizontalAngle); float sinPhi = Mathf.Sin(ElevationAngle); float cosPhi = Mathf.Cos(ElevationAngle); return InitialSpeed * new Vector3 ( cosPhi * sinTheta, sinPhi, cosPhi * cosTheta ); }

Being able to compute the initial velocity vector from a given initial speed, horizontal angle, and elevation angle, we are now well-equipped to simulate a cannonball:

void FireCannon() { velocity = ComputeInitialVelocity(); obj.transform.position = InitialPosition; } void Update() { float dt = Time.deltaTime; velocity += acceleration * dt; obj.transform.position += velocity * dt; } void DrawTrajectory() { float dt = Time.fixedDeltaTime; Vector3 velocity = ComputeInitialVelocity(); Vector3 position = InitialPosition; for (int i = 0; i < NumIterations; ++i) { velocity += acceleration * dt; position += velocity * dt; if (i % IterationsPerDot != 0) continue; DrawDot(position); }

## Placing Cannonball Targets

Now that we can fire cannonballs, let’s place some targets. If we want to place a target at a given horizontal distance away from the cannon, as well as at a given elevation angle, where exactly should we place the targets?

Below is the desired end result. Each target is at a fixed horizontal distance (on the XZ plane) away from the cannon, and is at a fixed elevation angle above ground. The targets are also equally spaced out horizontally, i.e. their horizontal angles relative to the cannon are equally spaced out.

![](../../assets/0a35f4faca7d397e.png)

We already know how to compute a horizontal unit vector from a horizontal angle ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com (\cos\theta, 0, \sin\theta)](../../assets/1c4c6f9824771a57.png)

![Rendered by QuickLaTeX.com D](../../assets/b45ae2142cb26a8a.png)

![Rendered by QuickLaTeX.com (D \cos\theta, 0, D \sin\theta)](../../assets/59c177e62ccfd565.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/7dd82b39b2e6635d.png)

The last step is to determine the Y coordinates of the targets, i.e. how far off ground the targets should be. Recall that if we know the length of the adjacent side to an angle ![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com J](../../assets/401c663f919c1f99.png)

![Rendered by QuickLaTeX.com J \tan\theta](../../assets/deae43e340e71a1f.png)


![](../../assets/2b93873446a413fb.png)

Substituting ![Rendered by QuickLaTeX.com J](../../assets/401c663f919c1f99.png)

![Rendered by QuickLaTeX.com D](../../assets/b45ae2142cb26a8a.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com \phi](../../assets/c5571bad897bf9dc.png)

![Rendered by QuickLaTeX.com D \tan\phi](../../assets/9fb6fedd4a39b66d.png)


![](../../assets/06dfbe7cab1a4e5a.png)

We can finally place our targets at the desired positions:

float theta = -0.5f * AngleInterval * (NumTargets - 1); float elevationTan = Mathf.Tan(ElevationAngle); foreach (var target in targetArray) { Vector3 horizontalVec = HorizontalDistance * new Vector3 ( Mathf.Sin(theta), 0.0f, Mathf.Cos(theta) ); theta += AngleInterval; Vector3 verticalVec = HorizontalDistance * elevationTan * Vector3.up; target.transform.position = Cannon.position + horizontalVec + verticalVec; }

![](../../assets/825f655807c2490f.png)

We haven’t talked about how to detect when a cannonball hits a target or the ground yet. Right now the cannonballs would just go through the targets:

Collision detection is beyond the scope of this tutorial, so I’ll just go over the very basics of sphere-sphere collision really quick.

To detect when a cannonball hits the target, check the distance between the centers of the two and see if it’s less than the sum of their radii. If the cannonball does collide with a target, we destroy the cannonball and the target.

Vector3 cannonballToTargetVec = target.transform.position - cannonball.transform.position; float cannonballToTargetDist = cannonballToTargetVec.magnitude; float radiusSum = cannonballRadius + targetRadius; if (cannonballToTargetDist < radiusSum) { DestroyCannonball(); DestroyTarget(); }

Using a similar technique when drawing the predicted trajectory, we can terminate the trajectory early when it hits a target.

However, this collision detection technique is **discrete**, meaning that the cannonball can still go through targets if it travels fast enough. We can mitigate this problem with a **continuous** collision detection technique, but that is also beyond the scope of this tutorial and will be touched on in later tutorials.

## Summary

Previously, we have been introduced to two basic trigonometric functions: sine and cosine. In this tutorial, we have seen a geometric interpretation of another trigonometric function: tangent. We have also learned the relationship among sine, cosine, and tangent, in the context of the unit circle, as well as right triangles.

Next, we have plotted the tangent function alongside sine and cosine; and we are now able to create smooth into and outro motion by utilizing the tangent function.

Finally, using the three basic trigonometric functions, we have learned how to predict and simulate the trajectory of a cannonball, given an initial speed and elevation angle. Plus, we have seen how to place targets, given a horizontal distance and an elevation angle.

We have learned the basics of the three fundamental trigonometric functions that are essential in solving daily gamedev problems. In later tutorials, I will go over more useful mathematical tools that are built on top of these trigonometric functions, as well as some of their practical applications.

If you enjoyed this tutorial and would like to see more, please consider supporting me on [Patreon](https://www.patreon.com/TheAllenChou). By doing so, you can also get updates on future tutorials. Thanks!