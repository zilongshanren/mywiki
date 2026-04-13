---
title: co_await is the .then of Coroutines
url: http://hacksoflife.blogspot.com/2021/06/coawait-is-then-of-coroutines.html
author: Benjamin Supnik
published: '2021-06-19'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is part three of a five part series on

[coroutines]in C++.

One more intuition about coroutines: the co_wait operator is to coroutines as .then (or some other continuation queueing routine) is to a callback/continuation/closure system.

In a continuation-based system, the fundamental thing we want to express is "happens after". We don't care when our code runs as long as it is after the stuff that must run before completes, and we'd rather not block or spin a thread to ensure that. Hence:

void dump_file(string path)

{

future<string> my_data = file.async_load("~/stuff.txt");

my_data.then([my_data](){

printf("File contained: %s\n", my_data.get().c_str());

});

}


The idea is that our file dumper will begin the async loading process and immediately return to the caller once we're IO bound. At some time later on some mystery thread (that's a separate rant) the IO will be done and our future will contain real data. At that point, our lambda runs and can use the data.

The ".then" API ensures that the file printing (which requires the data) *happens after* the file I/O.

With coroutines, co_await provides the same service.

async dump_file(string path)

{

string my_data = co_await file.async_load("~/stuff.txt");

printf("File contained: %s\n", my_data.c_str());

}


Just like before, the beginning of dump_file runs on the caller's thread and runs the code to begin the file load. Once we are I/O bound, we exit all the way back to the caller; some time later the rest of our coroutine will run (having access to the data) on a thread provided by the IO system.

Once we realize that co_await is the .then of coroutines, we can see that anything in our system with an async continuation callback could be an awaitable. A few possibilities:

- APIs that move execution to different thread pools ("run on X thread")
- Non-blocking I/O APIs that call a continuation once I/O is complete.
- Objects that load their internals asynchronously and run a continuation once they are fully loaded.
- Serial queues that guarantee only one continuation runs at a time to provide non-blocking async "mutex"-like behavior.

*who*any given coroutine is - await suspend gives you the coroutine handle of the client coroutine awaiting on you, which means you can save it and put it in a FIFO or anywhere else for resumption later. You also get to return a coroutine handle to switch to any other code execution path you want.

- Require the client to co_await the coroutine to begin execution - the awaitable that does this saves the client's coroutine handle.
- Use a final_suspend awaitable to return to the client whose coroutine we stashed.

## No comments:

## Post a Comment