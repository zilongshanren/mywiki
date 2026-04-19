---
title: The pitfalls of experience
url: https://c0de517e.blogspot.com/2010/02/pitfalls-of-experience.html
published: '2010-02-05'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Ours is an industry that, even being very young, treasures experience. And it's not hard to understand why. An AAA game is a product that (hopefully) will be sold to millions of users, eager to find faults in your work.

Usually your project will run from one to three years, from the beginning to the final shipped version with deadlines that most often than not, simply can't slip. In those years, you're going to face all kinds of engineering problems, from writing complicated technologies that have to work in realtime, to resolving intricate software and hardware problems, to managing team dynamics. And everything has to be done under ever changing requirements and designs.

Usually your project will run from one to three years, from the beginning to the final shipped version with deadlines that most often than not, simply can't slip. In those years, you're going to face all kinds of engineering problems, from writing complicated technologies that have to work in realtime, to resolving intricate software and hardware problems, to managing team dynamics. And everything has to be done under ever changing requirements and designs.

If you add on top of that, that most of the times you're going to work in a framework that effectively discourages experimentation, with punishing iteration times and complicated, badly written legacy code that just works if you don't ever touch it, you will easily understand why expertise is such a valuable virtue.

You have one shot to accomplish anything. You have to do everything right, on time, on budget, and you have to compete in an aggressive worldwide market. Wonder why lately, games are more and more always the same? Why we tend to take no risks?

Experience works wonderfully in those conditions. Because most of the times you already know how to solve a given problem, you're an expert. And all the others, you can still see a reasonable solution. One you'll confident will work. You can quickly discard bad ideas, you understand if something is possible or not, and can estimate how much effort a given thing will take.

Experience is an effective noise filter, it filters out the average ideas other people usually have, and focus on the more productive and safe path. And it's exactly there, that things start going all wrong. You know that a given thing will work because you already made it work in the past, or because you worked on something similar, you can interpolate between things you've done and adapt them.

You make great things possible, but totally discard the impossible ones. The impossible ideas, or even the wrong ideas, the unreasonable ideas, are the ones that geniuses have. Are the innovations, the change. Ironically, all game companies will have those words in their mission. But few do really know what that implies, and how you can encourage change.

We've all seen impossible things being done. And then, when we were told the magic behind an idea, a technique, most of the times we see how trivial a given solution really is, if you dare to explore outside the limits of your experience.

We've all seen impossible things being done. And then, when we were told the magic behind an idea, a technique, most of the times we see how trivial a given solution really is, if you dare to explore outside the limits of your experience.

*"Alice laughed: "There's no use trying," she said; "one can't believe impossible things."*

"I daresay you haven't had much practice," said the Queen. "When I was younger, I always did it for half an hour a day. Why, sometimes I've believed as many as six impossible things before breakfast."

"I daresay you haven't had much practice," said the Queen. "When I was younger, I always did it for half an hour a day. Why, sometimes I've believed as many as six impossible things before breakfast."

This, from "Alice in wonderland", is a fundamental lesson for us to learn. The first time I realized its importance, was by looking at Crysis. One of the artists in my company used a tool (3dripper) to dump all the meshes, rendercalls and textures of a frame of the game. While looking at them, he found a texture that looked like ambient occlusion, but done dynamically, and showed it to us (programmers).

I didn't know how that was possible, and before seeing it, I would not even have tried to do such a thing. But after I knew it was possible, it took me just a few days to come up with a shader, that then I found was really, really close to what they did. It used the depth buffer, and it did raytracing on it by sampling in steps, using a routine I adapted from relief mapping. All it took was to know it was possible.



Experience is not something that can be avoided. And it's something that indeed is useful. But as you become more and more experienced, make sure to always keep your mind open to new possibilities.


Experiment. One good thing that helps, is always to be more curious than expert. Knowledge is noise, is made of ideas that you can mix together to create new things. Experience filters the noise. Keeping them at always in a good balance is fundamental.


Talk to outsiders. Make presentations, discuss with other people, juniors, artists, people that have a different view of the problem. Most of the times, their ideas won't directly help you, but they will shake your brain, force to have another look at the problem, give you that spark that can become a new solution.

I've found myself often having new ideas, or finding better solution, by just presenting the work I've done. Most of the time, it's not even the discussion that helps, I have new ideas while I write the presentation, or while I explain it, even before we start debating about it.

Experiment. One good thing that helps, is always to be more curious than expert. Knowledge is noise, is made of ideas that you can mix together to create new things. Experience filters the noise. Keeping them at always in a good balance is fundamental.

Talk to outsiders. Make presentations, discuss with other people, juniors, artists, people that have a different view of the problem. Most of the times, their ideas won't directly help you, but they will shake your brain, force to have another look at the problem, give you that spark that can become a new solution.

I've found myself often having new ideas, or finding better solution, by just presenting the work I've done. Most of the time, it's not even the discussion that helps, I have new ideas while I write the presentation, or while I explain it, even before we start debating about it.


## 11 comments:

Great entry! Experience could be evil at times. Sometimes I think it was easier for me when I was starting programming and simply hadn't the knowledge that something is impossible... now as you said I sometimes reject solutions just because there is too many suggestions it won't work.

Riddlemaster: and 99 times out of 100 you'll be right and more productive. But that one that we're missing, can be revolutionary.

I've been thinking about this a lot lately...




I feel that programming is about experimentation, about making mistakes and discovering new things. That it should be both fun and a learning experience.

However, I've discovered that in corporate environments many people are very conservative about programming techniques, languages, etc, and don't like to try new things.

That isn't to say they aren't good engineers, sometimes they are very good. However, I just feel like it misses the point of programming...

Nice post, very true.





I feel that a good programmer should treasure his or others experience but not be too attached to them.

Like when you have some old code that's just standing there. You have to be critical. But I understand too big companies, they are taking risks to complete project and having a too "creative" programmer can be dangerous and not useful.

That's why I enjoy the preproduction phase of a game. You can actually create something new. You have a few weeks or months to flesh out what will be your core design. The rest of the work... just grunt work, talking with people and waiting assets.

But after preproduction I think you can't wait for the genial idea. There are milestones and routine work.

Txkun: true. The big key to experimentation is iteration time though. If you manage to achieve via tools, good code, good processes, a very fast iteration time, you can keep the creative thinking going on till the end of the project, and you can truly be agile etc... So it really depends.

I wouldnt rush to say that users are eager to find problems. When I play a game, the less I want to hit is a bug. But with a bigger user base comes greater chance to find weird things you could not foreseen.

rogerdv: irony?

Hi, sorry if this is off-topic but I can't find an email for you.




A couple of your posts say you don't need scene graphs. I've searched a little for alternatives to scene graphs but there doesn't seem to be much information on that.

I am writing a scene graph but I'm interested in what would be better, I'd appreciate if you could expand on why you don't need a scene graph and what the alternatives are?

Thanks.

Rob: I've commented on that matter even on those original posts.









I guess you should ask yourself why are you using those scenegraphs in the first place.

For hierarchical transformations? That's stupid, very few animations require that, most objects are not animated anyway, so it's a waste of memory, cache, performaces to assume that they are.

And anyways animations are a matter for the game to manage, not the 3d engine (that should only care about skinning and so on).

So, what else? Maybe you want to use a scenegraph for culling. Could be, but are you sure the same graph-based culling applies to all your objects? I don't think that's wise either.

In general, I don't see why a 3d engine should care about the "object" abstraction at all. I think it should care about managing the graphics device, providing rendering services and utilities, managing multithreading, providing math and geometrical functions, providing reflection and serialization and memory management and so on.

The actual draw commands should be issued by some "renderable entities", managers of some given objects in the scene (i.e. "terrain" could be one of those, "players" another... the "players" one will probably care about animations, while the "terrain" will care more about culling, maybe you'll need something to take care of other concepts, like "lights" or "shadows" etc... each with ad-hoc, fast code...)

The scenegraph stuff comes handy in engines that pretend to be able to render anything you throw at them without specialized code. That sucks and those engines are not that general anyway (i.e. unrealengine or gamebryo etc... they're all making the same kind of games...). Anyway, even if for some weird reason you would need such "generality" I still would suggest that you'd be better served by creating a bunch of configurable rendering entities and have a sistem to specify that a given 3d source is to be loaded and rendered by a specific instance of one of those...

I guess I should ask you. Why do you need a scenegraph? Then after you tell me a reason to use it, I can prove it wrong :D

Thanks for explaining. Oddly enough, in making my renderer platform agnostic it turned out somewhat like the renderer you describe. It is data driven and currently fed by a scenegraph but it is not as ruthlessly efficient as my cycle-counter associates would like.


I'll have to think more about whether I want a scenegraph at all now. I had been kind of hoping its utility would become more apparent once I started to exercise the renderer with larger volumes of content.

Post a Comment