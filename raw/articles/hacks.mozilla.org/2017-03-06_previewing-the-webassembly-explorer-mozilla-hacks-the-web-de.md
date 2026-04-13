---
title: Previewing the WebAssembly Explorer – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/03/previewing-the-webassembly-explorer/
author: Dan Callahan
published: '2017-03-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[WebAssembly](https://developer.mozilla.org/en-US/docs/WebAssembly) is a new, cross-browser format for programs on the Web. You can read all about it in [Lin Clark](https://twitter.com/linclark)‘s six-part series, [A cartoon intro to WebAssembly](https://hacks.mozilla.org/2017/02/a-cartoon-intro-to-webassembly/). Unlike JavaScript, WebAssembly is a binary format, which means developers need new tools to help understand and experiment with WebAssembly. One such tool is Mozilla’s [WebAssembly Explorer](https://mbebenita.github.io/WasmExplorer/).

The video below demonstrates the basic functions of the WebAssembly Explorer, which lets developers type in simple C or C++ programs and compile them to WebAssembly.

One advantage of WebAssembly—and of the WebAssembly Explorer—is that developers can see exactly what optimizations are being applied to their code. For example, the WebAssembly compiler in the video is able to use C’s type information to automatically select between traditional division and a more efficient bit-shifting shortcut. With JavaScript, a browser’s JIT compiler may eventually arrive at the same optimization, but there are no guarantees. Ahead-of-time compilation also avoids the profiling and observational overhead associated with opportunistic JIT compilers.

While the WebAssembly Explorer is a great learning tool, it’s still in early development and not yet suitable for complex programs. Developers who need a production-grade compiler suite should look to [Emscripten](http://emscripten.org), which was originally written to output [asm.js ](https://en.wikipedia.org/wiki/Asm.js)but has now been extended to produce WebAssembly as well.

You can find the WebAssembly Explorer’s source code [on GitHub](https://github.com/mbebenita/wasmexplorer), and you can begin experimenting with WebAssembly when it lands in Firefox 52 later this week.

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 5 comments

Rodolfo De NadaiMarch 7th, 2017 at 08:45JjMarch 7th, 2017 at 15:42Dan CallahanMarch 8th, 2017 at 07:23JeffreyMarch 30th, 2017 at 08:29Dan CallahanMarch 31st, 2017 at 14:31