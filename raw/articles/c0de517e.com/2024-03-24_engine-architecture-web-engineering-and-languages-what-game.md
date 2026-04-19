---
title: Engine Architecture, Web Engineering and Languages.What game devs (and programming
  languages!) should learn from the web.
url: https://c0de517e.com/013_web.htm
author: Angelo Pesce
published: '2024-03-24'
source_blog: 'c0de517e''s weblore: Main Entrance.'
source_site: https://c0de517e.com/
category: graphics
fetched: '2026-04-19'
---

[PSA: We announced the 2024 edition of the Rendering Engine Architecture Conference](enginearchitecture.org).

No, this is not an article about how to code with LLMs nor how to best use StackOverflow...

**Why the hate?**
Most "hardcore" systems (low-level, C++...) programmers balk at web anything. Every other week someone in my social network posts a screenshot of the Windows task manager proving how bloated web runtimes are, lamenting the emergence of Electron for desktop apps, the insanity of JSON serialization (or worse, XML!), the overheads of automatic memory management or interpreted/JIT languages, how wasteful everything is and once upon a time we fit the entire <computer, os, game, app> in <anywhere from a few K to a few Mb>.

Of course, in this atmosphere, it would be silly for someone to suggest that there is anything at all to be learned from our cousins in web development...

![](../../assets/b7325905f539b0a3.png)

Now, on one hand, I understand this, I can empathize. The art of programming close to the machine is disappearing. Kids these days... And it's not simply that nobody programs in assembly anymore, it's the silliness of divorcing programming from the craft of processing data. Of having built entire engineering practices, languages, systems, that created an unmanageable amount of complexity for no good reason.

And then to add insult to injury, layering on top more tools in the foolish errand of trying to solve complexity with complexity.

The web is bizarre. Computing starts from room-sized machines, then terminals and time-sharing to optimize their use. These then become networks, and an explosion of amazing ideas from iconic graybeards. Unix, Plan 9 and Inferno, Gopher and Usenet, X11... I don't need to list it all, the point is, we created the cyberspace, we had it all, systems designed with the network as their core...

Then the personal computer revolution happens, for good reasons, computers become pervasive, intermingled with humanity, every second of every life... and somehow, we "lose" it all. PCs don't start as part of the grand design of the net, and they won't join it for a decade or more. When they do, it's already late, we have clients, the web (HTML), and no real design. By the time the network becomes pervasive again (always connected devices, "the cloud") it's a mess. An organic abomination at each level of the "stack": hardware, OSes, languages, libraries, environments all the way to servers, protocols, and so on.

The average big user-facing computing thing (program, website, game...) is a monster so big that nobody understands it end-to-end. It takes two thousand people to make Candy-Crush, it took a handful to make Doom.

I know all this. I can empathize.

At the same time, the lamentations are entirely silly, and to show this, I'll have to state...

**The obvious.**
First of all, obviously, it's not that "the web" is made by morons, and gamedev is where "chad" elite-level programming lives. For how much I like the idea that rendering people (like me...) are Gods among humans, this clearly can't be true (only some of us are... ;).

Any human activity can reach the limits of human ability. There isn't something that is inherently harder than something else, everything is as hard as we are willing to push it. And that willingness depends entirely on the value it has in a society.

An easy example is sports. If you track the progress in any popular sport, you can see decade after decade the performance in the field improving. Soccer world champions of the sixties would likely be wiped out by a second-rate team in a B-level league today. Why? Is it that the human ability to kick a ball evolved in such a short time? No. It's the number of people playing the game, the selective pressure, the money in the sport, the facilities, tactics, strategies, training regimes, science, and so on.

Something

[can peak](https://c0de517e.com/012_peak_tech.htm), certain arts can be lost, but only because the attention and the market shifted.

The second thing to observe is that many of the issues I listed before, the perils of needless complexity, the mindless adoption of tools and techniques without good reason, the cargo-cult mentality, and hype cycles that often lead to these outcomes, well, these are universal problems.

We have them in gamedev, we always did, any experienced programmer lived through them, and is likely responsible for a few or many such mistakes themselves.

I can rant about contemporary C++, but let's not even go there. We do remember when people cargo-cult'd Design Patterns, right? When every single gamedev company used them in their hiring interviews? We do remember XML? Does Collada ring a bell? The abuse of OO? Shared pointers! CMake & friends! Games embedding entire web engines for their UI. Flash and ActionScript...

The scale changes, yes. And on average, gamedev is closer to the hardware, sure, it is more mindful of it. But not because we fundamentally are better, simply because the nature of our product demands it!

Of course I know how a GPU works at a level decently close to the actual silicon, and I don't know much of say, security or consensus algorithms or data integrity...

Enough with the obvious, let's see what we can learn now.

**#1: Embrace the "crap".**
Understand that great engineering is purposeful, it does not exist in the void.

If your code is "perfect" (if there could be even a singular definition for that), it's a finely honed piece of art, then its purpose must be the code itself.

It might be a piece of art, it might be something written for education, it might be made as a hobby, to bring enjoyment to the creator, but it has to have no other master than itself.

Beauty in the void, a relatively simple thing to achieve. If you have no users, crafting beauty is not as hard as some think it is. If "ideas are cheap", code, per se, is not that much more expensive.

Any code written for a product is beholden to the product's needs, and that inevitably makes it ugly. Code that is designed to be sold as such, where the code quality itself is a key part of the product is already crap. Middleware can be amazing, but it already shows the compromises of serving an ulterior motive: it needs to be optimized for many use cases, it needs to consider what to do not to break important licensees, the more successful it is, the more it grows complexity, the less optimal it becomes.

So, everything is crap? Nothing can be ever good? Of course not! The art of engineering is managing the success of a product, crafting technology that is maximally useful to its purpose, keeping it ahead of the competition in the areas that differentiate it, and balancing the mountain of short-term needs (production pressure) with the long-term survival of the codebase.

I can guarantee you that any big, successful, storied piece of code, has tons of "crap" in it. It is wasteful in myriads of ways.

Good engineering is when the crap is managed in such ways that does not show in the end product, in the moment, and over time. Great engineering is when "crap" (overhead, tech debt even) is leveraged, making computers sweat in order to ship better end products.

**Example.** I hate, and will never buy another Razer device, because it forces hundreds of megabytes of "driver" crap that is strictly malware, it provides negative value to me, it crashes, it spies etc.

At the same time, I ended up loving v.s. code and python, two things that are incredibly "wasteful" as they could do what they do in orders of magnitude fewer resources, but leverage that "waste" to facilitate people writing plugins, packages, and things that matter a lot of the respective products.

This is not even news! How many games in the eighties were made on top of VMs? Of scripting languages? Because code size (memory), and ease of portability were more important than raw performance, in the era of 64k computers, "bare metal" and no standardization?

And you can see good and bad engineering in gaming, all the time. There are franchises that ship year after year (or maintain GaaS platforms) for decades and each title/update works. Are they full of crap? Surely, but they are also well-engineered.

And on the other hand, you can see when the crap is in the "wrong" places, titles that ship and don't work, sales are impacted by technological choices, innovation stalling, and so on.

The

["but, can it run Crysis?"](https://knowyourmeme.com/memes/but-can-it-run-crysis) meme is what you never want to see as an engineer! You want

[r/itRunsDoom](https://www.reddit.com/r/itrunsdoom/), right?

**#2: Most Computer-Science is Scale-Agnostic.**
This is a powerful thing to notice, I find. Especially if one has some interest in computing history, it becomes easy to see patterns.

Algorithms designed when bottlenecks were around storage and retrieval of data from tapes are applicable today to hardware caches on mindbogglingly fast CPUs. Scheduling ideas in big-data Hadoop (map/reduce) clusters resemble patterns of highly efficient computation in GPUs. Plan 9 design describes, at a different scale, the ideas around the microservice architecture of today's web and so on...

And this isn't surprising, is it? Computation is local, it happens on "nearby" data. For data to grow, it has to become remote, and a price has to be paid to manage it. Independent computation can be carried out in parallel, dependencies introduce synchronization penalties. Computation speed grows faster than data speed.

Most rules around computing hardware are or at least have been, universal. Almost as solid as the immutable mathematics of logic, complexity, and computability.

My first computer, the Commodore 64, was "64" as in 64k. Memory was king, the CPU did not have caches and hardly even registers. RAM was faster than the CPU! Basic made sense not simply because PCs needed to be end-user programmable, but because it was compact (and interpreting costs are relatively low without pipelines and predictors).

And yet, even there, if you look at different scales - not how to optimize code on a single chip (today) but across chips - the same patterns emerge. And minicomputers a decade before the '64 already had "modern" caches and pipelines... distributed across different physical boards!

Even looking at people with pen and paper before the advent of computing machines, we can see ideas of "data movement", pipelining, and parallelism!

**#3: Learning from other fields.**
So, if in #1 I argue that both talent, and crap, are everywhere, and in #2 I'm saying that computation is not "that different" across different scales, we can now hope to find something to learn from fields that at a glance, might look irrelevant to us.

To be honest though, in the case of web services, the analogies with a game engine are so close that should be obvious.

A decade ago or so, I was "jealous" of web services mostly in terms of modularity. I have always espoused the benefits of live coding, hot-reloading (patching) and very few engines work that way. Moreover, few engines are even structured to have well-separated concerns.

![](../../assets/1c899b0f943dd921.png)

Let's see if any of the following is familiar to you. The audio/ui/rendering/ai/etc... system is crashing? Doesn't compile? Nobody can work! Do you want to grab a new version of the engine? You have to have it all and recompile it all. How long does it take? Are your engineers waiting? Testing? What testing!

![https://xkcd.com/303/](../../assets/3539f08629072962.png)

https://xkcd.com/303/
Of course, for all of these kinds of concerns, the web is king! Why? Are they smarter than us? What did I write already? Obviously not!

But, different priorities and constraints... Services run on different machines - for redundancy and scalability, thus, they naturally have to separate and communicate through interfaces. You want your services to be always "live", so you need to think of testing and patching... No wonder there are lessons to be learned!

Do game engines have theories of API development? Do engineers debate them? Do you start on a whiteboard sketching how subsystems will be divided? All of this is the bread and butter (from what I can tell) of web (backend) development!

One must look past the XML... REST is simply the idea of immutable data structures - referential transparency enabling caching/memoization. SOAP? Let's call it actors!

What I did not foresee a decade or so ago was how much even in terms of runtime performance we will end up close enough to be able to exchange ideas. At the time, we were at the very beginning of the "free lunch is over", starting to move to multithreading and data-parallel jobs - so coordination, throughput versus latency deliberations, etc were not top of mind.

![](../../assets/99e5805fb84d53d4.png)

FWIW - I still think this is not going to be very relevant anytime soon. I think it still makes sense to architect an engine around the concept of a "frame", with a simulation thread that is a frame ahead, a rendering thread that consumes the previous frame (somehow creating a copy of the data), and both trying to saturate CPUs mostly via parallel-for. I don't believe we need yet to pay for the complexity and overhead of more generic systems that can schedule much more complex graphs of work, without frame boundaries and so on... But that doesn't mean that we are not trending that way and that web services are not "ahead" of us in that game!

It's funny because elite game devs think of themselves to be the masters of data layout and transformation, especially now that OOP is generally ridiculed (itself a very recent thing to enter the gamedev's collective consciousness) and data-oriented design is king.

But we are just looking at other industries at the wrong scale. Yes, python web services might be wasting a CPU, but look at the databases they manage. How to lay out data? What to duplicate/cache, what not to? What to sort, what to have dictionaries to index, when to split across tables, and incur the cost of an indirection? Isn't that the same game we play?

Big data? Hadoop,

[Spark](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf) et al are very GPU-like... only again, at a completely different scale. And whilst in games, memory/bandwidte and compute might make you not reach 60fps or so, for the web, each of these things (storage, egress, computation) is something you pay for!

Figuring out the hotspots, optimizing code and data and so on, all very similar, and similarly, there are parts that are good, parts that are wasteful, parts that are bottlenecks and ones that are not. But optimizing 10% on a big web service might mean millions of $ in savings, or millions of dollars in extra user retention - for example if latency is reduced. The incentives are quite different!

TD;DR: be open-minded.

**#4 / Appendix: Programming languages care about the wrong scale.**
I'm not entirely sure why or how this happened. Maybe it's because type systems encourage us to think about single instructions. Maybe it's because for a while we thought that code reuse, from functions to metaprogramming, was the goal of languages. Maybe it's that most language concepts were invented in the early days of computers, where complexity was not a top concern, team sizes were small, and getting time to access a computer was a limiting factor... One way or the other, most programming languages encourage thinking of data, code, and APIs, at entirely the wrong scale.

Other than Erlang (to some degree) in fact, I don't know of a language where you have first-order modules, with data and processing isolation. Not in terms of runtime and its dependencies, nor in terms of build-time and code structure.

Even the Actor model, which is similar to Erlang's processes, in theory was meant to be applied to primitive data, e.g. "everything is an Actor" the same as real OO was meant to be "everything is an Object" (Smalltalk, Ruby...).

To add insult to injury, nowadays it became popular for languages to come with their own package management ecosystems, again, privileging the idea of code reuse over code isolation, which is the only cure (imho) for complexity - tackling it with well defined runtime barriers. We don't think about the gigantic amount of code that is "under" an app, in an OS, right? Why? Runtime isolation!

IMHO, this "code reuse" priority is

**completely** misguided.