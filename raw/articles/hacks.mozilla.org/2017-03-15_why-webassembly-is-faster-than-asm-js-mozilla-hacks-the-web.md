---
title: Why WebAssembly is Faster Than asm.js – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/03/why-webassembly-is-faster-than-asm-js/
author: Alon Zakai
published: '2017-03-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[WebAssembly](http://webassembly.org/), a new binary execution format for the Web, is starting to arrive in [stable versions of browsers](https://hacks.mozilla.org/2017/03/firefox-52-introducing-web-assembly-css-grid-and-the-grid-inspector/). A major goal of WebAssembly is to be *fast*. This post gives some technical details about how it achieves that.

Of course, “fast” is relative. Compared to JavaScript and other dynamic languages, WebAssembly is fast because it is [statically typed and simple to optimize](https://hacks.mozilla.org/2017/02/what-makes-webassembly-fast/). But WebAssembly is also intended to be as fast as native code. [asm.js](http://asmjs.org/) has already come [quite close to that](https://hacks.mozilla.org/2013/12/gap-between-asm-js-and-native-performance-gets-even-narrower-with-float32-optimizations/), and WebAssembly narrows the gap further. This post focuses therefore on why WebAssembly is faster than asm.js.

Before we start, the usual caveats: Performance is tricky to measure, and has many aspects. Also, in a new technology there are always going to be not-yet-optimized cases. So not every single benchmark will be fast on WebAssembly today. This post describes why WebAssembly *should* be fast; where it isn’t yet, those are bugs we need to fix.

With that out of the way, here is why WebAssembly is fast:

## 1. Startup

WebAssembly is designed to be small to download and fast to parse, so that even large applications start up quickly.

It’s actually not that easy to improve on the download size of gzipped minified JavaScript, as it’s [already fairly compact when compared with native code](http://mozakai.blogspot.com/2011/11/code-size-when-compiling-to-javascript.html). Still, [WebAssembly’s binary format](https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md) can improve on that, by being carefully designed for size in mind (indexes are [LEB128s](https://en.wikipedia.org/wiki/LEB128), etc.). It is often around [10–20% smaller](http://kripken.github.io/talks/emwasm.html#/9) (comparing gzipped sizes).

WebAssembly improves on parsing in a much bigger way: It can be parsed [an order of magnitude faster than JavaScript](http://webassembly.org/docs/faq/#why-create-a-new-standard-when-there-is-already-asmjs). This mostly comes down to binary formats being faster to parse, especially ones designed for that. WebAssembly also makes it easy to parse (and optimize) functions in parallel, which helps a lot on multicore machines.

Total startup time can include factors other than downloading and parsing, such as the VM fully optimizing the code, or downloading additional data files that are necessary before execution, etc. But downloading and parsing are *unavoidable* and therefore important to improve upon as much as possible. All the rest can be optimized or mitigated, either in the browser or in the app (for example, fully optimizing the code can be avoided by using a [baseline compiler](https://bugzilla.mozilla.org/show_bug.cgi?id=1232205) or interpreter for WebAssembly, for the first few frames).

## 2. CPU features

One trick that’s made asm.js so fast is that while all JavaScript numbers are doubles, in asm.js an addition will have a bitwise-and operation right after it, which makes it logically equivalent to the CPU doing a simple integer addition, which CPUs are very good at. So asm.js made it easy for VMs to use a lot of the full power of CPUs.

But asm.js was limited to things that are expressible in JavaScript. WebAssembly isn’t limited in that way, and lets us use even more CPU features, such as:

- 64-bit integers. Operations on them can be up to
[4x faster](http://kripken.github.io/talks/emwasm.html#/11). This can speed up hashing and encryption algorithms, for example. [Load and store offsets](http://webassembly.org/docs/rationale/#loadstore-addressing). This helps very broadly, basically anything that uses memory objects with fields at fixed offsets (C structs, etc.).- Unaligned loads and stores, avoiding asm.js’s need to mask (which asm.js did for Typed Array compatibility purposes). This helps with practically every load and store.
- Various CPU instructions like popcount, copysign, etc. Each of these can help in specific circumstances (e.g. popcount can help in
[cryptanalysis](https://en.wikipedia.org/wiki/Hamming_weight#Processor_support)).

How much a specific benchmark benefits will depend on whether it uses the features mentioned above. We often see a [5% speedup](http://kripken.github.io/talks/emwasm.html#/10) on average compared to asm.js. Further speedups are expected in the future from CPU features [like SIMD](https://github.com/WebAssembly/design/blob/master/FutureFeatures.md).

## 3. Toolchain Improvements

WebAssembly is primarily a compiler target, and therefore has two parts: Compilers that generate it (the toolchain side), and VMs that run it (the browser side). Good performance depends on both.

This was already the case with asm.js, and [Emscripten](http://kripken.github.io/emscripten-site/) did a bunch of toolchain optimizations, running LLVM’s optimizer and also Emscripten’s asm.js optimizer. For WebAssembly, we [built on top of that](http://kripken.github.io/emscripten-site/), but have also added some significant improvements while doing so. Both asm.js and WebAssembly are not typical compiler targets, and in similar ways, so lessons learned during the asm.js days helped do things better for WebAssembly. In particular:

- We replaced the Emscripten asm.js optimizer with the
[Binaryen](https://github.com/WebAssembly/binaryen)WebAssembly optimizer, which is designed for speed. That speed lets us run more costly optimization passes. For example, we[remove duplicate functions](https://github.com/WebAssembly/binaryen/blob/master/src/passes/DuplicateFunctionElimination.cpp)by default when optimizing, which often shrinks large compiled C++ codebases by around 5%. [Better optimizations for irreducible and convoluted control flow](https://github.com/WebAssembly/binaryen/blob/master/src/passes/RelooperJumpThreading.cpp), improving the[Relooper algorithm](https://github.com/WebAssembly/binaryen/blob/master/src/cfg/Relooper.h). Helps a lot on compiled interpreter-type loops.- The Binaryen optimizer was designed with experimentation in mind, and
[experiments with superoptimization](https://github.com/WebAssembly/binaryen/pull/900#issuecomment-279186640)have led to miscellaneous minor improvements — things which could have been done in asm.js too, had we thought of them.

Overall, these toolchain improvements help about as much as moving from asm.js to WebAssembly helps us ([7% and 5% on Box2D, respectively](http://kripken.github.io/talks/emwasm.html#/10)).

## 4. Predictably Good Performance

asm.js could run at [basically native speed](https://hacks.mozilla.org/2013/12/gap-between-asm-js-and-native-performance-gets-even-narrower-with-float32-optimizations/), but it never actually did so in all browsers consistently. The reason is that some tried to optimize it one way, some another, with differing results. Over time things [started to converge](https://hacks.mozilla.org/2015/03/asm-speedups-everywhere/), but the basic problem was that asm.js was not an actual standard: It was an informal spec of a subset of JavaScript, written by one vendor, that only gradually saw interest and adoption from the others.

WebAssembly, on the other hand, has been designed jointly by all major browsers. Unlike JavaScript, which could be made fast only using very [creative methods](https://hacks.mozilla.org/2017/02/what-makes-webassembly-fast/), or asm.js, which could be made fast using simple methods but not all browsers did so, WebAssembly has more agreement upon how to optimize it. There is still plenty of room for differentiation in VMs (different ways to tier compilation, AOT vs. JIT, etc.), but a good baseline of predictable performance can be expected across the entire Web.

## About Alon Zakai

Alon is on the research team at Mozilla, where he works primarily on Emscripten, a compiler from C and C++ to JavaScript. Alon founded the Emscripten project in 2010.

## 4 comments

Camilo MartinMarch 17th, 2017 at 08:57Alon ZakaiMarch 17th, 2017 at 11:30Carlos El JefeMarch 17th, 2017 at 18:25Adam ReedApril 1st, 2017 at 16:22