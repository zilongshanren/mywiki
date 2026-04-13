---
title: asm.js Speedups Everywhere – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/03/asm-speedups-everywhere/
author: Alon Zakai
published: '2015-03-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[asm.js](http://asmjs.org/) is an easy-to-optimize subset of JavaScript. It runs in all browsers without plugins, and is a good target for porting C/C++ codebases such as game engines – which have in fact been the biggest adopters of this approach, for example [Unity 3D](http://blogs.unity3d.com/2014/04/29/on-the-future-of-web-publishing-in-unity/) and [Unreal Engine](https://www.unrealengine.com/blog/unreal-engine-47-released).

Obviously, developers porting games using asm.js would like them to run well across **all** browsers. However, each browser has different performance characteristics, because each has a different JavaScript engine, different graphics implementation, and so forth. In this post, we’ll focus on JavaScript execution speed and see the significant progress towards fast asm.js execution that has been happening across the board. Let’s go over each of the four major browsers now.

**Chrome
**

Already in 2013, Google [released Octane 2.0](http://blog.chromium.org/2013/11/announcing-octane-20.html), a new version of their primary JavaScript benchmark suite, which contained a new asm.js benchmark, zlib. Benchmarks define what browsers optimize: things that matter are included in benchmarks, and browsers then compete to achieve the best scores. Therefore, adding an asm.js benchmark to Octane clearly signaled Google’s belief that asm.js content is important to optimize for.

A further major development happened more recently, when Google [landed TurboFan](https://groups.google.com/forum/#!msg/v8-dev/ab8V5Z58_70/5-05DvysCt8J), a new work-in-progress optimizing compiler for Chrome’s JavaScript engine,

**v8**. TurboFan has a “sea of nodes” architecture (which is new in the JavaScript space, and has been used very successfully elsewhere, for example in the Java server virtual machine), and aims to reach even higher speeds than CrankShaft, the first optimizing compiler for v8.

While TurboFan is not yet ready to be enabled on all JavaScript content, [as of Chrome 41 it is enabled on asm.js](https://code.google.com/p/v8/issues/detail?id=2599#c77). Getting the benefits of TurboFan early on asm.js shows the importance of optimizing asm.js for the Chrome team. And the benefits can be quite substantial: For example, TurboFan speeds up [Emscripten](http://emscripten.org/)‘s zlib benchmark by **13%**, and fasta by **24%**.

**Safari
**

During the last year, Safari’s JavaScript Engine, **JavaScriptCore**, [introduced a new JIT (Just In Time compiler) called FTL](https://www.webkit.org/blog/3362/introducing-the-webkit-ftl-jit/). FTL stands for “

[Fourth Tier LLVM](http://blog.llvm.org/2014/07/ftl-webkits-llvm-based-jit.html),” as it adds a fourth level of optimization above the three previously-existing ones, and it is based on

[LLVM](http://llvm.org/), a powerful open source compiler framework. This is exciting because LLVM is a top-tier general-purpose compiler, with many years of optimizations put into it, and Safari gets to reuse all those efforts. As shown in the blogposts linked to earlier, the speedups that FTL provides can be very substantial.

Another interesting development from Apple this year was the introduction of a new JavaScript benchmark, ** JetStream**. JetStream contains several asm.js benchmarks, an indication that Apple believes asm.js content is important to optimize for, just as when Google added an asm.js benchmark to Octane.

**Internet Explorer**

The JavaScript engine inside Internet Explorer is named **Chakra**. Last year, the Chakra team [blogged]( http://blogs.msdn.com/b/ie/archive/2014/10/09/announcing-key-advances-to-javascript-performance-in-windows-10-technical-preview.aspx) about a suite of optimizations coming to IE in Windows 10 and [pointed]( http://blogs.msdn.com/b/ie/archive/2014/10/09/announcing-key-advances-to-javascript-performance-in-windows-10-technical-preview.aspx#10563952) to significant improvements in the scores on asm.js workloads in Octane and JetStream. This is yet another example of how having asm.js workloads in common benchmarks drives measurement and optimization.

The **big news**, however, is the recent [announcement by the Chakra team](http://blogs.msdn.com/b/ie/archive/2015/02/18/bringing-asm-js-to-the-chakra-javascript-engine-in-windows-10.aspx) that they are working on adding specific asm.js optimizations, to arrive in Windows 10 together with the other optimizations mentioned earlier. These optimizations haven’t made it to the Preview channel yet, so we can’t measure and report on them here. However, we can *speculate* on the improvements based on the initial impact of landing asm.js optimizations in Firefox. As shown in [this benchmark comparisons slide](http://kripken.github.io/mloc_emscripten_talk/#/28) containing measurements from right after the landing, asm.js optimizations immediately brought Firefox to around 2x slower than native performance (from 5-12x native before). Why should these wins translate to Chakra? Because, as explained in [our previous post](https://blog.mozilla.org/luke/2015/02/18/microsoft-announces-asm-js-optimizations), the asm.js spec provides a **predictable** way to **validate** asm.js code and generate high-quality code based on the results.

So, here’s looking forward to good asm.js performance in Windows 10!

**Firefox**

As we mentioned before, the [initial landing](https://blog.mozilla.org/luke/2013/03/21/asm-js-in-firefox-nightly) of asm.js optimizations in Firefox generally put Firefox [within 2x of native](http://kripken.github.io/mloc_emscripten_talk/#/28) in terms of raw throughput. By the end of 2013, we were able to report that the gap had shrunk to [around 1.5x native](https://hacks.mozilla.org/2013/12/gap-between-asm-js-and-native-performance-gets-even-narrower-with-float32-optimizations) – which is close to the amount of variability that different native compilers have between each other anyhow, so comparisons to “native speed” start to be less meaningful.

At a high-level, this progress comes from two kinds of improvements: compiler backend optimizations and new JavaScript features. In the area of compiler backend optimizations, there has been a stream of tiny wins (specific to particular code patterns or hardware) making it difficult to point to any one thing. Two significant improvements stand out, though:

*a new register allocation algorithm*, based on the[new register allocator in LLVM 3.0](http://blog.llvm.org/2011/09/greedy-register-allocation-in-llvm-30.html): while speedups vary, one notable example is an initial 20% improvement on x86 on the zlib portion of Google’s[Octane benchmark](https://developers.google.com/octane/benchmark)and another 4% after[refinement](https://bugzilla.mozilla.org/show_bug.cgi?id=826741); and: a[effective address](https://en.wikipedia.org/wiki/Addressing_mode)optimizations[recent addition](https://bugzilla.mozilla.org/show_bug.cgi?id=986981)in Firefox Nightly, producing 5% – 10% speedups across heap-access-heavy workloads.

Along with backend optimization work, two new JavaScript features have been incorporated into asm.js which unlock new performance capabilities in the hardware. The first feature, [Math.fround](http://people.mozilla.org/~jorendorff/es6-draft.html#sec-math.fround), may look simple but it enables the compiler backend to generate single-precision floating-point arithmetic when used carefully in JS. As described in [this post](https://blog.mozilla.org/javascript/2013/11/07/efficient-float32-arithmetic-in-javascript), the switch can result in anywhere from a 5% – 60% speedup, depending on the workload. The second feature is much bigger: [SIMD.js](https://hacks.mozilla.org/2014/10/introducing-simd-js). This is still a [stage 1 proposal for ES7](https://github.com/tc39/ecma262) so the new SIMD operations and the associated [asm.js extensions](http://discourse.specifiction.org/t/request-for-comments-simd-js-in-asm-js/676/14) are only available in [Firefox Nightly](http://nightly.mozilla.org). [Initial results](https://01.org/blogs/tlcounts/2014/bringing-simd-javascript) are promising though.

Separate from all these *throughput* optimizations, there have also been a set of **load time** optimizations in Firefox: off-main-thread and parallel compilation of asm.js code as well as caching of the compiled machine code. As described in [this post](https://blog.mozilla.org/luke/2014/01/14/asm-js-aot-compilation-and-startup-performance), these optimizations significantly improve the experience of starting a Unity- or Epic-sized asm.js application. Existing asm.js workloads in the benchmarks mentioned above do not test this aspect of asm.js performance so we put together a new benchmark suite named [Massive](http://kripken.github.io/Massive) that does. Looking at [Firefox’s Massive score over time](https://hacks.mozilla.org/wp-content/uploads/2014/09/massive-milestones1.png), we can see the load-time optimizations contributing to a more than 6x improvement (more details in the Hacks post introducing [the Massive benchmark](https://hacks.mozilla.org/2014/11/massive-the-asm-js-benchmark)).

**The Bottom Line**

What is most important, in the end, are not the underlying implementation details, nor even specific performance numbers on this benchmark or that. What really matters is that applications run well. The best way to check that is to actually run real-world games! A nice example of an asm.js-using game is [Dead Trigger 2](http://beta.unity3d.com/jonas/DT2/), a Unity 3D game:

The video shows the game running on Firefox, but as it uses only standard web APIs, it should work in any browser. We tried it now, and it renders quite smoothly on Firefox, Chrome and Safari. We are looking forward to testing it on the next Preview version of Internet Explorer as well.

Another example is [Cloud Raiders](https://www.facebook.com/cloudraidersgame):

As with Unity, the developers of Cloud Raiders were able to compile their existing C++ codebase (using [Emscripten](http://emscripten.org/)) to run on the web without relying on plugins. The result runs well in all four of the major browsers.

**In conclusion, asm.js performance has made great strides over the last year.** There is still room for improvement – sometimes performance is not perfect, or a particular API is missing, in one browser or another – but **all** major browsers are working to make sure that asm.js runs quickly. We can see that by looking at the benchmarks they are optimizing on, which contain asm.js, and in the new improvements they are implementing in their JavaScript engines, which are often motivated by asm.js. As a result, games that not long ago would have required plugins are quickly getting to the point where they can run well without them, in modern browsers across the web.

## About Alon Zakai

Alon is on the research team at Mozilla, where he works primarily on Emscripten, a compiler from C and C++ to JavaScript. Alon founded the Emscripten project in 2010.

## About Luke Wagner

Luke Wagner is a Mozilla software engineer and hacks on JavaScript and WebAssembly in Firefox.

## 10 comments

David FlanaganMarch 3rd, 2015 at 11:56Alon ZakaiMarch 3rd, 2015 at 12:04William FurrMarch 3rd, 2015 at 14:48Gerard BraadMarch 3rd, 2015 at 17:36David FlanaganMarch 4th, 2015 at 23:37Luke WagnerMarch 5th, 2015 at 02:33Eric MorgenMarch 5th, 2015 at 09:42Owen DensmoreMarch 6th, 2015 at 09:49Alon ZakaiMarch 6th, 2015 at 18:06Paul ToppingMarch 11th, 2015 at 16:16