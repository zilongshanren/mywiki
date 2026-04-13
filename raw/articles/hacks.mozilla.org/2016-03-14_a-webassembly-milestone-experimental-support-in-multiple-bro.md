---
title: 'A WebAssembly Milestone: Experimental Support in Multiple Browsers – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2016/03/a-webassembly-milestone/
author: Luke Wagner
published: '2016-03-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*WebAssembly* is an emerging standard whose goal is to define a safe, portable, size- and load-time efficient binary compiler target which offers near-native performance—a virtual CPU for the Web. WebAssembly is being developed in a [W3C Community Group](https://www.w3.org/community/webassembly/) (CG) whose [members](https://www.w3.org/community/webassembly/participants) include Mozilla, Microsoft, Google and Apple.

I’m excited to announce that WebAssembly has reached an important milestone: **there are now multiple, interoperable, experimental browser implementations**. We still have a lot of work left on the standard implementation before shipping, but this is a good occasion to present our progress so far, talk about what’s coming next, and invite feedback.

## Why WebAssembly?

The low-level [asm.js](http://asmjs.org) subset of JavaScript has demonstrated not only that it’s possible for browsers to achieve safe, sandboxed, near-native computational performance, but that there’s tremendous demand for this kind of capability on the Web. Thanks to the [Emscripten](http://emscripten.org) compiler, we’ve seen asm.js used for a diverse and growing array of applications, including mapping, cryptography, compression, games, CAD, image editing, and facial recognition.

The WebAssembly CG formed [last year](https://blog.mozilla.org/luke/2015/06/17/webassembly/) to take the Web the next step further, with a standardized binary format whose storage size and decoding times could be optimized beyond what is possible with JavaScript. Additionally, by being a new standard, WebAssembly is able to evolve to accommodate low-level features independently of the evolution of JavaScript.

At the same time, we knew it was important for WebAssembly to be “of the Web:” it had to access existing Web APIs and integrate tightly with JavaScript by, e.g., allowing calls between WebAssembly and JavaScript. Unlike classic plugin models, this will allow WebAssembly to be more easily integrated into JavaScript applications and libraries, just as asm.js has been able to do.

Finally, we’ve been able to draw on our years 1,2,3,4,5,6,7 of experience with Emscripten and asm.js to guide and focus the initial design of WebAssembly. And crucially,

[with the great performance of asm.js code](https://hacks.mozilla.org/2015/03/asm-speedups-everywhere/)on modern browsers, the creation of

[polyfills](https://remysharp.com/2010/10/08/what-is-a-polyfill)will allow developers to begin using WebAssembly even before native implementations have reached saturation in the browser market.

## Progress

Fast forward to today, and the CG has already made a remarkable amount of progress. Within the [WebAssembly GitHub organization](http://github.com/webassembly/), the group has produced:

- a
[description and rationale](https://github.com/webassembly/design)of the initial feature set and planned future features; - a
[specification and reference interpreter](https://github.com/WebAssembly/spec/tree/master/ml-proto); - 13,000 lines of tests used to validate both the spec interpreter and browsers;
- a first draft of the
[binary format](https://github.com/WebAssembly/design/blob/master/BinaryEncoding.md#module-structure).

What’s more, engineers on four browser engines have implemented prototype WebAssembly implementations 1,2,3,4. Within Firefox, we refactored our existing asm.js optimization pipeline to use WebAssembly’s binary format as the representation of asm.js code sent from the main parsing thread to the background compiler threads.

This change ended up significantly improving asm.js parallel compilation performance by moving two costly steps, MIR and code generation, off the sequential critical path. With this refactored pipeline, native WebAssembly decoding only requires the addition of a small new frontend to validate the untrusted bytes:

For definitions of these terms and more background on JS and asm.js compilation, see [this](https://blog.mozilla.org/luke/2014/01/14/asm-js-aot-compilation-and-startup-performance/#jit) previous blog post.

## Experimenting with WebAssembly

With all these pieces in place, it’s now possible to build WebAssembly demos that run on multiple experimental implementations. We do mean “experimental”: both the binary format and JS bindings for WebAssembly will likely change incompatibly over the next months until the first edition is stabilized. And we don’t expect implementations to be mature enough for stress tests or benchmarking for some time yet. Rather, the importance of this milestone is getting all the browsers on the same page so we can continue to iterate in sync.

With all that said, it’s gratifying for us to see a [real, working demo](http://webassembly.github.io/demo) that will run in multiple browsers:

This particular demo actually has some nostalgic value: AngryBots is a Unity tutorial project which was used as a smoke test while bringing up Unity’s WebGL export. Good memories! :)

To run the demo, download a [Nightly](https://nightly.mozilla.org/) build, open `about:config`

and set `javascript.options.wasm`

to `true`

.

## Path To Release

So what’s next? There’s more to do before we have a stable, shippable first edition. In the CG, some big remaining tasks are:

**Define the**[official WebAssembly text format](https://github.com/WebAssembly/design/blob/master/TextFormat.md#official-text-format).**Further reduce binary format size.**While the current binary format is 42% smaller than asm.js uncompressed (12% smaller after gzip), we know from[previous prototype binary format work](https://github.com/WebAssembly/design/blob/master/FAQ.md#can-the-polyfill-really-be-efficient)that further significant size reductions are available.**Iterate on the WebAssembly JavaScript API.**Currently the experimental builds define a single new synchronous function,`Wasm.instantiateModule`

, that does both compilation and instantiation. There are tentative plans to break these steps apart and provide both synchronous and asynchronous functions that produce a[structured-cloneable](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm)code object. This gives developers more control over both compilation and machine-code caching than current[implicit machine-code caching for asm.js](https://blog.mozilla.org/luke/2014/01/14/asm-js-aot-compilation-and-startup-performance#caching)in Firefox.**Create more approachable documentation for compiler writers, tool authors, hackers, and students.****Add a bunch more tests to the test suite.**

In Firefox we’re also planning to:

**Add WebAssembly support to browser devtools, including both the debugger and profiler**. Fortunately, the JavaScript, Developer Tools and Firebug teams worked together to move tools over to a new, abstract, unit-testable[Debugger API](https://developer.mozilla.org/en-US/docs/Tools/Debugger-API)which we’ll be implementing for WebAssembly code. In fact, work has already[begun](https://bugzilla.mozilla.org/show_bug.cgi?id=1254893)which is why, if you open the Debugger tab for the above demo, you can already see a placeholder text format being generated for the binary code (which will, of course, switch over to the official text format when it’s ready).**Further reduce cold load time.**Measuring AngryBots compile time on a 16×2.4Ghz core Linux desktop, WebAssembly reduces compile time by about 52%. That’s a good start and leverages the fact that WebAssembly decoding is currently about 10× faster than asm.js parsing, but cold load time can be significantly further reduced by working on the other parts of the compilation pipeline.**Finish adding the full set of WebAssembly operators and import the test suite.**

## Full Speed Ahead

The progress on WebAssembly so far has been exhilarating. I continue to be impressed and appreciative of the collaborative atmosphere of the whole WebAssembly Community Group. If you want to learn more, the [GitHub org page](http://webassembly.github.io/) is a good starting point. Happy hacking!

## About Luke Wagner

Luke Wagner is a Mozilla software engineer and hacks on JavaScript and WebAssembly in Firefox.

## 14 comments

jiyinyiyongMarch 15th, 2016 at 08:09Luke WagnerMarch 15th, 2016 at 10:38niutechMarch 16th, 2016 at 19:47ITfindMarch 15th, 2016 at 11:11BrianMBMarch 15th, 2016 at 12:15Luke WagnerMarch 15th, 2016 at 16:12BrianMBMarch 15th, 2016 at 23:51rickMarch 16th, 2016 at 07:53EdgeMarch 17th, 2016 at 02:59niutechApril 6th, 2016 at 08:04IPv6March 16th, 2016 at 08:23andkaiMarch 23rd, 2016 at 04:21sboMarch 29th, 2016 at 01:28Dave BoyleApril 9th, 2016 at 12:55