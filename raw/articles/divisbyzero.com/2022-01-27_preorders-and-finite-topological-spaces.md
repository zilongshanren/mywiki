---
title: Preorders and Finite Topological Spaces
url: https://divisbyzero.com/2022/01/27/preorders-and-finite-topological-spaces/
author: Dave Richeson
published: '2022-01-27'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Today I tweeted that I had asked my topology students to find all of the different topologies of a two-point set and a three-point set. It turns out that there are three of the former and nine of the latter. (The sequence of the number of topologies for an *n*-point set begins 1 (for ), 3 (

), 9 (

), 33, 139, 718, 4535, 35979, 363083, 4717687, 79501654, 1744252509, 49872339897, 1856792610995, 89847422244493, 5637294117525695,… and is

[sequence A001930 in the OEIS](https://oeis.org/A001930).)

Akiva Weinberger ([@akivaw](https://twitter.com/akivaw)) tweeted back to me saying that this is the same number of “preorders” on a set with *n *elements. I admitted that I’d never heard of a preorder. Then he and Joel David Hamkins ([@jdhamkins](https://twitter.com/JDHamkins)) filled me in on what a preordered set is.

It found it to be pretty cool—especially the connection to topologies of finite sets. So I thought I’d share it here on my blog.

**TOTAL ORDERS, PARTIAL ORDERS, AND PREORDERS**

We are all familiar with sets that are *totally ordered* (like the integers or the real numbers). A set *S* is totally ordered with a relation ≤ if it has the following properties for all elements in *S*.

*Reflexivity*:*Transitivity*: ifand

then

*Antisymmetry*: ifand

then

*Comparability*: eitheror

(or both).


A set *S *with and relation ≤ that satisfies properties 1–3 (it is reflexive, transitive, and antisymmetric), but not necessarily property 4, is called a *partially ordered set*. For instance, we can put a partial order ≤ on the set of positive integers as follows. We’ll say that

provided

*a *divides *b. *Using this ordering, we have and

because both 2 and 3 divide 6. However, not all positive integers are comparable. For instance,

and

because 5 doesn’t divide 6 and 6 does not divide 5. So this relation gives a partial order and not a total order of the positive integers.


Now we are ready to talk about preordered sets. A relation ≤ gives a *preorder* on a set *S * provided it satisfies properties 1 and 2 (it is reflexive and transitive) but not necessarily properties 3 and 4. If we extend the divisibility relation to the full set of integers, we get a preorder that is not a partial order. The ordering is reflexive and transitive, but it is not antisymmetric. For example, because –2 divides 2,

and since 2 divides –2,

However,


One way to think about preorders is via *directed graphs* (mathematical graphs in which edges have a direction). Define a relation ≤ on the vertices of the graph as follows. We say that provided

*a *is *reachable *from *b*; that is, we can get from *b* to *a* along a path of directed edges (including the trivial path of not going anywhere).

For instance, the graph below has vertex set We see that

because we can get from vertex

*a *to vertex *e*. It is not too difficult to see that the relation is reflexive and transitive. However, notice that we can’t get from vertex *b *to vertex *e *nor from *e *to *b*, so they are incomparable (that is, property 4 fails). But also we have and

but

so the relation is not antisymmetric (property 3 fails). Thus, the relation is a preorder.


**TOPOLOGIES OF FINITE SETS**

Let’s see how preorders are related to the topologies of finite sets. First, let’s give the definition of a topology.

Let *X* be a set. A set of subsets of *X*, *T*, is a *topology* for *X* provided.

- The intersection of any finite number of sets in
*T*is in*T*. - The union of any collection (finite or infinite) of sets in
*T*is in*T*.

The sets in *T *are called *open sets.*

So, for instance, the three-point set has nine different topologies. (By “different” we mean that any other topology can be obtained from one of these just by renaming the letters

*a, b, *and* c.* Or, using more technical terminology, any other topology is homeomorphic to one of these.)

Given a topology *T* for a finite set *X* we can obtain a preorder on *X *as follows. We say that provided

*x *belongs to every open set that contains *y*.

So, the topology on the set

gives a preorder in which we can only say

and

Similarly, the topology

on the set

gives a preorder in which we can only say

and

The following graphs give the same preorders.


Notice that with respect to topology the so-called

*trivial topology*, we have all six relations




and

And with respect to

the so-called

*discrete topology*, none of the elements are comparable.

We can go the other way as well. Given a preorder of a finite a set *X*, we can produce a topology on the set *X* as follows. A set is an open set provided there is no element in

*X *that is less than any element in *U.* For instance, suppose we had the preorder corresponding to the graph with vertices at the beginning of the blog post. Then a set of vertices is an open set if there are no directed edges that point out of the set. In particular, the preorder corresponding to the graph gives topology


Pretty cool!

The following 1985 Math. Mag. paper is where I first heard about the correspondence between preorders and finite topologies (your students are lucky…unlike you and me, they got to hear about it in topology class!):

https://www.jstor.org/stable/2689890?origin=JSTOR-pdf

Also note:

1. A finite topological space is T_0 if and only if its corresponding preorder is a partial order.

2. Another name for preorder is quasiorder.

3. The definitive paper listed with sequence A001930 is the 2005 one by Brinkmann and McKay:

Click to access topologies.pdf

4. With help from McKay, last year I posted lists of all nonhomeomorphic finite topologies up to cardinality 11:

https://mathtransit.com/finite_topological_spaces.php

My Macbook Pro generally takes about ten days to go through the full list of 11-spaces. It’ll be a while before all 12-spaces can be tested on a home computer.