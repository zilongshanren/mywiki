---
title: Reading bits in far too many ways (part 3)
url: https://fgiesen.wordpress.com/2018/09/27/reading-bits-in-far-too-many-ways-part-3/
published: '2018-09-27'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Reading bits in far too many ways (part 3)

(Continued from [part 2](https://fgiesen.wordpress.com/2018/02/20/reading-bits-in-far-too-many-ways-part-2/). “[A whirlwind introduction to dataflow graphs](https://fgiesen.wordpress.com/2018/03/05/a-whirlwind-introduction-to-dataflow-graphs/)” is required reading.)

Last time, we saw a whole bunch of different bit reader implementations. This time, I’ll continue with a few more variants, implementation considerations on pipelined superscalar CPUs, and some ways to use the various degrees of freedom to our advantage.

### Dependency structure of bit readers

To get a better feel for where the bottlenecks in bit decoding are, let me restate some of the bit reading approaches we’ve covered in the previous parts again in our pseudo-assembly language, and then we can have a look at the corresponding dependency graphs.

Let’s start with variant 3 from last time, but I’ll do a LSB-first version this time:

refill3_lsb: rBytesConsumed = lsr(rBitPos, 3); rBitPtr = rBitPtr + rBytesConsumed; rBitBuf = load64LE(rBitPtr); rBitPos = rBitPos & 7; peekbits3_lsb(count): rBits = lsr(rBitBuf, rBitPos); rBitMask = lsl(1, count); rBitMask = rBitMask - 1; rBits = rBits & rBitMask; // result consume3_lsb(count): rBitPos = rBitPos + count;

Note that if `count`

is a compile-time constant, the computation for `rBitMask`

can be entirely constant-folded. Peeking ahead by a constant, fixed number of bits then working out from the result how many bits to actually consume is quite common in practice, so that’s what we’ll do. If we do a refill followed by two peek/consume cycles with the consume count being determined from the read bits “somehow”, followed by another refill (for the next loop iteration), the resulting pseudo-asm is like this:

// Initial refill rBytesConsumed = lsr(rBitPos, 3); // Consumed 0 rBitPtr = rBitPtr + rBytesConsumed; // Advance 0 rBitBuf = load64LE(rBitPtr); // Load 0 rBitPos = rBitPos & 7; // LeftoverBits 0 // First decode (peek count==19) rBits = lsr(rBitBuf, rBitPos); // BitsRemaining 0 rBits = rBits & 0x7ffff; // BitsMasked 0 rCount = determineCount(rBits); // DetermineCount 0 rBitPos = rBitPos + rCount; // PosInc 0 // Second decode rBits = lsr(rBitBuf, rBitPos); // BitsRemaining 1 rBits = rBits & 0x7ffff; // BitsMasked 1 rCount = determineCount(rBits); // DetermineCount 1 rBitPos = rBitPos + rCount; // PosInc 1 // Second refill rBytesConsumed = lsr(rBitPos, 3); // Consumed 1 rBitPtr = rBitPtr + rBytesConsumed; // Advance 1 rBitBuf = load64LE(rBitPtr); // Load 1 rBitPos = rBitPos & 7; // LeftoverBits 1

And the dependency graph looks dishearteningly long and skinny:

![Dependency graph for bit reading, variant 3](../../assets/3ca632226fb67ef8.png)


Ouch. That’s averaging less than one instruction per cycle, and it’s all in one big, serial dependency chain. Not depicted in this graph but also worth noting is that the 4-cycle latency edge from “Load” to “BitsRemaining” is a recurring delay that will occur on every refill, because the computation of the updated rBitPtr depends on the decode prior to the refill having been completed. Now this is not a full decoder, since I’m showing only the parts to do with the bitstream IO (presumably a real decoder also contains code to, you know, actually decode the bits and store the result somewhere), but it’s still somewhat disappointing. Note that the DetermineCount step is a placeholder: if the count is known in advance, for example because we’re reading a fixed-length field, you can ignore it completely. The single cycle depicted in the graph is OK for very simple cases; more complicated cases will often need multiple cycles here, for example because they perform a table lookup to figure out the count. Either way, even with our optimistic single-cycle single-operation DetermineCount step, the critical path through this graph is pretty long, and there’s very little latent parallelism in it.

Does variant 4 fare any better? The primitives look like this in pseudo-ASM:

refill4_lsb: rNext = load64LE(rBitPtr); rNextSh = lsl(rNext, rBitCount); rBitBuf = rBitBuf | rNextSh; // Most instruction sets don't have a subtract-from-immediate // but do have xor-by-immediate, so this is an advantageous // way to write 63 - rBitCount. (This works since we know that // rBitCount is in [0,63]). rBitsAdvance = rBitCount ^ 63; rBytesAdvance = lsr(rBitsAdvance, 3); rBitPtr = rBitPtr + rBytesAdvance; rBitCount = rBitCount | 56; peekbits4_lsb(count): rBitMask = lsl(1, count); rBitMask = rBitMask - 1; rBits = rBitBuf & rBitMask; // result consume4_lsb(count): rBitBuf = lsr(rBitBuf, count); rBitCount = rBitCount - count;

the pseudo-code for our “refill, do two peek/consume cycles, then refill again” scenario looks like this:

// Initial refill rNext = load64LE(rBitPtr); // LoadNext 0 rNextSh = lsl(rNext, rBitCount); // NextShift 0 rBitBuf = rBitBuf | rNextSh; // BitInsert 0 rBitsAdv = rBitCount ^ 63; // AdvanceBits 0 rBytesAdv = lsr(rBitsAdv, 3); // AdvanceBytes 0 rBitPtr = rBitPtr + rBytesAdv; // AdvancePtr 0 rBitCount = rBitCount | 56; // RefillCount 0 // First decode (peek count==19) rBits = rBitBuf & 0x7ffff; // BitsMasked 0 rCount = determineCount(rBits); // DetermineCount 0 rBitBuf = lsr(rBitBuf, rCount); // ConsumeShift 0 rBitCount = rBitCount - rCount; // ConsumeSub 0 // Second decode rBits = rBitBuf & 0x7ffff; // BitsMasked 1 rCount = determineCount(rBits); // DetermineCount 1 rBitBuf = lsr(rBitBuf, rCount); // ConsumeShift 1 rBitCount = rBitCount - rCount; // ConsumeSub 1 // Second refill rNext = load64LE(rBitPtr); // LoadNext 1 rNextSh = lsl(rNext, rBitCount); // NextShift 1 rBitBuf = rBitBuf | rNextSh; // BitInsert 1 rBitsAdv = rBitCount ^ 63; // AdvanceBits 1 rBytesAdv = lsr(rBitsAdv, 3); // AdvanceBytes 1 rBitPtr = rBitPtr + rBytesAdv; // AdvancePtr 1 rBitCount = rBitCount | 56; // RefillCount 1

with this dependency graph:

![Dependency graph for bit reading, variant 4](../../assets/20079ee4b7bb8ef6.png)


That’s a bunch of differences, and you might want to look at variant 3 and 4 in different windows side-by-side. The variant 4 refill does take 3 extra instructions, but we can immediately see that we get more latent instruction-level parallelism (ILP) in return:

- The variant 4 refill splits into three dependency chains, not two.
- The LoadNext for the second refill can start immediately after the AdvancePtr for the first refill, moving the load off the critical path for the second and subsequent iterations. Variant 3 has a 6-cycle latency from the determination of the final
`rBitPos`

in the first iteration to a refilled`rBitBuf`

; in variant 4, that latency shrinks to 2 cycles (one shift and an OR). In other words, while the refill takes more instructions, most of them are off the critical path. - The consume step in variant 4 has two parallel computations; in variant 3, the
`rBitPos`

update is critical and feeds into the shift in the next “peek” operation. Variant 4 has a single shift (to consume bits) on the critical path to the next peek; as a result, the latency between two subsequent decodes is one cycle less in variant 4: 3 cycles instead of 4.

In short, this version trades a slight increase in refill complexity for a noticeable latency reduction of several key steps, provided it’s running on a superscalar CPU. That’s definitely nice. On the other hand, the key decode steps are still very linear. We’re limited by the latency of a long chain of serial computations, which is a bad place to be: *if possible, it’s generally preferable to be limited by throughput (how many instructions we can execute), not latency (how fast we can complete them)*. Especially so if most of the latency in question comes from integer instructions that already have a single cycle of latency. Over the past 30 years, the number of executions units and instructions per cycle in mainstream CPU parts have steadily, if slowly, increased. But if we want to see any benefit from this, we need to write code that has a use for these extra execution resources.

### Multiple streams

As is often the case, the best solution to this problem is the straightforward one: if decoding from a single bitstream is too serial, then why not decode from multiple bitstreams at once? And indeed, this is much better; there’s not much point to showing a graph here, since it’s literally just two copies of a single-stream graph next to each other. Even with a very serial decoder like variant 3 above, you can come a lot closer to filling up a wide out-of-order machine as long as you use enough streams. To a first-order approximation, using N streams will also give you N times the latent ILP—and given how serial a lot of the direct decoders are, this will translate into a substantial (usually not quite N-times, but still very noticeable) speed-up in the decoder on wide-enough processors. So what’s the catch? There are several:

- Using multiple streams is a change to the bitstream format, not just an implementation detail. In particular, in any long-term storage format, any change in the number of bitstreams is effectively a change in the protocol or file format.
- You need to define how to turn the multiple streams into a single output bytestream. This can be simple concatenation along with a header, it can be some form of interleaving or a sophisticated framing format, but no matter what it ends up being, it’s an increase in complexity (and usually also in storage overhead) relative to producing a single bitstream that contains everything in the order it’s read.
- For anything with short packets and low latency requirements (e.g. game packets or voice chat), you either have to interleave streams fairly finely-grained (increasing size overhead), or suffer latency increases.
- Decoding from N streams in parallel increases the amount of internal state in the decoder. In the decoder variants shown above, a N-wide variant needs N copies of
`rBitBuf`

,`rBitPos`

/`rBitCount`

and`rBitPtr`

, at the very least, plus several temporary registers. For N=2 this is usually not a big deal, but for large counts you will start to run out of registers at least on some targets. There’s relatively little work being done on any given individual data item; if values get spilled from registers, the resulting loads and stores tend to have a very noticeable cost and will easily negate the benefit from using more streams.

In short, it’s not a panacea, but one of the usual engineering trade-offs. So how many streams should you use? It depends. At this point, for *anything* that is even remotely performance-sensitive, I would recommend trying at least N=2 streams. Even if your decoder has a lot of other stuff going on (computations with the decoded values etc.), bitstream decoding tends to be serial enough that there’s many wasted cycles otherwise, even on something relatively narrow like a dual-issue in-order machine. Having two streams adds a relatively small amount of overhead to the bitstream format (to signal the start of the data for stream 2 in every coding unit, or something equivalent), needs a modest amount of extra state for the second bit decoder, and tends to result in sizeable wins on pretty much any current CPU.

Using more than 2 streams can be a significant win in tight loops that do nothing but bitstream decoding, but is overkill in most other cases. Before you commit to a specific (high) number, you ideally want to try implementations on at least a few different target devices; a good number on one device may be past a big performance cliff on another, and having that kind of thing enshrined in a protocol or file format is unfortunate.

### Aside: SIMD? GPU?

If you use many streams, can you use SIMD instructions, or offload work to a GPU? Yes, you can, but the trade-offs get a bit icky here.

Vectorizing the simple decoders outlined above directly is, generally speaking, not great. There’s not a lot of computation going on per iteration, and operations such as refills end up using gathers, which tend to have a high associated overhead. To hide this overhead, and the associated latencies, you generally still need to be running multiple instances of your SIMD decoder in parallel, so your total number of streams ends up being the number of SIMD lanes times two (or more, if you need more instances). Having a high number of streams may be OK if all your targets have good wide SIMD support, but can be a real pain if you need to decode on at least one that doesn’t.

The same thing goes for GPUs, but even more so. With single warps/wavefronts of usually 16-64 invocations, we’re talking *many* streams just to not be running a kernel at quarter utilization, and we generally need to dispatch multiple warps worth of work to hide memory access latency. Between these two factors, it’s easy to end up needing well over 100 parallel streams just to not be stalled most of the time. At that scale, the extra overhead for signaling individual stream boundaries is definitely not negligible anymore, and the magic numbers are different between different GPU vendors; striking a useful compromise between the needs of different GPUs while also retaining the ability to decode on a CPU if no suitable GPU is available starts to get quite tricky.

There are techniques to at least make the memory access patterns and interleaving overhead somewhat more palatable (I wrote about this [elsewhere](https://arxiv.org/abs/1402.3392)), but this is an area of ongoing research, and so far there’s no silver bullet I could point at and just say “do this”. This is definitely a challenge going forward.

### Tricks with multiple streams

If you’re using multiple streams, you need to decide how these multiple streams get assembled into the final output bitstream. If you don’t have any particular reason to go with a fine-grained interleaving, the easiest and most straightforward option is to concatenate the sub-streams, with a header telling you how long the individual pieces are, here pictured for 3 streams:

![Three sub-streams, linear layout](../../assets/b921749e324dfa13.png)


Also pictured are the initial stream bit pointers before reading anything (pointers in a C-like or assembly-like setting; if you’re using something higher-level, probably indices into a byte slice). The beginning of stream 0 is implicit—right after the end of the header—and the end of the final stream is often supplied by an outer framing layer, but the initial positions of `bitptr1`

and `bitptr2`

need to be signaled in the bytestream somehow, usually by encoding the length of streams 0 and 1 in the header.

One thing I haven’t mentioned so far are bounds checks. Compressed data is normally untrusted since all the channels you might get that data from tend to be prone to either accidental (error during storage or in transit) or intentional (malicious attacker trying to craft harmful data) corruption, so careful input validation is not optional. What this usually boils down to in practice is that every load from the bitstream needs to be guarded by a range check that guarantees it’s in bounds. The overhead of this can be reduced in various ways. For example, one popular method is to unroll loops a few times and check at the top that there are enough bytes left for worst-case number of bytes consumed in the number of unrolled iterations, then only dropping to a careful loop that checks every single byte access at the very end of the stream. I’ve written about [another useful technique](https://fgiesen.wordpress.com/2016/01/02/end-of-buffer-checks-in-decompressors/) before.

But why am I mentioning this here? Because it turns out that with multiple streams laid out sequentially, the overhead of bounds checking can be reduced. A direct range check for 3 streams that checks whether there are at least K bytes left would look like this:

// This needs to happen before we do any loads: // If any of the streams are close to exhausted // (fewer than K bytes left), drop to careful loop if (bitend0 - bitptr0 < K || bitend1 - bitptr1 < K || bitend2 - bitptr2 < K) break;

But when the three streams are sequential, we can use a simpler expression. First, we don’t actually need to worry about reading past the end of stream 0 or stream 1 as long as we still stay within the overall containing byte slice. And second, we can relax the check in the inner loop to use a much weaker test:

// Only check the last stream against the end; for // other streams, simply test whether an the read // pointer for an earlier stream is overtaking the // read ponter for a later stream (which is never // valid) if (bitptr0 > bitptr1 || bitptr1 > bitptr2 || bitend2 - bitptr2 < K) break;

The idea is that `bitptr1`

starts out pointing at `bitend0`

, and only keeps increasing from there. Therefore, if we ever have `bitptr0`

> `bitptr1`

, we know for sure that something went wrong and we read past the end of stream 0. That will give us garbage data (which we need to handle anyway), but not read out of bounds, since the checks maintain the invariant that `bitptr0`

≤ `bitptr1`

≤ `bitptr2`

≤ `bitend2 - K`

. A later careful loop should use more precise checking, but this variant of the test is simpler and doesn’t require most of the `bitend`

values to be reloaded in every iteration of our decoding loop.

Another interesting option is to reverse the order of some of the streams (which flips endianness as a side effect), and then glue pairs of forward and backward streams together, like shown here for streams 1 and 2:

![Three sub-streams with forward/backward pair](../../assets/a69a84263c616d7d.png)


I admit this sounds odd, but this has a few interesting properties. One of them is that it shrinks the amount of header space somewhat: in the image, the initial stream pointer for stream 2 is the same as the end of the buffer, and if there were 4 streams, the initial read pointers for stream 2 and 3 would start out in the same location (but going opposite directions). In general, we only need to denote the boundaries between stream *pairs* instead of individual streams. Then we let the decoder run as before, checking that the read cursors for the forward/backward pair don’t cross. If everything went right, once we’ve consumed the entire input stream, the final read cursors in a forward/backward pair should end up right next to each other. It’s a bit strange in that we don’t know the size of either stream in advance, just their sum, but it works fine.

Another consequence is that there’s no need to keep track of an explicit end pointer in the inner decoder loop if the final stream is a backwards stream; the pointer-crossing check takes care of it. In our running example, we’re now down to

// Check for pointer crossing; if done right, we get end-of-buffer // checks for free. if (bitptr0 > bitptr1 || bitptr1 > bitptr2) break;

In this version, `bitptr0`

and `bitptr1`

point at the next byte to be read in the forwards stream, whereas `bitptr2`

is offset by -K to ensure we don’t overrun the buffer; this is just a constant offset however, which folds into the memory access on regular load instructions. It’s all a bit tricky, but it saves a couple instructions, makes the bitstream slightly smaller and reduces the number of live variables in a hot loop, with the savings usually being larger the cost of a single extra endian swap. With a two-stream layout, generating the second bitstream in reverse also happens to be convenient on the encoder side, because we can reserve memory for the expected (or budgeted) size of the combined bitstream without having to guess how many bytes end up in either half; it’s just a regular double-ended stack. Once encoding is done, the two parts can be compacted in-place by moving the second half downwards.

None of these properties are a big deal in and of themselves, but they make for a nice package, and a two-stream setup with a forwards/backwards pair is now our default layout for most parts in most parts of the Oodle bitstream (Oodle is a lossless data compression library I work on).

Between the various tricks outlined so far, the size overhead and the extra CPU cost for wrangling multiple streams can be squeezed down quite far. But we still have to deal with the increased number of live variables that multiple streams imply. It turns out that if we’re willing to tolerate a moderate increase in critical path latency, we can reduce the amount of state variables per bit reader, in some cases while simultaneously (slightly) reducing the number of instructions executed. The advantage here is that we can fit more streams into a given number of working registers than we could otherwise; if we can use enough streams that we’re primarily limited by execution *throughput* and not critical path latency, increasing said latency is OK, and reducing the overall number of instructions helps us increase the throughput even more. So how does that work?

### Bit reader variant 5: minimal state, throughput-optimized

The bit reader variants I’ve shown so far generally split the bit buffer state across two variables: one containing the actual bits and another keeping track of how many bits are left in the buffer (or, equivalently, keeping track of the current read position within the buffer). But there’s a simple trick that allows us to reduce this to a single state variable: the bit shifts we use always shift in zeros. If we turn the MSB (for a LSB-first bit buffer) or the LSB (for a MSB-first bit buffer) into a marker bit that’s always set, we can use that marker to track how many bits we’ve consumed in total come the next refill. That allows us to get rid of the bit count and the instructions that manipulate it. That means one less variable in need of a register, and depending on which variant we’re comparing to, also fewer instructions executed per “consume”.

I’ll present this variant in the LSB-first version, and this time there’s an actual reason to (slightly) prefer LSB-first over MSB-first.

const uint8_t *bitptr; // Pointer to current byte uint64_t bitbuf = 1ull << 63; // Init to marker in MSB void refill5_lsb() { assert(bitbuf != 0); // Count how many bits we consumed using a "leading zero // count" instruction. See notes below. int bits_consumed = CountLeadingZeros64(bitbuf); // Advance the pointer bitptr += bits_consumed >> 3; // Refill and put the marker in the MSB bitbuf = read64LE(bitptr) | (1ull << 63); // Consume the bits in this byte that we've already used. bitbuf >>= bits_consumed & 7; } uint64_t peekbits5_lsb(int count) { assert(count >= 1 && count <= 56); // Just need to mask the low bits. return bitbuf & ((1ull << count) - 1); } void consume5_lsb(int count) { bitbuf >>= count; }

This “count leading zeros” operation might seem strange and weird if you haven’t seen it before, but it happens to be something that’s useful in other contexts as well, and most current CPU architectures have fast instructions that do this! Other than the strangeness going on in the refill, where we first have to figure out the number of bits consumed from the old marker bit, then insert a new marker bit and do a final shift to consume the partial bits from the first byte, this is like a hybrid between variants 3 and 4 from last time.

The pseudo-assembly for our running “refill, two decodes, then another refill” scenario goes like this: (not writing out the marker constant explicitly here)

// Initial refill rBitsConsumed = clz64(rBitBuf); // CountLZ 0 rBytesAdv = lsr(rBitsConsumed, 3); // AdvanceBytes 0 rBitPtr = rBitPtr + rBytesAdv; // AdvancePtr 0 rNext = load64LE(rBitPtr); // LoadNext 0 rMarked = rNext | MARKER; // OrMarker 0 rLeftover = rBitsConsumed & 7; // LeftoverBits 0 rBitBuf = lsr(rMarked, rLeftover); // ConsumeLeftover 0 // First decode (peek count==19) rBits = rBitBuf & 0x7ffff; // BitsMasked 0 rCount = determineCount(rBits); // DetermineCount 0 rBitBuf = lsr(rBitBuf, rCount); // Consume 0 // Second decode rBits = rBitBuf & 0x7ffff; // BitsMasked 1 rCount = determineCount(rBits); // DetermineCount 1 rBitBuf = lsr(rBitBuf, rCount); // Consume 1 // Second refill rBitsConsumed = clz64(rBitBuf); // CountLZ 1 rBytesAdv = lsr(rBitsConsumed, 3); // AdvanceBytes 1 rBitPtr = rBitPtr + rBytesAdv; // AdvancePtr 1 rNext = load64LE(rBitPtr); // LoadNext 1 rMarked = rNext | MARKER; // OrMarker 1 rLeftover = rBitsConsumed & 7; // LeftoverBits 1 rBitBuf = lsr(rMarked, rLeftover); // ConsumeLeftover 1

The refill has 7 integer operations, the same as variant 4 (“looakhead”) above, and 3 more than variant 3 (“bit extract”), while the decode step takes 3 operations (including the `determineCount`

step), one fewer than variants 3 (“bit extract”) and 4 (“lookahead”). The latter means that we equalize with the regular bit extract form in terms of instruction count when we perform at least 3 decodes per refill, and start to pull ahead if we manage more than 3. For completeness, here’s the dependency graph:

![Dependency graph for bit reading, variant 5](../../assets/fd84373bd661a600.png)


Easily the longest critical path of the variants we’ve seen so far, and very serial indeed. It doesn’t help that not only do we not know the load address early, we also have several more steps in the refill compared to the basic variant 3. But having the entire “hot” bit buffer state concentrated in a single register (`rBitBuf`

) during the decodes means that we can afford *many* streams at once, and with enough streams that extra latency can be hidden.

This one definitely needs to be deployed carefully, but it’s a powerful tool when used in the right place. Several of the fastest (and hottest) decoder loops in Oodle use it.

Note that with this variation, there’s a reason to stick with the LSB-first version: the equivalent MSB-first version needs a way to count the number of *trailing* zero bits, which is a much less common instruction, although it can be synthesized from a leading zero count and standard arithmetic/logical operations at [acceptable extra cost](https://fgiesen.wordpress.com/2013/10/18/bit-scanning-equivalencies/). Which brings me to my final topic for this post.

### MSB-first vs. LSB-first: the final showdown

Throughout this 3-parter series, I’ve been continually emphasizing that there’s no *major* reason to prefer MSB-first or LSB-first for bit IO. Both are broadly equivalent and have efficient algorithms. But having now belabored that point sufficiently, if we can make both of them work, which one should we choose?

There are definitely differences that push you into one direction or another, depending on your intended use case. Here are some you might want to consider, in no particular order:

- As we saw in
[part 2](https://fgiesen.wordpress.com/2018/02/20/reading-bits-in-far-too-many-ways-part-2/), the natural MSB-first`peekbits`

and`getbits`

implementations run into trouble (of the undefined-behavior and hardware-actually-behaving-in-surprising-ways kind) when`count == 0`

, whereas with the natural LSB-first implementation, this case is unproblematic. If you need to support counts of 0 (usefol for e.g. variable-length codes), LSB-first tends to be slightly more convenient. Alternatives for MSB-first are a rotate-based implementation (which has no problems with 0 count) or using an extra shift, turning`x >> (64 - count)`

into`(x >> 1) >> (63 - count)`

. - MSB-first coding tends to have a big edge for universal variable-length codes. Unary codes can be decoded quickly via the aforementioned “count leading zero” instructions; gamma codes and the closely related Exp-Golomb codes also admit
[direct decoding](https://fgiesen.wordpress.com/2011/01/19/a-small-note-on-the-elias-gamma-cod/)in a fairly slick way; and the same goes for Golomb-Rice codes and a few others. If you’re considering universal codes, MSB-first is definitely handier. - At the other extreme, LSB-first coding often ends up slightly cheaper for the table-based decoders commonly used when a code isn’t fixed as part of the format; Huffman decoders for example.
- MSB-first meshes somewhat more naturally with big-endian byte order, and LSB-first with little-endian. If you’re deeply committed to either side in this particular holy war, this might drive you one way or the other.

Charles and me both tend to default to MSB-first but will switch to LSB-first where it’s a win on multiple target architectures (or on a single important target).

### Conclusion

That’s it for both this post and this mini-series; apologies for the long delay, caused by first a surprise deadline that got dropped in my lap right as I was writing the series originally, and then exacerbated by a combination of technical difficulties (alas, still ongoing) and me having gotten “out of the groove” in the intervening time.

This post ended up longer than my usual, and skips around topics a bit more than I’d like, but I really didn’t want to make this series a four-parter; I still have a few notes here and there, but I don’t want to drag this topic out much longer, not on this general level anyway. Instead, my plan is to write about some more down-to-earth case studies soon, so I can be less hand-wavy, and maybe even do some actual assembly-level analysis for an actual real-world CPU instead of an abstract idealized machine. We’ll see.

Until then!