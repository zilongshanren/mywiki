---
title: 'Entropy coding in Oodle Data: Huffman coding'
url: https://fgiesen.wordpress.com/2021/08/30/entropy-coding-in-oodle-data-huffman-coding/
published: '2021-08-30'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Entropy coding in Oodle Data: Huffman coding

Last time I covered the big picture, so we know the ground rules for the modular entropy coding layer in Oodle Data: bytestream consisting of several independent streams, pluggable algorithms, bytes in and bytes out, and entropy decoding is done as a separate pass, not inlined into the code that consumes the decoded data.

There are good and bad news here: the good news is that the encoders and decoders need to do just one thing, they have homogeneous data to work with, and they ultimately boil down to very simple operations in extremely predictable loops so they can pull out all the stops when it comes to optimization. The bad news is that since they are running on their own, if they’re inefficient, there’s no other useful work being accomplished when the decoders are stalled. Careful design is a necessity if we want to ensure that things go smoothly come decode time.

In this post, I’ll start by looking at Huffman coding, or rather, Huffman decoding; encoding, we won’t have to worry about much, since it’s an inherently easier problem to begin with and the design decisions we’ll make to enable fast decoding will also make encoding faster. Required reading for everything that follows will be my earlier posts [“A whirlwind introduction to dataflow graphs”](https://fgiesen.wordpress.com/2018/03/05/a-whirlwind-introduction-to-dataflow-graphs/) as well as my series [“Reading bits in far too many ways”](https://fgiesen.wordpress.com/2018/02/19/reading-bits-in-far-too-many-ways-part-1/) ([part 2](https://fgiesen.wordpress.com/2018/02/20/reading-bits-in-far-too-many-ways-part-2/), [part 3](https://fgiesen.wordpress.com/2018/09/27/reading-bits-in-far-too-many-ways-part-3/)). I will assume the contents of these posts as known, so if something is unclear and has to do with bit IO, it’s in there.

### Huffman (de)coding basics

Huffman coding is a form of variable-length coding that in its usual presentation is given a finite symbol alphabet *Σ* along with a positive count *f s* (the

*frequency*) of how often each symbol

*s*occurs in the source. Huffman’s classic algorithm then assigns variable-length binary codes (meaning strings of 0s and 1s) of length

*c*to each symbol that guarantee unique decodability and minimize the number of bits in the coded version of the source; we want to send the symbols from the source in fewer bits, and the way to do so is to assign shorter codes to more frequent symbols. To be precise, it solves the optimization problem

s(i.e. minimize the number of bits sent for the payload, because each *c s*-bit code word occurs

*f*times in the source) for integer

s*c*subject to the constraints

sThe first of these constraints just requires that code lengths be positive integers and is fairly self-explanatory, the second requires equality in the Kraft-McMillan inequality which guarantees that the resulting code is both complete and uniquely decodable; in fact, let’s just call the quantity the “Kraft defect”. When

*K*<0, the code has redundancy (i.e. there free code space left for assignment), for *K*=0 it is complete, and *K*>0 is over-complete (not uniquely decodable or using more code space than is available).

Huffman’s algorithm to perform this construction is a computer science classic, intuitive, a literal textbook example for greedy algorithms and matroids, and it even gives us not just the sequence of code lengths, but an actual code assignment that achieves those code lengths. Nevertheless, actual Huffman codes are of limited use in applications, primarily due to one big problem: the above problem places no upper bound on the code lengths, and indeed a *n*-symbol alphabet can reach a maximum code length of up to *n*-1 given the right (adversarial) frequency distribution that produces a fully left- or right-leaning tree. 1 This is bad for both encoders and decoders, which generally

*have*to adhere at the very least to limits derived from the choice of target platform (mostly register width) and bit I/O refill strategy (see my long series on the topic mentioned earlier), although it is often desirable to enforce much tighter limits (more on that below). One way to accomplish this is by taking the results of the standard Huffman construction and using heuristics and local rewrite rules on either the tree or the code lengths to make the longest codes shorter at the expense of making some other (more frequent) codes longer than they would otherwise have to be. Another easy heuristic option is to just use the regular Huffman construction and if codes end up over-long, divide all symbol frequencies by 2 while rounding up (so that non-zero symbol frequencies never drop to zero) and keep trying again until success. This works because it keeps the frequencies of more popular symbols approximately correct and in the right relation to each other, while it flattens out the distribution of the less popular symbols, which all end up eventually having symbol frequencies of 1, resulting in a uniform symbol distribution at the bottom end. A non-heuristic, actually optimal option is to directly solve a constrained version of the above optimized problem that adds a maximum codeword length constraint. The standard solution to the resulting combinatorial optimization problem is called the

[package-merge algorithm](https://en.wikipedia.org/wiki/Package-merge_algorithm).

A related observation is that there is really no particular reason to prefer the code assignment produced by Huffman’s algorithm. Even for cases where no length-limiting is required to fall within usual limits, there are usually many possible code assignments that all result in the exact same bit count for the payload portion; and given an assignment of code length to symbols, it is easy to come up with a codeword assignment that matches those code lengths. In short, the per-symbol code lengths make a difference to how efficient a given code is, but we can freely choose which codes we assign subject to the length constraint, and can do so in a way that is convenient for us.

This has the effect of deciding on a single *canonical* Huffman tree for each valid sequence of code lengths (valid here meaning *K*=0), even in cases where Huffman’s algorithm generates distinct trees and code assignments that happen to have the same code lengths. The actual coded bits are just part of the puzzle; an actual codec needs to transmit not just the coded bits, but also enough information for the decoder to work out what codes were assigned to which symbols, and specifying a canonical Huffman code requires less information than its non-canonical counterpart would. 2 There are several options as to how exactly we assign codes from code lengths, the most common of which is to assign code words sequentially to symbols in lexicographic order for the (

*c*,

s*s*) pairs—that is, code lengths paired up with symbol values, ordered by ascending code length and then symbol value.


[3](https://fgiesen.wordpress.com#fn3)Using canonical, length-limited codes is a common choice. For example, [Deflate](https://datatracker.ietf.org/doc/html/rfc1951) (the algorithm used in zlib/ZIP) uses canonical codes limited to a maximum length of 15 bits, and JPEG limits the maximum code length to 16 bits.

In principle, such a data stream can be decoded by reading a bit at a time and walking the Huffman tree accordingly, starting from the root. Whenever a leaf is reached, the corresponding symbol is emitted and the tree walk resets back to the root. However, processing data one bit at a time in this fashion is very slow, and implementations generally avoid it. Instead, decoders try to decode many bits at once. At the extreme, when all code lengths are below some upper bound *N*, a decoder can just “peek ahead” *N* bits into the bitstream, and prepare a table that contains the results of the tree walks for all 2 N possible bit patterns; table entries store which symbol was eventually reached and how many bits were actually consumed along the way. The decoder emits the symbol, advances its read cursor by the given number of bits, and reads the next symbol.

This method can be much faster and is easy to implement; however, when *N* is large, the resulting tables will be too, and there are steep penalties whenever table sizes start exceeding the sizes of successive cache levels, since the table lookups themselves are essentially random. 4 Furthermore, most sources being compressed aren’t static, so Huffman tables aren’t used forever. A typical Huffman table will

last somewhere between 5 and 100 kilobytes of data. For larger

*N*, it’s easy for table initialization to take as long, or longer, than actual bitstream decoding with that table, certainly for shorter-lived Huffman tables. The compromise most commonly used in practical implementations is to use a multi-level table scheme, where individual tables cover something like 9 to 12 bits worth of input. All the shorter symbols are decoded in a single table access, but the entries for longer symbols don’t contain a symbol value; instead, they reference a secondary table that resolves the remaining bits (there can be many such secondary tables). The point of Huffman coding is to assign shorter codes to more common symbols, so having to take a secondary table walk is relative uncommon. And of course there are many possible variants of this technique: table walks can do more than 2 levels, and in the other direction, if we have many shorter codes (say at most 4 bits long), then a single access to a 512-entry, 9-bit table can resolve two symbols (or even more) at once. This can accelerate decoding of very frequent symbols, at the expense of a more complicated decoder inner loop and slower table build step.


[5](https://fgiesen.wordpress.com#fn5)### Huffman coding in Oodle

Our older codecs, namely Oodle LZH and LZHLW, used a 15-bit code length limit and multi-level tables, both common choices. The problem with this design is that every symbol decode needs to check whether a second-level table lookup is necessary; a related problem is that efficient bit IO implementations maintain a small buffer that is periodically refilled to contain somewhere between 23 and 57 bits of data (details depend on the choice of bit IO implementation and whether we’re on a 32-bit or 64-bit platform, see the bit-IO series I referenced earlier). When we know that codes are guaranteed to be short enough, we can decode multiple symbols per refill. This is significant because refilling the bit buffer is about as expensive as decoding a symbol itself; being able to always decode two symbols per refill, as opposed to one, has the potential to reduce refill overhead from around 50% of decode time to about 33% on 32-bit targets!

When Charles first prototyped what later turned into Kraken, he was using our standard bit IO implementation, which uses byte-wise refill so post-refill, the 32-bit version guarantees at least 25 usable bits, while for in 64-bit the number is 57 bits, all typical limits.

Therefore, if codes are limited to at most 12 bits, the 32-bit decoder can sustain a guaranteed two symbols per refill; for 64-bit, we can manage 4 decodes per refill (using 48 out of 57 bits). As a side effect, the tables with a 12-bit limit are small enough that even without a multi-level table scheme, everything fits in the L1D cache. And if codes are limited to 11 bits, the 32-bit decoders still manage 2 symbols per refill, but the 64-bit decoders now go up to 5 decodes per refill, which is a nice win. Therefore, the newer Oodle codecs use Huffman codes length-limited to only 11 bits, which allows branch-free decoding of 2 symbols per refill on 32-bit platforms, and 5 symbols per refill on 64-bit targets.[6](https://fgiesen.wordpress.com#fn6)

The other question is, of course, how much limiting the code lengths aggressively in this way costs in terms of compression ratio, to which the answer is: not much, although I don’t have good numbers for the 11-bit limit we eventually ended up with. For a 12-bit limit, the numbers in our tests were below a 0.1% hit vs. the original 15-bit limit (albeit with a note that this was when using proper package-merge, and that the hit was appreciably worse with some of the hackier heuristics). We ended up getting a fairly significant speed-up from this choice, so that slight hit is well worth it.

With these simplifications applied, our core Huffman decoder uses pre-baked table entries like this:

struct HuffTableEntry { uint8_t len; // length of code in bits uint8_t sym; // symbol value };

and the decoder loop looks something like this (32-bit version):

while (!done) { bitbuf.refill(); // can decode up to 25 bits without refills! // Decode first symbol { intptr_t index = bitbuf.peek(11); HuffTableEntry e = table[index]; bitbuf.consume(e.len); output.append(e.sym); } // Decode second symbol { intptr_t index = bitbuf.peek(11); HuffTableEntry e = table[index]; bitbuf.consume(e.len); output.append(e.sym); } }

Note that with a typical bit buffer implementation, the `peek`

operation uses a single bit-wise AND or shift instruction; the table access is a 16-bit load (and load address calculation, which depending on the target CPU might or might not be an addressing mode). The bit buffer `consume`

operation usually takes an integer shift and an add, and finally the “append” step boils down to an integer store, possibly an integer shift to get the symbol value in the right place prior to the store (the details of this very much depend on the target ISA, I’ll get into such details in later posts in this series), and some pointer updating that are easily amortized if the loop is unrolled more than just twice.

That means that in terms of the work we’re doing, we’re already starting out with something around 5-7 machine instructions per symbol, and if we want good performance, it matters a lot what exactly those instructions are and how they relate. But before we get there, there’s a few other details about the resulting dataflow to understand first.

The first and most important thing to note here is what the critical path for the entire decoder operation is: everything is in serialized through the bit buffer access. The `peek`

operation depends on the bit buffer state after the previous `consume`

, the table access depends on the result of the `peek`

operation, and the `consume`

depends on the result of the table access (namely the `len`

field) which completes our cycle. This is the critical dependency chain for the entire decoder, and the actual symbol decoding or output isn’t even part of it. Nothing in this loop depends on or cares about `e.sym`

at all; its load and eventual store to the output buffer should be computed eventually, but there’s no rush. The code length determination, on the other hand, is our primary bottleneck. If the critical computation for `peek`

and `consume`

works out to a single 1-cycle latency integer instruction each (which it will turn out it does on most of the targets we’ll see later in this series), then everything hinges on how fast we can do that table access.

On current out-of-order CPUs (no matter the ISA), the answer usually turns out to be 4 or 5 clock cycles, making the critical path from one symbol decoded to the next either 6 or 7 clock cycles. This is very bad news, because as just pointed out, we’re executing around 5-7 instructions per symbol decoded, total. This means that, purely from the dependency structure, we’re limited to around 1 instruction per cycle average on CPUs that can easily sustain more than 3 instructions per cycle given the right code. Viewed another way, in those 7 cycles per symbol decoded, we could easily run 21 independent instructions (or even more) if we had them, but all we do is something like 6 or 7.[7](https://fgiesen.wordpress.com#fn7)

The obvious solution here is to not have a single bit buffer (or indeed bitstream), but several at once. Once again we were not the first or only ones to realize this, and e.g. Yann Collet’s Huff0 uses the same idea. If the symbols we want to decode are evenly distributed between multiple bitstreams, we can have multiple one-symbol-at-a-time dependency chains in flight at once, and hopefully get to a state where we’re mostly (or even completely) limited by instruction throughput (i.e. total instruction count) and not latency.

Our high-level plan of attack will be exactly that. Huff0 uses 4 parallel bitstreams. For reasons that will become clearer in subsequent parts of this series, Huffman coding in the newer Oodle codecs has two different modes, a 3-bitstream mode and a 6-bitstream mode. Using more bitstreams enables more parallelism but the flipside is that it also requires more registers to store the per-bitstream state and is more sensitive to other micro-architectural issues; the actual counts were chosen to be a good compromise between the desires of several different targets.[8](https://fgiesen.wordpress.com#fn8)

For the rest of this post, I’ll go over other considerations; in the next part of this series, I plan to start looking at some actual decoder inner loops.

### Aside: tANS vs. Huffman

The ANS family of algorithms is the new kid on the block among entropy coders. Originally we meant to use tANS in the original Kraken release back in 2016, but the shipping version of Kraken doesn’t contain it; it was later added as a new entropy coding variant in 2018 along with Leviathan, but is rarely used.

However, one myth that was repeatedly claimed around the appearance of tANS was that it is “faster than Huffman”. While it is true that some tANS decoders are faster than some Huffman decoders, this is mostly an artifact of other implementation choices and the resulting dependency structure of the decoder, so I want to spend a few paragraphs explaining when and why this effect appears, and why despite it, it’s generally not a good idea to replace Huffman decoders with tANS decoders.

I’m not going to explain any of the theory or construction of tANS here; all I’ll note is that the individual per-symbol decode step uses tables similar to a Huffman decode table, and paraphrasing [old code from Charles](http://cbloomrants.blogspot.com/2015/10/huffman-performance.html) here, the key decode step ends up being:

HuffTableEntry e = table[state]; state = next_state[state] | bitbuffer.get(e.len); output.append(e.sym);

In essence, this is a “lookahead Huffman” decoder, where each stream keeps *N* bits of lookahead at all times. Instead of looking at the next few bits in the bit buffer to figure out the next code length, we already have enough bits to figure out what the next code is stored in our `state`

, and after decoding a symbol we shift out a number of bits corresponding to the length of the code and replenish the bottom of our state from the bitstream.[9](https://fgiesen.wordpress.com#fn9)

The bits come from a different place, and we now have the extra `state`

de-facto shift register in the mix, so why would this run faster, at least sometimes? Again we need to look at the data dependencies.

In the regular Huffman decode, we had a single critical dependency chain with the peek/table lookup/consume loop, as well as the bit-buffer refill every few symbols. In this version of the loop, we get not one but two separate dependency chains:

- The
`state`

update has a table lookup (two in fact, but they’re independent and can overlap), the bit buffer`get`

operation to get the next set of low bits for the next state (usually something like an integer add and a shift), and an OR to combine them. This is not any better than the regular Huffman decoder (in fact it’s somewhat worse in multiple ways), but note that the high-latency memory loads happen*before*any interactions with the bit buffer. - The bit buffer update has the periodic refill, and then the
`get`

operations after the`state`

table lookups (which are a combined`peek`

and`consume`

).

The crucial difference here is that in the regular Huffman decoder, most of the “refill” operation (which needs to know how many bits were consumed, load extra bytes and shift them into place, then do some accounting) is on the same dependency chain as the symbol decoding, and decoding the next symbol after a refill can make no meaningful progress until that refill is complete. In the TANS-style decoder, the refill can overlap with the state-dependent table lookups; and then once those table lookups complete, the updates to the bit buffer state involve only ALU operations. In throughput terms the amount of work per symbol in the TANS-style decoder is not better (in fact it’s appreciably worse), but the critical-path latency is improved, and when not using enough streams to keep the machine busy, that latency is all that matters.

A related technique that muddles this further is that ANS-based coders can use interleaving, where (in essence) we just keep multiple `state`

values around, all of which use the same underlying bitstream. This gives us twice the parallelism: two TANS decoders with their own `state`

are independent, and even making them share the same underlying bitstream keeps much of the advantage, because the high-latency portion (the table lookup) is fully overlapped, and individual reads from the bit buffer (once all the lengths are known) can usually be staggered just 1 cycle apart from each other.

A 2× interleaved tANS decoder is substantially faster than a single-stream Huffman decoder, and has lower incremental cost (a single extra integer state is easier to add and track than the registers required for a second bitstream state). However it also does more work per symbol than a 2-stream Huffman decoder does, so asymptotically it is slower—if you ever get close to the asymptote, that is.

A major disadvantage of tANS-style decoding is that interleaving multiple states into the same bitstream means that there is essentially only a single viable decoder implementation; bits need to be read in the same way and at the same time by all decoders to produce the same results, fast implementations need larger and more expensive to set up tables than a straight Huffman decoder, plus other overheads in the bitstream. In contrast, as we’ll see later, the 6-stream Huffman

coding variant is decoded on some platforms as two 3-stream blocks, which would not easily map to a tANS-style implementation. In the end, the lower asymptotic performance and decreased flexibility is what made us stick with a regular Huffman decoder in Oodle Data, because as it turns out we can get decent wins from decoding the bitstreams somewhat differently on different machines.

### Huffman table initialization

As mentioned several times throughout this post, it’s easy for Huffman table initialization to become a major time sink, especially when tables are large, used for just a short time, or the table builder is unoptimized. Luckily, optimizing the table builder isn’t too hard, and it also gives a nice and intuitive (to me anyway) view of how canonical Huffman codes work in practice.

For now, suppose that decoding uses a MSB-first bit packing convention, i.e. a bit-at-a-time Huffman decoder would read the MSB of a codeword first and keep reading additional less significant bits until the symbol is determined. Although our 11-bit code length limit is quite short, that’s still a large number of bits to work through in an example, so let’s instead consider at a toy scenario with a code length limit of 4 bits and four symbols a, b, c, d with code lengths 1, 3, 2, and 3 bits, respectively.

The code length limit of 4 bits means we have a total space of 16 possible 4-bit patterns to cover; I’ll refer to each such bit pattern as a “slot”. Our 1-bit symbol “a” is the first and shortest, which means it gets assigned first, and as such gets a 1-bit code of “0”, with the next 3 bits irrelevant. In short, all slots with a leading 0 bit correspond to the symbol ‘a’; there’s 24-1 = 8 of them. The next-shortest symbol is ‘c’, which get the next available 2-bit code. All codes starting with 0 are taken; the next available slot starts with a 2-bit pattern of “10”, so that’s what we use. There are 24-2 = 4 slots corresponding to a bit pattern starting “10”, so that’s what we assign to c. The two remaining symbols ‘b’ and ‘d’ get 3-bit codes each. Anything starting with “0” or “10” is taken, so they need to start with “11”, which means our choice is forced: ‘b’ being earlier in the alphabet (since we break ties in code length by which symbol is lower-valued) gets the codes starting “110”, ‘d’ gets “111”, and both get 24-3=2 table slots each. If we write up the results, we get:

| Code | Sym | Len |
|---|---|---|
0000 |
a | 1 |
0001 |
a | 1 |
0010 |
a | 1 |
0011 |
a | 1 |
0100 |
a | 1 |
0101 |
a | 1 |
0110 |
a | 1 |
0111 |
a | 1 |
1000 |
c | 2 |
1001 |
c | 2 |
1010 |
c | 2 |
1011 |
c | 2 |
1100 |
b | 3 |
1101 |
b | 3 |
1110 |
d | 3 |
1111 |
d | 3 |

Note that we simply assigned all of the code space in linear order to symbols sorted by their code length and breaking ties by symbol value, where each symbol gets 2 N–k slots, where

*N*is the overall code length limit and

*k*is the code length for the symbol in question. At any step, the next code we assign simply maps to the first few bits of the next available table entry. It’s trivial to discover malformed codes in this form: we need to assign exactly 2

slots total. If any symbol has a code length larger than

*N**N*or we end up assigning more or less than that number of slots total, the code is, respectively, over- or under-complete; the current running total of slots assigned is a scaled version of the number in the Kraft inequality.

Moreover, it should also be obvious how the canonical table initialization for a MSB-first code works out in practice: the table is simply written top to bottom in linear order, with each entry repeated 2 N–k times; in essence, a slightly more complicated

`memset`

. Eventually, each slot is just duplicated a small number of times, like 4, 2 or just 1, so as code lengths get closer to the limit it’s better to use specialized loops and not treat it as a big memset anymore, but the basic idea remains the same.This approach requires a list of symbols sorted by code length; for Oodle, the code that decodes Huffman table descriptions already produces the symbol list in this form. Other than that, it is straightforward.

The only wrinkle is that, for reasons to do with the details of the decoder implementation (which will be covered in future posts), the fast Huffman decoders in Oodle do not actually work MSB-first; they work LSB-first. In effect, we produce the table as above, but then reverse all the bit strings. While it is possible to directly build a canonical Huffman decode table in a LSB-first fashion, all the nice (and SIMD-friendly) sequential memory writes we had before now turn into scatters, which is a lot messier. It turns out to be easier and faster to first build a MSB-first table as described above and then apply a separate bit-reverse permutation to the elements to obtain the corresponding LSB-first decoding table. This is extra work, but bit-reverse permutations have a very regular structure and also admit a fast SIMD implementation that ends up being essentially a variant of a matrix transpose operation. In our experiments, the SIMD-friendly (and memset-able) MSB-first table initialization followed by a MSB→LSB bit-reverse was much faster than a direct LSB-first canonical table initialization, and LSB-first decoding saved enough work in the core decode loops to be worth the extra step during table building for the vast majority of our Huffman tables, so that’s what we settled on.

And that’s it for the high-level overview of Huffman decoding in Oodle Data. For the next few upcoming posts, I plan to get into detail about a bunch of the decoder loops we use and the CPUs they are meant for, which should keep us busy for a while!

### Footnotes

[1] An easy way to construct a pathological frequency distribution is to pick the symbol frequencies as Fibonacci numbers. They grow exponentially with *n*, but not so quickly as to make the symbol frequencies required to exceed common practical code length limits impossible to occur for typical block sizes. The existence of such cases for at least certain input blocks means that implementations need to handle them.

[2] There are strictly more Huffman trees than there are canonical Huffman trees. For example, if symbol ‘a’ has a 1-bit code and symbols ‘b’ through ‘e’ all get 3-bit codes, then our corresponding canonical tree for that length distribution might be `(a ((b c) (d e)))`

, but it is equally possible (with the right symbol frequencies) to get say the tree `(a ((b d) (c e)))`

or one of many other possible trees that all result in the same code lengths. The encoded size depends only on the chosen code lengths, and spending extra bits on distinguishing between these equivalent trees is wasteful unless the tree shape carries other useful information, which it can in some applications, but not in usual Huffman coding. Along the same lines, for any given Huffman tree there are in general many possible sets of symbol frequencies that produce it, so sending an encoding of the original symbol frequencies rather than the tree shape they result in is even more wasteful.

[3] When assigning codewords this way and using a MSB-first bit packing convention, the blocks of codes assigned to a given code length form intervals. When codes are limited to *N* bits, that means the length of a variable-length code word in the bitstream can be determined by figuring out which interval a code falls into, which takes at most *N*-1 comparisons against constants of width ≤*N*-1 bits. This allows for different, and often more efficient, implementation options for the latency-critical length determination step.

[4] This is inherent: the entire point of entropy coding is to make bits in the output bitstream approach an actual information content around 1 bit. In the process of Huffman coding, we are purposefully making the output bitstream “more random”, so we can’t rely on locality of reference to give us better cache hit rates here.

[5] Decoding multiple symbols at once may sound like an easy win, but it does add extra work and complications to decoding symbols that are long enough not to participate in pair-at-a-time decoding, and once again the table build time needs to be carefully watched; generally speaking multi-symbol decoding tends to help on extremely redundant input but slows down decoding of data that achieves maybe 7 bits per byte from Huffman coding, and the latter tends to be more common than the former. The actual evaluation ends up far from straightforward and ends up highly dependent on other implementation details. Multi-symbol decoding tends to look good when plugged into otherwise inefficient decoders, but as these inefficiencies are eliminated the trade-offs get more complicated.

[6] No doubt we were neither the first nor last to arrive at that particular design point; with an 8-bit alphabet, the set of viable options for at least two decodes per refill if 32b targets matter essentially boils down to 9b to 12b, with 11b being the first where 5 decodes/refill on 64b targets are possible.

[7] This gap is one of the things that makes multi-symbol decoding look great when plugged into a simple toy decoder. Decoding multiple symbols at once requires extra bookkeeping and instructions, and also introduces extra dependencies between the stores since the number of symbols decoded in each step is no longer known at compile time and folded into an addressing mode, but when we’re only using about a third of the capacity of the machine, inserting extra instructions into the symbol decode is very cheap.

[8] Oodle has the same bitstream format for everyone; while we can (and do) make choices to avoid pathologies on all of the targets we care about, any choice we make that ends up in the bitstream needs to work reasonably well for all targets.

[9] `next_state`

here essentially just tabulates a shift and mask operation; in a “real” tANS decoder this can be more complicated, but when we’re looking at a case corresponding to a Huffman table and symbol distribution, that’s all it does.

Can’t you leverage the branch predictor to cut the fundamental data dependency chain of huffman decoding? In the decoder that doesn’t use prefix tables the inner loop is

loop {

prefix = Peek(n);

len = minCodeLen;

while (prefix >= base[len + 1]) len++;

*out++ = (prefix >> (n – len)) – offset[len];

Consume(len);

}

If the branch predictor would miraculous predict the exit condition correctly, then the chain for bitbuffer would just be a single cycle.

Now it’s unreasonable to assume the BP would do this. So the optimization in moffat/turpin is

loop {

prefix = Peek(n);

len = lengthTable[prefix >> k];

while (EXPECT_FALSE(prefix >= base[len + 1])) len++;

*out++ = (prefix >> (n – len)) – offset[len];

Consume(len);

}

Now in the vast majority of iterations the while loop is not taken and the BP will do a great job, however now the load is on the data chain. If k == 0 then it’s guaranteed the while loop will be skipped. The problem to me seems to be that lengthTable is incredibly low information. For most frequent prefixes the value only depends on the few most significant bits. With the least significant bits belonging to the next symbol. So it seems one could do

len = minCodeLen;

loop {

prefix = Peek(n);

while (EXPECT_FALSE(prefix >= base[len + 1])) len++;

*out++ = (prefix >> (n – len)) – offset[len];

Consume(len);

len = nextLengthEstimationTable[prefix];

}

The nextLengthEstimation table has much higher information content. It depends on the high bits to determine which of the low bits belong to the next symbol and the value depends on low bits.

I wouldn’t be surprised with a table size of 15 bits that in a very large fraction of the iterations the while loop is still not executed. So now we have

len -> bitbuffer = bitbuffer < prefix = bitbuffer >> (64 – n) -> len = table[prefix] (6 cycle chain)

Which makes a 7 cycle chain over over 2 iterations or 3.5 cycles per iteration.

Branch mispredictions in this are a significant cost you can’t neglect, because the discovery that the branch was even wrong in the first place is a load with a data-dependent address down from the critical path, increasing the effective branch misprediction latency by the load latency here. Even assuming fairly low costs of branch misprediction = 12 cycles, load latency of 4 cycles, plus another cycle for the compare and branch, that’s about 5 cycles after len is known until the branch result is known, and then 12 extra cycles worth of work in the pipeline that gets invalidated, so in effect you lose about 17 cycles worth of speculative work every time this happens. Even if that only happens once every 17 symbols (which seems wildly optimistic to me) that increases the expected cost by 1 cycle per symbol decoded, and I doubt it’s anywhere near that good in practice.

Separately, a table with 2^15 entries is already impractically large, for us anyway, for two separate reasons that are about equally important: first, that table size is all but guaranteeing you’re going to be thrashing the L1 data cache especially when there are multiple hardware threads active, and second, Huffman tables have a limited lifetime and table setup cost matters. In our case, we have a few tables that are long-lived (meaning they get used to decode about 60-80k worth of symbols, or even more in rare cases), but mostly they’re used for say ballpark 2k-8k worth of data. Even at the top end of that range, that means a 32k-entry table sets up 4 table entries for every one that is actually used by the decoder. You need to be careful with the accounting here, it’s easy to bake a lot of work up front into the tables, but you’re still doing that work, just during table setup not decoding.

If you’re going to set up a large table, the most straightforward thing is to make one that lets you decode multiple symbols at once where possible. This is a very straightforward change to the decoder that keeps it essentially branch-free, but does make the table entries larger and table setup more expensive. It’s helpful for very skewed distributions but at least in our case it’s pretty common for o0 entropy to be over 7 bits/symbol so you really do need something like 14 or 15 bits worth of table entries if you want to get double-decodes consistently. That’s at least 3 bytes per table entry – you need values for two decoded symbols (2 bytes), total number of bits consumed, and a flag or symbol count to tell you whether it was one or two symbols, which for a 15-bit table means about 96k, firmly putting you in a region where you’re going to be missing the L1D cache a lot, and taking up a sizeable fraction of L2 besides. Not good.

And of course using multiple streams sidesteps the issue entirely. Our most common format uses 6 streams, which means that 7-cycle latency from one symbol to the next is not much of a problem. It does mean you really need that table to fit comfortably in L1D and you don’t want any data-dependent branches in there because any misprediction caused by one stream wipes useful work done on all the other ones. For many-stream the major goals are just to keep state per stream small (lest you run out of registers), avoid stalls, and reduce instruction count as much as possible, since many-stream will let you move to a range where you’re limited by instruction throughput and not latency.

Oodle’s current decoders on recent Intel or AMD CPUs average well under 2 cycles per symbol decoded with all overheads included – code length decoding, table setup, the main fast loops, and the more careful loops that we switch to near the end of the input or output buffers.

Thank you for your reply. I understand that multiple streams is superior. I’m also interested, mostly as intellectual masturbation, how quickly you can parse a single stream.

There is a tantalizingly solution using no L1 cache tables at all. Something like

https://godbolt.org/z/GhP335e9P

would be an all register solution, useable if the code lengths are bounded [3 .. 11] or [4 .. 12]. Currently the chain is quite a bit longer than a L1 cache lookup, mainly because of long latencies of some of the instructions.

Being an expert on the subject,do you know the new technique of set shaping theory?

There is a lot of interest in this topic.

Nope!

In the table initialisation section you say “It turns out to be easier and faster to first build a MSB-first table as described above and then apply a separate bit-reverse permutation to the elements…”

Can you elaborate on what you mean here? I tried to work out what this “transpose variant” would look like, but I can’t seem to solve it without using a scatter.

For 16-bit entries and 128-bit vectors, it’s convenient to work in groups of 8×8. A single vector load grabs 8 adjacent entries.

Say your table has N entries. Do 8 loads at offsets 0, N/8, 2*N/8, …, 7*N/8 into 8 SIMD registers v0,…,v7. You now have 64 table entries in registers, and if you look at their corresponding table entries, you can number them: (MSB on the left, LSB on the right):

y2y1y0—-…—-|x2x1x0

“y” is the “row” index (top index bits), x is the “column” index (bottom index bits), “|” indicates that those 3 bits are element indices all in the same SIMD register. The — index bits (the middle bits) we’ll ignore for now.

If we do a 8×8 matrix transpose on these 8 vectors (standard SIMD algorithm, I also wrote some posts about SIMD transposes on this blog something like 10 years ago) then write down the indices, transposing swapped rows and columns, so now we have:

x2x1x0—-…—-|y2y1y0

Progress! That swapped the group of bottom 3 index bits with the top 3 index bits as a block, but didn’t reverse the order within the group.

That’s easily remedied though. We loaded our 8 vectors “in order”, but we instead load the 8 vectors not from offsets (0,1,2,3,4,5,6,7)*N/8, but instead offsets (0,4,2,6,1,5,3,7)*N/8 (note that’s a 3-bit bit-reversal permutation) then we start out (pre-transpose) with

y0y1y2—-…—-|x2x1x0

and end up (post-transpose) with

x2x1x0—-…—-|y0y1y2

the 8 combinations of x2x1x0 are in 8 different registers now, so while storing, we can also apply the bit-reversal permutation to the store offsets to get an effective permutation of

x0x1x2—-…—-|y0y1y2

So far, so good. We’ve reversed the top and bottom 3 index bits and swapped them to the right place, and we’re only doing aligned loads/stores and an in-register SIMD transpose to do it. Now all we need to do is to handle the middle bits.

If you do this out of place, we’re basically done now: we can use the above procedure to map table indices

y2y1y0|x2x1x0

to

x0x1x2|y0y1y2

This needs one regular integer bit reverse per group of 64 elements, and you just loop over all relevant values of “middle” here. You can just use a table (or whatever other method you want) to reverse the bits of “middle” here.

You can even do this in-place using an extension of this technique that Dougall Jones worked out here https://gist.github.com/dougallj/8acf4233e3534f3278bda5fdaa2f4051#file-fancy-bitreverse-c-L132; it still uses this basic approach to peel off square blocks (in his case 4×4 since he’s working with 128-bit vectors and blocks of 32-bit elements), but you now end up with two possible cases, since at the block level, some blocks switch places with another block and other blocks stay where they are. The out-of-place version is simpler.