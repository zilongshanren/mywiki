---
title: Half to float done quick
url: https://fgiesen.wordpress.com/2012/03/28/half-to-float-done-quic/
published: '2012-03-28'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Half to float done quick

It all started a few days ago with [this tweet](https://twitter.com/#!/castano/status/182252019418021888) by Ignacio Castaño – complaining about the speed of the standard library `half_to_float`

in [ISPC](http://ispc.github.com/). Tom then [replied](https://twitter.com/#!/tom_forsyth/status/182315716077301762) that this was hard to do well in code without dedicated HW support – then immediately followed it up with [an idea](https://twitter.com/#!/tom_forsyth/status/182316268681043968) of how you might do it. I love this kind of puzzle (and obviously follow both Ignacio and Tom), so I jumped in and offered to write some code. Tom’s initial approach was a dead end, but it turned out that it was in fact possible to do a pretty decent job using standard SSE2 instructions (available anywhere from Pentium 4 onwards) with no dedicated hardware support at all; that said, dedicated HW support will exist in Intel processors starting from “Ivy Bridge”, due later this year. My solutions involve some fun but not immediately obvious bit-twiddling on floats, so I figured I should take the time to write it up. If you’re impatient and just want the code, [knock yourself out](https://gist.github.com/2144712). Actually you might want to open that up anyway; I’ll copy over key passages but not all the details. The code was written for x86 machines using Little Endian, but it doesn’t use any particularly esoteric features, so it should be easily adapted for BE architectures or different vector instruction sets.

### What’s in a float?

If you don’t know or care how floating-point numbers are represented, this is *not* a useful article for you to read, because from here on out it will deal almost exclusively with various storage format details. If you don’t know how floats work but would like to learn, a good place to start is Bruce Dawson’s [article on the subject](https://randomascii.wordpress.com/2012/01/11/tricks-with-the-floating-point-format/). If you do know how floats work in principle but don’t remember the storage details of IEEE formats, make a quick stop at Wikipedia and read up on the layout of [single-precision](http://en.wikipedia.org/wiki/Single-precision) and [half-precision](http://en.wikipedia.org/wiki/Half-precision_floating-point_format) floats. Still here? Okay, great, let’s get started then!

### Half to float basics

Converting between the different float formats correctly is mostly about making sure you catch all the important cases and map them properly. So let’s make a list of all the different classes a floating point number can fall into:

**Normalized numbers**– the ones where the exponent bits are neither all-0 nor all-1. This is the majority of all floats. Single-precision floats have both a larger exponent range and more mantissa bits than half-precision floats, so converting normalized halfs is easy: just add a bunch of 0 bits at the end of the mantissa (a plain left shift on the integer representation) and adjust the exponent accordingly.**Zero**(exponent and mantissa both 0) should map to zero – easy.**Denormalized numbers**(exponent zero, mantissa nonzero). Values that are denormals in half-precision map to regular normalized numbers in single precision, so they need to be renormalized during conversion.**Infinities**(exponent all-ones, mantissa zero) map to infinities.- Finally,
**NaNs**(exponent all-ones, mantissa nonzero) should map to NaNs. There’s often an extra distinction between different types of NaNs, like quiet vs. signaling NaNs. It’s nice to preserve these semantics when possible, but in principle anything that maps NaNs to NaNs is acceptable.

Finally there’s also the matter of the sign bit. There’s two slightly weird cases here (signed zero and signed NaNs), but actually as far as conversions go you’ll never go wrong if you just preserve the sign bit on conversion, so that’s what we’ll do. If you just work through these cases one by one, you get something like `half_to_float_full`

in the code:

static FP32 half_to_float_full(FP16 h) { FP32 o = { 0 }; // From ISPC ref code if (h.Exponent == 0 && h.Mantissa == 0) // (Signed) zero o.Sign = h.Sign; else { if (h.Exponent == 0) // Denormal (converts to normalized) { // Adjust mantissa so it's normalized (and keep // track of exponent adjustment) int e = -1; uint m = h.Mantissa; do { e++; m <<= 1; } while ((m & 0x400) == 0); o.Mantissa = (m & 0x3ff) << 13; o.Exponent = 127 - 15 - e; o.Sign = h.Sign; } else if (h.Exponent == 0x1f) // Inf/NaN { // NOTE: Both can be handled with same code path // since we just pass through mantissa bits. o.Mantissa = h.Mantissa << 13; o.Exponent = 255; o.Sign = h.Sign; } else // Normalized number { o.Mantissa = h.Mantissa << 13; o.Exponent = 127 - 15 + h.Exponent; o.Sign = h.Sign; } } return o; }

Note how this code handles NaNs and infinities with the same code path; despite having a different *interpretation*, the actual work that needs to happen in both cases is exactly the same.

### Dealing with denormals

Clearly, the ugliest part of the whole thing is the handling of denormals. Can’t we do any better than that? Turns out we can. After all, the whole point of denormals is that they are *not normalized*; in other words, they’re just a scaled integer (fixed-point) representation of a fairly small number. For half-precision floats, they represent `Mantissa * 2^(-14)`

. If you’re on one of the architectures with a “convert integer to float” instruction that can scale by an arbitrary power of 2 along the way, you can handle this case with a single instruction. Otherwise, you can either use regular integer→float conversion followed by a multiply to scale the value properly or use a “magic number” based conversion (if you don’t know what that is, check out [Chris Hecker’s old GDMag article](http://chrishecker.com/images/f/fb/Gdmfp.pdf) on the subject). Either way, 0 happens to have all-0 mantissa bits; in short, same as with NaNs and infinities, we can actually funnel zero and denormals through the same code path. This leaves just three cases to take care of: normal, denormal, or NaN/infinity. `half_to_float_fast2`

is an implementation of this approach:

static FP32 half_to_float_fast2(FP16 h) { static const FP32 magic = { 126 << 23 }; FP32 o; if (h.Exponent == 0) // Zero / Denormal { o.u = magic.u + h.Mantissa; o.f -= magic.f; } else { o.Mantissa = h.Mantissa << 13; if (h.Exponent == 0x1f) // Inf/NaN o.Exponent = 255; else o.Exponent = 127 - 15 + h.Exponent; } o.Sign = h.Sign; return o; }

Variants 3, 4 and 4b all use this same underlying idea; they’re slightly different implementations, but nothing major (and the SSE2 versions are fairly straight translations of the corresponding scalar variants). Variant 5, however, uses a very different approach that reduces the number of distinct cases to handle from three down to two.

### A different method with other applications

Both single- and half-precision floats have denormals at the bottom of the exponent range. Other than the exact location of that “bottom”, they work exactly the same way. The idea, then, is to translate denormal halfs into denormal floats, and let the floating-point hardware deal with the rest (provided it supports denormals efficiently, that is). Essentially, all we need to do is to shift the input half by the difference in the amount of mantissa bits (13, as already seen above). This will map half-denormals to float-denormals and normalized halfs to normalized floats. The only problem is that all numbers converted this way will end up too small by a fixed factor that depends on the difference between the exponent biases (in this case, they need to be scaled up by ). That’s easily fixed with a single multiply. This reduces the number of fundamentally different cases from three to two: we still need to dedicate some work to handling infinities and NaNs, but that’s it. The code looks like this:


static FP32 half_to_float_fast5(FP16 h) { static const FP32 magic = { (254 - 15) << 23 }; static const FP32 was_infnan = { (127 + 16) << 23 }; FP32 o; o.u = (h.u & 0x7fff) << 13; // exponent/mantissa bits o.f *= magic.f; // exponent adjust if (o.f >= was_infnan.f) // make sure Inf/NaN survive o.u |= 255 << 23; o.u |= (h.u & 0x8000) << 16; // sign bit return o; }

This is not the fastest way to do the conversion, because it leans on HW to deal with denormals should they arise (something that floating-point HW tends to be quite slow at), but it’s definitely the slickest out of this bunch.

More importantly, unlike the other variants mentioned, this basic approach also works in the opposite direction (converting from floats to halfs), which in turn inspired [this code](https://gist.github.com/2156668). There’s a bit of extra work to ensure there’s no unintended double rounding and to handle NaNs and overflows correctly, but it’s still the same idea. Which goes to show – sometimes making things as simple as possible really does have rewards beyond the pure intellectual satisfaction. :)

And that’s it. I admit that play-by-play narration of source code isn’t particularly exciting, but in this case I thought the code itself was interesting and short enough to give it a shot. And now back to our regularly scheduled posts :)

The play by play narration of source code is _exactly_ what makes this interesting! I was following this on twitter, and I’m grateful that you assembled everything in this blog presentation.

No back to the Debris stuff! *cracks whip*

Is it worth rolling the zero and denormal case into one? I would assume that zeros are common in typical data and denormals are less common, so you want zero handling to be simpler (at least when not using SSE). Btw, I was looking for fast half->float conversion so a very timely post!

This was biased towards SSE (as mentioned in the article, I wrote this for ISPC). Any special case requires at least one compare to figure out whether you hit that case, and in general another 3 extra ops (PAND, PANDN, POR or ANDPS, ANDNPS, ORPS) to merge the separate results (on SSE4+ you get the BLENDV family of ops, which turns the 3-op-merge sequence into 1 op, making it a lot less troublesome). Plus in SIMD code you can only skip cases when none of the lanes hit them, and figuring that out isn’t free either. Unless one case is really expensive, it’s cheapest to just compute all of them and combine as required – and given the combining overhead, keeping the number of cases down is a big win.

Another recurring question is whether handling Inf/NaN or denormals is worth it in the first place. For denormals, the answer is that half-denormals aren’t as rare as float/double denormals (since the range is so small), so they’re worth thinking about. Inf is worth having for the same reason – overflows aren’t that rare. NaN, well, at least in the half->float case they’re basically free if you do Inf so why not?

More importantly, I think it’s worthwhile to have a fast algorithm that deals with all the edge cases correctly. If you don’t care about Inf/NaN and denormals, you can easily make a faster version by just throwing away the handling for those cases. Taking an approach that’s not set up to deal with the corner cases and adding them back in tends to be more difficult.

Some perf numbers: on my Sandy Bridge i7, if I modify half_to_float4b to use BLENDVPS and turn on AVX codegen in VS, the code averages about 6.4 cycles for a vector (be it 4-element or 8-element). Even the plain SSE2 version comes out around 8 cycles per vector. So it’s not like full generality slows it down – in fact the version with 3 separate cases isn’t appreciably slower than the 2-case variants for normal values, and much faster when denormals are involved. The bottleneck is along the critical path, adding more cases is rather cheap.

Nice work. Clearly explained and elegantly handled.

My understanding is that modern Intel CPUs handle denormals much faster than the horror-show slowdowns on the Pentium 4 (http://www.cygnus-software.com/papers/x86andinfinity.html) but your article has reminded me that I should measure the performance of infinities/denormals/NaNs on current-gen CPUs.

Didn’t check how fast arithmetic on infinities/NaNs works out. On my Sandy Bridge i7 and using the SSE2 code, converting 4 normal floats to halfs takes about 8 cycles. If they flush to denormal halfs though (which get mapped to denormal floats), that number increases to about 140 cycles.

I gather that Sandy Bridges are reasonably quick at adding denormals now, but multiplies involving them are still slow.

This is the easy direction. The other direction is harder to do right and fast.

You might try vImageConvert_PlanarFtoPlanar16F and vImageConvert_Planar16FtoPlanarF on OS X/ iOS.

Read the full post: the second-to-last paragraph has a link to the equivalent code for the other direction.

Both of these are fast in FTZ/DAZ (flush-to-zero/denormals-are-zero) mode, and slower when float/half denormals are involved otherwise. They agree with those two mode flags by design (and all of them take care to handle NaNs and infinities correctly as well). If you want to always flush to zero, that’s easy to add and doesn’t influence the speed much. Handling denormals quickly is trickier, in either direction.

I tried the code reference in the second-to-last paragraph (float_to_half_fast3), and it doesn’t appear to round correctly. Try e.g. adding the fp16 values 0x3c00 and 0x3c01 (by converting to fp32, adding them together, and then converting them back to fp16); you should get 0x3c00 due to round-to-nearest-even, but the result is 0x3c01. Similarly, converting 0.5*5.9604644775390625e-08 should yield 0x0000 (again due to round-to-nearest-even), but yields 0x0001 (smallest denormal). Am I missing something?

See the reference versions of the code at the top of the file; the float to half code implements round half up, not RTNE.

I can write a RTNE version if you’re interested. This code was originally intended to replace the ISPC standard library function (float_to_half_full) and matches its behavior.

An RTNE version would be interesting indeed. Somehow it feels like the most elegant would be to just use whatever is the current rounding mode (so that it matches cvtss2sh, which I guess wasn’t in silicon at the time this post was already written), but I’m not sure if you can do that quickly. Perhaps one could do something like f += f * (1 << 13), which would round off the mantissa, but I guess it wouldn't work with denormals.

By the way, modern CPUs have a one-cycle penalty if you treat something first as integers and then as floats (or the other way around), since it has to be sent back and forth between the different functional units. But in this kind of code, it sounds pretty much unavoidable.

Argh, peeve: it’s an extra bypass delay, not a penalty. The effective latency is higher, but execution and throughput are unaffected. As long as the bypass delay isn’t on the critical path, it doesn’t even affect latency for the whole function.

Anyway, there you go: gist is updated with a round-to-nearest-even variant!

Thanks! I’ll be sure to give it a try soon.

Indeed it seems to work beautifully. Of course, if only GCC did multiversioning of inline functions, I could use the native functions on Haswell and this otherwise… :-)

So, I hate to bother you with this, but in a great case of Baader-Meinhof phenomenon, I found a case where I actually wanted to use this code at work (in TensorFlow), not just in my hobby projects. However, the lawyers at work say that just “I place this in the public domain” does not count as an effective license grant in many jurisdictions, and thus is problematic to include. (I know—I am surprised as well.) Do you think you could explicitly license the gists under some sort of OSI-compatible license, e.g. a BSD license?

If not, then that’s totally fine and we’ll do something else instead, of course.

I changed the license statement to use the CC0 license, which I consider to be a sufficient approximation of PD in the legal jurisdictions I care about. Does this work? (If not, I can just make a fork that’s BSD-licensed, but I’d rather not require attribution, not even in the docs.)

Supposedly the thing to do if you want a “good” (for whatever legalese meaning of good) license but don’t want to deal with attribution, is to just take the BSD license and remove all the requirements. Legal’s specific suggestion was this:

Copyright (c) ,

All rights reserved.

Redistribution and use in source and binary forms, with or without

modification, are permitted.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS

“AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT

LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR

A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT

HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,

SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT

LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,

DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY

THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT

(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE

OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Re-licensed version at https://gist.github.com/rygorous/eb3a019b99fdaa9c3064 – does this work for you?

It definitely does! Thanks a lot.

So if you want to see what it’s being used for:

https://bitbucket.org/eigen/eigen/src/4b9c7d45d069dc47b9eec2e4fe1bde9a97796dce/Eigen/src/Core/arch/CUDA/Half.h?at=default&fileviewer=file-view-default

https://github.com/tensorflow/tensorflow/commit/9d03824d6740be0c043c431566c917ec0cf6cf3f

I think there’s an issue in the code; in the FP16 struct, you base your bitfields on uint32_t (well, you call it uint :-) ) instead of uint16_t. This makes sizeof(FP16)==4, which probably isn’t what you want (and I don’t know if it could also mess up the alignment of members in the union).

Yes, because I have to. Bitfields on smaller-than-int types are not technically allowed by the C standard; they’re a non-standard extension.

I only use the FP16 struct for “bit casts”, not storage.

The link http://altdevblogaday.com/2012/01/05/tricks-with-the-floating-point-format/ has apparently changed to https://randomascii.wordpress.com/2012/01/11/tricks-with-the-floating-point-format/.

Thanks for the heads-up! Link updated.