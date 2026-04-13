---
title: Photorealistic head with Octane Render
url: http://raytracey.blogspot.com/2012/12/photorealistic-head-with-octane-render.html
author: Sam Lapere
published: '2012-12-17'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just needed to share these jaw dropping images using Octane Render, they are too good to be true:

- ultra-detailed

__17 million triangle__human head mesh captured with OTOY's LightStage
- rendered with path tracing using physically based (unbiased) subsurface scattering

- HDRI environment map lighting

-

__2048x1024__resolution
-

**completely noiseless after 8 seconds with just one GTX 680 using Octane Render v1.01 (which features environment map importance sampling)**
And this is a 8192x4096 render (blogspot resized the image unfortunately). Note that all the detail is pure geometry, and is not coming from the normal maps

Another one:

[http://render.otoy.com/forum/viewtopic.php?f=6&t=25052](http://render.otoy.com/forum/viewtopic.php?f=6&t=25052)

## 23 comments:

have you played around with a lesser number of polys? I believe even with 1 million, or even 100k polys would have the same result and now visible "angles".

correction: *no* visible

Hi Mirror, yes, there actually are two lower poly versions of the same mesh. But to be honest we didn't bother trying those, because Octane handled the 17 million poly mesh as fluently as a one million poly mesh. And we don't like to compromise on quality :)

8 seconds.....


This is looking really insane and I can't get enough of Clay-renders...

Don't stop posting them please ;)

btw, in the forum link you provided, iceglace says it took him several minutes for the render, not 8 seconds.

Times you said are wrong, also i can't see any SSS on that head.


Nice quality though. Keep the good job.

Mirror: those timings are with Octane 1.0, which didn't have importance sampling of environment textures yet. With Octane 1.01 (which does have env importance sampling), the image converges in two seconds and is noisefree after 8 seconds for this model and resolution, and that includes subsurface scattering.



btw, icelaglace works in the same office as me, he showed me the interaction in this scene on his monitor, it's just unbelievable how fast it is.

Anonymous: you obviously didn't try Octane 1.01 :)

Strange, the timings on these screens tell it renders for 18sec:

http://www.pcgameshardware.de/screenshots/original/2012/12/HDRI_Environment_Importance_Sampling.jpg

Yes, we made that comparison to show off the new importance sampling feature in the 1.01 version and let it render for 18 seconds, but it was already clean after a couple of seconds.


dmcprince: we've got heaps of them, we'll post some new ones on the octane forum soon.

It's hard to notice the subsurface scattering. We are used to game techs and they are caricatural and coarse for now. Like the SSAO in fact.

MrPapillon: exactly, real SSS is much more subtle than what you see in games today. The backscattering on the ears for example is not as pronounced when lit with an HDRI map as opposed to using the sun in backlight.


btw, The difference between the head rendered with SSS and without SSS is very noticeable btw.

It reminds of when I first saw the Morpheus head for Matrix2 created by the ESC guys using mentalray... I was blown away that time too :)


god its been so long since ive done character work, all ive used is blender. (which is nice) but this octane render looks amazing, ive got a gtx690 so i should get it, and make something. I think id use 3dcoat for the sculpting of the scene.

Thanks for the comments guys






clintond: the first Matrix movie also blew me away (I was more impressed with the making of than the actual movie tbh), and I wanted to do those special effects in real-time; We're very close to that point now.

rouncer81: the gtx690 is a great card for Octane, you should try the standalone demo and see how it does

anonymous: we're workign on hair and eyes :)

funny you mention that nvidia human head: i had a discussion about that tech demo with icelaglace about how we were both impressed when we first saw it at the time of the gtx8800 launch. But it pales in comparison to what we can do now with octane. In the meantime another rasterized sss technique (separable sss) has surfaced, which looks a lot better than nvidia's head

Just to confirm what RayTracey is saying there.



These renders are noiseless after 8 seconds or something, it is true.

I left them running most of the time & I don't care about the speed when I do one big picture so that's why I don't really know how much time they take me. But then, yes; we tried & you have a clear image with SSS after 8 seconds.

+ SSS is not like your video games, guys. They just demonstrate it; it's not the proper use, it's the Sony way to do SSS; put everything red to show :hey look I have SSS, i'm so cool.

So yeah, Skin rendering is more complex than you get on video games that are screen-space effects mostly.

But still there are people from whom I hear/read things like this: “The level of visuals is as high as it will ever get. So why bother putting out new hardware and software to run the same basic things” and I’m glad there are people like you who I can use as a reference and just show people what we can expect in next gen games.

@Mark The problem at the moment is that there are lot of graphical issues with current gen and probably next gen. But compared to 8bits or 16bits issues, they are not elegant so people will rapidly enjoy the move to better graphics even if they don't understand why. I like to pinpoint the SSAO stuff that makes the game looks as if it was "painted" by an idiot.

Allow me to add that Octane is almost the next best thing since someone invented gravity. ;)





That being said let me just point out that people should get out more and see what the world realy looks like instead of comparing images to video games or other CG renders. In real life SSS is hardly noticeable unless lighting conditions are highlighting the effect (like studio lights or a sunset for example). Even then you'd have to look for it.

The same goes for color bleeding which was brought up in a previous entry. It certainly exists in real life but the effect is much less pronounced under normal lighting conditions than what you see in video games.

My point is, when trying to decide if something looks realistic you can only compare it to reality and not on other people's vision of reality.

Great job with the render Sam. Mind sharing some of the material settings? :p

Hi Hennie, I didn't make the renders myself, but Hayssam Keilany (aka icelaglace), a colleague of mine did. He is still perfecting the skin SSS material as you can see in the last pic I've uploaded, but I'm sure he will share it on the LiveDB once he's happy with it.


Glad to know you love Octane so much, it still amazes almost every day.

Everything's wonderful.

But let's see how he looks with eyes open.

The main problem area when it comes to CG human is eyes !!!

Wow this looks incredible

Good job, I like your post..

Post a Comment