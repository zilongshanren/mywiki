---
title: Implementing Forward Kinematics - Alan Zucconi
url: https://www.alanzucconi.com/2017/04/06/implementing-forward-kinematics/
author: Alan Zucconi
published: '2017-04-06'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial continues our quest to solve the problem of **forward kinematics**. After exploring a mathematical solution in [The Mathematics of Forward Kinematics](https://www.alanzucconi.com/?p=6142), we will see how to translate it into C# for Unity. The next tutorial, [An Introduction to Gradient Descent](https://www.alanzucconi.com/?p=6133), will finally show the theoretical foundations to solve **inverse kinematics**.

![](../../assets/ef6b390d1b154e7a.gif)

The other post in this series can be found here:

- Part 1.
[An Introduction to Procedural Animations](https://www.alanzucconi.com/?p=6131) - Part 2.
[The Mathematics of Forward Kinematics](https://www.alanzucconi.com/?p=6142) - Part 3.
**Implementing Forward Kinematics** - Part 4.
[An Introduction to Gradient Descent](https://www.alanzucconi.com/?p=6133) - Part 5.
[Inverse Kinematics for Robotic Arms](https://www.alanzucconi.com/?p=6135) - Part 6.
[Inverse Kinematics for Tentacles](https://www.alanzucconi.com/?p=6180) - Part 7. Inverse Kinematics for Spider Legs 🚧 (work in progress!)

At the end of this post you can find a link to download all the assets and scenes necessary to replicate this tutorial.

#### Introduction

In the second part of this tutorial on Inverse Kinematics, [The Mathematics of Forward Kinematics](https://www.alanzucconi.com/?p=6142), we have formalised how a robotic arm moves. We started with a toy example, made by three joints. When in their resting positions, they assume the configuration seen in the diagram below:

![](../../assets/57a0e5bb3afd2a0e.png)

In the diagram, the various ![Rendered by QuickLaTeX.com P_i](../../assets/b4a50ebd874809dc.png)

![Rendered by QuickLaTeX.com i](../../assets/9079b2bc6b821844.png)

*local angles* that indicates how much they rotate from their resting positions are labelled ![Rendered by QuickLaTeX.com \alpha_i](../../assets/e78226c943b43d37.png)


When joints rotate, we see the following:

![](../../assets/8aa79900a30b7404.png)

The behaviour of this system has been summarised with the following statements:

**Rotation.**The*global rotation*

of a joint is the sum of the rotations of all the previous joints:![Rendered by QuickLaTeX.com \[r_i = \sum_{k=0}^{i} {\alpha_k}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8adbf58ca07877653971e03e75433ff0_l3.png)

**Position.**The*global position*

of a joint is given by:![Rendered by QuickLaTeX.com \[P_{i} = P_{i-1} + rotate\left(D_i, P_{i-1}, \sum_{k=0}^{i-1}\alpha_k\right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-7aa6ae4e17c0600f1f9f53ff2e6b3a5a_l3.png)


Knowing all of the above, we can start thinking of a possible way to implement these behaviours in Unity.

#### GameObjects Hierarchy

Unity already comes with a way to implement all the requirements mentioned above: **parenting**. Setting a game object as a child of another one automatically inherit the position, the rotation and the scale.

![](../../assets/c49a90215f3bba7a.gif)

If you are familiar with rigging, this should not surprise you. The bones that represent the joints of a humanoid character are parented in such a way that rotations and translations are inherited. The following image, from [Unity Animation 3: Character Setup](https://michaelarbuthnot.wordpress.com/2015/07/23/tutorial-unity-animation-3-character-setup/) (by Michael Arbuthnot) shows a clear example of this.

![](../../assets/31e5c712a333866e.jpg)

While building your hierarchy of joints, you have to make sure that the robotic arm is in resting position when all the local Euler angles are set to zero. In a humanoid character, this usually corresponds to the **standard T-stance **seen in the picture above.

#### The Implementation

The parenting option in Unity is, *de-facto*, solving the problem of forward kinematics for us. Unfortunately this is not enough. We will see in next part of this tutorial, [Inverse Kinematics with Gradient Descent](https://www.alanzucconi.com/?p=6133)**,** that we actually need a way to test the position of the end effector *without* actually moving the robotic arm. This forces us to re-implement this basic feature in Unity.

The first step is to store some information on each joint of the robotic arm. This can be done by adding a script, such as `RobotJoint`

in the example below.

using UnityEngine; public class RobotJoint : MonoBehaviour { public Vector3 Axis; public Vector3 StartOffset; void Awake () { StartOffset = transform.localPosition; } }

You should add `RobotJoint`

script to each game object that serves as a joint for your robotic arm. Every game object that you want to be rotated by the IK system should have one such script attached to it.

To simplify the calculations, we assume that each joint can only rotate around one its local axes: either X, Y or Z. We indicate that with a variable called `Axis`

, which has a `1`

in the position relative to the rotation axis. If this joint rotates around the Y axis, `Axis`

would be `(0,1,0)`

. We will see how this allows us to avoid IF statements.

The actual IK code should be store in a different script, which will serve as an “IK manager”. You can put it inside the root of your robot arm, although it does not really matter where it is. Its purpose will be to perform both the forward and inverse kinematics. To do so, the manager script needs to know where the joints are. This will be possible by storing them inside an array or a list of `RobotJoint`

s, which will be called `Joints`

.

The manager script will need a function, called `ForwardKinematics`

. It takes as input an array of `float`

s, called `angles`

. The name is self-explanatory: `angles[i]`

contains the local rotation for the i-th joint contains in the `Joints`

list. The function returns the position of the end effector, in global coordinates.

public Vector3 ForwardKinematics (float [] angles) { ... }

The code is a straight forward implementation in C# of the position equation seen before. The `rotate`

function is implemented with the handy `Quaternion.AngleAxis`

.

Vector3 prevPoint = Joints[0].transform.position; Quaternion rotation = Quaternion.identity; for (int i = 1; i < Joints.Length; i++) { // Rotates around a new axis rotation *= Quaternion.AngleAxis(angles[i - 1], Joints[i - 1].Axis); Vector3 nextPoint = prevPoint + rotation * Joints[i].StartOffset; prevPoint = nextPoint; } return prevPoint;

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

Credits for the 3D model of the robotic arm goes to [Petr P](https://3dwarehouse.sketchup.com/model/92e064854f4dd504c8ab9067fbd9681d/Robotic-Arm-stainless-steel-R6Stainless). A big thanks also goes to [Maurizio Scuiar](https://www.linkedin.com/in/maurizio-scuiar-7b336315/).

## Leave a Reply Cancel reply