---
title: Why the rendering in The Order 1886 rocks.
url: http://c0de517e.blogspot.com/2015/02/why-rendering-in-order-1886-rocks.html
published: '2015-02-27'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**Premise**: Initially I thought I would post an "analysis" similar to the one I did on Battlefield a while ago, just my personal notes and screenshots taken as I played the game, isolated from any outside source of information (discussions between coworkers and other people, which I bet are happening everywhere right now across the industry).*In the end I took an even more "high level" approach, so these notes won't really talk about techniques and speculations (or at least, that's not the main point of view).*



*This is also because I am quite persuaded nowadays that being focused on what matters in an image, being really anal about image quality (correctness, perception) matters more than the specific techniques.*



*Certainly it matters more than "blindly" implementing a checklist of cool technology, better do less and even remove features, but be really conscious about what makes an image and why, rather than trying to add more and more fancy things without understanding.*



*Also, in the following I'll often say "you can/can't notice...". I have to specify, because it matters, that I mean to analyze things that you can notice during mostly "normal" gameplay (in a dark room, with a good projector on a sizeable screen), albeit undertaken by a rendering nerd.*

*Which is different from the work of actually trying to pixel-peep and reverse and break everything on purpose (not that it's easy anyhow in this game...). Which is -still- different from the (very hard) work needed to find all mistakes, as many are don't register rationally, but still are perceptually important.*

**1) Image stability. Technology that doesn't "show".**

Everybody is raving about The Order's antialiasing, and rightfully so. We know it's some sort of 4x MSAA (nowadays that still leaves open a lot of variables on how it's implemented...) and that certainly helps a lot.

But it's not just 4x MSAA, we've seen many titles with MSAA, and you can even crank it on PC titles, yet I'd say nothing before came close to the "offline" rendering feeling The Order exhibits.

![]() |

And I think that's not just supersampling, but it's paying attention to pixel quality overall. Supersample what can be supersampled, to the extent it can be, filter out the rest, or move it into noise. It's not just antialiasing, it's the whole post-effect pipeline that works together (if you pixel-peek you can actually notice how the motion blur sometimes actively helps killing a tiny bit of leftover specular shimmering).

Do less (in this case, -show- less pixel details) but better (more stable).

![]() |

And while I'm not personally against screen-space effects, in The Order they are noticeable for their absence. I spent some time trying to see if they had SSAO, SS-reflections and so on, and I didn't see anything.

And then you realize, all these techniques, at least as they have been implemented so far, can be spotted, they are not stable, they have telling artifacts.

If a rendering technique "shows", it's already a sign that there's something wrong (e.g. you can say this image has limited depth of field, but if you can spot, this image uses a separable blur, then that's already a problem).

The Order is remarkable even in that regard, a very technical, trained eye might form some educated guesses, but very vaguely I'd say it's really hard to pinpoint most of the specific techniques.

**2) Occlusions. Lighting without leaking.**

I always say, better to have missing lights that light where there shouldn't be.



Even in photography it's easier to see added light than "removed".

Even if you can't spill due to lack of shadowing...

Behind the scenes from Peter Lindbergh and Gregory Crewdson.

Even the unfortunate concession we sometimes do to gameplay, of adding "character" lights to better separate them from the background, visually can be quite "disturbing", but there it is by design - it's supposed to show.

|

Even if you can't spill due to lack of shadowing...

Behind the scenes from Peter Lindbergh and Gregory Crewdson.

![]() |

Don't add an unshadowed light if it's noticeable. And it will -always- be noticeable if it leaks behind surfaces.

While for example a "hair light" on a character in a cinematic can be quite hard to register, a ceiling light shining under a table "disconnects" surfaces and kills realism.

Nowadays occlusion is becoming "easier" with the ability of rendering more shadowmaps (albeit people still complain about the intricacies of shadowmapping) and with more memory many things can be cached as well.

Static, diffuse indirect global illumination is also not a huge deal (e.g. lightmaps and probes).

But specular will kill you. It's quite an hard problem. Bright highlights shining around object silhouettes, behind walls and so on, very tricky to occlude with ambient occlusion and such non-strongly directional methods exactly due to their intensity.

If you've ever played with screen-space reflections you might have noticed, more than solving the problem of missing reflections, they are useful because they effectively capture the right occlusion (together with reflection) of objects in contact with surfaces (which won't be captured with a cubemap probe, even after parallax correction as a box).

![]() |

how specular is hard and screenspace is not enough:

[see it in motion](http://www.benoitdereau.com/unrealparis.html).
Again, The Order doesn't reveal its hand, whatever it uses, it just works.

The importance of specular leaks, together with the fact that it's better to over-occlude than to leak, is always why I think if you can't do anything more, at least baking bent normals (even to the point of having only bent normals, without carrying two sets) pays off.

**3) Atmospherics. Shading the space in-between surfaces.**

We always had some atmospherics. Fog, "ground" fog, "god" rays...

What The Order does there is quite interesting though. London is foggy, and the air is not some kind of afterthought special effect. It's a protagonist in the shading of the image.

It's a recurring theme by now, but again, you can't really "see" it as a special effect or as a specific technique. It's a meaningful contribution to the image that it's much more subtle and harder to capture.

The surprising thing to me is how actually I couldn't really notice dynamic occlusion effects in the fog (volumetric shadows or god rays). Rather what surprises is not such effects but the fact that -every- light scatters, everything subtly changes the color of the fog.

And again the lack of artifacts. You can't see voxels, you can't see leaks, you can't notice particles rotating and fading in and out. Marvellous.

**4) Materials. Attention to detail.**

To each technique its own abuses. First was bloom. Then lens flares. Then depth of field and so on...

There's always a new "must have" feature that gets cranked to eleven to be "cool" and hip until everyone gets disgusted and dials back, just to latch to something else.

![]() |

For PBR it seems metals can be problematic. More than one game I've seen nowadays that pushes shiny, perfectly polished stuff everywhere, I can't really understand why.

![]() |

But it really has some issues with shiny metals, the Orlais palace is one of the worst offenders.

The Order instead doesn't ever lose its composure. Materials are never constant, are never flat, they are varied and realistic and realistically blend into each other. Even small details, light lightbulbs and refraction, or the sheen of the ink on printed paper, is great.

Texture resolution is constant, you never notice issues between textures of nearby objects with different densities.

![]() |



**Bonus round: baking.**

Many games, especially around the period of time when deferred got all the hype, lost many of these points (made them worse) by sacrificing baked solutions to real-time computations, often in a misguided attempt of solving authoring problems (which should be the domain of better -tools-, not runtime changes).

Real-time solutions are still useful when gameplay requires dynamic scenes and updates (and we can't stream these!), but if you need realtime feedback on GI, write a realtime path tracer for your lightmaps...

**Bonus round: F+.**

The Order 1886 is famously based on a forward+ lighting engine. I actually wonder how much different it would have been on a old-school "splitting" (static light assignment, to geometry) forward renderer with generous amounts of baking of "secondary" lights. Don't know.

**Bonus round: Next-gen and PC hardware.**

GPU power won't matter until we can specifically target it.

The Order shows that, and that's why a PS4 title can look better than other games which were still targeting the previous console generation and then where upgraded with a few extra techniques to push high-end PC GPUs.

Pushing certain marginal stuff to eleven doesn't make quite as much of a quality difference than creating assets and effects specifically for more powerful GPUs, and that's why even if PCs were already more powerful than these consoles at launch, we have to wait for console games to improve in order to see real advances in games graphics.

## 12 comments:

Offtopic: What kind of a helmet in DS2 screenshot is that?!

I don't know, I shamefully cropped the images from screenshots and videos on the internet. I had a good set of screenshots I've made while playing T.O. as "notes" of various technical things but I was 1) too lazy to grab them and 2) decided not to write the article from a "reverse engineering" point of view

It's a pity that there won't be a "reverse engineering" article. It's always interesting to read those and compare with own observations.


BTW this horse head helmet belongs to enemies called Stone Knights and can't be used by player.

Ready at Dawn has been always eager to share, so I'm sure it's just a matter of time...




I agree that reversing is fun especially as one can actually come up with different ideas!

No one stops people from discussing it here or on twitter or elsewhere... And I can always comment on a given idea outside from my evaluation of The Order.

It's always tricky for me to write articles about other games, and to write in a virtual "clean room" environment, this is the balance I've struck this time.

Seems as though the 2 big issues facing us right now are GI ( non baked ) and reflections. Ive noticed some holes in the 1886 reflection system, notably mirrors, but also some nice things. They have some way of calculating reflection occlusion. They appear to be using environment probes and then using something similar to a point light shadow, add dynamic occlusion to it. You can see it in reflections in small glossy objects like vases and such, and also larger metal objects where the reflection will darken from the influence of the character, but they are not explicitly visible in it, more like a blurry 'shadow figure' is apparent in the reflection. Im guessing they are sort of projecting a point shadow of a low res character model onto the faces of the environment probe. Cheap and effective I guess is how to describe it.

Just thought you should know, your article sold a copy of The Order: 1886—you should get commission or something.



I'm curious, what's your impression of the cut scenes? They look absolutely fantastic (as does the rest of the game), but it seems like they show hints of being rendered real-time, particularly in self-casted shadows on characters. Do you think everything in the game is rendered real-time? At their level, it seems like offline rendering would almost be a waste.

Great post, I enjoyed it!

Doug: that looks like the same tech used in "the last of us"





Michael: I'm pretty sure it's all realtime.

Speaking of artifacts if you look closely you can find a few, of course.

There is still some specular leak due to lack of occlusion of details of normalmaps, you can see some shadows "peter-panning" which is a tell-tale of the use of EVSM or similar and many other little things here and there.

That's why I wrote in the premise that when I say that there are no noticeable artifacts I mean during normal viewing, not pixel-peeking.

Another example might be the recent Call of Duty: Advanced Warfare.

I'd say aliasing isn't really noticeable during gameplay in that game (albeit certainly it doesn't have the same quality of The Order in that respect, both for lack of MSAA and for lack of aggressive blurring) which -really- surprised me.

But it's easy to see if one goes slowly and pays attention, that it does just some post-processing AA, it's just that art was made in a way such that it's never horribly distracting

Thanks for the response! I wonder how much of a difference having a controlled, non-interactive scene makes in terms of resource budget—I don't have experience with that. i.e., during the council scene, I noticed light scattering through a character's ears, but the character was far away, so while it could of course be faked (not calculated in real-time), it would seem that a break from PBR for such a small effect would be counterproductive and worse than actually implementing the technique. Just trying to learn by example/extension as I'm not that far along on these graphics things.

Certainly the more "fixed" your scenario is the more it helps in a number of ways, in fact you can see how on average "open world" games tend to have many more defects/issues that are easy to spot than linear "corridor" ones.


For the ear and nose translucency, I think it's realtime, and sometimes you can see how the technique is not perfect, I think in that regard Jorge Jimenez's work is the state of the art

Hi. Thank you for your quite interesting article !







I have some information about occlusion in "The Order : 1886".

>> Again, The Order doesn't reveal its hand, whatever it uses, it just works.

In GDC2014, they said that they are baking directional AO Maps (H-Basis) for characters and static geo.

And using them to mask specular from cubemaps.

( Please see the page 18 of this slide.

http://t.co/17GYfuVOze )

Very good analysis, thanks for writing this up.



The character reflections piqued my interest, they seem to use the same system for both glossy/water reflections and "contact AO" on walls etc. Their silhouette is too well defined to be based on Last of Us' capsule based system in my opinion, they look as if they render and project a blurry/low res version of the character instead.

Looking forward to a presentation of the render techniques, the game looks amazing.

Hm, it seems I was wrong, I went through the GDC presentation again, they do mention that the contact AO is indeed based on skinned capsules. The question then is how they do the reflections. :-)

Post a Comment