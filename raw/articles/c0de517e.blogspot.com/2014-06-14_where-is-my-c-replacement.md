---
title: Where is my C++ replacement?
url: https://c0de517e.blogspot.com/2014/06/where-is-my-c-replacement.html
published: '2014-06-14'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Nowadays I can safely say the OO fad, at least for the slice of the programming world I deal with, is over.

Not that we're not using classes anymore (and why should we not), but most good studios don't think OOP and thanks to a few

[high-profile](http://home.comcast.net/~tom_forsyth/blog.wiki.html#[[Data%20Oriented%20Luddites]])[programmers](http://macton.smugmug.com/gallery/8936708_T6zQX/1/593426709_ZX4pZ#!i=593426709&k=ZX4pZ)[who](http://research.scee.net/files/presentations/gcapaustralia09/Pitfalls_of_Object_Oriented_Programming_GCAP_09.pdf)[spoke](http://realtimecollisiondetection.net/blog/?p=81)[up](http://harmful.cat-v.org/software/c++/linus)(more amusing reads in the "The rest and the C++ box of chocolate"[section here](http://fabiensanglard.net/trespasser/index.php)) people are thinking about what programs do ([transform](http://www.slideshare.net/DICEStudio/introduction-to-data-oriented-design)[data](http://bitsquid.blogspot.ca/2010/05/practical-examples-in-data-oriented.html)) instead of how to create hierarchies.
I can't remember last time someone dared to ask about Design Patterns at a coding interview (or anywhere). Good.

Better yet, not only OOP has been under attack,

[but C++ as well](http://yosefk.com/c++fqa/). Metaprogramming via C++ templates? Not cool. Boost?[Laughed at](http://www.boost.org/doc/libs/1_55_0/libs/geometry/doc/html/geometry/design.html). I wouldn't be surprised if Alexandrescu even thought policies ([via C++ templates](http://en.wikipedia.org/wiki/Modern_C%2B%2B_Design)) are crazy...
And not only we subset C++ into a manageable, almost-sane language (via

[coding standards](http://google-styleguide.googlecode.com/svn/trunk/cppguide.xml)and linters), but more and more people are even going back to a C-like C++ style.
So it begs the question. If we're so unhappy about OO and even recognize many of the faults of C++, where is the replacement? Why are we still all using C++?

I wrote a big, followed post on



[programming languages back in 2011](http://c0de517e.blogspot.ca/2011/04/2011-current-and-future-programming.html)and I haven't updated it yet because I don't feel too much has changed...**Addendum**: I didn't really mean to discuss language features, just success and adoption in my field and some of the reasons I believe are behind it. But there was something I wanted to add when it comes to languages[and I wrote it here](http://c0de517e.blogspot.ca/2014/06/bonus-round-languages-metaprogramming.html)**- Engineers should know about marketing**

And people. And entrepreneurship. Really. I'll be writing some of the same considerations I've expressed in my last post about

[graphics APIs](http://c0de517e.blogspot.ca/2014/06/rate-my-api.html), but it's not a surprise, because they are universal.
So, let's do it again. How close are "C++ replacements" of being viable for us? What do we want from a new language?

- Solve pain (big returns). Oh, a new multi-paradigm, procedural, object-oriented, functional, generic language with type inference and dependent types? Cool! How does it make me happier? How does it solve my problems?

- Don't create pain (low investment). Legacy is a wall for the adoption of any new language. How easy is your new language to integrate in my workflow? Does it work with my other languages? Tools? IDEs?

Now, armed again with this obvious metric, let's see how some languages fare from the perspective of rendering/AAA videogames...



**- D language**

D should be the most obvious candidate as a C++ replacement. D is an attempt at a C++ "done right", learning from C++ mistakes, complexity issues, bad defaults and so on while keeping the feeling of a "systems" language, C-like, compiled.

It's not a "high-performance" language (in the sense of numerical HPC, even if it does, at least, support 128bit SIMD as part of the -standard- library, so in that respect it's an evolution) but, like C++, is relatively low-overhead on top of C.

So why doesn't it fly (at least yet)? Well, in my opinion the problem is that nowadays "fixing" C++ is not quite enough to switch. We already "fixed" C++ largely by writing sane libraries, by having great compilers and IDEs, detecting issues with linters and so on.



Yes, it would be great to have a language without so many pitfalls, but we worked around most of them. What does D do that our own "fixed" C++ subsets don't?

Garbage Collection, which is important for modularity but "systems" programmers hate (mostly out of prejudice and ignorance, really). Better templates to a community which is quite (rightfully) scared of meta-programming.

Garbage Collection, which is important for modularity but "systems" programmers hate (mostly out of prejudice and ignorance, really). Better templates to a community which is quite (rightfully) scared of meta-programming.

It doesn't even make adoption too hard, there are a number of compilers out there, even a LLVM based one (which guarantees good platform support also for the future), Visual Studio integration, it can natively call C functions with no overhead (but not C++

[in general](http://dlang.org/cpp_interface.html), even if it's an understandable decision).
It's good. But not compelling (enough) reason to switch. It quite clearly aims to be used for -any- code that C++ is used for by being prettier. That's like trying to replace EBay with a new site that has the same business plan as EBay but with a better interface (and no marketing)...


It almost seems to be made thinking that you can do something better and then people will flock to it because well, it's better. But things almost never go this way. Successful languages solve a need for some people and they often start with a focused niche of adopters and then if they're lucky they expand

Java, JavaScript, Perl, Python, all started in such a way. Some languages do arguably succeeded at being "just better" (or anyhow started from scratch to replace some others), but these they had huge groups pushing them behind them, like Microsoft did with C#.

It almost seems to be made thinking that you can do something better and then people will flock to it because well, it's better. But things almost never go this way. Successful languages solve a need for some people and they often start with a focused niche of adopters and then if they're lucky they expand

Java, JavaScript, Perl, Python, all started in such a way. Some languages do arguably succeeded at being "just better" (or anyhow started from scratch to replace some others), but these they had huge groups pushing them behind them, like Microsoft did with C#.



**- Rust**

Rust departs from C++ more than D and many people are looking at it with some hope it could be the systems language of the future. It's in its early stages of development still (v 0.10 as of today) but it starts well by having a big bold target: concurrency and safety, with low overhead


The latter attracted the interest of gamedevs (even if today, in its early implementation, Rust is not super fast), as while most type-safe languages have to rely on Garbage Collection, Rust does without, employing a more complex static type system instead.

[via an ingenious type system](http://doc.rust-lang.org/master/intro.html).The latter attracted the interest of gamedevs (even if today, in its early implementation, Rust is not super fast), as while most type-safe languages have to rely on Garbage Collection, Rust does without, employing a more complex static type system instead.

It's very interesting but for the time being and the foreseeable future for us (game/rendering programmers) Rust's aim is not so enticing.


We solved concurrency with a bunch of big parallel_for over large data arrays and some dependencies between a bunch of jobs carrying such loops.

We solved concurrency with a bunch of big parallel_for over large data arrays and some dependencies between a bunch of jobs carrying such loops.

We don't share data, we process arrays with very explicit flows and we know how to do this quite well already. Also, this organization is quite important for performance, a bunch of incoherent jobs would not use resources quite as well.


If we needed something "more" for less predictable computations (AI... gameplay...) we could employ messages (actors), but that kind of async computing is much slower. C++ doesn't make any of this trivial (of course!) but once it's up and running we don't have much to fear (that's also why fancy models like transactional shared memory are, I think, completely irrelevant to us).

If we needed something "more" for less predictable computations (AI... gameplay...) we could employ messages (actors), but that kind of async computing is much slower. C++ doesn't make any of this trivial (of course!) but once it's up and running we don't have much to fear (that's also why fancy models like transactional shared memory are, I think, completely irrelevant to us).

Safety could be a bit more interesting as safer type system could save us some time, if they don't end up in increased complexity. But, even if it's true that sometimes we have to chase horrific bugs, considering that we're working on the least safe language in the world, I'd say we're not doing badly.

Or maybe we are, but just think about all the times you considered a big refactoring to make the code more safe, and didn't manage to justify it well enough in terms of returns... And that's a much less ambitious thing than changing language!

I'd like to maintain a database of bugs (time spent, bug category and so on) in our industry to data-mine, many people are "scared" of allocation and memory related one but to be honest I wonder how much impact they have, armed with a good debugging allocator (logging, guard pages, pattern and canary checking and so on).


Maybe certain games do care more about safety (e.g. online servers) and maybe I'm biased being a rendering engineer, our code has (should have) simple data flows and really hard bugs are usually related to hardware (e.g. synchronization with GPU).

Not that we would not love to have Rust's benefits, I simply don't think though they are important enough to pay the price of a new language.


Nonetheless, it's a very interesting one to follow though, and it's still in its early stages, so I might change my ideas.



Maybe certain games do care more about safety (e.g. online servers) and maybe I'm biased being a rendering engineer, our code has (should have) simple data flows and really hard bugs are usually related to hardware (e.g. synchronization with GPU).

Not that we would not love to have Rust's benefits, I simply don't think though they are important enough to pay the price of a new language.

Nonetheless, it's a very interesting one to follow though, and it's still in its early stages, so I might change my ideas.

**- Golang**

Go is somehow similar to Rust at least as far as they are both C++ replacements born "out of the web" (even if Go was thought mostly for server-side stuff while Rust's first


In many ways it's


On one hand it's quite a bit simpler, with a much more familiar type system (also due to the fact that it doesn't try to enforce memory safety without a GC), so it requires a smaller investment, not quite as ground-breaking, but very practical.

[application aims to be a browser](http://en.wikipedia.org/wiki/Servo_(layout_engine))), but it could be a bit more interesting because of one of its objectives.In many ways it's

[not a great language](http://yager.io/programming/go.html)(especially right now) but it is promising.On one hand it's quite a bit simpler, with a much more familiar type system (also due to the fact that it doesn't try to enforce memory safety without a GC), so it requires a smaller investment, not quite as ground-breaking, but very practical.

On the other hand it has at least one very enticing core design feature for us: it's built for fast iteration, explicitly, and that is, finally, something we do really strongly care about in our day to day work!

We go to great lengths to avoid

[long iteration times](http://www.bitsquid.se/presentations/cutting-the-pipe.pdf), and

[C++ is](http://gameangst.com/?tag=code-bloat)

[so terrible](http://www.martinecker.com/rudebuild/)

[in that](http://www.altdev.co/2011/12/26/code-build-optimisation-part-4-incremental-linking-and-the-search-for-the-holy-grail/)

[respect](http://en.wikipedia.org/wiki/Opaque_pointer)

[that](http://tinodidriksen.com/2011/08/31/cpp-include-speed/)we even sacrifice performance with scripting or worse with "data-driven" logic (not data-driven programming, but logic, that's to say with data that doesn't express a Turing-complete language but yet expresses some of the logic that we need, usually requiring some very badly written interpreter of sorts).

It's also backed by a huge corporation, so it solved the "early adopters" issue easily.

Yet, as it stands now there is still too much friction for us to consider it: it doesn't quite work in our environments, it has a slow C interop and moreover most of its language features are not too relevant for us to a degree where just using C would be not much different in terms of expressiveness.

It's a nifty, simple language that has a strong backing and will probably succeed, but hardly for us, even if in principle it starts going somewhere we really need languages to go...



**- Irrelevance...**

That's a big problem, a substantial reason about why I think



**we**didn't find a C++ replacement.
It's not that all new languages don't understand what's needed for success, but most languages that do understand that are just interested in other fields.

Web really won. Python, Javascript (and the many languages built on top of it), Go, Rust, Ruby, Java (and the many languages built on top of the JVM).


If you look around the key is not to find a C++ replacement, that already widely happened in many performance critical fields. It's to find

If you look around the key is not to find a C++ replacement, that already widely happened in many performance critical fields. It's to find

**our**C++ replacement for our field that doesn't see anymore much language activity.
Application languages also left us behind, C# is

But it just seems that nobody is -really- concerned about making a static compiler for (most of) it that has the performance guarantees (contracts on stack, value-passing, inlining...) and the (zero cost) interoperability we'd like for it to really fly.

**great**as a language, clean, advanced, fast iteration, modern support for tools (reflection, code generation, annotations...) and the one that flirted with games most closely...But it just seems that nobody is -really- concerned about making a static compiler for (most of) it that has the performance guarantees (contracts on stack, value-passing, inlining...) and the (zero cost) interoperability we'd like for it to really fly.

High-performance computing does many of the same things we do, going wide with parallel instruction (SIMD), threads, GPUs. But they are not concerned with meshing with C/C++ almost at all, they are not low-overhead systems languages.

When you have to process arrays of thousand of elements, even the


Also, even when they are well integrated with C (i.e. C++AMP and OpenMP or the

Maybe in the future this will shift if we see an actual need of targeting

When you have to process arrays of thousand of elements, even the

[cost of interpreting](http://www.bitsquid.se/presentations/scripting-particles.pdf)[each operation](http://www.numpy.org/)that will then be executed wide, is not important, so HPC languages tend to be much higher-level that we'd like.Also, even when they are well integrated with C (i.e. C++AMP and OpenMP or the

[excellent ISPC](http://ispc.github.io/), Julia is also[worth a look](http://julialang.org/)), HPC takes care of small computational kernels which we know well how to code even all the way down to assembly, we're not too concerned about that.Maybe in the future this will shift if we see an actual need of targeting

[heterogeneous architectures](http://www.hsafoundation.com/)with a single code base, but right now that seems not too important.
Maybe mobile app development will save us, the irony. Not that I'm advocating Swift right now but it's certainly interesting that we see much more

[language dynamism there](https://developer.apple.com/swift/).**- In a perfect world...**

How could a language really please us? What should the next C++ even look like to make us happy? C++ was a small set of macros on top of C that added a feature that people at the time wanted, OO. What's the killer feature for us, today?


Nice is not enough. D is nice. Rust has lots of nice features and we can debate a lot about nice language features we'd like to have, and things that should be fixed, and I do enjoy that and I do love languages.


But, I don't think that's how change happens, it doesn't happen because something is simply better. Not even if it's


As engineers we sometimes tend to underestimate just how much something has to be conveniente in order to be adopted. It's

When all these are done, there is still the community to take care, the education, what your programmers know and what programmers you want to hire know... And when you have all these in line you still need to overcome people laziness, biases, irrationality (all defects I partake in myself).

And even if all is there you simply might not have the resources to pay for the cost, even if the investment is positive in the long run, or, which is actually harder, be able to prove that such investment will make more money!


It's a mountain. That's why C++ survives for us.


Back to the beginning, cost/return, how can we find a disruptive change in that equation? I think for us a new language can succeed only if it fulfills two requirements.


One is to be


The other is to be so compelling

We're good with performance already even if we have to sweat and we don't have standard vectors or good standard libraries and so on.

We don't care (IMHO) enough about safety, that we are becoming better at achieving with tools and static checkers. Not concurrency, that we solved. Not even simplicity, because we can "simplify" already our work by ignoring complex stuff... But productivity, that is my bet.

Nice is not enough. D is nice. Rust has lots of nice features and we can debate a lot about nice language features we'd like to have, and things that should be fixed, and I do enjoy that and I do love languages.

But, I don't think that's how change happens, it doesn't happen because something is simply better. Not even if it's

**much better**, not in big fields with lots of legacy (and not if "better" doesn't necessarily translate to making lots more money as well or spending lots less).As engineers we sometimes tend to underestimate just how much something has to be conveniente in order to be adopted. It's

**not only the technical plane (not at all)**. It's not only, the tools, the code legacy, the documentation.When all these are done, there is still the community to take care, the education, what your programmers know and what programmers you want to hire know... And when you have all these in line you still need to overcome people laziness, biases, irrationality (all defects I partake in myself).

And even if all is there you simply might not have the resources to pay for the cost, even if the investment is positive in the long run, or, which is actually harder, be able to prove that such investment will make more money!

It's a mountain. That's why C++ survives for us.

Back to the beginning, cost/return, how can we find a disruptive change in that equation? I think for us a new language can succeed only if it fulfills two requirements.

One is to be

**very**low-cost, preferably "free", like C++ was (C with Classes). Compiling down to C++ is a good option to have, makes us feel safe. That's why C++ superset and subset, are already very popular today: we lint, we parse, we code-generate... reflection, static-checking, enforcing of language subsets, extensions...The other is to be so compelling

**for our use cases**, that we can't do without. And in our industry that means I think something that saves order of magnitudes in effort, time and money.We're good with performance already even if we have to sweat and we don't have standard vectors or good standard libraries and so on.

We don't care (IMHO) enough about safety, that we are becoming better at achieving with tools and static checkers. Not concurrency, that we solved. Not even simplicity, because we can "simplify" already our work by ignoring complex stuff... But productivity, that is my bet.

**- Speed of light**

If I have to point at what is most needed for productivity, I'd say


That's so badly needed in our industry that we often just


Why did Lua succeed? It's a scripting language! Why aren't we hot-swapping D instead? We sacrificed runtime performance, to what? To both productivity and cost!

Lua is easy(-ish... with some


Among the languages that are "safe", guaranteed to work with all our platforms (even in the futre) and that interop with C easily, and that allow live-coding, Lua is the fastest, so we picked it. Not for any language feature (actually the language itself is not really ideal and it heap-allocates a lot). It could have been gwbasic I think for what we cared about the syntax...



[interactivity](http://art-of-optimization.blogspot.ca/2014/06/the-legacy-of-goal.html).[Interactive visualization](http://worrydream.com/), manipulation, REPLs,[exploratory programming](http://ipython.org/),[live-coding](http://toplap.org/category/software/).That's so badly needed in our industry that we often just

**pay the cost of integrating**(or craft other scripts), but that can work only in certain parts of the codebase...[Lua](http://www.lua.org/)Why did Lua succeed? It's a scripting language! Why aren't we hot-swapping D instead? We sacrificed runtime performance, to what? To both productivity and cost!

Lua is easy(-ish... with some

[modifications](http://www.havok.com/products/script)...) to integrate, maybe other languages could be as easy but crucially Lua being a portable interpreter guarantees it will work on any platform that supports C (or we can fix it to work, easily). And Lua is productive, allows interactive coding, it's even better than[hot-reloading](https://www.unrealengine.com/products/unreal-engine-4)[C++](http://runtimecompiledcplusplus.blogspot.ca/)in terms of iteration.Among the languages that are "safe", guaranteed to work with all our platforms (even in the futre) and that interop with C easily, and that allow live-coding, Lua is the fastest, so we picked it. Not for any language feature (actually the language itself is not really ideal and it heap-allocates a lot). It could have been gwbasic I think for what we cared about the syntax...

A language that meshes well with C/C++ codebases, that we can trust in its availability on all platforms (the option of a C/C++ codegen is a way to ensure that) but that offers fast iteration will succeed in our field.

In fact I would gladly give up any of the C++11 features (even


I really think iteration time is the key, and approaching interactivity is a game changer. I would take any language, regardless of the details, if it's interactive. In fact I do, as a rendering engineer, I love shader programming even if shader languages are not great and their tools are not great, just because shaders are trivial to hot-swap.

It's such a disruptive advantage, and it's really the only thing that I can think of that is compelling enough for us to pay the price of a new language.


My best hope nowadays is

That could enable low-cost adoption of new languages, well integrated with C/C++ compiler and libraries, the same as JS is now the web common substrate for a lot of languages (or JVM is for server stuff).

In fact I would gladly give up any of the C++11 features (even

[the few decent ones](http://c0de517e.blogspot.ca/2013/05/integrating-c11-in-your-diet.html)) for[modules](http://llvm.org/devmtg/2012-11/Gregor-Modules.pdf)(preferably dynamic, but even static would increase code malleability), but of course the committee[is a sad joke today](http://www.phoronix.com/scan.php?page=news_item&px=MTU1OTE)so, they rather just add complexity to one of the most arcane languages out there.I really think iteration time is the key, and approaching interactivity is a game changer. I would take any language, regardless of the details, if it's interactive. In fact I do, as a rendering engineer, I love shader programming even if shader languages are not great and their tools are not great, just because shaders are trivial to hot-swap.

It's such a disruptive advantage, and it's really the only thing that I can think of that is compelling enough for us to pay the price of a new language.

My best hope nowadays is

[LLVM](http://llvm.org/), which seems it's more and more poised to be the common substrate for systems programming across platforms (windows is still not the best target though, but work is in progress).That could enable low-cost adoption of new languages, well integrated with C/C++ compiler and libraries, the same as JS is now the web common substrate for a lot of languages (or JVM is for server stuff).

## 95 comments:

C++ is the best language in the world. It allows you to write very fast code in a concise manner. Could be more concise still, but at every new step in the standard they add things to make it more concise, less verbose.

To me a new language should be C++ without the C legacy, the preprocessor and the overly complex build mechanism.

If you really know what OO is about, the fundamentals : encapsulation, data hiding, ( compile time ) polymorphy ( I'll leave out inheritance ) then you can do wonderful stuff with templates and basic classes. Writing less code has never been easier with C++, and believe me, the last thing we need is more code.

I'm completely uninterested in debating C++ and OO "merits".









The war for me is over, all companies I know and I work with already shy away from most of C++ fads and defects, there are a large literature about them. If you want you can follow the links I provided in the article, I won't repeat the points everybody already knows.

Of course if you're perfectly happy with C++ then from even the title of the article you should have understood it's not something it might interest you to read...

I'm sorry if what I write disappoints people who love the language, I did love it a long time ago and then grew out of it, and most people I noticed follow a similar path to enlightenment.

I can only suggest to really ask yourself this question. How many languages do you really know? Most people are in love with C++ because they refuse to learn anything else. Do you know ML (SML or OCaml or F#)? Do you know Haskell? Are you a C# expert? Lisp/scheme, python, dylan and successors... Did you try to code in C or C-stlye for a while after falling for C++? If not, try seriously a few of these things (I'll reccomend starting with OcalML, for an hardcore C++ guy), you might grow out of C++.

I'll be strict and draw the line even before comments start flowing in.

I won't discuss why I think C++ is horrid anymore, the article just assumes it's a given and provides a few links (also I did various times already on the blog btw, and I'm not ignorant about C++, I use it, I know it well, I even know what's good and bad about C++11 and 14).

If people want to debate in the comments because they feel the need to defend the language or OOP in general, I'll kill these messages (thing that I usually -never- do).

You've been warned, don't waste your time typing, you'll be pissed when what you wrote disappears.

While people figure out how to replace C++, I simply went back to C. It is perfectly capable of 'transforming data.'



For more high level stuff that is not performance critical, Python has been a joy to use for me.

Rust/D/GO: unfortunately none of these have the tools or infrastructure to replace C++, and likely won't for many years.










What will likely replace C++, is C++14 and then C++17. Hopefully with modules, compile time reflection etc.

You seem to be equating OOP with C++ as in the OOP found in Java. Nobody (sane) uses C++ like that anymore.

Good C++ today is metaprogramming heavy, avoids complex hierarchy, data driven, and cache oriented.

You don't encounter this because you work in the games industry, which for historical reasons had to deal with very outdated compilers that didn't handle meta-programming well.

The games industry also has suffers from having older generations of C programmers who really have no idea how to use C++, but are doing so anyway.

I think that concepts lite will make metaprogramming much easier for people who have previously avoided it, it shortens the syntax, allows for concept based overloads, and makes errors much clearer.

Although I have little hope that this will enter the game industry anytime soon since the industry is pretty insular.

An example of good by game industry standards, but bad by modern standards C++ is UE4. The code is 10 years out of date with regards to C++, and is generally about 3-5x as verbose as it would be, if it were written in a modern style.

That said I still hate many things about C++(horrible build system, C legacy, still too verbose). Just not the same things you appear to hate.

ps. Alexandrescu is one the guys beind D, and D can handle "policy" based code in ways that C++ can really only dream of currently.

I believe you already said what succesor to C++ can be - actually something like cleaned up C++, or improved C. Main reason is backward compatibility with existing codebases, and the fact that most people use C++ subset anyway. I am not sure whether languages with automatic memory management models can be used in game and high performance programming environments. A lot of game memory usage patterns are not handled well by refcounting or GC. Very often we need explicit and predicable memory management. In any case language should support "unsafe" memory at least for graphics API.

D is still at the top of my list of C++ replacements - it does so much right compared to C++. Despite what you say, it is a high-performance language if you want it to be (use LDC instead of DMD to compile and turn off GC). My only outstanding concerns with it are that it still allows all pointers to accept nulls, its GC is particularly immature, and you can't really do much without first writing your own bindings.


You're right about Web winning though. I've loved studying computer vision, 3D graphics, and [video, image, data] compression, which are all C++-dominant realms. But the fact is that I make significantly more money being a "C#/JavaScript Ninja" than I could get from doing R&D or GameDev. It's gotten so bad that I've actually run out of ideas for hobby projects in systems-lveel languages - everything I want to play with is much easier to do in Python or JS.

I really really want to like D, but the tools are so bad right now. Tools matter. Alot.




D also has a pretty horrible GC design--

"But it just seems that nobody is really concerned about making a static compiler for (most of) it that has the performance guarantees and the interoperability we'd like for it to really fly."What do you think about .NET Native? Writing code in a "nice" language like C# and using (the backend of) the C++ compiler to produce a fast executable sounds good to me.

I'm pinning my hopes at Rust. Not necessarily because of their whole task/concurrency stuff but because they're making a language that takes the main *actual* productivity wins from modern high level languages, but culls out things that have unreasonable performance cost.




You don't need to deal with mysterious bugs anymore because your code is memory safe, but you don't to have to deal with a language that encourages allocations everywhere, and GC, etc.

Things like Go and D both make dumb choices IMO. Like leaving null pointers in there. That's a huge productivity drain (you may not ship null pointer exceptions, but catching them at compile time surely saves tons of time).

So Rust seems like the winner to me. Lots of high level affordances. Occasional restrictions to ensure high performance. But still has all the escape hatches that you need to do low level things.

Rust brings functional programming, which is kind of a better alternative to OOP, isn't that just what you are looking for?



Why do you say that D is not a "high-performance" language?

Interactivity is a great goal, but isn't it mostly a library-level thing?

What you are asking for is Swift





- without Apple Control

- removal of Obj-c runtime and Cocoa idioms

- Ofast turned by default which turns of safety and runtime check

- removal of ARC.

call it 0fast++

better trademark that fast.

Anonymous: "Good C++ today is metaprogramming heavy" - Kill that shit, with fire.






Bram: I like C-like C++, I won't go back to pure C as templates are good for containers (generics, basically) and overloading is good for numeric types. Classes are not that useful and any other use of templates and overloading I would be very cautious of, but for containers I don't want to go back to pure C.

Christoph: I didn't look much into .NET Native, thanks for the reminder, will try

Sebastian: nowadays I don't think productivity comes really from whatever nice high-level features a language offers, really. Of course it's nice to have lambdas or type inference, it's actually really great, but I'd take any language over any other if it offers faster iteration, no matter really the other details. Even basic. I really think that is the only compelling enough feature that can move codebases, because it's revolutionary.

VZQ: Functional is a nice programming paradigm, I don't think it's strictly "alternative" to OOP, in fact most functional languages tend to be both OO and functional... That said, it's nice, even lovely, C++11 adding lambdas got much closer in terms of allowing functional paradigms when needed though, and I don't think it's one way or another a huge deal. Functional can be a big departure from imperative when coupled with lazy evaluation, but that is impractical in our field, it's a completely different way of thinking but doesn't mesh well with what we do.

D is not "high-performance" the same way as C and C++ are not. Systems is not the same as high-performance. Fortran always has been more "high-performance" than C/C++ as it doesn't have pointer aliasing (think that C++ introduced restrict, which is the bread and butter of a HPC language only in C++11, same for threading, still no vector types...) for example. ISPC is a HPC language or Julia, Fortran, even Numpy if you want, not D or C or C++

Anonymous: I dunno if I'm asking for Swift because that's so new I didn't dabble with it at all, but it surely looks interesting! I don't actually care about it being made by Apple as I'm sure if it takes off it will have open implementations, like Java or C# and so on

"


it [D] can natively call C functions with no overhead (but not C++ ones unfortunately, even if it's an understandable decision)."Actually (to some degree), you can call C++ from D and the other way round, see: http://dlang.org/cpp_interface.html

Cheers,

Daniel

Daniel: thanks for the correction, I've edited the article to be more precise.

:-)





IMHO, while interfacing with C++ in D is not seamless, it looks like the best possible trade-off to me and (in contrast to writing C wrappers for the C++ Code first) it seems realistic/doable for many use cases.

My biggest issue with D2 (last time I tried it 2 years ago or so) was the incomplete standard library.

And I kinda fear that Alexandrescu's influence makes it too "boost-y" :-/

Still, it's a nice language, I wish it would get bigger traction, I think it would be quite suited for gamedev and I guess it would even be viable to use an existing (rendering) engine written in C++ and write all the game logic etc in D, doing the interfacing as described in the aforementioned link.

Cheers,

Daniel

What do you think about Haskell? Is it applicable for game development?

Anonymous: some concepts from Haskell would be interesting in an ideal language. Certainly having more safety through types is always a nice thing that we love to embrace (and to that end Rust is great too). But I don't think that alone would shift us, at all. If you want to do something like D, an "ideal" "nice" language, yes, some inspiration from Haskell is nice (Haskell per se is not, at all. I don't think pure functional languages work for us and I don't even think in general they are a nice idea or solve actual problems)... but overall it will be irrelevant because nice is not enough.

The main thing I want beyond C/C++: The ability to EFFICIENTLY PROVE some aspects of correctness.



I almost don't care if it's DBC, DependentTypes, Algebraic Types, garbage collectors, or a bunch of new pointer types. What we mainly have is a security and correctness crisis.

When arbitrary pointer arithmetic is admitted (with threads even), there is absolutely nothing you can be certain about in the runtime. In weak type systems, the declared types are often lies (ie: x points to an integer... no, it's a union of an int pointer, a null value, and junk...where if junk is allowed you can't discriminate which one it is solely based on its value. if you view types as propositions that must be true, then it's plain that the type system is full of lies.)

Rob: True, but videogames are kinda disposable. Well. Most are.





Some need to run over the years and defeat hackers and carry lots of value for the people involved, but most are not.

So I don't value their correctness much, I value them as art. They have to entertain, work when they ship, work for a few hours reasonably well, and be creative and fun.

And for these objectives what you need is iteration, productivity, experimentation. Now of course certain aspects of safety and security carry over to productivity because they remove certain nasty bug that waste our time.

But really I value any language feature by the time it saves, that's all, and fancy static typing is not the best in that metric, I think.

Look how much money goes through the game industry every year. You'd think we could get off our ass, divert a little bit of that, and make something good happen that saves tons of time/energy for everyone down the road.



I agree that safety hasn't been that bit a deal in the past but it is going to get bigger as more things are increasingly online. I think you could get safety for most code at no cost, and eliminating most NULL pointer problems has been handled by other languages (these are not hard to debug, of course, but they are common enough that they eat a lot of time just because of that, and they can lurk for a long time if your testing doesn't get full coverage of the code, which in games it never does).

But, I think shipping a single AAA game is probably MUCH harder than building a C++ replacement with an accompanying toolchain that beats the pants ofd Visual Studio. The problem is of course who do you trust to do this? An industry initiative is going to have guys from like EA on there, as well as "template metaprogramming is great" kinds of people. I think most often it is arguments about what should be in the language that then make the language mediocre in the end... like the Space Shuttle. You'd have to get someone with a strong vision leading the project and then avoid arguments somehow.

Haha, when posting my EA dig I forgot where you are. But I think you know what I mean...

Jonathan: I see the online point, but I'm not sure that affects the client part really, would agree it's a problem for servers especially if they store persistent, valuable users data.






As for our industry being rich but not willing to change, I think it's because engineering doesn't matter as much, that's my take.

With that I mean that if I make my game 10% faster and make it crash 10% less, chances are that it will translate in around 0% more sales.

Some games are so bad that engineering negatively affects sales, but most are good enough and the correlation between our work and money is not that direct.

On the other hand look at the web. There you optimize milliseconds and get higher attachment, you can measure these things and prove you're making more money. That means engineering is more powerful (not that all web projects are great examples of engineering, but it's hard to see that there is more activity there on the engineering side).

Even better is I think high performance trading, there you literally control money with code. We're too far removed from money and so it's harder to justify stuff like making or adopting new languages.

BTW, speaking of EA, I know there they made actually some great language experiments, really good stuff. It died. Nobody cared enough on the game teams to really adopt it. The successful language initiatives were always more "scripting" like languages with smaller niche domains, nice stuff, but no C++ killer.


Activision STRONGLY believes in studio indipendence so we don't really have as much in terms of shared tech and shared tech initiatives, we just have a shared pool of "talent" that helps the various studios when needed. Most of the code I've seen so far there is VERY C-Like C++, with some sprinkle of more "modern" C++ in some tools. But that shouldn't be surprising if one knows what we do...

I did a lecture at dconf that you might find interesting: https://www.youtube.com/watch?v=FKceA691Wcg




I agree with the closing point you made about productivity, and I attempted to address that in the context of D.

I was working at Remedy (Max Payne, Alan Wake...) where we were wrestling with the age-old solution for productivity. Lua is the conventional go-to, but we wanted a solution that systems programmers could become invested in. I am also quite enthusiastic about D, and it seemed like a natural fit for the system we crafted to address the productivity problem.

For my money, the most compelling solution for gamedev is D, and your arguments against it were, frankly, fairly weak. If a solution such as the one I demonstrate in my talk were widely available, would that be enough to sway your judgement?

Some derivative of Common Lisp could really hit the sweet spot for me. A derivative more in spirit than specification perhaps but it's a language that's ripe for a revitalization. Especially considering the idea of it's target applications being more like works of art requiring fast iteration, experimentation.


Beyond that Rust has really given me a lot of joy to work with (even with the pains of incompatible compiler updates).

Manu: thanks for the link, I'll have a look. About the arguments I might be very biased and wrong (of course!) but it seems D didn't really fly (I'd say I even saw more activity around Go than D...) so there has to be a reason (if we accept that premise at least)


Chip: I like lisp REPL and in general exploratory programming, and I love Mathematica (not much as a language, but the entire system is very compelling). Lisp as the idea of an almost syntax-less system doesn't really entice me and I think metaprogramming is really scary and to be taken with care, because it mostly means that you can't really know what code does by looking at it in isolation.

There's a few reasons for D's perception issues, I think...




D had a version change, D1 -> D2, where some mistakes were corrected, and language breaking evolutions were implemented. D2 is only just now becoming mature enough for enterprise use (and demonstrated by Facebook's interest for instance), so I'm not sure it's fair to say "It didn't really fly", since it's only just now reaching maturity. Whether it flew is yet to be demonstrated.

The other big issue I find with D, particularly in contrast with Rust and Go, is it's not written for a particular application. Both Rush and Go are written by special interest groups, and I think the target was more cohesive throughout the design.

Your analysis of D is fair, it is an essential attempt at C++ done right, and I don't think that's a bad thing necessarily. You made a lot of my points; aggressive language change == retraining staff, new tooling/workflow, etc.

D is enough like C++ that engineers can basically just start writing D code with no training, and gradually improve their 'style' by osmosis and through experience. I think this is important in terms of operational practicality.

I won't go into it, but D has some features that potentially enable significant evolutions from C++, but one of the biggest sellers for me is productivity; the language is tighter and more regular than C++, and as a result, it compiles FAST. Combined with solid reflection tech, you can do runtime re-compilation and REPL and things like that from a static language with just a little tooling support, and you finally start to address the long-standing C++ productivity issues within the same language that you can write the foundational systems. Goodbye Lua!

It is probably fair to say that D is a solution looking for a problem, and for my money, gamedev is a serious problem that D can help with. The fact that it's an OSS community too means it's highly susceptible to community weigh in. If significant number of gamedev's explored and invested in D, the community would promptly respond by focusing on gamedev requirements. There is a solid foundation, years of work are already done. It just needs to take the last few steps addressing specifics for our industry, and that will happen when we get involved and ask for it. You would be hard pressed to ask the same from other language communities, and that's the key reason why I feel D is the most realistic option for us.

C# with .NET Native and/or IL2CPP?

I just don't think C# is that great for native/systems dev.

Any language that requires conversion to C/C++ code is practically impossible to debug, and the toolchain turnaround would be even slower than C alone!

I think generating C++ code is tactically useful, though, as suggested in the post.


If you can target C++ code *or* native code, you make it easier for people with a mostly-C++ codebase to try you out. Then when they like it enough to start switching over, they will be willing to put up with more of the usual wall of glue that you have between languages.

Might surprise some but don't forget the ubiquitous presence of FreePascal http://freepascal.org/




... and it's acompanying GUI IDE http://lazarus.freepascal.org/

Some say FreePacal can even be used to write OS and it certainly does all this --

"Free Pascal is a 32,64 and 16 bit professional Pascal compiler. It can target multiple processor architectures: Intel x86, AMD64/x86-64, PowerPC, PowerPC64, SPARC, and ARM. Supported operating systems include Linux, FreeBSD, Haiku, Mac OS X/iOS/Darwin, DOS, Win32, Win64, WinCE, OS/2, MorphOS, Nintendo GBA, Nintendo DS, and Nintendo Wii. Additionally, JVM, MIPS (big and little endian variants), i8086 and Motorola 68k architecture targets are available in the development versions."

Manu: I agree with you, D's main issue is that it doesn't focus on a niche, and it didn't bother in trying to be successful before going big. Go for example is much, much smaller and simpler and less ambitious yet it had a clear focus on a niche and it's gaining more momentum.



I dunno, but I feel like just a "better" C++ for us that really are not too willing to change and are quite settled with a lot of C++ legacy, won't really cut it. A new language has to offer much more than incremental improvements, than fixing C++ issues. It has to be an order of magnitude better, disruptive, and focused to succeed.

If D added live-coding or hot swapping I think it would suddenly grab a LOT more attention than trying just to show how neat it is...

PaulANormanZ: pascal is not really much better than C or C++

Jonathan/Manu:



For a language targeting C++ (as a backend) is a failsafe, it makes people less concerned of losing all their code or not being able to ship on a new platform.

But it's not the best experience, for debugging and so on, so it's a great option to have but of course if you can pair that also with an LLVM backend that would be better!

C++ codegen for reflection and other "additive" features on top of C++ (e.g. serialization) is another thing and that's perfectly great and sound and we routinely do that.

The "C++ Killer" is C++.




C++11 is a new language, that happens to be backwards compatible with C++03.

C++17 will be another new language, that also happens to be backwards compatible with all C++ written in the last 30 years and most of C too.

LLVM tools for C++ are highly advanced. If you need a special language to do a specific task, just compile it to LLVM bytecode and statically link it to your C++. LLVM enables and unifies polyglot architectures.

Try Vala. Nuff said.

what about swift? i know it's mac, but it looks good to me

I think Scala is a serious contender, already in the backend. And if it's able to generate native code with llvm it could become the successor. For me it's a very good balance between C++ and Python to make things reasonably fast with a typed language and accessing a wide array of java libraries.

There is a better language and has been all along. It is called C. The call for "better" languages has always been "protect me from my own inadequacies". Trouble is this is actually the driving force, as most "software engineers" are not really computer-literate in any technical sense. Whilst running to adopt the next bizarrely non-orthogonal scripting language they never stop to think that in order to have any performance at all those same languages are, at bottom, written in C and almost always provide a linkage mechanism to externally compiled C code. When the code hits the metal it is C or assembler. There is certainly a productivity issue if you are not very good at either software engineering (not "OO"(!)), or C or both. But that also applies to C++ which does have a place at some higher levels of abstraction. It is possible to de-skill "programming" at some level as long as the goal is narrowly defined e.g. drawing pictures on the Web but for the vast panoply of applications a malleable and powerful implementation tool is called for - C. All, of course, IMHO, colleagues.

I fall in love C++, I hate C++.



I fall in love C++, I hate C++.

I fall in love C++, I hate C++.

...

I have looked for any language makes me more enthusiastic than C++ for a few months.

I tried to love Python, Perl, Common LISP, Scala, Haskell, Go, Rust etc.

The result is disappointment.

I decide to try Clojure for once :)

I think, my programmer life will finish with C++.

Metaprogramming is clearly the reason C++ is successful. It's also clearly horrible in C++ today; but without it you'd need to change the language every time you want to introduce new fundamental types (say, vectors & matrices for gamedev).





There does not seem to be a good reason why metaprogramming needs to be horrid, however. Why can't metaprogramming simply be programming that happens to run at compile time, and happens to generate code?

Both Rust and D improve on C++ here, but I worry that D doesn't stand much chance simply because it's not enough. The advantages D has over C++ just aren't enough to compensate for the legacy.

So, I'm betting on Rust. It brings something sufficiently different to the table that small changes in C++ design patterns can

t easily replicate.

Basically: without some features like "free parallism", GC, or "lisp-like code introspection" that C++ simply can't emulate easily, a language will have a tough time. Rust's take on almost-GC and easier parallelism *might* just be enough.

DEADC0DE said...


PaulANormanZ: pascal is not really much better than C or C++

DeadCode: You've worked in OpenPascal and Lazarus or http://www.pilotlogic.com/sitejoom/ ?

Here is Bjarne Stroustrup talking about his C++.



You guys should take a look a see how he thinks about his baby today and programming languages in general:

http://channel9.msdn.com/Events/Lang-NEXT/Lang-NEXT-2014/Keynote

He said something interesting at some point: I created a language at the time according to the needs of that time, using the resources available in that time...

"Locked my past in the basement...


I found you a perfect replacement"

In my opinion, best C++ replacement is Free Pascal.

I used to program in C, then in C++ and now do so in Java. Fundamentally, they look and behave very similar. Even Procedural languages look like OO ones. Yes, its mostly a matter of packaging.

One day, I want to learn completely different programming paradyns, like those inspired in Prolog.

However, I look at C++ and say how much of it there is that I still haven't mastered. Java is even more of an uphill battle as there are so many libraries and even language extensions to know. I only started to look at Java 8, even though I only glanced at Java 7.

I've been programming for 50 years...must have used dozens of language for actual commercial development. Right now my favorite is D if you need native performance (and your bottleneck is not network/database). All the comments are correct...C++ done right.



Don't be too quick to count D out. Languages sometimes need lots of time to gestate. It's a top 20 Tiobe language.

Beyond D, I like Python...but I do mostlt mathematical programming right now.

"Change the language" is the class.

"Remake a working code in the new language" is the inheritance.

Think that a "better language" make a "better programmer" is the interface.

The magic of OOP is only that people can magically think that a brain that is not able to do telekinesis, can do it only thinking different.

C++ don't does C better than C itself. An editor that help write better C code does it. And improve the C compiler and do some fine tuning of a single world wide known and distributed programming language are the other things to do. Learn an API requeire the time to learn an API. Learn a method require the time to learn the subjective way of thinking of that programmer.

All decently modern languages have good C interoperability these days. C++ interop is a much harder problem, which may eventually become somewhat easier if the ABI standardization proposals are implemented.




Have you actually tried using Julia? You link to its web page saying it is "much higher-level that we'd like." What does that even mean? In Julia you can write code that uses high-level functional abstractions, or loopy array-mutating code that looks a lot like C, or anything in between. You can prototype code as productively as if you were writing in Python, then immediately, interactively examine the JIT-compiled output at the AST level, LLVM IR, or native assembly. And it'll run at comparable speed to C/C++ (almost always within a factor of 2, often closer). There's always a productivity vs performance tradeoff, the interesting thing that Julia allows you to do is write high level logic and scripting, as well as performance-critical inner loops, all within the same language. No cognitive gear change of having to constantly switch back and forth between 2 or more different languages to get things done.

Julia has similar immaturity problems that Rust does, but it already has an excellent REPL and package manager, two things Rust badly needs but has struggled to get right so far. There are academic researchers using Julia very effectively for rendering tasks today. Its primary target use case is scientific computing, but once static compilation of Julia code is more fully supported (right now it's possible but not well-documented) it could serve quite a few more use cases that don't work as well in the current JIT model.

Rust will probably gain more traction in game development just based on the type of users they're targeting - almost entirely C++ people, as far as I can tell. But for specialized numerically-intensive tasks (and I mean complicated algorithms here, not just super-optimized well-understood individual kernels), you're doing yourself a disservice if you don't at least give Julia a try. Efforts in writing GPU kernels look to be at about the same maturity level in both Rust and Julia, but either or both should hopefully be able to come up with something much more usable than Cuda/OpenCL.

DEADC0DE: "I dunno, but I feel like just a "better" C++ for us that really are not too willing to change and are quite settled with a lot of C++ legacy, won't really cut it. A new language has to offer much more than incremental improvements, than fixing C++ issues. It has to be an order of magnitude better, disruptive, and focused to succeed."









I get the feeling you haven't really put any significant time into D. D is not just 'better C++', although it is, it is also so much more. C++11/14/17 is incremental fixes, D introduces new paradigms, suggests some radically different workflows, but it doesn't sacrifice it's compatibility with legacy which you've also flagged as important, and I agree is critical for practical adoption.

WRT legacy code, D can link against C and C++. You can use it alongside existing C/C++ code quite conveniently. Practically all my D code lives alongside my existing C/C++ engine code. At remedy, we used D in a plugin environment (see my lecture I linked prior), this was a great context to wean onto the language without making a full-scale (risky) commitment, by addressing a massive hole that wasn't addressed by other candidates (practical hot-rebuilding/reloading of code).

What 'focus' are you looking for? Go is focused, so is Rust... Go is definitely not applicable to gamedev. It just isn't. That is precisely the result of its 'focus'. Rust is still way too early to tell, and I maintain that it's extreme contrast from the current standards will pose a significant barrier to adoption. It doesn't interoperate well with existing C/C++ code, and that just won't fly.

WRT to the things D distinguishes itself by, it is an order of magnitude better. It has functional programming, which I appreciate as a gamedev, and C doesn't have at all. It's templates are so much more than templates, and offer some very novel opportunities (the D RegEx lib is a good starting point), it's a mistake to confuse them with C++ templates. Reflection! Slices are a novel feature, they seem trivial, but the impact it has on your code is difficult to explain until you use D for a while. Better type/memory safety; D has caught so many bugs in my code, even in my C code indirectly! That's time and money right there.

The thing that most people don't realise about D at a glance, is that while there is a simple migration path from C/C++ to D, that is, binary linkage and no need for programmer retraining (write D code like C/C++), as you become experienced with D, you stop writing C/C++ code in D, and start writing D code. Trust me, there is plenty in D already to have you flirting with many new patterns and approaches to traditionally awkward or messy problems.

I feel that the migration path is of particular practical value to gamedevs though, since it's very unlikely any migration could ever occur if it required a studio-wide retaining of staff one day. And what about the legacy code?

Finally, D *could* specifically target gamedev as a focused niche if gamedevs got involved in discussion and contribution. The thing I've appreciated more than anything about having a responsive OSS community backing the language is that I have successfully taken my concerns to the forums and had them addressed (promptly!) on numerous occasions.

I made a noise about SIMD; we need it in gamedev, it promptly appeared. I made it clear that Win64 was a requirement for gamedev, it promptly appeared, along with many other examples. Get involved and the community will go out of it's way to make sure application requirements are met.

If you're waiting on momentum, as you compared to Go, I'm not sure what you expect... Go is backed by Google, and D has no such marketing department. D trades solely on merit, and I'd suggest that the fact it has successfully climbed into the top 20 tiobe index is a considerable achievement, when contrasted with the others alongside, and the resources backing them.

The most important language in the world is the language of your application domain. From there, the best programming language is determined by the availability of libraries and utilities that support your development objectives. If you're metrics are driven by the core language features, you're in a very small subset of the development community that is guaranteed by economics to be a frustrated minority.




Almost every language that is listed in this post as an alternative began its life as a response to the deficiencies of C/C++ in the context of a specific development domain. They all began life with a fairly focused purpose and a clean definition, and then were slowly corrupted as they were extended as "general-purpose" development tools.

C++ is farther along the road to a mature process of negotiating such changes. Yes, it's slow, messy and political, but among the considerations in selecting a "replacement" is the existence of such a process. That's difficult. Sun tried with Java, and ultimately surrendered.

As a developer of engineering applications and complex host-side user interfaces, OO is critical to my success. Encoding of dynamic real-world state is essential. Abstraction (virtual) and encapsulation strategies (public, private, protected) are essential.

:) nice dispute, I was a Visual Basic user until I discovered WinDev from PcSoft a french IDE.






From now on, i see many faces laugh, but if you don't need to develop a game or a system driver, why programming with a machine language near language? Because many C++ developers are here, searching for work?!

So if you look at the other side, how many hours I need to work to get the job done? What are the costs for me as contractor (not a freelancer)? The customer pays in many cases a fixed price, not paying per hour... so if you get the job done in 100 hours or 30 hours, this is your income?

So I use WinDev, WebDev and WinDev Mobile to get the job done, I don't need to buy several add-ons for my programming language, a powerful programming language, cross platform, multi language GUI, setup and help authoring system, database included and many more, all integrated in one IDE.

So why learning C++? Because all programmers in the world are using C++?? Jump of this train, try different tracks...

yours

Alex

This turned out to be very interesting. I expected people to defend C++ and instead I got people quite strongly advocating D, Rust, Julia... someone also pointed at nimrod-lang, which I didn't know at all.






Maybe it's time to do another language poll like the one I ran in 2011...

But the point why I didn't do so is that I didn't see an actual change since then in adoption of languages for gamedev, and even the languages themselves are basically the same (Julia probably wasn't on the radar at that time).

So instead I tried to put in perspective -why- this didn't happen. Maybe I should not have put this as a critique of a few languages that I've posted just as -examples-, I do actually appreciate them as languages, they are good languages... but having a bit of experience I'm skeptical they will be adopted by us and I'd invite people still to reason about that.

If you feel that D or Rust or whatever is "promising" for -adoption- by gamedevs, why do you think so? What changed?

This article seems to miss the historical point of the creation of C++. C++ was developed as an object oriented scratch pad. Stroustrup, Coplien and many others wrote about this ad nauseum. Naturally it has insufficiencies of style and content. It was made not to do everything well or even to do everything but simply to allow everything.








Libraries, templates and tools are there to allow you to take C++ in the direction you need.

There are two primary problems with this approach in a production environment.

1) Little or no time is spent in design of an application defining what is wanted from the compiler and it's environment. One large by product of this problem is mentioned in the article: the build. This can easily become the octopus from hell if it is an afterthought rather than a function of design.

2) Maintainability. The problem here is one of misunderstanding personnel issues associated with software engineering. In a C++ shop, people will ask a dozen flavors of: "Do you know C++?" A better form of this question is: "How did you learn C++?" Because of the scratch pad nature of C++, they're going to have to learn the new environment. It won't have all the ramp up of learning a new language but it will be longer than most environments and will have substantial similarities to learning a new language.

There's much more to say about why other languages will not replace C++ in the foreseeable future. Here are some quick shots: It performs too well. There is a staggering $$ investment in it. It is flexible beyond all belief. Whatever your complaint about it can be addressed by a library, tool or environment. If it isn't, then you can make you're own...probably at least using pieces of other people's.

I argued C++ in place of fortran for years. In some pretty fancy national labs fortran still rules (I lost).

I don't really have a lot of sympathy for C++ haters. Yeah its ugly, but you can do anything you want with it. Just avoid what you dont like.

Try getting anything done in fortran.

Eamon: "Metaprogramming is clearly the reason C++ is successful. It's also clearly horrible in C++ today; but without it you'd need to change the language every time you want to introduce new fundamental types (say, vectors & matrices for gamedev)."






Eeeeh? A type system is what you need to introduce new types. About metaprogramming though, I've made a new post you might like

Walter: If I might advice, try learning SML or F# as a new language instead of Prolog. Then probably you'll appreciate C# and hate how slowly Java moves

Anon: I changed the reference to Julia as it was unfair to link it to the phrase I did link it to.

Brian: agree

Anon/2: definitely you don't need to go low-level in all application domains, even if to a degree being able to develop a mental model that goes all the way down always helps because there will be times things don't go like you think they should and you'll need to know exactly what's happening and why things aren't working. During these times knowing how things actually work will make the difference between someone that kicks a computer, reboots and reinstalls windows because it doesn't work from someone that can actually fix things. Not everybody needs that level though

SciBoy: it's not that because Fortran is not great that C++ becomes great. I cite Fortran sometimes only as a rebuttal to people that say C++ was made for performance, pointing that Fortran which is ancient understood performance much better (aliasing). But it's actually a miracle that the first programming language we created is still somewhat usable and used, actually!

"Things like FreeBasic provide much-needed therapy and a return to sanity and a correct appreciation of people. The arrogant folk really hate a word like 'Basic' - fine, and good riddance." ~ pragmatist

D, without GC, it would be the perfect replacemet for C++.


Anonymous: You don't have to use the GC, you can use custom allocators, see http://wiki.dlang.org/Memory_Management

DEADC0DE said:



> With that I mean that if I make my game 10% faster and make it crash 10% less, chances are that it will translate in around 0% more sales.

I disagree, and I think you're looking at it wrong. Instead of analyzing how many more copies of a game you're going to sell because a game's faster, look at how much sooner you're on to the next project (at least from an engineering pov) because you don't have to spend that extra time optimizing the engine to hit some fps goal. Or maybe you can spend the time you would have spent optimizing on some other really cool tech feature that *will* directly sell more copies. The same argument holds for "less crashing," I believe.

Those categories of improvements may not appear to directly improve ROI, but they do indirectly.

Anon: I don't argue that better code is better. I'm just saying that I think the reason we don't see money thrown at that problem is that it's much harder to quantify how much money versus how much you'll spend you'll make by having a language that somehow makes easier to optimize there or have less null-pointer bugs here.


While other fields of engineering have an immediate connection between for example milliseconds and sales, thus you can go and say, this technology will shave this amount of ms which will make this money, and you're much more likely to persuade people.

I think templates are great. What do you recommend as alternative?



Macros, duplication of algorithms across types or void* functions?

Truth is that yes OO is bad, and it's a shame that C++ makes it convenient to use. But you don't have to.

C++ does bring a whole lot of good things compared to C though.

It would be great to have a perfect replacement for C++. But I would pick C++ over C any day.

Jouan: generics for generics (see C#), hygienic macros for metaprogramming (which I don't love, but see lisp for an example of that).



C++ Templates are born out of sheer ignorance, they -clearly- wanted just to be generics but not knowing how to do generics right and safely as types they were implemented just as a code copynpaste instead thus allowing a lot of abuse and zero possibility for tools and debuggers to understand anything of them.

DEADC0DE: "If you feel that D or Rust or whatever is "promising" for -adoption- by gamedevs, why do you think so? What changed?"



I've already repeated a number of times, but in short, WRT D, it is reaching maturity.

The reason I back that horse is primarily for practical reasons, the migration path is PRACTICAL and realistic. In addition, it has excellent backend support (reference compiler + GCC + LLVM), performs very well, has a community that is sympathetic and responsive to users requirements.

It's not a fantasy like Rust, you can get to work with D, right now. I've already done some work proving D on consoles in the commercial AAA environment, and specifically addressing the rapid-turnaround thing that you seem to be most excited about.

D needs users. It's the D users that drive development, not corporate interest. If significant number of gamedev's take an interest, their requirements will become prioritised, and I've been amazed just how fast the turnaround can be when addressing critical issues.

For me safety (at least w.r.t. games) is entirely about productivity. We spend a lot of time chasing mysterious behavior caused by memory safety issues, and we also spend a lot of time chasing down mysterious behavior caused by the language encourage (or even requiring) an overly stateful style of programming.






Another point is that automatic refactoring tools can work much better with languages that are a bit more principled, *and* people will feel more confident in doing it. This makes it easier to fight code entropy as you go.

I do think high level features (such as nice, low cost iterators, cheap lambdas) have a big impact on productivity. They can reduce the amount of code you have to write and maintain, and thus reduce bug counts. They also make it easier to provide "macro-like" domain-specific helper functionality without having to reach for the big hammer of actual macros or template meta programming.

More importantly though I think you need to make the language *pleasant to use* in order to make people switch. Something that's on the same level as C w.r.t. safety and productivity but with faster compile times is not going to make anyone excited enough to cause a huge industry-wide change.

I think people would love to have a language that's higher level than C, with many of the nice high level affordances of Haskell, without costing performance or safety. It doesn't matter if you think that C and C++ is completely workable today, I don't think anyone will switch unless the new language is simultaneously better on everything including being more pleasant to work with.

Go and D does have fast compile times, but then compared to C and C++ so does Rust. It's doing more stuff in its type system so it's likely it'll always be a bit slower, but it's not *inherently* slow (unlike the C/C++ compilation model).

I'm not sure you'll convince people to switch to D or Go just because they compile fast (language encourages GC, allocations everywhere, etc. and just generally not enough improvement in programmer ergonomics and bug reduction.

This is really nice discussion, especially given the really cool embedded links (kudos for that), but it reminds me of a strikingly similar discussion I had with friends a little over 40 years ago.














At the time, we had this very lengthy discussion about who was going to replace the Beatles as the next "super group"..

And as I recall, not once did it occur to any of us that it would never happen.

Well, it never did. As everyone already knows by now, no musical group has ever come close to achieving the near-universal appeal of the Beatles. And in all probability, no one ever will..

My point is that the same can be said about the C language. Think about that for a moment - most of you are probably too young too remember it, but before K&R revealed C to the world, all computer languages (all, what, eight of them) were classified as either "high level", or "low level", and everyone and their brother agreed on that classification. Then C happened, and shattered that myth into a thousand pieces. Not only that, but K&R also included LEX and YACC into the mix, which made it painfully apparent to everyone that any program written in the C language could itself easily be used as data for the purposes of, among other things, implementing any form of meta-programming you care to imagine.

Of course, as we all now know, that last part never happened.

Why it didn't happen is a sordid story of rampant stupidity and ineptitude, but to make a long story short, there may still be time to get there.

What I mean by that is that the next "big thing" in software development will (hopefully) be when everyone wakes up from their language-centric slumber, and realizes that software development can be, and indeed should be, a multi-tier process. I can envision that so clearly: the C language would be used almost exclusively to express algorithms, and one or more meta-programming languages, whose input would come from YACC's output, could then be employed to *implement* those algorithms, using the C programs as data.

And since the output of all of the meta-programming languages would be C, the system could even be expanded to include a third tier, one that would manage and control feeding the output of the second tier back in to itself..

We programmers have got to stop thinking so one-dimensionally about computer language. Thirty years ago, the software industry was given a gift of immeasurable value - the C language - and what did we do with it? We almost immediately perverted it to include, of all things, some "paradigm" that was fashionable at the time. Disgusting.

C is like chess - you don't need to "improve" on it, you need to *build* on it.

Attempting to "Improve" the C language only makes it less usable as the natural language for expressing algorithms as data for any number of meta-programming tiers..

Short of that though, I don't think there will actually be a "successor" to C++, any more than there was a "successor" to the Beatles. We now live in a world where there is well over a thousand different computer "languages". Compare that to the number that existed when B.S. (Bjarne Stroustrup) came up with C++.. It's a different world now, and there's no going back..

DEADC0DE : As a game programmer, generics as in C# do not exist (C# is just too slow for engine programming, and also, I'm not sure of how radically different they are from C++ templates. I'm no C# expert though...).


Macros are just horrific (plainly impossible actually) for debugging. Templates, while not perfect are just way better when it comes to debugging. Also the syntax is much more understandable. I have witnessed some macros that are just crazy. I think lisp heavy usage of macros only exist because of the massive overhead of function calls...

I don't see any reasonable alternative to templates right now.

But I agree with you overall. There is a better language to be designed that doesn't carry all of the flaws of C++. I even have a few champions in mind but none of them are ready for prime time in my opinion.

Jouan: I'm sorry, but you should look at the things I pointed to before replying. I said generic types as in C#, now if you don't know C# well and don't know generics you should have a bit of curiosity and check how they are different than templates, before commenting (or just don't). The same goes for -hygienic- macros as in lisp, I didn't say C preprocessor macros, I made a precise example and if you don't know how these works I hope that can pique your interest and curiosity.

Anonymous: the problem is not C, is C++. And while I can accept that C is actually quite fine in its musical genre (improvable for sure, but there is hope it will improve through further iteration), C++ is playing quite out of tune, so much that people are starting to be nostalgic for the classic sounds. We can't go back to pure C, but C++ is a big pain. Other fields found their new idols, we are part of the few left behind.

Sebastian: I see what you're saying, and I do agree. Better is better. I just don't have confidence that's enough, that one day there will be something just like C++ but so nice, so safe, so sparkling and we will jump (if so, then we should be using D!). Well, that could happen if it was really a zero-cost investment, but it's unlikely.


Instead I think that we could jump regardless of how nice a language was if it brough a disruption, an order of magnitude change in something we really care about. And games, as an art form, really need iteration and experimentation, thus my bet is on live-coding.

If I'm going to use an Object Oriented implementation domain, I'm going to choose Smalltalk or Python. Why would I choose what was initially a structured language, morphed into a sad bloated Frankenstein that nobody uses consistently anyway?

from DEADCODE: "We can't go back to pure C"..








DEADCODE - stop right there. Please step AWAY from the keyboard..

If you read my post again, you should be able to discern that I never once advocated going "back" to C - that makes me sound like some kind of fanatic. What I was trying to explain is the concept of using C as the language of choice for transforming algorithmic information into retrievable data (through the use of either YACC or BISON, take your pick), which can then be processed further by one or more "tier 2" programming languages, where meta-programming and whatever programming paradigm of the week can (and should) reside.

C is perfect as a "tier 1" language, because it is powerful enough to encapsulate almost any algorithm, and yet at the same time is simple enough to manifest as retrievable data. Both are necessary constraints for an optimal "tier 1" language.

As I intimated more than once in my original post, this would represent a "multi-tier" approach to programming. This is not such a radical idea. In fact, in every other field of human endeavor, from mathematics to manufacturing, they're reaping enormous benefits from the very simple idea of building machines that build machines. Isn't it time we took the hint?

Well, I have to admit, that's probably not going to happen anytime soon, because software engineers are not really "engineers", are they? They just call themselves that to convince other people that they actually know what they're doing.. Right?

Did that sound bitter? Was that too much? Yeah, well, you earthlings are all so.. wait, I've said too much, I need to go..

DEADCODE: I don't think metaprogramming and the type system are fully separable. I mentioned vectors+matrices - while you can implement those "just" in the type system, doing so well is going to be hard.



You've mentioned C#/F# a few times; for example in such type systems expressing fixed size vectors and matrices is not possible (certainly not in a generic yet type-safe way). And even once you've expressed your vectors somehow, you want to define operators on them flexibly - i.e. you want to exploit the kind of expressions and sizes of the vectors in questions.

Hence, you want a compile-time code generator of some sort. It's no just vectors; D uses this for a regex implementation; you could use this for (de)serializers, ORMs, reactive datastructures, readable assertions... whenever you want to compute new behavior or types based on existing types & behaviors.

Anon: the problem of building languages on top of C is that it makes tools a nightmare, for example you entirely lose source-level debugging. While it's good to have a C backend for future-proofing a new language (C won't die, so worse come to worse the C backend will enable you not to lose code), it's not a great idea -at all- to just build on top of C. LLVM would be a much better target for that tiered approach and in fact that's what I advocate in the article


Fernando: code iteration, that's to say the time it takes from making a change in code to see the results, in C it's the time of the edit/compile/link/run cycle, other languages allow interactivity (see REPL)

from DEADCODE: "..it's not a great idea -at all- to just build on top of C."



DEADCODE: You are most certainly entitled to your opinion, but there are most certainly others:

https://en.wikipedia.org/wiki/C--

Anon out..

Anon: I provided clear justifications, not just opinions.






C-- makes lot less sense now that LLVM is so widespread, in fact I don't see really a lot of languages implemented on top of it...

Not to mention that compiles only down to x86, really, not a great example to bring forward.

GHC was but now it has its own native generator (and LLVM output too), and anyhow haskell has its own debugger.

In fact even in LLVM, which is a great backend nowadays, the debugger problem is not yet entirely solved as LLVM doesn't emit PBDs so it doesn't support Visual Studio. See http://dsource.org/projects/cv2pdb

I'm surprised that RAII hasn't got a mentioned here. It's central to resource management in C++ but ancillary or absent from just about every other language. It's the reason C++ got away with having no GC for so long and why C++ classes are so effective at taming low-level C APIs.





While far simpler and safer to work with, neither reference-counted nor tracing GC provide the same predictable performance guarantees. This is typical of the sort of trade-offs games programmers historically have been willing to make. No other language reflects this desire for high level features to be coupled with a lack of compromise over run-time performance versus development cost.

I'd like to think this degree of inflexibility was losing ground but it doesn't change the fact that stall-happy GC is seen as a deal breaker. So we're left with a 'good-enough' solution that is all but ubiquitous.

I do think that D is the most promising contender out there, but while it barely runs on anything other than PCs and while it's memory management is seen as a problem - rather than a solution, it's just too hard a sell for games.

JMcF

John: D and Rust have RAII. Languages like Java, C# or Go have "explicit" RAII via using (defer in go), which is actually -better- as it makes clear that you're dealing with a RAII type.



Also it might be that in very logic-heavy, asynchronous applications RAII is actually a must but in the code I write (rendering engines) it's really not.

We have quite strict control over performance and resources, we monitor them, and not too many code paths, mostly kernels that transform large amounts of data.

So in the end, RAII is not that unique, it's in other languages either just like C++ or in better forms, and in my experience and domain it's not even a deal-breaker not to have it.

Sometimes I wonder if it's that I have a different set of experiences or if really is that certain concepts are taught as solution to given problems, and people just apply them and recite the same stories of the problems that were solved... without ever really experiencing them.



Memory double free, null pointers, leaks, explicit malloc/free management or resource acquisition and disposal...

All these things are not huge issues in my book, you write some code, test it, with good logging/debug instrumentations (debug heaps and so on) you catch errors quite on the spot. And automated tests on the build machines do the rest.

Yes I've chased a few allocation related bugs in my lifetime, but was never the plague of issues sometimes people paint...

I think we have different ideas about what RAII means.

I must confess to only skimming through some of the comments, but it seems everyone is referring to C++ in a 'Systems' like environment. What about embedded applications running on limited resource microcontrollers ?

I write applications that must run on 50Mhz processors that have 128Kbytes of program memory and 8Kbytes or RAM. I cannot imagine using a language with heavy runtime overheads. Is there anything to replace C++ (or C) ?? Sometimes the only alternative is to code the solution in assembler... Aargh!

John: I doubt it


Anon: I'm not experienced there, my perspective is the one of a (console) rendering engineer.

Anon: Just like C/C++, D does not require linkage of its standard runtime.

Many people have written to-the-metal programs in D by not linking the runtime. D offers the same bare-bones environment as C/C++.

There are a couple of language features that depend on the runtime, but they are easy to avoid, and there's talk of a compiler flag to make use of those features generate compile errors for use with bare-bones software.

If I understand it correctly, Go's defer is much the same as D's scope(exit) and shares a similar aim to Python's with: they all trigger code - typically clean-up code - at the end of a block. They are necessary because object destruction is at the mercy of the GC: a tracing GC decouples lifetime from scope. They are not RAII. They are OO-free alternatives to it.


RAII in a memory-managed language is unremarkable compared to GC itself. C++ is an exception because it lacks inbuilt GC. (Ref-counted objects in languages such as Python and C++ do not guarantee lifetime.) RAII an oft-overlooked aspect of C++ with an woefully unhelpful name but it's helped keep the language alive well past its time.

John: just as I said on the D forum, RAII is -nice- but I don't think it's a must have, at least not for me.







In the code I deal with the best use of RAII is for scoped locks. Which you can imagine is a very nifty thing to have but it's also very rare. Other usages I can think of is profiling or logging blocks, again nifty to have but I won't be too bothered if it's missing.

Also it's true that things like c# using are due to the way the GC works, but it's not crazy to argue it might be better in general. It makes explicit that a given instance of a type is not like all the others but it's instead something that deals with resources.

John: also it's not a particular strength unique to C++, as I wrote most (all) other OO languages either support RAII as in C++ or have chosen to use a specialized syntax because well, they thought it's better, but one way or another you can replicate the behaviour

DEADCODE - using or try-with-resources are not RAII; nor are they nearly as practical and easy to use.






One point of RAII is that it's *easy* to use correctly. You cannot by default forget it; if something needs cleanup, it *will* be cleaned up, without need for special programmer attention. In a less "unsafe" language, the RAII pattern could be even safer (Rust/D perhaps provide that), but even in C++ it's unlikely you'll make a mistake.

Furthermore - and this is perhaps the most critical aspect of *any* software device - it's composable. The only way we have a hope in hell of controlling large systems as we need to do every day is by decomposing them into smaller parts. Virtually every major programming technique at some level is a solution to this universal problem - whether it's OOP, functional programming, parallelism by message passing. Composability is what makes programming practical.

I love C#; I maintain lots of C# code, and I think C# using is a good addition to the language - and I'm sure java's equivalent is just as useful. Nevertheless, they're terrible in comparison to RAII - it's *easy* to make mistakes because the compiler cannot detect when you forget to use using when you should. This isn't just a question of better compilers; lots of scenario's in C# require the use of IDisposables outside of using clauses - a really prominent one being Task<>. This is bad enough when you're writing code, but it's really terrible when you're refactoring code. If you move a resource about, then it's almost impossible to verify that the previously resourceless object is now used correctly as a resource without manually inspecting every single usage in an error-prone fashion. If you make a mistake, you probably won't notice until it's really expensive since most resource leaks aren't problematic in testing.

But the worst part about IDisposable is that it's not composable. There're no easy way to compose multiple IDisposible objects into a new IDisiposable object. The appropriate pattern to do so is complex; need correct usage of virtual method calls in it's default implementation, needs to account for finalization too simultaneously, really should be robust vs. exceptions in dispose methods (which makes for really messy heavily nested code in the wrappers dispose), and it's all not statically checkable. If you make a mistake, you may never find out. It's not just a lot of work; it precludes the usage of standard containers. A List<> of IDisposables is not itself IDisposable; a Tuple<,,,> with some IDisposable members doesn't implement IDisposable for you; anonymous types dont' work, Dictionaries don't work, etc. etc. etc. You basically need to reimplement the wheel. To add insult to injury, when you do reinvent the wheel, you'll also need to pay through the nose since such abstractions are anything but free in .NET.

I much prefer writing C# to C++, but I cannot for the life of me understand why anyone would prefer C#'s approach to resources over C++'s. It's so bad that I've used small bits of C++/CLI in otherwise C# projects just to implement the resourceful bits, because C++/CLI does the messy work of composability for you.

... EBay with a new site that is practically identical to EBay but with a better interface...




Yeah right. Listen to that for a change: https://archive.org/details/dconf2014-day-01-talk06

Then maybe... you'll put a hold on such constructive comparisons.

So you want a language to replace C++

Write your own. Everybody else is.

You know what you want. Just do it.

If you're looking to "replace c++" then you're solving the wrong problem. c++ is still around because it serves its niche rather well. Sure c++ gives you enough rope kill hang yourself. If you're a mountain climber would you want less rope than that? Rappelling with 3 foot bungee cords?



OOP is/was overused but is still useful. Design patterns also became oversubscribed, but are actually useful to not repeat the mistakes of the past. 20 years from now folks will probably be heaping scorn on the abundance of frameworks, VMs, and functional programming. I think you should assemble a good set of languages to accomplish a range of tasks. Personally the set c, c++, python, java (plus maybe scala in future) cover the sort of problems I've faced.

Still any language created to be the "next c++" is deemed to fail. They try to solve what they assume being defects because from their perception (use-cases0, they are indeed defects. But most of the so-said defects are features; and killing features do not make it better.






The only language that try to fix c++ problems is D and as you was fast enough to dismiss it, I don't think you are really looking for a c++ replacement.

From what I can see, you would be really really happy doing Javascript, so go for it!

Something I experience daily and I think is what you are experiencing is something called "aging". We accept some tradeoffs that we would not accept when younger. We are tired of dealing with "problems" because they are more annoying than problems and we start looking for alternatives.

And seriously, Rust, Go and Swift are very very far from being usable on perfomance critical systems.

As someone said on comments, the problem with the game industry are the constraints of outdated tools (even Visual Studio) and I don't see engineering as the time-sink, most of the problems are data build related and that does not need to be c++ to solve. Cut the data build to improve your iteration time and then we have something that can be then pointed guilty and compared to web dev.

@Anon: D is far from being usable in realtime critical systems. The reason is simple: the GC. You cannot stop the world just to do some unbound cleanup.

I work with a guy that thinks like you, his code is a ******* mess. Coherency and dependency issues all over the place.




I agree that the hierarchy solution was and has been over done but thinking in an object orientated way whilst coding will save you from the curse of C bug 'who changed my variable' debugging nightmare. People who think C++ is no good and also think that OO is pointless are the same people who have failed to keep up. Instead of refreshing their skills they throw their weight about saying it's all rubbish.

I'm an old school 8bit coder from the 80's and c++ is a great language and OO coding is very powerful and helps to avoid errors and improves maintenance.

Thanks for that article! That was interesting to read. Found something new for my self.

Interesting read. I wonder if anything changed in 6 years.







Also, any thoughts on Jai?

I've gotta agree that a killer feature nowadays is iteration time.

I started programming with Turbo Pascal on a 486, at 33mHz. You pressed ctrl+f9 and saw the compiling messagebox just blink before you were running the program. It was so fast I was constantly recompiling only to check for syntax error.

How comes we can't do it anymore with our multi-core gigahertz beasts with tons of ram and SSDs?

I still have to check freePascal/Lazarus. If it's still as fast it might be good.

Fast forward 20years and I've found a semi-equivalent with C#. We were 2 guys for 2 years (+a 3rd for a couple months) and we pulled off a whole game with tools, online, everything. (You might have heard of it, Streets of Rage 4) We probably would never have made it in that time frame, and at that quality level, if it wasn't so quick to iterate.

The VS integration is also much better than for C++. For example, renaming stuff is a breeze. There's no obstacle to keeping stuff clean. Makes life easier.

If I had to go with a rendering-heavy game, I'd probably make a thin rendering lib in C, and call it from C#. Mostly because I haven't found good C# bindings for DX/GL/VK yet. And I don't want to copy textures from unmanaged to managed to unmanaged to vRAM.

Ppl here put lots of emphasis on performance, but we're not writing drivers (anymore). The two areas where you need perf is graphics which is done with shaders, not C++, and physics, which is probably done in a 3rd party lib already. Moving gameplay code from Lua to C# and more importantly back in the actual codebase can't be such a bad thing!

I don't know why, but why doesn't everyone use C and the features of C++ that you pick and choose? For example, I only use templates if it offers distinct code paths that provide better performance (by leveraging if constexpr possibly, or the templated variable in the function).

Other than that, templates are rarely used, too much trouble with everything being in a header file... including in a header file more header files is far more complicated than including a header file in a source file.

I use classes and structs, typedefs, inheritance even multiple inheritance (though rare).

I use and experiment with new features from the language, but If I don't like it or am not interested, I don't use it. For example, structured bindings, there nice to return from a function, so I use it.

I use all the features of C, and pick & choose from C++

Now if only I could keep the compilation times to a reasonable.....

Post a Comment