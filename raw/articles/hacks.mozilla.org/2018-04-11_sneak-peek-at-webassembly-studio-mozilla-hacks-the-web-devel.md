---
title: Sneak Peek at WebAssembly Studio – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/04/sneak-peek-at-webassembly-studio/
author: Michael Bebenita
published: '2018-04-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[WebAssembly.Studio](https://webassembly.studio/) is an online IDE (integrated development environment) that helps you learn and teach others about WebAssembly. It’s also a Swiss Army knife that comes in handy whenever working with WebAssembly.

We started working on WebAssembly Studio in late December 2017, in an attempt to merge two existing tools that we had developed: [WasmExplorer](https://mbebenita.github.io/WasmExplorer/) and [WasmFiddle](https://wasdk.github.io/WasmFiddle/). Since then, thanks to several contributors who jumped into the project early, we’ve made quite a bit of progress. We’ve merged those two tools and added several new features. Our beta (more like an alpha) release is now live at [https://webassembly.studio](https://webassembly.studio) and we are very interested in your feedback.

### Quick Start

To get started with the example above, simply click **Build** and then **Run**. WebAssembly Studio first compiles `main.c`

to `out/main.wasm`

and then creates an iframe sandbox in which it loads `main.html`

. The HTML file loads `main.js`

which loads and executes the WebAssembly module that ultimately prints “Hello World”. To understand exactly what’s going on, read the README.md file included in the project. This is an example I put together to show how C programs interact with WebAPIs. Our hope is that others will put together interesting examples and use WebAssembly Studio as a teaching tool.

### Overview of Features

#### C/C++/Rust Support

WebAssembly Studio has basic (very primitive) support for C, C++ and Rust out of the box. At the moment, compilation services run mostly server-side but we’re hoping to do more of this work on the client.

#### Editable Compiler Artifacts

WebAssembly binary modules (.wasm) as well as text files (.wat) are fully editable in WebAssembly Studio. Try opening `out/main.wasm`

and you’ll see the disassembled .wat output. You can actually edit this text, and when you save, the original .wasm file will be reassembled.

![](../../assets/db4f07dbb71ca450.png)


![](../../assets/db4f07dbb71ca450.png)

![](../../assets/a4c197b2bffd6353.png)


![](../../assets/a4c197b2bffd6353.png)

#### Easily Accessible Tools

Many of the interesting features in WebAssembly Studio are stashed away under context menus. For instance, if you right-click on the `out/main.wasm`

file, you’ll see a pop-up menu appear with several commands:

![](../../assets/0fe8a538c062f167.png)


![](../../assets/0fe8a538c062f167.png)

You can use these context menu commands to apply various transformations on .wasm files:

- Validate uses
[Binaryen](https://github.com/WebAssembly/binaryen)to verify that a WebAssmebly Module is valid. - Optimize runs several Binaryen optimization passes over a WebAssembly module.

![](../../assets/d01ad1fd80bf2c70.png)


![](../../assets/d01ad1fd80bf2c70.png)

- Disassemble uses
[Wabt](https://github.com/WebAssembly/wabt)to convert the file to WebAssembly text format. This can then be edited and reassembled back into a WebAssembly file.

Some of the commands generate new files, for example “Firefox x86” will produce a .x86 file with the disassembled output from Firefox’s WebAssembly engine. While this may not be very useful (or actionable) to a JavaScript developer, I find it useful when teaching others about WebAssembly. (It’s proof that WebAssembly is low-level!)

![](../../assets/2cd6c6fe888dc368.png)


![](../../assets/2cd6c6fe888dc368.png)

- Binary Explorer helps you understand how WebAssembly code is represented at a binary level.

![](../../assets/9f7cfa6f94983e34.png)


![](../../assets/9f7cfa6f94983e34.png)

![](../../assets/32fb0557449c11aa.png)


![](../../assets/32fb0557449c11aa.png)

- Generate Call Graph plots the caller/callee relationships between functions (including imports and exports) to help you understand what’s included in a WebAssembly module.

![](../../assets/b7f7843999233da1.png)


![](../../assets/b7f7843999233da1.png)

Some of the features in WebAssembly Studio need hosted back-end services (compilation), but many others run directly in the browser. [Binaryen](https://github.com/WebAssembly/binaryen/), [Wabt](https://github.com/WebAssembly/wabt), [Capstone.js](https://alexaltea.github.io/capstone.js/) are all compiled to WebAssembly and run in the browser. This has the added benefit that we can scale much more easily, with less load on the server.

For a dose of WebAssembly magic, right click on `main.c`

and select:

… that’s right, [Clang Format](https://github.com/tbfleming/cib) is also compiled to WebAssembly, runs locally, and works great.

#### Interactive Embeddings

Interactive embeddings of WebAssembly Studio projects are now possible thanks to [embed.ly](http://embed.ly), a system for embedding interactive content in a wide variety of web [platforms](http://embed.ly/customers), including [medium.com](http://embed.ly). You can simply paste the link to a **Forked** project into your medium.com post

.

### What’s Next

Over the next few months we’re going to:

- Add better support for C/C++/Rust projects. For C/C++ applications we’re currently using the
[LLVM](https://llvm.org/)backend by itself, but we’re also hoping to add support for[Emscripten](https://github.com/kripken/emscripten)using that backend so that you can use APIs like SDL and OpenGL. For Rust, we’d like to support Cargo. - Continue to add new features and integrate additional tools into WebAssembly Studio.
- Make it possible to download and build WebAssembly Studio projects locally using familiar tools.
- Improve UX, error reporting, and general performance optimizations.

Want to learn more or get more involved in this project? Please share feedback, file issues, and add feature requests on the [WebAssembly Studio](https://github.com/wasdk/WebAssemblyStudio) GitHub repo. If you want to get more involved with WebAssembly [check out the main repo](https://github.com/webassembly) to learn more about the project and its infrastructure.

## 21 comments

Chris SellsApril 11th, 2018 at 10:24Michael BebenitaApril 11th, 2018 at 11:23MuzafarApril 12th, 2018 at 07:24Michael BebenitaApril 12th, 2018 at 08:49Christophe CoevoetApril 11th, 2018 at 10:39Michael BebenitaApril 11th, 2018 at 12:22Zachary CarterApril 11th, 2018 at 11:32Michael BebenitaApril 11th, 2018 at 11:56David RossApril 11th, 2018 at 11:48Michael BebenitaApril 11th, 2018 at 11:50Jeff NelsonApril 11th, 2018 at 12:00Michael BebenitaApril 11th, 2018 at 12:04jensApril 11th, 2018 at 13:40Michael BebenitaApril 12th, 2018 at 08:40Leviathan JeanisApril 12th, 2018 at 07:15Michael BebenitaApril 12th, 2018 at 08:45Josh YatesApril 12th, 2018 at 08:21Dennis van LeeuwenApril 12th, 2018 at 08:40NileshApril 12th, 2018 at 08:52SamuelApril 12th, 2018 at 10:03Kesus KimApril 12th, 2018 at 17:25