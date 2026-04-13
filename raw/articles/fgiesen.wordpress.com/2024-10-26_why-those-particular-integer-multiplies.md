---
title: Why those particular integer multiplies?
url: https://fgiesen.wordpress.com/2024/10/26/why-those-particular-integer-multiplies/
published: '2024-10-26'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Why those particular integer multiplies?

The x86 instruction set has a somewhat peculiar set of SIMD integer multiply operations, and Intel’s particular implementation of several of these operations in their headline core designs has certain idiosyncrasies that have been there for literally over 25 years at this point. I don’t actually have any inside information, but it’s fun to speculate, and it gives me an excuse to waffle about multiplier designs, so here we go!

### MMX

x86 doesn’t have explicit SIMD integer operations before MMX, which first showed up in – no big surprise – the Pentium MMX. Said Pentium MMX offers exactly three SIMD integer multiply instructions, and all three of them originally took 3 cycles (fully pipelined).

The first and most basic one is `PMULLW`

, “packed multiply low word”, which interprets its two 64-bit MMX register operands as containing four words (which in x86, if you’re not familiar, means 16-bit integers) each. The corresponding lanes in both operands are multiplied and the low 16 bits of the result written to the corresponding lane of the destination. We don’t need to say whether these integers are interpreted as signed or unsigned because for the low 16 bits, it doesn’t matter. In short, it’s a basic element-wise multiply working on 16-bit ints.

The second available integer multiply is `PMULHW`

, “packed multiply high word”. Again, we multiply 16-bit lanes together, which (in general) yields a 32-bit product, and this time, we get the top 16 bits of the result. This time, we need to make up our mind about whether the integers in question are considered signed or unsigned; in this case, it’s signed. A fun fact about “high multiply” type operations (which exist in a lot of instruction sets) is that there’s no practical way (at least, not that I’m aware of) to compute *just* those high bits. Getting those high bits right generally means computing the full product (in this case, 32 bits per lane) and then throwing away the bottom half. Therefore, a datapath that can support both types of multiplies will usually end up having a full 16×16->32-bit multiplier, compute all product bits, and then throw half of them away in either case.

That brings us to the third and last of the original Pentium MMX’s multiply-type instructions, and the most fun one, which is `PMADDWD`

. I think this originally stands for “packed multiply and add words to doublewords”. That makes it sound like it’s a multiply-add type operation, but really it’s more like a two-element dot product: in pseudocode, `PMADDWD`

computes `result.i32[i] = a.i16[i*2+0] * b.i16[i*2+0] + a.i16[i*2+1] * b.i16[i*2+1]`

. That is, it still does those same four signed 16×16-bit multiplies we’ve been doing for the other two instructions, but this time with a “use the whole pig” attitude where the full 32-bit results are most definitely not tossed out. If we can’t return the whole result in a 16-bit operation, well, just pair even and odd pairs of adjacent lanes together and sum across them. Because when we’re summing across pairs of adjacent lanes, we get 32 bits to return the result in, which is perfect (we don’t need to worry about overflow here because the two constituent products were signed; they can’t get too large).

Now, this description sounds like we’re still finishing computation of 32-bit results for each of the 16 bit lanes, and then doing a separate 32-bit addition after to combine the two. That’s a possible implementation, but not necessary; this is not a post about how multiplications are implemented (some other time, maybe!), but the gist of it is that multiplier hardware already breaks down N-bit by N-bit multiplies into many smaller multiplications (the “partial products”) of a N-bit number by a much smaller digit set. The obvious one would be N-bit-1 bit products, which leaves just “x*0” and “x*1” products, but in practice other options are much cheaper. The partial products are then summed together in a kind of reduction tree, and again, there’s slicker ways to do it than just throwing down a whole bunch of fast adders, but the details don’t matter here. What *does *matter is that you can have either of the even/odd 16-bit multipliers do their normal thing until very close to the end, and then do the “cross-over” and final 32-bit summation very late (again with plenty of hardware reuse compared with the 16-bit result paths).

In short, not only does `PMADDWD`

let us use both 32-bit results *that we already computed anyway* fully, it also doesn’t touch the first 90% of the datapath at all and can be made to share plenty of logic with the regular path for the final 10% too if desired. Which is why it’s fun.

### SSE

The headline item for SSE was SIMD floating point operations (not my subject today), but it also patched a hole in the original MMX design by adding `PMULHUW`

(packed multiply high unsigned word). This one does the multiply unsigned and gives you the high word result. Once again, this is a minor change to the hardware.

### SSE2

This one added 128-bit integer SIMD whereas MMX was just 64-bit. It did so, in its initial implementations, by adding 128-bit registers, but still used a 64-bit datapath and issuing instructions over two cycles. Not surprisingly, then, all the SSE2 integer multiply instructions (and in fact the vast majority of SSE/SSE2 instructions in general) can be understood as working on independent 64-bit blocks at a time. (AVX/AVX2 would later do the same thing with 128-bit blocks.)

It does however add the rather awkward-seeming `PMULUDQ`

(packed multiply unsigned doubleword to quadword), which multiplies two pairs of unsigned 32-bit integers (in bits [31:0] and [95:64] of either source) to give two 64-bit results. And it does so with the same latency as our 16-bit multiplies! Is that a much wider multiplier at work?

Turns out, not necessarily! Let’s look at a single 32-bit product `a * b`

, and split `a = (a1 * 65536) + a0`

and `b = (b1 * 65536) + b0`

. 65536 is of course 216 and we’re really just chopping a and b in half. Multiplying that out, we get:

```
a * b
=((a1 * b1) << 32) + ((a1 * b0 + a0 * b1) << 16) + (a0 * b0)
```


Wait a second. Those are two 16-bit by 16-bit multiplies (unsigned this time, but we added that capability back with the first SSE) and a PMADDWD-style operation (albeit also on unsigned values) in the middle. We do need four 16×16-bit multiplies total… but we’re producing a 64-bit result, so our result area covers four 16-bit lanes’ worth. So this time we do need a bit more logistics up front to route the individual pieces of a and b to four separate multipliers over our 64-bit result area to line up our individual products, and we also have a somewhat more complicated final output stage (what with the different alignments of the results) and actually need a mode in the multiplier where we run a full 64-bit add, not just 32-bit adds, to produce or results. In short, it does get more complicated, but we’re still getting to build it all around the 16×16-bit multipliers we’ve had since MMX.

### SSSE3

SSSE3 adds two more multiply operations, both of which are variations on themes we’ve seen so far, but let’s start with the simple one first.

That would be `PMULHRSW`

, Packed Multiply High Rounding Shifting Words (again, not the official name). It’s another signed 16×16 bit multiply. This one computes signed (not the official way it’s specified, but it’s equivalent) `(a * b + 0x4000) >> 15`

. This requires a slight tweak to the reduction tree to in the multiplier to sum in one extra term somewhere that we can use for the rounding bias. Grabbing different output bits from the result is not a big deal.

The more complicated one is `PMADDUBSW`

which is like `PMADDWD`

but on pairs bytes not words, and to keep things interesting, it’s an unsigned*signed multiply. I think this might have been inspired by AltiVec (or maybe there’s a common ancestor I’m not aware of?) which had this type of operation in its “msum” family of instructions (alongside a PMADDWD equivalent and some other operating modes), but the AltiVec version is nicer because it’s a 4-element dot product on bytes producing a 32-bit result. PMADDUBSW produces a word result which, in turns out, does not quite work. The problem is that multiplying unsigned by signed bytes means the individual product terms are in range [-128*255, 128*255] = [-32640,32640]. Our result is supposed to be a signed word, which means its value range is [-32768,32767]. If the two individual products are either near the negative or positive end of the possible output range, the sum overflows. PMADDUBSW decides to saturate the result, i.e. clamp it to lie within [-32768,32767] instead. This is well-defined but frequently quite annoying to work with.

In terms of implementation, I’ve not actually worked out the details here. I will point out that one way of designing multipliers is to use a few levels of a recursive decomposition into smaller multipliers much as I just did with `PMULUDQ`

; chopping the constituent 16-bit multipliers up into byte pieces would presumably work, although at this point, we don’t just have some extra muxing near the beginning or end of the datapath, we’re also starting to add a lot of constraints on the rest of the internal implementation (if we’re trying to share as much hardware as possible, that is). We’ve just about pushed this as far as we can go.

### SSE4.1

SSE4.1 adds `PMULDQ`

which is `PMULUDQ`

, but signed. The same basic approach as `PMULUDQ`

should work, so I’ll not get into it.

It also added the at that point long-awaited `PMULLD`

, doubleword-by-doubleword low multiplies. To date, we have not gotten any high multiplies for them, not in SSE4.1 nor in any subsequent extension, and it seems unlikely at this point.

Curiously, with PMULLD, something’s different: these have half the throughput and twice the latency as all the other multiply-type operations on Intel’s big core designs, and take two uops whereas all the other multiply-type operations mentioned so far take one.

Once again, I think the divide-and-conquer approach described for `PMULUDQ`

above explains both. Looking at the product terms:

```
a * b
=((a1 * b1) << 32) + ((a1 * b0 + a0 * b1) << 16) + (a0 * b0)
```


We don’t care about the high product term for a1 * b1 since we’re only returning the low 32 bits anyway. But we do need the other three product terms, and per each 32-bit result lane, we only have two 16×16 multipliers to work with. My best guess is that the first uop is a PMADDWD-like affair that computes the `(a1 * b0 + a0 * b1)`

portion and stashes the low 16 bits of the result, and the second uop gets issued immediately after and computes a regular `a0 * b0`

32-bit product in the low 16-bit lane then adds it together with the stashed product (shifted by 16, but that’s just wiring) – this is again a fairly minor variation of the logic that is used for PMADDWD. In short, I think a possible implementation of PMULLD on top of the 16-bit-multiplier-centric datapath that Intel seems to have been bolting more and more features onto for the past 25 years is using 2 uops that are slight variations of the PMADDWD flow, and it would be consistent with the somewhat odd characteristics of the instruction on Intel’s big cores.

### Is any of this definitive?

Oh hell no it’s not. But it would make sense given how the whole thing seems to have developed, and it fits available data.

Would I design a new unit this way now if I had to support all these instructions? Probably not. The original MMX/SSE-era design doesn’t need to do a lot of operations and is pretty sweet, but the doubleword->quadword multiplies in SSE2 started to muddle the waters, SSSE3 with PMADDUBSW (which although useful is very odd) made the 16-bit slices have to support some pretty odd things that really break out of a conventional multiplier dataflow (like the internal saturation), and as of SSE4.1 with PMULLD, honestly, instead of teaching this old dog the umpteenth new trick, maybe just throw some actual 32×32->32 multipliers in there as well instead of adding complications. That seems to be what AMD has done, as well as Intel’s E-cores. But it’s still fun to speculate!

### What about AVX-512 VPMULLQ, IFMA or VNNI?

The original VNNI is a pretty straightforward generalization of the PMADDWD/PMADDUBSW designs to include a final accumulation too, much like the aforementioned `vmsum`

family of instructions in PowerPC. I have a suspicion this might be due to a combination of a) x86 SIMD datapaths post-AVX2 (which added FMAs) having native support for 3-operand instructions and b) quite possibly some AltiVec-era instruction patents having expired in the meantime. For a), the extra addition is not the hard part (as mentioned above, the extra term is very natural to sneak into any multiplier datapath), the actual cost is all in the extra wiring and bypassing to have a 3-operand datapath. But once it’s a sunk cost because you want float FMAs anyway, might as well use it! For b), I have no idea whether this is the case or not, it’s just funny to me that AltiVec had these integer dot product instructions from the standard while x86 took forever to add them (after people used PMADDUBSW with a follow-up PMADDWD by an all-1’s vector literally just to sum the pairs of words in a 32-bit lane together for something like a decade).

IFMA is a completely different story because even though it’s an integer multiply, it’s very clearly designed to use the double-precision multiplier in the floating-point datapath. Completely different multiplier with a different set of fun design constraints!

VPMULLQ, I have nothing to say about. Literally haven’t ever looked into, or tried to figure out, how it’s implemented. Might do so at some point, but not today!

And I think that’s all of them.

`VPMULLQ`

is 3 uOps on Intel, which, to me, makes sense if you’re feeding it through a 32×32 -> 64b multiplier.If everything is using 16x16b multipliers, you’d think

`PMULLD`

and`PMULUDQ`

should have the same uOp count. If`PMULUDQ`

can do everything in 1 uOp, why can’t`PMULLD`

, which theoretically can do less work per lane, since it can skip the top 16x16b multiply?My theory is that there’s 32x32b multipliers, but only on every second lane. This directly maps to

`PMULUDQ`

, whilst`PMULLD`

has to feed the inputs through twice, thus two uOps. This also lines up with`VPMULLQ`

– it does the same as`PMULLD`

, but needs a third uOp for the remaining multiply*One odd thing about my theory is the instruction latencies – it’d suggest that the internal uOps can’t pipeline amongst themselves, so

`PMULLD`

has twice the latency of`PMULUDQ`

, and`VPMULLQ`

has triple that of`PMULUDQ`

.“If PMULUDQ can do everything in 1 uOp, why can’t PMULLD, which theoretically can do less work per lane, since it can skip the top 16x16b multiply?”

I go over this in the post. It’s not less work per lane. PMULUDQ needs four 16×16 multipliers per 64b lane, which are available, since one 64b lane spans four 16b lanes. PMULLD needs 3 16×16 multipliers per 32b lane, out of 2 available. PMULUDQ also existed (with the same uOp decomposition) from SSE2 (P4) through to SSE4.1 (Nehalem) when PMULLD was finally introduced, 8 years later, and all the preceding pipelines (and P4/Core 2 variant) stick with 16b-type multiplies only. It just seems more likely to me that PMULUDQ is mapped to 16-bit multipliers at least for that time rather than using a dedicated even-lane-only 32x32b multiplier that’s not exposed or used for anything else.

Karatsuba is not appealing here since it needs a very different adder topology on the output stage and a completed carrying add before the Booth recode stage. That’s a very different pipeline, not just a bit of extra muxing in the first and final stages. It would be very hard to fit into the regular multiplier design. Karatsuba does eventually become interesting, but your operands generally need to be more than just 2x larger than your underlying multiplier to justify it.

Ah, your second explanation makes more sense to me – thanks for the clarification!

I’m just a software person, so have no clue on hardware, so appreciate the explanation as well.

If we’re bringing in the double precision FMAC, then “32×32 multiplier every second lane” would technically be true, since 52×52->104b can accommodate that.

It’s worth noting that the IFMA instructions have a latency of 4 cycles, whilst the single uOp integer multiplies are 5 cycles.

If we use the idea that

`PMULLD`

is kinda like two chained`PMADDWD`

s, its latency of 10 cycles makes sense.`VPMULLQ`

has a latency of 15 cycles though, which numerically feels like it’d fit in more with 3 chained integer multiplies than IFMA’s 4 cycle ops. If`VPMULLQ`

took a similar approach to`PMULLD`

but with the 52b multiplier, you’d think the latency would be 3×4=12 instead of 15. Perhaps there’s a one cycle penalty for moving stuff around per multiply.`VPMULLQ`

did also appear before IFMA, though that probably doesn’t mean much.For what it’s worth, my leading candidate for VPMULLQ is using the significand path for the double precision float multiplier. That can do 52×52->104 bit (same as for IFMA). Not enough for 64×64->64 in one single go, but the usual three ops will work (up to some shifting/muxing).