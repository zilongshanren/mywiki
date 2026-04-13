---
title: Compare it!
url: https://bartwronski.com/2014/02/05/compare-it/
published: '2014-02-05'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## Cpt. Obvious

I have some mixed feelings about the blog post I’m about to write. On the one hand, it is something obvious and rudimentary in graphics workflows, lots of graphics blogs use such techniques, but on the other hand, I’ve seen tons of blog posts, programmer discussions and even scientific papers that seem to totally not care about it. So I still *feel* that it is quite important topic and will throw some ideas, so let’s get to it.

## Importance of having *some* reference

Imagine that you are working on some topic (new feature? major optimization that can sacrifice “a bit” of quality? new pipeline?) for couple days. You got some *promising* results, AD seems to like it, just some small changes and you will submit it. You watch your results on a daily basis (well, you see them all the time), but then you call another artist or programmer to help you evaluate the result and you start discussing/arguing/wondering, “should it really look like this”?

Well, that’s a perfect question. Is the image too bright? Or maybe your indirect light bounce is not strong enough? Is your area lights approximation plausible and energy conserving? What about the maths – did I forget the (infamous) divide by PI? Was my monitor de-calibrated by my cat, or maybe did art director look earlier from a different angle? 🙂

Honestly I always lost track of what looks ok and what doesn’t after just couple iterations – and checked back with a piece of concept art, AD feedback or photographs.

Answer to all of those questions is almost impossible to make just by looking at the image. It is also sometimes very difficult to make without complex and long analysis of code and maths. That’s why it is **essential** to have a reference / comparison version.

## NOT automatic testing

Just to clarify. I’m not talking about automatic testing. It is important topic, lots of companies use it and it makes perfect sense, but my blog post has nothing to do with it. It is relatively easier to keep away from breaking stuff that was already done right (or you accepted *some* version), but it is very difficult to get things “right” when you don’t know how the final result should look like.

## Reference version?

Ok, so what could be this reference version? I mean that you should have some implementation of a “brute-force” solution to the problem you are working on. Naive, without any approximations / optimizations, running in even seconds instead of your desired 16/33 millis.

For years, most of game 3d graphics people didn’t use any reference versions – and it has a perfect explanation. Games were so far away from CGI rendering that there was no point in comparing the results. Good game graphics were product of clever hacks, tricks and approximations and interesting art direction. Therefore, still lots of old school programmers and artists have a habit of only checking if something “looks ok” or hacking it until it does. While art direction will always be the most important part of amazing 3D visuals, since we discovered the power of physically based shading and started to use techniques like GI / AO / PBR / area lights etc. there is no turning back, some tricks must be replaced by terms that make physical / mathematical sense. Fortunately, we can compare them against ground truth.

I’m going to give just couple examples of applications of how it can be used and implemented for some selected topics.

## Area Lights

Actually, the topic of area lights is the one why I started to think about writing this blog post. We have seen multiple articles and presentations on that topic, some discussing energy conservation or looks of final light reflection shape – but how many have compared it against ground truth? And I’m not talking only about a comparison of incoming energy in Mathematica for some specific light / BRDF setup – it is important, but I believe that checking the results in real time in your game editor is way more useful.

Think about it – it is **trivial** to implement even 64 x 64 loop in your shader that integrates the light area by summing sub-lights – it will run in 10fps on your GTX Titan, but you will be able to immediately compare your approximations with ground truth. You will see the edge cases, where is diverges from expected results and will be able to truly evaluate this solution with your lighters.

You could even do it on the CPU side and have 64×64 grid of shadow casting lights and check the (soft)shadowing errors with those area lights how useful is that to check your PCSS soft-shadows?

## (Anti)aliasing

Very important one – as signal aliasing is one of the basic problems of real-time computer graphics. There are recently lots of talks about geometric aliasing, texture aliasing, shading aliasing (Toksvig, specular, or diffuse AA anyone?), problems with alpha tested geometry etc. Most of presentations and papers fortunately do present comparisons with a reference version, but have **you** compared it yourself in your engine? 🙂 Are you sure **you** got it right?

Maybe you have some MSAA bug, maybe your image-based AA works very poorly in motion or maybe your weights for temporal AA are all wrong? Maybe your specular / diffuse AA calculations are improper, or just the implementation has a typo in it? Maybe artist-authored vertex and pixel shaders are introducing some “procedural” aliasing? Maybe you have geometric normals shading aliasing (common techniques like Toksvig work only in normal-map space)? Maybe actually your shadow mapping algorithm is introducing some flickering / temporal instability?

There are tons of other potential problems with aliasing that comes from different sources (well… all the time we are trying to resample some data containing information way above Nyquist frequency), but we need to be sure if it is the source of our problem in given case.

Obviously, doing a proper, reference super-resolution image rendering and resampling it helps here. I would recommend two alternate solutions:

- True supersampling. This one is definitely the easiest to implement and closest to the ground truth, but usually the memory requirements make the cost prohibitive for higher supersampling factors, so this will be only small help…
- In-place supersampling. Oldschool technique that can be either image/tile-stitching based (Unreal Engine tiled screenshots) or sub pixel offset based (The Witcher 2 screenshots supersampled in place 256 times! 🙂 ).

I had good experiences with the second one (as it usually works well with blur-based post-effects like bloom), but to get it right don’t forget a small simple trick – apply a negative mip bias (~to log2 supersampling level in one axis) and a geometric LOD bias. This way your mip-mapping will work like if you had much higher screen resolution and you will potentially see some bugs that come from improper LODs. A fact that I find quite amusing – we implemented this for The Witcher 2 as graphic option for future players (we were really proud of graphics in the final game and thought that it would be awesome if your game looked as great in 10years, right? 🙂 ) – but most PC enthusiasts hated us for that! They are used to putting everything to max to test their $3-5k PC setups (and justify the expense), but this option “surprisingly” (even if there was a warning in the menu!) cut their performance for example 4x on the GPU. 😉

## Global Illumination

Probably the most controversial one – as very difficult and problematic to implement. I won’t cover here all the potential problems, but implementing reference GI could take weeks and rendering will take seconds / minutes to complete. Your materials could look different. CPU/GPU solutions require completely different implementations.

Still I think it is quite important, because I had endless discussions like “are we getting enough bounced lighting here?”, “this looks too bright / too dark” etc. and honestly – I was never sure of the answer…

This one could be easier for the ones who use Maya/other 3D software as their game editor, but probably will be problematic for all the other ones. Still you could consider doing it step by step – having a simple BVH/kd-Tree and raytracing based AO baker / estimator should be quite easy to write (max couple days), will help you to evaluate your SSAO and larger scale AO algorithms. In future you could extend it to multiple light bounce GI estimator. With PBR and next-gen gaming I think it will be the crucial factor at some point that could really speed-up both your R&D and the final production – as artists used to work in CGI/movies will get the same, *proper* results in the game engine.

## BRDF functions

A perfect example was given by Brian Karis on the last Physically Based Shading at Siggraph 2013 course on the topic of “environment BRDF”. By doing a brute force integration over whole hemisphere and BRDF response to the incoming irradiance from your env map, you can check how it is really supposed to look. I would recommend doing it without any importance sampling as a starting point – because you could also make a mistake or introduce some errors / bias doing so!

Having such reference version it is way easier to check your approximations – you will immediately see what are the edge cases and potential disadvantages of given approximation. Having such mode in your engine you will check if you pick proper mip maps or if you forgot to multiply/divide by some constant coefficient. You will see how much you are losing by ignoring the anisotropic lobe or by decoupling some integration terms. Just do it, it shouldn’t take you more than hours with all the proper testing!

## Implementation / usability

Just couple thoughts on how it should be implemented: I think there is quite a big problem of where you want to place your solution on the line where the two extremes are:

- Ease of implementation
- Ease of comparison

On one hand, if developing a reference version takes too much time, you are not going to do it. 🙂 The least usable solution is probably still better than **no** solution – if you will be scared (or not allowed to by your manager) of implementing a reference version because it takes too long to do so, you will not get any benefits.

On the other hand, if switching between versions takes too much time, you need to wait seconds to see some results or even have to manually recompile some shaders or compare versions in Photoshop, the benefits of having a reference version will be also diminished and there could be no point in using it.

Every case is different – probably a reference BRDF integrator will take minutes to write, but reference GI screenshots / live mode can take weeks to complete. Therefore I can only give you the advice to be reasonable about it. 🙂

One thing to think about is having some in-engine or in-editor support/framework that makes the use of referencing of various passes easier. Just look at photo applications like great Adobe Lightroom – you have both a “slider” for the split image modes as well as options to place compared images on different monitors.

There is also a “preview before” button always available. It could be useful for other topics – imagine how having such button for lighting / post-effects settings would make life easier for your lighting artist! One click to compare with what he had 10minutes ago – a great help for answering the classic “am I going in the right direction?” question. Having such tools as a part of your pipeline is probably not immediate thing to develop, you will need help of good tool programmers, but I think it may pay back quite quickly.

## Summary

Having a reference version will help you during development and optimization. Ground truth version is an objective reference point – unlike judgement of people that can be biased, subjective or depend on emotional / non-technical factors (see the list of cognitive biases in psychology! An amazing problem that you always need to take into account, not only working with other people, but also alone). Implementing a reference version can take various amount of time (from minutes to weeks) and probably sometimes it is too much work/difficulty to do, so you need to be reasonable about it (especially if you work in a production, non-academic environment), but just keeping it in mind could help you solve some problems or explain them to other people (artists, other programmers).

Pingback: https://bartwronski.com/2014/02/05/compare-it/ | Linked List

Pingback: Temporal supersampling and antialiasing | Bart Wronski