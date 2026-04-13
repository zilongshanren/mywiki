---
title: 'Game Physics: Collision Detection – CSO & Support Function | Ming-Lun "Allen"
  Chou | 周明倫'
url: https://allenchou.net/2013/12/game-physics-collision-detection-csos-support-functions/
author: Allen Chou
published: '2013-12-26'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

Configuration Space Object (CSO), a.k.a. Minkowski Difference or Minkowski Configuration Object, is a very important concept for collision detection. In addition to CSO, support function is an equally important mathematical concept & tool. Many algorithms related to collision detection, including the Gilbert-Johnson-Keerthi (GJK) algorithm, Expanding Polytop Algorithm (EPA), and Minkowski Portal Refinement (MPR) algorithm, heavily depend on the concept of CSO and the use of support functions.

### Configuration Space Object

As complicated as its name sounds, it is actually a very simple concept. Let’s first look at a mathematical operation called the [Minkowski Sum](http://en.wikipedia.org/wiki/Minkowski_addition).

Let ![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com A \oplus B](../../assets/ca4ea37435820fee.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)


![Rendered by QuickLaTeX.com \[ A \oplus B = \{ P_A + P_B \, | \, P_A \in A, P_B \in B \} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-42481ad16a3b19f24643e057cf4434f6_l3.png)


Let’s look at something more visual. The Minkowski Sum of a circle and a rectangle is a rounded rectangle.

![Minkowski Sum Circle Rect](../../assets/f4c7bdc2006e367c.png)



If we reflect ![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)


![Rendered by QuickLaTeX.com \[ -B = \{ -P_B \, | \, P_B \in B \} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-254fb2e28f90ba34915ede8bc6be82c9_l3.png)


We call the Minkowski Sum of ![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com -B](../../assets/1aca1bcc65384505.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com A \ominus B](../../assets/436a20d1afe505ae.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)


![Rendered by QuickLaTeX.com \[ A \ominus B = \{ P_A - P_B \, | \, P_A \in A, P_B \in B \} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7ba60fd2ff0b8f0d84e976d77c43a007_l3.png)


One important property of CSO is that **if the CSO of two shapes contains the origin, the two shapes are colliding**. You can verify this from the figure above: the circle and rectangle are colliding, and thus their CSO contains the origin.

This property is actually very easy to prove. If two shapes are colliding, it means that there are common points that are in both shapes. Remember that the CSO of two shapes are a collection of “point differences” of points from both shapes. As we construct the CSO point-by-point, if we choose the common points that are in both shapes, then we would end up with a “zero” point, which is exactly the origin. Thus the origin is within the CSO if the two shapes are colliding.

All collision detection algorithms are essentially determining if the CSO of two shapes contains the origin.

Another important property of CSO is that if the CSO contains the origin, then the distance between the origin and the closest point on the CSO’s boundary to the origin is the __penetration depth__ of the two colliding shapes. And if the CSO does not contain the origin (thus the two shapes are not colliding), the distance between the origin and the closest point on the CSO’s boundary to the origin is the __closest distance__ between the two shapes.

### Support Function

In order to efficiently determine if the CSO of two shapes contain the origin, many collision detection algorithms make use of a mathematical tool called the support function, a.k.a support mapping. A support function takes a direction and shape as input and returns a point as output. The output point is the furthest point inside the shape along the given direction. Note that there can be multiple points that are valid support function outputs for a particular shape. For instance, the support function of an AABB, given the positive x-axis direction, can return any point on the AABB’s face in the positive x-axis direction.

![Rendered by QuickLaTeX.com \[ Support(\overrightarrow{v}, A) = P \in A, \,\, (P \cdot\overrightarrow{v}) \ge (Q \cdot\overrightarrow{v}), \,\, \forall Q \in A \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-b30a798cf0a0e31a8002ed9ec9026774_l3.png)


For a reflected shape, the support function is as follows:

![Rendered by QuickLaTeX.com \[ Support(\overrightarrow{v}, -B) = -Support(- \overrightarrow{v}, B) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-0333035ec69b2688b05915c19dba9e87_l3.png)


The support function for a Minkowski Sum of two shapes can be expressed as the sum of the support functions of individual shapes:

![Rendered by QuickLaTeX.com \[ Support(\overrightarrow{v}, A \oplus B) = Support(\overrightarrow{v}, A) + Support(\overrightarrow{v}, B) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-77b65dda3cb3297d8169f95a8fcdbf8e_l3.png)


Thus, the support function of a CSO of two shapes is:

![Rendered by QuickLaTeX.com \[ Support(\overrightarrow{v}, A \ominus B) = Support(\overrightarrow{v}, A) - Support(- \overrightarrow{v}, B) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7916106f3783c2267dc56584c949f0cf_l3.png)


### Computing CSO Support Point with Space Conversion

Normally, the support functions for different collider geometry are implemented in model space. However, the support function output for a CSO and the direction passed to the function are both in world space. Here is how the space conversion works:

void CsoSupport ( const Collider &colliderA, const Collider &colliderB, const Vec3 &dir, Vec3 &support, Vec3 &supportA, Vec3 &supportB ) { const RigidBody *bodyA = colliderA->Body(); const RigidBody *bodyB = colliderB->Body(); // convert search direction to model space const Vec3 localDirA = bodyA->GlobalToLocalVec(dir); const Vec3 localDirB = bodyB->GlobalToLocalVec(-dir); // compute support points in model space supportA = colliderA.Support(localDirA); supportB = colliderB.Support(localDirB); // convert support points to world space supportA = bodyA->LocalToGlobal(supportA); supportB = bodyB->LocalToGlobal(supportB); // compute CSO support point support = supportA - supportB; }

### End of CSOs & Support Functions

I have covered the necessary tools for us to move onto actual collision detection algorithms. In the next post, I will introduce to you one of the most popular collision detection algorithms, the Gilbert-Johnson-Keerthi (GJK) algorithm.

Thank you. But I have a question.

In the last paragraph, the support function is mainly implemented in model spaces, is this just in terms of using it because many physics engines only keep model spaces in memory?

Yes.

Hi

You say “origin”, but you do not explain what that origin is.

It’s the point (0, 0) in 2D, or (0, 0, 0) in 3D.

Hi, I have one question about Minkowski Difference. I try some case for proving the property that if the CSO of two shapes contains the origin, the two shapes are colliding. It’s true. But I have no idea about it. Can you give me some tips or website resources about it? Thank you.

I have added a short paragraph. It shows a brief proof of why the fact that the CSO of two shapes contains the origin implies collision. I hope this helps.