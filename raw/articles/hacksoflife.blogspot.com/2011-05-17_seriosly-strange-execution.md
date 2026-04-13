---
title: Seriosly Strange Execution?
url: http://hacksoflife.blogspot.com/2011/05/seriosly-strange-execution.html
author: Benjamin Supnik
published: '2011-05-17'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Okay then. The last time I looked at SIMD code was with Altivec; having come from PPC code I'm only barely getting used to this whole "little endian" thing, let alone the mishmash that is x86 assembler.

So a __m128 looks a lot like a float[4], and it's little endian, so if I do something like this:

`float le[4] = { 0, 1, 2, 3 };`

__m128 aa = _mm_loadu_ps(le);

then GDB tells me that aa contains 0, 1, 2, 3 in those "slots". And a memory inspector shows 0 in the lowest four bytes. So far so good.

Then I do this:

`__m128 cc = _mm_shuffle_ps(aa,aa,_MM_SHUFFLE(3,3,3,1));`

and I get 1,3,3,3 in rising memory in cc.

Wha?

Well, we can actually tease that one apart.

- The _MM_SHUFFLE matrix takes its parameters from high to low bits, that is, in binary 3,3,3,1 becomes 11111101 or 0xFD.
- Thus the low two bits of the mask contain the shuffle mask (01) for the low order component of my vector.
- Thus "1" is selected into the lowest component [0] of my array.

*memory*order I see, so a selector

*value*of 1 selects the [1] component. (In my LE, I stuffed the content of the __m128 with the array slot as part of a test to wrap my head around this.

So that's actually completely logical, as long as you understand that _MM_SHUFFLE's four arguments come in as bit-value positions, which are always written "backward" on a little endian machine. Naively, I would have reversed the macro order (and there's nothing stopping a programmer from creating a "backward" shuffle macro that reads in "array component" order). While this wouldn't be an issue on a big endian machine, the order of everything would mismatch memory - it's sort of nice that component 0 sits in the low order bits. Really what we need to do is read from right to left!

So I thought I had my head around things, until I looked at the contents of %xmm0. The shuffle code gets implemented in GDB (optimizer off) like this:

`movaps %-0x48(%ebp),%xmm0`

shufps $0xfd,-0x48(%ebp),%xmm0

movaps %xmm0,-0x28(%ebp)

If you speak x86, that's like "see spot run", but for those who don't:

- %ebp is the stack frame pointer on
[OS X](http://developer.apple.com/library/mac/#documentation/DeveloperTools/Conceptual/LowLevelABI/130-IA-32_Function_Calling_Conventions/IA32.html); with the optimizer off my local __m128 variables have been given aligned storage below the frame pointer as part of the function they sit in. -0x48 is the offset for aa and -0x28 is the offset for cc. - This is GCC disassembly, so the destination is on the right.
- SSE operations typically work as src op dst -> dst.
- So this code loads aa into %xmm0, shuffles it with itself from memory (the results stay in %xmm0), then write %xmm0 back to cc.

When viewed as a 128 bit integer in the debugger, %xmm0 contains:

128i: 0000803f 00004040 00004040 00004040The memory for CC contains this byte string:

4x32i: 40400000 40400000 40400000 3f800000

16x8i: 40 40 00 00 40 40 00 00 40 40 00 00 3f 80 00 00

4x32f: 3.0 3.0 3.0 1.0

00 00 80 3f 00 00 40 40 00 00 40 40 00 00 40 40I spent about 15 minutes trying to understand what the hell I was looking at, but then took a step back: if a tree falls in a forest and no one can see the trunk without writing it ot to memory, who cares? I wrote some code to do unpacks and low-high moves and sure enough, completely consistent behavior. If you treat an __m128 as an array of four floats, unpack_lo_ps(a,b), for example, gives you { a[0], b[0], a[1], b[1] }.

So what have I learned? Well, if you look at an Intel SSE diagram like

[this](http://www.jaist.ac.jp/iscenter-new/mpc/altix/altixdata/opt/intel/vtune/doc/users_guide/mergedProjects/analyzer_ec/mergedProjects/reference_olh/mergedProjects/instructions/instruct32_hh/vc320.htm), my conclusion is: component 0 is the same as the low bits in memory, which is the same as the first item of an array. The fact that it is drawn on the right side of the diagram is an artifact of our left-to-right way of writing place-value numbers. (I can only speculate that Intel's Israeli design team must find these diagrams even more byzantine.)

* This is because until now in the X-Plane 10 development cycle, we haven't needed it - X-Plane 10 is the first build to do a fair amount of "uniform" transform on the CPU. If anything that's a step back, because we really should be doing that kind of thing on the GPU.

It helps to look at vector shifts to understand that vectors have their highest numbered elements on the left. _mm_srli_epi64 (aka PSRLQ, logical right-shift) shifts bits towards the bottom of element 0. Similarly, _mm_bsrli_si128 (PSRLDQ) right-shifts bytes, shifting in zeros starting with byte 15. This is just like integers: left shift multiplies by two regardless of the endianness in memory. So it can help to think of vectors as [ D C B A ] or similar when writing comments to track data movement.


ReplyDelete