---
title: 'Real-time GPU path tracing: Cubed City'
url: http://raytracey.blogspot.com/2013/01/real-time-gpu-path-tracing-cubed-city.html
author: Sam Lapere
published: '2013-01-16'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Quasi-random, more or less unbiased blog about real-time photorealistic GPU rendering

Wednesday, January 16, 2013

Real-time GPU path tracing: Cubed City

A new test with the Brigade path tracer, showing 1024 physics driven dynamic cubes in a street scene. It's incredibly fun to fly through a photoreal scene in real-time while tons of cubes are falling from the sky in slow motion and being able to change all the lighting and materials at the same time. The beauty of how instancing works in Brigade is that moving hundreds or even thousands of rigid objects happens for free, with almost no impact on the rendering performance. Brigade also doesn't care much about how many polygons these rigid objects contain: a 100K poly Stanford dragon will render nearly as fast as 3K poly Utah teapot. This opens up a lot of possibilities: you could for example render scenes with hundreds of spaceships flying around in an extremely detailed procedurally generated landscape. Dealing with non-rigid meshes like animated characters is a bit harder for a path tracer, because acceleration structures need to be updated every frame, but we have a solution to that problem as well (that's something for another post :) In the meantime, enjoy the video and screenshots below:

The Video looks great, maybe not that fast rendering as other scenes, but its a hard scenario for sure!

Only your description text starts to bother me. Nowadays they are full of glorification and super here, awesome there. The attitude of a person who is in love with the stuff he shows is lost and the smell of a marketing hype is everywhere :/

And yes, I know that if I don't like it, I don't need to read it ;)

Definitively no color bleeding. I think that you do something like just ignoring all secondary rays that are not reflective. But anyway instancing remains cool.

@Sam: Yes there is color bleeding in the screenshots. In the video however there doesn't seem to be any secondary light transport at all. I reckon turning that on is not yet a viable option for real time scenarios?

Mr Hankey: look again at the video, there is enough color bleeding in there to make the rainbow anemic. It is most noticeable on surfaces pointing downwards like the bottom of the cubes which get a yellowy shine. The video and screenshots are both rendered with full path tracing, just look closer.

Ok that is meaningless to judge on screenshots anyway. I am glad that you confirm that you still have full color bleeding support. I always have nightmares of you breaking that part for any reason.

fantastic! i trust you that you arent cutting corners. this is as good as the real deal gets. I was wondering if the textures are letting the realism of the city down, to me the blocks look more real than the city does!

@Sam: Yes, when I inspected the converged stills in the video, I indeed saw the second bounce lighting. In the dynamic sequences there is just not enough time for the second bounce light to converge. I've become quite cautious with the claims here on the blog. Mainly because I've felt quite a bit of an overdose in the optimism department since the time OTOY got involved. Well, good job in that case! I just wish you could sometimes deliver more technical information, and not just screenshots/stills!

>> @Sam: Yes, when I inspected the converged stills in the video, I indeed saw the second bounce lighting. In the dynamic sequences there is just not enough time for the second bounce light to converge.

Yes, it's easier to spot after a keeping the camera still for a second.

>> I've become quite cautious with the claims here on the blog. Mainly because I've felt quite a bit of an overdose in the optimism department since the time OTOY got involved. Well, good job in that case! I just wish you could sometimes deliver more technical information, and not just screenshots/stills!

Well, I've always been enthusiastic about real-time path tracing if you would check my posts from 2009 onwards. Brigade and Octane have been my favourite renderers since their launch in early 2010, because they both do something that I have been dreaming of since about 10 years i.e. photorealistic rendering on the GPU in real-time. For me it was a no brainer to jump on these two engines because I knew that this tech was going to be the future of real-time graphics. And now, by a stroke of fortune, I even have the opportunity to directly contribute to both these engines, which is enough reason to OD on optimism. The main obstacle of this tech was supporting highly dynamic scenes with tons of objects in real-time, which Brigade wasn't very good at until recently. In the last two months we've developed a brand new geometry engine for Brigade which can deal with thousands of dynamic rigid meshes in real-time. We also devised a clever solution for non-rigid dynamic meshes like characters, which we can now support almost as efficiently as rigid objects. It's based on an idea which hasn't been tried by anyone else yet afaik. You will see more of it in the coming months.

how fast would Brigade Engine 2 be, if i u could programm it with a Ray traced accelerated card like the Caustic R2500 from Imagination Tech? Is there any reason why mainstream graphic cards dont have hardware acceleration for Ray Tracing? I am not a programmer, but i am quiet interested in such things. Path tracer are awesome. Especially the one in Blender. :)

Anonymous: > how fast would Brigade Engine 2 be, if i u could programm it with a Ray traced accelerated card like the Caustic R2500 from Imagination Tech?

From what I've read about the Caustic R2500, Brigade would run slower on it than on the GPU, because ray tracing (traversal + intersection) and shading in Brigade all happen on the GPU, while the Caustic card only does the ray tracing part and relies on the CPU for the shading. This means that rendering with the Caustic card will only about 2-3x faster than doing it all on the CPU, while Brigade is easily 10x faster than CPU when using a GTX 590 (and the performance keeps improving significantly every week). I also don't see how instancing, motion blur and displacement mapping could work on the Caustic card (or volumetric effects for that matter). The shading in the promo videos I've seen looks very simple, using complex shaders would massively slow down the interactivity because shading is CPU bound. To be clear, I really like the idea of HW ray tracing, but the current Caustic HW cannot compete with a GPU only ray tracer. However, I can see this technology take off for games once the RTU chip is integrated on the GPU (which takes care of shading), and I hope to see PowerVR GPUs + integrated Caustic tech soon.

> Is there any reason why mainstream graphic cards dont have hardware acceleration for Ray Tracing? I am not a programmer, but i am quiet interested in such things.

The lack of flexibility in choice of primitives is one thing, and the continued research improvements in acceleration structures make it hard to settle on one approach in fixed function hardware.

Hey Anonymous, there haven't been much updates lately because we're working very hard on a tech demo with Brigade that we'll be showing in a couple of weeks, and I don't want to spoil the surprise. It will blow your mind, I will post lots of screenshots and videos when the show is over. I've got some ideas for simpler demos that I can show in the meantime (probably next week) to keep you busy :)

If you want to see some impressive new real-time path tracing video, check out this video we did, rendered with Octane in real-time, including a photoreal human head with unbiased SSS

Hey Anonymous, there haven't been much updates lately because we're working very hard on a tech demo with Brigade that we'll be showing in a couple of weeks, and I don't want to spoil the surprise. It will blow your mind, I will post lots of screenshots and videos when the show is over.

Will we see a 1080p demo or at least 1080p screenshots? you are allowed to tell this,or not? ;)

colocolo: Yes there will be 1080p screens and videos. We did some tests this and last week and Brigade runs incredibly well in 1080p. It's as if you're watching a movie that you can play, I was blown off my socks how good it looks.

## 22 comments:

The Video looks great, maybe not that fast rendering as other scenes, but its a hard scenario for sure!



Only your description text starts to bother me. Nowadays they are full of glorification and super here, awesome there. The attitude of a person who is in love with the stuff he shows is lost and the smell of a marketing hype is everywhere :/

And yes, I know that if I don't like it, I don't need to read it ;)

It looks more realistic then octane ;)


~Radiant

Definitively no color bleeding. I think that you do something like just ignoring all secondary rays that are not reflective.

But anyway instancing remains cool.

Zom-B: I have always used superlatives when talking about Brigade, since the very first posts in April 2010, check for example http://raytracey.blogspot.co.nz/2010/04/real-time-pathtracing-demo-shows-future.html. And I'm still amazed by its speed in dynamic scenarios, which is constantly improving :)





Radiant: not really, but it can get really close under the right lighting :)

MrPapillon: check the bottom of the cubes in the first screenshots again.

@Sam: Yes there is color bleeding in the screenshots. In the video however there doesn't seem to be any secondary light transport at all. I reckon turning that on is not yet a viable option for real time scenarios?

Mr Hankey: look again at the video, there is enough color bleeding in there to make the rainbow anemic. It is most noticeable on surfaces pointing downwards like the bottom of the cubes which get a yellowy shine. The video and screenshots are both rendered with full path tracing, just look closer.

Ok that is meaningless to judge on screenshots anyway. I am glad that you confirm that you still have full color bleeding support. I always have nightmares of you breaking that part for any reason.

Don't worry about it. Color bleeding is a key part in making the image look real, so it's not going anywhere soon.

fantastic! i trust you that you arent cutting corners. this is as good as the real deal gets. I was wondering if the textures are letting the realism of the city down, to me the blocks look more real than the city does!

Thanks rouncer81. The textures are fine actually, but I didn't spend much time on tweaking the materials in the scene. We've been working the past two weeks on getting the materials and lighting from the sky look better, maybe I can show some results next time. Here's a taste: http://www.dsogaming.com/news/new-screenshots-video-from-real-time-path-tracer-engine-brigade/#more-42658

@Sam: Yes, when I inspected the converged stills in the video, I indeed saw the second bounce lighting. In the dynamic sequences there is just not enough time for the second bounce light to converge.

I've become quite cautious with the claims here on the blog. Mainly because I've felt quite a bit of an overdose in the optimism department since the time OTOY got involved.

Well, good job in that case! I just wish you could sometimes deliver more technical information, and not just screenshots/stills!

>> @Sam: Yes, when I inspected the converged stills in the video, I indeed saw the second bounce lighting. In the dynamic sequences there is just not enough time for the second bounce light to converge.




Yes, it's easier to spot after a keeping the camera still for a second.

>> I've become quite cautious with the claims here on the blog. Mainly because I've felt quite a bit of an overdose in the optimism department since the time OTOY got involved.

Well, good job in that case! I just wish you could sometimes deliver more technical information, and not just screenshots/stills!

Well, I've always been enthusiastic about real-time path tracing if you would check my posts from 2009 onwards. Brigade and Octane have been my favourite renderers since their launch in early 2010, because they both do something that I have been dreaming of since about 10 years i.e. photorealistic rendering on the GPU in real-time. For me it was a no brainer to jump on these two engines because I knew that this tech was going to be the future of real-time graphics. And now, by a stroke of fortune, I even have the opportunity to directly contribute to both these engines, which is enough reason to OD on optimism. The main obstacle of this tech was supporting highly dynamic scenes with tons of objects in real-time, which Brigade wasn't very good at until recently. In the last two months we've developed a brand new geometry engine for Brigade which can deal with thousands of dynamic rigid meshes in real-time. We also devised a clever solution for non-rigid dynamic meshes like characters, which we can now support almost as efficiently as rigid objects. It's based on an idea which hasn't been tried by anyone else yet afaik. You will see more of it in the coming months.

If it's not too indiscreet, which studies have you followed and in which school ? Thanks

how fast would Brigade Engine 2 be, if i u could programm it with a Ray traced accelerated card like


the Caustic R2500 from Imagination Tech?

Is there any reason why mainstream graphic cards

dont have hardware acceleration for Ray Tracing?

I am not a programmer, but i am quiet interested

in such things.

Path tracer are awesome. Especially the one in Blender. :)

Anonymous:




> how fast would Brigade Engine 2 be, if i u could programm it with a Ray traced accelerated card like

the Caustic R2500 from Imagination Tech?

From what I've read about the Caustic R2500, Brigade would run slower on it than on the GPU, because ray tracing (traversal + intersection) and shading in Brigade all happen on the GPU, while the Caustic card only does the ray tracing part and relies on the CPU for the shading. This means that rendering with the Caustic card will only about 2-3x faster than doing it all on the CPU, while Brigade is easily 10x faster than CPU when using a GTX 590 (and the performance keeps improving significantly every week). I also don't see how instancing, motion blur and displacement mapping could work on the Caustic card (or volumetric effects for that matter). The shading in the promo videos I've seen looks very simple, using complex shaders would massively slow down the interactivity because shading is CPU bound. To be clear, I really like the idea of HW ray tracing, but the current Caustic HW cannot compete with a GPU only ray tracer. However, I can see this technology take off for games once the RTU chip is integrated on the GPU (which takes care of shading), and I hope to see PowerVR GPUs + integrated Caustic tech soon.

> Is there any reason why mainstream graphic cards

dont have hardware acceleration for Ray Tracing?

I am not a programmer, but i am quiet interested

in such things.

The lack of flexibility in choice of primitives is one thing, and the continued research improvements in acceleration structures make it hard to settle on one approach in fixed function hardware.

Hi Sam.. Is there any news? ))) (I'm sorry, you're gone and we get bored)

Hey Anonymous, there haven't been much updates lately because we're working very hard on a tech demo with Brigade that we'll be showing in a couple of weeks, and I don't want to spoil the surprise. It will blow your mind, I will post lots of screenshots and videos when the show is over. I've got some ideas for simpler demos that I can show in the meantime (probably next week) to keep you busy :)


If you want to see some impressive new real-time path tracing video, check out this video we did, rendered with Octane in real-time, including a photoreal human head with unbiased SSS

This new demo is for GDC, right? Cant wait.

@Anonymous




(Dunno if I am allowed to post this, feel free to delete my comment if I did any mistakes ;))

Seems like it's for GTC, found this:

http://registration.gputechconf.com/quicklink/2y2tQlD

Can't wait either, it'll be absolutely amazing!

Hey Anonymous, there haven't been much updates lately because we're working very hard on a tech demo with Brigade that we'll be showing in a couple of weeks, and I don't want to spoil the surprise. It will blow your mind, I will post lots of screenshots and videos when the show is over.


Will we see a 1080p demo or at least 1080p screenshots? you are allowed to tell this,or not? ;)

colocolo: Yes there will be 1080p screens and videos. We did some tests this and last week and Brigade runs incredibly well in 1080p. It's as if you're watching a movie that you can play, I was blown off my socks how good it looks.

Finally Something that feels like a step forward from Lightscape days. You should get Prof Greenbergs feedback on this ;-)

Post a Comment