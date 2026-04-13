---
title: Sci-Fi interior rendered with Brigade WIP 1
url: http://raytracey.blogspot.com/2012/05/interior-sci-fi-wip-1.html
author: Sam Lapere
published: '2012-05-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

First WIP screens from a highly detailed sci-fi scene:

This is quite a challenge for Brigade, because it's an enclosed environment with fairly complex geometry lit by multiple small mesh lights (no light from the sky or sun), a dreaded cause of Monte Carlo path tracing noise. In brief, a perfect environment to test Brigade's convergence speed. Much to my surprise, this scene converges extremely fast (as fast as an open outdoor scene lit by sun+sky), even with very small lights. Brigade never ceases to amaze me. More screens and video soon.

UPDATE: for comparison reasons, a screenshot of the original sci-fi scene (created by Stonemason/Stefan Morrell), which was rendered with finalRender can be seen here:

## 38 comments:

Wow! It's so amazing how different art can put a new perspective on a technology. This looks incredible, and really pushes the idea of real-time interactive graphics. To be honest, it looks as good as many pre-rendered movies.



Did you build the interior? Mad respect if you did, you are a very talented artist!

Keep it up!

Thanks for the great comment Sean.


The scene was built by Stonemason (stefan Morrell), an incredible artist who also made the Streets of Asia and Urban Sprawl scenes from previous blog posts. His scenes make perfect testcases for Brigade: higly detailed geometry and textures, every object has its own material and the scenes are always a piece of art.

Absolutely amazing!

pardon my french but this is fu*ing AMAZING :D


excellent work sam :)

Can't wait for the video.. wow, just wow..

Wow, yet again Brigade never ceases to amaze me.


Can you give us information about the polygon count of this scene?

Kevin, the triangle count is 226k in this scene (the number of primitives in the scene is always shown in the upper left corner of the screenshots)

@Sam


Any opinion on GK110 with respect to ray tracing? I'm not too familiar with ray tracing implementations to know the bottlenecks.

From what I've read about GK110 (http://fudzilla.com/home/item/27196-kepler-gk110-detailed-by-nvidia) it seems to have twice as much L2 cache as Fermi and twice the bandwidth, which should greatly benefit GPU path tracing. The Kepler cores are individually less performant than the Fermi cores, so it's impossible to deduce any useful conclusions from the 2880 core count number. It might be a lot faster than Fermi in path tracing, or not. Hard to say, because GK110 doesn't exist yet.

From an architectural point of view Kepler 1 and Kepler 2 are very similar: 8 vs 15 SMX.

L2 cache read per clock is 384, 512 and 768 byte per clock, for Fermi, Kepler1, Kepler 2.

Fermi optimized algorithms will need to be retuned for Kepler. I'm wondering what architectural change, between Fermi and Kepler, has hurt Brigade so much ?

I don't know, but Brigade has already gotten quite a large performance boost on Kepler since the first tests, and I have a feeling there are more speed gains ahead soon.

Seems that Brigade will soon be powered by Nvidia's Geforce GRID



http://fudzilla.com/images/stories/2012/May/General%20News/nvidia_geforcegrid_devs.jpg (notice OTOY listed as middleware)

http://fudzilla.com/home/item/27186-nvidia-promise-impressive-things-with-geforce-grid

Can't wait :)

hmmm, yeah, nvidia spoiled the surprise ;)

sam, did you see the Unreal 4 screenshots that were posted today on http://www.wired.com/gamelife/2012/05/ff_unreal4/all/1?pid=2562 ?


I think Brigade completely blows it away. Nice pics btw

Thanks Anonymous.


Yes, I've seen the screenshots. I wasn't terribly impressed either to be honest. Maybe it's just a badly chosen scene, but I expected more from Epic. The Wired article talked about photorealistic graphics, I think Brigade is much better in that respect. I need to see it in motion though before judging the graphics.

Now that I've seen a first glimpse of the Unreal Engine 4 I think that next-gen is truly in cloud gaming; the next gen consoles will only reach 2-3ish TFLOPS in their GPUs





(I doubt Sony and Microsoft will release something more powerful than this)and will be stuck on that for the next 8 years, instead of the initial 4.7 TFLOPS provided by Nvidia's Geforce GRID(which is almost the double than two Geforce 580, BTW)and the beauty of the cloud is that the hardware can be updated every new iteration per year, so there's a big win there.Cloud gaming could potentially destroy the market of console gaming like digital distribution killed PC retail (and very soon console) since the economic of scale is much cheaper than building a tight console with hardware that is sold at a loss.

They can incorporate cloud gaming on TVs, tablets, smartphones, everything with a display that has an internet connection.

I don't think Microsoft and Sony can't compete on that, but I think they will smart up and start offering these cloud gaming options sometime in the future, it will be fun to see all the reactions from that.

Times are truly changing and it's very exciting

Couldn't agree more FreDre

At least it will make building render servers a lot easier / cheaper, because of the hardware video encoding, also less lag and better image quality.

As long as cloud gaming is based on PC hardware, running PC games, it would actually be a good thing for PC gaming if cloud gaming would become more popular.

Yeah exactly. With these freshly announced dedicated cloud GPUs, cloud gaming will take off much faster.

btw: what version of Brigade2 are you using? Is it r2017 the one available on Jacco bikkers' site?




Also, you should put up the original renders so we can see the differences:

This is a link to Sci-Fi interior:

http://stefan-morrell.cgsociety.org/gallery/536375

I'm not using the public version of Brigade, but an in-house developed one.

Thanks Sam,


What I mean about showing the original vs the Brigade2 renders is to essentially "show off" the results of Brigade because they are quite impressive compared to the original ray-traced work.

Hi Sam me again,







would you be able to produce a video showing the differences between your in-house version of brigade and the public version on a similar model.

I know this is a lot to ask.. ;)

But if you don't have the time could you at least give an idea from your wealth of inside knowledge on the matter on these two questions.

Would the public version be able to do what you have shown here? taking into account volume of materials,3d data,lighting etc.. and the quality of the final render.

How much faster is the in-house version? 10%, 20% etc? over the public version.

regards

it would be easier if you had a name but okay.



I can't make such a comparison video, sorry.

The Brigade version that I'm working with is about 2.3x faster than the public version when the camera is not moving. It's more optimized and there's a bunch of other features as well, mostly experimental kernels. The public Brigade version should be able to do pretty much the same as what is shown in the screens, only slower and only on Nvidia GPUs. Try it :)

Here's a question for you: How many rays/sec do you think you could achieve on a geometrically simple scene like the Cornell Box, where cache misses are extremely unlikely?


I guess I'm trying to get a feel for how much of a role memory bandwidth plays on performance.. My guess is a lot, but many CUDA cores may hide much of this latency by queuing jobs while others are waiting on a fetch..

Hi Sam,





Thanks for the reply, well 2.5x faster is a lot, but its good to know it can render just as well or almost. ;)

Yes I will be trying it as soon as some GTX 590's come back in stock! If that will ever happen!

Regards

The guy with no name is Nicholas.

Sean, back in February I did a test with a Cornell box scene that you can see here:



http://i43.tinypic.com/72g047.png

About 240-270 Mrays/sec with a maximum path depth of 8 diffuse bounces with the Brigade code from February. Since then, there have been lots of speed boosts, today it would probably be somewhere between 500-800 Mrays/s. I can run the test again next week.

I think you go a bit too far when you say Brigade rivals the quality of FinalRender.

Look more closely, on the FinalRender image you have diffuse reflection of the lights on the ground for example.

And there are some odd white patches here and there on the Brigade render.

Anonymous: it was not my intention to reproduce the scene in the finalRender screenshot, I posted these screens before even seeing that screen.



The floor on the lower left part of the last screenshot shows proper glossy reflections (blinn).

The bright white spots are specular reflections from the ceiling lights (some are outside the viewing frustum)

These renders look really cool. This one (http://2.bp.blogspot.com/-vVeApoiH9h4/T7KFlcMHRmI/AAAAAAAACWI/Q7NA2XSDVGQ/s1600/scifi5.png I wonder how I properly use your a tag)looks like a photograph of a miniature (using a high ISO setting). I wonder, why do I interpret this as a miniature?

Thanks RC1290, I'm not sure why it gives the impression of a miniature. There's not much depth-of-field in there, maybe that's the reason.

Thanks Sam!



Wow, that's a tremendous amount of rays, and quite a few diffuse bounces. :) It would be interesting to see a test with simple boxes and not spheres (assuming the spheres were composed of triangles). In a simple scene with few to no cache misses, I would be curious how high the rays per second would climb.

Of course, I would not ask/expect you to run tests, though would be grateful if you entertained the idea!

Sean, I'll do a test with a Cornell box with boxes tomorrow and post some results

Sean, I'm getting 600+ Mrays/s in the cornell box scene with 2 GTX 580 cards:


http://i45.tinypic.com/28in6m0.png

Wow! Thanks Sam! :)



That's quite a hike in rays/sec but interestingly it seems that that memory bandwidth is not as high of a barrier as I had assumed. In this case, 3x - 6x performance on a simple scene over your far more complex examples. It's a significant boost, but certainly cache misses must be far more significant, so CUDA must deal with memory quite efficiently, have sufficient bandwidth, and perhaps the engine does some nifty pre-caching as well.

Anyway, thank you

very muchfor this! I would be interested to hear your thoughts!No problem sean, I like doing these little tests.


I'm afraid I can't tell you anything about the impact of the memory BW on brigade's performance. There are lots of factors that play a role, BW is one of them, but at this point it's not clear how much, so it's also very hard to predict Brigade's performance on any given HW architecture. In my personal experiments I've found out that using textures and normal maps doesn't have an impact on performance at all compared to rendering the scene without textures. Brigade is also quite insensitive to scene complexity.

Very, very interesting re: complexity scaling, which was always the ray tracing promise. It would be very interesting to see how far this could go with a stress-test environment before significant losses (no this isn't a request :P). But it's certainly promising for the future when performance is high enough to maintain adequate interactivity at which point tracing should provide a preferable alternative to rasterization (given the right APIs, of course).


That said, rasterization is seeing some cool advancements in photorealism, though it still looks quite

fake. Your examples are a revelation in real-time CGI.Thanks Sean, I appreciate it. I'm doing my best to push ray tracing as much as I can, because I'm getting tired of the virtual stand still in rasterization for the past 8 years.

Post a Comment