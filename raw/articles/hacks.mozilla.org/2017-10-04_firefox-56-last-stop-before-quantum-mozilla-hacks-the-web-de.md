---
title: 'Firefox 56: Last Stop before Quantum – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2017/10/firefox-56-last-stop-before-quantum/
author: Dan Callahan
published: '2017-10-04'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Here at Mozilla, we’re extremely excited about next month’s release of [Firefox Quantum](https://www.mozilla.org/en-US/firefox/quantum/) ([preview it today](https://hacks.mozilla.org/2017/09/firefox-quantum-developer-edition-fastest-firefox-ever/) in [Developer Edition](https://mozilla.org/firefox/developer)!) which brings massive speed improvements, a brand new UI, and several new or improved Developer Tools.

But that’s next month. What about last week’s release of Firefox 56?

## Browser Features

For users, Firefox 56 sports two major changes:

First, [Firefox Screenshots](https://screenshots.firefox.com/) is a brand new, built-in tool for capturing and (optionally) sharing images of web pages. The tool makes it easy to select regions of the page based on the underlying DOM structure, though both full-page and free-form screenshots are also available.

Of course, the Developer Tools retain their own [screenshot capabilities](https://developer.mozilla.org/en-US/docs/Tools/Taking_screenshots). For example, you can right-click on any node in the Inspector to capture a screenshot of that node, or you can use the `screenshot`

command in the [Developer Toolbar](https://developer.mozilla.org/en-US/docs/Tools/GCLI).

Second, Firefox is now 64-bit by default on all operating systems, and existing 32-bit installations will automatically upgrade to 64-bit builds if supported by the underlying hardware.

## What’s New for Developers

For developers, Firefox now supports [“headless” mode](https://developer.mozilla.org/en-US/Firefox/Headless_mode) on all operating systems, which makes it possible to run Firefox without actually displaying a window on the screen. This is remarkably useful for automated testing, both during local development and as part of a continuous integration (CI) pipeline.

We’ve also put an enormous amount of effort into Firefox’s Developer Tools. You can read all about the current and upcoming features in [Julian Descottes’s article](https://hacks.mozilla.org/2017/09/developer-edition-devtools-update-now-with-photon-ui/), but we’re especially proud of our completely new debugger: as part of the “[devtools.html](https://github.com/firefox-devtools)” project, we completely rewrote the debugger as a modern web application, powered by React / Redux, and using standard HTML, JavaScript, and CSS.

You can find the source code for the debugger on [GitHub](https://github.com/firefox-devtools/debugger.html).

## Bidding Farewell to Legacy Add-Ons

Finally, Firefox 56 is the last release to support [legacy APIs](https://developer.mozilla.org/en-US/Add-ons/Legacy_add_ons) for add-ons. In their place we’ve created “[WebExtensions](https://developer.mozilla.org/en-US/Add-ons/WebExtensions),” a set of cross-browser extension APIs that we hope to standardize at the W3C. Since many WebExtension APIs are compatible with Chrome, Edge, and Opera, popular add-ons from other browsers (like the [Vue.js DevTools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)) can run on Firefox without significant modification.

Unfortunately, the impending removal of old APIs with next month’s general release of Firefox Quantum will necessarily end support for several legacy add-ons. For example, the new APIs do not offer the degree of UI modification necessary to support [Classic Theme Restorer](https://addons.mozilla.org/en-US/firefox/addon/classicthemerestorer/). However, nearly 5,000 add-ons are [already available using the new APIs](https://addons.mozilla.org/en-US/firefox/tag/firefox57), including [Tree Style Tab](https://addons.mozilla.org/en-US/firefox/addon/tree-style-tab/?src=search), [Tab Center Redux](https://addons.mozilla.org/en-US/firefox/addon/tab-center-redux/), and [uBlock Origin](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/). The APIs themselves are also still being developed and expanded, so expect to see greater capabilities with each release of Firefox.

In most cases, the upgrade to Firefox Quantum will be painless. Most popular add-ons will update to the new APIs before the release of Firefox Quantum, and Firefox will suggest replacements inside `about:addons`

for those that don’t.

If you’ve ever built a Chrome extension, consider [porting it from Chrome](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Porting_a_Google_Chrome_extension) with the help of our [ExtensionTest.com](https://www.extensiontest.com) and `<a href="https://github.com/mozilla/web-ext">web-ext</a>`

tools. In most cases your Chrome browser extension will run in Firefox or Microsoft Edge with just a few changes. Let us know how it goes. If you have ideas or questions, you can contact the team on the [dev-addons mailing list](https://mail.mozilla.org/listinfo/dev-addons) or #extdev on IRC.

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 51 comments

jxnOctober 4th, 2017 at 09:36Dan CallahanOctober 4th, 2017 at 09:54MelchiorOctober 12th, 2017 at 10:34Camden NarztOctober 4th, 2017 at 10:45Dan CallahanOctober 4th, 2017 at 21:41Camden NarztOctober 5th, 2017 at 10:34Marcin W. DąbrowskiOctober 6th, 2017 at 10:24DuminduOctober 4th, 2017 at 11:35Dan CallahanOctober 4th, 2017 at 21:33AlbertOctober 6th, 2017 at 18:45DmitryOctober 4th, 2017 at 14:30Dan CallahanOctober 4th, 2017 at 21:29xn7October 4th, 2017 at 23:40Dan CallahanOctober 7th, 2017 at 11:43njnOctober 4th, 2017 at 21:10Álvaro GonzálezOctober 5th, 2017 at 01:07Dan CallahanOctober 7th, 2017 at 11:45Álvaro GonzálezOctober 12th, 2017 at 01:01Álvaro GonzálezOctober 12th, 2017 at 01:05KinneOctober 5th, 2017 at 01:11MarkOctober 6th, 2017 at 08:05Mr. CleanOctober 5th, 2017 at 08:08PrashantOctober 5th, 2017 at 11:56CatmatoOctober 13th, 2017 at 02:03Lorenzo GattiOctober 6th, 2017 at 03:08BrankoOctober 6th, 2017 at 07:44Dan CallahanOctober 7th, 2017 at 12:02TimOctober 6th, 2017 at 08:09Dan CallahanOctober 7th, 2017 at 12:04Michael CarperOctober 6th, 2017 at 08:11Dan CallahanOctober 7th, 2017 at 12:05erickOctober 6th, 2017 at 08:28Dan CallahanOctober 7th, 2017 at 12:07TiredOctober 6th, 2017 at 09:08Alex BOctober 6th, 2017 at 09:45Dan CallahanOctober 7th, 2017 at 12:12Alex BOctober 8th, 2017 at 08:55dddOctober 6th, 2017 at 18:08Dan CallahanOctober 7th, 2017 at 12:15AndrewOctober 6th, 2017 at 18:37Dan CallahanOctober 7th, 2017 at 12:27KonstantinOctober 9th, 2017 at 17:32FOctober 8th, 2017 at 09:10KonstantinOctober 8th, 2017 at 20:21MegamanOctober 9th, 2017 at 20:27bytemeOctober 10th, 2017 at 12:07EdiOctober 11th, 2017 at 01:15EllisOctober 11th, 2017 at 14:24subramaniamOctober 12th, 2017 at 13:07Vladamir DvorakOctober 13th, 2017 at 04:32Hal NewmanOctober 13th, 2017 at 10:09