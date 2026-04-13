---
title: Short names are short
url: https://bartwronski.com/2016/09/14/short-names-are-short/
published: '2016-09-14'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## Intro

This blog post is a counter-argument and response to a

[post by Bob Nystrom that got very popular few months ago](http://journal.stuffwithstuff.com/2016/06/16/long-names-are-long/)and was often re-shared. I disagree so much that I thought it’s worth sharing my opinion on this topic.Mine response here is very subjective, and contains opinions about quite a polarizing topic – if you want to read a pure facts / knowledge sharing post, you may as well stop reading it. This post is supposed to be short, fun and a bit provocative.

![opinion](../../assets/251aa8b3ca0657ee.png)

Also, I don’t think that single piece of advice “use shorter names” or “use longer names” without any context has any real value, so at the end instead of just ranting I will try to summarize my recommendations.

Having said that and if you want to read some rant, let’s go!

## What I agree with

Some personal story here – I used to write terrible, hacked code that now I am ashamed of. Fortunately, working at Ubisoft with colleagues with much higher standards and some discussion with them helped me understand clean code value. Working on one of codebases that they have cleaned up I was amazed how pleasant it can be to work with clear, good quality and well architected code and it made me realize my wrongdoings!

Today I believe that readability and simplicity are the most important features of good code (assuming that it’s correct, performs good enough etc.) to the point that I would always keep clear reference implementation until it’s really necessary to do magic, unclear optimization(s). You write code once, but you and your colleagues read it thousands of times and for years etc.

I definitely agree with Bob Nystrom that names should be:

**Clear**.

**Precise**.

However, this is I guess where points that we could agree upon end. I don’t think that short names for variables or functions serve readability at all!

## Understandability without context

Imagine that you debug a crash or weird functionality in a piece of code you are not familiar with. You start unwinding a callstack and see a variable named “elements” or looking at author’s example, “strawberries”.

What the hell is that? What are those elements? Is it local, temp array, or a member of debugged class? Wouldn’t tempCollectedStrawberiesToGarnish or m_garnishedStrawberies be

**more**readable?If you look at a crashdump on some crash aggregation website server and before downloading it and opening in IDE, it gets even more difficult! You will have completely no idea what given code does.

And this is not uncommon scenario – we work in teams and our teammates will debug our code many times. In a way, we are writing our code for them…

## Confusion and ambiguity

Second thing – I don’t believe that short names can be precise. Working in the past with some component based game engines and seeing “m_enabled” being checked / set with some extra logic around, I just wanted to face-palm. Fortunately people were not crazy enough to skip the member prefix and just operate on some “enabled” variable in long function – this would lead to even more / extreme confusion!

What does it mean that component is enabled / disabled? I guess that animation component is not updating skeleton / hierarchy (or is it?) and mesh component is probably not rendered, but how can I be sure? Wouldn’t be m_isSkeletonUpdated or m_pauseTick or m_isVisible more readable?

Side note: this point could be an argument against as well general class polymorphism / inheritance and reusing same fields for even slightly different functionalities.

## Less context switching

With slightly longer and more verbose names, it is easier to keep all information on one screen and within single mental “context”. The shorter the name, the larger and less obvious context you need to understand its purpose, role, lifetime and type.

If you need to constantly remind yourself of class name or variable type, or even worse need to check some name/type of parent class (again, not a problem if you don’t (ab)use OOP) the less effective and more distracted you are. In long, complex code this context switching can be detrimental to code understanding and make you less focused.

## Search-ability

This is probably my biggest problem with short names and a biggest NO. I use grep-like tools all the time and find them better and more robust than

**any**IDE-specific symbol searching. Don’t get me wrong! For example[VisualAssistX](http://www.wholetomato.com/)is an amazing extension and I use it all the time. It’s way faster than IntelliSense, however still can choke on very large code solutions – but this is not the main issue.The main issue is that

**every**codebase I worked in (and I guess any other serious and large codebase) has many different languages. I work daily with C/C++, HLSL/PSSL, Python, JSON, some form of makefiles and custom data definition languages. To look for some data that can be in either of those places (sometimes in many!) I use good, old “search in files”. I can recommend here a plugin called[Entrian Source Search](http://entrian.com/source-search/)(colleague from Ubisoft, Benjamin Rouveyrol recommended it to me and it completely transformed the way I work!) and it perfectly solves this problem. I can easily look for “*BRDF*” or “SpecularF0” and be sure that I’ll find all HLSL, C++ and data definitions references.Going back to the main topic – this is where short, ambiguous names completely fail! If you find 1000 references or given name then it could be considered just useless.

Just some examples.

Let’s look for “brilliantly” named variable or function

**– why would anyone need more context?***enable*![enable.png](../../assets/7fe54b10a6773b6c.png)

Note that this shows only whole words matching! Hmm, not good… How about “brilliant” short name

**?***update*![update.png](../../assets/de07cf7984944f2c.png)

Good luck with checking if anyone uses your class “update” function!

## Help with refactoring

Related to the previous topic – before starting refactoring, I always rely on code search. It’s really useful to locate it where given variable / function / class is being used, why, can it be removed?

Large codebases are often split into many sub-solutions to be lighter on memory (if you worked in a huge one in Visual Studio you know the pain!) and more useful for daily use / common use scenario. This is where IDE symbol search fails completely and can be an obstacle in any refactoring.

Again – in my personal opinion and experience, using straight grep-like search works much better than any flaky symbol search, and works across many code solutions and languages. Good, uncommon, clear and unique names really help it. I can immediately see when a function or variable is not used anywhere, who uses it, which parts of the pipeline need information about it. So basically – all necessary steps in planning a good refactor!

## Risks with refactoring

This point is a mix of previous one and section about confusion / ambiguity. It is a) very easy to misunderstand code with common names b) overload the original term, since it’s short and seems kind-of still accurate. This leads often to even more meaningless and confusing terms.

If you have a longer, more verbose name then you will think twice before changing its type or application – and hopefully rename it and/or reconsider/remove all prior uses.

## Self-documenting code

I believe in use of comments do document “non-obvious” parts of an algorithm or some assumptions (much better than offline documents that get sent in emails and lost or are put at some always-outdated wiki pages), but hate code constantly interleaved with short comments – for me because of context switching it increases cognitive load. Code should be self-documenting to some extent and I think it’s possible – as long as you don’t try to remove whole context information from variable names.

## When using short names is ok?

Ok, I listed hopefully enough arguments against using short, context-less names – but I sometimes use them myself!

As I said at the beginning – it all depends and “single advice fits all” attitude is usually piece of crap.

My guidelines would be – use rather long, unique and memorable names, giving enough information about the context, unless:

- It’s something like iterator in a short loop. I use C-style names like i, j, k quite often and don’t see it as a major problem provided that the loop is really short and simple.
- In general, it’s a local variable in a short function with clear use. So think about it this way – if someone else “lands” there accidentally with a debugger, would they require understanding of the system to figure out its purpose?
- If they are class or function names, only if they are guaranteed to be local in the scope of a file and not accessible from the outside. If you change such function from static to global, make sure you change the name as well!
- It is a part of convention that all programmers in the codebase agreed upon. For example that your physics simulation classes will start with a “P”, not “Physics”.
- You use POD types like structs and never write functions inside them – it’s fine to have their names short as you know they relate to the struct type.
- Similar to 5 – you use (not abuse!) namespaces and/or static class functions to provide this extra scope and information and always access it with a prefix (no “using” so search-ability is not impacted by it).

## Summary

Rant mode over! 🙂 I hope that this provocative post shown some disadvantages of over-simplified pieces of advice like “long names are long” and some benefits of slightly increased verbosity.

Yup. Imagine your teammates are reading your code through a toilet paper tube. Can they understand what some code does with such a limited view?