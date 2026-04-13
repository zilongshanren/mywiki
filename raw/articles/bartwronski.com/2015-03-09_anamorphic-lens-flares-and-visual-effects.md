---
title: Anamorphic lens flares and visual effects
url: https://bartwronski.com/2015/03/09/anamorphic-lens-flares-and-visual-effects/
published: '2015-03-09'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## Introduction

There are no visual effects that are more controversial than various **lens and sensor effects.** Lens flares, bloom, dirty lens, chromatic aberrations… All of those have their lovers and haters. Couple years ago many games used cheap pseudo HDR effect by blooming everything; then we had light-shafts craze (almost every UE3 game had them, often set terribly – “god rays” not matching the lighting environment and the light source at all) and more recently many lo-fi lens effects – dirty-lens, chromatic aberrations and anamorphic flares/bloom.

They are extremely polarizing – on the one hand for some reason art directors and artists **love **to use them, programmers engines implement them in their engines, but on the other hand lots of gamers or movie audience seem to **hate** those effects and find their use over the top or even distracting. Looking for some examples of those effects in games it is way easier to find criticism like [http://gamrconnect.vgchartz.com/thread.php?id=182932](http://gamrconnect.vgchartz.com/thread.php?id=182932) (more on neogaf and basically any large enough gamer forum) than any actual praise… Hands up if you have ever heard from a player “wow, this dirty lens effect was soooo immersive, more of that please!”. 😉

![Killzone lens flares - high dynamic range and highly saturated colors producing interesting beautiful effect, or abused effect and unclear image?](../../assets/7d4a5b049a2ce85b.jpg)


![Killzone lens flares - high dynamic range and highly saturated colors producing interesting beautiful effect, or abused effect and unclear image?](../../assets/7d4a5b049a2ce85b.jpg)

Killzone lens flares – high dynamic range and highly saturated colors producing interesting visuals, or abused effect and unclear image?

It is visible not only in games, but also movies – it went to the extreme point that after tons of criticism movie director J.J. Abrams supposedly [apologized for over-using the lens flares in his movies](http://www.craveonline.com/film/interviews/569755-exclusive-j-j-abrams-apologizes-for-his-lens-flares).

![Star Trek: Into Darkness lens effects example, source: http://www.slashfilm.com/star-trek-lens-flares/](../../assets/aab30b9c75331d17.jpg)


![Star Trek: Into Darkness lens effects example, source: http://www.slashfilm.com/star-trek-lens-flares/](../../assets/aab30b9c75331d17.jpg)

Star Trek: Into Darkness lens effects example, source: [http://www.slashfilm.com/star-trek-lens-flares/](http://www.slashfilm.com/star-trek-lens-flares/)

Among other graphics programmers and artists I have heard very often quite strong opinion “anamorphic effects are interesting, but are good only for the sci-fi genre or modern FPS”.

Before stating any opinion of my own, I wanted to write a bit more about anamorphic effects, which IMO are quite fascinating and actually physically “*inspired*“. To understand them, one has to understand the history of cinematography and analog film tapes.

## Anamorphic lenses and film format

I am not a cinema historian or expert, so first I will reference you to two links that cover the topic much more in depth and in my opinion much better and provide some information about the history:

To sum it up, **anamorphic lenses** are lenses that (almost always) provide **double** squeezing of the image in the horizontal plane. They were introduced to provide much higher vertical resolution of the image when cinema started to experiment with widescreen formats. At that time, most common film used were 35mm tapes and obviously whole industry didn’t want to exchange all of its equipment to larger format (impractical equipment size, more expensive processes), especially just for some experiments. Anamorphic lenses allowed for that by using essentially analog and optics-based **compression** scheme. This compression was literal one – by squeezing the image before exposing a film and later decompressing by unsqueezing it when screening it in the cinema.

First example of a movie shot using anamorphic lenses is The Robe from 1953, **over 60 years ago**! Anamorphic lenses provided simple **2:1 squeeze** no matter what was the target aspect ratio – but there were various different target aspect ratios depending if sound was encoded on the same tape, what was the format etc.



![Effect of increased vertical resolution due to anamorphic image stretching. Source: wikipedia author Wapcaplet](../../assets/07638daf5d43ef1c.jpg)


![Effect of increased vertical resolution due to anamorphic image stretching. Source: wikipedia author Wapcaplet](../../assets/07638daf5d43ef1c.jpg)

Effect of increased vertical resolution due to anamorphic image stretching. [Source: wikipedia author Wapcaplet](http://en.wikipedia.org/wiki/Anamorphic_format)

To compensate for squeezed, anamorphic image **inverse conversion and stretching** were performed during the actual movie **projection.** Such compression didn’t leave the image quality unaffected – due to lens imperfections it resulted in various interesting anamorphic effects (more about it later).

Anamorphic lenses are more or less a **thing of the past** – since the transition to digital format, 4K resolution etc. they are not really needed anymore and are expensive, but also incompatible with many cameras, poor optical quality etc. I don’t believe if anamorphic lenses are used anymore at all, maybe except for probably some niche experiments – but please correct me in comments if I’m wrong.

## Lens flares

Before proceeding with the description of how it affects the lens flares, I wanted to refer to a [great write-up by Padraic Hennessy about physical basis for the lens flares effects in actual, physical lenses](https://placeholderart.wordpress.com/2015/01/19/implementation-notes-physically-based-lens-flares/). This post covers comprehensively why all lenses (unfortunately) produce some flares and about simulation of this effects.

In shortcut – physical lenses used for movies and photography consist of many glass lens groups. Because of **Fresnel law** and different **IOR** of every layer, light is never transmitted perfectly and in 100% between the air and glass. Note: lens manufacturers coat glass with special nano-coating to reduce it as much as possible ([except for some hipster “oldschool” lenses versions](https://bartwronski.com/2014/08/08/voigtlander-nokton-classic-40mm-f1-4-m-on-sony-a7-review/))- but it’s impossible to reduce it completely.

Having many groups and different transmission values it results in light reflecting and bouncing multiple times inside the lens before hitting the film or sensor – and in effect some **light leaking, flares, transmittance loss and ghosting**. In cases of low dynamic range scenes, due to very small amount of light that gets reflected every time, it produces negligible results – but it is worth noting that the image **always** contains some ghosting and flares, sometimes it is not measurable. However with extremely high dynamic range light sources like sun (orders of orders of magnitude higher intensity), the light after bouncing and reflecting can be still brighter than actual other image pixels!

## Anamorphic lens flares

Ok, so we should understand at this point the anamorphic format, anamorphic lenses and the lens flares, so where do the anamorphic lens flares come from? This is relatively simple – light reflection on the glass-air contact surface can happen in many places in the physical lens. It can happen both **before** and **after** the anamorphic lens components. Therefore extra light transmitted and producing a lens flare will be ghosted as if the image was not-anamorphic and had regular, not squished aspect ratio. If you look at exposed and developed such film, you will see **squished image**, but with some regular looking **circular lens flares**. Then, during film projection it will be **stretched** and viola – an horizontal, streaked, anamorphic lens flare and bloom! 🙂

## Reproducing anamorphic effects – an experiment

Due to extremely simple nature of anamorphic effects – just your lens effects happen in 2x squeezed texture space, you can quite simply reproduce them. I added option to do so to [my C#/.NET Framework for graphics prototyping](https://bartwronski.com/2014/10/18/csharprenderer-framework-update/) (git update soon) together with some simplest procedural and fake lens flares and bloom. I just squeezed my smaller resolution buffers used for blurring by 2 – that simple. 🙂 Here are some comparison screenshots that I’ll comment in the next paragraph – for the first 3 of them the blur is relatively smaller. For some of them I added some bloom extra color multiplier (for the cheap sci fi look 😉 ), some other ones have uncolored bloom.

**Please note **that all of those screenshots are not supposed to produce artistically, aesthetically pleasing image, but to demonstrate the effect clearly!

In the following ones the bloom/flare blur is 2x stronger and the effect probably more natural:

**Bonus**:

I tried to play a bit with anamorphic bokeh achieved in similar way.

First of all, we can see that with simple, procedural effects and Gaussian blurs using **real** stretch ratio of 2:1 it is **impossible** to achieve crazy effect of anamorphic flares and bloom seen in many movies and games with single, thin lines across the whole screen. So be aware that it can be an artistic choice – but has nothing to do with real, old school movies and anamorphic lenses. Still, you will probably get such a request when working on an engine with real artists or for some customers – and there is nothing wrong with that.

Secondly, the fact that procedural effects are anamorphic, makes it more difficult to see the exact shape of ghosting, blends them together and makes less distracting. This is definitely a **good** thing. It is questionable if it can be achieved only by a more aggressive blur on its own – in my opinion the non-uniform blurring and making the shapes not mirrored perfectly is more effective for this purpose.

Thirdly, I had no expectations for the **anamorphic bokeh**, played with it as some bonus… And still don’t know what to think about it, as for the results I’m not as convinced. I never got a request from an artist to implement it and it definitely can look weird (more like a lazy programmer who wrongly implemented aspect ratio during DOF 😉 ), but it is worth knowing that such effects actually existed in the real, anamorphic lens/film format scenario.

Probably I would prefer to spend some time investigating the physical basis and how to implement [busy, circular bokeh](https://bartwronski.com/2014/04/07/bokeh-depth-of-field-going-insane-part-1/) (probably just some anamorphic stretch perpendicular to the radius of the image).

## My opinion

In my opinion, anamorphic effects like bloom, glare and lens flares are one of many effects and **tools in the artists toolbox**. There is a physical basis for such effect and they are well established in the history of the cinema. Therefore viewers and audience are used to their characteristic look and even subconsciously can expect to see them.

They can be abused, applied in ugly or over-stylized manner that has nothing to do with reality – but that is not the problem of the technique; it is again some artistic choice, fitting some specific vision. Trust your artists and their art direction.

**I personally really like subtle and physically inspired 2x ratio** of anamorphic lens flares, glare and bloom and think they make scene **look better** (less distracting) than isomorphic, regular procedural effects. Everything just “melts” together nicely.

I would** argue with someone saying such effects fit only sci-fi setting **– in my opinion creating simulation of cinematic experience (and a reference to the past movies…) is just as valid as trying to 100% simulate human vision only for any kind of game – it is matter of creative and artistic direction of the game and its rendering. Old movies didn’t pick anamorphic lens flares selectively for specific set&setting – it was a workaround for film technical limitation and used to exist in every genre of movies!

Therefore, I don’t mind them in some fantasy game – as long as the whole pipeline is created in cinematic and coherent way. Good example of 100% coherent and beautiful image pipeline is **The Order 1886** – their use of lens aberrations, distortion and film grain looks just right (and being an engineer – technically amazing!) and doesn’t interfere with the fantasy-Victorian game setting. 🙂

Probably over-stylized and sterile, extreme anamorphic lens flares and bloom producing horizontal light streaks over whole screen don’t fit into the same category though. I also find them quite uncanny in fantasy/historical settings. Still, as I said – at this point such extreme effects are probably a conscious decision of the art director and should serve some specific purpose.

I hope that my post helped at least a bit with understanding the history and reasoning behind the anamorphic effects – let me know in comments what you think!

Anamorphic lenses are actually still pretty popular: http://www.arri.com/camera/cine_lenses/prime_lenses/anamorphic/

Interesting, thanks for the info, I had no idea (being much more into still photography). 🙂 Do you know how commonly they are currently used?

Been looking forward to seeing your lens flares and bloom in your c# renderer. Will you be doing the git update soon? 🙂

hey, I hope soon 🙂 can’t promise anything though, there are some my experiments tangled in that I’m thinking of writing about as well 🙂 cheers!

Just wondering if you had written up any of the other experiments. I’m still interested to see an update to your git repo with these effects 🙂

These kinds of screen space effects come from a desire to flatten the projected image. To treat it like a 2d canvas rather than a true viewport. Film academic David Bordwell writes about “intensified continuity” referring to the trend over the last few decades for shorter cuts, and more extreme close ups in film.

This as opposed to what John Ford began in the 50’s with “The Searchers”, Orson Welles and Greg Toland achieved in “Citizen Kane” with deep focus and allowing the eye to move over the scene and choose, or switch between points of interest. Check out Mark Kermode’s “History of Film” for more information.

Similarly in game design from the 80’s which encouraged maximising exploration, and use of game spaces given the limitations of RAM we have seen a shift towards highly controlled set pieces, and corridoor -like play spaces. Where the interactivity takes a back seat to funneling players to the next vista or piece of eye candy. Again, turning a 3d spatial simulation into a higly controlled 2d expression of screen space.

Hi Chuan, thank you for your reply with such deep and interesting historical context and cross-media references. Where is this “History of Film” available, do you have a link? Cheers!

I would say that this trend is very visible in many other aspects of video game art direction. Many art directors want to treat final image as a matte paint and shape it this way (via depth of field, selective blur, motion blur, vignette, those flare effects, bloom etc.), removing from perception layer what the game medium really is about – exploration, engagement and the sense of presence. While I believe there is some place for such heavily art-directed and “flattened” games, I hope that this extreme trend is temporary as art directors will learn the different rules of interactive medium. Attempts to create VR-compatible content and learning how differently it is perceived could be the catalyst here.

Hi Bart —

My bad I just realised I got the reference mixed up. You want to find Mark Cousin’s “Story of Film : An Odyssey” and in particular Episode 5 on post war expressionism. He does a great job of tracing the influence of deep focus from Ford’s “Stage Coach” [ 1939 ] through to Greg Toland and beyond.

I agree with the 2d art direction argument, and that makes me all the more excited to be working on VR development where new interaction, storytelling techniques will be needed. In my opinion we ought to unlearn all these linear player “control” mechanisms and think about how to create scenes, locations with presence and overlapping consequence.

I really miss the sense of exploration we had in games when I was a kid playing “Ultima” on a 64 Kb machine, and a palette of three colours on screen. There must be some way to use the scale of production these days to generate 12 -hours of content that doesn’t have to be so god damn predictable.

Nice article. Seems every recent article about lens flare uses “Star Trek” as an example. lol

One question:

For photos taken by anamorphic lens, since it “can happen both before and after the anamorphic lens components”, does this mean:

On a squished image, some are regular looking circular lens flares., some are squished.

So after stretching images back to normal, some lens flares are stretched, some are becoming normal?

Is my understanding right? Thanks.

Hi, that’s exactly what I meant. VFX artists and directors don’t need to follow reality or physical processes and they don’t; They are usually quite liberal about it and freely mix various anamorphic and isomorphic lens flares (often with varying aspect ratios, which doesn’t have any meaning in optics unless there were many anamorphic components in lens) and don’t really care for any physical lens structure, but it can have some physical explanation to some extent. 🙂

Cheers!

Another question: Do we add the RGB values of a lens flare into the RGB values of the image?

I thought it was. But I found Knoll Light Factory does not do so with their lens flares.

Yes, they are additive – but pre-tonemapping. So final output and proportion is non-linear and depends on the used tonemapping operator and perceptual curve.

Thanks. Would you elaborate more regarding how to do it, or any link, please?

I find that sometimes simple addition seems not very natural.

There is no magic – simply adding flares, but in linear space, pre-tonemapping, pre-luminance calculations. 🙂 Which engine are you using?

Thanks. What did you mean by “engine”? I use OpenGL to draw some lens flare, and for now I directly do addition to the original image. I do not understand why pre-tonemapping is necessary? From the optical mechanism of lens flares, they are not related to the original image. They are another light source for the final image.

Yes, but tonemapping operator is non-linear, the same with blooming etc. Also doing it pre-tonemapping – in linear, not in gamma space is essential for proper color and light intensity blending…