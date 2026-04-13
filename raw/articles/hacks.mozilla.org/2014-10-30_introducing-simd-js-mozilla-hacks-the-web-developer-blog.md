---
title: Introducing SIMD.js – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/10/introducing-simd-js/
author: Dan Gohman
published: '2014-10-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

SIMD stands for [Single Instruction Multiple Data](http://en.wikipedia.org/wiki/SIMD), and is the name for performing operations on multiple data elements together. For example, a SIMD add instruction can add multiple values, in parallel. SIMD is a very popular technique for accelerating computations in graphics, audio, codecs, physics simulation, cryptography, and many other domains.

In addition to delivering performance, SIMD also reduces power usage, as it uses fewer instructions to do the same amount of work.

## SIMD.js

SIMD.js is a new API being developed by Intel, Google, and Mozilla for JavaScript which introduces several new types and functions for doing SIMD computations. For example, the Float32x4 type represents 4 [float32](http://en.wikipedia.org/wiki/Single-precision_floating-point_format) values packed up together. The API contains functions to operate on those values together, including all the basic arithmetic operations, and operations to rearrange, load, and store such values. The intent is for browsers to implement this API directly, and provide optimized implementations that make use of SIMD instructions in the underlying hardware.

The focus is currently on supporting both x86 platforms with SSE and ARM platforms with NEON. We’re also interested in the possibility of supporting other platforms, potentially including [MIPS](http://www.imgtec.com/mips/architectures/simd.asp), [Power](https://www.power.org/documentation/power-isa-version-2-07/), and others.

SIMD.js is originally derived from the Dart SIMD specification, and it is rapidly evolving to become a more general API, and to cover additional use cases such as those that require narrower integer types, including Int8x16 and Int16x8, and saturating operations.

SIMD.js is a fairly low-level API, and it is expected that libraries will be written on top of it to expose higher-level functionality such as matrix operations, transcendental functions, and more.

In addition to being usable in regular JS, there is also work is underway to add SIMD.js to asm.js too, so that it can be used from asm.js programs such those produced by Emscripten. In Emscripten, SIMD can be achieved through the built-in autovectorization, [the generic SIMD extensions](http://clang.llvm.org/docs/LanguageExtensions.html#vectors-and-extended-vectors), or [the new (and still growing) Emscripten-specific API](https://github.com/kripken/emscripten/blob/master/system/include/emscripten/vector.h). Emscripten will also be implementing subsets of popular headers such as <xmmintrin.h> with wrappers around the SIMD.js APIs, as additional ways to ease porting SIMD code in some situations.

## SIMD.js Today

The SIMD.js API itself is in active development. The [ecmascript_simd github repository](https://github.com/johnmccutchan/ecmascript_simd) is currently serving as a provision specification as well as providing a polyfill implementation to provide the functionality, though of course not the accelerated performance, of the SIMD API on existing browsers. It also includes some [benchmarks](https://github.com/johnmccutchan/ecmascript_simd/tree/master/src/benchmarks) which also serve as examples of basic SIMD.js usage.

To see SIMD.js in action, check out [the demo page accompanying the IDF2014 talk on SIMD.js](http://peterjensen.github.io/idf2014-simd/idf2014-simd).

The API has been presented to TC-39, which has approved it for stage 1 (Proposal). Work is proceeding in preparation for subsequent stages, which will involve proposing something closer to a finalized API.

SIMD.js implementation in Firefox Nightly is in active development. Internet Explorer has listed SIMD.js as [“under consideration”](https://status.modern.ie/simdes7?term=SIMD). There is also [a prototype implementation in a branch of Chromium](https://drive.google.com/folderview?id=0B9RVWZYRtYFeU1pHUWZIeVNtN0k&usp=sharing).

## Short SIMD and Long SIMD

One of the uses of SIMD is to accelerate processing of large arrays of data. If you have an array of N elements, and you want to do roughly the same thing to every element in the array, you can divide N by whatever SIMD size the platform makes available and run that many instances of your SIMD subroutine. Since N can can be very large, I call these kind of problems long SIMD problems.

Another use of SIMD is to accelerate processing of clusters of data. RGB or RGBA pixels, XYZW coordinates, or 4×4 matrices are all examples of such clusters, and I call problems which are expressed in these kinds of types short SIMD problems.

SIMD is a broad domain, and the boundary between short and long SIMD isn’t always clear, but at a high level, the two styles are quite different. Even the terminology used to describe them features a split: In the short SIMD world, the operation which copies a scalar value into every element of a vector value is called a “splat”, while in the long vector world the analogous operation is called a “broadcast”.

SIMD.js is primarily a “short” style API, and is well suited for short SIMD problems. SIMD.js can also be used for long SIMD problems, and it will still deliver significant speedups over plain scalar code. However, its fixed-length types aren’t going to achieve maximum performance of some of today’s CPUs, so there is still room for another solution to be developed to take advantage of that available performance.

## Portability and Performance

There is a natural tension in many parts of SIMD.js between the desire to have an API which runs consistently across all important platforms, and the desire to have the API run as fast as possible on each individual platform.

Fortunately, there is a core set of operations which are very consistent across a wide variety of platforms. These operations include most of the basic arithmetic operations and form the core of SIMD.js. In this set, little to no overhead is incurred because many of the corresponding SIMD API instructions map directly to individual instructions.

But, there also are many operations that perform well on one platform, and poorly on others. These can lead to surprising performance cliffs. The current approach of the SIMD.js API is to focus on the things that can be done well with as few performance cliffs as possible. It is also focused on providing portable behavior. In combination, the aim is to ensure that a program which runs well on one platform will likely run and run well on another.

In future iterations of SIMD.js, we expect to expand the scope and include more capabilities as well as mechanisms for querying capabilities of the underlying platform. Similar to WebGL, this will allow programs to determine what capabilities are available to them so they can decide whether to fall back to more conservative code, or disable optional functionality.

## The overall vision

SIMD.js will accelerate a wide range of demanding applications today, including games, video and audio manipulation, scientific simulations, and more, on the web. Applications will be able to use the SIMD.js API directly, libraries will be able to use SIMD.js to expose higher-level interfaces that applications can use, and Emscripten will compile C++ with popular SIMD idioms onto optimized SIMD.js code.

Looking forward, SIMD.js will continue to grow, to provide broader functionality. We hope to eventually accompany SIMD.js with a long-SIMD-style API as well, in which the two APIs can cooperate in a manner very similar to the way that OpenCL combines explicit vector types with the implicit long-vector parallelism of the underlying programming model.

## About
[
Dan Gohman ](http://sunfishcode.github.io/blog/)

I've worked at Cray, Apple, and Google on several different compilers in a variety of contexts. I'm currently a member of the Mozilla Research team primarily working on asm.js, SIMD.js, and Emscripten.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 10 comments

Peter JensenOctober 30th, 2014 at 09:37Peter JensenOctober 30th, 2014 at 10:08AlejandroGOctober 30th, 2014 at 12:12Rick WaldronOctober 31st, 2014 at 10:57Zac BowlingOctober 30th, 2014 at 15:48LukeOctober 30th, 2014 at 20:04Ningxin HuOctober 30th, 2014 at 17:43Jonathan Ragan-KelleyOctober 30th, 2014 at 17:57Dan GohmanOctober 30th, 2014 at 19:56TomNovember 4th, 2014 at 10:29