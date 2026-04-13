---
title: WebAssembly table imports… what are they? – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/07/webassembly-table-imports-what-are-they/
author: Lin Clark
published: '2017-07-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is the 3rd article in a 3-part series:*

*Creating a WebAssembly module instance with JavaScript**Memory in WebAssembly (and why it’s safer than you think)**WebAssembly table imports… what are they?*

In the [first article](https://hacks.mozilla.org/2017/07/creating-a-webassembly-module-instance-with-javascript/), I introduced the four different kinds of imports that a WebAssembly module instance can have:

- values
- function imports
- memory
- tables

That last one is probably a little unfamiliar. What is a table import and what is it used for?

Sometimes in a program you want to be able to have a variable that points to a function, like a callback. Then you can do things like pass it into another function.![Defining a callback and passing it into a function](../../assets/1d5743daa81869a2.png)


In C, these are called function pointers. The function lives in memory. The variable, the function pointer, just points to that memory address.

And if you need to, later you could point the variable to a different function. This should be a familiar concept.

In web pages, all functions are just JavaScript objects. And because they’re JavaScript objects, they live in memory addresses that are outside of WebAssembly’s memory.

If we want to have a variable that points to one of these functions, we need to take its address and put it into our memory.

But part of keeping web pages secure is keeping those memory addresses hidden. You don’t want code on the page to be able to see or manipulate that memory address. If there’s malicious code on the page, it can use that knowledge of where things are laid out in memory to create an exploit.

For example, it could change the memory address that you have in there, to point to a different memory location.

Then when you try and call the function, instead you would load whatever is in the memory address the attacker gave you.

That could be malicious code that was inserted into memory somehow, maybe embedded inside of a string.

Tables make it possible to have function pointers, but in a way that isn’t vulnerable to these kinds of attacks.

A table is an array that lives outside of WebAssembly’s memory. The values are references to functions.

Internally, these references contain memory addresses, but because it’s not inside WebAssembly’s memory, WebAssembly can’t see those addresses.

It does have access to the array indexes, though.

If the WebAssembly module wants to call one of these functions, it passes the index to an operation called `call_indirect`

. That will call the function.

Right now the use case for tables is pretty limited. They were added to the spec specifically to support these function pointers, because C and C++ rely pretty heavily on these function pointers.

Because of this, the only kinds of references that you can currently put in a table are references to functions. But as the capabilities of WebAssembly expand—for example, when direct access to the DOM is added—you’ll likely see other kinds of references being stored in tables and other operations on tables in addition to `call_indirect`

.

## About
[
Lin Clark ](https://twitter.com/linclark)

Lin works in Advanced Development at Mozilla, with a focus on Rust and WebAssembly.