---
title: Prepare to be flabberghasted...
url: http://raytracey.blogspot.com/2013/03/prepare-to-be-flabberghasted.html
author: Sam Lapere
published: '2013-03-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

After the successful

[presentation at Siggraph 2012](http://raytracey.blogspot.co.nz/2012/08/real-time-path-traced-brigade-demo-at.html), Brigade will rear its ugly ahead again in public next week. This time it's Nvidia's GTC conference, where OTOY will have[a 50 minute talk on Tuesday](http://registration.gputechconf.com/quicklink/bp5lpqU), showing off Brigade, Octane Render and LightStage. Make sure to be there if you want to see the scene below running in real-time:
It's going to simultaneously blow your mind and socks off your feet (I'm still not completely recovered from the breath taking beauty) and you will regret it for the rest of your life if you won't be there. However, in the unlikely case that you can't make it to the conference, do not despair, because I'll post tons of screenshots and videos when the event is over.

## 24 comments:

Hahaha zombies...

Thanks ahead. And can you post the report/lecture, not only screenshots and video?

Second that, nothing short of the full presentation will suffice. :)

is there going to be a livestream of the presentation?

I was wondering for quite some time now, I don’t want to intrude/put my nose where I’m not supposed to….but have you [maybe] been contacted by some gaming studios like Crytek (or others)? I mean seeing this and what you could do in the future and thinking of a possible combination between cryengine 3 or maybe 4 (which presumably will be presented at this year’s GDC) and Brigade. I really don’t understand why your engine isn’t used…well everywhere? Again I apologize for asking this kind of questions but still your doing amazing work and the whole world should know about you work.

Mark => Because it's not an "engine" (yet ?). It's just a renderer that displays polygons and animated polygons.

The big part of a game engine is the whole runtime + tools + content pipeline. And that means millions of lines of code.

Aha ok, thanks for the explanation MrPapillon.



But I was thinking more in the line of implementation of this technology (renderer), couldn’t it be implemented somehow? Like the soft-body physics in cryengine developed by BeamNG. Or is this technology nothing similar...thanks in advance.

@Mark: It's got to prove itself easy for developers to adapt to (their learning curve is time, and time is money), and it needs prove it can reach a large market base - realtime ray/path tracing hasn't proven it has that kind or market penetration yet, especially in the past when computers were slower and GPGPUs weren't a thing. Although it's very easy to see it's gaining that potential.



Rasterization is how it's been done in the past, with rendering APIs like OpenGL and DirectX so that's what will stay for right now since it's standardized and well supported - plus studios have decades of research and hands-on experience with these APIs. The demos you're seeing are run on hardware higher than your average consumer, and even then there's significant graininess even before reaching 30FPS and higher (which if you can't do that, expect consumers to complain) - and that's only for rendering these benchmark scenes, ignoring everything else that goes into a game. And you'll also notice they haven't shown off a lot of support for multiple un-instanced skinned characters - which is something that almost every game has.

I guess long story short, as far as mass-marketing goes: the technology isn't 100% there, it's still a work in progress, and it's also about developer confidence and adoption.

Thanks Reaven for the lengthy and quite clear explanation and yeah I thought as much… especially nowadays whit the cost of making AAA games.




But even with games like Crysis 3 where graphics are [almost] everything, they still aren’t (at least not to me) as photorealistic as advertised. And yeah you’re right about rasterization being the predominant technology, but I fell that in some cases it’s really showing its [old] age and limitations(?).

Maybe it’s just me and my wish for “true” photorealistic and seamless worlds.

Anyway thanks again.

I'm so stoked for this presentation, and I can't wait to see the materials posted on this site.







@Reaven

From a rendering perspective, I think that rasterization carries with it the very steep cost of trying to be frugal and clever doing things that you otherwise get for free with photo-real techniques like path-tracing. I would also add that even the

besteffects generated with rasterization lack the photorealism that I've seen come out of brigade almost effortlessly on this year's consumer-grade hardware to boot!Path tracers also seem to be far less sensitive to on-screen geometry.

I think this represents a very real cost saving to the developer and the artist, and will make a compelling case for adoption of the technology. The developer can focus more time on building the interacting game world than trying to be clever on how best to draw it, and artists need not adhere as closely to triangle budgets (especially given instancing for mostly static objects).

Thankfully, there's nothing to technically prevent developers from manipulating a frame-buffer, or rendering to special targets, so non-photoreal graphics could also benefit from this engine as well.

I think the savings to developers constitute a very significant advantage with a path tracer, which will push adoption. Since large games tend to take 2-3 years, it would be very prudent to consider brigade seriously for next-gen projects, as when they finally arrive, relatively inexpensive hardware should be able to handle them effortlessly.

As an anecdote: for all of the racing games out there, old and new, I have yet to see one that holds a candle to the photo-realism (after convergence) of the taxi-driving demo Sam put up on the site and developed in his spare time. That's saying something.

@ Sean Lumily

although i am not a programmer or hardware specialist, but tend to understand what are the major differences between rasterization and path tracing, i can foresee that a future that would come up with specialized

path tracing acceleration and hybrid memory cube which is 7x times faster than ddr4, will be a very bright one. i hope the revelations that otoy is going to make on tuesday will help me to understand the secrets of path tracing and its benefits against rasterization. what doesnt mean that rasterization is sth that is

worse, but that it was the lack of computional power which was present until nowadays.

@colocolo

Or the possible future use off memristor (http://www.techspot.com/news/38536-memristors-could-make-cpus-and-ram-obsolete.html)

Nice to hear the enthousiasm!

@colocolo

I agree that we've reached the point theorized years ago that ray-tracing has met and is now outpacing rasterization. The simple scene attached to this blog post far-and-away outpaces any rasterized scene running on consumer-grade hardware in both rendering quality and in-scene complexity. I think that from this point forward rasterization will be old-hat (remember hardware speed is still exponentially growing), and increasingly obfuscated.

I see you used YEBIS to render the post effects...

Do you use it for the demo as well?

Does Brigade have a material editor hopefully something node base(more powerful and flexible)?

Still 2 hours to go...

Cheers from Italy!

Hi, sorry for the delay in answering. Great to see so much enthusiasm :)










Anonymous, Teemu, colocolo: the session was recorded and shoulds appear on Nvida's website soon. I will post a link once it's there.

Mark: yes, we've been approached by some of the largest game developers in the industry to use Brigade. Unfortunately I can't tell which ones.

MrPapillon: exactly, we still need some work on the tools side of things, but we're getting there

Reaven: Brigade is actually quite easy to develop game content for. There are almost no corner cases compared to a rasterizer. You don't need to worry about transparent surfaces, hundreds of lights, shadow map resolution, depth of field artifacts, ...

The tech is not fully there yet, but we have made enormous progress over the course of one year (a year ago, I never thought we could do the massively dynamic scenes that we can do today) and I'm convinced that we will have a very compelling product very soon.

Sean: thanks for your comment, couldn't have said it better

Anonymous: yes, yebis is used. More on that on the GDC next week.

Anonymous: yes, we can now edit all the materials via a simple GUI at runtime.

During the next days, we are going to record and upload some videos of the Brigade demo shown at GTC. The video files are huge and Youtube sometimes tends to cancel the upload for no reason, so please be patient.

Hi Sam,






All this looks very impressive and I know this is designed primarily for realtime games content but can I ask about the future of it within Octane?

It seems to me this PT is a LOT faster than the one implemented into octane currently. How much faster is this when compared side by side? It's very hard to see from your videos how long it takes for a noiseless image to converge because it's always moving.

I understand this is a different engine, so does that mean the future features of Brigade's Pathtracer (things like sss, motion blur, blurry reflections, fog etc)... would need to be written from the ground up independently of Octane development? Or can it be integrated into their existing PT somehow to make use of existing features? (sorry, I'm not a programmer!)

A lot of questions I know, but all I see is this so much faster than what we're using, and the sooner this is a full production rendering engine the better :-)

Are we talking years or months for some kind of integration?

Very cool, Sam Please keep in mind I contacted you a good while back to ask about indie dev support :) .


I’m working on a project idea for my local area (Crowthorne, Berkshire) and try to bring in schools from the local area (edgbarrow, Wellington College) to set up a Development studio in the wellington business park next to Wellington College. Idea being a commercial studio to bring together commercial and community work (building a model to get funding from local council, welli college and any private business investment possible to purchase PS4 Dev kits, PC dev kits, Microsoft dev kits). Idea being we run courses and after school labs for up and coming real time devs for the future, but also commercial release's to give these young people studio experience from the youngest age possible, and hopefully make some money to (we all have to eat). I hope if things move on with my proposals that I can rely on the support of the Brigade team, wink wink.

Hope to see the new Vids up soon, as after seeing your teams dev work on this nearly a year ago, that made me dump the idea of using other free sdk’s that would just break when i put them to the test on large scale environments. Proper excited about these developments, Im such a Geek. Cheers

James

I just saw octane's cloud renderer at the GTC 2013 keynote. It was very impressive to see how quickly the image converged! It should prove to be an extremely valuable tool for designers, and the service model should make things so much easier as well.

Karl: very good questions, unfortunately I can't answer them in detail. Let's just say there's an interesting crosstalk of ideas happening between Octane and Brigade. Integration between the two renderers is already happening. Brigade is indeed really fast thanks to some tricks and is incredibly efficient for highly dynamic scenes, which is extremely interesting for Octane too.



KingBadger3d: coincidentally I watched your YT channel yesterday. The physics demo in Sponza is very cool. Your project sounds really fantastic and it's exactly the sort of audience that Brigade is meant for, because it's so incredibly to get great results with Brigade in no time. We are working on an API/SDK at the moment. The videos will probably be posted tomorrow. Hopefully our internet connection doesn't break down on us :)

Sean: yes, we worked very hard on that demo (video here: http://www.youtube.com/watch?v=HYUOUMy-VDo). You need to see it and play with it first hand, it's incredible.

i dont think that path tracing is the future ever because you are running your benchmark with high performance octane render( combination of 112 nvidia gpu) but still your scene have so much noise and now a days if you can really count the available polygons and triangles in a single scene of games like gta then it is in 100billion approx and one more thing increasing the amount of available gpu to render doesn't help to decrease the noise

Lovely post. It is really nice and pretty Brigade is indeed really fast thanks to some tricks and is incredibly efficient for highly dynamic scenes.

Post a Comment