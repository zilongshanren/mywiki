---
title: Inverse Kinematics for Robotic Arms - Alan Zucconi
url: https://www.alanzucconi.com/2017/04/10/robotic-arms/
author: Alan Zucconi
published: '2017-04-10'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

After a long journey about the Mathematics of Forward Kinematics and the geometrical details of gradient descent, we are ready to finally show a working implementation for the problem of inverse kinematics. This tutorial will show how it can be applied to a robotic arm, like the one in the image below.

![](../../assets/ef6b390d1b154e7a.gif)

The other post in this series can be found here:

- Part 1.
[An Introduction to Procedural Animations](https://www.alanzucconi.com/?p=6131) - Part 2.
[The Mathematics of Forward Kinematics](https://www.alanzucconi.com/?p=6142) - Part 3.
[Implementing Forward Kinematics](https://www.alanzucconi.com/?p=6170) - Part 4.
[An Introduction to Gradient Descent](https://www.alanzucconi.com/?p=6133) - Part 5.
**Inverse Kinematics for Robotic Arms** - Part 6.
[Inverse Kinematics for Tentacles](https://www.alanzucconi.com/?p=6180) - Part 7. Inverse Kinematics for Spider Legs 🚧 (work in progress!)

At the end of this post you can find a link to download all the assets and scenes necessary to replicate this tutorial.

#### Introduction

The previous tutorial, [An Introduction to Gradient Descent](https://www.alanzucconi.com/?p=6133), laid the mathematical foundations for a technique called **gradient descent**. What we have is a function, ![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)

![Rendered by QuickLaTeX.com \alpha_i](../../assets/e78226c943b43d37.png)

![Rendered by QuickLaTeX.com \alpha](../../assets/2f6dd9acb6fbfd6a.png)

![Rendered by QuickLaTeX.com f\left(\alpha\right)](../../assets/e5943b1b25f43e50.png)

![Rendered by QuickLaTeX.com T](../../assets/26eae1ea411a75f4.png)

![Rendered by QuickLaTeX.com \alpha](../../assets/2f6dd9acb6fbfd6a.png)

![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)


To do so, we first calculate the gradient of a function for the current ![Rendered by QuickLaTeX.com \alpha](../../assets/2f6dd9acb6fbfd6a.png)

**gradient** is a vector that indicates the direction of the steepest ascent. To put it simple, it’s an arrow that tells us the direction in which the function grows. Each element of our gradient is an estimation of the partial derivative of ![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)


For example, if our robotic arm has three joints, we will have a function ![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)

![Rendered by QuickLaTeX.com \alpha_0](../../assets/a35fe3cb2cdcbd02.png)

![Rendered by QuickLaTeX.com \alpha_1](../../assets/9c2cdbb5ae129bc1.png)

![Rendered by QuickLaTeX.com \alpha_2](../../assets/f94ec483f75712fc.png)

![Rendered by QuickLaTeX.com \nabla f](../../assets/a2ff892af9a5431e.png)


![Rendered by QuickLaTeX.com \[\nabla f \left(\alpha_0, \alpha_1, \alpha_2\right) = \left[\nabla {f}_{\alpha_0}\left(\alpha_0, \alpha_1, \alpha_2\right),\nabla{f}_{\alpha_1}\left(\alpha_0, \alpha_1, \alpha_2\right) ,\nabla{f}_{\alpha_2}\left(\alpha_0, \alpha_1, \alpha_2\right)\right]\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-59f3a5003dd0bde7b78ac4406e5d22d5_l3.png)


where:

![Rendered by QuickLaTeX.com \[\nabla {f}_{\alpha_0}\left(\alpha_0, \alpha_1, \alpha_2\right) \right )=\frac{f\left(\alpha_0 + \Delta_x, \alpha_1, \alpha_2\right)-f\left(\alpha_0, \alpha_1, \alpha_2\right)}{\Delta x}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-4626e93b73f6506ffc2dacc563cc508b_l3.png)


![Rendered by QuickLaTeX.com \[\nabla {f}_{\alpha_1}\left(\alpha_0, \alpha_1, \alpha_2\right) \right )=\frac{f\left(\alpha_0, \alpha_1+\Delta_y, \alpha_2\right)-f\left(\alpha_0, \alpha_1, \alpha_2\right)}{\Delta y}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-775b18ab9c3ecee9216ee4eb75113387_l3.png)


![Rendered by QuickLaTeX.com \[\nabla {f}_{\alpha_2}\left(\alpha_0, \alpha_1, \alpha_2\right) \right )= \frac{f\left(\alpha_0, \alpha_1, \alpha_2+\Delta_z\right)-f\left(\alpha_0, \alpha_1, \alpha_2\right)}{\Delta z}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-b86e067592a813fa0df382d57ca29b6d_l3.png)


and ![Rendered by QuickLaTeX.com \Delta x](../../assets/c3f96fe7e6c6e55a.png)

![Rendered by QuickLaTeX.com \Delta y](../../assets/25291a4f11405370.png)

![Rendered by QuickLaTeX.com \Delta z](../../assets/31e2a484f86356da.png)


Once we have our estimated gradient ![Rendered by QuickLaTeX.com \nabla f](../../assets/a2ff892af9a5431e.png)

![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)

![Rendered by QuickLaTeX.com \alpha_0](../../assets/a35fe3cb2cdcbd02.png)

![Rendered by QuickLaTeX.com \alpha_1](../../assets/9c2cdbb5ae129bc1.png)

![Rendered by QuickLaTeX.com \alpha_2](../../assets/f94ec483f75712fc.png)


![Rendered by QuickLaTeX.com \[\alpha_0 \leftarrow \alpha_0 - L \nabla {f} _{\alpha_0}\left(\alpha_0, \alpha_1, \alpha_2\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-67c7bd4f44e593f10c6418b737ba13a5_l3.png)


![Rendered by QuickLaTeX.com \[\alpha_1 \leftarrow \alpha_1 - L \nabla{f} _{\alpha_1}\left(\alpha_0, \alpha_1, \alpha_2\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-40601e66c2f53fa81eaa807584952f99_l3.png)


![Rendered by QuickLaTeX.com \[\alpha_2 \leftarrow \alpha_2 - L \nabla{f} _{\alpha_2}\left(\alpha_0, \alpha_1, \alpha_2\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-aaf493ff6b2e30a383a569d40572a713_l3.png)


where ![Rendered by QuickLaTeX.com L](../../assets/6046f3c7b4bcbd21.png)

**learning rate**, a positive parameter that controls how fast we move away from the ascending gradient.

#### Implementation

We have now all the knowledge necessary to implement a simple gradient descent in C#. Let’s start with a function that estimates the partial gradient ![Rendered by QuickLaTeX.com \nabla f_{\alpha_i}](../../assets/ec72ca8b844ab312.png)

`i`

th joints. As discussed, what we have to do is to sample function ![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)

`DistanceFromTarget`

defined in [An Introduction to Gradient Descent](https://www.alanzucconi.com/?p=6133)) at two different points:

public float PartialGradient (Vector3 target, float[] angles, int i) { // Saves the angle, // it will be restored later float angle = angles[i]; // Gradient : [F(x+SamplingDistance) - F(x)] / h float f_x = DistanceFromTarget(target, angles); angles[i] += SamplingDistance; float f_x_plus_d = DistanceFromTarget(target, angles); float gradient = (f_x_plus_d - f_x) / SamplingDistance; // Restores angles[i] = angle; return gradient; }

When invoked, this function returns a single number that indicates how the distance from our target changes as a function of the joint rotation.

What we have to do is to loop over all the joints, calculating its contribution to the gradient.

public void InverseKinematics (Vector3 target, float [] angles) { for (int i = 0; i < Joints.Length; i ++) { // Gradient descent // Update : Solution -= LearningRate * Gradient float gradient = PartialGradient(target, angles, i); angles[i] -= LearningRate * gradient; } }

Invoking `InverseKinematics`

repeatedly move the robotic arm closer to the target point.

#### Early Termination

One of the main problems of inverse kinematics made with such a naive implementation of gradient descent is that it is unlikely to converge. Depending on the values you have chosen for `LearningRate`

and `SamplingDistance`

, it is likely your robotic arm will “wiggle” around the actual solution.

![](../../assets/1ed179de529d529a.gif)

This happens because we update our angles too much, causing the robotic arm to overshoot the actual point. A proper solution to this problem would be to use an adaptive learning rate, which changes depending on how close we are to the solution. A cheaper alternative is to stop the optimisation algorithm if we are closer to a certain threshold:

public void InverseKinematics (Vector3 target, float [] angles) { if (DistanceFromTarget(target, angles) < DistanceThreshold) return; for (int i = Joints.Length -1; i >= 0; i --) { // Gradient descent // Update : Solution -= LearningRate * Gradient float gradient = PartialGradient(target, angles, i); angles[i] -= LearningRate * gradient; // Early termination if (DistanceFromTarget(target, angles) < DistanceThreshold) return; } }

If we repeat this check after each joint rotation, we ensure that we perform the minimum amount of movements required.

To further improve the performance of our arm, we can apply gradient descent in reverse order. Starting from the end of the arm, instead of its base, allows us to make the smaller movements. Overall, these little tricks allow to converge to a more *natural* solution.

#### Constraints

One of the features of real joints is that they tend to have a range of angles they can cover. Not all joints can fully rotate 360 degrees around their axes. Currently, we have put no restrictions on our optimisation algorithm. This means that we are likely to obtain behaviours like this one:

![](../../assets/6e6b93206e881ef6.gif)

The solution is rather straightforward. We can add minimum and maximum angles in the `RobotJoint`

class:

using UnityEngine; public class RobotJoint : MonoBehaviour { public Vector3 Axis; public Vector3 StartOffset; public float MinAngle; public float MaxAngle; void Awake () { StartOffset = transform.localPosition; } }

then, making sure that we clamp the angles in the proper range:

public void InverseKinematics (Vector3 target, float [] angles) { if (DistanceFromTarget(target, angles) < DistanceThreshold) return; for (int i = Joints.Length -1; i >= 0; i --) { // Gradient descent // Update : Solution -= LearningRate * Gradient float gradient = PartialGradient(target, angles, i); angles[i] -= LearningRate * gradient; // Clamp angles[i] = Mathf.Clamp(angles[i], Joints[i].MinAngle, Joints[i].MaxAngle); // Early termination if (DistanceFromTarget(target, angles) < DistanceThreshold) return; } }

#### Issues

Even with angle constraints and early termination, the algorithm that we have used is very simple. Too simple. There are many issue that you might encounter with this solution, most of them related with gradient descent. As described in [An Introduction to Gradient Descent](https://www.alanzucconi.com/?p=6133), the algorithm can get stuck in **local minima**. They represent *suboptimal solutions*: ways to approach the target that are unnatural or undesirable.

Look at the following animation:

![](../../assets/41e7c424e50deae4.gif)

The robotic arm has gone too far, and now that has returned back to its original position, is twisted. A better approach to avoid this is to add a **comfort function**. If we have reached destination, we should try to re-orient the robotic arm to a more comfortable, natural position. It should be noted that this might not always be possible. Re-orient a robotic arm might force the algorithm to increase the distance from the target, which might be against the specification.

#### Other resources

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