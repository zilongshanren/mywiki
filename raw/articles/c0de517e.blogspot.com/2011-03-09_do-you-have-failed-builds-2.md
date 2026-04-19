---
title: Do you have "failed builds"?
url: https://c0de517e.blogspot.com/2011/03/do-you-have-failed-builds.html
published: '2011-03-09'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Sometimes we are so used to our industy workflows that we "accept" things that are terribly wrong without questioning them anymore. It's like when some medias start broadcasting false facts, or misusing words, and slowly the wrong becomes right.

What does it mean that a "build failed"? An entire build fails, catastrophically? Not even a single source file compiled? Or maybe it's only a bit of the frontend that did not compile? Or a single art asset? It's like saying that a car does not work just because the air conditioning does not turn on.

Ban the "broken build" concept. Ban "game crashes". The audio system failed? Well I guess we have a build of the game without the audio. The rendering crashes? Well I guess we have to disable that (and maybe use a minimal "debug" version instead i.e. animation skeletons and collision meshes).

A game is a complex collection of components. Then why if just one component does not work, we consider the entire thing "bad"? Decouple, my friend!

## 11 comments:

hear hear!

A game is a complex collection of components. Then why if just one component does not work, we consider the entire thing "bad"?The decoupling obviously sounds nice, but it sounds tricky to jank out a failing component and hope the rest of the complex will be just fine. Your topic reminded me of this nice post and one of the takeaways: "it is preferable that the software call attention to the problem so that it can be fixed, rather than trying to muddle along in a bad state".

Obviously Eric is talking about exceptions instead of build failures, but I think it'd still apply. Is it safe to work off a build where one of the key components is temporarily in limbo?

Rim: It is very tricky if you didn't design your game into components that are optional. And I guess having a game without the front-end or audio will be "call attention" not to mention that you will still see the build of that component failing.



Of course if no one cares that a piece is failing for a long time it would be a problem, but that's not the point.

The point is that you should let the people that have to fix the problem be able to do their work without the need to stop everyone else...

I've yet to be on a team that invests enough in their automated testing and builds. Teams seems to consistently settle for the bare minimum in functionality e.g. a build is good or bad. I think this behavior means they miss allot of possible benefits.

The point is that you should let the people that have to fix the problem be able to do their work without the need to stop everyone else...My main worry would be that when everyone can continue working, they might be introducing new bugs that may only surface when the failing component is brought back online. My doom scenario is that you may introduce component-dependency-bugs:

"my code worked yesterday with the debug renderer and without audio, but today it's broken and I don't know why."Of course decoupling is everything and in general I agree with the merits of your idea. I'm just a worrying nitpick :)

Rim: having a better design does not mean that people should start to be morons and everything will work magically. Of course you still will have to be strict about fixing a broken component as soon as possible.


Component/dependency bugs would possibly emerge, as now the project has more than a single "all linked togheter" configuration. On the other hand these bugs are "healty" meaning that when discovered and fixed they actually fix design/coupling problems that otherwise you simply won't see (but they would still exist!).

Of course you still will have to be strict about fixing a broken component as soon as possible.I haven't had the benefit of working on a game with a large team, but shouldn't this kind of strictness ensure you don't check in broken failing builds in the first place?

Ah well, I'm probably doomsaying and as I said I agree in general to the whole decoupling idea, so I'll give it a rest. I can't help but smile grimly though at the thought of a poor lead explaining that

'these bugs are "healty"'coming up on a milestone :)Rim: Yes and no. Even in theory you can't always guarantee locally that a check-in won't break the build, you might for example need a bit more memory and that might be fine locally but conflict with some work done by someone else meanwhile.



Of course you could require people to check-in only if they are at "head" but that's really impractical as you would need to "lock" your source control while syncing head, merging and testing locally.

And then of course in practice people also make mistakes.

You are missing the concept here. Build failed is meant to alert you: "Hey shit is broken; stop blogging and fix it."






Maybe its not your shit that is broken. Maybe thats the complaint. But knowing that a part of the system is not compiling or something is missing, is important information.

Also, it seems that all the effort you would expend in trying to make the build failed message go away by decoupling, mocking what have you; would be better spent actually fixing the damn problem.

Thats the point of the message. Something is broken fix it.

Suppose we live in your perfect world where build failed doesn't happen on these conditions. Then wtf does it mean when the build passes? Does it mean you can do a clean checkout and run it? No.

So basically introducing your decoupling HACK makes build passed meaningless. Then you would have to build a brand no effing tool to check that the shit is truly built as opposed to happy land where build always passes.

I'm not sure about game engines (due to performance issues, they have modules which are tightly coupled) but on applications, the sort of thing you speak of is possible. Lookup for example JRebel.

Metaluim: JRebel is fairly cool but I won't say it's common. Lisp and Erlang also are great examples or runtime patching. In C/C++ though things are way more complex

Post a Comment