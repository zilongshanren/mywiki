---
title: Bink 2.2 integer DCT design, part 1
url: https://fgiesen.wordpress.com/2013/11/04/bink-2-2-integer-dct-design-part-1/
published: '2013-11-04'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Bink 2.2 integer DCT design, part 1

This subject is fairly technical, and I’m going to proceed at a somewhat higher speed than usual; part of the reason for this post is just as future reference material for myself.

### DCTs

There’s several different types of [discrete cosine transforms](http://en.wikipedia.org/wiki/Discrete_cosine_transform), or DCTs for short. All of them are linear transforms on N-dimensional vectors (i.e. they can be written as a N×N matrix), and they all relate to larger real DFTs (discrete Fourier transforms) in some way; the different types correspond to different boundary conditions and different types of symmetries. In signal processing and data compression, the most important variants are what’s called DCT-II through DCT-IV. What’s commonly called “the” DCT is the DCT-II; this is the transform used in, among other things, JPEG, MPEG-1 and MPEG-2. The DCT-III is the inverse of the DCT-II (up to scaling, depending on how the two are normalized; there’s different conventions in use). Thus it’s often called “the” IDCT (inverse DCT). The DCT-IV is its own inverse, and forms the basis for the MDCT (modified DCT), a lapped transform that’s at the heart of most popular perceptual audio codecs (MP3, AAC, Vorbis, and Opus, among others). DCTs I and V-VIII also exist but off the top of my head I can’t name any signal processing or data compression applications that use them (which doesn’t mean there aren’t any).

Various theoretical justifications exist for the DCT’s use in data compression; they are quite close to the optimal choice of orthogonal basis for certain classes of signals, the relationship to the DFT means there are fast (FFT-related) algorithms available to compute them, and they are a useful building block for other types of transforms. Empirically, after 25 years of DCT-based codecs, there’s little argument that they work fairly well in practice too.

Image (and video) codecs operate on 2D data; like the DFT, there are 2D versions of all DCTs that are separable: a 2D DCT of a M×N block decomposes into N 1D M-element DCTs on the columns followed by M N-element DCTs on the rows (or vice versa). JPEG and the MPEGs up to MPEG-4 ASP use 2D DCTs on blocks of 8×8 pixels. H.264 (aka MPEG-4 AVC) initially switched to 4×4 blocks, then added the 8×8 blocks back in as part of the “High” profile later. H.265 / HEVC has both sizes and also added support for 16×16 and 32×32 transform blocks. Bink 2 sticks with 8×8 DCTs on the block transform level.

### Algorithms

There are lots of different DCT algorithms, and I’m only going to mention a few of them. Like the DFT, DCTs have a recursive structure that allows them to be implemented in O(N log N) operations, instead of the O(N2) operations a full matrix-vector multiply would take. Unlike the FFT, which decomposes into nothing but smaller FFTs except for some multiplications by scalars (“twiddle factors”) plus a permutation, the recursive factorizations of one DCT type will usually contain other trigonometric transforms – both smaller DCTs and smaller DST (discrete sine transforms) of varying types.

The first important dedicated DCT algorithm is presented in [Chen77] (see references below), which provides a DCT factorization for any power-of-2 N which is substantially faster than computing the DCT using a larger FFT. Over a decade later, [LLM89] describes a family of minimum-complexity (in terms of number of arithmetic operations) solutions for N=8 derived using graph transforms, a separate algorithm that has no more than one multiply along any path (this is the version used in the [IJG](http://www.ijg.org/) JPEG library), and a then-new fast algorithm for N=16, all in a 4-page paper. [AAN88] introduces a scaled algorithm for N=8 which greatly reduces the number of multiplications. A “scaled” DCT is one where the output coefficients have non-uniform scaling factors; compression applications normally follow up the DCT with a quantization stage and precede the IDCT with a dequantization stage. The scale factors can be folded into the quantization / dequantization steps, which makes them effectively “free”. From today’s perspective, the quest for a minimal number of multiplies in DCT algorithms seems quaint; fast, pipelined multipliers are available almost everywhere these days, and today’s *mobile phone CPUs* achieve floating point throughputs higher than those of 1989’s fastest supercomputers (2012 Nexus 4: 2.8 GFLOPS measured with RgbenchMM; Cray-2: 1.9 GFLOPS peak – let that sink in for a minute). That said, the “scaled DCT” idea is important for other reasons.

There’s also direct 2D methods that can reduce number of arithmetic operations further relative to a separable 1D implementation; however, the overall reduction isn’t very large, the 2D algorithms require considerably more code (instead of 2 loops processing N elements each, there is a single “unrolled” computation processing N2 elements), and they have data flow patterns that are unfriendly to SIMD or hardware implementations (separable filters, on the other hand, are quite simple to implement in a SIMD fashion).

For 1D DCTs and N=8, the situation hasn’t substantially changed since the 1980s. Larger DCTs (16 and up) have seen some improvement on their arithmetic operation costs in recent years [Plonka02] [Johnson07], with algorithms derived symbolically from [split-radix FFTs](http://en.wikipedia.org/wiki/Split-radix_FFT_algorithm) (though again, how much of a win the better algorithms are heavily depends on the environment).

### Building blocks

Independent of the choice of DCT algorithm, they all break down into the following 3 basic components:

**Butterflies**. A butterfly is the transform(they’re called that way because of how they’re drawn in diagram form). A butterfly is also its own inverse, up to a scale factor of two, since

and likewise

.

**Planar rotations**. Take a pair of values, interpret them as coordinates in the plane, and rotate them about the origin. I’ve written about them (even in the context of DCTs)[before](https://fgiesen.wordpress.com/2010/11/05/planar-rotations-and-the-dct/). The inverse of a rotation by θ radians is a rotation by -θ radians. There’s also planar reflections which are[closely related](http://en.wikipedia.org/wiki/Coordinate_rotations_and_reflections)to rotations and work out pretty much the same on the implementation side. Reflections are self-inverse, and in fact a butterfly is just a reflection scaled by.

**Scalar multiplies**. Mapfor some nonzero constant c. The inverse is scaling by 1/c.


There are also a few properties of the DCT-II that simplify the situation further. Namely, the DCT-II (when properly normalized) is an *orthogonal* transform, which means it can be decomposed purely into planar rotations and potentially a few sign flips at the end (which can be represented as scalar multiplications). Butterflies, being as they are a scaled reflection, are used because they are cheaper than a “proper” rotation/reflection, but they introduce a scale factor of . So scalar multiplications are used to normalize the scaling across paths that go through a different number of butterflies; but the DCT algorithms we’re considering here only have scaling steps at the end, which can conveniently be dropped if a non-normalized (scaled) DCT is acceptable.


What this all boils down to is that a DCT implementation basically boils down to which planar rotations are performed when, and which of the various ways to perform rotations are employed. There are tons of tricky trade-offs here, and which variant is optimal really depends on the target machine. Older standards (JPEG, the earlier MPEGs) didn’t specify exactly which IDCT was to be used by decoders, leaving this up to the implementation. Every codec had its own DCT/IDCT implementations, which caused problems when a video was encoded using codec A and decoded using codec B – basically, over time, the decoded image could drift from what the encoder intended. Some codecs even had multiple DCT implementations with different algorithms (say one for MMX, and another for SSE2-capable CPUs) so this problem occurred even between different machines using the same codec. And of course there’s the general problem that the “real” DCT involves irrational numbers as coefficients, so there’s really no efficient way to compute it exactly for arbitrary inputs.

### Integer transforms

The solution to all these problems is to pick a specific IDCT approximation and specify it exactly – preferably using (narrow) integer operations only, since floating-point is expensive in hardware implementations and getting 100% bit-identical results for floating-point calculations across multiple platforms and architectures is [surprisingly hard](http://randomascii.wordpress.com/2013/07/16/floating-point-determinism/) in software.

So what denotes a good integer DCT? It depends on the application. As the title says, this post is about the 8×8 integer IDCT (and matching DCT) design used for Bink 2.2. We had the following requirements:

- Bit-exact implementation strictly required (Bink 2 will often go hundreds or even thousands of frames without a key frame). Whatever algorithm we use, it must be
*exactly*the same on all targets. - Must be separable, i.e. the 2D DCT factors into 1D DCT steps.
- Must be a close approximation to the DCT. The goal was to be within 2% in terms of the matrix 2-norm, and same for the
[coding gain](http://www.stanford.edu/class/ee398a/handouts/lectures/07-TransformCoding.pdf)compared to a “proper” DCT. Bink 2 was initially designed with a full-precision floating-point (or high-precision fixed point) DCT in mind and we wanted a drop-in solution that wouldn’t affect the rest of the codec too much. - Basis vectors must be fully orthogonal (or very close) to allow for
[trellis quantization](http://en.wikipedia.org/wiki/Trellis_quantization). - Must have an efficient SIMD implementation on all of the following:
- x86 with SSE2 or higher in both 32-bit and 64-bit modes.
- ARM with NEON support.
- PowerPC with VMX/AltiVec (e.g. PS3 Cell PPU).
- Cell SPUs (PS3 again).
- PowerPC with VMX128 (Xbox 360 CPU).

Yep, lots of game consoles – RAD’s a game middleware company.

- 16-bit integer preferred, to enable 8-wide operation on 128-bit SIMD instruction sets. To be more precise, for input values in the range [-255,255], we want intermediate values to fit inside 16 bits (signed) through all stages of the transform.

This turns out to limit our design space greatly. In particular, VMX128 removes *all* integer multiplication operations from AltiVec – integer multiplication by scalars, where desired, has to be synthesized from adds, subtractions and shifts. This constraint ended up driving the whole design.

There’s other integer DCTs designed along similar lines, including several used in other video codecs. However, while there’s several that only use 16-bit integer adds and shifts, they are generally much coarser approximations to the “true” DCT than what we were targeting. Note that this doesn’t mean they’re necessarily worse for compression purposes, or that the DCT described here is “better”; it just means that we wanted a drop-in replacement for the full-precision DCT, and the transform we ended up with is a closer to that goal than published variants with similar complexity.

### Building an integer DCT

Most of the integer DCT designs I’m aware of start with a DCT factorization; the Bink 2 DCT is no exception, and starts from the DCT-II factorizations given in [Plonka02]. For N=8, this is equivalent to the factorization described in [LLM89]: by reordering the rows of the butterfly matrices in Plonka’s factorization and flipping signs to turn rotation-reflections into pure rotations, the DCT-II factorization from example 2.8 can be expressed as the [butterfly diagram](http://en.wikipedia.org/wiki/Butterfly_diagram) (click to zoom)

which corresponds to the DCT variation on the left of the 2nd row in figure 4 of [LLM89], with the standard even part. However, [LLM89] covers only N=8, N=16 and (implicitly) N=4, whereas [Plonka02] provides factorizations for arbitrary power-of-2 N, making it easy to experiment with larger transform sizes with a single basic algorithm. **UPDATE**: The previous version of the diagram had a sign flip in the rightmost butterfly. Thanks to “terop” for pointing this out in the comments!

Now, we’re allowing a scaled DCT, so the final scale factors of can be omitted. As explained above, this leaves butterflies (which have simple and obvious integer implementations) and exactly three rotations, one in the even part (the top half, called “even” since it produces the even-numbered DCT coefficients) and two in the odd part:


As customary for DCT factorizations, and

. Note that due to the corresponding trig identities, we have

,

,

and

, which means that the three rotations we see here (and indeed all rotations referenced in [LLM89]) can be expressed in terms of just

,

,

,

,

and

.


Now, all we really need to do to get an integer DCT is to pick integer approximations for these rotations (preferably using only adds and shifts, see the constraints above!). One way to do so is the BinDCT [Liang01], which uses the decomposition of rotation into shears I explained [previously](https://fgiesen.wordpress.com/2010/11/05/planar-rotations-and-the-dct/) and then approximates the shears using simple dyadic fractions. This is a cool technique, but yields transforms with basis vectors that aren’t fully orthogonal; how big the non-orthogonality is depends on the quality of approximation, with cheaper approximations being less orthogonal. While not a show-stopper, imperfect orthogonality violates the assumptions inherent in [trellis quantization](http://en.wikipedia.org/wiki/Trellis_quantization) and thus reduces the quality of the rate-distortion optimization performed on the encoder side.

### Approximating rotations

So how do we approximate irrational rotations as integers (preferably small integers) with low error? The critical insight is that *any* matrix of the form

is a planar rotation about some angle θ such that . And more generally, any matrix of the form


is a *scaled* planar rotation. Thus, if we’re okay with a scaled DCT (and we are), we can just pick two arbitrary integers c, s that aren’t both zero and we get a scaled integer rotation (about some arbitrary angle). To approximate a *particular* rotation angle θ, we want to ensure that . Since we’d prefer small integer values s and c, we can find suitable approximations simply by enumerating all possibilities with a suitable ratio, checking how closely they approximate the target angle, and using the best one. This is easily done with a small program, and by itself sufficient to find a good solution for the rotation in the even part of the transform.


The odd part is a bit trickier, because it contains two rotations and butterflies that combine the results from different rotations. Therefore, if the two rotations were scaled differently, such a butterfly will result not in a scaled DCT, but a different transformation altogether. So simply approximating the rotations individually won’t work; however, we can approximate the two rotations simultaneously, and add the additional constraint that

(somewhat reminiscent of

[Pythagorean triples](http://en.wikipedia.org/wiki/Pythagorean_triple)), thus guaranteeing that the norm of the two rotations is the same. Initially I was a bit worried that this might over-constrain the problem, but it turns out that even with this extra complication, there are plenty of solutions to choose from. As before, this problem is amenable to an exhaustive search over all small integers that have the right ratios between each other.

Finally, we need implementations of the resulting rotations using only integer additions/subtractions and shifts. Since we’re already fully integer, all this means is that we need to express the integer multiplications using only adds/subtracts and shifts. This is an interesting and very tricky problem by itself, and I won’t cover it here; see books like [Hacker’s Delight](http://www.amazon.com/Hackers-Delight-Edition-Henry-Warren/dp/0321842685) for a discussion of the problem. I implemented a simple algorithm that just identifies runs of 0- and 1-bits in the binary representation of values. This is optimal for small integers (below 45) but not necessarily for larger ones, but it’s usually fairly good. And since the program already tries out a bunch of variants, I made it compute costs for the different ways to factor planar rotations as well.

The result is [findorth.cpp](https://github.com/rygorous/dct_blog/blob/master/findorth/findorth.cpp), a small C++ program that finds candidate small integer approximations to the DCT rotations and determines their approximate cost (in number of adds/subtractions and shifts) as well. Armed with this and the rest of the factorization above, it’s easy to come up with several families of integer DCT-like transforms at various quality and cost levels and compare them to existing published ones:

| Variant | (c2,s2) |
(c1,s1) |
(c3,s3) |
Cost | L2 err | Gain (dB) |
|---|---|---|---|---|---|---|
| A1 | (17,-7)/16 | (8,-1)/8 | (7,4)/8 | 32A 10S | 0.072 | 8.7971 |
| B1 | (5,-2)/4 | (8,-1)/8 | (7,4)/8 | 30A 10S | 0.072 | 8.7968 |
| A2 | (17,-7)/16 | (19,-4)/16 | (16,11)/16 | 38A 12S | 0.013 | 8.8253 |
| B2 | (5,-2)/4 | (19,-4)/16 | (16,11)/16 | 36A 12S | 0.013 | 8.8250 |
| A3 | (17,-7)/16 | (65,-13)/64 | (55,37)/64 | 42A 15S | 0.003 | 8.8258 |
| B3 | (5,-2)/4 | (65,-13)/64 | (55,37)/64 | 40A 15S | 0.012 | 8.8255 |
| Real DCT | – | – | – | – | 0.000 | 8.8259 |
| BinDCT-L1 | – | – | – | 40A 22S | 0.013 | 8.8257 |
| H.264 | – | – | – | 32A 10S | 0.078 | 8.7833 |
| VC-1 | – | – | – | ? | 0.078 | 8.7978 |

The cost is measured in adds/subtracts (“A”) and shifts (“S”); “L2 err” is the matrix 2-norm of the difference between the approximated DCT matrix and the true DCT, and “gain” denotes the coding gain assuming a first-order Gauss-Markov process with autocorrelation coefficient ρ=0.95 (a standard measure for the quality of transforms in image coding).

These are by far not all solutions that `findorth`

finds, but they’re what I consider the most interesting ones, i.e. they’re at good points on the cost/approximation quality curve. The resulting transforms compare favorably to published transforms at similar cost (and approximation quality) levels; Bink 2.2 uses variant “B2”, which is the cheapest one that met our quality targets. The Octave code for everything in this post is available on [Github](https://github.com/rygorous/dct_blog).

The H.264 transform is patented, and I believe the VC-1 transform is as well. The transforms described in this post are not (to the best of my knowledge), and RAD has no intention of ever patenting them or keeping them secret. Part of the reason for this post is that we wanted to make an integer DCT that is of similar (or higher) quality and comparable cost than those in existing video standards freely available to everyone. And should one of the particular transforms derived in this post turn out to be patent-encumbered, `findorth`

provides everything necessary to derive a (possibly slightly worse, or slightly more expensive) alternative. (Big thanks to my boss at RAD, Jeff Roberts, for allowing and even encouraging me to write all this up in such detail!)

This post describes the basic structure of the transform; I’ll later post a follow-up with the details of our 16-bit implementation, and the derivation for why 16 bits are sufficient provided input data is in the range of [-255,255].

### References

- [Chen77]
- Chen, Wen-Hsiung, C. H. Smith, and Sam Fralick. “A fast computational algorithm for the discrete cosine transform.” Communications, IEEE Transactions on 25.9 (1977): 1004-1009.
[PDF](http://www.cin.ufpe.br/~vak/tg/Chen-dct.pdf) - [AAN88]
- Yukihiro, Arai, Agui Takeshi, and Masayuki Nakajima. “A fast DCT-SQ scheme for images.” IEICE TRANSACTIONS (1976-1990) 71.11 (1988): 1095-1097.
- [LLM89]
- Loeffler, Christoph, Adriaan Ligtenberg, and George S. Moschytz. “Practical fast 1-D DCT algorithms with 11 multiplications.” Acoustics, Speech, and Signal Processing, 1989. ICASSP-89., 1989 International Conference on. IEEE, 1989.
[PDF](http://www3.matapp.unimib.it/corsi-2007-2008/matematica/istituzioni-di-analisi-numerica/jpeg/papers/11-multiplications.pdf) - [Liang01]
- Liang, Jie, and Trac D. Tran. “Fast multiplierless approximations of the DCT with the lifting scheme.” Signal Processing, IEEE Transactions on 49.12 (2001): 3032-3044.
[PDF](http://thanglong.ece.jhu.edu/Tran/Pub/binDCT.pdf) - [Plonka02]
- Plonka, Gerhard, and Manfred Tasche. “Split-radix algorithms for discrete trigonometric transforms.” (2002).
[PDF](http://duepublico.uni-duisburg-essen.de/servlets/DerivateServlet/Derivate-5235) - [Johnson07]
- Johnson, Steven G., and Matteo Frigo. “A modified split-radix FFT with fewer arithmetic operations.” Signal Processing, IEEE Transactions on 55.1 (2007): 111-119.
[PDF](http://ftp.fftw.org/newsplit.pdf)

Looking forward to the next part.

Thanks for providing all that detail – you guys at RAD rock :).

yup, all these guys at RAD / mollyrocket are really hardcore :D great article fabien!

One issue I don’t see addressed is the round-trip error. eg. minimize

| 1 – Inverse * Forward |

One of the reasons why the shear decomposition of rotations has been preferred by some approximations is that a shear can be done as lifting steps which are exactly invertible, so you can make a lossless DCT approximation sans quantization (or bounded loss, like inversion is within +-1).

I’m sure that in the Bink 2 domain, getting the DCT shape right is more important, but just curious if this was addressed somewhere.

| 1 – Inverse * Forward |

I suppose this is the same as the L2 error of the matrix, assuming that you are holding Forward constant as the true DCT (real numbers) and only optimizing Inverse, since

| 1 – Inverse * Forward | = | Forward^-1 – Inverse |

Yup, exactly.

=|Forward^T – Forward_Approx^T| (both are orthogonal)

=|(Forward – Forward_Approx)^T|

=|Forward – Forward_Approx| (2-norm is self-dual)

which is the matrix 2-norms I’m giving in the article. (So yeah I’m computing this from the normalized Forward_Approx, with the corrective diagonal matrix for the scaled DCT applied – see the Octave code, dct_quality.m).

See my reply to your other comment. But yeah in the bit rate range we’re targeting, perfect integer reversibility of the transform just isn’t that useful a feature – in normal operation, we’re too far away from “no quantization” for it ever to matter.

I actually spent about half the total design time on lifting-based approaches that I ultimately abandoned. Approximating the lifting factors does introduce a marked amount of non-orthogonality; the approximations I tried (I went through a few) usually had at least one pair of rows with |dot(row_i, row_j)| > 0.04 (and sometimes >0.07). If it was a tenth that (or less), I would’ve (probably) been fine with it, but this is in a range where I had to worry about “crosstalk” between coefficients for usual value ranges and quantization factors, meaning that it’s likely to make the quantizer pick the “wrong” rounding a decent percentage of the time; not something I wanted to throw at our quantization back end.

Also, the BinDCT design given in the paper combines lifting-based rotations with a scaled DCT, and scaled is really the last thing you want for lossless coding!

The factorization I showed (and most other ones) have half the signal paths going through 2 butterflies and the other half through 3; that’s where the sqrt(2) scale factors come from. For integer reversible, I’d use scale-free DCT: the final butterflies can’t be implemented as butterflies, but have to be a proper [c4 s4;s4 -c4], i.e. rotation by 22.5 degrees with sign flip at the end. Implement this with 3 lifting steps. Similarly, all other rotations should use the scale-free 3-step structure. This gives you an integer reversible transform that has a uniform gain of 2 (for N=8). IMO that’s the right way to build a suitable transform for lossless coding; but I’m not sold on DCTs for lossless coding to begin with (all the results I’ve seen so far have been very “meh”), and the requisite modifications do make the DCT/IDCT a good deal more expensive.

That said, the approach I took has some wrinkles too; in particular squeezing it into 16 bits is *really* tight, and the way I ended up doing it introduces some more rounding error. More details will be in the follow-up.

Doesn’t this produce incorrect results for X[3] and X[5]? It seems that the last butterfly has been flipped upside down in the image (Stage 4, https://fgiesen.files.wordpress.com/2013/11/plonka_dct.png).

Oops. Yes indeed, I labeled that wrong when transcribing the code (dct_plonka_schematic.m) into the diagram.

Thanks fgiesen for the great write up. Thoroughly interesting read and great to see RAD continuing to publish code and information that helps to advance the development of openly available knowledge. This helps allow us all to progress and hence in turn contribute to the evolution of code, mathematical implementation and efficiency in code, and the development of improved open source and creative commons tools and applications. Such an open approach to sharing knowledge helps provide a rich and fertile environment for the next generation of young developers and designers.

Memories of the 80’s rich open environment popped up when I was reading this article, such as early 80’s coding publications and companies like Commodore continuing to provide coding environments with their platforms eventually including CLI in Amiga Workstation along with detailed references you could teach yourself object orientated programming from out of the box. The sharing environment back then between perfect strangers at expos trading their own free programs with one another and enthusiastic community collaboration has allowed us to reach where we are today and thankfully still continues.

You guys really are RAD!

Hello,

thank you for all your explanations, they are precious to my design of a lossless DCT.

However, while trying to reproduce and extend your version of the Plonka butterfly diagram https://fgiesen.files.wordpress.com/2013/11/plonka_dct1.png I just found a discrepancy with [LLM89] for the computation of X[3] X[5].

I am building a DCT16 with the help of the last diagram of the Loeffler paper and the even 8-tap part should be substancially similar to your butterfly diagram. But the input of the last butterfly comes from different outputs, with different signs, yet the rotation angles are the same so I’m pretty sure the result is different.

Is this a known/solved issue ? I have seen that you have already been notified of this but did you correct the diagram ? Which version is correct ?

My past musings with the Winograd DCT8 http://ygdes.com/dct_fc0/dct_fc0.html was already plagued by this kind of typo (from upstream). And yes, my reverse engineering of the DCT8 (from forgotten code) was messed up, I realised this just recently so that’s why I’m redesigning it carefully now.

I’m not fluent with matrix transformations so I must rely on existing diagrams or working code to derive mine. I’m triple-checking all the connexions and try to input test vectors but I need a reliable reference…

As I mention in the article, the Plonka DCT factorization matches up with one of the “variations” in the LL&M paper, namely the one on in the left column of row 2 (from the top) in figure 4, and they agree. I haven’t looked at their 16-point DCT and can’t vouch for it (but do note that the even-odd part in the LL&M 16-point diagram uses a different ordering of output points than figure 4 in the same paper does! (Figure 4 has 1, 3, 5, -7; figure 9 corresponds to 1, 3, 7, 5, so the last two lanes are flipped).

If you need a reliable reference, don’t use a factored DCT at all. Just use the DCT-II definition directly.

Thank you Florian,

Yes I have noticed the reordering of the output but there must be something else swapped at the rotation level in figure 9.

I have chosen the version with rotations of 5pi and 7pi because they should inject less “approximation noise” than lower angles (1pi and 3pi). Low angles are notoriously noisy so it’s better to be near pi/2. According to the paper, the stage configuration you have chosen is the only one that is convenient with this angle constraint. Some versions have sign/negation and it confuses me.

I have compared with other decompositions and I have reordered the diagram to create this one : http://ygdes.com/~whygee/Plonka-DCT8.png I hope that it is “right” but it’s orthogonal to the technique I develop (more on this when it works)

Regards !

Hello,

Thank you for the explanations !

Is the X3-X5 issue corrected in the butterfly diagram ?

I compare the blog’s picture with the even part of the DCT16 in [LLM89] and I see a discrepancy. Which is correct ? I’m not fluent with matlab or matrix notation so I must rely on valid diagrams.

Regards!

Hey Fabian,

I tried to implement the DCT/iDCT out of curiosity and no matter what I do if I run DCT/iDCT with normalization it’s always looking “wrong”. I get pretty strong block artifacts already.

You mentioned the DCT isn’t meant to be perfectly inversible, but would have expected it to look okay with some minor differences.

Am I doing something wrong or is this expected?

If you’re getting blocking artifacts, you got the normalization wrong. The Bink DCT is, like e.g. the AA&N DCT algorithm (or H.264), a scaled transform.

In exact arithmetic, the 1D DCT is an unitary linear transform, up to scaling. That means if you have the 1D DCT matrix M, you know that there is some diagonal matrix D such that

(DM)^T * DM = I M^T D^2 M = I D^2 = inv(M^T) * inv(M) D^2 = inv(M * M^T) D^(-2) = M*M^T.

So you multiply M*M^T (you get M if you don’t have it simply by transforming [1;0;0;0;…], [0;1;0;0;…], [0;0;1;0;…] and so forth and putting the columns in a matrix). The result should be a diagonal matrix unless your DCT is buggy :), and on the diagonal are the squares of the reciprocals of the normalizing factors you need to make the forward or inverse steps properly unitary. That’s in the example Matlab code here. (I don’t remember what the actual scale factors are off the top of my head, but you can just get Octave and run the example to find out).

A full step of the forward 1D transforms is this:

1. Compute the integer DCT using the code described,

2. Multiply the resulting coefficients by the corresponding scale factors to get the real 1D DCT results. This step will in general be folded into the quantization matrix you also apply at this step, but while debugging, you should not have a quantization matrix in the mix here.

You can validate this by checking against the result of a proper DCT-II (definition is on Wikipedia). The Bink DCT is quite close (Bink uses variant B2); as the part 1 results show, the matrix 2-norm of the difference between the approximation and a “real” DCT (in floats!) is about 0.013, meaning that if you have some test vector x, you should get ||binkdct(x) – dct2(x)|| <= 0.013*||x|| (in the 2-norm, i.e. Euclidean length).

Likewise, the proper inverse transform is:

1. Multiply the integer coefficients by the same scale factors again (as before). Again this can be folded into the dequantization process.

2. Compute the IDCT.

Why multiply by scale factors twice, and not just once? Well, you can in principle, but the whole point of the quantization scale factor stuff is that you're trying to move to a space where the errors are more perceptually uniform. Messing with the scaling on the values you quantize destroys that.

A few more things to note:

1. This is all talking about the 1D transform. The 2D transform is separable, so you just do 1D on all rows and all columns. For the 2D transform, the effective scale factor at row i and column j is scale_factor_1d(i)*scale_factor_1d(j).

2. Speaking of transform ordering: the nicest implementation for SIMD is: 1D transform on all columns in parallel, transpose, 1D transform of all columns in parallel, transpose (Because working on all columns at the same time your SIMD vectors are nice contiguous rows). The corresponding inverse is then transpose, 1D on columns, transpose, 1D on columns. Note that the "inner" transposes are applied only to the transformed coefficients. You can get rid of them entirely by leaving the data as it is, and transposing your quantization matrix and the traversal pattern used to encode the coefficients instead.

3. The quantization stuff is usually done on all integers (although it doesn't have to be). If you're doing a fixed-point implementation, there's a few more tricks you can pull. For example, using an accurate fixed-point multiply in the decoder that needs extra fractional bits is a bit more expensive. What you can do instead is to not have the exact same scale factors at both ends. You can make the decoder use scaling factors that are say rounded to the nearest integer (with not a lot of extra fixed-point bits), and adapt the corresponding weighting on the encoder side to compensate for the error. As long as the encoder-side and decoder-side factors multiply out to the right overall scale, the results will be OK, but it does mean your quantization weighting is very slightly off. (Usually not a problem.)

Thank you for the detailed response Fabian. I indeed thought the scale factor was a constant for all of the 8 values after the DCT.

The DCT-II/DCT-III was already working fine. Thanks for the clarification, I will try this soon. For my experiments right now I just stick to the float DCT, shouldn’t make a difference if it’s that close.

I haven’t touched lossy compression at all and always wanted to learn more about it. Right now I’m like a factor 2-3x off from JPEG :)