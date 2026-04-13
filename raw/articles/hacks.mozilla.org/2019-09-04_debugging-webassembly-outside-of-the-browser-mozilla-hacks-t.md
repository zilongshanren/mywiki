---
title: Debugging WebAssembly Outside of the Browser – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2019/09/debugging-webassembly-outside-of-the-browser/
author: Dan Callahan
published: '2019-09-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

WebAssembly has begun to establish itself [outside of the browser](https://hacks.mozilla.org/2019/03/standardizing-wasi-a-webassembly-system-interface/) via dedicated runtimes like Mozilla’s [Wasmtime](https://wasmtime.dev/) and Fastly’s [Lucet](https://github.com/fastly/lucet/). While the promise of a new, universal format for programs is appealing, it also comes with new challenges. For instance, how do you debug .wasm binaries?

At Mozilla, we’ve been prototyping ways to enable source-level debugging of `.wasm`

files using traditional tools like [GDB](https://www.gnu.org/software/gdb/) and [LLDB](https://lldb.llvm.org/).

The [screencast](https://www.youtube.com/watch?v=PevI_Mn-UUE) below shows an example debugging session. Specifically, it demonstrates using Wasmtime and LLDB to inspect a program originally written in Rust, but compiled to WebAssembly.

This type of source-level debugging was previously impossible. And while the implementation details are subject to change, the developer experience—attaching a normal debugger to Wasmtime—will remain the same.

By allowing developers to examine programs in the same execution environment as a production WebAssembly program, Wasmtime’s debugging support makes it easier to catch and diagnose bugs that may not arise in a native build of the same code. For example, the [WebAssembly System Interface](https://wasi.dev/) (WASI) treats filesystem access more strictly than traditional Unix-style permissions. This could create issues that only manifest in WebAssembly runtimes.

Mozilla is proactively working to ensure that WebAssembly’s development tools are capable, complete, and ready to go as WebAssembly expands beyond the browser.

Please try it out and let us know what you think.


Note:Debugging using Wasmtime and LLDB should work out of the box on Linux with Rust programs, or with C/C++ projects built via the[WASI SDK].Debugging on macOS currently requires

[building and signing]a more recent version of LLDB.Unfortunately, LLDB for Windows does not yet support

[JIT debugging].

*Thanks to Lin Clark, Till Schneidereit, and Yury Delendik for their assistance on this post, and for their work on WebAssembly debugging.*

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.