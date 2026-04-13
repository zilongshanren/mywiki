---
title: 'Game Math: Swing-Twist Interpolation (…Sterp?) | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2018/05/game-math-swing-twist-interpolation-sterp/
author: Allen Chou
published: '2018-05-13'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

Source files are on [GitHub](https://github.com/TheAllenChou/unity-cj-lib).

[Shortcut](https://github.com/TheAllenChou/unity-cj-lib/blob/master/Unity%20CJ%20Lib/Assets/CjLib/QuaternionUtil.cs) to sterp implementation.

[Shortcut](https://github.com/TheAllenChou/unity-cj-lib/blob/master/Unity%20CJ%20Lib/Assets/Example/Quaternion%20Swing%20Twist%20Decomposition/QuaternionSwingTwistDecompositionDemo.cs) to code used to generate animations in this post.

### An Alternative to Slerp

[Slerp](http://allenchou.net/2014/04/game-math-quaternion-basics/#slerp), spherical linear interpolation, is an operation that interpolates from one orientation to another, using a rotational axis paired with the smallest angle possible.

Quick note: [Jonathan Blow](https://en.wikipedia.org/wiki/Jonathan_Blow) explains [here](http://number-none.com/product/Understanding%20Slerp,%20Then%20Not%20Using%20It/) how you should avoid using slerp, if normalized quaternion linear interpolation (nlerp) suffices. Long store short, nlerp is faster but does not maintain constant angular velocity, while slerp is slower but maintains constant angular velocity; use nlerp if you’re interpolating across small angles or you don’t care about constant angular velocity; use slerp if you’re interpolating across large angles and you care about constant angular velocity. But for the sake of using a more commonly known and used building block, the remaining post will only mention slerp. Replacing all following occurrences of slerp with nlerp would not change the validity of this post.

In general, slerp is considered superior over interpolating individual components of Euler angles, as the latter method usually yields orientational sways.

But, sometimes slerp might not be ideal. Look at the image below showing two different orientations of a rod. On the left is one orientation, and on the right is the resulting orientation of rotating around the axis shown as a cyan arrow, where the pivot is at one end of the rod.

![](../../assets/77fab0482a22e5fb.png)


If we slerp between the two orientations, this is what we get:

![](../../assets/8562462351c1a75d.gif)


Mathematically, slerp takes the “shortest rotational path”. The [quaternion](http://allenchou.net/2014/04/game-math-quaternion-basics/) representing the rod’s orientation travels along the shortest arc on a 4D hypersphere. But, given the rod’s elongated appearance, the rod’s moving end seems to be deviating from the shortest arc on a 3D sphere.

My intended effect here is for the rod’s moving end to travel along the shortest arc in 3D, like this:

![](../../assets/675906b3451b1887.gif)


The difference is more obvious if we compare them side-by-side:

![](../../assets/5c77b138aa297abb.gif)


This is where swing-twist decomposition comes in.


### Swing-Twist Decomposition

Swing-Twist decomposition is an operation that splits a rotation into two concatenated rotations, swing and twist. Given a twist axis, we would like to separate out the portion of a rotation that contributes to the twist around this axis, and what’s left behind is the remaining swing portion.

There are multiple ways to derive the formulas, but [this particular one](http://www.euclideanspace.com/maths/geometry/rotations/for/decomposition/forum.htm) by Michaele Norel seems to be the most elegant and efficient, and it’s the only one I’ve come across that does not involve any use of trigonometry functions. I will first show the formulas now and then paraphrase his proof later:

Given a rotation represented by a quaternion ![Rendered by QuickLaTeX.com R = [W_R, \overrightarrow{V_R}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-602c5da631f207762486848ed7811fe2_l3.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_T}](../../assets/5f178ec460e513a9.png)

![Rendered by QuickLaTeX.com R](../../assets/ab9820595f7b211b.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_R}](../../assets/3d0012ba9d25ac99.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_T}](../../assets/5f178ec460e513a9.png)


![Rendered by QuickLaTeX.com \[ T = [W_R, proj_{\overrightarrow{V_T}}(\overrightarrow{V_R})]. \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-602400e5f248c2133f3fb26758f500dc_l3.png)


We want to decompose ![Rendered by QuickLaTeX.com R](../../assets/ab9820595f7b211b.png)

![Rendered by QuickLaTeX.com S](../../assets/fd14bbf347776f9d.png)

![Rendered by QuickLaTeX.com R = ST](../../assets/d2d6c12a2cd87474.png)

![Rendered by QuickLaTeX.com R](../../assets/ab9820595f7b211b.png)

![Rendered by QuickLaTeX.com T](../../assets/1b8983ecb9847b06.png)


![Rendered by QuickLaTeX.com \[ S= R T^{-1} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-6a9dca239702385afa4472d48a23bd76_l3.png)


Beware that ![Rendered by QuickLaTeX.com S](../../assets/fd14bbf347776f9d.png)

![Rendered by QuickLaTeX.com T](../../assets/1b8983ecb9847b06.png)


Below is my code implementation of swing-twist decomposition. Note that it also takes care of the singularity that occurs when the rotation to be decomposed represents a 180-degree rotation.

public static void DecomposeSwingTwist ( Quaternion q, Vector3 twistAxis, out Quaternion swing, out Quaternion twist ) { Vector3 r = new Vector3(q.x, q.y, q.z); // singularity: rotation by 180 degree if (r.sqrMagnitude < MathUtil.Epsilon) { Vector3 rotatedTwistAxis = q * twistAxis; Vector3 swingAxis = Vector3.Cross(twistAxis, rotatedTwistAxis); if (swingAxis.sqrMagnitude > MathUtil.Epsilon) { float swingAngle = Vector3.Angle(twistAxis, rotatedTwistAxis); swing = Quaternion.AngleAxis(swingAngle, swingAxis); } else { // more singularity: // rotation axis parallel to twist axis swing = Quaternion.identity; // no swing } // always twist 180 degree on singularity twist = Quaternion.AngleAxis(180.0f, twistAxis); return; } // meat of swing-twist decomposition Vector3 p = Vector3.Project(r, twistAxis); twist = new Quaternion(p.x, p.y, p.z, q.w); twist = Normalize(twist); swing = q * Quaternion.Inverse(twist); }

Now that we have the means to decompose a rotation into swing and twist components, we need a way to use them to interpolate the rod’s orientation, replacing slerp.

### Swing-Twist Interpolation

Replacing slerp with the swing and twist components is actually pretty straightforward. Let the ![Rendered by QuickLaTeX.com Q_A](../../assets/c5d5d0ccebfb9382.png)

![Rendered by QuickLaTeX.com Q_B](../../assets/7551135c584dc6f1.png)

![Rendered by QuickLaTeX.com t](../../assets/2095d761bc925f10.png)

![Rendered by QuickLaTeX.com Q_I](../../assets/9733f02c171ea572.png)


So we replace:

![Rendered by QuickLaTeX.com \[ Slerp(Q_A, Q_B, t) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-839115f0ec861270f25ab50a364afd72_l3.png)


with:

![Rendered by QuickLaTeX.com \[ Slerp(Q_I, S, t) Slerp(Q_I, T, t) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-18a678598fc12fb52c4ef1adcd9ddc5b_l3.png)


From the rod example, we choose the twist axis to align with the rod’s longest side. Let’s look at the effect of the individual components ![Rendered by QuickLaTeX.com Slerp(Q_I, S, t)](../../assets/65ea527691a4bd87.png)

![Rendered by QuickLaTeX.com Slerp(Q_I, T, t)](../../assets/4c4a7a54ab2fcd1d.png)

![Rendered by QuickLaTeX.com t](../../assets/2095d761bc925f10.png)


![](../../assets/bd4f006358180f31.gif)


And as we concatenate these two components together, we get a swing-twist interpolation that rotates the rod such that its moving end travels in the shortest arc in 3D. Again, here is a side-by-side comparison of slerp (left) and swing-twist interpolation (right):

![](../../assets/5c77b138aa297abb.gif)


I decided to name my swing-twist interpolation function **sterp**. I think it’s cool because it sounds like it belongs to the function family of **lerp** and **slerp**. Here’s to hoping that this name catches on.

And here’s my code implementation:

public static Quaternion Sterp ( Quaternion a, Quaternion b, Vector3 twistAxis, float t ) { Quaternion deltaRotation = b * Quaternion.Inverse(a); Quaternion swingFull; Quaternion twistFull; QuaternionUtil.DecomposeSwingTwist ( deltaRotation, twistAxis, out swingFull, out twistFull ); Quaternion swing = Quaternion.Slerp(Quaternion.identity, swingFull, t); Quaternion twist = Quaternion.Slerp(Quaternion.identity, twistFull, t); return twist * swing; }

### Proof

Lastly, let’s look at the proof for the swing-twist decomposition formulas. All that needs to be proven is that the swing component ![Rendered by QuickLaTeX.com S](../../assets/fd14bbf347776f9d.png)

![Rendered by QuickLaTeX.com S](../../assets/fd14bbf347776f9d.png)


Let ![Rendered by QuickLaTeX.com \overrightarrow{V_{R\parallel}}](../../assets/7438a8766c9ccba6.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_R}](../../assets/3d0012ba9d25ac99.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_T}](../../assets/5f178ec460e513a9.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_R}](../../assets/3d0012ba9d25ac99.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_T}](../../assets/5f178ec460e513a9.png)


![Rendered by QuickLaTeX.com \[ \overrightarrow{V_{R\parallel}} = proj_{\overrightarrow{V_T}}(\overrightarrow{V_R}) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-d976f5dd8d000c41c14ed7fcf33faf01_l3.png)


Let ![Rendered by QuickLaTeX.com \overrightarrow{V_{R\bot}}](../../assets/39418034d7ecf11e.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_R}](../../assets/3d0012ba9d25ac99.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_T}](../../assets/5f178ec460e513a9.png)


![Rendered by QuickLaTeX.com \[ \overrightarrow{V_{R\bot}} = \overrightarrow{V_R} - \overrightarrow{V_{R\parallel}} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-f28bf681d9445d75956ea54161735398_l3.png)


So the scalar-vector form of ![Rendered by QuickLaTeX.com T](../../assets/1b8983ecb9847b06.png)


![Rendered by QuickLaTeX.com \[ T = [W_R, proj_{\overrightarrow{V_T}}(\overrightarrow{V_R})] = [W_R, \overrightarrow{V_{R\parallel}}] \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-10c873619125ff3f87cbccf8917aca44_l3.png)


Using the [quaternion multiplication](http://allenchou.net/2014/04/game-math-quaternion-basics/#multiplication) formula, here is the scalar-vector form of the swing quaternion:

![Rendered by QuickLaTeX.com \begin{flalign*} S &= R T^{-1} \\ &= [W_R, \overrightarrow{V_R}] [W_R, -\overrightarrow{V_{R\parallel}}] \\ &= [W_R^2 - \overrightarrow{V_R} \cdot (-\overrightarrow{V_{R\parallel}}), \overrightarrow{V_R} \times (-\overrightarrow{V_{R\parallel}}) + W_R \overrightarrow{V_R} + W_R (-\overrightarrow{V_{R\parallel}})] \\ &= [W_R^2 - \overrightarrow{V_R} \cdot (-\overrightarrow{V_{R\parallel}}), \overrightarrow{V_R} \times (-\overrightarrow{V_{R\parallel}}) + W_R (\overrightarrow{V_R} -\overrightarrow{V_{R\parallel}})] \\ &= [W_R^2 - \overrightarrow{V_R} \cdot (-\overrightarrow{V_{R\parallel}}), \overrightarrow{V_R} \times (-\overrightarrow{V_{R\parallel}}) + W_R \overrightarrow{V_{R\bot}}] \end{flalign*}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-038d03f9f07393032c889c60a1a5d7a2_l3.png)


Take notice of the vector part of the result:

![Rendered by QuickLaTeX.com \[ \overrightarrow{V_R} \times (-\overrightarrow{V_{R\parallel}}) + W_R \overrightarrow{V_{R\bot}} \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-84cc308d27458e50c39c58b5b3b83771_l3.png)


This is a vector parallel to the rotational axis of ![Rendered by QuickLaTeX.com S](../../assets/fd14bbf347776f9d.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_R} \times (-\overrightarrow{V_{R\parallel}})](../../assets/6926543015e1f7de.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_{R\bot}}](../../assets/39418034d7ecf11e.png)

![Rendered by QuickLaTeX.com \overrightarrow{V_T}](../../assets/5f178ec460e513a9.png)

![Rendered by QuickLaTeX.com S](../../assets/fd14bbf347776f9d.png)

![Rendered by QuickLaTeX.com S](../../assets/fd14bbf347776f9d.png)

![Rendered by QuickLaTeX.com T](../../assets/1b8983ecb9847b06.png)


### Conclusion

That’s all.

Given a twist axis, I have shown how to decompose a rotation into a swing component and a twist component.

Such decomposition can be used for swing-twist interpolation, an alternative to slerp that interpolates between two orientations, which can be useful if you’d like some point on a rotating object to travel along the shortest arc.

I like to call such interpolation **sterp**.

Sterp is merely an alternative to slerp, not a replacement. Also, slerp is definitely more efficient than sterp. Most of the time slerp should work just fine, but if you find unwanted orientational sway on an object’s moving end, you might want to give sterp a try.

### Edit: Application in 2D

An application of swing-twist decomposition in 2D just came to mind.

If the twist axis is chosen to be orthogonal to the screen, then we can utilize swing-twist decomposition to use the orientation of objects in 3D to drive the rotation of 2D elements in screen space or some other data. The twist component represents exactly the portion of 3D rotation projected onto screen space.

However, in terms of performance, we might be better off just projecting a 3D object’s local axis onto screen space and find the angle between it and a screen space axis. But then again, the swing-twist decomposition approach doesn’t have the singularity the projection approach has when the chosen local axis becomes orthogonal to the screen.

Interesting! Great with some example code because the papers on this are a bit tricky to read.

Can you elaborate some more on the singularity condition? I tried to implement something myself with the help of this and some other sources and I try to understand some more.

It depends on the software library you use, but provided it is Unity it seems that first you check the squared norm of the imaginary part? A square norm of zero on the imaginary part would imply an identity quaternion, or a N*360 degree rotation, which the “meat” of the algorithm already would handle implicitly by returning two identity quaternions, at least analytically speaking. Is this then for coping with numerical issues when being very close to identity perhaps?

If q is an identity quaternion, “Vector3 rotatedTwistAxis = q * twistAxis” should be a no-op. Then “Vector3 swingAxis = Vector3.Cross(twistAxis, rotatedTwistAxis);” will always be a zero vector.

That implies that swing will be returned as an identity quaternion, but twist on the other hand will be “// always twist 180 degree on singularity

twist = Quaternion.AngleAxis(180.0f, twistAxis); ”

a rotation of 180 degrees. But, it is there, so I guess it solves some problem?

Here is a thread wich a discussion on the subject: https://math.stackexchange.com/questions/4031687/singularity-of-swing-twist-decomposition

Hi,

I think you need to multiply by the result by a in your sterp function, ie. twist * swing * a. Because twist * swing is only the delta rotation. If we want a quaternion between a and b, we need to start from a, and as such multiply by a in the result.

Thanks for the interesting article!