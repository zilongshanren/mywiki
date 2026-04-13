---
title: Bink 2.2 integer DCT design, part 2
url: https://fgiesen.wordpress.com/2013/11/10/bink-2-2-integer-dct-design-part-2/
published: '2013-11-10'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Bink 2.2 integer DCT design, part 2

[Last time](https://fgiesen.wordpress.com/2013/11/04/bink-2-2-integer-dct-design-part-1/), I talked about DCTs in general and how the core problem in designing integer DCTs are the rotations. However, I promised an 8×8 IDCT that is suitable for SIMD implementation using 16-bit integer arithmetic without multiplies, and we’re not there yet. I’m going to be focusing on the “B2” variant of the transform in this post, for concreteness. That means the starting point will be [this implementation](https://github.com/rygorous/dct_blog/blob/master/bink_dct_approx.m), which is just a scaled version of Plonka’s DCT factorization with the rotation approximations discussed last time.

### Normalization

The DCT described last time (and implemented with the Matlab/Octave code above) is a scaled DCT, and I didn’t mention the scale factors last time. However, they’re easy enough to solve for. We have a forward transform matrix, . Since the rows are orthogonal (by construction), the inverse of

(and hence our IDCT) is its transpose, up to scaling. We can write this as matrix equation

where S ought to be a diagonal matrix. Solving for S yields

. This gives the total scaling when multiplying by both

and

; what we really want is a normalizing diagonal matrix

such that

is orthogonal, which means


since N is diagonal, so , and again because the two are diagonal this just means that the diagonal entries of N are the square roots of the diagonal entries of S. Then we multiply once by N just before quantization on the encoder side, and another time by N just after dequantization on the decoder side. In practice, this scaling can be folded directly into the quantization/dequantization process, but conceptually they’re distinct steps.


This normalization is the right one to use to compare against the “proper” orthogonal DCT-II. That said, with a non-lifting all-integer transform, normalizing to unit gain is a bad idea; we actually *want* some gain to reduce round-off error. A good compromise is to normalize everything to the gain of the DC coefficient, which is for the 1D transform. Using this normalization ensures that DC, which usually contains a significant amount of the overall energy, is not subject to scaling-induced round-off error and thus reproduced exactly.


In the 2D transform, each coefficient takes part in first a column DCT and then a row DCT (or vice versa). That means the gain of a separable 2D 8×8 DCT is the square of the gain for the 1D DCT, which in our case means 8. And since the IDCT is just the transpose of the DCT, it has the same gain, so following up the 2D DCT with the corresponding 2D IDCT introduces another 8x gain increase, bringing the total gain for the transform → normalize → inverse transform chain up to 64.

Well, the input to the DCT in a video codec is the difference between the actual pixel values and the prediction (usually motion compensation or some geometric/gradient predictor), and with 8-bit input signals that means the input is the difference between two values in [0, 255]. The worst cases are when the predicted value is 0 and the actual value is 255 or vice versa, leading to a worst-case input value range of [-255, 255] for our integer DCT. Multiply this by a gain factor of 64 and you get [-16320, 16320]. Considering that the plan is to have a 16-bit integer implementation, this should make it obvious what the problem is: it all fits, but only just, and we have to be *really* careful about overflow and value ranges.

### Dynamic range

This all falls under the umbrella term of the dynamic range of the transform. The smallest representable non-zero sample values we support are ±1. With 16-bit integer, the largest values we can support are ±32767; -32768 is out since there’s no corresponding positive value. The ratio between the two is the total dynamic range we have to work with. For transforms, it’s customary to define the dynamic range relative to the input value range, not the smallest representable non-zero signal; in our case, the maximum total scaling we can tolerate along any signal path is 32767/255, or about 128.498; anything larger and we might get overflows.

Now, this problem might seem like it’s self-made: as described above, both the forward and inverse transforms have a total gain of 8x, which seems wasteful. Why don’t we, say, leave the 8x gain on the forward transform but try to normalize the inverse transform such that it doesn’t have any extra gain?

Well, yes and no. We can, but it’s addressing the wrong part of the problem. The figures I’ve been quoting so far are for the gain as measured in the 2-norm (Euclidean norm). But for dynamic range analysis, what we need to know is the infinity norm (aka [“uniform norm”](http://en.wikipedia.org/wiki/Uniform_norm) or “maximum norm”): what is the largest absolute value we’re going to encounter in our vectors? And it turns out that with respect to the infinity norm, the picture looks a bit different.

To see why, let’s start with a toy example. Say we just have two samples, and our transform is a single butterfly:

As covered last time, B is a scaled reflection, its own inverse up to said scaling, and its matrix 2-norm is . However, B’s infinity-norm is 2. For example, the input vector

(maximum value of 1) maps to

(maximum value of 2) under B. In other words, if we add (or subtract) two numbers, we might get a number back that is up to twice as big as either of the inputs – this shouldn’t come as a surprise. Now let’s apply the transpose of B, which happens to be B itself:


This is just a scaled identity transform, and its 2-norm and infinity norm are 2 exactly. In other words, the 2-norm grew in the second application of B, but with respect to the infinity norm, things were already as bad as they were going to get after the forward transform. And it’s this infinity norm that we need to worry about if we want to avoid overflows.

### Scaling along the signal path

So what’s our actual matrix norms along the signal path, with the “B2” DCT variant from last time? This is why I published the Octave code on [Github](https://github.com/rygorous/dct_blog). Let’s work through the 1D DCT first:

2> M=bink_dct_B2(eye(8)); 3> S=diag(8 ./ diag(M*M')); 4> norm(M,2) ans = 3.4324 5> norm(M,'inf') ans = 8.7500 6> norm(S*M,2) ans = 3.2962 7> norm(S*M,'inf') ans = 8.4881 8> norm(M'*S*M,2) ans = 8.0000 9> norm(M'*S*M,'inf') ans = 8.0000

This gives both the 2-norms and infinity norms for first the forward DCT only (`M`

), then forward DCT followed by scaling (`S*M`

), and finally with the inverse transform as well (`M'*S*M`

), although at that point it’s really just a scaled identity matrix so the result isn’t particularly interesting. We can do the same thing with 2D transforms using `kron`

which computes the [Kronecker product](http://en.wikipedia.org/wiki/Kronecker_product) of two matrices (corresponding to the tensor product of linear maps, which is the mathematical background underlying separable transforms):

10> norm(kron(M,M),'inf') ans = 76.563 11> norm(kron(S,S) * kron(M,M),2) ans = 10.865 12> norm(kron(S,S) * kron(M,M),'inf') ans = 72.047 13> norm(kron(M',M') * kron(S,S) * kron(M,M), 2) ans = 64.000 14> norm(kron(M',M') * kron(S,S) * kron(M,M), 'inf') ans = 64.000 15> norm(kron(M',M') * kron(S,S) * kron(M,M) - 64*eye(64), 'inf') ans = 8.5487e-014 16> 64*eps ans = 1.4211e-014

As you can see, the situation is very similar to what we saw in the butterfly example: while the 2-norm keeps growing throughout the entire process, the infinity norm actually maxes out right after the forward transform and stays roughly at the same level afterwards. The last two lines are just there to show that the entire 2D transform chain really does come out to be a scaled identity transform, to within a bit more than 6 ulps.

More importantly however, we do see a gain factor of around 76.6 right after the forward transform, and the inverse transform starts out with a total gain around 72; remember that this value has to be less than 128 for us to be able to do the transform using 16-bit integer arithmetic. As said before, it can fit, but it’s a close shave; we have less than 1 bit of headroom, so we need to be really careful about overflow – there’s no margin for sloppiness. And furthermore, while this means that the *entire transform* fits inside 16 bits, what we really need to make sure is that the way we’re computing it is free of overflows; we need to drill down a bit further.

For this, it helps to have a direct implementation of the DCT and IDCT; a direct implementation (still in Octave) for the DCT is [here](https://github.com/rygorous/dct_blog/blob/master/bink_dct_B2.m), and I’ve also checked in a [direct IDCT](https://github.com/rygorous/dct_blog/blob/master/bink_idct_B2_partial.m) taking an extra parameter that determines how many stages of the IDCT to compute. A “stage” is a set of mutually independent butterflies or rotations that may depend on previous stages (corresponding to “clean breaks” in a butterfly diagram or the various matrix factors in a matrix decomposition).

I’m not going to quote the entire code (it’s not very long, but there’s no point), but here’s a small snippet to show what’s going on:

% odd stage 4 c4 = d4; c5 = d5 + d6; c7 = d5 - d6; c6 = d7; if stages > 1 % odd stage 3 b4 = c4 + c5; b5 = c4 - c5; b6 = c6 + c7; b7 = c6 - c7; % even stage 3 b0 = c0 + c1; b1 = c0 - c1; b2 = c2 + c2/4 + c3/2; % 5/4*c2 + 1/2*c3 b3 = c2/2 - c3 - c3/4; % 1/2*c3 - 5/4*c3 % ... end

The trick is that within each stage, there are only integer additions and right-shifts (here written as divisions because this is Octave code, but in integer code it should really be shifts and not divisions) of values computed in a previous stage. The latter can never overflow. The former may have intermediate overflows in 16-bit integer, but provided that computations are done in two’s complement arithmetic, the results will be equal to the results of the corresponding exact integer computation modulo 216. So as long as said exact integer computation has a result that fits into 16 bits, the computed results are going to be correct, even if there are intermediate overflows. Note that this is true when computed using SIMD intrinsics that have explicit two’s complement semantics, but is *not* guaranteed to be true when implemented using 16-bit integers in C/C++ code, since signed overflow in C triggers undefined behavior!

Also note that we can’t compute values such as `5/4*c2`

as `(5*c2)/4`

, since the intermediate value `5*c2`

can overflow – and knowing as we do already that we have less than 1 bit of headroom left, likely will for some inputs. One option is to do the shift first: `5*(c2/4)`

. This works but throws away some of the least-significant bits. The form `c2 + (c2/4)`

chosen here is a compromise; it has larger round-off error than the preferred `(5*c2)/4`

but will only overflow if the final result does. The [findorth](https://github.com/rygorous/dct_blog/blob/master/findorth/findorth.cpp) tool described last time automatically determines expressions in this form.

### Verification

Okay, that’s all the ingredients we need. We have the transform decomposed into separate stages; we know the value range at the input to each stage, and we know that if both the inputs and the outputs fit inside 16 bits, the results computed in each stage will be correct. So now all we need to do is verify that last bit – *are* the outputs of the intermediate stages all 16 bits or less?

2> I=eye(8); 3> F=bink_dct_B2(I); 4> S=diag(8 ./ diag(F*F')); 5> Inv1=bink_idct_B2_partial(I,1); 6> Inv2=bink_idct_B2_partial(I,2); 7> Inv3=bink_idct_B2_partial(I,3); 8> Inv4=bink_idct_B2_partial(I,4); 9> Scaled=kron(S,S) * kron(F,F); 10> norm(kron(I,I) * Scaled, 'inf') ans = 72.047 11> norm(kron(I,Inv1) * Scaled, 'inf') ans = 72.047 12> norm(kron(I,Inv2) * Scaled, 'inf') ans = 77.811 13> norm(kron(I,Inv3) * Scaled, 'inf') ans = 77.811 14> norm(kron(I,Inv4) * Scaled, 'inf') ans = 67.905 15> norm(kron(Inv1,Inv4) * Scaled, 'inf') ans = 67.905 16> norm(kron(Inv2,Inv4) * Scaled, 'inf') ans = 73.337 17> norm(kron(Inv3,Inv4) * Scaled, 'inf') ans = 73.337 18> norm(kron(Inv4,Inv4) * Scaled, 'inf') ans = 64.000

Lines 2-4 compute the forward DCT and scaling matrices. 5 through 9 compute various partial IDCTs (`Inv4`

is the full IDCT) and the matrix representing the results after the 2D forward DCT and scaling. After that, we successively calculate the norms of more and more of the 2D IDCT: no IDCT, first stage of row IDCT, first and second stage of row IDCT, …, full row IDCT, full row IDCT and first stage of column IDCT, …, full 2D IDCT.

Long story short, the worst matrix infinity norm we have along the whole transform chain is 77.811, which is well below 128; hence the Bink B2 IDCT is overflow-free for 8-bit signals when implemented using 16-bit integers.

A similar process can be used for the forward DCT, but in our case, we just implement it in 32-bit arithmetic (and actually floating-point arithmetic at that, purely for convenience). The forward DCT is only used in the encoder, which spends *a lot* more time per block than the decoder ever does, and almost none of it in the DCT. Finally, there’s the scaling step itself; there’s ways to do this using only 16 bits on the decoder side as well (see for example [“Low-complexity transform and quantization in H. 264/AVC”](http://homepages.cae.wisc.edu/~ece734/references/malvar03.pdf)), but since the scaling only needs to be applied to non-zero coefficients and the post-quantization DCT coefficients in a video codec are *very* sparse, it’s not a big cost to do the scaling during entropy decoding using regular, scalar 32-bit fixed point arithmetic. And if the scaling is designed such that no intermediate values ever take more than 24 bits (which is much easier to satisfy than 16), this integer computation can be performed exactly using floating-point SIMD too, on platforms where 32-bit integer multiplies are slow.

And that’s it! Congratulations, you now know everything worth knowing about Bink 2.2’s integer DCTs. :)