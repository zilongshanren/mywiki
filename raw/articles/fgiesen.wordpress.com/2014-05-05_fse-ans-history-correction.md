---
title: FSE/ANS history correction
url: https://fgiesen.wordpress.com/2014/05/05/fseans-history-correction/
published: '2014-05-05'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# FSE/ANS history correction

I’ve been meaning to write another proper post on this for a while, but the last few months have been very busy and I didn’t feel like writing in my spare time.

This is not that post, sadly. This is about something else: namely, me only citing Jarek Duda’s work on ANS and not [Yann Collet](http://fastcompression.blogspot.com/)‘s work on FSE. Apparently, there were multiple versions of Jarek’s ANS paper, and the second version (which contains rANS, the topic I’ve been writing about) was significantly influenced by Yann’s experiences with integrating ideas from the first version into FSE.

Anyway, I did not mention Yann’s work in my rANS posts at all. I just want to make clear that this was because I was writing about rANS not tANS (the family that FSE is a member of), and I simply wasn’t aware that Yann’s work and input significantly influenced the second version of the ANS paper. My apologies; this was a simple oversight, not a deliberate attempt to talk down Yann’s contribution!

On a separate but related note: Mid-february, I wrote a short [paper](http://arxiv.org/abs/1402.3392) on how entropy coders (with a focus on ANS) can be interleaved on the encode side to allow the decoder side to exploit instruction-level parallelism and/or SIMD instructions. I originally meant to do a separate post about it here, but on trying to write it discovered that I didn’t have much to say on the topic that wasn’t in the paper. Hence, no separate blog post. But I figured I should at least link to it once from here.

Anyway, more regular blog updates should start again soon. Until then!

Thanks for clarification Fabian.

For the sake of accuracy :

Although it’s correct to say that FSE was instrumental in renewing Jarek’s interest into his own ANS theory, resulting in his publication of updated ANS papers (http://arxiv.org/abs/1311.2540, especially version v2 of January 6th where rANS and tANS names are created (they did not exist when FSE was first published)),

rANS is nonetheless rightfully Jarek’s invention.

I believe it’s the consequence of a discussion we had late December on limiting the memory impact of decoding tables, since it was identified as a remaining advantage for Huffman :

http://encode.ru/threads/1845-Finite-State-Entropy?p=35975&viewfull=1#post35975

My “high level” perspective on his algorithm is that it’s a clever generalization of Matt’s Mahoney work on ABS (the binary version) : http://mattmahoney.net/dc/dce.html#Section_33

The rest we know about : that’s the version you focused on, and proved to work way better than anticipated.

As most algorithms you work on, by the way…

Regarding your paper on interleaved encoding, I have to acknowledge its usage within FSE. It translates into an almost 2x speed improvement, which is very significant (albeit, mostly on 64-bits variants, probably due to register scarcity on 32-bits x86).

Your paper arrived at the best possible moment : I was then experiencing with merging different data sources into a single FSE stream (namely match length, run length, offset, last-bits, etc.). I was therefore experiencing the speed-up effect, but without properly understanding it.

I was in a kind of “meh” state, when you published on arxiv. Your paper provided the perfect background to explain why all this works. It allowed the (relatively fast) publication of an updated, cleaner code, without any more feeling of having missed something.

I have no idea if this is just convergent simultaneous ideas, but I proposed an interleaved encoder for arithmetic coding (before becoming aware of the excellent properties of rANS) in January, along with a practical example and benchmarks.

http://encode.ru/threads/1867-Unrolling-arithmetic-coding

It’s not quite the same as for ANS though as ANS optimally handles interleaving within the same bit stream, which is a wonderful property. My interleaving of arithmetic coders is simply to distribute the incoming data to separate and distinct codecs so that they can be interleaved, but each writing to their own block of memory instead of the same one. This is clearly one place where ANS wins out.

PS. I am indebted to Eugene Shelwien for the original AC implementation I based my unrolled code around. Cheers for everyone. :-)