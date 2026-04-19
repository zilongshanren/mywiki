---
title: 'From the archive: Making a greener grass.Part 2/2 on COD:BO4 vegetation system.'
url: https://c0de517e.com/017_vegetation_part2.htm
author: Angelo Pesce
published: '2024-12-07'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

In the previous post, I wrote about the scattering system that helped Call of Duty Black Ops 4 to achieve its ambition of being the first COD with a "big map" mode, and I briefly mentioned that part of that solution involved separating the grass into its own rendering system.

Today I'll go through my notes to show how that was done - and perhaps there might be a few interesting tricks to pick up along the way.

Same as in part 1 - this work was not done just by me. When I joined the effort on the grass, most of the system had already been stood up. If I recall, Wade (one of the smartest people in a company full of true genius) came to me saying that he had a very particular set of skills... He knew how to make code run fast, and understood machines, but he had no talent for the "artistic" side of the job: making things look nice. There he needed help.

![Early tests - grass instanced with the terrain quadtree.](../../assets/7b8122c0a2f570fa.png)

Early tests - grass instanced with the terrain quadtree.
Indeed the prototype he had was fantastic: grass made of individual blades, all pure triangle geometry (i.e. not the usual alpha-cut cards or shells). Through the magic of instancing, a smart LOD system (protip: NaNs in the vertex position outputs kill triangles) and understanding how to make code to maximally utilize PS4's GCN GPU, rendering with the grass turned on ended up being FASTER than without!

How's that possible you ask? Well, consider what's underneath the grass! It turns out that decent terrain shaders are quite expensive, as they blend many texture layers - the grass system only needed basic terrain information (color, geometric normals - sampled from the terrain and passed to the grass vertices) - and being solid geometry it occluded the terrain saving GPU time!

So, my mission was to take this blazing fast system and make it look nice - hopefully without slowing it down (ok, by the end of it I might even have made it faster - at least when it comes to GPU programming, it turns out I'm no slouch either).

![Final results...](../../assets/7553d4b73b22468d.png)

Final results...
**Touch grass.**
Now, how do we approach this? Go out and touch grass - in this case, literally - might be a good starting point, and I have to admit I spent quite some time on my daily commute wandering around Vancouver's parks and looking at the grass from various angles - mostly frustrated at how complicated nature is.

You could approach it from a "physically-based rendering" standpoint and start searching for literature on the BRDFs of plants (fun fact - that's quite well studied especially in the aggregate, e.g. whole forests, etc - as it clearly has a big impact on things like climate...) or try to measure data (and we had a few tools for that, for a while we were also toying with SVBRDF scanners and glossmeters - but that's another story) - but in this case, I knew it would not help.

This was the case for at least a couple of reasons.

First, I knew that what we had was not close to real grass geometry - grass in games never is (at least thus far - I guess if we had that kind of time, we could have tried for a GPU SW raster approach).

There's no way you could feasibly have blades that are similar to actual grass dimensions, you'd simply need to have too many of them to achieve any sensible coverage - and even if you did, you'd quickly end up with very hard aliasing problems to solve.

![Close-up blades are much thicker than the real thing, and the shape is not very realistic either.](../../assets/12aef0ce8ae995b4.png)

Close-up blades are much thicker than the real thing, and the shape is not very realistic either.
So what you have instead is the "idea" of grass, something that kind of evokes the subject, whilst not being at all an accurate representation. To make things even more complex, you also have to account for the fact that your grass geometry is always "wrong" compared to the real thing, but in practice, it's also wrong in different ways depending on the distance.

Grass LODs typically work by gradually changing the geometry, shortening it in the distance, until it's possible to use fewer triangles and in the end, start removing/sinking into the ground blades - at which point your grass gets represented by the "bare" terrain - and shading has to account for all of this not to create an obvious difference.

![Level-of-detail of the blades.](../../assets/9d531b6fb30112ed.png)

Level-of-detail of the blades.
Second, COD:BO4, like BO3 before it, was a deferred-shading renderer - which meant that realistically I could not use the kind of complex, ad-hoc shading that vegetation BRDFs would need (and I did not have not enough time to try to tweak the gbuffer and specialize lighting pass shaders either - this meant for example that I could not do proper translucency).

**Observation.**
So our task is the following:

1) Understand how grass works in the real world.

2) Somehow make our fake, wrong grass look similar.

3) Blend the tricks we're going to use on grass with the terrain look, far away, to mask the transition.

Coincidentally, around this time I noticed this tweet on my timeline, by a talented indie/graphics dev:

![](../../assets/4fdc429d86ceb1d3.png)

"Most important thing about grass seem [sic] to be self-shadowing and accurate high-poly normals". Interesting, is this correct?

![Real world.](../../assets/f9009e407a3dcdfd.png)

Real world.
As mentioned, I had lots of photos of Vancouver's grassland, but to illustrate the point google image stuff suffices. You can see a few things in these...

Grass seems to have three "frequencies" - so to speak.

![Velvet-y.](../../assets/6ef9ae3e6cbe0674.png)

Velvet-y.
There is a low-frequency component that just conforms with the terrain, and far-away looks like a velvet-y BRDF. It's not surprising that grass looks like a fabric, in the end, the blades are sort of like fibers. So, somehow, globally the grass still shades "like" the terrain (say, according to the terrain normals), with a given BRDF.

![Bump-y.](../../assets/5c94d1c3de236eb7.png)

Bump-y.
At a medium frequency, you can often see that grass has its own texture. It shows bumps and clusters, and what's interesting is that these bumps are still behaving "like a BRDF", you can see they shade due to self-shadowing, and actually can even go quite the distance.

![Shiny!](../../assets/875710f28df1caeb.png)

Shiny!
And lastly of course, if you look up close, you see individual blades with strong specular, strong translucency, and so on.

**Experimentation.**
Now of course, if we could model and render grass accurately, i.e. with millimeters-width blades and exact shadowing, translucency, light bounces etc, etc, then antialias everything by brute-force, we'd probably have no problems in reproducing the real-world look.

![Brute-force offline rendering: not hard to get the right look!](../../assets/62ed8716ea450432.png)

Brute-force offline rendering: not hard to get the right look!
But we already noted we can't do any of that! In fact, the trick here is to do the opposite - not care much about the rendered grass geometry, and instead "paint over it" the look.

In a way, you can think about the geometry as a means to break the terrain silhouette and provide perhaps some amount of parallax in the shading, giving us positions in the world to paint.

The shading itself will be in-between the idea of shading the blade geometry and creating a BRDF that tries to mimic the aggregate behavior of real grass, just like textile BRDFs do not shade fiber geometry, but try to recreate the look of the aggregate statistics.

Before delving into coding, I did some experiments to understand better what I needed and what was not as important for the end results. For these, I used the offline Arnold renderer and some high-quality grass assets I downloaded from the internet.

This is a technique I like to use whenever I can - it's often possible to use off-the-shelf tools, especially for offline rendering, to prove hypotheses. For example, we could try to understand how important is the role of self-shadowing for the overall look, if the "bumps" we saw in photos are mostly about the orientation of the blades (think: diffuse dot product) or the shape of the terrain underneath (blades occluding light). We can try to narrow down the parameters of a conventional BRDF and see if we can obtain a good look without specialized shading. We can understand how much translucency matters, or how much GI does.

![Lambert, direct lighting only. Lambert+GI. Lambert+GI+Translucency.](../../assets/33e1f5e0fc249adc.png)

Lambert, direct lighting only. Lambert+GI. Lambert+GI+Translucency.![Experiments with specular highlights.](../../assets/1682eebf76aa2358.png)

Experiments with specular highlights.
Observations:

- Translucency is key, without it, the grass looks way too dark, even with GI.

- Specular is hard, even with the high-quality assets I was using, the models were not looking right.

![Going even closer...](../../assets/31b98939f1f10f96.png)

Going even closer...
If we look really close, grass seems to be made by strands that create a strong anisotropic effect. We'd need to take that into account as well...

**Faking it!**
Here's the plan - taken verbatim from my notes:

- Fake translucency.

- Try your best at normals.

- Fix specular as needed, fake occlusion.

- Add (nice looking) noise.

- Fade your fakes.

-- Far away, as we LOD out and we need to blend with the terrain

-- At very close range, as the blade shapes (and normals) are not too realistic (for coverage), and yet we don't have that much density so the ground still shows and we want to blend with that as well.

Now, faking translucency is relatively easy... in forward! We know how to do this well enough for thin geometry, but again for this, I could not add a bit to mark the grass and change the lighting shaders.

So instead we went with the assumption that we'd be mostly interested in the grass outdoors - i.e. shaded by the sun. With that, you can some some of the forward trickery in deferred, because you know now the light direction you expect.

The solution, in the end, was simple: we flip the normal and boost albedo saturation if we are not facing the sun, with some trickery to avoid singularities. Without it though, using the blade's geometric normals would have been a non-starter: we would have needed to either to "billboard" (rotate to the camera) the grass or use the terrain normals instead, both of which give a very "painterly" look and won't work for specular.

![Top: without the normal-flipping trick. Bottom: with, made using grass normals viable!](../../assets/138aeb92cc1aa6ab.png)

Top: without the normal-flipping trick. Bottom: with, made using grass normals viable!
Now, speaking of normals... Starting with geometric ones from the blade is better, we get more interesting detail - but some more hacks are needed for specular.

In the beginning, I exaggerated normal "rounding" near the blade's tips, to have smaller/sharper speculars. It's not what ended up shipping - but I knew from some level of decoupling of geometric normal from the actual geometric shape was needed.

In general, you end up with this idea that geometry has to be made "for coverage" (i.e. to fully hide the terrain underneath without needing crazy amounts of blades) and thus it is not the best for shading.

From the observation of the real grass (which in the end, is still a leaf, it has a central vein) I ended up creating a procedural normalmap done by passing the geometric normal and tangent, blending the two based on the distance from the center of the blade to create a "V" shape.

This has the added benefit of visually "thinning" the specular highlights a lot - almost creating a blade of grass inside the grass.

![Visualizing the grass specular only.](../../assets/ec8bc0de2979d7f0.png)

Visualizing the grass specular only.
I ended up rotating the grass blades according to the terrain normal (estimated from the terrain heightfield via usual differencing tricks) - and this gives some of the "medium frequency" bumpy details I observed in nature. I did notice though that a viable option was even just to rotate the grass geometric normals according to the terrain ones - not the actual grass blade shape - which could be a handy fact to further decouple shading from coverage.

To make things even more interesting, I added noise to the terrain heightfield before estimating normals, creating a "combing" effect that adds some medium-frequency bumps.

That's not the end though - specular was is still a huge pain, even with somewhat decent normals. From my experiments and some imagination, I deduced that the problem was mostly because you can't get precise blade-to-blade occlusion (shadowing) - on top of the normals still being not -that- great.

This is the pain of non-physically-based rendering - it's hard to procedurally create a great solution especially when there are lots of interconnected hacks - even if you did all your homework and you at least know what you are doing and why...

So first, I added a random, procedural per-blade "dome" shadow (mask) along the blade length that controls where the specular can be.

This still did look at times too bright though - turns out that environment map specular on the grass doesn't look all that good... Unfortunately, again due to having to work with deferred shading on a fixed g-buffer, I could not kill it without removing all specular - but here I went again with the idea of prioritizing the sun... I computed a quick and hacky Blinn term (with the sun direction) and used that to modulate the specular g-buffer term - effectively adding another mask so that highlights can exist mostly where the sun specular would be...

At this point, you might start thinking why didn't I just set specular to zero, compute it with the sun only in the grass g-buffer shaders, and add the result as white in the albedo... Well, I tried, and it worked, but of course that trick does not allow you to inject energy, so you're limited in the resulting lighting range... not great with HDR in other words.

The cherry on top? What's another hack among friends, right?

All this specular shaping/masking stuff doesn't really work if you try to modulate just the specular color (F0), because Fresnel will kick in at grazing angles and make everything shiny (in a PBR renderer)! So for the most part all these specular hacks were done by changing gloss (roughness) instead!

![Final version, with all the specular-modulation trickery to control where the highlights could be.](../../assets/c748e6147f47ed32.png)

Final version, with all the specular-modulation trickery to control where the highlights could be.
I think in the end I just wrote out a constant specular color (unmasked), modulated with some noise. Various kinds of noise are of course key in all of this - the grass is effectively all shaped and positioned via vertex and pixel-shaders: only the most basic, straight-up blade geometry was baked in the instanced vertex data.

Various uncorrelated per-blade noise channels drove lots of the blade properties, like shape and rotation and so on, but the most important noise was the medium-frequency pattern used for the grass "combing" which also ended up driving some of the shading variation - to further accentuate the "bumps" I liked in real-world grasslands.

**Fading the fakes.**
Lastly, as most of the grass is a huge hack, we need to hide problems when our hacks "break", fading away certain tricks that can't work in all situations...

Going again back to my notes, here are some of the counter-hacks I wrote down:

- The normals revert to pure terrain ones (+ medium frequency noise) far away. I.e. not using the grass blade geometric ones - this is quite obviously needed.

- Specular fades very near to the camera, to avoid having too sharp highlights and showing the artificial "normalmap" tricker. Particularly important when hiding in the grass (proning).

- There is a "darkening" height ramp that is applied mostly to albedo, as the main source of ambient occlusion. It worked -wonders-, but it broke all the times we can clearly see the ground, so, far away (LODding) and close up (blades are too sparse). Thus, I faded it away in these cases.

The last hack - the height ramp, is amazing. To illustrate how important it can be, see the following shadertoy creations (unfortunately, I lost the link - sorry to the authors):

![](../../assets/b084540ee0b445ca.png)

![](../../assets/866bafb4cd01b867.png)

In both cases the only shading comes from a constant ramp on the grass blades, there is no actual lighting! Yet at medium/far distances (i.e. medium-low frequency), the grass looks quite convincing, all thanks to the shaping of the blades/heightfields that provides occlusion to hide parts of the blades...

**End results.**
Some more shots I had from development. If you fire up CO:BO4 today, you might not see this - as both programmers and artists keep tweaking the game post-shipping, I have no idea of how things are rendered today!

![](../../assets/ea69ba2255447dac.png)

![](../../assets/aa6747b3a2472287.png)

![](../../assets/3942c59c64a7aff7.png)

![](../../assets/792d3b3a599882f3.png)

**Bonus materials.**
Fun fact. Soon after finishing the grass, we got feedback, I think from testers, that without grass the streams of the games (think Twitch et al) looked much better. Oh no! What was going on?

Well, you might already imagine the problem - grass adds lots of high-frequency detail that video compression does not cope with great, both smearing the grass itself but worse, trying to spend more bits to cope with that, and lowering the image quality overall!

For a bit, I experimented with guiding the video compression using information from the engine to optimize it - even just simple masks of where the important stuff is would help - in the end, though this was not viable at least on consoles where (at least at the time) there was no way to send such information to the hardware encoders. Fun though to play with all of that!

Second and last fun thing - for a while, I experimented with the idea of rendering far-away grass volumetrically. This did not matter for the kind of short grass I've shown so far, but if we wanted to have taller grass that would have needed to be rendered far into the world - because players can hide in the tall grass, so if you LOD it away conventionally, you end revealing where enemies are!

This did not end up being a thing, but it did result is some interesting Instagram posts on my part of shadertoys that looked like random procedural art stuff, but in actuality were the early stages of experimenting with raymarching and other ideas of how one could represent far-and-tall grass.

![](../../assets/27b68c3f0945f1a0.png)

![](../../assets/fdaf6b2c07644fee.png)

![](../../assets/6304d38c6ee1e692.png)

More:

[1](https://www.instagram.com/kenpex/reel/BkyE7H5lD9f/),

[2](https://www.instagram.com/kenpex/reel/BkyZB4aFq2y/),

[3](https://www.instagram.com/kenpex/reel/BlMFwEMjrHR/),

[4](https://www.instagram.com/kenpex/reel/Bk3DQT9D887/),

[5](https://www.instagram.com/kenpex/reel/Bk0rkddDIle/).

!["...CS Software Raster might be the fastest and more general option..."](../../assets/018aa36e7f729963.png)

"...CS Software Raster might be the fastest and more general option..."
![People over the internet forcing the lowest LODs everywhere...](../../assets/fc427cc288446c6f.png)

People over the internet forcing the lowest LODs everywhere...![...reveals some of the LOD magic!](../../assets/ef9360013c9b9caf.png)

...reveals some of the LOD magic!![](../../assets/029aca74378e6971.png)

![My desk near the end of production.](../../assets/c837bc67a997c026.png)

My desk near the end of production.