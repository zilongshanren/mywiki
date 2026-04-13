---
title: WebAssembly Browser Preview – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/10/webassembly-browser-preview/
author: Luke Wagner
published: '2016-10-31'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Since the [last WebAssembly milestone](https://hacks.mozilla.org/2016/03/a-webassembly-milestone/) we reached in March, we’ve been hard at work in the [WebAssembly Community Group](http://webassembly.org/) to define a standard and to implement that standard in our respective browsers.

I’m happy to say now that we have a binary format release candidate and there are compatible implementations already in trunk [SpiderMonkey](https://bugzilla.mozilla.org/show_bug.cgi?id=wasm) and [V8](http://v8project.blogspot.com/2016/10/webassembly-browser-preview.html), with active ongoing work in [Chakra](https://blogs.windows.com/msedgedev/2016/10/31/webassembly-browser-preview/) and [JavaScriptCore](https://bugs.webkit.org/show_bug.cgi?id=159775). Having reached this important milestone, we’d now like to encourage broader feedback from the community, especially anyone who has been waiting for things to settle down before taking a look.

During this “Browser Preview” period, WebAssembly will still be behind a flag and there will be at least one planned change to reset the [binary version](http://webassembly.org/docs/binary-encoding/#high-level-structure) to 1, where we hope it will stay forever. By design that means no one should attempt to use WebAssembly binaries in production yet. However, assuming no issues are found that require substantial time to address, the WebAssembly Community Group would like to mark an initial version of the standard as “done” in Q1 2017 which would then enable browsers to start shipping WebAssembly without a flag. For our part, in Firefox, this green light would mean shipping WebAssembly in Firefox 52 (March 2017).

## What’s new since the last milestone?

If you’ve been following the development, there’s been a lot of progress since the last milestone in March:

- Hundreds of issues filed and resolved in the WebAssembly
[design](http://github.com/webassembly/design)and[spec](http://github.com/webassembly/spec/)repos. - Three cross-browser-and-toolchain-synchronized iterations of the binary format.
- A major expansion of the
[JS WebAssembly API](http://webassembly.org/docs/js), which now allows developers to explicitly request[parallel compilation](https://github.com/WebAssembly/design/blob/master/JS.md#webassemblycompile),[machine-code caching and code sharing](https://github.com/WebAssembly/design/blob/master/JS.md#structured-clone-of-a-webassemblymodule),[dynamic linking](https://github.com/WebAssembly/design/blob/master/DynamicLinking.md)(and eventually[streaming compilation](https://github.com/WebAssembly/design/blob/master/FutureFeatures.md#streaming-compilation)). - On the Mozilla side, a complete (modulo boogs
) implementation of WebAssembly in Firefox, including extension of the JIT compiler backend to support i64 on 32-bit and the full suite of[1](https://bugzilla.mozilla.org/show_bug.cgi?id=1313176),[2](https://bugzilla.mozilla.org/show_bug.cgi?id=1313180)[IEEE 754 floating point conversion operators](https://github.com/WebAssembly/design/blob/master/Semantics.md#datatype-conversions-truncations-reinterpretations-promotions-and-demotions). - Progress and optimization of the WebAssembly compiler pipeline including the upstream WebAssembly
[LLVM](https://github.com/llvm-mirror/llvm/blob/master/lib/Target/WebAssembly/README.txt)[backend](https://github.com/kripken/emscripten/wiki/New-WebAssembly-Backend)and[Binaryen](https://github.com/WebAssembly/binaryen#binaryen).

[With all this work, we can also get some initial numbers on classic ][Emscripten-internal measurements](https://github.com/kripken/emscripten/blob/caa37c2e281d30195bee01207ac6c1aa61b6f831/tests/test_benchmark.py) comparing end-to-end asm.js vs WebAssembly [measured on 64-bit Firefox 52 (Nightly), Intel Core i7-2600 @ 3.40GHz, Linux]:

![asmjs-wasm-comparison](../../assets/d368114413d66d1f.png)


The speedups we see here are due to a combination of [Binaryen](https://github.com/WebAssembly/binaryen#binaryen) optimizations, browser optimizations and new hardware capabilities exposed by WebAssembly. Optimization of the entire pipeline is still ongoing, so the results will hopefully improve before launch (~~with anomalies, like the slight slowdown in Bullet, understood and fixed~~ *UPDATE 11/21: fixed by more recent Binaryen optimizations*). But even now, we can see that WebAssembly is a distinct improvement, even for Firefox users who were already benefitting from

[asm.js optimizations](https://blog.mozilla.org/luke/2015/02/18/microsoft-announces-asm-js-optimizations/#asmjs-opts).

Moreover, computational kernels which stress new WebAssembly operations can show far greater speedups. For example, using the same experimental setup as above, a [64-bit integer arithmetic kernel](https://github.com/kripken/emscripten/blob/caa37c2e281d30195bee01207ac6c1aa61b6f831/tests/test_benchmark.py#L500) runs 8.93× slower than native speed in asm.js due to emulation using 32-bit JS operations, while it runs at only 1.13× slower than native speed in WebAssembly.

## Trying it out

To try out WebAssembly, head over to [webassembly.org](http://webassembly.org) which contains instructions for [compiling a WebAssembly module with Emscripten](http://webassembly.org/getting-started/developers-guide/) and then [loading and running a WebAssembly module from JavaScript](http://webassembly.org/getting-started/js-api/).

Since this is still pretty bleeding-edge stuff, a few caveats apply:

First, to reiterate above: Things will change right up until the standard is marked done and WebAssembly is enabled in browsers (and then it’s back to *don’t break the web* as usual!). To help communicate changes to the community, we’ll post past or planned changes to our [roadmap](http://webassembly.org/roadmap/) page. It’s also a good idea to always test with [Nightly](http://nightly.mozilla.org/) builds.

Second, the full WebAssembly “spec” is currently scattered across various Markdown files in the [design](https://github.com/webassembly/design) repo, and some details (like the validation rules) are only present in the [reference interpreter](https://github.com/WebAssembly/spec/tree/master/interpreter). During the Browser Preview, we’ll be collecting these scattered bits and writing a single, coherent specification in the [spec](https://github.com/WebAssembly/spec/) repo.

Finally, while you can currently see the WebAssembly text format rendered in Firefox’s Debugger source view, the full debugger is not yet working (though we’re [getting close](https://www.youtube.com/watch?v=R1WtBkMeGds)!). In the meantime, though, experimenters will need to use the time-honored tradition of `printf`

-debugging.

With those caveats out of the way, we’re already seeing a lot of exciting experimentation and we hope to see more in the coming months. There are a number of places to provide feedback depending on whether your feedback pertains to the overall design, the reference interpreter, or a specific browser implementation; we’ve collected [a list of feedback links](http://webassembly.org/community/feedback/) at webassembly.org. Happy hacking!

## About Luke Wagner

Luke Wagner is a Mozilla software engineer and hacks on JavaScript and WebAssembly in Firefox.

## 5 comments

Rob GOctober 31st, 2016 at 16:41AndrewNovember 1st, 2016 at 11:02chadNovember 1st, 2016 at 22:47mihaiNovember 3rd, 2016 at 05:02Luke WagnerNovember 3rd, 2016 at 06:26