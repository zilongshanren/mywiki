---
title: runevision blog
url: https://blog.runevision.com/2026/
published: '2026-03-30'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

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