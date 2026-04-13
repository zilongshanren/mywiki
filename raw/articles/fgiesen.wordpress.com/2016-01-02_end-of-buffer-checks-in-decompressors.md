---
title: End-of-buffer checks in decompressors
url: https://fgiesen.wordpress.com/2016/01/02/end-of-buffer-checks-in-decompressors/
published: '2016-01-02'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# End-of-buffer checks in decompressors

This post is about general techniques for handling end-of-buffer checks in code that processes an input stream a byte at a time, or a few bytes at a time at the most. Concretely, I’ll be talking about decompression code, but many of these ideas are also applicable to related sequential input processing tasks like lexical analysis.

### A basic decoder

To show how the problem crops up, let’s look at a simple decompressor and at what happens when we try to make an efficient implementation. Here’s our simple decoder for a toy LZ77 variant:

while (!done) { // main loop if (get_bits(1) != 0) { // match int offset = 1 + get_bits(13); int len = 3 + get_bits(5); copy_match(dest, dest - offset, len); } else { // uncompressed 8-bit literal *dest++ = get_bits(8); } }

This particular coding scheme is just arbitrarily chosen to have a simple example, by the way. It’s not one I would actually use.

How does `get_bits`

look like? The design space of bit IO is a big topic on its own, and I won’t be spending any time on the trade-offs here; let’s just use a basic variant with MSB-first (big endian-like) bit packing, reading the input stream from a memory buffer, one byte at a time:

const uint8_t *input_cursor; // current input cursor const uint8_t *input_end; // end of input buffer uint8_t read_byte() { // If we reached the end of the input buffer, return 0! if (input_cursor >= input_end) return 0; return *input_cursor++; } uint32_t bitcount; // number of bits in bitbuf uint32_t bitbuf; // values of bits (bitcount bits from MSB down) uint32_t get_bits(uint32_t nbits) { assert(0 < nbits && nbits <= 24); // Refill: read extra bytes until we have enough bits // in buffer. Insert new bits below the ones we already // have. while (bitcount < nbits) { bitbuf |= read_byte() << (24 - bitcount); bitcount += 8; } // The requested bits are the top nbits bits of bitbuf. uint32_t ret = bitbuf >> (32 - nbits); // Shift them out. bitbuf <<= nbits; bitcount -= nbits; return ret; }

Note we do an explicit end-of-buffer check in `read_byte`

and return a defined value (0 in this case) past the end of the input stream. This kind of check is generally required to avoid crashes (or buffer overrun bugs!) if there is any chance the input stream might be invalid or corrupted – be it as the result of a deliberate attack, or just a transmission error. Returning 0 past the end of buffer is an arbitrary choice, but a convention I tend to stick with in my code.

### Reducing overhead

As for `get_bits`

, the implementation is a fairly typical one. However, as should be obvious, reading a few bits like this is still a relatively involved process, because every call to `get_bits`

involves the refill check and an update of the bit buffer state. A key trick in many decompressors is to reduce this overhead by separating *looking* at bits from *consuming* them, which allows us to grab lots of bits at once (speculatively), and then later decide how far to move the input cursor. This basically boils down to splitting `get_bits`

into two parts:

uint32_t peek_bits(uint32_t nbits) { assert(0 < nbits && nbits <= 24); // Refill: read extra bytes until we have enough bits // in buffer. Insert new bits below the ones we already // have. while (bitcount < nbits) { bitbuf |= readbyte() << (24 - bitcount); bitcount += 8; } // Return requested bits, starting from the MSB in bitbuf. return bitbuf >> (32 - nbits); } void consume_bits(uint32_t nbits) { assert(bitcount <= nbits); bitbuf <<= nbits; // shift them out bitcount -= nbits; }

Using this new interface, we can modify our decoder to reduce bit IO overhead, by doing a single `peek_bits`

call early and then manually extracting the different sub-fields from it:

while (!done) { // main loop // We read up to 19 bits; grab them all at once! uint32_t bits = peek_bits(19); if (bits & (1u << 18)) { // match bit set? int offset = 1 + ((bits >> 5) & 0x1fff); int len = 3 + (bits & 0x1f); consume_bits(19); // 1b flag + 13b offs + 5b len copy_match(dest, dest - offset, len); } else { // uncompressed 8-bit literal *dest++ = (uint8_t) (bits >> 10); consume_bits(9); // 1b flag + 8b value } }

This trick of peeking ahead and deciding later how many bits were actually consumed is *very* important in practice. The example given here is a simple one; a very important use case is decoding Huffman codes (or other variable-length codes) aided by a look-up table.

Note, however, that we changed the input behavior: before, we really only called `read_byte`

when we knew it was necessary to complete reading the current code. Now, we peek ahead more aggressively, and will actually peek past the end of the input bitstream whenever the last token is a literal. It’s possible to avoid this type of problem by being more restrained in the usage of `peek_bits`

: only ever peek ahead by the minimum amount of bits that we *know* is going to get consumed no matter what. However, doing so forces us to do a bit more work at runtime than the code fragment shown above entails.

However, the variant shown above is still completely correct: our implementation of `read_byte`

checks for the end of the input stream, and returns zeroes once we’ve passed it. However, this is no longer an exceptional condition: rather than being a “contingency plan” in case of corrupted input data, we can now expect to hit this path when decoding many valid bit streams.

In short, we’re taking a check we need for correctness (the end-of-buffer check) and making it serve double duty to simplify the rest of our decoder. So far, all the code we’ve seen is very standard and not remarkable at all. The resulting bit-IO implementation is fairly typical, more so once we stop trying to only call `read_byte`

when strictly necessary and simplify the buffer refill logic slightly by always refilling to have >24 bits in the buffer no matter what the peek amount is.

Even beyond such details, though, this underlying idea is actually quite interesting: the end-of-buffer check is not one we can easily get rid of without losing correctness (or at least robustness in the face of invalid data). But we *can* leverage it to simplify other parts of the decoder, reducing the “sting”.

How far can we push this? If we take as granted that reading past the end of the buffer is never acceptable, what is the least amount of work we can do to enforce that invariant?

### Relaxed requirements

In fact, let’s first go one further and just allow reading past the end-of-buffer too. You only live once, right? Let’s pull out all the stops and worry about correctness later!

It turns out that if we’re allowed to read a few bytes past the end of the buffer, we can use a nifty branch-free refill technique. At this point, I’m going to manually inline the bit IO so we can see more clearly what’s going on:

while (!done) { // main loop // how many bytes to read into bit buffer? uint32_t refill_bytes = (32 - bitcount) / 8; // refill! bitbuf |= read_be32_unaligned(input_cursor) >> bitcount; bitcount += refill_bytes * 8; input_cursor += refill_bytes; assert(bitcount > 24); // peek at next 19 bits uint32_t bits = bitbuf >> (32 - 19); if (bits & (1u << 18)) { // match bit set? int offset = 1 + ((bits >> 5) & 0x1fff); int len = 3 + (bits & 0x1f); // consume_bits(19); bitbuf <<= 19; bitcount -= 19; copy_match(dest, dest - offset, len); } else { // uncompressed 8-bit literal *dest++ = (uint8_t) (bits >> 10); // consume_bits(9); bitbuf <<= 9; bitcount -= 9; } }

This style of branchless bit IO is used in e.g. [Yann Collet’s FSE](http://github.com/Cyan4973/FiniteStateEntropy/) and works great when the target machine supports reading unaligned 32-bit big endian values quickly — the `read_be32_unaligned`

function referenced above. This is the case on x86 (`MOV`

and `BSWAP`

or just `MOVBE`

where supported), ARMv6 and later (`LDR`

provided unaligned accesses are allowed, plus `REV`

when in little-endian mode) and POWER/PPC; not sure about other architectures. And for what it’s worth, I’m only showing 32-bit IO here, but this technique really comes into its own on 64-bit architectures, since having at least 56 bits in the buffer means we can usually go for a long while without further refill checks.

That’s a pretty nice decoder! The only problem being that we have no insurance against corrupted bit streams at all, and even valid streams will read past the end of the buffer as part of regular operation. This is, *ahem*, hardly ideal.

But all is not lost. We know exactly how this code behaves: every iteration, it *will* try reading 4 bytes starting at `input_cursor`

. We just need to make sure that we don’t execute this load if we know it’s going to be trouble.

Let’s say we work out the location of the spot where we need to start being careful:

// Before the decoder runs: const uint8_t *input_mark; if (input_end - input_cursor >= 4) input_mark = input_end - 4; else input_mark = input_cursor;

The simplest thing we can do with that information is to just switch over to a slower (but safe) decoder once we’re past that spot:

while (!done && input_cursor <= input_mark) { // fast decoder here: we know that reading 4 bytes // starting at input_cursor is safe, so we can use // branchless bit IO } while (!done) { // finish using safe decoder that refills one byte at // a time with careful checks! }

This works just fine, and is the technique chosen in e.g. the zlib inflate implementation: one fast decoder that runs when the buffer pointers are well away from the boundaries, and a slower decoder that does precise checking.

Note that the `input_cursor < input_mark`

check is the only addition to our fast decoder that was necessary to make the overall process safe. We have some more prep work, and it turns out we ended up with an entire extra copy of the decoder for the cold “near the end of the buffer” path, but the path we expect to be much more common — decoding while still being safely away from the end of the input stream — really only does that one extra compare (and branch) more than the “fast but unshippable” decoder does!

And now that I’ve done my due diligence and told you about the boring way that involves code duplication, let’s do something *much* more fun instead!

### One decoder should be enough for anyone!

The problem we’re running into is that our buffer is running out of bytes to read. The “safe decoder” solution just tries to be *really* careful in that scenario. But if we’re not feeling very careful today, well, there’s always the ham-fisted alternative: just switch to a *different* input buffer that’s not as close to being exhausted yet!

Our input buffers are just arrays of bytes. If we start getting too close to the end of our “real” input buffer, we can just copy the remaining bytes over to a small temp buffer that ends with a few padding bytes:

uint8_t temp_buf[16]; // any size >=4 bytes will do. while (!done) { if (input_cursor >= input_mark) { assert(input_cursor < input_end); // copy remaining bytes to temp_buf size_t bytes_left = (size_t) (input_end - input_cursor); assert(bytes_left < sizeof(temp_buf)); memmove(temp_buf, input_cursor, bytes_left); // fill rest of temp_buf with zeros memset(temp_buf + bytes_left, 0, sizeof(temp_buf) - bytes_left); // and update our buffer pointers! input_cursor = temp_buf; input_end = temp_buf + sizeof(temp_buf); input_mark = input_end - 4; } assert(input_cursor <= input_mark); // rest of fast decoder using branchless bit IO }

And with that little bit of extra logic, we can use our fast decoder for everything: note that we never read past the bounds of the original buffer. Also note that the logic given above can generate an *arbitrary* amount of trailing zero bytes: if after swapping buffers around, our input cursor hits the mark again, we just hit the refill path again to generate more zeroes. (This is why the copying code uses `memmove`

).

This is nifty already, but we can push this idea much further still.

### Switching input buffers

So far, we’re effectively switching from our regular input buffer to the conceptual equivalent of `/dev/zero`

. But there’s no need for that restriction: we can use the same technique to switch over to a different input buffer altogether.

We again use a temporary transition buffer that we switch to when we reach the end of the current input buffer, but this time, we copy over the first few bytes from the next input buffer after the end of the current buffer, instead of filling the rest with zeroes. We still do this using our small temp buffer.

We place our input mark at the position in the temp buffer where data from the new input buffer starts. Once our input cursor is past that mark, we can change pointers again to resume reading from the new input buffer directly, instead of copying data to the temp buffer.

Note that handling cases like really short input buffers (shorter than our 4-byte “looakhead window”) requires some care here, whereas it’s not a big deal when we do the bounds checking on every consumed input byte. We’re not getting something for nothing here: our “sloppy” end-of-input window simplifies the core loop at the expense of adding some complexity in the boundary case handling.

Once we reach the actual end of the input stream, we start zero-filling, just as before. This all dovetails nicely into my old post [“Buffer-centric IO”](https://fgiesen.wordpress.com/2011/11/21/buffer-centric-io/) which combines very well with this technique. Together, we get almost-zero-copy IO, except for the copies into the transition buffer near buffer boundaries, which only touch a small fraction of all bytes and are there to make our lives easier.

### A final few generalizations

The example I’ve been using was based on a single `get_bits`

(or later `peek_bits`

) call. But this is really not substantial at all. The crucial property we’re exploiting in the decoder above is that we have a known bound for the number of bytes that can be consumed by a single iteration of the loop. As long as we can establish such a bound, we can do a single check per iteration, and in general, we need to check our input cursor at least once inside every loop that consume a potentially unbounded (or at least large) number of input bytes — which in this example is only the main loop.

For the final generalization, note that a lot of compressors use a stream interface similar to zlib. In essence, this is a buffer interface similar to the one described in [“Buffer-centric IO”](https://fgiesen.wordpress.com/2011/11/21/buffer-centric-io/) for both the input and output buffers; the decompressor then gets called and processes data until the input or output buffers are exhausted, the end of stream is reached, or an error occurs, whichever happens first. This type of interface makes the (de)compressor somewhat harder to write but is much more convenient for the *client* code, which can just hand in whatever.

A typical way to implement this type of interface is described in Simon Tatham’s old article [“Coroutines in C”](http://www.chiark.greenend.org.uk/~sgtatham/coroutines.html) — the key property being that the called function needs to be able to save its state at any point where I/O happens, in case it runs out of buffer space; and furthermore it needs to be able to later resume at exactly that point.

The solution is to effectively turn the (de)compressor into a state machine, and Tatham’s article describes a way to do so using a variant of [Duff’s Device](https://de.wikipedia.org/wiki/Duff%E2%80%99s_Device), quite probably the most infamous coding trick in the C language. Most (de)compressors with a zlib-like interface end up using this technique (or an equivalent) so they can jump into the middle of the decoder and resume where they left off.

So why do I mention all this? Well, the technique I’ve outlined in this article is applicable here as well: Tatham’s description assumes byte-level granularity IO, which means there’s generally lots of points inside the decoder main loop where we might need to save our state and resume later. If the decoder instead ensures there’s enough bytes left in the buffer to make it through one full iteration of the main loop no matter what, that means we have many fewer points where we need to save our state and later resume, often only in a single location.

What’s particularly interesting about combining the relaxed-refill technique with a coroutine-style decoder is that all of the refill and transition buffer logic can be pulled outside of the decoder proper. In library code, that means it can be shared between multiple decoders; so the logic that deals with the transition buffers and short input buffers only needs to be implemented and debugged once.

### Discussion

The key simplification in this scheme is relaxing the strict “check for end of buffer on every byte consumed” check. Instead, we establish an upper bound N on the number of input bytes that can be consumed in a single iteration through our decoder main loop, and make sure that our current input buffer *always* has at least N bytes left — by switching to a different temporary input buffer if necessary.

This allows us to reduce the number of end-of-buffer checks we need to execute substantially. More importantly, it greatly increases the applicability of branch-less refill techniques in bit IO and arithmetic coding, without having to keep a separate “safe” decoder around.

The net effect is one of concentrating a little complexity from several places in hot code paths (end-of-buffer checks on every byte consumed) into somewhat increased complexity in a single cold code path (buffer switching). This is often desirable.

The biggest single caveat with this technique is that as a result of the decoder requiring N bytes in the input buffer at all times, the decoder effectively “lags behind” by that many bytes – or, depending on your point of view, it “looks ahead” by N bytes, reading from the input stream sooner than strictly necessary.

This can be a problem when, for example, several compressed streams are concatenated into a single file: the decoder may only get to decoding the “end of stream” symbol for stream A after N bytes from stream B have already been submitted to the decoder. The decoder would then need to “un-read” (in the sense of `ungetc`

) the last few bytes or seek backwards. No matter how you dice it, this is annoying and awkward.

As a result, this technique is not all that useful when this is a required feature (e.g. as part of a DEFLATE decoder obeying the zlib interface).

However, there are ways to sidestep this problem: if the bitstream specifies the compressed size for either the entire stream or individual blocks, or if the framing format ends in N or more trailing “footer” bytes (a checksum or something similar), we can use this approach just fine.

**UPDATE**: As commenter derf_ notes on [Hacker News](https://news.ycombinator.com/item?id=10828404), there’s a nice trick to produce implicit trailing zero bits in a bit reader like the one described above by just setting `bitcount`

to a high value once the last byte’s been read into `bitbuf`

. However, this only works with a decoder exactly like the one shown above. The nice part about switching to an explicit zero-padding buffer is that it works not just with all bit IO implementations I’m aware of, but also with byte-normalized (or larger) arithmetic coders like typical range coders or rANS.

Great article, and one I can relate to, having authored LZ77 class compression algorithms (of course, very advanced derivatives of such), and an open source class for bit I/O. Love your attention to detail when it comes to code efficiency.