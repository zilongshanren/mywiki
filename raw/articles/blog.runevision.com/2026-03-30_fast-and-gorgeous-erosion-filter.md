---
title: Fast and Gorgeous Erosion Filter
url: https://blog.runevision.com/2026/03/fast-and-gorgeous-erosion-filter.html
published: '2026-03-30'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

## Fast and Gorgeous Erosion Filter

This blog post and the [companion video](https://www.youtube.com/watch?v=r4V21_uUK8Y) both explain an erosion technique I’ve worked on over the past eight months. The video has lots of elaborate animated visuals, and is more focused on my process of discovering, refining, and evolving the technique, while this post has a bit more implementation details on the final iteration. I suggest watching the video first, but it’s not required. You can also skip right to the [links](https://blog.runevision.com#links) at the end.

In the real world, rainfall on mountains tends to converge into water streams and rivers, which carve gullies in the mountain sides. These gullies may form branching patterns, as smaller water streams merge into larger ones. And the gullies often butt up against each other, leaving sharp ridges dividing them.

But when generating virtual landscapes, the simulation of countless water drops is slow. It’s not very suitable for generation in chunks either, which means it’s not practical to use when generating landscapes that are too large to generate all at once.

This means techniques are sought after, which can produce the appearance of erosion without having to deal with simulating the process of it. This post is about such a technique.

![](../../assets/5b25cb1586d590c4.png)

[Advanced Terrain Erosion Filter](https://www.shadertoy.com/view/wXcfWn)Shadertoy by me.

It’s essentially a special kind of noise which produces gorgeous branching gullies and ridges, while still allowing every point to be evaluated in isolation, which means it’s fast, GPU-friendly, and trivial to generate in chunks.

Furthermore, rather than defining the landscape entirely, it can be applied on top of any height function, essentially applying erosion on top as a filter.

### Background

There’s a website called Shadertoy where people create and share standalone shaders. A shader is a program that runs on the GPU, which can be used to determine what a virtual surface should look like, or for various other effects, or even entire scenes.

In 2018 a user called Clay John ([Bluesky](https://bsky.app/profile/clayjohn.bsky.social)) posted a Shadertoy called [Eroded Terrain Noise](https://www.shadertoy.com/view/MtGcWh). He wrote:

This shader is the result of a long time dreaming of a noise function that looked like eroded terrain, complete with branching structure, that could be run in a single pass pixel shader. I wanted to avoid anything simulated because then you cannot easily make infinite terrains.

That dream sounds familiar, but Clay John actually made it work. His Shadertoy is the original version of this technique. Hats off to him.

Later, in 2023, a user called Fewes, aka Felix Westin ([website](https://fewes.se/)), posted a Shadertoy which built on top of the one by Clay John. [Fewes’ version](https://www.shadertoy.com/view/7ljcRW) slightly tweaked how the erosion effect worked, and presented it in a vastly more polished way.

![](../../assets/db69831db52765c8.png)

[Terrain Erosion Noise](https://www.shadertoy.com/view/7ljcRW)Shadertoy by Felix Westin (Fewes).

In 2025 to 2026 I’ve implemented my own versions of the technique. First I made a version that addresses a few shortcomings of the original technique, and has more intuitive parameters. Eventually I developed a version that works in a completely different way, which produces crisper gullies and ridges and has more expressive parameters. But before going over the differences, let’s start with the basics of the original technique.

### The basic idea

We start with a height function where we know not just the height at each point, but also the gradient, meaning the direction and steepness of the steepest ascent. Water flows in the opposite direction, so you can think of the negative gradient at each point as an arrow showing the direction that water would flow down the slope.

![](../../assets/c61d606f34c06dcf.png)

Let’s start simple, with a slanted surface, where the gradient is the same everywhere.

We use the gradient to add stripes that run along this direction. The stripes produce alternating gullies and ridges, that could plausibly have been created by water eroding the terrain.

![](../../assets/7bcac171503860ce.png)

The sides of these gullies and ridges come with their own gradients, which are added to the original to produce new combined gradients.

We can then repeat the whole thing again at a smaller scale: Add smaller stripes which run along the new slopes. These form new gullies and ridges which naturally branch out at an angle from the first ones.

By convention, each repetition is called an octave. Add a few more octaves, and we should be done, right?

![](../../assets/65170324405fe013.png)

Except – it’s not quite as simple as I just made it sound.

If we apply the erosion to our original height function, where the gradient is *not* the same everywhere, we get a chaotic mess. Even if we show it with just a single octave, it’s still full of chaotic gullies that are often not aligned with the slopes at all. What’s going on?

![](../../assets/559d2b6683a4066e.png)

### Generating stripes

To rotate the stripe pattern, we have to choose some pivot point to rotate it around.

![](../../assets/df905cf2fe207756.png)

The problem is the rotation around this pivot point will create increasingly large distortions in the output the further away from the pivot point we are. This is because changes in the rotation angle not only changes the direction of the stripes at a given point, but also shifts *which* stripe is under that point.

The approach used in the erosion implementation is to divide the pattern into cells that each have their own pivot point for the stripes. If you imagine a square grid, there’s one cell per grid square, with its pivot placed randomly inside the square, similar to simple [Worley noise](https://en.wikipedia.org/wiki/Worley_noise).

We still get a bit of distortion, but it’s not too bad, since the pivot point is never too far away. At least as long as the gradient of the height function doesn’t change too drastically within a single cell.

![](../../assets/5fa381fb00000105.png)

![](../../assets/ca8c08cbd23e3c4e.png)

To ensure smooth results without discontinuities, we blend the stripes of neighboring cells. The stripes are essentially extruded sine waves, specifically a cosine wave for the height offset and a sine wave for the derivative (slope).

![](../../assets/0ab07deb118c28ca.png)

The reason the stripes blend so nicely together even when not aligned, is that if you blend two unaligned sine waves, you just get a new sine wave with a smaller amplitude.

![](../../assets/2fd6ea39edda8945.png)

The cell size has a big effect. If we choose a cell size that’s large compared to the stripe width, we get significant distortion issues, just like when we used a single pivot point. If we choose a small cell size, there’s barely room for any stripes, and we get a kind of grainy noise instead.

If we make the cell size even smaller relative to the stripe thickness, the pattern begins to be all white. Or in terms of ridges and gullies, it’s all ridge and no gully. This is because each cell uses a stripe pattern with a white stripe in the center.

### Preserving peaks

When I talk about peaks and valleys, I’m referring to the local maxima and minima of the original height function, whereas when I talk about ridges and gullies, I’m referring to the local maxima and minima of the gully stripes applied in each octave of the erosion filter.

Now that we can generate stripes aligned with any gradient, we can apply our erosion effect to the height function without getting chaotic distortions.

However, although we’ve now got nice gullies on the mountain sides, the mountain peaks look wrong. They barely look like peaks at all.

![](../../assets/4c4507376f6b2342.png)

That’s because the peaks may be located anywhere in our stripe pattern, and they get arbitrarily lifted or lowered based on that. Furthermore, there’s an issue whenever the surface steepness approaches zero, which happens at peaks and valleys. When the slope is zero, the gradient has no defined direction, so the direction of the gradient changes abruptly around those spots, which creates chaotic stripe patterns in the surrounding area.

There are two ways we can address this, and both are based on the steepness of the slopes. There’s the original approach used by Clay John and Fewes, which I call *the frequency approach*, and there’s an alternative approach I came up with, which I call *the fade approach*.

### The frequency approach

The original approach used by Clay John and Fewes is to make the stripe frequency proportional to the slope, so the stripes are thicker, the flatter the terrain is.

At peaks and valleys, where the steepness is zero, the stripes become infinitely thick. And because each cell has a white stripe in the center, this means mountain peaks and valleys, where the slope is zero, always land on the part of the stripe pattern that corresponds to a ridge, and never a gully.

This works great for mountain peaks, but I discovered that it unfortunately causes valleys to have bulges at the bottom, since they land on "ridges" in the stripe pattern too. This is not visible in their Shadertoys, because they have faded out the erosion at lower altitudes. And this workaround is great if you want smooth valleys.

However, if you apply the erosion at equal strength everywhere, the bulges at valleys appear, and it means you can’t get crisp, V-shaped valleys.

![](../../assets/00863c53b5d7e0f5.png)

You can find [my Shadertoy here](https://www.shadertoy.com/view/33cXW8) based on the frequency approach. It’s similar to the one by Fewes, but is refactored to have more intuitive parameters.


### The fade approach

I came up with a different approach, which is to keep the stripe widths consistent and instead fade out the stripes where the steepness approaches zero. If we fade towards "white" – the maximum value of the gully octave – we get a similar effect as with the frequency approach, that the shape of peaks is preserved, but there are bulges at the bottom of valleys.

Now, if we fade towards "black" instead – the minimum value of the gully octave – we don’t get any bulge at the valleys, but instead we get a crease at the peaks. But if we fade towards a value that goes from black at mountain valleys to white at mountain peaks, we can get nice crisp peaks and valleys at the same time.

![](../../assets/4d2d295ccd8c7827.png)

In my implementations, I let it be up to the user to supply this *fade target* value as an input parameter to the erosion function, for example based on altitude.

For a height value `h` at the current point, it could look like this, if the expected height range goes from `valleyAlt` to `peakAl`t:

float inverse_lerp(float a, float b, float v) { return (v - a) / (b - a); }

// Convert the altitude to a value between -1 and 1. float fadeTarget = inverse_lerp(valleyAlt, peakAlt, h) * 2.0 - 1.0;

The fade approach has a different issue that needs to be carefully handled. It initially seemed to create visible folds – also called discontinuities – caused by abrupt changes in the gradient directions around the peaks and valleys. But I later found out that this can be addressed by using an appropriate shaping function on the slope.

From early on, I had been raising the steepness of the slope to a power of 0.5, which is equivalent to taking the square root of the slope. This applies erosion more evenly than if we used the slope directly. Unfortunately it produces sharp discontinuities at peaks and valleys. This is because the square root curve starts off vertically, so as the slope increases from zero to even the tiniest slant, the erosion immediately increases drastically.

![](../../assets/0f1dd6b6e7517399.png)

0.5.

![](../../assets/262e03645a846555.png)

2.

But there are many other functions we can use to shape the erosion. The one I ended up using is to flip the curve vertically by subtracting it from one, then raising it to a power of two, and then flipping the result back.

float ease_out(float t) { // Flip by subtracting from one. // The saturate function clamps between 0 and 1. float v = 1.0 - saturate(t); // Raise to a power of two and flip back. return 1.0 - v * v; }

This has a somewhat similar shape as the square root – in fact it’s mirrored around the diagonal – but the curve starts off much more moderately. This mostly removes the appearance of discontinuities, especially when we layer multiple octaves of gullies.

With this tweak, the fade approach works just as well as the frequency approach. And unlike the frequency approach, it works well when applying the erosion at full strength everywhere, which can be used to create sharp V-shaped valleys, if desired.

### The quest for crisp, branching gullies

The erosion we’ve got so far looks nice, but the larger gullies and ridges get a little bit lost in the smaller ones. I’d prefer if the gullies at all scales could have crisper ridges and creases, and more clearly show a branching pattern.

To address this, I did a lot of experimentation, and developed three techniques that go hand in hand. I call them stacked fading, normalized gullies, and straight gullies, and I’ll go over each of them in the next sections.

![](../../assets/9708f2bbbeb85eb3.png)

![](../../assets/de05f98d58be93ea.png)

### Stacked fading

We already fixed a problem with crispness earlier. The mountain peaks and valleys didn’t look crisp until we began fading towards black or white for the valleys and peaks respectively. And it turns out we can do something similar for the gullies and ridges.

Let’s establish a few terms first.

I’m calling the value we fade towards the *fade target* and it’s generally expressed in a variable that goes from -1 at valleys to 1 at peaks.

Then there’s the amount we’re fading towards the fade target. We’re doing a weighted average (also known as a lerp or a mix) of the gullies and the fade target, which can be 100% gullies at steep slopes, 100% fade target at flat terrain, or some mix of the two, depending on the slope. We can think of this as a *mask* applied to the fade target, before we layer it on top of the gullies.

When we’ve been talking about *the fade approach*, the fade target and mask have been based on the original height function and its slopes. But just like we don’t want gullies right on top of the mountain peaks or valleys, we also don’t want smaller gullies right on top of the ridges or creases of larger gullies. We can achieve this if we conclude each octave by updating the mask and fade target to also be black and white at that octave’s creases and ridges.

![](../../assets/2241130883d5a74b.png)

*fade target*and

*masks*affects each octave of gullies.

The diagram above may seem daunting, but here’s the gist of it:

- The
*octave 1 raw gullies*are faded towards the*input fade target*based on the*input mask*to produce the*octave 1 faded gullies*. You can think of it as the masked fade target being "overlaid" on top of the octave 1 raw gullies. Nothing new so far. - The
*octave 1 faded gullies*are then used as the new fade target for the next octave. The mask is also updated: From the*octave 1 raw gullies*, a mask contribution is created which is opaque at the creases and ridges, where the slope is zero. The existing mask is layered on top of the new mask contribution to produce the new*combi-mask after octave 1*. - The same steps are repeated for each new octave. The
*octave 2 raw gullies*are faded towards the new*fade target*based on the new*combi-mask*to produce the*octave 2 faded gullies*. These are used as the new fade target, and the mask is updated with a new contribution based on the octave 2 raw gullies. And so on.

In broad terms, each new octave adds more ridges and creases to the terrain surface, which increasingly restricts the surface area where subsequent gullies can have any influence on the surface.

How are new mask contributions combined with the existing combi-mask? Let me start by saying that it was easiest in the diagram above to conceptualize the mask as being applied to the fade target, but in the code it’s actually a mask applied to the gullies, so 0 means all fade target and 1 means all gully. In this form, the new mask contribution can simply be multiplied onto the combi-mask to produce the new combi-mask.

We can furthermore implement a useful control here. By raising the inverse of the combi-mask (meaning its complement) to some power before multiplying it with the new contribution, we can control how detailed the erosion looks. Lower values restrict the effect of higher frequency gullies to steeper slopes.

float pow_inv(float t, float power) { // Flip, raise to the power, and flip back. // The saturate function clamps between 0 and 1. return 1.0 - pow(1.0 - saturate(t), power); }

combiMask = pow_inv(combiMask, detail) * newMask;

![](../../assets/d1938cd3c16ac8d1.png)

### Normalized gullies

One thing that’s holding back crisper ridges and creases is the inconsistent magnitude of the gullies, caused by the interpolation of stripes that may or may not be well aligned.

At one point I realized that since we interpolate both cosine and sine waves in parallel, we can think of each cosine/sine pair as a point on a unit circle, and the interpolated value as a point on a circle too. The interpolated circle point may have shrunk to a radius smaller than one, but it’s trivial to normalize it back to one. And this in turn means that both the interpolated cosine and sine waves have a consistent magnitude of one.

Now, in the actual interpolated stripe function we’ve used up until this point, the sines are multiplied with a vector orthogonal to the terrain gradient in order to calculate the gradient of the slope. But since this vector is the same for all contributing samples, the multiplication can be postponed and applied to the interpolated result rather than to each contributing sample, leaving us free to perform the normalization first.

When straightforward normalization is applied, some curious artifacts appear where ridges and creases join up and form loops. Supposedly, this happens at points where the interpolated waves cancel out completely; something that seems to unavoidably happen with some regularity. On the terrain, this manifests as spiky protrusions (and holes).

However, the loopy artifacts can be avoided if we only normalize lengths above a certain threshold. To avoid discontinuities between normalized and non-normalized gullies, we can use the following approach:

- Scale lengths by a factor
`k`that’s larger than one. - Clamp resulting lengths to one.

I’ve used a factor `k` of 2, such that lengths greater than 0.5 become normalized. This produces a good tradeoff with lots of gullies of consistent magnitude and without loopy artifacts.

![](../../assets/d0aaa21957735349.png)

![](../../assets/ebe7ba073c283255.png)

![](../../assets/3f9e7587e4aa8995.png)

The style of partial normalization I’ve chosen produces second order discontinuities (abrupt changes in slope) in some places, but as it’s not noticeable once multiple octaves are used, I haven’t bothered with a more sophisticated approach.

I figured that the ability to produce directional noise is useful for many other purposes than erosion, so I’ve released the noise function as [Phacelle Noise, which I’ve written about here](https://blog.runevision.com/2026/01/phacelle-cheap-directional-noise.html).

### Straight gullies

Once the ridges and creases got more crisp, another issue became apparent. Smaller ridges and creases would often run along larger ones for a little distance before branching out.

It’s here that the limitations of modeling gullies as extruded sine waves becomes apparent. See, on the side of gullies, the terrain slope is strongly affected by it, pointing sideways away from the ridges. But at the bottom and top of gullies, they have virtually no effect on the terrain slope. So at those points, smaller gullies will simply run parallel to the larger ones.

![](../../assets/ad826f69e03a9379.png)

Since the effect is gradual, smaller gullies tend to curl at the ends, rather than branching off cleanly from the larger gullies. A visualization of the ridges and creases with just two octaves of gullies shows the difference clearly.

![](../../assets/e1900b77aae2f3bc.png)

![](../../assets/e71257082e1d09c3.png)

The effect of non-straight gullies is more subtle on the actual terrain surface. But when carefully comparing the images below, you may find that the first one, which does not have straight gullies, has more instances of ridges with small grooves on top, less instances of gullies branching out at clean angles rather than curving, and an overall texture which feels a bit more stringy and smushy.

![](../../assets/69850d655b09c984.png)

![](../../assets/de05f98d58be93ea.png)

I fixed the issue of non-straight gullies by essentially faking consistent slopes when calculating the slopes used for the gully stripe pattern directions.

We can pretend that the slope of a gully is constant from top to bottom, as if the gullies were extruded triangle waves instead of sine waves. The faked slope is implemented by using the sign of the sine wave that controls the gully slope, rather than using its value directly. That is, if the sine is negative, we use a value of -1, and otherwise a value of 1.

![](../../assets/f7296f43ca257b4a.png)

I also tried making the gullies actually be extruded triangle waves, but due to complex interactions in how the different octaves combine, that just ended up looking worse.

One aspect of the overall erosion technique I haven’t explicitly covered yet is that it outputs not only the heights of the eroded terrain, but also the analytical derivatives. However, those derivatives were never very accurate, whether in Clay John and Fewes’ implementations or my own. They are used internally to calculate the gully directions, but the output derivatives were never actually used for anything.

But even if not accurate, they can still come in handy, so I don’t want to remove support for them. (I actually did begin using them to calculate tree coverage.)

With the *fade approach*, the mask is also used on the derivatives of each octave. They are faded towards a slope of zero rather than the *fade target* value, which is only relevant for heights. But fading the derivatives towards zero at ridges and creases undermines the straight gullies technique.

So I began calculating derivatives in two different ways in parallel. The output derivatives are stored as part of a `heightAndSlope` variable whereas the internal version is stored in a `gullySlope` variable. And while the former is faded towards zero according to the mask, the latter is not.

The faked gully slope does mean that the new straight gullies created based on it have discontinuities at the creases and ridges of the faked slopes, as stripes going in different directions butt right up against each other. This can be seen in the *octave 2 raw gullies* part of the diagram from earlier.

But these discontinuities are fully faded away in the faded gullies used for the output height offset (and output derivatives), so they’re not a problem.

![](../../assets/06fbb13e66c93a6c.gif)

One issue with the slopes remains. For the gullies, we could pretend they’re triangle waves, and calculate the slope of those pretend-triangle-waves according to the frequency and magnitude, but not so with the slopes of the input heights, of which we can assume very little.

If we use the input slope unchanged, the initial gully octave will have a disproportionally large effect near the peaks and valleys, where the input heights are typically rounded and thus have little to no slope contribution. But in the eroded output terrain, the peaks and valleys are typically pointy, with just as steep slopes as elsewhere.

I’ve experimented with a variety of solutions to this, but in the end what produced the best results was to just pretend that the input heights have a specific slope everywhere. This pretend slope can be tweaked to somewhat match the typical slope the eroded terrain ends up having.

It’s a bit ironic that my early work on the erosion technique was focused on making the analytical derivatives more accurate, only to end up giving up on that entirely. But that’s just how a labyrinthine process of discovery sometimes goes.

### New coat of paint

The technique has now changed sufficiently that some tweaking of the parameters is in order, to make the most of the new functionality. While at it, I also found a new spot in the heightmap to focus on. Below is the reference terrain I’ll use going forward, which also includes features covered in the remainder of this article.

![](../../assets/9608df17558fefa8.png)

While not part of the erosion technique itself, it’s also fun to dress up the terrain with nice materials. I’ve been tweaking the logic inherited from the Shadertoy by Fewes, and added bumpy parts to it that evokes trees too. Furthermore, I managed to add little streaks that evoke water drainage using a technique I’ll discuss further down.

![](../../assets/5e93517d35738634.png)

### Pointy peaks

It turns out that normalizing the gullies make the mountains less pointy, keeping more of the rounded shape of the input height function.

At first, I tried to compensate by applying a special function to the input height that made peaks more pointy, prior to passing them to the erosion function. But I later found that there is a simpler solution that can be trivially implemented in the erosion function itself: Simply scale down the gullies part of the faded gullies by some *gully weight* factor (such as 0.5) and compensate by scaling up the erosion strength by the inverse factor (like 2.0).

![](../../assets/77a95ec524df5c61.png)

Pointy peaks are still dependent on the fade target having a value close to 1.0, so in all the example images, the peaks at lower altitudes are less pronounced.

We can look at what happens when the gully weight is reduced to zero. This preserves the overall shape of the eroded mountains, including crisp peaks and valleys, but without all the gullies.

There is a subtle kind of ghosting effect of the gullies present, where ridges and creases alike are turned into all ridges where the original fade target is positive, and all creases where it’s negative. This unhelpfully counteracts half of the intended creases and ridges if very low gully weight values are used, but at larger values there are no noticeable issues.

There are undoubtedly other ways to go around this, but the approach here is simple and works well enough.

### Rounding of ridges and creases

The implemented technique can produce very sharp ridges and creases, but something not quite as sharp is often desired. For example:

- Real mountain peaks and ridges tend to not be razor sharp if you zoom in sufficiently.
- Valleys and the bottom of gullies can get a rounded shape if sediment builds up in them.

For this reason I implemented "edge rounding" with separate control for creases and ridges. As I’ve previously touched upon, the *mask* is based on the slope passed through a shaping function. By chaining a variable-size ease-in function onto this shaping function, rounding of the ridges and creases can be achieved. And by mixing two different rounding values – one for ridges and another for creases – based on the *fade target*, the amount of rounding can be controlled separately for those.

![](../../assets/b9a46cf41c1c54cc.png)

I wanted the rounding to have the same size for gullies of all octaves, so the rounding values are counter-adjusted in accordance with the erosion lacunarity value, which controls how much smaller the gullies are in each octave (typically half the size).

The rounding also affects peaks and valleys stemming from the original height function (and its slopes), but the erosion function doesn’t know about the sizes of the terrain features coming from those, so an input value is provided for tweaking the rounding of those.

### Water drainage

While getting the erosion increasingly crisp, the idea of a holy grail occurred to me: Could the technique model the branching gullies so crisply that it could render little branching river networks? It turns out: Kind of, with some caveats.

Side note: I later learned that the branching streaks on mountain sides I had in mind constitute *dendritic drainage*, which, apart from rivers and creeks, also include channels of snow, sediment, and debris-flow. The colored streaks are often not the water itself, but the leftover rocks and sediment which is colored differently from the surrounding soil or vegetation. Either way, it tends to look like bright lines.

If we ignore the recently discussed gully weights and ridge and crease rounding, then the *fade target* is practically already a map of the ridges and creases in the eroded terrain, once the technique has gone through all the gully octaves. Only, the last octave appears with much thicker lines than the rest, since it hasn’t been filtered through the *mask*. This can be resolved by fading it towards a neutral value of zero / gray based on the mask, resulting in what I call a *ridge map*.

![](../../assets/ba27f39487d67fcf.png)

Now, those recently discussed features do undermine the ridge map, so in order to avoid having to choose between one and the other, we can keep track of two copies of the *fade target* and *mask* in parallel, and process the ones for the ridge map without those features.

Here’s a visualization of the ridge map on the terrain:

![](../../assets/107f4e75de062cd5.png)

With the ridge map, it’s easy to draw little lines at the bottom of all the gullies that resemble dendritic drainage. Here’s the image of the textured terrain again:

![](../../assets/5e93517d35738634.png)

It’s not a perfect solution, since the interpolated stripes we use for the gullies cannot consistently produce unbroken lines. So sometimes a gully, and the drawn water drainage at its bottom, just stops halfway down a mountainside rather than following through all the way down to the lowest reachable point. Nevertheless, it looks nice and can be sufficient for use cases that don’t require accuracy in this regard.

### Future work

You can see my final iteration of the technique in my Shadertoys [Advanced Terrain Erosion Filter](https://www.shadertoy.com/view/wXcfWn) and [Mouse-Paint Eroded Mountains](https://www.shadertoy.com/view/sf23W1).

As has hopefully been clear, the erosion technique I’ve described in this post is highly malleable. Compared to the original version by Clay John and Fewes, I’ve modified it to a point where its internal workings, capabilities, and characteristics are entirely different.

While I don’t have plans to further work on this technique myself, I find it likely that others will, given how open-ended the nature of the technique is, and how ripe it is with potential.

In my work with the technique, I’ve simply aimed to make the eroded terrain look good to my eyes, loosely using a bunch of reference images for inspiration.

An interesting jumping off point for future work could be to try to use the technique to emulate a variety of specific eroded terrain types, each based on different references. The input parameters should allow for a wide variety of looks on their own, especially when considering most of them can be varied based on other variables. If the technique then falls short of being able to emulate certain terrain characteristics, that could point the way towards potential future improvements.

I’ve released my code under the Mozilla Public License v2 in order to encourage further sharing of improvements. I’m looking forward to seeing how the technique evolves in the future!

*Based on feedback after publication I've added some additional notes after the links section.*

#### YouTube videos

Some things are easier to explain in motion.

- My video
[Fast & Gorgeous Erosion Filter Explained](https://www.youtube.com/watch?v=r4V21_uUK8Y)has more elaborate visualizations than this blog post, and more details on the initial process I went through. [Better Mountain Generators That Aren’t Perlin Noise or Erosion](https://www.youtube.com/watch?v=gsJHzBTPG0Y)on Josh’s Channel is a highly polished and well explained video on two other non-simulated erosion techniques. I reference this video in my own video.

#### Shadertoys

You can run and see these visuals directly in your browser, and easily see and modify the source shader code too.

[Eroded Terrain Noise](https://www.shadertoy.com/view/MtGcWh)by Clay John ([Bluesky](https://bsky.app/profile/clayjohn.bsky.social)). The original version of the technique.[Terrain Erosion Noise](https://www.shadertoy.com/view/7ljcRW)by Felix Westin (Fewes) ([website](https://fewes.se/)). Slightly tweaked erosion effect, and presented in a vastly more polished way.[Clean Terrain Erosion Filter](https://www.shadertoy.com/view/33cXW8)by me. My earlier rewrite of Clay John and Fewes’ technique (based on the frequency approach), with more intuitive parameters.[Advanced Terrain Erosion Filter](https://www.shadertoy.com/view/wXcfWn)by me. My final iteration of the technique, with animated parameters.[Mouse-Paint Eroded Mountains](https://www.shadertoy.com/view/sf23W1)by me. My final iteration of the technique, with interactive mouse painting of the terrain.[Phacelle Noise Animation](https://www.shadertoy.com/view/t3dyWl)by me. A demonstration of the Phacelle Noise I extracted into a self-contained function ([blog post here](https://blog.runevision.com/2026/01/phacelle-cheap-directional-noise.html)).

#### Shadertoy video exporters

This is not entirely related to erosion techniques, but here are the tools I used to render high quality Shadertoys footage for the video. Okay, I may also be using the links section here to tell a side story about my video production woes.

[Shadertoy Exporter (original)](https://github.com/KoltesDigital/shadertoy-exporter)by Jonathan Giroux (Koltes). This tool worked great, until it broke when the Shadertoy website introduced Cloudflare human verification in early October 2025.[Shadertoy Exporter (forked)](https://github.com/larathedev/shadertoy-exporter)by Lara Davidova (larathedev). This fork was made to work with the Cloudflare human verification, and was briefly functional, until the Shadertoy website entirely disallowed being displayed in an iframe later in October 2025.[Shadertoy Exporter (Godot version)](https://github.com/NodotProject/shadertoy-exporter)by krazyjakee (NodotProject). This rewrite based on Godot is partially functional at the time of writing. It’s Windows-only, and (for me) has the following bugs: Does not convert the rendered frames into videos, has to be restarted after each render, and frequently does not register text input until the window focus is switched away and back. I begrudgingly used this for later footage in the video, manually running[ffmpeg](https://www.ffmpeg.org/)on the frames.- I’m aware there are also frame exporter browser plugins
[for Firefox](https://chromewebstore.google.com/detail/shadertoy-frame-exporter/bkompdalfpocndfcbcdajnfkjklbecjn)and[for Chrome](https://addons.mozilla.org/en-US/firefox/addon/shadertoy-frame-exporter/), but these have even worse usability for me. I have my browser set to display a save dialog when downloading a file, so when I try to render a Shadertoy for 200 frames, it opens 200 save dialogs.

#### Erosion filters in the wild

Let me know if you use the erosion filter technique in your project and have public images or videos to show for it!

I'm very happy so many people have found the technique useful enough to make their own implementations in a variety of shapes and forms. Some of the ones below are faithful implementations, while others are partial, derived, or based on an earlier version of the technique.

Implementations in tools and engines

- Implementation in Unity Burst
[posted on Reddit](https://www.reddit.com/r/Unity3D/comments/1salvh2/i_ported_an_advanced_erosion_terrain_shader_to/)and[released on Github](https://github.com/lpmitchell/AdvancedTerrainErosion)by Luke Mitchell. - Implementation in Unity Shadergraph
[posted on Bluesky](https://bsky.app/profile/jens06409515.bsky.social/post/3mikfzbi2gs24)and[released on Github](https://github.com/Jens-Maier/erosionFilter)by Jens Maier. - Implementation in Unreal's landmass plugin
[posted on Twitter](https://x.com/MichaelKinsey3D/status/2043407307984523608)by Michael Kinsey. - Implementation in Godot
[posted (with source) on Godot forum](https://forum.godotengine.org/t/fast-and-gorgeous-erosion-filter/136436)by Henry. - Implementation in Houdini
[blog post with source files](https://dailyhip.wordpress.com/2025/07/23/erosion-filter/)by eetu.

Implementations in games and private experiments

- Implementation in Hytale's Worldgen v2
[posted on Bluesky](https://bsky.app/profile/verday.bsky.social/post/3mijpnoirpc2a)and[released on Github](https://github.com/ItsVerday/Hytale_Worldgen_Additions)by Verday. - Erosion on a sphere
[posted on Mastodon](https://mastodon.gamedev.place/@metarapi/116205272100793897)by metarapi. - |peak|
[erosion noise in Desmos graphing calculator](https://www.desmos.com/3d/trzh59qzgq)by lemon (and a simpler version[here](https://www.desmos.com/3d/wkhxovnz3u)).

#### On using the second derivatives (curvature) for the fade target

Several people have suggested using the second derivatives (curvature) instead of the altitude for the fade target.

Using altitude is indeed not robust in the general case, since e.g. some valley could be higher up than some mountain peak. I'm not sure there's a perfect solution, and I kind of let it be up to the user to decide what to base the input fade target parameter on. I just base it on altitude in all my demonstrations.

I did think about using the second derivatives (curvature), but then every function involved in producing the input heights has to calculate and return those second order derivatives, or alternatively it has to be done numerically which is either slow (via multi-sampling) or rather inaccurate (via shader derivatives).

On top of that, curvature does not produce a value that's between -1 and 1 as the fade target needs, so you'd have to combine it with other things (like the first derivatives) to wrangle it into a useful range. That's absolutely possible, but hand-tweaking the particulars may still be needed.

So while it's something I considered, I don't really have a good solution. I'm curious if others will find a better way to handle this.

## 7 comments:

This is a really interesting read. I've been trying to implement my own version following your blog post, and I can't seem to get the results on the third picture. Is that picture a direct application of the algorithm? or did you do a modification to show it so cleanly?


My gullies, even in a second octave look too high frequency, while the first one looks fine.

I'm not quite sure which picture you count as the third. The initial pictures in for example the section "the basic idea" are mostly for illustrating concepts. The technique doesn't work right until "stripes in blended cells" is implemented.


At the end of the article you can find links to Shadertoys that have shader code included.

Hi, I am not familiar with shadertoy. I have a heightmap where I would love to apply this filter. Is there an application available for using this shader/filter where I can export the new heightmap?

Hi! There is no such application at this time. Maybe someone will make one, or maybe as plugins to existing applications. I find this likely to happen at some point, given how much interest I've seen in the technique, also from developers, but it may take some time. I don't have time to make such an application myself.

I'm making a citybuilder/total war type game called Iron Chieftain and would like to implement something like this for random map generation. I'll follow your method but since unreal engine's support for compute shaders is so convoluted I might just multithread it on the CPU.


When I first saw this on youtube I couldn't believe my eyes. The old method of simulating every droplet just feels archaic now. Amazing work.

you should have a look at artifexian's worldbuilders youtube channel - for good ideas on how to colour - things like beaches, rain shadows around mountains, prevailing winds, etc

I study remote sensing and this has quite an interesting overlap with fastscape from the GFZ in Potsdam.

Post a Comment