---
title: Exact UNORM8 to float
url: https://fgiesen.wordpress.com/2024/11/06/exact-unorm8-to-float/
published: '2024-11-06'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Exact UNORM8 to float

GPUs support UNORM formats that represent a number inside [0,1] as an 8-bit unsigned integer. In exact arithmetic, the conversion to a floating-point number is straightforward: take the integer and divide it by 255. 8-bit integers are for sure machine numbers (exactly represented) in float32 and so is 255, so if you’re willing to do a “proper” divide, that’s the end of it; both inputs are exact, so the result of the division is the same as the result of the computation in exact arithmetic rounded to the nearest float32 (as per active rounding mode anyway), which is the best we can hope for.

The D3D11.3 functional spec [chickened out](https://microsoft.github.io/DirectX-Specs/d3d/archive/D3D11_3_FunctionalSpec.htm#3.2.3.5%20UNORM%20-%3E%20FLOAT) here a bit (granted, this verbiage was already in the D3D10 version as I recall) and added the disclaimer that

Requiring exact (1/2 ULP) conversion precision is acknowledged to be too expensive.


For what it’s worth, I had reason to test this a while back (as part of my [GPU BCn decoding experiments](https://fgiesen.wordpress.com/2021/10/04/gpu-bcn-decoding/)) and at the time anyway, all GPUs I got my hands on for testing seemed to do exact conversions anyway. It turns out that doing the conversion exactly is not particularly expensive in HW (that might be a post for another day) and certainly doesn’t require anything like a “real” divider, which usually does not exist in GPUs; correctly rounded float32 divisions, when requested, are usually done as a lengthy instruction sequence (plus possibly an even lengthier fallback handler in rare cases).

A conversion that is close enough for essentially all practical purposes is to simply multiply by the float32 reciprocal, i.e. `1.f / 255.f`

, instead. This is not the same as the exact calculation, but considering you’re quantizing data into an uint8 format to begin with, is almost certainly way more precision than you need.

What if, as a matter of principle, we want an exact solution, though?

### Option 1: work in double (float64)

Not much to say here. Converting the 8-bit value `x`

to double, multiplying by `1. / 255.`

, then converting the result to float32 happens to give the same results as the exact calc (i.e. dividing `x / 255.f`

). This is trivial to verify by exhaustive testing. It’s just 256 possible inputs.

### Option 2: but I don’t want to use doubles either!

Picky, are we? OK, fine, let’s get to the meat of this post. What if we’d like an exact conversion, would prefer to not use a divide, and would also prefer to avoid using doubles?

This is the fun part. First, let’s turn 1/255 into a geometric series:

and therefore

Going from a single divide to an infinite series might seem like it’s making our problems worse, but it’s progress. The divides by 256k are easy because those are powers of 2, hence exact (and, incidentally, non-overlapping bit shifts). Of course we can’t sum infinitely many terms, but we also don’t need to. All we need is an approximation that gets close enough to round to the right value. How many series terms is that?

The hardest to round cases turn out to be powers of 2, x=2k, k = 0, …, 7. They’re all basically the same, so let’s stick with the easiest example x=1 (k=0). Float32 has 24 effective significand bits (only 23 stored, since a leading 1 is implied). To round correctly, we need 24 correct bits after the leading 1 bit (23 actual bits plus the first truncated bit for rounding)… and then actually another term after that to make sure we don’t accidentally hit an exact halfway case. Our infinite series never terminates, so we need that extra term for non-0 values to make sure the sticky bit gets set pre-normalization to indicate unambiguously that the value ought to round up (and not break the tie towards evens).

Each term contributes 8 bits, and in our x=1 case, normalizing the floating-point number shifts out the first term entirely. In short, we need 1 “sacrificial” term that might get mostly normalized away (in the power-of-2 cases), 3 more terms for the bulk of the mantissa, and then 1 more term after that to avoid the halfway-case problem and ensure our sticky bit gets set correctly come rounding time.

So am I proposing summing 5 terms of a series? That doesn’t sound fast! And, fortunately, no. We don’t need to sum terms one by one; if we’re going to be multiplying anyway, we might as well combine multiple terms into one. Here’s the actual solution I’m thinking of (note this assumes compilation with proper IEEE semantics, not fast math shenanigans):

```
// Constants here written for posterity but assumed
// to be evaluated at compile time.
// All values exactly representable as float32.
const float k0 = (1.f + 256.f + 65536.f) / 16777216.f;
const float k1 = k0 / 16777216.f;
// suppose x is integer in [0,255], then:
float ref = x / 255.f;
// is exactly the same (in IEEE-754 float32 with RN) as
float tmp = (float)x;
float no_div = (tmp * k0) + (tmp * k1);
```


That first calculation of `tmp * k0`

creates 3 back-to-back copies of `x`

. That’s 24 bits of significand which is (just) exactly representable in float32 thanks to the implicit 1 bit. `tmp * k1`

creates another 3 copies (and thus terms of the series) scaled down by 2-24, which is likewise exact (it’s the same as the first term except for the exponent). That means we end up with two machine numbers, and adding them together has one final rounding step – the only rounding we’ll do. 6 series terms is more than we needed (and in fact 5 works fine), but the constants are easier to write down with 6 terms instead of 5 and it doesn’t really matter.

Final tally: after the int->float conversion, two multiplies and an add. When FMAs are available, the second multiply and the final add can also be replaced with a FMA, meaning this comes in at two FP ops with FMAs available, and 3 without. If there’s a way to do the exact conversion with less, I don’t know it.

**UPDATE:** Alexandre Mutel sent in a very slick suggestion on Mastodon based on a completely different approach that boils down to

```
// Constants evaluated at compile time.
const float k0 = 3.f;
const float k1 = 1.f / (255.f * 3.f);
return ((float)x * k0) * k1;
```


The realization here simply is that while the float32 reciprocal of 255 isn’t accurate enough to produce correct rounding, the reciprocal of 255*3 is, and multiplying integers in [0,255] by 3 is (easily) exact in float32. In this case I wrote the multiplication by 3 after floating point, but it can of course also be done on the integer side (which was Alexandre’s original suggestion); whichever is more convenient. This is two multiplications after the int->float conversion, even when no FMAs are available, so I think that’s our new winner.

Super interesting! I recently had this problem of precision when converting colors. I came with a slightly different solution to this problem, giving similar exact results and slightly 10% faster. Code in C#:

`static float ByteToFloat(byte value) => (value + value + value) * (1.0f / (3.0f * 255.0f));`

There’s also a somewhat clumsy option of intBitsToFloat(floatBitsToInt(float(x)*0x10101p-24f)+(x>0)). In denormals-are-zero environment, plain intBitsToFloat(floatBitsToInt(float(x)*0x10101p-24f)+1) probably “works” as well. The constant is just 1/255 rounded down.

These are exact versions for snorm8 and snorm16:

float decode_snorm8(int x) { if (x <= -127) x = -127; return float(31 * x) * (1.0f / (31 * 127)); }float decode_snorm16(int x) { if (x <= -32767) x = -32767; return float(73 * x) * (1.0f / (73 * 32767)); }

Sadly, there doesn’t seem to be such constant for unorm16: the best I could find has the first mismatch at x=61457:

float decode_unorm16_approx(int x) { return float(273 * x) * (1.0f / 17891056); }

Fix: float decode_unorm16_test(int x) { return float(273 * x) * (float)(1.0 / (273 * 65535)); }. The constant needs to be computed in double because 273 * 65535 doesn’t fit in a float. Or you can write 5.5893853e-8f directly.