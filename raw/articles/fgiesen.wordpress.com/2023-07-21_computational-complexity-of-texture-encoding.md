---
title: Computational complexity of texture encoding
url: https://fgiesen.wordpress.com/2023/07/21/computational-complexity-of-texture-encoding/
published: '2023-07-21'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Computational complexity of texture encoding

Most standard texture compression formats use a type of algorithmic vector quantization (meaning that instead of storing an explicit codebook of possible blocks, the codebook entries are determined by an algorithm that uses the encoded block as an input). This is the case for all the BCn formats, ETC/EAC, and ASTC, but not PVRTC, where the decoded pixels near the edge of a block also depend on adjacent blocks, which makes the encoding process more of a global problem (so the notes in this post do not apply).

Furthermore, the contents of the encoded blocks can usually be partitioned into three categories:

- Header/mode bits, which determine how the remaining contents of the block are to be interpreted.
- Endpoints, which specify some of the colors present in the block in some form. The endpoints are then expanded into a larger palette of colors, and pixels select which color they want using
- Indices into the palette. Pixels generally pick the index that gives the closest match in the palette according to some error metric.

The expansion process from specified endpoints into the full palette frequently involves some form of linear interpolation, and the error metric is usually some variant of squared error (possibly weighted), for numerous reasons.

I have now several times run into people who thought that encoding textures at reasonable speed was impressive because this problem looks like certain well-known hard problems such as Integer Least Squares. This is not the case, for at least two orthogonal reasons:

- Being able to reduce a problem to some variant of Integer Least Squares, or Integer Linear Programming, does not automatically make it hard in a computational complexity sense. The reduction in a hardness proof needs to go the other way: you need to be able to turn an arbitrary instance of a known hard problem into an instance of your problem to prove that your problem is hard. It is entirely possible, and frequently quite easy, to go the other way and turn trivial problems into instances of NP-hard or worse problems (usually by accident).
- Hyper-polynomial growth of the best-known solution to a problem as a function of problem size N matters when the problem size depends on the input, but this is not the case for block-based texture compression. When the N for some hyper-polynomial algorithm is bounded by a constant independent of the size of the input (in this case that would be the dimensions of the texture), the asymptotic complexity of whatever algorithm you use to solve a NP-hard subproblem does not really matter.

In particular, if you chop an image/texture into fixed-size blocks (i.e. block size doesn’t depend on the input) that are then encoded fully independently, and encoding any given block takes a bounded amount of time, that makes encoding of the full image linear time in the number of input pixels, even if encoding any individual block is a combinatorial nightmare. You might not like the constant factors in front, but it’s still going to be linear time.

For the purposes of computational complexity, behold the following universal algorithm to encode compressed textures:

```
best, best_dist = None, None
for E in enumerate_coded_blocks():
D = decode_block(E)
dist = distance_metric(D, original_block)
if best_dist is None or dist < best_dist:
best_dist = dist
best = E
return best
```


This is a perfectly fine linear-time algorithm with the only problem being that even with something as modest as 64-bit blocks, it’s not expected to finish before the heat death of the universe. Don’t worry though, this post is not just an exercise in pedantry.

Namely, the other thing we can immediately do from the decomposition of a block into its constituent parts above is to shrink the search space drastically, and of course practical encoding algorithms do just that.

- Not all header/mode bits need to be explored. If desired, methods that still want to guarantee optimality can use branch-and-bound techniques to prune the search. In practice, nobody actually wants to spend the extra time (or cares about the generally tiny improvements from) guaranteeing optimality, so more commonly heuristics are used here as well.
- Formats that split their blocks into subsets let you do parts of the solve separately, which shrinks the search space considerably where it applies.
- Given a set of endpoints, the source pixels, and a distance metric, it is pointless to try all possible choices of indices. Once we fix the endpoints for a subset (and possibly some index constraints resulting from that choice), the optimal indices can generally be determined directly. This direction is usually cheap to solve exactly, but the endpoints are a somewhat awkward search space.
- In the other direction, if we fix a set of indices, the source pixels, and the distance metric, we can try to solve for the optimal endpoints given that set of indices. This direction is usually tricky to solve exactly, but the search space is easier to prune to a small subset. It’s the basis of cluster fit methods like the original algorithm in the S3TC patent and methods derived from it.

The actual reason I’m writing this post is that for several of the simpler formats, the resulting search space is small enough that exhaustive search is completely viable. Not so much for real-world texture encoding, it’s too slow and the benefits are way too small for that. For BC1-5, it’s also pointless because the decoder isn’t exactly specified. But it’s definitely doable to get reference results if you want to see what optimality actually looks like.

In particular, for BC3 alpha or BC4 blocks, the set of possible endpoint/mode combinations is just 16 bits (the ordering of the endpoints selects one of two modes), so 65536 possible choices of endpoint pairs. Determining the optimal endpoints *in 1D* isn’t even hard (and can be done exactly using fairly straightforward math), and it’s all very easy to accelerate using SIMD, using a GPU, or both. This is not only eminently viable, it’s viable enough that not only can this be used to test individual blocks (or small image snippets), you can encode full textures this way just fine. Sure, encoding a 1024×1024 texture that way takes seconds instead of milliseconds but that’s not long to wait for a reference result at all.

BC5 is just two independent BC4 blocks, one per channel, and they’re completely independent, so this also applies to BC5. BC1 color blocks are still 64-bit blocks and have a 32-bit space of possible endpoint pairs. However, 232 = about 4 billion “interesting” encodings (since we don’t care about sub-optimal choices of indices) is still small enough that exhaustive testing is totally viable on either CPU or GPU if you’re using an optimized search, a beefy CPU/GPU, parallelization and are willing to wait a bit to encode a single 4×4 pixel block. (In this case, you probably would not want to encode a full 1024×1024 texture this way.) And if we can do BC1 and BC4, we can also do BC2 (the alpha part is trivial) and BC3 (effectively separate BC1+BC4, they decompose). In short, BC1-5 are actually totally practical to do exhaustive encoding these days, and the same applies to ETC and EAC.

Would you use this for a practical encoder? Definitely not. Likewise, it’s not viable for the more complex formats like BC6-7 or ASTC. Nevertheless, it felt worth pointing out that optimal BC4-5/EAC encoding (in the least-squares sense anyway) for a known decoder is eminently possible even at home for real-world-sized textures if you’re willing to wait for a few seconds (and that’s with no pruning whatsoever). BC1-3/ETC are more involved, but still at a timescale where determining optimal solutions (given a known decoder) for a small image patch is something you can easily do on a regular home computer even without using any pruning strategies if you’re willing to wait a few hours.

Now the actual application given here is obviously very specific to what I happen to be working on, but the reason I’m writing it up is that I’m trying to make a few more general points: first, “this looks like what I know is a NP-hard problem” is no reason to assume something is actually hard (never mind infeasible) in practice, even if you actually want optimality – hardness reductions work the other way round, and this is by no means the only instance of NP-hard subproblems *of bounded size* that I’ve run into, which are a very different beast. Second, exploiting even some very basic symmetries can sometimes take combinatorial optimization problems from “never going to happen” to “that’ll be 5 minutes”, so it’s worth looking. Third, *computers are fast*. Trying on the order of 100,000 things if said trials don’t take long is just not that big a deal and hasn’t been for a long time. For that matter, trying 4 billion things has also been entirely practical for a while, as long as individual trials are in the “100s to 1000s of cycles” range (i.e. don’t try this with slow interpreted languages) and you have a few cores. For the past 15 years or so, pretty much every unary function on 32-bit inputs (especially floats) and every binary function on pairs of 16-bit inputs, I’ve just tested exhaustively on all possible inputs unless there was a very compelling reason why this wasn’t possible.

You are weirdo :D