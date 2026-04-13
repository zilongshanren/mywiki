---
title: 'SSE: mind the gap!'
url: https://fgiesen.wordpress.com/2016/04/03/sse-mind-the-gap/
published: '2016-04-03'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# SSE: mind the gap!

SSE and SSE2 are available in every single x86-family CPU with 64-bit support. You too can play around with SIMD, which is great fun! Unfortunately, SSE2 level in particular also happens to be what is probably the most maddeningly non-orthogonal SIMD instruction set in the world, where operations are either available or not available for particular data types with little rhyme or reason, especially where integers are involved. Later revisions (especially starting around SSE4.1) fill in some of the more annoying gaps, but plenty of us are stuck with supporting the older CPUs for at least a few more years, and besides – not to mess with the *authentic SSE experience* – even on AVX2-supporting CPUs, there’s still a few of the classic gaps remaining.

So, here’s a list of tricks to get you around some of the more common, eh, “idiosyncrasies” of SSE and its descendants. This happens to be mostly focused on the integer side; the floating-point side is generally less, well, weird. I’ll keep the individual descriptions relatively brief since the whole point of this post is to collect lots of tricks. The assumption here is that you’re already somewhat familiar with the instructions, so I’ll not explain the basics (maybe another time). I’ll use the official Intel intrinsics (as exposed in C/C++) since that’s probably the most common way people interact with these instructions *intentionally* (awkward glance in the direction of auto-vectorization here. No making eye contact. Moving on.)

### Branchless “select” (cond ? a : b)

The natural mode of operation in SIMD computations is to do things branchlessly. If some part of a computation is conditional, rather than doing the equivalent of an `if`

, it’s more typical to do both the computation for the “if” and “else” forks, and then merge the results based on the condition. The “select” I mean is the operation which takes the condition and both results and performs the rough equivalent of C’s ternary operator `cond ? a : b`

. You first evaluate both sides, giving `a`

and `b`

. You then evaluate the condition using a SIMD compare, which returns a vector containing a bit mask that is has all bits set for lanes that meet `cond`

, and all bits clear for lanes that don’t.

This select operation can always be done using a few bitwise operations (which is well known), but starting in SSE 4.1 we get slightly more efficient variants too (less well known, and the reason I mention this):

- Integer (all vers):
`_mm_or_si128(_mm_and_si128(a, cond), _mm_andnot_si128(cond, b))`

. - 32-bit float (all vers):
`_mm_or_ps(_mm_and_ps(a, cond), _mm_andnot_ps(cond, b))`

. - 64-bit float (all vers):
`_mm_or_pd(_mm_and_pd(a, cond), _mm_andnot_pd(cond, b))`

. - Integer (SSE4.1+):
`_mm_blendv_epi8(a, b, cond)`

. - 32-bit float (SSE4.1+):
`_mm_blendv_ps(a, b, cond)`

. - 64-bit float (SSE4.1+):
`_mm_blendv_pd(a, b, cond)`

.

The `andnot`

operations don’t come in handy very often, but they’re the best choice here (pre-SSE4.1).

If you don’t want to use `cond`

but its logical negation, just switch the positions of `a`

and `b`

, since `(!cond) ? a : b`

is the same as `cond ? b : a`

.

### Unsigned integer compares

SSE, in all incarnations, offers precisely two types of integer comparisons: test for equality (`PCMPEQt`

, `_mm_cmpeq_T`

, where t and T stand for various type suffixes) and test for signed greater-than (`PCMPGTt`

, `_mm_cmpgt_T`

). Most other comparison types can be produced using nothing but logical negation and standard identities:

`a == b`

is supported directly.`a != b`

is`!(a == b)`

.`a > b`

(signed) is supported directly.`a < b`

(signed) is the same as`b > a`

(swap a and b).`a >= b`

(signed) is`!(a < b)`

(which in turn is`!(b > a)`

).`a <= b`

(signed) is`!(a > b)`

.

See previous note on selection operations on how to get rid of the NOT in the most common use case. Conspicuously absent from that list is any type of *unsigned* ordered comparison. However, a trick that works is to bias both integers so that signed comparison does the right thing:

`a > b`

(unsigned, 8-bit) is the same as`(a - 0x80) > (b - 0x80)`

(signed, 8-bit).`a > b`

(unsigned, 16-bit) is the same as`(a - 0x8000) > (b - 0x8000)`

(signed, 16-bit).`a > b`

(unsigned, 32-bit) is the same as`(a - 0x80000000) > (b - 0x80000000)`

(signed, 32-bit).

The same argument-swapping and NOT-ing tricks as above still apply to give you the other compare types. In general, the trick is to add (or subtract, or XOR – they all do the same thing in this particular case) the INT_MIN for the respective type from both operands before doing the compare. This turns the smallest possible unsigned integer, 0, into the smallest possible signed integer for the given type; after that, the ordering works out. In particular, when comparing against a constant, this addition (or subtraction, or XOR) can be baked into the constant operand, so the unsigned compare “only” ends up doing one more operation than a signed compare (instead of two).

A completely different approach is to use the unsigned integer min/max instructions (more about those in a second) to build less-or-equal or greater-or-equal comparisons:

`a <= b`

if and only if`max(a, b) == b`

.`a >= b`

if and only if`min(a, b) == b`

.

The good news is that this reduces unsigned comparisons to either an unsigned min or a max, followed by an equality comparison, which is only 2 instead of 3 operations. The bad news is that the requisite unsigned min/max operations only exist for uint8s in SSE2. The uint16/uint32 variants were finally added with SSE4.1; if your minimum target is earlier, you’re stuck with the bias-then-compare variants above.

### Integer min and max

SSE4.1 has the full set of integer min/max for 8-, 16- and 32-bit types, both signed and unsigned. So if you’re targeting SSE4.1 or later, good for you!

If you’re stuck with anything earlier, you’re decidedly more limited. In SSE2, you get integer min/max for uint8 and int16. If you need min/max for int8, uint16, or anything 32-bit, you’re on your own.

Luckily, we can just combine some of the techniques above to derive a solution. The general patterns here are:

max(a, b) == (a > b) ? a : b; min(a, b) == (a > b) ? b : a;

So this is just a combination of a compare and a “select” operation. When the compare is signed (the int8 and int32 cases), the comparison maps to a single SSE intrinsic. The unsigned compares (uint16 and uint32) can be solved using the bias-then-signed-compare trick which in turn gives us an unsigned min/max.

### 32-bit and 64-bit loads/stores

This one has nothing to do with the actual instruction set and everything to do with the intrinsics: yes, SSE2 has 32-bit (`MOVD`

) and 64-bit (`MOVQ`

) loads and stores, the standard intrinsics just do their best to confuse you about it:

- 64-bit loads are
`_mm_loadl_epi64`

. This intrinsic takes a`__m128i *`

as an argument. Don’t take that seriously. The actual load is 64-bit sized, not 128-bit sized, and there is no alignment requirement. - 64-bit stores are
`_mm_storel_epi64`

. Again, the`__m128i *`

is confusing and does not mean that the actual store is 128-bit or that there are alignment requirements. It isn’t and there are not. - 32-bit loads are even more hidden! Namely, you write
`_mm_cvtsi32_si128(*x)`

where`x`

is a pointer to a 32-bit integer. No direct load intrinsic, but compilers will turn this into a`MOVD`

with memory operand where applicable. - 32-bit stores, likewise:
`*x = _mm_cvtsi128_si32(value)`

. Now you know.

### Multiplies

There’s lots of different ways to provide multiplies in a SIMD instruction set, and by now SSE has tried most of them in one form or another.

Let’s start with the (historically) first variant: multiplying 16-bit numbers. The relevant instructions originated in the Pentium MMX and compute the low and high halves (bottom and top 16 bits) of a signed 16-bit×16-bit product. MMX only has signed multiplies, but SSE also added a “high half of unsigned 16-bit times 16-bit product” instruction (the low halves of signed and unsigned products are identical), so we’re not gonna have to worry about *that* particular problem, not yet anyway.

These instructions are fine if you want the low or high halves of the product. What if you want the full 32-bit product of vectors of 16-bit values? You compute the low and high halves and then merge them using the “unpack” instructions. This is the standard approach, but not very obvious if you haven’t deal with this kind of thing before. So for a full 16×16→32-bit product (note this produces two vectors worth of results), we get:

// EITHER: a*b (16-bit lanes), signed __m128i lo16 = _mm_mullo_epi16(a, b); __m128i hi16 = _mm_mulhi_epi16(a, b); // OR: a*b (16-bit lanes), unsigned __m128i lo16 = _mm_mullo_epi16(a, b); __m128i hi16 = _mm_mulhi_epu16(a, b); // THEN: merge results __m128i res0 = _mm_unpacklo_epi16(lo16, hi16); // result lanes 0..3 __m128i res1 = _mm_unpackhi_epi16(lo16, hi16); // result lanes 4..7

But what if you’re working with 32-bit values? There is a 32×32→32-bit product (`PMULLD`

/ `_mm_mullo_epi32`

), but it was only added with SSE4.1, and it’s significantly slower than the other SSE2 multiplies in many implementations. So you might either not want to set your minimum target that high, or you might be looking for something quicker.

There’s full 32×32→64-bit products, which are available from SSE2 on as

`PMULUDQ`

/`_mm_mul_epu32`

(unsigned). SSE4.1 adds the signed equivalent `PMULDQ`

/`_mm_mul_epi32`

(**UPDATE**: An older version of this post incorrectly stated that PMULDQ was SSE2. Thanks Exophase for pointing it out!). These ones only compute two products (between the even lanes of the two sources) and place them in a 128-bit result. The odd 32-bit lanes are ignored completely, so if you want four 32×32→32-bit products, you need at least two of these multiplies and a lot of wrangling:

// res = _mm_mullo_epi32(a, b) equivalent using SSE2, via PMULUDQ. // even and odd lane products __m128i evnp = _mm_mul_epu32(a, b); __m128i odda = _mm_srli_epi64(a, 32); __m128i oddb = _mm_srli_epi64(b, 32); __m128i oddp = _mm_mul_epu32(odda, oddb); // merge results __m128i evn_mask = _mm_setr_epi32(-1, 0, -1, 0); __m128i evn_result = _mm_and_si128(evnp, evn_mask); __m128i odd_result = _mm_slli_epi64(oddp, 32); __m128i res = _mm_or_si128(evn_result, odd_result);

It works, but it’s a mouthful.

But what if you’re using 32-bit vector lanes, but happen to know that the numbers we’re trying to multiply are in fact in the range [-32768,32767] (i.e. representable as signed 16-bit integers)? We could try narrowing the 32-bit lanes into 16 bits then using the 16×16→32 sequences above, but is that really the best we can do?

It is not: `PMADDWD`

(`_mm_madd_epi16`

), MMX/SSE2’s amazing and strange (but mostly amazing) dot product operation, has our back, for we can do this:

// a and b have 32-bit lanes with values that fit in int16s. // produces the 32-bit result // res[i] = a[i] * b[i] // clears high 16 bits of every 32-bit lane __m128i bm = _mm_and_si128(b, _mm_set1_epi32(0xffff)); // after this, madd_epi16 does what we want! __m128i res = _mm_madd_epi16(a, bm); // can swap role of a and b above too, when convenient.

That’s a lot shorter than narrowing to 16-bit first would be! Alas, it only works for int16 (signed). What if we’re working in 32-bit lanes with values that fit inside a uint16 (unsigned)? It’s not quite as slick, but still, better than narrowing to 16-bit first or dealing with the logistics when synthesizing 32×32→32-bit muls from `PMULDQ`

/`PMULUDQ`

:

// a and b have 32-bit lanes with values that fit in uint16s, // i.e. a[i] == (uint16)a[i] and same for b[i]. // // produces the 32-bit result // res[i] = a[i] * b[i] // compute low and high 16-bit products __m128i lop = _mm_mullo_epi16(a, b); __m128i hip = _mm_mulhi_epu16(a, b); // merge results __m128i res = _mm_or_si128(lop, _mm_slli_epi32(hip, 16));

### Horizontal adds, dot products etc. (float)

SSE3 adds horizontal adds `HADDPS`

(`_mm_hadd_ps`

) and `HADDPD`

(`_mm_hadd_pd`

) and SSE4.1 throws in the dot-product instructions `DPPS`

(`_mm_dp_ps`

) and `DPPD`

(_mm_dp_pd).

Generally, don’t expect these operations to be magic. They exist in the instruction set but are fast precisely nowhere; in all x86 implementations I’m familiar with, they just turn into a canned sequence of more basic (SSE2-level) operations. So more often that not, you will end up requiring a higher minimum CPU target for little to no speed gain. Caveat: these instructions *are* a smaller than their replacement instruction sequence, so using them can reduce code size slightly. But still, don’t expect this to be fast.

If you want good SIMD performance, don’t lean on horizontal and dot-product style operations; process data in batches (not just one vec4 at a time) and [transpose](https://fgiesen.wordpress.com/2013/07/09/simd-transposes-1/) on input, or use a [SoA layout](https://software.intel.com/en-us/articles/memory-layout-transformations) to begin with.

### The other kind of horizontal adds, dot products etc. (integer)

SSE *does* have a bunch of horizontal add and dot product-style operations that don’t suck, but they’re on the integer pipe, and not what you’d expect.

Nope, not `PHADDW`

/`PHADDD`

(`_mm_hadd_epi16`

/`_mm_hadd_epi32`

). These are SSSE3 and later only and OK but not particularly great (similar disclaimer as for the floating-point horizontal adds applies).

No, I’m talking about `PMADDWD`

(`_mm_madd_epi16`

, SSE2 with its ancestor around since the original MMX), `PSADBW`

(`_mm_sad_epu8`

, SSE2) and `PMADDUBSW`

(`_mm_maddubs_epi16`

, SSSE3). The official manuals describe what these instructions do, so I won’t bother going into too much detail, but here’s the basic idea: `PMADDWD`

and `PMADDUBSW`

are 2-element dot-product instructions between pairs of adjacent SIMD lanes. `PMADDWD`

computes two int16 by int16 products for each pair of 16-bit lanes and sums the 32-bit integer products to yield the 32-bit result lanes. `PMADDUBSW`

computes two uint8 by int8 products for each pair of 8-bit lanes and sums the 16-bit integer products to yield the 16-bit result lanes. These can be used to compute dot products of this problem; but they also have “degenerate” configurations that are very useful:

`_mm_madd_epi16(x, _mm_set1_epi16(1))`

sums the 16-bit even and odd lanes of x in pairs to yield 32-bit results.`_mm_maddubs_epi16(_mm_unpacklo_epi8(a, b), _mm_setr_epi8(1, -1, 1, -1, ..., 1, -1))`

happens to be the fastest way to compute the 16-bit signed differences between 8-bit unsigned vectors`a`

and`b`

on processors that support SSSE3.- The 16-bit multiply example above shows another special configuration.

Long story short, these dot product instructions are surprisingly versatile in decidedly non-obvious ways.

Finally, `PSADBW`

(`_mm_sad_epu8`

, SSE2). This one is intended for motion estimation in video codecs, but it also happens to be the one actually really fast horizontal add you get on x86. In particular, `_mm_sad_epu8(x, _mm_setzero_si128())`

computes two 16-bit horizontal sums of groups of 8 uint8 lanes in a single, and quite fast, operation. We can do the same trick we did for compares in reverse to compute the sum of 8 int8s instead: add (or subtract, or XOR) `_mm_set1_epi8(-128)`

to `x`

(before the `PSADBW`

), the subtract 128×8 from the resulting 16-bit sums.

### To be continued!

There’s a lot more of these, but this feels like enough to chew on for a single blog post. So there will be a sequel covering, at least, integer widening/narrowing and variable shifts. Until then!

What do you think of auto-vectorization? You made a remark about it.

I’m not the author, but I can tell you my experiences with my code haven’t been that positive using either GCC or ICC. In fact, the latest ICC is a little slower than the latest GCC. This is with code that had a lot of vectorizing potential, something I know because I wrote it with SIMD in mind and hand-converted most of it to NEON assembly. There are some ways in which the SSE equivalent is a lot worse due to lacking NEON features, but I still got huge improvements over auto-vectorization with hand-written SSSE3. Like a factor of 2-3x, and this is vs auto-vectorization targeting AVX-128 no less.

The code is almost entirely integer and does a lot of width conversions. The thing is that it’s not that the compiler failed to vectorize anything, it’s more that it vectorized things in a really bad way.

PMADDWD is awesome, indeed. You can use it for complex multiplies as well, IIRC.

Another great one is PSHUFB (if you have it), mainly because it’s so insanely fast, so for almost any operation you can specify in terms of it, it will be the fastest. But I suppose that’s in part 2 :-)

Sadly pshufb is another one of those instructions that’s mysteriously very slow on Atoms out so far. It takes a whopping 6 cycles on Saltwell and 5 cycles on Silvermont, and I mean back to back throughput, not latency.

Oh, and a different version of your blend that’s probably slower (less ILP) but needs one temporary less (so could be useful if you’re very starved for registers): a ^ ((a ^ b) & cond)

_mm_set1_epi32(0xffff)

can be replaced with

auto allOnes = _mm_cmpeq_epi32(_mm_setzero_si128(), _mm_setzero_si128());

_mm_srli_epi32(allOnes, 16);

which is more instructions, but avoids the memory access Visual C++ generates for constants in _mm_set1_XXX (often, you need every line of cache). Clang may be smarter.

You can also get allOnes by doing a pcmpeq (of any type) with the same value for both source operands.

But in this case it’s used for clearing the bottom 16-bits of a 32-bit lane, so if the goal is to avoid having to use a memory variable for a constant you could just do a 32-bit left shift of 16 followed by a right shift of 16.

Isn’t my code exactly the pcmpeq way you propose? (Compilers will merge the two setzeros to the same register)

You’re absolutely right about the shifts, another instruction saved :)

A constant 0xffff mask load can be hoisted out loops and moved into a register (or just turned into a load-op), two shifts can’t.

As a general rule, I would not recommend replacing constants with math sequences to compute them on anything newer than a Pentium 4. Load-op operands work really well on modern x86s, and your code should be able to make better use of execution resources than computing constants with them. (No matter your cache pressure, I’ve never found 1-2 cache lines spent on constants to be problematic.)

Besides, expressions such as these will be detected as loop-invariant by all major compilers and hoisted out of loops anyway (where they will then either be placed in a register or spilled to the stack). Don’t get fancy with stuff like this unless you’ve actually profiled it and found the loads to be a bottleneck.

Krishty; The point I’m getting at is that the operands don’t have to be initialized to anything. Like if you did this:

__m128i allOnes;

allOnes = _mm_cmpeq_epi32(allOnes, allOnes);

Presumably it’d compile to something like:

pcmpeqd xmm0, xmm0

While yours would presumably compile to something like:

pxor xmm0, xmm0

pcmpeqd xmm0, xmm0

It might optimize the pxor out but it’d be a pretty obscure optimization. On the other hand, the former might result in a warning because a variable is being used uninitialized.

@Exophase: (sorry, for some reason I can’t reply to your comment #7490 directly)

You’re right in that the register doesn’t have to be zero. However, an uninitialized triggers the worst possible code generation in VC 2015 x64 (a memory load!):

movdqa xmm0,xmmword ptr [rsp+30h]

pcmpeqd xmm0,xmm0

In ryg’s case, the optimal choice probably is recycling the register of the “b” variable.

@ryg: Of course constant shifts can be moved out of loops. It all depends on the use case. Another one is compiling for size. pcmpeqd + shifting is 5 + 5 B on x64, a 16-B global + movdqa is 16 + 6.

Great writeup. I too have gained a lot using pmaddubsw and psadbw in ways they weren’t meant to be used.

One minor correction: pmuldq is an SSE4.1 instruction, not SSE2. I was actually burned by the same mistake; I coded something up on my desktop using this instruction (Sandy Bridge, so AVX1 level) which then crashed on some of the targets (Saltwell Atoms on Android, SSSE3)

Initially I looked at using pmuludq with conditional negations. The problem there is that paddq and psubq are very slow on all Atoms, among some other frustrating performance problems.

My inputs were actually s32 * u15 -> s47. The u15 was designed deliberately so it could be used as a signed 16-bit value. I rewrote the code to compose the multiplication from several 16-bit multiplications and adds, which should have been slightly faster than the original pmuldq version, but definitely a lot harder to write.

Oops, thanks. Good catch!

For floating point branchless select we used c = b + (a – b) & cond:

__m128 t = _mm_sub_ps( arg1, arg2 ); // t = arg1 – arg2

return _mm_add_ps( arg2, _mm_and_ps( t, cond ) ); // r = arg2 + (t & cond)

This does not work with Inf & NaNs arguments though.

The reason is that on pre-Nehalem architectures the bitwise logic units live on the integer ports, and there is a latency cost from moving between the integer & floating point ports back and forth. Unfortunately not all of the “and” operations could be removed as you can see.

AFAIK post-Nehalem this trick makes no sense (and may be detrimental) as the floating point & integer units now have their own bitwise units, thus not incurring in the latency hit. Perhaps some Intel engineer could add more detail. Fun times.

Please don’t do *any* of that, ever! I’m sorry, but this is just seriously wrong in many different ways.

First, for floating-point numbers, even when no IEEE specials are involved, b+(a-b) != a generally. In particular, if |a| is significantly smaller than |b|, a-b rounds to -b and this will produce 0 not a. So this is just broken.

Second, there’s no such thing as “bitwise logic units that live on the integer ports” in any major x86 implementation, certainly not Intel’s. Not to nit-pick, but what you mean is clusters not ports; e.g. on Intel archs, ports 0, 1 and 5 handle all kinds of integer operations (scalar and SIMD both), but also plenty of floating-point operations. There’s no dedicated SIMD FP-only or SIMD int-only ports, although many types of operations are only available on one of the ports.

Now, x86 has several different types of bitwise logic instructions: they exist in SIMD Int (PAND, POR etc.), SIMD FP32 (ANDPS, ORPS etc.) and SIMD FP64 (ANDPD, ORPD) variants. In some implementations they’re all performed by the same units. In others (including all major Intel “big cores” since the Core 2) there are distinct SIMD integer and SIMD FP clusters, and crossing between these clusters has an extra 1-cycle data bypass latency.

However,

you only cross clusters when you use the wrong type of logic op. Using ANDPS on floats is not crossing clusters; using PAND is, but there’s no reason to use it to begin with. In every cluster, you have a version of the logic ops that doesn’t include extra latency, and that’s the versions I gave in the post.Third, even if using (the right types of) logic ops on floats caused a data bypass delay, which it does not, these delays occur on

crossingbetween different clusters. So if doing logic was on a different cluster, you would have 1 cycle latency for the operands to arrive at that cluster, and 1 cycle latency for the results to go back to the FP cluster. It’s not an extra latency on every operation; it’s just extra latency every time you switch clusters. So whether you do a single operation (e.g. the AND in your example) or several (e.g. AND, ANDN, OR) on that cluster doesn’t matter; it’s the same 2 crossings either way. If the logic ops were only on one cluster, they would still be able to transfer results between each other without extra delays.Fourth, the extra bypass latency is just that: latency. It’s

nota stall. It does not cost you any issue slots, and it does not reduce your throughput. Many people worry about latency way too much. As long as there’s other independent work to schedule, you’re good; latency only actually costs you when there’s nothing to for the core but twiddle thumbs until results are ready. That’s sometimes the case, but not nearly as often as people seem to think it is. In particular, in moderately-sized loops (say 40-50 instructions) with independent iterations, even if the work within an iteration is quite serial, out-of-order CPUs will naturally overlap the end of one iteration with the start of the next iteration. You really need to have one single, very long, dependency chain for latency to become the dominant concern.Fifth and last, what you’re suggesting replaces three 1-cycle instructions (ANDPS; ANDNPS; ORPS), two of which (the ANDPS and ANDNPS) can issue in the same cycle on several microarchitectures, with a sequence of three dependent instructions; ADDPS and SUBPS are 3 cycles latency each (on everything from Core2 through Haswell; 4 cycles on Skylake!) and the ANDPS is 1 cycle. Your code replaces a 2-cycle critical path with a 7-cycle one (9 cycles on Skylake), in a way that also loses precision. So this is a significant pessimization in terms of latency, not an improvement.

The variants I gave are generally the fastest. In certain situations you might want to instead use xor(a, and(xor(b, a), mask)) (for example, if either a or b needs to stick around for another computation, this can save a register), which is also 3 instructions and has a 3-cycle critical path (instead of 2 cycles on archs that can issue ANDPS and ANDNPS in the same cycle).

Ok ok, I get it! it’s bad.

“However, you only cross clusters when you use the wrong type of logic op. Using ANDPS on floats is not crossing clusters; using PAND is”

That’s where my knowledge differs from yours. It is my understanding that on Core2 architectures, using andps **still** needs to cross and that in fact in the Core2 archs issuing ANDPS or PAND is just the same. Hence the problem. Read this from Intel forums straight from an Intel engineer reply. Though Intel engineers have been wrong before, but carefully reading the manuals seemed to corroborate this.

The idea is that since both arguments (a, b) need to cross to perform the AND operation, then later again cross back to keep performing floating point operations with the result, it could add a latency of around 3-4 cycles. So those 2-3 cycles you mention become 5-7.

As for the cycle count, agreed it’s a bad idea on modern architectures (i.e. not Core2). In fact you convinced me to review some old code. I didn’t know the impact on Skylake was that bad (going from 2-3 cycles to 9 is bad!).

As for the precision problem, yeah that’s a given.

I just checked and you’re correct that Core 2 (so before NHM) runs logic ops on the int pipe; sorry about that.

However, the math you’re doing on latencies doesn’t work that way. The latencies for two operands that need to cross clusters don’t add; they overlap. The net effect of a N-cycle bypass delay is that the observed latency of the instruction that produces said operand is N cycles more than it would otherwise be.

That means that: 1. having two operands that cross clusters does not inherently introduce any extra delay; an instruction always waits for its “slowest” operand before it can issue. It’s about the critical path, not an additive cost. 2. unless one of the instruction’s operands is on the critical path, there is no observable extra delay at all. 3. in code that is throughput- not latency-limited (as said, the typical case for SIMD code), it doesn’t matter.

Skylake doesn’t “go from 2-3 cycles to 9”. The latencies for the float code you give are at best 7, as I mentioned (ADDPS and SUBPS are both 3 cycles latency, ANDPS at least 1). A FP add has 2 cycles extra latency than a logical op, so even with domain crossings in the mix, the FP ops don’t come out ahead.

Just so we’re in the same line, with Skylake I meant that an operation that could be running at 2-3 cycles (optimum version) ends up running in 7-9 cycles (controversial “b + a-b” version).

You’ve pretty much convinced me to revise that old code and just use the andps orps andnps version.

Since we’re into collecting tricks:

Flipping signs:

const float sign = valueWithSign >= 0 ? 1 : -1;

x *= sign;

y *= sign;

z *= sign;

SSE2 version:

const __m128 signMask = _mm_set1_ps( -0.0f );

const __m128 sign = _mm_and_ps( signMask, valueWithSign );

x = _mm_xor_ps( x, sign );

y = _mm_xor_ps( y, sign );

z = _mm_xor_ps( z, sign );

————————————————————————-

Horizontal min i.e. r = min( x, y, z, w ):

float r;

__m128 t0 = _mm_shuffle_ps( a, a, _MM_SHUFFLE( 2, 3, 2, 3 ) );

t0 = _mm_min_ps( a, t0 );

a = _mm_shuffle_ps( t0, t0, _MM_SHUFFLE( 1, 1, 0, 0 ) );

t0 = _mm_min_ps( a, t0 );

_mm_store_ss( &r, t0 );

If you’ve got a faster version for horizontal min/max I’m all ears :)

I don’t find _mm_and_epi32 in https://software.intel.com/sites/landingpage/IntrinsicsGuide/

What am I missing? I do see _mm_and_si128

It’s just a typo. It should be and_si128. Thanks!

Thanks for the great article. There’s a minor typo in the last paragraph. I believe you want to subtract 128×16 from the two 16 bit values