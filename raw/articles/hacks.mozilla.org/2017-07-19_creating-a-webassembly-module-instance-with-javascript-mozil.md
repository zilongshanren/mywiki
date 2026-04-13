---
title: Creating a WebAssembly module instance with JavaScript – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2017/07/creating-a-webassembly-module-instance-with-javascript/
author: Lin Clark
published: '2017-07-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is the 1st article in a 3-part series:*

*Creating a WebAssembly module instance with JavaScript**Memory in WebAssembly (and why it’s safer than you think)**WebAssembly table imports… what are they?*

WebAssembly is a [new way of running code](https://hacks.mozilla.org/2017/02/a-cartoon-intro-to-webassembly/) on the web. With it, you can write modules in languages like C or C++ and run them in the browser.

Currently modules can’t run on their own, though. This is expected to change as ES module support comes to browsers. Once that’s in place, WebAssembly modules will [likely be loaded in the same way as other ES modules](https://github.com/WebAssembly/design/issues/1087), e.g. using `<script type="module">`

.

But for now, you need to use JavaScript to boot the WebAssembly module. This creates an instance of the module. Then your JavaScript code can call functions on that WebAssembly module instance.

For example, let’s look at how React would instantiate a WebAssembly module. (You can learn more in this video about [how React could use WebAssembly](https://www.youtube.com/watch%3Fv%3D3GHJ4cbxsVQ).)

When the user loads the page, it would start in the same way.

The browser would download the JS file. In addition, a .wasm file would be fetched. That contains the WebAssembly code, which is binary.

We’ll need to load the code in these files in order to run it. First comes the .js file, which loads the JavaScript part of React. That JavaScript will then create an instance of a WebAssembly module… the reconciler.

To do that, it will call `WebAssembly.instantiate`

.

Let’s take a closer look at this.

The first thing we pass into `WebAssembly.instantiate`

is going to be the binary code that we got in that .wasm file. That’s the module code.

So we extract the binary into a buffer, and then pass it in.

The engine will start compiling the module code down to something that is specific to the machine that it’s running on.

But we don’t want to do this on the main thread. I’ve talked before about how the main thread is like a full stack developer because it handles JavaScript, the DOM, and layout. We don’t want to block the main thread while we compile the module. So what `WebAssembly.instantiate`

returns is a promise.

This lets the main thread get back to its other work. The main thread knows that once the compiler is finished compiling this module, it will be notified by the promise. That promise will give it the instance.

But the compiled module is not the only thing needed to create the instance. I think of the module as kind of like an instruction book.

The instance is like a person who’s trying to make something with the instruction book. In order to make that thing, they also need raw materials. They need things that they can work with.

This is where the second parameter to `WebAssembly.instantiate`

comes in. That is the imports object.

![Arrow pointing to importObject param of WebAssembly.instantiate](../../assets/f66c57393dd5c206.png)


I think of the imports object as a box of those raw materials, like you would get from IKEA. The instance uses these raw materials—these imports—to build a thing, as directed by the instructions. Just as an instruction manual expects a certain set of raw materials, each module expects a specific set of imports.

So when you are instantiating a module, you pass it an imports object that has those imports attached to it. Each import can be one of these four kinds of imports:

- values
- function closures
- memory
- tables

#### Values

It can have values, which are basically global variables. The only types that WebAssembly supports right now are integers and floats, so values have to be one of those two types. That will change as more types are added in the WebAssembly spec.

#### Function closures

It can also have function closures. This means you can pass in JavaScript functions, which WebAssembly can then call.

This is particularly useful because in the current version of WebAssembly, you can’t call DOM methods directly. Direct DOM access is on the WebAssembly roadmap, but not part of the spec yet.

What you can do in the meantime is pass in a JavaScript function that can interact with the DOM in the way you need. Then WebAssembly can just call that JS function.

#### Memory

Another kind of import is the memory object. This object makes it possible for WebAssembly code to emulate manual memory management. The concept of the memory object confuses people, so I‘ve gone into a little bit [more depth in another article](https://hacks.mozilla.org/2017/07/memory-in-webassembly-and-why-its-safer-than-you-think/), the next post in this series.

#### Tables

The final type of import is related to security as well. It’s called a table. It makes it possible for you to use something called function pointers. Again, this is kind of complicated, so I [explain it in the third part of this series](https://hacks.mozilla.org/2017/07/webassembly-table-imports-what-are-they/).

Those are the different kinds of imports that you can equip your instance with.

To return the instance, the promise returned from `WebAssembly.instantiate`

is resolved. It contains two things: the instance and, separately, the compiled module.

The nice thing about having the compiled module is that you can spin up other instances of the same module quickly. All you do is pass the module in as the `source`

parameter. The module itself doesn’t have any state (that’s all attached to the instance). That means that instances can share the compiled module code.

Your instance is now fully equipped and ready to go. It has its instruction manual, which is the compiled code, and all of its imports. You can now call its methods.

In the next two articles, we’ll dig deeper into the [memory import](https://hacks.mozilla.org/2017/07/memory-in-webassembly-and-why-its-safer-than-you-think/) and the [table import](https://hacks.mozilla.org/2017/07/webassembly-table-imports-what-are-they/).

## About
[
Lin Clark ](https://twitter.com/linclark)

Lin works in Advanced Development at Mozilla, with a focus on Rust and WebAssembly.

## 3 comments

TimothyJuly 23rd, 2017 at 10:57Lin ClarkJuly 23rd, 2017 at 11:05Mathieu DébitJuly 31st, 2017 at 14:10