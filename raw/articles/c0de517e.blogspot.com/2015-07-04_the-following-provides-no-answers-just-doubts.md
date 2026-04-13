---
title: The following provides no answers, just doubts.
url: http://c0de517e.blogspot.com/2015/07/the-following-provides-no-answers-just.html
published: '2015-07-04'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Technical debt, software rot, programming practices, sharing and reuse etcetera. Many words have been written on software engineering, just today I was reading a blog post which triggered this one.

Software does tend to become impervious to change and harder to understand as it ages and increases in complexity, that much is universally agreed on, and in general it's understood that malleability is one key measure of code and practices that improve or retain it are often sensible.

But when does code stop to be an asset and starts being a liability? For example when should we invest on a rewrite?

Most people seem to be divided in camps on these topics, at least in my experience I’ve often seen arguments and entire teams even run on one conviction or another, either aggressively throwing away code to maintain quality or never allowing rewrites to capitalize on investments made in debugging, optimization and so on.

Smarter people might tell you that different decisions are adeguate for different situations. Not all code needs to be malleable, as we stratify certain layers become more complex but also require less change, new layers are the ones that we actively iterate upon and need more speed.

Certainly this position has lots of merit, and it can be extended to the full production stack I’d say, including the tools we use, the operating systems we use and such things.

Such position just makes our evaluation more nuanced and reasonable, but it doesn’t really answer many questions. What is the acceptable level of stiffness in a given codebase? Is there a measure, who do we ask? It might be tempting just to look at the rate of change, where do we usually put more effort, but most of these things are exposed to a number of biases.

For example I usually tend to use certain systems and avoid others based on what makes my life easier when solving a problem. That doesn’t mean that I use the best systems for a given problem, that I wouldn’t like to try different solutions and that these wouldn’t be better for the end product.

Simply though, as I know they would take more effort I might think they are not worth pursuing. An observer, looking at this workflow would infer that the systems I don’t use don’t need much flexibility, but on the contrary I might not be using them exactly because they are too inflexible.

In time, with experience, I’ve started to believe that all these questions are hard for a reason, they fundamentally involve people.

As an engineer, or rather a scientist, one grows with the ideal of simple formula to explain complex phenomena, but people behaviour still seems to elude such simplifications.

Like cheap management books (are there any other?) you might get certain simple list of rules that do make a lot of sense, but are really just arbitrary rules that happened to work for someone (in the best case, very specific tools, worst just crap that seems reasonable enough but has no basis), they gain momentum until people realize they don’t really work that well and someone else comes up with a different, but equally arbitrary set of new rules and best practices.

Never they are backed by real, scientific data.

Never they are backed by real, scientific data.

In reality your people matters more than any rule, the practices of a given successful team don’t transfer to other teams, often I’ve seen different teams making even similar products successfully, using radically different methodologies, and viceversa teams using the same methodologies in the same company managing to achieve radically different results.

Catering to a given team culture is fundamental, what works for a relatively small team of seniors won’t apply to a team for example with much higher turnover of junior engineers.

Failure often comes from people who grew in given environments with given methodologies adapted to the culture of a certain team, and as that was successful once try to apply the same to other contexts where they are not appropriate.

In many ways it’s interesting, working with people encourages

__real immersion into an environment and reasoning, observing and experimenting__what specific problems and specific solutions one can find, rather than trying to apply a rulebook.
In some others I still believe it’s impossibile to shut that nagging feeling that we should be more scientific, that if medicine manages to work with best practices based on statistics so can any other field. I've never seen so far big attempts at making software development a science, deployed in a production environment.


Maybe I'm wrong and there is an universal best way of working, for everyone. Maybe certain things that are considered universal today, really aren't. It wouldn't be surprising as these kinds of paradigm seem to happen in the history of other scientific fields.



Maybe I'm wrong and there is an universal best way of working, for everyone. Maybe certain things that are considered universal today, really aren't. It wouldn't be surprising as these kinds of paradigm seem to happen in the history of other scientific fields.

Interestingly we often fill questionaries to gather subjective opinions about many things, from meeting to overall job satisfaction, but never (in my experience) on code we write or the way we make it, time spent where, bugs found where and so on...

I find amusing to observe how code and computer science is used to create marvels of technological progress, incredible products and tools that improve people’s lives, and that are scientifically designed to do so, yet often the way these are made is quite arbitrary, messy and unproductive.

And that also means that more often than not we use and appreciate certain tools we use to make our products but we can’t dare to think how they really work internally, or how they were made, because if we knew or focused on that, we would be quite horrified.




*P.S.*
## 7 comments:

Thank you for writing this article I completely agree. A not so crapy management book which takes a 'scientific methodology' is Creativity, inc from Ed Catmull. It might give you some light in the challenging subjects you mention..

Yes, I bought that at Siggraph and I'm reading it, it's a good book indeed.

Malleability is an interesting lens to look at programming. It seems that one way people (and teams) can differ greatly is agreeing how exactly to make code malleable.

There's the generalists, who think keeping code malleable means writing everything as general as possible, such that it is ready for all possible future uses and requirements. Their code gets stuck not because it's not general enough, but simply by the cost of the extra complexity of generality, and predicting the future wrongly. When they fail, instead of understanding that you can't predict the future, they conclude that next time they must be even more general to avoid the same fate.

Then there's the YAGNI/OAOO/continous refactoring people, that think malleability simply is implied by the process of refactoring. Their downfall is often is that while continuous refactoring is simple in theory, it is super labor intensive in practice, and being lazy with it makes quality (and malleability) plummet.

Like you say, teams can be successful with widely differing strategies. Generalists occasionally get lucky predicting the future, and refactoring aficionados occasionally have the right team and the right amount of time to get it done.

The biggest hell is being on a team consisting of two halves of each, which pretty much guarantees failure.

Like you say, some code (like e.g. the zlib library) doesn't need to be malleable. But the amount of software that falls in that category is so small compared to the amount that doesn't, that we might as well ignore it.

Wouter: I agree, that is a very interesting axis, probably the most important one, and it's chiefly influenced by the attitudes you describe.



I think it's not only dependent on the team (culture, seniority, size, turnover...) but also on the problem domain, of which I don't speak of because I mostly assume the specifics of a game/realtime rendering programming team, as that is what I'm most accustomed to. But there are many others, along the axes of predictability of requirements and ease of change, for example (e.g. a military software might be very well specified and almost impossible to change after deployment and so on)

It is interesting to think about these axes and design spaces, but the more you do the more you risk sounding, as I wrote, like a bad management book. Many things do make intuitive sense, but very few to none are actually proven in measurable data.

p.s. "generalists" carries already a meaning when applied to a programmers so I'd say "generalizers" instead.

I've been trying and failing to program/finish something for over 10 years and what stops me most is usually esoteric software configurations, so I opt for concise setups that just work. Yesterday I finally did the impossible in my preprocessor adventures (pastebin.com/JP4LYiD9) and this sentiment of "specify it once, make it crystal clear to read and figure out" is a pleasing hobby in and of itself (like gardening I expect). Now imagine cold, corporate gardening organizations - no warmth, no passion, but most logically - no actual coherent long term personal investment (a will to plan ahead and protect the weak and stave off corruption).




Clean, clear and concise, /nuanced/ code is just a necessity for my general standards for myself and what I end up doing. gwan.com is a nice read. I /do/ understand more than plenty programming concepts conceptually, but I don't like wasting time learning ins and outs (which add multiples of time for maintenance). Case in point STL. Case in point Unreal Engine 4, I just don't trust the software architects and they don't seem to listen. Breaking rules is fine or indeed necessary when it advances and improves - but never at the cost of more esoteric, unintuitive, inconsistent setups.

If programming will get more powerful and flexible and concise in the future, then surely there will be a far matured and more intelligent approach, to be able to get there. To completely and effectively lift the functionality of project A to B you need to know everything about both. The program loop unrolling is here - it's unprecedented in comparison to the level of sophistication of /use of/ the software we have today. We desperately need more software reduced to their bare minimum (like the compile time string hash on StackOverflow) which in themselves are a comforting mark of evolution and triumph.

The useful index is intelligence, not code malleability. Smart people can do truly anything within reason. Ultimately I know that you just don't get supremely well "problem unwrapped" codebases without being extremely smart. Most (hello UE4!) are the epitome of convoluted, with no starting intention of being repurposed. Still, in theory there's always much better to be had, even if it seems out of reach. We will get there. In the meantime.. there's C++.

Anon: I guess you're the same anon who ranted on the "sharing is caring", again I don't understand most of what you are saying. The pastebin you posted is not available. The link to gwan seems irrelevant. Again, I don't get what you're trying to say and how is it a relevant comment to what I posted.

Agreed, I'm also biased by game development, and my "wisdom" is 100% anecdotal. Seems that's all we have :)

Post a Comment