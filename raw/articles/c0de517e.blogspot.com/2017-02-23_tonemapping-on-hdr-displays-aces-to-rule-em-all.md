---
title: Tonemapping on HDR displays. ACES to rule ‘em all?
url: https://c0de517e.blogspot.com/2017/02/tonemapping-on-hdr-displays-aces-to.html
published: '2017-02-23'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

HDR displays are upon us, and I’m sure rendering engineers worldwide are trying to figure out how to best use them. What to do with post-effects? How to do antialiasing. How to deal with particles and UI. What framebuffer formats to use and so forth.



Well, it appears that in this ocean of new research, some standards are emerging, and one solution that seem to be popular is to use the ACES tone-mapping curve (RRT: Reference Rendering Transform) with an appropriate HDR display curve (ODT: Output Display Transform).

[Infamous Second Son](http://www.glowybits.com/blog/2016/12/21/ifl_iss_hdr_1/)uses it.[Rise of the Tomb Raider](https://developer.nvidia.com/implementing-hdr-rise-tomb-raider)(and it's the advice NVidia is giving).[Krzysztof Narkowicz](https://knarkowicz.wordpress.com/2016/08/31/hdr-display-first-steps/)wrote some very good articles and found good approximations.- Recently it was even added to Unreal Engine.

To my dismay though I have to say I’m a bit baffled, and perhaps someone will persuade me otherwise in the future, but I don’t see why ACES would be a solid choice.

First of all, let’s all be persuaded we indeed need to tone-map our HDR data. Why can’t we just apply exposure and send linear HDR to a TV?

At first, it could seem that should be a reasonable choice: the PQ encoding curve we use to send the signal to TVs peaks at 10.000 nits, which is not too bad, it could allow to encode a scene-referred signal and let the TV do the rest (tone-map according to their characteristics).

At first, it could seem that should be a reasonable choice: the PQ encoding curve we use to send the signal to TVs peaks at 10.000 nits, which is not too bad, it could allow to encode a scene-referred signal and let the TV do the rest (tone-map according to their characteristics).

This is not what TVs do, though. Leaving the transform from scene values to display would allow for lots of flexibility, but would also give to the display too much responsibility over the final look of the image.

So, the way it works instead is that TVs do have some tone-mapping functionality, but they are quite linear till they reach their peak intensity, where they seem to just have a sharp shoulder.

How sharp that shoulder is can depend, as content can also send along meta-data telling what’s the maximum nits it was authored at: for content that matches the TV, in theory no rolloff is needed at all, as the TV will know the signal will never exceed its abilities (in practice though, said abilities change based on lots of factors due to energy limits).



Some TVs will also expose silly controls, like gamma in HDR: what it seems is that these alter their response curve in the “SDR” range of their output, for now let's ignore all that.

Regardless of these specifics, it's clear that you’re supposed to bring your values from scene-referred to display-referred, and to decide where you want your mid-gray to be, and how to roll highlights from there. You need tone mapping in HDR.

Ok, so let’s backtrack a second. What’s the goal a tone-mapping curve? I think it depends, but you might have one or more of the following goals:

- To compress dynamic range in order to best use the available bits. A form of mu-law encoding.
- To provide a baseline for authoring. Arguably that should be a “naturalistic”, perceptual rendition of an HDR scene, but it might even be something closer to the final image.
- To achieve a given final look, on a given display.

HDR screens add a fourth possible objective creating a curve that makes possible for artists on SDR monitor to easily validate HDR values.

I'd argue though that this is a fool's errand though, so we won't investigate it. A better and simpler way to author HDR values on SDR monitors is by showing out-of-range warnings and allowing to easily see the scene at various exposures, to check that shadows/ambient-diffuse-highlight-emissive are all in the ranges they should be.

**How does ACES fit in all this?**

It surely was not designed with compression in mind (unlike for example, the PQ curve), albeit it might somewhat work, the RRT is meant to be quite “wide” (both in dynamic range and gamut), because it’s supposed to then be further compressed by the ODT.

Compression really depends on what do you care about and how many bits you have, so a one-size-fits all curve is in general not probably going to cut it.

Moreover, the RRT is not meant to be easily invertible, much simpler compression curves can be applied, if the goal is to save bits (e.g. to squish the scene into a range that can then be manipulated with the usual color-grading 3d LUTs we are accustomed to).

It wasn’t designed to be particularly perceptually linear either, preserve colors, preserve brightness: the RRT is modelled after film stock.

So we’re left with the third option, a curve that we can use for final output on a display. Well, that’s arguably one of the most important goals, so if ACES does well there, it would be plenty.

At a glance also, that should be really its strength, thanks to the fact that it couples a first compression curve with a second one, specific to a given display (or rather, a display standard and its EOTF: electro-optical transfer function). But here’s the problem. Is it reasonable to tone-map to given output levels, in this situation?

With the old SDR standards (rec.709 / BT.1886) one could think that there was a standard display and viewing ambient we targeted, and that users and TVs would compensate for specific environments. It would have been a lie, but one could have hand-waved things like that (in practice, I think we never really considered the ambient seriously).

In HDR though this is definitely not true, we know different displays will have different peak nits, and we know that the actual amount of dynamic range will vary from something not too different than SDR, in the worst ambients, to something wide enough that could even cause discomfort if too bright areas are displayed for too long.

ACES itself has different ODTs based on the intended peak nits of the display (and this also couples with the metadata you can specify together with your content).



All this might work, in practice today we don’t have displays that exceed 1000 nits, so we could use ACES, do an ODT to 1000 nits and if we can even send the appropriate meta-data, leaving all the eventual other adjustments to the TV and its user-facing settings. Should we though?

If we know that the dynamic range varies so much, why would we constrain ourselves to a somewhat even complex system that was never made with our specific needs in mind? To me it seems quite a cop-out.





*Note: for ACES, targeting a fixed range makes a lot of sense, because really once a film is mastered (e.g. onto a blue-ray) the TM can't change, so all you want to do is make sure what the director saw on the reference screen (that had a given peak nits) matches the output, and that's all left to the metadata+output devices. In games though, we can change TM based on the specific device/ambient... I'm not questioning the virtues of ACES for movies, the RRT even was clearly devised as something that resembles film so that the baseline TM would look like something that movie people are accustomed to.***Tone-mapping as display calibration.**
I already wasn't a fan of blindly following film-based curves and looks in SDR, I don’t see why this would be the best for the future as well.

Sure, filmic stocks evolved over many years to look nice, but they are constrained to what is achievable with chemicals on a film…


It is true that these film stocks did define a given visual language we are very accustomed to, but we have much more freedom in the digital world today to exploit.

We can preserve colors much better, we control how much glare we want to add, we can do

Sure, filmic stocks evolved over many years to look nice, but they are constrained to what is achievable with chemicals on a film…

It is true that these film stocks did define a given visual language we are very accustomed to, but we have much more freedom in the digital world today to exploit.

We can preserve colors much better, we control how much glare we want to add, we can do

[localized tone-mapping](http://c0de517e.blogspot.ca/2016/10/more-silly-tone-mapping-ideas.html)and so on. Not to mention that we got so much latitude with color grading that even if a filmic look is desired, it's probably not worth delegating the responsibility of achieving it to the TM curve!
To me it seems that with HDR displays the main function of the final tone-mapping curve should be to adapt to the variability of end displays and viewing environments, while specific “looks” should be achieved via grading, e.g. with the help of compression curves (like



[s-log](https://pro.sony.com/bbsccms/assets/files/mkt/cinema/solutions/slog_manual.pdf)) and grading 3d LUTs.
Wouldn’t it be better, for the final display, to have a curve where it’s easy for the end user to tweak

[the level at which mid-grays will sit, while independently control how much to roll the highlights](http://gpuopen.com/vdr-follow-up-fine-art-of-film-grain/)based on the capabilities of the TV? Maybe even having two different "toes" for OLED vs LCDs...
I think it would even be easier and safer to even just modify our current tone-mapping curves to give them a control over highlight clipping, while preserving the same look we have in SDR for most of the range.

That might avoid headaches with how much we have to adjust our grading between SDR and HDR targets, while still giving more flexibility when it comes to display/ambient calibration.


HDR brings some new interesting problems, but so far I don't see ACES solving any of them. To me, the first problem, pragmatically, today, is calibration.

A more interesting but less immediate one is how much HDR changes perception, how to use it not just as a special effects for brighter highlights, but to really be able to create displays that look more "transparent" (as in: looking through a window).

That might avoid headaches with how much we have to adjust our grading between SDR and HDR targets, while still giving more flexibility when it comes to display/ambient calibration.

HDR brings some new interesting problems, but so far I don't see ACES solving any of them. To me, the first problem, pragmatically, today, is calibration.

A more interesting but less immediate one is how much HDR changes perception, how to use it not just as a special effects for brighter highlights, but to really be able to create displays that look more "transparent" (as in: looking through a window).

Is there a solid reason behind ACES, or are we adopting it just because it’s popular, it was made by very knowledgeable people, and we follow?



Because that might not be the worst thing, to follow blindly, but in the past so many times did lead to huge mistakes that we all committed because we didn’t question what we were doing… Speaking of colors and displays, a few years ago, we were all rendering using non-linear (gamma transformed) values, weren’t we?








**Update!**

*The ACES committee recognized some of the issues I described there, and are working on a new standard. A document*["ACES Retrospectives and Enhancements"](https://github.com/colour-science/aces-retrospective-and-enhancements)was made, which I find very agreeable.

*I'm still not sure what would be the benefit to go towards ACES for us (we don't mix and match shots from different sources, we really don't care about a standard).**FWIW I'm now completely persuaded we should just do a simple, fixed-shape TM step to compress our render output into a space that allows to color-grade, perform all artistic decision in grade then do a final TM step to adapt to the TV output.**This step is also described very well in Timothy Lottes GDC presentation*["](https://32ipi028l5q82yhj72224m8j-wpengine.netdna-ssl.com/wp-content/uploads/2016/03/GdcVdrLottes.pdf)[Advanced Techniquesand Optimization of VDR Color Pipelines".](https://32ipi028l5q82yhj72224m8j-wpengine.netdna-ssl.com/wp-content/uploads/2016/03/GdcVdrLottes.pdf)

*Furthermore, games should set on a neutral default grading that is used through production as a baseline for asset review - and that should not be based on ACES, but on a curve that tries to be as neutral/naturalistic as possible.*
## 4 comments:

The goal of HDR screens from the HDR-BD point of view is to reproduce the pixels that the Director saw on the Mastering screen just in your home. There is a promise of fidelity that, given the panel you have purchased, the resulting image will be as similar to the Directors' Mastering image as possible.




We need to take the same outlook in games. You master it then ship it and HSDR screens will faithfully reproduce the look you had on your screen at release. The issues of perceived contrast reduction because of viewing in brightly lit rooms or with white surrounds is something the TVs allow the user to fix locally using their TV controls.

The Filmic Curves are used in ACES to allow a director to view Slog3 or Linear data with a look applied that matches what he would have seen in rushes if he had used film - it's a familiar look, a basic "first pass" tool for use live and on-set. Making it the ultimate look for games is mystifying.

So, for that you don't need ACES, right? You can use whatever random curve, it doesn't matter. What might matter at best is that you match your peak nits with the metadata, but that's afaik not something we have control over right now.




Pragmatically though, saying that the users and TVs will figure it out is a cop-out I feel. Why then we added gamma-calibration screens to games? We did because in practice, even in the world of SDR, which had less variance, we needed to give some control and some calibration (and gamma might actually not have been the best control, but I don't think anyone really gave -a lot- of thought to the problem).

Regarding having a standard look, I'd argue that the film look should not be our standard, but that's another war... More importantly though I think that whatever look you want to give your artists as a base, that is something you can establish more precisely and easily via a standard grade, instead of a TM curve.

There is some discussion in the ACES community on simplifying the RRT and making it invertible, as well as moving the "film stock" flavor to a LMT (which is arguably where it belongs conceptually).




If you've followed the film vs digital debate, you know that there are some psychological advantages in having "film stock" qualities to your system. In the motion pictures industry, where resistance from DoPs and directors has been really strong, it took years and a "film stock" qualities digital camera from Arri to establish digital, despite its numerous practical advantages. No wonder that this became an integral part of the initial iteration of ACES.

ACES is fundamentally just a color management framework. Color fidelity framework, if you will. These have been around in the film/video context, originally introduced by Filmlight for their Baselight grading system, and later added to more grading platforms. ACES is then just a continuation of these efforts, an attempt for standardizing a color workflow practice and facilitating interop: you often have cameras from multiple vendors pouring footage in a project, multiple houses producing VFX, compositing, grading, etc. Should they always use ACES? Certainly not. The film industry was doing ok even before ACES. But it sure helps some.

Should this be copied blindly to video games? Nope. (And, ofc, nothing should be copied blindly, in general.) Ideally, it should be just an option. A tool in the box. It may come handy, though, if you want to use CGI made in a game engine in a film production. And I'd argue that in a world of meh washed out tone curves, the ACES curve is among the better choices for a default in a mass market engine, so its default status in Unreal is well grounded.

IMO, the point of using ACES in a game engine is very similar to the point in the movie industry: standardization.











I'm sure we all agree that you can not render linear values directly to a display and have it look perceptually correct. Not to mention clipping at the shoulder. Same way you can not take linear output from a CCD sensor and display it directly. It will look like crap. So you need SOME tone curve.

I hope no one is arguing for a tone curve that is linear except for the shoulder roll-off to avoid clipping. See above. It'll look like crap, and you'll never be able to tune your lighting and materials to look reasonable in all conditions, because you're compensating in the materials for the wrong tone curve. Been there, done that.

PBR materials use albedo textures, which should ideally contain correct reflectance values captured from the real world. Those materials look reasonable by default under a filmic tone curve, as the goal of your HDR/PBR rendering is to generate linear luminance values that match the real world. The same values a CCD sees. So if you can apply a filmic tone curve to CCD output and have it look reasonable, you should be able to apply the same filmic curve to game engine output, and have it look just as reasonable. Conversely, you don't display linear CCD output on a display linearly and call it a day. You need some s-shaped, "filmic" curve, with a shoulder and a toe.

Once we agree that you need a filmic curve: there's ACES.

Now why not use the Uncharted tone curve, or some other random tone curve?

Standardization.

Sure, you can make a nice looking game with just about any filmic tone curve. But while it's nice to think that PBR materials all use real world albedo values, in a game that's not generally the case. Artists will paint stuff, and they will paint it to look nice given the tone curve and lighting. Since PBR lighting is a known quantity, and it's generally done well, a light source in Substance Designer should affect a material about the same as a light source in your engine. Any intensity difference is just an exposure adjustment, and exposure is not a real issue when authoring materials. The tone curve is, because it affects contrast and saturation. So if let's say Substance used an Uncharted tone curve, and your engine used ACES, stock Substance materials would not look quite as intended in your engine, and artists would constantly have to tweak stock Substance materials. Colors would be over or under-saturated, albedos at the darker end of the scale might look black or washed out grey, etc.

What's worse is that Substance and other content creation packages have been using a linear tone curve since the beginning of time, and only now people are starting to catch on. Rendering with a linear tone curve is almost as wrong as rendering in gamma space. It's taken way too long for the industry to catch on.

If everyone in the game industry transitions to ACES, then it's a lot more feasible to share material assets between packages. See Substance materials, Megascans, etc.

You still have full control over color grading at the end of the pipe, to tune the look of your game to your taste, just as you do in film. That is not the job of the tone mapper. The job of the tone mapper is to represent a linear image in a perceptually reasonable way on a display, which is the mission statement of the ACES RRT. Everything before color grading needs to be predictable and standardized to enable sharing of assets. The old standard "linear" is atrocious. ACES is reasonable. So we might as well use ACES!

Post a Comment