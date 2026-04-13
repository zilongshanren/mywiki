---
title: 'Game Physics: Motion Dynamics Fundamentals | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2013/12/game-physics-motion-dynamics-fundamentals/
author: Allen Chou
published: '2013-12-19'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

Before delving deep into the programming aspect of physics engines, I would like to first go over the fundamentals of motion dynamics. Unless specified otherwise, all discussion is in 3D. Also, when it comes to formula consisting of vectors and matrices, all vectors are considered to be column vectors.


### Position & Orientation

Position and orientation of a rigid body are both positional properties. Position is a linear property that defines where the object is located in space, and orientation is an angular property that defines how the object is oriented.

Position is typically represented as a vector, and orientation in 3D can be represented by a 3D vector (the direction is the rotation axis, and the magnitude is the rotation angle), a 3-by-3 matrix (basis vectors as columns), or a [quaternion](http://en.wikipedia.org/wiki/Quaternion).

I prefer storing a 3-by-3 orientation matrix and, in addition, its inverse. These two matrices are used to transform vectors between world space (global coordinates) and model space (rigid body’s local coordinates), an operation that would be carried out quite frequently within a single time step.

### Linear Velocity & Angular Velocity

Linear velocity, denoted ![Rendered by QuickLaTeX.com v(t)](../../assets/ce2a3e67e6df23df.png)

![Rendered by QuickLaTeX.com x(t)](../../assets/79ede47a51122770.png)

[Euler Method](http://en.wikipedia.org/wiki/Euler_method), the formula is as follows:

![Rendered by QuickLaTeX.com \[ x(t + \Delta t) = x(t) + v(t) \Delta t \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-a5c390d4dcddfa4c4525700f279a675a_l3.png)


Angular velocity, denoted ![Rendered by QuickLaTeX.com \omega (t)](../../assets/4d79200017508703.png)

![Rendered by QuickLaTeX.com o(t)](../../assets/87e2475345e5c52b.png)


![Rendered by QuickLaTeX.com \[ o(t + \Delta t) = o(t) + \omega (t) \Delta t \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-b04f89e9dceb01349db3252a065cf79c_l3.png)


However, this gets trickier in 3D. In 3D, angular velocity is typically represented as a 3D vector, where its direction is the axis of rotation, and its magnitude is the rotation angle. True, if the representation of choice for orientation is also a 3D vector, then the formula for change of orientation would be the same as the 2D case (as shown above). However, if the orientation is represented as a 3-by-3 matrix, then computing the change of orientation involves first converting the angular velocity vector into a rotation matrix and then prepend that matrix to the orientation matrix.

![Rendered by QuickLaTeX.com \[ o(t + \Delta t) = R(\hat{\omega} (t), |\omega(t)| \, \Delta t) \,\, o(t), \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-e4c8bc6d949edf68e2201c6dfc339273_l3.png)


where ![Rendered by QuickLaTeX.com \hat{\omega}(t)](../../assets/1ade74ea31383be1.png)

![Rendered by QuickLaTeX.com \omega (t)](../../assets/4d79200017508703.png)

![Rendered by QuickLaTeX.com |\omega (t)|](../../assets/ecdb6ef03361add3.png)

![Rendered by QuickLaTeX.com \omega (t)](../../assets/4d79200017508703.png)

![Rendered by QuickLaTeX.com R(\hat{n}, \theta)](../../assets/47cac017bd1b153b.png)

[angle-axis rotation matrix](http://en.wikipedia.org/wiki/Rotation_matrix#Axis_and_angle) with axis ![Rendered by QuickLaTeX.com \hat{n}](../../assets/4886076b0ee0fb7f.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


### Force & Torque

When you apply a force, denoted ![Rendered by QuickLaTeX.com F(t)](../../assets/e337674ea977aacd.png)


Each force application corresponds to a resulting torque, denoted ![Rendered by QuickLaTeX.com \tau (t)](../../assets/0a18cd1e6c576477.png)

![Rendered by QuickLaTeX.com r(t)](../../assets/1214603af4afb13d.png)


![Rendered by QuickLaTeX.com \[ \tau (t) = r(t) \times F(t) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-f136e73ac74e2cb70eb3a037777bb6f3_l3.png)


### Mass & Moment of Inertia

Mass, denoted ![Rendered by QuickLaTeX.com m](../../assets/53d492fff6de1c67.png)


Moment of inertia is the angular counterpart of mass that defines how difficult it is to rotate an object along a certain axis. With different rotation axis of choice, the moment of inertia might be different. To fully describe the moment of inertia of an object with respect to any arbitrary axis, we usually use a 3-by-3 matrix called “inertia tensor”, denoted ![Rendered by QuickLaTeX.com I](../../assets/98cca4d8316e15f2.png)

![Rendered by QuickLaTeX.com \hat{n}](../../assets/4886076b0ee0fb7f.png)


![Rendered by QuickLaTeX.com \[ I_{\hat{n}} = \hat{n}^T \, I \, \hat{n}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-f3e9b19fb5e9463676273ed07546984f_l3.png)


where ![Rendered by QuickLaTeX.com \hat{n}^T](../../assets/163104724d4803df.png)

![Rendered by QuickLaTeX.com \hat{n}](../../assets/4886076b0ee0fb7f.png)

[ here](http://en.wikipedia.org/wiki/List_of_moment_of_inertia_tensors).

For other shapes, the inertia tensor can be calculated using the formula below:

![Rendered by QuickLaTeX.com \[ I = \int _{V} {\left[ {\begin{array}{ccc} y^2 + z^2 & -xy & -xz \\ -xy & x^2 + z^2 & -yz \\ -xz & -yz & x^2 + y^2 \\ \end{array} } \right]} \rho \, \mathrm{d}V, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-4e33a97f2bd408c76e0de2c1a08598c5_l3.png)


where ![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

![Rendered by QuickLaTeX.com \mathrm{d}V](../../assets/c356d7ee96bd97b6.png)

![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

![Rendered by QuickLaTeX.com (x, y, z)](../../assets/d07300f37c3ec746.png)

![Rendered by QuickLaTeX.com \rho](../../assets/c5de483310004f54.png)

![Rendered by QuickLaTeX.com \mathrm{d}V](../../assets/c356d7ee96bd97b6.png)

![Rendered by QuickLaTeX.com (x, y, z)](../../assets/d07300f37c3ec746.png)


### Linear Momentum & Angular Momentum

Linear momentum, denoted ![Rendered by QuickLaTeX.com P(t)](../../assets/99383f0b10844798.png)


![Rendered by QuickLaTeX.com \[ P(t) = m \, v(t) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-cff42c026dc6b847779eb4426694eec4_l3.png)


Angular momentum, denoted ![Rendered by QuickLaTeX.com L(t)](../../assets/aea3810b78a29ad5.png)


![Rendered by QuickLaTeX.com \[ L(t) = I \, \omega(t), \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-3341f38af87189baf31cf0860a254c5b_l3.png)


### Linear Impulse & Angular Impulse

The integrals of force and torque over time are respectively defined as linear impulse, denoted ![Rendered by QuickLaTeX.com \Delta P](../../assets/ca80952da1d62afb.png)

![Rendered by QuickLaTeX.com \Delta L](../../assets/b8c45947a7b185b1.png)


![Rendered by QuickLaTeX.com \[ \Delta P = F(t) \Delta t \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-fa29e15661d09af24d05339be3477951_l3.png)


![Rendered by QuickLaTeX.com \[ \Delta L = \tau (t) \Delta t \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-e27673ef7acac7a7331d7349e41d8f9a_l3.png)


Applying linear impulse and angular impulse would change the velocity and angular velocity, respectively.

The change of linear velocity due to a linear impulse is the linear impulse divided by mass or, in other words, product between inverse mass and linear impulse.

![Rendered by QuickLaTeX.com \[ \Delta v = m^{-1} \Delta P \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5cd437720c5e30d175f2c25bc5e52b88_l3.png)


The change of angular velocity due to an angular impulse is the product between the inverse of inertia tensor and angular impulse. Note that we have to convert the angular impulse to the object’s model space and then convert the change of angular velocity back to world space, since the inertia tensor is computed in the object’s model space.

![Rendered by QuickLaTeX.com \[ \Delta \omega = Q I^{-1} Q^T \Delta L, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-31928387a2bac3c82da0d3c846aa151c_l3.png)


where ![Rendered by QuickLaTeX.com Q](../../assets/8a1341208f50fa66.png)

![Rendered by QuickLaTeX.com Q](../../assets/8a1341208f50fa66.png)

![Rendered by QuickLaTeX.com Q^{-1}](../../assets/e95a67807200b7a1.png)

![Rendered by QuickLaTeX.com Q^T](../../assets/d83bf0a694dcf081.png)


### End of Motion Dynamics Fundamentals

That’s it. I have covered the aspects of motion dynamics you’ll need for building a physics engine. I strongly encourage you to get very familiar with these definitions and relationships between properties, so familiar that they become your second instinct. After all, you probably don’t want to be bothered by these fundamentals when you really want to focus on the physics engine.

You use basis vector once but don’t define what a basis vector is.

In the context of orientation, the 3 basis vectors of an oriented object in 3D are the object’s X, Y, and Z axes in world space.