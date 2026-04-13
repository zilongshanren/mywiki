---
title: A Coroutine Can Be An Awaitable
url: http://hacksoflife.blogspot.com/2021/06/a-coroutine-can-be-awaitable.html
author: Benjamin Supnik
published: '2021-06-21'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is part five of a five part series on

[coroutines]in C++.

The relationship between awaitables and coroutines is a little bit complicated.

First, an awaitable is anything that a coroutine can "run after". So an awaitable could be an object like a mutex or an IO subsystem or an object representing an operation (I "awaited" my download object and ran later once the download was done).

I suppose you could say that an awaitable is an "event source" where the event is the wait being over. Or you could say events can be awaitables and it's a good fit.

A coroutine is something that at least partly "happens later" - it's the thing that does the awaiting. (You need a coroutine to do the awaiting because you need something that is *code* to execute. The awaitable might be an object, e.g. a noun.)

Where things get interesting is that coroutines **can** be awaitables, because coroutines (at least ones that don't infinite loop) have endings, and when they end, that's something that you can "run after". The event is "the coroutine is over."

To make your coroutine awaitable you need to do two things:

- Give it a co_await operator so the compiler understands how to build an awaitable object that talks to it and
- Come up with a reason to wake the caller back up again later.

- The tasks start suspended, so they run when you co_await them.
- They use their final_suspend object to resume the coroutine that awaited them to start them off.

*can*be an awaitable, they might no be. I built a "fire and forget" async coroutine that cleans itself up when it runs off the end - it's meant to be a top level coroutine that can be run from synchronous code, thus it doesn't try to use coroutine tech to signal back to its caller. The actual C++ in the coroutine need to decide how to register their final results with the host app, maybe by calling some other non-coroutine execution mechanism.

## No comments:

## Post a Comment