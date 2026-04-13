---
title: Securing Firefox with WebAssembly – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/02/securing-firefox-with-webassembly/
author: Nathan Froyd
published: '2020-02-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Protecting the security and privacy of individuals is a [central tenet](https://www.mozilla.org/en-US/about/manifesto/) of Mozilla’s mission, and so we constantly endeavor to make our users safer online. With a complex and highly-optimized system like Firefox, [memory safety](https://hacks.mozilla.org/2019/01/fearless-security-memory-safety/) is one of the biggest security challenges. Firefox is mostly written in C and C++. These languages are notoriously difficult to use safely, since any mistake can lead to complete compromise of the program. We work hard to [find and eliminate memory hazards](https://github.com/MozillaSecurity), but we’re also evolving the Firefox codebase to address these attack vectors at a deeper level. Thus far, we’ve focused primarily on two techniques:

[Breaking code into multiple sandboxed processes with reduced privileges](https://wiki.mozilla.org/Security/Sandbox)[Rewriting code in a safe language like Rust](https://hacks.mozilla.org/2019/02/rewriting-a-browser-component-in-rust/)

### A new approach

While we continue to make extensive use of both sandboxing and Rust in Firefox, each has its limitations. Process-level sandboxing works well for large, pre-existing components, but consumes substantial system resources and thus must be used sparingly. Rust is lightweight, but rewriting millions of lines of existing C++ code is a labor-intensive process.

Consider the [Graphite font shaping library](http://scripts.sil.org/cms/scripts/page.php?site_id=projects&item_id=graphite_home), which Firefox uses to correctly render certain complex fonts. It’s too small to put in its own process. And yet, if a memory hazard were uncovered, even a site-isolated process architecture wouldn’t prevent a malicious font from compromising the page that loaded it. At the same time, rewriting and maintaining this kind of domain-specialized code is not an ideal use of our limited engineering resources.

So today, we’re adding a third approach to our arsenal. [RLBox](https://rlbox.dev), a new sandboxing technology developed by researchers at the University of California, San Diego, the University of Texas, Austin, and Stanford University, allows us to quickly and efficiently convert existing Firefox components to run inside a WebAssembly sandbox. Thanks to the tireless efforts of [Shravan Narayan](https://shravanrn.com/), [Deian Stefan](https://cseweb.ucsd.edu/~dstefan/), [Tal Garfinkel](http://xenon.stanford.edu/~talg/), and [Hovav Shacham](https://www.cs.utexas.edu/~hovav/), we’ve successfully integrated this technology into our codebase and used it to sandbox Graphite.

This isolation will ship to Linux users in Firefox 74 and to Mac users in Firefox 75, with Windows support following soon after. You can read more about this work in the press releases from [UCSD](https://ucsdnews.ucsd.edu/pressrelease/researchers-develop-framework-that-improves-firefox-security) and [UT Austin](https://cns.utexas.edu/news/new-sandboxing-approach-in-web-browser-increases-security) along with the joint [research paper](https://usenix2020.rlbox.dev/). Read on for a technical overview of how we integrated it into Firefox.

### Building a wasm sandbox

The core implementation idea behind wasm sandboxing is that you can compile C/C++ into wasm code, and then you can compile that wasm code into native code for the machine your program actually runs on. These steps are similar to what you’d do [to run C/C++ applications in the browser](https://hacks.mozilla.org/2019/04/pyodide-bringing-the-scientific-python-stack-to-the-browser/), but we’re performing the wasm to native code translation ahead of time, when Firefox itself is built. Each of these two steps rely on significant pieces of software in their own right, and we add a third step to make the sandboxing conversion more straightforward and less error prone.

First, you need to be able to compile C/C++ into wasm code. As part of the WebAssembly effort, a wasm backend was added to [Clang and LLVM](https://llvm.org/). Having a compiler is not enough, though; you also need a standard library for C/C++. This component is provided via [wasi-sdk](https://github.com/CraneStation/wasi-sdk). With those pieces, we have enough to translate C/C++ into wasm code.

Second, you need to be able to convert the wasm code into native object files. When we first started implementing wasm sandboxing, we were often asked, “why do you even need this step? You could distribute the wasm code and compile it on-the-fly on the user’s machine when Firefox starts.” We could have done that, but that method requires the wasm code to be freshly compiled for every sandbox instance. Per-sandbox compiled code is unnecessary duplication in a world where every origin resides in a separate process. Our chosen approach enables sharing compiled native code between multiple processes, resulting in significant memory savings. This approach also improves the startup speed of the sandbox, which is important for fine-grained sandboxing, e.g. sandboxing the code associated with every font accessed or image loaded.

### Ahead-of-time compilation with Cranelift and friends

This approach does not imply that we have to write our own wasm to native code compiler! We implemented this ahead-of-time compilation using the same compiler backend that will eventually power the wasm component of Firefox’s JavaScript engine: [Cranelift](https://github.com/bytecodealliance/cranelift), via the Bytecode Alliance’s [Lucet compiler and runtime](https://github.com/bytecodealliance/lucet). This code sharing ensures that improvements benefit both our JavaScript engine and our wasm sandboxing compiler. These two pieces of code currently use different versions of Cranelift for engineering reasons. As our sandboxing technology matures, however, we expect to modify them to use the exact same codebase.

Now that we’ve translated the wasm code into native object code, we need to be able to call into that sandboxed code from C++. If the sandboxed code was running in a separate virtual machine, this step would involve looking up function names at runtime and managing state associated with the virtual machine. With the setup above, however, sandboxed code is native compiled code that respects the wasm security model. Therefore, sandboxed functions can be called using the same mechanisms as calling regular native code. We have to take some care to respect the different machine models involved: wasm code uses 32-bit pointers, whereas our initial target platform, x86-64 Linux, uses 64-bit pointers. But there are other hurdles to overcome, which leads us to the final step of the conversion process.

### Getting sandboxing correct

Calling sandboxed code with the same mechanisms as regular native code is convenient, but it hides an important detail. We cannot trust anything coming out of the sandbox, as an adversary may have compromised the sandbox.

For instance, for a sandboxed function:

```
/* Returns values between zero and sixteen. */
int return_the_value();
```


We cannot guarantee that this sandboxed function follows its contract. Therefore, we need to ensure that the returned value falls in the range that we expect.

Similarly, for a sandboxed function returning a pointer:

`extern const char* do_the_thing();`


We cannot guarantee that the returned pointer actually points to memory controlled by the sandbox. An adversary may have forced the returned pointer to point somewhere in the application outside of the sandbox. Therefore, we validate the pointer before using it.

There are additional runtime constraints that are not obvious from reading the source. For instance, the pointer returned above may point to dynamically allocated memory from the sandbox. In that case, the pointer should be freed by the sandbox, not by the host application. We could rely on developers to always remember which values are application values and which values are sandbox values. Experience has shown that approach is not feasible.

### Tainted data

The above two examples point to a general principle: data returned from the sandbox should be specifically identified as such. With this identification in hand, we can ensure the data is handled in appropriate ways.

We label data associated with the sandbox as “tainted”. Tainted data can be freely manipulated (e.g. pointer arithmetic, accessing fields) to produce more tainted data. But when we convert tainted data to non-tainted data, we want those operations to be as explicit as possible. Taintedness is valuable not just for managing memory returned from the sandbox. It’s also valuable for identifying data returned from the sandbox that may need additional verification, e.g. indices pointing into some external array.

We therefore model all exposed functions from the sandbox as returning tainted data. Such functions also take tainted data as arguments, because anything they manipulate must belong to the sandbox in some way. Once function calls have this interface, the compiler becomes a taintedness checker. Compiler errors will occur when tainted data is used in contexts that want untainted data, or vice versa. These contexts are precisely the places where tainted data needs to be propagated and/or data needs to be validated. [RLBox](http://rlbox.dev) handles all the details of tainted data and provides features that make incremental conversion of a library’s interface to a sandboxed interface straightforward.

### Next Steps

With the core infrastructure for wasm sandboxing in place, we can focus on increasing its impact across the Firefox codebase – both by bringing it to all of our supported platforms, and by applying it to more components. Since this technique is lightweight and easy to use, we expect to make rapid progress sandboxing more parts of Firefox in the coming months. We’re focusing our initial efforts on third-party libraries bundled with Firefox. Such libraries generally have well-defined entry points and don’t pervasively share memory with the rest of the system. In the future, however, we also plan to apply this technology to first-party code.

### Acknowledgements

We are deeply grateful for the work of our research partners at UCSD, UT Austin, and Stanford, who were the driving force behind this effort. We’d also like to extend a special thanks to our partners at the Bytecode Alliance – particularly the engineering team at Fastly, who developed Lucet and helped us extend its capabilities to make this project possible.

## About Nathan Froyd

Nathan Froyd is a software engineer working on Firefox. He writes code to help other people write code. In his free time he enjoys Olympic weightlifting and reading.

## 9 comments

MatthijsFebruary 25th, 2020 at 11:14Nathan FroydFebruary 25th, 2020 at 13:59anonFebruary 25th, 2020 at 16:18RajeeshFebruary 26th, 2020 at 01:04Nathan FroydFebruary 26th, 2020 at 10:48AnonymousFebruary 26th, 2020 at 10:41Nathan FroydFebruary 26th, 2020 at 10:47Clemens EissererFebruary 27th, 2020 at 03:13Nathan FroydFebruary 28th, 2020 at 10:03