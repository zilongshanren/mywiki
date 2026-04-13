---
title: rANS with static probability distributions
url: https://fgiesen.wordpress.com/2014/02/18/rans-with-static-probability-distributions/
published: '2014-02-18'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# rANS with static probability distributions

In the [previous post](https://fgiesen.wordpress.com/2014/02/02/rans-notes/), I wrote about rANS in general. The ANS family is, in essence, just a different design approach for arithmetic coders, with somewhat different trade-offs, strengths and weaknesses than existing coders. In this post, I am going to talk specifically about using rANS as a drop-in replacement for (static) Huffman coding: that is, we are encoding data with a known, static probability distribution for symbols. I am also going to assume a compress-once decode-often scenario: slowing down the encoder (within reason) is acceptable if doing so makes the decoder faster. It turns out that rANS is very useful in this kind of setting.

### Review

Last time, we defined the rANS encoding and decoding functions, assuming a finite alphabet of n symbols numbered 0 to n-1.



where

.


where is the frequency of symbol s,

is the sum of the frequencies of all symbols before s, and

is the sum of all symbol frequencies. Then a given symbol s has (assumed) probability

.


Furthermore, as noted in the previous post, M can’t be chosen arbitrarily; it must divide L (the lower bound of our normalized interval) for the encoding/decoding algorithms we saw to work.

Given these constraints and the form of C and D, it’s very convenient to have M be a power of 2; this replaces the divisions and modulo operations in the decoder with bit masking and bit shifts. We also choose L as a power of 2 (which needs to be at least as large as M, since otherwise M can’t divide L).

This means that, starting from a reference probability distribution, we need to approximate the probabilities as fractions with common denominator M. My colleague Charles Bloom just wrote [a blog post on that very topic](http://cbloomrants.blogspot.com/2014/02/02-11-14-understanding-ans-10.html), so I’m going to refer you there for details on how to do this optimally.

### Getting rid of per-symbol divisions in the encoder

Making M a power of two removes the division/modulo operations in the decoder, but the encoder still has to perform them. However, note that we’re only ever dividing by the symbol frequencies , which are known at the start of the encoding operation (in our “static probability distribution” setting). The question is, does that help?


You bet it does. A little known fact (amongst most programmers who aren’t compiler writers or bit hacking aficionados anyway) is that division of a -bit unsigned integer by a constant can always be performed as fixed-point multiplication with a reciprocal, using

bits (or less) of intermediate precision. This is

*exact* – no round-off error involved. Compilers like to use this technique on integer divisions by constants, since multiplication (even long multiplication) is typically much faster than division.

There are several papers on how to choose the “magic constants” (with proofs); however, most of them are designed to be used in the code generator of a compiler. As such, they generally have several possible code sequences for division by constants, and try to use the cheapest one that works for the given divisor. This makes sense in a compiler, but not in our case, where the exact frequencies are not known at compile time and doing run-time branching between different possible instruction sequences would cost more than it saves. Therefore, I would suggest sticking with Alverson’s original paper [“Integer division using reciprocals”](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.33.1710).

The [example code](https://github.com/rygorous/ryg_rans/blob/854451f698c3a604de7441d0a3f953a2b3053ac9/rans_byte.h#L150) I linked to implements this approach, replacing the division/modulo pair with a pair of integer multiplications; when using this approach, it makes sense to limit the state variable to 31 bits (or 63 bits on 64-bit architectures): as said before, the reciprocal method requires bits working precision for worst-case divisors, and reducing the range by 1 bit enables a faster (and simpler) implementation than would be required for a full-range variant (especially in C/C++ code, where multi-precision arithmetic is not easy to express). Note that handling the case

requires some extra work; details are explained in the code.


### Symbol lookup

There’s one important step in the decoder that I haven’t talked about yet: mapping from the “slot index” to the corresponding symbol index. In normal rANS, each symbol covers a contiguous range of the “slot index” space (by contrast to say tANS, where the slots for any given symbol are

[spread relatively uniformly across the slot index space](http://cbloomrants.blogspot.com/2014/02/02-06-14-understanding-ans-8.html)). That means that, if all else fails, we can figure out the symbol ID using a binary search in steps (remember that n is the size of our alphabet) from the cumulative frequency table (the

, which take O(n) space) – independent of the size of M. That’s comforting to know, but doing a binary search per symbol is, in practice, quite expensive compared to the rest of the decoding work we do.


At the other extreme, we can just prepare a look-up table mapping from the cumulative frequency to the corresponding symbol ID. This is very simple (and the technique used in the example code) and theoretically constant-time per symbol, but it requires a table with M entries – and if the table ends up being too large to fit comfortably in a core’s L1 cache, real-world performance (although still technically bounded by a constant per symbol) can get quite bad. Moving in the other direction, if M is small enough, it can make sense to store the per-symbol information in the M-indexed table too, and avoid the extra indirection; I would not recommend this far beyond M=212 though.

Anyway, that gives us two design points: we can use space, at a cost of

per symbol lookup; or we can use

space, with

symbol lookup cost. Now what we’d really like is to get

symbol lookup in

space, but sadly that option’s not on the menu.


Or is it?

### The alias method

To make a long story short, I’m not aware of any way to meet our performance goals with the original unmodified rANS algorithm; however, we can do much better if we’re willing to relax our requirements a bit. Notably, there’s no deep reason for us to require that the slots assigned to a given symbol s be contiguous; we already know that e.g. tANS works in a much more relaxed setting. So let’s assume, for the time being, that we can rearrange our slot to symbol mapping arbitrarily (we’ll have to check if this is actually true later, and also work through what it means for our encoder). What does that buy us?

It buys us all we need to meet our performance goals, it turns out (props to my colleague Sean Barrett, who was the first one to figure this out, in our internal email exchanges anyway). As the section title says, the key turns out to be a stochastic sampling technique called the [“alias method”](http://en.wikipedia.org/wiki/Alias_method). I’m not gonna explain the details here and instead refer you to [this short introduction](http://pandasthumb.org/archives/2012/08/lab-notes-the-a.html) (written by a computational evolutionary geneticist, on randomly picking base pairs) and [“Darts, Dice and Coins”](http://www.keithschwarz.com/darts-dice-coins/), a much longer article that covers multiple ways to sample from a nonuniform distribution (by the way, note that the warnings about numerical instability that often accompany descriptions of the alias method need not worry us; we’re dealing with integer frequencies here so there’s no round-off error).

At this point, you might be wondering what the alias method, a technique for sampling from a non-uniform discrete probability distribution, has anything to do with entropy (de)coding. The answer is that the symbol look-up problem is essentially the same thing: we have a “random” value from the interval [0,M-1], and a matching non-uniform probability distribution (our symbol frequencies). Drawing symbols according to that distribution defines a map from [0,M-1] to our symbol alphabet, which is precisely what we need for our decoding function.


So what does the alias method do? Well, if you followed the link to the [article I mentioned earlier](http://pandasthumb.org/archives/2012/08/lab-notes-the-a.html), you get the general picture: it partitions the probabilities for our n-symbol alphabet into n “buckets”, such that each bucket i references at most 2 symbols (one of which is symbol i), and the probabilities within each bucket sum to the same value (namely, 1/n). This is *always* possible, and there is an algorithm (due to Vose) which determines such a partition in O(n) time. More generally, we can do so for any N≥n, by just adding some dummy symbols with frequency 0 at the end. In practice, it’s convenient to have N be a power of two, so for arbitrary n we would just pick N to be the smallest power of 2 that is ≥n.

Translating the sampling terminology to our rANS setting: we can subdivide our interval [0,M-1] into N sub-intervals (“buckets”) of equal size k=M/N, such that each bucket i references at most 2 distinct symbols, one of which is symbol i. We also need to know what the other symbol referenced in this bucket is – `alias[i]`

, the “alias” that gives the methods its name – and the position `divider[i]`

of the “dividing line” between the two symbols.

With these two tables, determining the symbol ID from x is quick and easy:

uint xM = x % M; // bit masking (power-of-2 M) uint bucket_id = xM / K; // shift (power-of-2 M/N!) uint symbol = bucket_id; if (xM >= divider[bucket_id]) // primary symbol or alias? symbol = alias[bucket_id];

This is O(1) time and O(N) = O(n) space (for the “divider” and “alias” arrays), as promised. However, this isn’t quite enough for rANS: remember that for our decoding function D, we need to know not just the symbol ID, but also which of the (potentially many) slots assigned to that symbol we ended up in; with regular rANS, this was simple since all slots assigned to a symbol are sequential, starting at slot :


where

.


Here, the part is the number we need. Now with the alias method, the slot IDs assigned to a symbol aren’t necessarily contiguous anymore. However, within each bucket, the slot IDs assigned to a symbol are sequential – which means that instead of the cumulative frequencies

, we now have two separate per bucket. This allows us to define the complete “alias rANS” decoding function:


// s, x = D(x) with "alias rANS" uint xM = x % M; uint bucket_id = xM / K; uint symbol, bias; if (xM < divider[bucket_id]) { // primary symbol or alias? symbol = bucket_id; bias = primary_start[bucket_id]; } else { symbol = alias[bucket_id]; bias = alias_start[bucket_id]; } x = (x / M) * freq[symbol] + xM - bias;

And although this code is written with branches for clarity, it is in fact fairly easy to do branch-free. We gained another two tables indexed with the bucket ID; generating them is another straightforward linear pass over the buckets: we just need to keep track of how many slots we’ve assigned to each symbol so far. And that’s it – this is all we need for a complete “alias rANS” decoder.

However, there’s one more minor tweak we can make: note that the only part of the computation that actually depends on `symbol`

is the evaluation of `freq[symbol]`

; if we store the frequencies for both symbols in each alias table bucket, we can get rid of the dependent look-ups. This can be a performance win in practice; on the other hand, it does waste a bit of extra memory on the alias table, so you might want to skip on it.

Either way, this alias method allow us to perform quite fast (though not as fast as a fully-unrolled table for small M) symbol look-ups, for large M, with memory overhead (and preparation time) proportional to n. That’s quite cool, and might be particularly interesting in cases where you either have relatively small alphabets (say on the order of 15-25 symbols), need lots of different tables, or frequently switch between tables.

### Encoding

However, we haven’t covered encoding yet. With regular rANS, encoding is easy, since – again – the slot ranges for each symbol are contiguous; the encoder just does


where is the slot id corresponding to the

‘th appearance of symbol s.


With alias rANS, each symbol may have its slots distributed across multiple, disjoint intervals – up to N of them. And the encoder now needs to map to a corresponding slot index that will decode correctly. One way to do this is to just keep track of the mapping as we build the alias table; this takes O(M) space and is O(1) cost per symbol. Another is to keep a sorted list of subintervals (and their cumulative sizes) assigned to each symbol; this takes only O(N) space, but adds a $O(\log_2 N)$ (worst-case) lookup per symbol in the encoder. Sound familiar?


In short, using the alias method doesn’t *really* solve the symbol lookup problem for large M; or, more precisely, it solves the lookup problem on the decoder side, but at the cost of adding an equivalent problem on the encoder side. What this means is that we have to pick our poison: faster encoding (at the some extra cost in the decoder), or faster decoding (at some extra cost in the encoder). This is fine, though; it means we get to make a trade-off, depending on which of the two steps is more important to us overall. And as long as we are in a compress-once decompress-often scenario (which is fairly typical), making the decoder faster at some reasonable extra cost in the encoder is definitely useful.

### Conclusion

We can exploit static, known probabilities in several ways for rANS and related coders: for encoding, we can precompute the right “magic values” to avoid divisions in the hot encoding loop; and if we want to support large M, the alias method enables fast decoding without generating a giant table with M entries – with an O(n) preprocessing step (where n is the number of symbols), we can still support O(1) symbol decoding, albeit with a (slightly) higher constant factor.

I’m aware that this post is somewhat hand-wavey; the problem is that while Vose’s algorithm and the associated post-processing are actually quite straightforward, there’s a lot of index manipulation, and I find the relevant steps to be quite hard to express in prose without the “explanation” ending up harder to read than the actual code. So instead, my intent was to convey the “big picture”; a sample implementation of alias table rANS, with all the details, can be found – as usual – on [Github](https://github.com/rygorous/ryg_rans/blob/master/main_alias.cpp#L159).

And that’s it for today – take care!

hi ryg,

Thanks for interesting method – it allows for good accuracy using a few times less memory than tANS at cost of speed.

As there is often needed binary entropy coder – with probability varying from bit to bit, I wonder how your SIMD approach would compare to used methods? For binary case, determining the symbol is simpler – just a single ‘if’. However, for low state size version, I’m afraid the range variants are not accurate enough – but 256 states for 16-way case should be sufficient for much more accurate uABS (b=2) variant?

Thanks,

Jarek

The SIMD/GPU approach is, at least in principle, completely orthogonal to which coder family you use.

I emphasize large-radix variants in the paper since they lead to (by far) the simplest implementations, but this is not a necessity. You could still use b=2, count the bits required in each vector lane, use a prefix sum for each vector lane to figure out where its bits come from (or go to, in the case of an encoder), and structure the IO that way. This would be fairly awkward in a CPU implementation, but maps reasonably well to (at least some) GPU instruction sets.

Also, why do you worry about low state sizes? The SIMD implementation I describe has 32-bit states (albeit with a large variation in relative precision over time, since I use a very large radix of b=2^16) and 64-bit states are not out of the question.

With regards to binary coders, there’s two problems:

1. In typical use, they rapidly switch contexts (in a way that depends on previous coded bits). This forces serial processing on the decoder end – the decoder doesn’t know what model to use until it’s decoded everything before it! Which in turn means there’s no efficient way to apply SIMD processing.

2. Separately, they also *update* the model after every bit decoded. Thus, even if two SIMD lanes share the same model, its corresponding probability is different between them.

1), you really just can’t do if you want efficient SIMD decoding. The contexts need not necessarily be determined *completely* independent of what’s happening in other lanes, but if there is some fine-grained context switching, it must be explicitly designed to be SIMDable.

2) can be fixed by “batching” updates; e.g. only update model probabilities every 64 symbols, which allows a 64-wide decoder. Whether this is efficient or not depends on how many potential contexts might be used. Keeping track of the balance of 0s/1s coded when there are only 4 potential contexts used is relatively easy and fast; when there are 400 contexts that might need to be updated, not so much.

Fabian, sure there is usually dependence in the binary case, but still e.g. tABS has a few advantages. For example let say 64 tables for different quantized probability of the least probable symbol on 64 states – a few kilobytes of tables for deltaH~0.0001 bits/symbol (or less than a kilobyte for perfect for cheap hardware implementation qABS):

Encoding: buffering (symbol,probability) we can use SIMD version – getting a few times speedup.

Decoding: tABS step is just a table use and BitOr – CABAC M-coder has additionally renormalization and addition – tABS should be at least 20% faster, and both Charles and Yann’s implementations seem to be.

Additionally, sometimes there can appear independence of a few succeeding probabilities, what allows to use a few times faster SIMD variant – there can be a few separate decoding step variants depending on the number of bits to decode in this step.

Oh, one more thing:

In my experiments, and with an optimized implementation (i.e. not the one on Github, since that’s written for readability and portability not speed) rANS + alias table is actually *faster* than tANS once m becomes large enough (the cutoff is usually somewhere between m=2^13 and m=2^15, depending on what exactly is stored in the tables).

Basically, tANS performance *really* suffers once the tables become large enough to drop out of the L1 cache (as does a rANS implementation if it’s using a cumulative probability->symbol table of some kind).

Now, the question is whether you need large m. Certainly if you rebuild your static models every 8k-32k or so, there’s little point; so I’m not sure whether the alias table approach is useful in that case.

It’s definitely useful when you want several probability distributions for small alphabets, though; say m=2^10 and an alphabet with 16-20 symbols. With the alias table approach, you can store 10+ different PDs in the same amount of space you would use for one tANS table. This makes it viable to perform adaptation (and some basic context modeling) by just switching between different prepared tables.

I think additional advantage of rANS with alias method is that it allows for cheap dynamical updating of probability distribution for some adaptive methods – most updates of probabilities can be made by just shifting single divider (and updating further starts).

It is at cost of alias probability, which is usually much larger so its probability change has smaller impact on entropy.

It’s not really a good way to do things; anything that only adjusts one divider has to take all of the redistributed probability density away from a single source symbol, which is not ideal.

Indeed it is not ideal – shifting single divider changes probability at cost of other symbol. However, as deltaH~sum_s (p_s – q_s)^2/p_s, accuracy of low probable symbol has much larger impact and the alias has often much larger probability (is distributed among multiple buckets), so such improving accuracy of lower probable symbol would improve deltaH.

Generally, designing a good updater here is a difficult task, sometimes it could shift a few dividers instead and sometimes would need to make a structural change (alias->bucket distribution), but could allow for fast symbol-by-symbol adaptive compressors – tracking especially the very low probable symbols (e.g. every count update asks if lower/upper boundary for this symbol hasn’t been reached – if so, update coding tables).

Anyway, there were dynamic updating approaches for Huffman – I am just saying that alias rANS looks much better for something like that: is accurate and seems cheaper to modify.

I believe there’s a typo. You defined M by summing over nothing:

M = \sum_{i=0}^{n-1}

This should be:

M = \sum_{i=0}^{n-1}F_i

Yes indeed. Good catch, thanks!

Fabian,

you can use the full range for reciprocal-by-mult by removing the leading ‘1’ from the multiplying factor and keeping only the fractional part of it. In Alverson’s notation:

W = 16, 32 or 64 bits of precision

shift = ceil(log2(y))

sh = W + shift

a = ceil((1 << sh) / y) – (1 <> W; // that’s the __umulh

result = (tmp + x) >> shift; // the ‘+ x’ restores the missing leading bit, that’s the trick

There’s a caveat though: ‘tmp + x’ can overflow by 1bit the W-bit register, so some care is needed here.

This might make it even with just using W=31 reduced precision, as you mentioned.

Still, for W=16bit (and 32-bit state), this method might be useful. And also if you need to store precomputed ‘a’ somewhere, since they now fit in W bits, not W+1.

More comments and code here: https://github.com/skal65535/fsc/blob/master/divide.h

(btw, say “Hi!” to Won!)

Hi Pascal!

Yeah, if your state is significantly smaller than your registers, there’s several techniques that work.

The proble with classic Alverson’s is the need for an extra bit during the accumulation, as you mention. This has several problems if you’re working with full-width registers: first, it can’t be conveniently expressed in C/C++, and even in ASM it does require using relatively slow instructions. There’s two primary ways to do it:

1. Use one register plus carry bit. Boils down to (on x64):

You use the same basic approach for the usual divide-by-reciprocal-mult sequence.

`rcr`

isn’t the fastest instruction, but there’s a more serious problem: this doesn’t work for the divisor=1 case where shift=0! You don’t care for this in a compiler for code generation (constant x/1 is trivially strength-reduced), but in this setting we do need to support 1 directly, so this approach isn’t viable. Which brings us to:2. Full-on double-width arithmetic

This works, but still, a good deal of extra work.

The problem with using W=31 (or W=63) directly in this scheme is that it turns the shift on the

multiplyinto a shift by 31 instead of 32, (63 instead of 64 in 64-bit mode). On x86/x64, that now means we have to do the shift explicitly, using either SHRLD or a replacement sequence, instead of just getting the result in a separate register “free of charge”. On other architectures (everything I do at RAD has to keep at least ARM and POWER in mind) it’s worse, because we now also need a multiply-low/multiply-high combination instead of a single multiply-high instruction.The version in the code I published is the one with the shortest critical path of all variants I could come up with, and it only works because it cheats (using the “bias” value, which is actually the start of the symbol range, as an extra DOF). Note that the division part turns into just:

Of the variants I could come up with, this one performed best. That said, I didn’t spend a lot of time on it, so I might well be missing something.

nice explanation, thanks for filling in the details Fabian!

It’s true that things get hairy without fine-control over the ASM.

And even so, since in this case you have control over the bias too (and

not just the multiplier), it’s harmless to use one ‘less’ bit of accuracy

since the f=1 case is handled nicely on the side.

good stuff!

/skal

(btw: i’m toying with SSSE3/SSE4.1 implementation now. Strange thing is

that it’s slower than plain-C here. Not sure why. I’ll post the code somewhere

when i’ve figured that strangeness out…)

The SSE impls are all about the gathers for the symbol frequencies and the renormalization. The math is almost free.

Part of my interest in rANS is because it admits practical GPU-side decoder implementations that are 100% bitstream-compatible with certain (multi-way interleaved) serial designs – see my paper.

GPU changes the trade-offs somewhat compared to CPU. Same as for low-power RISCs, you want to work with 32-bit regs, and ideally renormalize 16 bits at a time (=no loops in renorm). Gathers are cheap (if they’re in cache), compute is cheap, but large table accesses on the critical path are terrible (unless you want to go super-wide with the interleaving, which has its own issues).

Hence interleaved alias rANS. The compute is cheap. We’re reading sequentially from a single input stream (much better than reading from N separate input streams in terms of memory access, and no tricky demuxing). And the alias decoding tables are really compact for small alphabets, so they have a good chance of staying in L1.

For video/images, most of the alphabets I’d want to use multisymbol coding for have less than 30 symbols, so this seems plausible. (Then, use multiple static tables instead of real adaptivity? Not sure.) Combine that with simple, ultra-cheap bypass coding and a matching (quite precise) binary coder in the form of uABS for decision bits, and it seems like it could really work. Haven’t gotten around to actually trying any of this, though.

How does choose of L impacts performance or compression ratio? In your implementation, you have chosen (1u << 23). Why so big?

(I am so inspired by rANS so I decided to learn compression algorithms and entropy coding algorithms. Maybe as an overwhelmed beginner, I do not see something obvious).

The three implementations in ryg_rans all use different values of L! rans_word has L=2^16, rans_byte has 2^23 and rans64 has 2^31.

It’s like the normalized interval size in an arithmetic coder. The higher you make it, the less coding loss there is. That said the gains are pretty minor, but in a SW implementation there is no real cost to making it as large as will fit the underlying data types.

The largest you can make the range is ultimately limited by the width of the data type and the renormalization granularity. rans_byte uses 32-bit uint states and byte-granularity renormalization, making 2^24 the maximum possible. rans_byte uses 2^23 instead because the division by multiplying with a fixed-point reciprocal used in the RansEncSymbol functions would need to use 33-bit reciprocals to give the correct result for all 32-bit numbers. By limiting the range so 31 bits, the reciprocals can be 32 bits instead.

The choice of L=2^31 in the 32-bit renormalization rans64 is similar: this limits the maximum state value to 2^63-1 which means the reciprocals fit in 64 bits. Flushing out full 32-bit values at once also means there are never multiple renormalization steps when encoding a value; unlike the byte version which can emit multiple bytes after a symbol, the 64-bit version either emits a single 32-bit word or it doesn’t.

rans_word keeps a 32-bit state and emits 16-bit words at a time. This means L can at most be 2^16. rans_word is meant to illustrate a different idea and doesn’t use either a static model or the reciprocal trick so it can use the full 32 bits, and indeed you wouldn’t want to lose any more bits. With L=2^16, you’re already losing quite a bit of probability resolution; this is mostly OK for 14-bit probabilities but that’s already pushing it.