---
title: Editing a Very Poorly Written Proof
url: https://divisbyzero.com/2015/10/10/editing-a-very-poorly-written-proof/
author: Dave Richeson
published: '2015-10-10'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I’m teaching Discrete Math this semester. Discrete Math is our college’s “introduction to proofs” class. We spend a lot of time talking about and practicing proofwriting. In earlier blog posts I shared my “[Nuts and Bolts of Writing Mathematics](https://divisbyzero.com/2009/09/17/the-nuts-and-bolts-of-writing-mathematics-2/)” and an “[editing checklist](https://divisbyzero.com/2013/02/10/editing-mathematical-writing/)” that I give to them.

Yesterday, I gave them an example of a very, very poorly written proof that I created. (It was fun trying to insert as many problems as I could into the short proof!) I had them work on the assignment in class for about 7 minutes. Then we came together and talked about all the errors that we could find, and finally we rewrote the proof in the correct way. Here’s a [pdf of the assignment](http://users.dickinson.edu/~richesod/badwriting2.pdf), and I’ve posted a screenshot below.

In case you are wondering, here are the errors in the proof. Numbers refer to sentence numbers.

- The proof should be begin immediately after the word PROOF.
- The entire proof should be written in paragraph form.
- 1. Capitalize the first word of the sentence.
- 1. Split this sentence in two: The first sentence should be “Let
*m*be an odd integer and*n*be an even integer.” In the second sentence we apply the definition of even and odd. - 1. Do not use
*k*for both the even and the odd numbers. - 1. Don’t use a symbol (#) in place of a word.
- 2. Start the sentence with a word, not a mathematical expression.
- 2. The correct expression is
*mn*2, not*m*2*n*. - 2. “Equivalent to” is a term we use for logical expressions, not numbers. It should be “equal to”—and in fact, we should just use “=.”
- 2. Algebra error: the term 8
*k*should be 8*k*2. - 2. In a 200-level math class we do not have to show all of these algebraic details.
- 3. This is not how we show that a number is even—we must show that
*mn*2satisfies the definition of even. - 3. Do not use the word “obviously.”
- 3. In a proof like this we’d have to show that the three terms satisfy the definition of even.
- 3. “There” should be “their.”
- 3. Missing dollar signs around 2
*k*in the LaTeX code. - 4. Do not use the passive voice.
- 4. Missing period at the end of the sentence.
- 4. and 5. Write in present tense.
- 5. Do not put an example in a proof.
- 5. There are missing dollar signs in the LaTeX : after
*m*=5 and before*n*=4. - 5. It should be first person plural, not first person singular (“we” not “I”).
- 5. Replace “is = to” with “=.”

Here is our corrected proof:

> “Equivalent to” is a term we use for logical expressions, not numbers.

Let x be an element of Zmod4. Let Y be x + 4. Note that y is equivalent to x.

I think ‘equivalent’ is the correct word to describe any relation that is symmetrical, transitive and reflexive.

OK, I should have said “In this course ‘equivalent to’ is a term we use for logical expression, not numbers.” Students often use “equal to” and “equivalent to” interchangeably, which they shouldn’t. I think they think “equivalent” is a fancier way of saying “equal.”

By convention, although equality is (trivially) an equivalence relation, the term equivalent is usually reserved for non-trivial relations.

Also, if x is an element of Z mod 4, then x + 4 is not defined (since 4 is a number not an equivalence class mod 4. If you meant the equivalence class of 4 instead, then by the definition of modular arithmetic, y =x and the think you mean to say that if

I would probably avoid ‘l’ in such a write-up (and if you are in LaTeX then at least use $\ell$?). In this particular case, I probably would’ve started with a & b, and then re-written them as 2m+1 & 2n.

More deeply, though it may not be especially relevant for your present purpose: I think the fundamental insight here is that the product of an even integer & any other integer is even. (Proof: Write the former as 2m and the latter as n; then their product is 2mn, which is an integer multiple of 2, i.e., even.)

Corollary: Any even squared is even.

Corollary to corollary: Your original Theorem.

I expect that for these students the corollaries should actually have their proofs written out, which would make the entire endeavor a bit verbose. Still, I think an important part of proof-writing is looking for insights that arise and using those to refine one’s work.

In the case of your Theorem, the result follows because you end up with an integer that is a multiple of 2; well, where did that 2 come from? Etc.

This is just what I have been looking for…I’m currently teaching students who want to study Maths at University and need to do the Cambridge STEP Papers…but they are so reluctant to lay their proofs out properly or even just use a few words of English to explain their argument. I will direct them to this post!

How did your students respond to the excercise>

The first thing I noticed seems not to be mentioned anywhere, although I might have missed it. The definitions classify “integers” while the theorem is about “numbers”.