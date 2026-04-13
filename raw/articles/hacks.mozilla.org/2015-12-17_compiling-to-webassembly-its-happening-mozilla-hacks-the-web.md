---
title: 'Compiling to WebAssembly: It’s Happening! – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2015/12/compiling-to-webassembly-its-happening/
author: Alon Zakai
published: '2015-12-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[WebAssembly](https://github.com/WebAssembly/design) is a new binary format for compilation to the web. It is in the process of being designed and implemented as we speak, in collaboration among the major browser vendors. Things are moving quickly! In this post we’ll show some of our recent progress with a deep dive into the toolchain side of WebAssembly.

For WebAssembly to be usable, we need two major components: **toolchains** that **compile** code into WebAssembly, and **browsers** that can **execute** that output. Both of those components depend on progress in finishing the WebAssembly [spec](https://github.com/WebAssembly/spec), but otherwise are largely separate engineering efforts. This separation is a good thing, as it will enable compilers to emit WebAssembly that runs in any browser, and browsers to run WebAssembly no matter which compiler generated it; in other words, it allows multiple toolchains and multiple browsers to work together, improving user choice. The separation also allows work on the two components to proceed in parallel right now.

A new project on the toolchain side of WebAssembly is ** Binaryen**. Binaryen is a compiler infrastructure library for WebAssembly, written in C++. If you’re not working on a WebAssembly compiler yourself, you’ll probably never need to know anything about it, but if you use a WebAssembly compiler then it might use Binaryen for you under the hood; we’ll see examples of that later.

At Binaryen’s core is a modular set of classes that can parse and emit WebAssembly, as well as represent it in an [AST](https://github.com/WebAssembly/design/blob/master/AstSemantics.md) designed for writing flexible transformation passes on. Built on top of that are several useful tools:

- The
**Binaryen shell,**which can load a WebAssembly module, transform it, execute it in an interpreter, print it, etc. Loading and printing use WebAssembly’s current temporary s-expression format, which has the suffix .wast (work is underway on designing the[WebAssembly binary format](https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md), as well as the final[text format](https://github.com/WebAssembly/design/blob/master/TextFormat.md), but they aren’t ready yet). **asm2wasm**, which compiles asm.js into WebAssembly.**wasm2asm**, which compiles WebAssembly into asm.js. (This is a work in progress.)**s2wasm**, which compiles .s files, in the format emitted by the[new WebAssembly backend being developed in LLVM](http://llvm.org/devmtg/2015-10/slides/BastienGohman-WebAssembly-HereBeDragons.pdf), to WebAssembly.**wasm.js**, a port of Binaryen itself to JavaScript. This lets us run all the above components on a web page or any other JavaScript environment.

For a general overview of Binaryen, you can see [these slides](https://kripken.github.io/talks/wasm.html) from a talk I recently gave. Don’t skip [slide #9](https://kripken.github.io/talks/wasm.html#/9) :)

It’s important to note that WebAssembly is still in the design phase, and the formats that Binaryen can read and write (.wast, .s) are not final. Binaryen has been constantly updating with those changes; the rate of churn is decreasing, but expect breakage.

Let’s discuss some of the specific areas where Binaryen can be helpful.

### Compiling to WebAssembly using Emscripten

Emscripten can compile C and C++ to asm.js, and Binaryen’s asm2wasm tool can compile asm.js to WebAssembly, so together Emscripten+Binaryen provide a complete way to compile C and C++ to WebAssembly. You can run asm2wasm on asm.js code directly (it can be run on the commandline), but it’s easiest to let Emscripten do it for you, using something like

emcc file.cpp -o file.js -s ‘BINARYEN=”path-to-binaryen”’

Emscripten will compile file.cpp, and emit a main JavaScript file and a separate file for the WebAssembly output, in .wast format. Under the hood, Emscripten compiles to asm.js, then runs asm2wasm on the asm.js file to produce the .wast file. For more details, see the [Emscripten wiki page on WebAssembly](https://github.com/kripken/emscripten/wiki/WebAssembly).

But wait, what good is it to compile to WebAssembly when browsers don’t support it yet? Good question :) Yes, we don’t want to ship this code since browsers can’t run it. But it is still very useful for *testing* purposes: we want to know that Emscripten can compile properly to WebAssembly as soon as we can, since we don’t want to wait on browser support.

But how can we check that Emscripten is in fact compiling properly to WebAssembly, if we can’t run it? For that, we can use wasm.js, which Emscripten integrated into our output .js file when we ran that emcc command before. wasm.js contains portions of Binaryen compiled to JavaScript, including the Binaryen interpreter. If you run file.js (in node.js, or on a web page) then what happens is the interpreter will execute that WebAssembly. That lets us actually verify that the compiled WebAssembly code does the right thing. You can see an example of such a compiled program [here](https://kripken.github.io/talks/wasm.html#/11), and there are some more builds for testing purposes in the [build suite repo](https://github.com/WebAssembly/build-suite).

Of course, we are not quite on as solid ground as we would like, given this weird testing environment: a C++ program compiled to WebAssembly, running in a WebAssembly interpreter itself compiled from C++ to JavaScript, and no other way to run the program yet. But we have a few reasons to be confident in the results:

- This output passes the Emscripten test suite. That includes many real-world codebases (Python, zlib, SQLite, etc.) as well as lots of unit tests for corner cases in C and C++. Experience has shown that when that test suite is passed, it’s very likely that other code will work too.
- The Binaryen interpreter passes the WebAssembly spec test suite, indicating that it is running WebAssembly properly. In other words, when browsers get native support, they should run it in the same way (except much faster! this code is running in a simple intepreter for testing purposes, so it’s very slow; but note that there is work in progress on
[fast](https://github.com/WebAssembly/design/blob/master/FAQ.md#can-the-polyfill-really-be-efficient)[ways](https://github.com/WebAssembly/polyfill-prototype-2)[to](https://github.com/WebAssembly/binaryen/blob/master/src/wasm2asm.h)[polyfill](https://remysharp.com/2010/10/08/what-is-a-polyfill)). - This output was generated using Emscripten, which is a stable compiler used in production, and a relatively small amount of code on top of that in Binaryen (just a few thousand lines). The less new code, the less risk of bugs.

Overall, this indicates that we are in good shape here, and can compile C and C++ to WebAssembly today using Emscripten + Binaryen, even if browsers can’t run it yet.

Note that aside from emitting WebAssembly, the builds that we emit in this mode use everything else from the Emscripten toolchain normally: Emscripten’s port of the musl libc and syscalls to access it, OpenGL/WebGL code, browser integration code, node.js integration code, and so forth. As a result, this supports everything Emscripten already does, and existing projects using Emscripten can switch to emitting WebAssembly with just the flip of a switch. This is a key part of letting existing C++ projects that compile to the web benefit from WebAssembly when it launches, with little or no effort on their part.

### Using the new experimental LLVM WebAssembly backend with Emscripten

We just saw an important milestone for Emscripten, in that it can compile to WebAssembly and even test that we get valid output. But things don’t stop there: that was using Emscripten’s current asm.js compiler backend, together with asm2wasm. There is a new [LLVM](http://llvm.org/) backend for WebAssembly in development directly in the upstream LLVM repository, and while it isn’t ready for general use yet, in the long term it will be very important. Binaryen has support for that too.

The LLVM backend, like most LLVM backends, emits assembly code, in this case in a specific .s format. That output is close to WebAssembly, but not identical – it looks more like the output of a C compiler (linear list of instructions, one instruction per line, etc.) rather than WebAssembly’s more structured [AST](https://github.com/WebAssembly/design/blob/master/AstSemantics.md). The .s file can be translated into WebAssembly in a fairly straightforward way, though, and Binaryen includes s2wasm, a tool that translates .s to WebAssembly. It can be run standalone on the commandline, but also has Emscripten integration support: Emscripten now has a WASM_BACKEND option, which you can use like this:

emcc file.cpp -o file.js -s ‘BINARYEN=”path-to-binaryen”’ -s WASM_BACKEND=1

(Note that you also need the BINARYEN option, as s2wasm is part of Binaryen.) When that option is provided, Emscripten uses the new WebAssembly backend instead of the existing asm.js one. After calling the backend and receiving .s from it, Emscripten calls s2wasm to convert that to WebAssembly. Some examples of programs you can build with the new backend are [on the Emscripten wiki](https://github.com/kripken/emscripten/wiki/WebAssembly).

There are, therefore, two ways to compile to WebAssembly using Binaryen: **Emscripten + asm.js backend + asm2wasm**, which works right now and should be fairly robust and reliable, and **Emscripten + new WebAssembly backend + s2wasm**, which is not yet fully functional, but as the WebAssembly backend matures it should become a powerful option, and hopefully will replace the asm.js backend in the future. The goal is to make that transition seamless: flipping between the two WebAssembly modes is just a matter of setting an option, as we saw.

The same is also true between asm.js and WebAssembly support in Emscripten, which is also just an option you can set, and the transition there should be seamless as well. In other words, there will be a straight and simple path from

- using Emscripten to emit asm.js today, to
- using it to emit WebAssembly using asm2wasm (possible today, but browsers can’t run it yet), to
- using it to emit WebAssembly using the new LLVM backend (once the backend is ready).

Each step should provide substantial benefits, with no extra effort for developers.

In closing, note that while this post focused on using Binaryen with Emscripten, at its core it is designed to be a general-purpose WebAssembly library in C++: If you want to write something toolchain-related with WebAssembly, you probably need code to read WebAssembly, print it out, an AST to operate on, etc., which Binaryen provides. It was very useful in writing asm2wasm, s2wasm, etc., and hopefully other projects will find it useful as well.

## About Alon Zakai

Alon is on the research team at Mozilla, where he works primarily on Emscripten, a compiler from C and C++ to JavaScript. Alon founded the Emscripten project in 2010.

## 21 comments

Juan LinietskyDecember 17th, 2015 at 11:35EtieneDecember 17th, 2015 at 13:19RobinDecember 17th, 2015 at 13:27Tom MarsdenDecember 17th, 2015 at 16:18jiyinyiyongDecember 17th, 2015 at 19:16BanMeDecember 17th, 2015 at 20:56Sajid QureshiDecember 18th, 2015 at 03:08About TimeDecember 18th, 2015 at 06:25Steve NaidamastDecember 18th, 2015 at 08:43Alon ZakaiDecember 18th, 2015 at 09:11Steve NaidamastDecember 18th, 2015 at 12:19JimDecember 19th, 2015 at 01:21hutzlibuDecember 19th, 2015 at 01:33Francis Kim (@franciskim_co)December 19th, 2015 at 19:34BaasBartelsDecember 20th, 2015 at 01:03DustyDecember 21st, 2015 at 01:19Jim LoneroDecember 21st, 2015 at 09:12Alon ZakaiDecember 21st, 2015 at 10:15JSDecember 28th, 2015 at 06:44RavenmetrixJanuary 2nd, 2016 at 07:32AndyXJanuary 6th, 2016 at 19:24