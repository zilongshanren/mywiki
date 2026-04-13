---
title: Inverse Kinematics in 3D - Alan Zucconi
url: https://www.alanzucconi.com/2020/09/14/inverse-kinematics-in-3d/
author: Alan Zucconi
published: '2020-09-14'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will teach you how to master inverse kinematics in 3D: the technique that solves the problem of moving a robotic arm to reach for a specific target.

You can read the rest of this online course here:

![](../../assets/adc188efbc4350bf.gif)

A link to download the entire Unity package can be found at the end of this tutorial.

## Introduction

There are a few topics that keep recurring on this blog: one of them is, without any doubt, **inverse kinematics**. I have tackled this fascinating problem in two series so far, for a total of 8 separate articles. And yet, there is still so much more to write about inverse kinematics in the context of video games.

What makes inverse kinematics so interesting and complex to require this many posts? The truth is that inverse kinematics is a problem that recurs not only in video games, but in both engineering and science in general. From the design of **robotic arms** to the understanding of **motor control** in the human brain, inverse kinematics—in one form or another—plays an important role.

### A Brief Summary

The first series dedicated to the topic, [An Introduction to Procedural Animations](https://www.alanzucconi.com/?p=6131), came out in 2017 and further popularized the term “**procedural animations**” among indie developers. It provided a general solution based on a **gradient descent algorithm**, which could potentially be used on rather “exotic” riggings, such as tentacles and spider legs.

The second series, [Inverse Kinematics in 2D](https://www.alanzucconi.com/?p=8368), came out one year later and focused on a very specific case: a two-joint arm constrained in a 2D plane (below). Exactly as the name suggested: inverse kinematics in 2D. Each one of the two joints is controlled by an angle, ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

**end effector**, will reach different locations.

![](../../assets/4bb40a4a7d3b823e.png)

The problem of inverse kinematics is to find the angles ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)


![](../../assets/b832f213d64e2f2b.gif)

Technically speaking, the solution presented on [Inverse Kinematics for Robotic Arms](https://www.alanzucconi.com/?p=6135) can work with potentially *any* number of joints. So why focusing on a less powerful technique? The answer is simple: efficiency. What made this worth writing about was the fact that, in the specific scenario just described, a solution can be found using a simple equation instead of a rather complex algorithm. That is thanks to the fact that we can imagine the robotic arm as a triangle (below) with two internal angles ![Rendered by QuickLaTeX.com \alpha](../../assets/2f6dd9acb6fbfd6a.png)

![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)


![](../../assets/ddfd2bbdaac6da0f.png)

With a little bit of trigonometry, we found out the values for such angles to be:

(1) ![Rendered by QuickLaTeX.com \begin{equation*} \alpha = \cos^{-1}{\left(\frac{b^2+c^2-a^2}{2bc}\right)}\end{equation*}](../../assets/8893f5f688a8064e.png)


(2) ![Rendered by QuickLaTeX.com \begin{equation*} \beta=\cos^{-1}{\left(\frac{a^2 + c^2 -b^2}{2ac}\right)}\end{equation*}](../../assets/270f887de80bd790.png)


where ![Rendered by QuickLaTeX.com a](../../assets/2f5fc5259ecc795a.png)

![Rendered by QuickLaTeX.com b](../../assets/0bcd696a7c0431b0.png)

![Rendered by QuickLaTeX.com c](../../assets/ce510e21eb93eebe.png)


However, the joints of the robotic arm are controlled using ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)


(3) ![Rendered by QuickLaTeX.com \begin{equation*} A = \alpha + A'\end{equation*}](../../assets/2256374fe7e35b9c.png)


(4) ![Rendered by QuickLaTeX.com \begin{equation*} B = \pi - \beta\end{equation*}](../../assets/4663cc1dac805052.png)


where:

(5) ![Rendered by QuickLaTeX.com \begin{equation*} A' = \tan^{-1}{\left(\frac{C_Y-A_Y}{C_X-A_X}\right)}\end{equation*}](../../assets/b811b989c51270eb.png)


## Extending into the Third Dimension

If you have followed the [Inverse Kinematics in 2D](https://www.alanzucconi.com/?p=8368) series before, there should not be anything new in the previous section. If you have not, do not worry: that is all you need to know.

What makes that simplified case worth discussing, is that it can be used as the starting point for solving inverse kinematics in 3D.

First of all, we need to understand that the scenario of a two-joint arm in 2D is a problem with **two degrees of freedom** (2DOF). Conversely to what one might imagine, it does not mean that we have *two segments*; but that we have control over *two variables* (which, in this case, turns out of to be the joint angles).

When we extend this problem to the third dimension, our robotic arm still has two segments and two joints. However, the problem has now **three degrees of freedom** (3DOF), if we assume that we can also rotate the arm freely around its first joint.

Under this new scenario, the second joint (![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

**hip**, and the second as the **knee**. Your knee has generally only one degree of freedom (forwards/backwards), while your hip has two (forwards/backwards and inwards/outwards). The angle around which the hips rotates is indicated with ![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)


We can imagine a robotic arm in which both joints can have two degrees of freedom, for a total of four. The problem at that point is that there will be multiple solutions, making our approach not effective anymore. “Leg-like” robotic arms (meaning: arms that have a hip and a knee joints) are very common both in games and in the industry in general. So this approach is probably worth studying.

If you have read the previous articles, you might remember that if the target is reachable in 2D, there are always two “specular” solutions (below).

![](../../assets/d0f9bf4bb1f5bb97.png)

The same problem occurs in 3D; this time, the solutions are infinite. This is because the configuration can rotate around the axis of symmetry represented by the straight line that connects the origin from the target. The solution is to… focus on just one solution! In this tutorial, we will focus on the most simple to find, which assumes (0, 1, 0) as the “up” direction.

### From 2D to 3D

So far, we only know how to solve the problem of inverse kinematics when the movement is constraints to the XY plane. The trick to go from 2D to 3D is to re-use the 2D solution. The animation below shows a robotic arm reaching for a point in 3D space, which revolves around the Y-axis. It is pretty obvious to see that the only thing the arm does is to revolve as well; its angles ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)


![](../../assets/8fec8bf394d98544.gif)

This means that, if we know how to perform IK on the XY plane (and we do!) we know how to perform it on the entire XYZ space with two simple rotations. Conceptually, we can solve the problem in three steps:

- Rotate the target point around the Y-axis, until it lies on the XY plane
- Move the robotic arms so that it can reach for the point, as if it was in 2D
- “Undo” the rotation by rotating the entire robotic arm in the opposite direction on the Y-axis.

We can do this more efficiently by simply performing the 2D inverse kinematics not on the XY plane, but on the vertical plane passing from the root of the robotic arm to the target point.

## Rotation Around Y-Axis

To perform inverse kinematics in 3D, the first thing that we need to calculate is ![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)


![](../../assets/cb2b2362b200a212.png)

The best way to find it, is to assume that the robotic arm has already reached the position (meaning that ![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)


If we look at the segment ![Rendered by QuickLaTeX.com \overline{AC}](../../assets/69f71321c9e91bc2.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)


(6) ![Rendered by QuickLaTeX.com \begin{equation*} \theta = \tan^{-1}{\left(\frac{\Delta z}{\Delta x}\right)}= \tan^{-1}{\left(\frac{C_Z-C_Z}{C_X-A_X}\right)}\end{equation*}](../../assets/6a1a90b80f92fa9e.png)


### ⭐ Recommended Unity Assets

## Inverse Kinematics on the WY Plane

Technically speaking, knowing ![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

![Rendered by QuickLaTeX.com -\theta](../../assets/02ea7b02e2a19f1b.png)

![Rendered by QuickLaTeX.com +\theta](../../assets/567090fc8f47eca8.png)


A quicker version is to perform the inverse kinematics not on the 2D plane, but directly on the vertical plane passing through the hip joint and the target point. There is, unfortunately, something that is preventing us from doing so. Let’s look once again at the diagram which indicates all of the angles used:

![](../../assets/ddfd2bbdaac6da0f.png)

In order to calculate ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com A'](../../assets/cf585d59f274a571.png)

[5](https://www.alanzucconi.com#id1456798080)) used to calculate ![Rendered by QuickLaTeX.com A'](../../assets/cf585d59f274a571.png)


![Rendered by QuickLaTeX.com \begin{equation*}A' = \tan^{-1}{\left(\frac{C_Y-A_Y}{C_X-A_X}\right)}\end{equation}](../../assets/ee028e0da7199de1.png)


In our 3D scenario, unfortunately the robotic arm would be rotated by ![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)

![Rendered by QuickLaTeX.com \theta](../../assets/b55496429621e4ab.png)


![](../../assets/8832a7c264a91c9c.png)

We cannot simply do ![Rendered by QuickLaTeX.com D_X-A_X](../../assets/e902fc63e7801b5c.png)

![Rendered by QuickLaTeX.com \Delta y](../../assets/25291a4f11405370.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com D](../../assets/81012a1469029eac.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com D](../../assets/81012a1469029eac.png)

![Rendered by QuickLaTeX.com \Delta w](../../assets/939ed8332921a0bc.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com D](../../assets/81012a1469029eac.png)

![Rendered by QuickLaTeX.com \Delta w](../../assets/939ed8332921a0bc.png)

![Rendered by QuickLaTeX.com \Delta w](../../assets/939ed8332921a0bc.png)


(9) ![Rendered by QuickLaTeX.com \begin{equation*} A' = \tan^{-1}{\left(\frac{\Delta y}{\Delta w}\right)}=\tan^{-1}{\left(\frac{C_Y-D_Y}{\left|\overline{A D}\right|}\right)}\end{equation*}](../../assets/0a66e9ba5f4a8d74.png)


where ![Rendered by QuickLaTeX.com \left|\overline{A D}\right|](../../assets/0344cb11ba2b1470.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com D](../../assets/81012a1469029eac.png)

`Vector3.Distance`

, or you could also use Pythagoras’ theorem directly:

(10) ![Rendered by QuickLaTeX.com \begin{equation*}\begin{align}A' &=& \tan^{-1}{\left(\frac{C_Y-D_Y}{\sqrt{\left(C_X - A_X\right)^2+\left(A_Y- A_Y\right)^2+\left(C_Z - A_Z\right)^2}}\right)}= \\&=& \tan^{-1}{\left(\frac{C_Y-D_Y}{\sqrt{\left(C_X - A_X\right)^2+\left(C_Z - A_Z\right)^2}}\right)}\end{align}\end{equation*}](../../assets/27a034d3adc991d3.png)


In the equation above, the Y contribution from the Pythagoras’ theorem cancels itself out because the point ![Rendered by QuickLaTeX.com D](../../assets/81012a1469029eac.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com \Delta y](../../assets/25291a4f11405370.png)


![](../../assets/bf3e9a2fd7c10dbe.gif)

Now, we really do have everything to perform inverse kinematics in 3D for robotic arms with one keen and hip joint:

(11) ![Rendered by QuickLaTeX.com \begin{equation*} \theta = \tan^{-1}{\left(\frac{C_Z-C_Z}{C_X-A_X}\right)}\end{equation*}](../../assets/ae516f931ce22280.png)


(12) ![Rendered by QuickLaTeX.com \begin{equation*} A = \cos^{-1}{\left(\frac{b^2+c^2-a^2}{2bc}\right)} +\tan^{-1}{\left(\frac{C_Y-D_Y}{\sqrt{\left(C_X - A_X\right)^2+\left(C_Z - A_Z\right)^2}}\right)}\end{equation*}](../../assets/0a502b8665674aec.png)


(13) ![Rendered by QuickLaTeX.com \begin{equation*} B &=& \pi - \cos^{-1}{\left(\frac{a^2 + c^2 -b^2}{2ac}\right)}\end{equation*}](../../assets/2ce124f3cd173de1.png)


While looking scary, these equations are simple to implement and allows to perform inverse kinematics in 3D as fast as possible.

## What’s Next…

The next tutorial in this series will show how to use inverse kinematics to create believable legged creatures. Yes, the anticipated tutorial about inverse kinematics for spider legs is finally coming!!!

![](../../assets/5e4c4c9dfbaa45b6.gif)

## Unity Package Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the assets used in this tutorial to have a fully functional robotic arm for Unity.

Feature |
Standard |
|---|


**Premium****Feature****Standard**
## Leave a Reply Cancel reply