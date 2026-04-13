---
title: Oodle, Kraken etc. misconceptions
url: https://fgiesen.wordpress.com/2024/08/08/oodle-kraken-etc-misconceptions/
published: '2024-08-08'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Oodle, Kraken etc. misconceptions

Hi. I’m Fabian “ryg” Giesen, one of the co-authors of Oodle, originally made and sold by RAD Game Tools, now (after an acquisition in late 2020) officially Epic Games Tools as per the business license. Everyone (even at Epic) still mostly refers to us as RAD though; it’s been a long-standing name and nobody sees much point in a rebranding campaign. There’s several misconceptions about Oodle etc. floating around. There’s a lot more technical details on the[ RAD home page](https://www.radgametools.com/) and in the docs (if you’re a licensee) but this is a shorter version that tries to give the executive summary of what is what in a few paragraphs each.

### What is Oodle?

Oodle is a suite of data compression-related libraries, with three main ones: Oodle Data, which does lossless data compression – think ZIP/Deflate, 7zip/LZMA, Zstd, LZ4, that kind of thing. It was originally designed for storing game assets on disk, but it’s lossless and can be used for whatever data you want. The algorithms in Oodle Data generally emphasize fast decompression. For example, Kraken decodes around 4x faster than Deflate/ZIP for typical data.

Then there’s Oodle Network, which focuses especially on UDP network packets. These are often much smaller (frequently around 100 bytes or less). Oodle Network is also lossless, but is optimized for small, independent amounts of data. It’s slower to decode but has essentially no per-packet overhead.

Finally, we have Oodle Texture, which takes images and encodes them to the “BCn” family of GPU compressed texture formats. Oodle Texture provides high-quality compressors for these formats and supports RDO (Rate-Distortion Optimization), which encodes textures in a different way that takes the same amount of space in GPU memory but will be much smaller on disk after applying a standard lossless compressor like Deflate, Zstd or, of course, Oodle Data.

### Kraken

Oodle Kraken, or just Kraken when the context is clear, is one of the algorithms supported by Oodle Data. It’s a good jack-of-all-trades that usually offers much better compression than say Deflate/ZIP and slightly better compression than Zstd, while also being very fast to decode.

Kraken (in our usual software implementation as part of Oodle Data) turned out to be quite popular among PlayStation 4 games and as a result was licensed by Sony for use in the PlayStation 5, which implements a decoder in hardware, making Kraken decompression on PS5 essentially “free”. This decoder was developed by Sony and AMD.

Sometimes, PS5 game package sizes are compared with the sizes of the corresponding game packages on PS4. While Kraken is likely part of any observed size differences, the typical difference between Kraken and a much older format like Deflate/ZIP is around 10-15% or so. In the lossless compression world, even a one-percentage-point difference is considered a big deal, but we’re not talking huge differences here. Some PS4 games are much smaller on PS5, and although the details depend on the individual game, in general, when that happens, it’s almost certainly not primarily due to Kraken. PS4 games are designed to load from a fairly slow hard drive and often duplicate data on disk multiple times to avoid long seek times. PS5 game packages, on the other hand, are always stored on a SSD where seeks are not a major concern. The PS5 packaging tools automatically find and eliminate large duplicated chunks of data, so when PS5 versions of PS4 games are much smaller, this is likely to be single biggest contributor. All credit here is due to the people at Sony who design and maintain these packaging tools.

### Mermaid, Selkie, Leviathan

Oodle Data provides algorithms other than Kraken. Mermaid is faster to decode than Kraken but provides lower compression. Selkie is even faster and even lower compression. In the other direction, Leviathan takes longer to decode than Kraken but provides higher compression.

All of these algorithms provide different trade-offs. Game developers can and do choose between them based on their CPU and disk space budget. The latter is often still subject to certain “magic numbers” for games that get physical releases on Blu-Ray discs or similar, where say a 99GB game fits on a 100GB Blu-Ray disc while a 105GB game does not. So even though we’re usually talking about differences of a few percentage points here, sometimes those few percent really do make a big difference.

### Oodle Texture

Oodle Texture is, first and foremost, an encoder for BC1-BC7 format textures (collectively referred to as BCn). These texture formats are always lossy. BCn textures are designed for random access on the GPU and chop up images into small, fixed-size blocks. BCn textures are already compressed, but usually get stored on disk with an extra layer of lossless compression applied. Intuitively, think of it like this: because BCn blocks are fixed-size, “easy” regions of an image are sent with more bits than they need, which is the price we pay for fast random access. We’re OK with this once textures are in memory, but on disk it’s just a pointless waste of space, and the extra layer of compression fixes it.

Oodle Texture aims to provide very high-quality encoding while still being relatively fast (to keep artist iteration times manageable). Its main feature is RDO. Oodle Texture RDO makes the BCn encoder aware of that second layer of compression happening, and explicitly tries to make the “easy” blocks more compressible. This does introduce some extra error but can reduce on-disk and download sizes of textures considerably, often by more than 2x in shipping games. It does not make a difference either way in VRAM usage, since the data in VRAM is in the fixed-bit-rate BCn formats.

Oodle Texture RDO results are still just regular BCn textures – they just happen to compress much better when passed into most lossless compressors. There are no extra decode steps required at runtime.

We try quite hard to provide really good BCn encoders. The goal is that at typical settings, Oodle Texture RDO results have similar error to most other (non-RDO) encoders. BCn are lossy formats, so some amount of error is in general unavoidable. But our goal is to provide the same level of fidelity that you’d get without Oodle Texture, just with smaller disk and download footprint.