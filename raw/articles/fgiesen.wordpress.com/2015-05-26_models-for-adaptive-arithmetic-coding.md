---
title: Models for adaptive arithmetic coding
url: https://fgiesen.wordpress.com/2015/05/26/models-for-adaptive-arithmetic-coding/
published: '2015-05-26'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Models for adaptive arithmetic coding

My colleague Charles Bloom [recently announced](http://cbloomrants.blogspot.com/2015/05/05-09-15-oodle-lzna.html) Oodle LZNA (a new compressor for RAD’s Oodle compression library), which usually beats LZMA on compression while being *much* faster to decode. The major innovation in LZNA is switching the coding back-end from bit-wise adaptive modeling to models with larger alphabets. With traditional arithmetic coders, you take a pretty big speed hit going from binary to larger alphabets, and you end up leaning heavily on integer divides (one per symbol usually), which is the neglected bastard stepchild of every integer instruction set. But as of last year, we have the ANS family of coders, which alters the cost landscape considerably. Most interesting for use with adaptive models is [rANS](https://fgiesen.wordpress.com/2014/02/02/rans-notes/), which is significantly cheaper than conventional large-alphabet arithmetic (and without divisions in the decoder), but can still code directly from a cumulative probability distribution, just like other arithmetic coders. In short, rANS speeds up non-binary alphabets enough that it makes sense to revisit adaptive modeling for larger alphabets in practical coder design, something that’s been pretty much on hold since the late 90s.

In this post, I will try to explain the high-level design behind the adaptive models that underlie LZNA, and why they are interesting. But let’s start with the models they are derived from.

### Adaptive binary models

The canonical adaptive binary model simply keeps count of how many 0s and 1s have been seen:

counts[0] = 1; // or different init counts[1] = 1; prob_for_1 = 0.5; // used for coding/decoding void adapt(int bit) { counts[bit]++; prob_for_1 = counts[1] / (counts[0] + counts[1]); }

This is the obvious construction. The problem with this is that probabilities move quickly after initialization, but very soon start to calcify; after a few thousand symbols, any individual observation barely changes the probabilities at all. This sucks for heterogeneous data, or just data where the statistics change over time: we spend a *long* time coding with a model that’s a poor fit, trying to “unlearn” the previous stats.

A better approach for data with statistics that change over time is to gradually “forget” old stats. The resulting models are much quicker to respond to changed input characteristics, which is usually a decent win in practice. The canonical “leaky” adaptive binary model is, essentially, an exponential moving average:

prob_for_1 = 0.5; f = 1.0 - 1.0 / 32.0; // adaptation rate, usually 1/pow2 void adapt(int bit) { if (bit == 0) prob_for_1 *= f; else prob_for_1 = prob_for_1 * f + (1.0 - f); }

This type of model goes back to Howard and Vitter in “[Practical implementations of arithmetic coding](ftp://ftp.cs.brown.edu/pub/techreports/91/cs91-45.pdf)” (section 3.4). It is absolutely everywhere, albeit usually implemented in fixed point arithmetic and using shifts instead of multiplications. That means you will normally see the logic above implemented like this:

scale_factor = 4096; // .12 fixed point prob_for_1_scaled = scale_factor / 2; void adapt(int bit) { if (bit == 0) prob_for_1_scaled -= prob_for_1_scaled >> 5; else prob_for_1_scaled += (scale_factor - prob_for_1_scaled) >> 5; }

This *looks* like it’s a straightforward fixed-point version of the code above, but there’s a subtle but important difference: the top version, when evaluated in real-number arithmetic, can have `prob_for_1`

get arbitrarily close to 0 or 1. The bottom version cannot; when `prob_for_1_scaled`

≤ 31, it cannot shrink further, and likewise, it cannot grow past `scale_factor`

– 31. So the version below (with a fixed-point scale factor of 4096 and using a right-shift of 5) will keep scaled probabilities in the range [31,4065], corresponding to about [0.0076, 0.9924].

Note that with a shift of 5, we always stay 31 steps away from the top and bottom end of the interval – *independent of what our scale factor is*. That means that, somewhat counter-intuitively, that both the scale factor *and* the adaptation rate determine what the minimum and maximum representable probability are. In compression terms, the clamped minimum and maximum probabilities are equivalent to mixing a uniform model into a “real” (infinite-precision) Howard/Vitter-style adaptive model, with low weight. Accounting for this fact is important when trying to analyze (and understand) the behavior of the fixed-point models.

### A symmetric formulation

Implementations of binary adaptive models usually only track one probability; since there are two symbols and the probabilities must sum to 1, this is sufficient. But since we’re interested in models for larger than binary alphabets, let’s aim for a more symmetric formulation in the hopes that it will generalize nicely. To do this, we take the probabilities p0 and p1 for 0 and 1, respectively, and stack them into a column vector **p**:

Now, let’s look at what the Howard/Vitter update rule produces for the updated vector **p**‘ when we see a 0 bit (this is just plugging in the update formula from the first program above and using p1 = 1 – p0):

And for the “bit is 1” case, we get:

And just like that, we have a nice symmetric formulation of our update rule: when the input bit is *i*, the updated probability vector is

where the **e**i are the canonical basis vectors. Once it’s written in this vectorial form, it’s obvious how to generalize this adaptation rule to a larger alphabet: just use a larger probability vector! I’ll go over the implications of this in a second, but first, let me do a brief interlude for those who recognize the shape of that update expression.

### Aside: the DSP connection

Interpreted as a discrete-time system

where the sk denote the input symbol stream, note that we’re effectively just running a multi-channel IIR filter here (one channel per symbol in the alphabet). Each “channel” is simple linearly interpolating between its previous state and the new input value – it’s a discrete-time [leaky integrator](http://en.wikipedia.org/wiki/Leaky_integrator), a 1st-order low-pass filter.

Is it possible to use other low-pass filters? You bet! In particular, one popular variant on the fixed-point update rule has two accumulators with different update rates and averages them together. The result is equivalent to a 2nd-order (two-pole) low-pass filter. Its impulse response, corresponding to the weight of symbols over time, initially decays faster but has a longer tail than the 1st-order filter.

And of course you can use FIR low-pass filters too: for example, the incremental box filters described in my post [Fast blurs 1](https://fgiesen.wordpress.com/2012/07/30/fast-blurs-1/) correspond to a “sliding window” model. This approach readily generalizes to more general piecewise-polynomial weighting kernels using the approach described in Heckberts [“Filtering by repeated integration”](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.72.4795). I doubt that these are actually useful for compression, but it’s always nice to know you have the option.

Can we use arbitrary low-pass filters? Alas, we can’t: we absolutely need linear filters with unit gain (so that the sum of all probabilities stays 1 exactly), and furthermore our filters need to have non-negative impulse responses, since we’re dealing with probabilities here, and probabilities need to stay non-negative. Still, we have several degrees of freedom here, and at least in compression, this space is definitely under-explored right now. I’m sure some of it will come in handy.

### Practical non-binary adaptive models

As noted before, the update expression we just derived

quite naturally generalizes to non-binary alphabets: just stack more than two probabilities into the vector **p**. But it also generalizes in a different direction: note that we’re just linearly interpolating between the old model **p** and the “model” for the newly observed symbol, as given by **e**i. We can change the model we’re mixing in if we want different update characteristics. For example, instead of using a single spike at symbol i (as represented by **e**i), we might decide to slightly boost the probabilities for adjacent values as well.

Another option is to blend between the “spike” and a uniform distribution with a given weight *u*:

where **1** is the vector consisting of all-1s. This is a way to give us the clamping of probabilities at some minimum level, like we get in the fixed-point binary adaptive models, but in a much more controlled fashion; no implicit dependency on the scaling factor in this formulation! (Although of course an integer implementation will still have some rounding effects.) Note that, for a fixed value of *u*, the entire right-hand side of that expression only depends on *i* and does not care about the current value of **p** at all.

Okay, so we can design a bunch of models using this on paper, but is this actually practical? Note that, in the end, we will still want to get fixed-point integer probabilities out of this, and we would greatly prefer them to all sum to a power of 2, because then we can use rANS. This is where my previous post [“Mixing discrete probability distributions”](https://fgiesen.wordpress.com/2015/02/20/mixing-discrete-probability-distributions/) comes in. And this is where I’ll stop torturing you and skip straight to the punchline: a working adaptation step, with pre-computed mix-in models (depending on *i* only), can be written like this:

int rate = 5; // use whatever you want! int CDF[nsyms + 1]; // CDF[nsyms] is pow2 int mixin_CDFs[nsyms][nsyms + 1]; void adapt(int sym) { // no need to touch CDF[0] and CDF[nsyms]; they always stay // the same. int *mixin = mixin_CDFs[sym]; for (int i = 1; i < nsyms; ++i) CDF[i] += (mixin[i] - CDF[i]) >> rate; }

which is a pretty sweet generalization of the binary model update rule. As per the “Mixing discrete probability distributions”, this has several non-obvious nice properties. In particular, if the initial CDF has nonzero probability for every symbol, and all the `mixin_CDFs`

do as well, then symbol probabilities will never drop down to zero as a result of this mixing, and we always maintain a constant total throughout. What this variant doesn’t handle very well is round-off; there’s better approaches (although you do want to make sure that something like the spacing lemma from the mixing article still holds), but this variant is decent, and it’s certainly the most satisfying because it’s so breathtakingly simple.

Note that the computations for each *i* are completely independent, so this is data-parallel and can be written using SIMD instructions, which is pretty important to make larger models practical. This makes the update step fast; you do still need to be careful in implementing the other half of an arithmetic coding model, the symbol lookup step.

### Building from here

This is a pretty neat idea, and a very cool new building block to play with, but it’s not a working compressor yet. So what we can do with this, and where is it interesting?

Well. For a long time, in arithmetic coding, there were basically two choices. You could use larger models with very high per-symbol overhead: one or more divisions per symbol decoded, a binary search to locate the right symbol… pretty expensive stuff. Expensive enough that you want to make sure you code very few symbols this way. Adaptive symbols, using something like Fenwick trees, were even worse, and limited in the set of update rules they could support. In practice, truly adaptive large-alphabet models were exceedingly rare; if you needed some adaptation, you were more likely to use a deferred summation model (keep histogramming data and periodically rebuild your CDF from the last histogram) than true per-symbol adaptation, because it was so damn expensive.

At the other extreme, you had binary models. Binary arithmetic coders have *much* lower per-symbol cost than their non-binary cousins, and good binary models (like the fixed-point Howard/Vitter model we looked at) are likewise quite cheap to update. But the problem is that with a binary coder, you end up sending *many* more symbols. For example, in LZMA, a single 256-symbol alphabet model gets replaced with 8 binary coding steps. While the individual binary coding steps are much faster, they’re typically not *that* much faster that you can do 8× as many and still come out much faster. There’s ways to reduce the number of symbols processed. For example, instead of a balanced binary tree binarization, you can build a Huffman tree and use that instead… yes, using a Huffman tree to do arithmetic coding, I know. This absolutely works, and it is faster, but it’s also a bit of a mess and fundamentally very unsatisfying.

But now we have options in the middle: with rANS giving us larger-alphabet arithmetic decoders that are merely slightly slower than binary arithmetic coding, we can do something better. The models described above are *not* directly useful on a 256-symbol alphabet. No amount of SIMD will make updating 256 probability estimates per input symbol fast. But they *are* useful on medium-sized alphabets. The LZNA in “Oodle LZNA” stands for “LZ-nibbled-ANS”, because the literals are split into nibbles: instead of having a single adaptive 256-symbol model, or a binary tree of adaptive binary models, LZNA has much flatter trees of medium-sized models. Instead of having one glacially slow decode step per symbol, or eight faster steps per symbol, we can decode an 8-bit symbol in two still-quite-fast steps. The right decomposition depends on the data, and of course on the relative speeds of the decoding steps. But hey, now we have a whole continuum to play with, rather than just two equally unsavory points at the extreme ends!

This is not a “just paste it into your code” solution; there’s still quite a bit of art in constructing useful models out of this, several fun tricks in actually writing a fast decoder for this, some subtle variations on how to do the updates. And we haven’t even begun to properly play with different mix-in models and “integrator” types yet.

Charles’ LZNA is the first compressor we’ve shipped that uses these ideas. It’s not gonna be the last.

**UPDATE**: As pointed out by commenter “derf_” on Hacker News, the non-binary context modeling in the current Daala draft apparently describes the exact same type of model. Details [here](https://tools.ietf.org/html/draft-terriberry-codingtools-02#section-2) (section 2.2, “Non-binary context modeling”, variant 3). This apparently was proposed in 2012. We (RAD) weren’t aware of this earlier (pity, that would’ve saved some time); very cool, and thanks derf for the link!

Exciting stuff!

“// no need to touch CDF[0] and CDF[nsyms]; they always stay the same.”

Doesn’t this mean that “i” can start at 1 in the following for loop?

Indeed., habit. :) Thanks, fixed.

I did once replace divisions by multiplications with ~25% faster results for the arithmetic coders:

https://sourceforge.net/p/pyramidworkshop/code/HEAD/tree/libcoding-0.0.0/Interval/Arithmetic.hpp#l922

I did manage to do a specific range coder in SSE even, which does two division by the same divisor in the decoding. It’s a pain to develop, but’s faster. :)

Anyhow. Do you decode or encode in reverse? If you encode in reverse, do you store the ANS-state for replay, or the CDF-state?

We encode in two passes, treating the rANS as if it was a regular arithmetic coder. One pass forward does the adaptive modeling and pushes the intervals for each symbol, then a backwards pass that pops the symbols from the stack and does the actual rANS encode. You want to process data in chunks and periodically (but not too often) flush the ANS so you can use a bounded-size stack (and bounded-size staging area for the output bits).

I see. In your rANS-example code you record the interval (coder input), while in a tANS-implementation you’d record the bit-pattern (coder output).

No, my rANS example code is single-pass. It’s just the encoder, which makes you submit symbols backwards, and then produces the bitstream in reverse order. tANS is exactly the same – you submit symbols in reverse order, and get a reversed bitstream back.

You can’t do single-pass rANS with an adaptive model since encoder and decoder need to be adapting models in the same direction – the order the decoder receives the data in. Hence the encoder does the modeling forwards (the same direction the decoder sees the data) and buffers up the intervals, then does a backwards encode in a second pass.

It seems that there is a missing line break in your code:

for (int i = 1; i > rate;

This should be:

for (int i = 1; i > rate;

Stupid wordpress comment field. Once again:

for (int i = 1; …) CDF[i] += …;

should be replaced with:

for (int i = 1; …)

CDF[i] += …;

What’s the change?

Shouldn’t you be using discrete probability distribution instead of CDF for the adaptation (CDF[i] – CDF[i-1] )?

This is discrete. The C stands for cumulative not continuous. Adapting the (quantized, remember!) probabilities directly doesn’t work; in general they won’t sum to 1 after you combine them.

Nevermind, expanded it with some steps and found out the mixed distribution function covers that

I believe I’ve missed something, but where do the starting values for CDF and mixin_CDF come from? Is mixin_CDF precomputed, is there a way to decide what the best initial values in them should be?

CDF can start out however you want; if you’re unsure, just use a uniform distribution.

The mixin distributions are the CDFs for PDFs of the form “(1-u)e_i + u*1” as given in the math. Just summing that and going to fixed point yields an expression of the type

`mixin_CDF[i][j] = (kMaxProb - kSpikeHeight) * j / nsyms + ((i >= j) ? kSpikeHeight : 0);`

kMaxProb is your overall probability scale factor (usually a power of 2), kSpikeHeight corresponds to (1-u)*kMaxProb in the math.

Ah yes, that makes sense.

Thanks.

The values in CDF should be a true CDF right? Always right increasing values?

Yup, needs to be strictly increasing.

Excellent! I have buggy code and no clue why. ;)

Time to sprinkle asserts everywhere like magical bug fighting fairy dust.