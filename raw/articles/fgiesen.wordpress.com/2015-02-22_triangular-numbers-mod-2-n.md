---
title: Triangular numbers mod 2^n
url: https://fgiesen.wordpress.com/2015/02/22/triangular-numbers-mod-2n/
published: '2015-02-22'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Triangular numbers mod 2^n

are a standard sequence used in [quadratic probing](http://en.wikipedia.org/wiki/Quadratic_probing) of [open hash tables](http://en.wikipedia.org/wiki/Hash_table#Open_addressing). For example, they’re [used](http://goog-sparsehash.sourceforge.net/doc/implementation.html) in Google’s `sparse_hash`

and `dense_hash`

, generally considered to be very competitive hash table implementations.

You can find lots of places on the web mentioning that the resulting probe sequence will visit every element of a power-of-2 sized hash table exactly once; more precisely, the function is a permutation on

. But it’s pretty hard to find a proof; everybody seems to refer back to Knuth, and in The Art of Compute Programming, Volume 3, Chapter 6.4, the proof appears as an exercise (number 20 in the Second Edition).


If you want to do this exercise yourself, please stop reading now; spoilers ahead!

Anyway, turns out I arrived at the solution very differently from Knuth. His proof is much shorter and slicker, but pretty “magic” and unmotivated, so let’s take the scenic route! The first step is to look at a bunch of small values and see if we can spot any patterns.

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
Tk |
0 | 1 | 3 | 6 | 10 | 15 | 21 | 28 | 36 | 45 | 55 | 66 |
Tk mod 8 |
0 | 1 | 3 | 6 | 2 | 7 | 5 | 4 | 4 | 5 | 7 | 2 |
Tk mod 4 |
0 | 1 | 3 | 2 | 2 | 3 | 1 | 0 | 0 | 1 | 3 | 2 |
Tk mod 2 |
0 | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0 |

And indeed, there are several patterns that might be useful: looking at the row for “mod 2”, we see that it seems to be just the values 0, 1, 1, 0 repeating, and that sequence itself is just 0, 1 followed by its reverse. The row for “mod 4” likewise looks like it’s just alternating between normal and reverse copies of 0, 1, 3, 2, and the “mod 8” row certainly looks like it might be following a similar pattern. Can we prove this?

First, the mirroring suggests that it might be worthwhile to look at the differences





Both terms are multiples of n, so we have , which proves the mirroring (incidentally, for any n, not just powers of 2). Furthermore, the first term is a multiple of 2n too, and the second term

*almost* is: we have . This will come in handy soon.


To prove that is 2n-periodic, first note the standard identity for triangular numbers




in particular, we have

Again, this is for arbitrary n ≥ 1. So far, we’ve proven that for arbitrary positive integer n, the sequence is 2n-periodic, with the second half being a mirrored copy of the first half. It turns out that we can wrangle this one fact into a complete proof of the

, 0 ≤ k < 2

m being a permutation fairly easily by using induction:

**Basis** (m=0): , and the function

is a permutation on { 0 }.


**Inductive step**: Suppose is a permutation on

. Then the values of

must surely be pairwise distinct for 0 ≤ k < 2

m, since they’re already distinct mod 2m. That means we only have to deal with the second half. But above (taking n=2m), we proved that

and letting k run from 0 to 2m-1, we notice that mod 2m, these values are congruent to the values in the first half, but mod 2m+1, they differ by an additional term of -n. This implies that the values in the second half are pairwise distinct both from the first half and from each other. This proves that fm+1 is injective, and because it’s mapping the 2m+1-element set onto itself, it must be a permutation.


Which, by mathematical induction, proves our claim.

To motivate Knuth’s proof you can think about why there can’t be any triangular number other than $T_n$ that’s congruent to $T_n$ mod $2^m$ for $n \in [0..2^m-1]$. If there were then $f(k)$ wouldn’t be a bijection. The inverse of $f(k)$ is to find the smallest (really, the only) $k + a2^m$ with $a$ non-negative that is a triangular number, then find the index of that triangular number by quadratic formula. If there were another $T_n$ congruent to $k$ mod $2^m$ then you’d have $k$ corresponding to two $T_n$’s (two values of $a$ that work) and you wouldn’t have a bijection. Knuth’s restriction that $j = k$ preserves the bijection. Since it’s a bijection and the domain is $[0..2^m-1]$, it’s also a permutation.

(I hope the latex works in comments.)

The LaTeX doesn’t even work that way in the main text, sorry. (You need extra markup)