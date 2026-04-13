---
title: A small note on SIMD matrix-vector multiplication
url: https://fgiesen.wordpress.com/2015/02/05/a-small-note-on-simd-matrix-vector-multiplication/
published: '2015-02-05'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# A small note on SIMD matrix-vector multiplication

Suppose we want to calculate a product between a 4×4 matrix M and a 4-element vector v:

The standard approach to computing Mv using SIMD instructions boils down to taking a linear combination of the four column vectors a, b, c and d, using standard SIMD componentwise addition, multiplication and broadcast shuffles.

// Given M as its four constituent column vectors a, b, c, d, // compute r=M*v. r = v.xxxx*a + v.yyyy*b + v.zzzz*c + v.wwww*d;

This computes the vector-matrix product using four shuffles, four (SIMD) multiplies, and three additions. This is all bog-standard. And if the ISA we’re working on has free broadcast swizzles (ARM NEON for example), we’re done. But if not, can we do better? Certainly if we know things about M or v: if M has a special structure, or some components of v are known to be always 0, 1 or -1, chances are good we can save a bit of work (whether it makes a difference is another matter). But what if M and v are completely general, and all we know is that we want to transform a lot of vectors with a single M? If v is either given as or returned in SoA form (structure-of-arrays), we can reduce the number of per-vector shuffles greatly if we’re willing to preprocess M a bit and have enough registers available. But let’s say we’re not doing that either: our input v is in packed form, and we want the results packed too. Is there anything we can do?

There’s no way to reduce the number of multiplies or additions in general, but we can get rid of exactly one shuffle per vector, if we’re willing to rearrange M a bit. The trick is to realize that we’re using each of v.x, v.y, v.z, and v.w exactly four times, and that the computations we’re doing (a bunch of component-wise multiplies and additions) are commutative and associative, so we can reorder them, in exact arithmetic anyway. (This type of computation is usually done in floating point, where we don’t actually have associativity, but I’m going to gloss over this.)

Let’s look at the our first set of products, `v.xxxx * a`

. We’re just walking down a column of M, multiplying each element we see by vx. What if we walk in a different direction? Going along horizontals turns out to be boring (it’s essentially the same, just transposed), but diagonals of M are interesting, the main diagonal in particular.

So here’s the punch line: we form four new vectors by walking along diagonals (with wrap-around) as follows:

Phrasing the matrix multiply in terms of these four vectors, we get:

r = v*e + v.yzwx*f + v.zwxy*g + v.wxyz*h;

Same number of multiplies and adds, but one shuffle per vector less (because the swizzle pattern for v in the first term is `xyzw`

, which is the natural ordering of v). Also note that forming e, f, g, and h given M in column vector form is also relatively cheap: it’s a matrix transposition with a few post-swizzles to implement the cyclic rotations. If you have M as row vectors (for example because it’s stored in row-major order), it’s even cheaper.

So: multiplying a packed 4-vector with a constant 4×4-matrix takes one shuffle less than the standard approach, if we’re willing to do some preprocessing on M (or store our matrices in a weird layout to begin with). Does this matter? It depends. On current desktop x86 cores, it’s pretty marginal, because SIMD shuffles can execute in parallel (during the same cycle) with additions and multiplications. On older cores with less execution resources, on in-order SIMD CPUs, and on low-power parts, it can definitely help though.

For what it’s worth: if your 4D vectors come from graphics or physics workloads and are actually homogeneous 3-vectors with a constant w=1 and no projective transforms anywhere in sight, you can exploit that structure explicitly for higher gains than this. But I ran into this with a DSP workload (with v just being a vector of 4 arbitrary samples), and in that case it’s definitely useful to know, especially since anything convolution-related tends to have highly diagonal ([Toeplitz](http://en.wikipedia.org/wiki/Toeplitz_matrix), to be precise) structure to begin with.

I found a way to efficiently retrieve diagonal vectors out of a matrix with SIMD:

http://stackoverflow.com/questions/15198011/how-to-load-a-sliding-diagonal-vector-from-data-stored-column-wise-withsse/15198012#15198012

If your matrix M, would have been much bigger than 4×4, maybe your matrix – vector multiplication algorithm could have benefited from being used together with my diagonal loader algorithm?