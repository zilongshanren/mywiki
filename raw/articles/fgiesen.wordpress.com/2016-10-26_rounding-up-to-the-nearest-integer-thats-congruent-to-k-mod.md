---
title: Rounding up to the nearest integer that’s congruent to k mod N
url: https://fgiesen.wordpress.com/2016/10/26/rounding-up-to-the-nearest-int-k-mod-n/
published: '2016-10-26'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Rounding up to the nearest integer that’s congruent to k mod N

It’s fairly well-known (among programmers anyway) that say rounding up x to the nearest multiple of 8 can be accomplished using the formula `(x + 7) & ~7`

, and that in general rounding up to the nearest multiple of N (where N is a power of 2) can be accomplished using `(x + N - 1) & ~(N - 1)`

. But sometimes you need a slightly generalized version: round up to the nearest value that is congruent to some ; for example, this crops up in boundary tag-using memory allocators when the user requests aligned memory. Such allocators put a header before allocated blocks (just before the address returned to the caller). For the user-visible pointer to be aligned by say 32, that header needs to fall at an address that’s

*off* alignment by a specified distance (which brings us to our problem).

It’s not immediately obvious how to adapt the original formula to this case (there is a way; I’ll get to it in a second). Now this is not exactly a frequent problem, nor is there any real need for a clever solution, but it turns out there is a very nice, satisfying solution anyway, and I wanted to write a few words about it. The solution is simply `x + ((k - x) & (N - 1))`

for power-of-2 N. The basic approach works in principle for arbitrary N, but `x + ((k - x) % N)`

will not work properly in environments using truncated division where taking the modulus of a negative argument can return negative results, which sadly is most of them. That said, in the remainder of this short post I’ll write `% N`

instead of `& (N - 1)`

with a “N needs to be a power of 2” disclaimer anyway, since there’s really nothing about the method that really requires it. Finally, this expression works fine even in overflowing unsigned integer arithmetic when N is a power of 2, but not for non-power-of-2 N.

What I like about this solution is that, once you see it written down, it’s fairly clear that and why it works (unlike many bit manipulation tricks), provided you know the rules of modular arithmetic: . We’re adding a non-negative value to x, so it’s clear that the result is ≥ x (provided there is no overflow). And we’re adding the smallest possible value we can to get to a value that’s congruent to k (mod N); I wrote about similar things before in my post

[“Intervals in modular arithmetic”](https://fgiesen.wordpress.com/2015/09/24/intervals-in-modular-arithmetic/).

There’s an equivalent expression for rounding down to the nearest value congruent to k (mod N): `x - ((x - k) % N)`

that works (and is easy to prove) the same way.

It’s interesting to consider the case k=0. The round-down variant, `x - (x % N)`

, feels fairly natural and is something I’ve seen in “real-world” code more than once. The round-up variant, `x + (-x % N)`

is something I’ve never seen anywhere. Once you throw the k in there, it all makes sense, but without it the expression looks quite odd.

Finally, here’s the aforementioned way to adapt the “regular” round-up formula to produce a value that’s congruent to k (instead of 0) mod N (and we’re back to requiring power-of-2 N here): `((x - k + N - 1) & ~(N - 1)) + k`

. This uses a different trick from the intervals in modular arithmetic paper: shift the origin around. In this case, we don’t have a formula for arbitrary k, but we do have a formula to round up to the nearest multiple of N. So we first subtract k; in this new shifted coordinate system, we want to round up to the next-larger multiple of N, which we know how to do. And finally, we add back k. It gets the job done, but it’s not as pretty as the other variant (in my opinion anyway), and it takes some thinking to convince yourself that it works at all.