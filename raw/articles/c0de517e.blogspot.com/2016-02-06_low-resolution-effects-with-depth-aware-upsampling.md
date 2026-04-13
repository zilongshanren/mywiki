---
title: Low-resolution effects with depth-aware upsampling
url: http://c0de517e.blogspot.com/2016/02/downsampled-effects-with-depth-aware.html
published: '2016-02-06'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I have to confess, till recently I was never fond of doing half or quarter res effects via a bilateral upsampling step. It's a very popular technique, but all the times I tried it I found it causing serious edge artifacts...

On Fight Night Champion I ended up shipping AO and deferred shadows without any depth aware upsampling (just separating the ring and fighters from the background, and using a

[bias towards over-shadowing](http://c0de517e.blogspot.ca/2011/09/fight-night-champion-gdc.html)); Space Marines ended up shipping with a bilateral upsampling on AO ([but no bilateral blurring or noise](http://c0de517e.blogspot.ca/2012/10/notes-on-optimizing-deferred-renderer.html)) but it still had artifacts. In the end it sort-of worked, via some hacks that were good enough to ship, but that I never really understood.
For Call of Duty Black Ops 3 we needed to compute some effects (volumetric lighting) at quarter-res or less, to respect the performance budgets we had, so depth-aware upsampling was definitely a necessity, so I needed to investigate a bit more into it.

A quite extreme example of "god rays" in COD:BO3

I found a solution that is very simple, that I understand quite well, and that works well in practice. I'm sure it's something many other games are doing and many other people discovered (due to its simplicity), but I'm not aware of it being presented publicly, so here it is, my notes on how not to suck at bilateral upsampling:

![]() |

**1) Bilateral weighting doesn't make a lot of sense for upsampling.**

The most commonly used bilateral upsampling scheme works by using the same four texels that would be involved in bilinear filtering, but changing their weights by multiplying them by a function of the depth difference between the true surface (high res z-buffer) and their depths (low-res z-buffer).

This method makes little sense, really, because you can have the extreme case where the bilinear weights select only one sample, but that sample is not similar to the surface depth you need at all! Samples that are not detected to be part of the full-res surface should simply be ignored, regardless of how "strongly" biliear wants to access them...

A better option is to simply -choose- between bilinear filtering or nearest depth point sampling, based on if the low-res samples are part of the high-res surface or not. This can be done in a variety of ways, for example:

- lerp(bilinear_weights, depth_weights, f(depth_discontinuity)) * four_samples

- lerp(biliear_sample, best_depth_sample, f(depth_discontinuity))

- bilinear_fetch(lerp(bilinear_texcoords, best_depth_texcoords, f(depth_discontinuity)))

Where the weighting function f() is quite "sharp" or even just a step function. The latter scheme is similar to

[nVidia's "nearest depth sampling"](http://developer.download.nvidia.com/assets/gamedev/files/sdk/11/OpacityMappingSDKWhitePaper.pdf), it's the fastest alternative but in Black Ops 3 I ended up sharply going from bilateral to "depth only" weights if a too big discontinuity is detected in the four bilinear texels.**2) Choose the low-res samples to maximise the chances of finding a representative.**

It's widely known that a depth buffer can't be downsampled averaging values, that would result in depths that do not exist in the original buffer, and that are not representative of any surface, but "floating" in between surfaces at edge discontinuities. So either min or max filtering is used, commonly preferring nearest-to-camera samples, with the reasoning that closest surfaces are more important, and thus should be sampled more (McGuire tested various strategies in the context of SSAO, see

[Table 1 here](http://graphics.cs.williams.edu/papers/SAOHPG12/McGuire12SAO.pdf)).
But if we think in terms of the reconstruction filter and its failure cases, it's clear that preferring a single set of depths doesn't make a lot of sense. We want to maximize the chance of finding, among the texels we consider for upsamping, some that represent well the surfaces in the full resolution scene. Effectively in the downsampling step we're selecting on points we want to compute the low-res effect, clearly we want to do that so we distribute samples evenly across surfaces.



A good way of doing this is to chose per each sample in the downsampled z-buffer, a surface that is different from the ones of its neighbors. There are many ways this could be done, but the simplest is to just alternate min and max downsampling in a checkerboard patter, making sure that for each 2x2 quad, if we are in a region that has multiple surfaces, at least two of them will be represented in the low-res buffer.

In theory it's possible to push even more surfaces in a quad, for example we could record the second smallest or second biggest, or the median or any other scheme (even a quasi-random choice) to select a depth (we shouldn't use averages though, as these will generate samples that belong to no surface), but in practice this didn't seem to work great with my upsampling, I guess because it reduces spatial resolution in favour of depth resolution, but your mileage may vary depending on the effect, the upsampling filter and the downsampling ratio.

![]() |

when there is no good point sample in the 2x2 neighborhood.



**Further notes.**

**The nearest-depth upsampling with a min/max checkerboard pattern downsampling worked well enough for Black Ops 3 that no further research was done, but there are still things that could be clearly improved:**


- Clustering for depth selection.

A compute shader could do actual depth clustering to try to understand how many surfaces there are in an area, and chose what depths to store and the tradeoffs between depth resolution and screenspace resolution.

- Gradients.

Depth discontinuity in the upsampling step is a very simplistic metric, more information can be used to understand if samples belong to the same surface, like normals, g-buffer attributes and so on.

- Wider filters.

Using a 2x2 quad of samples for the upsampling filter is convenient as it allows to naturally fall back to bilinear if we think the samples are representative of the high-res surface, but there is no reason to limit the search to such neighborhood, wider filters could be used, both for higher-order filtering and to have better chances of finding representative samples.

- Better filtering of the representative depth samples.

There is no reason to revert to point-sampling in presence of discontinuities (or purely depth-weighted sampling), it's still possible to reject samples that are not representative of the surface while weighting the useful ones with a filter that depends on the subtexel position.

Special cases could be considered for horizontal and vertical edges, where we could do 1d linear interpolation on the axis of the surface. Bart Wronski has something along these lines

[here](http://bartwronski.com/2014/10/18/csharprenderer-framework-update/)(and the idea of baking an UV offset to be reused by different effects also allows in general to use more complex logic, and amortize it among effects).
- "Separable" bilateral filters.

Often when depth-aware upsampling is employed we also use depth-aware (bilateral) filters, typically blurs. These are often done in separate horizontal/vertical passes, even if technically such filters are not separable at all.

This is particularly a problem with depth-aware filters because the second pass will use values that are not anymore relative to the depths in the low-res depth buffer, but result from a combination of samples from the first pass, done at different depths.

The filter can still look right if we can always correctly reject samples not belonging to the surface at center texel of a filter, because anyway the filtered value is from the surface of the center texel, so doing the second pass using a rejection logic that uses attributes (depth...) at the center of the filtered value sort-of works (it's still a depth of the right surface).

In practice though that's not always the case, especially if the rejection is done with depth distances only, and it causes visible bleeds in the direction of the second filter pass. A better alternative in these cases (if the surface sample rejection can't be fixed...) is to do separate passes not in an horizontal/vertical fashion but in a staggered grid (e.g. first considering a NxN box filter pass then doing a second pass by sampling every N pixels in horizontal and vertical directions).

## 2 comments:

Bilinear weights are just different metric that you can use while doing the bilateral. They give you additional information about how the surface you are reconstructing is related to the actual surface. You can have similar issues with depth/color metric ie. they miss the "true" surface.




I like the checker idea though. What i used to do back in the day was to generate min/max values (ao, ambient etc) on smaller res and use min/max low res depth buffer to blend between those values while upsampling. It worked way better then doing pure bilateral upsampling and it wasnt that big of a performance hit since it usually vectorized pretty nicely (ps3/x360).

Yes min/max values work well especially if the function you're evaluating is not discontinuous/is monotone respect to depth. Bilinear weights per se are fine, what is not great is to use them by just multiplying them with the depth weights.

Post a Comment