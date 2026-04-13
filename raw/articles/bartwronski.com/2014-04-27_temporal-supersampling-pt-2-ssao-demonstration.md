---
title: Temporal supersampling pt. 2 – SSAO demonstration
url: https://bartwronski.com/2014/04/27/temporal-supersampling-pt-2-ssao-demonstration/
published: '2014-04-27'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

This weekend I’ve been working on my [Digital Dragons 2014](http://www.digitaldragons.pl/en/) presentation (a great Polish game developers conference I was invited to – if you will be somewhere around central Europe early May be sure to check it out) and finally got to take some screenshots/movies of temporal supersampling in action on SSAO. I promised to take them quite a while ago in [my previous post about temporal techniques](https://bartwronski.com/2014/03/15/temporal-supersampling-and-antialiasing/) and almost forgot. 🙂

To be honest, I never really had time to “benchmark” properly its quality increase when developing for Assassin’s Creed 4 – it came very late in the production, actually for a title update/patch – in the same patch as increased PS4 resolution and our temporal anti-aliasing. I had motion vectors so I simply plugged it in, tweaked params a bit, double-checked the profilers, asked other programmers and artists to help me assess increase in quality (everybody was super happy with it) and review it, gave for full testing and later submitted.

Now I took my time to do proper before-after screenshots and the results are surprising ever for me.

Let’s have a look at comparison screenshots:


On a single image with contrast boosted (click it to see in higher res):

Quite decent improvement (if we take into account a negligible runtime cost), right? We see that ugly pattern / noise around foliage disappeared and undersampling behind the ladder became less visible.

But it’s nothing compared to to how it behaves in motion – be sure to watch it in fullscreen!

(if you see poor quality/compression on wordpress media, check out [direct link](https://bartwronski.com/wp-content/uploads/2014/04/ssao_temporal.mp4))

I think that in motion the difference is huge and orders of magnitude better! It fixes all the issues typical to the SSAO algorithms that happen because of undersampling. I will explain in a minute why it gets so much better in motion.

You can see on the video some artifacts (minor trailing / slow appearance of some information), but I don’t know if I would notice them not knowing what to look for (and with applied lighting, our SSAO was quite subtle – which is great and exactly how SSAO should look like – we had great technical art directors 🙂 ).

Let’s have a look what we have done to achieve it.


## Algorithm overview

Our SSAO was based on [Scalable Ambient Obscurance algorithm by McGuire et al. [1]](http://graphics.cs.williams.edu/papers/SAOHPG12/)

The algorithm itself has a very good console performance (around 1.6ms on consoles for full res AO + two passes of bilateral blur!), decent quality and is able to calculate ambient obscurance of quite high radius (up to 1.5m in our case) with fixed performance cost. Original paper presents multiple interesting concepts / tricks, so be sure to read it!

We plugged our temporal supersampling to the AO pass of algorithm – we used 3 rotations of SSAO sampling pattern (that was unique for every per screen space pixel position) alternating every frame (so after 3 frames you got the same pattern).

To combine them, we simply took previous ssao buffer (so it became effectively accumulation texture), took offset based on motion vectors, read it and after deciding on rejection or acceptance (smooth weight) combined them together with a fixed exponential decay (weight of 0.9 for history accumulation buffer on acceptance, it got down to zero on rejection) and output the AO.

For a static image it meant tripling the effective sample count and supersampling – which is nice. But given the fact that every screen space pixel has a different sampling pattern it meant that number of samples contributing to the final image when moving game camera could be hundreds of times higher! With camera moving and pixel reprojection we were getting more and more different sampling patterns and information from different pixels and they all accumulated together into one AO buffer – that’s why it behaves so well in motion.

Why we supersampled during the AO pass, not after blur? My motivation was that I wanted to do the supersampling, so increase the number of samples taken by AO by splitting them across multiple frames / pixels. It seemed to make more sense (temporal supersampling + smoothing, not just the smoothing) and was much better at preserving the details than doing it after blur – when the information is already lost (low-pass filter) and scattered around multiple pixels.

To calculate the rejection/acceptance we used the fact the Scalable Ambient Obscurance has a simple, but great trick of storing and compressing depth into same texture as AO (really accelerates the subsequent bilateral blurring passes, only 1 sample taken each tap) – 16bit depth gets stored in 2 8-bit channels. Therefore we had depth information ready and available with the AO and could do the depth rejection for no additional cost! Furthermore, as our motion vectors and temporal AO surfaces were 8 bits only, they didn’t pollute the cache too much and fetching those textures pipelined very well – I couldn’t see any additional cost of temporal supersampling on a typical scene.

Depth rejection has a problem of information “trailing”, (when occluder disappears, occluded pixel has no knowledge of it – and cannot reject the “wrong” history / accumulation) but it was much cheaper to do (information for given pixel compressed and fetched with color) than multi-tap color-based rejection and as I said – neither we, nor any testers / players have seen any actual trailing issues.


## Comparison to previous approaches

Idea to apply temporal smoothing on SSAO is not new. There were presentations from [DICE [2]](http://www.slideshare.net/DICEStudio/stable-ssao-in-battlefield-3-with-selective-temporal-filtering) and [Epic Games [3]](http://qa.gdcvault.com/play/1295/Rendering-Techniques-in-GEARS-OF) about similar approaches (thanks for Stephen Hill for mentioning the second one – I had no idea about it), but they differed from our approach a lot not only in implementation, but also in both reasoning as well as application. They used temporal reprojection to help smoothen the effect and reduce the flickering when camera was moving, especially to reduce half resolution artifacts when calculating SSAO in half res (essential for getting acceptable perf on the expensive HBAO algorithm). On the other hand, for us it was not only to smoothen the effect, but to really increase the number of samples and do the supersampling distributed across mutliple frames distributed in time and main motivation/inspiration came from temporal antialiasing techniques. Therefore our rejection heuristic was totally different than the one used by DICE presentation – they wanted to do temporal smoothing only on “unstable” pixels, while we wanted to keep the history accumulation for as long as possible on every pixel and get the proper supersampling.


## Summary

I hope I have proved that temporal supersampling works extremely well on some techniques that take multiple stochastic samples like SSAO and solves common issues (undersampling, noise, temporal instability, flickering) at a negligible cost.

So… what is your excuse for not using it for AA, screen-space reflections, AO and other algorithms? 🙂


## References


Pingback: Digital Dragons 2014 slides | Bart Wronski

Pingback: C#/.NET graphics framework on GitHub + updates | Bart Wronski

Pingback: Dynamic shadow casting point lights for tiled deferred rendering | Alexandre Pestana

Pingback: Project Journal – Smoothing – Michael Daltrey

Pingback: Local linear models and guided filtering – an alternative to bilateral filter | Bart Wronski

Pingback: Bilinear texture filtering – artifacts, alternatives, and frequency domain analysis | Bart Wronski

Pingback: Why are video games graphics (still) a challenge? Productionizing rendering algorithms | Bart Wronski

Pingback: Gradient-descent optimized recursive filters for deconvolution / deblurring | Bart Wronski