---
title: 'Entropy coding in Oodle Data: the big picture'
url: https://fgiesen.wordpress.com/2021/07/09/entropy-coding-in-oodle-data-the-big-picture/
published: '2021-07-09'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Entropy coding in Oodle Data: the big picture

April 26, 2016 was the release date of Oodle 2.1.5 which introduced Kraken, so it celebrated its 5-year anniversary recently. A few months later we launched Selkie and Mermaid, which wetre already deep in development at the time of the Kraken release but not quite finished yet, and in early 2018 we added Leviathan, adding a higher-compression option to our current suite of codecs, the “sea beastiary”.

In those 5 years, these codecs have seen wide adoption in their intended market (which is video games).

There’s a few interesting things to talk about, and the 5-year anniversary seems as good a reason as any to get started; this is the first in what will be a series of yet to be determined length, in which I’ll do a deep-dive on one interesting aspect of these codecs, namely the way they handle entropy coding.

Before I can get into any details, first some general notes on how things fit together. Kraken, Mermaid, Selkie, and Leviathan are lossless data compression algorithms, all variations on the basic LZ77 + entropy coding formula that has been the de facto standard in general-purpose compressors since the late 80s, because such codecs can achieve a good balance of compression ratio and compression/decompression speed for practical applications. Other codecs belonging to this family include Deflate (ZIP/gzip), LZX (Amiga LZX/CAB), LZMA (7zip/xz), Zstd, Brotli, LZHAM, and many others, including most of the older Oodle Data codecs (Oodle LZH/LZHLW, LZA, LZNA, and BitKnit).

The “LZ77” portion here refers to the LZ77 algorithm, which, broadly speaking, compresses data by replacing repeated byte sequences in a stream with references to prior occurrences; as long as the back-reference is smaller than the bytes themselves, this will result in compression. Nobody actually uses the original LZ77 algorithm per se (which has a very inefficient encoding by today’s standards), but the general idea remains the same. Some codecs, especially ones designed for faster decoding or encoding, use just this byte/string matching approach without any entropy decoding; this includes many well-known faster codecs such as LZ4, Snappy, LZO, and again many others, including the remaining older Oodle Data

codecs (Oodle LZB/LZBLW and LZNib).

I won’t talk about the LZ77 portion here (that’s its whole own thing), and instead focus on the “entropy coding” portion of things. In essence, what all these codecs do is identify repeated strings, resulting in some mixture of back-references (“matches”) and bytes that couldn’t be profitably matched to anything earlier in the data stream (“literals”). All the codecs mentioned differ in how exactly these things are encoded, but all of them eventually boil it down to one

or more data streams that each have symbols from a finite-size and not too large alphabet (typical sizes include a few dozen to a few hundred distinct symbols in the alphabet), plus maybe a few extra streams that contain raw bits for data that is essentially random.

Entropy coding, then, processes these streams of symbols from a finite alphabet and tries to turn them into an equivalent form that is smaller. There are numerous ways to do this; one well-known method, and indeed a mainstay in data compression to this day (with some caveats), is Huffman coding, which counts how often individual symbols occur and assigns short bit codes to more likely symbols and longer symbols to less likely symbols, in a way that remains unambiguous and uniquely decodable.[1](https://fgiesen.wordpress.com#fn1)

The second major class of techniques is arithmetic coding, which compresses slightly better than Huffman for typical data and can give significant improvements on either small alphabets or highly skewed distributions, and is also more suitable for applications when there is not an a priori known fixed symbol distribution, but rather an on-line model that is being updated as new data is seen (“adaptive coding”).

Finally, the new kid on the block is the ANS (“Asymmetric Numeral System”) family of methods, which is conceptually related to arithmetic coding but works differently, and has different trade-offs. Kraken and Mermaid use ANS sometimes and Leviathan frequently; I’m sure I’ll cover its usage in those codecs at some point, and for now there are plenty of my older writings on the topic from around 2014-2016.

Anyway, it is common for LZ77-derived algorithms with a Huffman or arithmetic coding backend to use odd alphabet sizes; when you’re assigning variable-length codes to everything anyway, it doesn’t really matter whether your alphabet has just 256 distinct byte values in it, or if the limit is 290 or 400 or something else non-power-of-2. It’s likewise common to interleave all kinds of data into a single contiguous bitstream. The sea beastiary family does things a bit differently than most codecs.

Namely, the input (uncompressed) data is processed in 128KiB chunks, which all have self-contained bytestreams with an explicitly signaled size. 2 These chunk bytestreams are themselves made up out of multiple independent bitstreams for different types of data, and most of these streams (except for a few “misc”/leftover data streams) use a single shared entropy coding layer to handle what we now call “primary streams”.


[3](https://fgiesen.wordpress.com#fn3)This layer works on streams that always use a byte alphabet, i.e. unsigned values between 0 and 255. That means that everything that goes through this layer needs to be presented in a byte-packed format. This kind of restriction is common in fast byte-aligned LZ77 coders without a final entropy coding stage (like LZ4 or Snappy), but atypical outside of that space.

Working in bytes needs some care to be taken in other parts of the codec design, but comes with a massive advantage, because it allows us to have an uncompressed mode that just stores streams as uncompressed bytestreams and doesn’t need any decoding at all. That means that streams that are nearly random, or just short, don’t have to waste CPU time on setting up a more complicated decoder and then decoding bytes individually through a more complicated algorithm when just grabbing uncompressed bytes straight from the bytestream is good enough.

In short, for most codecs, the choice of entropy coding scheme is a design-time decision. Algorithms like Deflate which uses LZ+Huffman *always* perform Huffman coding, even when doing so isn’t actually worthwhile, because they use extended alphabets with more than 256 symbols in them that mean pass-through coding would still need to use larger-than-8-bit units, both introducing extra waste and making it more expensive in terms of CPU time. Sticking with a byte alphabet means that the Oodle sea beastiary codecs can either use a conventional entropy coding stage or choose to send data uncompressed and act like a faster byte-aligned LZ codec. In fact, that is exactly how Selkie works: under the hood, Selkie is the same codec as Mermaid, but with all streams in uncompressed mode at all times (and some other features disabled).

The final big departure from most codecs is that the sea beastiary codecs run all entropy decoding as separate passes that consume an input bytestream with a common header and output an array of bytes. Uncompressed streams can skip the decoding step and consume data straight from the input bytestream. These passes just handle whatever entropy coding scheme is used and nothing else. This means that instead of the choice of entropy coders being fundamentally built into the algorithm, it’s a collection of small loops that can easily be interchanged or added to, and indeed that’s what we’ve been doing; the original version of Kraken shipped in Oodle 2.1.5 with a choice between just uncompressed streams and one particular version of Huffman coding. We’ve added several more options since then, including an alternative Huffman coding variant, an optional RLE pre-pass, TANS, and the ability to mix-and-match all of these within a single stream, all without it being a big redesign, and we’re quite happy with the results.

There’s many interesting things in here that I plan to cover in small installments, starting with the way we do Huffman (de)coding, which is worth several posts on its own. I’ll try to keep updating this at a reasonable cadence, but no promises since my blogging time is pretty limited these days!

### Footnotes

[1] Huffman coding technically refers to such variable-length

coding (meaning not all symbols need to be coded with the same number of bits) only when the code in question is actually generated via Huffman’s algorithm (which minimizes the length of the coded stream given a certain number of assumptions), but in practice most implementations don’t actually use Huffman’s original algorithm which can assign awkwardly long code lengths to rare symbols. Instead the maximum code length is usually capped, which is a different problem and yields codes that are not actually Huffman codes (and are very slightly less efficient), but just general variable-length codes. Having said that, approximately everyone calls it Huffman coding even when the codes are length-limited anyway, and I won’t sweat it either in the following.

[2] The chunks being independent is how we implement what is called “thread-phased” decoding. As is explained further down in the article, Oodle decodes the bitstreams to temporary memory buffers in a first phase, and the chunks can be processed completely independently for this part of the process, making it a prime candidate to move off to a separate thread (or threads). After phase 1 completes, the actual LZ decoding takes place in “phase 2”; this portion can make references to any bytes earlier in the stream, so it must be run in order and can’t as easily be threaded. Customers that want wider parallelism (or easy seeking) usually chop data into fixed-size blocks, typically between 64KiB and 512KiB, that are encoded independently with no back-references permitted across block boundaries. This decreases compression ratio but makes it trivial to have many workers decoding different blocks at the same time.

[3] In the original code, these streams of bytes are, very non-distinctly, just called “arrays”. When specifying the bitstream more formally, a lot of things suddenly needed proper names to avoid confusion, and “arrays” was just too indistinct and overloaded, so “primary streams” was what we settled on. Sometimes additional data streams exist within a chunk for information not contained in the primary streams, and these are therefore called “secondary streams”.

Small typo here I think s/to/do “In essence, what all these codecs to is identify repeated…”

Thanks, fixed!