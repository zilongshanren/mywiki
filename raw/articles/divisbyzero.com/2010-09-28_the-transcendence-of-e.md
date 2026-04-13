---
title: The transcendence of e
url: https://divisbyzero.com/2010/09/28/the-transcendence-of-e/
author: Dave Richeson
published: '2010-09-28'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

A real number is called

[ algebraic](http://en.wikipedia.org/wiki/Algebraic_number) if it is the root of a polynomial with integer coefficients. Examples of algebraic numbers are

[golden ratio](http://en.wikipedia.org/wiki/Golden_ratio)(

[cannot be expressed with radicals](http://en.wikipedia.org/wiki/Quintic)).

A real number that is not algebraic is called [ transcendental](http://en.wikipedia.org/wiki/Transcendental_number). It is easy to see that every transcendental number is irrational, but, as we see above, not every irrational number is transcendental. In 1874

[Georg Cantor](http://www-groups.dcs.st-and.ac.uk/~history/Biographies/Cantor.html)proved that there are only countably many algebraic numbers. Thus there must be uncountably many transcendental numbers! The vast, vast majority of real numbers are transcendental.

Despite the fact that almost every real number is transcendental, it is very difficult to prove that a given number is transcendental. [Joseph Liouville](http://www-history.mcs.st-and.ac.uk/Biographies/Liouville.html) discovered the first transcendental number in 1844:

In 1873 [Charles Hermite](http://www-history.mcs.st-and.ac.uk/Biographies/Hermite.html) proved that is transcendental and nine years later

[Ferdinand von Lindemann](http://www-history.mcs.st-and.ac.uk/Biographies/Lindemann.html) proved that is transcendental. Some other transcendental numbers are:

(we have not yet proved that

is transcendental),

,

,

, and

(yes, this is a real number:

).


In this sequence of three blog posts I will prove that is transcendental. At a glance the proof looks long and complicated, but the proof is really quite straightforward (this post is the longest of the three). Most of the proof is nothing more than algebraic manipulations and divisibility arguments with integers. There is some differential calculus, but nothing beyond Calculus I: the mean value theorem, the derivative of

the product rule, and the limit

. The proof also uses the infinitude of primes.


This proof is based on [Adolf Hurwitz](http://www-history.mcs.st-and.ac.uk/Biographies/Hurwitz.html)‘s 1893 simplification of Hermite’s proof. (To be specific, I used Herstein’s *Topics in Algebra* as a source for the details of Hurwitz’s proof.)

**Three-step proof that is transcendental
Step 1**

[Step 2](https://divisbyzero.com/2010/09/28/the-transcendence-of-e-part-2/)


[Step 3](https://divisbyzero.com/2010/09/28/the-transcendence-of-e-part-3/)

**Theorem.** is transcendental.


This is a proof by contradiction. Suppose is algebraic. That is,

is the root of a polynomial

with integer coefficients. In other words,


We may assume that . (If

is zero divide

by

, or a sufficiently large power of

; if

, multiply

by

.)


* Step 1.*

In this first post we will prove the following lemma. We use the familiar notation that is the

th derivative of

(and

).


**Lemma 1.** Suppose is a root of the polynomial

. Let

be a polynomial and

. Then there exist

such that

, where

.


Suppose is a polynomial of degree

with real coefficients. Then

. In particular, the function

is a finite sum:


Notice that the derivative of has the following simple form





Define a new function . The derivative of

also has a compact form. Using the product rule we obtain





At this point we must invoke the mean value theorem.

**Theorem.** [Mean value theorem] Suppose is a differentiable function and

. Then there exists

such that

.


Since the number is between

and

, we can write it as

where

. Thus we may restate the theorem as follows.


**Theorem.** [Mean value theorem (vers. 2)] Suppose is a differentiable function and

. Then there exists

such that

.


The function is differentiable, so we may apply the mean value theorem to the interval

(

,

). It guarantees

such that


Using the definition of and our expression for

this equality becomes


A little algebra yields the following equality (we will call this common value ).


We now repeat this for all of the intervals for

, where

is the degree of the polynomial

for which

. Each application of the mean value theorem yields its own

and its own corresponding

:


Multiply the left and right sides of this equality by (the

th coefficient of

) to obtain


Summing these equation for we obtain


But, since , we know that

. So the equality simplifies to


This proves the lemma.

In the [next step](https://divisbyzero.com/2010/09/28/the-transcendence-of-e-part-2/) we will choose a specific polynomial for the lemma.


## 2 Comments

Comments are closed.