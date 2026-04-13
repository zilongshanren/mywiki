---
title: UNORM and SNORM to float, hardware edition
url: https://fgiesen.wordpress.com/2024/12/24/unorm-and-snorm-to-float-hardware-edition/
published: '2024-12-24'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# UNORM and SNORM to float, hardware edition

I mentioned in a [previous post](https://fgiesen.wordpress.com/2024/11/06/exact-unorm8-to-float/) that doing exact UNORM or SNORM conversions to float in hardware was not particularly expensive, but didn’t go into detail how. Let’s rectify that! (If you haven’t read that post yet, please start there if you need an explanation of what the UNORM and SNORM formats are, as well as the basic idea.)

Previously, I explained how for n ≥ 1,

using the specific case n=8, but the proof is identical for other n. For UNORM8, SNORM8, UNORM16 and SNORM16 we need the cases n=8, n=7, n=16 and n=15, respectively. This is already good news, because this boils down to just a number of bit shifts (for the divisions by powers of two) and adds. In the cases we care about for UNORM/SNORM conversions, we also have 0 ≤ x ≤ 2n – 1, meaning it’s actually even simpler than adds, because we have n-bit values shifted by multiples of n bits, making the bit ranges non-overlapping, so there’s not even real additions involved, we’re really just repeating a bit string over and over. Therefore, even though expanding our division by 2n – 1 into an infinite series looks scary at first sight, it gives us a straightforward way to get the exact quotient to as many significant digits as we want.

With the scary-looking division step turning into something fairly benign, this looks fairly doable, but there’s a few special cases to take care of first.

### Special values

Ultimately, our goal is to turn our integer inputs into floating-point numbers. In this post I’m assuming we want to convert to the IEEE 754 [binary32](https://en.wikipedia.org/wiki/Single-precision_floating-point_format#IEEE_754_standard:_binary32) format, other output formats work similarly though. That means we need to determine the correct values for the sign, exponent and significand fields.

Both UNORM and SNORM formats have a few particular values that need some extra care for various reasons. For UNORM8, the two special values are the extremal ones: 0x00 (which turns into 0.0) and 0xff (which turns into 1.0). Both of these produce all-zero significand bits and exponent values that don’t occur for any of the other values (biased exponent values of 0 and 127, respectively), and it’s easiest to treat them as special cases.

UNORM16 is similar, with the special values being 0x0000 (turns into 0.0) and 0xffff (turns into 1.0). Also, UNORM8 and UNORM16 are very closely related. Converting a UNORM8 value x to float is exactly the same as converting the UNORM16 value `(x << 8) | x`

to float. (This works because 65535 = 2562 – 12 = (256 – 1) * (256 + 1) = 255 * 257 by the usual difference-of-squares formula, so instead of dividing x/255 we can also divide x*257 by 65535.) Since this is just repeating the same byte value twice, one possible, and entirely sensible, implementation of both UNORM8- and UNORM16-to-float conversions is to treat the former as the latter with the single byte input replicated twice.

The SNORM formats are slightly more complicated: the divisors 127 and 32767 don’t have a common factor, so they’re actually distinct cases as far as we’re concerned. We also need to handle the sign, and there are a few more special values to consider. For the latter, in the SNORM8 case, 0 and 127 (bit patterns 0x00 and 0x7f) turn into 0.0 and 1.0 respectively, and we gain two additional inputs, -128 and -127 (bit patterns 0x80 and 0x81 respectively) that both map to -1.0. For SNORM16, the relevant bit patterns are 0x0000 -> 0.0, 0x7fff -> 1.0, { 0x8000, 0x8001 } -> -1.0.

IEEE754 binary32 float is a sign-magnitude format; we therefore also need to convert the two’s complement SNORM input values into separate sign and magnitude, which boils down to extracting the sign bit (MSB) and computing the absolute value of the input integer. The latter requires a 15-bit adder for SNORM16 that is also sufficient for SNORM8.

For both UNORM and SNORM formats, this takes care of all the special cases and leaves us with a fraction x / (2n – 1) where we know that x is nonzero and the quotient is not an integer, since we just took care of the cases with exact integer results.

### The general case

That leaves the remaining cases, where we need to determine the exponent and the significand rounded to the target precision. I’ll work through it in detail for UNORM16, and add some final remarks at the end on how to handle the SNORM8 and SNORM16 cases. (UNORM8 is trivial to reduce to UNORM16, as pointed out above.)

For UNORM16, conceptually we want to compute x/65535.0 with infinite precision and then round the result to the nearest representable binary32 float, or whatever our target format is. All binary32 floats representing UNORM16 values are outside the subnormal range, which makes things fairly easy. The main thing is that we need to align the significand so it starts with a 1 bit to determine the correct exponent. We know x≠0, so there is definitely a 1 bit somewhere in x’s binary expansion. Therefore, normalizing x boils down to doing a leading zero count and shifting x accordingly:

```
// x has at most 16 bits (covers SNORM8/SNORM16 cases too)
num_lz = clz16(x)
normalized_x = x << num_lz
```


In practice, `normalized_x`

and `num_lz`

can be computed at the same time, not serially. One straightforward divide-and-conquer approach goes like this, but there are others:

```
normalized_x = x
num_lz = 0
if (normalized_x & 0xff00) == 0:
num_lz += 8
normalized_x <<= 8
if (normalized_x & 0xf000) == 0:
num_lz += 4
normalized_x <<= 4
if (normalized_x & 0xc000) == 0:
num_lz += 2
normalized_x <<= 2
if (normalized_x & 0x8000) == 0:
num_lz += 1
normalized_x <<= 1
```


This is not particular to UNORM->binary32 float conversions; regular uint16->binary32 conversions perform the same normalization step (and can easily be handled on the same datapath if desired).

Afterwards, `normalized_x`

is known to have its MSB (bit 15) set, so we can treat it as a constant 1, which simplifies things very slightly.

Next, we compute the tentative exponent (which turns out to be the final exponent because there are no rounding cases that would change it). The largest UNORM16 value we handle in this path is 0xfffe, which falls into the [0.5,1) interval, and has a binary32 biased exponent of 126. Any extra leading zeros decrement that exponent further, so we get

`exponent : uint8 = 126 - num_lz`


and our calculation earlier told us that to get x/65535.0, we just need to keep repeating the normalized mantissa. Sans implicit leading 1 bit, that means we get 23 bits worth of significand by concatenating

`initial_significand = { normalized_x[14:0], normalized_x[15:8] }`


However, we still need to perform rounding. If we’re doing truncation (or rounding towards negative infinity, which is the same for non-negative numbers), this significand is final. If we’re rounding towards positive infinity or away from zero, we’re always adding 1 – `normalized_x`

is not 0, which means there are always non-0 digits to the right of our significand, which means we should always round up in this case. That leaves round-to-nearest, which needs to look at the next-lower unrounded fraction bit, which in our case comes from `normalized_x[7]`

. If that bit is 1, we need to increment `initial_significand`

, otherwise we leave it as it is, meaning the final significand calculation for round-to-nearest is:

`final_significand = initial_significand + normalized_x[7]`


In short, all the standard IEEE rounding modes are easy and just require a single add at the end. This does not require a full-width adder: we don’t need to handle the case where the 16-bit normalized_x is all 1s, since that’s one of the special cases we handled outside. Since the bottom bits of `initial_significand`

all come from `normalized_x`

(with wrap-around since we keep repeating it), and we only ever add at most 1, we know carries can’t propagate arbitrarily far – any carries will be absorbed after at most 15 bits, since we eventually have to run into at least one originally 0 bit in `normalized_x`

. This is slightly more convenient than the situation with normal int-to-float conversions, where rounding can end up propagating a carry all the way across every significand bit and into the exponent bits. For UNORM or SNORM conversions, our initial guess at the exponent is always correct; the only case where rounding would ordinarily cause us to increment the exponent is the inputs corresponding to -1.0 and 1.0, but we handle those as special cases elsewhere.

For UNORM8/UNORM16, what’s the damage in total? A bit of multiplexing up front to handle UNORM8 and UNORM16 inputs both (to replicate the input byte into two copies turning UNORM8 into UNORM16), the detection and handling of the two special inputs 0x0000 and 0xffff, the 16-bit leading zero count/normalization, a 16-bit adder for the rounding, and the rest is wiring. Nothing particularly expensive!

### Dealing with SNORM formats

I won’t work through it in detail for SNORM8/SNORM16, but the same idea applies. For these formats, there’s a few more special cases to handle up front, and (as I’ve described it) we need to also detect the sign of the input (trivial, it’s just in the operand MSB) and compute the absolute value (in effect, a 16-bit adder).

After that, the significand datapath works the exact same way as the UNORM case. If we want to support directed roundings, we now have a sign bit to worry about, but that’s bog standard IEEE stuff and not hard. If we want a datapath that can handle all four of { UNORM8, UNORM16, SNORM8, SNORM16 }, probably the easiest way to do it is to place the SNORM8/SNORM16 absolute-value inputs into the top bits of the 16-bit leading-zero-count/normalize path.

Below that, we repeat the mantissa bits with a period of 15 bits for SNORM16 and a period of 7 bits for SNORM8 – a tiny bit more muxing. The rounding works exactly the same and the argument for why rounding only needs an adder covering the low 16 mantissa bits also stays the same.

And that’s it!

Does anyone have reason to care about this that doesn’t already know it? Probably not. I just thought it was fun to write up. I also wrote a small C++ [test program](https://gist.github.com/rygorous/056cb0219e6e65d50457d4b60a33a225?ts=4) to demonstrate that it this approach really gives the correct results.