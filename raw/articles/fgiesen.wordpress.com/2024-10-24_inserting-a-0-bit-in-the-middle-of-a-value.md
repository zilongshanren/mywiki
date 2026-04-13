---
title: Inserting a 0 bit in the middle of a value
url: https://fgiesen.wordpress.com/2024/10/24/inserting-a-0-bit-in-the-middle-of-a-value/
published: '2024-10-24'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Inserting a 0 bit in the middle of a value

This one originally came up for me in Oodle Texture’s BC7 decoder. In the [BC7 format](https://registry.khronos.org/DataFormat/specs/1.3/dataformat.1.3.html#bptc_bc7), each pixel within a 4×4 block can choose from a limited set of between 4 to 16 colors (ignoring some caveats like the dual-index modes that don’t matter here) and consequently between 2 and 4 bits per pixel are used to store a color index. Some pixels are “anchors” which (for reasons outside the scope of this post) are forced to have the MSB of their color index be 0. Because these index bits are always 0, they aren’t actually transmitted in the compressed encoding. The end result makes for some rather hairy-looking index arithmetic in the spec a few paragraphs above [table 114](https://registry.khronos.org/DataFormat/specs/1.3/dataformat.1.3.html#bptcP2subset).

Needless to say, it’s inconvenient working in this form. Removing those always-0 index bits is among the last things a BC7 encoder usually does, and conversely, re-inserting them is among the first things a decoder wants to do, because there’s only ever between 1 and 3 anchor bits and having each index be the same bit width is definitely easier in the rest of the code.

Inserting a 0 bit in the middle of a value is not hard to do: we can split the original value into the bits below and at or above the target bit position, shift the top bits left by 1 more unit to make space, then reassemble everything together:

```
uint64 insert_zero_bit(uint64 value, int pos) {
uint64 bottom_mask = (1u64 << pos) - 1;
uint64 top_mask = ~bottom_mask;
uint64 bottom_bits = value & bottom_mask;
uint64 top_bits = value & top_mask;
return bottom_bits | (top_bits << 1);
}
```


This works fine, there’s nothing wrong with it, it’s not a bottleneck or anything, but it bothered me just how much of a production it was for what seemed like a simple operation. Some tinkering later, I found a slicker solution:

```
uint64 insert_zero_bit(uint64 value, int pos) {
uint64 top_mask = ~0u64 << pos;
return value + (value & top_mask);
}
```


The first part creates `top_mask`

directly. This version doesn’t need or use `bottom_mask`

, so creating top_mask from it is not a good way to do things here. In fact, even though creating a mask for the bottom N bits the way I did in the first code fragment is the more idiomatic way, creating the opposite mask that selects just the high bits is actually often cheaper, as this example shows: all you do is start with an all-1 mask (which is just a -1 constant in two’s complement) and shift it left. That’s not the point of this post, but I guess it counts as a bonus trick.

The actual point of this post is the second line. Adding a value to itself just gives two times that value, which is the same as left-shifting by 1; but in this case, we’re adding a copy of `value`

that has its low bits masked off. The end result is that we add 0 to those low bits, i.e. they stay the same. At or above bit number `pos`

, we do add the remaining bits of the value – which has the end consequence of shifting just those bits left and leaving the rest as it was. It only works for inserting exactly 1 bit, but it’s cute. (In the BC7 case with sometimes 2 or 3 anchors, we can just do it multiple times.)

We can also reverse this and remove a single bit in the middle when we know its value is 0:

```
uint64 remove_zero_bit(uint64 value, int pos) {
uint64 top_mask = ~0u64 << pos;
return value - ((value & top_mask) >> 1);
}
```


This version may look a bit funky because we build `top_mask`

from `pos`

. Shouldn’t we use `pos + 1`

, or set `top_mask = ~1u64 << pos`

, or something like that, since we start out with the extra zero bit there? But precisely because we already assume that bit is 0, it turns out not to matter. (Exercise to the reader.) Either way, this is not quite as nice as the insertion variant because of the extra shift.

Alternatively, if you don’t need the value aligned at the bottom of the uint (or are fine with shifting after), you can also use the dual of the bit insertion and add `value + (value & bottom_mask)`

to get a number that has everything shifted by 1.

Anyway. In the BC7 case it really didn’t matter, it just bothered me. But it’s cute regardless and I’ve found other uses for it since (that would have taken even more of a preamble to introduce).