---
title: Planar rotations and the DCT
url: https://fgiesen.wordpress.com/2010/11/05/planar-rotations-and-the-dct/
published: '2010-11-05'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Planar rotations and the DCT

I’ve been looking a bit at [DCT](http://en.wikipedia.org/wiki/Discrete_cosine_transform) algorithms recently. Most fast DCTs are designed under two assumptions that are worth re-examining: 1. Multiplies are a lot more expensive than additions and should be avoided and 2. The cost of a DCT is mainly a function of the number of multiplies and adds performed. (1) isn’t really true anymore, particularly in current floating point/SIMD processors where multiplies and adds often take the same time and fused multiply-adds are available, and (2) also is overly naive for current architectures – again, particularly with SIMD implementations, the cost of loading, storing and shuffling values around can easily be as high as the actual computations, if not higher. Tricks that save a few arithmetic ops will backfire if they make the dataflow more complicated. Anyway, I don’t have any conclusions on that yet (it’s still a work in progress), but I do have some notes on one important ingredient: planar rotations. And now excuse my hypocrisy as I’ll be (shamelessly) only talking about the number of arithmetic ops for the rest of this post. :)

To briefly set the stage, basically all DCT algorithms decompose into a sequence of two types of operations:

**“Butterflies”**. The basic transform is(this is also a 2-point FFT, a 2-point DCT, and a 2-point Hadamard transform – they’re all identical in this case, up to normalization). The name “butterfly” comes from the way these operations are typically drawn in a dataflow graphs.

**Planar rotations**. A bog-standard 2D rotation of the form.


There’s not much to do about the butterflies, but the planar rotations are interesting, and different DCT algorithms use different ways of performing them. Let’s look at some:

### Method 1: The obvious way

You can just do the matrix-vector multiply directly. Cost: 4 multiplies and 2 adds, or 2 multiplies and 2 FMAs.

### Method 2: Saving a multiply

Rearranging the equation a bit allows us to extract a common factor:

For constant , the sums/differences of cos/sin terms can be precomputed and we end up with 3 multiplies and 3 adds, or 1 multiply, 1 add and 2 FMAs. If only the computation of t was a multiply-add and not an add followed by a multiply… anyway, this reduces the number of arithmetic ops in the “classic” model, but not in a FMA-based model, and it has a chain of 3 dependent operations whereas Method 1 only has 2. This technique is used in most DCT factorizations, including the LL&M DCT used by the IJG JPEG lib for the “slow” integer transform (the default).


Note that there’s no special reason to base t off the cosine term, we could do the same with sin at the same cost:

### Method 3: A scaled rotation

A different trick is used in the AA&N DCT (used by the IJG JPEG lib for the fast integer transform and the floating-point version):

Note that this is just Method 1 multiplied by . Cost: Same as Method 1 – 4 adds 2 multiplies or 2 FMA and 2 multiplies. But we gained something: We can try to propagate the constant scale factor along all the rest of the computation (note we need to be careful when combining differently scaled values) and simply return scaled results. This is what the original AA&N DCT does. We can also delay the multiply by just one step: If the rotation is used as input to a butterfly step, we can absorb the scale factor into the butterfly and turn two adds/subs into two FMAs, which means we get a planar rotation for the cost of 2 independent FMAs. Nice!


(Again, there’s a dual version which multiplies by the cotangent of and returns results scaled by

).


### Method 4: Decompose into shears

There’s more: We can also write a rotation as three shears:

Note that this can be done without using any extra registers. Cost: 3 multiplies and 3 adds or 3 FMAs, but every operation is dependent on the previous one, so we get a chain of 3 dependent ops, same as for Method 2.

One interesting side effect of doing the computation this way is that the integer version of this is perfectly reversible, even if there are truncation errors in the multiplies – you just do the steps in reverse. Integer lifting formulations of wavelet transforms use the same primitive. One interesting consequence of this rotation formula is that it can be used to instantly obtain “integer lifting” versions of any orthogonal transform: You can compute the QR decomposition of any matrix using Givens rotations, which are just ordinary planar rotations and can be performed using this technique. If the matrix under consideration is orthogonal, then by uniqueness of the QR decomposition up to sign, we know that R is just a diagonal matrix with all entries being 1 or -1, so multiplication by R is perfectly reversible in integer values as well.

This nice property aside, the long dependency chains are somewhat bothersome. But it’s an interesting formula, and one that’s been used to design exactly reversible integer-to-integer DCTs (search for “BinDCT”).

### Honorary mention: Complex multiply

There’s also a related formula to perform complex multiplication with just 3 multiplies instead of the usual 4 in the obvious formula

Compute it as

instead, using 3 multiplies and 5 adds. For a known fixed that we’re multiplying with (as in the DCT case), one of the adds can be precomputed, but it’s still 3 muls 4 adds and has a 4-operation dependency chain, so it’s not really useful in this application. But it’s nice to know anyway.


### So which one do you use?

Well, I haven’t decided yet. For floating-point implementations on platforms with FMA support, method 3 is definitely the most attractive one, since absorbing scale factors into later butterflies is simple and doesn’t cause any trouble. Interestingly, both the very early Chen DCT factorization and the LL&M DCT factorization turn into algorithms with 22 FMAs and 4 adds when you apply this, and other FMA-optimized DCT algorithms use 26 ops as well. Interesting. Anyway, fixed-point is more bothersome: Every multiplication causes round-off error so you don’t want to have too many of them, or paths with a lot of multiplies in them. Also, multiplying by values with an absolute value larger than 1 (or 0.5, depending on the instruction set) is bothersome for fixed-point SIMD implementations. I haven’t decided yet what I’ll use.

Closing note: Don’t forget that arithmetic is only half of it – in this case, almost literally: I have a (untested, so beware) prototype implementation of a floating-point, FMA-based algorithm in a JPEG-like setting on Xbox 360. Half of the time in an 8×8 IDCT is actually spent doing the IDCT, the rest is loading, unpacking, tranposing, packing and storing. Still, the overall cost seems to be about 4.5 cycles per pixel (as said, not final code, so this might either increase or decrease by the time I’m done), so it’s not too bad. It also illustrates another point about image/video compression: The goddamn entropy coder ruins everything. 4.5 cycles per pixel for the IDCT is one thing, but you still have to decode the coefficients first. Chances are you need at least one variable-amount shift per coefficient during entropy decoding, and on the Cell/Xbox 360, these don’t come cheap – they’re microcoded, *slow*, and they block the second hardware thread while they run. And to add insult to injury, bitstream decoding is an inherently serial process while the rest is usable amenable to SIMD and parallelization. And yet none of our existing multimedia formats are designed to be efficiently decodeable using multiple cores; the current H.265 proposals started taking this into account, but virtually everything else is still completely serial. This particular bottleneck is going to stay with us for a long time.

Interesting post!

I agree about the entropy decoding part, it’s very problematic. You can only parallelize 60-80% of the decode of JPEG in most images (either too small to amortize the cost of thread creation and entropy block skipping or no support for resync markers).

I’ve written my own research x86 JPEG decoders (3rd iteration, 4th being written) and here is the single-threaded performance I get for doing a complete decode (32-bits only for now) :

– Core 2 Duo E6600 : 21.4 cycles/pixel

– Core i5 M430 : 16.3 cycles/pixel

The test material is a 40MP photo in YCrCb with no sub-sampling and is decoded to RGBA.

(–> not much shuffling in the color-space converter)

As I’ve spent most of my time working on Huffman decoding, I used J.M.P. van Waveren’s iDCT decoder as it’s pretty good. I enhanced it a bit by grouping all 4 xmm (4×16 = 64 bytes = 1 cache line) writes at the very end to enable the CPU to do write combining.

I’ll try to profile the iDCT in the coming days to see where it stands and report back if you’re interested.

Please, keep up with the good posts man! :-)

” And to add insult to injury, bitstream decoding is an inherently serial process…”

There is still the probabilistic trick some HW does for CAVLC: Guess what might be coming and decode next-next symbol based on that guess in parallel. If the guess turned out to be right, you saved some time. But yeah, I would not call this “parallelization” either ;)

And you can always ‘unpack’ the next frame while progressing on the current frame’s coefficients in a parallel way (on the cost of buffer space and higher bus loads).

The first one is just speculative execution applied to decoding. A reasonable approach, but just as serial as the first one: even if you had perfect prediction, you’d still just be decoding two symbols at a time instead of one – it’s still serial.

The second one is conceptually the same as pipelining, and inherently limited by the number of pipeline stages you can add and the level of balance you can achieve. That will allow you to get your video decoder from single-threaded to dual-threaded, but you still have the entropy decoding stage as one monolithic block that can’t easily be split further. And even in the best case, it won’t give you a 2x speedup, since the post-entropy stages now read their input from the L2 cache or even L3/memory instead of L1. I wouldn’t worry too much about memory/bus BW, at least on PCs – they’ve got plenty of bandwidth to burn. Embedded devices are another matter entirely, though :)

Relevant to your interests: https://people.xiph.org/~xiphmont/AOM/Daala-TX.pdf

Oops, meant to link: https://datatracker.ietf.org/meeting/100/materials/slides-100-netvc-daalaav1-update-on-transforms-00 (both are relevant but there isn’t much context on the first)

Note that this blog post is 8 years old! (No idea why it’s on HN now.)

PMULHRSW etc. are nice when you get them. Our currently shipping codes don’t get to use integer multiplies at all in either the transforms or motion compensation filters because they had to work on the Xbox 360, which removed all integer multiplies from the SIMD units (to free up encoding space and area for other features they put in instead).

Lifting-based is fine when you have decent precision for your factors but is noticeably non-orthogonal when you use heavily quantized factors for a shift-and-add based implementation, enough so to cause noticeable efficiency loss in standard trellis quantization. (The cost function even in the L2 metric is not really separable.)

For these reasons Bink 2 went with a scaled but orthogonal integer transform instead. Design detailed at https://fgiesen.wordpress.com/2013/11/04/bink-2-2-integer-dct-design-part-1/ and https://fgiesen.wordpress.com/2013/11/10/bink-2-2-integer-dct-design-part-2/ – these two are merely 5 years old, spring chickens relative to this post! :)