---
title: 'Follow-up: Why classes.'
url: http://c0de517e.blogspot.com/2012/09/follow-up-why-classes.html
published: '2012-09-10'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Originally I planned to start writing something far more interesting, but all Saturday and some of Sunday I spent playing with Mathematica to refine my tone mapping function, so, no time for blog articles. But I still wanted to write down this little follow up, I had some discussions about my previous article with some friends, and I hope this helps. It surely helps me. You don't really have to read this. You most probably, know already :)


So... Let's assume, reasonably, that we do use our language constructs as we need them. We move across abstraction layers when we need so in order to make our work easier and our code simpler. So we start:

**"Pure" functions**. Structured programming won many years ago, so this is a no brainier, we start with functions. Note that I write pure here not in the functional sense of purity, as that's violated already with stack variables, we could talk about determinism here, but I don't think formalism matters.

*We need state*>

**Functions and pointers to state**.

[This is were we left last time](http://c0de517e.blogspot.ca/2012/09/doing-some-homework-c-style-and-pain.html). We could use globals or local static data as well, at least if we need a single instance of state. Global state has a deserved bad reputation because it can cause coupling, if exposed, and both do not play well with threads. What is worse though, is that it hinders readability. A function call to a routine with static state looks like any other at the call site, but it behaves differently. For these reasons we usually don't like static state and we pass it explicitly instead, it's a trade off between being more verbose but more readable.

*We need many instances of state, with complex lifetimes*>

**Destructors and Classes**. Here, this is when we _need_ classes. The inheritance and OOP things are better served, and it should not be news, by purely virtual interfaces, so we won't discuss this here (nor later, we'll leave the rest out and stop at this level).

Having methods in a class, public and private visibility, const attributes, all these are not much more than typographic conventions, they are not a very compelling reason to use classes. A function with a "this" pointer and a method call are not dissimilar in terms of expressive power, there are some aesthetic differences between the two, but functionally they are the same, methods do not offer more power, or safety, or convenience.

What we really gain from classes is lifetime control of their instances: constructors, destructors, copy constructors. We can now safely create instances on the stack, in local scopes, have collections and so on.

The price we pay for this, in C++, is that even thought classes are structures, we can't forward declare their members, nor we have a way of creating interfaces without paying the price of virtual calls, so in order to get all the advantages of destructors, the entire class has to be made visible. Moreover, C++ has no way of telling the size of a class if it doesn't see the full declaration, so even if we had a way of creating interfaces*, we still need to disclose all the details about our class internals.

This is where the all evil lies. And to be clear, it's not because we're "shy" of the implementation internals, we don't want other programmers to see them or such aesthetic considerations. It's because it creates coupling and dependencies, everyone that sees the class declaration has to also know about the declarations of all the member types and so on, recursively, until the linker dies compiling templates.

Now, I know, we can pay a little price and do pimpl. Or we can cheat and use pure virtual but do certain compile arrangements in our "release" version so the compiler knows that virtual always has only one implementation and resolves all calls statically. Yes, it's true, and here is were the

[previous article starts](http://c0de517e.blogspot.ca/2012/09/doing-some-homework-c-style-and-pain.html), if you wish.
The
beauty of multiparadigm languages is that they offer you an arsenal of
tools to express your computation, and of course, funny exercises and
Turin tarpits aside, some map better to certain problems than others. Now,
what does "map better" mean? It might seem trivial, but it's the reason
people argue over these things. So right before starting, let's me say
again what I think it's the most important quality metric: malleability.
If your field, your experience or so calls for different metrics, fine,
you can stop here.

Quickly now! Malleability = Simplicity / Coupling, roughly. Simplicity = Words * Ease_Of_Reading * Ease_Of_Writing. Some clarifying examples, it's often easy to create constructs that are compact but very foreign (think, most abuses of operator overloads), or that are readable but very hard to write or change (most abuses of templates fit this).

**Note: For the hacker, if you wanted to scare and confuse your coworkers, the debugger and tools, you could achieve non-virtual interfaces in C++. Just declare you class with no other members than the public interface, then in the new operator you can allocate more space than the size of the class and use that to store a structure with all your internals. This fails of course for classes on the stack or as members of other structures, it's a "valid" hack only if we disallow such uses...*

## No comments:

Post a Comment