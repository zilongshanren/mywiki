---
title: Binary alias coding
url: https://fgiesen.wordpress.com/2014/12/08/binary-alias-coding/
published: '2014-12-08'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Binary alias coding

Applying the rANS-with-alias-table construction from [“rANS with static probability distributions”](https://fgiesen.wordpress.com/2014/02/18/rans-with-static-probability-distributions/) to Huffman codes has some interesting results. In a sense, there’s nothing new here once you have these two ingredients. I remember mentioning this idea in a mail when I wrote [ryg_rans](https://github.com/rygorous/ryg_rans), but it didn’t seem worth writing an article about. I’ve changed my mind on that: while the restriction to Huffman-like code lengths is strictly weaker than “proper” arithmetic coding, we do get a pretty interesting variant on table/state machine-style “Huffman” decoders out of the deal. So let’s start with a description of how they usually operate and work our way to the alias rANS variant.

### Table-based Huffman decoders

Conceptually, a Huffman decoder starts from the root, then reads one bit at a time, descending into the sub-tree denoted by that bit. If that sub-tree is a leaf node, return the corresponding symbol. Otherwise, keep reading more bits and descending into smaller and smaller sub-trees until you do hit a leaf node. That’s all there is to it.

Except, of course, no serious implementation of Huffman decoding works that way. Processing the input one bit at a time is just a lot of overhead for very little useful work done. Instead, normal implementations effectively look ahead by a bunch of bits and table-drive the whole thing. Peek ahead by *k* bits, say *k=10*. You also prepare a table with 2 k entries that encodes what the one-bit-at-a-time Huffman decoder would do when faced with those k input bits:

struct TableEntry { int num_bits; // Number of bits consumed int symbol; // Index of decoded symbol };

If it reaches a leaf node, you record the ID of the symbol it arrived at, and how many input bits were actually consumed to get there (which can be less than *k*). If not, the next symbol takes more than *k* bits, and you need a back-up plan. Set `num_bits`

to 0 (or some other value that’s not a valid code length) and use a different strategy to decode the next symbol: typically, you either chain to another (secondary) table or fall back to a slower (one-bit-at-a-time or similar) Huffman decoder with no length limit. Since Huffman coding only assigns long codes to rare symbols – that is, after all, the whole point – it doesn’t tend to matter much; with well-chosen *k* (typically, slightly larger than the log2 of the size of your symbol alphabet), the “long symbol” case is pretty rare.

So you get an overall decoder that looks like this:

while (!done) { // Read next k bits without advancing the cursor int bits = peekBits(k); // Decode using our table int nbits = table[bits].num_bits; if (nbits != 0) { // Symbol *out++ = table[bits].symbol; consumeBits(nbits); } else { // Fall-back path for long symbols here! } }

This ends up particularly nice combined with [canonical Huffman codes](http://en.wikipedia.org/wiki/Canonical_Huffman_code), and some variant of it is used in most widely deployed Huffman decoders. All of this is classic and much has been written about it elsewhere. If any of this is news to you, I recommend Moffat and Turpin’s 1997 paper [“On the implementation of minimum redundancy prefix codes”](http://www.researchgate.net/publication/3159499_On_the_implementation_of_minimum_redundancy_prefix_codes/file/3deec51d0e74f8c73e.pdf). I’m gonna assume it’s not and move on.

### State machines

For the next step, suppose we fix *k* to be the length of our longest codeword. Anything smaller and we need to deal with the special cases just discussed; anything larger is pointless. A table like the one above then tells us what to do for every possible combination of *k* input bits, and when we turn the *k*-bit lookahead into explicit state, we get a finite-state machine that decodes Huffman codes:

state = getBits(k); // read initial k bits while (!done) { // Current state determines output symbol *out++ = table[state].symbol; // Update state (assuming MSB-first bit packing) int nbits = table[state].num_bits; state = (state << nbits) & ((1 << k) - 1); state |= getBits(nbits); }

`state`

is essentially a *k*-bit shift register that contains our lookahead bits, and we need to update it in a way that matches our bit packing rule. Note that this is precisely the type of Huffman decoder Charles talks about [here](http://cbloomrants.blogspot.com/2014/02/02-01-14-understanding-ans-3.html) while explaining ANS. Alternatively, with LSB-first bit packing:

state = getBits(k); while (!done) { // Current state determines output symbol *out++ = table[state].symbol; // Update state (assuming LSB-first bit packing) int nbits = table[state].num_bits; state >>= nbits; state |= getBits(nbits) << (k - nbits); }

This is still the exact same table as before, but because we’ve sized the table so that each symbol is decoded in one step, we don’t need a fallback path. But so far this is completely equivalent to what we did before; we’re just explicitly keeping track of our lookahead bits in `state`

.

But this process still involves, essentially, two separate state machines: one explicit for our Huffman decoder, and one implicit in the implementation of our bitwise IO functions, which ultimately read data from the input stream at least one byte at a time.

### A bit buffer state machine

For our next trick, let’s look at the bitwise IO we need and turn that into an explicit state machine as well. I’m assuming you’ve implemented bitwise IO before; if not, I suggest you stop here and try to figure out how to do it before reading on.

Anyway, how exactly the bit IO works depends on the bit packing convention used, the little/big endian of the compression world. Both have their advantages and their disadvantages; in this post, my primary version is going to be LSB-first, since it has a clearer correspondence to rANS which we’ll get to later. Anyway, whether LSB-first or MSB-first, a typical bit IO implementation uses two variables, one for the “bit buffer” and one that counts how many bits are currently in it. A typical implementation looks like this:

uint32_t buffer; // The bits themselves uint32_t num_bits; // Number of bits in the buffer right now uint32_t getBits(uint32_t count) { // Return low "count" bits from buffer uint32_t ret = buffer & ((1 << count) - 1); // Consume them buffer >>= count; num_bits -= count; // Refill the bit buffer by reading more bytes // (kMinBits is a constant here) while (num_bits < kMinBits) { buffer |= *in++ << num_bits; num_bits += 8; } return ret; }

Okay. That’s fine, but we’d like for there to be only one state variable in our state machine, and preferably not just on a technicality such as declaring our one state variable to be a pair of two values. Luckily, there’s a nice trick to encode both the data and the number of bits in the bit buffer in a single value: we just keep an extra 1 bit in the `state`

, always just past the last “real” data bit. Say we have a 8-bit `state`

, then we assign the following codes (in binary):

| in_binary(state) | num_bits |
`0 0 0 0 0 0 0 1` |
0 |
`0 0 0 0 0 0 1 *` |
1 |
`0 0 0 0 0 1 * *` |
2 |
`0 0 0 0 1 * * *` |
3 |
`0 0 0 1 * * * *` |
4 |
`0 0 1 * * * * *` |
5 |
`0 1 * * * * * *` |
6 |
`1 * * * * * * *` |
7 |

The locations denoted `*`

store the actual data bits. Note that we’re fitting 1 + 2 + … + 128 = 255 different states into a 8-bit byte, as we should. The only value we’re not using is “0”. Also note that we have `num_bits = floor(log2(state))`

precisely, and that we can determine `num_bits`

using [bit scanning](https://fgiesen.wordpress.com/2013/10/18/bit-scanning-equivalencies/) instructions when we need to. Let’s look at how the code comes out:

uint32_t state; // As described above uint32_t getBits(uint32_t count) { // Return low "count" bits from state uint32_t ret = state & ((1 << count) - 1); // Consume them state >>= count; // Refill the bit buffer by reading more bytes // (kMinBits is a constant here) // Note num_bits is a local variable! uint32_t num_bits = find_highest_set_bit(state); while (num_bits < kMinBits) { // Need to clear 1-bit at position "num_bits" // and add a 1-bit at bit "num_bits + 8", hence the // "+ (256 - 1)". state += (*in++ + (256 - 1)) << num_bits; num_bits += 8; } return ret; }

Okay. This is written to be as similar as possible to the implementation we had before. You can phrase the `while`

condition in terms of `state`

and only compute `num_bits`

inside the refill loop, which makes the non-refill case slightly faster, but I wrote it the way I did to emphasize the similarities.

Consuming bits is slightly cheaper than the regular bit buffer, refilling is a bit more expensive, but we’re down to one state variable instead of two. Let’s call that a win for our purposes (and it certainly can be when low on registers). Note I only covered LSB-first bit packing here, but we can do a similar trick for MSB bit buffers by using the least-significant set bit as a sentinel instead. It works out very similar.

So what happens when we plug this into the finite-state Huffman decoder from before?

### State machine Huffman decoder with built-in bit IO

Note that our state machine decoder above still just kept the *k* lookahead bits in `state`

, and that they’re not exactly hard to recover from our bit buffer `state`

. In fact, they’re pretty much the same. So we can just fuse them together to get a state machine-based Huffman decoder that only uses byte-wise IO:

state = 1; // No bits in buffer refill(); // Run "refill" step from the loop once while (!done) { // Current state determines output symbol index = state & ((1 << k) - 1); *out++ = table[index].symbol; // Update state (consume bits) state >>= table[index].num_bits; // Refill bit buffer (make sure at least k bits in it) // This reads bytes at a time, but could just as well // read 16 or 32 bits if "state" is large enough. num_bits = find_highest_set_bit(state); while (num_bits < k) { state += (*in++ + (256 - 1)) << num_bits; num_bits += 8; } }

The slightly weird `refill()`

call at the start is just to keep the structure as similar as possible to what we had before. And there we have it, a simple Huffman decoder with one state variable and a table. Of course you can combine this type of bit IO with other Huffman approaches, such as multi-table decoding, too. You could also go even further and bake most of the bit IO into tables like Charles describes [here](http://cbloomrants.blogspot.com/2009/05/05-20-09-some-huffman-notes.html), effectively using a table on the actual `state`

and not just its low bits, but that leads to enormous tables and is really not a good idea in practice; not only are the tables too large to fit in the cache, general-purpose compressors will also usually spend more time building these tables than they ever spend using them (since it’s rare to use a single Huffman table for more than a few dozen kilobytes at a time).

Okay. So far, there’s nothing in here that’s not at least 20 years old.

### Let’s get weird, stage 1

The decoder above still reads the exact same bit stream as the original LSB-first decoder. But if we’re willing to prescribe the exact form of the decoder, we can use a different refilling strategy that’s more convenient (or cheaper). In particular, we can do this:

state = read_3_bytes() | (1 << 24); // might as well! while (!done) { // Current state determines output symbol index = state & ((1 << k) - 1); *out++ = table[index].symbol; // Update state (consume bits) state >>= table[index].num_bits; // Refill while (state < (1 << k)) state = (state << 8) | *in++; }

This is still workable a Huffman decoder, and it’s cheaper than the one we saw before, because refilling got cheaper. But it also got a bit, well, *strange*. Note we’re reading 8 bits and putting them into the *low* bits of `state`

; since we’re processing bits LSB-first, that means we added them at the “front” of our bit queue, rather than appending them as we used to! In principle, this is fine. Bits are bits. But processing bits out-of-sequence in that way is certainly atypical, and means extra work for the encoder, which now needs to do extra work to figure out exactly how to permute the bits so the decoder reads them in the right order. In fact, it’s not exactly obvious that you can encode this format efficiently to begin with.

But you definitely can, by encoding backwards. Because, drum roll: this isn’t a regular table-driven Huffman decoder anymore. What this actually is is a rANS decoder for symbols with power-of-2 probabilities. The `state >>= table[index].num_bits;`

is what the decoding state transition function for rANS reduces to in that case.

In other words, this is where we start to see new stuff. It might be possible that someone did a decoder like this before last year, but if they did, I certainly never encountered it before. And trust me, it *is* weird; the byte stream the corresponding encoder emits is uniquely decodable and has the same length as the bit stream generated for the corresponding Huffman or canonical Huffman code, but the bit-shuffling means it’s not even a regular prefix code stream.

### Let’s get weird, stage 2: binary alias coding

But there’s one more, which is a direct corollary of the existence of [alias rANS](https://fgiesen.wordpress.com/2014/02/18/rans-with-static-probability-distributions/): we can use the [alias method](http://en.wikipedia.org/wiki/Alias_method) to build a fast decoding table with size proportional to the number of symbols in the alphabet, completely independent of the code lengths!

Note the alias method allows you to construct a table with an arbitrary number of entries, as long as it’s larger than the number of symbols. For efficiency, you’ll typically want to round up to the next power of 2. I’m not going to describe the exact encoder details here, simply because it’s just rANS with power-of-2 probabilities, and the `ryg_rans`

encoder/decoder can handle that part just fine. So you already have example code. But that means you can build a fast “Huffman” decoder like this:

kMaxCodeLen = 24; // max code len in bits kCodeMask = (1 << kMaxCodeLen) - 1; kBucketShift = kMaxCodeLen - SymbolStats::LOG2NSYMS; state = read_3_bytes() | (1 << 24); // might as well! while (!done) { // Figure out bucket in alias table; same data structures as in // ryg_rans, except syms->slot_nbits (number of bits in Huffman // code for symbol) instead of syms->slot_nfreqs is given. uint32_t index = state & kCodeMask; uint32_t bucket_id = index >> kBucketShift; uint32_t bucket2 = bucket_id * 2; if (index < syms->divider[bucket_id]) ++bucket2; // bucket determines output symbol *out++ = syms->sym_id[bucket2]; // Update state (just D(x) for pow2 probabilities) state = (state & ~kCodeMask) >> syms->slot_nbits[bucket2]; state += index - syms->slot_adjust[bucket2]; // Refill (make sure at least kMaxCodeLen bits in buffer) while (state <= kCodeMask) state = (state << 8) | *in++; }

I find this remarkable because essentially all other fast (~constant time per symbol) Huffman decoding tricks have some dependence on the distribution of code lengths. This one does not; the alias table size is determined strictly by the number of symbols. The only fundamental data-dependency is how often the “refill” code is run (it runs, necessarily, once per input byte, so it will run less often – relatively speaking – on highly compressible data than it will on high-entropy data). (I’m not counting the computation of `bucket2`

here because it’s just a conditional add, and is in fact written the way it is precisely so that it can be mapped to a compare-then-add-with-carry sequence.)

Note that this one really is a lot weirder still than the previous variant, which at least kept the “space” assigned to individual codes connected. This one will, through the alias table construction, end up allocating small parts of the code range for large symbols all over the place. It’s still exactly equivalent to a Huffman coder in terms compression ratio and code “lengths”, but the underlying construction really doesn’t have much to do with Huffman at all at this point, and we’re not even emitting particular bit strings for code words anymore.

All that said, I don’t think this final variant is actually interesting *in practice*; if I did, I would have written about it earlier. If you’re bothering to implement rANS and build an alias table, it really doesn’t make sense to skimp out on the one extra multiply that turns this algorithm into a full arithmetic decoder (as opposed to quasi-Huffman), unless your multiplier is really slow that is.

But I do find it to be an interesting construction from a theoretical standpoint, if nothing else. And if you don’t agree, well, maybe you at least learned something about certain types of Huffman decoders and their relation to table-based ANS decoders. :)

Indeed, very interesting.

I think the “Stage 1” transformation is another neat way of seeing the fundamental difference between ANS and other entropy coders.