---
title: 'Bonus round: languages, metaprogramming and terseness'
url: https://c0de517e.blogspot.com/2014/06/bonus-round-languages-metaprogramming.html
published: '2014-06-16'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

People always surprise me. I didn't expect a lot

[out of my latest post](http://c0de517e.blogspot.ca/2014/06/where-is-my-c-replacement.html)but instead it spawned many very interesting comments and discussion over twitter and a few Reddit threads.
I didn't want to talk about languages really, I did so already a lot in the past, I wanted to make a few silly examples to the point of why we code in C++ and what could be needed to move us out of it (and only us, gamedevs, system, low-level, AAA console guys, not in general the programming world which often already ditched C++ and sometimes is even perfectly ok with OO) but instead I got people being really passionate about languages and touting the merits of D, Rust, Julia (or even

[Nimrod](http://nimrod-lang.org/)and[Vala](https://wiki.gnome.org/Projects/Vala)).
Also to my surprise I didn't get any C++ related flame, nobody trying really to prove that C++ was the best possible given the constraints or arguing the virtues of OO and so on, it really seems most agree today and we're actually ready and waiting for the switch!

Anyhow, I wanted to write an addendum to the post because it's related to the humanistic POV I tried to make, talking about language design.

**- Beauty and terseness**

Some people started talking about meta-programming and in general expressiveness and terseness. I wanted to offer a perspective on how I see some language concepts in terms of what I do.

In theory, beauty in programming is simplicity and expressiveness, and terseness. To a degree programming itself can be seen as data compression, so the more powerful our statements are, the more they express, the more they compress, the better.

But obviously this analogy goes only so far, as we wouldn't consider programming in a LZ-compressed code representation to be beautiful, even if it would be truly be more terse (and it would be a form of meta-programming, even).

That's obviously because programming languages are not only made to be expressive, but also understandable by the meat bags that type them in, so there are trade-offs. And I think we have to be very cautious with them.

Take meta-programming for example, it allows truly beautiful constructions, the ability of extending your language semantics and adapting it to your domain, all the way to

[embedded DSLs](http://www.haskell.org/haskellwiki/Embedded_domain_specific_language)and the infamous[homoiconicity](http://c2.com/cgi/wiki?HomoiconicLanguages)dear to lispers.
But as a side effect, the most you dabble in that, the more your language statements lose meaning in isolation (to the lisp extreme where there is almost no syntax to carry any meaning), and that's not great.

There might be some contexts where a team can accept to build upon a particular framework of interpretation of statements, and they get trained in it and know that in this context a given statement has a given meaning.

To a degree we all need to get used to a codebase before really understanding what's going on, but it is a very hard trade the one that adds burden to the mental model of what things mean.

For gamedev in particular is quite important not only that A = B/C means A = B/C, but also that it is executed in a fixed way. Perhaps certain times we overemphasize the need of control (and for example often have to debate to persuade people that GC isn't evil, lack of control over heap allocation is) because of a given cultural background, but undeniably it does exist.

*[Small rant] Certainly I would not be happy if B/C meant something silly like concatenating strings. I could possibly even tolerate "+" for that because it's so common it is a natural semantic, maybe stretching it even "|" or "&". But "/" would be completely fucked up. Unless*

[you're a Boost programmer](http://www.boost.org/doc/libs/1_55_0/libs/filesystem/doc/reference.html)and are really furiously masturbating on the thought of how pretty is to use "/" to concatenate paths because directory dividers are slashes and you feel so damn smart.
That's why most teams won't accept metaprogramming in general and will allow C++ templates only as generics, for collections. And will allow operator overloading only for numeric types and basic operations.

...And why don't like references if they are non-const (the argument is that a mutable reference parameter to a function can change the value of a variable and that change is not syntactically highlighted at the call-site, a better option would be to have an "out" annotation like C# or HLSL). ...And don't like anything that adds complexity to the resolution rules of C++ calls, or exceptions, or the auto-generated operators of C++ classes, and

[should thus stay away also from R-value references](http://c0de517e.blogspot.ca/2013/05/integrating-c11-in-your-diet.html).**- Meatbags**

For humans certain

**are good, they are actually liberating. Knowing exactly what things will do allows me to reason about them more easily than languages that require lots of context and mental models to interpret statements. That's why going back to C is often as fun as discovering python for the first time.**[constraints](http://www.forbes.com/sites/groupthink/2013/07/12/creativity-how-constraints-drive-genius/)
Now of course YMMV, and there are situations where truly we can tolerate more

**magic**.[I love dabbling with Mathematica](http://c0de517e.blogspot.ca/2013/10/wolframs-mathematica-101.html), even if most of the times I don't exactly know how the interpreter will chain rules to compute something, it works and even when it doesn't I can iterate quickly and try workarounds until it does work.
Sometimes I really need to know more and there is when you open a can of worms, but for that kind of work it's fine, it's prototyping, it's exploratory programming, it's fun and empowering and productive. And I'm fine not knowing and just kicking stuff, clicking buttons until things work in these contexts, not everybody has to know how things work all the way to the metal and definitely not all the time, there are places where we should just take a step back...

But I wouldn't write a AAA console game engine that way. I need to understand, be able to have a precise simple mental model that is "standard" and understood by everybody on a project, even new hires. C++ is already too complex for this to happen and that's one of the big reasons we "subset" it into a manageable variant enforced by standard and linters.


Abstractions are powerful but we should be aware of their mental cost, and maybe counter it with simple implementations and great tools (e.g. not make templates impossible to debug like in C++ are...) so it doesn't feel like you're digging in a compiler, when they fail.


Not that all language refinements impose a burden, so there can't be a more expressive than C language that is still similarly easy to understand, but many language decisions come with a tradeoff, and I find ones that loosen the relationship between syntax and semantics particularly taxing.



But I wouldn't write a AAA console game engine that way. I need to understand, be able to have a precise simple mental model that is "standard" and understood by everybody on a project, even new hires. C++ is already too complex for this to happen and that's one of the big reasons we "subset" it into a manageable variant enforced by standard and linters.

Abstractions are powerful but we should be aware of their mental cost, and maybe counter it with simple implementations and great tools (e.g. not make templates impossible to debug like in C++ are...) so it doesn't feel like you're digging in a compiler, when they fail.

Not that all language refinements impose a burden, so there can't be a more expressive than C language that is still similarly easy to understand, but many language decisions come with a tradeoff, and I find ones that loosen the relationship between syntax and semantics particularly taxing.

*As the infamous Gang of Four wrote (and I feel dirty citing a book that I so adverse): "highly parameterized software is harder to understand and build than more static software".*That's why I advocate for increased productivity to seek interactivity and zero-iteration times, live-coding and live-inspection over most other language features these days.

And before going to metaprogramming I'd advocate to seek solutions (if needed) in better type systems. C++ functors are just lambdas and first-class functions done wrong, parametric polymorphism should be bounded, auto_ptr is a way to express linear types and so on... Bringing functionality into the language is often better than having a generic language that ca be extended in custom ways. Better for the meatbags and for the machine (tools, compilers and so on)

That said, every tool is just that, a tool. Even when I diss OOP it's not that per se having OO is evil, really a tool is a tool, the evil starts when people reason in certain ways and code in certain ways.

Sometimes also the implementation of a given tool is particularly, objectively broken. If you only know metaprogramming from C++ templates, that were just an ignorant attempt at generics went very wrong (and that is still today not patched,

[concepts](http://en.wikipedia.org/wiki/Concepts_(C%2B%2B))were rejected and I don't trust anyways them to be implemented in a sane way), then you might be overly pessimistic.
But with great power comes often great complexity to really know what's going on, and sane constraints are often an undervalued tool, we often assume that less constraints will be a productivity win and that's not true at all.





As an example I'll post here a much more reasonable use case someone showed me in a discussion, I


va << 10, 10, 255, 0, 0, 255;


Can you guess what's that? I can't, so I would go and look at the declaration of va for guidance.


vertex_array < attrib < GLfloat, 2 >, attrib < GLubyte, 4 > > va;


Ok so now it's clear, right? The code is taking numbers and packing into an interleaved buffer for rendering. I can also imagine how it's implemented, but not with certainty, I'd have to check. The full code snippet was:


vertex_array < attrib < GLfloat, 2 >, attrib < GLubyte, 4 > > va;


va << 10, 10, 255, 0, 0, 255; // add vertex with attributes (10, 10) and (255, 0, 0, 255)

// ...

va.draw(GL_TRIANGLE_STRIP);


This is quite tricky to implement in a simpler C-style C++ also because it hits certain deficiencies of C, the unsafe variadic functions and the lack of array literals.

Let's try, one possibility is:


VertexType vtype = {GLfloat, 2, GLubyte, 3};

void *va = MakeVertexArray(vtype);


AddVertexData(&va, vtype, 10, 10, 255, 0, 0, 255, END);

Draw(va, vtype);


But that's still quite a bit magical at the call-site, not really any better. Can we improve? What about:


VertexType vtype = {GLfloat, 2, GLubyte, 3};

void *va = MakeVertexArray(vtype);


va = AddFloatVertexData(va, 10, 10);

va = AddByteVertexData(va, 0, 0, 255);

Draw(va);


or better (as chances are that you want to pass vertex data as arrays here and there):


VertexType vtype = {GLfloat, 2, GLubyte, 3};

void *va = MakeVertexArray(vtype);


float vertexPos[] = {10, 10};

byte vertexColor[] = {0, 0, 255};

va = AddVertexData(va, vertexPos, array_size(vertexPos));

va = AddVertexData(va, vertexColor, array_size(vertexColor));

Draw(va);


And that's basically plain old ugly C! How does this fare?


The code is obviously more verbose, true. But it also tells exactly what's going on without the need of -any- global information, in fact we're hardly using types at all. We don't have to look around or to add comments, and we can exactly imagine from the call site the logic behind the implementation.

It's not "neat" at all, but it's not "magical" anymore. It's also much more "grep-able" which is a great added bonus.


And now try to imagine the implementation of both options. How much simpler and smaller the C version will be? We gained clarity both at call-site and in the implementation using a much less "powerful" paradigm!




An objection could be that the templated and overloaded version is faster, because it knows statically the sizes of the arrays and the types and so on, but it's quite moot. The -only- reason the template knows it's really because it's inline, and it -must- be. The C-style version offers the option of being inline for performance, or not, if you don't need and want the bloat.


It's true that the fancy typed C++ version is more safe, and it is equally true that such safety could be achieved with a better type system. Not -all- language innovations carry a burden on the mental model of program execution.


Already in C99 for example you could use variable length arrays and compound literals to somewhat ameliorate the situation, but really a simple solution that would go a long way would be array literals and the support of knowing array sizes passed to functions (an optional implicit extra parameter).




**- Extra marks: a concrete example****When I saw Boost::Geometry I was so enraged I wanted to blog about it, but it's really so hyperbolically idiotic that I decided to take the high road and ignore it - Non ragioniam di lor, ma guarda e passa.**

As an example I'll post here a much more reasonable use case someone showed me in a discussion, I

__have actually no qualms with this code__, it's not even metaprogramming (just parametric types and unorthodox operator overloading) and could be appropriate in certain contexts, so it's useful to__show some tradeoffs__.va << 10, 10, 255, 0, 0, 255;

Can you guess what's that? I can't, so I would go and look at the declaration of va for guidance.

vertex_array < attrib < GLfloat, 2 >, attrib < GLubyte, 4 > > va;

Ok so now it's clear, right? The code is taking numbers and packing into an interleaved buffer for rendering. I can also imagine how it's implemented, but not with certainty, I'd have to check. The full code snippet was:

vertex_array < attrib < GLfloat, 2 >, attrib < GLubyte, 4 > > va;

// ...

va.draw(GL_TRIANGLE_STRIP);

This is quite tricky to implement in a simpler C-style C++ also because it hits certain deficiencies of C, the unsafe variadic functions and the lack of array literals.

Let's try, one possibility is:

VertexType vtype = {GLfloat, 2, GLubyte, 3};

void *va = MakeVertexArray(vtype);

AddVertexData(&va, vtype, 10, 10, 255, 0, 0, 255, END);

Draw(va, vtype);

But that's still quite a bit magical at the call-site, not really any better. Can we improve? What about:

VertexType vtype = {GLfloat, 2, GLubyte, 3};

void *va = MakeVertexArray(vtype);

va = AddFloatVertexData(va, 10, 10);

va = AddByteVertexData(va, 0, 0, 255);

Draw(va);

or better (as chances are that you want to pass vertex data as arrays here and there):

VertexType vtype = {GLfloat, 2, GLubyte, 3};

void *va = MakeVertexArray(vtype);

float vertexPos[] = {10, 10};

byte vertexColor[] = {0, 0, 255};

va = AddVertexData(va, vertexPos, array_size(vertexPos));

va = AddVertexData(va, vertexColor, array_size(vertexColor));

Draw(va);

And that's basically plain old ugly C! How does this fare?

The code is obviously more verbose, true. But it also tells exactly what's going on without the need of -any- global information, in fact we're hardly using types at all. We don't have to look around or to add comments, and we can exactly imagine from the call site the logic behind the implementation.

It's not "neat" at all, but it's not "magical" anymore. It's also much more "grep-able" which is a great added bonus.

And now try to imagine the implementation of both options. How much simpler and smaller the C version will be? We gained clarity both at call-site and in the implementation using a much less "powerful" paradigm!

[Other tradeoffs could be made](http://c0de517e.blogspot.ca/2012/09/follow-up-why-classes.html), templates without the overloading would already be more explicit, or we could use a fixed array class for example to pass data safely, but the C-style version scores very well in terms of**lines of code versus computation**(actual work done, bits changed doing useful stuff) and locality of semantics (versus having to know the environment to understand what the code does).An objection could be that the templated and overloaded version is faster, because it knows statically the sizes of the arrays and the types and so on, but it's quite moot. The -only- reason the template knows it's really because it's inline, and it -must- be. The C-style version offers the option of being inline for performance, or not, if you don't need and want the bloat.

It's true that the fancy typed C++ version is more safe, and it is equally true that such safety could be achieved with a better type system. Not -all- language innovations carry a burden on the mental model of program execution.

Already in C99 for example you could use variable length arrays and compound literals to somewhat ameliorate the situation, but really a simple solution that would go a long way would be array literals and the support of knowing array sizes passed to functions (an optional implicit extra parameter).


*Note that I wrote this in C++, but it's not about C++, even in metaprogramming environments that are MUCH better than C++, like Lisp with hygienic macros, metaprogramming should be used with caution.**In Lisp it's easy to introduce all kind of new constructs that look nifty and shorten the code, but each time you add one it's one more foreign syntax that is local to a context and people have to learn and recognize. Not to be abused.**Also, this is valid for any abstraction, abstraction always is a matter of trade-offs. We sometimes forget this, and start "loving" the "beauty" of generic code even if it's not actually the best choice for a problem.*
## 9 comments:

Concepts was rejected, but has returned.





See Concepts lite:

Concepts lite

It seems likely to be approved, possibly later this year as a C++14 TS.

I know. The point is that modules and concepts where a thousand times more valuable than all the C++11 "improvements" added together.




Apart from a couple all C++11 features (auto, lambdas) are either dangerous (rvalues) or standardization of trivial stuff that everybody already had implemented (threads, alignment, smartpointers).

Modules and concepts, unlike threads and the other crap, can't be implemented by users and are very valuable, but were scraped.

It's sad.

I don't think many will disagree with you that C++ has serious flaws. If I could find a replacement for game development that ticket every box, I'd jump at it, but it hasn't happened.








I agree that better language support for hot-reloadable code would be very nice.

On the other hand, I disagree with your condemnation of metaprogramming in C++. It is verbose and unconstrained, but if you think of it as a pure functional compile time version of haskell(with ugly syntax), it isn't too hard to reason about what is going on.

And Concepts lite will soon fix the lack of constraints, and reduce verbosity.

Here is an example of concepts lite.

Unconstrained template:

template void swap(T& a, T& b);Constrained template:

void swap(Swapable& a, Swapable& b);By "soon" you mean maybe at the end of the year (if they are on-time, which you can doubt) for the approved spec and years later for solid, wide-spread cross-platform implementation and many years later for people to actually trust they can use it in big production projects... So like, 2020 :)



Anyhow I'll add an example of what I'm talking about later.

BTW I'm ok with templates for containers (basically generics), even if they are a bad implementation of generic types, it's very useful and I have no problems accepting that.

"That's why most teams won't accept metaprogramming in general and will allow C++ templates only as generics, for collections. And will allow operator overloading only for numeric types and basic operations.


And don't like references if they are non-const (the argument is that a mutable reference parameter to a function can change the value of a variable and that change is not syntactically highlighted at the call-site, a better option would be to have an "out" annotation like C# or HLSL).

And don't like anything that adds complexity to the resolution rules of C++ calls, or exceptions, or the auto-generated operators of C++ classes, and should thus stay away also from R-value references."

I just have a feeling that the programmers you are talking about are stuck in 10 years ago, and like grumpy old men shoot at the new stuff. C is broken ( void*, function pointers, ... ), C++ 98 was broken, C++ 11 is much less broken, and C++ 14 will be even less so. It looks like you are looking at C++ and saying "look at how you can shoot yourself in the foot in such complex ways, that language is no good". You don't like references without const - and neither do I - and yet you also take a stab at that very feature that allows you to write functional code regardless of the resources allocated by the returned object namely R-value references.

It's not about how you can shoot yourself in the foot, it's about writing less code, because - and this is by far the most important reason why you should write less code - it will ensure greater code coverage while testing, thus improving the quality of your code immensely.

And yet, nobody is trying to put compile-time introspection (or even runtime ditto) into C++, leading to gobs of kludges and macros for re-implementing something the compiler already knows in any I/O code.


User-defined qualifiers (like const and volatile) would be nice, too, to make sure I could have the compiler check for thread or memory type errors for me.

jwatte_food: There are actually several proposal for compile time reflection in C++.Though given the general slowness of the committee I don't expect to be writing any reflection code until C++17.

I think perhaps you're missing the forest for the trees.






Sure, specific instances of metaprogramming can go awry. Code generation gives you lots of rope to hang yourself.

Simultaneously, I don't think we'd be where we are without metaprogramming because it enables rapid experimentation with new constructs. Putting things *in* the language is a truly slow process; mistakes are usually made yet very hard to fix; and limitations can be hard to work around.

I think your examples of poor metaprogramming only underline how *important* it is because the alternative would be to make those mistakes in the language itself (a really bad idea), or to simply cease evolution. There's no third option; there's no magical solution to not make mistakes.

And in any case: I'll gladly accept 10 metaprogramming annoyances if I can get one Eigen or whatever. It's not a coincidence that even currently more popular languages lack C++'s diversity of data structures and libraries (e.g. Java in particular) - that's because many of these things simply can't be expressed practically without at least some metaprogramming.

I think it's in any case wrong to blame the concept of metaprogramming for C++'s warts. C++'s faults are largely unrelated to metaprogramming as a concept, and more to its huge syntax and peculiar way of expressing metaprogramming.

I left C++ and C 10 years ago after burning out at a "games" company. I now use Ada for my programming. It's not 100% what I want, but it's closer than anything else at this time.

Post a Comment