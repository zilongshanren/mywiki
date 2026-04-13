---
title: Memory in WebAssembly (and why it’s safer than you think) – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2017/07/memory-in-webassembly-and-why-its-safer-than-you-think/
author: Lin Clark
published: '2017-07-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is the 2nd article in a 3-part series:*

*Creating a WebAssembly module instance with JavaScript**Memory in WebAssembly (and why it’s safer than you think)**WebAssembly table imports… what are they?*

Memory in WebAssembly works a little differently than it does in JavaScript. With WebAssembly, you have direct access to the raw bytes… and that worries some people. But it’s actually safer than you might think.

### What is the memory object?

When a WebAssembly module is instantiated, it needs a memory object. You can either create a new `WebAssembly.Memory`

and pass that object in. Or, if you don’t, a memory object will be created and attached to the instance automatically.

All the JS engine will do internally is create an ArrayBuffer (which I explain in [another article](https://hacks.mozilla.org/2017/06/a-cartoon-intro-to-arraybuffers-and-sharedarraybuffers/)). The ArrayBuffer is a JavaScript object that JS has a reference to. JS allocates the memory for you. You tell it how much memory are going to need, and it will create an ArrayBuffer of that size.

The indexes to the array can be treated as though they were memory addresses. And if you need more memory later, you can do something called *growing* to make the array larger.

Handling WebAssembly’s memory as an ArrayBuffer — as an object in JavaScript — does two things:

- makes it easy to pass values between JS and WebAssembly
- helps make the memory management safe

### Passing values between JS and WebAssembly

Because this is just a JavaScript object, that means that JavaScript can also dig around in the bytes of this memory. So in this way, WebAssembly and JavaScript can share memory and pass values back and forth.

Instead of using a memory address, they use an array index to access each box.

For example, the WebAssembly could put a string in memory. It would encode it into bytes…

…and then put those bytes in the array.

Then it would return the first index, which is an integer, to JavaScript. So JavaScript can pull the bytes out and use them.

Now, most JavaScript doesn’t know how to work directly with bytes. So you’ll need something on the JavaScript side, like you do on the WebAssembly side, that can convert from bytes into more useful values like strings.

In some browsers, you can use the [TextDecoder](https://developer.mozilla.org/en-US/docs/Web/API/TextDecoder) and [TextEncoder](https://developer.mozilla.org/en-US/docs/Web/API/TextEncoder) APIs. Or you can add helper functions into your .js file. For example, a tool like [Emscripten](https://github.com/kripken/emscripten) can add encoding and decoding helpers.

So that’s the first benefit of WebAssembly memory just being a JS object. WebAssembly and JavaScript can pass values back and forth directly through memory.

### Making memory access safer

There’s another benefit that comes from this WebAssembly memory just being a JavaScript object: safety. It makes things safer by helping to prevent browser-level memory leaks and providing memory isolation.

#### Memory leaks

As I mentioned in the article on memory management, when you manage your own memory you may forget to clear it out. This can cause the system to run out of memory.

If a WebAssembly module instance had direct access to memory, and if it forgot to clear out that memory before it went out of scope, then the browser could leak memory.

But because the memory object is just a JavaScript object, it itself is tracked by the garbage collector (even though its contents are not).

That means that when the WebAssembly instance that the memory object is attached to goes out of scope, this whole memory array can just be garbage collected.

#### Memory isolation

When people hear that WebAssembly gives you direct access to memory, it can make them a little nervous. They think that a malicious WebAssembly module could go in and dig around in memory it shouldn’t be able to. But that isn’t the case.

The bounds of the ArrayBuffer provide a boundary. It’s a limit to what memory the WebAssembly module can touch directly.

It can directly touch the bytes that are inside of this array but it can’t see anything that’s outside the bounds of this array.

For example, any other JS objects that are in memory, like the window global, aren’t accessible to WebAssembly. That’s really important for security.

Whenever there’s a load or a store in WebAssembly, the engine does an array bounds checks to make sure that the address is inside the WebAssembly instance’s memory.

If the code tries to access an out-of-bounds address, the engine will throw an exception. This protects the rest of the memory.

So that’s the memory import. In the next article, we’ll look at another kind of import that makes things safer… the [table import](https://hacks.mozilla.org/2017/07/webassembly-table-imports-what-are-they/).

## About
[
Lin Clark ](https://twitter.com/linclark)

Lin works in Advanced Development at Mozilla, with a focus on Rust and WebAssembly.

## 6 comments

Ari OgokeJuly 20th, 2017 at 19:50Duc NguyenJuly 21st, 2017 at 18:21Shamim AhmmedJuly 22nd, 2017 at 00:30GabrielleJuly 23rd, 2017 at 12:52AngJuly 24th, 2017 at 20:11Lin ClarkJuly 25th, 2017 at 17:34