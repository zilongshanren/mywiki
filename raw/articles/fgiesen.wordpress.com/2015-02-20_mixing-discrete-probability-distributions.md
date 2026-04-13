---
title: Mixing discrete probability distributions
url: https://fgiesen.wordpress.com/2015/02/20/mixing-discrete-probability-distributions/
published: '2015-02-20'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Mixing discrete probability distributions

Let’s talk a bit about probability distributions in data compression; more specifically, about a problem in dealing with multi-symbol alphabets during adaptation.

Distributions over a binary alphabet are easy to mix (in the “context mixing” sense): they can be represented by a single scalar (I’ll use the probability of the symbol being a ‘1’, probability of ‘0’ works too) which are easily combined with other scalars. In practice, these probabilities are represented as fixed-size integers in a specific range. A typical choice is . Often, p=0 (“it’s certainly a 0”) and p=1 (certain 1) are excluded, because they only allow us to “encode” (using zero bits!) one of the two symbols.


Multi-symbol alphabets are trickier. A binary alphabet can be described using one probability p; the probability of the other symbol must be 1-p. Larger alphabets involve multiple probabilities, and that makes things trickier. Say we have a n-symbol alphabet. A probability distribution for such an alphabet is, conventionally, a vector such that

for all

and furthermore

. In practice, we will again represent them using integers. Rather than dealing with the hassle of having fractions everywhere, let’s just define our “finite-precision distributions” as integer vectors

, again

for all k, and

where T is the total. Same as with the binary case, we would like T to be a constant power of 2. This lets us use cheaper variants of conventional arithmetic coders, as well as

[rANS](https://fgiesen.wordpress.com/2014/02/02/rans-notes/). Unlike the binary case, maintaining this invariant takes explicit work, and it’s not cheap.

In practice, the common choice is to either drop the requirement that T be constant (most adaptive multi-symbol models for arithmetic coding take that route), or switch to a semi-adaptive model such as [deferred summation](http://www.cbloom.com/papers/context.pdf) that performs model updates in batches, which can either pick batches such that the constant sum is automatically maintained, or at least amortize the work spent enforcing it. A last option is using a “sliding window” style model that just uses a history of character counts over the last N input symbols. This makes it easy to maintain the constant sum, but it’s pretty limited.

A second problem is mixing – both as an explicit operation for things like context mixing, and as a building block for model updates more sophisticated than simply incrementing a counter. With binary models, this is easy – just a weighted sum of probabilities. Multi-symbol models with a constant sum are harder: for example, say we want to average the two 3-symbol models and

while maintaining a total of T=8. Computing

illustrates the problem: the two non-integer counts have to get rounded back to integers

*somehow*. But if we round both up, we end up at a total of 9; and if we round both down, we end up with a total of 7. To achieve our desired total of 8, we need to round one up, and one down – but it’s not exactly obvious how we should choose on any given symbol! In short, maintaining a constant total while mixing in this form proves to be tricky.

However, I recently realized that these problems all disappear when we work with the cumulative distribution function (CDF) instead of the raw symbol counts.

### Working with cumulative counts

For a discrete probability distribution p with total T, define the corresponding cumulative probabilities:

P0 is an empty sum, so P0=0. On the other end, Pn = T, since that’s just the sum over all values in p, and we know the total is T. For the elements in between, pk ≥ 0 implies that Pk ≥ Pk-1, i.e. P is monotonically non-decreasing. Conversely, given any P with these three properties, we can compute the differences between adjacent elements and determine the underlying distribution p.

And it turns out that while mixing quantized symbol probabilities is problematic, mixing cumulative distribution functions pretty much just works. To wit: suppose we are given two CDFs P and Q with the same total T, and a blending factor , then define:


Note that because summation is linear, we have



so this is indeed the CDF corresponding to a blended model between p and q. However, we’re still dealing with real values here; we need integers, and the easiest way to get there is to just truncate, possibly with some rounding bias :


It turns out that this just works, but this requires proof, and to get there it helps to prove a little lemma first.

**Spacing lemma**: Suppose that for some j, and

where m is an arbitrary integer. Then we also have

.


**Proof**: We start by noting that

and since m is an integer, we have





which was our claim.

Using the lemma, it’s now easy to show that R is a valid CDF with total T: we need to establish that R0=0, Rn=T, and show that R is monotonic. The first two are easy, since the P and Q we’re mixing both agree at these points and 0≤b<1.



As for monotonicity, note that is the same as

(and the same for P and Q). Therefore, we can apply the spacing lemma with m=0 for 1≤j≤n: monotonicity of P and Q implies that R will be monotonic too. And that’s it: this proves that R is valid CDF for a distribution with total T. If we want the individual symbol frequencies, we can recover them as

.


Note that the spacing lemma is a fair bit stronger than just establishing monotonicity. Most importantly, if pk≥m and qk≥m, the spacing lemma tells us that rk≥m – these properties carry over to the blended distribution, as one would expect! I make note of this because this kind of invariant is often violated by approximate techniques that first round the probabilities, then fudge them to make the total come out right.

### Conclusion

This gives us a way to blend between two probability distributions while maintaining a constant total, without having to deal with dodgy ad-hoc rounding decisions. This requires working in CDF form, but that’s pretty common for arithmetic coding models anyway. As long as the mixing computation is done exactly (which is straightforward when working in integers), the total will remain constant.

I only described linear blending, but the construction generalizes in the obvious way to arbitrary [convex combinations](http://en.wikipedia.org/wiki/Convex_combination). It is thus directly applicable to mixing more than two distributions while only rounding once. Furthermore, given the CDFs of the input models, the corresponding interval for a single symbol can be found using just two mixing operations to find the two interval end points; there’s no need to compute the entire CDF for the mixed model. This is in contrast to direct mixing of the symbol probabilities, which in general needs to look at all symbols to either determine the total (if a non-constant-T approach is used) or perform the adjustments to make the total come out to T.

Furthermore, the construction shows that probability distributions with sum T are closed under “rounded convex combinations” (as used in the proof). The spacing lemma implies that the same is true for a multitude of more restricted distributions: for example, the set of probability distributions where each symbol has a nonzero probability (corresponding to distributions with monotonically increasing, instead of merely non-decreasing, CDFs) is also closed under convex combinations in this sense. This is a non-obvious result, to me anyway.

One application for this (as frequently noted) is context mixing of multi-symbol distributions. Another is as a building block in adaptive model updates that’s a good deal more versatile than the obvious “steal the count from one symbol, add it to another” update step.

I have no idea whether this is new or not (probably not); I certainly hadn’t seen it before, and neither had anyone else at RAD. Nor do I know whether this will be useful to anyone else, but it seemed worth writing up!

A very important issue when updating probabilities

is what to do with smallest ones,

and the impact it introduces for all others.

Typically, in the blending example, think about updating Pi, with :

Pi = A*Ni + (1-A)Oi ;

if Ni == 1 , and Oi == 0, then Pi < 1.

Nonetheless, for the compression to work properly, it's necessary to give to Pi the minimum possible weight, 1.

This makes it difficult to "just use Ri (== S(P(0,i))) – R(i-1) (== S(P(0,i-1)))" to find back Pi, since depending on rounding rules, it may end up with Pi = Ri – R(i-1) = 0 , crashing the compression.

Spread over several symbols, such "minimum threshold" allocation will make a bunch of rare symbols take a fairly larger chunk of probability than they should, hence pressuring all the others to "live with less".

For information, a close variation of cumulative distribution strategy used to be the initial way FSE attributed weights to symbols. It was fast and looked efficient, but was later scraped, because its performance (in term of compression ratio) wasn't too good. The most important cause, I believe : fractional rounding was poor.

For example a 1.2 could be rounded to 2.0 because it followed a 1.8 which itself was rounded to 1.0. In this example, the rounding is clearly wrong, and basically depends on prior fractional distribution. Granted, it's more probable for 1.8 to be rounded up, but that's not good enough.

Another,more complex effect, is that fractional rounding has not the same importance depending on the integer prefix.

For example, Rounding up 1.7 to 2.0 end ups being a better choice than rounding up 99.9 to 100.0, which is not intuitive (but more clearly visible using logarithm).

As a consequence, the new version is a bit complex to describe, but I believe this post makes a relatively good job at presenting the basic concepts :

http://fastcompression.blogspot.com/2014/04/ultra-fast-normalization.html

The two standard strategies here are either having an escape symbol or just making sure the probabilities don’t get too small.

If you have an escape, you don’t care about symbol probabilities dropping to 0; all you need to make sure is that your escape symbol has nonzero probability.

If you can’t handle symbol props getting down to 0, well, you have to keep them nonzero. The whole point of this approach is that it makes it easy (or easier, anyway). You just have to make sure the p_k are all >=1 in all the distributions you’re mixing between, which then (by the spacing lemma) guarantees that the result won’t have non-representable symbols either.

The exact effects of rounding small probabilties are mainly important for FSE/tANS approaches because they use such a low probability resolution to begin with. For a conventional arithmetic rANS coder, it’s totally practical to use T>=2^16 (and a 64-bit rANS or regular arithmetic coder can easily use much more). My initial implementation of this worked with T=2^20. At that point it’s just not an issue. It’s the artihmetic coding equivalent of length-limited prefix codes: yes, using a code that’s length-limited to 20 bits is worse than using a Huffman code, but the effect is microscopic in practice.

Oh, one more point: the rounding details of FSE/tANS matter because it’s a model you’ll be using for a lot of symbols (several thousand, probably).

The setting I’m concerned about is adaptive models, as noted in the introduction. A single distribution is only used for a very short amount of time (context mixing blends differently on every symbol; adaptive update changes the distribution on every symbol, and semi-adaptive every few symbols). Allocating a sub-optimal probability to a single symbol isn’t a big deal if that particular model is only going to be used once!

Right. Indeed, if you can make sure that all symbols always have a discrete probability >= 1, then your lemma applies, and it just works.

I also agree that if your use case is about relatively small set of symbols over a large probability scale (such as the mentioned 2^20), then all discrete probabilities should be relative large, and the specific issues relative to small probabilities become secondary.

Note however that adding an escape symbol is not a transparent nor “cheap” operation.

It introduces one more branch into a critical loop, with the potential to kill performance.

This is only critical if the escape symbol aggregates a too large cumulative probability (regrouping multiple symbols). 10% for example would be too much. Keeping it < 1% is a good way to ensure the branch will have a manageable speed impact. But then, in some circumstances, low probability symbols are just numerous, and their combined probability is just non negligible.

Once again, it could be that such use case is simply not one you would have to deal with for your adaptive model.

I didn’t say that escapes were fast; I said that they solve the problem.

Besides, if you’re aiming for high performance, step 1: don’t do adaptive models or context mixing.

There is a typo (missing “+”) in:

= m + \lfloor \tilde{R}_{j-1} b \rfloor – \lfloor \tilde{R}_{j-1} + b \rfloor = m

It should be:

= m + \lfloor \tilde{R}_{j-1} + b \rfloor – \lfloor \tilde{R}_{j-1} + b \rfloor = m

Thanks. Fixed!