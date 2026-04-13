---
title: Advice for a game engine newcomer
url: http://gameenginebook.blogspot.com/2012/01/advice-for-game-engine-newcomer.html
author: Jqgregory
published: '2012-01-05'
source_blog: Game Engine Architecture
source_site: http://gameenginebook.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Selected email conversations, errata and announcements regarding "Game Engine Architecture" by Jason Gregory

Thursday, January 5, 2012

Advice for a game engine newcomer

From: Mike Breske

Hi Jason,

I am currently working as a consultant, doing a lot of work with ASP.NET web applications and business applications built with .NET C#. I'm a relatively new college graduate (applied mathematics degree), and I'm quickly learning that my passions lie outside the world business related applications. I love developing solutions using computer science and mathematics, but the domain isn't right for me.

A friend of mine shares similar sentiments, and we're both looking to work our way into the gaming industry (how many times have you heard that line?). It's my understanding that is not an easy task, as experience is the key. Our plan is to do what we can outside of work and start building games, as bad as they may turn out at first. We want as much experience as possible with the various aspects of the game development process.

To that end, we want to build our own engine. I plan on purchasing your Game Engine Architecturetextbook as a core resource. Do you think building a very basic engine from the ground up, then a game using that engine, is a reasonable task for a team of two guys to handle? Do you recommend a different approach or have any other advice? I obviously don't expect you to take a keen interest in my career or anything, but it's nice to be able to solicit guidance from someone who's in a place you want to be.

I saw that you worked on the Uncharted series and I had to see if I could get in contact with you, even for some small tidbits of knowledge. Uncharted 2 changed how I view what's possible in a game, the production value was incredible. I have some serious respect for the team that put that game together.

Thank you for your time!

Mike Breske

________________________

Hi Mike,

An insightful analysis! You are quite right that breaking into the game industry requires some significant effort. And the best way to prepare for entry into the industry is to develop some game software on your own.

That said, embarking on building a game engine from the ground up is a monumental task, and may not serve your immediate purposes. I would recommend instead that you get a hold of a pre-existing engine (e.g. Unreal, Half Life Source, Cryengine, Microsoft XNA, etc.) and "mod" it to make a game. That will give you exposure to a full-fledged engine, and allow you to build something that you can show off, in much less time than it would take to build an engine and then build a game. (Companies with 50 engineers have tried this and failed, so 2 engineers will probably find it a little tricky to pull off!) And building an engine without having seen one is a bit like trying to invent a new automobile without first learning how to change the oil on your existing car.

That said, I do suggest you read my book, as another way to get the "big picture" of how a game engine typically works. That combined with some experience with an existing engine should give you a solid foundation and put you ahead of your peers. Then if you have a demo or two, you should be golden.

You needn't make a full game, by the way. Try to figure out your passion, and make a demo to explore that. You might want to demonstrate your abilities at level design -- in which case you could make a couple of way-cool multiplayer arenas. Or you might want to explore 3D graphics -- in which case you might try using Ogre3D, or raw OpenGL or DirectX, to create a rendering demo with shadows, spherical harmonics, subsurface scattering -- or whatever technology seems interesting. The list goes on. Your demo doesn't have to be huge, either. It can be small and focused, as long as it demonstrates the ability to take on a non-trivial task, solve some difficult problems, and see it through to completion. That's what most employers are looking for -- someone who can not only start the job, but finish it and do it well.

Also, I can't stress enough the importance of practicing your 3D vector math. Knowing how to think in two and three dimensions, working equations in terms of vector notation (rather than always breaking things into x,y,z components), intuitively understanding that a dot product represents a projection, being comfortable with matrices as transformations of either points and vectors or (the inverse) coordinate axes -- these are also things game employers look for. Naughty Dog tests 3D math first, and if you fail that they don't even ask you about your software engineering skills.

Best of luck! Please keep me posted on how things go.

This is an interesting post, I'm in a (somewhat) similar position myself. I've been in the industry for a couple of years working mainly with Unity, so I don't terribly often have to do anything 3D math related (other than just moving stuff around and rotating it). I'm not 100% of whether I want to be an engine programmer, gameplay programmer, network programmer, etc, I enjoy all of those things! What kind of things could I do to make sure I keep my 3D math sharp?

You're welcome guys. Re keeping your 3D math sharp, the best way is to try to solve real problems within whatever game project you're working on. Whether it's determining whether an aircraft has passed through a "trigger region", or calculating the closest entry point into an animation, or figuring out which game object is intersected by a ray from the camera (for object selection) -- 3D math pops up everywhere. Put it another way -- if 3D math ISN'T popping up everywhere, then you're probably leaning too hard on what your game engine can *already* do, rather than pushing it to do new things. That said, I'll try to include some typical 3D math problems in the 2nd ed of my book (which I will be starting work on soon). Cheers, J

This is an interesting post, I'm in a (somewhat) similar position myself. I've been in the industry for a couple of years working mainly with Unity, so I don't terribly often have to do anything 3D math related (other than just moving stuff around and rotating it). I'm not 100% of whether I want to be an engine programmer, gameplay programmer, network programmer, etc, I enjoy all of those things! What kind of things could I do to make sure I keep my 3D math sharp?


ReplyDeleteCheers v much, and the book is fantastic

J

You're welcome guys. Re keeping your 3D math sharp, the best way is to try to solve real problems within whatever game project you're working on. Whether it's determining whether an aircraft has passed through a "trigger region", or calculating the closest entry point into an animation, or figuring out which game object is intersected by a ray from the camera (for object selection) -- 3D math pops up everywhere. Put it another way -- if 3D math ISN'T popping up everywhere, then you're probably leaning too hard on what your game engine can *already* do, rather than pushing it to do new things. That said, I'll try to include some typical 3D math problems in the 2nd ed of my book (which I will be starting work on soon). Cheers, J

ReplyDelete