---
title: 2011 Future programming languages for games - POLL
url: http://c0de517e.blogspot.com/2011/05/2011-future-programming-languages-for.html
published: '2011-05-08'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**Prerequisite**:

[this](http://c0de517e.blogspot.com/2011/04/2011-current-and-future-programming.html).

It took some time, but here there are, the results of the 2011 Future Languages for Games poll. I have to say the poll itself could have been better, I'm sorry but it was my first experiment with SurveyMonkey.

Nonetheless, I've got 174 responses that is fairly good, considering the subject…

Let's begin reviewing this data… from the end, the questions about expertise.

The majority of people that answered the survey self-rated themselves as "hobbyists" (25.6%), followed by a 23.3% that just started working in the filed, 21.1% that worked for at least 3 years and shipped at least a title, 18.9% of very experienced professionals (technical directors or equivalent) and the remaining 11.1% claimed to be working for at least 5 years, shipping multiple titles.

Most people claimed to know a few languages and to be interested in knowing more or to even use multiple languages and paradigms in substantial projects. (37.8% each). A few know only one or two languages, the ones they use at work (10%) and some claimed to be languages gurus having used many languages and designed some of their own (14.4%).

Now this sounds a bit atypical to me, it might be related to the topic of the survey itself (most probably) and also a bit to the fact that less experienced programmers tend to overestimate themselves, so I expect them to be more accurate in the question about expertise, which was stated in more strict temporal terms, than the one about knowledge.

I don't have a professional account, so I can't do correlation analysis, that would have been handy. Next year I'll also setup multiple gathering links, so I can see which audience I have from which sources (reddit, my blog, twitter…).

The "meat" of the survey was of course the question about which programming languages are in use today for games, and which ones would be preferred if the subject were to start a new game engine from scratch today. Let's see:

Pure C. Today: 30. Tomorrow: 30

Pure C++. Today: 66. Tomorrow: 53

C++ extended via tools. Today 22. Tomorrow: 20

C extended via tools. Today 9. Tomorrow: 7

Java. Today: 8. Tomorrow: 7

C#. Today: 32. Tomorrow: 29

D. Today: 2. Tomorrow: 12

Objective-C. Today: 11. Tomoorow: 6

OpenCL. Today: 7. Tomorrow: 10

Erlang. Today: 3. Tomorrow: 2

ML-Famliy. Today: 3. Tomorrow: 6

DSLs code-generated to C/C++. Today: 2. Tomorrow: 1

DSLs, compiled. Today: 2. Tomorrow: 2

DSLs, interpreted. Today: 3. Tomorrow: 1

Lua. Today: 35. Tomorrow: 34

Proprietary scripting. Today: 13. Tomorrow: 4

Other scripting languages. Today: 12. Tomorrow: 15

Python. Today: 8. Tomorrow: 6

Haskell. Today: 2. Tomorrow: 2

JavaScript. Today: 3. Tomorrow: 2

No big surprises here. Today's languages are C++/C, Lua and C#. DSLs are not so popular, and proprietary scripting systems are still the first alternative to Lua, with all the other scripting languages trailing behind.

The question also asked for language usage in the "high-level" and "low-level" components of the engine. It's interesting there to note that C is used today mostly for the "low-level" while C++ scores almost equally for "low" and "high". C++ extended via tools (i.e. code generation) is on the other hand mostly for the "high level" as all other languages, with D being the only exception.

For the future, C remains stable, while C++ loses some points. Also, proprietary scripting and DSLs are not sense as a good alternative for the future, probably recognizing the difficulties that engineering a language entail.

Surprisingly (to me at least) C# does not rise either, while D seems to be a language quite a few people are hoping to use. No other language registers such a sharp rise, it seems that people still want the next C++ to look very similar to C, rather than a higher level alternative.

Speaking of programming paradigms, it seems that none is really neglected, everything has its use. Imperative and stream/dataflow programming are the champions of rendering, functional, declarative and actors are seen as suited for AI, while OO and events (reactive programming) are still strong for Gameplay. Asset loading is quite obviously dominated by data-driven strategies, together with generic/template based, that are strong also for the build system part of the problem even if in that case, declarative programming seems to be the preferred choice.

Next question was about which languages are most known, most liked and most likely to be used in a game. C++ is the most well-known language (68.2% say "a lot"), and the most likely to be used in a game (52.3% choose "a lot") but it's comparatively less liked (36%).

C is of course very well known as well, and most people say they know and like C# well enough, even if there are way less "C# experts "than C++ (and that might be the reason why many C# tools are so slow, and so many people have wrong ideas about GC and related concepts. C# is deceivingly similar to C++, but we are all C++ experts and often reason "in C++" also when coding in other languages, thus making naive mistakes).

Lua is a lesser known and liked language, but comparatively many people are willing to use it, a sign that it's probably seen as a language for designers, to be added to an engine but not used by the engine team itself.

All the other languages are not nearly as well known. After Lua we have Python, Javascript, D, Scheme/Lisp, Objective-C and ML-family.

Among the tools to create languages, code generation and code parsing still score more points than the relatively "recent" LLVM framework. Compiler-compilers are also not so well known but as it happens with LLVM, the few experts that know these tools tend to like them at lot. LLVM scores well also in the suitability for games field.

Last but not least, I asked what feature of C++ make it so suitable for games. Of course the first and foremost is "platform availability" (selected by almost everyone, 86.8%), followed by the ability of directly manipulating raw memory via pointers, encapsulation in classes and the compile-time knowledge of type size (67%).

Function pointers and Templates are still seen as a very important feature, followed by const-correctness and inheritance from interfaces (inheritance from concrete classes and multiple inheritance are way less popular). Surprisingly (for some) explicit new and delete and destructors (RAII) are not so high in the list, and half of the respondents don't deem them as being so important. All the other features have smaller numbers, the least liked being the STL, RTTI, Multiple Inheritance, Exception handling and reinterpret_cast.

For C++ I also asked which features where perceived as being well-implemented. Now, among the ones that are scored well for their practical usage, the worst are related to the object system, in particular inheritance, overloading and templates. Memory management is also not really loved, and in general, no C++ feature seems to score really high, the most liked are the ones of C heritage, in particular platform support and pointers.

So in conclusion, what did I learn?

Well, quite a few things I have to admit. C++, even if it's showing its problems, is less hated overall than I expected, and its "better designed" cousin D seems to be have a few people hoping it will be a protagonist in the future.

People are looking everywhere, considering many different paradigms but still even if there is quite a lot of interest for many different things, only a few languages are really well known, the usual suspects (C/C++, C#, Lua…).

So what are you doing still reading this? Go,

[download a language](http://msdn.microsoft.com/en-us/fsharp)and start using it!

## 2 comments:

Great sum up!

LOL, why did you linked F#?

Post a Comment