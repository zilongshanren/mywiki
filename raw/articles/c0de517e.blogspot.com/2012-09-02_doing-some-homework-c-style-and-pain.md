---
title: Doing some homework. C-Style and pain.
url: https://c0de517e.blogspot.com/2012/09/doing-some-homework-c-style-and-pain.html
published: '2012-09-02'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

So, lately I've been doing some coding at home for a couple of projects, which is not as usual as I would like to be for me. One of these involved creating a little testbed for some DX9 rendering, pretty standard stuff and I would normally use one of the things I have in C# but this time I had reasons to use C++ so I opened Visual Studio and created an empty application with the wizard. Around two in the night I had most of what I wanted and I closed the case.


What usually happens when I code is that I really don't like the coding itself, even more if I'm not working in a particularly expressive framework. Writing code is a chore, but after I start a project I come to think about it a lot while I do all other things, and there is where most of the improvements happen, in my head (usually while I walk back home from work).


This time was no different, what I found worth blogging though is how I happened to structure the code itself. I sometimes used classes, sometimes I used "C-style" objects (functions, passing as the first parameter the "state" or what it could have been the this pointer in C++) and I even wrote a few templates.


I didn't code this with any particular stylistic goal or experiment in mind, the only difference between this and work is that I was not constrained by a preexisting framework, and hundreds of thousands of line of code around my changes.


So, what guides these decisions? Of course, while I code I work out of experience and a given sense of aesthetic. Now my aesthetic is mostly being lazy, mixed with a sense that what I do has to be readable by someone else. For some reason, that was always with me since I was a kid building Lego, I wanted to create things to last, so even in my laziness I think I'm not too sloppy.


What I think it happens is like speaking a language fluently, you don't reason in terms of rules, these do exist of course but they become an intuition in your mind, and indeed these rules are not arbitrary, they are there to codify hundreds of years of practice and evolution, guided by the very same logic that builds up in your brain after practice.


This evolution goes from rules (education) to practice, to new rules, and in a similar way I started thinking about my code and trying to understand if some rules can be derived from practice. Now, don't expect anything earth shattering, with all the discussions about OO and against it, I think there is nothing new to be said really. As for all my posts, I'm just writing down some thoughts.



What usually happens when I code is that I really don't like the coding itself, even more if I'm not working in a particularly expressive framework. Writing code is a chore, but after I start a project I come to think about it a lot while I do all other things, and there is where most of the improvements happen, in my head (usually while I walk back home from work).

This time was no different, what I found worth blogging though is how I happened to structure the code itself. I sometimes used classes, sometimes I used "C-style" objects (functions, passing as the first parameter the "state" or what it could have been the this pointer in C++) and I even wrote a few templates.

I didn't code this with any particular stylistic goal or experiment in mind, the only difference between this and work is that I was not constrained by a preexisting framework, and hundreds of thousands of line of code around my changes.

So, what guides these decisions? Of course, while I code I work out of experience and a given sense of aesthetic. Now my aesthetic is mostly being lazy, mixed with a sense that what I do has to be readable by someone else. For some reason, that was always with me since I was a kid building Lego, I wanted to create things to last, so even in my laziness I think I'm not too sloppy.

What I think it happens is like speaking a language fluently, you don't reason in terms of rules, these do exist of course but they become an intuition in your mind, and indeed these rules are not arbitrary, they are there to codify hundreds of years of practice and evolution, guided by the very same logic that builds up in your brain after practice.

This evolution goes from rules (education) to practice, to new rules, and in a similar way I started thinking about my code and trying to understand if some rules can be derived from practice. Now, don't expect anything earth shattering, with all the discussions about OO and against it, I think there is nothing new to be said really. As for all my posts, I'm just writing down some thoughts.

So, where did I use C style and where did I use objects? Well, in this very small sample, it turns out all the graphics API I had to write was C style.


Think something like


Nothing really fancy, right, what would this achieve, other than some nostalgia of pre-C++ days? Well, indeed it does not achieve anything, what I find is how many constructs we invented to do the very same, wrapped into a C++ class. Let's see...




Now, a








And we lose sight, so easily, about what really matters, being lazy, using concepts only when they actually happen to save us something, lowering our code complexity. Going back to said project, I can have a look at where I did use classes or structures with methods. Every time the object lifetime is more complex I started using constructors and especially destructors, I remember in an implementation needing to type a few times the call to a teardown of a given private structure, and moving that code into a destructor. I wrote templates for some simple data structures just not to have that code intermixed with other concepts in my implementation. I would have used classes also if I needed virtual interfaces and multiple implementations of a number of methods, operator overloading can be useful when it's not confusing, and so on and on.


Really, the key is to be lazy, don't reach for structures because they are fancy, or you think you _might_ need them in some eventual future, predictions work almost never (that's why we all work on "agile" and such methods). Certainly don't use things becuase of their hype, try to understand. It also helps if you consider coding a form of pain. And if you hate your language, I think *. Also, you might consider reading this from




Think something like

*gContext = Initialize()*somewhere in the main application, then most calls require gContext, and there is of course an explicit teardown method. The type for this context is not visible from the application, it's just a forward declaration of a struct and everything happens passing pointers.Nothing really fancy, right, what would this achieve, other than some nostalgia of pre-C++ days? Well, indeed it does not achieve anything, what I find is how many constructs we invented to do the very same, wrapped into a C++ class. Let's see...

**First**of all this entity I was coding, in the specific case the API for the graphics subsystem, has very few instances. Maybe one, or one per thread or process... I've already blogged about the uselessness of design patterns and about the king of useless patterns... you know what I'm talking about, the singleton. Once upon a time, a lead programmer told me that in games he didn't think singletons were not really about a single instance, but control over creation and destruction times of certain global subsystems. Yes. Just like a pointer, with new and delete. It might sound crazy, but if you look around you'll find many "smart" singletons with explicit create and destroy calls. Here, done that!Now, a

**second**thing that happens with singletons that experts will tell you to avoid, is that once you include the singleton class with all the nice methods you want to call, you also have direct access to the singleton instance. So everybody can call your subsystem directly, everywhere, and you won't see said subsystem being "passed around", an innocent looking function can call in its implementation all the evil and you'll never know. So, you learn to practice "dependency injection". Here, C-Style by default does not encourage that, you can include the API but you'll still need a pointer to the context, and this pointer can be made not accessible from the application who created it, so the application can pass it around explicitly only to the function it wants. Done that, too!**Third**? Well, what about[pimpl](http://c2.com/cgi/wiki?PimplIdiom), facades and such? Yes, decoupling implementation from interface, hiding implementation details. C++ does not provide any convenient way of doing so. You might be as minimal as possible, ban private methods (starting for private static, which have no place to exist) and use all implementation side functions. You can include in your class only the minimal API needed for the object, and you should, but no matter how you dice it, you can't hide private member variables. This is bad not only "aesthetically", because you have a sense of hiding the internals, it hurts more concretely in terms of dependencies and how much you have to include just to let another file use a given API. I won't delve into the details of the template usage, but the C style allowed me to use all templates only implementation side, which is a great thing. I even used a bit of STL :)**More**? Well, in most coding guidelines and best practices you learn the need to always declare your class copy constructor, and it turns out most times if you follow this practice, you will end up declaring them private with no implementation. You don't want subsystems to be cloned around, and here, this is done too "automatically" by this new invention. What about "mixins" or splitting your subsystem implementation in multiple files? What for all the methods which need more than one "context"? In which class should they live? Here, you have functions, this new invention avoids all these questions.**So what?**Am I dissing again C++? Or in general OO? Well not really it turns out, not this time, not as my main point... It just that it's incredible to observe how often we complicate needlessly. I do understand why this happens, because I was once "seduced" by this too. "Advanced" techniques, cutting edge big words and hype. Especially when you have more "knowledge" than reasoning and experience, I mean, out of university, OO is the thing right, maybe even design patterns...And we lose sight, so easily, about what really matters, being lazy, using concepts only when they actually happen to save us something, lowering our code complexity. Going back to said project, I can have a look at where I did use classes or structures with methods. Every time the object lifetime is more complex I started using constructors and especially destructors, I remember in an implementation needing to type a few times the call to a teardown of a given private structure, and moving that code into a destructor. I wrote templates for some simple data structures just not to have that code intermixed with other concepts in my implementation. I would have used classes also if I needed virtual interfaces and multiple implementations of a number of methods, operator overloading can be useful when it's not confusing, and so on and on.

Really, the key is to be lazy, don't reach for structures because they are fancy, or you think you _might_ need them in some eventual future, predictions work almost never (that's why we all work on "agile" and such methods). Certainly don't use things becuase of their hype, try to understand. It also helps if you consider coding a form of pain. And if you hate your language, I think *. Also, you might consider reading this from

[Nick Porcino](http://meshula1.appspot.com/blog/posts/post135.html)on[Futurist Programming](http://www.graficaobscura.com/future/index.html).**Note:*Many of the times one sees crazy things, wild operator overloads, templates that require hours to understand, compile or debug and so on, it's because someone loved the language itself, and the possibility of doing such things, more than how he loved his time or other's people time.

P.S. What bit of STL did I use? std::sort, because it's great really. Until you need to iterate on your own weird data structures, which might happen because at least in my line of work, STL implements only some of the least frequently used ones (before someone asks -P.S. What bit of STL did I use? std::sort, because it's great really. Until you need to iterate on your own weird data structures, which might happen because at least in my line of work, STL implements only some of the least frequently used ones (before someone asks -

## 3 comments:

Using a language feature just because of the hype or because you think it's great, it part of the learning process of a programmer. Don't you think?


The real problem is when you find out that you don't really need that feature but you keep using it :-)

I totally understand the process, in fact I was surely over-engineering everything in my first days with C++ and templates and such, it's normal.





The problem is not in that learning process, but it starts where as an industry we begin to standardize overengineering practices and consider them normal.

Nowadays one "expert" out of two will talk about the failures of OO and how cool functional programming is. Even hacking functional into C++ which is another ugly hack (think boost::lambda, a monstrosity)

Now "functional" is moving to "data oriented" and it's all good, it's all good... But we built such a castle of things, and totally ignored others, you know some as I do. I.E. 15-30min compile and link on 360 is not unseen, no modules but "design patterns" everywhere... It's not only people who are learning, we (industry) made often overly complicated things that serve no purpose.

Have you seen this series of reviews on ID public sources? It's so nicely organized... http://fabiensanglard.net/quake2/index.php

I too was all about using the latest C/C++ tricks and paradigms, but these recent days I focus on the idea(s) first. I go about my products in three phases:








1. Brainstorm, design and plan the idea.

2. Implement the solution in the cleanest/simplest way possible, even if that slightly hinders speed.

3. Then after the idea has been implemented and a prototype is running, I'll go back and benchmark what modules/parts could benefit from the said engineering tricks.

At the end of the day the languages are just tools, hence "means" to an end. The idea is the "end".

It also keeps me from burning out as everyday spurs new ideas, or builds upon yesterday's!

Post a Comment