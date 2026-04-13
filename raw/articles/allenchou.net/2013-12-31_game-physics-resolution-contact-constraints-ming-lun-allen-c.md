---
title: 'Game Physics: Resolution – Contact Constraints | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2013/12/game-physics-resolution-contact-constraints/
author: Allen Chou
published: '2013-12-31'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

Contact constraints are amongst the most important constraints for a physics engine, because you would want to resolve collision in most scenarios. And if not done properly, your rigid bodies can behave in a very visually jarring way to the player.

### Derivation

Remember that Sequential Impulse models constraints in the form of ![Rendered by QuickLaTeX.com JV + b = 0](../../assets/a0c8cdc3f81f8237.png)

![Rendered by QuickLaTeX.com J](../../assets/401c663f919c1f99.png)

__Jacobian matrix__, ![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

__velocity vector__, and ![Rendered by QuickLaTeX.com b](../../assets/f18bd22e727492e1.png)

__bias term__. [Erin Catto](http://twitter.com/erin_catto) (author of [Box2D](http://box2d.org)) proposed a systematic way to derive velocity constraints: you first find the position constraint ![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com \dot{C}](../../assets/1caecbbdafaabeb1.png)


Based on the contact format [previously described](http://allenchou.net/2013/12/game-physics-contact-generation-epa/), a possible interface for contact data may look as follows.

struct Contact { // contact point data Vec3 globalPositionA; Vec3 globalPositionB; Vec3 localPositionA; Vec3 localPositionB; // these 3 vectors form an orthonormal basis Vec3 normal; // points from colliderA to colliderB Vec3 tangent1, tangent2; // penetration depth float depth; // for clamping (more on this later) float normalImpulseSum; float tangentImpulseSum1; float tangentImpulseSUm2; Contact(void) : normalImpulseSum(0.0f) , tangentImpulseSum1(0.0f) , tangentImpulseSum2(0.0f) { } // there's typically more stuff // but omitted for simplicity's sake };

Let us look at the figure below before moving onto finding the position constraint.

![contacts-figure](../../assets/ebceafc1479fbad5.png)



![Rendered by QuickLaTeX.com C_A](../../assets/37caae3cabfba064.png)

![Rendered by QuickLaTeX.com C_B](../../assets/4964440e506e009e.png)

![Rendered by QuickLaTeX.com P_A](../../assets/464522535cfb765a.png)

![Rendered by QuickLaTeX.com P_B](../../assets/be75799220c572d1.png)

![Rendered by QuickLaTeX.com \overrightarrow{r_A}](../../assets/dc76c2cacee48eca.png)

![Rendered by QuickLaTeX.com \overrightarrow{r_b}](../../assets/c75cb3a195770cad.png)

![Rendered by QuickLaTeX.com \overrightarrow{n}](../../assets/58afda5173643155.png)

![Rendered by QuickLaTeX.com \overrightarrow{t_1}](../../assets/36a222cf90c023de.png)

![Rendered by QuickLaTeX.com \overrightarrow{t_2}](../../assets/0e5181861f282ed8.png)

![Rendered by QuickLaTeX.com \overrightarrow{t_2}](../../assets/0e5181861f282ed8.png)


We basically want our penetration depth to be zero, so the position constraint states that: the vector from ![Rendered by QuickLaTeX.com P_A](../../assets/464522535cfb765a.png)

![Rendered by QuickLaTeX.com P_B](../../assets/be75799220c572d1.png)

![Rendered by QuickLaTeX.com \overrightarrow{n}](../../assets/58afda5173643155.png)

![Rendered by QuickLaTeX.com \ge 0](../../assets/d1401dfad749ce81.png)


We can see that:

![Rendered by QuickLaTeX.com \[P_A = C_A + \overrightarrow{r_A}\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-f500f490c64e4f824908e22061c69dde_l3.png)


![Rendered by QuickLaTeX.com \[P_B = C_B + \overrightarrow{r_B}\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-38fe387e33eb7f4df4d722187bf6d8df_l3.png)


So, the position constraint ![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)


![Rendered by QuickLaTeX.com \[C \, : \, (P_B - P_A) \cdot \overrightarrow{n} \ge 0\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-4ea9d107a6f8c66918ba61f364ba8c84_l3.png)


![Rendered by QuickLaTeX.com \[C \, : \, (C_B + \overrightarrow{r_B} - C_A - \overrightarrow{r_A}) \cdot \overrightarrow{n} \ge 0\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-fc5df65c8b31667ed53ee6a843f63d47_l3.png)


By differentiating ![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com \dot{C}](../../assets/1caecbbdafaabeb1.png)


![Rendered by QuickLaTeX.com \[\dot{C} \, : \, (-\overrightarrow{V_A} - \overrightarrow{\omega_A} \times \overrightarrow{r_A} + \overrightarrow{V_B} + \overrightarrow{\omega_B} \times \overrightarrow{r_B}) \cdot \overrightarrow{n} \ge 0\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-d1db09413b97b163fd13dc74a6826941_l3.png)


By some algebraic manipulation and making use of the triple product identity ![Rendered by QuickLaTeX.com \overrightarrow{A} \times \overrightarrow{B} \cdot \overrightarrow{C} = \overrightarrow{C} \times \overrightarrow{A} \cdot \overrightarrow{B}](../../assets/ace11c58350f6f1c.png)


![Rendered by QuickLaTeX.com \[\dot{C} \, : \, JV + b \ge 0,\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-27780ca003ab5a50b673acdc73c73af5_l3.png)


where:

![Rendered by QuickLaTeX.com \[J ={\left[ {\begin{array}{cccc}-\overrightarrow{n}^T & (-\overrightarrow{r_A} \times \overrightarrow{n})^T & \overrightarrow{n}^T & (\overrightarrow{r_B} \times \overrightarrow{n})^T \\\end{array} } \right]},\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-8091b2aa6fd4843118c68cdea2cf3c47_l3.png)


![Rendered by QuickLaTeX.com \[V ={\left[ {\begin{array}{ccc}\overrightarrow{V_A} \\\overrightarrow{\omega_A} \\\overrightarrow{V_B} \\\overrightarrow{\omega_B} \\\end{array} } \right]}\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-df52ad744223846fcae750b902f262b0_l3.png)


![Rendered by QuickLaTeX.com \[b = 0\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-37778ddf9f5221b6c168c62aaf5f6a25_l3.png)


Note that the form of our velocity constraint is ![Rendered by QuickLaTeX.com JV + b \ge 0](../../assets/2fd503014b06733e.png)

![Rendered by QuickLaTeX.com JV + b = 0](../../assets/a0c8cdc3f81f8237.png)

![Rendered by QuickLaTeX.com JV + b = 0](../../assets/a0c8cdc3f81f8237.png)


The geometric interpretation of the velocity constraint we just derived is as follows: __the projection of the relative velocity of the two contact points onto the contact normal is zero__. This means if we solve this constraint, the two contact points would not penetrate further.

Recall that the correction to the velocity vector ![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

![Rendered by QuickLaTeX.com \Delta V = M^{-1} J^T \lambda](../../assets/76910ec9b07752db.png)

![Rendered by QuickLaTeX.com \lambda](../../assets/9c8bfcca431ca886.png)


![Rendered by QuickLaTeX.com \[\lambda = \frac {-(JV + b)} {J M^{-1} J^T}\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-877b775a6d3702f14e4a8160979466cd_l3.png)


and ![Rendered by QuickLaTeX.com M](../../assets/91ac030eac3e8e2e.png)


![Rendered by QuickLaTeX.com \[M ={\left[ {\begin{array}{cccc}M_A & 0 & 0 & 0 \\0 & I_A & 0 & 0 \\0 & 0 & M_B & 0 \\0 & 0 & 0 & I_B \\\end{array} } \right]},\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1952b2959a3848c31129d3ae4dd5f2cb_l3.png)


### Clamping The Lagrangian Multiplier

We have found out how to solve the contact constraint. However, this is not the entire picture. Remember there are usually more than one contact constraints in the entire physics system. The Sequential Impulse method iterates through all contacts and solve each contact constraints one-by-one:

for (Manifold manifold: manifolds) for (Contact contact : manifold.contacts) SolveContactConstraints(contact);

The change to a collider’s velocity will affect the result of later resolution of the same collider. At one point, you may end up with a velocity change that actually pulls a collider pairs closer instead of pushing them apart. For this reason, we need to perform some clamping when applying velocity change using ![Rendered by QuickLaTeX.com \lambda](../../assets/9c8bfcca431ca886.png)

`normalImpulseSum`

.

We want to make sure that throughout all iterations within one time step, the following inequality is satisfied:

![Rendered by QuickLaTeX.com \[\Sigma \lambda_i \ge 0,\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-570b1348cfac7a81bd7ca27e9c7ac4f0_l3.png)


where ![Rendered by QuickLaTeX.com \lambda_i](../../assets/bd234e615413f523.png)


Each time we compute ![Rendered by QuickLaTeX.com \lambda](../../assets/9c8bfcca431ca886.png)

`normalImpulseSum`

, add ![Rendered by QuickLaTeX.com \lambda](../../assets/9c8bfcca431ca886.png)

`normalImpulseSum`

, clamp `normalImpulseSum`

between 0 and positive infinity, and then calculate the difference of the clamped `normalImpulseSum`

from the previously copied `normalImpulseSum`

. This difference is the actual Lagrangian Multiplier we want to use to solve the contact constraint.

### Baumgarte Stabilization

Solving the velocity constraint is not enough. Remember that by solving the velocity constraint, we only prevent the two colliders from further penetrating. It does nothing to actually push them apart. The accumulated error results in “positional drift”.

This is when Baumgarte Stabilization comes into play. Some call this method a hack, some view it as an elegant way to fix positional drifts. Either way, it works.

The basic idea is to feed the penetration depth (position error) back into the velocity constraint as a bias, so just a little bit of energy is introduced into the system to push the two colliders apart.

As previously shown, the bias term ![Rendered by QuickLaTeX.com b](../../assets/f18bd22e727492e1.png)


To compute the penetration depth ![Rendered by QuickLaTeX.com d](../../assets/2ec4f4c38fda79cb.png)


![Rendered by QuickLaTeX.com \[d = (P_B - P_A) \cdot (- \overrightarrow{n})\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-504c0619b94f6adc524352c37e218f98_l3.png)


We then feed this back into the constraint equation ![Rendered by QuickLaTeX.com JV + b = 0](../../assets/a0c8cdc3f81f8237.png)

![Rendered by QuickLaTeX.com d](../../assets/2ec4f4c38fda79cb.png)

__Baumgarte term__:

![Rendered by QuickLaTeX.com \[b = -\frac{\beta}{\Delta t} \cdot d,\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-6c3ad091e3046faf98ade633a35417dd_l3.png)


where ![Rendered by QuickLaTeX.com \beta](../../assets/d8727045a49e383c.png)

![Rendered by QuickLaTeX.com \beta](../../assets/d8727045a49e383c.png)


### Restitution

Wait, what about having the colliders “bouncing” apart? So far by solving the velocity contact constraints only make sure that the two colliders do not penetrate any further. There is another quantity we are going to add to the bias term in the constraint equation in addition to the Baumgarte term: the __restitution term__.

The __coefficient of restitution__ between two objects, denoted ![Rendered by QuickLaTeX.com C_R](../../assets/390a14ecfddb41dd.png)

__the ratio between the parting speed of two colliders after collision and the closing speed before collision__; for realistic result, you would want to set this value between zero and one.

Therefore, the contribution of the restitution term to the bias term is simply the coefficient of restitution times the projection of the closing velocity of two contact points onto the normal vector:

![Rendered by QuickLaTeX.com \[C_R (-\overrightarrow{V_A} - \overrightarrow{\omega_A} \times \overrightarrow{r_A} + \overrightarrow{V_B} + \overrightarrow{\omega_B} \times \overrightarrow{r_B}) \cdot \overrightarrow{n}\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-5000af7ce3ca37c6301e0cce6e115a59_l3.png)


So our final bias term ![Rendered by QuickLaTeX.com b](../../assets/f18bd22e727492e1.png)


![Rendered by QuickLaTeX.com \[b = -\frac{\beta}{\Delta t} \cdot d + C_R (-\overrightarrow{V_A} - \overrightarrow{\omega_A} \times \overrightarrow{r_A} + \overrightarrow{V_B} + \overrightarrow{\omega_B} \times \overrightarrow{r_B}) \cdot \overrightarrow{n}\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-ae46da4986bd7523299cfbaeb9efda64_l3.png)


### Frictions

So far we have only covered the normal part of contact constraints. Now I’m going to talk about the tangential part of contact constraints, a.k.a. frictions.

Frictional forces are proportional to normal forces, so they are dependent on the result of contact resolution in the normal direction. Thus, we typically solve the tangential part of contact constraints after the normal part.

The normal part of contact constraints attempts to zero out the projection of the relative velocity of two contact points onto the contact normal (without considering the bias term ![Rendered by QuickLaTeX.com b](../../assets/f18bd22e727492e1.png)


The tangential part and normal part of contact constraints are basically doing the same thing, except that the directions onto which the relative velocity of the two contact points are projected are different. So there is no surprise to see that the Jacobians for the two contact tangents look very similar to the Jacobian for the contact normal. Let’s relabel the Jacobian for the contact normal ![Rendered by QuickLaTeX.com J_\overrightarrow{n}](../../assets/9ac8465434075766.png)

![Rendered by QuickLaTeX.com J_\overrightarrow{t_1}](../../assets/b975c782136e65fd.png)

![Rendered by QuickLaTeX.com J_\overrightarrow{t_2}](../../assets/a1225b6eb6e95f2c.png)


![Rendered by QuickLaTeX.com \[J_\overrightarrow{n} ={\left[ {\begin{array}{cccc}-\overrightarrow{n}^T & (-\overrightarrow{r_A} \times \overrightarrow{n})^T & \overrightarrow{n}^T & (\overrightarrow{r_B} \times \overrightarrow{n})^T \\\end{array} } \right]}\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-b2da3d43e974ff6269daf57f5f4decac_l3.png)


![Rendered by QuickLaTeX.com \[J_\overrightarrow{t_1} ={\left[ {\begin{array}{cccc}-\overrightarrow{t_1}^T & (-\overrightarrow{r_A} \times \overrightarrow{t_1})^T & \overrightarrow{t_1}^T & (\overrightarrow{r_B} \times \overrightarrow{t_1})^T \\\end{array} } \right]}\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-808be8290dc356f991d7ac3e3f055df0_l3.png)


![Rendered by QuickLaTeX.com \[J_\overrightarrow{t_2} ={\left[ {\begin{array}{cccc}-\overrightarrow{t_2}^T & (-\overrightarrow{r_A} \times \overrightarrow{t_2})^T & \overrightarrow{t_2}^T & (\overrightarrow{r_B} \times \overrightarrow{t_2})^T \\\end{array} } \right]}\]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-48538f4c25351fb49ce35edfd65a4c4f_l3.png)


Pretty similar, right?

What is also similar is that the Lagrangian Multipliers computed for the contact tangents also need clamping. However, instead of clamping between zero and positive infinity, the boundaries the Lagrangian Multipliers are clamped depend on the normal impulse sum, which is stored in the `normalImpulseSum`

data member. The clamping boundaries are negative and positive `normalImpulseSum`

multiplied by the __coefficient of friction__, denoted ![Rendered by QuickLaTeX.com C_F](../../assets/de550ba7e6c1b1d5.png)

`normalImpulseSum`

as ![Rendered by QuickLaTeX.com \lambda_\overrightarrow{n}_{sum}](../../assets/38b0124d9c2027ea.png)


The clamping process is extremely similar to the normal part: we make copies of `tagentImpulseSum1`

and `tangentImpulseSum2`

, add the Lagrangian Multipliers computed from both tangential Jacobians to `tangentImpulseSum1`

and `tangentImpulseSum2`

, clamp `tangentImpulseSum1`

and `tangentImpulseSum2`

between ![Rendered by QuickLaTeX.com -C_F \lambda_\overrightarrow{n}_{sum}](../../assets/adf9e6bc1aa4a116.png)

![Rendered by QuickLaTeX.com C_F \lambda_\overrightarrow{n}_{sum}](../../assets/17a6df9cb244f0bc.png)

`tangentImpulseSum1`

from the previously copied `tangentImpulseSum1`

and the difference of the clamped `tangentImpulseSum2`

from the previously copied `tangentImpulseSum2`

. These differences are the actual Lagrangian Multipliers we want to use to solve the tangential part of contact constraints.

You might notice that this clamping method is not perfect. We can end up with clamping the magnitude of total tangential impulse to ![Rendered by QuickLaTeX.com \sqrt{2} C_F \lambda_\overrightarrow{n}_{sum}](../../assets/8f2b516243c5bf6d.png)

[DigiPen Institute of Technology](https://www.digipen.edu/), informed me of this idea).

### End of Contact Constraints

This is the end of the derivation of contact constraints and demonstration on how to solve them. I will cover stability issues and how to improve stability using a technique called “warm starting” in later posts.

I implemented this method for multiple corners of a cube to prevent it from falling through the floor.

Most things seem to work well, however if I place the cube on an incline it will automatically slide UP the incline.

Any thoughts on where that sort of error might be?

Nothing immediately comes to mind. Unfortunately, I can only give the boring suggestion of stepping through the calculations to figure out where the upward velocity component comes from.

Thanks. The issue was my contact normal. I didn’t do the transformation correctly between by code and the 3d model code I’m working with (which is left handed).

I have one comment about the line C_dot : JV+b >= 0. Either I misunderstood something, or maybe there needs to be a clarification. It seems that if the contact normal always points from object A to object B then C_dot will always be less than 0 if the two objects are closing on one another (even when not making contact). There has to be something to flip the sign, like having the normal direct be scaled by the sign of the penetration depth.

C_dot is expected to violate the constraint whenever the two objects are closing on one another. The velocity constraint JV + b >= 0 is only enforced when there’s actual penetration.

Thank you, Allen! Using these articles as a guide, I was able to create a simple 2D physics system (no rotation) using circles and boxes. At first it was a bit strange thinking in terms of constraint systems, but it helped to write down and understand each step. I’m pleased with the stability and flexibility of the simulations.

Hi, John. Glad to hear that!

Knowing that my posts are helping people learn makes me happy.

Helped me a lot to understand it! In 2D, what will the mass matrix be?

You just take out the rows and columns related to the Z dimension.

Hi!

How do you derive that differentiating rB is wB x rB?

Thx

The derivative of rB with respect to time is (vB + wB x rB), where vB is the linear part and (wB x rB) is the angular part of the velocity at rB.

Thanks, I think I get it now.

Hi, I’m working on a physics engine based on constraints. At the point “Clamping the Langrangian Multiplier” I dont understand what you are doing. What is the variable

`normalImpulseSum`

for? Is it just the sum of the impulses of the two bodies? And when I read in Erin Catto’s papers he made a large matrix containing all contraints at the same time. Is this a similiar method to the one you’re describing? By the way great website, took me a great step forward:)1. Throughout the iterations within one time step, sometimes you will get a negative normal impulse for one contact as a result of resolving other contacts., which will pull penetrating objects even closer; this is not what we want. The variable

`normalImpulseSum`

is for keeping track of the total normal impulse for a contact throughout the iterations to ensure that it never becomes negative.2. Theoretically, we will get the optimal results by solving all constraints at once in a big matrix. But this is not possible due to limits on computational power. So we use the Sequential Impulse approach, where we solve one to a few constraints at a time, and the we iterate through all constraints multiple times in a single time step.

Hi Allen, i have tried to implement it, but does not work, can i see your implementation please?

The only implementation I have is the one I did for my school project at DigiPen, which I am not allowed to disclose because it belongs to DigiPen. However, you can check out Erin Catto’s implementation in Box2D. I used it as a reference.

Or, you can show your implementation using online paste tools like Pastebin so I can take a look at what’s wrong.

Hi, according to this method, every thing will be solved by velocity changes, but i’m thinking of where is the position constraint solver?

don’t we need to apply Baumgarte directly on our bodies position?

By applying Baumgarte stabilization to solve velocity constraints, we are feeding back positional errors into velocity changes. This has the effect of correcting the positional errors over a few time steps, instead of instantaneously. To apply instant positional correction, you basically integrate the position using the velocity change computed from Baumgarte stabilization and the delta time. This approach can potentially give you faster positional correction, but might introduce more jitter if you have too many conflicting positional constraints. I personally prefer just using Baumgarte stabilization to solve for velocity constraints. It takes multiple frames to correct positional errors, but it’s visually smoother and more stable.

Hi there Erin, I imagine this is because the constraint space for contact constraints is relative to the collision normal itself. Would this be why the orientation of the collision normal in world space is irrelevant?

Hi Allen. I like your site and you have a nice blog! Also congratulations on your position at Naughty Dog!

When you differentiate C, did you consider that the normal vector is not constant? It can rotate with time. But somehow it doesn’t matter that you skipped it. Why?

Wow, it’s Erin Catto himself! I am a big fan of your work, and I love your presentations at GDC and DigiPen.

Actually, I didn’t consider the fact that the normal vector is not constant when I derived the constraint equation, and everything works quite fine for me. Now that you mentioned it, I should probably go back and check my derivation…

[Edit]

On a second thought, a new normal is computed upon every new contact data generation. Normals are treated as constant only when caching (warm starting) is at work, which happens due to frame coherency, so the normals shouldn’t change too much. Do you think it still matters?

Hi Allen, thanks a lot for writing this blog. It’s awesome and I’ve learned a lot. I was wondering about this issue too… The neglected term is basically the penetration depth vector dotted with the derivative of the normal vector. If you look at Erin Catto’s paper “iterative dynamics with temporal coherence”, he mentions that this term is usually neglected as an approximation because the penetration depth is usually small. I have two questions about that… firstly, since we usually use discrete collision detection, why is this assumption valid? Can’t the penetration depth be arbitrary? And also, since the chain rule guarantees C dot=Jv, doesn’t that mean we should still be able to simplify the entire expression into this form, including the neglected term?

Best articles on the subject I have come across! I will need to implement constraints in a project I’m working on and thanks to these articles I’m starting to understand how it all works. Thank you very much. Keep writing them!

You are very welcome. I’m glad this article helped.