---
title: Goodstein’s unprovable theorem
url: https://divisbyzero.com/2010/08/16/goodsteins-unprovable-theorem/
author: Dave Richeson
published: '2010-08-16'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Recently I learned about a family of sequences of nonnegative integers (called Goodstein sequences) and two remarkable theorems about these sequences.

Begin with any positive integer . This is the first term in the sequence. For example, suppose we begin with

.


The first step in computing the second term of the sequence, , is to write

in

[ hereditary base 2 notation](http://mathworld.wolfram.com/HereditaryRepresentation.html). That is, write

To obtain we change all of the 2’s to 3’s, then subtract 1. For our example,

. Notice that

is very large number; it is approximately


We continue in the same way. We obtain from

by writing

in hereditary base

notation, changing all of the

‘s to

‘s, and subtracting 1.


To obtain we must express

in hereditary base 6 notation. First notice that


(An easy way to see this is that written in base 6, is

, 1 followed by

zeros. So

is

,

fives.) But this expansion of

is not in hereditary base 6 notation yet. We must express the towers of exponents in base 6, etc. When that is done, we replace the 6’s with 7’s and subtract 1. In the end,

is a gigantic number.


Now here are two amazing theorems about this sequence of integers. In 1944 [Reuben Goodstein proved](http://en.wikipedia.org/wiki/Goodstein's_theorem):

**Theorem.** There is a such that

.


That is, this sequence, which looks like it is rocketing to infinity, will eventually become zero and terminate. Wow! The proof of this theorem is very sophisticated and uses the theory of [ordinal numbers](http://en.wikipedia.org/wiki/Ordinal_number).

I’ll have to file this sequence away as an example that shows why we can’t use the behavior of the first few (or first few million) terms of a sequence to determine the limiting behavior of a sequence.

Then, in 1982 Laurie Kirby and Jeff Paris proved the following theorem.

**Theorem.** Goodstein’s Theorem is not provable using the Peano axioms of arithmetic.

In other words, this is exactly the type of theorem described in 1931 by [Gödel’s first incompleteness theorem](http://en.wikipedia.org/wiki/Gödel's_incompleteness_theorems)!

Recall what Gödel’s theorem says. If there is an axiomatic that is rich enough to express all elementary arithmetic (such as that formed from the [Peano axioms](http://en.wikipedia.org/wiki/Peano_axioms)), then it must be incomplete. In other words, there must be a true statement about arithmetic that cannot be proven from the axioms. In his proof Gödel produces an explicit example of a true, but unprovable statement. But it is complicated to grasp and more reminiscent of a logical paradox than a mathematical statement.

The first nice mathematical example of such a statement was presented in 1977 by [Paris and Harrington](http://en.wikipedia.org/wiki/Paris-Harrington_theorem) (in a field called Ramsey theory). Then in 1982 Kirby and Paris proved that Goodstein’s theorem was unprovable and they gave another elementary example, called “Hercules versus the hydra,” which relates to the growth of the hydra (a tree) and its destruction by Hercules.

“In other words, this is exactly the type of theorem predicted in 1931 by Gödel’s first incompleteness theorem!”

Heuristic correction: Godel didn’t “predict” unprovable theorems, he PRESENTED A RECIPE to generate lots and lots of unprovable theorems.

It’s possible by that word “predicted” you were gesturing toward the common noob complaint “but those aren’t “real” or “natural” theorems! they’re so contrived!”. If that’s the issue, then whatever. Theorems are theorems.

Math doesn’t discriminate against its theorems – only mathematicians do. And in the case of Godelian issues, typically only those mathematicians who don’t much bother with “fringe” maths.

Great post! The summer is a good time to be one of your blog readers.

@sherifffruitfly I don’t understand the distinction you are making. Correct me if I’m wrong, but while Godel’s first incompleteness theorem proved the existence of such theorems and provided examples, it certainly did not enumerate the ways to construct all such theorems.

Therefore one could certainly say that Goodstein’s theorem “is exactly the type of theorem **described** in 1931 by Gödel’s first incompleteness theorem.” Checking the etymology of “predict” (and our intuitive sense of the word) “describing in advance” is a reasonable definition, which is exactly the sense in which it was used.

Don’t be so hasty!

Thanks for the kind words Brendan! @sherifffruitfly I see what you’re saying that “predicted” probably isn’t the best word choice, although I don’t think it is as bad as you do—I like Brendan’s suggestion of “described.”

Very nice – I have been thinking about unprovable theorems a bit, as I recently wrote an article about recent progress in the field: http://www.newscientist.com/article/mg20727731.300-to-infinity-and-beyond-the-struggle-to-save-arithmetic.html?full=true

The lexicon of ‘concrete’ unprovable theorems is more well developed than one might expect. See e.g 48. Unprovable theorems, here:

http://www.math.ohio-state.edu/~friedman/manuscripts.html

Fast growing sequences and gigantic numbers play a prominent role. Another very striking example is H. Friedman’s (again!) finite version of Kruskal’s theorem on trees:

http://en.wikipedia.org/wiki/Kruskal%27s_tree_theorem

I *meant* to link to your New Scientist article in my blog post—sorry about that. I read your article yesterday and saw the blurb about the Paris/Harrington theorem at theend—it was the first time I’d seen that. It is fascinating. I’m no expert on any of this, but I’ve read all or part of 4 or 5 books on Russell, Gödel, etc. in the last few months. So your article really caught my attention. Thanks.

How does 3^3^3 + 3^3^0 become 6.63 * 10^12 ????

The only way I can get 6.63 * 10^X is by cubing 3 seven times :

3^3^3^3^3^3^3 = 6.628 * 10^347

What’s wrong?

Thanks for catching that typo. It should have been

, not

. I fixed it.

The link to Gödel’s first incompleteness theorem needs correcting.

Thanks. My blog editor apparently didn’t like the “ö” in the url.

I don’t understand. If there exists a k such that m_k=0, then there should be a trivial proof. All you need to do compute each m_n until you reach m_k=0. Since k exists, this computation will take finite time, and your proof will be of finite length and won’t do anything beyond simple computation.

Sure it’ll take a long time, and we don’t know what the proof will be, but it seems clear that such a proof exists.

If the theorem is true, the only way I can see it being unprovable using the Peano axioms of arithmetic is if you can’t compute m_(n+1) from m_(n) using the Peano axioms of arithmetic, which would mean you can’t even prove what m_2 is.

Okay, I misunderstood the problem.

The theorem says that for all m_1 there exists a k such that m_k = 0, not just that if m_1 = 18 there exists a k such that m_k = 0.

It’s things like this that drive me to want to continue studying mathematics at the graduate level, so I can understand and grasp these proofs. Is either proof particularly elegant or beautiful?