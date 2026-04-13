---
title: The Mathematics of Forward Kinematics - Alan Zucconi
url: https://www.alanzucconi.com/2017/04/06/forward-kinematics/
author: Alan Zucconi
published: '2017-04-06'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial starts our journey into the world of **inverse kinematics**. There are countless ways to approach this problem, but they all starts with **forward kinematics**.

Inverse kinematics takes a point in space, and tells you how to move your arm to reach it. Forward kinematics solves the opposite, *dual* problem. Knowing how you are moving your arm, it tells which point in space it reaches.

![](../../assets/ef6b390d1b154e7a.gif)

The other post in this series can be found here:

- Part 1.
[An Introduction to Procedural Animations](https://www.alanzucconi.com/?p=6131) - Part 2.
**The Mathematics of Forward Kinematics** - Part 3.
[Implementing Forward Kinematics](https://www.alanzucconi.com/?p=6170) - Part 4.
[An Introduction to Gradient Descent](https://www.alanzucconi.com/?p=6133) - Part 5.
[Inverse Kinematics for Robotic Arms](https://www.alanzucconi.com/?p=6135) - Part 6.
[Inverse Kinematics for Tentacles](https://www.alanzucconi.com/?p=6180) - Part 7. Inverse Kinematics for Spider Legs 🚧 (work in progress!)

At the end of this post you can find a link to download all the assets and scenes necessary to replicate this tutorial.

#### Robotic Arm

Inverse kinematics has been originally applied to control **robotic arms**. For this reason, this tutorial will make assumptions and use terminology related to robotics. This, however, does not limit the possible applications of inverse kinematics. Non-robotic scenarios, such as human arms, spider spiders and tentacles, are still possible.

First of all, let’s start showing what we mean with the term “robotic arm”:

![](../../assets/ae90f9ec286ba654.png)

The picture above shows a typical robotic arm, made of “limbs” connected by “joints”. Since the robotic arm from the picture has five independent joints, it is said to have five **degrees of freedom**. Each joint is controller by a motor, which allows to moves the connected link to a certain angle.

Without losing generalisation, we can draw a precise schematics of the joints. In this particular tutorial, we will assume that each joint can only rotate on a single axis.

![](../../assets/d7d1e8ddea763363.png)

The tool attached at the end of the robotic arm is known as **end effector**. Depending on the context, it can be counted or not as a degree of freedom. In this tutorial, the end effector will not be considered since we will focus solely on the reaching movement.

#### Forward Kinematics

In this toy example, each joint is able to rotate on a specific axis. The state of each joint is hence measured as an angle. By rotating each joint to a specific angle, we cause the end effector to reach different points in space. Knowing where the end effector is, given the angles of the joints, is known as **forward kinematics**.

The forward kinematics is an “easy” problem. This means that for each set of angles, there is one and only one result, which can be calculated with no ambiguity. Understanding how a robotic arm moves depending on the inputs we provide to its motors is an essential step to find a solution to its dual problem of inverse kinematics.

#### Geometrical Interpretation

Before writing even a single line of code, we need to understand the Mathematics behind forward kinematics. And even before that, we need to understand what that means spatially and geometrically.

Since visualising rotations in 3D is not that easy, let’s start with a simple robotic arm that lies in a 2D space. A robotic arm has a “resting position”; that is the configuration when all the joints are rotated back to their “zero angle”.

![](../../assets/57a0e5bb3afd2a0e.png)

The diagram above shows a robotic arm with three degrees of freedom. Each joint is rotated to its zero angle, resulting in this initial configuration. We can see how such configuration changes by rotating the first joint at ![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

![Rendered by QuickLaTeX.com \alpha_0](../../assets/a35fe3cb2cdcbd02.png)

![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)


![](../../assets/a84ecce7d7944bbf.png)

It is important to notice that the motors attached to other joints have not moved. Each joint contributes to the local rotation of its forward chain of links. The following diagram shows how the configuration changes when the second joint rotates by ![Rendered by QuickLaTeX.com \alpha_1](../../assets/9c2cdbb5ae129bc1.png)


![](../../assets/8aa79900a30b7404.png)

While only ![Rendered by QuickLaTeX.com \alpha_0](../../assets/a35fe3cb2cdcbd02.png)

![Rendered by QuickLaTeX.com P_1](../../assets/ac81ff325fec7791.png)

![Rendered by QuickLaTeX.com P_2](../../assets/2e2bcf5cc12d64bd.png)

![Rendered by QuickLaTeX.com \alpha_0](../../assets/a35fe3cb2cdcbd02.png)

![Rendered by QuickLaTeX.com \alpha_1](../../assets/9c2cdbb5ae129bc1.png)


#### The Maths

From the previous diagrams it should be clear to solve the problem of forward kinematics, we need to be able to calculate the position of nested objects due to their rotation.

Let’s see how this is calculated with just two joints. Once solved for two, we can just replicate it in sequence to solve chains of any length.

Let’s start with the easy case, the one in which the first joint is in its starting position. This means that ![Rendered by QuickLaTeX.com \alpha_0=0](../../assets/b36b41030bd0abfb.png)


![](../../assets/cd60d45cddc81e41.png)

This means that, simply:

![Rendered by QuickLaTeX.com \[P_1 = P_0 + D_1\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c889c96e2dc93395f220405926d5903f_l3.png)


When ![Rendered by QuickLaTeX.com \alpha_0](../../assets/a35fe3cb2cdcbd02.png)

![Rendered by QuickLaTeX.com D_1](../../assets/e8b40fcdaa8059ef.png)

![Rendered by QuickLaTeX.com P_0](../../assets/e51c31256f08ccef.png)

![Rendered by QuickLaTeX.com \alpha_0](../../assets/a35fe3cb2cdcbd02.png)


![](../../assets/9270e24b5d7199b1.png)

Mathematically we can write this as:

![Rendered by QuickLaTeX.com \[P_1 = P_0 + rotate\left(D_1, P_0, \alpha_0\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f96e356f85df7fc94f6e3ca1136867fc_l3.png)


We will see later how we can use the function `AngleAxis`

([Unity Documentation](https://docs.unity3d.com/ScriptReference/Quaternion.AngleAxis.html)), without messing up with trigonometry.

By replicating the same logic, we can derive the equation for ![Rendered by QuickLaTeX.com P_2](../../assets/2e2bcf5cc12d64bd.png)


![Rendered by QuickLaTeX.com \[P_2 = P_1 + rotate\left(D_2, P_1, \alpha_0 + \alpha_1\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0653ac1911d9ff07943698f03312fc49_l3.png)


And finally, the general equation:

![Rendered by QuickLaTeX.com \[P_{i} = P_{i-1} + rotate\left(D_i, P_{i-1}, \sum_{k=0}^{i-1}\alpha_k\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7aa6ae4e17c0600f1f9f53ff2e6b3a5a_l3.png)


We will see in the next part of this tutorial, [Implementing Forward Kinematics](https://www.alanzucconi.com/?p=6170), how that equation will translated *nicely* to C# code.

### 📚 Recommended Books

#### Other Resources

- Part 1.
[An Introduction to Procedural Animations](https://www.alanzucconi.com/?p=6131) - Part 2.
[The Mathematics of Forward Kinematics](https://www.alanzucconi.com/?p=6142) - Part 3.
[Implementing Forward Kinematics](https://www.alanzucconi.com/?p=6170) - Part 4.
[An Introduction to Gradient Descent](https://www.alanzucconi.com/?p=6133) - Part 5.
[Inverse Kinematics for Robotic Arms](https://www.alanzucconi.com/?p=6135) - Part 6.
[Inverse Kinematics for Tentacles](https://www.alanzucconi.com/?p=6180) - Part 7. Inverse Kinematics for Spider Legs 🚧 (work in progress!)

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download the Unity project for this tutorial on [Patreon](https://www.patreon.com/posts/8928832).

Credits for the 3D model of the robotic arm goes to [Petr P](https://3dwarehouse.sketchup.com/model/92e064854f4dd504c8ab9067fbd9681d/Robotic-Arm-stainless-steel-R6Stainless).

## Leave a Reply Cancel reply