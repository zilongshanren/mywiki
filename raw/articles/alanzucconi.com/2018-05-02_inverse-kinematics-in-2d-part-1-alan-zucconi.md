---
title: Inverse Kinematics in 2D - Part 1 - Alan Zucconi
url: https://www.alanzucconi.com/2018/05/02/ik-2d-1/
author: Alan Zucconi
published: '2018-05-02'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

If you have been following this blog for a while, you might have noticed some recurring themes. **Inverse Kinematics** is definitely one them, and I have dedicated an entire series on how to apply it to [robotic arms](https://www.alanzucconi.com/?p=6135) and [tentacles](https://www.alanzucconi.com/?p=6180). If you have not read them, do not fear: this new series will be self-contained, as it reviews the problem of Inverse Kinematics from a new perspective.

![](../../assets/1e5fa555092670f4.gif)

You can read the rest of this online course here:

A follow-up that focuses on 3D is also available:

- Part 3.
[Inverse Kinematics in 3D](https://www.alanzucconi.com/?p=12166)

#### Introduction

We are so used to interact with the world around us that is easy to underestimate how complex moving our hands and arms really is. In the academic literature, the task of controlling a robotic arm is known as inverse kinematics. *Kinematics* stands for *movements*, and *inverse* refers to the fact that we don’t usually control the arm itself. What we control are the motors that rotate each individual joint. Inverse kinematics is the task of deciding how to drive these motors to move the arm to a certain point of position. And in its general form, it is an exceptionally challenging task. To give a feeling for *how* challenging it is, you can think about games such as [QWOP](https://www.youtube.com/watch?v=HBFYJvq_o_4), [GIRP](http://www.foddy.net/GIRP.html) or even [Lunar Lander](https://en.wikipedia.org/wiki/Lunar_Lander_(video_game_genre)), where you do not decide *where* to go, but *which* muscles (or thrusters) to activate.

The task of controlling moving actuators predates even the field of robotics. It should not come as a surprise that, throughout the centuries, mathematicians and engineers have been developing countless solutions. Most 3D modelling softwares and game engines (including Unity) come with a set of tools that allow the rigging of human-like and dog-like creatures. For all different setups (such as robotic arms, tails, tentacles, wings, …) no built-in solution is usually offered.

![](../../assets/ef6b390d1b154e7a.gif)

This is why in the previous series on [Procedural Animations and Inverse Kinematics](https://www.alanzucconi.com/?p=6131), I have introduced a very general and effective solution that works on potentially *any* setup. But such a power comes at a cost: efficiency. One of the main criticism that the series has received is that it was too time-consuming and expensive to be used on hundreds of characters at the same time. This is why I have decided to start a new series that is specifically focused on Inverse Kinematics for arms with two degrees of freedom. The technique you will discover in this tutorial is exceptionally efficient and can truly be run on dozens (if not hundreds!) of characters at the same time.

#### Inverse Kinematics

Let’s imagine a robotic arm with two segments and two joints, like the one seen in the diagram below. At the end of the arm, there is the **end effector** that we want to control. We do not have direct control on the position of the end effector; we can only rotate the joints. The problem of inverse kinematics is to find the best way to rotate the joints to move the end effector to the desired position.

![](../../assets/4bb40a4a7d3b823e.png)

The solution that is proposing in this new series will only work on robotic arms with two joints. In the academic literature is often said that these robotic arms have **two degrees of freedom**. The reason for this will be very clear by looking at the diagram below. A robotic arm with two degrees of freedom can be modelled as a triangle, which is one of the most studied geometrical figures in geometry.

![](../../assets/e19b98b63f65af55.png)

Let’s start by formalising the problem a little bit more. The two joints, ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)


#### Internal Angles

We can use the three points ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com C](../../assets/3a238a676a4030d3.png)

![Rendered by QuickLaTeX.com \alpha](../../assets/2f6dd9acb6fbfd6a.png)

![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

![Rendered by QuickLaTeX.com \gamma](../../assets/3a86849de177f9bb.png)


![](../../assets/a5bdeae4013197f3.png)

While these three angles are unknown, we know the length of all edges.

- The segment

represents the **arm**and has length

; - The segment

represents the **forearm**and has length

; - The segment

represents the distance between the **shoulder joint**and the hand, and has length

.

Knowing the three sides of a triangle is enough to find all of its angles. This is possible thanks to the **law of cosines**, a generalisation of Pythagora’s theorem for triangles that are not necessarily at right angles.

The two angles that are needed to control the robotic arm are ![Rendered by QuickLaTeX.com \alpha](../../assets/2f6dd9acb6fbfd6a.png)

![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

![Rendered by QuickLaTeX.com \alpha](../../assets/2f6dd9acb6fbfd6a.png)

![Rendered by QuickLaTeX.com \alpha](../../assets/2f6dd9acb6fbfd6a.png)


(1) ![Rendered by QuickLaTeX.com \begin{equation*} a^2 = b^2 + c^2 - 2 bc \cos{\alpha} \end{equation*}](../../assets/f96e90711f46ba1f.png)


We can refector ([1](https://www.alanzucconi.com#id2559766926)) to extract ![Rendered by QuickLaTeX.com \cos\alpha](../../assets/bb33590c3828e212.png)


![Rendered by QuickLaTeX.com \[ \begin{split} \cos{\alpha} & =\frac{a^2-b^2-c^2}{-2bc} = \\ & =\boxed{\frac{b^2+c^2-a^2}{2bc}} \end{split} \]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-67807e40b367dee25ccf4347b9450bdd_l3.png)


What is now needed is to use the inverse cosine function ![Rendered by QuickLaTeX.com \cos^{-1}](../../assets/29337d3c244aab87.png)

**arcosine**) to find the ![Rendered by QuickLaTeX.com \alpha](../../assets/2f6dd9acb6fbfd6a.png)


(2) ![Rendered by QuickLaTeX.com \begin{equation*} \alpha = \cos^{-1}{\left(\boxed{\frac{b^2+c^2-a^2}{2bc}}\right)} \end{equation*}](../../assets/8764d9e1c3ef5b78.png)


With the same procedure, we can apply the law of cosine once again to find ![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)


![Rendered by QuickLaTeX.com \[b^2 = a^2 + c^2 - 2ac \cos{\beta}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-2eaf92ed4e4609c122fb29644f32721e_l3.png)


![Rendered by QuickLaTeX.com \[\cos{\beta}=\frac{a^2 + c^2 -b^2}{2ac}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-0a347b2694deacd8027582849e059034_l3.png)


(3) ![Rendered by QuickLaTeX.com \begin{equation*} \beta=\cos^{-1}{\left(\frac{a^2 + c^2 -b^2}{2ac}\right)} \end{equation*}](../../assets/884a6144351f22a7.png)


#### Joint Angles

Using the law of cosines we have calculated the values for ![Rendered by QuickLaTeX.com \alpha](../../assets/2f6dd9acb6fbfd6a.png)

![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)



![](../../assets/ddfd2bbdaac6da0f.png)

Let’s start by calculating ![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com \beta](../../assets/df9863c7aea130fd.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)

![Rendered by QuickLaTeX.com 180^{\circ}](../../assets/f555d372e2c265dd.png)

![Rendered by QuickLaTeX.com \pi](../../assets/f1a7a5860bb46ab3.png)


(11) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{split} \beta + B = \pi \\ B = \pi - \beta \end{split} \end{equation*}](../../assets/688e80380d852bcf.png)


Calculating ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com A'](../../assets/cf585d59f274a571.png)

![Rendered by QuickLaTeX.com \overline{AC}](../../assets/69f71321c9e91bc2.png)

**arcotangent** function ![Rendered by QuickLaTeX.com \tan^{-1}](../../assets/3084efdbda8b95ba.png)


(12) ![Rendered by QuickLaTeX.com \begin{equation*} A' = \tan^{-1}{\left(\frac{C_Y-A_Y}{C_X-A_X}\right)} \end{equation*}](../../assets/3c64d9cc79639d8a.png)


Which leads to:

(13) ![Rendered by QuickLaTeX.com \begin{equation*} A = \alpha + A' \end{equation*}](../../assets/e1c5a02853592958.png)


The sign of the angles ![Rendered by QuickLaTeX.com A](../../assets/c9cad4bbd3de006d.png)

![Rendered by QuickLaTeX.com A'](../../assets/cf585d59f274a571.png)

![Rendered by QuickLaTeX.com B](../../assets/83a66c67694b2bb9.png)


### ⭐ Recommended Unity Assets

#### What’s Next…

This post concludes the introduction on the Mathematics of Inverse Kinematics for robotic arms with two degrees of freedom.

The next post will explore how we can use the equations derived to efficiently move a robotic arm in Unity.

You can read the rest of this online course here:

A follow-up that focuses on 3D is also available:

- Part 3.
[Inverse Kinematics in 3D](https://www.alanzucconi.com/?p=12166)

The line art animals that have been featured in this tutorial have been inspired by the work of [WithOneLine](https://www.etsy.com/uk/shop/WithOneLine).

#### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the assets used in this tutorial to have a fully functional robotic arm for Unity.

Feature |
Standard |
|---|


**Premium****Download**[Standard](https://www.patreon.com/posts/18553107)[Premium](https://www.patreon.com/posts/18553038)![](../../assets/ea9ed8330e6cc351.gif)

## Leave a Reply Cancel reply