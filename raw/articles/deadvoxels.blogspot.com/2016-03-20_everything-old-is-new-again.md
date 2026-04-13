---
title: Everything Old is New Again!
url: http://deadvoxels.blogspot.com/2016/03/everything-old-is-new-again.html
author: Jon Greenberg
published: '2016-03-20'
source_blog: Dead Voxels
source_site: http://deadvoxels.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

- Ensure all your objects can be charted.

- Build a list of visible objects.

- Attempt to atlas all your visible charts together into a texture page, allocating them space proportional to their projected screen area.

- Assuming you've got world-space normals, PBR Data, and position maps, light into this atlased texture page, outputting final view-dependent lit results.

- Generate a couple mips to handle varying lookup gradients.

- Now render the screen-space image, with each object simply doing a lookup into the atlas.

Pretty elegant. Lots of advantages in this:

- essentially you keep lighting costs fixed (proportional to the super-chart's resolution)

- your really expensive material and lighting work doesn't contend with small triangle issues.

- all your filtering while lighting and shading is brutally cheap.

- because things are done in object space, even if you undersample things, should look "okay".

Now, as suggested there are a few issues that I think are mostly ignore-able due to the fact that this was designed around RTSs - I think in a general case you'd really want to be a lot more careful about how things get atlassed as I think something like an FPS can fairly easily create pathological cases that "break" if you're just using projected area. For example, imagine looking at a row of human characters forming a Shiva-pose, by which I mean, standing one behind the other with their arms at different positions. Of course, this doesn't really break anything, but it does mean you're likely to oversubscribe the atlas and have quality bounce around depending on what's going on. Even so, still pretty interesting to play around with.

So, I'm going to propose a different way to think about this which is actually in many ways so obvious I'm surprised more people didn't bring it up when we excitedly discussed OSS - lightmapping. Ironically this is something people have been trying to get away from, but I guess I'll propose a way to restate the problem:

Consider that not everything necessarily needs the same quality lighting, or needs to be updated every frame. So let's start by considering that we could maybe build three atlases - one for things that need updating every frame, and two low frequency atlases, which we update on alternating frames. Now if we assume we're outputting final lighting this might be a bit problematic because specularity is obviously view dependent and changing our view doesn't change the highlight.

Okay, so what if we don't output final shading but instead light directly into some kind of lighting basis? For example, the HalfLife-2 basis (Radiosity Normal Maps or RNMs), or maybe Spherical Gaussians as demo'd by Ready At Dawn. Now obviously your specular highlights will no longer be accurate as you're picking artificial local light directions.

As well, RNMs and much of their ilk tend to be defined in tangent-space, not world-space, so that's somewhat less convenient, as instead of needing to provide your lighting engine with just a normal, you actually need the tangent basis instead, so you can rotate the basis into world-space before accumulating coefficients. But its been demonstrated by Farcry4 you could do this by encoding a quaternion in 32 bits, so hardly impossible. And FWIW, RNMs tend to be fairly compressible (6 coefficients, using an average color, are typically fine).

Anyway, storing things in a basis in this way provides a number of interesting advantages that should be pretty familiar:

- Lighting is independent of material state/model/BRDF. You don't need the albedo, metalness, roughness, etc. This means that in cases where your materials are animating, you can still provide the appearance of high frequency material updates. You can still have entirely different lighting models from object to object if you so choose. Because of this, all you need to initially provide to the lighting system is the tangent basis and world-space position of each corresponding texel. Your BRDF itself doesn't matter for building up the basis, so you can essentially do your BRDF evaluation when you read back the basis in a later phase (probably final shading). This is analogous to, say, lighting into an SH basis where you simply project the lights into SH and sum them up - the SH basis texel density can be pretty sparse while still providing nice looking lighting results so long as your lighting variation frequency is proportional to less than the lighting density. Of course, specularity can be problematic depending on what you're trying to do, but more on that below.

- As said, lighting spatial frequency doesn't have to be anywhere near shading frequency and can be considerably lower as lerping most lighting bases tends to produce nice results without affecting the final lighting quality significantly (with the exception of shadowing, typically).

- Specular highlights, while inaccurate due to compressing lighting into a basis, can properly respond to SpecPower changes quite nicely. There's also nothing stopping you from still using reflections as one normally would during the shading phase. Lots of common lightmap+reflection tricks could be exploited here as well. If you end up only needing diffuse for some reason, SH should be adequate (so long as you still cull backfacing lights), and would remove the tangent-space storage requirements - though you'd need to track vertex normals.

- There's no law that says *all* lighting needs to be done uniformly in the same way. You could do this as a distinctly separate pass that feeds the pass that Baker described, or process them in the forward pass should the need arise.

And last but not least, if you're moving lighting into a basis like this, there's no rule that says you need to update everything every frame. So for example, you could partition things into update-frequency-oriented groups and update based on your importance score. This would also allow for your light caching to be a little more involved as you could now keep things around a lot longer (in a more general LRU cache). For example, you could have very very low res lighting charts per object, all atlased together into one big page that's built on level load as a fallback if something suddenly comes into view, loose bounce determination, or distant LODs. You could even PRT the whole thing into a super-atlas, assign each object a page, and treat the whole thing as a cache that you only update as needed!

Anyway, just some ideas I've been playing around with that I figured I'd share with everyone.

-Jon

## No comments:

## Post a Comment