---
title: Firefox Focus with GeckoView – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/09/focus-with-geckoview/
author: Dan Callahan
published: '2018-09-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Firefox Focus](https://www.mozilla.org/firefox/mobile/#focus) is private browsing as an app: It automatically blocks ads and trackers, so you can surf the web in peace. When you’re done, a single tap completely erases your history, cookies, and other local data.

Protecting you from invasive tracking is part of Mozilla’s non-profit mission, and Focus’s built-in tracking protection helps keep you safe. It also makes websites load faster!

With Focus, you don’t have to worry about your browsing history coming back to haunt you in [retargeted](https://www.adroll.com/learn-more/retargeting) ads on other websites.

## Bringing Gecko to Focus

In the next weeks, we’ll release a new version of [Focus for Android](https://www.mozilla.org/firefox/mobile/#focus), and for the first time, Focus will come bundled with Gecko, the browser engine that powers [Firefox Quantum](https://www.mozilla.org/firefox/new/). This is a major architectural change, so while every copy of Focus will *include* Gecko—hence the larger download size—we plan on *enabling* it gradually to ensure a smooth transition. You can help us test Gecko in Focus today by installing the [Focus Beta](https://github.com/mozilla-mobile/focus-android/wiki/Release-tracks).

*Note: At time of publishing, Focus Beta is conducting an A/B test between the old and new engines. Look for “ Gecko/62.0” in your User-Agent String to determine if your copy is using Gecko or not.*

Up until this point, Focus has been powered exclusively by Android’s built-in WebView. This made sense for initial development, since WebView was already on every Android device, but we quickly ran into limitations. Foremost, it isn’t designed for building browsers. Despite being based on Chromium, WebView only supports a subset of web standards, as Google expects app developers to use native Android APIs, and not the Web, for advanced functionality. Instead, we’d prefer if apps had access to the entirety of the open, standards-based web platform.

In Focus’s case, we can only build [next-generation privacy features](https://blog.mozilla.org/futurereleases/2018/08/30/changing-our-approach-to-anti-tracking/) if we have deep access to the browser internals, and that means we need our own engine. We need Gecko. Fortunately, Firefox for Android already uses Gecko, just not in a way that’s easy to reuse in other applications. That’s where GeckoView comes in.

## GeckoView: Making Gecko Reusable

GeckoView is Gecko packaged as a reusable Android library. We’ve worked to decouple the engine itself from its user interface, and made it easy to embed in other applications. Thanks to GeckoView’s clean architecture, our initial benchmarks of the new Focus show a median page load improvement of 20% compared to Firefox for Android, making GeckoView our fastest version of Gecko on Android yet.

We first put GeckoView into production last year, powering both [Progressive Web Apps](https://developer.mozilla.org/en-US/docs/Web/Apps/Progressive) (PWAs) and [Custom Tabs](https://developer.chrome.com/multidevice/android/customtabs) in Firefox for Android. These minimal, self-contained features were good initial projects, but with Focus we’re going much further. Focus will be our first time using GeckoView to completely power an existing, successful, and standalone product.

We’re also using GeckoView in entirely new products like [Firefox Reality](https://blog.mozvr.com/firefox-reality-bringing-the-immersive-web-to-mixed-reality-headsets/), a browser designed exclusively for virtual and augmented reality headsets. We’ll be sharing more about it later this year.

## Building Browsers with Android Components

To build a web browser, you need more than just an engine. You also need common functionality like tabs, auto-complete, search suggestions, and so on. To avoid unnecessary duplication of effort, we’ve also created [Android Components](https://github.com/mozilla-mobile/android-components), a collection of independent, ready-to-use libraries for building browsers and browser-like applications on Android.

For Mozilla, GeckoView means we can leverage all of our Firefox expertise in building more compelling, safe, and robust online experiences, while Android Components ensures that we can continue experimenting with new projects (like Focus and Firefox Reality) without reinventing wheels. In many ways, these projects set the stage for the next generation of the Firefox family of browsers on Android.

For Android developers, GeckoView means control. It’s a production-grade engine with a [stable and expansive API](https://mozilla.github.io/geckoview/javadoc/mozilla-central/), usable either on its own or through Android Components. Because GeckoView is a self-contained library, you don’t have to compile it yourself. Furthermore, powering your app with GeckoView gives you a specific web engine version you can work with. Compare that to WebView, which tends to have quite a bit of variance between versions depending on the OS and Chrome version available on the device. With GeckoView, you always know what you’re getting — and you benefit from Gecko’s excellent, cross-platform support for web standards.

## Get Involved

We’re really excited about what GeckoView means for the future of browsers on Android, and we’d love for you to get involved:

- Consider installing the
[Focus Beta](https://github.com/mozilla-mobile/focus-android/wiki/Release-tracks)and[reporting any issues](https://github.com/mozilla-mobile/focus-android/issues)you find. - If you’re a Web Developer,
*start testing your mobile experience in Gecko*, either via[Focus Beta](https://github.com/mozilla-mobile/focus-android/wiki/Release-tracks),[Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox), or Firefox’s built-in[responsive design mode](https://developer.mozilla.org/en-US/docs/Tools/Responsive_Design_Mode). - If you’re an Android Developer, consider
[GeckoView](https://wiki.mozilla.org/Mobile/GeckoView)for your next project, or contribute directly by helping us[fix bugs in Focus](https://github.com/mozilla-mobile/focus-android/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22)and[Components](https://github.com/mozilla-mobile/android-components/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22).

Let us know what you think of GeckoView and the new Focus in the comments below!

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 10 comments

PhistucKSeptember 13th, 2018 at 11:03Dan CallahanSeptember 13th, 2018 at 14:03Colin LeeSeptember 13th, 2018 at 18:39JensSeptember 13th, 2018 at 11:07Dan CallahanSeptember 13th, 2018 at 14:32Christopher AnthonySeptember 13th, 2018 at 13:57Dan CallahanSeptember 13th, 2018 at 14:10NavSeptember 13th, 2018 at 14:16Dan CallahanSeptember 13th, 2018 at 14:53Andreas BovensSeptember 17th, 2018 at 04:35