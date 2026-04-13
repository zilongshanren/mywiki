---
title: 64-bit mode and 3-operand instructions
url: https://fgiesen.wordpress.com/2013/03/13/extra-registers-and-3-operand-instructions/
published: '2013-03-13'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# 64-bit mode and 3-operand instructions

One interesting thing about x86 is that it’s changed two major architectural “magic values” in the past 10 years. The first is the addition of 64-bit mode, which not only widens all general-purpose registers and gives a much larger virtual address space, it also increases the number of general-purpose and XMM registers from 8 to 16. The second is AVX, which allows all SSE (and other SIMD) instructions to be encoded using non-destructive 3-operand forms instead of the original 2-operand forms.

Since modern x86 processors are trying really hard to run both 32- and 64-bit code well (and same for SSE vs. AVX), this gives us an opportunity to compare the relative performance of these choices in a reasonably level playing field, when running the same (C++) code. Of course, this is nowhere near a perfect comparison, especially since switching from 32 to 64 bits also changes the sizes of pointers and (at the very least) the code generator used by the compiler, but it’s still interesting to be able to do the experiment on a single machine with no fuss. So, without further ado, here’s a quick comparison using the [Software Occlusion Culling demo](https://fgiesen.wordpress.com/2013/03/10/optimizing-software-occlusion-culling-the-reckoning/) I’ve been writing about for the past month – a fairly SIMD-heavy workload.

| Version | Occlusion cull | Render scene |
|---|---|---|
| x86 (baseline) | 2.88ms | 1.39ms |
x86, `/arch:SSE2` |
2.88ms (+0.2%) | 1.48ms (+5.8%) |
x86, `/arch:AVX` |
2.77ms (-3.8%) | 1.43ms (+2.7%) |
| x64 | 2.71ms (-5.7%) | 1.29ms (-7.2%) |
x64, `/arch:AVX` |
2.63ms (-8.7%) | 1.28ms (-8.5%) |

Note that `/arch:AVX`

makes VC++ use AVX forms of SSE vector instructions (i.e. 3-operand), but it’s all still 4-wide SIMD, not the new 8-wide SIMD floating point. Getting that would require changes to the code. And of course the code uses SSE2 (and, in fact, even SSE4.1) instructions whether we turn on `/arch:SSE2`

on x86 or not – this only affects how “regular” floating-point code is generated. Also, the speedup percentages are computed from the full-precision values, not the truncated values I put in the table. (Which doesn’t mean much, since I truncated the values to about their level of accuracy)

So what does this tell us? Hard to be sure. It’s very few data points and I haven’t done any work to eliminate the effect of e.g. memory layout / code placement, which can be very much significant. And of course I’ve also changed the compiler. That said, a few observations:

- Not much of a win turning on
`/arch:SSE2`

on the regular x86 code. If anything, the rendering part of the code gets worse from the “enhanced instruction set” usage. I did not investigate further. - The 3-operand AVX instructions provide a solid win of a few percentage points in both 32-bit and 64-bit mode. Considering I’m not using any 8-wide instructions, this is almost exclusively the impact of having less register-register move instructions.
- Yes, going to 64 bits does make a noticeable difference. Note in particular the dip in rendering time. Whether it’s due to the overhead of 32-bit thunks on a 64-bit system, better code generation on the app side, better code on the D3D runtime/driver side, or most likely a combination of all these factors, the D3D rendering code sure gets a lot faster. And similarly, the SIMD-heavy occlusion cull code sees a good speed-up too. I have not investigated whether this is primarily due to the extra registers, or due to code generation improvements.

I don’t think there’s any particular lesson here, but it’s definitely interesting.

I’m in the habit of using x64 for exactly this reason. Free perf! I was surprised at first because bandwidth seems to only get more important every year, and 64-bit pointers require 2X memory and bandwidth v 32-bit. I need to do some experiments replacing pointers with indexes. Get the x64 perf gain and keep the x86 bandwidth advantage.

Interesting idea, using indexes instead of pointers to reduce memory bandwidth.

I’ve done this in some numerical code and had some good wins from it, but it’s not always straightforward – you need to have access to the base address as well as the offset, and sometimes that can be a little awkward. A better solution for many (most?) people is the X32 ABI if it’s available to you.

I wonder, how /fp:fast or /fp:precise would affect the test results.

Regarding the dude over here ( http://athile.net/library/blog/?tag=archsse2 ) SSE2 with default “/fp” setting (=precise) generates a lot of CVTPS2PD instructions to maintain floating point precision.

The CVTPS2PDs have nothing to do with “maintaining floating point precision” and everything to do with maintaining VS’s traditional floating point semantics for 32-bit code. :) (32-bit VS implements the old-school K&R-era semantics of “all FP computations are done with doubles, float is just a storage format”).

Either way, /fp:fast or not has little impact on this particular code base, because almost all of its FP computations are done using SSE intrinsics anyway.

There’s (relatively recent) x32 ABI on Linux, which is essentially x86_64 with 32-bit pointers. I didn’t make any experiments with it, but it promises to have the best of both worlds: plenty of registers, sane calling convention, and at the same time small memory footprint.