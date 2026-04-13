---
title: The character animation workflow for Awesomenauts
url: http://joostdevblog.blogspot.com/2013/03/the-character-animation-workflow-for.html
author: Joost van Dongen
published: '2013-03-09'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com). This is indeed a big and interesting topic, so today, I would like to discuss that in more detail!

I have previously shown how we make characters

[aim in all directions](http://joostdevblog.blogspot.nl/2012/08/making-2d-characters-aim-in-all.html)and

[shoot in all directions](http://joostdevblog.blogspot.nl/2012/09/shooting-animations-in-awesomenauts.html), but that did not explain the workflow and tools that our artists use to actually make those animations and put them in the game. Today's post will!

The core animation work for Awesomenauts is done in After Effects. This may come as a surprise to people who don't know the tool, since After Effects is mostly known as a video editing tool, but it is actually a great general animation tool.

It is also a big step up in comparison to

[Swords & Soldiers](http://www.swordsandsoldiers.com), which was animated in Flash. The biggest problem with Flash was that it only works well with vector-art. Our artists generally don't like working with vectors and would rather paint in Photoshop instead. This was especially a hot topic in our studio just after the release of Swords & Soldiers, because some commenters on the internet thought the stylised vector-art meant it was a small Flash-game that needed to be free. Flash is a great platform of course, but mostly known for small, simple games. Swords & Soldiers had way more content and polish than most Flash-games, so we felt insulted and wanted to make sure our next game had visuals that didn't remind anyone of Flash. This was an extra reason that we didn't want to use vector-art for Awesomenauts.

Another reason not to use Flash is that Flash is a rather basic animation tool. More advanced things just don't work as well as they do in After Effects. Looking for an alternative to Flash, we took a little detour around other tools before we found After Effects. We tried some things like Toonboom, but either the interface or the price were not to our liking. Then our former art intern

[Marlies Barends](http://www.worksofheart.nl/)demoed After Effects to us and to our surprise it was exactly what we were looking for.

After Effects is only one part of our total animation workflow, though. In the end, we combined Photoshop, After Effects and our own tools and exporters to create this pipeline:

![](../../assets/f3c834241cc9a700.jpg)

Note that although I was the architect of the technical parts of this pipeline, I did not actually write a lot of the code: that was mostly done by our programming interns Niels and Thijs. The art, of course, is all made by our great art team: Ralph, Olivier, Martijn and Gijs, and our more recent additions Koen and Tim. Especially Martijn came up with a lot of smart tricks to speed up the workflow in Photoshop and After Effects.

A particularly important choice here is how to make animations. There are roughly two approaches here. The traditional method is to animate frame-to-frame: the entire character is redrawn every frame. This creates extremely dynamic animation, but also costs an enormous amount of time. So we chose a different solution: the art is drawn in separate elements and these are animated by moving, rotating, scaling and deforming them. These transformations can be interpolated and thus it is possible to create a lot of frames in relatively little time.

After Effects is a great tool for this. Not just is animating basic transformation great there, but it also has tools to do skeletal animation (I believe with plugins, not sure) and, more interestingly, the so-called "Puppet Pins". Puppet Pins make it extremely easy to deform a shape, so that things like bulging muscles are easy and fast to animate. Puppet Pins are a simple concept, but also an extremely nice one, so if you never used them: be sure to give Puppet Pins a try!

Besides After Effects, the scheme mentions a lot of tools, exporters and converters. We made those ourselves and they come with a lot of features. I think they are a pretty impressive bunch, so I'd like to show this trailer of them again, which shows all of our editors in action:

The scheme above is a nice example of how complex game development really is. For an indie game, Awesomenauts is a very big production, but it is still small fries in comparison to the big AAA games like Uncharted and Killzone. Tons of development topics have many details to them, and making the wrong choices can cost so much time, that I can hardly even imagine the complexities of making something like the incredible new

[Killzone: Shadow Fall](http://www.youtube.com/watch?v=PDfu1mYQXEg)for PS4 (Dutch glory, woohoo!). Awesomenauts is small in comparison, but there are still many complex topics like this animation workflow. For example, I previously wrote a similar post about

[how we make level art for Awesomenauts](http://joostdevblog.blogspot.nl/2012/03/how-we-made-awesomenauts-level-art.html), and that big scheme didn't even include any info on the foregrounds and backgrounds!

Looking at the animation workflow scheme, you may have noticed that the small image at the top shows concept art for alternative designs for Genji, the new Awesomenauts character that we released recently. Especially the Space Marine Butterfly is so insane that I'd like to show these a bit bigger:

![](../../assets/7bfd33aac193f753.jpg)

[Click for high-res](http://www.proun-game.com/Oogst3D/BLOG/Awesomenauts%20Character%20Animation%20Pipeline%20Genji%20concept%20art%20high-res.jpg)

There are so many interesting details to all the parts of this workflow that I could talk about it forever, but I have to stop somewhere and I hope this blogpost gives a nice overview.

*Now, let me get back to the waiting queue for Simcity! I have been looking forward to a new Simcity for years, so looking at a screen that tells me it is going to try to start the game again in 20 minutes is incredibly exiting!*

TL:DR

ReplyDeleteOi a little bit of respect for someone putting work into this.!

DeleteThat is why you fail.

DeleteToo short, wanted more :P A really interesting read into how you make such amazingly animated characters. Thank you for taking the time to write it! :D

ReplyDeleteThis is really interesting!

ReplyDeleteI haven't found any other games companies that use After Effects for in game animations of anything.

Thanks for sharing :)

Very interesting! Thanks for the information. It really helps me as a student to learn about real company's workflow! I'm going to try out After Effects for animating a 3D car, Ill look around for doing some 2D animations as well!

ReplyDeleteFor 3D, After Effects is known to be extremely basic. If you want to do 3D animation, you are better of using something like 3dsmax, Maya or Blender.

DeleteThis is some very interesting stuff. Thank you for sharing! It's nice to know what makes this awesome game be what it is.

ReplyDeleteVery nice explanation and actually nothing too surprising. Although, are there some major benefits from baking the animations to sprite-sheets?

ReplyDeleteWell, we need to render out the frames to textures in some way. The benefit of using a sprite sheet is that it is one file instead of 200 separate files per character. This also helps a lot because we stream character textures in and out depending on who is in the match, so we only need to stream in 1 texture instead of 200.

DeleteI see. Didn't realise there were that many seperate pieces on a character. Thanks for the answer.

DeleteAmazing! Honestly I had no idea that you could use after effects for feats like this.


ReplyDeleteIn other topic, which language did you use to make your in-house editor? It looks pretty nice!

Most editors are in-game and thus written in C++, since they are part of the game project. The AI editor is external and is also C++. The Settings editor is also external and is C#.

DeleteWOW this has got to be the best editor ive ever seen. However if you can edit that fast why not make new maps.

ReplyDeleteI mean theirs only 3. Minus the balanceing plus animation artwork you should be albe to build maps quit quickly. I expect many new things to come and im not rushing anybody im just saying instead of balancing try to focus on variaty. yours truly Roman!!!

Since the tools are so fast, that part is indeed not a lot of work. But tweaking a level until it is really fun and has some unique twist still takes a lot of time and playtesting. Also, AI paths and triggers need to be added, and the graphics need to be made. The graphics are the most work, just like at how much handwork there is in the scheme in this post: http://joostdevblog.blogspot.nl/2012/03/how-we-made-awesomenauts-level-art.html


DeleteIn general, in games, making SOMETHING is pretty quick, but making something GOOD is an enormous amount of work.

Amazing! :O

ReplyDeleteWow Joost, this is truly amazing. Makes me look up to you guys even more!

ReplyDeleteThis is an Awesome editor. I've never seen such a complex editor before. When the AI editor appeared, I was simply mindblown.

ReplyDeleteGood job!

I wonder if After Effects allows some internal scripting so instead of producing large sprite sheets it could be possible to export only images of separate limbs with transforms for each animation. This is what we actually do with Flash. However we are not satisfied with Flash: it's slow, crashes to often, etc. So we are thinking of migrating to a more professional tool. May give After Effects a try after this blog post :) BTW, did you consider Maya as well?

ReplyDeleteExporting limbs separately would definitely be possible. Scripting in After Effects is pretty nice and we have several of our own scripts running on Adobe projects already.






DeleteHowever, I really wouldn't want to do that:

-It would reduce texture space, but would greatly increase the number of objects I am rendering each frame. In general, my performance problems are usually in the number of render calls and the fillrate. Splitting characters into overlapping pieces that are animated separately would be pretty bad for that.

-Our artists use a pretty complex feature set from After Effects that I wouldn't want to replicate in code. Just deforming parts is easy enough. It gets a little bit more complicated but still doable because parts are sometimes swapped mid-animation for frame-to-frame like animation. It gets really complex when we get to puppet pins, though. Deformation like that is more complex than what standard bones can achieve and having a real-time implementation of that would cost me a lot more performance and an immense amount of work to get exactly the same as in After Effects.

-Our artists generate an outline around the entire character in After Effects. This outline is not around the individual parts, but around the whole, so doing that in real-time would require quite a complex post-process or rendering characters to a rendertexture first, something like that. Doable, but again, a lot of work to implement and eats a lot of real-time performance.

-As for Maya: I am a 3dsmax person, so I considered that, but 3D engines just don't have a very smooth workflow when you try to do 2D art in them. After Effects is great and 2D and is thus way better for that in every way.

Thanks a lot for the detailed answer!



DeleteWe are targeting mobile platforms and for this reason video memory budgets are quite low. We simply had no choice but to use the approach I described above. We have no problems with the amount of render calls (it's basically the same as in your approach since the render state doesn't change between limbs). As for fillrate, it is probably an issue however not so serious as in parallax backgrounds...

BTW, could you please share how you are planning your video memory budget?

We don't plan video memory all that early: we first start making the first assets and gameplay to see what the game is actually going to look and play like. Once we have a bunch of 'final' art, I analyse what is there and how that is going to multiply for the final game, to see whether there are going to be any problems.



DeleteHowever, in practice we basically just plan very little and fix whatever problems arise, which is a lot easier on console/PC than on mobile: there is just a lot of video memory. In Awesomenauts we used too much for PS3, so at some point I had our artists optimise their art and they optimised away 50mb in just a week! I also added texture streaming on character textures to reduce what is in memory at any given moment, and by that point texture usage was good enough for release.

So not too much planning, not like what I imagine you must be doing on mobile to make it fit. How DO you plan that?

Well, currently we are using a very simple rule since we are still targeting devices from the "iPhone 3GS" era and since mobile devices use unified memory architecture: stay below 90 mb for all memory allocations. Textures may take up to 75%, 15% - audio, 10% - gameplay structures.

DeleteThis comment has been removed by the author.

ReplyDelete