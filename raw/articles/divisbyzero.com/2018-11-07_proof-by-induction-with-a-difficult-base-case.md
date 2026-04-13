---
title: Proof by Induction with a Difficult Base Case
url: https://divisbyzero.com/2018/11/07/proof-by-induction-with-a-difficult-base-case/
author: Dave Richeson
published: '2018-11-07'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I’m teaching Discrete Mathematics this semester. It is our “intro to proofs” class. One of the proof techniques the students learn is proof by induction. I told the class that usually the base case for induction proofs are easy and that most of the work occurs in the inductive step. Indeed, most of the proofs that they see have base cases that are elementary to check (performing elementary calculations to conclude that 1=1, for instance). I warned them that this was not always the case. Sometimes the base case is the most difficult part of the induction proof.

I spent a while thinking about an example I could show them where this is the case. I found this [Math Overflow link on this same question](https://math.stackexchange.com/questions/43007/what-are-some-examples-of-induction-where-the-base-case-is-difficult-but-the-ind/43010). They gave a few examples. Here’s one of them—the multi-function product rule for derivatives. The base case requires using the definitions of continuity and differentiability and the theorem that every function differentiable at a point is continuous at the point. It is not a simple “1=1” base case. The inductive step is much easier, although it is still not totally trivial because it requires using both the base case and the inductive hypothesis.

**Theorem.** *Let be at least two functions that are differentiable at some point . Then *

**Proof. **This is a proof by induction on Let

be the statement that given

differentiable functions

it follows that


Base case: Let

and

be differentiable at

Recall that because

is differentiable at

it is continuous at

Then


The penultimate equality follows from the continuity of at

and the final equality follows from the differentiability of

and

at

Thus

holds.


Inductive step. Suppose holds for some integer

Let

be functions that are differentiable at some point

. Then

By the base case, this equals

By the inductive assumption, this equals


Thus, holds.


It follows that holds for all

#


If you have another example—especially one that would be suitable for into-to-proof students (who don’t have an extensive math background)—post them in the comments.

You could do much the same thing for DeMorgan’s law (either the set-theoretic or propositional logic versions). Assuming the base case is at n=2.

Good point. That would fit within the subject matter better than the calculus theorem. (On the flip side, the base case wouldn’t be quite as messy/deep as the base case is here).