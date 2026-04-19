---
title: Lossy Compression of Unsigned Float Numbers
url: https://www.4rknova.com/blog/2023/01/15/float-compression
author: Nikolaos Papadopoulos
published: '2023-01-15'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

I recently stumbled upon a very interesting blog post from [Martin Fuller](https://martinfullerblog.wordpress.com/) on the topic of normalized float compression [1]. What follows is a summary of Martin’s write up along with some additional material from relevant resources and some notes of my own. Some of the content below is copied verbatim from the sources referenced at the end.

# IEEE754 Single Precision Floats

The IEEE754 standard for floating point arithmetic defines a single precision 32-bit float using three components:

- A sign bit
- An 8 bit exponent
- A 23 bit mantissa

The number is computed as:

\[x = (-1)^{sign} \times 2^{exponent-bias} \times (1 + \sum_{i=_1}^{23} b_{23-i} 2^{-i})\]The bias depends on the number of bits in the exponent part and is computed as:

\[bias = 2^{k-1} - 1\]In the format above k = 8, therefore the bias is 127.

The exponent component defines the numerical range that the mantissa essentially quantizes. The bigger that range is, the lower the precision that can be encoded within that range. The size of the set of numbers that can be represented by the mantissa is fixed as there are always exactly 23 bits available in each of those ranges for 32-bit floats.

Below is an example of the calculation using a 16-bit half precision float with a 5-bit exponent and 10-bit mantissa:

![IEEE754 32bit Single Precision Float](../../assets/efa016d4d716de0e.webp)

# Lossy Compression of Unsigned Floats

The compression technique proposed by Martin uses 24 bits to encode the value and introduces a maximum error of 5.96046448e-8 (= 0.0000000596448).

The first step in understanding how this works is to inspect the various ranges that map to the different exponent values. The table below lists a small sample of those exponent values along with their respective numerical ranges.

| Exponent | Approx. Range |
|---|---|
| 01111100 | [0.125, 0.24999998509] |
| 01111101 | [0.250, 0.49999997019] |
| 01111110 | [0.500, 0.99999994039] |
| 01111111 | [1.000, 1.99999988079] |
| 10000000 | [2.000, 3.99999976158] |

The goal is to encode normalized numerical values (ie. in [0.0, 1.0] range) using less bits. The most intuitive way to achieve that is to drop one or more of the float number components discussed above. Since we are encoding an unsigned value, the sign bit is redundant and can be omitted. As shown in the table abovem, there is one and only one exponent value that maps to a range that is approximately 1 unit wide, therefore, if that exponent value is used, the exponent bits can be omitted as well. There is however one issue with this. As shown in the table, it is not possible to represent the exact upper end of our range (i.e. 1). The solution is to use an additional bit to handle this special case. The 23 bits of the mantissa and the 1 additional bit that is used for the special case of the upper bound sum up to 24-bits. This gives us back 8 bits which could be repurposed to store other data.

There are two simple steps involved in this encoding algorithm:

- Shift the normalized float into the [1,2) range by adding 1.0 to its value. The exponent bits are now fixed to 01111111 and no longer need to be stored. This introduces an error (hence why the compression is lossy) as the precision in this range is lower. We are essentially packing information that is normally encoded across multiple ranges into a single range.
- Store the 23-bit mantissa along with an additional bit to denote whether the value is exactly 1.

Martin’s implementation is included below with some additional comments:

```
uint CompressNormalFloatTo24bits(float floatIn)
{
// Transform from the [0.0, 1.0] range into [1.0, 1.99999988079).
floatIn += 1.0;
// Check if the value touches the bound and set the extra bit
// accordingly. Note that ((1 << 23) - 1) is equivalent to:
// 10000000000000000000000
// – 00000000000000000000001
// = 01111111111111111111111
// which is a mask for the bottom 23 bits
return (floatIn >= 2.0)
? (1 << 23)
: asuint(floatIn) & ((1 << 23) - 1);
}
// Note: The input has to have 0 in the top 8 bits
float DecompressNormalFloatFrom24bits(uint uintIn)
{
// Note that 0x3f800000 is equivalent to
// 00111111100000000000000000000000
// which is a mask with the value needed in the upper 9 bits for sign +
// exponent. An OR operator is used to set all the bits correctly. This
// is why the requirement exists that the upper 8 bits of the input must
// be set to 0.
// The subtraction of 1.0 at the end transforms the number back to the
// [0.0, 1.0] range.
return (uintIn & (1 << 23))
? 1.0
: asfloat(uintIn | 0x3f800000) - 1.0;
}
```