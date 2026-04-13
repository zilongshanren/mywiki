---
title: Surviving C++
url: http://c0de517e.blogspot.com/2011/02/surviving-c.html
published: '2011-02-26'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**WARNING:**This post (as 99% of my posts regarding C++) contains suggestions

__but also scathing critiques to what it could be your beloved language__.

If you are offended by the former, please before rushing to post a comment, at least make sure you've read and understood the "Defective C++" section of

[this faq](http://yosefk.com/c++fqa/), that contains some of the most high-level remarks (i.e. without going down to many of the details, like bad defaults or awkward keywords) on what is bad about C++ design.

I know it's hard to get out of our own comfort zone, and we all tend to get defensive about things we are used to, even if they really suck. If you want to argue and discuss on the merit, then I'm happy to chat either via comments or you can find an MSN widget somewhere on the right of this blog page. If you just want to write that I don't understand C++ or something like that, avoid, it's just a waste of time (and I would really love to check if you are a better C/C++ or any other language programmer than I am...)


**Introduction**


If you've been reading my blog for some time, you know what I think about C++. It's an horrible mess that managed to be successful exactly because it's lame. It was designed to be a glorified macro system on top of C in order to please the market of C programmers, not scare them with this new "OO" thing but just give them something they could relate to, that they could reason in terms of C. In retrospect, it was not even a good at achieving that (see

[D](http://www.digitalmars.com/d/)for example) but it was the first and in a few years most C programmers were "won" by C++ (not[all](http://gigamonkeys.wordpress.com/2009/10/16/coders-c-plus-plus/#)) so now we have to live with it.How do we survive it? How do we manage to create projects and sell software made with it? Well, the best answer so far has been to "subset" it. Basically every professional studio working in C++ (that is, in gaming, everyone) restricts C++ in a "somewhat safe" subset that is more manageable and less tricky to work with, to avoid at least the biggest pitfalls.

What does it take to be a C++ masters? Is it the knowledge of fancy design patterns (omg!) or expression templates? Of course not, these are things that all the kids talk about out! To be a C++ master is really about knowing C++ defects more than its features, as it's demonstrated by these three fundamental, cornerstone books:

[Effective C++, More Effective C++](http://www.aristeia.com/books.html),[C++ Coding Standards](http://www.gotw.ca/publications/c++cs.htm).In fact, no one uses straight C++ to make anything, in real world everyone starts by sub-setting C++ into something "safer" and then adding back the fundamental missing features (i.e. memory management, serialization, reflection and so on) via libraries, macros or other trickery (i.e. code to code transformers, code generators or parsers and so on), so really the C++ we use is not a standard, but a studio specific version of the language.

This "custom" C++ is then enforced either informally via code reviews and coding standards, or more strictly with the help of configurable "lint"

[software](http://www.gimpel.com/html/pcl.htm).So one day I decided to stop using the blog only to blame C++ but actually try to help developers by seeing if people could agree on some "gaming/realtime rendering" C++ standards. With the help of a shared notepad, I seeded the guidelines with my personal considerations and waited for people to start adding their own.

I think we got something interesting there, and I'll clean it up and post a snapshot on the blog of that work. But the more I got into this the more I grew dissatisfied with the guidelines, as it seems to me most of them are "aesthetic" in some sense that they are certainly needed to reduce the WTF/minute ratio when dealing with a C++, but they don't change fundamentally the experience of developing a project.

What is fundamental, really, when dealing with a big software project? What is the first thing we need in order to survive?



**Everything else does not matter (much)**

Apart from running and producing an output, what is the most important quality that a software project has to have, from a development perspective? If you think about it it's obvious. The most important quality that we want is the ability to change it.

That is what we do all day, all days, we edit code. We don't just add functionality. We don't design a perfect, immutable system that will withstand centuries (especially not if you're making a game!).

Code changes, code rots, hardware changes, design changes, ideas change, players change, the single most important quality of code is its ability to be changed without breaking, without effort.

Also, really, if we can change code easily, we have all that we need. A junior programmer made a mess in our camera system near the deadline of our game? No problem, for the next title we can rewrite it! We have a crash that we don't have any clue about? Well, maybe we can rip out some systems, one by one, and find out the culprit. Designers changed their mind on the control system? Well, we might write some prototypes with them at their desk.

The more our language and project is easy to change, the less time and less obstacles it poses to change, the more all the other problems fade in the background. It's not a coincidence that the more a language is dynamic, the less need there is for fancy debugging tools. Who needs a watch window indeed, if I can just add on the fly a widget on screen that graphs the value of a given variable?

Unfortunately though, when you look at our beloved (not!) C++, there is little to be happy about. C++ as a medium for our art looks more like statuary marble than modeling clay: it requires a team of muscular stone cutters under the guidance of a genius in order to produce some amazing sculptures. And once a given idea has been translated into the stone, you hardy can change it without re-sculpting most of it or having to work in the constraints that the shape it currently has impose on you.

C++ is not only static typed but also statically linked and its performance depends on that. You don't get any fancy JIT or runtime optimization, but not even a standard way of loading modules or functions (even if to be fair, 99% of the systems you work with will have some non-standard functionality to achieve some sort of dynamic linking). Not that I'm advocating dynamic typing here, that's another can of worms (and you might even argue that types

[are not really the best form](http://lambda-the-ultimate.org/node/2828)of static checking, and C++ classes are surely not the best expression of user defined types, I digress...), but static linking surely give us less options.So what we can do? Well, the art of sculpting in C++, the art of design, becomes really the art of subdividing our sculpture in pieces, the real design challenge is all about how to cut or work into pieces. Too many of them and the sculpture will be a fragile and ugly mess (translation: craptastically slow OOP shit). Too little and we loose flexibility.

Also, we would of course love if each piece was connected to as few other pieces as possible, otherwise replacing it would be a pain, and that the connections themselves to be as simple as possible.

How do we achieve that? Well, it can be tricky because dependencies are in many ways evil, but they are also the most innocent looking features of any languages, devils in disguise. Structured programming is all about composition (even disregarding the excesses of OOP)!

**If you see these... think twice.**

I originally thought this as some "coding flashcards" for a course at my former workplace but project deadlines had priority and I didn't end up finishing it. So when I started the collaborative guidelines experiment I wrote them in a similar "visual" style: if you see this code, then your spider-coding-senses should tingle.

Great, experienced coders develop an instinct, an aesthetic if you want, something really subconscious about good structure and good looking code that is often difficult to formalize, is some sort of gut feeling that comes from having read a lot of code and knowing the perils of some structures.

So here it is. This is the part that really matters of these visual coding guidelines: the global-disaster causing wall of shame.

*You see:*

**Foo.h**(header file)

*You think:*

- Is everything in this header really meant to be seen outside?
- Can we make more things part of the implementation?
- I.E. Look for private functions that could be outside of the class.
- Is everything in this header really meant to be seen by every other module depending on this one?
- Can we more move things into a header that is seen by this module only (i.e. a good schema would be to have local includes in a module_name/source directory and the outside visible ones in a module_name/include/module_name one)
- Should we consider using PIMPL (Façade if you like changing names of existing techniques)? Or abstract interfaces?
- Are we exporting concrete types, or contracts and functions?
- If we are exporting concrete types, are they fundamental enough? If we are exporting interfaces, do we really need them or are we over-abstracting, over-generalizing?
- Remember: don't generalize something if you don't already have two/three different usages of a given thing. Don't abstract anything if you don't have two/three different dependencies on a given thing. Code should change to adapt to situations, not try to predict them.

*You see:*

**#include**(especially in an header)

*You think:*

- Do we really need the include or we can use forward declaration?
- Can we include that file or are we introducing a dependency that we don’t want across two modules of our system? (even better, make sure that this can't happen by structuring your project in a way that to access a given module from another one, the project properties have to be changed, and make sure you have all these changes approved by a technical director)
- Is the dependency static (function linking / inline functions / templates / types) or dynamic (interface calls / function pointers)?
- Which one makes most sense here? Do we need performance or abstraction?
- You will usually want to statically depend on core system libraries (memory, math...) and dynamically from other modules.

*You see:*

**a_type* Foo(...) or a_type& Foo(...)**(interface returning a pointer, or returning a structure containing pointers)

*You think:*

- Who will own that memory? Who will destroy it? When?
- What if we want to hot-swap resources?
- Better use a handle? Reference counted?
- Should we be allowed to mutate it (non-const)?
- And who else will mutate it?
- Is the pointer type the least derived (if it's part of a type hierarchy) possible?

*You see:*

**class Foo : public Bar**

*You think:*

- Are we inheriting from an interface (pure abstract class)? Are we generalizing needlessly? Is the interface as small as possible? Then go ahead.
- Otherwise, the class has to have some data associated with it. Are we sure we want to link Foo both to the interface of Bar and to its in memory layout?
- No, you are not. Don't do it, use composition instead. [More Effective C++, 33 Make non-leaf classes abstract]

*You see:*

**Class Foo{ void MyFunction(…) }**

*You think:*

- Can it be implemented as an external function instead?
- Especially if it's private, should it be visible to anyone that can see the header? Prefer implementation-only functions to private member functions.
- Should MyFunction be const?
- Has it really to be part of the class or should it be an external utility function?
- Is it needed to make the class complete and minimal?
- Should it be declared const?

*You see:*

**static**

*You think:*

- Can we safely have multiple instances of this static (i.e. if we link this statically to multiple dynamically-linked modules), or it will be a problem with DLLs?
- Can we safely access this static from multiple threads, will that be needed?

**Conclusion**

This is it for now. Look at the typewithme pad above to see the full coding guidelines. I'm sure I forgot other things and I will probably edit this post over and over. If you want, comment as usual or better, join the discussion on the typewithme shared document!


p.s. There is of course quite some discussion in the comments and actually something persuaded me that I should clarify here. A point someone raised is basically: "you seem to hate C++ but still in the end you say things about decoupling that will apply to many other languages (to some degree - I would add).


It is 100% true and right. That is what I felt and what I probably failed to clearly express. I started this "collaborative guidelines" experiment, I got some great input there and it was all nice and exciting. But then I started thinking that yes, these are the landmines we all know and have to avoid, there are books written on them and everyone really agrees.


Yes, there might be people arguing on the details (Boost is good or evill? Design patterns? and so on), surely everyone comes up with their own implementation of the same extensions (reference counting, serialization and on and on) and that sucks but still the bottom line is, everyone knows that the default new/delete operators are useless, everyone knows that "friend" is bad and so on.

There are things to avoid always, things to mostly avoid and things to remember because of bad defaults (i.e. "explicit" or "virtual ~Foo", redefining equality operators or hiding them and so on) and probably even many things that everyone forgets until they hit them, but at the end of the day... they don't matter much.


In all my years as a professional programmer I've learned that. You can work with the worst code and language and tools on earth, if the problems are "local", they are hidden behind well designed abstractions, then all the implementation behind them does not really matter. Or it matters, yes, but at a totally different order of magnitude.



So yes, I still hate C++. But we can work with it. If we pay attention to the only thing that really matters, the decoupling, then life will be fine. And slowly, we will even be able to move stuff over other languages, if it's all nicely decouple and the interfaces are sane. And believe it or not, it's already happening.



Now go, look at your project and try to do an experiment. Take a small piece that has defined inputs and outputs, with some coworkers we tried once with our camera library. Can you take it apart and put it in a DLL? Or rewrite it in another language? If yes, then sweet dreams, your project is nice. If not, then you should think, maybe you have a problem...


p.s. There is of course quite some discussion in the comments and actually something persuaded me that I should clarify here. A point someone raised is basically: "you seem to hate C++ but still in the end you say things about decoupling that will apply to many other languages (to some degree - I would add).

It is 100% true and right. That is what I felt and what I probably failed to clearly express. I started this "collaborative guidelines" experiment, I got some great input there and it was all nice and exciting. But then I started thinking that yes, these are the landmines we all know and have to avoid, there are books written on them and everyone really agrees.

Yes, there might be people arguing on the details (Boost is good or evill? Design patterns? and so on), surely everyone comes up with their own implementation of the same extensions (reference counting, serialization and on and on) and that sucks but still the bottom line is, everyone knows that the default new/delete operators are useless, everyone knows that "friend" is bad and so on.

There are things to avoid always, things to mostly avoid and things to remember because of bad defaults (i.e. "explicit" or "virtual ~Foo", redefining equality operators or hiding them and so on) and probably even many things that everyone forgets until they hit them, but at the end of the day... they don't matter much.

In all my years as a professional programmer I've learned that. You can work with the worst code and language and tools on earth, if the problems are "local", they are hidden behind well designed abstractions, then all the implementation behind them does not really matter. Or it matters, yes, but at a totally different order of magnitude.

So yes, I still hate C++. But we can work with it. If we pay attention to the only thing that really matters, the decoupling, then life will be fine. And slowly, we will even be able to move stuff over other languages, if it's all nicely decouple and the interfaces are sane. And believe it or not, it's already happening.

Now go, look at your project and try to do an experiment. Take a small piece that has defined inputs and outputs, with some coworkers we tried once with our camera library. Can you take it apart and put it in a DLL? Or rewrite it in another language? If yes, then sweet dreams, your project is nice. If not, then you should think, maybe you have a problem...

## 71 comments:

Many interesting hints you give us here. However, I'm not sure I parse "Can it be implemented as an external function instead? Especially if it's private, should it be visible to anyone that can see the header? " correctly. I understand you suggest that my_helper_function that is used by class Foo only appear in Foo.c as a "regular" function, and therefore needn't to have an exported prototype. That could make sense -- especially if its private. But I wouldn't be able to access Foo member variable or any non-public items then, would I ?


Or should I make my_helper_function a friend of class Foo ? Can this be done anywhere else but in the (global, exported) definition of Foo ?

I strongly disagree.


C++ takes time to learn and use. It's like driving a manual car but expecting it to drive like an automatic.

let's recycle the same old points everyone uses. nice article man.

sylvainulg: you're right, you can't access private members of course.




But many times you don't need that, you are really writing a private function that it's an utility for the implementation part that could be rewritten accessing only the public interface.

Or, if you even have to access the private data, are you sure that you can't pass it to the function instead?

And won't that actually make the code even look better, and the function you're writing more general?

Dustin: if you want to disagree strongly feel free, but it would be nicer to argument your arguments instead of trolling like the anonymous guys next to your comment...

I never cease to be fascinated with people who like to call themselves software

engineersbut lack the discipline to properly learn the tools and technologies.I would really like to see what do you suggest as a better option, especially if you look at it in the original C++ context (good luck running that Java VM on hardware from 1980). Even regardless of that, as a general purpose language, C++ beats a crap out of Javas and C#s, especially if you are not in the field of writing webapps and application which shuffle documents. Of course, it has to be used by a competent developer.

I feel a bit uneasy knowing that my bank account might be handled with software written by people who lack the capability to program in C++

I would say your post is rather high on the rant, and low on the argumentation. You say "everyone" uses a subset without mentioning what that subset is. Also the fact that you dont menation STL and generic programming suggests you don't really get C++. You can do things in C++ that are impossible or impractically slow in any other popular language

Actually, looking at your post again, the things you list are mostly the upsides of C++ or common to most other popular languages. Let's check just few (in order not to be accused of trolling like Dustin):








"Are we exporting concrete types, or contracts and functions?" - Glad you asked, in Java or C# I can't export the standalone function. I need to wrap it into a class although it doesn't make sense: what entity does a class with only static methods represent?

"If we are exporting interfaces, do we really need them or are we over-abstracting, over-generalizing?" - How's that different from e.g Java? With a difference that I can use templates as often a superior tool for polymorphism

"Which one makes most sense here? Do we need performance or abstraction?" - when I finally decide I make the proper choice. Unlike Java/C#, the language hasn't already decided that for me, regardless of my requirements.

"Who will own that memory? Who will destroy it? When?" - Memory will be owned by entity of my choice. Maybe you are confusing C with C++? If I really need to make sure that memory is released at exact time, I am the one who will choose. How do you answer "When?" in GC'ed languages? BTW, RAII is your friend.

"Should we be allowed to mutate it (non-const)?" - Of course, it depends on requirements. It beats having to implement each type as immutable like in other languages, unless you really, really want to enable each method to change your object. Good luck debugging.

Bunch of other issues about proper abstraction and hierarchy level is common to all languages which support inheritance. Same for multithreaded access to static members. Of course, you implement all your code in pure functional languages, so you don't have that problem, right?

The fact that C++ gives you a bunch of tools (as multiparadigmatic and not an OO language) is a good thing. Choose the subset you need. The company which built my house can build with bricks, concrete, steel and glass. They can build bridges and pools. However, my house is built of brick and doesn't have any bridges: they didn't feel the need to use everything thay could

zdeslav: If it matters, I hate being called an engineer, I didn't study engineering. Even the translation "computer scientist" really sucks as I didn't study computers that much, it's like calling a surgeon a "scalper scientist".








That said, about the better option. Right now there is no better option, that's why I use C++, everyone else uses C++, and why I write about it (even if to be fair, more and more people think about going back to C or at least, a less OO-oriented style of doing things).

In the 80ies? Was there a better option? Well in theory yes, but C was so successful and people are scared of going outside their comfort zone.

They transition to something different only if it's not too different. That's also why Java was so successful, it looks close enough to attract people, even if then they are bitten by how different it is in its underlying concepts (and that's also why we still have a lot of Java and C# code written as it was C++ that really runs poorly).

So what's your point? C++ is successful yes. Does that mean it is good? Then DOS is the god of OS, Windows is the best of the best, Visual Basic kicked ass. Let's shut our brains, not reason and surrender to the "best option".

If on the other hand for "best option" you mean "in theory" not considering marketing aspects and tool availability and so on, then yes there are a ton of better options, and there were also 20 years ago. The SML family of languages for example is static typing and static linking done wonderfully right.

If you look at the language design, and not the compiler implementation of it, there is an infinite number of superior choices. Actually, if you look at the language design itself C++ is not really performance-oriented at all.

Fortran, one of the first programming languages ever, had no pointer aliasing and better parallelism support from the start. In fact for years Fortran outperformed C and C++ and sometimes it still does today.

Petke: my point was exactly that everyone builds its OWN subset of the language. About templates and so on, please make some examples, because I'm pretty sure that I understand C++ let's say "better than the average". I'm not really a beginner, so go ahead, challenge. If you want to argue I'm open to arguing, I love the blog because it gets me to know more people and more opinions.


If you just say "this is cool you don't know what you're talking about" as you did well, that is not really having a discussion, that's called trolling, and you can go do that on some other people's blogs, I don't force anyone to read or comment here.

Zdeslav: yes i agree, many coupling problems that c++ has are shared by other languages that were mostly inspired by it, java and c# are clearly an attemp at doing the same c++ did to c, be similar enough to get people on. And i don't really love java anyway, it's another marketing accident, like c++, it's not really well designed.


So i agree. Even if on most actual details of what you write i don't (i.e. gc makes possible to share objects across classes, manual memory management does not,and it's rather inexcusable for an OO langauge, while it was fine for C not being OO, then again C had some thoughts behind its design), i'm on my ipad now and i won't go in arguing wiyh everything, it's a pain to type on this thing.

I'm not sure where my second, and rather longish, post went, and I'm not willing to repost it.





I am not sure why do you obsess so much with performance in your reply: I haven't even mentioned it.

When I say that C++ is superior to most popular languages I don't really consider speed to be a deal breaker. FORTRAN may be faster, but you will have a hard time writing a debugger in it.

The important thing is that it is a language which allows you to choose the approach which fits the problem best: procedural, OO, metaprogramming, even perf-optimized, if that's what you need. Besides that, it provides a number of extremely powerful tools and idioms (templates, RAII, etc) which don't exist in most popular alternatives.

As I mentioned in my second post, the most of the issues you have listed either plague the other languages too (so no need to single out C++) or are actually advantages which give you the choice instead of already being chosen by language designer.

Does it come at a price? Yes.

Does it have its problems? Yes.

As any powerful tool, it takes time until you master it. It gives you choice, but expects you to decide what you'll use.

Actually, I will qoute you as a conclusion:

"It's just that some people just go with the latest trend, they switch their brain off and not think that every new technique is a tool in your arsenal but it's still up to you to use the right tools in the right places."

Zdeslav: of couse c# and java have still less "oh shit" moments and features. You don't have to read ten books and write coding guidelines and static checkers juts to avoid the ugliest bugs of the design. It's not about options, i'm sure you're familian with Scott Meyers and so on, how many things are really in the form "never do this, it's just bad" or "if you do this, remeber to do also x,y, and z, it should be the langauge default but it's not, sorry".



C++ is not a set of tools, it's a set of tools with mines all around them, and you have to create a map of all of them. And most of the time the map is sort of the same (all guidelines avoid mostly the same things) but it differs enough not to make anything really inter operate (i.e.eeveryone reimplements differently memory management, rc or gc, threadng, simd, reflection, serialization and so on)

Still, and that was the point of the post, in the end it does not matter so much, because no matter how much your world sucks, if it sucks only locally, if you decouple (as you'll need to do in any language to an extent), then you can throw the garbage when it's too much. Oh hell, if you decouple right, you can even eventually rewrite pieces n other langauages, and reallywe always d, no game I shipped was pure c++, under the hood, maybe in disguise, there were at least 3/4 languages...

Just seen your other post:






Well, in my opinion, C++ is extremely well designed for the requirements it had. If you remove many of those requirements, than some parts of C++ will not make sense.

C++ is NOT an OO language. That is a common misconception: it's a multiparadigm language. Unlike e.g. C#, it doesn't force me to put Max function into Math class although Math is not an entity in my model, and has no state. It lets me define function where I need function and class where I need class.

Regarding GC, I would take RAII over it any day (btw, I would also take templates over it). Why is the memory only important resource? How does GC help you to handle other resources: bitmaps, DB connection, handles? I write realtime software for living: I can't afford GC thread running in the middle of time-critical piece of code. I guess that users in early 80ies where in the same boat: try selling them GC with hardware from that time.

I'm not sure I understand what "gc makes possible to share objects across classes" means, but if I'm guessing well, you can use shared pointers.

BTW, it's funny that both Java and C#, as most popular GC languages, provide WeakReference class in their libraries.

for some reason, my comments keep disappearing.



I don't take 'Java/C# have less shit features' for a simple reason. I can do in C++ everything I can do in C#, but not the other way round. C++ is the only language which lets me write anything from very high-level code (templates, standard OO stuff) to very low-level (assembly code).

A couple of months ago, I needed to implement a slightly specific buffer pool in C# to hand out preallocated arrays of different sizes. It was impossible to do it (mostly for the reason that you can't represent a part of an array as separate array in a clean way).

zdeslav: I actually saw your comment in my email but it's true, it's not on the blog. I hope that it's just a temporary problem and they will reappear eventually.













I dare to disagree though on some of the practical things you say. You often mention that C++ has more options and you can do everything in C++ but I don't really see it.

You mentioned at one point templates. In which way templates are cool? As a mean of parametric polymorphism? I don't think so, for that they really suck, C# generics is parametric polymorphism done right. C++ tried to patch itself with contracts but they even fell out of the next standard...

You might say that templates are not only about parametric types, they are really a macro system. But that really really sucks, it's incredibly hard to reason about them as a macro system, I can't avoid thinking they were just parametric types _implemented_ as a macro system because Stroustrup is dumb (sorry).

But ok, if we take them as a metaprogramming system, are they any good? I mean they look way inferior to lisp macros of course that were around since forever, but even to C# reflection and code generation abilities, F# expression templates and so on an on.

Then you say "I can do everything in C++ that I can do in C# but not vice-versa". Can I dare to say that's because maybe you're not that experienced with C# yet?

Some examples: Can you do reflection in C++? Not really, everyone tries to emulate that with hacks that half-work (imposing restrictions, requiring to derive from a base class, not working with multiple inheritance etc) and it's a pretty fundamental feature.

Sharing objects? Again, RC is a fairly bad solution, it's slow, it does not work with cyclic references, still it's the most common solution in C++.

Functors are a really bad hack for first-class functions. Functional programming in C++ is so bad to emulate it's practically useless (you end up writing more code and more complicated than without)

Dynamic code linking? Not standard in C++, can't discover new types, can't link generics and so on.

Yes, C++ is low-level enough to have some sort of work around for many problems, but that's sort of like saying that you can do in C everything you can do in C++. Classes? Well you can roll your own structures of function pointers. Hey what about assembly? It's turning into a Turing tarpit argument.

Threads? Non standard. SIMD? Non standard. Even the "high-level" C# has means of object alignment...

There are many thing that you can't do cleanly at all in C++, and they are really fundamental, so much that in all the projects I've worked in we tried with macros and hacks to roll our own...

Compared with Java, C++ was not well thought out. But it would be unfair to say this because the Java creators did learn from the mistakes of C++.


Also you didn't mention that the technique called C++ metaprograming has evolved into a self-indulgent perversion of programming sensibilities. At least obfuscation contests don't consider their entries as examples of good programming style.

I find the static typing and static linking to be features of C++ that I like.


I do agree that if you are serious about doing C++ development, you better own Effective C++ and More Effective C++.

zdeslav: replying to more of your comments (that I still can see in my email even if they don't show here for some reason)






C++ is not an OO language: well I say C++ is OO meaning that the "++" part is the OO part, I love the rest (that is, the C language). As a sidenote, it's funny how during the years C has always been more performance aware than C++. It was the first to have the restrict keyword, and it will be the first with memory alignment and threading.

RAII. I guess this is a personal preference, I really like "using" more than RAII as it's explicit at the call-site and not implicit in the type. Also I don't think such decisions should go with the type, they should be left to the callee.

This discussion http://blogs.msdn.com/b/brada/archive/2005/02/11/371015.aspx sheds some light on why C# does not have RAII

About the shared pointers, well I have a post on RC and GC somewhere, bottom line RC is a retarded GC, it's not fast (can't be delayed, can't really be parallel, causes a lot of cache misses on destruction), it not as powerful (can't compact the heap and so on) and in the end the performance manual memory management in general is a myth. In no realtime application I've shipped we did allocate/deallocate memory during the realtime part. If we had to do, we used linear allocators, not the heap. So with manual memory management you don't get nice performances, you get nice performances by not allocating so many objects, and you can do that with GC too.

With GC you also get other perks though, like heap compaction and better cache usage. Fragmentation really kills you, and all the games I shipped had at least one engineer working full time on the memory subsystem and optimization... of course it would be unfair to compare that to just random C# code, people think that GC means "you don't have to think about memory" well that's very wrong.

I don't get why the weakreferences are funny, so I can't comment on that.

About C++ being well designed for the requirements it has, I think it's a false myth, but if you show me more concrete examples I can comment further. As I wrote D for example works within some very similar requirements and still manages to be less dumb.

zdeslav: oh forgot... You say C++ is "multiparadigm"... this is like the template metaprogramming thing, I really believe it was not a design decision, I think it was a consequence of the bad way C++ was developed.




C++ was initially (and it still clearly shows) a macro system on top of C. Templates wanted to be generics, made with macros, so in the end they are bad generics (not really strong) and as a side-effect, a bad metaprogramming system too.

Same with the "multiparadigm" thing. It's just a consequence of being a macro system on top of C, of course it would support the underlying language as well, so you get the "++" part (OO) and the old system (structured, imperative) as well. That's all the "multiparadigm" it is.

It's actually way less "multiparadigm" than dunno C#, python, lua or javascript where you can write heavily OO stuff but also functional or even be more "C-like".

You've described my sentiment perfectly.



More over, I'd like to point out the amount of security vulnerabilities C++ and C has caused since they were invented; pretty much 99.9%.

This isn't because of language popularity, it is because you can write hidden (but often fatal) mistakes in C/C++ more than in any other language I know about (that makes about ~15).

good article! In our project we are using cppcheck (http://sourceforge.net/projects/cppcheck/), an open source static code analysis tool to find some coding bugs.

i agree to a certain extent. C++ is not a perfect language. Most of the times the problems and error caused by using the wrong tool, in this case c++, for the problem. This often end up as new user tend to have a misconception that c++ is the best solution for everything. e.g developing a notepad editor, i wouldn't use c++ for it. However C++ still does have it uses. For example when writing a binary slot vertex cache to optimize for rendering, it is much easier to write that in C++ as oppose to say C#.


p.s. personally i don't think it reflects very well on calling another person dumb. sure the person might not produce the best tool or best of things, but it does not mean we should call them dumb.

hmmm, you are wrong.





C++ was designed as multiparadigmatic language from the start, it was not an afterthought. C# doesn't come even close, while I agree that Python might be better than C++ in that respect. However, although Lua and JavaScript have some nice features, good luck implementing your next game in that (not just scripting). They are all generic and multiparadigmatic, right?

regarding 'more choices', a few examples:

- if I need polymorphism I can choose between static (templates) and dynamic (virtual methods) type. when I need to control execution constraints I can choose (templates are resolved during compilation). In Java I can't, Gosling did it for me :)

- if I need something to be a function, I can have it that way. Why do I have to put Min/Max static methods into Math class, again? What entity is that? If it's just for the naming scope, why isn't that a free function inside a namespace? What object do you model in OOP with class that has no state?

- templates are great, I dare to say that you don't get them if you don't agree. It doesn't make sense to discuss this, we'll not agree. They can be hard to undersand if written poorly, but I have seen my share of poor Java/C# code. I'm not a big fan metaprogramming (it's different from templates), but it's a great tool for a set of problems

- generics are crap, because they always have to rely on interfaces to define constraints. Good like trying to write generic Max(). Oh right, I need to implement IComparable everywhere

- I have enough experience with C# and I dare to say that I am quite good in it. Feel free to implement a class which preallocates a buffer, and then serves parts of it as arrays of certain type. BTW, this is a workaround for implementation issues of .NET heap and GC mechanism (LOH, specifically). You mention that you don't allocate/deallocate in RT part of the game an use custom allocators. I am glad that you used the language which allows you to implement better solution when the default one is not good enough. Now try to do that in C# (exactly the issue I described), I'll wait.

- reflection: not out of the box, but I can provide it with additional code without leaving C++.

- Functors are just fine, thanks. no issue there

- dynamic linking: this is the feature of .NET platform, not C#. Btw, for templates, code generation is the point, not linking - templates are concepts, not complete types so nothing to link there. I agree that component model is the weakest part of C++, but that's not a big issue.

- threads are also fine. having them as a standard is a library issue, and I believe that it's actually good that they didn't put everything in. You can choose independent portable threading libraries. Do you claim that developer should never need to use anything out of the standard lib?

- object alignment? of course you can control that.

- RAII vs using: using is an abomination - a keyword in language to handle the type which is merely a convention. BTW, when you share your IDisposable object among few other objects, who calls Dispose() and when? Oh, you will leave it to finalizer?

'++' in C++ is not only for OO. And even than, OO is not classes and interfaces. Templates are far more OO than that.

the point: I agree that some of these thing can't be done cleanly in C++, but can be done. For Java/C# some things can't be done at all. The proof is that these platforms are useless in area where I work, while I'm not aware of any area where it is technically impossible to use C++.

to Anonymous: if Java is so much better thought out that C++ how come that you can't write system software or realtime software with it? Oh, right, it's great for limited set of problems. I'm not a native speaker, but i think that it's called 'one trick monkey' in english (ok, just flaming a bit :)

You don't give any concrete examples to back up your points. You just rant basically saying "it's rubbish", with no evidence what-so-ever. Judging by your current employer I'm waiting for you to say "Use C# instead...".

The fact you seem to think it's become popular by mistake and not due to the judgement of countless highly intelligent individuals shows a large degree of arrogance and ego.

@Everyone: See 'Imperfect C++' for a real, balanced and informative discussion of the weaker aspects of C++ (including ways to add missing functionality).

@zledav: all the explanations you give and details about how "you can chose to X" reveal to me why there has been so much hype towards Java/C#. The fact that they _impose_ way to work means that a large team of dudes can work collaboratively with less effort. Clearly, if I am the "C" guy and write my code assuming RAII, but that the "V" or "M" guy has failed to implement it properly, then our code will have problems.



That makes C++ somehow an hostile environment for a developer, hence the desire for "lint"ing ... (That could makes good C++ developer feel heroic for mastering that environment, though)

I'm not a C++ expert, by far. I keep trying it. It fails making "the hard thing easy and the easy elegant", which I consider as a strong feature for a language.

C style is ugly and type unsafe, and so is much of OOP style as its highy coupled and inflexible. Those are the two alternative styles to the genric programming style. In most popular languages you cant do genric programming style, in C++ you can do it typesafely. To make it concrete with an example: STL has a dozen different collections, and hundreds of algorithms that work for every collection. With OOP style this would mean that there would be a combinatorial explosion of methods. NumCol*NumAlg methods instead of NumCol+NumAlg as in STL. Also any algorithm can unitrusively be spezialized for some conceptual iterator type, and all collections will pick it up automagically. That is very cool. C++ is so special that it provides these very powerful abstractions without any perfomance penatly. You dont get that with other popular languages. Ignoring generic programming style, and critizizng C++ because C-style and OOP are ugly shows you dont really get modern C++. Also you dont mention RAII once. RAII is probably the other imoprtant concept in modern C++. Again you cant do it in many other popular languages.


To get up to date with STL.. check out the easy to watch STL series: http://channel9.msdn.com/Shows/Going+Deep/STL-Some-Underlying-Algorithms-Data-Structures-and-More-with-Stephan-T-Lavavej

C/C++ (native) is the best thing out there. 99% of the "other" languages are designed for code monkeys who don't have the base knowledge to write in a demanding languge such as C/C++. Becomeing a good native programmer doesn't happen over night. Clearly you have a few more years to go. All your suggestions sound like they came from a "begining C/C++" book...

Ah man, does any one understand one of the number one benefit of C++ is that you can customize the language to do what ever you want regardless of the project at hand. That is probably one of the reasons most game shop use C++ is the sure fact that you can customize the bloody piss out of it (not including almost direct access to the hardware [ go further use assembly :D]).








Even though you hate C++ you have to admit that C++ is the most customizable language in existence. For example a basic vector 2 class.

class Vec2 {

public:

float x; // public because it easier to access

float y;

... // Constructor or what not

Vec2 operator + (const Vec2& v) {

return Vec2(x+v.x, y+v.y);

}

Vec2 operator - (const Vec2& v) {

return Vec2(x-v.x, y-v.y);

}

Vec2 operator * (const float& f) {

return Vec2(x*f, y*f);

}

... // More stuff added such as additional operators like / += -= *= /=, and methods for general vector 2 operator such as dot

};

As of yet I haven't seen any other language that can make a class manipulate its operators like this. And not just math constructs you can override both new and delete for a custom memory manager which can be placed at a global scope or class, struct, union scope. This will lead to memory optimization which is impossible to do in languages like Java or C# because it depends on there Garbage Collector. And possibly other optimizations could be done too. C can do this too but C++ way of doing it is much more uniformed because you are simply override new and delete.

If you can find a language that can be customized to this extent than congrats I'm wrong. If I'm right then that is one of the most unique feature that will help you in a bind especially math part of game development which is sometimes a pain or the memory part of the project as well. Oh well enough babbling, need nicotine.

Consolidating:

I don't get it. If you hate C++ so much why don't you change careers? I let science to get away from Fortran because I didn't want to be the guy moaning all the time about how much I hated something.

Just a thought, take it or leave it...

Nice article though. I like your choice of books, and, have also seen people try to pick out the 'safe subsets' (ugggh).

It sounds like your heart is somewhere else, why not go there?

And, by the way, I was part of a project that profiled fortran against C+ on a number of different supercomputer architectures

and the conclusion was that fortran was not faster, in fact, due to more sophisticated compilers C++ had the upper hand (in response to the

comment above).

I am trying to hard to read between the lines of your blog and figure out what you are really trying to say? Game programming should be in java not C++?

Or just a general disatisfaction with the complexity of C++ and a desire for something more elegant?

And as far as standards go, my experience has been that the utopians of coding usually end up like the utopias of life.

Controll freak disasters!

I love C++, though I do acknowledge the weaknesses I think you see... Believe me, there are worse languages out there to be stuck with...

If all you want is glossing over, then use a lipstick, not a scalpel.




The problem with C/C++ is not the language, but the people flourishing it like a dabber to apply rouge, rather than the scalpel that it really is. No wonder so many people get injured and so many people cry bloody murder when they come into contact with C++ for the first time.

I do not agree with most of the complaints you make, in fact I think most of them are merely a matter of personal preference. Or the consequence of your project requirements: If your applications is bound to gobble up so much memory dynamically that any garbage collector will simply burst, then you'll be bound to use a language that has the

featureto be able to manually allocate and manage your memory resources in the most efficient way. If all you want is a shiny web app of course, then you might consider the lack of a garbage collector a drawback in C++. It's all a matter of perspective.In that context, I would agree. I would agree that C++ is not the right language for the job. But I'd never state that C++ is a bad language because of that! Don't blame the scalpel for cutting - it just does what it was designed to do!

While everyone seems to agree that a program should be user friendly, and a library should be developer friendly, I find it quite surprising that programming languages get a free pass in this regard. After all, a programming language is a developer interface to the machine.









The principle of least astonishment states that, when two elements of an interface conflict, or are ambiguous, the behaviour should be that which will least surprise the user.

Alan Kay states that "Simple things should be simple, complex things should be possible." Meaning that the simple case should be easy to do.

C++ fails on both of these fronts. Just getting it to work in the common case requires esoteric knowledge into the intricate and complicated rules of virtual, const, references, initialization, and all the other gotchas that prompted books like "Effective C++" to be written. In no other language would I be completely unable to trust a junior programmer to design a class. Hell, I don't even trust the intermediate developers!

It reminds me a lot of what the unix neckbeards used to say (and in some cases still do): "If it was hard to write, it should be hard to understand". In fact, all the comments to the effect of "you need to learn the tools properly" are making essentially the same argument, but there's a reason why bash shell scripting is a terrible experience, and there's a reason why C++ is a terrible experience.

As Scott Meyers said in his Effective C++ book, you want to design an interface in such a way that it is difficult to do the wrong thing. Amen, brother! C++ is an interface to the compiler. It should be difficult to do the wrong thing there, too.

"Any fool can make things bigger, more complex, and more violent. It takes a touch of genius -- and a lot of courage -- to move in the opposite direction."

- Albert Einstein

@Karl:



Don't forget C++ was conceived more than 25 years ago. At that time it went a loooong way towards user friendlyness, as it would complain at compile time at countless inaccuracies that no C-compiler ever worried about!

C++ introduced type safety, more detailled declarations, and the ability to design type dependencies that formerly only ever existed on paper.

It's easy to complain now, 25 years later, that your Volkswagen doesn't have GPS. And of course, knowing that there was no GPS 25 years ago doesn't make you feel any better. But then you have to consider that your Volkswagen was designed to go everywhere you want it to, not just where some hippie UI-developers once thought you might like to be!

@Anonymous talking about operators:





So you really think that C++ is the only one that allows operator overloading?? I think you need to research a bit.

Just research about C# and you will quickly realize how ignorant you're beeing on that matter.

@Author:

I love C++ simply because of the challenge of coding in it. It also helps understand how things go under the hood and makes me a better C# programmer (my mainstream activity).

It could be simpler, obviously, but I think it's not enough to hate (among your other arguments) and in the end I'd love to be expert C++ programmer and work on games (my dream job since childhood), but where I'm from C++ is rare and gaming industry tiny.

I hope someday to have the opportunity move to US or any other country where the gaming industry is big.

Learning C++ is like learning to fly...a 747. If you don't know how to fly, C++ is not the best choice for your first airplane. If you are used to flying a piper cub, you will be appalled by all the buttons and displays. But if you want to move a big load a long way quickly, you gotta learn it.





I recently got a look at google's internal C++ coding standard, which says "we don't use this feature and we don't use that feature." It's an interesting document. It clearly shows that some senior google-ites were not experienced with some of C++'s more useful features.

C++ had its genesis in 1981(!) when there were fewer developers, and their average I.Q.s were higher. It may be that the average programmer isn't smart enough to use C++ well, or an equally valid view, that C++ is just too hard to learn for the average programmer. It's certainly not a language you can just pick up. It takes years to get good at C++ and all its features.

The world doesn't reward you for learning C++ either. It's not the wizzy language of the month, so those job offers that need you to know the wizzy language of the month don't go to devs who spent the years to master C++.

On the other hand, C++ is old enough to vote now, and there are still C++ jobs. We'll see how long the wizzy language of the month lasts, and whether two years of experience in it ends up being worth anything at all compared to the new graduate with the wizzier language of the month for this month's experience.

@Sl@sh:





That's kind of my point. C++ has not aged well. The design choices made during the evolution of the language, though likely taken with the best of intentions, have resulted in an awkward tool that's as unforgiving as nitroglycerine.

The reason we see so many new languages emerging is because there is a rising, though yet largely unvoiced consensus, that a language should be elegantly designed, easy to use, yet have the possibility for much power under the hood. The concept itself is nothing new, of course. Lisp is ample evidence of that.

I find it comical the way so many veteran developers rag on the newer languages ("Kids have it so easy these days!").

I find it absolutely laughable how so many of them like to throw intelligence around, suggesting that lack of understanding is a result of insufficient brain power rather than poor design. In fact, thanks to the Flynn effect, the average IQ has increased by 20 points since C++ was born.

The sad truth is that it takes a genius to make things simple. All master artists understand that (Picasso in particular). Even Einstein understood that.

The Flynn effect, that's great!

As an ex math teacher I can guarantee you that IQ's haven't gone up (or down) with the younger generation! Texting doesn't help anyone do calculus....

Maybe the 80/20 rule applies to the whole discussion. If you have a physics kernel, but go into the disassembler and you'll see that C++, C or fortran are the only way to go (or cuda). But for higher level manipulation, maybe java or C# makes a lot of sense (but remember you're giving up several orders of magnitude --go into the assembler if you don't believe me--, so be careful....).

@Petke: "In most popular languages you cant do genric programming style"




-- actually many other languages support generic programming but in better ways, from c# to ML

", in C++ you can do it typesafely" -- nothing is typesafe in C++, so I wonder how generics can be... C++ templates are macros and they are 100% type-unsafe, c++0x tried to patch the uglyness with contracts but failed to deliver

"STL has a dozen different collections, and hundreds of algorithms that work for every collection. With OOP style this would mean that there would be a combinatorial explosion of methods" -- EEEEH? Dynamic polymorphism can be slower than static but surely won't get into a "combinatorial explosion"

"That is very cool. C++ is so special that it provides these very powerful abstractions without any perfomance penatly. You dont get that with other popular languages" - Again, Java, C#, Lisp, ML...

@Anonym:





"Ah man, does any one understand one of the number one benefit of C++ is that you can customize the language to do what ever you want regardless of the project at hand." -- No, it's not that you CAN. It's that you HAVE TO. And no two "shops" do that exactly the same. Try sharing objects between two libraries with two different RCounting systems. Fun fun fun!

"That is probably one of the reasons most game shop use C++ is the sure fact that you can customize the bloody piss out of it" -- No, it's because C++ compilers and tools are fast, proven and available everywhere. The only other language with these requirements is C... Note that any "game shop" will still avoid C++ as soon as it can (i.e. all the tools are written in C# nowadays practically everywhere, because tools are PC only so we don't care about compiler availability)

"As of yet I haven't seen any other language that can make a class manipulate its operators like this." -- Then I dare to say that you have not seen many other languages... :D

"This will lead to memory optimization which is impossible to do in languages like Java or C# because it depends on there Garbage Collector" -- Actually a GC makes optimization possible that you can't do in a non GC language (heap compaction), while the opposite is not true (object pools and other lame stuff are possible in GC languages as well)

SciBoy:



"If you hate C++ so much why don't you change careers?" -- I've been called a "rendering engineer", a "r&d scientist" a "team lead" but never my job title was "C++ programmer". I don't care _that_ much about the programming language to not work with any given one, but still that does not mean that I don't want to try to improve any environment I'm working in.

"I am trying to hard to read between the lines of your blog and figure out what you are really trying to say? Game programming should be in java not C++?" -- I would love if GP was in another langauge but that's not the real point. First of all, I don't really write with much of a "purpose", mostly my stuff are "notes to self". I do enjoy if people want to discuss about the stuff I write, maybe I'll change some people's mind, maybe I'll give some tricks, maybe they won't read this blog a second time.

sl@sh: "In that context, I would agree. I would agree that C++ is not the right language for the job. But I'd never state that C++ is a bad language because of that! Don't blame the scalpel for cutting - it just does what it was designed to do!"



No, I think C++ is a bad design for the job it wants to do, it's not that I want to apply it in situations where it does not apply. I'm a rendering engineer, I work on consoles with 256mb of memory and render 60fps, I happen to be a pretty low-level hacker...

BTW it's funny how people are all focusing on the "C++ sucks" part, and not on the "dependencies sucks" one that is the meat of the article...

sl@sh again: "@Karl:




Don't forget C++ was conceived more than 25 years ago. At that time it went a loooong way towards user friendlyness, as it would complain at compile time at countless inaccuracies that no C-compiler ever worried about!"

Loool. Yes if all your programming world was about C and then someone gave you C++, then maybe I would agree there is something sort-of-nice in that. And that's why we use C++ for games and not C (even if more and more people are thinking to switch back or at least to restrict most of the programming in a more C-style fashion)

But even 20 years ago there was a lot more than that! There was ML, that did "generics" much better, there was Lisp, that did "metaprogramming" muuuuuuch better, there was Fortran, that did "performance" much better and Smalltalk that did "OO" much better...

Of course if all you know is C and C++ then yes, I would understand your remarks.

Anonym: "It's an interesting document. It clearly shows that some senior google-ites were not experienced with some of C++'s more useful features."



HAHAHAHAHAHAHAAAAAAAAAaaaaaaaaaaaaaHahahaha.

Your ego has just exceeded the critical mass, you're turning into a white dwarf right now. Sorry, I'll ignore your post.

A lot of commenters here are missing the point. After several years using C++ in the game industry, I completely agree with most of the points of the original post.




All serious C++ projects are written using a subset (sometimes a rather small subset) of the features. Almost no C++ developers are "highly familiar" with all of the language features. So everybody who "knows C++" is highly familiar with their chosen subset, and less familiar with the other weirder darker corners of the language. The C++ language is full of features that interact badly with each other (e.g. function templates and overloading) or increase the complexity of correctly using each other (e.g. exceptions and constructors/destructors). In what other language could this situation even be possible? When you want to express a high-level concept, C++ often requires you to use several low-level features together in some magic combination in order to get the result you want. There is no way to package up that abstraction in a reusable form (such as the already-alluded-to-above lisp macros).

In the game industry, we almost never use C++ exceptions or RTTI. We write our own macro-based or code-generator-based systems for reflection, persistence, and dynamic casting (we don't use the language-builtin dynamic cast). Some teams avoid templates entirely, others use moderate amounts of them. Some use STL (EA even has their own re-implementation of it), but many eschew STL for a variety of reasons (performance, code size, whatever) and use their own homegrown libraries of containers and algorithms instead. Some teams use extensions like Boost, others avoid it like the plague. Most avoid use multiple inheritance of concrete types, virtual base classes, etc. Each engine/team/project uses only a specific subset of the language, on top of which they build a rich set of primitives to extend this into a richer base for building their software (macros/templates/external codegen tools). We write our own memory allocators, our own threading libraries, and our own profiling tools because there is nothing standardized that meets our needs.

I hate C++ and would love to see some newer, better-designed language come along that was suitable for writing game engines in. Unfortunately, despite years of looking I've found no other languages that could replace C or C++ as languages for us to write game engines in. C++ is a lousy language in many ways but there's nothing else around that can serve this niche, and this is probably true of a lot of other niches that are still dominated by C++.

"C++ is not a set of tools, it's a set of tools with mines all around them" Yet any significant piece of software on your desktop is made of C++ code... Well, well how can this even be possible ???

Anonym: Yet a lot of software has been written with Visual Basic. Yet Internet Explorer powers 50% of the internet users. Yet marketing triumphs quality. Yet...

Anonym: if we keep using the "popularity" metric, then Java is the best, and C is still a bit "better" than C++ http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html

@Deadc0de: "BTW it's funny how people are all focusing on the "C++ sucks" part, and not on the "dependencies sucks" one that is the meat of the article... "


Well, since you've introduced your article with a full page of C++ bashing of the worst sort don't be surprised that, if you ask 'how did you find the steak?', you'll get the answer 'under the lentils'.

Anyway, none of these 'dependency' concerns are really worth discussing any more than a carpenter would discuss what hammer to take to drive a nail into the wood. Know your tools and get the job done!

sl@sh: if you don't find anything worth discussing here, then please use your writing skills somewhere else.

DEADCODE, you can't read ! I said any 'significant' piece of software. By your own logic, it's a miracle we even can write software in C++ yet any 'SIGNIFICANT' piece of software on your desktop is written in C++. Including games.


If C++ is such an horrible, how is that even possible ????

Anon: But you want to tell me how games are made? I might know.







I know that C++ is popular, and I know that right now for many applications is the only choice. Including games.

What I tried to tell you is that if something is popular, or it's used, or is the best option, does not mean that it's good or great.

If on one platform I have only one language, I have to use it, it does not mean it's great. Consoles usually provide only a C/C++ compiler, so there is no choice.

I find objectiveC++ odd, yet there are 200.000 or so applications written in it, so it's clearly great?

Javascript is the most popular client side web language, so javascript is a perfect language for client side scripting? No, it has a lot of flaws and weird stuff. It's the most successful language for client side scripting and if you have to do that, then that's the tool you want to use. For sure! But that does not mean that many of its design choices are not bad or that people can't write articles about its flaws!

Success != Quality, that's all I wanted to try to tell you, the reasoning "it's used everywhere" means it got a great marketing, and I respect Stroustroup for that, he was a great marketing guy, he understood that people don't want to change too much and manufactured something that looked so much like C that the "shock" lasted only a few years. But it does not mean that C++ is a great language.

Switching gears away from scathing, uninformed criticism, I'm curious what your thoughts as a game developer are regarding the directions D (Not 1.0, but 2.0) is taking. In about a year or so, I could honestly see it start to gain serious traction (or, at least, get taken seriously by the C++ apologists).

Wyatt: My scathing criticism is not uninformed, I'm open to debate as you can see I reply to each and every comment of people discussing my articles.










Maybe I didn't write enough to persuade people or maybe what I wrote is wrong, if you want to argue I'm here, if you or others just come and say "you don't get it, C++ is great" comments will be deleted (and btw, maybe I even have more C++ experience and knowledge than the average programmer, the fact that I dislike it does not mean that I can't program in it).

That said, about D... there is very little interest around it from what I've seen.

First problem is that it compiles currently only to x86, so it's kinda useless because on PC you can already use so many other languages.

Second problem imho is that even if D is some sort of "C++ done right", it's still basically at the same level of abstraction of C++.

At this point C++ is the de-facto standard for that level of abstraction, there is so much legacy and experience there that I don't see things changing towards such a similar language.

Also it would be really hard to recruit talents that know D, you would need to tech it to every employee, it doesn't sound practical.

From what I've seen there is a strong drive towards C# (.net). It's available on multiple platforms thanks to mono (even if has some licensing issues -you have to pay-), a lot of people know it, a lot of people like it, and actually shipped some games already (not only stuff made with unity3d).

In general I think the most common idea is to have a high-level language for most of the game code, C++ for the "engine", and ideally something like OpenCL (-ish) for heavy computation (threads, SPUs etc).

In practice today 90% of the times this translates to Lua/C++/C++ modules (DLLs or so, basically providing a stateless worker function), with the "middle" C++ "engine" part being bigger that it should be as Lua on one end is too slow to do everything it should, and parallel programming being in most games still limited to the few biggest performance offenders.

Things are changing though.

@Deadc0de:





I didn't say there's nothing worth discussing, just that I consider different things worth discussing than you do.

I agree that C++ is very hard to use properly, and can be very demanding. Probably more so than just about any other current programming language. I even agree with lots of your other statements, such as DOS, Windows, or Javascript being very successful in spite of their flaws. But I don't buy into your assertion that the same is true for C++.

There are tons of other languages around, and people _do_ use them if they make more sense for the problem they face. Dos, Windows and Javascript however are often being used even when alternatives are available that are better suited.

C++ is not being used because everybody uses it, and definitely not because of good marketing - that was the most hilarious statement you ever made - Stroustrup as a marketing guy!! C++ is being used because it is the best option for very complex and resource-hungry applications. And - unfortunately for you - that includes games.

There are many areas of software development that don't require C++. In fact the majority: last time I've looked for a job only 1 in 10 wanted a C++ programmer! So there's plenty of options for you. Or will you stick with C++ just 'because everybody uses it'? ;o)

sl@sh:








"But I don't buy into your assertion that the same is true for C++" you don't but please if you think what I say is wrong, argument about it, tell me what is technically wrong, you keep replying not on the actual technical flaws but still using arguments about "market".

Let's not debate of what's used why, let's just look at the standard and argue, are these choices decent, or are they means of programmer's torture? Are they needed for performance and C back-compatibility or is that just a lame excuse?

For me it's the latter and I can provide tons of examples, from the need of the "explicit" keyword to the pitfals of a generic system that does not enforce any constraint on types (templates). And as I wrote, the greatest collection of such bad design choices is actually in the most famoust C++ books, read Effectice C++ and tell me how many times you find things that are advised to either never be used or to always do a given thing if you do another. That to me means the language has badly designed features and defaults that have to be "patched" by the programmer's experience.

"C++ is being used because it is the best option for very complex and resource-hungry applications. And - unfortunately for you - that includes games." I 100% agree, I already wrote that. It's the best option. And it sucks, we need more options. I never ever said that right now it's not the best option, it is because there is no other fast language you can in practice use for games or in many other fields. That does not mean it's good! That does not mean there are not other fast languages! It's a pile of crap but it is successful, it is supported, it has the tools, so in practice right now it's the only realistic option.

Last but not least... About the "marketing" thing, keep laughing, but while you laugh to tears let me paste a quote from a silly guy called Ken Thompson:

"Stroustrup campaigned for years and years and years, way beyond any sort of technical contributions he made to the language, to get it adopted and used. And he sort of ran all the standards committees with a whip and a chair. And he said “no” to no one. He put every feature in that language that ever existed. It wasn’t cleanly designed—it was just the union of everything that came along. And I think it suffered drastically from that."

Isn't that called marketing?

hi DeadCode,







You simply don't want to understand.

"Success != Quality, that's all I wanted to try to tell you, the reasoning "it's used everywhere" means it got a great marketing,"

I'm not talking about success, I'm talking about significant software (huge, vast, important ...).

If C++ was the horror you describe, how are these significant software built ??? In another language in secret and then the code is magically transformed into C++ ?

In reality, C++ is a complex language that demands years of experience (not 3 months, not even 3 years) but that doesn't prevent it for being an effective (even productive sometimes when you use the right tools) and enjoyable language to write good software in. As someone you know once said : "good C++ code is better than good C code, but bad C++ can be much, much worse than bad C code."

This taken in consideration makes your rant pretty much incomprehensible. C++ is not the horror your describing, every software on your desktop proves it. If it was such an horror, even Wordpad would be a nightmare to write in C++. That's not the case.

Anonym: Pyramids are an impressive accomplishment, not matched by anything we build today, still I doubt slaves and wood trunks are the best tech to erect a building.













"C++ is not the horror your describing, every software on your desktop proves it. If it was such an horror, even Wordpad would be a nightmare to write in C++"... There are incredible pieces of software written in assembly, incredible pieces of software written in C, in Pascal, in Cobol, in Fortran. What does that mean? Seriously... All OSX software is made in ObjC so ObjC is great? People can do amazing things with any tool! Which tool they use depend on the context they work with. Does that imply anything about the quality of the language design?

"C++ is not the horror your describing, every software on your desktop proves it" isn't this exactly an argument about success? "you can do good things with it, people use it to build good things, thus it has to be good".

It's simply not true, it's not an argument. People are often forced to use a tool simply because of factors that are not dependent on its inherent qualities (language design in this case).

The quality of a language is not judged by the quality of the software made in it! Otherwise obviously all the non-popular languages would be considered shit...

Again, I want to write an iPad game, I have to use ObjC++. There are many nice iPad games, this proves that ObjC++ is great?

We don't choose technology based on its quality, we choose it based on which fits best our use case. 99% of the time it's a matter of support!

It's so obvious I don't know how to make this simpler.

Let's say I have the language A, that is a piece of shit but it's widely supported, has nice tools, most people out there know it and I have a big amount of legacy code written in it.

Then I have the language B, that is the God of all languages, but it only comes with a compiler for a single architecture and from a single vendor, has a shitty debugger and no one on the planet knows it.

Which one would a company use? A right. And it will make some nice products with it if it's a good company!

Does that mean that A has a great design and B is horrible?

I don't know what more to say, if you don't get it after this I surrender :D

"there are incredible pieces of software written in assembly,"





It's not that you don't understand, it's that you can't understand.

No there's no significant piece of software on your desktop coded in assembly. Because it would be a nightmare to code a significant piece of modern software in assembly.

"There are many nice iPad games, this proves that ObjC++ is great?"

Maybe that's your problem.

I surrender :) live happily in your language comfort zone, where great products prove the quality of the tools that have been used, see you on other posts if you will still follow what I write. I'm just a bit incerned that I will keep doing great games in c++ thus reiforcing your idea that as they are great, c++ rocks.

To clarify, DEADC0DE, I actually agree with you that C++ is a crap language that no one should ever have to use. I'm sorry you thought the "scathing uninformed criticism" was aimed at you; that was not my intent. I probably should have said something like "C++ apologists" instead, but I get riled by idealists that can't be arsed to listen to the experiences of people "in the trenches" so I was perhaps unnecessarily harsh.







As for the D stuff, thanks for your perspective. A few errata, though:

DMD compiles to x86, 86_64, and I think SPARC too. I'm pretty sure GDC compiles to pretty much everything GCC targets, including PPC and ARM (the most relevant alternative targets these days). And LDC outputs LLVM IR, so if it can be targeted by LLVM, it can be targeted from D. Regardless, by that same logic, every other new language is also useless because it usually targets x86 of some sort first.

"C++ done right" is one way of putting it, I suppose, but calling it a successor is probably more accurate. Walter Bright, you may recall, WAS a C++ guy (as in, he wrote Zortech C++). As are Andrei Alexandrescu and Bartosz Milewski and numerous others. That sort of legacy and experience is precisely why I'm hesitant to dismiss it out of turn.

What legacy do you speak of? Libraries can be wrapped in SWIG or replaced wholesale by built-in language features. The syntax is largely the same and none of the C and C++ paradigms are restricted. Really, pretty much any paradigm or combination of paradigms you could want are supported.

Re: the compiled core and scripts-- Native D compiler and rdmd offer the equivalent while not requiring two separate languages to be used.

But yes, sorry about the confusion.

PS: Oh dear, and you even updated the post! Now I feel even worse. :( (Haha, C++ FQA, so great.)

Wyatt: Oh I see now what you meant. Personally I like D, I don't know if it's an evolution of C++ or it's a "bugfix" of C++ or really what's the difference between the two things, but the language is cool.




But I didn't see it being discussed much in the industry, and I think for the reasons I explained. I know that D can interface well with legacy c/c++ code, but are we really goin to go through that burden just to end up with a bugfixed c++ that very few programmers know?

I would like that to happen but in practice I really doubt it, I think we are going to stick to c++ for the "engine", bugfix the language through lint as we already do, and as I wrote use something more high level for the stuff above the engine, and maybe somthin more peformance friendly for some inner loops.

It sucks but in order to be successful you have to be innovative enough to be perceived as a real difference from the status quo and conservative enough to not scare users that do not want o leave their comfort zone. If I look around, D is not differen enough, langauages like Ocaml are too different... C# and OpenCL are ok, and in fact they are already finding their ways in the industry...

Wyatt: I didn't update the post because of you, even if I misinterpreted your first statement the comment was intesting.

When Java got its enum, I let out a sigh of relief as it finally got a fundamental feature that has existed in other languages for years.








C++ is a bad tool because people write C++ in the way they write Java, and the fact that people are comparing it to new languages that learned from it.

I'm an ex-C++, currently Java developer by trade (Scala developer at home). While I appreciate reflection, an ABI defined in the specs, and a vast standard library, Java itself will still be a toy language to me until it supports:

1. a const or readonly modifier. final is a joke.

2. operator overloading and multiple inheritance (Scala's got them)

3. RAII. C# can do it thru "using".

4. The use of unchecked exceptions as default.

Looks like C# with its unsafe part will be my ultimate language.

Also don't forget stack-based objects, inline assembly, and non-virtual classes...

Anon: Actually I find it's quite the opposite, many people write C# like it was C++, without understanding the memory implications, without using the proper techniques, and then they complain that C# is unresponsive after they allocate 1000 resources without ever releasing them...



That said, I mostly agree with you about Java, even if you're very wrong on the unchecked exceptions, they are a curse, and on the const stuff, that is a joke in C++.

Const in C++ is nothing more than a programmer's comment, it's not even a compiler's hint, other than the problem that it is "shallow". It does not even deserve to be a language feature, you can implement it via annotations in no time, as a learning exercise...

I have implemented annotation processors in Java, precisely to limit the use of setters that seem to be so pervasive to Java-school-graduates who says "immutability is not flexible". Yikes.



And I disagree about const - if it's a joke, then final is 10 times the joke.

About checked exceptions, there's only one reason why Java is the only language in the entire history of computing that enforces checked exception in compile-time - that this feature is a mistake.

Anon: I would love to have a "serious" const implementation too, I like static checks.






And I'm not say that Java "final" is nice. What I'm saying is that C++ const is not a role model.

I agree that is better than nothing and better than the out-of-the-box final, but it's still wrong and it actually can be added to languages that support annotations with not much effort.

About exceptions, personally I won't ever use them in any language because I think they are fairly ugly no matter what, so I don't have a "solution" to make them nice.

But if you don't require to catch or re-throw then it's impossible to reason about the code, in any given point you could have any exception, who knows what will be throwing what?

I guess that's cool in a dynamic language but I don't love it in general.

It is interesting how this mindset persists in the game industry. I also work in games so I know that your(DEADCODE) opinion is fairly common.












While I started out this way, over the years as I've increased my understanding of templates/RAII etc, I've found them to be moderately elegant solutions once you properly understand how to use them.

I do agree that C++ has many many problems, and some features are best avoided(RTTI/exceptions) because of the potential slow, and compiler dependent, way in which they implemented.

The language desperately needs some form of reflection.

Concepts lite will be introduced soon in a post C++14 TR, this should help template use for people who don't already get them.

Anyway I suspect the game industry has lagged behind in C++ primarily because of out of date compilers/tools which they are often forced to use on certain platforms.

Some studios may have older programmers- who are often unwilling to learn new concepts.

Also the desire to throw a junior programmer at the code without overwhelming them with concepts they won't understand. Personally, I disagree with this. I think the #1 issue in a codebase for a junior programmer is often the sheer # of lines of code. Besides that, I think they would be better off raising the bar, and perhaps expecting that junior programmers do in fact understand what a template is.

On one of the previous projects I worked on, for a fairly well known game engine(you have mentioned it in this blog), a very large subsystem was written in what I'd say was "c with classes" style.

For what it did, it was far too many lines of code. The sheer volume of code made making changes difficult. I'd estimate that had it been written in a modern C++ style it would have been a fraction the size, and would have had far less untracked side effects.

I also have to say the idea that C# generics are in any way superior to C++ templates, really makes no sense at all. C# generics can only do a very small subset of the things templates can do.

I think you are a very smart individual, based on your other blog posts, but I don't think you really understand templates/RAII.

On memory management-

RC is a last resort, tracing GC should also be seen as a last resort. Most types do not need to be shared. Uniqueness is something I've yet to see any game industry codebase grok, but std::unique_ptr enforces this concept, acting as a form of GC with none of the downsides of RC or tracing.

The combination of (value > optional > (weak | unique) > shared ) is IMO superior to just throwing a tracing GC at the problem and hoping everything works out. Tracing GC also do not support RAII.

well enough rambling-

Post a Comment