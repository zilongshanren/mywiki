---
title: An Introduction to Gradient Descent - Alan Zucconi
url: https://www.alanzucconi.com/2017/04/10/gradient-descent/
author: Alan Zucconi
published: '2017-04-10'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post concludes the theoretical introduction to **Inverse Kinematics**, providing a programmatical solution based on **gradient descent**. This article does not aim to be a comprehensive guide on the topic, but a gentle introduction. The next post, [Inverse Kinematics for Robotic Arms](https://www.alanzucconi.com/?p=6135), will show an actual C# implementation of this algorithm in with Unity.

![](../../assets/ef6b390d1b154e7a.gif)

The other post in this series can be found here:DistanceFromTarget

- Part 1.
[An Introduction to Procedural Animations](https://www.alanzucconi.com/?p=6131) - Part 2.
[The Mathematics of Forward Kinematics](https://www.alanzucconi.com/?p=6142) - Part 3.
[Implementing Forward Kinematics](https://www.alanzucconi.com/?p=6170) - Part 4.
**An Introduction to Gradient Descent** - Part 5.
[Inverse Kinematics for Robotic Arms](https://www.alanzucconi.com/?p=6135) - Part 6.
[Inverse Kinematics for Tentacles](https://www.alanzucconi.com/?p=6180) - Part 7. Inverse Kinematics for Spider Legs 🚧 (work in progress!)

At the end of this post you can find a link to download all the assets and scenes necessary to replicate this tutorial.

#### Introduction

The previous post in this series, [Implementing Forward Kinematics](https://www.alanzucconi.com/?p=6170), provided a solution to the problem of **Forward Kinematics**. We have left with a function, called `ForwardKinematics`

, which indicates which point in space our robotic arm is currently touching.

If we have a specific point in space that we want to reach, we can use `ForwardKinematics`

to estimate how close we are, given the current joint configuration. The distance from the target is a function that can be implemented like this:

public float DistanceFromTarget(Vector3 target, float [] angles) { Vector3 point = ForwardKinematics (angles); return Vector3.Distance(point, target); }

Finding a solution for the problem of Inverse Kinematics means that we want to minimise the value returned from `DistanceFromTarget`

. Minimising a function is one of most common problems, both in programming and Mathematics. The approach we will use relies on a technique called **gradient descent **([Wikipedia](https://en.wikipedia.org/wiki/Gradient_descent)). Despite not being the most efficient, it has the advantage of being *problem-agnostic* and requires knowledge that most programmers already have.

#### Gradient Descent

The easiest way to understand how gradient descent works, is to imagine a hilly landscape. We find ourselves on a random location, and we want to reach its lowest point. We call that the **minimum** of the landscape. At each step, gradient descent tells you to move in the direction that lowers your altitude. If the geometry of the landscape is relatively *simple*, this approach will converge towards the bottom of the valley.

The diagram below shows a typical scenario in which gradient descent is successful. In this toy example, we have a function that takes a single parameter (X axis), and returns an error value (Y axis). Starting from random points on the X axis (blue and green points), gradient descent should force us to move in the direction of the minimum (blue and green arrows).

![](../../assets/5ddba4a9fa208ce4.png)

Looking at the function in its entirety, the direction in which we have to move is obvious. Unfortunately, gradient descent has no prior knowledge of where the minimum is. The best guess the algorithm can do is to move in the direction that of the slope, also called the **gradient** of the function. If you are on a hill, let a ball go and follow it to reach the valley. The diagram below shows the gradient of the error function at two different points.

![](../../assets/f4bb7ec1d6a8e055.png)

#### Gradient Estimation

If you have studied Calculus before, you might know the **gradient** of a function is deeply connected to its **derivative**. Calculating the derivative, however, requires the function to satisfy certain mathematical properties that, in general, cannot be guaranteed for arbitrary problems. Moreover, the analytical derivation of the derivative needs the error function to be presented analytically. Once again, you do not always have access to an analytical version of the function you are trying to minimise.

In all those cases, it is impossible to access the *true* derivative of the function. The solution is to give a rough estimate of its value. The diagram below shows how this can be done in one dimension. By sampling nearby points, you can get a feeling for the local gradient of the function. If the error function is smaller on the left, you go on the left. Likewise, if it is smaller on the right, you go on the right.

![](../../assets/fdf572581ed9e522.png)

This **sampling distance** will be called ![Rendered by QuickLaTeX.com \Delta x](../../assets/c3f96fe7e6c6e55a.png)


#### The Maths

Now that we have a general understanding of how gradient descent works graphically, let’s see how this translates mathematically. The first step is to calculate the gradient of our error function ![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)

![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)


Mathematically speaking, the derivative of ![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)

![Rendered by QuickLaTeX.com {f}'](../../assets/f00075d20c85bda8.png)

![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

![Rendered by QuickLaTeX.com {f}'\left(p\right)](../../assets/adc0b5feb2abe7ae.png)



is going up, locally;

is going down, locally;

is flat, locally.

The idea is to use an estimation of ![Rendered by QuickLaTeX.com {f}'\left(p\right)](../../assets/adc0b5feb2abe7ae.png)

![Rendered by QuickLaTeX.com \nabla f](../../assets/a2ff892af9a5431e.png)

![Rendered by QuickLaTeX.com {f}'](../../assets/f00075d20c85bda8.png)


![Rendered by QuickLaTeX.com \[{f}'\left(p\right) \right ) = \lim_{\Delta x \rightarrow 0} \frac{f\left(p+\Delta x\right) - f\left(p\right)}{\Delta x}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e3b6d9c52dd0a28f06a481e0ca770ecd_l3.png)


The following diagram shows what this means:

![](../../assets/618edbee571a1b6b.gif)

For what we are concerned, to estimate the derivative we need to sample the error function at two different points. The small distance between them, ![Rendered by QuickLaTeX.com \Delta x](../../assets/c3f96fe7e6c6e55a.png)

**sampling distance** that we have introduced in the previous section.

To recap. The actual derivative of a function requires the usage of a limit. Our gradient is an estimation of the derivative, made using a sufficiently small sampling distance:

**Derivative**![Rendered by QuickLaTeX.com \[{f}'\left(p\right) \right ) = \lim_{\Delta x \rightarrow 0} \frac{f\left(p+\Delta x\right) - f\left(p\right)}{\Delta x}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e3b6d9c52dd0a28f06a481e0ca770ecd_l3.png)

**Estimated gradient**![Rendered by QuickLaTeX.com \[\nabla{f}\left(p\right) \right ) = \frac{f\left(p+\Delta x\right) - f\left(p\right)}{\Delta x}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-3e79ff44f4778d2284eeb96651712f4d_l3.png)


We will see in the next section how these two differ for functions with multiple variables.

Once we have found our estimated derivative, we need to move in its opposite direction to climb down the function. This means that we have to update our parameter ![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)


![Rendered by QuickLaTeX.com \[p_{i+1} = p_{i} - L \nabla {f}\left(p_i\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-4e671f2ddfcd5b5f561ea33e300d7e7b_l3.png)


The constant ![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

**learning rate**, and it dictates how fast we move against the gradient. Larger values approach the solution faster, but are also more likely to overshoot it.

#### Multiple Variables

The solution we have found so far works on a single dimension. What it means is that we have given the definition of the derivative for a function of the type ![Rendered by QuickLaTeX.com f\left(p\right)](../../assets/ad03f669d0053725.png)

![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)

![Rendered by QuickLaTeX.com p](../../assets/fd0a1880d4f5faaf.png)

![Rendered by QuickLaTeX.com p+\Delta x](../../assets/6ef6be1d7c954133.png)


A function with a single parameter corresponds to robot arm with a single joint. If we want to perform gradient descent for more complex robotic arms, we need to define the gradient for functions on multiple variables. If our robotic arm has three joints, for instance, our function will look more like ![Rendered by QuickLaTeX.com f\left(\alpha_0, \alpha_1, \alpha_2\right)](../../assets/8cedba01cf195d5f.png)

![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)


We can introduce the concept of **partial derivatives**, which essentially are “traditional” derivatives, calculated on a single variable at a time:

![Rendered by QuickLaTeX.com \[{f}'_{\alpha_0}\left(\alpha_0, \alpha_1, \alpha_2\right) \right )=\lim_{\Delta x \rightarrow 0} \frac{f\left(\alpha_0 + \Delta_x, \alpha_1, \alpha_2\right)-f\left(\alpha_0, \alpha_1, \alpha_2\right)}{\Delta x}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e95b8a4b5582f2bb8469608423c1e5cb_l3.png)


![Rendered by QuickLaTeX.com \[{f}'_{\alpha_1}\left(\alpha_0, \alpha_1, \alpha_2\right) \right )=\lim_{\Delta y \rightarrow 0} \frac{f\left(\alpha_0, \alpha_1+\Delta_y, \alpha_2\right)-f\left(\alpha_0, \alpha_1, \alpha_2\right)}{\Delta y}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-425c67fea0833b03934dd69bf95cbd61_l3.png)


![Rendered by QuickLaTeX.com \[{f}'_{\alpha_2}\left(\alpha_0, \alpha_1, \alpha_2\right) \right )=\lim_{\Delta z \rightarrow 0} \frac{f\left(\alpha_0, \alpha_1, \alpha_2+\Delta_z\right)-f\left(\alpha_0, \alpha_1, \alpha_2\right)}{\Delta z}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-5481078734133a5ee42c7a6609931bca_l3.png)


They represent three different scalar numbers, each indicating how the function grows on a specific direction (or axes). To calculate our total gradient, we approximate each partial derivative with a correspondent gradient, using sufficiently small sampling distances ![Rendered by QuickLaTeX.com \Delta x](../../assets/c3f96fe7e6c6e55a.png)

![Rendered by QuickLaTeX.com \Delta y](../../assets/25291a4f11405370.png)

![Rendered by QuickLaTeX.com \Delta z](../../assets/31e2a484f86356da.png)


![Rendered by QuickLaTeX.com \[\nabla {f}_{\alpha_0}\left(\alpha_0, \alpha_1, \alpha_2\right) \right )=\frac{f\left(\alpha_0 + \Delta_x, \alpha_1, \alpha_2\right)-f\left(\alpha_0, \alpha_1, \alpha_2\right)}{\Delta x}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-4626e93b73f6506ffc2dacc563cc508b_l3.png)


![Rendered by QuickLaTeX.com \[\nabla {f}_{\alpha_1}\left(\alpha_0, \alpha_1, \alpha_2\right) \right )=\frac{f\left(\alpha_0, \alpha_1+\Delta_y, \alpha_2\right)-f\left(\alpha_0, \alpha_1, \alpha_2\right)}{\Delta y}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-775b18ab9c3ecee9216ee4eb75113387_l3.png)


![Rendered by QuickLaTeX.com \[\nabla {f}_{\alpha_2}\left(\alpha_0, \alpha_1, \alpha_2\right) \right )= \frac{f\left(\alpha_0, \alpha_1, \alpha_2+\Delta_z\right)-f\left(\alpha_0, \alpha_1, \alpha_2\right)}{\Delta z}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b86e067592a813fa0df382d57ca29b6d_l3.png)


For our gradient descent, we will use the vector that incorporates those three results as the gradient:

![Rendered by QuickLaTeX.com \[\nabla f \left(\alpha_0, \alpha_1, \alpha_2\right) = \left[\nabla {f}_{\alpha_0}\left(\alpha_0, \alpha_1, \alpha_2\right),\nabla{f}_{\alpha_1}\left(\alpha_0, \alpha_1, \alpha_2\right) ,\nabla{f}_{\alpha_2}\left(\alpha_0, \alpha_1, \alpha_2\right)\right]\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-59f3a5003dd0bde7b78ac4406e5d22d5_l3.png)


### 📚 Recommended Books

#### Other resources

The next part of this tutorial will finally show a working implementation of this algorithm.

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