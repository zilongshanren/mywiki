---
title: The transcendence of e (part 2)
url: https://divisbyzero.com/2010/09/28/the-transcendence-of-e-part-2/
author: Dave Richeson
published: '2010-09-28'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

This is the second part in a 3-part blog post in which we prove that is transcendental.


**Three-step proof that is transcendental
**

[Step 1](https://divisbyzero.com/2010/09/28/the-transcendence-of-e/)


**Step 2**


[Step 3](https://divisbyzero.com/2010/09/28/the-transcendence-of-e-part-3/)

Recall that in [step 1] we proved the following lemma.

**Lemma 1.** Suppose is a root of the polynomial

. Let

be a polynomial and

. Then there exist

such that

, where

.


** Step 2.**

Now we are ready pick a specific polynomial for Lemma 1. Since there are infinitely many primes, we can find a prime number

greater than both

and

. Let


Our goal for this step is to show that is a nonzero integer. In fact we will show is that it is an integer not divisible by

, which implies that it is nonzero.


We will accomplish this by proving that for ,

(and hence

) is an integer divisible by

, but that

is an integer that is not divisible by

.


First we state but do not prove the following lemma. (This is a homework problem in Herstein.)

**Lemma 2.** If is a polynomial with integer coefficients and

, then for

,

is a polynomial with integer coefficients, each of which is divisible by

.


Applying Lemma 2 to our function we see that when

,

is a polynomial with integer coefficients, each of which is divisible by

. In particular, when

and

is any integer,

is an integer that is divisible by

.


Now let us restrict our attention to . From the definition of

we see that

is a root of

with multiplicity

. The following lemma tells us that

. (We leave the proof of this lemma as an exercise for the reader.)


**Lemma 3.** Suppose is a root of a polynomial

with multiplicity

. Then

for

.


So,



We know from above that each of the terms is an integer divisible by

. Thus

is an integer divisible by

.


Now let us consider . By the definition of

,

is a root with multiplicity

. By Lemma 3,

.


Thus,



From the result above, we know that are all divisible by

. What about

?


If we multiply out the terms in , we obtain


So,

and hence . Since

,

does not divide

. Therefore

does not divide

. Moreover,

, so

does not divide

. We conclude that

does not divide

.


Finally this implies that is an integer not divisible by

. In particular, it is a nonzero integer.


We are almost finished with the proof. In the [next step](https://divisbyzero.com/2010/09/28/the-transcendence-of-e-part-3/) we will show that , thus it cannot be a nonzero integer and we will obtain our sought-after contradiction.


Thanks for posting this, it’s very helpful. I have one question though, I know I’m being stupid but I can’t seem to prove lemma 2. I’d really appreciate any help on this. Thank you.

For simplicity, suppose

. Then

. Rewritten, the coefficient is

. Seen in this way, it is clearly an integer divisible by

.

Thanks a lot for your help, I really should have been able to work that out myself!

Sorry to bother you again, but I’ve been trying to prove that $e^{m/n}$ is transcendental, where $m>0$ and $n$ are integers (it’s an exercise in Herstein on p.178), but I’ve had no luck. Any help would be much appreciated. Thanks.