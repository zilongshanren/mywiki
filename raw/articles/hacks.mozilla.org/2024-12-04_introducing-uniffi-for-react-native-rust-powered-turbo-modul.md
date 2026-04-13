---
title: 'Introducing Uniffi for React Native: Rust-Powered Turbo Modules – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2024/12/introducing-uniffi-for-react-native-rust-powered-turbo-modules/
author: Mark Mayo
published: '2024-12-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Today [Mozilla](https://www.mozilla.org/en-US/) and [Filament](https://filament.dm/) are releasing [Uniffi for React Native](https://github.com/jhugman/uniffi-bindgen-react-native), a new tool we’ve been using to build React Native Turbo Modules in Rust, under an open source license. This allows millions of developers writing cross-platform [React Native](https://en.wikipedia.org/wiki/React_Native) apps to use[ Rust ](https://hacks.mozilla.org/2018/12/rust-2018-is-here/) – a modern programming language known for its safety and performance benefits to build single implementations of their app’s core logic to work seamlessly across iOS and Android.

This is a big win for us and for [Filament](https://filament.dm/) who co-developed the library with Mozilla and [James Hugman](https://github.com/jhugman), the lead developer. We think it will be awesome for many other developers too. Less code is good. Memory safety is good. Performance is good. We get all three, plus the joy of using a language we love in more places.

For those familiar with React Native, it’s a great framework for creating cross-platform apps, but it has its challenges. React Native apps rely on a single JavaScript thread, which can slow things down when handling complex tasks. Developers have traditionally worked around this by writing code twice – once for iOS and once for Android – or by using C++, which can be difficult to manage. Uniffi for React Native offers a better solution by enabling developers to offload heavy tasks to Rust, which is now easy to integrate with React Native. As a result, you’ve got faster, smoother apps and a streamlined development process.

## How Uniffi for React Native works

Unifii for React Native is a uniFFI bindings generator for using Rust from React Native via Turbo Modules. It lets us work at an abstraction level high enough to stay focused on our applications’s needs rather than getting lost in the gory technical details of bespoke native cross-platform development It provides tooling to generate:

- Typescript and JSI C++ to call Rust from Typescript and back again
- A Turbo-Module that installs the bindings into a running React Native library.

We’re stoked about this work continuing. In 2020, we started with [Uniffi ](https://mozilla.github.io/uniffi-rs/latest/)as a modern day ‘write once; run anywhere’ toolset for Rust. Uniffi has come a long way since we developed the technology as a bit of a hack to get us a single implementation of Firefox Sync’s core (in Rust) that we could then deploy to both our Android and iOS apps! Since then Mozilla has used [uniffi-rs](https://mozilla.github.io/uniffi-rs/latest/) to successfully deploy Rust in mobile and desktop products used by hundreds of millions of users. This Rust code runs important subsystems such as bookmarks and history sync, Firefox Suggest, telemetry and experimentation. Beyond Mozilla, Uniffi is used in Android (in [AOSP](https://android.googlesource.com/platform/external/rust/crates/uniffi/)), high-profile [security](https://nordsecurity.com/) [products](https://bitwarden.com/) and some [complex](https://dotlottie.io/) [libraries](https://native.live/) familiar to the community.

Currently the Uniffi for React Native project is an early release. We don’t have a cool landing page or examples in the repo (coming!), but open source contributor [Johannes Marbach](https://github.com/johennes) has already been sponsored by [Unomed](https://www.unomed.ch/) to use Uniffi for React Native to create [a React Native Library for the Matrix SDK](https://github.com/unomed-dev/react-native-matrix-sdk) .

Need an idea on how you might give it a whirl? I’ve got two uses that we’re very excited about:

1) Use Rust to offload computationally heavy code to a multi-threaded/memory-safe subsystem to escape single-threaded JS performance bottlenecks in React Native. If you know, you know.

2) Leverage the incredible library of [Rust crates](https://crates.io/) in your React Native app. One of the Filament devs showed how powerful this is, recently. With a rudimentary knowledge of Rust, they were able to find a fast blurhashing library on crates.io to replace a slow Typescript implementation and get it running the same day. We’re hoping we can really improve the tooling even more to make this kind of optimization as easy as possible.

Uniffi represents a step forward in cross-platform development, combining the power of Rust with the flexibility of React Native to unlock new possibilities for app developers.

We’re excited to have the community explore what’s possible. Please check out [the library on Github](https://github.com/jhugman/uniffi-bindgen-react-native) and [jump into the conversation on Matrix](https://matrix.to/#/#uniffi-bindgen-js:matrix.org).

*Disclosure: in addition to this collaboration, **Mozilla Ventures** is an investor in Filament. *


## About Mark Mayo

Technologist at Mozilla Innovations

## About Tony Haile

CEO at Filament