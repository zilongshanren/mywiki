---
title: 3D Engines out there
url: http://c0de517e.blogspot.com/2010/03/3d-engines-out-there.html
published: '2010-03-03'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Every now and then people ask me for recommendations on 3d engines for their projects. Honestly I'm not such an expert on the topic, I've always written or used in-house solutions, so my knowledge about free middleware is pretty thin.

On top of that, it does not help that most of the engines I've checked out looked terrible to me. You would expect people trying new and cool ideas in the opensource world, where you're not tied to deadlines and products.

You'll be wrong or at least, I've never seen anything interesting or new among the thousands of engines sources you can find on the net. Most of the times, they follow the same pattern, they are textbook engines.

They are all scenegraph based. They don't really care about caches or threads. They don't care about iteration time or ergonomy. They support all the wrong formats (i.e. the horrible Collada XML) and they're all busy implementing every "technique" out there. They go against everything I advocate on this blog :D

But enough of this. Here it comes my list of notable opensource 3d engines out there:



[Ogre3D](http://www.ogre3d.org/). This is perhaps the most famous one. The good thing is that there are some commercial products using it, most of them are not graphically intensive, but still, a good sign.

The community is huge, the documentation is huge, you'll expect this engine to be well tested. Also, there are bindings for any language out there, and even a C# native port (

[Axiom](http://axiomengine.sourceforge.net/)).The architecture does not look very interesting, the engine is big and complicated, but it focuses more in getting a lot of things done than solving the fundamental problems that a 3d engine should address. For example, it has little support for multithreading, just some locks and they seem to be not too tested as well.

It's packed with a lot of ready made stuff, from terrain to shadows, to LODs, particles, various culling methods and so on. All that I can say it that the quality of those black boxes varies at best though. A few years ago I remember looking into its lispsm shadows only to find it seriously broken.

Nebula (

**UPDATE**: last? version in the comments

[here](http://flohofwoe.blogspot.com/2010/06/radon-labs-rip-2000-2010.html), Radon labs is no more,

[Nebula 2](http://sourceforge.net/projects/nebuladevice/)could be interesting too, Nebula 3 is a rewrite -

[latest version](http://flohofwoe.blogspot.com/2009/11/nebula3-sdk-nov-2009-changelog.html),

[unofficial community?](http://nebuladevice.cubik.org/)): This is actually the only opensource 3d engine that I really like among the ones I've looked. It's made by the game company

[Radon Labs](http://www.radonlabs.de/), that offers it to the public.

Focuses on a lot of the right things, cares about the general infrastructure more than specific features. Also it has been used on commercial titles, with great results. Radon Labs ships titles for all the consoles, but obviously the opensource engine can't include parts of the 360 or Ps3 devkits. That said, their experience outside the PC realm, where you can push polygons for free, without needing to care much about performances or good coding practice (if you're not shipping an AAA title, that is) is a bless!

Recommended, even if the community does not seem to be huge or too active, it seems to be mostly carried over by Radon alone. That means that it's maybe better not to jump on it if you're a total beginner that does not want to learn from the source...



Here you can find its

Same really goes for

[OpenSceneGraph](http://www.openscenegraph.org/projects/osg): This one is interesting, it focuses on performance and multithreading, even if it's OpenGL only and it focuses a lot on portability, it's more a visualization engine than a game one, somewhat like NVidia[Scenix](http://developer.nvidia.com/object/scenix-home.html)or the old OpenGL Performer.Here you can find its

[mission](http://www.openscenegraph.org/projects/osg/wiki/Support/ProgrammingGuides/MissionStatement), and here its[forum](http://forum.openscenegraph.org/index.php)and development[blog](http://blog.openscenegraph.org/). Obviously it's scenegraph based and as I said, it's looks like it's an opensource replacement of the dead Performer or the never-born project Fahrenheit. So overall I won't use it and you need to keep in mind what's its purpose, but overall it has with lots of things going on, a good community and a clear design. There is even a nodekit for postprocessing, and some extensions to use Cuda and OpenCL.Same really goes for

[OpenSG](http://www.opensg.org/), both are worth a look but I won't recommend either for games or as a guide to design a 3d engine.[Panda3d](http://www.panda3d.org/): Another engine I don't know much about. But it has shipped titles, and from what I can see, I would prefer this as an alternative to OGRE.

[Sauerbraten](http://sauerbraten.org/): The guy behind this engine/game (

[Wouter van Oortmerssen](http://strlen.com/)) is a genius, he implemented more programming languages than the ones I know, and he worked on Far Cry! Sauerbraten is a very fast 3d engine, to the point that it has even been successfully ported to the iPhone. Surely interesting, even if it's very specialized in what it does, it's worth a look.

[Quake 3](ftp://ftp.idsoftware.com/idstuff/source/quake3-1.32b-source.zip): It's old, it's very specific, and it's not actively supported. But it's a serious commercial engine, and it was made by ID. That's more than enough.

Other worth mentioning.

## 43 comments:

I like irrlicht for small projects, it's small and relatively neat. But, as you say, a textbook engine.

Regarding your comment about Collada, I agree it's terrible, but it saves you from writing an exporter. According to my experience, writing a Collada converter to some internal format is more manageable than maintaining an exporter across DCC tools and versions.


What would you recommend to avoid Collada altogether?

For Quake3 you should better reference ioQuake: "This project, ioquake3 (or ioq3 for short,) aims to build upon id Software's Quake 3 source code release. The source code was released on August 20, 2005 under the GPLv2. Since then, we have been cleaning up, fixing bugs, and adding features."

Adrain: afaik, irrlicht is not better engineered than Ogre, but it has a smaller community and no shipped titles. Considering that I included Ogre only because of its support, and that anyway I won't recommend it for anything, I disregarded irrlicht. Maybe I'm wrong, as I said, I'm no expert in those engines, but I really can't see no use of those. If I was an hobbyist playing with 3d I would probably prefer either to craft my own engine, or go with Nebula. If I was a small company with no budget, I'd probably choose Unity.

Drealmer: it frees you from a simple task, and imposes a bad design on you.







What does Collada do for you? It exports vertices, normals, texcoords and so on in a rather bad format. But that's trivial, I mean, you can do better in 15 minutes of maxscript programming...

It still ends up being dependent on the specific exporter and application you're using (think for example about tangent spaces), so no cross-platform dreams.

Everything else, materials, tags, animations and so on, are even more dependent on the exporter/application. Chances are that your 3d application already has a native export format in ascii that is easy to import, and at least it will support everything the application can do...

But really, the point with interfacing engines to DCC is not about exporting geometries. That's trivial. It's about conditioning those geometries, optimizing them. It's about live-linking your game with the application. It's about managing material parameters, about interfacing with your version control, introducing asset consistency checks, previewing your rendering in the application and so on... All things for which you'd want to create your own plugins and tools in the application anyway.

Exporting meshes is really not a problem, and Collada really does not solve it.

If you want to support a cross-application format, and not write your own exporter, I would rather consider FBX anyway.

Thanks for the additional info!




I still think that an external Collada converter is easier to write, debug and maintain than a Max export plugin. I guess it's a matter of taste :)

But I would not recommend FBX, I had a really terrible experience with it, the error handling is awful, it crashes all the time at the slightest unexpected bit in a file.

Googling around I found Autodesk Crosswalk and it sounds promising, I should give it a try one of these days.

Drealmer: I wrote a pipeline that went from Max->Collada->Game, I worked with an engines whose pipeline imports directly maya files, and ones that have their own exporter plugins.





It might be that in those (two) years that passed since I worked with it, Collada has evolved to something more useful, but when I used it I found it to be incredibly bad.

When for a smaller project in the same company, we needed to support a third-party engine, we did a maxscript exporter for it and it took literally no time (even if being maxscript based, it was fairly slow).

As for FBX I can't judge its quality, and I personally won't use it as it's too closed but at least it's a real cross-application format, that really delivers on that promise.

Now I think that having a cross-application format does not matter at all, as anyway you have to customize your 3d application and exporting meshes is a non-problem. But if I wanted one, I'd bet on FBX more than Collada.

Do you know R5 ? A one man project that went open source not long ago.

You have to look there http://flohofwoe.blogspot.com/ for latest Nebula3 SDK.


They just don't update the googlecode project anymore.

Also, I would be interested in your opinion about writing a 3d engine from scratch that is not a textbook engine: what classes, utilities do you need, in which order?


This could be the subject of a book actually :/

I see you disregard OGRE and praise another engine because of iPhone support. The latest OGRE version (1.7) supports iPhone and there's work in supporting both Android and Symbian.






I would like to see more arguments against OGRE, and if you could, I think your opinions about how OGRE should change would be valuable for the team.

In Open Source we must never forget that usually the writer's of a certain application are no experts on the subject (at least when they started the project), and that effort and time involved are never repaid, so bleeding edge development is done only when someone has the time and is capable of such effort. Or when someone is paid for developing that bleeding edge.

Also, in my opinion, the benefits of a third party engine are that it should have been tested, proved to work, and support as many features as possible, so I understand that everyone tries to support every bit of functionality before actually developing new techniques.

Even if the team policy wasn't to add known techniques before creating new ones, with a very big community is likely that well known techniques were demanded or contributed to the codebase by the community before the team could implement new experimental techniques.

I'd like to know your opinion on this subject.

Regarding the Nebula 3 engine you linked to an UNOFFICIAL google code drop of the project that is extremely updated.


Please direct people to the proper link on Andre's blog: http://flohofwoe.blogspot.com/ where you can get the latest drop updated September 2009!

Maybe you want to join the discussion at:


http://www.ogre3d.org/forums/viewtopic.php?f=1&t=55993

To Shadow007/Anonymous: there is no point discussing on Ogre's forum, to convince who? people actively participating in the Ogre community... come on



Quoted from the Ogre's forum thread: "he's either not too experienced or simply just looking to stir up a discussion and get ad hits on his blog or he wouldn't make some of the claims he make"

seriously, where are the ads? who's not too experienced? there is really nothing to discuss there (and note facing this truth doesn't even involve my own opinion about Ogre's architecture)

Regarding Collada:




Collada is clearly over-engineered and it would often have been preferable to provide a single way to store the data instead of ten different ones.

However, as an intermediate format for a conditioning pipeline it is not too bad. The nice thing is that you don't have to care about exporters. Having to maintain exporters for constantly updated 32 and 64 bit versions of Max, Maya, XSI and the smaller DCC tools like Mode is quite annoying. With Collada you just write a single conditioning tool.

Horde3D for example has such conditioning tool that converts a tree of collada files into a custom, potentially platform-optimized format.

Joe: Thanks for the nebula link, I actually follow that blog already.





Kris: I gave a quick look at this K5 and it seems to be a small experiment right now. I think it has a long way to go to become something than an external team could consider.

Anonymous: I didn't reference ioQuake because there are many similar projects and I don't think any is more interesting than the original sourcecode as learning material.

guardian: sooner or later I should write a post about that. Even if I really hate to make a bullet-point wish list, I'll just list some of the things that make me happy when I see them in an engine.

Reflection/Serialization. Paramter system/Scripting and tool interface. Object lifetime. Resource loading/hotswapping/streaming. Code iteration/hotswapping. Performance (simd math libraries, cache efficient collections and so on). CPU texture and mesh processing. GPGPU scheduling.

mukik182: I don't "praise another engine because of iPhone support", that engine is iPhone only and I'm suggesting that if you're going to write for the iPhone, looking at that one can be a good learning experience, as it has some nifty snippets, like a vectorized assembly math library.

About Ogre: I don't think I can give suggestions to OGRE. I mean, their project is pretty successful, even if I don't understand what "market" does it have what's the focus.

I think as a project is well maintained with a good community, but it's a well maintained textbook, amateur engine.

What I'd personally love to see more in opensource is the opposite, it's the experimental, the new, the unconstrained. Not the boring scenegraph and shadowmaps stuff.

I respect the OGRE community, they have this project and they're successful with it, but if I have to suggest an engine, or if I had to use one, my vote would be against it.

It's something like PovRay. As a raytracer is useless, if I had a graphics blog I won't suggest to use it (even 10 years ago). But you don't go there and say "hey, you should stop making this raytracer that it's all about primitives and scripting, we're not in 1980 anymore". That would be stupid, because that's what PovRay is, and in what it does it's the best so far.

Anonymous. Again about Collada. I understand the argument, again my points are:


1- It's not true that Collada gives you independence, for a lot of important details and flags and stuff it's still up to the specific application/exporter. So there is no real saving

2- Even if you had some saving, it's very little when you have anyway to write plugins to 3d applications to support your engine features, live updates, previews etc (that is, fundamental stuff) and you still have to write conditioning. So it "saves" you the least of the effort of managing data, introducing a bad and inefficient design...

BTW the OGRE forum does not allow unregistered users to post, I'm too lazy to sign in, and anyway I don't think there's anything to say. This is a small post only to answer some questions that people ask me, and it's my personal impression. That might even be very wrong, I said that I don't have strong opinions about those projects anyway.

The Nebula engine does not seem to be very open.





Where can we download an SDK, for example? All the links I found from the blog of the author are DEAD.

I can see there is a google code page for the project but as far as I can see it is not an 'official' page - it is not maintained by the author of the project. And by the update frequency from that page I could consider the project 'dead'.

Considering that, I don't think I could choose Nebula over Ogre3D. It has to be opened up if it is supposed to compete with engines like Ogre3D. It may or may not be better for all I know but finding out is pretty hard when finding an SDK is so hard.

Also there seems to be conflicting information of whether it supports Linux or not. It seems someone may have added such support, but it is not official. This is a big minus as far as I am concerned. It may not be a big minus for serious commercial game projects, but for the "open-source" crowd it certainly is.

Anonymous: (could you non registered guys sign with a nick anyways?)






I know that the last nebula update is from 2008 and I wrote about that. But if you notice the last game radon shipped was in 2008 too, so I suspect they're waiting for their latest effort to come out.

That means indeed that you don't have much support probably, and it would mean that you need to be more expert. It's something to consider, and in fact I listed OGRE among the notable engines as well. It's a tradeoff, and the choice is yours of course! Nothing wrong with that.

As for the opensource thing. I don't think being opensource is a virtue per se. I know that there are people that think otherwise, and in that case be free to do as you wish. Personally I don't care about linux as I think it is irrelevant if you want to make a game so I didn't list linux compatibility as a feature, actually for me supporting OpenGL only is something that I see as a defect. Again, it's an opinion.

If you love linux and love opensource and love having a rich community to help you, then your priorities and different than mine, and by any mean, go with OGRE.

WTF in the end there are also people that find PovRay, GIMP or dunno, EMACS or PHP useful, so by any mean, go with those if you need them. But I won't recommend them on this blog. It's not a democracy.

You recommend FBX over Collada?!!

I've spent a lot of time writing importers for both and I can tell you that if I had to pick one I would choose Collada DAE without hesitation.

Importing a mesh from either isn't so hard, but once you get into the details of how to transform things properly (e.g. for skinned meshes) the fact that Collada has a written specification makes the job so much easier. FBX has very little documentation and you can't view the source of the SDK so figuring it out requires long, painful experimentation.

Just look at the official FBX discussion board to see how much pain and anger it causes!

First of all, it's my first comment here, I'm not any of the Anonymous in the previous comments.













Secondly, please accept my excuses for the way I posted about your blog on the Ogre forum. I didn't want to write anything aggressive, but just try and provoke thoughtfull response the kind of which I usually see on the Ogre forum.

I absolutely don't endorse Stefan Lundmark's dismissive comment.

Now please understand that I quite agree/acknowledge that a blog is the right spot to voice it's own opinions, and don't want to sell you something that you clearly don't want/need.

I now see I should have instead have asked you here to elaborate on your post regarding Ogre before posting on the Ogre forum.

From your replies, I think I understand some of your critiques, and you may be right, Ogre seems to be a "by the book" kind of Graphics engine rather than a State of the Art one or even an "highly innovative" or creative one.

It may have quite a lot of other shortcomings, one of them beeing a "Graphics engine" only rather than a complete "Games Engine". An other one is the multi-threading integration, which has recently had some changes, and will more completely evolve. The ressource management also is having big changes with many evolutions for background loading and so on...

As for some of the other features you mention in response to Guardian, I think most of them should be more integrated in a complete Game engine rather than in its graphics part which is Ogre's only goal.

At last, regarding Ogre and innovation, I need to mention that Ogre 2.0 (Codename Tindalos) should allow quite innovative work, even though it's still really a long shot and quite far away.

(http://www.ogre3d.org/forums/viewtopic.php?t=30250)

Once again, Ogre's goal is to provide a modular base for the graphics part of a Game engine, and should clearly NOT be seen as a game engine in it's entirety. As such, it is used by people who want an "out of the box" graphics engine, without having to spend precious time reinventing a wheel or having to buy one too costly.

I think that if Runic-Games team saw enough value in it to create Torchlight, it should be enough to at least give it some credibility to Ogre's value (amateur ? right ...).

Shadow007> sorry :)


About giving credibility to Ogre, it's also worth noting Jason Gregory mentions it favorably several time in his Game Engine Architecture book ( http://www.gameenginebook.com/ )

Shadow007: I wasn't offended by any post, nor by the reaction on OGRE forums. And I know there are some very good indie games made with it, I said so in the post.













I understand that OGRE is perfectly usable to make such games.

So let me clarify further.

When I wrote this post, I was thinking about recommendations both in terms of engines to in practice make a game or a realtime project, or in general for learning about 3d graphics.

Now, for 3d graphics, there is so much information around, and so much sourcecode. But most of it is in what I called "textbook" style, that's to say, implemented more on the theory than on the understanding of what really matters in the production on an AAA game.

I don't consider that to be much valuable for learning, because there is an overflow of engines that use the same stuff, it's trivial nowadays.

From what I know about OGRE (that is not much), I don't see it as being an interesting engine learning-wise. Why so? Again because it's a pretty plain design that you can find anywhere else.

For an actual project, I think OGRE can be used, and that's why it made into the list. It's well supported and well tested, and has shipped products. And I said so.

Overall I won't still encourage anyone towards it because in my view, if your goal is to ship an actual product, then you should rather be using Unity. It's not free nor opensource, but it's cheap enough to not be a problem for most of you.

Michael: Can we dismiss this Collada thing? It seems that everyone is getting it wrong.

I don't advocate the use of FBX, I don't advocate the use of intermediate files at all, because, and it's the tenth time I say this, reading in the mesh is the least of your problems, writing an exporter is a trivial task, and you need to have a plugin in your DCC application anyway for so many other things that it's fine to manage the export there too.

Then I said, IF for some strange reason, you don't want to write such plugins, because you want to support a format that works with every 3d application, AT LEAST choose one that really delivers on that promise.

Hope it's clear, I won't reply about Collada anymore.

Thanks, I stand corrected and appreciate the further explanation of your points, which for me wasn't clear enough in the post. Thank you for your time, I appreciate it.


Sidenote: I think Gregory Junker praises OGRE often because he is a very active community member, but I'm not sure.

"I know that the last nebula update is from 2008 and I wrote about that. But if you notice the last game radon shipped was in 2008 too, so I suspect they're waiting for their latest effort to come out."







- As I mentioned earlier in on this post this is

completely incorrectinformation.Two facts:

1.) The link you keep giving saying that "Radon Labs has not updated it since 2008" is to a Google Code project of Nebula 3 that is not owned or maintained by Radon Labs!

2.) The SDK has been updated as recently as November 2009 and can be freely downloaded: http://flohofwoe.blogspot.com/2009/11/nebula3-sdk-nov-2009-changelog.html

I am unsure why you keep telling people it hasn't been updated since 2008 when that is clearly not the case? Andre has done 2-4 releases per year of the engine and there have been

manySDK releases since the one in 2008 that you keep referencing.Sorry I just wanted to clear up these misconceptions.

Joe: Thanks for the info! To be fair, it's not my fault. The radon labs website links only to this (Nebula community) http://nebuladevice.cubik.org/ that in turn, clearly links to the google code stuff. I understand now that this is unofficial, but it's easy to be fooled.

Anyway I'll edit my post to link to this newer version of the engine as well.

I have to say that even if you look at commercial engines, many of them are scenegraph based.





I would even say that it's commonly believed that a good game engine implements a good scenegraph architecture.

I do understand why you would look at other architectures but the considerations you have are concerns of console programming world where cache-misses and threading are criticals.

Such concerns are totally ignored by hobbyist. And I would add that there's not many hobbyist targetting consoles.

So unless a professional start a project just for fun, you will not likely find an engine that meets your wishes.

mukik182:



Gregory Junker != Jason Gregory

Gregory Junker is an active member of the ogre community and has written the book Pro Ogre 3D Programming.

Jason Gregory is a programmer at Naughty Dog and the author of Game Engine Architecture. He uses Ogre among other engines to explain stuff in his book.

JS: Sure thing, but again my recommendations = my concerns.



Also I don't like the design behind many commercial engines, you have to realize that in many cases their attractiveness is not in their design at all, but in the fact that they're proven and tested, and have good tools and pipelines.

Also a lot of those have a long history, and so some core design choices can be less than revolutionary. I think Gamebryo is a good example of that.

I completely understand how you made the mistake as it really isn't clear. I just wanted to clarify it so that you could fix it in your article, that way people won't get the wrong impression that it is a stalled or dead project.

I wonder why everyone is bashing scene graph based engines. Sure, a scene graph which tries to optimize everything (as in the very old OpenGL engines) is completely retarded these days but what's wrong with a scene tree which just stores transformation hierarchies?


It is better if the renderer does not know about any scene structure (hence submission based), however, most open source graphics engines are not just pure renderers but provide 3d engine (spatial organization, culling, etc.) and basic low-level animation functionality.

Anonymous: I wrote a post about that. Bottom line: organizing your objects around a transform scenegraph is retarded (imho) because well... because a 3d engine should not care about transform hierarchies AT ALL.








Long story:

I mean, it's stupid enough to suppose that all your objects need that, when in reality only skeletons and little else do (in fact, most of the objects in an average game are static).

But it's even worse because anyway, animations are a realm of the game. They should be managed by your "game thread" and your 3d engine should not concern itself with managing transform hierarchies at all!

Managing animations on the "render-side-of-the-world" is totally wrong. More often than not, the game needs to know the result of a given animation anyway, i.e. know where the hands of the player are.

Having the 3d engine managing those establishes a bidirectional dependency between game and rendering: the game tells the rendering what animations to apply, the rendering tells the game what is the result.

It's an obviously bad design, but it's so widespread that it's even hard to persuade people to see the evidence...

p.s. It would be a little bit more reasonable to organize your scenegraph as an hierarchy of bounding boxes. At least in that case you're dealing with something that an engine should concern itself with. But I think that fixing that as your fundamental structure is a bit too much of an assumption, but at the very least, it would be a more reasonable choice.

What would you use instead of a scenegraph? Just the final transformation matrix for each object?

Deadc0de:







As for the scene graph, I partly agree. (sono pienamente d'accordo a metà col mister!)

If you refer to a singlethreaded design, except pointing out to let the renderer animate stuff has a little to do with the data structure in use, I agree.

It is a design flaw. An huge design flaw.

When you introduce concepts like "game thread" I don't follow you anymore.

Multithreading is another world.

Another universe.

Ok, let's assume we have a game thread and a rendering thread.

The game thread animates stuff and the rendering thread renders it.

What's the point in having the game thread running at 25/50hz and the rendering thread running at 200fps?

It will always look like you'll be at 25/50fps!

On the other hand if you sequentially executed the game and rendering threads, then it would be pointless to have threads.

You clearly need something more, and this something must be part of the rendering thread, because execution has to be sequential!

IMHO, to say animation must not be on the "render-side-of-the-world" is ok for a singlethreaded engine but it's not always true in a multithreaded one...

Dr.Kappa: indeed that's a problem. But let's review your assumptions first. And this will be a long story...












Why you start assuming that game and render threads would run at different frequencies? Is that the usual case, when dealing with multithreading?

That might have been the case in the last generation, when threads were not used for performance, but to deal with different tasks in the same application.

But today? What's the most usual safe and useful threading method?

Well I'd say, thread pools with data-parallel tasks, and dependecies between them, right?

Now when you start playing with such a threading architecture, you'll realize that if you just use it as is, you'll get sub-optimal thread utilization. Why? Because even if the data-parallel tasks parallelize well, often their dependencies are in a long chain, so you can't execute more than one of such parallel tasks... in parallel.

Hopefully, you're still following me there. What's the usual solution for that? Well we can split our dependency chain by adding buffers and latency.

I can take a dependency chain, split it, and instead of feeding the output of one end to the input of the other, save the output in a double (or more) buffer, and feet the input with the previous-frame contents of the buffer.

That's what happens with the "game" and "render" threads. They are usually nothing else than a way of separating dependencies, normally you would get a number of tasks to perform in the game side, but all of those are inputs to the rendering, that should wait for them and then its tasks can happen.

By putting a double buffer you can still ensure they are executing at the same frequency, in sync, but with a one frame delay, the rendering will render what the game computed the last frame...

And this is really what also happens between the rendering on the CPU, and the rendering on the GPU, right?

So in most cases, your assumption is flawed, simply does not hold. If then you would ask me if it is possible to make such a thing, to decouple rendering and simulation at a level were they can even run at different frequencies, while the animations still play smoothly... Well, there is a way to achieve that too, at least if you have a bound on the worst-case between the two. It does not change the overall design of the rendering or of the game, it only requires to change the buffering layer between the two...

But that's another story, I'll leave that as an exercise for the reader :D

Bottom line: animation is always a "game" or "simulation" task. It should not influence the design of the rendering.


And EVEN MORE WITH MULTITHREADING. As I said, the problems of considering animation as a rendering task, is that you introduce duplex communication between the game and the rendering. With multithreading communication is harder (involves sync) so it only makes the problem worse.

I agree with your post, that's (almost) the way I implemented my multitheaded renderer. No synch points, no locks, thread pools/task trees, communication via double/triple buffers.




My question is: you submit data to the renderer, then it turns out the rendering thread has the potential to perform 2-3 renders while the game thread is calculating another frame.. what is the render supposed to do?

1- re-render the same data 2/3 times.

2- stop until new data arrives

3- something else...

Solutions number 1/2 look suboptimal to me. It's like introducing a fake synch point by design. Why should I want to spend time desynching game and rendering threads if I can't take advantage of extra rendering time and I'm forced to stop the rendering thread or make it render the same things?

It would be easier (and much less elegant) to have a gigantic task tree/thread pool whose final node/entry is the rendering task/tread.

Dr.Kappa: There is a way around it but I'm not going to explain it because AFAIK it might be IP of my company, as I have yet to see someone doing what we do.







But even if you just double buffer, it's still a perfectly good approach, especially on the consoles where the time spent in the two threads is predictable.

You've created a pipeline, and yes, maybe now one part of it is stalling everything else. So what? It's exactly the situation we have on the GPUs and we know already the solution. Either you remove the bottleneck, or use it as an opportunity.

To remove it you can either optimize the code (obvious) or just add buffers and latency (i.e. if your game thread is doing AI and animation, and both of them are too expensive, just add a double buffer between the two and so you can fold them again, as you did with game and render)

To leverage it you can just consider all those milliseconds you have nothing to do on the render thread, as free ones! Just use them to do something useful...

Rebalance the pipeline :D

p.s. Option 1 is bad, option 2 is always better.

Thank you very much for your reply. The fact you can't say more is enough for me!





My code uses another solution, I never read about it in papers or presentations.

When I tried it for the first time I thought it was crazy but it works well for me: no locks, no synch points, clean, elegant and no wasted cycles or waiting threads.

Maybe my solution and yours are similar, who knows? ;)

Thank you again, I'm a long time lurker and I love your blog!

i m using ogre for creating games :) so far so good

Joe: Have you or are you using Nebula3? I'm trying to find users that may have some experience with it as I agree it does look like one of better engines

Post a Comment