---
title: 'The Baseline Interpreter: a faster JS interpreter in Firefox 70 – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2019/08/the-baseline-interpreter-a-faster-js-interpreter-in-firefox-70/
author: Jan de Mooij
published: '2019-08-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Introduction

Modern web applications load and execute a lot more JavaScript code than they did just a few years ago. While [JIT (just-in-time) compilers](https://hacks.mozilla.org/2017/02/a-crash-course-in-just-in-time-jit-compilers/) have been very successful in making JavaScript performant, we needed a better solution to deal with these new workloads.

To address this, we’ve added a new, generated JavaScript bytecode interpreter to the JavaScript engine in Firefox 70. The interpreter is available now in the Firefox Nightly channel, and will go to general release in October. Instead of writing or generating a new interpreter from scratch, we found a way to do this by sharing most code with our existing Baseline JIT.

The new Baseline Interpreter has resulted in performance improvements, memory usage reductions and code simplifications. Here’s how we got there:

## Execution tiers

In modern JavaScript engines, each function is initially executed in a [bytecode interpreter](https://en.wikipedia.org/wiki/Bytecode). Functions that are called a lot (or perform many loop iterations) are compiled to native machine code. (This is called [JIT compilation](https://hacks.mozilla.org/2017/02/a-crash-course-in-just-in-time-jit-compilers/).)

Firefox has an interpreter written in C++ and multiple JIT tiers:

- The
**Baseline JIT**. Each bytecode instruction is compiled directly to a small piece of machine code. It uses[Inline Caches (ICs)](https://en.wikipedia.org/wiki/Inline_caching)both as performance optimization and to collect type information for Ion. **IonMonkey**(or just Ion), the optimizing JIT. It uses advanced compiler optimizations to generate fast code for hot functions (at the expense of slower compile times).

Ion JIT code for a function can be ‘deoptimized’ and thrown away for various reasons, for example when the function is called with a new argument type. This is called a *bailout*. When a bailout happens, execution continues in the Baseline code until the next Ion compilation.

Until Firefox 70, the execution pipeline for a very hot function looked like this:

## Problems

Although this works pretty well, we ran into the following problems with the first part of the pipeline (C++ Interpreter and Baseline JIT):

- Baseline JIT compilation is fast, but modern web applications like Google Docs or Gmail execute so much JavaScript code that we could spend quite some time in the Baseline compiler, compiling thousands of functions.
- Because the C++ interpreter is so slow and doesn’t collect type information, delaying Baseline compilation or moving it off-thread would have been a performance risk.
- As you can see in the diagram above, optimized Ion JIT code was only able to bail out to the Baseline JIT. To make this work, Baseline JIT code required extra metadata (the machine code offset corresponding to each bytecode instruction).
- The Baseline JIT had some complicated code for bailouts, debugger support, and exception handling. This was especially true where these features intersect!

## Solution: generate a faster interpreter

We needed type information from the Baseline JIT to enable the more optimized tiers, and we wanted to use JIT compilation for runtime speed. However, the modern web has such large codebases that even the relatively fast Baseline JIT Compiler spent a lot of time compiling. To address this, Firefox 70 adds a new tier called the Baseline Interpreter to the pipeline:

The Baseline Interpreter sits between the C++ interpreter and the Baseline JIT and has elements from both. It executes all bytecode instructions with a fixed interpreter loop (like the C++ interpreter). In addition, it uses Inline Caches to improve performance and collect type information (like the Baseline JIT).

Generating an interpreter isn’t a new idea. However, we found a nice new way to do it by reusing most of the Baseline JIT Compiler code. The Baseline JIT is a template JIT, meaning each bytecode instruction is compiled to a mostly fixed sequence of machine instructions. We generate those sequences into an interpreter loop instead.

## Sharing Inline Caches and profiling data

As mentioned above, the Baseline JIT uses Inline Caches (ICs) both to make it fast and to help Ion compilation. To get type information, the Ion JIT compiler can inspect the Baseline ICs.

Because we wanted the Baseline Interpreter to use exactly the same Inline Caches and type information as the Baseline JIT, we added a new data structure called [JitScript](https://searchfox.org/mozilla-central/rev/325c1a707819602feff736f129cb36055ba6d94f/js/src/jit/JitScript.h#54-113). JitScript contains all type information and IC data structures used by both the Baseline Interpreter and JIT.

The diagram below shows what this looks like in memory. Each arrow is a pointer in C++. Initially, the function just has a JSScript with the bytecode that can be interpreted by the C++ interpreter. After a few calls/iterations we create the JitScript, attach it to the JSScript and can now run the script in the Baseline Interpreter.

As the code gets warmer we may also create the BaselineScript (Baseline JIT code) and then the IonScript (Ion JIT code).


Note that the Baseline JIT data for a function is now just the machine code. We’ve moved all the inline caches and profiling data into JitScript.

## Sharing the frame layout

The Baseline Interpreter uses the same frame layout as the Baseline JIT, but we’ve added some [interpreter-specific fields](https://searchfox.org/mozilla-central/rev/325c1a707819602feff736f129cb36055ba6d94f/js/src/jit/BaselineFrame.h#55-58) to the frame. For example, the bytecode PC (program counter), a pointer to the bytecode instruction we are currently executing, is not updated explicitly in Baseline JIT code. It can be determined from the return address if needed, but the Baseline Interpreter has to store it in the frame.

Sharing the frame layout like this has a lot of advantages. We’ve made almost no changes to C++ and IC code to support Baseline Interpreter frames—they’re just like Baseline JIT frames. Furthermore, When the script is warm enough for Baseline JIT compilation, switching from Baseline Interpreter code to Baseline JIT code is a matter of [jumping from](https://searchfox.org/mozilla-central/rev/8ea946dcf51f0d6400362cc1d49c8d4808eeacf1/js/src/jit/BaselineCodeGen.cpp#1385-1392) the interpreter code [into JIT code](https://searchfox.org/mozilla-central/rev/8ea946dcf51f0d6400362cc1d49c8d4808eeacf1/js/src/jit/BaselineCodeGen.cpp#1262-1275).

## Sharing code generation

Because the Baseline Interpreter and JIT are so similar, a lot of the code generation code can be shared too. To do this, we added a templated [ BaselineCodeGen base class](https://searchfox.org/mozilla-central/rev/8ea946dcf51f0d6400362cc1d49c8d4808eeacf1/js/src/jit/BaselineCodeGen.h#264-269) with two derived classes:

: used by the Baseline JIT to compile a script’s bytecode to machine code.`BaselineCompiler`

: used to generate the Baseline Interpreter code.`BaselineInterpreterGenerator`


The base class has a Handler C++ template argument that can be used to specialize behavior for either the Baseline Interpreter or JIT. A lot of Baseline JIT code can be shared this way. For example, the implementation of the `JSOP_GETPROP`

bytecode instruction (for a property access like `obj.foo`

in JavaScript code) [is shared code](https://searchfox.org/mozilla-central/rev/8ea946dcf51f0d6400362cc1d49c8d4808eeacf1/js/src/jit/BaselineCodeGen.cpp#3446-3459). It calls the `emitNextIC`

helper method that’s [specialized](https://searchfox.org/mozilla-central/rev/8ea946dcf51f0d6400362cc1d49c8d4808eeacf1/js/src/jit/BaselineCodeGen.cpp#531-588) for either Interpreter or JIT mode.

## Generating the Interpreter

With all these pieces in place, we were able to implement the `BaselineInterpreterGenerator`

class to generate the Baseline Interpreter! It generates a threaded interpreter loop: The code for each bytecode instruction is [followed by](https://searchfox.org/mozilla-central/rev/8ea946dcf51f0d6400362cc1d49c8d4808eeacf1/js/src/jit/BaselineCodeGen.cpp#6920-6922) an indirect jump to the next bytecode instruction.

For example, on x64 we currently generate the following machine code to interpret [ JSOP_ZERO](https://searchfox.org/mozilla-central/rev/8ea946dcf51f0d6400362cc1d49c8d4808eeacf1/js/src/jit/BaselineCodeGen.cpp#2402-2406) (bytecode instruction to push a zero value on the stack):

```
// Push Int32Value(0).
movabsq $-0x7800000000000, %r11
pushq %r11
// Increment bytecode pc register.
addq $0x1, %r14
// Patchable NOP for debugger support.
nopl (%rax,%rax)
// Load the next opcode.
movzbl (%r14), %ecx
// Jump to interpreter code for the next instruction.
leaq 0x432e(%rip), %rbx
jmpq *(%rbx,%rcx,8)
```


When we enabled the Baseline Interpreter in Firefox Nightly (version 70) back in July, we increased the Baseline JIT warm-up threshold from 10 to 100. The warm-up count is determined by counting the number of calls to the function + the number of loop iterations so far. The Baseline Interpreter has a threshold of 10, same as the old Baseline JIT threshold. This means that the Baseline JIT has a lot less code to compile.

## Results

### Performance and memory usage

After this landed in Firefox Nightly our performance testing infrastructure detected several improvements:

- Various 2-8%
[page load improvements](https://treeherder.mozilla.org/perf.html#/alerts?id=21879). A lot happens during page load in addition to JS execution (parsing, style, layout, graphics). Improvements like this are quite significant. - Many devtools performance tests
[improved by 2-10%](https://treeherder.mozilla.org/perf.html#/alerts?id=21880). - Some small memory usage wins.

Note that we’ve landed more performance improvements since this first landed.

To measure how the Baseline Interpreter’s performance compares to the C++ Interpreter and the Baseline JIT, I ran Speedometer and Google Docs on Windows 10 64-bit on Mozilla’s Try server and enabled the tiers one by one. (The following numbers reflect the best of 7 runs.):


On Google Docs we see that the Baseline Interpreter is much faster than just the C++ Interpreter. Enabling the Baseline JIT too makes the page load only a little bit faster.

On the Speedometer benchmark we get noticeably better results when we enable the Baseline JIT tier. The Baseline Interpreter does again much better than just the C++ Interpreter:


We think these numbers are great: the Baseline Interpreter is much faster than the C++ Interpreter and its start-up time (JitScript allocation) is much faster than Baseline JIT compilation (at least 10 times faster).

### Simplifications

After this all landed and stuck, we were able to simplify the Baseline JIT and Ion code by taking advantage of the Baseline Interpreter.

For example, deoptimization bailouts from Ion now resume in the Baseline Interpreter instead of in the Baseline JIT. The interpreter can re-enter Baseline JIT code at the next loop iteration in the JS code. Resuming in the interpreter is much easier than resuming in the middle of Baseline JIT code. We now have to record less metadata for Baseline JIT code, so Baseline JIT compilation got faster too. Similarly, we were able to [remove a lot of complicated code](https://hg.mozilla.org/mozilla-central/rev/49a2da59aa3e#l3.535) for debugger support and exception handling.

## What’s next?

With the Baseline Interpreter in place, it should now be possible to move Baseline JIT compilation off-thread. We will be working on that in the coming months, and we anticipate more performance improvements in this area.

## Acknowledgements

Although I did most of the Baseline Interpreter work, many others contributed to this project. In particular Ted Campbell and Kannan Vijayan reviewed most of the code changes and had great design feedback.

Also thanks to Steven DeTar, Chris Fallin, Havi Hoffman, Yulia Startsev, and Luke Wagner for their feedback on this blog post.

## About Jan de Mooij

Jan is a software engineer at Mozilla where he works on SpiderMonkey, the JavaScript Engine in Firefox. He lives in the Netherlands.

## 14 comments

KellyAugust 30th, 2019 at 11:34Jan de MooijAugust 30th, 2019 at 23:31bobAugust 30th, 2019 at 13:51Yan LuoAugust 30th, 2019 at 20:48Jan de MooijAugust 30th, 2019 at 23:58JaenAugust 31st, 2019 at 00:13Yan LuoAugust 31st, 2019 at 15:32Yan LuoAugust 31st, 2019 at 15:33DRSAgileSeptember 3rd, 2019 at 23:00Jan de MooijSeptember 3rd, 2019 at 23:39Aaron WSeptember 6th, 2019 at 16:20HoracioSeptember 8th, 2019 at 05:27Spudd86September 23rd, 2019 at 11:34Jan de MooijSeptember 24th, 2019 at 03:01