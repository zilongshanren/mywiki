---
title: Hi there! | Sebastian Schöner
url: https://blog.s-schoener.com/page6/
author: Sebastian Schöner
published: '2025-07-07'
source_blog: Hi there! | Sebastian Schöner
source_site: https://blog.s-schoener.com/
category: graphics
fetched: '2026-04-19'
---

I recently needed to run a callback on thread shutdown and creation, on Windows. For exiting, you can apparently use FlsAlloc (MSDN), which is a part of the Fiber API. I’ve tried that, it works. But there are other options!
[Read More]

I recently had to understand the details of what happens when on Windows you have a global variable in a DLL and try to use it from another. I did not find this spelled-out anywhere, so let’s change that.
[Read More]

Recently I got a message from someone that ran into a performance problem with a tool I wrote 15 years ago. On shutdown, the program would completely grind the entire machine to a halt for 3 minutes. Was I able to help them? A little bit, I think: We had...
[Read More]

I have been grappling with a really silly C++ problem for a long time: I don’t like member functions, but I need to write member functions to get a decent programming UX. Member functions give me two things: scoping and discoverability. Scoping is the lesser of the two, because my...
[Read More]