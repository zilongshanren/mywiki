---
title: The three skin rendering horrors you want to avoid
url: http://c0de517e.blogspot.com/2011/12/three-skin-rendering-horrors-you-want.html
published: '2011-12-12'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

It's 2011 and still most games come with some truly horrific skin rendering. I don't think skin is that hard to get decent, but you have to understand what's important and how to hack it in your lighting/rendering model.

This article won't focus on the state of the art skin rendering techniques or on the state of the art acquired data for skin, these things are really important, fundamental, go ahead and google them, there's plenty to read and it's not hidden knowledge at all (start with

[Debevec](http://www.pauldebevec.com/)and[Jensen](http://scholar.google.ca/scholar?q=related:3H8Wormo6doJ:scholar.google.com/&hl=en&as_sdt=0,5)).
What I want to do here is just a write up of what I've learned about skin in my experience, and some of the common technical mistakes I've seen.

**1- Bad tone**

![]() |

By far, the

[worst offender](http://c0de517e.blogspot.com/2010/03/skin.html). Nailing the right colours from the day to the nightside of the skin is the most important, and most often neglected things. And yes, it is mostly (but not only) a matter of subsurface scattering, as most of the skin diffuse lighting comes from it, but it's not about complicated techniques. It's about understanding what happens, what's important to model and how to hack it in whatever lighting model you have in your rendering.
You can get great skintones with even the simplest hacks on top of your basic lambert, and horrible tones by badly tuned texturespace or screenspace diffusion techniques. Penner's

Also, remember that scattering will affect all the skin shading, you might want to "ramp" the edges of the shadowmaps (again, Penner's paper covers that) but it's actually often even more important to properly blend AO on skin, especially if you're using a normal-aware SSAO which is capable of capturing very fine details, a straight multiply will create some really questionable gray patches. Again, even simple hacks, like adding a slight constant colour to your SSAO, will go a long way towards creating more organic skin.



Debevec, Digital Emily, Acquired Diffuse


[pre-integrated skin shading](http://www.ericpenner.net/portfolio/)is the current champion of the lambert hacks, but truth is that some sort of ramp on top of your lambert is everything you need (that's to say, you can most often get decent results without even bothering to approximate the geometry with the curvature, as Eric does) if you nail the right hues!Also, remember that scattering will affect all the skin shading, you might want to "ramp" the edges of the shadowmaps (again, Penner's paper covers that) but it's actually often even more important to properly blend AO on skin, especially if you're using a normal-aware SSAO which is capable of capturing very fine details, a straight multiply will create some really questionable gray patches. Again, even simple hacks, like adding a slight constant colour to your SSAO, will go a long way towards creating more organic skin.

![]() |

Give your artists the right tools! It's fundamental to be able to tune the skin while comparing the rendered results with some reference material (put an image viewer and color sampler in game!), it's fundamental to tune colors after fixing your tone-mapping operator, and it's fundamental to understand _all_ your sources of color: shading model, parameters, textures.

![]() |

In practice, especially in the realtime rendering world, we mix together all the skin layers and more often than not the problem with skin textures is that they are not saturated enough (consider that the white, additive specular sheen should be responsible for some of the loss of saturation in the final rendering) and have too uniform hues (skin hue shifts quite a lot in many regions, i.e. elbows, joints, hands and

[feet](http://www.3dtotal.com/index_tutorial_detailed.php?id=762), and usually presents quite a few blemishes)

**2- Bad detail**

Skin detail does not come from diffuse! That's quite obvious as we said that diffuse lighting is mostly due to subsurface scattering.

![]() |

Detail is all in the specular layer, ideally, you would need two different normalmaps for diffuse and specular (actually, Debevec achieves good results rendering with different normals for each of the RGB channels of the diffuse), fetching the same at different miplevels (bias) is often good enough and in a pinch, even just using the geometric normals for diffuse (or a lerp between the normalmap normal and the geometric ones) is way better than using the specular normals.

Skin pores are a really, really fine detail which is both difficult to capture and easy to get in the way of your BRDF. Most of the times, it's better to have the pore details as self-occlusion in the specular map than in the normalmaps (which being a derived measure will require higher resolution to capture the same amount of detail).

Also, you either have to model skin for a given viewing distance, or you'd better consider that at all but the closest distances the pores will/should fade in your miplevels and their scattering effect should be modeled by varying the specular exponent (broadening it with the distance, you can use ddx and ddy to estimate the filtering width, our use cLEAN), there is no way to tune the specular with a constant exponent that will yield both the right amount of detail up-close and the broad sheen you see from a distance.

Also, you either have to model skin for a given viewing distance, or you'd better consider that at all but the closest distances the pores will/should fade in your miplevels and their scattering effect should be modeled by varying the specular exponent (broadening it with the distance, you can use ddx and ddy to estimate the filtering width, our use cLEAN), there is no way to tune the specular with a constant exponent that will yield both the right amount of detail up-close and the broad sheen you see from a distance.

Peach fuzz on dry skin is another geometrical source of specular detail perturbation, you might want to model it by adding noise at the grazing angles if you need that amount of detail.

**3- Bad volume**

![]() |

When it works is one of the few games that captures volume right...

Skin texture luminosity is often quite uniform, and in caucasians quite light too, making skin shading more a matter of volume and shape than texture. Three elements here are important: specular, ambient and normals.



Normals are tricky because skin is often... skinned. Conventional bone skinning yields bad geometric normals. I've already



Normals are tricky because skin is often... skinned. Conventional bone skinning yields bad geometric normals. I've already

[blogged about that](http://c0de517e.blogspot.com/2011/05/skinning-normals-notes.html)so I won't repeat myself here.
Ambient is "easy" but really important, a simple contant won't do the job, it just flattens everything, even a simple hemispherical (top/bottom, a lerp between two colors based on the geometric normal y component, boils down to a single madd) is way better.

Observe and understand. Look at your references, understand what's important, understand your visual errors and their sources. The "correct hack" really depends on the context, if your environment is quite fixed, like in a sport or racing game you can model ambient with different components: a sky layer which does not depend on the position plus a ground reflection that maybe fades on the model based on the distance to the ground and so on...



Shadows, AO, Ambient model... All coming together nicely


Ambient occlusion is fundamental, ideally you'd want to have some directionality in the occlusion: bent normals, or encoding the occlusion in some base. Really "occlusion" is fundamental for volume. Each light component (ambient, diffuse, specular etc) should be occluded in a reasonable way.

Again, there are many ways, technically to achieve that, I won't delve into any detail because it depends on the context, you might want to agument SSAO to encode directional information (as I already said), or precompute occlusion at the vertices (SH or similar), cast rays in screenspace (i.e. screenspace reflection occlusion is easy, especially at the all-important fresnel angles, for rim occlusion) or even simpler hacks.

The important message here is that volume requires occlusion, look at your rendering and understand your visual defects, look for light leaks, compare with real-world references and acquired data and craft your own solution!

Sometimes the actual technical answer is dead simple (an example - one of the improvements on Champion over Round 4 was a "downgrade", we went from VSM to simple PCF filtering because VSM even if on average are "nicer" were not able to capture the very important occlusions on the face due to precision issues, the nose shadows and the eye-sockets. Going back to PCF gave us "worse" shadows but way better faces!)



Phong, modified to behave better with Schlick. No lousy round highlights!


Observe and understand. Look at your references, understand what's important, understand your visual errors and their sources. The "correct hack" really depends on the context, if your environment is quite fixed, like in a sport or racing game you can model ambient with different components: a sky layer which does not depend on the position plus a ground reflection that maybe fades on the model based on the distance to the ground and so on...

![]() |

Again, there are many ways, technically to achieve that, I won't delve into any detail because it depends on the context, you might want to agument SSAO to encode directional information (as I already said), or precompute occlusion at the vertices (SH or similar), cast rays in screenspace (i.e. screenspace reflection occlusion is easy, especially at the all-important fresnel angles, for rim occlusion) or even simpler hacks.

The important message here is that volume requires occlusion, look at your rendering and understand your visual defects, look for light leaks, compare with real-world references and acquired data and craft your own solution!

Sometimes the actual technical answer is dead simple (an example - one of the improvements on Champion over Round 4 was a "downgrade", we went from VSM to simple PCF filtering because VSM even if on average are "nicer" were not able to capture the very important occlusions on the face due to precision issues, the nose shadows and the eye-sockets. Going back to PCF gave us "worse" shadows but way better faces!)

![]() |

Achieving proper specular on skin is probably one of the trickiest parts as unfortunately, right now in realtime rendering we have either the choice of employing nice material models on simple analytic lights. It's well-known that the

[Kelemen/Szirmay-Kalos model fits the skin](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch14.html)acquired data very well and if you can afford it it's probably the way to go, especially if you lighting is not very complex (i.e. outdoor, harshly lit scenes).
Unfortunately, in many contexts we want to use some image-based lighting approach (baking reflection cubemaps), and that restricts the BRDF filtering we can employ pretty much to Phong, and straight Phong is really, really bad on skin.

Again, it's important here to observe and understand what is important, what qualities we want to model or hack. The specular sheen, other than affecting the saturation and the skin detail, as we discussed already, is important for the



[perception of the shape](http://www.google.ca/search?q=shape+perception+and+specular). Human vision can't really distinguish the effects of the various lights in the specular, we can't relate well the scene lighting with the specular hightlights shapes.
What we do with the specular is to understand the surface shape and material, so what's important is more to model the general shape of the specular, than the link between the specular and the actual scene lights.

That's why we can often ignore accurate specular occlusion (and just modulate all the specular light with our single shadowmap and omnidirectional ambient occlusion... or even "worse" multiply some of the diffuse product into phong, not ideal, but decent) and we can often disregard accurate light positions and use reflection cubemaps. And that's why what's really important is the shape of the specular sheen, and you get quite some latitude in hacking that in, as we can't really "see" these hacks as long as the final shape behaves "well".

What phong get really wrong is the highlight shape, which is too uniformly circular, and the lack of frensel. You can "break" the highlights using an exponent map (which should always be present, but it's especially important with Phong), adding fresnel is not easy as Phong simply does not reflect enough light at the grazing angles, and thus even multiplying with a decent approximation, like Schlick's, does not usually yield great results, it's better to use fresnel to (also) drive other parameters in the Phong model instead, either bending the reflection normal, or lowering the exponent.




I probably should have included a fourth horror "bad behavior", as most CG humans (all? in videogames) really lack the proper "fleshiness" in terms of animation and behaviour, but that's a harder problem to tackle which is probably outside the realm of realtime animation, at least for most games where you have many characters on screen and you can't afford having 300 bones in each plus some soft-body system and some UV relaxation and so on...


Really what I wanted to point out are some



Then the actual techniques really depend on your project, for those of you that really want to delve into some actual tech, an example of a possible solution for skin rendering is



Hair is a huge pain, on this generation we're stuck with hair cards. Cards don't sort well, are hard to shadow and hard to shade. My usual suggestion is to avoid spending too much time on it, it's not really worth it.

Shading usually employs Kajiya-Kay for specular (card will require a tangent shifting map to avoid having uniform highlights on a card, which are ok only for very straight hair), some wrap lighting for diffuse and a way of getting good rim.

For sorting, the usual solution is to go multipass, first doing alpha testing with z-writes, and then alpha blending with z-testing. You can somewhat pre-sort the triangles from in to out, some games do the alpha blending pass in two phases, first the backface cards then the frontfacing ones. It's decent, but defects will still be there, even sorting per triangle, if you can, doesn't solve them all as cards often intersect. I honestly think a better solution is to just alpha test and rely on alpha to coverage, if you can. This is what Fight Night Champion did by the way (Round 4 did a three-pass alpha blending).


Eyes are way, way more important. Shading is not that hard, specular/reflection is done with a cubemap usually, diffuse would need SSS but again some wrap is good, on Fight Night we computed a second set of normals to match the diffuse lighting with the skin around the eyes, probably a bit overkill. Behavior is hard, and getting it right is crucial! On the shading side, one trick I used is to disable the mipmaps, and the bilinear filtering on the reflection cube, to get aliasing far away that in turns create some shimmering in the small highlights. But most of it is in the animation, and some procedural techniques are to be employed.

Ears have lots of translucency, again, it can be faked easily, I won't lose my sleep there. For teeth, the important thing is to use the right occlusion and avoid them to become too bright, shadows from the mouth and lips onto the teeth are very hard to cast so again, you'll have to do some faking.

Bottom line, for each of these elements there are some easy hacks, but it's important to consider them. Once you understand what each of them needs and what physical things are important to model for each (ear: translucency, eyes: SSS and behavior, teeth: occlusion etc...), the actual techniques are "easy" or can be easily faked to a decent standard.

**Conclusions**I probably should have included a fourth horror "bad behavior", as most CG humans (all? in videogames) really lack the proper "fleshiness" in terms of animation and behaviour, but that's a harder problem to tackle which is probably outside the realm of realtime animation, at least for most games where you have many characters on screen and you can't afford having 300 bones in each plus some soft-body system and some UV relaxation and so on...

Really what I wanted to point out are some

**simple**things that**every game**should do, aspects which can most of the times be fixed to a decent degree with really cheap hacks, but do require an understanding of how the underlying physics work and how our perception works to then focus on what really matters visually.Then the actual techniques really depend on your project, for those of you that really want to delve into some actual tech, an example of a possible solution for skin rendering is

[here](http://c0de517e.blogspot.com/2011/09/fight-night-champion-gdc.html).**Addendum: Hair, Eyes, Teeth, Ears**Hair is a huge pain, on this generation we're stuck with hair cards. Cards don't sort well, are hard to shadow and hard to shade. My usual suggestion is to avoid spending too much time on it, it's not really worth it.

Shading usually employs Kajiya-Kay for specular (card will require a tangent shifting map to avoid having uniform highlights on a card, which are ok only for very straight hair), some wrap lighting for diffuse and a way of getting good rim.

For sorting, the usual solution is to go multipass, first doing alpha testing with z-writes, and then alpha blending with z-testing. You can somewhat pre-sort the triangles from in to out, some games do the alpha blending pass in two phases, first the backface cards then the frontfacing ones. It's decent, but defects will still be there, even sorting per triangle, if you can, doesn't solve them all as cards often intersect. I honestly think a better solution is to just alpha test and rely on alpha to coverage, if you can. This is what Fight Night Champion did by the way (Round 4 did a three-pass alpha blending).

Eyes are way, way more important. Shading is not that hard, specular/reflection is done with a cubemap usually, diffuse would need SSS but again some wrap is good, on Fight Night we computed a second set of normals to match the diffuse lighting with the skin around the eyes, probably a bit overkill. Behavior is hard, and getting it right is crucial! On the shading side, one trick I used is to disable the mipmaps, and the bilinear filtering on the reflection cube, to get aliasing far away that in turns create some shimmering in the small highlights. But most of it is in the animation, and some procedural techniques are to be employed.

Ears have lots of translucency, again, it can be faked easily, I won't lose my sleep there. For teeth, the important thing is to use the right occlusion and avoid them to become too bright, shadows from the mouth and lips onto the teeth are very hard to cast so again, you'll have to do some faking.

Bottom line, for each of these elements there are some easy hacks, but it's important to consider them. Once you understand what each of them needs and what physical things are important to model for each (ear: translucency, eyes: SSS and behavior, teeth: occlusion etc...), the actual techniques are "easy" or can be easily faked to a decent standard.

## 9 comments:

Excellent post. I would only add that using *linear color* (and not sRGB!) in your shading code is of vital importance to subtleties like skin rendering. Most professional titles don't make this mistake, but a lot of newer developers do. A great treatment with example shots is here: http://http.developer.nvidia.com/GPUGems3/gpugems3_ch24.html

I'v only recently started reading up on gamma (I'm a graphics amateur after all) and I can't really wrap my head around how the problem came to be in the first place. I think I understand the need for the linear space, but the entire problem seems caused by an unfortunate convention to pre-adjust images rather than actually do the rendering correctly in the first place. Would that view be correct or too simple or plain wrong?

Historically it came to be I believe due to the response curve of monitors but I'm not 100% sure. It is a good thing though as it makes a better usage of whatever bit precision you have to encode colours, non-linear spaces are not good for math but they do behave better perceptually. If you try to encode an image in linear space with 8bpp you'll end up with a lot of banding in the darks.

P.s. that's whynin the photoshop cleartype script I posted for example, i go linear after switching to 16bpp, doing it on 8bpp would be very bad...

...I just realized that :)


I'd better go recode that demo to 16bpp or 32bpp, thanks!

That the origin of the gamma curve was a "mistake" is a common misconception. Yes, monitors do have this response curve (both old CRTs and new LCDs), but this was an intentional design goal. The hardware engineers could have just as easily made monitors with a linear response.



The reason for it is precision. If you display an 8-bit gradient with linear response, more banding is evident than if a gamma curve is present. It moves more values into the "darks", where a human eye is more likely to notice. The term used for this is "gamma compression".

This was considered a good thing to add to display hardware since something like 10 or 12 bits (or maybe more) would otherwise be needed in the processing to reach the same apparent quality.

You are totally right about "bad behavior" and lack of fleshiness being another problem. Proper animation technology seems to be lagging far behind graphics these days. And without it we still only achieve beautifully rendered wax puppets.



I like what they're doing with simulated tendons and wrinkly-face technology in this video: http://vimeo.com/23593380

Wrinkles and muscle strain could be stored in a set of animated normalmaps, to be blended in or out based on some animation meta-data, stored in addition to bone transforms in a skeleton, for example.

Monkey: ye, wrinkle maps are actually quite easy and very common, fight night uses them since round 3 I think. The truth is that not only most games can't skin so many bones (Champion I think uses around three hundreds per boxer) but that authoring of facial animation is extremely hard even with offline techniques (you still see movies today doing a really bad job at that, for example the latest Tron) and physical simulators are useful to reduce the complexity, but are still hard to understand/control. It requires a lot of skill...

@jeffdr: It took me a while to get back to this thread, but thanks for the info. I'm still wondering about some things, but I'll resist the temptation of rambling on and on about gamma and just figure those out myself.


@DEADC0DE: Sorry about rambling on and on about gamma, especially since it was rather offtopic here :)

Post a Comment