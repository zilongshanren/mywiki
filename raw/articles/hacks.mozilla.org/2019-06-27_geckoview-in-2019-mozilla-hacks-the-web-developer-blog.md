---
title: GeckoView in 2019 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/06/geckoview-in-2019/
author: Dan Callahan
published: '2019-06-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![GeckoView Logo of GeckoView](../../assets/728221b83be0d4ea.png)

[using GeckoView](https://hacks.mozilla.org/2018/09/focus-with-geckoview/) to bring Firefox’s rendering engine to Android as a reusable library. By decoupling the Gecko engine from the Firefox application, we’ve created a newer, faster, and more maintainable way to create Android applications. This approach leverages Gecko’s excellent performance, privacy, and support for cutting-edge web standards.

With today’s release of our GeckoView-powered Firefox Preview, we’d like to share an update on what we’ve accomplished and where GeckoView is going in 2019.

## Introducing Firefox Preview

We’re excited to announce today’s ![Wordmark of Firefox Preview](../../assets/9a864b48a4adf449.png)


[initial release of Firefox Preview](https://app.adjust.com/n9x7nra)(

[GitHub](https://github.com/mozilla-mobile/fenix)), an entire browser built from the ground up with

[GeckoView](https://mozilla.github.io/geckoview/)and

[Mozilla Android Components](https://github.com/mozilla-mobile/android-components)at its core. Though still an early preview, this is our first end-user product built completely with these new technologies.

Firefox Preview is our platform for building, testing, and delivering unique features. We’ll use it to explore new concepts for how mobile browsers should look and feel. We encourage you to [give it a try](https://app.adjust.com/n9x7nra)!

## Other Projects using GeckoView

But that is not all — Mozilla is using GeckoView in many other products as well:

### Firefox Focus

![Firefox Focus Logo of Firefox Focus](../../assets/3b05088f45699607.png)

[Firefox Focus](https://github.com/mozilla-mobile/focus-android) has been our most prominent consumer of GeckoView. Focus’s simplicity lends itself to experimentation. Currently we’re using Focus to split test between GeckoView and Android’s built-in WebView. This helps us ensure that GeckoView’s performance and stability meet or exceed expectations set by Android’s platform libraries.

While Focus is great at what it does, it is not a general purpose browser. By design, Focus does not keep track of history or bookmarks, nor does it support APIs like WebRTC. Yet we need a place to test those features to ensure that GeckoView is sufficiently robust and capable of building fully-featured browsers. That’s where Reference Browser comes in.

### Reference Browser

![Reference Browser Logo of Reference Browser](../../assets/68e289618968d779.png)

[Reference Browser](https://github.com/mozilla-mobile/reference-browser) is a full browser built with GeckoView and Mozilla Android Components, but crucially, *it is not an end-user product*. Its intended audience is browser developers. Indeed, Reference Browser is a proving ground where we validate that GeckoView and the Components fit together and work as expected. We gain the ability to develop our core libraries without the constraints of an in-market product.

### Firefox Reality

![Firefox Reality Logo of Firefox Reality](../../assets/ed76fd6b804b51e3.png)

[Firefox Reality](https://mixedreality.mozilla.org/firefox-reality/), a browser designed for standalone virtual reality headsets. In addition to leveraging Gecko’s excellent support for immersive web technologies, Firefox Reality demonstrates GeckoView’s versatility. The same library that’s at the heart of “traditional” browsers like Focus and Firefox Preview can also power experiences in an entirely different medium.

### Firefox for Android

![Firefox for Android Logo of Firefox](../../assets/e266b528c6fd3a32.png)

[Firefox for Android](https://www.mozilla.org/firefox/mobile/) (“Fennec”) does not use GeckoView for normal browsing, it *does* use it to support Progressive Web Apps and Custom Tabs. Moreover, because GeckoView and Fennec are both based on Gecko, they jointly benefit from improvements to that common infrastructure.

GeckoView is the foundation of Mozilla’s next generation of mobile products. To better support that future, we’ve halted new feature development on Focus while we concentrate on refining GeckoView and prepare for the launch of Firefox Preview. If you’re interested in supporting Focus in the future, please help by filling out [this survey](https://www.surveygizmo.com/s3/5022894/Firefox-Focus-Survey).

## Internals

Aside from product development, the past six months have seen many improvements to GeckoView’s internals, especially around compiler-level optimizations and support for additional CPU architectures. Highlights include:

- Profile-Guided Optimization (
[PGO](https://en.wikipedia.org/wiki/Profile-guided_optimization)) on Android is[now enabled](https://bugzilla.mozilla.org/show_bug.cgi?id=632954), which allows the compiler to generate more efficient code by considering data gathered by actually running and observing GeckoView. - The
[IonMonkey](https://wiki.mozilla.org/IonMonkey)JavaScript JIT compiler is[now enabled](https://bugzilla.mozilla.org/show_bug.cgi?id=1536220)for 64-bit ARM builds of GeckoView. - We’re now producing builds of GeckoView for the x86_64 architecture.

In addition to meeting [Google’s upcoming requirements](https://android-developers.googleblog.com/2017/12/improving-app-security-and-performance.html) for listing in the Play Store, supporting 64-bit architectures further improves GeckoView’s stability (fewer out-of-memory crashes) and security.

For upcoming releases, we’re working on support for web push and “add to home screen,” among other things.

## Get involved

GeckoView isn’t just for Mozilla, we want it to be useful to you.

Thanks to Emily Toop for new work on the [GeckoView Documentation](https://mozilla.github.io/geckoview/) website. It’s easier than ever to get started, either as an app developer using GeckoView or as a GeckoView contributor. If you spot something that could be better documented, [pull requests](https://github.com/mozilla/geckoview/) are always welcome.

![Firefox for Android, Firefox Focus, Firefox Reality, Reference Browser, and Firefox Preview Logos of all GeckoView-powered projects](../../assets/855f69127a82ad6c.png)


We’d also love to help you directly. If you need assistance with anything GeckoView-related, you can find us:

- in the
[#mobile](ircs://irc.mozilla.org:6697/#mobile)channel of[Mozilla’s IRC server](https://wiki.mozilla.org/Irc), or - on the
[mobile-firefox-dev](https://mail.mozilla.org/listinfo/mobile-firefox-dev)mailing list, or - at
[@geckoview](https://twitter.com/geckoview)on Twitter.

Please do reach out with any questions or comments.

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 5 comments

todd parrishJuly 6th, 2019 at 19:50Alexandre LeducJuly 11th, 2019 at 04:41Dan CallahanJuly 12th, 2019 at 05:19Andrew VickersJuly 18th, 2019 at 19:13Dan CallahanJuly 19th, 2019 at 05:46