---
title: White balance and physically based rendering pipelines. Part 2 – practical
  problems.
url: https://bartwronski.com/2015/10/14/white-balance-and-physically-based-rendering-pipelines-part-2-practical-problems/
published: '2015-10-14'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## White balance and lighting conditions

After [this long introduction](https://bartwronski.com/2015/10/14/white-balance-and-physically-based-rendering-pipelines-part-1-introduction/) (be sure to check part one if you haven’t!), we can finally go to the problem that started whole idea for this post (as in my opinion it is unsolved problem – or rather many small problems).

The problem is – what kind of white balance you should use when capturing and using IBLs? What color and white balance you should use while accumulating lights. When the white balance correction should happen? But first things first.

Image based lighting and spherical panoramas. Typical workflow for them is fixing the exposure and *some* white balance (to avoid color shifts between shots), taking N required bracketed shots and later merging them in “proper” software to panoramas. Then it is saved in some format (DDS and EXR seem to be most common?) that usually is only a container format and has no color space information and then after pre-filtering used in the game engine as the light source. Finally magic happens, lighting, BRDFs, some tonemapping, color grading, output to sRGB with known target monitor color balance and view conditions… But before that “magic” did you notice how vaguely I described white balance and color management? Well, unfortunately this is how most pipelines treat this topic…

## Why it can be problematic?

Ok, let’s go back to setting of white balance, during single time of day, same sun position – just a photo captured in shadows and in the sunlight.

![Photo 1, Lightroom/ACR Cloudy WB (6500K) – shadows have no tint, but the photo looks probably too warm / orange.](../../assets/577f542ccccf2335.jpg)


![Photo 1, Lightroom/ACR Cloudy WB (6500K) – shadows have no tint, but the photo looks probably too warm / orange.](../../assets/577f542ccccf2335.jpg)

Photo 1, Lightroom/ACR Cloudy WB (**6500K**) – shadows have no tint, but the photo looks probably too warm / orange.

![Photo 2, same time and location, behind the building, camera auto WB (5050K) – blue color cast.](../../assets/9f9183794dc8427a.jpg)


![Photo 2, same time and location, behind the building, camera auto WB (5050K) – blue color cast.](../../assets/9f9183794dc8427a.jpg)

Photo 2, same time and location, behind the building, camera auto WB (**5050K**) – strong blue color cast.

![Photo 2, same time and location, behind the building, cloudy WB (6500K) – color cast gone (maybe slight hint of magenta).](../../assets/4dda396210999971.jpg)


![Photo 2, same time and location, behind the building, cloudy WB (6500K) – color cast gone (maybe slight hint of magenta).](../../assets/4dda396210999971.jpg)

Photo 2, same time and location, behind the building, cloudy WB (**6500K**) – color cast almost gone (slight hint of magenta).

Imagine now that you use this images as an input to your engine IBL solution. Obviously, you are going to get different results… To emphasize the difference, I did a small collage of 2 opposite potential solutions.

In this example the difference can be quite subtle (but obviously shadowed parts either get blueish tint or not). Sometimes (especially with lower sun elevations – long shadows, lower light intensities, more scattering because light travels through larger layer of the atmosphere) it can get extreme – that it is impossible to balance wb even within a single photo!

Example:

![“Neutral”/medium white balance, 5350K. People probably wouldn’t look right neither in shadows (too strong blue tint) nor in sunlight (too strong orange/yellow tint). This is however how I think I perceived the scene at this time.](../../assets/cdae4a4d906fa5e8.jpg)


![“Neutral”/medium white balance, 5350K. People probably wouldn’t look right neither in shadows (too strong blue tint) nor in sunlight (too strong orange/yellow tint). This is however how I think I perceived the scene at this time.](../../assets/cdae4a4d906fa5e8.jpg)

“Neutral”/medium white balance, **5350K**. People probably wouldn’t look right neither in shadows (too strong blue tint) nor in sunlight (too strong orange/yellow tint). This is however how I think I perceived the scene at that time.

What is really interesting is that depending on which point you use for your IBL capture (is your WB and grey card set in shadows or in sunlit part), you will get vastly different lighting and scene colors.

So, depending on the white balance setting, I got completely different colors in lights and shadows. It affects the mood of whole image, so should depend on artistic needs for given photograph/scene, but this level of control cannot be applied on the final, sRGB image (too small color gamut and information loss). So when this artist control should happen? During the capture? During lighting? During color grading?

## Digression – baking lighting, diffuse bounces and scattering taking full light spectrum into account

Quite interesting side note and observation to which I also don’t have a clear answer – if you go with one of the extremes when taking your panorama for IBL, you can even get different GI response after the light baking! Just imagine tungsten lights in a blue room; or pure, clear sky early afternoon lighting in an orange room – depending if you perform the WB correction or not you can get almost none multi-bounced lighting versus quite intense one.

The only 100% robust solution is to use spectral renderer. Not many GI bakers (actually, are there any?) support spectral rendering. Some renderers start to use it – there was an interesting presentation this year at Siggraph about its use at Weta [http://blog.selfshadow.com/publications/s2015-shading-course/](http://blog.selfshadow.com/publications/s2015-shading-course/) “Physically Based Material Modeling at Weta Digital” by **Luca Fascione** (slides not yet there…).

In similar manner **Oskar Elek** and **Petr Kmoch** pointed out importance of spectral computations when simulating scattering and interaction of atmosphere and water: [http://people.mpi-inf.mpg.de/~oelek/](http://people.mpi-inf.mpg.de/~oelek/) [http://www.oskee.wz.cz/stranka/uploads/Real-Time_Spectral_Scattering_in_Large-Scale_Natural_Participating_Media.pdf](http://www.oskee.wz.cz/stranka/uploads/Real-Time_Spectral_Scattering_in_Large-Scale_Natural_Participating_Media.pdf) .

I don’t think we need to go that far – at least for this new console generation and until we eliminate much more severe simplifications in the rendering. Still – it’s definitely something to be aware of…

## White balance problem and real-time rendering / games

Coming back to our main problem – since all those images come from a photograph and natural, physical light sources this is an actual, potentially serious problem –if you are using or considering use of real-world data acquisition for the IBLs and/or scientific physical sky models for sky and ambient lighting.

Just to briefly summarize the problem and what we know so far:

- Different times of day and lighting conditions result with completely different temperature of light even just for sun and sky lighting.
- Panoramas captured with different white balance camera settings that could depend on the first shot will result with completely different color temperature.
- Images or light sources with different color temperature don’t work well together (mixing/blending).
- If you stay with 1 white balance value for every scene, uncorrected lighting will look
**extreme**and ugly (tungsten lights example or extremely blue skies). - Sometimes there are many light sources in the scene with different color temperature (simplest example– sky/sun) and you cannot find a white balance that will work in every situation; you can end up with strong tint of objects when only 1 of light sources is dominating the lighting (the other one in the shadows) no matter what are your settings.
- Different white balance can achieve different mood (cool / warm; day / afternoon / evening; happy / sad) of final presented scene – but it is not (only) part of color grading; usually it is set for “raw” data, way before setting the final mood; when computing the sky model or capturing skies / panoramas.

Such summary and analysis of the problem suggests some possible solutions.

Before suggesting them, I’m going to write about how those problems were “hidden” in previous console generation and why we didn’t notice them.

## Why in previous generation games and non-PBR workflows we didn’t notice those problems? How we solved them?

In previous console generation, light color and intensity and ambient color were abstract, purely **artistic** concepts and often **LDR** and “**gamma**“. The most important part is especially the ambient color. “Ambient” was defined in many alternative ways (ambient hemispheres – 2 colors, ambient cube – 3-6 colors), but it had nothing to do with sky and sun rendering.

So lighters would light environment and characters to achieve specific look and color balance (usually working mentally 100% in sRGB), not taking into consideration any physical properties and color temperature of light sources to achieve specific look that they or the art director envisiounes. Even with HDR workflows, ambient and light intensities had nothing to do with real ones, were rather set to be convenient and easy to control with exposure. In ** Assassin’s Creed 4: Black Flag **we had no exposure control / variable exposure at all! Very talented lighting artists were able to create believable world working in 8bit sRGB as both final and intermediate color space!

Then concept, environment and effect artists would paint and model sky and clouds, throw in some sun disk flare or post effect god rays and viola. Reflections were handled only for by special system of planar (or cube) reflections, but indirect speculars were virtually non-existent. Metals had some special, custom, artist authored (and again sRGB/gamma) cubes that had nothing to do with the sky and often the environment itself.

This doesn’t mean that there was no problem. Wrong handling reflections and indirect specular lighting was one of many reasons for the transition for PBR workflows (and this is why so many engines demos show buzz-worded “next-gen PBR rendering” with metal/wet/shiny areas 😉 ). Without taking properly environment and image based lighting into account, surfaces looked flat, plastic, and unnatural. When we integrated IBL and “everything has specular and Fresnel” workflows, suddenly artists realized that different sky and reflections can look wrong and result in weird rim lighting with intensity and color not matching the environments. Things would get completely out of control…

Also modern normalized and energy conserving specular distribution functions, physically correct atmospheric and fog effects and energy conserving GI started to emphasize the importance of high dynamic range lighting (you don’t have big dynamic range of your lights? Well, say goodbye to volumetric fog light shafts). As intuitively understanding differences in lighting intensity of many EV within a single scene is IMO virtually impossible, to gain to get consistent behavior we started to look at physical and correct sky and sun models. This on the other hand – both if using analytical models as well as IBL/photogrammetry/real captured panoramas – shown us problems with the white balance and varied color temperature of lighting.

![Intuitively set and “hacked” proper, film-like color balance in Witcher 2. Lots of work and tweaking, but at that time the result was amazing and critically acclaimed –all thanks to good artists with good understanding of photographic concepts and hours and hours of tweaking and iteration...](../../assets/a845bdb57402e43b.jpg)


![Intuitively set and “hacked” proper, film-like color balance in Witcher 2. Lots of work and tweaking, but at that time the result was amazing and critically acclaimed –all thanks to good artists with good understanding of photographic concepts and hours and hours of tweaking and iteration...](../../assets/a845bdb57402e43b.jpg)

Intuitively set and “hacked” proper, film-like color balance in **The Witcher 2**. Lots of work and tweaking, but at that time the result was amazing and critically acclaimed –all thanks to good artists with good understanding of photographic concepts and hours and hours of tweaking and iteration…

Before I proceed with describing more proper solutions I wanted to emphasize – importance of it now doesn’t change the fact that we were looking at importance of color balance even with previous, physically not correct games. It was partially achieved through lighting, partially through color grading, but artists requested various “tweaks” and “hacks” for it.

On * The Witcher 2* I had a privilege to work with amazing artists (in all departments) and lots of them were photographers and understood photography, lighting and all such processes very well. We experimented with various elements of photographic workflow, like simulation of

**polarizing filter**to get more saturated skies (and not affecting the tonemapping too much). Or sometimes we would prototype total hacks like special color grading (as you can imagine usually blue) applied only in shadows (you can imagine why it was quite a terrible idea 😀 but this shows how intuitive need for specific look can be attempted to be achieved in “hacked” ways).

With one of artists we even tried to simulate **dynamic white balance (in 2011/2012?)** – by changing it in artist authored way depending on the scene average luminance (not average chrominance or anything related) – to simulate whole screen color cast and get warmer WB in shadows/darker areas; and on the other hand had nice color variation and blueish shadows when the scene had mostly sunlit areas.

Now lots of it sounds funny, but on the other hand I see how artists’ requests were driven by actual, difficult physical problems. With better understanding of PBR, real world lighting interactions and BRDF we can finally look at more proper/systemic solutions!

## Dealing with the white balance – proposed solutions

In this paragraph I will first present my general opinions but later group some “alternatives” I don’t have strong opinion about.

One thing that I would assume is a must (if you don’t agree – please comment!) is sticking with a single color balance value for at least a scene (game fragment / time of day?). This should be done by a lighter / artist with strong photographic / movie background and good understanding of white balance. This way you get proper analytical lights interactions and realistic resulting colors (warm sun color and cooler sky color balance out perfectly).

One could argue that “old-school” way of mixing various light sources with different color balance, just artists making them quite “neutral” and not tinted and rely on color grading is “better”/”easier”. But then you will never get natural looking, blueish shadows and perfect HDR balance of light/shadow. Also you lose one of biggest advantages of PBR – possibility to reason about the outcome, to verify every element in the equation, find errors and make your lights / materials / scenes easily interchangeable (consistency in whole game!).

Ok, one light white balance value. How should you chose this color balance? I see two options:

- Sticking with a
**single value for whole game**– like this common final sRGB**6500K**for**D65**. And therefore achieving all the proper color warmth / coolness via final color balance/grading/correction only. It is definitely possible, but without color balance applied (pre color correction), some scenes will look extremely weird (orange/blue or even green if you have fluorescent lights). You also need to do your color correction in a gamut wider than regular sRGB (which is assumed to be in final white balance) – just like for proper photo WB you need “**RAW files**“. I see many more benefits of color grading in wider color spaces and higher dynamic range (maybe I will write more about it in future), but it’s not something that many titles seem to be doing now. - Picking this
**value per scene**to “neutralize” white balance either in shadows or sunlit parts (or maybe a 50/50 mix of both?). It gives much easier starting point, nice looking intermediate values, understandable and good looking HDR sky cubemaps and artist-authorable skydomes – but you need to be aware of it all the time! Also blending between various lighting conditions / zones becomes more tricky and you cannot as easily swap elements in the equation – “*lets take sky capture from the noon and sun radiance from the morning*” won’t work. On the other hand it is probably not very good idea anyway. 🙂 Still, it can be more difficult for games with dynamic / varying time of day.

Finally, should the color corrected, display white balance be fixed or should it auto-adapt? This is the most controversial topic. Lots of programmers and artists just hate automatic exposure / eye adaptation… And for a good reason.

It is **very** difficult (impossible) to do properly… and almost nothing really works just like artist / art director would like it to work… too much contrast / not enough contrast; too dark / too bright; too slow / too fast. It’s impossible to be solved completely – no matter how accurate, you can imagine manual settings being artistically better and better serving the scene.

And yet, here we talk about adding an additional dimension to the whole auto-camera-settings problem!

I see 2 “basic” solutions:

- Accepting
**no white balance eye adaptation**and different color cast in shadows and lights. For crucial cinematics that happen in specified spots, manually overriding it and embedding in color grading/color correction fixed to this cinematic. Either fading it in smoothly, or accepting difference between camera cuts. - Adding
**auto white balance**. I still think that my original “old-school” idea of calculating it depending on the average reflected**luminance**+ knowledge of the scene light sources can work pretty well… After all, we are lighting the scene and have all the information – way more than available in cameras! If not, then taking diffuse lighting (we definitely don’t want to take albedo into account! On the other hand, albedo is partially baked in with the GI / indirect lighting…) and calculating clamped/limited white balance.

But I see a third one and that can actually work for auto-exposure as well:

- Relying on some baked or dynamically calculated
**information about shadows, sky visibility**averaged between some sparse points around the camera. We tend to perceive white balance and exposure “spatially” (and averaging values when looking around), not only depending on current “frame” (effective sharp FOV vs. lateral vision) and I see no reason why we shouldn’t try it in real time rendering.

For me this is quite fascinating and open topic and I’m still not sure what kind of attitude I would advocate – probably it would depend on the title, setting, lighting conditions, and existence or not of day cycle etc.

I hope I presented enough ideas and arguments to inspire some discussion – if you have any feedback on this topic, please comment!

(Next paragraph is just a small rant and feel free to skip it.)

### Is research of Physically Based Rendering workflows inventing new / non-existent / abstract problems?

This sub-chapter is again a digression, probably could be in any article about anything PBR workflow-related.

But yet this is a question I keep hearing very often and probably any programmer or technical artist will hear it over and over. If you think a bit about it, it’s like with deeper and deeper understanding of physically-based-rendering and more and more advanced workflows we “invent” some new problems that didn’t exist in the past…

Yes, everyone who is in the industry for a while has shipped games with gamma-space lighting, without properly calibrated monitors (my pet peeve – suggestions of “calibrating” for an “average” TV…), with no care for sRGB/REC-709, color spaces, energy conservation, physical light units, EVs or this unfortunate white balance…

In Witcher 2 we didn’t care about any BRDFs; most reflective surfaces and their indirect speculars were achieved through artist-assigned per-shader tweaked cubemaps – so characters had different ones, environment assets had different ones, water had different ones… And still the game looked truly amazing at that time.

Does that mean we shouldn’t care for understanding of all those topics? No, definitely not. We are simply further on the curve of diminishing returns – we must invest much more, gain way more understanding and knowledge to progress further. Things are getting more complicated and complex, it can be overwhelming.

But then you can just look at recent titles like Assassin’s Creed: Unity, The Order 1886. The upcoming Frostbite engine games like Star Wars: Battlefront. Demos from Unreal Engine 4. Photogrammetrically scanned titles like The Vanishing of Ethan Carter made by teams of 7 people! You can clearly see that this extra know-how and knowledge pays off.

Good luck getting such fidelity of results in such scale with old bag of hacks!

Pingback: White balance and physically based rendering pipelines. Part 1 – introduction. | Bart Wronski

Excellent, thoughtful observations, Bart!

While PBR material authoring has become common practice, PBR light authoring practices are less mature. Some blockers preventing runtime white balance correction would be cases where perceived white-balance correction is baked in to content. For example, artists may author incandescent light and sun-light colors with similar yellow hues, where those light sources should have very different temperatures. HDRI IBL photos can be captured at different white balance corrections in order to recreate perceived colors, where interior and exterior IBLs should co-exist at very different temperatures. How can we author HDR and wide-color range content in ways that can be intuitive for artists?

Hi David! Thanks for stopping by and commenting. 🙂

As I said, I don’t really know and I’m not sure what is the correct answer. One extreme end of the spectrum (no pun intended) and “proper” solution is spectral rendering and picking lights only from presets that follow single, united and pre-defined space and possibly spectral rendering using real wavelengths of the sources (or some color space like LAB / CIE XYZ). Opposite, more “game” and old-school approach is just sticking with colors and intensities and hoping that artists intuitively understand those properties. While I think we are slowly heading towards really physically correct rendering and correctness, now optimal workflow is somewhere in the middle. My intuition says that storing HDRI IBL with capture settings (EV corresponding to aperture/ISO/f-stop AND the capture white balance) and converting in the engine to “transparent” / invisible to artist color spaces, mixing lights and converting back to REC-709 with artist-specified white balance is the way to go. Plus maybe some minor, constrained auto WB. I will try to push such workflow in the studio, but have no idea if it will work out well – hence my posts and asking the rendering community how everyone else deals with this problems…

This is going to be fun when trying to ship an “HDR TV” game! Current specs call for DCI colorspace, 1,000 nits max, and 10bit output. Not too bad from a 64bit tonemapping perspective, but then you’re going to have to ship REC 709 standard at the same time! Wheeeee.

Oh yes! Twice the problems for balancing and testing… I wonder how much HDR TVs are going to become a standard and how much of it is a temporary trend (a bit like 3D TV for games)…

For automatic white balance, could you calculate the average scene color temperature using the albedo channel from the Gbuffer, and compare that to the average scene color temperature after applying lighting? (Or use a separate buffer that stores lighting only, if available)

Then you could use the difference of the two to adjust the white balance in post-processing. (You could also interpolate this over time, similar to eye-adaptation)

Thanks for the awesome blog posts by the way!

Yes, so generally it’s possible to compute it from lighting buffer – albedo wouldn’t work as you don’t want to adapt to colors

of objects; this is called “grey world model” and has been a bane of many white balancing algorithms for a long time.

On God of War I used some computations from lighting buffer and it can work, but then you encounter mentioned problems of mixed lighting.

Funnily I’m now on the other side of the fence – work on computational photography algorithms 🙂 – and mixed lighting and white balancing it is still a big, unsolved problem and something many photographers would like to see addressed.