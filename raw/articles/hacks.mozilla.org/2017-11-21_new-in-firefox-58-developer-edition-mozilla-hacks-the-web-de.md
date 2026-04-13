---
title: 'New in Firefox 58: Developer Edition – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2017/11/new-in-firefox-58-developer-edition/
author: Dan Callahan
published: '2017-11-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox Quantum [made Firefox fast again](https://hacks.mozilla.org/2017/11/entering-the-quantum-era-how-firefox-got-fast-again-and-where-its-going-to-get-faster/), but speed is only part of the story. A ton of work has gone into making Firefox an exceptional tool for *creating* on the Web. Let’s dive into the changes coming in Firefox 58, currently available to preview in [Firefox Developer Edition](https://www.mozilla.org/firefox/developer/).

## More Control for CSS Authors

Following the success of Firefox’s powerful [CSS Grid Inspector](https://hacks.mozilla.org/2017/06/new-css-grid-layout-panel-in-firefox-nightly/), we’re excited to introduce a [Shape Path Editor](https://developer.mozilla.org/docs/Tools/Page_Inspector/How_to/Edit_CSS_shapes) for elements with a [ clip-path](https://developer.mozilla.org/docs/Web/CSS/clip-path) property.

Try it yourself on [this CodePen](https://codepen.io/chriscoyier/pen/wBKPOm) by Chris Coyier.

We’ve also implemented the CSS [ font-display](https://developer.mozilla.org/docs/Web/CSS/@font-face/font-display) property, allowing authors to specify how long the browser should wait for a web font, and when it should consider swapping in a font once it’s loaded.

Firefox Quantum also introduced [a brand new CSS engine](https://hacks.mozilla.org/2017/08/inside-a-super-fast-css-engine-quantum-css-aka-stylo/) (“Quantum CSS”) which fixed numerous [bugs and inconsistencies](https://developer.mozilla.org/en-US/Firefox/Releases/57#Quantum_CSS_notes) with CSS in Firefox. For example, [ calc()](https://developer.mozilla.org/docs/Web/CSS/calc) now works everywhere that the spec says it should.

## An Even Better Debugger

Piece by piece, we’ve been [rewriting our developer tools](https://hacks.mozilla.org/2016/09/introducing-debugger-html/) in standard Web technologies. In Developer Edition, the Console, Debugger, Network Monitor, and Responsive Design Mode are all implemented in plain HTML, JavaScript, and CSS atop common libraries like React and Redux. This means that you can use your existing web development skills to hack on the DevTools. The source for [debugger.html is on GitHub](https://github.com/firefox-devtools/debugger.html), and we do our best to tag [good first bugs](https://github.com/firefox-devtools/debugger.html/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22) and mentor new contributors.

We’ve implemented [tons of new features](https://hacks.mozilla.org/2017/09/developer-edition-devtools-update-now-with-photon-ui/) during the rewrite, but the debugger deserves special mention. First, source maps finally work everywhere, and even include proper syntax highlighting for markup like JSX:

You might also notice that the debugger recognized Webpack, and appropriately labeled it in the Sources tree.![Screenshot of the Debugger showing JSX syntax highlighting for a React component](../../assets/20d108a04da545fd.png)


Similarly, the debugger can recognize two dozen common JavaScript libraries and group their stack frames in the call stack. This makes it easy to separate the code you wrote from code provided by a framework when you’re tracking down a bug:

We even implemented “sticky” breakpoints that intelligently move with your code when you refactor or rearrange declarations in a file.![Screenshot showing the call stack in the Debugger. Instead of one undifferentiated list, the new Debugger has grouped the stack frames by library, showing React calling Redux calling Lodash.](../../assets/af84ee140771f8ba.png)


The other tools have also improved: [console groups](https://developer.mozilla.org/en-US/docs/Web/API/console#Using_groups_in_the_console) can now be collapsed, the network monitor [can be paused](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor#Pausing_and_resume_network_traffic_recording), etc.

The best way to discover the new DevTools is to [download Developer Edition](https://www.mozilla.org/firefox/developer/) and try them yourself.

## WebVR, FLAC, and Other Tidbits

Firefox is driving new, fundamental capabilities of the Web. Firefox 55 [introduced support for WebVR](https://hacks.mozilla.org/2017/08/firefox-55-supports-webvr/) on Windows, and included [experimental support for macOS](https://hacks.mozilla.org/2017/06/announcing-webvr-on-mac/). With Firefox 58, WebVR now is supported by default on both Windows and macOS.

If you’re interested in creating virtual reality experiences on the Web, check out the [A-Frame](https://aframe.io/) library, or read our article on [how Firefox Quantum delivers smooth WebVR performance](https://hacks.mozilla.org/2017/11/a-super-stable-webvr-user-experience-thanks-to-firefox-quantum/) at 90 fps.

In other firsts, Firefox 51 was the first browser to support [FLAC](https://xiph.org/flac/), a lossless audio format, on the Web. Until now, this support was limited to Firefox on desktop platforms (Windows, macOS, and Linux), but Firefox 58 brings FLAC support to Android. That means that Firefox, Chrome, and Edge [all support FLAC](https://caniuse.com/#feat=flac) on every platform but iOS.

We also landed a few changes to help measure and improve Firefox’s performance:

- The
provides access to performance metrics related to page loading.`PerformanceNavigationTiming`

API - Off Main Thread Painting (“OMTP”) has been enabled by default on Windows, which improves Firefox’s responsiveness by reducing the workload on the main thread.
- We’ve enabled
[budget-based background timeout throttling](https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API#Policies_in_place_to_aid_background_page_performance)which slows down scripts running in background tabs to save further CPU resources.

Lastly, Content Security Policies (CSPs) now support the [ worker-src](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/worker-src) directive.

## WebExtension API Additions

Firefox Quantum removed support for legacy add-ons and added dozens of [new WebExtension APIs](https://developer.mozilla.org/en-US/Firefox/Releases/57#WebExtensions). Firefox 58 adds [even more APIs](https://blog.mozilla.org/addons/2017/11/20/extensions-in-firefox-58/), including ones to:

- Access brand new
[website privacy](https://developer.mozilla.org/Add-ons/WebExtensions/API/privacy/websites)controls like first-party isolation and[fingerprinting resistance](https://wiki.mozilla.org/Security/Fingerprinting), added as part of the ongoing[Tor Uplift](https://wiki.mozilla.org/Security/Tor_Uplift). [Toggle](https://developer.mozilla.org/Add-ons/WebExtensions/API/tabs/toggleReaderMode), observe, and control whether or not a tab is displayed in[Reader Mode](https://support.mozilla.org/kb/firefox-reader-view-clutter-free-web-pages).[Query](https://developer.mozilla.org/Add-ons/WebExtensions/API/theme/getCurrent)and[observe changes](https://developer.mozilla.org/Add-ons/WebExtensions/API/theme/onUpdated)to the browser theme, making it possible for add-ons to adapt themselves to fit in with arbitrary themes.

For example, [Tree Style Tab](https://addons.mozilla.org/firefox/addon/tree-style-tab/) can now adopt theme colors from WebExtensions like [VivaldiFox](https://addons.mozilla.org/firefox/addon/vivaldifox/):

![Animated screenshot of Tree Style Tab adopting dynamic theme colors from VivaldiFox](../../assets/c16cb6787c24806e.gif)


We’re currently planning additional WebExtension capabilities for 2018, including looking into possibilities for [hiding individual tabs, or the entire tab bar](https://wiki.mozilla.org/WebExtensions/TabHiding).

## Wrapping Up

These are just the highlights. To learn more about what to expect in Firefox 58—currently available in [Beta](https://www.mozilla.org/firefox/channel/desktop/#beta) and [Developer Edition](https://www.mozilla.org/firefox/developer)—check out the [Release Notes](https://www.mozilla.org/firefox/58.0beta/releasenotes/) and MDN’s [Firefox 58 for Developers](https://developer.mozilla.org/Firefox/Releases/58).

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 41 comments

JimNovember 21st, 2017 at 14:05Dan CallahanNovember 22nd, 2017 at 16:21RSNovember 21st, 2017 at 16:07Dan CallahanNovember 22nd, 2017 at 16:23JamesNovember 30th, 2017 at 05:50Robert AbNovember 21st, 2017 at 22:29Dan CallahanNovember 22nd, 2017 at 16:33Robert AbNovember 22nd, 2017 at 16:55Sahriar SykatNovember 21st, 2017 at 23:00Dan CallahanNovember 22nd, 2017 at 16:34Andrew de RidderNovember 22nd, 2017 at 05:06Dan CallahanNovember 22nd, 2017 at 16:10AngryPenguinNovember 22nd, 2017 at 06:59Roger H ThomasNovember 22nd, 2017 at 08:50Dan CallahanNovember 22nd, 2017 at 16:18Daniel Lo NigroNovember 22nd, 2017 at 09:35Dan CallahanNovember 22nd, 2017 at 16:35KeesNovember 22nd, 2017 at 12:17Dan CallahanNovember 22nd, 2017 at 16:39MichaelNovember 28th, 2017 at 23:44pjsNovember 22nd, 2017 at 17:05Patrik ÄNovember 23rd, 2017 at 01:21Magic JohnsonNovember 23rd, 2017 at 08:11BernieNovember 24th, 2017 at 11:31Jesús CeaNovember 24th, 2017 at 17:37RichardNovember 24th, 2017 at 21:09AlfonzNovember 24th, 2017 at 23:05JkeksNovember 26th, 2017 at 09:49AlexNovember 26th, 2017 at 10:03daveNovember 27th, 2017 at 08:42Gy. OwenNovember 27th, 2017 at 11:31SaraNovember 27th, 2017 at 12:41AndreaNovember 28th, 2017 at 09:44Matt SmartNovember 29th, 2017 at 04:33RickNovember 29th, 2017 at 04:37Rob TNovember 29th, 2017 at 07:12voidpointerNovember 29th, 2017 at 11:55KonstantinNovember 29th, 2017 at 16:05rane58November 30th, 2017 at 09:16Martin GrayNovember 30th, 2017 at 11:12Judev5762November 30th, 2017 at 12:31