---
title: What OOP Isn't
url: http://hacksoflife.blogspot.com/2010/12/what-oop-isnt.html
author: Benjamin Supnik
published: '2010-12-09'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

(If you're wondering how this works, most list editing operations had to be stack-recursive - a node would set its 'next' to the return value of a call on its next, allowing a node to 'cut itself out'. It made it very hard for students who had never used linked lists to understand what was going on, because they had to learn recursion and linked lists at the same time. The result was something with the performance of LISP and elegance of C++. It was horrible.)

They told us that OOP involved encapsulation, polymorphism, and inheritance; I have commented in the past on why this last idea is

[often just a poor idea](http://hacksoflife.blogspot.com/2007/01/inheritance-of-implementation-is-evil.html). At the time, in school I only had enough programming experience to say that what we were being taught (all OOP, all the time, period) was a lot more difficult than what I had been doing (use an object for something big, like a game character) and was producing code that was more verbose and not particularly fast. Now that I have some software engineering experience, I think i can articulate the problem more precisely.

When talking to a new programmer who is looking at OOP and trying to figure out what it's all about, I say that the relative importance of encapsulation, polymorphism, and inheritance is approximately 90%, 10%, 0% respectively. The vast majority of the value of OOP is that it provides an idiom to keep one piece of code from becoming hopelessly intertwined with other pieces of code, and that's valuable in large software projects. It's also impossible to teach to undergraduates because they never have a chance to write enough code for it to matter.

Polymorphism is nice, but in my experience it's not as useful as encapsulation. If you have a polymorphic interface, you have an interface, which means that it's encapsulated...but there are plenty of cases where an interface is one-off and has no polymorphic properties. Maybe 90%-10% is harsh, but I think it's the encapsulation that matters. It may be that some product spaces are more polymorphic than others. WorldEditor (LR's open source scenery editor) has polymorphic hierarchies for most of its core components, while X-Plane itself has very few.

I bring this up because I'd like to advance (in a future blog post) a comparison of OOP techniques to others (for real software engineering problems), but OOP

[comes with a bit of baggage](http://en.wikipedia.org/wiki/Object-oriented_programming#Criticisms). The notion that OOP would make us better programmers, help us write bug free code faster, or help bad programmers become good programmers have all proven to be naively optimistic. (In particular, bad programmers have proven to be surprisingly resourceful at writing bad code given virtually any programming idiom.)

So I'd like to define (OOP - hype) as something like: good language support for idioms that make encapsulation and sometimes polymorphic interfaces faster to code. And that's useful to me! I could code the same thing in pure C, but it would make my repetitive stress injuries worse from more typing, so why do that?

Benjamin,





ReplyDeleteWe have never met. In fact, I just started reading your blog because of my interest in XPlane.

At any rate, I too am a Software Engineer. In fact, I interviewed a candidate two days ago who was fresh out of school and I, it not quite the same words, asked her to talk about some of the advantages and key features of OOP. Honestly, having asked this question before I expected Encapsulation, Polymorphism and Inheritance but this candidate bumbled around the question and eventually landed on inheritance. When I asked her what made inheritance so great, she blurted out code reuse and wasn't really able to articulate further.

While somewhat of a stretch, I think that reflects the core of my problem with your rant on inheritance. Your argument discards the concept based solely on its misuse as a "code reuse" vehicle. If it was solely about code reuse, I believe it wouldn't exist. There are much simpler and cleaner ways to go about reusing code.

In many languages, inheritance is the vehicle for polymorphism. It affords a level of logical abstraction that makes the world a better place especially when more than one developer is working on a project. Or, heaven forbid, someone other than the author has to maintain their code. I believe a procedural code fairy dies every time inheritance is used correctly :-)

I've been a software engineer for over 10 years professionally, and programmed almost 10 years more unprofessionally (taught myself programming as a kid).


ReplyDeleteIn the past I used to believe in OOP, then changed my mind and started to believe in minimal OOP.

Nowadays I'm leaning more towards data orientated programming and writing code as simple and maintainable (extendable & rewritable) as possible, and only building what you need *now* because it's almost impossible to predict how you will use pieces of software in the future.

If you try to make something generic (something which OOP almost demands of you) you will always waste time on writing stuff that never gets used, and you will always miss some functionality that you'll need to implement later (which usually means rewriting a whole chunk of code).

In the end, it's better to be pragmatic and minimalistic when writing code.

Just my 2cts

@david: loved the fairy death mention ;)

ReplyDeleteHi David,





ReplyDeleteOf course you're right, in a language where polymorphism is actuated via inheritance, I can't _really_ plausibly give inheritance 0% value. :-) I suppose a more nuanced assault on inheritance would go sometihng like:

- Inheritance of interface is just groovy when you want polymorphic interfaces.

- Inheritance of implementation is often harder to manage than composition as a way of combining components.

- Inheritance of implementation doesn't inherently provide better code reuse compared to composition.

I think LogicalError's observation is spot on ... often it's better to write less code and not try to pre-solve an area that doesn't need to be solved. Not only does this avoid unused code that has to be maintained, but (in my experience) you can write the best code when you have expertise in a problem domain; if you aren't even going to _use_ the code, often this is correlated with not being an expert. (That is to say, don't design for the future until you've designed the future.)

So ... I think my real decision on inheritance with implementation would be based on my expected refactoring. If I am going to make a UI class hierarchy (like in WED) and build 50 UI classes at once, I'm going to inherit implementation, try to use patterns like "template method" to control the chaos, and be happy.

If I am going to make a library of components that I am going to put down now and maybe pick up one at a time over 10 months, or extend incrementally, I might prefer the simplicity of composition.

Inheritance as a vehicle for polymorphism is in fact one of the biggest _problems_ with many OO languages -- that they encourage that, or make it the only vehicle. Code-reuse (inheritance) and interface-reuse (polymorphism) ought to be decoupled, so you don't end up doing one when you mean the other. One of the problems of using inheritance for polymorphism is when you later want a type that matches _without_ reusing any code, suddenly you're trapped. That few OO langauges make it obvious to concisely use polymorphism without inheritance is what gives OO a bad name.

ReplyDeleteI think we risk chaos of terms here.




ReplyDeleteInterface re-use and implementation re-use are clearly different concepts.

But inheritance, as a C++ monkey like me thinks of it, isn't clearly _either_, because the term is used for _both_ implementing an interface and deriving from an implementation. Hence David's original post that you can't have polymorphism without inheritance in C++. (And I would argue that if you derive from an abstract class in C++, this is "inheritance" as C++ defines it, but is not code-reuse.)

This is why, while I am not a fan of Java, I can understand the limitation of multiple inheritance to abstract classes/interfaces only.

I think you would find polymorphism pretty tricky without inheritance ;)



ReplyDeleteI think there's truth in a lot said here. LogicalError's comments tout practicality or purism, which makes a lot of sense. I just feel sometimes programmers use this as a rationale to justify short sighted code.

I do agree that encapsulation is by far the most important and used aspect of OOP, but I'm personally a fan of inheritance of implementation when the situation calls for it. The question I always ask in interviews is how, using OOP, would you build a set of classes for an abstract database class? This, IMO, is a situation that calls for it: A necessarily abstract class with defined requirements that are very similar among the dervied classes, differing only in underlying implementation.

Tony: Polymorphism is dirt simple without inheritance. Duck-typing is one way to do it.

ReplyDeleteLinus: can you reference any ways of supporting polymorphic behavior that don't use inheritance but have run-time performance at least as good as inheritance?


ReplyDelete(I suppose this begs the question of whether templating is 'polymorphic'; generic programming proponents would argue that it is. But it's certainly a very different beast in that it doesn't provide the 'physical insulation' that inheritance and RTTI-style polymorphism provide.)

Great post. Before OOP came along, we were taught ADTs, which from the early Waterloo perspective was to model absolutely everything (except big algorithms) as just data structures. It was likely a continuation of Knuth's work. OOP took some of those basic ideas (with a model that mixed data and code) and implemented them directly into the language (in an attempt to lead programmers in a better direction). It can be elegant code, particularly when it is matched back to a presentation abstraction, but it wasn't very long before the whole thing started to derail and become a an excuse for creating a mess (as usual in programming).


ReplyDeleteThese days I tend to be semi-OOP. That is, I love polymorphism (to save on lots of code) and try to encapsulate absolutely everything. I'll often use inheritance, but I try not to go overboard. I do this in the upper layers, but then I roll up any lower objects into their parents (thus avoiding the Smalltalk fate). It mostly looks OOP, but not entirely. I think the old adage "wisdom is knowing when to break the rules" is very apropos for programmers.

As a database application developer, my reaction to OOP was the old joke, when all you have is a hammer, everything looks like a nail. And if you all you have is classes, everything looks like a thumb.


ReplyDeleteIn the end I came down in the semi-OOP camp as well, using it where there was a proven advantage (mostly in UI), and otherwise not changing anything that was not broken.

Yes. OO provides many good ways to achieve good separation. It's the separation/encapsulation that's important.

ReplyDelete