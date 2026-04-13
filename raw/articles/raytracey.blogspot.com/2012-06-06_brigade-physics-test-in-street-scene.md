---
title: Brigade physics test in street scene
url: http://raytracey.blogspot.com/2012/06/brigade-physics-test-in-street-scene.html
author: Sam Lapere
published: '2012-06-06'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

^^ Yes , and when they walk into one another , they hit one another and either both fly off spiraling into walls etc, or whatever else you can think of Sam!

Sam, you must check out (possibly forward) this Siggraph 2012 submission on "Adaptive Manifolds" for denoising in linear time: http://inf.ufrgs.br/~eslgastal/AdaptiveManifolds/ VIDEO: http://www.youtube.com/watch?v=h7DCdgU93To&feature=player_embedded

Bonus, they also use a path-traced image as an example! The results are simply incredible! Something like this implemented in Brigade would result in no-noise interactivity over night.

Reaven, the current acceleration structure in Brigade doesn't allow many detailed characters/dynamic objects at the same time. We're looking into a novel acc str which should make this possible though.

Sean, that's awesome! Thanks very much for finding this. The best thing about this filter is that it's real-time and can be used for denoising path traced image.

Exactly! I was so excited to pass it on when I found it. It's a game changer for path tracers, and certainly for other media types as well, not only as a real-time de-noiser, but also an edge-aware enhancer. It could lead to all sorts of interesting effects. :)

It's amazing to think that photo-real graphics (including noiseless movement) are literally right around the corner!

I don't you about you guys but it seems to me that "Adaptive Manifolds for Real-Time High-Dimensional Filtering" is highly destructive in certain scenarios, look at the clouds, and look at the peek of the roof in the lighthouse photo.

This technique tries to interpret blurry areas as either motion blur or depth of field , so it can't handle water, or clouds, obviously glossy reflections won't work either. But if that can be disabled or minimized then it could work.

Glossy reflections should actually benefit from the slight blurring. Either way, I think the blurred result might still look better than noise, if you look at the bust.

The authors will also release the source code soon, so it's definitely worth trying this out.

Yes I agree that the center of a glossy reflective surface would benefit, but I presume here that if it destroyed parts of the peak of the roof that meet the sky in the lighthouse image, I assume it will do the same around the edges or perimeter of a glossy object or glass. But we shall see.

you can set a user defined threshold for the edge-preserving parameter. Ideally you should be able to define masks for the skytexture so that it remains crispy.

btw, Lehtinen et al. are also presenting a paper on Siggraph about noise reduction in what appears to be Monte Carlo GI (Reconstructing the Indirect Light Field for Global Illumination) which should also be quite interesting.

You should also be able to decreasingly composite the de-noised image result with the increasingly converged path-traced image. Alternatively, you can replace dark yet-to-be converged path-traced pixels with pixels from the de-noised image. etc.

I'm sure there are many ways to exploit this technique without using it in an all-or-nothing way.

AO you say? So this scene is rendered with direct + AO, which means it's not unbiased anymore, or does not even have indirect light :( But at least it's really fast :)

Have a look at the AO preset mode in Octane Render which renders direct light + AO with variable dist + 1 bounce of indirect light. It converges extremely fast, there's almost no noise and looks almost indistinguishable from full-blown path tracing ;-)

True, but precomputed AO will look incorrect when it's directly lit and real-time raytraced AO on dynamic objects looks tons better than SSAO or SSDO, and it's not limited to screen space, so it will always look correct. You can also scale the quality of raytraced AO by simply changing the AO ray length. The first bounce GI approximation in games is in many cases a very rough approximation (like LPV) and limited to mostly diffuse materials. In Brigade you can have materials on the whole spectrum from perfectly diffuse over glossy to perfectly specular (+ all combinations of these). The raytraced AO with first bounce color bleeding will make the image complete, with no precomputation needed at all.

Amazing work Sam! I'm starting to believe you can get a noise free image and have it render at 30-60 fps. Obviously there is still some noise in the video but its TONS better than before, you guys just need to push it abit further :)

If you like to do that you can disable precomputed AO in lit areas computationally really cheap in screen space. SSDO is in a way even superior to rt-AO in that it kinda considers the first light bounce (there will be artifacts but less than with SSAO). The LPV approach can be extended to glossy bounces, and even puddles and similar things can be rendered plausibly by Cryengine 3 in a screen space raytracing approach. I really don't think it's a good idea to do AO + first bounce if you can do full blown PT. Because most of the noise comes from the first bounce anyway. I don't think that this (sometimes pretty crude) approximation is justifiable when shooting for photorealism even if you get a major speed bump.

I'd like to add that I consider this mode a really nice addition to the engine, but I'd be really sad if you abandoned realtime pathtracing in favour of this approximation :(

>>If you like to do that you can disable precomputed AO in lit areas computationally really cheap in screen space. SSDO is in a way even superior to rt-AO in that it kinda considers the first light bounce (there will be artifacts but less than with SSAO).

The first bounce in SSDO is only from very nearby surfaces and is dependent on screen space, rt AO + real first bounce (path traced) is vastly superior to that.

>> The LPV approach can be extended to glossy bounces, and even puddles and similar things can be rendered plausibly by Cryengine 3 in a screen space raytracing approach. I really don't think it's a good idea to do AO + first bounce if you can do full blown PT. Because most of the noise comes from the first bounce anyway. I don't think that this (sometimes pretty crude) approximation is justifiable when shooting for photorealism even if you get a major speed bump.

Try out the AO preset mode in Octane Render which also does one-bounce GI, you will be blown away by the speed, photorealistic image quality and quasi absence of noise. It's entirely justifiable.

>> I'd like to add that I consider this mode a really nice addition to the engine, but I'd be really sad if you abandoned realtime pathtracing in favour of this approximation :(

Filtering techniques like the Adaptive Manifold one mentioned by Sean (and lots of other stuff) will enable us to use real-time path tracing again at some point in the future, in the meantime it'll be something between AO and path tracing.

btw, about screen space reflections: once you can do real raytraced reflections (glossy and specular), which are pretty cheap btw, there's absolutely no point going back to screen space stuff. Moreover, screen space reflections only work for windows and puddles seen from grazing angles, if you're standing right in front of a window or mirror, the reflection will be empty.

Whether it's unbiased or biased is not important, whats more important is is pleasing to the eye and does it run at a decent frame yet? This video looks much better than any engine on the market today, I'd love to see a 720P version.

Also Sam check this Luminous engine tech demo:

http://www.youtube.com/watch?v=HdGxUyGc1tg

It's rasterization but it still pleasing to the eye(which imho is important)

Is the new kernel still superior to Luminous engine, given it had the high quality content to show off?

Yeah, the Luminous demo was the best looking demo at E3 this year, it really had this next gen vibe to it. I've been following the research of Shinji Ogaki (one of the Luminous developers who used to work at Square but not anymore, also authored "Real-time bidirectional path tracing via rasterization") and it looks like Luminous is using very high quality precomputed lightmaps (see http://raytracey.blogspot.be/2011/12/real-time-bidirectional-path-tracing.html). A lot of the magic in the Luminous graphics comes from post processing FX as well and the crapload of particles. All in all, they did a truly amazing job with the graphics. Still, if you look closely, most materials are diffuse and reflections are in screen space. So to answer your question, given the same scene I think the new kernel in Brigade should be able to deliver higher quality for dynamically changing lighting and for materials (especially specular) once first bounce GI is included. Particles and all the dynamic stuff are still a bit problematic, but eventually we're going to solve that as well ;)

The Luminous stuff is amazing, and produces very realistic graphics.

What Brigade brings should not be (just) expressed in image quality though: Brigade is a simple engine, developed by a small team, and the art being used here is simply downloaded from the internet. Luminous is a massive undertaking, and the art is (no doubt) produced by an enormous team, specifically for this engine.

Brigade makes things look good with far less effort, and far less stacked algorithms. It's a 'realism' thing, but also a 'productivity' thing.

Nothing is stopping OTOY from hiring many 3D artist to create a realtime cutscene using Brigade ;) No doubt Brigade has a bright future, I can't wait to see where you guys take the engine, though it will still require alot of work to create a very user friendly game engine(i.e. Unreal Engine 4):

What do you think about Isotropix' Clarisse? http://www.isotropix.com/clarisse_ifx_tech_specs.html It is some CPU-based editor+renderer. They claim billions of polygons (which come from instancing the stones and grass blades using procedurals and matrices) and interactive shading, which uses a lot of approximations - but it is very nice at the same time

btw, I spotted a weird rendering bug in the developer walkthrough video you linked to at 00:57. The gold statue has a glossy reflection in the floor, but there's no reflection of the dynamic ball. The reflection in the silver statue doesn't have self occlusion etc., Surely Brigade can do better than that ;)

>> Try out the AO preset mode in Octane Render which also does one-bounce GI, you will be blown away by the speed, photorealistic image quality and quasi absence of noise. It's entirely justifiable.

I don't have Octane but I know what to expect from my experiences with my own raytracer. It's not justifiable because the majority of the noise comes from the first bounce, further noise gets strongly attenuated due to the nature of light transport. By combining AO + first-bounce-pathtracing you gain perhaps 50% in speed but you sacrifice the entire realism. It's already visible in the demo you posted, even when considering it is the best-case scenario, because lighting from a skydome is very close to AO. I know that the logic of capitalism drives you towards a marketable product as soon as possible. But then you have to go with AO only and not AO + first bounce pathtracing, because that makes absolutely no sense.

Well I have been running some tests on Brigade and I am impressed.

In 32 bit I was able to load 60*50*50 textured cubes for a total of 5.5 million verts, and 1.8 million faces at 11 fps on 1 gtx 580.

In 64 bit I have not even gone to the limit, I got as far as 80*80*80 cubes for a total of 18.4 million verts, and 6.1 million faces, at 2.2 fps on 1 gtx 580.

now all the textures were the same, 1 diffuse map, still this is quite impressive.

Hi! I have just tried out this Adaptive Manifold Filter and it's awesome! You can avoid texture blurring if you supply texture information to the filter. But it works poorly with glass material. It might be better with more info like secondary bounce colors or something.

## 40 comments:

You have really gone a long way in reducing the noise.. but need a better quality video to see the finer details.

The credits go to Jeroen van Schijndel for that.


In high res, the framerate is slower, but the noise reduction works even better and the image looks much more real :)

I think the next step in these city demos is to populate them with a crowd of walking pedestrians.

^^ Yes , and when they walk into one another , they hit one another and either both fly off spiraling into walls etc, or whatever else you can think of Sam!

Sam, you must check out (possibly forward) this Siggraph 2012 submission on "Adaptive Manifolds" for denoising in linear time:



http://inf.ufrgs.br/~eslgastal/AdaptiveManifolds/

VIDEO: http://www.youtube.com/watch?v=h7DCdgU93To&feature=player_embedded

Bonus, they also use a path-traced image as an example! The results are simply incredible! Something like this implemented in Brigade would result in no-noise interactivity over night.

Oh, and the progress is looking amazing!

Reaven, the current acceleration structure in Brigade doesn't allow many detailed characters/dynamic objects at the same time. We're looking into a novel acc str which should make this possible though.

Sean, that's awesome! Thanks very much for finding this. The best thing about this filter is that it's real-time and can be used for denoising path traced image.

Exactly! I was so excited to pass it on when I found it. It's a game changer for path tracers, and certainly for other media types as well, not only as a real-time de-noiser, but also an edge-aware enhancer. It could lead to all sorts of interesting effects. :)


It's amazing to think that photo-real graphics (including noiseless movement) are literally right around the corner!

Nice to know someone else is as excited about this stuff as I am :)

Possibly more! I'm so excited that I'm finding it difficult to work! :)

I don't you about you guys but it seems to me that "Adaptive Manifolds for Real-Time High-Dimensional Filtering" is highly destructive in certain scenarios, look at the clouds, and look at the peek of the roof in the lighthouse photo.


This technique tries to interpret blurry areas as either motion blur or depth of field , so it can't handle water, or clouds, obviously glossy reflections won't work either. But if that can be disabled or minimized then it could work.

Glossy reflections should actually benefit from the slight blurring. Either way, I think the blurred result might still look better than noise, if you look at the bust.


The authors will also release the source code soon, so it's definitely worth trying this out.

Yes I agree that the center of a glossy reflective surface would benefit, but I presume here that if it destroyed parts of the peak of the roof that meet the sky in the lighthouse image, I assume it will do the same around the edges or perimeter of a glossy object or glass. But we shall see.

you can set a user defined threshold for the edge-preserving parameter. Ideally you should be able to define masks for the skytexture so that it remains crispy.


btw, Lehtinen et al. are also presenting a paper on Siggraph about noise reduction in what appears to be Monte Carlo GI (Reconstructing the Indirect Light Field for Global Illumination) which should also be quite interesting.

You should also be able to decreasingly composite the de-noised image result with the increasingly converged path-traced image. Alternatively, you can replace dark yet-to-be converged path-traced pixels with pixels from the de-noised image. etc.


I'm sure there are many ways to exploit this technique without using it in an all-or-nothing way.

Right Sean I agree with your last sentence.


This technique uses multiple images also, so I guess it shouldn't be a problem.

AO you say? So this scene is rendered with direct + AO, which means it's not unbiased anymore, or does not even have indirect light :( But at least it's really fast :)

Have a look at the AO preset mode in Octane Render which renders direct light + AO with variable dist + 1 bounce of indirect light. It converges extremely fast, there's almost no noise and looks almost indistinguishable from full-blown path tracing ;-)

The thing is that there are already games on the market that feature precomputed AO/SSAO/SSDO and some kind of first bounce approximation.

True, but precomputed AO will look incorrect when it's directly lit and real-time raytraced AO on dynamic objects looks tons better than SSAO or SSDO, and it's not limited to screen space, so it will always look correct. You can also scale the quality of raytraced AO by simply changing the AO ray length. The first bounce GI approximation in games is in many cases a very rough approximation (like LPV) and limited to mostly diffuse materials. In Brigade you can have materials on the whole spectrum from perfectly diffuse over glossy to perfectly specular (+ all combinations of these). The raytraced AO with first bounce color bleeding will make the image complete, with no precomputation needed at all.

Amazing work Sam! I'm starting to believe you can get a noise free image and have it render at 30-60 fps. Obviously there is still some noise in the video but its TONS better than before, you guys just need to push it abit further :)

If you like to do that you can disable precomputed AO in lit areas computationally really cheap in screen space. SSDO is in a way even superior to rt-AO in that it kinda considers the first light bounce (there will be artifacts but less than with SSAO).

The LPV approach can be extended to glossy bounces, and even puddles and similar things can be rendered plausibly by Cryengine 3 in a screen space raytracing approach.

I really don't think it's a good idea to do AO + first bounce if you can do full blown PT. Because most of the noise comes from the first bounce anyway. I don't think that this (sometimes pretty crude) approximation is justifiable when shooting for photorealism even if you get a major speed bump.

I'd like to add that I consider this mode a really nice addition to the engine, but I'd be really sad if you abandoned realtime pathtracing in favour of this approximation :(

The adaptive manifolds stuff could be very interesting in case of non-realistic scenes with path tracers. Like cartoonish or minimalism.

Anonymous:






>>If you like to do that you can disable precomputed AO in lit areas computationally really cheap in screen space. SSDO is in a way even superior to rt-AO in that it kinda considers the first light bounce (there will be artifacts but less than with SSAO).

The first bounce in SSDO is only from very nearby surfaces and is dependent on screen space, rt AO + real first bounce (path traced) is vastly superior to that.

>> The LPV approach can be extended to glossy bounces, and even puddles and similar things can be rendered plausibly by Cryengine 3 in a screen space raytracing approach.

I really don't think it's a good idea to do AO + first bounce if you can do full blown PT. Because most of the noise comes from the first bounce anyway. I don't think that this (sometimes pretty crude) approximation is justifiable when shooting for photorealism even if you get a major speed bump.

Try out the AO preset mode in Octane Render which also does one-bounce GI, you will be blown away by the speed, photorealistic image quality and quasi absence of noise. It's entirely justifiable.

Anonymous:





>> I'd like to add that I consider this mode a really nice addition to the engine, but I'd be really sad if you abandoned realtime pathtracing in favour of this approximation :(

Filtering techniques like the Adaptive Manifold one mentioned by Sean (and lots of other stuff) will enable us to use real-time path tracing again at some point in the future, in the meantime it'll be something between AO and path tracing.

btw, about screen space reflections: once you can do real raytraced reflections (glossy and specular), which are pretty cheap btw, there's absolutely no point going back to screen space stuff. Moreover, screen space reflections only work for windows and puddles seen from grazing angles, if you're standing right in front of a window or mirror, the reflection will be empty.

Whether it's unbiased or biased is not important, whats more important is is pleasing to the eye and does it run at a decent frame yet? This video looks much better than any engine on the market today, I'd love to see a 720P version.





Also Sam check this Luminous engine tech demo:

http://www.youtube.com/watch?v=HdGxUyGc1tg

It's rasterization but it still pleasing to the eye(which imho is important)

Is the new kernel still superior to Luminous engine, given it had the high quality content to show off?

Yeah, the Luminous demo was the best looking demo at E3 this year, it really had this next gen vibe to it. I've been following the research of Shinji Ogaki (one of the Luminous developers who used to work at Square but not anymore, also authored "Real-time bidirectional path tracing via rasterization") and it looks like Luminous is using very high quality precomputed lightmaps (see http://raytracey.blogspot.be/2011/12/real-time-bidirectional-path-tracing.html). A lot of the magic in the Luminous graphics comes from post processing FX as well and the crapload of particles. All in all, they did a truly amazing job with the graphics. Still, if you look closely, most materials are diffuse and reflections are in screen space. So to answer your question, given the same scene I think the new kernel in Brigade should be able to deliver higher quality for dynamically changing lighting and for materials (especially specular) once first bounce GI is included. Particles and all the dynamic stuff are still a bit problematic, but eventually we're going to solve that as well ;)

The Luminous stuff is amazing, and produces very realistic graphics.




What Brigade brings should not be (just) expressed in image quality though: Brigade is a simple engine, developed by a small team, and the art being used here is simply downloaded from the internet. Luminous is a massive undertaking, and the art is (no doubt) produced by an enormous team, specifically for this engine.

Brigade makes things look good with far less effort, and far less stacked algorithms. It's a 'realism' thing, but also a 'productivity' thing.

- Jacco.

@ Jacco



Nothing is stopping OTOY from hiring many 3D artist to create a realtime cutscene using Brigade ;) No doubt Brigade has a bright future, I can't wait to see where you guys take the engine, though it will still require alot of work to create a very user friendly game engine(i.e. Unreal Engine 4):

http://www.youtube.com/watch?v=MOvfn1p92_8

What do you think about Isotropix' Clarisse? http://www.isotropix.com/clarisse_ifx_tech_specs.html

It is some CPU-based editor+renderer. They claim billions of polygons (which come from instancing the stones and grass blades using procedurals and matrices) and interactive shading, which uses a lot of approximations - but it is very nice at the same time

Now we're on the topic of UE4 :)


btw, I spotted a weird rendering bug in the developer walkthrough video you linked to at 00:57. The gold statue has a glossy reflection in the floor, but there's no reflection of the dynamic ball. The reflection in the silver statue doesn't have self occlusion etc., Surely Brigade can do better than that ;)

Isotropix Clarisse is awesome, the workflow demo video just floored me. I wish it would only render faster.

>> Try out the AO preset mode in Octane Render which also does one-bounce GI, you will be blown away by the speed, photorealistic image quality and quasi absence of noise. It's entirely justifiable.


I don't have Octane but I know what to expect from my experiences with my own raytracer. It's not justifiable because the majority of the noise comes from the first bounce, further noise gets strongly attenuated due to the nature of light transport. By combining AO + first-bounce-pathtracing you gain perhaps 50% in speed but you sacrifice the entire realism. It's already visible in the demo you posted, even when considering it is the best-case scenario, because lighting from a skydome is very close to AO.

I know that the logic of capitalism drives you towards a marketable product as soon as possible. But then you have to go with AO only and not AO + first bounce pathtracing, because that makes absolutely no sense.

You definitely haven't tried the AO kernel in Octane then (which also does 1 bounce of GI). Download the free demo if you have an Nvidia card.

Well I have been running some tests on Brigade and I am impressed.




In 32 bit I was able to load 60*50*50 textured cubes for a total of 5.5 million verts, and 1.8 million faces at 11 fps on 1 gtx 580.

In 64 bit I have not even gone to the limit, I got as far as 80*80*80 cubes for a total of 18.4 million verts, and 6.1 million faces, at 2.2 fps on 1 gtx 580.

now all the textures were the same, 1 diffuse map, still this is quite impressive.

Interesting, thanks! I haven't tested the geometrical limits of Brigade like that.


But aren't those cubes getting boring after a while? You should try some spheres next time ;)

potato potahto, tomato tomahto it's all the same ;)

Hi! I have just tried out this Adaptive Manifold Filter and it's awesome! You can avoid texture blurring if you supply texture information to the filter. But it works poorly with glass material. It might be better with more info like secondary bounce colors or something.

Post a Comment