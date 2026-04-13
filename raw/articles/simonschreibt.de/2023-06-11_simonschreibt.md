---
title: Simonschreibt.
url: https://simonschreibt.de/gat/gta-v-underestimated-glow/
author: Simon
published: '2023-06-11'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Below, you can see a traffic light in [GTA V](https://www.rockstargames.com/gta-v) at night. It has a nice glow. You might think this is nothing special but look at the scrollbar of this website. There is **a lot** to talk about! Get yourself a tea and then let’s go!

# Foreword

First, we’ll talk about different solutions to create such a glow and why one could run into problems when trying to replicate it (depending on the engine; keyword: Tone mapping). Next, we’ll learn about billboards and see an example of [Rockstars](https://www.rockstargames.com) amazing attention to detail. At the end, I’ll present four little knowledge nuggets which I learned about game development and myself.

[Bloom & Tone Mapping](https://simonschreibt.de#bloom) • [Billboards](https://simonschreibt.de#billboards) • [Tips & Thoughts](https://simonschreibt.de#additional)

# Introduction

To get a glow like in GTA V, one could:

- Use a billboard (with a blob-texture to fake volumetric lighting)
- Use post FX Bloom
~~Use real volumetric lighting~~

As far as I can tell, small light sources like this traffic light do **not** render as real volumetrics in GTA V (so we can rule out number 3). So let’s talk about bloom first:

# Bloom

[Bloom](https://www.froyok.fr/blog/2021-12-ue4-custom-bloom/#what_is_bloom) is basically blurring the image and slapping it as an additional layer on top of the existing image. **Important:** To get such a glow in Unreal or Unity, you need to set your emissive material to a **very bright** value, which normally leads to a **desaturation** of the core. In the video below, you can see how the sphere tends more and more toward white, the higher its emissive values go:

But that’s weird, isn’t it? GTA achieved the glow **without** the having the core desaturated!

Question: Maybe they didn’t use high emissive values at all?

Answer: They did! When looking at the draw call (where the base geometry and the bloom are combined), we can see that both buffers use values **far above 1.0**!

But remember, if we’d do this in Unreal, it would immediately burn out into desaturated versions of red like shown above!

**Or would it? **

I’ve asked [Froyok](https://www.froyok.fr/) (because she wrote amazing articles about [bloom](https://www.froyok.fr/blog/2021-12-ue4-custom-bloom/) and [lens flares](https://www.froyok.fr/blog/2021-09-ue4-custom-lens-flare/)!) and she said: *“Could be the tone mapper which doesn’t let the colors burn into white.”*

So I’ve tried to find more information about tone mapping, stumbled across this [cool video from tharlevfx about GT Tone mapper](https://youtu.be/hZwo7XEgZ50) which led me to two very interesting information:

1. Unreal has **not** always done the bloom like they do it today! Their documentation shows (see video below) the old version, where the colors do **not** desaturate and the new filmic version, where the behavior is more realistic:

[Color Grading and Filmic](https://docs.unrealengine.com/4.27/en-US/RenderingAndGraphics/PostProcessEffects/ColorGrading/)

[Tone mapper](https://docs.unrealengine.com/4.27/en-US/RenderingAndGraphics/PostProcessEffects/ColorGrading/)

2. There are indeed Tone mappers which do **not** let the colors burn into whites! Using them is an **artistic decision** to strive for a certain look instead of realism. Here is an example from Grand Tourismo:

[Gran](https://www.shadertoy.com/view/Xstyzn)

[Turismo Tonemapper by Meshula](https://www.shadertoy.com/view/Xstyzn)

Here is a [wonderful breakdown example from Alex Beddows](https://www.exp-points.com/alex-beddows-cerberus-focusing-on-the-task-megascans-ue4) which shows how artistic direction leads to an active choice for a different tone mapper.

According to the amazing [GTA V frame study by Adrian Courrèges](https://www.adriancourreges.com/blog/2015/11/02/gta-v-graphics-study/#tone-mapping-and-bloom) the game (GTA V) uses a Tone mapper created for Uncharted 2 and this works differently from what we see in (the new) filmic version from Unreal:

Adrian Courrèges

“These operators apply the same calculation to R, G, B independently. One channel has no influence on the other. A component which is at zero will stay at zero after tonemapping. Which is why a very bright pure red, will stay pure red, and never turn white.”

Adrian even provides [this Shadertoy Example](https://www.shadertoy.com/view/dtGSDw) where you can see how different tone mappers react to the high emissive values (I’ve changed line 52 to `vec3 color = HDRColor * (sin(iTime) * 0.5 + 0.5);`

to have it animated):

[Tonemapper Comparison by Adrian Courrèges](https://www.shadertoy.com/view/dtGSDw)

**Summary**: The traffic lights in GTA V use high emissive values to get a nice glow, **but** the tone mapper prevents the color from burning into white.

By the way: Whenever we see the usual behavior of light sources turning toward white, it’s painted directly into the texture. Here are some examples:

By the way, the texture for the pizza place is based on a photo and this place really exists! [Check out my tweet about it](https://twitter.com/simonschreibt/status/1665803333649440770)!

But there’s something else: When one disables the post FX, there is **still** a little bit of glow around the light. It’s based on billboards and also a bit fascinating.

# Billboards

Using billboards to visualize lens flares or glows is nothing special (we will see an old-school example later). **But**: In GTA V, instead of only one, they use **two billboards**. There is also a nice texture and everything together is another great example on how much detail the people at Rockstar put into their work.

Why am I so fascinated with that? Look at this video below! It shows what exactly happens in our eye: We see fine glare patterns with subtle movements because of little particles in our lens. And the Rockstar artists did not only make a texture with a lot of detail to replicate the pattern (see above, I’ve increased the luminance a bit for better visibility) …

[Temporal Glare: Real-Time Dynamic Simulation of the Scattering in the Human Eye (Eurographics 2009 Supplemental Video)](https://youtu.be/5ewKMOodT1Y)

…they also use the **two** billboards to rotate them against each other to add the subtle movement which we saw in the video above. Here is an example on their cars:

[GTA V](https://www.rockstargames.com/gta-v)

That’s very nice, isn’t it?

By the way: The billboards shrink and grow depending on the viewing angle:

[GTA V](https://www.rockstargames.com/gta-v)

The same goes for the car lights:

[GTA V](https://www.rockstargames.com/gta-v)

**Summary**: In addition to the existing bloom, GTA V uses billboards to mimic effects which we know from our real-world eye vision. I love that these billboards also serve as a **fallback** in case someone disables the bloom.

# Tips & Thoughts

I’d like to share some knowledge nuggets and personal experiences now.

## 1. Sparkly Tip

Sometimes one may want sparkles with a nice glow, but they shall not be super outstanding. In these cases, you can use a bigger particle and a texture where the glow is painted in (**left**) instead of relying on glow through post FX. This has more overdraw as the particles are bigger, but you get a nice subtle fairy dust. In the **middle,** you can see the unspectacular particles without glow and on the **right** an example of how much you’d have to push the emissive values to get the same size of glow by relying on post FX Bloom – but these sparkles now really SCREAM for attention, which is something you may not always want.

## 2. Old School

Game Dev History Lesson: Billboards for lens flares were used very early. Below is an example from Unreal 1.

[Unreal](https://de.wikipedia.org/wiki/Unreal)

Did you notice, that the lens flares take a little time to fade out and sometimes appear **through** the floor? This is a little artifact from trying to replicate an effect which we know from the real world: Lens flares do not just disappear, but they get gradually smaller depending on how much of the light source is covered:

[[Source]](https://www.youtube.com/watch?v=pZk8mR6grjE)

## 3. New Tech != Always Better

New technologies don’t make games always look better. Here is an example from [NFS](https://store.steampowered.com/app/1262540/Need_for_Speed/) (which has exceptional good-looking lighting in my eyes!) and we can see the volumetric light around the streetlights far in the distance. Very nice!

[Need for Speed](https://store.steampowered.com/app/1262540/Need_for_Speed/)

But turns out: They are not volumetric. It’s just billboards. Lol, old-school!!

[Need for Speed](https://store.steampowered.com/app/1262540/Need_for_Speed/)

Now let’s look at a **modern** game. This is [Watch Dogs®: Legion](https://store.steampowered.com/app/2239550/Watch_Dogs_Legion/) and it offers real **volumetric lights**! Must look way better than these weird billboards, mustn’t it?

[Watch Dogs Legion Night Drive Around London In Foggy Wet Streets](https://youtu.be/N2kk_Nvra84)

You may notice, that the volumetric cones of the streetlamps are **not visible in the distance**. They fade in quite close to the player. This is most likely an [optimization which is described in this fantastic video](https://youtu.be/G0sYTrX3VHI?t=903).

I made another video where is effect is seen even better because I’ve set the game to **low settings** so that we can even see the big voxels “flicker” a bit (but I don’t understand why they also fade the volume out when the camera comes closer):

Another example: The blue spotlights from these drones just disappear in the distance (and reappear when I come closer again). With old-school billboards, this wouldn’t happen (except you want to cull them):

**Summary**: I don’t want to talk bad about the Watch Dogs Tech! It’s just that sometimes it takes a while, until new technology is performing well (or until graphic cards allow everyone to enjoy it in great detail). But until this is the case, old-school tricks like billboards can sometimes look better than the more advanced tech.

## 4. Being Cocky

This is a personal story: I work(ed) for many years in custom engines and sometimes, when I hear about cool new features (for example from Unreal), I start to look down on our own tech.

Example: A long time ago, I heard that Unreal now supports **post FX lens flares** and from that moment I just assumed (without verifying if this is true) that **all** of their lens flares are now done with this cool new tech. I was laughing about our own engine, which still used old school billboards – rofl rofl lol lol!

But then the brand new [Infiltrator Demo](https://youtu.be/dO2rM-l-vdQ) came out and guess what: They use old school billboards as well! In the video below, you can see how the billboard cuts into the geometry (which usually doesn’t happen with “real” lens flares because they arise in the camera and in games are rendered on top of everything):

So, turns out: I was wrong to look down on our little custom engine. I was arrogant, didn’t educate myself, and there is nothing wrong with using old school methods. Don’t be like past-Simon.

Thanks for reading until here, I hope you liked the article. Let me know in the comments.

Thank you [Adrian Courrèges](https://www.adriancourreges.com/), [Froyok](https://www.froyok.fr/) & [Tharlsvfx](https://www.youtube.com/@tharlevfx/videos) for your help and your work in form of articles/videos/examples! You helped me a ton!

Have a very nice day!

Simon ♥

This was a really great read Simon. The tone mapper settings in Unreal is something I’ve struggled with for a bit and this cleared some things up! Thanks for sharing 💜

Thank you! Make sure to check out the video from TharlsVFX which I linked in the article. It gives great examples on how to deal with the tone mapper.

Oh billboards and sprites … 😌

Back at radonlabs & Bigpoint we used to have a custom scripts repository for Maya. I made a one-click “make sprite” script that made a setup that mimicked the in-engine behavior for vfx assets.

The good ol days 👴

Oh nice! I always wondered why Maya/Max/etc didn’t behave more like real-time engines. Setting up transparencies was always a struggle … at least in Maya 7. Looked very bad, while it looked already ok in games :D

Interesting article!

I’ve always been amazed by how “old school” techniques can achieve great results while using minimal resources.

That would be great to see if having multiple layers of billboards has still a good render compare. I can imagine some sort of flickering when a billboard depth order changes suddenly. Probably depends on how color synthesis is done,…

Good job!

Ps: spotted a typo in “But until this is the case, old-school tricks like billboards can sometiems look better than the more advanced tech.”(sometimes).

I think the flickering could be avoided by giving one of their materials a higher render priority so that it always renders in front of the other. Thanks for the kind words and the mentioning the typo, I will correct it!

Thanks Simon! Great article!

You have always been inspiring to me!

Great article again Simon!

Forgive me if I’ve missed something but there is a couple of _really_ simple ways to get the look of the legacy tonemapper built into Unreal. I’ve used this a few times on projects that required more artistic control over the colours. The first is heavy handed and involved just disabling the filming tonemapper with the cvar r.TonemapperFilm 0. This will put you back to the legacy tonemapper and your reds will be GLORIOUS. Check the screenshot example below.

A slightly less heavy handed approach is to continue to use the filmic tonemapper but control the tone curve, and you can do this directly in the post processing volume using the ‘Tone Curve Amount’ scalar. You can actually fine tune a look with the slider where you can go BETWEEN filmic and legacy – if you are that way inclined.

https://imgur.com/a/gLEr7gC

The benefits of these methods as opposed to tharlevfx’s custom tonemapper is you don’t lose any built in features – bloom, exposure, colour correction, it all still works with both of these. Also it saves you a lot of time and effort :D

Bonus tip, you can set r.Bloom.Cross -1 to get a more anamorphic look to your bloom, which can be tweaked to look good by adjusting the sizes of the kernels in the post processing volume.

Also all of this MIGHT only apply to UE4 as I’m yet to move up due to multiple projects stuck in legacy limbo :(

Cheers!

Wow, nice! Thank you very much for this insightful comment! <3

Very cool read, Simon. We tend to forget those old school techniques for the more “shiny and new” techniques. Billboards are still a very mighty tool for performance optimization. In Unity there is an asset that generates “Impostor” Billboards from 3D Models in the Scene to replace LOD just by taking Screenshots from all sides. It incredible effective and you can’t see a difference.

That the old ways of doing it that are just born out of necessity are sometimes way superior is also very visible in movies today. You just have to compare the Lord of The Rings and Rings of Power. Practical effects vs 100% CGI.

Love your articles, Simon!

About that pizza place… I went researching and found out: It was called “Paramount Cafe” and located next to the Hard Rock Cafe (1501 Broadway, New York, NY 10036 US). It does not exist anymore since around 2011, according to Google Streetview.

https://www.alamy.com/stock-photo-patisserie-croissants-bakery-at-times-square-7th-avenue-and-44th-street-25307300.html

Oh noooo! It could have been the famous pizza place every gta fan would go to :( They could have been rich! Thanks for the research :)