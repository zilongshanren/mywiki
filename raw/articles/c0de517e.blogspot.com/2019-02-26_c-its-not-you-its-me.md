---
title: C++, it’s not you. It’s me.
url: http://c0de517e.blogspot.com/2019/02/c-its-not-you-its-me.html
published: '2019-02-26'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**How I learned not to worry and tolerate C++**

If you follow the twitter-verse (ok, and you happen to be in the same small circle of grumpy gamedevs that forms my bubble) you might have noticed lately a rise of rage and sarcasm against C++ and the direction it's taking.

I don't want to post all the relevant bits, but the crux of the issue, for the lucky among you who don't do social media, is the growing disconnect between people woking on big, complex, performance-sensitive and often monolithic and legacy-ridden codebases that we find in game development, and the ideas of "modernity” of the C++ standard community.

Our use-case is perhaps peculiar. We maintain large codebases, with large teams, but we never did great at modularization. This is our fault, and I’m not sure why it happened. Maybe it’s a combination of factors, including certain platforms and compilers not working well with dynamic libraries, or performance concerns. But most likely, it’s also the product of a creative environment where experimentation is a necessity, planning is inherently hard and architecture work is often simply neglected due to other production pressures.

**The (AAA) gamedev use-case**

Whatever are the historical reasons, the reality is that we live in an environment where most often than not:

- We don’t care about the STL, not its performance improvements. We developed our own bespoke containers, both because we need very ad-hoc algorithms tuned to specific problem sizes, and because of design issues of the STL itself which made it impossible to use (e.g. its historical reluctance to play well with things like memory alignment).
- We do care about all declinations of “performance”. Not only the final, all-optimizations enabled, code generation, but also performance in debug builds, and compiler performance. Iteration times.
- We care about being able to reason about code. Simplicity, not counted as lines of code, but as the ability to clearly understand what a line of code does. We often would prefer verbose, even in the eyes of some more arcane code, to unpredictable code, where to understand the relation between what we wrote and what happens requires a lot of context, of “global” information.

Given this scenario, it should be clear to see how most of the C++ additions since C++11 have gone in the “wrong” direction. They are typically not adding any expressive power for our use-cases, but instead, bring lots of complexity to an already almost impossible-to-master language. Complexity that also “trickles” down to tooling, compilers, compile times, debuggers and so on.

It’s hard to overstate how bad this chasm is growing, with some direction being truly infuriating, but let me just bring a concrete example. Take the modernization of STL containers, say r-value references, initializer lists and all the ecosystem around that. Clearly, a huge feature for C++, allowing even significant savings for certain uses of the STL. And what you would call “a zero cost abstraction” - if you don’t use it, you don’t see it. Everyone’s happy, right?

Quite the contrary! The prime example of something that is entirely useless for people who already know about the cost of constructors, temporaries and the like, designed their code thinking of how to layout and transform bits, instead of higher level concepts sketched in a UML diagram.

Useless but dangerous, as these concepts increased the complexity of the language exponentially, to the point that very few can really claim to understand all their nuances, and yet are still hard to entirely avoid in projects made by lots of people, and where you do not necessarily even have the control of all the code due to external libraries.

And when all this humongous effort is taken on one side, features that would truly help performance sensitive large “system” programming, are still completely ignored. C++ still doesn’t have a “restrict” keyword. Strict aliasing is incredibly troublesome and even getting worse with certain proposals. Threads and memory alignment were implemented first (and arguably better) in the good old C.

We still don’t have vector types, not to mention fancier features like the ability of “transposing” the memory layout of arrays of structures (into SOAs or AOSOA and so on). We don’t have anything to help tooling, or compile times, like standardized reflection, serialization or proper modules. And we keep adding metaprogramming (templates) features before tacking complexity and usability issues (e.g. concepts, that now are scheduled to be in C++20).

**What’s C++ anyway?**

I think part of the disconnect, and even anger in the community, is due to a misinterpretation of what C++ is and always has been.

There is this myth that C++ is a low-level, high-performance/system programming language. It’s false, and it has always been false.

Clearly, a language that didn’t bother until recently to implement threads, is not a language for high-performance anything. There is nothing in C++ that concerns with system programming either, that is the C part of it, really. And so on and so forth, the more you look the more evident that truth is. Even the ancient Fortran can say it’s more concerned with performance than C++. C++ is not ISPC, nor Cuda. It doesn’t come with algorithms and data structure for low-latency, constrained memory use-cases, neither does care about large-scale data cases. Even python can be seen as a better language for high-performance computation, due to its ability to quickly implement embedded-DSLs. Nowadays, a lot of high-performance code leverages specialized compilers that use are embedded in relatively high-level languages via reflection. None of that is possible in C++.

C++ is a “zero cost abstraction” language. That part is true. But “zero cost” is not about performance. In fact, the guarantee that something won’t cost you anything when it’s not used doesn’t really mean that it will be fast when you do use it! What it gives, instead, is peace-of-mind. Bjarne said, do you like C? And its ecosystem? Great! Use this one, I guarantee I won’t screw with C, and if you like anything else I added, you get to use it.

And don’t get me wrong. This is genius. And a fundamental lesson that so many other languages still today don’t understand. Making a nice language is the easy part. If you’re even just a tourist of computer languages, have been exposed with concepts from veterans like Lisp and ML and so on, it’s not that hard to come up with a perfectly pleasant little language. And in fact, we have so, so many of them today. The hard part is selling such language! And if you don’t have a community with a strong need that nobody but you serve, that means you have to persuade people to hop over from whatever what they’re currently using. That is almost impossible.

Bjarne understood that the ecosystem is what matters most and C++ succeeded by being a drop-in replacement for C. Unfortunately now C++ is so complex, that creating a new language that seamlessly can work and replace it is a tall order, but it would also be an incredibly powerful tool for adoption.

**Why things changed and what can we do about it?**

Bjarne got marketing right, he probably understood people more than languages, which is not an insult, to the contrary! People are all that matters.

But if this is the premise, it wouldn’t even be surprising that C++ is drifting away from systems programming, from what C programmers care about. Nowadays, these use-cases are a minority.

It is not unreasonable, from that point of view, to now try to appease to the cool kids writing web stuff. People who might be using python, or java, or go and so on. Programmers who are accustomed to working fast, gluing together frameworks and libraries more than they write any bespoke algorithm and data structure. In fact, when you think about it, adding OO to C was just what was trendiest at the time. It was a hype and marketing based decision, not really a smart one, as we now maybe see more clearly as the OO hype dissipates.

But I don’t even think it’s necessarily a conscious design decision. This language is huge today. Its community its huge, and it decided to go the way of the design by committee. Should you never do that? In my circles, the answer is definitely no, design by committee is the death of technology. But let’s present a more positive way of looking at it.

We know that democracy has a cost, a huge cost. It’s definitely not the most efficient way of governing, nor it produces the most brilliant decisions. It can be in fact, incredibly dumb. This is not news, even in the Roman Republic there were provisions for senators to elect a dictator for a temporary period when strong leadership was deemed necessary. Of course, the risk is for a dictator to become a tyrant, as Romans learned. So, democracies trade efficiency for risk aversion, variance for mean.

And that is what C++ is today. It’s an old language, even if it wants to play cool, it fundamentally is in maintenance mode, listening to a lot of people with a lot of ideas and going in the direction of the majority, not of strong design decisions. Sometimes people argue that the solution would be to have more representation of certain use cases in the committee.

Perhaps a bit would help, but for how much I do like politics, I really don’t care about language ones. If I could vote on something, I would vote to remove people from the committee, make it a smaller one, not a noisier and bigger one, even if the noise was to argue “in my favor”. I simply don’t think you can have a lot of compromise in technology without ending up with something mediocre.

So? So we live with C++. Not because we like it, but because we need the ecosystem. The compilers, the IDEs, the language extensions, the low-level intrinsics, the legacy code. We restrict our usage to mostly C, and grab whatever rare new feature happens to integrate decently in our workflows. Maybe one day some new language will come, we already use bits and pieces of other ones when needed.

And maybe someday someone will learn the real lesson Bjarne had to teach, and really kill it! There is actually no reason for example that a language could not compile its own syntax in its files, but also allow to include C++ headers. Yes, you’d have to suffer and pay the pain of integrating a C++ compiler in whatever you come up with, and yes, your language would most probably just be something that expands to C++. Exactly how C++ started on top of C. But it’s unsexy, boring work, so most people will write yet another C-ish thing with a bit of ML in it on top of LLVM and call it a day...



*Addendum: "Alex" asked an interesting question in the comments - why don't we make our own. I tried to answer that as well if you have a look below!*
## 8 comments:

It's clear to me that C++ has a very useful and powerful ecosystem for the game development community but have two doubts:

1) While game development community is very diffident about all recent extensions some programmers stated at the end that they are not interested in using such sophisticated extensions.

2) I am wondering why the rich videogame industry has not yet take into account the development of a programming language dedicated to videogame development.

I didn't get what you're asking in 1), but I'll gladly answer 2)









Videogame studios should never ever make their own programming language. And they already do. Allow me to explain.

Unfortunately there is this common misconception that the more revenue you make, the bigger your company is, the more you have freedom to do things. This is wrong. Usually money comes with more restrictions on how you invest it, not less. Especially in the common case where making a big company means dealing with other people's money (investors, either private or public).

In this context, making a C++ replacement would be foolish. A serious programming language is a decade-long endeavour, just to get started. Then there is the ecosystem problem and finding and training talent. All the hot new languages people talk about, are really 10+ years old. In 2011 I wrote a long post about programming languages, and I never found it useful to write another one because I never thought the landscape changed. I talk back then about Rust for example, and what I thought back then mostly still applies today - http://c0de517e.blogspot.com/2011/04/2011-current-and-future-programming.html

Replacing C++ would be only an improvement for programmers, if any! That's to say, assuming we are successful, which, given how hard is to work the ecosystem, is not an easy thing. You want to have profilers, debuggers, linters, code-reviewing, distributed building/caching and so on and so forth. And all this in a context where you change platforms every 6-7 years (consoles, phones, whatnot) and you have zero control over these platforms (e.g. would they still use LLVM? who knows).

Programmers don't really matter, in the grand scheme of things. Yes yes, you heard me. Games, especially big games, are mostly content when you look at costs, and mostly design when you look at innovations that matter/make users happy/sell...

Of course there is the argument that if you make programmers happier (more productive), these can in turn make it "trickle down", but in practice that's also true to a limited extent. How do I know? Well, because I've never seen a game company where we had even addressed just all the "low hanging fruits" for productivity enhancements with the tools we have. Not for programmers, not for artists and so on. There is always a balance between getting these multipliers, and the reality of also shipping a game and keeping the production happy. If you've played any management game, Sim City, Stardew Valley, Starcraft, whatever you like, you'll have experienced these tradeoffs!

That if for "we should never do it" part. Why I say though that we already do? Because we do! But in the part that can get us a ROI. I said that game design for example is much more important. And in fact you will find there lots of custom scripting languages and environments made to help people create new things. Even custom VMs, custom compilers, transpilers and so on. Same with artists, you get node-graphs, scripting languages and other similar things.

Hope this helps!

(that's also why it's most likely for languages to be started by individuals with some amount of time on their hands, e.g. https://github.com/BSVino/JaiPrimer/blob/master/JaiPrimer.md or say http://arclanguage.org/ or dunno, https://bitbucket.org/duangle/scopes/wiki/Home https://nim-lang.org/ and so on and so forth)


Have you ever looked at D language?

You said:


“Nowadays, a lot of high-performance code leverages specialized compilers that use are embedded in relatively high-level languages via reflection.”

What are some examples of this approach?

Unity's Burst compiler is a great example of this. Written in C#, but with a specialised compiler to write high-performance byte code based on a subset of the language http://lucasmeijer.com/posts/cpp_unity/

Yes, also plenty of numerical, big data and machine learning things. For example, pyCuda, parakeet python, numba, cython, theano, pytorch and so on... All code-generators that either use the python AST or equivalent methods to embed themselves in the language.

Yes, I've looked at D.






Some old articles: http://c0de517e.blogspot.com/2011/04/2011-current-and-future-programming.html

http://c0de517e.blogspot.com/2014/06/where-is-my-c-replacement.html

http://c0de517e.blogspot.com/2014/06/bonus-round-languages-metaprogramming.html

The tl;dr; version is that yes, D is wonderful. It's C++ done right. Even Rust could be wonderful, but I personally "disagree" with the borrow-checker (its usefulness in our domain).

But, all these things are incremental improvements, and I think they won't fly. Relatively small improvements are ok only if you keep full compatibility with the past (like C++ did with C).

Otherwise you'd really need to show a huge leap to be able to win over the inertia of our large, risk-averse, multi-platform legacy codebases and all the very significant tooling ecosystem built around them.

Especially as, then again, there isn't a lot of space for improving the "living coditions" of these C++ codebases. There is some space, yes, but not for huge investments, because at that point you run into tradeoffs where your time would be much better spent improving other areas that impact the end product more.

Post a Comment