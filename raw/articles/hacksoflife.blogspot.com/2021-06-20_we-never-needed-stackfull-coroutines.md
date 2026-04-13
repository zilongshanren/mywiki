---
title: We Never Needed Stackfull Coroutines
url: http://hacksoflife.blogspot.com/2021/06/we-never-needed-stackfull-coroutines.html
author: Benjamin Supnik
published: '2021-06-20'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is part for of a five part series on

[coroutines]in C++.

You've probably seen libraries that provide a "cooperative threading" API, e.g. threads of execution that yield to each other at specific times, rather than when the Kernel decides to. Windows [Fibers](https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-switchtofiber), [Boost Fibers](https://www.boost.org/doc/libs/1_76_0/libs/fiber/doc/html/fiber/overview.html), [ucontext](https://linux.die.net/man/3/swapcontext) on Linux. I've been programming for a very long time, so I have written code for MacOS's cooperative "[Thread Manager](http://mirror.informatimago.com/next/developer.apple.com/documentation/macos8/pdf/ThreadManager.pdf)", back before cooperative multi-tasking was cool - at the time we were really annoyed that there was no pre-emption and that one bad worker thread would hang your whole machine. We were truly savages back then.

The gag for all of these "fiber" systems is the same - you have these 'threads' that only yield the CPU to another one via a yield API call - the yield call may name its successor or just pick any runnable non-running thread. Each thread has its own stack, thus our function (and its callstack and all state) is suspended mid-execution at the yield call.

Sounds a bit like coroutines, right?

There are two flavors of coroutines - stackful, and stackless. Fibers are stackful coroutines - the whole stack is saved to suspend the routine, allowing us to suspend at any point in execution anywhere.

C++20 coroutines are stackless, which means you can only suspend inside a coroutine itself - suspension depends on the compiler transforms of the coroutine (into a state machine object) to achieve the suspend.

When I first heard this, I thought: "well, performance is good but I wonder if I'll miss having full stack saves."

As it turns out, we don't need stack saves - here's why.

First, a coroutine is a function that has at least one potential suspend point. If there are zero potential suspend points, it's just a function, like from the 70s with the weed an the K&R syntax, and to state the obvious, we don't have to worry about a plain old function trying to suspend on us.

So if a coroutine calls a plain old function, the function can't suspend, so not being able to save the whole stack isn't important. We only need ask: "what happens if a coroutine calls a coroutine, and the child coroutine suspends?"

Well, we don't really "call" a child coroutine - we co_await it! And co_awaiting Just Works™.

- When our parent coroutine co_awaits the child routine, the child coroutine (via the awaitable mediating this transfer of execution) gets a handle to the parent coroutine to stash for later. We can think of this as the "return address" from a stack function call, and the child coroutine can stash it somewhere in its promise storage.
- When the child coroutine co-awaits (e.g. on I/O) this works as expected - we don't return to the parent coroutine because it's already suspended.
- When the child coroutine finishes for real, its final suspend awaitable can return the parent coroutine handle (that we stashed) to transfer control back to the parent - this is the equivalent of using a RET opcode to pop the stack and jump to the return address.

## No comments:

## Post a Comment