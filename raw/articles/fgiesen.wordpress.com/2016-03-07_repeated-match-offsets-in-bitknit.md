---
title: Repeated match offsets in BitKnit
url: https://fgiesen.wordpress.com/2016/03/07/repeated-match-offsets-in-bitknit/
published: '2016-03-07'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Repeated match offsets in BitKnit

I spent the majority of last year working on LZ77-style codecs. I’ve [written](https://fgiesen.wordpress.com/2016/01/02/end-of-buffer-checks-in-decompressors/) [about](https://fgiesen.wordpress.com/2015/12/21/rans-in-practice/) [some](https://fgiesen.wordpress.com/2015/05/26/models-for-adaptive-arithmetic-coding/) [results](https://fgiesen.wordpress.com/2015/02/20/mixing-discrete-probability-distributions/) before. But there were also several smaller (in scope) but still quite neat discoveries along the way.

One of them has to do with repeated match offsets. BitKnit was originally designed for Granny files, which usually contain 3D meshes, animations, sometimes textures, and can also store other user-defined data. As far as a compressor is concerned, Granny files are highly structured, mostly consisting of a few large, homogeneous arrays of fixed-size records.

### Repeated match offsets

Often, there is significant correlation between adjacent records, for various reasons. What this means in a LZ77-style dictionary compressor is that there will usually be a lot of matches with a match distance (or match offset) that is a small integer multiple of the record size, and matches with the same offset tend to clump together.

The way LZ77 compressors typically exploit this fact is by reserving special codes for “reuse a recent match distance”. To my knowledge, this technique first appeared in [LZX](https://en.wikipedia.org/wiki/LZX_%28algorithm%29), which keeps a 3-element cache of recent match offsets with a LRU eviction policy. The basic idea seems to have spread from there. Many compressors (too many to list) reserve at least a single special, cheaper code to send another match with the same offset as the previous one (corresponding to a 1-element “cache”). This, among other things, gives a cheaper way to code “gap matches” (a match that resumes after being interrupted by a few mismatching bytes) and appears to be beneficial on most types of data.

On text and data that skews towards variable-size records, having extra codes for more repeated match offsets doesn’t help much, if at all (at least, they don’t seem to hurt, either). However, on data heavy on fixed-size records, it is often a big win. LZX, as mentioned before, has 3 “repeat offset slots”. [LZMA](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm) uses 4. Several experiments early in the design of BitKnit indicated that at least for the highly structured Granny files it was designed for, there was a good case to be made for having even more repeat offset slots. We re-evaluated this several times, but a repeat offset count of 8 made it into the final codec; essentially, having a larger number of offset slots allows us to “get away” with an overall less sophisticated offset coder (reducing compression, but improving decoder speed), and is a very solid win on the highly structured data that was the target use case.

### Experiments with lots of repeat match offsets

Two interesting problems arise from making the “repeat offset cache” this large. First, 8 entries is large enough that it’s worth thinking about different algorithmic variants. Second, at that size, it makes sense to investigate different eviction policies as well as other strategies such as maybe “pinning” a few match distances that we expect to be useful (for example, multiples of the record size in front of homogeneous sections).

Second part first: the effect of either “preloading” or pinning useful match distances was either “in the noise” (almost any change to a LZ encoder using adaptive models will make some files larger and others smaller simply due to getting a slightly different parse) or strictly worse in all our tests. Considering how much interface complications this implies (the pre-loaded offsets for different sections need to get to the compressor somehow, and they either need to be known in the decoder from other sources or stored in the compression stream, reducing the gains even further) that makes the idea fairly uninteresting. Empirically, at least in our tests, LZ compressors find useful match distances quickly, and once they’re in the cache, they tend to stick around. Since such a cache is naturally adaptive to the data (whereas static pinned offsets are not), keeping them fully dynamic seems like a good idea.

The next test was to decouple the eviction policy from offset modeling. LZX, LZMA etc. always keep their list of recent match offsets in MRU order: slot 0 is the most recently used offset, slot 1 is the second-most recent, and so forth. One experiment we tried with a very early version of BitKnit was a variant I dubbed “stable index MRU”: offsets are still evicted on a LRU basis, but instead of shuffling the indices around on every match so that the new most recent match gets offset 0, new offsets would get inserted into the least recently referenced slot without moving the slot IDs around.

This affects the modeling; before, you have a very skewed distribution: slot 0 (most recent) is much more important than slot 1, which is more important than slot 2, and so forth. After, they are more spread out; but the idea was that in highly structured files where the same few offsets stick around for a fairly long time, you might capture more useful correlations by keeping these offsets in a single spot (which the entropy coder then tried to capitalize on).

Here were the results on a few granny files, listing the compressed sizes in bytes, with “anchor” being a x86 executable file that doesn’t have a significant amount of record-structured data in it, as a baseline. “MTF” refers to move-to-front index update policy, “stable” is the stable-index variant just described.

| Configuration | granny1 | granny2 | granny3 | anchor |
|---|---|---|---|---|
| 4 offsets, MTF | 18561994 | 22127519 | 15156085 | 1300427 |
| 4 offsets, stable | 18533728 | 22261691 | 15177584 | 1300980 |
| 8 offsets, MTF | 17825495 | 21746140 | 14800616 | 1300534 |
| 8 offsets, stable | 17580201 | 21777192 | 14819439 | 1304406 |
| 12 offsets, MTF | 17619775 | 21640749 | 14677706 | 1301007 |
| 12 offsets, stable | 17415560 | 21448142 | 14681142 | 1306434 |
| 16 offsets, MTF | 17554769 | 21523058 | 14600474 | 1300984 |
| 16 offsets, stable | 17341154 | 21462241 | 14669793 | 1308508 |

First off, as you can see from these experiments, going from 4 to 8 repeat match offsets really does help significantly on these files; an extra 1.5%-4% reduction in file size may not sound like much, but it’s a fairly big deal in compression terms. The experiments with even more repeat offsets were mainly to get a feel for when we start to hit diminishing returns; also, as you can see, the compressed size for the “anchor” file (which is not record-structured) doesn’t seem to care much about the difference between 4 and 8 repeat offset slots, and gets worse after.

As for stable-index coding, well, it’s a mixed bag. It does help on some files, and on the files that do seem to improve from it, it’s a bigger win when using more offset slots, but on e.g. “granny3” and “anchor” it was a net negative. Interesting experiment, but it didn’t go in.

### Insertion policy

Another experiment we ran was on insertion policy. Specifically, our hypothesis was that at least on highly structured data (where the repeat offsets really help), we really want to make sure the important offsets stay “in front”. But occasionally, you will still get other matches that “don’t fit the pattern”. The problem is that this puts some other random offset in front that will then slowly “slide down” and meanwhile cause our actually important offsets to be more expensive to code.

This is more of a problem with greedy LZ parsers (which make their decisions locally); optimizing parsers (which usually try to look ahead by a few kilobytes or so) are better at correctly estimating the cost of “disrupting” the set of offsets. Either way, it’s annoying.

We tried a couple different approaches with this; the best overall approach we found in our tests was to stick with a basic MTF coding scheme and LRU eviction policy (bog-standard in other words), but distinguish between updates caused by repeat matches and those caused by inserting a new offset not currently in the repeat offset set. The former (repeat matches) just do a full move-to-front step, as usual. The latter don’t; instead of inserting a new offset all the way in front, we insert it further back. If it then gets reused a second time, it really will be moved all the way to the front of the list; but if it doesn’t get referenced again, it will drop out more quickly and with less disruption of the remaining repeat offsets.

Here’s the batch of test results, from the same compressor version. “kSlotNew” is the slot where new offsets are inserted; 0 corresponds to inserting in front (regular MTF), 1 is the second position, and so forth.

| Configuration | granny1 | granny2 | granny3 | anchor |
|---|---|---|---|---|
| 4 offsets, kSlotNew=0 | 18561994 | 22127519 | 15156085 | 1300427 |
| 4 offsets, kSlotNew=1 | 18450961 | 22153774 | 15154609 | 1304707 |
| 4 offsets, kSlotNew=2 | 18118014 | 22000266 | 15181128 | 1305755 |
| 4 offsets, kSlotNew=3 | 17736663 | 22002942 | 15209073 | 1307550 |
| 8 offsets, kSlotNew=0 | 17825495 | 21746140 | 14800616 | 1300534 |
| 8 offsets, kSlotNew=4 | 17327247 | 21546289 | 14771634 | 1305128 |
| 8 offsets, kSlotNew=6 | 17197347 | 21425116 | 14713121 | 1305588 |
| 16 offsets, kSlotNew=0 | 17554769 | 21523058 | 14600474 | 1300984 |
| 16 offsets, kSlotNew=14 | 17122510 | 21177337 | 14578492 | 1305432 |

We can see that the anchor prefers pure MTF, but the Granny files definitely see a win from not moving new offsets all the way to the front the first time they’re seen. There were a few more tests than the one shown, but in general, inserting new offsets in the second-to-last slot seemed like a good rule of thumb for the Granny files.

This one is definitely more contextual. As you can see, different types of files really prefer different settings here. BitKnit went with 8 offsets and insertion at the second-to-last slot (corresponding to the “8 offsets, kSlotNew=6” row above), because it produced the overall best results on the data it was designed for. (As evaluated on a larger test set not shown here.)

So, this is fairly neat, and a comparatively major win over the baseline 4 offsets and insert-in-front variant (a la LZMA) for the data in question. Now how to implement this efficiently?

### Implementation notes

The basic implementation of the offset maintenance logic in the decoder is dead simple. You just keep an array of recent offsets and shuffle it around with something like this:

if (is_repeat_match) { // move slot "rep_idx" to front. // this involves grabbing the offset at the corresponding // location and then sliding everything before that position // down by one slot. tmp = offsets[rep_idx]; for (uint i = rep_idx; i > 0; --i) offsets[i] = offsets[i - 1]; offsets[0] = tmp; } else { // implement the "insert in second-to-last position" // rule, which touches exactly two elements. offsets[kNumReps - 1] = offsets[kNumReps - 2]; offsets[kNumReps - 2] = newOffset; }

This works just fine, but it has a lot of data-dependent branches in the repeat match case, which is a performance trap in decompressors; generally speaking, you want to avoid branching on data you just read out of a bitstream, because it tends to be relatively high entropy and thus cause a lot of branch mispredictions, which are expensive.

One way to fix this is to add several entries worth of padding in front of the actual used part of `offsets`

, and always copy the same number of entries in the “sliding down” phase. This gets rid of the data-dependent branches and makes it easy to unroll the loop fully (since the trip count is now constant) or express it using a few unaligned SIMD loads/stores (where supported).

However, BitKnit uses a different approach derived from our earlier experiments with “stable index MRU” that doesn’t need anything beyond regular integer arithmetic. The basic idea is to leave the `offsets`

array alone; instead, we keep a secondary “data structure” that tells us which logical “repeat offset” list position corresponds to which index in the `offsets`

array.

I write “data structure” in quotes because that information is actually stored in (drum roll)… a single 32-bit unsigned integer! Here’s the idea: we have a `uint32_t mtf_state`

that represents the current offset permutation. It does this by storing the offset array index for the i’th logical repeat offset slot in the i’th nibble (numbered starting from the LSB upwards). At initialization time, we set `mtf_state = 0x76543210`

, the identity mapping: the logical and actual offset indices coincide.

Why does this help? Because the fundamental operation for move-to-front processing is moving a bunch of offsets “one slot down” in their array position. If they’re separate integers, that means either a lot of copying, or less copying but using much wider (e.g. SIMD) instructions. Our array of 4-bit indices is compact enough that 8 indices fit inside a single 32-bit uint; we can slide them all “down” or “up” using nothing but a single bit shift. Now, our code above doesn’t actually move *all* elements, just the ones at position ≥`rep_idx`

; but that turns out to be easily remedied with some bit masking operations.

So the alternative variant is this:

if (is_repeat_match) { // move slot "rep_idx" to front by permuting mtf_state. first, // determine the offset slot ID at that position in the list uint32_t rep_idx4 = rep_idx*4; uint32_t slot_id = (mtf_state >> rep_idx4) & 0xf; match_offs = offsets[slot_id]; // decoder needs this later! // moved_mtf: slide down everything by one slot, then put // "slot_id" in front. uint32_t moved_mtf = (mtf_state << 4) + slot_id; uint32_t keep_mask = ~0xf << rep_idx4; // bits that don't move mtf_state = (mtf_state & keep_mask) | (moved_mtf & ~keep_mask); } else { // implement the "insert in second-to-last position" // rule, which touches exactly two elements. this is easier // to do by just modifying the offsets directly. uint32_t last = (mtf_state >> ((kNumReps - 1)*4)) & 0xf; uint32_t before_last = (mtf_state >> ((kNumReps - 2)*4)) & 0xf; offsets[last] = offsets[before_last]; offsets[before_last] = newOffset; }

It’s a bit of integer arithmetic, but not a lot, and there’s no dependence on vector instructions, fast unaligned memory access, or in fact anything outside of standard C/C++. BitKnit uses a 32-bit `mtf_state`

to implement an 8-entry LRU cache. Using 64-bit values (and still using nibbles to store array indices), the exact same approach (with essentially no modifications to the source save for type names) can manage a 16-entry LRU.

An 8-entry LRU actually only needs 24 bits (when storing array indices in groups of three bits instead of nibbles), but that’s not a very useful size. A 4-entry LRU state fits in 4*log2(4) = 8 bits, which is nice and compact, although for 4 entries, this way is generally not a win (at least in our tests).

And now this is time to come clean: I kinda like this approach, and it’s the real reason I wrote this whole thing up. I probably would’ve still written it up even if it hadn’t turned out to be useful in practice, but it did, which is always a nice bonus.

Finally, over the years, I’ve found a few instances like this where packing a small “data structure” (using the term loosely) inside a single register-width integer produces interesting results. There’s a good chance I’ll write about more in the future! Until then.

Very interesting entry as usual Fabian.

A quick question regarding “starting the list” :

If I do understand your proposed scheme correctly (8 entry, start pos 6),

it means that as long as no repeated offset is detected yet,

there are only 2 entries in the table (pos 6 & 7).

Intuitively, it reduces the chances to detect a repeated match, since it must repeat itself pretty fast before being expurged from the list.

Or do you have some special “initialization” scheme to fill the 8 slots at the beginning ?

That is correct. Until a match is actually repeated for the first time, this scheme effectively acts like a 2-entry last offset cache, and yes, matches must repeat quickly to be “promoted”. That was, after all, the idea (to separate “transient” offsets from one with longer-term utility).

This form of update is definitely biased towards files with a particular structure. You can see it in the effect on the “anchor” file (Win32 EXE file), which does not have that type of structure. Interestingly, as far as I’ve been able to tell, the actual compression hit due to only having 2 effective last offset slots on files like “anchor” is quite minor; the main reason the non-record-heavy files seem to see a hit from inserting in a different position is that doing so “splits the vote” in the repeat offset index model. Normally, such files have a single peak in the model for last offset slot 0, and rapidly decaying probability after that. Inserting new offsets somewhere other than 0 makes the probability distribution bimodal; you now get two peaks located at 0 and the insertion position, with (very roughly) geometric falloff after those peaks. This distribution has higher entropy than the original (simple) last offset model, which adds up over time.

Yo Ryg, Where can I get this BitKnit? ;)

It only ships as part of commercial products by RAD Game Tools! But I’m documenting the interesting internals so that the knowledge still benefits the community.

It doesn’t benefit anything if people can’t even use it unless they pay thousand of dollars.

On the contrary, it benefits the Granny and Oodle users who

paid for its development.Very interesting, especially the insertion policy. I have my own nibble based compressor where I keep a 16 entry match history simply because I’m not entropy coding and have a nibble due to how I’ve constructed the format. I don’t do a strict move to front, but instead in the repeat match index isn’t 0, I swap that indexes entry with zero.

On lzt24 (structured file Charles released), I get:

RepMatch Counts/Index :

0 : 168073

1 : 14039

2 : 4244

3 : 2979

4 : 2213

5 : 2026

6 : 1680

7 : 1495

8 : 1374

9 : 1279

10 : 1235

11 : 1101

12 : 1006

13 : 1022

14 : 988

15 : 876

For comparsion with a text file, here are the results for Enwik8

RepMatch Counts/Index :

0 : 103964

1 : 43344

2 : 16716

3 : 12221

4 : 9946

5 : 8950

6 : 8317

7 : 7926

8 : 7262

9 : 7175

10 : 6958

11 : 6637

12 : 6562

13 : 6382

14 : 6274

15 : 6586

Gains with more offsets in the history, but the distribution is similar. One thing that surprised me is what is in the offset. Quite often I’d see offsets that were very close – within a few bytes of each other. Which became obvious when looking at the data – often matches would be partially floats, or uint32_t rather than being on the fundamental offset for the underlying structure. I’ve been wondering whether small deltas relative to an offset in the history would be worthwhile. Brotli includes +/- 1-3 for the last, or second to last offsets which is one way of doing that. Masking off a few bottom bits and then replacing with new entropy coded bits is one other idea. Or separate out the repeat match index with another entropy decode to get a delta. That is likely too expensive in decompression terms relative to any compression gains. But extending from 8 to 16 codes using the second 8 as a very limited set of fixed delta codes might be interesting.

Related question. How do you fill in

`is_repeat_match`

and`rep_idx`

? Do you go through each nibble and check if the corresponding position in the array matches the newOfset? Something like:Doesn’t come up in the BitKnit encoder. Offsets are never searched in the repeat-match-offset array. Instead, the encoder first looks at all repeat offset candidates, and only starts looking at the main search structure if there was no good enough match.

That is to say, there is never a need to look up index from offset because the search proceeds the other way, from index to offset.

Aah that makes sense. Thanks.