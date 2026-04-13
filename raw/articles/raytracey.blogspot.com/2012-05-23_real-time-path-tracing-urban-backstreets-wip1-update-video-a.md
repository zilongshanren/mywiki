---
title: 'Real-time path tracing: urban backstreets WIP1 UPDATE: video added'
url: http://raytracey.blogspot.com/2012/05/real-time-path-tracing-urban.html
author: Sam Lapere
published: '2012-05-23'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Quasi-random, more or less unbiased blog about real-time photorealistic GPU rendering

Wednesday, May 23, 2012

Real-time path tracing: urban backstreets WIP1 UPDATE: video added

Some screens of a new scene (which might eventually be used in a small proof-of-concept game), rendered in real-time with Brigade (the scene is called "the Backstreets" and was made by Stonemason):

And that floors me! And you estimate that we'll see this in around 6-12mo? Incredible.

I read your comment yesterday that Brigade is still very brute force with a lot of room for optimization. This is impressive as it already is performing amazingly well, and hardware performance is also increasing at a blistering rate. What's even more exciting is companies like Imagination getting in on the action and pushing forward with their own dedicated hardware for precisely this task. Soon, something with the calibre of Avatar being rendered real-time will be a realistic aim.

Just for interest: Have you seen Cryteks approach to high performance stereo rendering? It's a really neat scheme and something to keep in the back of your mind. Brigade in stereo would be incredible. A similar technique could apply to cloud rendering without the need to push two full frames for each eye! http://crytek.com/cryengine/presentations&page=1 (first presentation)

Aha so you're a Canuck? :) Last year I've been hiking in the Canadian Rockies for a month, too beautiful for words :)

Stereo rendering is indeed an option, holographic rendering as well. You know, the cloud will be so powerful that it will enable new kinds of entertainment that people haven't even imagined yet.

The Rockies are something I have yet to see, but I hear really great things!

Hmm... I've never heard of holographic rendering, but it sounds pretty neat. Is it basically rendering a 'volume' of data that can be viewed from any angle, like multiple FB's each with depth?

That would certainly be neat, and even beneficial for performance in a multi-player world where the hologram can be shared among players rather than rendering each distinct view..

Yes, I have no doubt that the cloud will bring neat experiences.

There are also at least 3 good Head Mounted Displays on the market (ST1080, HMZ-T1, Cinimizer) so applications like virtual reality are closer than ever. I would love to step into Brigade and walk around!

Ah, of course.. Yes indeed, that is really cool! Path tracing would yield very high fidelity, photo-real objects if the image quality of the projection could be raised.

The interesting bit about the ST1080 HMD is that it actually doubles as an augmented reality display, with some 10% transparency. Future versions will be more transparent, but it doesn't take much to imagine using these with good head tracking and being able to walk around a virtual object without the blindness that generally accompanies strictly-VR HMDs.

Of course, holographs do not require additional equipment which is a nice perk. :)

You seem to know a lot about these HMDs. Do you happen to have one of those by coincidence or work in a related field? I know Carmack is testing the hell out of them as well.

Heh.. I only know as much as an avid enthusiast that dreams of romping through virtual fields in the near future! The (reborn) VR uprising is a niche at the moment, but thanks to new hardware, there are many enthusiasts hacking together working solutions. A search on youtube yields tons of results.

There aren't too many consumer-level products aside from the 3 that I listed (ST1080, HMZ-T1, Cinimizer), so it's easy to get up to speed on all of them. However, these devices just cover the eyes, and many enthusiasts hobble together various technologies to incorporate mobility, or head tracking for actual VR applications.

Take a look at this video for an idea of what's being done: http://vimeo.com/41350330

It seems that nobody has quite struck the cord for compelling VR but the pieces are there and are waiting for a game/project to really show what the medium is capable of (like Avatar was for modern 3D movies). That said, I'm glad that a prolific developer like Carmack with a proven track record is undertaking some testing.

I think it's only a matter of time before we step inside of the games that we play, or telepresence, or socialize in a virtual world. Certainly graphics make a difference and I see Brigade playing a part in that.

As for me, I'm slowly getting up to speed on graphics rendering, and I think I might try my hand at doing some research in the field with an eye on VR. There is much math to learn, but it doesn't seem that difficult, just esoteric to the uninitiated.

The Cinimizer movie looks very cool but the Mass Effect 3 VR movie looks like a missed oportunity, the third person perspective just destroys the immersion imo. And the guy with the gun doesn't seem to be doing much.

You hit it right on the head. The Mass effect demo is disappointing for a few reasons. As you mentioned, the third person kills the experience, and also it's gun tracked rather than head tracked. This is why his head stays so still. Ideally, you would want something that is head tracked and hand tracked for a better sense of immersion. After all, we don't constantly point and look in the same direction.

Feeble first steps, but I'm glad that some action is being taken to bring this type of experience out of the lab and into the home.

I should have linked to this example of the same DIY'er playing Skyrim (head tracked w/ wiimote for slashing): http://www.youtube.com/watch?v=jBP0q_kNdMY

Well I originally wanted a GTX 690, but then I wasn't sure if the public version of Brigade would work on that, so I set my sights on a GTX 590, but none are in stock anywhere, doesn't matter where you go online. so I finally got a gtx 580 3Gig, and even though tigerdirect.ca shows it in stock in Canadian locations in actual fact its shipping from the US, so you can't even rely on what is shown on the websites.

What is odd, is as soon as I purchased it tiger direct have changed all the shipping info, and it seems you can only purchase it in-store now.. I don't know what that means. But clearly they didn't have the product in stock.

So I'm just lucky I guess.

This can't be good for Nvidia , when you can't buy a high end video card anywhere , even one that is already 1 year old.

Hope you won't mind my comment : Although the "still pictures" are really impressive, intermediate ones like in the movies are quite noisy.

Would it be possible to try this idea : making a "convergence" estimation for each frame (based on difference between the version and the last), and only switching the previous visible frame with the current one when adequate (parametered) convergence is reached ? (in the meantime, changes to the scene should be delayed though). This would greatly reduce FPS (since only one in 10 or twenty is shown) but would better illustrate the final visual quality

The SFReader: I see what you mean, maybe it would indeed be better to increase the spp per frame at the cost of the framerate, but that would defeat the purpose of a real-time path tracer. But there are some improvements underway which should significantly increase the convergence rate.

The problem is currently, with the movies, you showcase neither picture quality since noise is still quite visible, nor real-timeness, since it's clear that for appropiate picture quality some delay is missing.

My proposal's results would be to show that while Real-Time is not there yet (at adequate picture quality), that picture quality IS there, and still, even if 1fps or 2fps, the it's almost interactive speed.

When we see the "still pictures", it's really clear that YES, Ray Tracing is the way to go. but the movie OTOH shows it in a not quite positive way.

Oh.. I thought you were working on it as you mentioned trying different kernels, speed augmentation, and you work as a graphics developer for OTOY etc... so naturally I thought you specifically were part of those who were enhancing it.

Brigade's ray tracing core is being worked on by Jeroen van Schijndel en Jacco Bikker, I've been writing some code to make frame averaging work, physics library integration, tweaking geometry, lighting and materials to render without hickups and look as good as possible with the least possible noise, trying different settings for diffuse and specular ray depths, pdf cutoffs, number of lights and intensity, experimenting with different noise filters, all enhancements which don't require much math.

## 33 comments:

Incredible! Those puddles instantly make me


seephoto instead of render. The dusk lighting is also amazingly convincing. Well done!I'm really looking forward to cloud gaming. I just hope the telcos keep up with increasingly more generous data caps.

Thanks Sean, this is just a taste of what cloud games will look like.

And that




floorsme! And you estimate that we'll see this in around 6-12mo? Incredible.I read your comment yesterday that Brigade is still very brute force with a lot of room for optimization. This is impressive as it already is performing amazingly well, and hardware performance is also increasing at a blistering rate. What's even more exciting is companies like Imagination getting in on the action and pushing forward with their own dedicated hardware for precisely this task. Soon, something with the calibre of Avatar being rendered real-time will be a realistic aim.

Just for interest: Have you seen Cryteks approach to high performance stereo rendering? It's a really neat scheme and something to keep in the back of your mind. Brigade in stereo would be incredible. A similar technique could apply to cloud rendering without the need to push two full frames for each eye!

http://crytek.com/cryengine/presentations&page=1 (first presentation)

I am one happy Canadian!

Aha so you're a Canuck? :) Last year I've been hiking in the Canadian Rockies for a month, too beautiful for words :)


Stereo rendering is indeed an option, holographic rendering as well. You know, the cloud will be so powerful that it will enable new kinds of entertainment that people haven't even imagined yet.

The Rockies are something I have yet to see, but I hear really great things!





Hmm... I've never heard of holographic rendering, but it sounds pretty neat. Is it basically rendering a 'volume' of data that can be viewed from any angle, like multiple FB's each with depth?

That would certainly be neat, and even beneficial for performance in a multi-player world where the hologram can be shared among players rather than rendering each distinct view..

Yes, I have no doubt that the cloud will bring neat experiences.

There are also at least 3 good Head Mounted Displays on the market (ST1080, HMZ-T1, Cinimizer) so applications like virtual reality are closer than ever. I would love to step into Brigade and walk around!

This video is a great example of what I meant with holographic rendering (the best is kept for last);



http://www.youtube.com/watch?v=eNWJ9XtRhLw&feature=relmfu

Virtual Reality with HMD's are another option and Brigade running in the cloud would be very well suited for that purpose.

Ah, of course.. Yes indeed, that is really cool! Path tracing would yield very high fidelity, photo-real objects if the image quality of the projection could be raised.



The interesting bit about the ST1080 HMD is that it actually doubles as an augmented reality display, with some 10% transparency. Future versions will be more transparent, but it doesn't take much to imagine using these with good head tracking and being able to walk around a virtual object without the blindness that generally accompanies strictly-VR HMDs.

Of course, holographs do not require additional equipment which is a nice perk. :)

You seem to know a lot about these HMDs. Do you happen to have one of those by coincidence or work in a related field? I know Carmack is testing the hell out of them as well.

It is any hope ;p to see a scene with moving parts and/or human model ??

BTW Amazing job

dozer_xtgx, I've made a scene with a moving object (Stanford bunny) some time ago, you can see it here:


http://raytracey.blogspot.com/2012/05/blinn-bunny.html

Heh.. I only know as much as an avid enthusiast that dreams of romping through virtual fields in the near future! The (reborn) VR uprising is a niche at the moment, but thanks to new hardware, there are many enthusiasts hacking together working solutions. A search on youtube yields tons of results.






There aren't too many consumer-level products aside from the 3 that I listed (ST1080, HMZ-T1, Cinimizer), so it's easy to get up to speed on all of them. However, these devices just cover the eyes, and many enthusiasts hobble together various technologies to incorporate mobility, or head tracking for actual VR applications.

Take a look at this video for an idea of what's being done:

http://vimeo.com/41350330

It seems that nobody has quite struck the cord for compelling VR but the pieces are there and are waiting for a game/project to really show what the medium is capable of (like Avatar was for modern 3D movies). That said, I'm glad that a prolific developer like Carmack with a proven track record is undertaking some testing.

I think it's only a matter of time before we step inside of the games that we play, or telepresence, or socialize in a virtual world. Certainly graphics make a difference and I see Brigade playing a part in that.

As for me, I'm slowly getting up to speed on graphics rendering, and I think I might try my hand at doing some research in the field with an eye on VR. There is much math to learn, but it doesn't seem that difficult, just esoteric to the uninitiated.

Here are some slightly better examples:



Cinimizer VR Setup:

http://www.youtube.com/watch?v=GaD44Keye1s

DIY HMZ-T1 VR Setup:

http://www.youtube.com/watch?v=lMIWAV5h4EI

The Cinimizer movie looks very cool but the Mass Effect 3 VR movie looks like a missed oportunity, the third person perspective just destroys the immersion imo. And the guy with the gun doesn't seem to be doing much.

You hit it right on the head. The Mass effect demo is disappointing for a few reasons. As you mentioned, the third person kills the experience, and also it's gun tracked rather than head tracked. This is why his head stays so still. Ideally, you would want something that is head tracked



andhand tracked for a better sense of immersion. After all, we don't constantly point and look in the same direction.Feeble first steps, but I'm glad that some action is being taken to bring this type of experience out of the lab and into the home.

Anyway, back on topic: Brigade is great! :)

I should have linked to this example of the same DIY'er playing Skyrim (head tracked w/ wiimote for slashing):


http://www.youtube.com/watch?v=jBP0q_kNdMY

Ok, I'm done :)

http://www.youtube.com/watch?v=jBP0q_kNdMY


Looks more like it! :) Much better graphics as well. Thanks for the links, might be useful sometime.

The video looks incredible, Sam. I can only imagine what a lush forest like scene would look like!

Thanks Sean.


We first need to have instancing in Brigade before we can render forests efficiently.

Yes, I can only imagine that instancing would be key for the amount of geometry in a forest!

As usual nice results, finally got an nvidia card shipped, was not able to get what I wanted but at least I will have a card that can run Brigade.

Nice, but what card did you actually want?

Well I originally wanted a GTX 690, but then I wasn't sure if the public version of Brigade would work on that, so I set my sights on a GTX 590, but none are in stock anywhere, doesn't matter where you go online. so I finally got a gtx 580 3Gig, and even though tigerdirect.ca shows it in stock in Canadian locations in actual fact its shipping from the US, so you can't even rely on what is shown on the websites.




What is odd, is as soon as I purchased it tiger direct have changed all the shipping info, and it seems you can only purchase it in-store now.. I don't know what that means. But clearly they didn't have the product in stock.

So I'm just lucky I guess.

This can't be good for Nvidia , when you can't buy a high end video card anywhere , even one that is already 1 year old.

The GTX 580 is a very good card for Brigade, two of them are even better :)

Hope you won't mind my comment : Although the "still pictures" are really impressive, intermediate ones like in the movies are quite noisy.


Would it be possible to try this idea : making a "convergence" estimation for each frame (based on difference between the version and the last), and only switching the previous visible frame with the current one when adequate (parametered) convergence is reached ? (in the meantime, changes to the scene should be delayed though).

This would greatly reduce FPS (since only one in 10 or twenty is shown) but would better illustrate the final visual quality

The SFReader: I see what you mean, maybe it would indeed be better to increase the spp per frame at the cost of the framerate, but that would defeat the purpose of a real-time path tracer. But there are some improvements underway which should significantly increase the convergence rate.

The problem is currently, with the movies, you showcase neither picture quality since noise is still quite visible, nor real-timeness, since it's clear that for appropiate picture quality some delay is missing.



My proposal's results would be to show that while Real-Time is not there yet (at adequate picture quality), that picture quality IS there, and still, even if 1fps or 2fps, the it's almost interactive speed.

When we see the "still pictures", it's really clear that YES, Ray Tracing is the way to go. but the movie OTOH shows it in a not quite positive way.

great work Sam, I wish I had the strong math background to do this kind of stuff.

Nicholas; thanks, there's not much math involved in purely making demos with Brigade

Oh.. I thought you were working on it as you mentioned trying different kernels, speed augmentation, and you work as a graphics developer for OTOY etc... so naturally I thought you specifically were part of those who were enhancing it.

Brigade's ray tracing core is being worked on by Jeroen van Schijndel en Jacco Bikker, I've been writing some code to make frame averaging work, physics library integration, tweaking geometry, lighting and materials to render without hickups and look as good as possible with the least possible noise, trying different settings for diffuse and specular ray depths, pdf cutoffs, number of lights and intensity, experimenting with different noise filters, all enhancements which don't require much math.

will a newer version be released in the future ,with all the recent optimizations?



ps: Good work regardless ;) happy to have someone dealing with all the questions the curious may have.

There isn't much I can say about new releases

Post a Comment