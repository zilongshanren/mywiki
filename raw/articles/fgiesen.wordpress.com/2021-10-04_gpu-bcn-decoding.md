---
title: GPU BCn decoding
url: https://fgiesen.wordpress.com/2021/10/04/gpu-bcn-decoding/
published: '2021-10-04'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# GPU BCn decoding

BC1-7 (variously also known by the older names S3TC, DXTC, RGTC and BPTC) are the standard compressed texture formats on PC. The newer BC6H and BC7 formats have precise specs that require bit-exact decoding, which means that encoders know exactly what results they’re going to get. The older BC1-5 are a lot more loosely specified, which has been a source of annoyance and problems for BCn encoder authors for some time.

While working on Oodle Texture, I did some experimentation trying to figure out what various GPU hardware decoders actually did. I did get good results for BC1-3 but BC4 and BC5 turned out to be a bit more troublesome. More recently, my colleague Sean Barrett spend some more time on this and we managed to get bit-exact equivalent expressions for Intel and NVidia hardware, but not AMD, where we were off by the last bit on some 32-bit float results in a small number of cases. This is completely irrelevant in practice but it bothered me, so last weekend I spent some more time trying to figure out those results too. I now have satisfying models for all three vendor decoders which match bit-exactly in my tests. That level of precision is unlikely to ever matter to anyone, but along the way there are several common mistakes in BC1-5 implementations and misunderstandings about the format to clear up, so it seems worth it to do a write-up.

### Overview

BC1-7 encode fixed-size blocks of 4×4 pixels to a fixed-size output: 64 bits (8 bytes) per block for BC1 and BC4, 128 bits (16 bytes) for all the other formats. The basic idea is to approximate the colors of pixels in a block by a small number of colors spaced evenly along one or more line segments in RGBA space. Per block, we send the endpoints of the line segment (quantized to a relatively low number of bits), plus an index per pixel that selects which of the colors along the line segment to use. These indices are usually between 2 and 4 bits each. Additionally, almost all of these formats have multiple modes that distribute the values slightly differently. Let’s briefly go over each format in turn:

BC1 sends color endpoints in RGB565 encoding (5 bits for red and blue, 6 bits for green). Somewhat unfortunately, this choice of encoding contains no exact grayscale values other than black and white, which means that slow grayscale gradients in this format tend to oscillate between areas tinged green and areas tinged purple. There are two modes, both of which use a 4-color palette and 2 index bits per pixel to select the palette entry (2×16 bits for the endpoints plus 16×2 bits for 16 2-bit indices, one per pixel, makes 64 bits total). The more commonly used mode uses the two specified endpoint colors, plus another two interpolated colors located 1/3rd and 2/3rds of the way along the line segment between them respectively, for a palette of 4 colors (all 4 colors have 1.0 in the alpha channel). The second mode has only one interpolated color halfway between the two endpoints; the third color has R=G=B=A=0, “transparent black” (in some cases, this is considered a separate “BC1A” format, and stock “BC1” decodes as R=G=B=0 and A=1; this distinction is not available everywhere though). This was intended for use with 1-bit alpha textures. If whoever reads the texture doesn’t care about the alpha channel, this second mode can also be used to get a “free black” even when the line between endpoints goes nowhere near actual black.

BC2 is for textures with an alpha channel that needs more than 1 bit. It consists of what is basically a BC1 color block (except here, all blocks are always in the first mode with 4 interpolated colors; the secondary mode is not available) and 4 bits of alpha per pixel, stored in memory before the BC1-esque color bits. BC2 has existed since the original S3TC, but I’ve never actually seen it used in practice. My guess is that the main reason it’s still around is that it costs very little hardware if you already support BC1 and 3, so despite little practical use, it’s cheap enough to support that nobody has lobbied to get it deprecated.

BC3 is the other format for RGBA textures. Once again, it contains a BC1 color block that is locked into the 4-color interpolation mode, and a different 64-bit encoding for the alpha bits in front. This one specifies two endpoints in the A channel as 8-bit values, followed by 48 bits (3 bits per pixel) to select the palette index. Once again, there are two modes: the more common one has the 8 colors spaced evenly along the line segment, the secondary mode only spaces 6 points along the line and adds two special indices that always decode to 0.0 and 1.0 no matter what the endpoint values are. BC3 is one of the two primary formats used for RGBA texture data.

BC4, unlike the previous formats, is intended for single-channel textures. It is often described as “just a BC3 alpha block”, which is close but not quite true as we’ll see later. There are unsigned and signed variants; the unsigned variants use the regular 8-bit UNorm encoding for values between 0 and 1, the signed variants use 8-bit SNorm for values between -1 and 1. In the signed variant, the special indices in the secondary mode correspond to -1 and +1, respectively.

BC5 also has unsigned and signed variants. A BC5 block is really just two independent BC4 blocks, one for the red and one for the green channel.

BC6H is meant for HDR color data. It only encodes RGB channels, the alpha channel always decodes to 1. There are unsigned and signed variants. The format decodes to 16-bit half-float format and color interpolation works by essentially treating the 16-bit half-floats as a 16-bit sign-magnitude integer value and interpolating those linearly, which works decently for unsigned data, not so well for signed data for blocks containing sign changes. BC6H has 14 modes, sort of, but most of these work essentially the same except for allocating endpoint bits slightly differently, depending on how close the values are to each other. There are two “major” modes in the format, one which specifies 2 sets of line segments (plus a code denoting which pixels use which line segment, from a small set of supported patterns) and has 3 bits of index data per pixel, and one of which specifies just one line segment with 4 bits of index data per pixel. BC6H decoding is complicated but specified bit-exactly so I won’t be talking about it in the rest of this post.

BC7 is a more complicated version of BC3 that adds several more options. It has 8 modes, 4 of which are RGB-only (with A decoding to 1.0), the idea being that even textures with alpha often have large opaque regions, and it helps everything to have more options for coding these color-only regions well. The different modes in BC7 contain various combination of either 1, 2, or 3 different line segments (and corresponding sets of endpoints), once again with the assignment of pixels to line segments chosen from a small, fixed set; either one index per pixel (when RGB and A behave similarly) or two (when they do not); and various index pixel depth, plus several other features that I won’t get into here. BC7 decoding is also complicated but specified bit-exactly and won’t appear in the rest of this post.

### Common (software) mistakes

This is the part that’s probably the most applicable to the majority of readers: before we even get to specification details, many encoders and decoders make two small mistakes in how they implement the basics.

The first and most common one is about the different modes in the BC1 format. The way a BC1 encoder selects which mode it wants a block to use is by sending the coded endpoints in a different order. Note that both color endpoints get packed to RGR565 format. When the first endpoint, interpreted as an unsigned 16-bit integer, is larger than the second one, this selects the more common four-color mode. If the first endpoint is less than or equal to the second, that selects three-color + transparent black mode. Note that when both colors are equal, you have no choice; you always end up in three-color mode (where the 3rd palette entry is special). This is not much of a problem because both endpoints being equal is a degenerate case anyway; all three other palette entries are equal in that situation, so just avoid the third. In all other cases, when the colors you picked result in the wrong order, the encoder can just swap them around and adjust the indices to match. Linear interpolation is symmetric so this does not change the set of available colors. This much, essentially all implementations get right. The tricky part involves BC2 and BC3: BC2 and BC3 blocks *almost* contain regular BC1 blocks, except they don’t have any mode-switching. The color values in BC2/3 always use the four-color mode. (This is pointed out in all specifications of the format, but easy to miss.) Several encoders only ever use the four-color mode to begin with, and swapping endpoints into the order you would need for BC1 never hurts; just be aware that three-color mode is not an option for BC2 or 3, and encoding assuming you have it available will give the wrong results.

The second mistake involves BC4 and 5. BC4 encoders/decoders often take “it’s just like a BC3 alpha block” too far and actually encode or decode unsigned BC4 (or BC5) as BC3 8-bit data. This is not far off, but it’s an approximation. BC4 and BC5 actually decode somewhat differently than BC3 alpha does, with measurably different results and higher internal precision. For most textures this doesn’t matter too much, but the extra precision is definitely useful for content like normal maps. BC5 two-channel normal maps can get up to nearly 11 bits of precision in regions with small value range, as opposed to the at most 8 bits you would get out of regular R8G8B8A8 or BC3 alpha encoding. It’s highly contextual whether this matters or not, and especially for rough surfaces there’s usually not much difference, but it can be useful especially when rendering things with reflective, smooth surfaces like machine parts, cars and so forth.

### What do the specs say?

The premise of this post is that GPU decoders don’t exactly agree with each other, but of course they at least approximately agree or the formats would be useless in practice. Can we say something more about what “approximately agree” means? The two primary sources for this sort of thing in the PC space are the Khronos Data Format Specification and the D3D11 Functional Spec. The Khronos spec is in force for Vulkan and supplants the older OpenGL extensions saying the same thing; as of this writing, the current version is 1.3 and the description of the BC1 formats starts [here](https://www.khronos.org/registry/DataFormat/specs/1.3/dataformat.1.3.html#S3TC). It short and to the point, but unfortunately fairly light on details and completely missing any compliance requirements; it specifies what results an ideal decoder should produce, but not how close practical implementations need to be to be considered good enough.

Our secondary primary source is the D3D11 Functional Spec (a descendant of the D3D10 spec and the D3D12 spec is given as differences from D3D11, so this is still in force). The relevant sections start [here](https://microsoft.github.io/DirectX-Specs/d3d/archive/D3D11_3_FunctionalSpec.htm#19.5%20Block%20Compression%20Formats). In theory, GL/Vulkan devices could do something completely different, but in practice the same hardware is designed to work for both (for obvious reasons), so whichever spec has the more detailed requirements ends up determining the requirements that the hardware is actually trying to satisfy. And the D3D11 version of the spec is a lot more detailed; in particular it has the short section 19.5.2 “Error Tolerance” which I’ll quote verbatim:

Valid implementations of BC formats other than BC6H and BC7 may optionally promote or do round-to-nearest division, so long as they meet the following equation for all channels of all texels:

| generated - reference | < absolute_error + 0.03 *MAX( | endpoint_0 - endpoint_1 |, | endpoint_0_promoted - endpoint_1_promoted | )absolute_error is defined in the description of each format.

endpoint_0, endpoint_1, and their promoted counterparts have been converted to float from either UNORM or SNORM as specified in the Integer Conversion rules. Values that the reference decodes to 0.0, 1.0 or -1.0 must always be exact.

For BC6H and BC7, decompression hardware is required to be bit accurate; the hardware must give results that are identical to the decoder described in this specification.


The part about promotion is clarified in the next 2 subsections and boils down to implementations being allowed to do fixed-point computations at an intermediate wider bit width, as long as values are extended to that intermediate bit width as specified. For the rest, I’ll note that all formats under consideration permit endpoint_0=endpoint_1, in which case the error term reduces to `| generated - reference | < absolute_error`

, so the absolute error term (I’ll get to that in a minute) primarily affects how precise decoding of the endpoint values themselves is. This value is 1/255 for BC1-3, 1/32767 for the signed BC4/BC5 formats, and 1/65535 for unsigned BC4/5 (indicating that BC4/5 have higher internal resolution). The second, relative error term requires that implementations have to be within ±3% of the reference, which is really not a tight bound: even for usual 8-bit texels in a range of [0,255], ±3% works out to ±7 in the integer space (actually 7.65, but when only considering integers, we can round down here) in the worst case when we choose endpoint_0 so that it decodes 0 to and endpoint_1 to decode to 1, or vice versa. This relative error term matters most when the endpoints are far from each other in a given channel, and the rationale for it is that the BC1 quantization is pretty harsh to begin with (you only get 4 values to cover that range). An extra 3% is less than one fifth the expected quantization error from getting to use at most 4 colors, so in that sense, it’s not a big deal. The problem for encoders is that there are often many candidate encodings for a block that have similar error; more possible encodings gives us more chances to get overall errors low if we can manage to find just the right combination of endpoints and indices, including spacing endpoints much further apart than necessary given the range of values in the block because it makes one of the interpolated values land exactly where we need it. Having this relative error term in the mix means we have to play it safe here.

More to the point, having this level of allowed differences between hardware encoders also means that the same texture wil decode differently on different GPUs, even if we’re not trying to do anything tricky. Sometimes blocks legitimately have a large value range because that’s what those blocks’ contents are, and having large differences possible between decoder implementations is a bummer, because we don’t even get an accurate picture of what the error from encoding any particular texture in BC1-5 is; it depends on what GPU it’s decoded on!

The reason I originally looked into this for Oodle Texture was because I wanted tighter error bounds than just the spec requirements. While in theory there is a large space of possible decoder implementations permitted by the spec, in practice there is a very small number of GPU vendors active in the PC space, and once they’ve settled on a particular decoder implementation, they really have no reason to ever change it unless the spec changes again. So I did some testing, and as far as I can tell, indeed neither NVidia, AMD nor Intel seem to have touched their BCn decoder blocks in the last 10 years or so (and why would they?). That means that both in terms of the current marketplace and installed base, there’s mostly just 3 decoders we have to worry about; that excludes really old hardware as well as vendors with a tiny market share, but if nothing else it will give us an idea of what we should really expect.

### Probing what decoders do

Luckily, the BCn formats have many properties that make it fairly tractable to completely capture decoder behavior. For the BC1/BC2-3 color portion, the R, G, B channels are decoded independently from each other, and the pixels don’t influence each other. R and B endpoints are specified with 5 bits of precision and G with 6. That means we can look at all possible combinations of R/B endpoint values with a 128×128 pixel texture (32×32 blocks). In each block, we make sure to use each of the 4 indices at least once, and then write a compute shader that does a `Load`

/ `texelFetch`

operation for every pixel (so that filtering doesn’t confuse the results) and writes the result to a 32-bit float/channel texture. For G we need a texture with 256×256 pixels for 64×64 blocks. That’s a set of 3 small images that completely captures BC1 decoder behavior. For BC3 alpha and BC4 unsigned/signed we have 8-bit endpoints in a single channel, so we need an entire 1024×1024 pixels (256×256 blocks). For BC2 and BC5 we can do some quick tests just to confirm that they behave as expected (BC2: alpha is a 4-bit encoding that decodes as expected, BC5: same as two BC4 blocks, one for R and one for G).

Some more quick tests indicated that:

- As far as I can tell, on all three vendors tested (AMD, NV, Intel), BC1 internally decodes to 8-bit fixed point, which then, depending on whether the format is UNorm or UNorm_sRGB, gets converted to float either using the same conversion the GPU uses for regular 8-bit UNorm textures, or a 256-entry LUT (or maybe LUT + math combination?) used for sRGB->float conversions (hard to be sure, but tested by noting that all values obtained for 8-bit BC1 RGB channels appear in the list of 256 values output by regular UNorm or UNorm_sRGB conversions; if this is not what’s happening the observed behavior appears to be equivalent).
- On all three vendors, BC3 alpha appears to decode to 8-bit fixed point, once again matching the 8-bit UNorm->float conversions, which in turn for all 3 vendors exactly match the results of rounding “x/255” to the nearest floating-point value. Setting e.g. endpoint_0=0 and endpoint_1=1 (8-bit integer values) did
*not*result in any interpolated values inside the open interval (0,1/255). - On all three vendors, BC4 and BC5 decode to more than 8 bits of precision. For Intel and NVidia, all interpolated values for unsigned/signed BC4/5 formats occur on the list of decoded 16-bit UNorm and 16-bit SNorm values, respectively, and they are consistent with first decoding to 16-bit int then converting to float via the UNorm/SNorm conversions. On all three vendors, 16-bit UNorm decode as correctly rounded
`x/65535`

and 16-bit SNorm as correctly rounded`max(x,-32767)/32767`

, respectively. On AMD, the resulting floats do*not*all appear on the list of UNorm16/SNorm16 values; instead the decoder appears to use an internal 14-bit format, details below. Setting e.g. endpoint_0=0, endpoint_1=1 (integer byte values) for BC4 unsigned*does*result in interpolated values inside (0,1/255).

Furthermore, Ignacio Castaño wrote a [2009 blog post](http://www.ludicon.com/castano/blog/2009/03/gpu-dxt-decompression/) on how NVidia GPUs decompress BC1 (with mention of the relevant patent), and it was straightforward to verify that more recent NV GPUs (tested on GeForce 1080 and 2070 series devices) still appear to use the same logic. For Intel, testing was done on a late-2013 laptop with Haswell integrated GPU, and we contacted Tom Forsyth at Intel to confirm that the BCn decoder logic was still essentially unchanged and answer some questions regarding the exact BC4/5 decoder behavior. For AMD, testing was done with an old Radeon HD 7000 series GPU we had kicking around the office as well as game console devkits for the previous and current generation (GCN2 and RDNA2 variants, respectively), the latter on account of them already being on the network and set up for remote testing. (So no pre-GCN AMD GPU in the mix, not sure if that makes a difference).

### What all decoders seem to agree on

For all vendors, the endpoint_0 and endpoint_1 values in all formats (which always appear as palette entries 0 and 1, respectively) appear to be reproduced exactly the same. BC1 as written in the D3D11 functional spec first expands the endpoint values from 5 or 6 bits to 8 bits by replicating the top bits; all three vendors appear to do this or something equivalent, and then convert the result from 8-bit UNorm to float exactly. For BC4/5, likewise palette entries 0 and 1 always seem to exactly make the result of the respective correctly rounded UNorm8 or SNorm8 to float conversion, respectively. Furthermore the D3D11 functional spec requires (quoted above) that the values specified to decode to exactly 0, 1 or -1 indeed decode to these values in all implementations, and this appears to hold.

Taking these all together, this means that for BC1/BC2-3 color, the parts that decoders actually differ in are how exactly the colors 1/3rd and 2/3rds of the way (in four-color mode) or 1/2 of the way (in 3-color mode) are computed, and for BC3 alpha and BC4/5, how the 6 (respectively 4, depending on the mode) actually interpolated values are determined. I’ll cover these vendor by vendor, in order of increasing complexity (of description though not necessarily hardware).

### Intel GPUs

Intel’s decoders are the most straightforward to describe. BC1-3 color is computed in fixed point, from the endpoint values extended to 8 bits using bit replication, using the formula `((256-w)*a + w*b + 128) >> 8`

or something equivalent, i.e. 8-bit fixed-point linear interpolation with round-to-nearest. For the 1/2-of-the-way color in 3-color mode, the weight is w=128 (of course); in 4-color mode, the interpolation weights are w=85 (for the 1/3rd point) and w=171 (for 2/3rds), respectively. These weights are just `round(k*256 / 3)`

for k=1, 2.

BC3 alpha appears to use the weights `round(k*256/7)`

for k=1,…,6 in 6-interpolated color mode, and `round(k*256/5)`

for k=1,…,4 in 4-interpolated-color mode.

BC4, signed and unsigned both, takes the integer UNorm/SNorm endpoint values (for SNorm, -128 is an alternative encoding for -127, they mean the same thing), and use the 16-bit interpolation formula `t = ((65536-w)*a + w*b + 128) >> 8`

to get the interpolation result, where `w=round(k*65536/7)`

, k=1,…,6 in 6-interpolated-color mode, `w=round(k*65536/5)`

, k=1,…,4 in 4-interpolated-color mode.

For BC4/5 unsigned, the GPU then computes `t + (t >> 8)`

; the resulting integer is treated as a 16-bit UNorm value and finally converted to float. For signed, the GPU computes `abs(t) + (abs(t) >> 7) + (abs(t) >> 14)`

with the sign of the original t (i.e. if t was negative, this result is then negated). This number is treated as 16-bit SNorm value and converted to float.

### AMD GPUs

AMDs GPUs still behave in a way that is straightforward to describe, with a wrinkle involving BC4/5. But let’s start with BC1-3: BC1-3 is computed in fixed point, from the endpoint values extended to 8 bits using bit replication, using the formula `((64-w)*a + w*b + 32) >> 6`

or something equivalent, i.e. 6-bit fixed-point linear interpolation with round-to-nearest. This is the exact same computation that is prescribed for interpolation in BC7 decoders, so it likely uses the same hardware. In BC1 3-color mode halfway points, we have w=32 (again, no surprise), and for 4-color mode the weights are 21 and 43, again matching BC7 and equivalent to `w=round(k*64/3)`

for k=1, 2.

BC3 alpha uses the weights `round(k*64/7)`

for k=1,…,6 in 6-color mode, `round(k*64/5)`

for k=1,…4 in 4-color mode.

BC4/5, signed and unsigned both, tales the integer UNorm/SNorm endpoint values (for SNorm, after the -128 -> -127 correction) and uses the same interpolation formula, just without the shift or rounding term: `t = (64-w)*a + w*b`

, again suggesting that it’s probably all using the same hardware. The resulting product fits in a 14-bit integer. Note that by construction, t is either in [-127*64,127*64] for signed values or [0,255*64] for unsigned ones.

For BC4/5 SNorm, this result is then converted to float by effectively doing a correctly rounded division by 127*64 = 8128. This turns out to be somewhat more complicated than the straight division by 127 used for 8-bit SNorm values, mainly due to the extra 6 bits in the input. For BC4/5 UNorm, the result is converted to float by doing an *almost* correctly rounded division by 255*64 = 16320. Once again, this would ordinarily be a bit more complicated than the division by 255 used for UNorm8->float, again due to the extra 6 bits of input; however, here, for whatever reason, be it just a bug or a small hardware optimization that is not clear to me, a very small subset of values (13 total of the 16077 unique possible results for all combinations of inputs) is rounded incorrectly.

This result differs in final mantissa bit of the 32-bit float values only and it truly does not matter for any use case I can imagine since actual BC4/5 encoding-induced errors are many orders of magnitude larger than this, but in case anyone cares about reproducing the results exactly, my hacky conversion function that manually detects the incorrectly-rounded cases is [here](https://gist.github.com/rygorous/ea042174cc289c3153876d2cace970d2). (The version for signed decoding is unnecessary because that case is correctly rounded. I thought implementing it might give me an idea of what’s going on with the unsigned version, but no dice.)

OK, so both Intel and AMD are reasonably easy to explain, and probably just reuse hardware that is already there; it’s worth pointing out that BC6H also uses the same interpolation formula as BC7 and works on signed 17-bit integers internally, so there’s probably at least 3 color channels worth of 6×17-bit multipliers lying around somewhere in the decoder path. I was initially very surprised about the 16-bit weights used by the Intel version, but if they just swap the operands between BC4/5 and BC6 and build something like a 8×17-bit multiplier instead, that might be totally fine. (Or maybe they even have their own wider multiplier for BC4/5. Don’t know, I’m just guessing at likely implementation options from the observed behavior here.)

### NVidia GPUs

The formulas used by NVidia GPUs are nothing like the other two vendors, and do not look like they can share any hardware with BC6H/BC7 decoding at all. They do, however, very much look like they’re designed to share as much as possible between BC1-5, and by someone who is dead set to spend as little logic on it as they can reasonably get away with. My best guess is that this design probably predates BC6H/BC7; BC6 forces you into having at least a few rectangular multipliers in the BCn decoder block and once you have them, there’s not much reason to avoid using them.

Anyway, the decoders we’ve seen before use simple linear interpolation formulas with round-to-nearest, or at least give results that are equivalent to them. The NVidia decoders use different formulas for the 5-bit-endpoint red/blue channels in BC1 than they use for the 6-bit-endpoint green channel, and then green/alpha channel logic seems to be the same, with BC4 and BC5 using just the green/alpha channel decoders (and ignoring red/blue). This in turn means that red/blue only ever work from 5-bit inputs, whereas green needs to support both 6-bit and 8-bit endpoints (the latter for use in BC5), and alpha always has 8-bit endpoints (for BC3).

Let’s do the simpler red/blue channels first. Ignacio’s 2009 article gives the formulas for palette entries 0/1 as well, but those are just equivalent ways of writing the 5->8 bit expand using bit replication. The interesting palette entries are 2 and 3, and those are (again, not following Ignacio’s presentation here, but this gives bit-equivalent results):

// red/blue, four-color mode; a, b are 5-bit col2 = ((2*a + b) * 22) >> 3; col3 = ((2*b + a) * 22) >> 3;

The rationale here is that expanding from 5 bits to 8 is effectively multiplying by 255/31, and if we compute (2*a + b) we need to divide the result by 3; the final fraction of 255/(31*3) = 2.741935 is quite close to 11/4, so that’s what it’s approximated by. So this calculation folds bit-expansion and linear interpolation into one and can work with slightly smaller intermediate values as a result (the multiplications by known constants are just shifts and adds).

For red and blue, the halfway point in three-color mode is computed similarly:

// red/blue, three-color mode; a, b are 5-bit col2 = ((a + b) * 33) >> 3;

This is a decent approximation, but somewhat annoyingly, it just behaves differently from the more straightforward AMD/Intel ones; folding the scaling and lerp into one makes the weight constants slightly smaller but also makes the overall rounding behavior different, which is awkward. Oh well.

Anyway, green and alpha is when the fun really starts. Both green and alpha do use a more explicit linear interpolation formulation with round-to-nearest, but the values being multiplied by and the overall way things are put together are still decidedly odd. But let’s start at the beginning. First, BC1 green, four-color mode (again, presentation different from Ignacio’s, but equivalent)

// green, four-color mode, a, b are 6-bit ae = (a << 2) | (a >> 4); // bit expand be = (b << 2) | (b >> 4); diff = be - ae; scaled_diff = 80*diff + (diff >> 2); col2 = ae + ((128 + scaled_diff) >> 8); col3 = be + ((128 - scaled_diff) >> 8);

and in three-color mode:

// green, three-color mode, ae, be as above diff = be - ae; scaled_diff = 128*diff + (diff >> 2); col2 = ae + ((128 * scaled_diff) >> 8);

Here, the effective factor is something like 80.25/256, which is pretty far off (the correct fraction for a real 1/3rd here would be around 85.33/256).

On to BC4/5. Here, our interpolation factor are multiples of 1/7th and 1/5th, respectively. NVidia conceptually splits this into two parts: we first multiply by the small integer numerator, and then by a fixed-point approximation of the reciprocal of 1/5 and 1/7, and all of that is sandwiched into our interpolation formula above.

The set of numbers we might want to multiply by here are thus 0,1,2,3,4,5,6, and 7. For one final trick, note that instead of saying that we want “1/5th of the way from a to b”, we might equivalently say (by symmetry) “4/5ths of the way from b to a”, and NV decoder uses this to avoid doing any multiplies in the “multiply by numerator” portion: of the values 0 to 5 we need for the multiples of one fifth, 0 is 0 (which is very cheap to multiply by indeed) and 1, 2, and 4 are powers of 2 (shifts). Of the remaining numbers, 5=5-0 (so instead of going 5/5ths from a to b, we can go 0/5ths from b to a) and 3=5-2 (turn 3/5ths from a to b into 2/5ths from b to a). For the multiples of 1/7th, it works similarly: 0,1,2,4 are already easy, and for the remaining ones, 7-3=4 (which is easy), 7-5=2 (easy), 7-6=1 (easy), and 7-7=0 (easy). So the HW here can switch “a” and “b” around so that the factor is either 0 or a power of 2, choosing which end of the line segment to interpolate from.

Either way, the interpolation procedure for BC4 in 6-interpolated-color mode works out to:

// BC4; a, b are 8-bit, 6-interp mode ae = expand_to_16(a); be = expand_to_16(b); diff = b - a; // b, a not be, ae! col0 = ae; col1 = be; col2 = ae + 36*(diff); // 1/7 col3 = ae + 36*(diff<<1); // 2/7 col4 = be - 36*(diff<<2); // 3/7 col5 = ae + 36*(diff<<2); // 4/7 col6 = be - 36*(diff<<1); // 5/7 col7 = be - 36*(diff); // 6/7

where `expand_to_16(x) = (x<<8) | x`

for unsigned formats and the way less nice `expand_to_16(x) = copysign((abs(x) * ((1<<14) + (1<<7) + 1) >> 6, x)`

(aside from the sign manipulation this is just shifts and ORs, I just wrote it more compactly).

Here 36=32+4 is a convenient number with just 2 set bits which makes it easy to multiply by with just shifts and adds. The actual factor we would want to approximate for the reciprocal here is 65535/(255 * 7) is about 36.714, so this is not terrible. In 4-interpolated-color mode for BC4, we get:

// BC4; a, b are 8-bit, 4-interp mode ae = expand_to_16(a); be = expand_to_16(b); diff = b - a; // b, a not be, ae! col0 = ae; col1 = be; col2 = ae + 48*(diff); // 1/5 col3 = ae + 48*(diff<<1); // 2/5 col4 = be - 48*(diff<<1); // 3/5 col5 = be - 48*(diff); // 4/5

48 = 32 + 16 is again just 2 set bits, the factor to approximate is 65535/(255*5) = 51.4, so that one’s somewhat dubious, but oh well, it is what it is.

BC5 is just two of those. Finally, for BC3 alpha, we get variation of the BC4 unsigned formulas, but this time we want a 8-bit result not a 16-bit result, so the mystery shift along with the rounding bias is back. Let `scale_and_round(k,d) = ((k*d + (d >> 3) + 128) >> 8)`

, then

// BC3 alpha; a, b are 8-bit, 6-interp mode diff = b - a; col0 = a; col1 = b; col2 = a + scale_and_round(36, diff); col3 = a + scale_and_round(36, diff*2); col4 = b + scale_and_round(36, -diff*4); col5 = a + scale_and_round(36, diff*4); col6 = b + scale_and_round(36, -diff*2); col7 = b + scale_and_round(36, -diff);

and finally:

// BC3 alpha; a, b are 8-bit, 4-interp mode diff = b - a; col0 = a; col1 = b; col2 = a + scale_and_round(48, diff); col3 = a + scale_and_round(48, diff*2); col4 = b + scale_and_round(48, -diff*2); col5 = b + scale_and_round(48, -diff);

And that, at long last, is it.

### Conclusions

If you got here, you have no-one to blame but yourself. If you’re one of the handful of people actively working on BCn encoders (hi!), this is probably actionable information to you. If you read this far out of curiosity or because you want to know exactly what you’re getting on the various GPUs, hopefully now you know. And in the not unlikely scenario that you are someone from the future with a question about weird BCn decoding behavior that I referred to this post, well, hopefully this makes it a bit clearer what’s going on. It’s also hopefully usable if you want a software model of the given three GPU vendors’ decoders without having to juggle multiple machines or video cards around all the time.

If you’re an encoder author and not sure what to do about this, one of the main takeaways from this for me was that even though the D3D spec formulation of BC1 decoding explicitly works on 8-bit integer values and divides by 2 or 3 with truncation, and the Khronos spec treats everything as real numbers with unspecified precision, both Intel and AMD actually use the (somewhat nicer) division with round to nearest, and NVidia uses it as well in the green channel, while in the red/blue channels “it’s complicated” (because of the scaling factor folded into the linear interpolation). My older rygdxt (then turned into stb_dxt) used round-to-nearest, Oodle Texture used to default to the D3D spec behavior of truncating, but between AMD and Intel explicitly rounding and NVidia being somewhere in the middle, the next Oodle Texture release (2.9.5) will probably switch to round to nearest.

Also, instead of using the same weights for red, green, and blue, we are currently planning to use 85/256ths as our new approximation to 1/3 (we used to divide by 3 exactly) in the red and blue channels, and 83/256ths in the green channel, in the spirit of making everyone equally unhappy, to land somewhere between Intel’s choice of 85/256ths, AMDs of 21/64ths = 84/256ths, and NVidias sort-of 80.25/256th’s. It was chosen as a convenient dyadic fraction with not too many significant digits that had OK error estimates over the relevant range for all three vendors; somewhat higher for NV than for AMD or Intel, but they chose this crappy approximation themselves, so that’s on them. (For the halfway point, we use 1/2 with round to nearest, same as AMD and Intel.)

The main reason for this change is that Oodle Texture used to solely encode for the a D3D reference decoder that does not actually ship anywhere; we worked to stay within the relevant tolerances (the 3% relative error etc.) to avoid truly nasty surprises, but at the end of the day nobody ships against the D3D reference rasterizer, they ship on actual GPUs. The new approximate decoder model is not particularly complicated (the main weirdness is the different weights for G and R/B) and targeting it made the errors as computed with the accurate hardware models go down across the board, even though the error as measured against the D3D reference increased (it would have to, seeing as that was the sole metric we used to target before). As of this writing we haven’t done anything about BC3 alpha or BC4/5 yet, but we might change our reference/target decoder for that as well in the foreseeable future.

All three decoders are well within the error bounds required by the D3D spec (and Khronos doesn’t have any particular requirements to begin with). In an ideal world, we’d just pick one of these options (doesn’t matter which) and standardize on it; we have standardized the behavior of pretty much all other numbers formats that GPUs work with and that’s been good for everyone. It wouldn’t do much good for any new software for a while, as long as the multiple HW variants are around, but I don’t see texture memory bandwidth concerns or the BCn formats going away any time soon, the more complex BC6-7 and ASTC already nail down their respective decoder behavior, and it sure would be nice to put the current mess behind us *eventually*, even if it’s another 10 years from now.

Finally, the formulas and explanations given here are collated from data collected over several runs and experiments conducted over a period of one and a half years or so; I tried to unify the presentation somewhat for this blog post but I probably introduced mistakes along the way. If you find any problems, it’s probably a bug. Ping me and I’ll try to fix it.

Many thanks to Sean Barrett who did a lot of the legwork to figure out the last few details of Intels and AMDs BC4/5 decoders, Tom Forsyth who crucially told us that yes indeed the Intel decoders for BC4/5 used full 16-bit weights (something I dismissed as implausible for a good long while), and Ignacio Castaño for his 2009 write-up on the NVidia BCn decoders.

Great post! It’s awesome to have a reference for this.

I tried to reproduce your experiments on the Apple M1. It looks like Apple matches AMD for all BC1 values, all BC3 alpha values, all but the 13 incorrectly rounded BC4 UNorm values (which are rounded correctly), and all BC4 SNorm values that don’t use -128. For BC4 SNorm, they don’t convert -128 to -127, and instead treat values less than -127*64 as -127*64 at the division. (Amusingly, this means that a value Intel and AMD decode as 1.0 can be decoded as -1.0 by Apple.)

Great, that’s good to know!

I’m assuming your pathological example relies on the special case where endpoint 0 is -127, and endpoint 1 is -128? For everyone else wondering, the two compare as equal when the -128 |-> 127 remapping happens first, which selects the mode with 4 interpolated colors and -1/+1 constants at indices 6 and 7, respectively. If the compare is done on the un-remapped integers, e0 > e1, which selects the 6-interpolated color mode, and all palette entries end up mapping to -1. So by emitting a block with e0=-127, e1=-128, and all indices 7, you can emit a block that is all -1 on some hardware and all +1 on other hardware.

The D3D11 functional spec code requires that the order be remap before compare. The Khronos data format spec has a special caveat in section 19.2 (https://www.khronos.org/registry/DataFormat/specs/1.3/dataformat.1.3.html#_bc4_signed, last paragraph of section) that notes that this combination of endpoint values is to be considered undefined. If you’re writing an encoder, this is not a problem: -128 being a redundant encoding for -127 is not particularly useful (it doesn’t give you anything that can’t be coded differently already) and is prone to weird edge cases like this, so it’s best to just avoid it entirely. That’s what we do in Oodle Texture, anyway.

Yep, that’s the one! In all other cases the errors are small, and, as you said, easily avoided by not using the redundant -128 encoding.

The choices of the different vendors (with Nvidia riding the line of what’s allowable by spec, Intel using tons of precision, and AMD somewhere in the middle) matches up with what we found in PCSX2 with the handling of shader output into blending.

In PCSX2, we attempted to emulate the PS2’s blend hardware (which rounds down) using PC blending (which rounds nearest) by configuring the hardware blend to do src + dst * (1-alpha), and then doing src * alpha – 0.5/255 in the shader to offset the value so it would round down. Turns out GPUs do not in fact want to send a full 4×32-bit float to the ROP if they don’t have to (and no matter what offset I tried, it didn’t seem to help on Nvidia GPUs), so to decide on what constant to actually subtract, I ended up doing a survey of how much precision each GPU had when sending shader output to blend into an RGBA8Unorm texture.

The result: Intel preserves ~14 bits of precision (error was between -5.7e-5 and 8.5e-5). AMD quantizes to half (it happens in the shader so you can see it in a disassembly), so 11 bits of precision near one, increasing as you get closer to zero. Nvidia goes straight to 8 bit unorm before any blending happens (the minimum allowable by spec), which is why we weren’t able to get anything fun out of it.