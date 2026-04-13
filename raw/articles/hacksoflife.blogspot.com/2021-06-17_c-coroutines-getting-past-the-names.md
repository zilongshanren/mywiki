---
title: C++ Coroutines - Getting Past the Names
url: http://hacksoflife.blogspot.com/2021/06/c-coroutines-getting-past-names.html
author: Benjamin Supnik
published: '2021-06-17'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is part one of a five part series on

[coroutines]in C++.

I really like the C++20 coroutine language features - coroutines are a great way to write asynchronous code, and the language facilities give us a lot of power and client code that should be very manageable to write.

My one gripe is with the naming of a few of the various parts of the coroutine control structures. This shouldn't matter that much because only library writers have to care, but right now we're in the library wild west (which is fine by me - I'm old enough to be very skeptical of "the standard library should have everything" and happy to roll my own) so we can't avoid them.

A coroutine's overall behavior is mediated by its declared return type, which will typically be a struct or class from library code that looks something like this:

template<typename T>

struct task {

struct task_promise_thingie {

auto initial_suspend() { return std::suspend_always(); }

...

};

using promise_type = task_promise_thingie;

};


The inner struct (it could be separate but the nested structure expresses the relationship to client code in ar reasonable way I think) is called the "promise type" and ... man, do I hate that name. Partly because I consider the whole promise-future async model from C++11 to be bad, and partly because the promise type" does a lot of things, of which the promise might be the least important.

I'm not sure what I would have called the promise type, but I'd lean toward "traits" or "control block", because the promise type does a few key things for you:

- It defines the beginning and end of the lifecycle of your co-routine. Does the coroutine immediately start when created, or does it immediately suspend until someone kicks it? Does the coroutine run off the end and die on its own or wait until someone kills it off.
- It defines the flow control on the CPU at the beginning and end of the co-routine. Because the beginning and end of a coroutine's life are controlled by awaitables, you can launch an arbitrary coroutine at either point! For example, if the coroutine delivers its output to another coroutine, you can, at final suspend, resume that parent co-routine on whatever thread you ended on.
- It defines the "handle" type that client code will see when creating the coroutine.

## No comments:

## Post a Comment