---
title: Autogenerating Rust-JS bindings with UniFFI – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2023/08/autogenerating-rust-js-bindings-with-uniffi/
author: Ben Dean-Kawamura
published: '2023-08-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/2ee9d4a4bcc9772e.png)


I work on the Firefox sync team at Mozilla. Four years ago, we wrote a [blog post describing our strategy to ship cross-platform Rust components](https://hacks.mozilla.org/2019/04/crossing-the-rust-ffi-frontier-with-protocol-buffers/) for syncing and storage on all our platforms. The vision was to consolidate the separate implementations of features like history, logins, and syncing that existed on Firefox Desktop, Android, and iOS.

We would replace those implementations with a core written in Rust and a set of hand-written foreign language wrappers for each platform: JavaScript for Desktop, Kotlin for Android, and Swift for iOS.

Since then, we’ve learned some lessons and had to modify our strategy. It turns out that creating hand-written wrappers in multiple languages is a huge time-sink. The wrappers required a significant amount of time to write, but more importantly, they were responsible for many serious bugs.

These bugs were easy to miss, hard to debug, and often led to crashes. One of the largest benefits of Rust is memory safety, but these hand-written wrappers were negating much of that benefit.

To solve this problem, we developed [UniFFI](https://mozilla.github.io/uniffi-rs/): a Rust library for auto-generating foreign language bindings. UniFFI allowed us to create wrappers quickly and safely, but there was one issue: UniFFI supported Kotlin and Swift, but not JavaScript, which powers the Firefox Desktop front-end. UniFFI helped us ship shared components for Firefox Android and iOS, but Desktop remained out of reach.

This changed with Firefox 105 when we added support for generating JavaScript bindings via UniFFI which enabled us to continue pushing forward on our single component vision. This project validated some core concepts that have been in UniFFI from the start but also required us to extend UniFFI in several ways. This blog post will walk through some of the issues that arose along the way and how we handled them.

**Prior Art**

This project has already been tried at least once before at Mozilla. The team was able to get some of the functionality supported, but some parts remained out of reach. One of the first things we realized was that the general approach the previous attempts took would probably not support the UniFFI features we were using in our components.

Does this mean the previous work was a failure? Absolutely not. The team left behind a wonderful trove of design documents, discussions, and code that we made sure to study and steal from. In particular, there was an [ADR](https://adr.github.io/) that discussed different approaches which we studied, as well as a [working C++/WebIDL code](https://github.com/mozilla/uniffi-rs/pull/255) that we repurposed for our project.

**Calling the FFI functions**

UniFFI bindings live on top of an [FFI](https://en.wikipedia.org/wiki/Foreign_function_interface) layer using the C ABI that we call “the scaffolding.” Then the user API is defined on top of the scaffolding layer, in the foreign language. This allows the user API to support features not directly expressible in C and also allows the generated API to feel idiomatic and natural. However, JavaScript complicates this picture because it doesn’t have support for calling C functions. Privileged code in Firefox can use the Mozilla [js-ctypes](http://www.devdoc.net/web/developer.mozilla.org/en-US/docs/js-ctypes.html) library, but its use is deprecated.

The previous project solved this problem by using C++ to call into the scaffolding functions, then leveraged the [Firefox WebIDL code generation tools](https://firefox-source-docs.mozilla.org/dom/webIdlBindings/index.html) to create the JavaScript API. That code generation tool is quite nice and allowed us to define the user API using a combination of [WebIDL](https://developer.mozilla.org/en-US/docs/MDN/Contribute/Howto/Write_an_API_reference/Information_contained_in_a_WebIDL_file) and C++ glue code. However, it was limited and did not support all UniFFI features.

Our team decided to use the same WebIDL code generation tool, but to generate just the scaffolding layer instead of the entire user API. Then we used JavaScript to define the user API on top of that, just like for other languages. We were fairly confident that the code generation tool would no longer be a limiting factor, since the scaffolding layer is designed to be minimalistic and expressible in C.

**Async functions**

The threading model for UniFFI interfaces is not very flexible: all function and method calls are blocking. It’s the caller’s responsibility to ensure that calls don’t block the wrong thread. Typically this means executing UniFFI calls in a thread pool.

The threading model for Firefox frontend JavaScript code is equally inflexible: you must never block the main thread. The main JavaScript thread is responsible for all UI updates and blocking it means an unresponsive browser. Furthermore, the only way to start another thread in JavaScript is using [Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers), but those are not currently used by the frontend code.

To resolve the unstoppable force vs. immovable object situation we found ourselves in, we simply reversed the UniFFI model and made all calls asynchronous. This means that all functions return a [promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) rather than their return value directly.

The “all functions are async” model seems reasonable, at least for the first few projects we intend to use with UniFFI. However, not all functions really need to be async – some are quick enough that they aren’t blocking. Eventually, we plan to add a way for users to customize which functions are blocking and which are async. This will probably happen alongside some general work for async UniFFI, since we’ve found that async execution is an issue for many components using UniFFI.

**How has it been working?**

Since landing UniFFI support in Firefox 105, we’ve slowly started adding some UniFFI’ed Rust components to Firefox. In Firefox 108 we added the Rust remote tabs syncing engine, making it the first component shared by Firefox on all three of our platforms. The new tabs engine uses UniFFI to generate JS bindings on Desktop, Kotlin bindings on Android, and Swift bindings on iOS.

We’ve also been continuing to advance our shared component strategy on Mobile. Firefox iOS has historically lagged behind Android in terms of shared component adoption, but the Firefox iOS 116 release will use our shared sync manager component. This means that both mobile browsers will be using all of the shared components we’ve written so far.

We also use UniFFI to generate bindings for [Glean](https://mozilla.github.io/glean/dev/index.html), a Mozilla telemetry library, which was a bit of an unusual case. Glean doesn’t generate JS bindings; it only generates the scaffolding API, which ends up in the [GeckoView](https://mozilla.github.io/geckoview/) library that powers Firefox Android. Firefox Android can then consume Glean via the generated Kotlin bindings which link to the scaffolding in Geckoview.

If you’re interested in this project or UniFFI in general, please join us in [#uniffi](https://matrix.to/#/#uniffi:mozilla.org) on the Mozilla Matrix chat.