---
title: 'Entropy decoding in Oodle Data: x86-64 6-stream Huffman decoders'
url: https://fgiesen.wordpress.com/2023/10/29/entropy-decoding-in-oodle-data-x86-64-6-stream-huffman-decoders/
published: '2023-10-29'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Entropy decoding in Oodle Data: x86-64 6-stream Huffman decoders

It’s been a while! [Last time](https://fgiesen.wordpress.com/2022/09/05/entropy-decoding-in-oodle-data-x86-64-3-stream-huffman-decoders/), I went over how the 3-stream Huffman decoders in Oodle Data work. The 3-stream layout is what we originally went with. It gives near-ideal performance on the last game console generation’s [AMD Jaguar cores](https://fgiesen.wordpress.com/2022/04/04/entropy-decoding-in-oodle-data-huffman-decoding-on-the-jaguar/) and is also a good fit for 32-bit x86 and ARM targets, both of which were still a pretty important target for us at the time the scheme was designed (today, pretty much anything new uses 64-bit code, so that’s what we’re designing for; sub-optimal performance on 32b targets is not a reason for us to keep features out of the bitstream anymore).

As per the analysis in the last part, the 3-stream decoders are getting decent issue slot utilization out of a Skylake-era x86 core, but are still fundamentally limited by the critical path latency for individual symbol decodes and the bit buffer refill. We’re also using a lot of extra instructions compared to the minimum necessary to shave a few cycles off that critical path latency. Instead, what we can do is optimize for instruction/issue slot count and throughput at the expense of a slight increase in latency, and then use a lot more streams. Ideally, if we have enough independent work to keep the machine filled, the critical path latency stops being the primary limiter altogether.

That said, we still have those 32-bit and Jaguar targets who prefer the 3-stream layout and could maybe use 4 streams without introducing a lot of extra spills, but certainly not a lot more. The compromise we use in Oodle Data is that we introduced a 6-stream layout that uses 3 streams for the front half of the data being coded, and an independent 3-stream group for the back half. In effect, we’re doing two 3-stream decodes (with two separate output buffers) at the same time. The platforms that would rather have 3 streams decode the two in sequence instead.[1](https://fgiesen.wordpress.com#fn1)

### Many-stream logistics

The number 6 was chosen because it cleanly divides into two sets of 3 (for the platforms that prefer 3), but it also happened to work out in other ways: it turns out both 4 and 8 streams are a bit awkward in terms of register use on x86-64 and 32-bit ARM, and would introduce several extra spills. Probably wouldn’t be a huge deal, but the odd counts are there for a reason.

Anyway, register use is the watchword in general here: the scheme described in the 3-stream article uses 3 registers worth of state per stream: the actual bit buffer, the “number of bits present” count, and the stream read pointer. On x86-64, we have 16 integer GPRs, sort of. The stack pointer is really spoken for, though, which leaves us with 15. 6 streams at 3 registers of state per stream would need 18 registers’ worth just for the bit stream state; the stream read pointer is only used during refill so spilling those during the core decoding loop isn’t the end of the world, but even so, that’s 12 registers allocated, and we still need an output pointer (actually two in our case), a pointer to the decoding table, and at least one or two registers worth of temporary space… and that’s more registers than we have available already. Spilling and reloading around the bit buffer refill isn’t ideal, but workable. When just cycling between our 6 streams means some amount of register thrashing, though, we’re paying an extra tax not just per every 5 symbols decoded, but for every single symbol. The idea with using more streams was to be able to use fewer instructions per decode to use the machine more efficiently. If we’re saving one instructions’ worth of work per symbol and then adding two instructions worth of spill and reload, we’re not doing great. This can still be worth it if we get better instruction-level parallelism (ILP) potential out of it, but we’d rather not.

Therefore, our goal is to be efficient both in terms of instructions executed and in terms of register state we need to keep around. This [old post](https://fgiesen.wordpress.com/2018/09/27/reading-bits-in-far-too-many-ways-part-3/) of mine conveniently presents a solution, in the form of bit reader “variant 5”, the throughput-optimized one. The actual scheme is explained in that post, so I won’t reiterate it here. Just know that the basic idea is to get rid of the “bits consumed” counter per stream by setting the MSB of the 64-bit bit buffer upon refill (then shifting the whole word down if parts of the first byte were already consumed earlier), and determining the consumed bit count using a leading zero count. Conveniently, shifting out just-consumed low bits using an unsigned bit-shift right also updates the consumed bit count for us. Therefore, we save both the extra register for the counter and the extra instructions for maintaining it. The trade-off is that this version of bit-buffer IO doesn’t have the “lookahead” property where the refill load can start before the final consumed bit count of the previous iteration is done. Therefore, we pick up one more load latency along the critical path.

Enough build-up, how does a single-symbol decode look like in this form? Assuming BMI2 is available, it’s this:[2](https://fgiesen.wordpress.com#fn2)

```
andn rcx, rMask, rBits ; peek (rMask = ~2047)
movzx ecx, word [rTablePtr + rcx*2] ; table fetch
shrx rBits, rBits, rcx ; bit buffer update
mov [rDest + <index>], ch ; emit byte
```


Four instructions and 5 uops (4 fused-domain; the store is 2 ops, one store address and one store data which counts as a single uop in the fused domain, the others are 1 uop each) per symbol decoded, which is pretty sweet. Note we splurge on an extra register to keep the constant ~2047 just so we can do the masking with ANDN, which has a non-destructive 3-register form, instead of MOV/AND. The extra MOV doesn’t matter that much when MOV elimination is active, but due to CPU bugs this was actually later disabled in several CPU models, so this is more consistent. Also note both our destination pointers need to be kept within the low 8 registers so the move-from-CH instruction encoding is available, or else it takes an extra shift instruction and uop. (That’s weird quirks of the x64 encoding for you.) The scheme from the previous article takes 5 instructions and 6 uops per symbol decoded (if we use the same ANDN trick, one more of each otherwise), so this change saves us one instruction and one register’s worth of state per stream, with the latter saving further instructions that would otherwise go into spills and reloads if we used 6 streams naively.

The critical path for this is simple: the first three instructions are on it (for any given stream), the last one is not. The AND and shift have 1 cycle of latency each, the indexed load has 5 cycles (on Skylake), for 7 cycles total. Continuing with last article’s assumption of around 4 fused-domain uop issue slots per cycle (the reality is a bit more complicated, but this is good enough), over these 7 cycles, we get 4×7 = 28 issue slots, of which we’re filling 24 when we’re doing 6 streams. When we’re doing this 5 times in a row, that means 5×4 = 20 unused issue slots by the core decode; we do have other things in the loop such as constant loads, pointer increments, the loop condition, the stream overlap checks, and maybe some spills and reloads around the refill stage, so these remaining slots don’t necessarily have to go to waste either. We don’t get to fill every issue slot every cycle anyway because the scheduling and load balancing in the CPU is not perfect, but this is still a promising setup.

### Refill

How do we do the bit buffer refill with this? Well, this again follows the basic logic from “Reading bits in far too many ways (part 3)”. If we implement that naively, we get something like this (per stream):

```
lzcnt rBits, rBits ; # bits consumed
mov rcx, rBits
shr rcx, 3 ; # of full bytes consumed
add rBitsPtr, rcx ; advance ptr
and rBits, 7 ; leftover bit count
mov rcx, [rBitsPtr] ; load next
or rcx, rMarker ; set marker bit (MSB)
shrx rBits, rcx, rBits ; consume leftover bits
```


This is already not bad, but note that most of this is on the critical path for the refill as written. The most annoying part of that is the `lzcnt`

which has a 3-cycle latency on most Intel parts. However, note that the rBits value we do the `lzcnt`

on is always the `shrx`

result of the final decode from that stream, and nothing else looks at the contents of the bit buffer after said shift. Therefore, we can juggle things around to do the leading zero count early. The final decode for each of the 6 streams does:

```
andn rcx, rMask, rBits ; peek (rMask = ~2047)
lzcnt rBits, rBits ; early lzcnt
movzx ecx, word [rTablePtr + rcx*2] ; table fetch
add rBits, rcx ; lzcnt update
mov [rDest + <index>], ch ; emit byte
```


Instead of a final `shrx`

, we use an add instruction instead (making the bits past the initial 8 bits garbage, but we can deal with that), and we move the `lzcnt`

up so it happens concurrent with the table load (which has 5 cycles latency and is on the critical path). That takes the leading zero count off the critical path entirely and doesn’t need us to execute any extra instructions. We do need to clear the garbage bits that end up at bit 8 and above in rBits afterwards. However, if we look at the refill code given above, that’s a trivial fix (funny how that works out):

```
; # bits consumed already in low 8 bits of rBits
movzx rcx, low_byte(rBits)
shr rcx, 3 ; # of full bytes consumed
add rBitsPtr, rcx ; advance ptr
and rBits, 7 ; leftover bit count
mov rcx, [rBitsPtr] ; load next
or rcx, rMarker ; set marker bit (MSB)
shrx rBits, rcx, rBits ; consume leftover bits
```


The code still has some other details to take care of. Because we treat 6-stream blocks as a pair of 3-stream blocks, we still have one backwards, reverse-endian stream in there, we need to maintain 2 separate output pointers, we still need to do the stream-crossing checks and have our loop condition, and so forth. All of that is routine and I won’t go into it here, other than noting that the reverse-endian streams require a 64-bit `bswap`

for their refill, which adds 2 uops and 2 cycle latency to their respective critical paths (on Intel), so those streams have the longest critical-path latency.

### Analysis and results

I already went into the core symbol decode step before, noting that it takes 4 instructions, 4 fused-domain uops, and 5 unfused-domain uops per symbol. For the rest of our critical path candidate, that leaves the refill.

With the tweaked final decode described above, the leading zero count is off the critical path, but we still count it as 1 uop that effectively belongs with the refill (it also changes one `shrx`

to an `add`

, but that doesn’t make a difference at the level of analysis I’m doing in this series, although I will note that this is also slightly beneficial since there are more execution ports that can take integer adds than there are ports that execute shifts).

For the refill, that leaves us with 8 instructions executed (including the `lzcnt`

), all single-uop. The critical path for the refill (after the final rBits update for a stream) goes movzx, shr rcx, add rBitsPtr, mov [rBitsPtr], or rBits, shrx rBits. All of these except for the load are 1 cycle latency, the load is 4 cycles on Skylake and derivatives, 5 on newer uArchs. That’s 9 or 10 cycles critical path latency through the refill, respectively, 11/12 cycles on the reversed streams that need the `bswap`

.

We’re doing this for 6 streams; 8 uops × 6 streams = 48 uops and issue slots – plus another 4 uops for the two `bswaps`

implied by the two backwards streams, implying a grand total of 52 uops. By our previous “about 4 unfused domain uop issue slots per cycle” rule of thumb, that’s around 52/4 = 13 cycles worth of work – we’re actually throughput limited on this portion, for once. And since we’re running this in a loop, we can expect the throughput-limited refill and “other loop overhead” portions to collapse with the latency-limited symbol decode step to some extent.

In the “production” version of the loop, it turns out there’s 15-20 fused-domain uops worth of other work (that’s not symbol decoding or refill) in this loop. I’m giving a range because 5 of these are compare-branch instruction pairs that *can* be macro-fused but whether that actually happens in any given instance is again a bit complicated and depends on other factors such as code alignment that are outside the scope of the level of analysis I’m doing here.

If we take the higher count of 20, this happens to line up precisely with the 20 “wasted” issue slots we noticed during the symbol decode portion. I did not notice this before writing this post and highly doubt that things shake up anywhere close to this in practice, because machine behavior gets fairly “twitchy” in the high-ILP regime and any stray disturbance such as non-ideal scheduler instruction picks or individual L1 cache misses cause long ripple effects. Nevertheless, it does suggest that on Skylake and its many process tweaks, we expect to be, just about, throughput-bound.

This time we’re decoding from 6 streams, 5 symbols each, for 30 symbols decoded per loop iteration. We expect to take 4 issue slots per symbol decode (120 slots total), 8 issue slots per refill (48 slots total), and 20 issue slots worth of bookkeeping etc. per loop iteration, for a total of 188 issue slots. With our 4 issue slots per cycle rule of thumb, if everything works out perfectly, that comes out to 47 cycles per iteration exactly.

For critical path latency, we have 6 independent streams, and the slowest ones are the two byte-reversed ones. Their critical path goes through the symbol decode and refill. We have 5 decodes of 7 cycles each plus a refill of 11 cycles, giving us a latency estimate of about 46 cycles if everything works out right.

In short, under very idealized circumstances, we expect to be throughput-bound (or close to), and hitting around 47/30 = 1.57 cycles/symbol decoded.

How fast does the “production” version of this loop actually run on a Skylake machine, in a real workload, on real data? This is where I would ordinarily post results of a test run, but as I’m writing this, the Skylake test machine I’ve been using for this series isn’t letting me remote in for some reason, so I don’t have same-machine results to post just yet. The values I remember are around 1.83 cycles/symbol for 55 cycles per loop iteration, off from our ideal throughput estimate by 8 cycles or about 17%. (I’ll try to remember to update that with recent measured figures once I get that machine back up and running). That’s a higher discrepancy than I’m comfortable with, but we’re running into the limits of what we can do with our very basic back-of-the-envelope estimates here. A more detailed analysis using [uICA](https://uops.info/uiCA.html) gives a lower-bound estimate of 49.75 cycles for Skylake, with the listed bottleneck being “Decoder”. That is about 10% smaller than the actual observed figures on real workloads that I remember, which as noted in the previous installment of this series is a pretty typical ratio for real-world results (involving cache misses, branch mispredictions, other process/OS interference etc.) vs. throughput estimates. Either way, at around 1.83 cycles/symbol observed for 6-stream compared to 2.79 cycles/symbol observed for 3-stream, we get a 1.53x speed-up from doubling the number of streams.

I do have actual measured results on my home desktop machine, which as of this writing is an AMD Ryzen 9 7950X3D (Zen 4) at 4.2GHz nominal. On that machine, when doing single-threaded Huffman decoding using the 3-stream BMI2 decoder, I get around 2.08 RDTSC ticks (which are not actually clock cycles due to dynamic frequency scaling) per symbol, while the 6-stream BMI2 variant gets around 1.37 RDTSC ticks per symbol, for a speed-up factor of around 1.52x from using 6 streams – almost exactly the same ratio, on a different microarchitecture. (There are also dedicated Zen-optimized versions of the inner loop, which exploit some specifics of AMDs Zen microarchitectures, and average around 1.79 RDTSC ticks/symbol for 3-stream and 1.29 ticks/symbol for 6-stream on the same machine; in this case, the speed-up works out to “only” 1.39x)

For what it’s worth, around 1.5x is also about the level of speed-up I see on wider 64-bit ARM machines, although the really wide ones (e.g. Apple M1/M2) can see even larger speed-ups from 6-stream.

On said Zen 4 machine, the pure 6-stream Huffman decoding BMI2 inner loop hits a rate of around 3.07 GB/s decoded per second (in our case, 1 symbol=1 byte), on a single core, with the system otherwise mostly idle, i.e., running the OS and desktop but nothing particularly taxing. When using the Zen-optimized variant, it hits 3.25GB/s.

The entire Huffman decode on the same data, same machine averages 2.52GB/s on a single core (using the straight BMI2 variant, 2.65GB/s for the Zen-optimized variant); this includes other tasks like reading the Huffman code lengths from the bit stream, setting up decode tables, as well as the careful end-of-stream processing.

### Discussion and conclusion

The original 6-stream design started as a thought experiment about how many streams a purely throughput-bound Huffman decoder would have to be using on a theoretical x86 with as many registers as we wanted, but the same basic instruction latencies as the Haswell/Broadwell/Skylake machines that were current at the time (early 2016). Once it became clear that the 4-instruction/symbol decode step was not hard to do and the resulting stream count worked out to “around 6”, exactly twice what we were shipping previously and without bumping into register count limits, the (admittedly slightly off-kilter) pair-of-3-streams design coalesced as something that was easy to fit into the existing bitstream structure and could just be ignored on targets that didn’t benefit from it, while giving us a considerable speed boost on the rest.

In aggregate, this series of posts is meant both as an explanation of the methods used and more generally, as an illustrative worked example about what designing a data format for higher ILP potential looks like. A “standard” single-stream Huffman decoder is fundamentally bottlenecked by its single serial dependency chain, but the “right” number of dependency chains for a given task is not necessarily straightforward, nor is it always easy to figure out by experimentation. For example, the throughput-optimized decode step used in this version of the Huffman decoder is strictly worse than the latency-optimized decoder for typical 3- or 4-stream setups, so unless you’re aware of the underlying dynamics, you wouldn’t even try it for anything larger. Likewise, the latency-optimized approaches that work best for smaller stream counts run out of steam as more streams are added (mostly from extra spills), suggesting that there is no further win to be had from increased stream counts when in fact there is.

The particular numbers here are always subject to change; the original 3-stream count in the Oodle Kraken format was motivated primarily by the AMD Jaguar cores that were our most important target at the time, and the 6-stream version, although it happens to work out fine, was just a convenient multiple. As CPU designs get wider, the optimal number of streams keeps increasing, provided other likely bottlenecks keep getting fixed alongside. 3 That said, a not-quite-ideal 6-stream arrangement on a machine that would do even better with 9 is still much preferable to your usual single serial bitstream decode.

If nothing else, takes this series as a practical demonstration of just how much wasted potential there is on current hardware (“current” here really meaning “anything built in the 21st century”) in serialization formats with a single stream of variable-sized data where each token needs to be decoded to be able to start decoding the next. Of course decoding speed is far from the only concern in practice, but it should at least be considered, when too often it is ignored entirely. There are definitely problems with multi-stream formats (especially when consuming data incrementally or in a streaming fashion), so they are not a panacea, but in many use cases it is completely fine to decode data in small batches (on the order of tens of kilobytes) with some buffering, and in those cases a multi-stream design can offer substantial benefits, especially in write-once read-many scenarios.

Finally, one lengthy digression on a complementary strategy: decoding multiple Huffman symbols at once. The basic idea here is straightforward: if we’re doing a table lookup per symbol anyway, and if the whole point of variable-length codes is to assign shorter code to more common symbols, can’t we decode multiple symbols from a single table lookup, provided those symbols are all fully contained in the portion of the bitstream we peeked at? And yes, of course we can, but there are considerable logistical difficulties if we look again at the final per-symbol decode step we ended up with:

```
andn rcx, rMask, rBits ; peek (rMask = ~2047)
movzx ecx, word [rTablePtr + rcx*2] ; table fetch
shrx rBits, rBits, rcx ; bit buffer update
mov [rDest + <index>], ch ; emit byte
```


This design uses 2 bytes per table entry so it doesn’t have space to decode multiple symbols at once. The easiest generalization is to allow decoding either 1 or 2 symbols per step. That means per table entry, we now need the combined length of all symbols decoded, the values for the first and (potentially) second symbol decoded, and a symbol count (or other flag) for whether the table entry describes 1 or 2 symbols. Take a basic layout of a 32-bit table entry containing 4 bytes (len, nsyms, sym1, sym2) for a concrete example (that’s not the only possible design point, but it is a sensible one). Note that our table entries are now twice the size (and much trickier to initialize), and furthermore, for each table lookup, we don’t know anymore whether we’re going to decode 1 or 2 symbols, so we can’t use immediate offsets for our stores anymore; in every decode step, we need to figure out what the symbol count is and advance the output pointer. We also either need multiple loads or do a single combined 32-bit load and shift to get access to the various fields; pick your poison. My best bet at a workable 1-or-2 symbol decode step looks something like this:

```
andn rcx, rMask, rBits ; peek (rMask = ~2047)
mov ecx, dword [rTablePtr + rcx*4] ; table fetch
shrx rBits, rBits, rcx ; bit buffer update
movzx rNumSyms, ch ; extract nsyms
shr ecx, 16 ; align output byte(s)
mov [rDest], cx ; emit output byte(s)
add rDest, rNumSyms ; advance write pointer
```


Note that despite still using oddball tricks like the movzx-from-ch to get (effectively) a bitfield extract, which comes with strings attached (rNumSyms can’t be just any register for this to work), we’re now using 7 instructions and 7 fused-domain uops (8 unfused-domain) to decode either 1 or 2 symbols. Furthermore, we’re adding a secondary dependency chain on the outputs between adjacent logical streams: the `add rDest, rNumSyms`

needs to complete before the next stream can finish its output. That’s not the end of the world since only the stores depend on it, but it’s an extra potential for slowdown.

This is just not all that appealing. As noted above, we already get to be mostly throughput-bound (actually frontend, but at least we’re not constantly waiting on dependency chains anymore) on the original Skylake target, using 4 instructions per symbol decoded. This modified version will in the best case only ever write 2-symbol pairs and use 7 instructions to do so, for 3.5 instructions per symbol decoded. But that’s with a 100% success rate. Even if we manage to decode a pair of symbols a staggering 75% of the time, we’re still taking 7 instructions to decode a single symbol in the remaining cases, which works out to an average of 0.25 × 7 + 0.75 × 3.5 = 4.375 instructions per symbol – still worse than a single symbol decode, although to be fair, the double-symbol decodes end up doing a refill less often when they hit. Considering that, it’s likely that around 75% pair decode rate, we’d probably break even or see a slight speed-up using multi-symbol decoding.

That’s still not particularly promising though; from multi-symbol decoding, we’d like to see a lot more than “break even around the point where we decode 2 symbols at once 3/4 of the time”. Moreover, from the entropy of the symbol stream, we can work out how big the decode table needs to be to be able to successfully decode symbol pairs on most decode steps. Oodle Data uses a (very low) code-length limit of 11 bits to facilitate infrequent refills. In our existing table size of 2048 entries, we can expect to see frequent pairs of symbols if the entropy is around 5.5 bits per symbol or so, which is very low. Our typical data for things like literals after LZ compression is more frequently around 7.2-7.8 bits per symbol (each of which is from an 8-bit alphabet). We would need something on the order of 215 = 32768 table entries for pair decodes to be common; at 4 bytes per table entry, that’s 128KiB, which is definitely outside the L1D cache, and in fact takes up a sizeable fraction of the L2 cache as well. So now we’re expecting to miss the L1D cache on those table accesses as well, meaning our expected latency per symbol decode for the memory access goes from around 5 cycles to around 16-20, which completely blows up our assumptions. Now we have nowhere near enough streams to hide that latency again, and we also need to spend the time to set up these giant tables; as you can see from the numbers quoted in the preceding section, the time spent setting up the decoding tables even for our small (2048-entry, 2 bytes/entry) configuration is not negligible, and multi-symbol decode tables need more space per element, more elements, and are more expensive to set up.

Add all these together, and the case for table-driven multi-symbol decoding *in the general case* just doesn’t look great: it increases the amount of work per decode step, which is disproportionately felt when the decode steps are otherwise lightweight or there are multiple streams available to compensate for critical-path latency. It increases table build time, which can be a significant fraction of overall decode time if tables change frequently, table building isn’t optimized (it often isn’t) or tables are large, and it often ends up requiring impractically large tables to be able to decode pairs to begin with.

That doesn’t mean that it doesn’t have its uses, especially in cases where you know the expected entropy is low. For example, the JPEG decoder in stb_image normally decodes AC coefficients in two steps, first reading a (run,level) pair (this is encoded into a single 8-bit value as per the JPEG spec) and then reading an extra number of bits determined by the “level” value to figure out the coefficient value. Most AC coefficients are very small (mostly ±1 or ±2), so stb_image’s JPEG decoder additionally has the “fast AC” table that combines decoding (run,level,extra_bits) all into one table lookup (into a 1KiB table) in the typical case when the AC coeffs are very small.

However, for general-purpose lossless (de)coding in software, multi-symbol decoding just isn’t very compelling in my experience.

And that’s it for this post and the Huffman portion of this series, unless there’s interest in some of the other targets. (There’s also a suite of optimized ARM decoders, both 32- and 64-bit, and while they have some cool tricks I’m happy with, they don’t add anything substantially new to the material already covered so far.) I’m leaving the door open to do another follow-up on the non-Huffman portions of Oodle Data’s entropy coding—especially TANS—but I don’t have any concrete plans yet. We’ll see!

### Footnotes

[1] This does give us a full 6 independent streams when batch-decoding the entire contents of a Huffman block up front, but is still effectively 3 streams when decoding incrementally. Not a problem in the regular SW Oodle decoders, but there are other “streaming” implementations that don’t get a benefit out of the 6-stream layout. The platforms we support that greatly prefer 3-stream batch decoding were much more important to our customers than the streaming use case at the time this was designed, so this was a sensible trade-off.

[2] You might notice that this code has a tendency to keep all shift counts in explicitly rcx, that exact register, not just a named temporary like I do for the other register references. That’s because even though I’m showing the BMI2 versions of everything, we also support non-BMI2 paths for machines that don’t have it, and in those we want to use the `shr reg, cl`

forms. We also use the store-from-ch instruction, so the register receiving the table load needs to be one of eax, ebx, ecx or edx anyhow; it’s easiest to just make rcx the dedicated temporary register in this code and make sure everything that needs to be a shift count ends up in there in, that way the BMI2 and non-BMI2 paths can be very similar.

[3] [Dougall Johnson](https://github.com/dougallj) has done some experimentation on Apple M1/M2 hardware and according to him, going up to even 12 streams is still beneficial, but I haven’t tried to replicate this myself.