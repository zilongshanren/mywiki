---
title: 'Modern Data Compression in 2021 Part 2 : The Battle to Dethrone JPEG with
  JPEG-XL, AVIF, and WEBP'
url: https://chipsandcheese.com/p/modern-data-compression-in-2021-part-2-the-battle-to-dethrone-jpeg-with-jpeg-xl-avif-and-webp
author: BlueSwordM
published: '2021-02-28'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Modern Data Compression in 2021 Part 2 : The Battle to Dethrone JPEG with JPEG-XL, AVIF, and WEBP

This is the 2nd article of a multi-part series, with the focus starting on image compression. I would heavily recommend reading the 1st article as it explores a part of the history of image compression, which leads to talking quite a bit about the basis of the JPG image codec: [https://chipsandcheese.com/2021/01/30/modern-data-compression-in-2021-part-1-a-simple-overview-on-the-art-of-image-encoding/](https://chipsandcheese.com/2021/01/30/modern-data-compression-in-2021-part-1-a-simple-overview-on-the-art-of-image-encoding/)

Essentially, most modern image codecs work with a lot of the techniques that were first worked on with JPG itself, and were then expanded upon or taken in a different direction altogether by using similar, but different sets of tools to achieve better results.

## Succeeding the beast that is JPEG

As mentioned in the previous article, some of these efforts ended up creating codecs like JPEG2000 (the currently most used niche JPEG evolution), JPEG XT, JPEG XS, and JPEG XR (created and used by Microsoft for HDR images in Windows). None of these standards managed to either dethrone JPEG on most use cases or even achieve remotely close to its success due to patent issues, little benefit over using 3rd party JPG encoders, or being too niche for their own right. That is why you mostly see them used in proprietary systems. There wasn’t really a superior solution to all of their individual use cases… until recently: **that is the basis of JPEG-XL.**

## JPEG-XL: An evolutionary step towards revolution

JPEG-XL is a new standard built on the shoulders of JPEG to attain even further heights in terms of image compression technology.

Essentially, it takes most of the technologies found in JPG, and *cranks up everything to 11*.

It preserves 8×8 DCT processing, progressive decoding (instead of loading the image sequentially, it shows a lower quality image until the rest of the data is downloaded), full YUV 4:4:4 chroma sampling with optional chroma subsampling, and it can even represent JPEG data losslessly, meaning you don’t get any generational losses from transcoding, and allows for lossless recompression from JPEG to JPEG-XL, which is a very impressive feature in itself.

We then come to the main features added to JPEG-XL:

Instead of using the static 8×8 DCT blocks used for processing, it introduces variable DCT (VARDCT) block sizes, from 4×4 to 256×256

Better progressive image support with the option of creating multiple progressive images

It uses the better perceptually oriented XYB color space

It features powerful adaptive quantization, very high bit depth support, expressing values of up to 32-bit floats

Multi-frame layering, allowing for multiple layers such as depth maps or even heat maps

Powerful lossless encoding

Animation support to finally replace the aging GIF

Very fast parallel encoding/decoding (faster than even libjpeg-turbo on multi-core CPUs, the current fastest JPEG implementation)


It is also fast to encode and very fast to decode (faster than libjpeg-turbo on multi-core CPUs, the fastest current JPEG implementation). Overall, a very promising format that has had a lot of work put into it. There will be a much more detailed article about JPEG-XL, since the format is much more complex than it seems with its multiple operating modes and features, which makes it rather difficult to talk about in a detailed manner without bloating the article.

## A small story on WebP

On the other side of the fence, you have image formats derived from video codecs. One of the more popular codecs in this regard is WebP: the lossy part of WebP is based on VP8, and it is decently fast and efficient. However, the benefit over JPG is rather small in the lossy department, and in many cases against better 3rd encoders(like mozjpg), there’s no improvement, or even a slight quality degradation in rare cases. The lossless/near-lossless WebP has been developed as an image codec first and foremost though, and consistently beats PNG compression in this regard. Adoption has been very slow as format however, since until very recently, not many browsers/devices or applications supported the format natively, so the classical combo of JPEG/PNG had stayed relatively unharmed. However, the developers of WebP have currently been working on a new format to succeed it, WebP2. It is currently in early development, and the format has not been finalized, so it will not be discussed in much detail in this article.

## The mix of videos and images: AV1 to AVIF

A more recent development on the basis of video codecs is AVIF (AV1 image format), an image standard based on AV1. AV1 is a royalty-free open video standard backed by multiple large entities and corporations, which all formed the Alliance for Open Media (AOM). Therefore, AVIF is a royalty-free open image codec based on AV1, except it only compresses images without being able to use motion estimation or many of its more fancy video codec techniques when encoding a single image (hence why enthusiasts/developers will often call AVIF and other image formats intra-only, intra indicating a full quality compressed image). It uses many features from the base AV1 specification, like:

High Bit Depth or HBD support (implying 10-12 bit for HDR and wide color-gamut support)

Powerful filtering and directional prediction.

Great low BPP performance (bits per pixel, so the size based on how many bits per pixel are being used)

Great animation support due to its background as a video format(that is where it truly shines, since the encoders can use their vast array of tools to greatly compress videos)

Good image threading possibilities with multiple forms of threading


However, since it is based on AV1, it seem to have the disadvantage of slower encoding and even decoding performance for intra only encoding(full size frames only), but that remains to be compared against to get as a point of reference later in the article. It also has a resolution limit (35 megapixels), which can pose some problems in some scenarios if you need more than that, since you need to introduce purely independent tiles.

Finally, keep in mind that there are multiple AV1 encoders with their own strengths and weaknesses (like rav1e), and that encoders are still progressing.

With all of this in mind, we can see that AVIF and JPEG-XL combined have the best shot at finally dethroning the classic JPEG/PNG combo once and for all in almost all use cases: next generation image coding is finally underway with the frameworks we have in place.

## Visual testing and examples

Of course, new formats may be more efficient according to subjective testing and metrics, but what matters in the end are 4 things: **image quality, threading, efficiency, and speed**.

If you have a very efficient encoder that can create excellent looking images while talking massive amounts of time per image, or if the encoder is very fast and efficient, but removes many important details in the image(makes the image more visually appealing while lowering fidelity) or if the encoder depends on per file threading to achieve acceptable encoding speeds, these outcomes are not very desirable in some sense, so balanced encoder that can be as good as possible in as many scenarios as possible is rather important.

In this section, I will be testing various image formats with various image sources to see what each of their upsides and downsides are.

The encoders used for each format are mentioned below.

*Default flags (except for quality to achieve certain file sizes). Reasonable speed presets will be used, with single-threaded encoding used as a basis unless mentioned otherwise.*

*Quality or Q/q usually indicates targeting a certain quality target, while -d or distance in JPEG-XL indicates trying to target a certain perceptual visual quality.*

*All non JPG images will be decoded to PNG and lossless compressed with ECT to save on size.* *File sizes are around 5% of each other at the maximum and minimum.*

JPG compression with mozjpeg 4.0.2 with these settings: **cjpeg -optimize -maxmemory 1000M -quality xx -dc-scan-opt 2 -outfile “ouptut.jpg” “source.png”**

WebP compression with cwebp 1.2.0 with these settings: **cwebp -m 6 -q XX “source.png” -o “output.webp”**

AVIF compression using the libaom-av1 2.0.2-1286 encoder with avifenc: **avifenc -j 1 –min QX –max QX+5 -s 3 “source.png” “output.avif”**

JPEG-XL compression using the CJXL 0.3.2 encoder: **cjxl “source.png” “output.jxl” -s 7 -d XX –num_threads=1 **or** cjxl “source.png” “output.jxl” -s 7 -q XX** **–num_threads=1**

**Important note: If you click the links, beware that they may consume a lot of bandwidth due to the lossless nature of PNG images. You have been warned.**

Note for some of the game screenshot results(6th and 9th): Getting similar filesizes out of AVIF libaom-av1 was actually rather difficult. Its behavior wasn’t very predictable in terms of file sizes, so this made it rather hard to make the comparison, and took longer to do. I managed to do it in the end, but the results are interesting, specifically for the detail retention in the 9th comparison.

## Discussion of the results

So, with all of the visual samples shown above, certain patterns can be deduced: JPEG-XL and WebP are rather close in terms of speed per thread alongside mozjpg, with JPEG-XL being a bit faster in some images and WebP in others, with AVIF in dead last using the libaom-av1 encoder. The difference in single-threaded speed vs the other encoders is just staggering: even using the modest speed 4 preset(-s 4), the encoder is still an order of magnitude slower than the others(although JPEG-XL could be made even slower still with higher efficiency still with the slower -s 8 and -s 9 presets). That could be improved with higher speeds, better efficiency-speed tuning, and just plain speed increases.

Another interesting thing is that JPEG-XL, outside of its lower speed presets(-s 3 to -s 5, which were not used), is currently not very well multi-threaded. That is why if you encode directly with AVIF libaom-av1, you will see that the speed disparity may not seem that large because it may be fully utilizing your CPU’s full power by default. On the other side, the reference JPEG-XL encoder might be only using 1-2 threads at the end of the encoding process, greatly reducing speed. That could easily be fixed with a software update however.

In terms of general fidelity, JPEG-XL wins, with AVIF trailing behind. WebP is in an interesting spot, and looks about as good as mozjpeg in most scenarios, having different tradeoffs than JPEG due to its roots in VP8 (you can see that in the higher amount of banding and different block artifacts in some of the images). In terms of very low image size performance (low BPP), I will be doing that comparison in the next part, since JPEG-XL and AVIF are rather interesting in this regard due to their different operating modes, while WebP and mozjpeg don’t do very well in that regard.

In terms of decoding speed, JPEG-XL is the fastest with mozjpeg being very close, with WebP trailing behind alongside, and AVIF is last. With the images used, AVIF using dav1d decoding is still very fast, but with larger images, the difference might get larger. All of them are actually rather fast in terms of decompression speed at these image sizes, but using JPEG-XL would be preferred since it supports native progressing decoding, a very important feature for previews and website image loading.

The last 2 images are interesting: they’re just using lossless JPEG-XL compression! It’s literally free compression if you did not manage to keep the originals. Of course, the image could be made even smaller if you actually used the highest quality source possible with the pure lossy JXL mode.

In the end, all of the encoders for the various formats did well, but there are definitely 3 that stick out in order: JPEG-XL, AVIF, and mozjpeg. Mozjpeg is particularly interesting in the fact that even though it is based on a nearly 30 year old format, it is still doing rather well. WebP also does decently well, but it is understandable why it didn’t really catch on. JPEG-XL and AVIF are the definite stars of the show, with JPEG-XL taking the main lead.

Its encoding and decoding speeds are excellent, it supports progressive decoding, and it preserves detail quite a bit better than AVIF using the libaom-av1 encoder at mid-high bpp, and still does a good job at lower fidelity levels. It’s also much more efficient than mozjpeg and WebP at the same quality, or as seen in the article, gets higher quality at the same file size. However, at low bpp, AVIF wins by a nice margin, at the cost of worse and detail retention in exchange for considerably less artifacts(small spoiler for the next article). I guess the directional and loop filtering built into AV1 does better at these very low file sizes, although there is still a lot work being done with JPEG-XL to make it better in this regard, so no winner yet. With all of this mind, I would like to end this 2nd part by saying one thing: JPEG-XL should be used for everything image related, and AV1 should mainly be used for video encoding, and not much in terms of general image encoding(although AVIF could be used for some stuff).

If you have any more questions on the subject, leave them down below.