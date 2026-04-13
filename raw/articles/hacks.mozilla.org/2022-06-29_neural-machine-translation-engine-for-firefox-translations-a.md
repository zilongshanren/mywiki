---
title: Neural Machine Translation Engine for Firefox Translations add-on – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2022/06/neural-machine-translation-engine-for-firefox-translations-add-on/
author: Posted; Featured Article; Firefox; Machine Translation
published: '2022-06-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Firefox Translations](https://addons.mozilla.org/en-US/firefox/addon/firefox-translations/) is a website translation add-on that provides an automated translation of web content. Unlike cloud-based alternatives, translation is done locally on the client-side in the user’s computer so that the text being translated does not leave your machine, making it entirely private. The add-on is available for installation on Firefox Nightly, Beta and in General Release.

The add-on utilizes proceedings of project [Bergamot](https://browser.mt/) which is a collaboration between Mozilla, the University of Edinburgh, Charles University in Prague, the University of Sheffield, and the University of Tartu with funding from the European Union’s Horizon 2020 research and innovation programme.

The add-on is powered internally by [Bergamot Translator](https://github.com/mozilla/bergamot-translator), a Neural Machine Translation engine that performs the actual task of translation. This engine can also be utilized in different contexts, [like in this demo website](https://mozilla.github.io/translate/), which lets the user perform free-form translations without using the cloud.

In this article, we will discuss the technical challenges around the development of the translation engine and how we solved them to build a usable Firefox Translations add-on.

## Challenges

The translation engine is built on top of [marian framework](https://marian-nmt.github.io/), which is a free Neural Machine Translation framework written in pure C++. The framework has a standalone native application that can provide simple translation functionality. However, two novel features needed to be introduced to the add-on that was not present in the existing native application.

The first was translation of forms, allowing users to input text in their own language and dynamically translate it on-the-fly into the page’s language. The second was estimating the quality of the translations so that low-confidence translations could be automatically highlighted in the page, in order to notify the user of potential errors. This led to the development of the translation engine which is a [high level C++ API layer on top of marian](https://github.com/mozilla/bergamot-translator).

The resulting translation engine is compiled directly to native code. There were three [potential architectural solutions](https://github.com/browsermt/marian-dev/issues/5) to integrating it into the add-on:

- Native integration to Firefox: Bundling the entire translation engine native code into Firefox.
[Native messaging](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging): Deploying the translation engine as a native application on the user’s computer and allowing the add-on to exchange messages with it.[Wasm](https://webassembly.org/): Porting the translation engine to Wasm and integrating it to the add-on using the developed JS bindings.

We evaluated these solutions on the following factors which we believed were crucial to develop a production ready translation add-on:

- Security: The approach of native integration inside the Firefox Web Browser was discarded following Mozilla’s internal security review of the engine code base, which highlighted issues over the number of third-party dependencies of the marian framework.
- Scalability and Maintainability: Native messaging would have posed challenges around distributing the code for the project because of the overhead of providing builds compatible with all platforms supported by Firefox. This would have been impractical to scale and maintain.
- Platform Support: The underlying marian framework of the translation engine supports translation only on x86/x86_64 architecture based processors. Given the increasing availability of ARM based consumer devices, the native messaging approach would have restricted the reach of the private and local translation technology to a wider audience.
- Performance: Wasm runs slower compared to the native code. However, it has potential to execute at near native speed by taking advantage of common hardware capabilities available on a wide range of platforms.

Wasm design as a portable compilation target for programming languages means developing and distributing a single binary running on all platforms. Additionally, Wasm is memory-safe and runs in a sandboxed execution environment, making it secure when parsing and processing Web content. All these advantages coupled with its potential to execute at near native speed gave us motivation to prototype this architectural solution and evaluate whether it meets the performance requirement of the translation add-on.

## Prototyping: Porting to Wasm

We chose the Emscripten toolchain for compiling the translation engine to Wasm. The engine didn’t compile to Wasm out of the box and we made [few changes](https://github.com/browsermt/marian-dev/pull/24) to successfully compile and perform translation using the generated Wasm binary, some of which are as follows:

- Disabled training specific native code of the marian framework as only translation specific code was required for the translation engine to work.
- Disabled multithreading code as any pthread compiled code to Wasm requires SharedArrayBuffer support in the browsers, which at the time of the development was going through the transition from
[disabled to being re-enabled](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer#security_requirements). - The engine depends on trained model(s), vocabulary along with an optional shortlist file to be able to perform the translation and expects its user to provide them from outside. As
[native code and normal JavaScript use different file-access paradigms](https://emscripten.org/docs/porting/files/file_systems_overview.html#emscripten-file-system-runtime-environment), we[packaged all the required files](https://emscripten.org/docs/porting/files/packaging_files.html)in Emscripten’s virtual file system for faster prototyping. - Replaced the
[proprietary library (Intel MKL) with an open source one (onnxjs)](https://github.com/browsermt/marian-dev/pull/24/commits/6b95d313ce6cf7c54dbc2ad711151b0fcab52ea3)for performing SGEMM operation in the attention layer of marian framework. - Fixed the issue related to the
[rogue usage of native data type size_t](https://github.com/browsermt/marian-dev/pull/24/commits/310cba7d2f92204a67c6929a032bd4a6f2830a98)in the marian framework, which was causing failures during translation.

## Prototyping to integration

### Problems

After having a working translation Wasm binary, we identified a few key problems that needed to be solved to convert the prototype to a usable product.

#### Scalability

Packaging of all the files for each supported language pair in the Wasm binary meant it was impractical to scale for new language pairs. All the files of each language pair (translating from one language to another and vice versa) in compressed form amount to ~40MB of disk space. As an example, supporting translation of 6 language pairs made the size of the binary ~250 MB.

#### Demand-based language support

The packaging of files for each supported language pair in the Wasm binary meant that the users will be forced to download all supported language pairs even if they intended to use only a few of them. This is highly inefficient compared to downloading files for language pairs based on the user’s demand.

#### Performance

We benchmarked the translation engine on three main metrics which we believed were critical from a usability perspective.

- Startup time: The time it takes for the engine to be ready for translation. The engine loads models, vocabularies, and optionally a shortlist file contents during this step.
- Translation speed: The time taken by the engine to translate a given text after its successful startup, measured in the number of words translated per second aka wps.
- Wasm binary size: The disk space of the generated Wasm binary.

The size of the generated Wasm binary, owing to the packaging, became dependent on the number of language pairs supported. The translation engine took an unusually long time (~8 seconds) to startup and was extremely slow in performing translation making it unusable.

As an example, translation from English to German language using [corresponding trained models](https://github.com/mozilla/firefox-translations-models/tree/main/models/prod/ende) gave only 95 wps on a MacBook Pro (15-inch, 2017), MacOS version 11.6.2, 3.1 GHz Quad-Core Intel Core i7 processor, 16 GB 2133 MHz RAM.

### Solution

#### Scalability, demand-based language support and binary size

As packaging of the files affected the usability of the translation engine on multiple fronts, we decided to solve that problem first. We introduced a new API in the translation engine to [pass required files as byte buffers](https://github.com/browsermt/bergamot-translator/issues/28) from outside instead of packing them during compile time in Emscripten’s virtual file system.

This allowed the translation engine to scale for new languages without increasing the size of the Wasm binary and enabled the add-on to dynamically download files of only those language pairs that the users were interested in. The final size of the Wasm binary (~6.5 MB) was well within the limits of the corresponding metric.

#### Startup time optimization

The new API that we developed to solve the packaging problem, coupled with [few other optimizations](https://github.com/browsermt/marian-dev/issues/19) in the marian framework, solved the long startup time problem. Engine’s startup time reduced substantially (~1 second) which was well within the acceptable limits of this performance criteria.

#### Translation speed optimization

Profiling the translation step in the browser indicated that the General matrix multiply (GEMM) instruction for 8-bit integer operands was the most computational intensive operation, and the [exception handling code](https://emscripten.org/docs/porting/exceptions.html#javascript-based-exception-support) had a high overhead on translation speed. We focused our efforts to optimize both of them.

- Optimizing exception handling code: We replaced
[try/catch with if/else based implementation](https://github.com/browsermt/marian-dev/pull/24/commits/f00909e7e3abc99cd00bf837b0af8fea23a0ebb3)in a function that was frequently called during the translation step which resulted in ~20% boost in translation speed. - Optimizing GEMM operation: Deeper investigation on profiling results revealed that the
[absence of GEMM instruction in Wasm standard](https://github.com/WebAssembly/relaxed-simd/issues/9)was the reason for it to perform so poorly on Wasm.[Experimental GEMM instructions](https://bugzilla.mozilla.org/show_bug.cgi?id=1672160): Purely for performance evaluation of GEMM instruction without getting it standardized in Wasm, we landed two experimental instructions in Firefox Nightly and Release for x86/x86_64 architecture. These instructions improved the[translation speed by ~310%](https://bugzilla.mozilla.org/show_bug.cgi?id=1746631#c1)and the translation of webpages seemed fast enough for the feature to be usable on these architectures. This feature was protected behind a flag and was exposed only to privileged extensions in Firefox Release owing to its experimental nature. We still wanted to figure out a standard based solution before this could be released as production software but it allowed us to continue developing the extension while we worked with the Firefox WASM team on a better long-term solution.[Non-standard long term solution](https://bugzilla.mozilla.org/show_bug.cgi?id=1762413): In the absence of a concrete timeline regarding the implementation of GEMM instruction in the Wasm standard, we replaced the experimental GEMM instructions with a Firefox specific non-standard long term solution which provided the[same or more translation speeds](https://github.com/mozilla/firefox-translations/pull/353#issue-1258348941)as provided by the experimental GEMM instructions. Apart from privileged extensions, this solution enabled translation functionallity for non-privileged extensions as well as regular content with same translation speeds and enabled translation on ARM64 based platforms, albeit with low speeds. None of this was possible with experimental GEMM instructions.[Native GEMM intrinsics](https://bugzilla.mozilla.org/show_bug.cgi?id=1746631): In an effort to improve translation speeds further, we landed a native GEMM implementation in Firefox Nightly protected behind a flag and exposed as intrinsics. The translation engine would directly call these intrinsics during the translation step whenever it is running in Firefox Nightly on x86/x86_64 architecture based systems. This work increased the translation speeds by[25% and 43%](https://bugzilla.mozilla.org/show_bug.cgi?id=1746631#c1)for SSSE3 and AVX2 simd extensions respectively compared to the experimental instructions that we had landed earlier.

[Emscripten toolchain upgrade](https://github.com/browsermt/bergamot-translator/pull/414): The most recent effort of updating the Emscripten toolchain to the latest version increased the translation speeds for all platforms by ~15% on Firefox and reduced the size of the Wasm binary further by ~25% (final size ~4.94 MB).

Eventually, we achieved the [translation speeds of ~870 wps](https://github.com/mozilla/firefox-translations/pull/353#issue-1258348941) for translation from English to German language using [corresponding trained models](https://github.com/mozilla/firefox-translations-models/tree/main/models/prod/ende) on Firefox Release on a MacBook Pro (15-inch, 2017), MacOS version 11.6.2, 3.1 GHz Quad-Core Intel Core i7 processor, 16 GB 2133 MHz RAM.

## Future

The translation engine is optimized to run at high translation speeds only for x86/x86_64 processors and we have ideas for improving the situation on ARM. A standardized Wasm GEMM instruction can achieve similar speeds on ARM, providing benefits to emerging class of consumer laptops and mobile devices. We also know that the native Marian engine performs even better with multithreading, but we had to disable multithreaded code in this version of the translation engine. Once SharedArrayBuffer support is broadly enabled, we believe we could re-enable multithreading and even faster translation speeds are possible.

## Acknowledgement

I would like to thank Bergamot consortium partners, Mozilla’s Wasm team and my teammates Andre Natal, Evgeny Pavlov for their contributions in developing a mature translation engine. I am thankful to Lonnen along with Mozilla’s Add-on team, Localization team, Q&A team and Mozilla community who supported us and contributed to the development of the Firefox Translations add-on.

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 825303.