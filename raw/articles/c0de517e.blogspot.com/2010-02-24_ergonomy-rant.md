---
title: Ergonomy rant
url: http://c0de517e.blogspot.com/2010/02/ergonomy-rant.html
published: '2010-02-24'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I need more time. The more I gain experience in this industry, the more I realize, time is everything. Nothing else matters. Too often we are worried about adding bells and whistles, marketable features, things to put on the back of the box, and that are ultimately irrelevant.

Do you want to build the best 3d engine out there? Then forget about VSM, SSAO, DOF, SH, CSM, HDR and similar acronyms, none of those should be part of the features of it.

Learn from cameras (I feel like I made this analogy far too many times). What's the difference between a professional camera, and a prosumer or consumer digicam? Let's consider the

[Canon 7d](http://www.dpreview.com/reviews/canoneos7d/)as a consumer one, the[5d Mark II](http://www.dpreview.com/reviews/canoneos5dmarkii/)as a prosumer, and the[1D Mark IV](http://www.dpreview.com/reviews/canoneos1dmarkIV/)as the professional. The price difference between those is substantial. What would you expect to be the most striking difference between those? The image quality?Well if so, you would be wrong. In fact, for some uses, one could argue that the 7d even outperforms the other two. Even in the numbers, the 1D manages to be the one with the least megapixels across the three. Why the 1D is so expensive? Probably surprisingly, it's because it's fast. It can shoot 10 fps versus the 3.9 of the 5DMk2, and it flash syncs up to 1/300 of a second, versus the (nominal) 1/200 of the closest rival. It's a camera made for people that can't miss the shot, and that have to work fast, focus fast, and work with flashes against the sun. Photojournalists.

What's the main difference between the 5D and the 7D then? Well, to me the best feature of the 5D is its big viewfinder. Let's go even cheaper, the

[550D](http://www.dpreview.com/previews/CanonEOS550D/), that is the most recent breed of the cheapest digital reflex line Canon has. What's the big deal between that one, and its bigger brother? To me is that the more expensive one, has an extra dial on the back, it's faster and easier to change its settings. Ergonomy again.And so on really, you can go back and forth, compare cheap compacts with

[professional](http://www.hasselbladusa.com/products/v-system/503cw.aspx)[film](http://www.photoethnography.com/ClassicCameras/index-frameset.html?LeicaR6.html%7EmainFrame)[cameras](http://en.leica-camera.com/photography/m_system/mp/). It's not about the number of fancy features. It's about being able to do your job at the best. Quality, durability, ergonomy, speed.You need to be able to focus on your job. If you're able to iterate fast, if you have the right utilities and services in your framework, then your 3d engine can be as thin as being directly the native API. It doesn't really matter. You can observe that the faster you can change, tinker, experiment, write code, the less you even need anything else.

For example, it's surely handy to have a tool that gathers metrics and displays performance graphs, to be able to understand what's going wrong in your rendering. I love PIX. But would you need it less, if you could just change your rendering on the fly?

What about a debugger? It's a fundamental, fundamental tool, and in no way I'm saying we shouldn't leverage on all kinds of tools... But when you're coding in a scripting language, and you can change things while they're running... Well, then, does using prints to debug code look so horrible?

All that is true especially for the expert. The more experienced you are, the more you don't mind the learning curve. You don't need canned components and automatisms. You don't need babysitting.

A tourist snapping casual pictures may still find handy to have a camera that's capable of putting fancy frames on a sepia-toned image, recognize faces while focusing, and automatically firing the flash when it thinks its necessary. For a professional, being unable to tinker, and having all those useless buttons in the way of his creative thinking, is an hassle.

That said, it does not mean that engineering a compact, consumer digital camera is easy or should not be done. There's a market for that. And we have to cater that market too. Not many (successful) companies are made only by experts in code-crunching. And indeed, in many cases we code to make others work easier, not our own. That might be the right choice sometimes but we should always try to achieve that at no cost for the programmers.

I've already said this a thousands of times, but building a complex data driven tool to make a given workflow easier, while complicating the overall structure of your code, it's a bad choice. Having a thin, fast, robust, high quality infrastructure, with layers on top to ease the most common tasks, is far bettter.

## 9 comments:

I think part of the reason the Unreal Engine is so successful is that it offers 'Ergonomy' to artists (and to some extent designers). Most programmers hate the codebase but the artists love the fact that they can use the tools to create without having to keep going to a programmer to beg for some feature.



Despite all its flaws UE3 is data driven where it matters and caters to artists in a way that few other game-specific tools manage. As a programmer I'm often horrified about how inefficiently something is implemented but from the artists point of view they've been able to do something that would have required 3 weeks of escalating feature requests under a traditional game development pipeline.

Love my Canon XSi by the way, but have just recently discovered the difference a good lens makes. When will games technology mature to the point where I can make a living selling the equivalent of a Sigma 30mm f/1.4?

I ranted a similar rant to this just a while back.



http://callofcode.blogspot.com/2010/01/designing-things-very-carefully.html#comments

The longer I spend in games development, the more I think we should be spending our time refactoring rather than architecting.

Mattnewport: I agree. Unreal Engine is artist friendly, and it's robust and proven.




If the artists are the main users of the rendering, then it's a wise choice. Of course is limiting in some way, you won't create an Uncharted 2 out of it, but for games like Mass Effect is a wise choice.

Again, I would still like to have something that can cater both audiences. There are some engines out there that do that very well BTW.

Richard: Refactoring is the only choice. But here I'm not talking about how to achieve a given result, but what we should be building. It's not about engineering, it's about marketing.

Mattnewport: now, your lens analogy btw went over my head :D

Sorry, the lens analogy was a bit obscure :)



The point I was trying to make is that thanks to the standardization of camera technology (standardized Canon lens mounts) a market exists for a company like Sigma to sell high quality lenses that cater to a fairly niche market. You see a somewhat similar phenomenon with small companies (or even one man shops) selling specialized plugins for Photoshop or After Effects thanks to the standardization of the process of shooting photos or making movies.

I'd love to be able to do the equivalent of making plugins (or high quality lenses) for the games industry but the technology hasn't matured/settled to the point where it is really feasible.

Mattnewport: Ah! I understand...




But Sigma is not the best example, as they reverse engineer the Canon mount, and every new generation of cameras can and sometimes does, break Sigma lenses (they provide a firmaware update... but it's not that easy sometimes).

Sigma right now, is the same as rendering tech. You can make stuff like SpeedTreeRT or so, but then it's up to you to connect the thing to every rendering engine you want to support :)

It's not such a big hassle as it seems.

I love your comparisons to taking photos. I own 400D and only recently discovered it's too slow at times (just because I started to think about photography more seriously) even though image quality is more than often satisfactory.

I agree that engines like UE are the way to go (even though programmers are not the big fans of it). I work in a company in which a fully working 3D prototype was made in a few days in Unity. I was amazed by this... it's a real click & play (if you remember this funny piece of software) but much more powerful. I also remember working on Unigine which we, programmers hated at times and called it a black box, but for artists and designers working with it was very effective.

You are wrong, the prof camera is expected to have a better image quality though: its sensor is way larger, so less noise. Megapixels is a tool to fool consumers, like GHz was for CPUs.

asdf: Consider better what you write. I provided links to DPReview for the camera uninitiated to understand better.





You're missing the point. I never said that there is no quality difference, that would be stupid. I said it's not the MAIN difference.

...And actually the 5dMk2 has both more megapixels, and a bigger sensor than the three times more expensive 1D.

...And all three of them will deliver more or less the exact same quality, especially at low iso.

...And often, the low-end (300d 350d 400d etc) and the next level up (10d 20d 30d...) share exactly the same sensor.

Post a Comment