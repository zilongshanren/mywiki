---
title: Reading bits in far too many ways (part 2)
url: https://fgiesen.wordpress.com/2018/02/20/reading-bits-in-far-too-many-ways-part-2/
published: '2018-02-20'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Reading bits in far too many ways (part 2)

(Continued from [part 1](https://fgiesen.wordpress.com/2018/02/19/reading-bits-in-far-too-many-ways-part-1/).)

Last time, I established the basic problem and went through various ways of doing shifting and masking, and the surprising difficulties inherent therein. The “bit extract” style I picked is based on a stateless primitive, which made it convenient to start with because there’s no loop invariants involved.

This time, we’re going to switch to the stateful style employed by most bit readers you’re likely to encounter (because it ends up cheaper). We’re also going to switch from a monolithic `getbits`

function to something a bit more fine-grained. But let’s start at the beginning.

### Variant 1: reading the input one byte at a time

Our “extract”-style reader assumed the entire bitstream was available in memory ahead of time. This is not always possible or desirable; so let’s investigate the other extreme, a bit reader that requests additional bytes one at a time, and only when they’re needed.

In general, our stateful variants will dribble in input a few bytes at a time, and have partially processed bytes lying around. We need to store that data in a variable that I will call the “bit buffer”:

// Again, this is understood to be per-bit-reader state or local // variables, not globals. uint64_t bitbuf = 0; // value of bits in buffer int bitcount = 0; // number of bits in buffer

While processing input, we will always be seesawing between putting more bits into that buffer when we’re running low, and then consuming bits from that buffer while we can.

Without further ado, let’s do our first stateful `getbits`

implementation, reading one byte at a time, and starting with MSB-first this time:

// Invariant: there are "bitcount" bits in "bitbuf", stored from the // MSB downwards; the remaining bits in "bitbuf" are 0. uint64_t getbits1_msb(int count) { assert(count >= 1 && count <= 57); // Keep reading extra bytes until we have enough bits buffered // Big endian; our current bits are at the top of the word, // new bits get added at the bottom. while (bitcount < count) { bitbuf |= (uint64_t)getbyte() << (56 - bitcount); bitcount += 8; } // We now have enough bits present; the most significant // "count" bits in "bitbuf" are our result. uint64_t result = bitbuf >> (64 - count); // Now remove these bits from the buffer bitbuf <<= count; bitcount -= count; return result; }

As before, we can get rid of the `count`

≥1 requirement by changing the way we grab the result bits, as explained in the last part. This is the last time I’ll mention this; just keep in mind that whenever I show any algorithm variant here, the variations from last time automatically apply.

The idea here is quite simple: first, we check whether there’s enough bits in our buffer to satisfy the request immediately. If not, we dribble in extra bytes one at a time until we have enough. `getbyte()`

here is understood to ideally use some [buffered IO mechanism](https://fgiesen.wordpress.com/2011/11/21/buffer-centric-io/) that just boils down to dereferencing and incrementing a pointer on the hot path; it should *not* be a function call or anything expensive if you can avoid it. Because we insert 8 bits at a time, the maximum number of bits we can read in a single call is 57 bits; that’s the largest number of bits we can refill the buffer to without risking anything dropping out.

After that, we grab the top `count`

bits from our buffer, then shift them out. The invariant we maintain here is that the first unconsumed bit is kept at the MSB of the buffer.

The other thing I want you to notice is that this process breaks down neatly into three separate smaller operations, which I’m going to call “refill”, “peek” and “consume”, respectively. The “refill” phase ensures that a certain given minimum number of bits is present in the buffer; “peek” returns the next few bits in the buffer, without discarding them; and “consume” removes bits without looking at them. These all turn out to be individually useful operations; to show how things shake out, here’s the equivalent LSB-first algorithm, factored into smaller parts:

// Invariant: there are "bitcount" bits in "bitbuf", stored from the // LSB upwards; the remaining bits in "bitbuf" are 0. void refill1_lsb(int count) { assert(count >= 0 && count <= 57); // New bytes get inserted at the top end. while (bitcount < count) { bitbuf |= (uint64_t)getbyte() << bitcount; bitcount += 8; } } uint64_t peekbits1_lsb(int count) { assert(bit_count >= count); return bitbuf & ((1ull << count) - 1); } void consume1_lsb(int count) { assert(bit_count >= count); bitbuf >>= count; bitcount -= count; } uint64_t getbits1_lsb(int count) { refill1_lsb(count); uint64_t result = peekbits1_lsb(count); consume1_lsb(count); return result; }

Writing `getbits`

as the composition of these three smaller primitives is not always optimal. For example, if you use the rotate method for MSB-first bit buffers, you really want to have only rotate shared by the `peekbits`

and `consume`

phases; an optimal implementation shares that work between the two. However, breaking it down into these individual steps is still a useful thing to do, because once you conceptualize these three phases as distinct things, you can start putting them together differently.

### Lookahead

The most important such transform is amortizing refills over multiple decode operations. Let’s start with a simple toy example: say we want to read our three example bit fields from the last part:

a = getbits(4); b = getbits(3); c = getbits(5);

With `getbits`

implemented as above, this will do the refill check (and potentially some actual refilling) up to 3 times. But this is silly; we know in advance that we’re going to be reading 4+3+5=12 bits in one go, so we might as well grab them all at once:

refill(4+3+5); a = getbits_no_refill(4); b = getbits_no_refill(3); c = getbits_no_refill(5);

where `getbits_no_refill`

is yet another getbits variant that does `peekbits`

and `consume`

, but, as the name suggests, no refilling. And once you get rid of the refill loop between the individual `getbits`

invocations, you’re just left with straight-line integer code, which compilers are good at optimizing further. That said, the all-fixed-length case is a bit of a cheap shot; it gets far more interesting when we’re not sure exactly how many bits we’re actually going to consume, like in this example:

temp = getbits(5); if (temp < 28) result = temp; else result = 28 + (temp - 28)*16 + getbits(4);

This is a simple variable-length code where values from 0 through 27 are sent in 5 bits, and values from 28 through 91 are sent in 9 bits. The point being, in this case, we don’t know in advance how many bits we’re eventually going to consume. We do know that it’s going to be no more than 9 bits, though, so we can still make sure we only refill once:

refill(9); temp = getbits_no_refill(5); if (temp < 28) result = temp; else result = 28 + (temp - 28)*16 + getbits_no_refill(4);

In fact, if you want to, you can go wild and split operations even more, so that both execution paths only `consume`

bits once. For example, assuming a MSB-first bit buffer, we could write this small decoder as follows:

refill(9); temp = peekbits(5); if (temp < 28) { result = temp; consume(5); } else { // The "upper" and "lower" code are back-to-back, // and combine exactly the way we want! Synergy! result = getbits_no_refill(9) - 28*16 + 28; }

This kind of micro-tweaking is *really* not recommended outside very hot loops, but as I mentioned in the previous part, some of these decoder loops are quite hot indeed, and in that case saving a few instructions here and a few instructions there adds up. One particularly important technique for decoding variable-length codes (e.g. Huffman codes) is to peek ahead by some fixed number of bits and then do a table lookup based on the result. The table entry then lists what the decoded symbol should be, and how many bits to consume (i.e. how many of the bits we just peeked at really belonged to the symbol). This is *significantly* faster than reading the code a bit or two at a time and consulting a Huffman tree at every step (the method sadly taught in many textbooks and other introductory texts.)

There’s a problem, though. The technique of peeking ahead a bit (no pun intended) and then later deciding how many bits you actually want to consume is quite powerful, but we’ve just changed the rules: the `getbits`

implementation above is careful to only read extra bytes when it’s strictly necessary. But our modified variable-length code reader example above always refills so the buffer contains at least 9 bits, even when we’re only going to consume 5 bits in the end. Depending on where that refill happens, it might even cause us to read past the end of the actual data stream.

In short, we’ve introduced *lookahead*. The modified code reader starts grabbing extra input bytes before it’s sure whether it needs them. This has many advantages, but the trade-off is that it may cause us to read past the logical end of a bit stream; it certainly implies that we have to make sure this case is handled correctly. It certainly should never crash or read out of bounds; but beyond that, it implies certain thing about the way input buffering or the framing layer have to work.

Namely, if we’re going to do any lookahead, we need to figure out a way to handle this. The primary options are as follows:

- We can punt and make it someone else’s problem by just requiring that everyone hand us valid data with some extra padding bytes after the end. This makes our lives easier but is an inconvenience for everyone else.
- We can arrange things so the outer framing layer that feeds bytes to our
`getbits`

routine knows when the real data stream is over (either due to some escape mechanism or because the size is sent explicitly); then we can either stop doing any lookahead and switch to a more careful decoder when we’re getting close to the end, or pad the stream with some dummy value after its end (zeroes being the most popular choice). - We can make sure that whatever bytes we might grab during lookahead while decoding a valid stream are still part of our overall byte stream that’s being processed by our code. For example, if you use a 64-bit bit buffer, we can finagle our way around the problem by requiring that some 8-byte footer (say a checksum or something) be present right after a valid bit stream. So while our bit buffer might overshoot, it’s still data that’s ultimately going to be consumed by the decoder, which simplifies the logistics considerably.
- Barring that, whatever I/O buffering layer we’re using needs to allow us to return some extra bytes we didn’t actually consume into the buffer. Namely, whatever lookahead bytes we have left in our bit buffer after we’re done decoding need to be returned to the buffer for whoever is going to read it next. This is essentially what the C standard library function
does, except you’re not allowed to call`ungetc`

`ungetc`

more than once, and we might need to. So going along this route essentially dooms you to taking charge of IO buffer management.

I won’t sugarcoat it, all of these options are a pain in the neck, some more so than others: hand-waving it away by putting something else at the end is easiest, handling it in some outer framing layer isn’t too bad, and taking over all IO buffering so you can un-read multiple bytes is positively hideous, but you don’t have great options when you don’t control your framing. In the past, I’ve written [posts](https://fgiesen.wordpress.com/2011/11/21/buffer-centric-io/) about [handy techniques](https://fgiesen.wordpress.com/2016/01/02/end-of-buffer-checks-in-decompressors/) that might help you in this context; and in some implementations you can work around it, for example by setting `bitcount`

to a huge value just after inserting the final byte from the stream. But in general, if you want lookahead, you’re going to have to put some amount of work into it. That said, the winnings tend to be fairly good, so it’s not all for nothing.

### Variant 2: when you *really* want to read 64 bits at once

The methods I’ve discussed so far both have some “slop” from working in byte granularity. The extract-style bit reader started with a full 64-bit read but then had to shift by up to 7 positions to discard the part of the current byte that’s already consumed, and the `getbits1`

above inserts one byte at a time into the bit buffer; if there’s 57 bits already in the buffer, there’s no space for another byte (because that would make 65 bits, more than the width of our buffer), so that’s the maximum width the `getbits1`

method supports. Now 57 bits is a useful amount; but if you’re doing this on a 32-bit platform, the equivalent magic number is 25 bits (32-7), and that’s definitely on the low side, enough so to be inconvenient sometimes.

Luckily, if you want the full width, there’s a way to do it (like the rotate-and-mask technique for MSB-first bit buffers, I learned this at RAD). At this point, I think you get the correspondence between the MSB-first and LSB-first methods, so I’m only going to show one per variant. Let’s do LSB-first for this one:

// Invariant: "bitbuf" contains "bitcount" bits, starting from the // LSB up; 1 <= bitcount <= 64 uint64_t bitbuf = 0; // value of bits in buffer int bitcount = 0; // number of bits in buffer uint64_t lookahead = 0; // next 64 bits bool have_lookahead = false; // Must do this to prime the pump! void initialize() { bitbuf = get_uint64LE(); bitcount = 64; have_lookahead = false; } void ensure_lookahead() { // grabs the lookahead word, if we don't have // it already. if (!have_lookahead) { lookahead = get_uint64LE(); have_lookahead = true; } } uint64_t peekbits2_lsb(int count) { assert(bitcount >= 1); assert(count >= 0 && count <= 64); if (count <= bitcount) { // enough bits in buf return bitbuf & width_to_mask_table[count]; } else { ensure_lookahead(); // combine current bitbuf with lookahead // (lookahead bits go above end of current buf) uint64_t next_bits = bitbuf; next_bits |= lookahead << bitcount; return next_bits & width_to_mask_table[count]; } } void consume2_lsb(int count) { assert(bitcount >= 1); assert(count >= 0 && count <= 64); if (count < bitcount) { // still in current buf // just shift the bits out bitbuf >>= count; bitcount -= count; } else { // all of current buf consumed ensure_lookahead(); // we advanced fully into the lookahead word int lookahead_consumed = count - bitcount; bitbuf = lookahead >> lookahead_consumed; bitcount = 64 - lookahead_consumed; have_lookahead = false; } assert(bitcount >= 1); } uint64_t getbits2_lsb(int count) { uint64_t result = peekbits2_lsb(count); consume2_lsb(count); return result; }

This one is a bit more complicated than the ones we’ve seen before, and needs an explicit initialization step to make the invariants work out *just right*. It also involves several extra branches compared to the variants we’ve seen before, which makes it less than ideal for deeply pipelined machines, which includes desktop PCs, and note that I’m using the `width_to_mask_table`

again, and not just for show: none of the arithmetic expressions we saw last time to compute the mask for a given width work for the full 0-64 range of allowed `width`

s on any common 64-bit architecture that’s not POWER, and even that only if we ignore them invoking undefined behavior, which we *really* shouldn’t.

The underlying idea is fairly simple: instead of just one bit buffer, we keep track of two values. We have however many bits are left of the last 64-bit value we read, and when that’s not enough for a `peekbits`

, we grab the next 64-bit value from the input stream (via some externally-implemented `get_uint64LE()`

) to give us the bits we’re missing. Likewise, `consume`

checks whether there will still be any bits left in the current input buffer after consuming `width`

bits. If not, we switch over to the bits from the lookahead value (shifting out however many of them we consumed) and clear the `have_lookahead`

flag to indicate that what used to be our lookahead value is now just the contents of our bit buffer.

There are some contortions in this code to ensure we don’t do out-of-range (undefined-behavior-inducing) shifts. For example, note how `peekbits`

tests whether `count <= bitcount`

to detect the bits-present-in-buffer case, whereas `consume`

uses `count < bitcount`

. This is not an accident: in `peekbits`

, the `next_bits`

calculation involves a right-shift by `bitcount`

. Since it only happens in the path where `bitcount`

< `count`

≤ 64, that means that `bitcount < 64`

, and we’re safe. In `consume`

, the situation is reversed: we shift by `lookahead_consumed = count - bitcount`

. The condition around the block guarantees that `lookahead_consumed`

≥ 0; in the other direction, because `count`

is at most 64 and `bitcount`

is at least 1, we have `lookahead_consumed`

≤ 64 – 1 = 63. That said, to paraphrase Knuth: beware of bugs in the above code; I’ve only proved it correct, not tried it.

This technique has another thing going for it besides supporting bigger bit field widths: note how it always reads full 64-bit uints at a time. Variant 1 above only reads bytes at a time, but requires a refill loop; the various branchless variants we’ll see later implicitly rely on the target CPU supporting fast unaligned reads. This version alone has the distinction of doing reads of a single size and with consistent alignment, which makes it more attractive on targets that don’t support fast unaligned reads, such as many old-school RISC CPUs.

Finally, as usual, there’s several more variations here that I’m not showing. For example, if you happen to have the data you’re decoding fully in memory, there’s no reason to bother with the boolean `have_lookahead`

flag; just keep a pointer to the current lookahead word, and bump that pointer up whenever the current lookahead is consumed.

### Variant 3: bit extraction redux

The original bit extraction-based bit reader from the previous part was a bit on the expensive side. But as long as we’re OK with the requirement that the entire input stream be in memory at once, we can wrangle it into the refill/peek/consume pattern to get something useful. It still gives us a bit reader that looks ahead (and hence has the resulting difficulties), but such is life. For this one, let’s do MSB again:

const uint8_t *bitptr; // Pointer to current byte uint64_t bitbuf = 0; // last 64 bits we read int bitpos = 0; // how many of those bits we've consumed void refill3_msb() { assert(bitpos <= 64); // Advance the pointer by however many full bytes we consumed bitptr += bitpos >> 3; // Refill bitbuf = read64BE(bitptr); // Number of bits in the current byte we've already consumed // (we took care of the full bytes; these are the leftover // bits that didn't make a full byte.) bitpos &= 7; } uint64_t peekbits3_msb(int count) { assert(bitpos + count <= 64); assert(count >= 1 && count <= 64 - 7); // Shift out the bits we've already consumed uint64_t remaining = bitbuf << bitpos; // Return the top "count" bits return remaining >> (64 - count); } void consume3_msb(int count) { bitpos += count; }

This time, I’ve also left out the `getbits`

built from refill / peek / consume calls, because that’s yet another pattern that should be pretty clear by now.

It’s a pretty sweet variant. Once we break the bit extraction logic into separate “refill” and “peek”/”consume” pieces, it becomes clear how all of the individual pieces are fairly small and clean. It’s also completely branchless! It does expect unaligned 64-bit big-endian reads to exist and be reasonably cheap (not a problem on mainstream x86s or ARMs), and of course a realistic implementation needs to include handling of the end-of-buffer cases; see the discussion in the “lookahead” section.

### Variant 4: a different kind of lookahead

And now that we’re here, let’s do another branchless lookahead variant. This exact variant is, to the best of my knowledge, another RAD special – discovered by my colleague Charles Bloom and me while working on Kraken (**UPDATE:** as Yann points out in the comments, this basic idea was apparently used in Eric Biggers’ “Xpack” long before Kraken was launched; I wasn’t aware of this and I don’t think Charles was either, but that means we’re definitely not the first ones to come up with the idea. Our variant has an interesting wrinkle though – details [in my reply](https://fgiesen.wordpress.com/2018/02/20/reading-bits-in-far-too-many-ways-part-2/#comment-10923)). Now all branchless (well, branchless if you ignore end-of-buffer checking in the refill etc.) bit readers look very much alike, but this particular variant has a few interesting properties (some of which I’ll only discuss later because we’re lacking a bit of necessary background right now), and that I haven’t seen anywhere else in this combination; if someone else did it first, feel free to inform me in the comments, and I’ll add the proper attribution! Here goes; back to LSB-first again, because I’m committed to hammering home just how similar and interchangeable LSB-first/MSB-first are at this level, holy wars notwithstanding.

const uint8_t *bitptr; // Pointer to next byte to insert into buf uint64_t bitbuf = 0; // value of bits in buffer int bitcount = 0; // number of bits in buffer void refill4_lsb() { // Grab the next few bytes and insert them right above // the current top. bitbuf |= read64LE(bitptr) << bitcount; // Advance the read pointer for next iteration bitptr += (63 - bitcount) >> 3; // Update the available bit count bitcount |= 56; // now bitcount is in [56,63] } uint64_t peekbits4_lsb(int count) { assert(count >= 0 && count <= 56); assert(count <= bitcount); return bitbuf & ((1ull << count) - 1); } void consume4_lsb(int count) { assert(count <= bitcount); bitbuf >>= count; bitcount -= count; }

The peek and consume phases are nothing we haven’t seen before, although this time the maximum permissible bit width seems to have shrunk by one more bit down to 56 bits for some reason.

That reason is in the refill phase, which works slightly differently from the ones we’ve seen so far. Reading 64 little-endian bits and shifting them up to align with the top of our current bit buffer should be straightforward at this point. But the `bitptr`

/ `bitcount`

manipulation needs some explanation.

It’s actually easier to start with the `bitcount`

part. The variants we’ve seen so far generally have between 57 and 64 bits in the buffer after refill. This version instead targets having between 56 and 63 bits in the buffer (which is also why the limit on count went down by one). But why? Well, inserting some integer number of bytes means `bitcount`

is going to be incremented by some multiple of 8 during the refill; that means that `bitcount & 7`

(the low 3 bits) won’t change. And if we refill to a target of [56,63] bits in the buffer, we can compute the updated bit count with a single binary OR operation.

Which brings me to the question of how many bytes we should advance the pointer by. Well, let’s just look at the values of the original `bitcount`

:

- If 56 ≤
`bitcount`

≤ 63, we were already in our target range and don’t want to advance by another byte. - If 48 ≤
`bitcount`

≤ 55, we’re adding exactly 1 byte (and so want to advance`bit_ptr`

by that much). - If 40 ≤
`bitcount`

≤ 47, we’re adding exactly 2 bytes.

and so forth. This works out to the `(63 - bitcount) >> 3`

bytes we’re adding to `bitptr`

.

Now, the bits in `bitbuf`

above `bitcount`

can end up getting ORed over multiple times. However, when that happens, we OR over the same value every time, so it doesn’t change the result. Therefore, once they later travel downwards (from the right-shift in the consume function), they’re fine; no need to worry about garbage.

Okay. So what’s interesting, but what’s so special about this particular variant? When would you choose this over, say, variant 3 above?

One simple reason: in this variant, the address the `refill`

is loading from does not have a dependency on the current value of `bitcount`

. In fact, the next load address is known as soon as the *previous* refill is complete. This is a subtle distinction that turns out to be a fairly major advantage on an out-of-order CPU. Among integer operations, even when hitting the L1 cache, loads are on the high latency side (typically somewhere between 3 and 5 cycles, whereas most integer operations take a single cycle), and the exact value of `bitcount`

at the end of some loop iteration is often only known late (consider the simple variable-length code example I gave above).

Having the load address not depend on `bitcount`

means the load can potentially issue as soon as the previous refill is complete; then we have plenty of time to complete the load, potentially byte-swap the value if the endianness of our load doesn’t match the target ISA (say because we’re using a MSB-first bit buffer on a little-endian CPU), and then the only thing that depends on the previous value of `bitcount`

is the shift, which is a regular ALU operation and generally takes a single cycle.

In short, this somewhat obscure form of refill looks weird, but provides a tangible increase in available instruction-level parallelism. It was good for about a 10% throughput improvement on desktop PCs (vs. the earlier branchless refill it replaced) in the then-current version of the Kraken Huffman decoder when I tested it in early 2016.

Consider this a teaser for the next (and hopefully last) part of this series, in which I *won’t* introduce many more variants (maybe one more), and will instead talk a lot more about the performance of bit stream decoders and what kinds of things to watch out for.

Until then!

The separation of refill, peek & consume is really an important conceptual step for high performance bit stream reading.

(there’s a similar conjugate in bit stream writing, you want to break putbits into adding bits and flushing, and do multiple adds per flush)

One of the things we spend a lot of time on is figuring out how to do the maximum amount of work per refill. The crucial thing there is limiting the maximum length of codes on the hot path. Then you also want to construct your bit stream code so that the many bit reads per refill have a short dependency path between them to maximize ILP.

Something seems off in how you’re generating your code snippets.

In the Variant 2 code snippet, the curly braces don’t match, and one line is the non-sensical “if (count >= count;”. In Variant 3, peekbits3_msb has an operator but no return statement.

I hit a

really nastybug in the WordPress editor with this post.I use the HTML editor which means you have to manually enter ” as < and >. A recent version of the HTML editor seems to have a bug where that manual markup is turned back into un-escaped tags whenever you load something again for editing. And then the input sanitizing that runs when you save strips any “illegal” mismatched HTML tags.

Long story short, I edited this page earlier today to fix a typo someone reported, and didn’t realize it had un-escaped by angle brackets as part of reloading it into the editor, and now basically all the code fragments are mangled beyond repair.

I’m presently trying to see whether I can recover the original version, but it’s not looking good. I might have to retype the code. :/

Markup fixed, managed to recover it from a cached version of the non-broken post someone found. WordPress bug is reported. We’ll see how it goes.

Thanks for the blog post, it’s a very interesting read Fabian.

Eric Biggers’ Xpack is the first source where I’ve noticed Variant 4 :

https://github.com/ebiggers/xpack/blob/master/lib/xpack_decompress.c#L371

It was published 2 years ago, that’s even before Kraken announcement, though it doesn’t mean it’s the first program to use it.

I’ve always been interested by this refill method, precisely for the reason you mention : it’s possible to compute the load address in advance, without waiting for the nb of bits consumed.

As you know, FSE has been working on Variant 3 since pretty much the beginning.

But interestingly, every time I would try to adapt Variant 4 to it, I would end up losing performance, instead of gaining some.

Which always puzzled me.

That might be one these cases where a subtle difference changes the whole outcome.

Indeed, FSE uses MSB and reads backward, but that shouldn’t change much the logic compared to LSB forward, pretty much a mirror scenario…

Ah, didn’t know about that one! I’ll update the post.

That said, our variant has one very intentional extra wrinkle: turns out refilling to target 63 instead of 64 makes a noticeable difference here. With 64, you can’t do the OR trick, and (63 – bitcount)>>3 obeys several useful identifies for algebraic refactoring that (64-bitcount)>>3 does not. For example, (63-bitcount) == (63^bitcount) if bitcount>3 == 7-(bitcount>>3) (which is essentially a consequence of the previous one). The 7 is just a constant offset and can be absorbed into adjacent addressing modes, so this can end up saving another few instructions when you have several refills in the same basic block. . You only actually add the bias of 7*number_of_refills to the pointer for real once at the very end. (NB this is very much an assembly-level optimization that has to either be done by the compiler or in hand-written ASM; you can’t do this “by hand” in C/C++, the intermediate pointers you’ll get will likely end up going outside the containing object for at least some inputs, that’s no good.)

I admit I’ve gotten “a bit” obsessive with some of this over the years, to the point where I’ve written specialized CPU pipeline simulators to verify my understanding of the way some of our loops execute, and we actually ended up finding serious perf bugs in 2 separate ARM 64-bit microarchitectures that way. :)

Kraken uses all 4 of {LSB,MSB} x {forward,backward}, with at least 2 different algorithm variants used per-platform (some have 3) in different places for different reasons. I’ll cover some of the reasons you might do that in the next post. (Or that’s the plan, anyway).

Oh by the way, separate point: FSE/TANS is a special case for this particular issue because the dependency arcs for bitcount and refill

in a TANS decoderare usually not critical – at least, nowhere near to the extent you normally see in bitstream decoders.To explain what I mean, take a usual Huffman decoder. The critical path goes peek -> do a table lookup to figure out length (the symbol value / store output path is usually not critical, and it’s a dataflow sink so you really don’t have to worry about it much) -> consume that number of bits -> next peek. Note the table lookup (usually 3-5 cycles for a L1 hit, depending on uArch) is on the critical path. That’s why you need multiple streams to keep a Huffman reader fed.

Now take an interleaved TANS coder. You have multiple state values in flight, and the table lookup you do only depends on the state value, not on the bit reader. The bit reader only comes into it after the table read, and the lookup is not on the critical path.for the counts. (Unless you’re not interleaving enough.)

If you have a N-way interleaved FSE/TANS coder, the N table lookups can all start and proceed in parallel; the state refills (i.e. the per-symbol getbits) ultimately serialize on either the shift or the count update, depending on exactly what bit IO implementation you use, but either is not a big deal since both of these operations can happen in N back-to-back cycles for the N state updates. That’s nowhere near as bad as the situation is in a typical Huffman (or other variable-length code) decoder, and there’s still a bunch of work that can execute after the getbits in parallel with the refill for the next iteration – for example, finalizing the state updates and determining and storing the output symbols.

As a result, FSE/TANS impls are not particularly sensitive to the refill latency (they’re not completely immune, but it’s a much smaller effect). They’re much more sensitive to throughput issues (especially since they execute more instructions per symbol than a straight Huffman decoder does), and if you want your FSE/TANS to perform well, you want to use a throughput-optimized bit reader, not a latency-optimized one.

A Huffman decoder OTOH generally demands latency-optimized unless you really make sure you have enough independent work to hide the higher latency of throughput-optimized variants.

Thanks for these insightful additional details @Fabian !

Having spent some time around the bitstream readers of projects like libav (bitstream.*) and ffmpeg (get_bits.h + vlc.h), these are very interesting posts, which I would have liked to write myself.

I’m so waiting to see further details on what “cb” (Charles?) describes as “how to do the maximum amount of work per refill”, as indeed it is crucial. What Fabian describes in part2 around prefix codes is, I bet, only a stepping stone…

One last bit I observed around this refill and the various variants, is that 32bits and 64bits systems may need different ones. Hoping to see this in a later part maybe.