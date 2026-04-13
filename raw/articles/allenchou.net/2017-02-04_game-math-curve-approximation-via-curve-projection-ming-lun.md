---
title: 'Game Math: Curve Approximation via Curve “Projection” | Ming-Lun "Allen" Chou
  | 周明倫'
url: https://allenchou.net/2017/02/curve-approximation-via-curve-projection/
author: Allen Chou
published: '2017-02-04'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Math Series](http://allenchou.net/game-math-series/).

Also, this post is part 2 of a series ([part 1](http://allenchou.net/2017/01/projecting-a-curve-onto-another/)) leading up to a geometric interpretation of [Fourier transform](https://en.wikipedia.org/wiki/Fourier_transform) and [spherical harmonics](https://en.wikipedia.org/wiki/Spherical_harmonics).

Drawing analogy from vector projection, we have seen what it means to “project” a curve onto another in the previous post. This time, we’ll see how to find a the closest vector on a plane via vector projection, and then we’ll see how it translates to finding the best approximation of a curve via curve “projection”. This handy analogy can help us take another step closer to a geometric interpretation of Fourier transform and spherical harmonics later.


### Closest Vector on a Plane

Given vectors

,

, and

, the closest vector on the plane formed (or “[spanned](https://en.wikipedia.org/wiki/Linear_span)” in [linear algebra](https://en.wikipedia.org/wiki/Linear_algebra) jargon) by

and

is the projection of

onto the plane. This projection, denoted

, is a combination of scaled

and

, in the form of

, that has the least error from

.

The error is measured by the magnitude of the difference vector:

![Rendered by QuickLaTeX.com \[ err(\vec{a}, \vec{d}) = |\vec{a} - \vec{d}| \\ \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-949c58b44ad3110605259f35beb108dc_l3.png)


As pointed out in the [previous post](http://allenchou.net/2017/01/projecting-a-curve-onto-another/), minimizing this error is essentially equivalent to minimizing the [root mean square error](https://en.wikipedia.org/wiki/Root-mean-square_deviation) (RMSE):

![Rendered by QuickLaTeX.com \[ \text{minimize} \enspace err(\vec{a}, \vec{d}) \enspace \Leftrightarrow \enspace \text{minimize} \enspace RMSE(\vec{a}, \vec{d}) \]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-0eb8c65d8c6679aae6f2c424910a46f0_l3.png)


This is what the relationship of

,

,

, and

looks like visually:

![](../../assets/4a583cbe3d7f1bf3.png)


The projection of

onto the plane spanned by

and

, is the vector

on the plan that has the least error from

, and the difference vector

is orthogonal to the plane.

So how do we compute

? In the previous post we’ve seen how to project a vector onto another, so would computing

be as simple as projecting

onto

, and then project the result again onto

? Not really. Here’s why:

As you can see in the figure above,

isn’t parallel to

nor

. Projecting

onto

would give you a vector that is parallel to

, and a subsequent projection onto

would leave you with a result that is parallel to

, which is definitely not

.

One way to do it is to calculate a vector orthogonal to the plane, i.e. a plane normal

, by taking the cross product of the two vectors that span the plane:

. Then, take out the part in

that is parallel to

by subtracting the projection of

onto

from

. What is left of

is the part of

that is parallel to the plane, i.e. the projection:

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{n} &= \vec{b} \times \vec{c} \\ \vec{d} &= \vec{a} - proj(\vec{a}, \vec{n}) \\ \end{flalign*}](../../assets/61f4cacf1f967ba6.png)


But, I want to talk about another way of performing the projection, which is easier to translate to curves later.

and

are not necessarily orthogonal to each other. Let’s find two orthogonal vectors that lie on the plane spanned by

and

. Then, we split

into two parts, one parallel to one vector and one parallel to the other vector. Finally, we combine these two parts together to obtain a vector that is essentially the part of

that is parallel to the plane.

As a simple illustration, if the plane is the X-Z plane, then the obvious two orthogonal vectors of choice would be

and

. To project a vector

onto the X-Z plane, we split it into a part that is parallel to

, which is

, and a part that is parallel to

, which is

. Combining those two parts together would give us

. This makes sense, because projecting a vector onto the X-Z plane is just as simple as dropping the Y component.

Now, given two arbitrary vectors

and

that span a plane, we can generate two orthogonal vectors, denoted

and

, by using a method called the [Gram-Schmidt process](https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process). The first vector

would simply be the

. To compute the second vector

, we take away from

its part that is parallel to

; what’s left of

is orthogonal to

:

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{e}_0 &= \vec{b} \\ \vec{e}_1 &= \vec{c} - proj(\vec{c}, \vec{e}_0) \\ \end{flalign*}](../../assets/54f47f3d2747e728.png)


To compute

, we combine the parts of

that are parallel to

and

, respectively:

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{a}_0 &= proj(\vec{a}, \vec{e}_0) \\ \vec{a}_1 &= proj(\vec{a}, \vec{e}_1) \\ \vec{d} &= \vec{a}_0 + \vec{a}_1 \end{flalign*}](../../assets/0f49cc2c248e0930.png)


### More on Gram-Schmidt Process

The Gram-Schmidt process is actually more general than described above. It can apply to higher dimensions. Given

vectors, denoted

to

, in an

-dimensional space (

), and if the

vectors are [linearly independent](https://en.wikipedia.org/wiki/Linear_independence), i.e. they span an

-dimensional subspace, then we can generate

vectors that are orthogonal to each other, denoted

through

, spanning the same subspace, using the Gram-Schmidt process.

The first vector

would simply be

. To compute the second vector

, we take away from

its part that is parallel to

. To compute the third vector

, we take away from

its part that is parallel to **all previously generated orthogonal vectors**,

and

. Repeat this process until we have reached

and produced

:

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{q}_0 &= \vec{p}_0 \\ \vec{q}_1 &= \vec{p}_1 - proj(\vec{p}_1, \vec{q}_0) \\ \vec{q}_2 &= \vec{p}_2 - proj(\vec{p}_2, \vec{q}_0) - proj(\vec{p}_2, \vec{q}_1) \\ ... \\ \vec{q}_{M-1} &= \vec{p}_{M-1} - \sum^{M-2}_{i=0}{proj(\vec{p}_{M-1}, \vec{q}_i)} \\ \end{flalign*}](../../assets/1d8153d018931942.png)


Projecting an

-dimensional vector onto this

-dimensional subspace would involve combining the parts of the vector parallel to each of the orthogonal vectors. In our example above that involves 3D vectors,

and

. In higher dimensions, no simple 3D cross products can save you there.

Now we are done with vectors. Let’s take a look at curves!

### Curve Approximation

Let’s say our interval of interest is

. Given a 3rd-order polynomial curve

, what’s the best approximation using a 2st-order polynomial curve, or a 1th-order polynomial curve (flat line)? How about simply dropping the higher-order terms, so we get

and

? Here’s what they look like:

![](../../assets/851d2cd8d791fbe0.png)


At first glance, I’d say

and

are not what we want. We can definitely find a parabolic curve and a line that approximate

better. Look at just how far apart

and

are from

at

. Clearly,

and

are not the 2nd-order and 1st-order polynomial curves that have the least RMSEs from

. Simply dropping higher-order terms turns out to be a naive approach. The right way to do it is just like what we did with vectors: projection.

In the vector example above, we were operating in the 3D geometric space. Now we are working with a more abstract 3rd-order polynomial space where

lives in. The lower-order polynomial curve that has the least RMSE from

is the projection of

into that lower-order polynomial space. Let’s start with finding the 2nd-order polynomial curve that has the least RMSE from

.

The 2nd-order polynomial subspace is 3-dimensional, since a 2nd-order polynomial curve has the form

. Let’s first find 3 curves that span the subspace. An easy pick would be

,

, and

. Now we need to use them to generate a set of orthogonal curves,

,

, and

using the Gram-Schmidt process:

![Rendered by QuickLaTeX.com \begin{flalign*} k_0(t) &= j_0(t) \\ k_1(t) &= j_1(t) - proj(j_1(t), k_0(t)) \\ k_2(t) &= j_2(t) - proj(j_2(t), k_0(t)) - proj(j_2(t), k_1(t)) \\ \end{flalign*}](../../assets/42d86b9ea05f8f8b.png)


If you forgot how to “project” a curve onto another, please refer to the [previous post](http://allenchou.net/2017/01/projecting-a-curve-onto-another/).

Here are the results:

![Rendered by QuickLaTeX.com \begin{flalign*} k_0(t) &= 1 \\ k_1(t) &= \dfrac{-1}{2} + t \\ k_2(t) &= \dfrac{1}{6} - t + t^2 \\ \end{flalign*}](../../assets/654f7a16ebd4a8ea.png)


You can say that

,

, and

are a set of orthogonal axes spanning the 2nd-order polynomial subspace. Now we split

into three orthogonal parts by projecting it onto

,

, and

:

![Rendered by QuickLaTeX.com \begin{flalign*} s_0(t) &= proj(f(t), k_0(t)) = \dfrac{25}{12} \\ s_1(t) &= proj(f(t), k_1(t)) = \dfrac{-29}{10} + \dfrac{29}{20}t \\ s_2(t) &= proj(f(t), k_2(t)) = \dfrac{5}{12} - \dfrac{-5}{2}t + \dfrac{5}{2}t^2 \\ \end{flalign*}](../../assets/9224bda4950a5a8b.png)


Here’s what

,

, and

look like alongside

:

![](../../assets/af95cf8f831846f2.png)


![](../../assets/ed4db86059067494.png)


![](../../assets/895f4b2212144d68.png)



and

might not look like they are close to

, but they are the closest curves you can get along the axes

and

that have the least RMSEs from

.

Now, we can combine the three orthogonal parts of

to form the 2nd-order polynomial curve that is the best approximation of

:

![Rendered by QuickLaTeX.com \begin{flalign*} g(t) &= s_0(t) + s_1(t) + s_2(t) \\ &= \dfrac{21}{20} + \dfrac{2}{5}t + \dfrac{5}{2}t^2 \\ \end{flalign*}](../../assets/cbe26ca2738050e2.png)


![](../../assets/ae8e782860979e4a.png)


This looks way better than the result of simply dropping the 3rd-order term, as shown in the figure above.

Since the three parts are already orthogonal, we can actually obtain the 1st-order polynomial curve that best approximates

by simply dropping

from

:

![Rendered by QuickLaTeX.com \begin{flalign*} h(t) &= s_0(t) + s_1(t) \\ &= \dfrac{19}{30} + \dfrac{29}{10}t \\ \end{flalign*}](../../assets/e17b12cfc394c028.png)


![](../../assets/c238080fdaae315b.png)


Also looking good, compared to simply dropping the 3rd-order and 2nd-order terms.

That’s it. In this post, we’ve seen how to generate a set of orthogonal curves from a set of curves spanning a lower-dimensional subspace of curves, and use the orthogonal curves to find the best approximation of a curve via curve “projection”.

We now have all the tools we need to move onto Fourier transform and spherical harmonics in the next post. Finally, something game-related!

This is really great! 🙂 When we could expect the next part? I’m not trying to hurry you, I can imagine that writing on such topic is not an easy task (or at least not a quick task). I’m just wondering if you already scheduled the next part? Or is it postpone when you have more time?

It’s on my list. But there are other things going on right now, so it’s currently not my top priority.

I see. Thanks for the quick answer.