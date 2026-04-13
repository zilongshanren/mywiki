---
title: DXT Compression, Codebooks and Sliding Windows
url: https://www.jonolick.com/home/dxt-compression-codebooks-and-sliding-windows
published: '2013-02-07'
source_blog: Jon Olick - Home
source_site: https://www.jonolick.com/home
category: graphics
fetched: '2026-04-13'
---

|
Today I've been researching various DXT compression algorithms that attempt to reduce the on disk footprint of DXT textures. I have a loose requirement though that it has to be lossless. The reason is we already have blocking artifacts due to DXT and I don't want to make them worse. The exception of course is if it really is absolutely not noticeable, even to an artist. What I'm currently doing is 3 different methods. 1) LZMA of the raw DXT data. 2) LZMA of the transpose of the raw DXT data. (this groups the endpoints and other pieces together). 3) LZMA of the golomb encoded, PNG like DPCM encoded color lines and raw selector bits. The results are that 2 is the winner most of the time, with 1 coming out ahead with trivial textures and 3 picking up the slack when the textures just happen have data that this compresses well. All these techniques are not new and can be found in other places for more information. I came across
A good overview of the general principles behind the technique are located
Also, a great presentation linked from there is located here and also explains a similar approach to crunch.
While I haven't yet disected crunch's code, he talks about Zeng codebook optimization. I have put up a local copy of the PDF here. This is supposedly a well known technique in the compression world so I won't go into too much detail about how it works. Essentially from a high level it re-orders the palette entries to reduce the delta of palette entries between neighboring pixels. Followed with delta-compression and zip (or golomb coding which should be optimal) this can be a powerful way to reduce data sizes.
Jumping to the video presentation he talked about a particular problem with codebooks where you can always use 8bit indices by using a sliding 256 element window of the codebook. Presumably this means that anytime you specify the 256th element, the codebook window is slid to the left and the bottom element is dropped. This means that your codebook is bigger than it should be with duplicate elements, but if you have more indexes than the size of your codebook, its probably a win. One other way to do a similar technique is anytime the 256th palette entry is specified you also need to specify an additional byte which specifies the position in the codebook window to insert at. This has two possible benefits. 1) You may be able to organize your codebook to achieve better compression (Zeng like) 2) The lifetime of a particular codebook entry is defined somewhat by its position it is inserted at. If you are willing to give up 2 entries to the code book you can combine the original approach and the new one. Entry 255 means put at the end, Entry 256 means put at spot X. So, in effect, it allows for a non-greedy, and possibly much better, optimization. For example, this means that you can control the lifetime of various entries to minimize the entire size of the codebook and also do tradeoffs to increase the compressibility of the indexes. Like all things, I'm sure this has been done before. ;) I started at ~3bpp, lets see where this goes.
|
## Archives
## Categories |