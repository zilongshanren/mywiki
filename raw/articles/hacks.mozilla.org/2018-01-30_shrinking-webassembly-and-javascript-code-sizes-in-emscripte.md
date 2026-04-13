---
title: Shrinking WebAssembly and JavaScript code sizes in Emscripten – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2018/01/shrinking-webassembly-and-javascript-code-sizes-in-emscripten/
author: Alon Zakai
published: '2018-01-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Emscripten](http://emscripten.org/) is a compiler toolchain for asm.js and WebAssembly which lets you run C and C++ on the web at near-native speed.

Emscripten output sizes have decreased a lot recently, especially for smaller programs. For example, here’s a little C code:

```
#include <emscripten.h>
EMSCRIPTEN_KEEPALIVE
int add(int x, int y) {
return x + y;
}
```


This is the “hello world” of pure computation: it exports a single function that adds two numbers. Compiling that with **-Os -s WASM=1** (optimize for size, build to wasm), the WebAssembly binary is just **42 bytes**. Disassembling it, it contains exactly what you’d expect and no more:

```
(module
(type $0 (func (param i32 i32) (result i32)))
(export "_add" (func $0))
(func $0 (; 0 ;) (type $0) (param $var$0 i32) (param $var$1 i32) (result i32)
(i32.add
(get_local $var$1)
(get_local $var$0)
)
)
)
```


Pretty good! In fact, it’s so small you can see that even though Emscripten also created a JavaScript file to load it for you, you could easily write your own loading code since it doesn’t depend on any special runtime support.

For comparison, Emscripten 1.37.22 used to emit a WebAssembly binary of 10,837 bytes for that code sample, so the improvement to 42 bytes is dramatic. What about bigger programs? There’s a lot of improvement there too: Comparing a C hello world program using `printf`

on Emscripten 1.37.22 vs 1.37.29, the WebAssembly binary goes from 11,745 to 2,438 bytes, almost **5x** smaller. Looking at the emitted JavaScript file, and running emcc with **–closure-compiler 1** to run the [Closure Compiler](https://developers.google.com/closure/compiler/) — which is highly recommended! — the recent Emscripten improvements shrink it from 23,707 bytes to 11,690, over **2x** smaller. (More on these numbers later.)

### What changed?

Emscripten has mostly focused on making it [easy](https://twitter.com/jharler_dev/status/932740513962299393) [to](https://crimild.wordpress.com/2018/01/08/experimenting-with-emscripten/) [port](https://twitter.com/exezin/status/932620231436095489) [existing](https://www.reddit.com/r/godot/comments/7gtaap/godotonline_now_ready_for_use/) C/C++ code. That means supporting various POSIX APIs, emulating a filesystem, and special handling of things like [ longjmp](http://www.cplusplus.com/reference/csetjmp/longjmp/) and C++ exceptions that don’t yet have native support in WebAssembly. We also try to make it easy to use that compiled code from JavaScript, by providing various JavaScript APIs (

[, etc.). And all that makes it practical to port useful APIs like](https://kripken.github.io/emscripten-site/docs/porting/connecting_cpp_and_javascript/Interacting-with-code.html#interacting-with-code-ccall-cwrap)

`ccall`

[OpenGL](https://kripken.github.io/emscripten-site/docs/porting/multimedia_and_graphics/OpenGL-support.html)and

[SDL](https://github.com/emscripten-ports/SDL2)to the Web. These capabilities depend on Emscripten’s runtime and libraries, and we used to include more of those than you actually need, for two main reasons.

First, we used to export many things by default, that is, we included too many things in our output that you *might* use. We recently focused on [changing the defaults to something more reasonable](https://groups.google.com/d/msg/emscripten-discuss/OY_6JCIjimc/6IrUGdjbBQAJ).

The second reason is much more interesting: Emscripten emits a combination of WebAssembly and JavaScript, conceptually like this:

The circles represent functions and the arrows are calls. Some of those functions may be roots, things we must keep alive, and we want to perform Dead Code Elimination (DCE), which is to remove everything not reachable from a root. But if we do this while looking at just one side of things (just JavaScript, or just WebAssembly) then we have to consider anything reachable from the other as a root, and so we would not be able to remove things like the last 2 parts of the chain on top and the entire cycle on bottom.

Things actually weren’t quite so bad before, as we did consider some connections between the two domains — enough to do a decent job for larger programs (e.g., we only include necessary JS library code, so you don’t get WebGL support if you don’t need it). But we failed to remove core runtime components when you didn’t use them, which is very noticeable in smaller programs.

The solution to this is something we call, for lack of a better name, **meta-DCE**. It looks at the combined graph of WebAssembly and JavaScript as a whole. In practice, this works by scanning the JavaScript side and passing that information into Binaryen’s [wasm-metadce](https://github.com/WebAssembly/binaryen/blob/master/src/tools/wasm-metadce.cpp#L18) tool, which can then see the full picture and figure out what can be eliminated. It removes the unnecessary WebAssembly things, optimizes the module (removing things may open up new optimization opportunities in the remaining code), and reports back about what can be removed in JavaScript (which the Emscripten JavaScript optimizer stubs out, and we rely on the Closure Compiler to clean up all the rest).

The need to DCE JavaScript and WebAssembly together is inherent and unavoidable whenever a project contains both JavaScript and WebAssembly and allows for interesting connections between them. Such applications are expected to become more common and so this issue will be important not just in Emscripten. Perhaps, for example, Binaryen’s wasm-metadce tool could be integrated as an option in JavaScript module bundlers: that way if you include a WebAssembly library then the parts of it you don’t actually use can be automatically removed.

### More on Code Size

Let’s go back to a C hello world. To stress the importance of optimizations, if you compile it with just **-s WASM=1** (build to wasm, no optimizations specified) you will get 44,954 bytes of WebAssembly and 100,462 of JavaScript. Without optimizations the compiler makes no effort to reduce code size, so the output contains things like comments and whitespace and unnecessary code. Adding **-Os –closure 1** to optimize for size, we get 2,438 bytes of WebAssembly and 11,690 of JavaScript, as mentioned earlier in this post. That’s much better — over 10x smaller than the unoptimized build, in fact — but why isn’t that even smaller? In fact, why isn’t it just outputting **console.log(“hello, world”)**?

C hello world uses [ printf](https://linux.die.net/man/3/printf), which is implemented in libc (

[musl](https://www.musl-libc.org/)in Emscripten).

`printf`

uses libc streams code that is generic enough to handle not just printing to the console but also arbitrary devices like files, and it implements buffering and error handling, etc. It’s unreasonable to expect an optimizer to remove all that complexity — really, the issue is that if we want to just print to the console then we should use a simpler API than `printf`

.One option is to use [ emscripten_log](https://kripken.github.io/emscripten-site/docs/api_reference/emscripten.h.html#c.emscripten_log), which only prints to the console, but it supports a bunch of options (like printing stack traces, formatting, etc.) so it doesn’t help that much in reducing code size. If we really want to just use

`console.log`

, we can, by using [EM_ASM](https://kripken.github.io/emscripten-site/docs/api_reference/emscripten.h.html#c.EM_ASM), which is a way to call arbitrary JavaScript:

```
#include <emscripten.h>
int main() {
EM_ASM({
console.log("hello, world!");
});
}
```


(We can also receive parameters and return a result, so we could implement our own minimal logging method this way.) This file compiles to 206 bytes of WebAssembly and 10,272 of JavaScript. That gets us almost where we want, but why is the JavaScript still not tiny? That’s because Emscripten’s JavaScript output supports a bunch of things:

- It can run on the Web, in Node.js, and in various JavaScript VM shells. We have a bunch of code to smooth over the differences between those.
- The WebAssembly loading code supports a bunch of options like using
[streaming](https://hacks.mozilla.org/2018/01/making-webassembly-even-faster-firefoxs-new-streaming-and-tiering-compiler/)if available. - Hooks are provided to let you run code at various points in the program’s execution (just before
`main()`

, for example). These are useful since WebAssembly startup is asynchronous.

All those are fairly important so it’s hard to just remove them. But in the future perhaps those could be made optional, and maybe we can find ways to do them in less code.

### Looking Forward

With meta-DCE in place, we have most of the optimization infrastructure we need for code size. But there are more things we can do, in addition to the possible JavaScript improvements mentioned at the end of the last section. Want to get involved? Take a look at the issues below, and see if there’s something you’d like to look into:

[Modularizing Emscripten’s JavaScript libraries and output](https://github.com/kripken/emscripten/issues/5828)might give code size wins.[Ongoing](https://github.com/WebAssembly/binaryen/pull/1352)[wasm](https://github.com/WebAssembly/binaryen/pull/1334)[shrinking](https://github.com/WebAssembly/binaryen/pull/1297)[work](https://github.com/WebAssembly/binaryen/pull/1344)[is](https://github.com/WebAssembly/binaryen/pull/1179)[happening](https://github.com/WebAssembly/binaryen/pull/1375)in the Binaryen optimizer.

## About Alon Zakai

Alon is on the research team at Mozilla, where he works primarily on Emscripten, a compiler from C and C++ to JavaScript. Alon founded the Emscripten project in 2010.

## 3 comments

Hernan SaezJanuary 30th, 2018 at 10:24Josh TriplettJanuary 30th, 2018 at 11:55Alon ZakaiJanuary 30th, 2018 at 12:28