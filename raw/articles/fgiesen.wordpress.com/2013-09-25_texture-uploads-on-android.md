---
title: Texture uploads on Android
url: https://fgiesen.wordpress.com/2013/09/25/texture-uploads-on-android/
published: '2013-09-25'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Texture uploads on Android

RAD Game Tools, my employer, [recently](http://www.radgametools.com/bnkhist.htm) (version 2.2e) started shipping Bink 2.2 on Android, and we decided it was time to go over the example texture upload code in our SDK and see if there was any changes we should make – the original code was written years ago. So far, the answer seems to be “no”: what we’re doing seems to be about as good as we can expect when sticking to “mainstream” GL ES, reasonably widely-deployed extensions and the parts of Android officially exposed in the NDK. That said, I have done a bunch of performance measurements over the past few days, and they paint an interesting (if somewhat depressing) picture. A lot of people on Twitter seemed to be interested in my initial findings, so I asked my boss if it was okay if I published the “proper” results here and he said yes – hence this post.

### Setting

Okay, here’s what we’re measuring: we’re playing back a 1280×720 29.97fps Bink 2 video – namely, an earlier cut of [this trailer](http://www.youtube.com/watch?v=r9fSkcAYyZ8) that we have a very high-quality master version of (it’s one of our standard test videos); I’m sure the exact version of the video we use is on the Internet somewhere too, but I didn’t find it within the 2 minutes of googling, so here goes. We’re only using the first 700 frames of the video to speed up testing (700 frames is enough to get a decent sample).

Like most popular video codecs, Bink 2 produces output data in planar YUV, with the U/V color planes sub-sampled 2x both horizontally and vertically. These three planes get uploaded as 3 separate textures (which together form a “texture set”): one 1280×720 texture for luminance (Y) and two 640×360 textures for chrominance (Cb/Cr). (Bink and Bink 2 also support encoding an alpha channel, which adds another 1280×720 texture to the set). All three textures use the `GL_LUMINANCE`

pixel format by default, with `GL_UNSIGNED_BYTE`

data; that is, one byte per texel. This data is converted to RGB using a simple fragment shader.

Every frame, we upload new data for all 3 textures in a set using `glTexSubImage2D`

from the internal video frame buffers, uploading the entire image (we could track dirty regions fairly easily, but with slow uploads this increases frame rate variance, which is a bad thing). We then draw a single quad using the 3 textures and our fragment shader. All very straightforward stuff.

Furthermore, we actually keep two texture sets around – everything is double-buffered. You will see why this is a good idea despite the increased memory consumption in a second.

### A wrinkle

One problem with GL ES targets is that the original GL ES went a bit overboard in removing core GL features. One important feature they removed was `GL_UNPACK_ROW_LENGTH`

– this parameter sets the distance between adjacent rows in a client-specified image, counted in pixels. Why would you care about this? Simple: Say you have a 256×256 texture that you want to update from a system memory copy, but you know that you only changed the lower-left 128×128 pixels. By default, `glTexSubImage2D`

with `width = height = 128`

will assume that the rows of the source image are 128 pixels wide and densely packed. Thus, to update just a 128×128 pixel region, you would have to either copy the lower left 128×128 pixels of your system memory texture into a smaller array that is densely packed, or call `glTexSubImage2D`

128 times, uploading a row at a time. Neither of these is very appealing from a performance perspective. But if you have `GL_UNPACK_ROW_LENGTH`

, you can just set it to 256 and upload everything with a single call. Much nicer.

The reason Bink 2 needs this is because we support arbitrary-width videos, but like most video codecs, the actual coding is done in terms of larger units. For example, MPEG 1 through to H.264 all use 16×16-pixel “macroblocks”, and any video that is not a multiple of 16 pixels will get padded out to a multiple-of-16-size internally. Even if you didn’t need the extra data in the codec, you would still want adjacent rows in the plane buffers to be multiples of at least 16 pixels, simply so that every row is 16-byte aligned (an important magic number for a lot of SIMD instruction sets). Bink 2’s equivalent of macroblocks is 32×32 pixels in size, so we internally want rows to be a multiple of 32 pixels wide.

What this all means is that if you decide you really want a 65×65 pixel video, that’s fine, but we’re going to allocate our internal buffers as if it was 96 pixels wide (and 80 pixels tall – we can omit storage for the last 16 rows in the last macroblock). Which is where the unpack row length comes into play – if we have it, we can support “odd-sized” videos efficiently; if we don’t, we have to use the slower fallback, i.e. call `glTexSubImage2D`

for every scan line individually. Luckily, there is the [GL_EXT_unpack_subimage](http://www.khronos.org/registry/gles/extensions/EXT/GL_EXT_unpack_subimage.txt) GL ES extension that adds this feature back in and is available on most recent devices; but for “odd” sizes on older devices, we’re stuck with uploading a row at a time.

That said, none of this affects our test video, since 1280 pixels width is a multiple of 32; I just though I’d mention it anyway since it’s one of random, non-obvious API compatibility issues you run into. Anyway, back to the subject.

### Measuring texture updates

Okay, so here’s what I did: Bink 2 decodes the video on another (or multiple other) threads. Periodically – ideally, 30 times a second – we upload the current frame and draw it to the screen. My test program will never drop any frames; in other words, we may run *slower* than 30fps, but we will always upload and render all 700 frames, and we will never run *faster* than 30fps (well, 29.997fps, but close enough).

Around the texture upload, my test program does this:

// update the GL textures clock_t start = clock(); Update_Bink_textures( &TextureSet, Bink ); clock_t total = clock() - start; upload_stats.record( (float) ( 1000.0 * total / CLOCKS_PER_SEC ) );

where `upload_stats`

is an instance of the [ RunStatistics](https://github.com/rygorous/intel_occlusion_cull/blob/blog_past_the_end/SoftwareOcclusionCulling/SoftwareOcclusionCulling.cpp#L60) class I used in the Optimizing Software Occlusion Culling series. This gives me order statistics, mean and standard deviation for the texture update times, in milliseconds.

I also have several different test variants that I run:

`GL_LUMINANCE`

tests upload the texture data as`GL_LUMINANCE`

as explained above. This is the “normal” path.`GL_RGBA`

tests upload*the same bytes*as a`GL_RGBA`

texture, with all X coordinates (and the texture width) divided by 4. In other words, they transfer the same amount of data (and in fact the same data), just interpreted differently. This was done to check whether RGBA textures enjoy special optimizations in the drivers (spoiler: it seems like they do).`use1x1`

tests force all`glTexSubImage2D`

calls to upload just 1×1 pixels – in other words, this gives us the cost of API overhead, possible synchronization and[texture ghosting](http://withimagination.imgtec.com/index.php/powervr/how-to-improve-your-renderer-on-powervr-based-platforms)while virtually removing any per-pixel costs (such as CPU color space conversion, swizzling, DMA transfers or memory bandwidth).`nodraw`

tests do all of the texture uploading, but then don’t actually draw the quad. This still measures processing time for the texture upload, but since the texture isn’t actually used, no synchronization or ghosting is ever necessary.`uploadall`

uses`glTexImage2D`

instead of`glTexSubImage2D`

to upload the whole texture. In theory, this will guarantee to the driver that all existing texture data is overwritten – so while texture ghosting might still have to allocate memory for a new texture, it won’t have to copy the old contents at least. In practice, it’s not clear if the drivers actually make use of that fact. For obvious reasons, this and`use1x1`

are mutually exclusive, and I only ran this test on the PowerVR device.

### Results

So, without further ado, here’s the results on the 4 devices I tested: (apologies for the tiny font size, but that was the only way to squeeze it into the blog layout)

| Device / GPU | Format | min | 25th | med | 75th | max | avg | sdev |
|---|---|---|---|---|---|---|---|---|
| 2010 Droid X (PowerVR SGX 530) | GL_LUMINANCE | 14.190 | 15.472 | 17.700 | 20.233 | 70.893 | 19.704 | 5.955 |
| GL_RGBA | 11.139 | 13.245 | 14.221 | 14.832 | 28.412 | 14.382 | 1.830 | |
| GL_LUMINANCE use1x1 | 0.061 | 38.269 | 39.398 | 41.077 | 93.750 | 41.905 | 6.517 | |
| GL_RGBA use1x1 | 0.061 | 30.761 | 32.348 | 32.837 | 59.906 | 33.165 | 4.305 | |
| GL_LUMINANCE nodraw | 9.979 | 12.726 | 13.427 | 14.985 | 29.632 | 13.854 | 1.788 | |
| GL_RGBA nodraw | 5.188 | 10.376 | 11.291 | 12.024 | 26.215 | 10.864 | 2.013 | |
| GL_LUMINANCE use1x1 nodraw | 0.030 | 0.061 | 0.061 | 0.092 | 0.733 | 0.086 | 0.058 | |
| GL_RGBA use1x1 nodraw | 0.030 | 0.061 | 0.061 | 0.091 | 0.916 | 0.082 | 0.081 | |
| GL_LUMINANCE uploadall | 13.611 | 15.106 | 17.822 | 19.653 | 73.944 | 19.312 | 6.145 | |
| GL_RGBA uploadall | 7.171 | 12.543 | 13.489 | 14.282 | 34.119 | 13.751 | 1.854 | |
| GL_LUMINANCE uploadall nodraw | 9.491 | 12.756 | 13.702 | 14.862 | 33.966 | 13.994 | 2.176 | |
| GL_RGBA uploadall nodraw | 5.158 | 9.796 | 10.956 | 11.718 | 22.735 | 10.465 | 2.135 | |
| 2012 Nexus 7 (Nvidia Tegra 3) | GL_LUMINANCE | 6.659 | 7.706 | 8.710 | 10.627 | 18.842 | 9.597 | 2.745 |
| GL_RGBA | 3.278 | 3.600 | 4.128 | 4.906 | 9.244 | 4.395 | 1.011 | |
| GL_LUMINANCE use1x1 | 0.298 | 0.361 | 0.421 | 0.567 | 1.843 | 0.468 | 0.151 | |
| GL_RGBA use1x1 | 0.297 | 0.354 | 0.422 | 0.561 | 1.687 | 0.468 | 0.152 | |
| GL_LUMINANCE nodraw | 6.690 | 7.674 | 8.669 | 9.815 | 24.035 | 9.495 | 2.929 | |
| GL_RGBA nodraw | 3.208 | 3.501 | 3.973 | 5.974 | 12.059 | 4.737 | 1.589 | |
| GL_LUMINANCE use1x1 nodraw | 0.295 | 0.360 | 0.413 | 0.676 | 1.569 | 0.520 | 0.204 | |
| GL_RGBA use1x1 nodraw | 0.270 | 0.327 | 0.404 | 0.663 | 1.946 | 0.506 | 0.234 | |
| 2013 Nexus 7 (Qualcomm Adreno 320) | GL_LUMINANCE | 0.732 | 0.976 | 1.190 | 3.907 | 22.249 | 2.383 | 1.879 |
| GL_RGBA | 0.610 | 0.824 | 0.977 | 3.510 | 13.368 | 2.163 | 1.695 | |
| GL_LUMINANCE use1x1 | 0.030 | 0.061 | 0.061 | 0.091 | 3.143 | 0.080 | 0.187 | |
| GL_RGBA use1x1 | 0.030 | 0.061 | 0.091 | 0.092 | 4.303 | 0.104 | 0.248 | |
| GL_LUMINANCE nodraw | 0.793 | 1.098 | 3.570 | 4.425 | 25.760 | 3.001 | 2.076 | |
| GL_RGBA nodraw | 0.732 | 0.916 | 1.038 | 3.937 | 26.370 | 2.416 | 2.190 | |
| GL_LUMINANCE use1x1 nodraw | 0.030 | 0.061 | 0.091 | 0.092 | 4.181 | 0.090 | 0.204 | |
| GL_RGBA use1x1 nodraw | 0.030 | 0.061 | 0.091 | 0.122 | 4.272 | 0.114 | 0.292 | |
| 2012 Nexus 10 (ARM Mali T604) | GL_LUMINANCE | 1.292 | 2.782 | 3.590 | 4.439 | 16.893 | 3.656 | 1.256 |
| GL_RGBA | 1.451 | 2.782 | 3.432 | 4.358 | 8.517 | 3.551 | 0.982 | |
| GL_LUMINANCE use1x1 | 0.193 | 0.284 | 0.369 | 0.670 | 17.598 | 0.862 | 2.230 | |
| GL_RGBA use1x1 | 0.100 | 0.147 | 0.199 | 0.313 | 20.896 | 0.656 | 2.349 | |
| GL_LUMINANCE nodraw | 1.314 | 2.179 | 2.320 | 2.823 | 10.677 | 2.548 | 0.700 | |
| GL_RGBA nodraw | 1.209 | 2.101 | 2.196 | 2.539 | 5.008 | 2.414 | 0.553 | |
| GL_LUMINANCE use1x1 nodraw | 0.190 | 0.294 | 0.365 | 0.601 | 2.113 | 0.456 | 0.228 | |
| GL_RGBA use1x1 nodraw | 0.094 | 0.119 | 0.162 | 0.288 | 2.771 | 0.217 | 0.162 |

Yes, bunch of raw data, no fancy graphs – not this time. Here’s my observations:

`GL_RGBA`

textures are indeed a good deal faster than luminance ones on most devices. However, the ratio is not big enough to make CPU-side color space conversion to RGB (or even just interleaving the planes into an RGBA layout on the CPU side) a win, so there’s not much to do about it.- Variability between devices is huge. Hooray for fragmentation.
- Newer devices tend to have fairly reasonable texture upload times, but there’s still lots of variation.
- Holy crap does the Droid X show badly in this test – it has both really slow upload times
*and*horrible texture ghosting costs, and that despite us already alternating between a pair of texture sets! I hope that’s a problem that’s been fixed in the meantime, but since I don’t have any newer PowerVR devices here to test with, I can’t be sure.

So, to summarize it in one word: Ugh.

If you’re displaying the video in a sufficiently constrained way (overlaying everything else, and with scaling but no rotation), it should be hugely faster to convince SurfaceFlinger to display your images in a new surface and avoid touching OpenGL at all – you can pass the surface a YCbCr_420_SP buffer, and typically the composition hardware will spit it out directly to the display essentially for free.

If you really need to render it with GL, I’d expect creating a YCbCr surface and passing its buffers to eglCreateImageKHR(… EGL_NATIVE_BUFFER_ANDROID, …) etc should also be reasonably fast, since people building Android devices care about the power usage of camera preview which is basically doing that.

I’m not certain how much of this is exposed through the NDK or Java API though. And there will be lots of device-specific performance quirks and bugs. The weakness of the hardware and the lack of quality in the drivers is quite a pain when you try to do anything the device wasn’t explicitly optimised for :-(

In one place you say 29.997 fps when you mean 29.97 fps. It’s probably worth correcting that just to avoid confusing readers.

IIRC the video was actually tagged as 29.997fps not 29.97fps in the header. People mistyping the frame rate as they render out videos happens more often than you’d think. :)

thx for this benchmark !

about extensions, sometimes even GL_EXT_unpack_subimage is not defined, but the device supports it.

exemple GT-I9505 samsung s4 – Adreno (TM) 320