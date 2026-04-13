---
title: UE4 available to all
url: http://graphicrants.blogspot.com/2014/03/ue4-available-to-all.html
author: Brian Karis
published: '2014-03-29'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Unreal Engine 4 is now available to everyone for only $19/month + 5% royalties](https://www.unrealengine.com/).

There's been a lot said already about why this is cool, opinions, comparisons to competitors and so forth. From a business model point of view I feel it has been covered better than I could possibly say. If you are interested check out

[Mark Rein's post](http://www.gamasutra.com/view/news/213517/Epic_radically_changes_licensing_model_for_Unreal_Engine.php#comment234566)or

[hear it from the man himself Tim Sweeney](http://www.gamasutra.com/view/news/213647/Epics_Tim_Sweeney_lays_out_the_case_for_Unreal_Engine_4.php)for very compelling reasons why this is a good idea for us to provide and for developers to subscribe.

I wanted to give my own personal perspective as an engineer. What Epic just did is absolutely revolutionary and I am privileged to be part of it. I am super excited! Let me explain why.

If you've followed this blog for a while you may remember

[I gave Epic huge props for releasing UDK](http://graphicrants.blogspot.com/2009/11/udk.html)back in 2009. That was great for artists and designers, not that great for programmers. This is the next step down that path and its a doozy.

Now there have been naysayers that compare the numbers 19/month + 5%, is that better or worse, is it new or been done before, and so on. They are missing the point. It isn't the price, it isn't even the features. The revolution is this: for a 1/3 the cost of a new video game you can get access to the complete source code for our cutting edge game engine. The entire engine source code, every bit of it, the exact same we use in house and the same provided to private licensees, is available to you for only $19 (except for XB1 and PS4 code we aren't legally able to give you due to NDAs). This is the same tech that will be powering many of the top AAA games developed this generation. As Mark put it "Right now 7 of the top 21 (!) all-time highest rated Xbox 360 games (by Metacritic score) were powered by Unreal Engine 3" and you damn well better bet we are going to do the same or better this time around with UE4.

Now you may say John Carmack and id have open sourced their engines many times. That is true and I commend them for it. John has had a lasting impact on how many coders, myself included, write software due to these efforts. Unfortunately, the strict licensing terms have resulted in basically no commercial products using the id engines from that open source license. John has even lamented this recently "It is self-serving at this point, but looking back, I wish I could have released all the Id code under a more permissive license. GPL never did really do anything for game code, and I do wonder whether it was a fundamental cultural incompatibility. GPL was probably the best that could have flown politically for the code releases -- posterity without copy-paste into competition." And my own personal twist with this situation is after Zenimax bought id, their engines were no longer commercially licensable meaning anything built on top of that code base had to be scraped. GPL is simply not an option for commercial games.

There are other examples of open sourced game engines or cheaply priced engine source code but they all have something in common which is they were never up to date. The id engines were only open sourced years after the game that used them shipped. Id had already moved onto their next technology. For example the engine that powered Doom 3 wasn't opened sourced until 6 years after the game shipped. By that point Rage had even shipped. The reason for this is obvious. The point where releasing the code is non-threatening to execs is the point where a competitor can't use the code to their advantage. This means every single engine code base available to indie devs or students was either not commercially developed or purposely not competitive in its capabilities.

With the UE4 subscription, you can today get complete source that is totally up to date and will continue to be. This isn't any old engine, its the same cutting edge technology that will be powering many of the top AAA games of this generation. And as soon as we add new features you'll get them. In fact you'll even see the work in progress before they're done. How crazy is that?

Look, its easy to brush this off as the guy who works for Epic telling me I should give him money. That isn't why I'm writing this. What I am most excited about by far is in what I can share and give back the the gamedev community. That is the reason I have this blog, its the reason I have presented at conferences and will again in the future.

If you are a teacher, check out the license terms, they are ridiculously nice for schools. If you are a student, tell your school about it or grab a personal subscription.

For all those wanting to get into the game industry, the same response you will hear from everyone is make something. No one lands a game job because of their great grades or fancy degrees. They get it by making something cool. I wrote my own engine. That's how I landed my first job. Although I learned a ton if I were in that place today I would modify UE4. There is literally nothing else more applicable to a engine programming position than proving you can do the work. Hell, make something cool enough we'll hire you!

I can't wait to see what people make with this. It's a great time to be a programmer!

## 6 comments:

"GPL is simply not an option for commercial games." - as long as you don't target consoles and are ok to share your code, it's fine.


Also: I agree that this is an incredible move from Epic and I like the idea of engince licensees collaborating on Github.

However, one thing I don't like: AFAIK as a game developer you're not allowed to ship tools (level editor, ..) with your UE4 game, so every gamer who wants to create levels or whatever for your game would have to get the $19,99/month subscription as well, right?

I agree with you Brian. I think one of the most important aspects of this, beside of the potential to create new games/applications, is the fact that developers with no prior experience working on large commercial games get to see how things are done on a large scale. I think this fills up the huge gap there is between being a developer in a small scale product (or learning from gamedev.net and similar sites), and being a developer on a AAA title.

I wish you had done that before I put several full time months into upgrading Doom 3 (fully working Android support, cool renderer upgrades with my knowledge from XreaL, very flexible Lua GUI system and other stuff).








Binary blob solutions like the UDK or Unity 3D were a devastating experience for me because I'm primarily a programmer and there was a lot of stuff I couldn't fix without source access. Working with a black box just sucks.

With the very liberal and cheap UE4 license everything has changed and I'm grateful. This also allows to make a lot more potential revenues.

You really have a point about the GPL. The GPL was mainly only useful for people how to learn coding. The only successful but free projects derived by the Q3A release were total conversions where everything was already done.

There was only one commercial game with the Q3A engine: Space Traders.

In the end the primary function of the GPL code in the Quake 1-3 eras was that the community could maintain and port it to wherever it was needed. However there were always problems with the GPL like missing Punkbuster support or the general linking issue against non-GPL compatible libraries.

I like the UE4 tools. They have become alot better with the new Blueprint system and Epic removed really everything I had to critisize: Unrealscript, managing assets in control version system unfriendly upks, Flash for GUIs.

I hope that Epic keeps this way for the next 10 years or longer.

The biggest problem of the GPL engines wasn't that small developers could only ship for PC, it was that it prevented large commercial developers from kicking code back to it to keep it modern (i.e. as has happened to LLVM and Bullet).


I've long lamented the lack of options for new developers to tinker with the low-level internals of a modern game though, so this is definitely a nice thing to see happen.

Bullet physics is under the zlib license and LLVM is under the openBSD license, both of which are permissive for gamedev. They allow use without being forced to expose your own code. Even with limited GPL the lawyers don't want to touch it with a 10ft pole. Even if everyone in your studio is fine with it (rare) a publisher won't fund you.


MIT, BSD and zlib licensed open source code is commonly used in gamedev. In fact UE4 uses some code under these licenses (forget which).

The legal aspect of GPL isn't very scary, what's needed to stay compliant is well-known (to the point that V2 was heavily evaded). The unacceptable linking/platform limitations are the real problem, and are why the lawyers won't touch it, but we'd also need to have a very high-quality GPL game to test that theory and I don't think that will ever happen.


My point though was that even if a small developer was okay with the GPL limitations, one of the main advantage of open source is supposed to be community contribution, and the GPL license guaranteed that commercial developers wouldn't be interested and in turn contributing.

Post a Comment