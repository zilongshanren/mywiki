---
title: Creating and working with WebAssembly modules – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/02/creating-and-working-with-webassembly-modules/
author: Lin Clark
published: '2017-02-28'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is the fourth part in a series on WebAssembly and what makes it fast. If you haven’t read the others, we recommend starting from the beginning.*

[WebAssembly](https://research.mozilla.org/webassembly/) is a way to run programming languages other than JavaScript on web pages. In the past when you wanted to run code in the browser to interact with the different parts of the web page, your only option was JavaScript.

So when people talk about WebAssembly being fast, the apples to apples comparison is to JavaScript. But that doesn’t mean that it’s an either/or situation—that you are either using WebAssembly, or you’re using JavaScript.

In fact, we expect that developers are going to use both WebAssembly and JavaScript in the same application. Even if you don’t write WebAssembly yourself, you can take advantage of it.

WebAssembly modules define functions that can be used from JavaScript. So just like you download a module like lodash from npm today and call functions that are part of its API, you will be able to download WebAssembly modules in the future.

So let’s see how we can create WebAssembly modules, and then how we can use them from JavaScript.

## Where does WebAssembly fit?

In the article about [assembly](https://hacks.mozilla.org/2017/02/a-crash-course-in-assembly/), I talked about how compilers take high-level programming languages and translate them to machine code.

Where does WebAssembly fit into this picture?

You might think it is just another one of the target assembly languages. That is kind of true, except that each one of those languages (x86, ARM ) corresponds to a particular machine architecture.

When you’re delivering code to be executed on the user’s machine across the web, you don’t know what your target architecture the code will be running on.

So WebAssembly is a little bit different than other kinds of assembly. It’s a machine language for a conceptual machine, not an actual, physical machine.

Because of this, WebAssembly instructions are sometimes called virtual instructions. They have a much more direct mapping to machine code than JavaScript source code. They represent a sort of intersection of what can be done efficiently across common popular hardware. But they aren’t direct mappings to the particular machine code of one specific hardware.

The browser downloads the WebAssembly. Then, it can make the short hop from WebAssembly to that target machine’s assembly code.

## Compiling to .wasm

The compiler tool chain that currently has the most support for WebAssembly is called LLVM. There are a number of different front-ends and back-ends that can be plugged into LLVM.


Note: Most WebAssembly module developers will code in languages like C and Rust and then compile to WebAssembly, but there are other ways to create a WebAssembly module. For example, there is an experimental tool that helps you[build a WebAssembly module using TypeScript], or you can[code in the text representation of WebAssembly directly].


Let’s say that we wanted to go from C to WebAssembly. We could use the clang front-end to go from C to the LLVM intermediate representation. Once it’s in LLVM’s IR, LLVM understands it, so LLVM can perform some optimizations.

To go from LLVM’s IR ([intermediate representation](https://en.wikipedia.org/wiki/Intermediate_representation)) to WebAssembly, we need a back-end. There is one that’s currently in progress in the LLVM project. That back-end is most of the way there and should be finalized soon. However, it can be tricky to get it working today.

There’s another tool called Emscripten which is a bit easier to use at the moment. It has its own back-end that can produce WebAssembly by compiling to another target (called asm.js) and then converting that to WebAssembly. It uses LLVM under the hood, though, so you can switch between the two back-ends from Emscripten.

Emscripten includes many additional tools and libraries to allow porting whole C/C++ codebases, so it’s more of a software developer kit (SDK) than a compiler. For example, systems developers are used to having a filesystem that they can read from and write to, so Emscripten can simulate a file system using IndexedDB.

Regardless of the toolchain you’ve used, the end result is a file that ends in .wasm. I’ll explain more about the structure of the .wasm file below. First, let’s look at how you can use it in JS.

## Loading a .wasm module in JavaScript

The .wasm file is the WebAssembly module, and it can be loaded in JavaScript. As of this moment, the loading process is a little bit complicated.

```
function fetchAndInstantiate(url, importObject) {
return fetch(url).then(response =>
response.arrayBuffer()
).then(bytes =>
WebAssembly.instantiate(bytes, importObject)
).then(results =>
results.instance
);
}
```


You can see this in more depth in [our docs](https://developer.mozilla.org/en-US/docs/WebAssembly).

We’re working on making this process easier. We expect to make improvements to the toolchain and integrate with existing module bundlers like webpack or loaders like SystemJS. We believe that loading WebAssembly modules can be as easy as as loading JavaScript ones.

There is a major difference between WebAssembly modules and JS modules, though. Currently, functions in WebAssembly can only use numbers (integers or floating point numbers) as parameters or return values.

For any data types that are more complex, like strings, you have to use the WebAssembly module’s memory.

If you’ve mostly worked with JavaScript, having direct access to memory isn’t so familiar. More performant languages like C, C++, and Rust, tend to have manual memory management. The WebAssembly module’s memory simulates the heap that you would find in those languages.

To do this, it uses something in JavaScript called an ArrayBuffer. The array buffer is an array of bytes. So the indexes of the array serve as memory addresses.

If you want to pass a string between the JavaScript and the WebAssembly, you convert the characters to their character code equivalent. Then you write that into the memory array. Since indexes are integers, an index can be passed in to the WebAssembly function. Thus, the index of the first character of the string can be used as a pointer.

It’s likely that anybody who’s developing a WebAssembly module to be used by web developers is going to create a wrapper around that module. That way, you as a consumer of the module don’t need to know about memory management.

If you want to learn more, check out our docs on [working with WebAssembly’s memory](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_objects/WebAssembly/Memory).

## The structure of a .wasm file

If you are writing code in a higher level language and then compiling it to WebAssembly, you don’t need to know how the WebAssembly module is structured. But it can help to understand the basics.

If you haven’t already, we suggest reading the [article on assembly](https://hacks.mozilla.org/2017/02/a-crash-course-in-assembly/) (part 3 of the series).

Here’s a C function that we’ll turn into WebAssembly:

```
int add42(int num) {
return num + 42;
}
```


You can try using the [WASM Explorer](http://mbebenita.github.io/WasmExplorer/) to compile this function.

If you open up the .wasm file (and if your editor supports displaying it), you’ll see something like this.

```
00 61 73 6D 0D 00 00 00 01 86 80 80 80 00 01 60
01 7F 01 7F 03 82 80 80 80 00 01 00 04 84 80 80
80 00 01 70 00 00 05 83 80 80 80 00 01 00 01 06
81 80 80 80 00 00 07 96 80 80 80 00 02 06 6D 65
6D 6F 72 79 02 00 09 5F 5A 35 61 64 64 34 32 69
00 00 0A 8D 80 80 80 00 01 87 80 80 80 00 00 20
00 41 2A 6A 0B
```


That is the module in its “binary” representation. I put quotes around binary because it’s usually displayed in hexadecimal notation, but that can be easily converted to binary notation, or to a human readable format.

For example, here’s what `num + 42`

looks like.

### How the code works: a stack machine

In case you’re wondering, here’s what those instructions would do.

You might have noticed that the `add`

operation didn’t say where its values should come from. This is because WebAssembly is an example of something called a stack machine. This means that all of the values an operation needs are queued up on the stack before the operation is performed.

Operations like `add`

know how many values they need. Since `add`

needs two, it will take two values from the top of the stack. This means that the `add`

instruction can be short (a single byte), because the instruction doesn’t need to specify source or destination registers. This reduces the size of the .wasm file, which means it takes less time to download.

Even though WebAssembly is specified in terms of a stack machine, that’s not how it works on the physical machine. When the browser translates WebAssembly to the machine code for the machine the browser is running on, it will use registers. Since the WebAssembly code doesn’t specify registers, it gives the browser more flexibility to use the best register allocation for that machine.

### Sections of the module

Besides the `add42`

function itself, there are other parts in the .wasm file. These are called sections. Some of the sections are required for any module, and some are optional.

Required:

**Type**. Contains the function signatures for functions defined in this module and any imported functions.**Function**. Gives an index to each function defined in this module.**Code**. The actual function bodies for each function in this module.

Optional:

**Export**. Makes functions, memories, tables, and globals available to other WebAssembly modules and JavaScript. This allows separately-compiled modules to be dynamically linked together. This is WebAssembly’s version of a .dll.**Import**. Specifies functions, memories, tables, and globals to import from other WebAssembly modules or JavaScript.**Start**. A function that will automatically run when the WebAssembly module is loaded (basically like a main function).**Global**. Declares global variables for the module.**Memory**. Defines the memory this module will use.**Table**. Makes it possible to map to values outside of the WebAssembly module, such as JavaScript objects. This is especially useful for allowing indirect function calls.**Data**. Initializes imported or local memory.**Element**. Initializes an imported or local table.

For more on sections, here’s a great in-depth [explanation of how these sections work](https://rsms.me/wasm-intro).

## Coming up next

Now that you know how to work with WebAssembly modules, let’s look at [why WebAssembly is fast](https://hacks.mozilla.org/2017/02/what-makes-webassembly-fast/).

## About
[
Lin Clark ](https://twitter.com/linclark)

Lin works in Advanced Development at Mozilla, with a focus on Rust and WebAssembly.

## 4 comments

Nitin PasumarthyMarch 4th, 2017 at 14:25Lin ClarkMarch 4th, 2017 at 15:16Jochen WiedmannMarch 8th, 2017 at 03:01Christian WenzMarch 23rd, 2017 at 03:06