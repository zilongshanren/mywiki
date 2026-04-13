---
title: rANS in practice
url: https://fgiesen.wordpress.com/2015/12/21/rans-in-practice/
published: '2015-12-21'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# rANS in practice

This year, we ([RAD](http://www.radgametools.com/)) shipped two new lossless codecs, both using [rANS](https://fgiesen.wordpress.com/2014/02/02/rans-notes/). One of the two is Oodle LZNA (released in May), which Charles has already [written about](http://cbloomrants.blogspot.com/2015/05/05-09-15-oodle-lzna.html). The other is called BitKnit, which first shipped in July as part of [Granny](http://www.radgametools.com/granny.html), and is slated for inclusion into more RAD products.

So, with two production-quality versions written and successfully shipped, this seems like a good time to write up some of the things we’ve learned, especially in terms of implementation concerns. Let’s get cracking! (I’m assuming you’re familiar with ANS. If not, I wrote a [paper](http://arxiv.org/pdf/1402.3392v1) that has a brief explanation, and various older blog posts that give more details on the proofs. I’m also assuming you’re familiar with “conventional” arithmetic coding; if not, you’re not gonna get much out of this.)

### One small note before we start…

I’ll be referring to the ANS family as a class of arithmetic coders, because that’s what they are (and so are “[range coders](http://cbloomrants.blogspot.com/2008/10/10-05-08-5.html)“, by the way). So here’s a small historical note before we get cracking: the “bottom-up” construction of ANS and the LIFO encoding seem quite foreign once you’re used to most “modern” arithmetic coders, but what’s interesting is that some of the earliest arithmetic coders actually looked very similar.

In particular, I’m talking about Rissanen’s 1976 paper “[Generalized Kraft Inequality and Arithmetic Coding](https://www.ic.tu-berlin.de/fileadmin/fg121/Source-Coding_WS12/selected-readings/Rissanen__1976.pdf)” (which coined the term!). Note the encoding and decoding functions C and D on the second page, very reminiscent to the “bottom-up” construction of ANS (with the code being represented by a number that keeps growing), and the decoder returning symbols in the opposite order they were encoded!

Rissanen’s coder (with its rather cumbersome manual truncated floating point arithmetic subject to careful rounding considerations) never saw any widespread application, as far as I can tell. The coders that actually got traction use the now familiar top-down interval subdivision approach, and a different strategy to adapt to fixed-precision operation. But reading Rissanen’s paper from today’s perspective is really interesting; it feels like a very natural precursor to ANS, and much closer in spirit to ANS than to most of the other algorithms that descended from it.

### Why rANS (and not FSE/tANS)?

On my blog especially, I’ve been talking almost exclusively about rANS, and not so much FSE/tANS, the members of the ANS family that have probably been getting the most attention. Why is that?

Briefly, because they’re good at different things. FSE/tANS are (nearly) drop-in replacements for Huffman coding, and have similar strengths and weaknesses. They have very low (and similar) per-symbol decode overhead, but the fast decoders are table-driven, where the table depends on the symbol probabilities. Building Huffman decoding tables is somewhat faster; FSE/tANS offer better compression. Both Huffman and FSE/tANS can in theory support adaptive probabilities, but there’s little point in doing anything but periodic rebuilds; true incremental updates are too slow to be worthwhile. At that point you might as well use a coder which is more suited to incremental adaptation.

Which brings us to rANS. rANS is (again, nearly) a drop-in replacement for multi-symbol Arithmetic coders (such as range coders). It uses fewer registers than most arithmetic coders, has good precision, and the decoder is division-free without introducing any approximations that hurt coding efficiency. Especially with the various tweaks I’ll describe throughout this post, rANS has what are easily the fastest practical multi-symbol alphabet arithmetic decoders I know. rANS coders are also quite simple in implementation, with none of the tricky overflow and underflow concerns that plague most arithmetic coders.

So rANS is a pretty sweet deal if you want a fast arithmetic coder that deals well with relatively fast-changing probabilities. Great! How do we make it work?

### Reverse encoding

As mentioned above, ANS coders are LIFO: whatever order you encode symbols in, the decoder will produce them in the opposite order. All my ANS coders (including the public [ryg_rans](https://github.com/rygorous/ryg_rans)) use the convention that the encoder processes the data in reverse (working from the end towards the beginning), whereas the decoder works forwards (beginning towards end).

With a static model, this is odd, but not especially problematic. With an adaptive model, decoder and model have to process data in the same direction, since the decoder updates the model as it goes along and needs current model probabilities to even know what to read next. So the decoder and the model want to process data in the same direction (forward being the natural choice), and the rANS encoder needs to be processing symbols in the opposite order.

This is where it comes in handy that rANS has an interface very much like a regular arithmetic coder. For example, in my [sample implementation](https://github.com/rygorous/ryg_rans/blob/master/rans_byte.h#L83), the symbol is described by two values, `start`

and `freq`

, which are equivalent to the symbol interval lower bound and size in a conventional arithmetic coder, respectively.

Most arithmetic coders perform the encoding operation right there and then. In rANS, we need to do the actual encoding backwards, which means we need to buffer the symbols first: (the first description I’ve seen of this idea was in Matt Mahoney’s [fpaqa](http://mattmahoney.net/dc/#fpaq0))

// Say our probabilities use 16-bit fixed point. struct RansSymbol { uint16_t start; // start of symbol interval uint16_t range; // size of symbol interval }; class BufferedRansEncoder { std::vector<RansSymbol> syms; // or similar public: void encode(uint16_t start, uint16_t range) { assert(range >= 1); assert(start + range <= 0x10000); // no wrap-around RansSymbol sym = { start, range }; syms.push_back(sym); } void flush_to(RansEncoder &coder); };

With this, we can use rANS exactly like we would any other arithmetic coder. However, it will not be generating the bitstream incrementally during calls to `encode`

; instead, it simply buffers up operations to be performed later. Once we’re done we can then pop off the symbols one by one, in reverse order, and generate the output bitstream. Easy:

void BufferedRansEncoder::flush_to(RansEncoder &coder) { // Replays the buffered symbols in reverse order to // the actual encoder. while (!syms.empty()) { RansSymbol sym = syms.back(); coder.encode(sym.start, sym.range); syms.pop_back(); } }

Once you have this small piece of scaffolding, you really can use rANS as a drop-in replacement for a conventional arithmetic coder. There’s two problems with this, though: if you use this to encode an entire large file, your symbol buffer can get pretty huge, and you won’t get a single bit of output until you’ve processed the entire input stream.

The solution is simple (and can also be found in the aforementioned `fpaqa`

): instead of accumulating all symbols emitted over the entire input stream and doing one big flush at the end, you just process the input data in chunks and flush the coder periodically, resetting the rANS state every time. That reduces compression slightly but means the encoder memory usage remains bounded, which is an important practical consideration. It also guarantees that output is not delayed until the end of stream; finally, lots of compressors are already chunk-based anyway. (For the opportunity to send incompressible data uncompressed rather than wasting time on the decoder end, among other things.)

### Basic interleaving

One thing that rANS makes easy is interleaving the output from several encoders into a single bitstream without needing any extra signaling. I’m not going into detail why that works here; I wrote a [paper](http://arxiv.org/pdf/1402.3392v1) on the subject if you’re interested in details. But the upshot is that you can use multiple rANS encoders and decoders simultaneously, writing to the same output bitstream, rather than having a single one.

Why do we care? Because this is what decoding a single symbol via rANS looks like (adapted from my public `ryg_rans`

code):

static const uint32_t kProbBits = 16; static const uint32_t kProbMask = (1 << kScaleBits) - 1; class RansDecoder { uint32_t state; // current rANS state // (IO stuff omitted) uint32_t renormalize_state(uint32_t x) { // Byte-wise for simplicity; can use other ways. while (x < RANS_L) x = (x << 8) | read_byte(); return x; } public: uint32_t decode_symbol() { uint32_t x = state; // Current state value uint32_t xm = x & kProbMask; // low bits determine symbol Symbol sym = lookup_symbol(xm); // (various ways to do this) // rANS state advance x = sym.range * (x >> kProbBits) + xm - sym.start; x = renormalize_state(x); // Save updated state and return symbol state = x; return sym.id; } };

Note how literally every single line depends on the results of the previous one. This translates to machine code that has a single, very long, dependency chain with relatively low potential for instruction-level parallelism (ILP). This is fairly typical for *all* entropy coder inner loops, by the way, not just rANS. And because superscalar processors depend on ILP to deliver high performance, this is bad news; we’re not making good use of the machine.

Hence interleaving. The idea is that we have two `RansDecoder`

instances, each with their own `state`

, but implicitly sharing the same bitstream read pointer (referenced by `read_byte`

). Now, when we have code like this:

RansDecoder dec0, dec1; // ... uint32_t sym0 = dec0.decode_symbol(): uint32_t sym1 = dec1.decode_symbol();

the processor’s out-of-order execution logic can overlap execution of both decodes, effectively running them *at the same time*. The renormalize step for `dec0`

needs to happen before the renormalize of `dec1`

, but other than that, there’s no dependencies between the two. For what it’s worth, this does not actually require out-of-order execution; a compiler for an in-order architecture can also work with this, provided it has enough dataflow information to know that `dec0`

calling `read_byte()`

does not influence anything that dec1 does before its renormalize step. So what interleaving does is convert a very serial task into one that’s much more amenable to superscalar execution.

What it boils down to is this: a regular rANS decoder is a fast, precise, divide-less arithmetic decoder (which is nice to begin with). Interleave two streams using what is otherwise the *exact same code*, and you get a pretty good boost in performance; (very roughly) around 1.4× faster, on both the decoder and encoder. But this is by now an old hat; this was all in the initial release of [ryg_rans](https://github.com/rygorous/ryg_rans/).

Some of the early experiments leading up to what later became BitKnit uses this directly, pretty much the same as in the `ryg_rans`

example code, but it turns out it was a bit of a pain in the neck to work with: because the two streams need to interleave properly, the `BufferedRansEncoder`

needs to keep track of which symbol goes to which stream, and both the encoder and decoder code needs to (somewhat arbitrarily) assign symbols to either stream 0 or stream 1. You’d prefer the streams to keep alternating along any given control-flow path, but that’s not always possible, since sometimes you have conditionals where there’s an even number of symbols send on one path, and an odd number sent on the other! So having two explicit streams: not so great. But we found a better way.

### Implicit interleaving to the rescue

What we actually ended up doing was interleaving with a twist – literally. We give the underlying rANS encoders (and decoders) two separate state values, and simply swap the two stream states after every encoding and decoding operation (that’s where the “BitKnit” name comes from – it keeps two active states on the same “needle” and alternates between them). The modifications from the decoder shown above are pretty small:

class RansDecoder { uint32_t state1; // state for "thread 1" uint32_t state2; // state for "thread 2" // ... public: uint32_t decode_symbol() { uint32_t x = state1; // Pick up thread 1 // ---- BEGIN of code that's identical to the above uint32_t xm = x & kProbMask; // low bits determine symbol Symbol sym = lookup_symbol(xm); // (various ways to do this) // rANS state advance x = sym.range * (x >> kProbBits) + xm - sym.start; x = renormalize_state(x); // ---- END of code that's identical to the above // Save updated state, switch the threads, and return symbol state1 = state2; // state2 becomes new state1 state2 = x; // updated state goes to state2 return sym.id; } };

The changes to the encoder are analogous and just as simple. It turns out that this really is enough to get all the performance benefits of 2× interleaving, with none of the extra interface complexity. It just looks like a regular arithmetic decoder (or encoder). And assuming you write your implementation carefully, compilers are able to eliminate the one extra register-register move instruction we get from swapping the threads on most paths. It’s all win, basically.

### Bypass coding

Borrowing a term from CABAC here; the “bypass coding mode” refers to a mode in the arithmetic coder that just sends raw bits, which you use for data that’s known a priori to be essentially random/incompressible, or at least not worth modeling further. With conventional arithmetic coders, you really need special support for this, since interleaving an arithmetic code stream with a raw bitstream is not trivial.

With rANS, that’s much less of a problem: you can just use a separate bitbuffer and mix it into the target bitstream with no trouble. However, you may not *want* to: rANS has essentially all of the machinery you need to act as a bit buffer. Can you do it?

Well, first of, you can just use the arithmetic coder with a uniform distribution to send a set number of bits (up to the probability resolution). This works with any arithmetic coder, rANS included, and is fairly trivial:

// write value "bits" using "numbits" coder.encode(bits << (kProbBits - numbits), 1 << (kProbBits - numbits));

and the equivalent on the decoder side. However, this is not particularly fast. Fortunately, it’s actually really easy to throw raw bit IO into a rANS coder: we just add the bits at the bottom of our `state`

variable (or remove them from there in the decoder). That’s it! The only thing we need to do is work out the renormalization condition in the encoder. Using the conventions from the bytewise `ryg_rans`

, an example implementation of the encoder is:

static inline void RansEncPutBits(RansState* r, uint8_t** pptr, uint32_t val, uint32_t nbits) { assert(nbits <= 16); assert(val < (1u << nbits)); // nbits <= 16! RansState x = RansEncRenorm(*r, pptr, 1 << (16 - nbits), 16); // x = C(s,x) *r = (x << nbits) | val; }

and the corresponding `getbits`

in our ongoing example decoder looks like this:

class RansDecoder { // ... uint32_t get_bits(uint32_t nbits) { uint32_t x = state1; // Pick up thread 1 // Get value from low bits then shift them out and // renormalize uint32_t val = x & ((1u << nbits) - 1); x = renormalize_state(x >> nbits); // Save updated state, switch the threads, and return value state1 = state2; // state2 becomes new state1 state2 = x; // updated state goes to state2 return val; } };

note that except for the funky state swap (which we carry through for consistency), this is essentially just a regular bit IO implementation. So our dual-state rANS admits a “bypass mode” that is quite cheap; usually cheaper than having a separate bit buffer would be (which would occupy yet another CPU register in the decoder), at least in my tests.

Note that if you combine this with the buffering encoder described above, you need a way to flag whether you want to emit a regular symbol or a burst of raw bits, so our `RansSymbol`

structure (and the code doing the actual encoding) gets slightly more complicated since we now have two separate types of “opcodes”.

The implementation above has a limit of 16 bits you can write in a single call to `RansEncPutBits`

. How many bits you can send at once depends on the details of your renormalization logic, and how many bits of rANS state you keep. If you need to send more than 16, you need to split it into multiple operations.

### Tying the knot

I got one more: a rANS encoder needs to write its final state to the bitstream, so that the decoder knows where to start. You can just send this state raw; it works just fine. That’s what the `ryg_rans`

example code does.

However, rANS states are not equally likely. In fact, state x occurs with a probability [proportional to 1/x](http://cbloomrants.blogspot.com/2014/02/02-10-14-understanding-ans-9.html). That means that an ideal code should spend approximately bits to encode a final state of x. Charles has already

[written about this](http://cbloomrants.blogspot.com/2015/05/05-11-15-ans-minimal-flush.html). Fortunately, the ideal coder for this distribution is easy: we simply send the index of the highest set bit in the state (using a uniform code), followed by the remaining bits.

One options is to do this using regular bit I/O. But now you still need a separate bit IO implementation!

Fortunately, we just covered how do send raw bits through a rANS encoder. So one thing we can do is encode the final state value of stream 2 using the “stream 1” rANS as the output bit buffer, using the putbits functionality just described (albeit without the thread-switching this time). Then we send the final state of the “stream 1” rANS raw (or using a byte-aligned encoding).

This approach is interesting because it takes a pair of two rANS encoder threads and “ties them together” – making a knot, so to speak. In the decoder, undoing the knot is serial (and uses a single rANS decoder), but immediately after initialization, you have a working dual-stream coder. This saves a few bytes compared to the sloppier flushing and is just plain cute.

This technique really comes into its own for the wide-interleave SIMD rANS coders described in my paper, because it can be done in parallel on lots of simultaneous rANS coders in a reduction tree: group lanes into pairs, have each odd-indexed lane flush into its even-indexed neighbor. Now look at groups of 4 lanes; two have already been flushed, and we can flush the rightmost “live” lane into the leftmost lane coder. And so forth. This allows flushing a N× interleaved SIMD rANS coder in coding operations, and still has some parallelism while doing so. This is not very exciting for a 2× or 4× interleaved coder, but for GPU applications N is typically on the order of 32 or 64, and at that level it’s definitely interesting.


### Conclusion and final notes

Using the techniques described in this post, you can write rANS encoders and decoders that have about the same amount of code as a conventional arithmetic coder with comparable feature set, have a similar interface (aside from the requirement to flush the encoder regularly), are significantly faster to decode (due to the combination of the already-fast rANS decoder with implicit interleaving), and have very cheap “bypass coding” modes.

This is a really sweet package, and we’re quite happy with it. Anyone interested in (de)compression using adaptive models should at least take a look. (For static models, FSE/tANS are stronger contenders.)

What example code there is in this article uses byte-wise renormalization. That’s probably the simplest way, but not the fastest. Oodle LZNA uses a 63-bit rANS state with 32-bits-at-a-time renormalization, just like [rans64.h in ryg_rans](https://github.com/rygorous/ryg_rans/blob/master/rans64.h). That’s a good choice if you’re primarily targeting 64-bit platforms and can afford a 64-bit divide in the encoder (which is quite a bit more expensive than a 32-bit divide on common CPUs). BitKnit uses a 32-bit rANS state with 16-bits-at-a-time renormalization, similar to the coder in [ryg_rans rans_word_sse41.h](https://github.com/rygorous/ryg_rans/blob/master/rans_word_sse41.h). This is friendlier to 32-bit targets and admits a branch-free renormalize option, but also means the coder has somewhat lower precision. Using a probability range of 16 bits would not be wise in this case; BitKnit uses 14 bits.

Great piece of blog, as usual Fabian.

I guess I only have one question, and it’s only indirectly related to rANS.

One of the key advantages of rANS mentioned in your article is the ability to work with adaptive statistics. Since you mention this advantage compared to table-based implementations, I suspect you mean “per symbol adaptive”, although I could be wrong so please correct me if you meant “per block adaptive” instead,

In https://fgiesen.wordpress.com/2015/05/26/models-for-adaptive-arithmetic-coding and https://fgiesen.wordpress.com/2015/02/20/mixing-discrete-probability-distributions, you describe a clever method to update a multi-symbols alphabet by working directly on cumulative probabilities.

I suspect it means 2 things :

– Probability of symbols is not stored directly but calculated by a trivial subtraction operation. Should be very fast, but still, one more operation in a critical loop.

– Updating probabilities still requires as many updates as there are symbols in the alphabet, although your proposed construction allows some parallelization.

Considering that the rANS implementation described in this article should run very fast, I’m wondering if the cost of updating the model is a significant contributor to total encoding / decoding time.

LZNA targets the same level of compression as LZMA and does model updates after every single symbol. This is by no means cheap but neither is the binary tree of single-bit models that LZMA uses. And as noted in “Models for adaptive arithmetic coding”, the model is suitable for SIMD implementation. This is still

manymore operations per symbol than tANS or anything similar, but remember that a nibble-based model is competing with a 4-level bit tree, which has on the order of 2 expected branch misprediction (about 30 cycles!). You can do a lot in that kind of time if you don’t spend it with the core stalled. Interleaving also helps in that the model processing for the second half can start issuing well before the first half is finished.BitKnit uses deferred-summation type models that rebuild every few hundred symbols, with relatively high probability resolution (14 bits), and keeps several different contexts. That’s too frequent updates for the (relatively expensive) FSE/tANS table build, and with 14 bits of resolution, a full rANS state->symbol table is not practical either (also too expensive in terms of build time, and besides I need L1 cache space for other things too!). So the design problem there is getting decent symbol lookup performance with low memory usage and no expensive data structure updates.

Thanks for this very clear answer.

Hello Fabian

Thanks for a great blog, I learned a lot from it (and I guess still have much more to learn). There is one question that puzzles me, thought. I wonder how should one apply rANS to quantised DCT data. About the only reference I could find about this was [a=”http://cbloomrants.blogspot.com/2014/02/02-18-14-ansfast-implementation-notes.html?showComment=1393360801479#c8824551396044596309″]your comment on Charles Bloom blog[/a]. Could you please explain a bit what you meant by “Use rANS/tANS to code log(|x|) as one symbol then send sign+suffix bits raw”. Using exp-Golomb codes for AC coefficients and compressing magnitude only, and sending sign/suffix in “bypass mode”?

I also wonder how would application of rANS (or other entropy codecs) change if one were to compress DCT coefficients not on per-block basis (such as ordinary JPEG, MPEG or whatever compression standard does), but grouping similar “subband” coefficients from bigger area, or even whole image (for example whole zig/zags from standard zigzag scanning order). Of course decoding costs would rise (no longer single-pass), but perhaps worth the effort?

Never mind the DCT coefficients coding, figured it out :-)

Hi, is there around a more readable python implementation? I’m new to compression algorithms and I’m try to learn them for designing dedicated hardware, and starting with a full-of-pointers C code is not exactly the simplest thing around…

thanks!

Nope!

ok I’m trying to do it by myself… I’m trying to use it to encode short strings of bits (144), any suggestions about parameters (like n or the target value for frequencies) ?

rANS is the wrong algorithm for that kind of application.

We’ve been experimenting with implementing vectorized rANS coding with a large number of threads, and using BitKnit to code the ANS head at the end of encoding as you described in this article. We found that we were getting a slight overhead in compression rate (around 8% in the worst case), which scaled linearly with the number of threads. We just discovered the cause, and anyone implementing a similar system might find this interesting…

There is a slight mistake in the post:

… state x occurs with a probability proportional to 1/x. <– This is correct

… Fortunately, the ideal coder for this distribution is easy: we simply send the index of the highest set bit in the state (using a uniform code), followed by the remaining bits. <– This is slightly wrong

The reason that that coding scheme isn't perfect is that conditioned on the position of the highest set bit, the remaining bits aren't exactly uniformly distributed. In particular, if x' is x with the leading 1 removed, and L denotes the index of the highest set bit (which is random), then

p(x' | L) \propto 1 / x = 1 / (2 ^ L + x')

Clearly this distribution places more mass on smaller x', and therefore it isn't uniform. You can closely approximate the cdf by

F(x' | L) = (lg(2 ^ L + x') – L) / (lg(2 ^ (L + 1)) – L)

We tried coding the first few remaining bits according to the above distribution (instead of uniform) and the 8% overhead is reduced to below 0.1%. Will be releasing code soon on https://github.com/j-towns/.

Forgot to say thanks for the blog post and the fantastic rANS implementation, super clear and useful!