---
title: Phacelle - Cheap Directional Noise
url: https://blog.runevision.com/2026/01/phacelle-cheap-directional-noise.html
published: '2026-01-22'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

## Phacelle - Cheap Directional Noise

While working on a novel erosion algorithm last fall (which I'll release at a later time), I developed a directional noise function in the process, which combines various traits of other ones. Since I haven't come across one quite like this, I'll share my findings here. I call it Phacelle Noise, a portmanteau of phase and cell.

Update: After discussing with two of the authors of Phasor Noise, I've added a section at the end about the ways in which Phacelle Noise differs from Phasor Noise.

[this Shadertoy](https://www.shadertoy.com/view/t3dyWl).

![](../../assets/67e0bdf15e971571.png)

I ended up making two versions, but let's start with *Simple Phacelle Noise*. For each point, it takes a 2D vector as input, which indicates the direction that stripes should be aligned with at that point. As output it produces another 2D vector from which a phase (or angle) can be reconstructed. Based on this phase, a wide variety of stripe shape profiles can be achieved, for example applying a square wave, a triangle wave, a sawtooth wave, or similar.

It's also possible to use the X or Y component of the output vector directly. These both produce stripes with a sine wave shape profile, a quarter cycle apart (so essentially a cosine and sine).

Even for use cases satisfied by sine wave based stripes, interpolating both cosine and sine waves simultaneously has a significant benefit. See, interpolating multiple kernels of sine waves normally produces a result where the amplitude of the output varies greatly depending on how in phase or out of phase the kernels are. However, when both the interpolated cosine and sine are available, the resulting output vector can be normalized, which ensures both the output sine and cosine waves have constant amplitudes of one.

The other version, *Sampled Phacelle Noise*, is very similar to Simple Phacelle Noise, except that instead of taking the input direction as an input parameter, it samples the input pattern once per cell, which amounts to 16 times per pixel. Before I go more into that, let's look at some pictures.

### Visual comparison with Phasor Noise

With respect to use cases and functionality, the closest other noise function I know of is Phasor Noise ([website](http://thibaulttricard.fr/project_page/phasor_noise/phasor.html), [paper](https://inria.hal.science/hal-02118508)), itself a reformulation of Gabor Noise. But Phacelle Noise works in quite a different way, which appears to be much simpler and computationally cheaper, and produces a bit different results.

Here's a comparison of Phasor Noise (top) with Simple Phacelle Noise (middle) and Sampled Phacelle Noise (bottom):

![](../../assets/67e0bdf15e971571.png)

[this Shadertoy](https://www.shadertoy.com/view/wlsXWf).

![](../../assets/4de09ea0186f1c60.png)

[this Shadertoy](https://www.shadertoy.com/view/t3KczR).

![](../../assets/7628e5287e9be4d9.png)

[this Shadertoy](https://www.shadertoy.com/view/w3ycRw).

To me eyes, these images above look remarkably similar, but there are subtle differences if you look closely. Specifically around areas in the pattern where there are discontinuities in the input direction.

To make the respective handling of discontinuities super obvious, let's use a different input pattern that alternates between horizontal and vertical directions in a checker pattern:

![](../../assets/062d0906d5ef3f30.png)

![](../../assets/0c6254b61d8c8f50.png)

![](../../assets/d8f5482e6704cd17.png)

Here you can see that Simple Phacelle Noise has abrupt discontinuities in its generated stripe pattern, while Phasor Noise and Sampled Phacelle Noise do not. Ultimately it's a matter of personal preference, or use case, which one is preferable. For raw stripey patterns, the discontinuities in Simple Phacelle Noise are probably not desirable. For the erosion use case I worked on, it works well, since the stripe (gully) pattern is masked out in those areas of discontinuities anyway.

The visual difference between Phasor Noise and Sampled Phacelle Noise is harder to put the finger on. It seems the latter has a bit higher tendency to produce broken lines rather than merged ones?

### Performance

Performance-wise, both versions of Phacelle Noise are much simpler and cheaper than Phasor Noise. In Phasor Noise the innermost loop code (in [their provided reference code](https://www.shadertoy.com/view/t3KczR)) runs 5 * 5 * 16 = 400 times per pixel, and the input pattern is sampled in that inner loop, so 400 times per pixel as well. The primary author of the Phasor Noise paper Thibault Tricard pointed me to a [corrected implementation](https://www.shadertoy.com/view/NsdGz2) by his colleague Xavier Chermain, which reduces the innermost loop count to 3 x 3 x 16 = 144 times per pixel.

On the other hand, the innermost loop code in Phacelle Noise runs 4 * 4 = 16 times per pixel. The input pattern is sampled only once per pixel for Simple Phacelle Noise (where it's simply passed as an iput parameter) and 16 times per pixel (that is, one sample per loop) for Sampled Phacelle Noise.

| Noise | Loops per pixel | Samples per pixel |
|---|---|---|
| Phasor (
|

**400**(5 x 5 x 16)**400**(one per loop)[Shadertoy by Xavier Chermain](https://www.shadertoy.com/view/NsdGz2))

**144**(3 x 3 x 16)**144**(one per loop)[Shadertoy](https://www.shadertoy.com/view/t3KczR))

**16**(4 x 4)**1**(input parameter)[Shadertoy](https://www.shadertoy.com/view/w3ycRw))

**16**(4 x 4)**16**(one per loop)In practise I can also see that both Phacelle Shadertoys run many times faster than the Phasor Shadertoy (when switching them all to use a sample pattern which is not itself computationally heavy). I haven't done a more in-depth performance analysis since I don't have much experience profiling shaders, especially Shadertoys.

In Simple Phacelle Noise, the fact that the input pattern is sampled only once per pixel means that it can be passed to the Phacelle Noise function as a simple input parameter. With Phasor Noise (and to a lesser extent Sampled Phacelle Noise), storing the calculated input pattern in a buffer to avoid excessive recalculations is more or less a necessity (if it's not trivial), while no such buffer is needed with Simple Phacelle Noise. This also makes it easier to make the Simple Phacelle Noise implementation fully self-contained and reusable, since it does not need access to evaluate another function or buffer.

### Function lineage

I didn't actually know of Phasor Noise when I implemented Phacelle Noise (the simple variant), and I felt very clever for coming up with the idea that by interpolating kernels of both cosine and sine waves simultaneously, the interpolated result can be interpreted as a vector that can be normalized, and from which a phase can be reconstructed.

Phacelle Noise is derived from a function called `erosion` in this 2018 [Eroded Terrain Noise Shadertoy](https://www.shadertoy.com/view/MtGcWh) by user *clayjohn*. This function interpolates kernels of both cosine and sine waves, but the sine part is multiplied with a vector largely orthogonal to the stripe direction (but slightly different per kernel). Calculating both cosine and sine here has nothing to do with normalization or phase, but is rather done to get both a stripe pattern and its analytical derivative. The stripe pattern is used to carve gullies in a terrain based on the slope of the terrain, and the derivatives (the slope of the gullies) are used to further produce more gullies, branching out in a fractal manner.

In 2023, user *Fewes* made a refined presentation of clayjohn's erosion technique in this [Terrain Erosion Noise Shadertoy](https://www.shadertoy.com/view/7ljcRW). While the core technique was kept mostly the same, Fewes did simplify the vector multiplied onto the sine component of each kernel, making it the same for all the kernels.

My own erosion work in 2025 was based on Fewes' version as a starting point. The sine component being premultiplied with a vector makes normalization and phase extraction less straightforward. It's nevertheless what I did initially, since my use case was erosion too, and I needed the derivatives. However, I eventually realized that there's no need for the direction vector to be premultiplied onto each kernel, as multiplying it onto the interpolated result is fully equivalent. This makes it easy to get the best of both worlds, both clean interpolated cosine and sine waves, and a simple way to get the derivatives too.

Digging further back, clayjohn's erosion function was derived from a function called `gavoronoi4` is this [Gavoronoise Shadertoy](https://www.shadertoy.com/view/llsGWl) by user *guil*. This function produces stripes by interpolating kernels of cosine only, and the stripe direction is global rather than variable per pixel.

In turn, Gavoronoise Noise was inspired by Gabor and Voronoi Noise. Gabor Noise because it interpolates stripes produced by sine waves, and Voronoi Noise – specifically this [Voronoi Shadertoy](https://www.shadertoy.com/view/Xd23Dh) by user *iq* is quoted as a source – because it interpolates a "moving window" of cells, such that an infinite pattern of cells can be achieved while sampling only a finite number of cells at a time (typically 3 x 3, 4 x 4, or 5 x 5).

### Readability

Regardless of whether Phacelle Noise is actually anything new (which will be discussed in the section following this one), I bet that my implementation is easier to read and understand.

See, most Shadertoys read to me as if the authors thought they were in an obfuscation contest. Variables are commonly one or two letters long, and it's your lucky day if there's even just a word or two of comments. This makes a lot of this code opaque to me. It's cumbersome having to reverse engineer what each variable means, and I'll have forgotten what the first one means once I'm done figuring out the third one.

It's here that I'll admit I don't actually understand how Phasor Noise works, despite having stared at the code for it for some time. I came away with certain conclusions (like the number of iterations and input pattern samples), but far from a full picture. I don't know what the innermost loop actually does.

Some of this culture of compact, non-verbose variable names might inherit from traditions in mathematical notation, where every variable is a single letter or symbol only, which similarly makes mathematical formulas (a frequent occurance in papers about graphics) often appear opaque to me. It's here that I'll admit I also read the [paper on Phasor Noise](https://inria.hal.science/hal-02118508), but that didn't help me understand it either. I mean, I understand the phase part perfectly, but not the part about how exactly kernels are computed and interpolated, and what those 400 inner loop iterations are needed for.

Mathematical notation is tricky to reform away from single-letter variables (even if there was willingness), since sequences of letters right after each other are interpreted as variables being multiplied. Except when they're not, as in `sin`, `cos`, and a host of other function names that are somehow allowed to be multi-letter by convention.

But the way I see it, with code there's no excuse not to make it as readable as possible without the reader having to resort to guesswork and reverse engineering.

So in my own Shadertoys I try to use as descriptive variable names I can, and I strive to add plenty of comments. And in that way, I hope my implementation of Phacelle Noise will be helpful to some people out there.

### How Phacelle Noise differs from Phasor Noise

Is Phacelle Noise different from Phasor Noise?

Right after posting the first version of this blog post, I pinged Fabrice Neyret – prolific Shadertoy user and a co-author on the Phasor paper (and many others) – in the Shadertoy Discord server, and said I'd love to hear his input if he got a chance to take a look. Fabrice in turn pinged the first author of the Phasor paper, Thibault Tricard, to bring him into the conversation too.

I started the conversation this way:

There's two things I'm kind of wondering. One is how Phasor noise works, since I can't quite figure it out based on the Shadertoy code or the paper. There is an inner loop that does something with impulses, but I don't understand what it is?

The other is – I'm not in the academic world, nor super aware of all the various noise types that's been shared on Shadertoy over the years. And I'm wondering whether the Phacelle noise I just shared is functionally identical to some existing approach out there, that I just didn't happen to come across.


A rather long discussion ensued, where I gradually understood Phasor Noise better, and formed a clearer view about to which degree Phacelle Noise is new.

In the following, I'll refer to the "cells" in Phacelle Noise as "splats", since this seems to be one established terminology. ("Kernel" is another term for the same thing, but it can mean other things in graphics too.) "Cells" instead refers to the square grid cells that the "splats" are randomly placed inside.

As to my question about impulses, I understood from the conversation that "impulses" simply means the number of splats per square cell, since Phasor Noise places more than one of them per cell.

#### Difference in how kernel orientations are handled (for Simple Phacelle Noise)

Some parts of the discussion was specifically about Simple Phacelle Noise, since it's more different from Phasor Noise than Sampled Phacelle Noise is.

In the Phasor paper, the description includes "kernels of different frequencies, orientation, bandwidth and amplitudes may be summed". But in the 'one sample per pixel' approach used in Simple Phacelle Noise, the different kernels do not have different orientations. For a given point being evaluated, all kernels have identical orientation, which is the orientation of the input pattern at the currently evaluated point. Rather, the different stripe directions over space come from all the kernel orientations changing *in unison* as a function of the input direction at the currently evaluated point.

Thibault noted that it is indeed different from what the paper describes, although figure 20 in the Phasor paper uses this technique. He said it's a trick that was given to him by his PhD advisor at the time, and mused that it might be what is sometimes called "ghost knowledge": Knowledge that is present somewhere in the epistemic community, but is not really written down anywhere. Later he went on to try to find out which paper it was first described in, but it is in any case not described in the Phasor paper, or consistent with how that paper describes Phasor Noise.

I somewhat disagree with calling it a mere trick, as it makes the whole thing work in a different way, which is in opposition to what the paper describes. It has completely different properties in terms of qualities of the output, and which use cases it's suitable for.

Fabrice said that the difference in output is only notable "in the case where the vector field violates the requirement of changing slower than the sine wavelength" and that "In theory you should pre-filter it (which is not easy). After a while there would be little difference between the two approaches." But this "requirement" makes a lot of assumptions, and I reject it being universally relevant. I pointed out that in use for erosion, it's actually advantageous that the output changes abruptly around e.g. a mountain peak rather than always changing smoothly. Hence the qualities of the output are just *different*. Whether one is better than the other depends on the use case.

Besides the visual difference in output, it also makes a big difference in which setups are viable. Consider a use case where you need to chain many directional noise invocation after each other, each new one dependent on the output from the last. With an implementation that samples the input pattern per splat, this would require a separate buffer for each invocation, or else each "layer" would contribute to a combinatorial explosion of samples that would be completely infeasible to run.

Whereas with Simple Phacelle noise it's trivial. No buffers are needed, and no combinatorial explosion happens. The computational complexity scales simply linearly with the number of invocations.

In the end I suggested that it may simultaneously be a "trick" to an existing technique in one context, and in another context be the primary technque in its own right, and Thibault said that he was fine with that.

#### Speed optimizations

Phacelle Noise is (in its current implementations) hardcoded to sample 4 x 4 splats, randomly placed inside 4 x 4 square cells. It makes the most of those samples, producing results that often look similar to Phasor noise implementations that use an order of magnitude more samples. Furthermore, the fact that Phacelle uses only one splat per square cell differs from the Phasor Noise implementations I've seen, which have invariably used multiple splats per cell. Using only one splat per cell produces a distribution that's more evenly spread out (on average).

In practise, when I tried to reduce the number of samples in the Phasor implementations I saw, the results got worse than Phacelle Noise long before the number of samples got near to 16.

Apart from that, in the Phacelle Noise implementations I've put some effort into moving as many calculations as possible outside of the loops for performance reasons, while the Phasor implementations I saw repeat a lot of identical calculations for each sample.

#### Avoidance of artifacts caused by discontinuities in the splat weight functions

Phasor noise uses Gaussian functions for weighting its splats. And those functions never reach zero at any distance from the splat center. This works well for implementations that always sample all splats. But for implementations that only sample the nearest splats (for example because there are infinite splats), it creates artifacts because of discontinuities in the *effective* weight functions.

In the implementations where splats are divided up into square grid cells, the artefacts appear along the grid lines. It may not be visible in most presentations, but I've seen these artefacts clearly in terrain height use cases I've worked on.

This is why I subtract a value from the `exp` weight function ([Desmos demonstration here](https://www.desmos.com/calculator/jb2w4dpeo0)), chosen such that it ensures the weight function gradually goes down to zero, and reaches it without discontinuities at the exact minimum distance from the evaluated point where splats may stop being evaluated. Fabrice said this is a common fix to apply to weight functions. Nevertheless it was not described in the Phasor paper or present in Phasor implementations I've been pointed towards, so it's a practial implementation difference between Phasor (as described) and Phacelle.

#### API surface and ease of use

I must say that although everyone involved did their best to be helpful and constructive, there was also a lot of friction in the conversation in general. Occasionally I would see comments dropped outside of the Discord conversation on my Shadertoys [here](https://www.shadertoy.com/view/tXGcWR) and [here](https://www.shadertoy.com/view/t3KczR), and they may give a bit of an impression of what I mean.

I felt that we were often talking past each other. In the Discord conversation, I tried to put that into the following words:

It seems you approach the concepts we're discussing mostly in terms of abstract classification. My own interest however is more rooted in concrete functionality and user experience, and as such is centered around things like ease of use, applicable use cases, API surface design, proper documentation, etc.

And in a lot of Shadertoy implementations I've seen of Phasor noise, the ease of use has been very poor for me. I didn't understand the code due to few or no comments, and there was often not even a clear seperation between code that's noise implementation and code that relates to presentation. This makes it very hard for someone who's not intimately familiar with the technique to just copy the noise function into another Shadertoy and use it there.

Case in point, I still haven't seen any Phasor noise function that takes the pattern direction as an input parameter; it always seems to be hardcoded into the function itself in one way or another.

To me, user experience, API design, etc. matters a lot, and is in itself justification to give things names. As a parallel example, I know of several libraries that does Voronoi tesselation, but they have completely different API design and functionality. Some are useful to me while others are useless. And it's pracical for me to be able to refer other people to the ones I find useful, and not just tell them to "use Voronoi tesselation", as there are a lot of details that matter beyond the basic technique.

As such, since the API design, possible use cases, characteristics and documentation of my Phacelle implementation is quite different from any Phasor noise implementations I've seen, I find it useful and practical that I and others can refer directly to this implementation by name.


Thibault replied that he agreed that Phasor implementations that are currently available are not well documented, and that most of them are code from the Siggraph deadline that have barely been cleaned up since. He added that he might create a cleaner example one day when he'll get some time.

#### Verdict from two of the Phasor authors

Thibault's verdict was that Phacelle Noise gives results visually similar to Phasor in 2D, but cheaper, although it does not provide any of the frequential guarantee given by Phasor, which he said was very important for texture synthesis and for anisotropic filtering. He said it also doesn't offer control over the isotropy of the generated noise (an aspect of the Phasor Noise paper which is not utilized in the Phasor implementations I compare Phacelle Noise with).

He concluded that if the question is whether anybody did exactly the same thing, the answer would be no, but that Phacelle did not do anything new that warranted publishing. Which is fine, as I have no intention of publishing.

Fabrice added that what I propose is a discussion about technical choices, and that while he believed no scientific reviewer would agree it's a new method, it could totally be accepted as such in practical (and lovely) venues like the JCGT journal (a follow-up to the Graphics Gem book series), which is interested in how to make things usable. (But again, I'm not interested in publishing.)

### Links

Implementations used for reference:

- My
[Simple Phacelle Noise Profile](https://www.shadertoy.com/view/t3KczR)Shadertoy. - My
[Sampled Phacelle Noise Profile](https://www.shadertoy.com/view/w3ycRw)Shadertoy. - The original
[Procedural Phasor Noise Profile](https://www.shadertoy.com/view/wlsXWf)Shadertoy by Thibault Tricard (Phasor first author). - My forked
[Phasor Noise Profile](https://www.shadertoy.com/view/33yyWR)Shadertoy, which has additional sample patterns, such as the checker one. [Phasor noise](https://www.shadertoy.com/view/NsdGz2)Shadertoy by Xavier Chermain (a colleague of Phasor author Thibault Tricard) which corrected some mistakes in the original Phasor Shadertoys.

Related Shadertoys I'm aware of:

[Gabor/Phasor flow](https://www.shadertoy.com/view/3tKGWR)Shadertoy by Fabrice Neyret (Phasor co-author).[Gabor 4: normalized](https://www.shadertoy.com/view/XlsGDs)Shadertoy by Fabrice Neyret (Phasor co-author).[Textured Torus , phasor example](https://www.shadertoy.com/view/wtj3RV)Shadertoy by Thibault Tricard (Phasor first author).

Presentations and artistic experiments based on Phacelle Noise:

[Phacelle Noise Animation](https://www.shadertoy.com/view/t3dyWl)Shadertoy by me.[Luminescent Growth](https://www.shadertoy.com/view/tXGcWR)Shadertoy by me.[Spiked Fire Lines](https://www.shadertoy.com/view/3XGyDz)Shadertoy by me.

## 1 comment:

Thanks for the write-up. Learned more about noise which I'm always interested in :D

Post a Comment