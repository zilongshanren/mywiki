---
title: Morton codes addendum
url: https://fgiesen.wordpress.com/2022/09/09/morton-codes-addendum/
published: '2022-09-09'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Morton codes addendum

I wrote about Morton codes [long ago](https://fgiesen.wordpress.com/2009/12/13/decoding-morton-codes/), and I see that post and the accompanying code referenced frequently, but there’s a few points I want to make about it.

First, if you’re on a x86 CPU with BMI2 support, you have access to `PDEP`

and `PEXT`

, which make Morton encoding/decoding trivial. 2D Morton encoding one 16-bit coordinate to a 32-bit word is a single 32-bit `PDEP`

with `0x55555555`

, decoding it is a `PEXT`

with the same mask, and you can also use the same thing to encode 64-bit values with appropriate longer masks extended in the obvious way. The only fly in the ointment is that earlier AMD Zen CPUs technically support `PDEP`

and `PEXT`

but with an incredibly slow implementation, so this is not a good implementation if your target HW includes those CPUs. That said on Zen 3 and later the two instructions are fine, and ARM has added an equivalent to their vector pipes with SVE2, so while a bit iffy right now, I expect this might be the method of choice eventually, for CPUs anyway. I’ve been seeing this a fair amount in GPU shaders too, though, which brings me to the next subject for today.

The methods presented in the original post assume that the Morton-coded index value is 32 bits. I did not point this out explicitly in the text back in 2009, but you can either add another pass to produce a 64-bit result, or remove passes if you don’t need full pairs of 16-bit coordinates (or triples of 10-bit coordinates) interleaved into one 32-bit value.

For example, I gave this code for Morton-encoding a pair of unsigned 16-bit values to form a 32-bit index: (Dropping the comments that detail the bit layout after each step because they cause formatting issues)

// "Insert" a 0 bit after each of the 16 low bits of x uint32_t Part1By1(uint32_t x) { x &= 0x0000ffff; x = (x ^ (x << 8)) & 0x00ff00ff; x = (x ^ (x << 4)) & 0x0f0f0f0f; x = (x ^ (x << 2)) & 0x33333333; x = (x ^ (x << 1)) & 0x55555555; return x; } uint32 EncodeMorton2(uint32_t x, uint32_t y) { return (Part1By1(y) << 1) + Part1By1(x); }

If we only care about 8 bits worth of x and y, that first shift-and-xor pass (which tries to move the high 8 bits of `x`

into place) is useless and we can just skip it:

// "Insert" a 0 bit after each of the 16 low bits of x uint32_t Part1By1_8b(uint32_t x) { x &= 0xff; // 8 bits only this time! x = (x ^ (x << 4)) & 0x0f0f0f0f; // 0x0f0f would suffice x = (x ^ (x << 2)) & 0x33333333; // 0x3333 would suffice x = (x ^ (x << 1)) & 0x55555555; // 0x5555 would suffice return x; } // Only uses low 8 bits of x, y uint32 EncodeMorton2_8b(uint32_t x, uint32_t y) { return (Part1By1_8b(y) << 1) + Part1By1_8b(x); }

Lastly, if you’re encoding or decoding multiple values, which is extremely common because after all the whole point is to turn a pair (or triple) of values into a single integer, and the values are sufficiently narrow, we can handle x and y at once, by packing them into a suitable value before we do the rest of the computation.

For example, the case above where we only have 8-bit x and y coordinates (not that uncommon, say within a tile) can do a variant of the trick above to handle the full pair at only slightly more work than just handling a single coordinate in the original code would be:

uint32_t EncodeMorton2_8b_better(uint32_t x, uint32_t y) { // Pack x and y into t, starting at bits 0 and 16 respectively uint32_t t = (x & 0xff) | ((y & 0xff) << 16); // Do the full interleave as above (this time the full // 32-bit masks are necessary) t = (t ^ (t << 4)) & 0x0f0f0f0f; t = (t ^ (t << 2)) & 0x33333333; t = (t ^ (t << 1)) & 0x55555555; // Merge the halves. // All the odd bits are clear, so instead of shifting t right by // 16 to get y and then shifting left by 1, we can just shift right // by 15. return (t >> 15) | (t & 0xffff); }

All in all is this is roughly the same cost of a single invocation of the original `Part1By1`

. If you need a full 16-bit x and y but have 64-bit registers available, you can get a 32-bit result using a 64-bit extension of the original code (you just need to expand the masks appropriately).

This technique is independent of how exactly you do the bit-(de-)interleaving, so you can in principle combine this with `PDEP`

and `PEXT`

. There’s not much point though, because if you have a good implementation then doing two `PDEP`

with different masks and a final OR will be cheaper, and if you might encounter one of the bad implementations you just want to avoid these instructions entirely and use the above SIMD-within-a-register (SWAR) algorithms.

I’ve only showed 2D encoding here, the same trick works for decoding:

pair<uint32_t,uint32_t> DecodeMorton2_8b(uint32_t code) { // Separate even and odd bits to top and bottom half, respectively uint32_t t = (code & 0x5555) | ((code & 0xaaaa) << 15); // Decode passes t = (t ^ (t >> 1)) & 0x33333333; t = (t ^ (t >> 2)) & 0x0f0f0f0f; t ^= t >> 4; // No final mask, we mask next anyway: // Return x and y return make_pair(t & 0xff, (t >> 16) & 0xff); }

And of course the same idea works for the 3D variants as well.

In summary, To Whom It May Concern: 1. PDEP/PEXT and friends (when available and reliably good) make this trivial, 2. if you only need a few bits you can skip passes and make it cheaper, 3. the bit movement is completely regular so you can also pack multiple values ahead of time and get two (de)interleaves for the price of one.

`uint32` instead of `uint32_t` in some places. Typo?

Probably beside the point, but for 2×8->16, `lut_lo[x&0xff]^lut_hi[y&0xff]` seems to be faster than EncodeMorton2_8b_better (in scalar case, anyway), assuming you can spare 1024 bytes.