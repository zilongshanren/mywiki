---
title: 'Game Physics: Resolution – Constraints & Sequential Impulse | Ming-Lun "Allen"
  Chou | 周明倫'
url: https://allenchou.net/2013/12/game-physics-constraints-sequential-impulse/
author: Allen Chou
published: '2013-12-30'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

### Constraints

The resolution phase of a constraints-based physics engine uses the concept of __constraints__. A free rigid body in 3D has 6 __degrees of freedom__: 3 positional and 3 rotational; a rigid body in 2D has 3 degrees of freedom: 2 positional and 1 rotational. A constraint decreases the degrees of freedom of a rigid body. For instance, a constraint that pins an object in space at its center of mass decreases the object’s degrees of freedom by 3: all the positional degrees of freedom are removed and the object can thus now only rotate with 3 degrees of freedom.

In a constraint-based physics engine, we model everything as a constraint: including collision contacts, frictions, springs, pulleys, you name it. A __joint__ is a constraint that involves the interaction of 2 rigid bodies; the examples enumerated here are all technically joints.

Mathematically, a constraint is of the form ![Rendered by QuickLaTeX.com C = 0](../../assets/6fc856fb0a01e122.png)

![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)



### Sequential Impulse

The part of code during the resolution phase that makes sure all constraints are satisfied is referred to as the __constraint solver__. There are numerous ways to perform this task. One of the most popular methods is Sequential Impulse, proposed and popularized by [Erin Catto](https://twitter.com/erin_catto), author of the famous [Box2D](http://box2d.org). Unless specifically stated otherwise, from here on I will be talking about Sequential Impulse in terms of resolution. Later on, I will draw an analogy between the process of solving constraints with Sequential Impulse and point projections.

Directly manipulating position properties of rigid bodies to satisfy constraints is a bad idea, because it would result in excessive jitters and your game would look really bad. Instead, Erin Catto proposed that we derive the expression for ![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com \dot{C}](../../assets/1caecbbdafaabeb1.png)

![Rendered by QuickLaTeX.com \dot{C}](../../assets/1caecbbdafaabeb1.png)


A velocity constraint ![Rendered by QuickLaTeX.com \dot{C}](../../assets/1caecbbdafaabeb1.png)


![Rendered by QuickLaTeX.com \[ \dot{C} : JV + b = 0, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-55a9d3b967fa752c492a6afe168de8d4_l3.png)


where ![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

__velocity vector__ that contains the linear and angular velocities of both rigid bodies:

![Rendered by QuickLaTeX.com \[ V = {\left[ {\begin{array}{ccc} \overrightarrow{V_A} \\ \overrightarrow{\omega_A} \\ \overrightarrow{V_B} \\ \overrightarrow{\omega_B} \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-52f17adb2c14ef48f6866e8e79c43637_l3.png)


![Rendered by QuickLaTeX.com V_A](../../assets/75d9f7a3ee3d4f3a.png)

![Rendered by QuickLaTeX.com V_B](../../assets/7f99277352ce27d0.png)

![Rendered by QuickLaTeX.com \omega_A](../../assets/6585f77075f70ad1.png)

![Rendered by QuickLaTeX.com \omega_B](../../assets/595ead3957c4eb3e.png)


![Rendered by QuickLaTeX.com J](../../assets/401c663f919c1f99.png)

__Jacobian__ that contains the coefficients of linear combination of velocity components:

![Rendered by QuickLaTeX.com \[ J = {\left[ {\begin{array}{cccc} \overrightarrow{J_{V_A}}^T & \overrightarrow{J_{\omega_A}}^T & \overrightarrow{J_{V_B}}^T & \overrightarrow{J_{\omega_B}}^T \\ \end{array} } \right]}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-cfbfcbdfc1d302cf7e86f3558dc5b970_l3.png)


where ![Rendered by QuickLaTeX.com \overrightarrow{J_{V_A}}](../../assets/d5eafd3ea7eeaf9b.png)

![Rendered by QuickLaTeX.com \overrightarrow{J_{\omega_A}}](../../assets/22b6ca92880d4a35.png)

![Rendered by QuickLaTeX.com \overrightarrow{J_{V_B}}](../../assets/e1e9d16a210a00b3.png)

![Rendered by QuickLaTeX.com \overrightarrow{J_{\omega_B}}](../../assets/98f133eb5ef3e4c5.png)


The bias term ![Rendered by QuickLaTeX.com b](../../assets/f18bd22e727492e1.png)


### Solving Constraints

So, for a single constraint ![Rendered by QuickLaTeX.com \dot{C} : JV + b = 0](../../assets/2a6e9b53d30051d2.png)


First, please take a leap of faith here and believe that the change we need to apply to the velocity vector ![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

![Rendered by QuickLaTeX.com \Delta V](../../assets/4cd3577dafc4c6aa.png)

![Rendered by QuickLaTeX.com M^{-1} J^T](../../assets/2262a70bf44d536a.png)

![Rendered by QuickLaTeX.com M](../../assets/91ac030eac3e8e2e.png)

__mass matrix__:

![Rendered by QuickLaTeX.com \[ M = {\left[ {\begin{array}{cccc} M_A & 0 & 0 & 0 \\ 0 & I_A & 0 & 0 \\ 0 & 0 & M_B & 0 \\ 0 & 0 & 0 & I_B \\ \end{array} } \right]}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-3acd4af3e6b02093deea9c72ed1b1395_l3.png)


where each ![Rendered by QuickLaTeX.com 0](../../assets/478d6682b71a5d02.png)

![Rendered by QuickLaTeX.com M_A](../../assets/522191c8047131e3.png)

![Rendered by QuickLaTeX.com m_A](../../assets/5b3e9ee6cc6f23c3.png)

![Rendered by QuickLaTeX.com I_A](../../assets/455424870f36c04e.png)

![Rendered by QuickLaTeX.com M_B](../../assets/121a05aff813a207.png)

![Rendered by QuickLaTeX.com m_B](../../assets/3c30df0a487d28ae.png)

![Rendered by QuickLaTeX.com I_B](../../assets/22493514ae16f0a4.png)


![Rendered by QuickLaTeX.com \[ M_A = {\left[ {\begin{array}{ccc} m_A & 0 & 0 \\ 0 & m_A & 0 \\ 0 & 0 & m_A \\ \end{array} } \right]}, \, M_B = {\left[ {\begin{array}{ccc} m_B & 0 & 0 \\ 0 & m_B & 0 \\ 0 & 0 & m_B \\ \end{array} } \right]}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-40c8fed8e44410a0229b37f36ae1ccb2_l3.png)


The inverse of the mass matrix is thus:

![Rendered by QuickLaTeX.com \[ M^{-1} = {\left[ {\begin{array}{cccc} M_A^{-1} & 0 & 0 & 0 \\ 0 & I_A^{-1} & 0 & 0 \\ 0 & 0 & M_B^{-1} & 0 \\ 0 & 0 & 0 & I_B^{-1} \\ \end{array} } \right]}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7429620bcadd885305c6b3d231caec92_l3.png)


Now that we know (or assume at this point) that the required change to the velocity vector is proportional to ![Rendered by QuickLaTeX.com M^{-1} J^T](../../assets/2262a70bf44d536a.png)

![Rendered by QuickLaTeX.com \dot{C} : JV + b = 0](../../assets/2a6e9b53d30051d2.png)

![Rendered by QuickLaTeX.com \lambda](../../assets/9c8bfcca431ca886.png)

__Lagrangian Multiplier__. So the required change to the velocity vector is ![Rendered by QuickLaTeX.com M^{-1} J^T \lambda](../../assets/37a6b26fb3f8733b.png)

![Rendered by QuickLaTeX.com \Delta V](../../assets/4cd3577dafc4c6aa.png)


![Rendered by QuickLaTeX.com \[ J(V + \Delta V) + b = 0, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-3bde27675853768bde0f4b32ae10a0fe_l3.png)


and ![Rendered by QuickLaTeX.com \Delta V](../../assets/4cd3577dafc4c6aa.png)

![Rendered by QuickLaTeX.com M^{-1} J^T \lambda](../../assets/37a6b26fb3f8733b.png)


![Rendered by QuickLaTeX.com \[ J(V + M^{-1} J^T \lambda) + b = 0. \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-90cbcb6b402bc3c7977f17d23003f2a8_l3.png)


So, with a few algebraic manipulations, we get the following formula:

![Rendered by QuickLaTeX.com \[ \lambda = \frac {-(JV + b)} {J M^{-1} J^T} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9adea8b2587d49430b97e587e71365e1_l3.png)


We call ![Rendered by QuickLaTeX.com J M^{-1} J^T](../../assets/f3948f9e9bcef31f.png)

__effective mass__.

Great. We now have a way to solve for ![Rendered by QuickLaTeX.com \lambda](../../assets/9c8bfcca431ca886.png)

![Rendered by QuickLaTeX.com \Delta V = M^{-1} J^T \lambda](../../assets/76910ec9b07752db.png)

![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

![Rendered by QuickLaTeX.com \dot{C} = JV + b](../../assets/01f587186073939e.png)


If we have multiple constraints in the physics system, we then just iteratively repeat this process on all constraints, and the system would converge to a global solution, hence the name Sequential Impulse.

### The Point-Projection Analogy

Remember the leap of faith of believing that ![Rendered by QuickLaTeX.com \Delta V](../../assets/4cd3577dafc4c6aa.png)

![Rendered by QuickLaTeX.com M^{-1} J^T](../../assets/2262a70bf44d536a.png)


Recall your high school math and look at the equation below:

![Rendered by QuickLaTeX.com \[ ax + by + cz + d = 0 \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1efb65da2882fdb823dc3f3982a0b1e7_l3.png)


What does it look like? Right, a plane equation in 3D.

If a point ![Rendered by QuickLaTeX.com (x, y, z)](../../assets/d07300f37c3ec746.png)

![Rendered by QuickLaTeX.com ax + by + cz + d \ne 0](../../assets/749269e38d6063c6.png)

![Rendered by QuickLaTeX.com (a, b, c)](../../assets/2782738043c20166.png)


If we group the coefficients and variables into separate matrices, the plane equation becomes:

![Rendered by QuickLaTeX.com \[ NP + d = 0, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-6a255f7322af25eeaafe72506cc19b98_l3.png)


where ![Rendered by QuickLaTeX.com N](../../assets/60aa89f3f3987398.png)

![Rendered by QuickLaTeX.com (a, b, c)](../../assets/2782738043c20166.png)


![Rendered by QuickLaTeX.com \[ N = {\left[ {\begin{array}{ccc} a & b & c \end{array} } \right]}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9e26526143ad45e5b5618ebf804f8a6e_l3.png)


and ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com (x, y, z)](../../assets/d07300f37c3ec746.png)


![Rendered by QuickLaTeX.com \[ P = {\left[ {\begin{array}{c} x \\ y \\ z \\ \end{array} } \right]} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-acb7d3f2017c39786294694a2720c20a_l3.png)


![Rendered by QuickLaTeX.com d](../../assets/2ec4f4c38fda79cb.png)


The required change to ![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com \Delta P](../../assets/ca80952da1d62afb.png)

![Rendered by QuickLaTeX.com N^T](../../assets/dbbff845844d1e6a.png)


Do you see it now? ![Rendered by QuickLaTeX.com NP + d = 0](../../assets/efd3f80d100dd3f8.png)

![Rendered by QuickLaTeX.com JV + b = 0](../../assets/a0c8cdc3f81f8237.png)

![Rendered by QuickLaTeX.com \Delta V](../../assets/4cd3577dafc4c6aa.png)

![Rendered by QuickLaTeX.com J^T](../../assets/df4f64753b6617fc.png)

![Rendered by QuickLaTeX.com J^T](../../assets/df4f64753b6617fc.png)

![Rendered by QuickLaTeX.com M^{-1} J^T](../../assets/2262a70bf44d536a.png)


Using Sequential Impulse, we iteratively repeat the process of “point projection”. If there are not conflicting constraints, we would eventually converge to the “intersection of all planes”, which is the global solution.

On a side note, if our physics system contains conflicting constraints (say, an impossible setup of distant joints), then Sequential Impulse cannot find a proper global solution, which is equivalent to trying to find an intersection of planes that don’t actually have a common intersection.

### Solving Multiple Constraints in One Shot

Sometimes, we would like to solve multiple constraints at once for stability considerations. For instance, it is better to solve a [prismatic joint](http://en.wikipedia.org/wiki/Prismatic_joint) as solving a distance joint and angular joint simultaneously rather than solving them separately.

In the aforementioned example, the Jacobian matrix would be a 2-by-12 matrix, instead of a 1-by-12 matrix. And the formula for the Lagrangian Multiplier will change from this:

![Rendered by QuickLaTeX.com \[ \lambda = \frac {-(JV + b)} {J M^{-1} J^T} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9adea8b2587d49430b97e587e71365e1_l3.png)


to this:

![Rendered by QuickLaTeX.com \[ \lambda = (J M^{-1} J^T)^{-1} \, (-JV - b)}, \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-dd368399a47f3b8479cf1b7a6469adab_l3.png)


where the effective mass ![Rendered by QuickLaTeX.com J M^{-1} J^T](../../assets/f3948f9e9bcef31f.png)

![Rendered by QuickLaTeX.com \lambda](../../assets/9c8bfcca431ca886.png)


However, ![Rendered by QuickLaTeX.com \Delta V](../../assets/4cd3577dafc4c6aa.png)

![Rendered by QuickLaTeX.com M^{-1} J^T \lambda](../../assets/37a6b26fb3f8733b.png)


### End of Constraints & Sequential Impulse

Now you understand the theory behind velocity constraints and how to solve them with Sequential Impulse. In the following post, I will go on and derive one of the most important constraints for a physics engine: the contact constraint.

I think what you’re calling the “effective mass” is actually the “inverse effective mass”.

I’ve seen both definitions. I’m using the one I saw on the Bullet forums. I can see how “inverse effective mass” would make more sense, since there’s an inverse mass matrix in the definition.

Hello, i have implemented the principles in your articles and it works great for a pairwise constrain, but how can i join more particles togheter without exploding the simulation ?

I tried to constrain 3 particles togheter and they races agaiinst each other.

Iterative impulses didn’t work either.

Are you trying to “constrain” 3 particles together so that they don’t have relative motion? If so, you should try a technique called “composition”. Essentially, a single rigid body owns the three particles, and the rigid body is integrated as a single object. Each particle stores relative position from the rigid body’s center of mass (computed from the particles) and update its position after the rigid body is integrated, no constraints involved.